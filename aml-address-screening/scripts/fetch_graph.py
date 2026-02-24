"""
fetch_graph.py - A lightweight script to interact with the TrustIn API and retrieve
the raw transaction graph data for a given blockchain address.

This script does NOT perform rule evaluation. It only fetches the data and saves it
to a JSON file for downstream LLM or system consumption.
"""
import os
import json
import argparse
from typing import Dict
from datetime import datetime

from trustin_api import TrustInAPI

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def fetch_graph(chain: str, address: str, direction: str = "inflow", inflow_hops: int = 3, outflow_hops: int = 3, api_key: str = None) -> Dict:
    """Fetches graph data for an address using TrustInAPI."""
    start_time = datetime.now()
        
    try:
        api = TrustInAPI(api_key=api_key)
        # TrustIn API automatically uses async_detect underneath
        result = api.kya_pro_detect(chain, address, inflow_hops=inflow_hops, outflow_hops=outflow_hops)
        
        # Package the raw graph details returned by the API
        response = {
            "chain": chain,
            "address": address,
            "direction": direction,
            "hops_requested": {
                "inflow": inflow_hops,
                "outflow": outflow_hops
            },
            "timestamp": datetime.now().isoformat(),
            "execution_time": str(datetime.now() - start_time),
            "graph_data": result.details # The raw parsed JSON graph
        }
        return response
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch graph: {str(e)}")
        import traceback
        traceback.print_exc()
        return {}

def main():
    parser = argparse.ArgumentParser(description="Fetch TrustIn raw graph data.")
    parser.add_argument("chain", help="Blockchain network (e.g., Tron, Ethereum)")
    parser.add_argument("address", help="Wallet address to investigate")
    parser.add_argument("--direction", choices=["inflow", "outflow", "all"], default="inflow", help="Trace direction")
    parser.add_argument("--inflow-hops", type=int, default=3, help="Inflow depth (default: 3)")
    parser.add_argument("--outflow-hops", type=int, default=3, help="Outflow depth (default: 3)")
    parser.add_argument("--api-key", help="TrustIn API Key (optional if in env)")
    
    args = parser.parse_args()
    
    print(f"📡 Fetching Graph for {args.chain} - {args.address}...")
    print(f"   Direction: {args.direction.upper()} | Inflow: {args.inflow_hops} hops | Outflow: {args.outflow_hops} hops")
    
    result = fetch_graph(
        chain=args.chain,
        address=args.address,
        direction=args.direction,
        inflow_hops=args.inflow_hops,
        outflow_hops=args.outflow_hops,
        api_key=args.api_key
    )
    
    if result and result.get("graph_data"):
        # Create directories in the current working directory
        reports_dir = os.path.join(os.getcwd(), "reports")
        graph_dir = os.path.join(os.getcwd(), "graph_data")
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(graph_dir, exist_ok=True)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join(graph_dir, f"raw_graph_{args.address}_{timestamp_str}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        print(f"\n✅ SUCCESS: Raw Graph JSON saved to: {json_path}")
        print(f"👉 Now hand over to the LLM Agent to evaluate against rules.json!")
    else:
        print("\n❌ FAILED: Could not retrieve graph data.")
        exit(1)

if __name__ == "__main__":
    main()
