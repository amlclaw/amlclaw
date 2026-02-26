# AML Rule Generator — Design Document

> This document explains the architectural decisions and technical design behind the AML Rule Generator skill.
> 本文档阐述 AML 规则生成器技能的架构决策和技术设计。

## 1. Overview — 概述

The AML Rule Generator translates regulatory compliance requirements into **machine-readable JSON rules** that the Address Screening skill can automatically enforce.

The core insight is that AML compliance policies are ultimately a set of conditional triggers: "If an address has property X, take action Y." This skill formalizes that pattern into a strict JSON schema, so an LLM agent can:

1. **Read** regulatory documents (FATF guidelines, MAS notices, SFC rules)
2. **Extract** compliance requirements as structured rules
3. **Output** a `rules.json` file that the screening engine consumes

> 核心思想：AML 合规政策本质上是一组条件触发器。本技能将其形式化为严格的 JSON 结构。

## 2. Rule Schema Design — 规则模式设计

### 2.1 Four Categories — 四个类别

Every rule belongs to exactly one business scenario category:

| Category | When Applied | What It Checks |
|---|---|---|
| **Deposit** | `--scenario deposit` or `onboarding` | Fund sources (inflow), outflow history, target self-tags |
| **Withdrawal** | `--scenario withdrawal` | Fund destinations (outflow), target self-tags |
| **CDD** | `--scenario cdd` | Transaction amount thresholds |
| **Ongoing Monitoring** | `--scenario monitoring` | Daily volume, structuring patterns |

> 每条规则属于且仅属于一个业务场景类别。

### 2.2 Why Onboarding Was Merged into Deposit — 为什么入驻合并到入金

**V1 Design**: 5 categories — Onboarding was separate, using `target.tags.*` conditions to check the address's own labels.

**V2 Decision**: Merge Onboarding into Deposit. Reasons:

1. **Risk is temporal**: An address clean at onboarding may later be flagged. Re-running the same Deposit rules at each deposit ensures consistent coverage.
2. **Self-tag rules remain**: `DEP-SELF-*` rules (using `target.tags.*` conditions) handle the "is this address itself flagged?" check that onboarding requires.
3. **Simpler mental model**: Instead of asking "is this an onboarding rule or a deposit rule?", all inflow risk assessment lives under one category.

The `onboarding` scenario still exists in the screening tool — it simply applies Deposit rules.

> V1 有 5 个类别。V2 将 Onboarding 合并到 Deposit，因为风险随时间变化，每次入金都应重新评估。

### 2.3 Rule-Level Direction and Hop Fields — 规则级方向和跳数字段

**V1 Problem**: Direction and hop distance were encoded as `conditions[]` entries:
```json
{"parameter": "path.node.deep", "operator": "<=", "value": 3}
```

This mixed contextual filtering with content matching, making it harder to reason about rules.

**V2 Solution**: Three optional top-level fields:

| Field | Type | Description |
|---|---|---|
| `direction` | `"inflow"` / `"outflow"` | Which path direction this rule matches |
| `min_hops` | integer (1-10) | Minimum hop distance (inclusive) |
| `max_hops` | integer (1-10) | Maximum hop distance (inclusive) |

```json
{
  "rule_id": "SG-DPT-DEP-SEVERE-001",
  "category": "Deposit",
  "direction": "inflow",
  "min_hops": 1,
  "max_hops": 1,
  "conditions": [
    {"parameter": "path.node.tags.primary_category", "operator": "IN", "value": ["Sanctions", "Cybercrime"]}
  ],
  "risk_level": "Severe",
  "action": "Freeze"
}
```

Benefits:
- **Clear separation**: "When does this rule apply?" (direction + hops) vs "What does it match?" (conditions)
- **Hop-tiered severity**: Different rules for different distances, enabling the Pollution Decay Principle

> V2 将方向和跳数提升为顶层字段。好处：清晰分离"何时适用"和"匹配什么"。

### 2.4 Pollution Decay Principle — 污染衰减原则

Rules are tiered by hop distance to reflect real-world risk decay:

```
Tier 1: Hop 1 (direct)   → Severe / Freeze    (DEP-SEVERE-001, WDR-SEVERE-001)
Tier 2: Hop 2-3 (near)   → Severe / Freeze    (DEP-SEVERE-002, WDR-SEVERE-002)
Tier 3: Hop 4-5 (far)    → High / EDD         (DEP-HIGH-001, WDR-HIGH-001)
```

This creates a natural risk gradient: direct counterparties trigger the harshest response, while distant connections trigger enhanced due diligence rather than immediate freezing.

> 跳数分层反映现实风险衰减：直接对手方触发最严厉响应，远距离连接触发增强尽调。

### 2.5 AND-Logic Conditions, OR via Separate Rules — AND 逻辑条件

Within a single rule, all conditions are evaluated with **AND logic**:

```json
{
  "conditions": [
    {"parameter": "path.node.tags.primary_category", "operator": "==", "value": "Sanctions"},
    {"parameter": "path.node.tags.risk_level", "operator": "==", "value": "high"}
  ]
}
```
→ Both must be true for the rule to match.

For **OR logic**, create separate rules:
```json
// Rule A: Sanctions → Severe
{"conditions": [{"parameter": "...", "value": "Sanctions"}]}
// Rule B: Cybercrime → Severe
{"conditions": [{"parameter": "...", "value": "Cybercrime"}]}
```

Or use the `IN` operator for OR within a single parameter:
```json
{"parameter": "path.node.tags.primary_category", "operator": "IN", "value": ["Sanctions", "Cybercrime"]}
```

> 单条规则内使用 AND 逻辑。OR 逻辑通过创建多条规则或使用 IN 运算符实现。

### 2.6 Parameter Taxonomy — 参数分类

Rule conditions reference specific JSON paths in the TrustIn Graph API response:

| Parameter Level | Parameters | Used By |
|---|---|---|
| **Path-node** | `path.node.tags.primary_category`, `.secondary_category`, `.risk_level` | Deposit, Withdrawal rules |
| **Target** | `target.tags.primary_category`, `.secondary_category`, `.risk_level` | Self-tag rules (DEP-SELF-*, WDR-SELF-*) |
| **Path-amount** | `path.amount`, `path.risk_amount_usd`, `path.risk_percentage` | CDD rules |
| **Monitoring** | `target.daily_deposit_usd`, `target.daily_withdrawal_usd` | Ongoing Monitoring rules |

Condition values must use **exact TrustIn tag strings** (case-sensitive). Valid values are documented in `references/Trustin AML labels.md`.

> 参数对应 TrustIn Graph API 的 JSON 路径。条件值必须使用精确的 TrustIn 标签字符串（区分大小写）。

### 2.7 Rule Naming Convention — 规则命名约定

Rule IDs follow a structured naming pattern:

```
{REGION}-DPT-{SCENARIO}-{SEVERITY}-{NUMBER}
```

| Component | Values | Example |
|---|---|---|
| Region | `SG` (Singapore), `HK` (Hong Kong), `UAE` (Dubai) | `SG-DPT` |
| Scenario | `DEP` (Deposit), `WDR` (Withdrawal), `CDD`, `TX` (Monitoring) | `DEP-SEVERE` |
| Self-tag | `DEP-SELF`, `WDR-SELF` | `DEP-SELF-SEVERE-001` |
| Outflow history | `DEP-OUT` | `DEP-OUT-SEVERE-001` |
| Whitelist | `WHL` | `WHL-001` |
| Severity | `SEVERE`, `HIGH`, `MEDIUM`, `LOW` | `SEVERE-001` |

> 规则 ID 遵循结构化命名模式：区域-业务-场景-严重性-编号。

## 3. Regional Default Rulesets — 区域默认规则集

### 3.1 Design Philosophy — 设计理念

Each regional ruleset is crafted to reflect the jurisdiction's specific regulatory framework:

| Region | Regulator | Rules | Focus |
|---|---|---|---|
| **Singapore MAS** | MAS PSN02/DPT | 19 rules | Strict sanctions, conservative thresholds |
| **Hong Kong SFC** | SFC VASP Guidelines | 18 rules | Balanced risk-based approach |
| **Dubai VARA** | VARA Rulebook | 19 rules | Growth-oriented with clear red lines |

All three rulesets share the same architectural pattern:
- **Deposit**: 2 SEVERE (hop-tiered), 3 HIGH (far-distance + threshold), 2 DEP-OUT (outflow history), 2 DEP-SELF (self-tags), 1 WHL (whitelist)
- **Withdrawal**: 2 SEVERE (hop-tiered), 2 HIGH (far-distance + threshold), 2 WDR-SELF (self-tags)
- **CDD/Monitoring**: 1-2 transaction threshold rules

> 三个区域规则集共享相同的架构模式，但阈值和严重性反映各管辖区的监管框架。

### 3.2 Differences Between Regions — 区域差异

The rulesets differ in:
- **Threshold amounts**: Singapore MAS has lower CDD thresholds (stricter) than Dubai VARA
- **Category coverage**: Which TrustIn tag categories trigger which severity level
- **Action mapping**: Some jurisdictions default to `Freeze` while others default to `EDD` for the same risk level
- **Regulatory references**: Each rule links to the specific clause in the local regulation

## 4. Validation Pipeline — 验证管道

`validate_rules.py` performs four checks after every rules.json save:

| Check | What It Validates |
|---|---|
| **JSON Structure** | Valid JSON array, required fields present, valid types |
| **Schema Compliance** | Categories, risk levels, actions, operators match schema enums |
| **Field Validation** | `direction` ∈ {inflow, outflow}, `min_hops` ≤ `max_hops`, positive integers |
| **Uniqueness** | No duplicate `rule_id` values |

The validator has **zero external dependencies** — it's pure Python stdlib. This ensures it can run in any environment without pip installs.

> 验证器执行四项检查：JSON 结构、模式合规、字段验证、唯一性。零外部依赖。

## 5. Compliance Document Generation — 合规文件生成

The skill can convert `rules.json` into a formal AML Policy document:

```
rules.json → compliance_doc_prompt.md → LLM → aml_policy.md
```

The LLM reads the raw JSON and the prompt template, then generates a human-readable document suitable for regulatory submission. Technical parameter paths are replaced with business descriptions:

| JSON Parameter | Human-Readable |
|---|---|
| `path.node.tags.primary_category IN ["Sanctions"]` | "Monitor for funds linked to sanctioned entities" |
| `min_hops: 1, max_hops: 1` | "Direct counterparty (1 hop)" |
| `action: "Freeze"` | "Immediately freeze the account and escalate to MLRO" |

> rules.json 可转换为正式的 AML 政策文件，适合提交给监管机构。
