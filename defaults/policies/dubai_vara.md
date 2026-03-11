# Dubai VARA — AML/CFT Compliance Policy for Virtual Asset Service Providers

## 1. Jurisdiction Overview

This policy applies to Virtual Asset Service Providers (VASPs) licensed by the Dubai Virtual Assets Regulatory Authority (VARA) under the Dubai Virtual Assets Regulation Law. It implements requirements from:

- **VARA Compliance and Risk Management Rules** — Virtual Asset regulatory framework
- **UAE Federal AML/CFT Law** — Federal Decree-Law No. 20 of 2018
- **FATF Recommendations** — 40 Recommendations, VA/VASP Guidance
- **OFAC/UN Sanctions** — International sanctions compliance
- **UAE National Risk Assessment** — Country-specific ML/TF risk factors

## 2. Key Regulatory Requirements

### 2.1 Customer Due Diligence (CDD)
- Verify identity of all customers prior to onboarding using reliable, independent sources
- Identify Ultimate Beneficial Owners (UBOs) with >25% ownership or control
- Assess purpose and intended nature of virtual asset activities
- Continuous due diligence with risk-based approach

### 2.2 Enhanced Due Diligence (EDD)
Required when:
- Customer from high-risk jurisdiction per FATF or UAE NRA
- Transaction involves PEPs, their family members, or close associates
- Blockchain analytics reveal counterparty risk within 3 hops
- Transactions above AED 55,000 (~USD 15,000) without clear economic rationale
- Complex or unusual transaction patterns

### 2.3 Suspicious Activity Reporting (SAR)
- Report to UAE Financial Intelligence Unit (FIU) — goAML portal
- File within 30 calendar days of suspicion
- Maintain strict confidentiality
- Retain records for minimum 5 years (8 years for high-risk)

## 3. Risk Categories and Thresholds

| Risk Level | Trigger | Action |
|------------|---------|--------|
| **Severe** | Direct (Hop 1) Sanctions, Terrorism Financing, Public Freezing Action | **Freeze** — Immediate freeze, file SAR |
| **Severe** | Near-distance (Hop 2-3) Sanctions, Terrorism Financing | **Freeze** — Freeze pending investigation |
| **High** | Direct (Hop 1) Mixers, Darknet, Hacker/Thief, Gambling, Illicit Markets | **EDD** — Enhanced due diligence |
| **High** | Near-distance (Hop 2-3) Mixers, Darknet | **EDD** — Enhanced due diligence |
| **High** | Far-distance (Hop 4-5) Sanctions, Terrorism | **EDD** — Investigate taint |
| **Medium** | Gambling (Hop 2-3), unhosted wallets, P2P exchanges | **Flag** — Monitor and review |
| **Low** | No risk indicators detected | **Allow** — Standard processing |

### Self-Tag Checks
- Target tagged as Sanctioned Entity, Terrorism Financing → **Immediate Freeze**
- Target tagged as Mixer, Darknet, Gambling → **EDD** required
- Target tagged as Other Financial Crimes → **EDD** required

### Outflow History Checks
- Outflow to Sanctions/Terrorism entities → **Freeze**
- Outflow to Mixers/Darknet → **EDD**

## 4. Required Procedures

### 4.1 Onboarding
1. Collect Emirates ID/passport, proof of address, source of funds declaration
2. Screen wallet address: `--scenario onboarding`
3. Severe risk → reject onboarding, file SAR with FIU
4. High risk → proceed with EDD, MLRO approval required
5. Low/Medium → approve with standard monitoring

### 4.2 Transaction Monitoring
- Screen all deposits: `--scenario deposit`
- Screen all withdrawals: `--scenario withdrawal`
- Ongoing monitoring: `--scenario monitoring` for structuring detection
- CDD threshold: transactions > AED 55,000 trigger enhanced review
- Wire transfer rule: cross-border VA transfers > AED 3,500 require originator/beneficiary info

### 4.3 Record Keeping
- Retain CDD records for minimum 5 years (8 years for high-risk customers)
- Retain transaction records for minimum 5 years from date of transaction
- Maintain complete screening audit trail including graph data

## 5. Monitoring Requirements

- **Real-time**: All deposits and withdrawals screened prior to settlement
- **Periodic**: Semi-annual portfolio re-screening for all customers
- **Event-driven**: Immediate re-screening on sanctions updates or risk escalation
- **Sanctions**: Re-screen full portfolio within 24 hours of OFAC/UN/UAE local list updates
- **VARA reporting**: Quarterly compliance metrics submission

## 6. Escalation

1. **Automated flag** → Compliance analyst review within 24 hours
2. **EDD trigger** → Compliance Officer review within 48 hours
3. **Freeze trigger** → Immediate MLRO escalation, asset freeze, SAR filing within 30 days
4. **VARA notification** → Report material compliance breaches to VARA within 5 business days
5. **Annual review** → Board-level AML/CFT effectiveness review
