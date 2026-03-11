# Hong Kong SFC — AML/CFT Compliance Policy for Virtual Asset Service Providers

## 1. Jurisdiction Overview

This policy applies to Virtual Asset Service Providers (VASPs) and Licensed Virtual Asset Trading Platforms (VATPs) operating under the Hong Kong Securities and Futures Commission (SFC) regulatory framework. It implements requirements from:

- **Anti-Money Laundering and Counter-Terrorist Financing Ordinance (AMLO)** — Cap. 615
- **SFC AML/CFT Guidelines** — Guidelines for Licensed Corporations and SFC-Licensed VATPs
- **FATF Recommendations** — 40 Recommendations, VA/VASP Guidance
- **OFAC/UN Sanctions** — International sanctions compliance

## 2. Key Regulatory Requirements

### 2.1 Customer Due Diligence (CDD)
- Verify identity before establishing business relationships or conducting occasional transactions ≥ HK$8,000
- Identify and verify beneficial owners (>25% ownership threshold)
- Understand nature and purpose of business relationship
- Ongoing monitoring of transactions and updating of customer information

### 2.2 Enhanced Due Diligence (EDD)
Required when:
- Higher ML/TF risk identified through risk assessment
- Customer is a PEP or associated with a PEP
- Transactions linked to high-risk jurisdictions
- Blockchain analytics show connections to high-risk entities (Hop 1-3)
- Complex or unusually large transactions with no apparent economic purpose

### 2.3 Suspicious Transaction Reporting (STR)
- Report to Joint Financial Intelligence Unit (JFIU) as soon as reasonably practicable
- Maintain confidentiality — no tipping off
- Retain records for minimum 6 years

## 3. Risk Categories and Thresholds

| Risk Level | Trigger | Action |
|------------|---------|--------|
| **Severe** | Direct (Hop 1) Sanctions, Terrorism Financing, Public Freezing Action | **Freeze** — Immediate freeze, report to JFIU |
| **Severe** | Near-distance (Hop 2-3) Sanctions, Terrorism Financing | **Freeze** — Freeze pending investigation |
| **High** | Direct (Hop 1) Mixers, Darknet, Hacker/Thief, Gambling, Illicit Markets | **EDD** — Enhanced due diligence |
| **High** | Near-distance (Hop 2-3) Mixers, Darknet, Gambling | **EDD** — Enhanced due diligence |
| **High** | Far-distance (Hop 4-5) Sanctions, Terrorism | **EDD** — Investigate with reduced severity |
| **Medium** | Exposure to unhosted wallets, P2P exchanges | **Flag** — Monitor and document |
| **Low** | No risk indicators | **Allow** — Standard processing |

### Self-Tag Checks
- Target tagged as Sanctioned Entity or Terrorism Financing → **Immediate Freeze**
- Target tagged as Mixer, Darknet, Gambling → **EDD** required

### Outflow History Checks
- Outflow to Sanctions/Terrorism entities → **Freeze**
- Outflow to Mixers/Darknet/Gambling → **EDD**

## 4. Required Procedures

### 4.1 Onboarding
1. Customer identification and verification (HKID/passport, proof of address)
2. Screen wallet address: `--scenario onboarding`
3. Severe risk → reject, file STR with JFIU
4. High risk → proceed with EDD, senior management approval required
5. Low/Medium → approve with standard monitoring tier

### 4.2 Transaction Monitoring
- Screen all deposits: `--scenario deposit`
- Screen all withdrawals: `--scenario withdrawal`
- Ongoing monitoring: `--scenario monitoring`
- CDD threshold: single transaction > HK$8,000 (occasional) or patterns suggesting structuring

### 4.3 Record Keeping
- Retain all CDD records for minimum 6 years after termination of business relationship
- Retain transaction records for minimum 6 years from date of transaction
- Maintain full audit trail of screening decisions

## 5. Monitoring Requirements

- **Real-time**: Screen all deposit and withdrawal transactions
- **Periodic**: Quarterly risk reassessment of high-risk customers; annual for standard
- **Event-driven**: Re-screen on regulatory alerts, sanctions list updates, or customer behavior change
- **Sanctions**: Re-screen within 24 hours of sanctions list updates

## 6. Escalation

1. **Automated flag** → Compliance team review within 24 hours
2. **EDD trigger** → Compliance Officer review within 48 hours
3. **Freeze trigger** → Immediate escalation to MLRO, freeze assets, STR to JFIU
4. **Regulatory reporting** → Quarterly compliance report to SFC, annual AML return
