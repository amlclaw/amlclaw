# AML Compliance Document Generation Prompt

You are an expert AML Compliance Documentation Writer. Your task is to generate a formal, professional AML/CFT Policy Document based strictly on the current rules defined in `rules.json`.

**Target Audience**: Regulators (e.g., MAS, SFC, VARA, Financial Intelligence Units), banking partners, and internal compliance teams.
**Purpose**: To serve as the official documented proof of the platform's on-chain AML risk management frameworks, demonstrating how the platform screens, categorizes, and actions different blockchain risks.

## Instructions
1. **Read the Rules**: Analyze the provided JSON rules array.
2. **Structure the Document**: Use the following standard compliance policy structure:
    - **1. Purpose & Scope**: Brief intro about the document governing on-chain risk.
    - **2. Risk Appetite & Sanctions**: Detail the zero-tolerance policy for Sanctions and Terrorism Financing based on the rules.
    - **3. Onboarding & Counterparty Screening**: Explain how the engine checks `target.tags` at onboarding.
    - **4. Transaction Monitoring (Inflow/Deposit)**:
        - Describe the hop-depth tracing policy. (e.g., "The system traces deposits up to X hops for exposure to Y").
        - Explain percentage and amount thresholds. (e.g., "If exposure to High-Risk entities exceeds X% of the transaction AND the absolute risk amount is greater than Y USD...").
        - Detail the actions taken for direct (1-hop) vs indirect exposure to High-Risk entities (Cybercrime, Darknet, Mixers), and any Whitelist protocols to prevent false positives.
    - **5. Travel Rule, Occasional Transactions & Structuring Monitoring**:
        - Specify the exact Travel Rule threshold limit being enforced (based on the `path.amount` value).
        - Specify CDD thresholds for occasional transactions.
        - Detail the Anti-Smurfing / Structuring alerts based on `target.daily_deposit_usd` accumulation thresholds.
        - Specify the exact Travel Rule threshold limit being enforced (based on the `path.amount` value in the rules).
        - Detail interactions with external high-risk VASPs.
    - **6. Escalation Matrix**: A summary table of what triggers `Review`, `EDD`, and `Freeze`/`Reject`.
3. **Professional Tone**: Use formal legal/compliance terminology. Replace technical JSON paths (like `path.node.tags.primary_category`) with business language (e.g., "Entity categorization via blockchain analytics"). Use the `reference` fields to cite regulations where applicable.
4. **Output Format**: Format the output as a clean, highly readable Markdown document.

## Input Context
Please convert the following rules into the compliance policy document:
[INSERT JSON HERE]
