#!/usr/bin/env python3
"""
run_screening.py
----------------
Orchestrates the full AML address-screening pipeline:
1. Fetches raw graph via TrustIn API (up to 5 hops).
2. Extracts risk-relevant paths (1 to 5 hops) by cross-referencing rules.json.
3. Provides instructions for the final LLM report generation.
"""

import argparse
import subprocess
import os
import json
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Run full AML screening pipeline (Fetch -> Extract).")
    parser.add_argument("chain", help="Blockchain network (e.g., Tron, Ethereum)")
    parser.add_argument("address", help="Address to investigate")
    parser.add_argument("--direction", choices=["inflow", "outflow", "all"], default="inflow", help="Trace direction")
    parser.add_argument("--inflow-hops", type=int, default=3, help="Inflow hop depth")
    parser.add_argument("--outflow-hops", type=int, default=3, help="Outflow hop depth")
    parser.add_argument("--max-nodes", type=int, default=100, help="Max nodes per hop")
    parser.add_argument("--min-timestamp", type=int, help="Min timestamp (ms)")
    parser.add_argument("--max-timestamp", type=int, help="Max timestamp (ms)")
    parser.add_argument("--rules-config", default=os.path.join(os.getcwd(), "rules.json"), help="Path to rules.json")
    parser.add_argument("--max-depth", type=int, help="Deprecated (use --inflow-hops/--outflow-hops)")
    args = parser.parse_args()
    
    # Handle legacy --max-depth
    if args.max_depth is not None:
        inflow = outflow = args.max_depth
    else:
        inflow = args.inflow_hops
        outflow = args.outflow_hops

    print("\n" + "="*50)
    print(f"🚀 [STEP 1/3] Fetching Raw Graph (Max Depth: {args.max_depth})")
    print("="*50)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fetch_script = os.path.join(script_dir, "fetch_graph.py")
    
    fetch_cmd = [
        "python3", fetch_script,
        args.chain, args.address,
        "--direction", args.direction,
        "--inflow-hops", str(inflow),
        "--outflow-hops", str(outflow),
        "--max-nodes", str(args.max_nodes)
    ]
    if args.min_timestamp:
        fetch_cmd.extend(["--min-timestamp", str(args.min_timestamp)])
    if args.max_timestamp:
        fetch_cmd.extend(["--max-timestamp", str(args.max_timestamp)])
    
    try:
        subprocess.run(fetch_cmd, check=True)
    except subprocess.CalledProcessError:
        print("❌ FAILED: API extraction aborted.")
        sys.exit(1)

    # Locate the most recently generated raw graph file
    graph_dir = os.path.join(os.getcwd(), "graph_data")
    if not os.path.exists(graph_dir):
        print("❌ FAILED: Directory graph_data/ not found.")
        sys.exit(1)
        
    raw_files = sorted([f for f in os.listdir(graph_dir) if f.startswith(f"raw_graph_{args.address}_") and f.endswith(".json")])
    if not raw_files:
        print("❌ FAILED: Could not find newly generated raw graph file.")
        sys.exit(1)
        
    raw_path = os.path.join(graph_dir, raw_files[-1])
    
    print("\n" + "="*50)
    print(f"🕵️‍♂️ [STEP 2/3] Extracting Risk Paths (Layers 1 through {args.max_depth})")
    print("="*50)
    
    extract_script = os.path.join(script_dir, "extract_risk_paths.py")
    rules_path = args.rules_config
    
    if not os.path.exists(rules_path):
        print(f"❌ FAILED: rules.json not found at {rules_path}. Please run aml-rule-generator first.")
        sys.exit(1)

    extract_cmd = [
        "python3", extract_script,
        "--graph", raw_path,
        "--rules", rules_path,
        "--max-depth", str(max(inflow, outflow))
    ]
    
    try:
        result = subprocess.run(extract_cmd, capture_output=True, text=True, check=True)
        # Parse output from extract_risk_paths.py
        for line in result.stdout.split('\n'):
            if line.startswith('{"status": "success"'):
                out_data = json.loads(line)
                risk_path_file = out_data["output"]
                path_count = out_data["count"]
                print(f"✅ Extracted {path_count} specific risk paths matching rules.json.")
                break
        else:
            print("⚠️ Warning: Could not parse exact path count, but extraction completed.")
            # Fallback path finding
            risk_files = sorted([f for f in os.listdir(graph_dir) if f.startswith(f"risk_paths_{args.address}_") and f.endswith(".json")])
            risk_path_file = os.path.join(graph_dir, risk_files[-1]) if risk_files else "UNKNOWN"
            
    except subprocess.CalledProcessError as e:
        print("❌ FAILED: Python extraction failed.")
        print(e.stderr)
        sys.exit(1)

    print("\n" + "="*50)
    print(f"🤖 [STEP 3/3] AI Agent Evaluation Handoff")
    print("="*50)
    print("Data extraction is complete! The risk data has been heavily condensed to prevent LLM hallucination and context-loss.")
    print(f"\n👉 NEXT STEP FOR AI AGENT:")
    print(f"1. Read the parsed risk evidence: `{risk_path_file}`")
    print(f"2. Read the rule framework: `{rules_path}`")
    print(f"3. Strictly follow instructions in `prompts/evaluation_prompt.md` to write the final Markdown report.")

if __name__ == "__main__":
    main()
