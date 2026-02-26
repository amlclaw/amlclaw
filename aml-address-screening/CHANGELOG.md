# Changelog

All notable changes to the **AML Address Screening** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-26

### Added
- Scenario-based screening with `--scenario` flag (onboarding, deposit, withdrawal, cdd, monitoring, all)
  > 基于场景的筛查：不同业务场景自动加载对应规则类别和路径方向
- Rule-level `direction`/`min_hops`/`max_hops` filtering via `rule_applies_to_context()`
  > 规则级方向和跳数过滤，替代旧的 path.node.deep 条件
- Pollution Decay Principle: hop-based risk tiering (Hop 1 → Severe, Hop 2-3 → Severe, Hop 4-5 → High)
  > 污染衰减原则：跳数越远，风险越低
- Target self-tag evaluation independent of path traversal (DEP-SELF-*, WDR-SELF-* rules)
  > 目标自身标签评估：检查目标地址是否被制裁/冻结
- Deposit outflow history detection (DEP-OUT-* rules)
  > 入金场景的出金历史检测：目标地址是否曾向制裁实体转账
- `evaluate_target_rules()` function for self-tag matching
  > 新增目标标签评估函数

### Changed
- Deposit scenario now fetches both inflow + outflow paths (was inflow-only)
  > 入金场景改为获取双向路径，以支持出金历史规则
- Onboarding scenario uses Deposit rules exclusively (was Onboarding + Deposit)
  > 入驻场景仅使用 Deposit 规则（不再有独立的 Onboarding 类别）
- Removed `path.node.deep` from evaluable condition parameters
  > 移除 path.node.deep 条件参数，改用规则级 min_hops/max_hops

## [0.1.0] - 2026-02-24

### Added
- Initial KYA screening pipeline: `fetch_graph.py` → `extract_risk_paths.py` → LLM evaluation
  > 初始 KYA 筛查管道：获取图数据 → 提取风险路径 → LLM 评估
- TrustIn KYA Pro API v2 integration with async submit → poll → result pattern
  > TrustIn KYA Pro API v2 集成，异步提交 → 轮询 → 获取结果
- Evidence chain rendering with fund flow amounts in USD
  > 证据链渲染，显示资金流向和金额
- Positional hop computation via `compute_true_deep()` (workaround for unreliable API `deep` field)
  > 位置化跳数计算，解决 API deep 字段不可靠的问题
- Graph path deduplication by address with evidence capping (max 3 per entity)
  > 按地址去重，每个实体最多保留 3 条证据路径
- LLM evaluation prompt template (`evaluation_prompt.md`)
  > LLM 评估提示模板
- `run_screening.py` orchestrator combining fetch + extract stages
  > run_screening.py 编排器，串联获取和提取阶段
