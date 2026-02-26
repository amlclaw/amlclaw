# Changelog

All notable changes to the **AML Rule Generator** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-26

### Added
- Rule-level `direction`, `min_hops`, `max_hops` fields for contextual filtering
  > 新增规则级方向和跳数字段，用于上下文过滤
- DEP-SELF-*, WDR-SELF-* self-tag rules using `target.tags.*` conditions
  > 自身标签规则：检查目标地址是否被制裁/冻结
- DEP-OUT-* outflow history rules (deposit context, outflow direction)
  > 出金历史规则：入金场景中检查目标的出金历史
- Hop-tiered rules implementing Pollution Decay Principle (3 tiers per scenario)
  > 跳数分层规则，实现污染衰减原则
- `validate_rules.py` validates new `direction`, `min_hops`, `max_hops` fields
  > 验证脚本支持新字段验证

### Changed
- Removed `Onboarding` category — merged into `Deposit`
  > 移除 Onboarding 类别，合并到 Deposit
- Removed `path.node.deep` from valid condition parameters
  > 移除 path.node.deep 条件参数
- Updated all 3 default rulesets to V2 format:
  - Singapore MAS: 19 rules (was 12)
  - Hong Kong SFC: 18 rules (was 11)
  - Dubai VARA: 19 rules (was 12)
  > 更新三个区域默认规则集到 V2 格式

## [0.1.0] - 2026-02-24

### Added
- JSON rule schema (`rule_schema.json`) with 5 categories (Onboarding, Deposit, Withdrawal, CDD, Ongoing Monitoring)
  > JSON 规则模式，5 个业务场景类别
- Default regional rulesets: Singapore MAS, Hong Kong SFC, Dubai VARA
  > 区域默认规则集：新加坡 MAS、香港 SFC、迪拜 VARA
- Rule validation script (`validate_rules.py`): schema + uniqueness + TrustIn label cross-check
  > 规则验证脚本：模式验证 + 唯一性 + TrustIn 标签交叉检查
- Compliance document generation via LLM (`compliance_doc_prompt.md`)
  > 通过 LLM 生成合规文件
- FATF reference library (40 Recommendations, VA/VASP Guidance, Travel Rule)
  > FATF 参考文献库
- Sanctions reference library (FATF High-Risk, OFAC, UN)
  > 制裁参考文献库
- Regional regulatory guides: Singapore MAS, Hong Kong SFC, Dubai VARA (Chinese)
  > 区域监管指南（中文）
