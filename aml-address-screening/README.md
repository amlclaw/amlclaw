# AML Address Screening Skill

This skill brings enterprise-grade blockchain tracking to your local workspace, leveraging the TrustIn KYA (Know Your Address) API to automatically trace fund flows, map exposure to sanctions/cybercrime, and evaluate those risks against your localized compliance policies.

## 🚀 Purpose
To fully automate Level-1 and Level-2 blockchain AML investigations. The skill fetches up to 5 hops of bidirectional (inflow/outflow) transaction graphs, filters the noise using mathematical thresholds, and outputs a ready-to-file Compliance Audit Report.

## 📁 Directory Structure
- `scripts/`: Contains the core Python scripts.
  - `trustin_api.py`: The wrapper for interacting with the TrustIn v2 API.
  - `fetch_graph.py`: Fetches raw graph data given an address.
  - `extract_risk_paths.py`: Aggressively trims the raw graph against a `rules.json` file.
  - `run_screening.py`: The main orchestrator that automates fetching and extraction.
- `prompts/`: Contains the LLM instructions (`evaluation_prompt.md`, `analysis_prompt.md`) detailing how to parse the JSON and draft the final markdown report.

## ⚙️ Configuration

1. You must have a `rules.json` file in your main workspace (generate one using the `aml-rule-generator` skill).
2. You need a `.env` file with a valid `TRUSTIN_API_KEY` (Free via [trustin.info](https://trustin.info)).

## 📖 Documentation

- **[DESIGN.md](DESIGN.md)** — Architecture, design decisions, and rule matching logic
- **[CHANGELOG.md](CHANGELOG.md)** — Version history and release notes

## 🧠 How to Use (For Agents)

When asked to screen an address, perform these steps:
1. Ensure the user's `rules.json` is present.
2. Run the orchestrator:
   ```bash
   python3 scripts/run_screening.py <CHAIN> <ADDRESS> --direction all --inflow-hops 5 --outflow-hops 5 --max-nodes 100
   ```
3. Read the generated `risk_paths...json` file found in `scripts/graph_data/`.
4. Follow the `prompts/evaluation_prompt.md` to format and generate the final report in the `reports/` folder.
