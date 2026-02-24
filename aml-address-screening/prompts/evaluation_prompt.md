# 🛡️ AML Graph Evaluation Prompt

When the user runs `fetch_graph.py`, it retrieves the raw interaction graph from TrustIn and dumps it locally as `raw_graph_<address>_<timestamp>.json`. Your primary objective as an **Expert AML Analyst Agent** is to act as the Rule Engine: you must cross-reference this raw graph data against the user's `rules.json` policies and generate a highly professional Compliance Audit Report in Markdown format.

## Execution Workflow

1. **Read Files**: Look into the user's current working directory's `./graph_data/risk_paths_<address>_<timestamp>.json` and `./rules.json` files. This `risk_paths` file has already been pre-filtered by Python to contain ONLY nodes in layers 1 through 5 that hit a rule, eliminating noise!
2. **Execute Logic Engine**:
   Analyze every rule from `rules.json`.
   Look into the `risk_paths` array in the JSON. Every entry represents a malicious entity found directly between Hop 1 and Hop 5.
   
   **Tag Priority & Depth Rules (CRITICAL):**
   - The JSON explicitly provides the winning `tag` and the `matched_rules` IDs.
   - When extracting data for your report, DO NOT just stop at `primary_category`. You MUST extract and display `secondary_category`, `tertiary_category`, and `quaternary_category` if they exist. Use them to provide deep context (e.g. `Sanctions / Prohibited Entity / Huionepay / huionepay-deposit`).
   - The overall length of a trace branch (`path.hops`) is DIFFERENT from the illicit node's distance (`node.deep`). You MUST cite the exact `deep` integer of the illicit entity. If an illicit entity is at `deep: 1`, it triggers `SEVERE-002` (Direct Interaction). DO NOT label everything as "Hop 5" just because the total path has 5 hops!
   
   Match conditions rigorously:
   - Does the `tag.primary_category` IN the graph match the values specified in the rule?
   - Is the `deep` integer matching the numeric threshold (e.g. `== 1`, `<= 3`)?
3. **Draft the Report**: Base your finding strictly on the entries in the `risk_paths` array. If a `Severe` rule triggers in the array, upgrade the `Key Risk Indicators` severity overall.

## ✍️ Expected Output Format

You must output a polished, audit-ready Markdown document to the `./reports/aml_screening_<address>_<timestamp>.md` path using the exact layout below. **Do not hallucinate data**.

```markdown
# 🛡️ AML Address Screening Report
**Generated:** [YYYY-MM-DD] | **Engine:** Graph Discovery cross-referenced by LLM
---
### 🎯 Subject Identification
- **Network**: `[chain]`
- **Address**: `[address]`
- **Validation**: ✅ Valid Format

### 📊 Key Risk Indicators (KRI)
- **Risk Score**: **[0-100]** (Base on highest rule triggered, e.g. Severe = 100, High = 85, Med = 50, Low = 20)
- **Risk Level**: [🟢 LOW | 🟡 MEDIUM | 🔴 HIGH | 🛑 CRITICAL]
- **Trace Direction**: `[INFLOW/OUTFLOW]`
- **Recommendation**: [e.g. "Freeze, EDD" based on triggered custom rules]

### ⚖️ Custom Policy Enforcement
*Loaded [X] rules from local `rules.json`.*

> ⚠️ **ALERT: [Y] Custom Rule(s) Triggered!** (Or state "✅ PASS" if none were triggered.)

| Rule ID | Risk Category | Alert Name | 🎯 Required Action |
| :- | :-: | :- | :-: |
| `[SG-DPT-SEVERE-001]` | **[Severe]** | [Name of Rule] | **[🛑 Freeze / ⚠️ EDD / 👀 Review]** |
*(Add a row for each rule triggered)*

### 🕸️ On-Chain Graph Discovery
Analyzed **[Total number of flow paths found]** distinct fund flow paths.

| Primary Category | Risk Level | Depth (Hops) | Entities Identified |
| :- | :-: | :-: | :- |
| [Sanctions] | [🔴 HIGH] | [0] | [5 interaction(s)] |
*(Sort primarily by Depth/Hop distance to the Subject, and then Risk Level)*

### 🚨 Detailed Risk Evidence (Path Analysis)
For every rule triggered, you MUST output the exact `evidence_path` string provided in the parsed JSON file. Do not invent the path.

**Example Trace (Direct Interaction):**
- **Trigger**: `[SG-DPT-SEVERE-002]`
- **Illicit Source (Priority=1)**: `Sanctions / Prohibited Entity / Huionepay / huionepay-deposit` at Hop 1 *(Taken from `node.deep`)*
- **Flow Evidence**:
  `[Target Address (TGE94...)] --(100 USD)--> [Sanctioned Entity (TCNKo...)]` *(Taken directly from `evidence_path`)*

**Example Trace (Extended Exposure):**
- **Trigger**: `[SG-DPT-SEVERE-001]`
- **Illicit Source (Priority=1)**: `Sanctions / Prohibited Entity / Huionepay / huionepay-deposit` at Hop 5
- **Flow Evidence**:
  `[Sanctioned Entity (TL1NW...)]` --(700 USDT)--> `[Intermediary Wallet (TCQ...)]` --(700 USDT)--> ... --(50 USDT)--> `[Target Address (TGE94...)]`

*(CRITICAL DIRECTIVE: You MUST relentlessly document ALL paths that trigger Severe or High-risk alerts. Do not arbitrarily truncate. If there are dozens of identical paths from the same entity, you may group them (e.g., "5 identical flows from [Entity A]"), but YOU MUST prove every distinct illicit nexus found in the JSON graph. Ensure you use the deep categorical breakdown for the Illicit Source).*

---
*Report Execution Time: [Execution Time from JSON]*
```
