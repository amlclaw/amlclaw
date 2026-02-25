# AML Rule Generator Skill

This skill autonomously reads extensive compliance and anti-money laundering (AML) regulatory documents and distills them into a standardized, machine-readable `rules.json` framework.

## 🚀 Purpose
LLMs and human analysts need a common language to understand what constitutes a "High Risk" or "Severe Risk" transaction according to different local jurisdictions (like MAS in Singapore or VARA in Dubai). This skill generator creates that localized policy engine.

## 📁 Directory Structure
- `references/`: Place raw `.md` or `.pdf` regulatory guidelines here. The agent will read these to understand the local laws.
- `schema/`: Contains `rule_schema.json`, which defines the exact data structure the generated rules must follow.
- `defaults/`: Optional pre-generated default rules for common jurisdictions.
- `scripts/`: Python utility scripts for the skill.
- `prompts/`: Contains the LLM instructions for generating the rules and also for generating a human-readable compliance policy document based on those rules.

## 🧠 How to Use (For Agents)

1. **Read References:** Analyze documents in the `references/` directory.
2. **Read Schema:** Understand the rule constraints in `schema/rule_schema.json`.
3. **Generate Rules:** Output a strictly formatted `rules.json` file to the root workspace.
4. **Generate Policy:** (Optional) Use `prompts/compliance_doc_prompt.md` to generate a beautiful, human-readable Markdown policy document summarizing the exact technical triggers in the JSON.
