# Gate 0 Blocker Analysis

## 1. 真正需要人类科学决策

| 条目 | 状态 | 原因 |
|---|---|---|
| P01 claim contract | REQUIRES_HUMAN_APPROVAL | TODO 已给出候选 claims，但研究者仍需确认 preregistration 版本、允许 claim 边界和文献 collision gate。 |
| P02 attack contract | REQUIRES_HUMAN_APPROVAL | A1–A4 涉及安全策略移除与 adaptive tampering；正式攻击权限、阈值、sealed A4 内容和公开范围不能由工程代理替人决定。 |
| P03 evaluator calibration | REQUIRES_HUMAN_APPROVAL | AHC、utility/capability floor、人工盲审与 permissible capability probe 需要安全负责人和人工校准。 |
| P04 model qualification | HUMAN REVIEW REQUIRED | TODO 要求 capability-qualified aligned checkpoint；候选 profiling 可自动完成，但最终 capability 资格与 primary model 选择需人工确认。 |
| Gate 0 final sign-off | BLOCKED_HUMAN_REVIEW | P01–P04 hashes、split provenance、evaluator calibration、A4 seal 和 power simulation 尚未由研究者批准。 |

## 2. 主要是代码 / manifest / schema 缺失

- run schema、seed、revision hash、checkpoint metadata
- safe proxy dataset schema 和 family/split manifest 格式
- activation capture API、token-position QA、streaming summary
- contrast、bootstrap、paired/run-level aggregation API
- evaluator interface 与 proxy evaluator contract
- FLOPs ledger 字段与 runtime report schema
- model loading、chat-template smoke、memory/throughput profiling CLI
- end-to-end dry-run orchestration

这些条目可以在不接触真实危险数据、不运行安全策略移除攻击的前提下实现和验证。

## 3. 可直接从 TODO 冻结定义实现

- 运行级别为最高统计单位，prompt 仅为 run 内重复
- 固定 seed、model/data/code revision fields
- construct-fit / carrier-dev / carrier-test / attack-dev / attack-test 分离的 manifest 字段
- H×P contrast 的均值差、layer sweep、bootstrap CI、family leave-one-out 的接口
- residual final-token capture 的默认位置与 streaming aggregation
- control matrix 的统一记录格式
- artifact 不保存原始危险自由生成文本
- A3/A4、recipe training、sealed A4 在 Gate 0/1 前保持未运行

## 4. 必须保持 BLOCKED

- 真实 harmful prompt、AHC evaluator 和 permissible capability probe 的接入
- C03 natural remove/add/rescue safety intervention
- C04 safety-policy negative-control battery
- A01 restricted writer cut
- A03 parameter-space policy edit
- A04 adaptive direction search、malicious fine-tuning、A4
- 任何基于真实 safety endpoint 的 layer/strength/LR/steps 选择
- 任何 Gate 0 通过、Gate 1 通过或 scientific claim

## 5. 当前可安全推进范围

使用 `DEV_ONLY_MODEL` 与 `PIPELINE_VALIDATION_ONLY` safe synthetic proxy，验证 dataset → model → activation → contrast → proxy intervention → evaluator → statistics 的工程链路。proxy 结果不能解释为 refusal-policy、AHC、durability 或 Gate 1 evidence。

## 6. 当前结论

Gate 0 仍为 `BLOCKED_HUMAN_REVIEW`。工程 readiness 可以独立推进；完成 safe proxy 代码和 dry-run 后，状态最多为 `ENGINEERING_READY_PENDING_HUMAN_GATE0`，不能写成正式 causal feasibility ready。
