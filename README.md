# AMLClaw SDK 🦅

AMLClaw is an open-source, LLM-native toolkit designed for automated Crypto AML (Anti-Money Laundering) investigations, rule-engine configuration, and Continuous Risk Monitoring. 

This repository operates primarily as a "**Skill Pack**" intended to be utilized by autonomous coding agents (like Claude Code, OpenClaw, or Gemini Agents) rather than traditional human CLI interaction, although manual execution is supported.

## 📦 Included Skills

This repository contains standalone agentic "skills". By cloning this repo, your Agent immediately inherits the ability to perform complex compliance operations.

| Skill | Directory | Description |
| :--- | :--- | :--- |
| **AML Rule Generator** | `/aml-rule-generator` | Reads global crypto regulatory documents (FATF, MAS, VARA) and synthesizes localized, machine-readable `rules.json` enforcement policies. |
| **Address Screening (KYA)** | `/aml-address-screening` | Deep-scans a blockchain address up to 5 hops, mathematically maps fund flows, and evaluates exposure against your local `rules.json` to produce professional Markdown Audit reports. |

## 🚀 Installation for LLM Agents

If you are using an Agent Framework (like Claude Code or OpenClaw), simply clone this repository into your workspace. 

```bash
git clone https://github.com/YourUsername/amlclaw.git ./skills/amlclaw
```

Because each skill contains a standardized `SKILL.md` instruction file, your agent will autonomously ingest the operating capabilities, prerequisites, and Python execution strings.

## ⚙️ Requirements & Configuration

1. **Python 3.10+** is required to run the data extraction scripts.
2. Install dependencies:
   ```bash
   pip install -r aml-address-screening/requirements.txt
   ```
3. **Environment Setup**: The graphing engine requires an API key from the TrustIn Graph provider. Unzip or copy the `.env.example` file to create your local `.env`.

```bash
cp .env.example .env
# Edit .env and insert your TRUSTIN_API_KEY
```

## 🧠 Example Agent Prompts

Try asking your Agent the following once `amlclaw` is installed:

> "Read the MAS regulatory notice in the rule generator's reference folder, and construct a severe zero-tolerance deposit policy for Singapore."

> "Use the AML Address Screening skill to investigate Tron address `TGE94...` using our new rules.json file. Check both inflows and outflows up to 3 hops."

---
*Built for the next generation of predictive LLM compliance.*
