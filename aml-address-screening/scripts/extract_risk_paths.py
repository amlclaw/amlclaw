#!/usr/bin/env python3
"""
extract_risk_paths.py
--------------------
Utility script for the AML Address Screening skill.
It reads the raw graph JSON produced by `fetch_graph.py` and the user-provided `rules.json`.
It extracts every node/tag that is within a maximum depth (hops) of 5 and that matches any rule condition.
The result is written to `graph_data/risk_paths_<address>_<timestamp>.json` for downstream LLM evaluation.
"""
import argparse
import json
import os
import sys
from datetime import datetime

def load_rules(rules_path: str):
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_graph(graph_path: str):
    with open(graph_path, "r", encoding="utf-8") as f:
        return json.load(f)

def prioritize_tag(tags):
    """Return the tag dict with the lowest `priority` value.
    If multiple tags share the same lowest priority, the first encountered is returned.
    """
    if not tags:
        return None
    # Ensure priority is an int; if missing, treat as large number
    def pr(tag):
        try:
            return int(tag.get("priority", 9999))
        except Exception:
            return 9999
    return min(tags, key=pr)

def rule_matches_node(rule, node):
    """Very simple matcher for the current rule set.
    Supports primary_category IN list and deep equality checks.
    """
    # Extract conditions list
    for cond in rule.get("conditions", []):
        param = cond.get("parameter")
        op = cond.get("operator")
        value = cond.get("value")
        if param == "path.node.tags.primary_category":
            # node is expected to have a 'tags' list
            tag = prioritize_tag(node.get("tags", []))
            if not tag:
                return False
            primary = tag.get("primary_category")
            if op == "IN":
                if primary not in value:
                    return False
            else:
                # unsupported operator for this param
                return False
        elif param == "path.node.deep":
            deep = node.get("deep")
            if op == "==":
                if deep != value:
                    return False
            elif op == "<=":
                if deep > value:
                    return False
            elif op == ">=":
                if deep < value:
                    return False
            else:
                return False
        # Additional condition types can be added here
    return True

def format_evidence_path(nodes, illicit_index, path_direction):
    """
    Format the evidence string representing the fund flow.
    For INFLOW (-1): The graph traces backwards. The API returns: [Source, ..., Target].
                     So the illicit flow is nodes[illicit_index] -> nodes[illicit_index+1] -> ... -> nodes[-1] (Target)
    For OUTFLOW (1): The graph traces forwards. The API returns: [Target, ..., Destination].
                     So the illicit flow is nodes[0] (Target) -> nodes[1] -> ... -> nodes[illicit_index]
    """
    if path_direction == -1: # Inflow
        relevant_nodes = nodes[illicit_index:]
    elif path_direction == 1: # Outflow
        relevant_nodes = nodes[:illicit_index+1]
    else:
        relevant_nodes = nodes
        
    parts = []
    for i, n in enumerate(relevant_nodes):
        addr = n.get("address", "Unknown")
        amount = n.get("amount", 0)
        if amount is None:
            amount = 0
            
        # Extract a succinct label for the address if available
        tags = n.get("tags", [])
        label_str = ""
        if tags:
            # prioritize_tag returns the most important tag
            best_tag = prioritize_tag(tags)
            if best_tag:
                lbl = best_tag.get("quaternary_category") or best_tag.get("tertiary_category") or best_tag.get("primary_category")
                if lbl:
                    label_str = f" ({lbl})"
        
        # If it's not the first element, add the transfer arrow
        if i > 0:
            parts.append(f"--({amount} USD)-->")
            
        parts.append(f"[{addr}{label_str}]")
        
    return " ".join(parts)

def extract_risk_paths(graph_data, rules, max_depth=5):
    risk_paths = []
    # The graph JSON structure is expected to have a top-level key "graph_data" with a "data" dict
    data = graph_data.get("graph_data", {}).get("data", {})
    for path in data.get("paths", []):
        # Each path has a list of node dicts under "path"
        nodes = path.get("path", [])
        path_dir = path.get("direction", -1)
        
        if not nodes:
            continue
            
        target_inflow_deep = nodes[-1].get("deep", 0)
        target_outflow_deep = nodes[0].get("deep", 0)
        
        for node in nodes:
            raw_deep = node.get("deep")
            if raw_deep is None:
                continue
                
            # Calculate true distance from target
            if path_dir == -1:
                true_deep = target_inflow_deep - raw_deep
            else:
                true_deep = raw_deep - target_outflow_deep
                
            if true_deep > max_depth:
                continue
                
            # Temporarily inject true_deep into node for correct rule evaluation
            node["deep"] = true_deep
            
            # Determine the winning tag (lowest priority)
            tag = prioritize_tag(node.get("tags", []))
            if not tag:
                continue
            # Find matching rules for this node
            matched_rule_ids = []
            for rule in rules:
                if rule_matches_node(rule, node):
                    matched_rule_ids.append(rule.get("rule_id"))
            if matched_rule_ids:
                illicit_index = nodes.index(node)
                evidence_path_str = format_evidence_path(nodes, illicit_index, path_dir)
                
                risk_paths.append({
                    "address": node.get("address"),
                    "deep": true_deep,
                    "tag": tag,
                    "matched_rules": matched_rule_ids,
                    "path_index": data.get("paths", []).index(path),
                    "evidence_path": evidence_path_str
                })
    return risk_paths

def main():
    parser = argparse.ArgumentParser(description="Extract risk-relevant paths within 5 hops.")
    parser.add_argument("--graph", required=True, help="Path to raw_graph JSON file.")
    parser.add_argument("--rules", default="rules.json", help="Path to rules.json (default: ./rules.json).")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum hop depth to consider.")
    args = parser.parse_args()

    if not os.path.isfile(args.graph):
        print(json.dumps({"error": f"Graph file not found: {args.graph}"}))
        sys.exit(1)
    if not os.path.isfile(args.rules):
        print(json.dumps({"error": f"Rules file not found: {args.rules}"}))
        sys.exit(1)

    graph = load_graph(args.graph)
    rules = load_rules(args.rules)

    risk_paths = extract_risk_paths(graph, rules, max_depth=args.max_depth)

    # Prepare output path
    base_name = os.path.basename(args.graph)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"risk_paths_{base_name.replace('raw_graph_', '')}_{timestamp}.json"
    out_dir = os.path.join(os.getcwd(), "graph_data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"risk_paths": risk_paths}, f, indent=2, ensure_ascii=False)
    print(json.dumps({"status": "success", "output": out_path, "count": len(risk_paths)}))

if __name__ == "__main__":
    main()
