# Singapore MAS — AML/CFT Compliance Policy for Digital Payment Token Services

## 1. Jurisdiction Overview

This policy applies to Digital Payment Token (DPT) service providers licensed under the Payment Services Act 2019 (PS Act) in Singapore, regulated by the Monetary Authority of Singapore (MAS). It implements requirements from:

- **MAS Notice PSN02** — Prevention of Money Laundering and Countering the Financing of Terrorism
- **MAS Notice PSN08** — Technology Risk Management
- **FATF Recommendations** — 40 Recommendations (2023 update), VA/VASP Guidance (2021)
- **OFAC SDN List** — US Office of Foreign Assets Control Specially Designated Nationals

## 2. Key Regulatory Requirements

### 2.1 Customer Due Diligence (CDD)
- Verify identity of all customers before establishing a business relationship
- Obtain beneficial ownership information for legal entities
- Understand the purpose and intended nature of the business relationship
- Perform ongoing due diligence including transaction monitoring

### 2.2 Enhanced Due Diligence (EDD)
Required when:
- Customer or counterparty is from a high-risk jurisdiction (FATF grey/black list)
- Transaction involves a Politically Exposed Person (PEP)
- Unusual or complex transaction patterns detected
- Blockchain analytics reveal connections to high-risk entities within 3 hops

### 2.3 Suspicious Transaction Reporting (STR)
- File STR with the Suspicious Transaction Reporting Office (STRO) within 15 business days
- Maintain records of all STRs filed for a minimum of 5 years
- No tipping-off of subjects under investigation

## 3. Risk Categories and Thresholds

| Risk Level | Trigger | Action |
|------------|---------|--------|
| **Severe** | Direct (Hop 1) exposure to Sanctions, Terrorism Financing, Illicit Markets | **Freeze** — Immediate asset freeze, file STR |
| **Severe** | Near-distance (Hop 2-3) exposure to Sanctions, Terrorism Financing | **Freeze** — Asset freeze pending investigation |
| **High** | Direct (Hop 1) exposure to Mixers, Darknet, Hacker/Thief, Gambling | **EDD** — Enhanced due diligence required |
| **High** | Near-distance (Hop 2-3) exposure to Mixers, Darknet, Gambling | **EDD** — Enhanced due diligence required |
| **High** | Far-distance (Hop 4-5) exposure to Sanctions, Terrorism | **EDD** — Investigate taint propagation |
| **Medium** | Exposure to unhosted wallets, P2P exchanges at any distance | **Flag** — Monitor and document |
| **Low** | No risk indicators detected | **Allow** — Standard processing |

### Self-Tag Checks (Target Address)
- If the target address itself is tagged as Sanctioned Entity, Terrorism Financing, or subject to Public Freezing Action → **Immediate Freeze**
- If tagged as Mixer, Darknet, Gambling → **EDD** required

### Outflow History Checks (Deposit Context)
- DEP-OUT rules examine where the target has previously sent funds
- Direct outflow to Sanctions/Terrorism entities → **Freeze**
- Direct outflow to Mixers/Darknet → **EDD**

## 4. Required Procedures

### 4.1 Onboarding
1. Collect and verify customer identity (NRIC/passport, proof of address)
2. Screen address using AMLClaw with `--scenario onboarding`
3. If Severe risk → reject onboarding, file STR
4. If High risk → proceed with EDD, obtain additional documentation
5. If Low/Medium → approve with standard monitoring

### 4.2 Transaction Monitoring
- Screen all deposit addresses with `--scenario deposit`
- Screen withdrawal destinations with `--scenario withdrawal`
- Run `--scenario monitoring` for ongoing structuring detection
- CDD thresholds: single transaction > S$20,000 triggers enhanced review

### 4.3 Record Keeping
- Maintain all screening reports for minimum 5 years after relationship ends
- Store rules.json version history for audit trail
- Archive all graph_data and risk_paths outputs

## 5. Monitoring Requirements

- **Real-time**: All deposits and withdrawals screened before processing
- **Periodic**: Monthly full portfolio re-screening using `--scenario cdd`
- **Event-driven**: Re-screen on material change in customer risk profile
- **Sanctions updates**: Re-screen portfolio within 24 hours of OFAC/UN list updates

## 6. Escalation

1. **Automated flag** → Compliance officer review within 24 hours
2. **EDD trigger** → Senior compliance officer review within 48 hours
3. **Freeze trigger** → Immediate escalation to MLRO, asset freeze, STR filing within 15 business days
4. **Regulatory reporting** → Annual compliance report to MAS
