# Refusal Geometry v3：Agent 执行清单

本文件把 `refusal_geometry_research_v3.md` 拆成可独立领取、可验收、尽量不互相修改同一文件的工作包。研究目标不是制造所谓“不可绕过”的 open-weight safeguard，而是测量并提高攻击者在保持模型正常能力时移除安全策略所需的成本。

## 0. 执行约定

状态统一使用：

```text
TODO | READY | IN_PROGRESS | BLOCKED | DONE | DROPPED
```

每个 agent 一次只领取一个任务 ID。完成时必须交付：

1. 代码或配置；
2. 最小测试；
3. `reports/<TASK_ID>.md`，记录命令、输入版本、结果和遗留问题；
4. 机器可读结果，保存到 `runs/<TASK_ID>/`，不只贴终端输出；
5. 不提交原始危险生成文本，只提交数据 manifest、哈希、聚合指标和经过审查的示例。

为避免并行冲突：

- 基础 agent 负责公共接口；实验 agent 不擅自修改公共 schema。
- 每个任务只写自己名下的模块、配置、报告和 run 目录。
- 新依赖先写进任务报告，由集成任务统一更新环境文件。
- 所有比较必须使用固定 split、固定 evaluator 版本和显式 seed。
- 失败也是有效结果，但必须能从报告和 artifacts 复现。

建议的目标目录：

```text
configs/                 实验配置，每个任务单独文件
data/manifests/          数据来源、split、hash；不提交大体积原始数据
docs/contracts/          指标、schema、threat model
src/refusal_geometry/    公共实现
tests/                   小模型/合成数据测试
runs/<TASK_ID>/          机器可读结果
reports/<TASK_ID>.md     人类可读结论
```

## 1. 总体依赖与并行波次

```text
Wave 0  P00–P05  冻结接口、数据和评测合同
             ↓
Wave 1  M10–M14  建立 activation → direction → intervention 显微镜
             ↓
Wave 2  B20–B25  复现单方向基线并通过第一个 Go/No-Go
             ↓
Wave 3  G30–G35  建立 geometry 与 RGRC 测量
          ↙       ↘
Wave 4  D40–D43   T44–T48  构建受控数据并完成三类训练
               ↓
Wave 5  C50–C55  optimization → representation → behavior 因果实验
               ↓
Wave 6  A60–A64  攻击梯度与 Tamper Cost Curve
               ↓
Wave 7  F70–F75  选择一个 defense、复验、第二 backbone
```

同一 wave 内，在依赖满足后可以并行。`B25`、`T48`、`C55` 等决策任务只负责汇总，不应把实现工作重新做一遍。`D40–D43` 在 P04 完成后即可与 Wave 1–3 并行准备，但训练任务仍需通过 B25。

---

# Wave 0：公共合同与工程底座

## P00 — 工程骨架与可复现实验入口

- 状态：TODO
- 预计：0.5–1 agent-day
- 依赖：无
- 独占路径：`pyproject.toml`、`src/refusal_geometry/__init__.py`、`tests/fixtures/`、基础目录
- 工作：建立包结构、统一 CLI 入口、日志目录和最小 toy-model fixture。
- 产物：`python -m refusal_geometry --help` 可运行；一个无需下载大模型的 smoke test。
- 验收：干净环境完成 import、测试和空配置校验；没有模型或数据硬编码路径。

## P01 — Threat model 与安全边界合同

- 状态：TODO
- 预计：0.5 agent-day
- 依赖：无
- 独占路径：`docs/contracts/threat_model.md`
- 工作：定义攻击者是否拥有 weights、训练数据、梯度、推理代码与计算预算；明确本项目优化的是 durability/work factor，不宣称密码学不可绕过。
- 产物：A0–A4 每级攻击权限、预算和成功条件表。
- 验收：每个后续 attack 都能唯一映射到一个级别；列出明确的 out-of-scope 项。

## P02 — Run schema 与 artifact 合同

- 状态：TODO
- 预计：0.5–1 agent-day
- 依赖：P00
- 独占路径：`docs/contracts/run_schema.md`、`src/refusal_geometry/schema.py`、`tests/test_schema.py`
- 工作：定义 `run_id`、model revision、dataset hash、seed、checkpoint、layer、token position、metric version 等字段。
- 产物：JSON schema/dataclass 和配置校验器。
- 验收：缺 seed、数据 hash 或模型 revision 的 run 必须失败；旧结果不可静默覆盖。

## P03 — 指标定义合同

- 状态：TODO
- 预计：1 agent-day
- 依赖：P01
- 独占路径：`docs/contracts/metrics.md`
- 工作：冻结 safety、refusal、over-refusal、benign utility、KL/model drift、`k50`、RGRC-AUC、MTC50 的数学定义和边界情况。
- 产物：指标输入/输出、归一化、置信区间和缺失值规则。
- 验收：给出至少三个手算示例；明确“安全下降 50%”相对哪个 baseline。

## P04 — 数据治理与 split 合同

- 状态：TODO
- 预计：1 agent-day
- 依赖：P01
- 独占路径：`docs/contracts/data_protocol.md`、`data/manifests/schema.json`
- 工作：定义 extraction/train/dev/test/attack/held-out attack 的隔离规则、去重标准、prompt family 分层和数据许可记录。
- 产物：manifest schema、污染检查清单和禁止提交内容说明。
- 验收：同一 prompt/paraphrase family 不可跨关键 split；每条数据能追溯来源与许可。

## P05 — Behavior matching 预注册

- 状态：TODO
- 预计：0.5–1 agent-day
- 依赖：P03、P04
- 独占路径：`docs/contracts/behavior_matching.md`
- 工作：预先确定 matching 指标、容差、checkpoint 选择算法和无法匹配时的处理方式。
- 产物：匹配算法伪代码及 full-trajectory 报告要求。
- 验收：禁止看完 geometry 结果后再改变 matching 规则；匹配失败必须显式报告。

---

# Wave 1：测量显微镜

## M10 — Activation capture 模块

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：P00、P02
- 独占路径：`src/refusal_geometry/capture.py`、`tests/test_capture.py`
- 工作：捕获逐层 residual stream，显式支持 token position、batching、dtype 和磁盘分片。
- 产物：统一 activation artifact，包含 shape、mask、prompt ID、layer 与 token 元数据。
- 验收：同一 seed 重跑数值一致；padding 和变长输入不串位；fixture 测试通过。

## M11 — Refusal direction 提取器

- 状态：TODO
- 预计：1 agent-day
- 依赖：M10
- 独占路径：`src/refusal_geometry/directions.py`、`tests/test_directions.py`
- 工作：实现 harmful/harmless mean difference、归一化、train-only fitting 和方向符号约定。
- 产物：逐层 direction artifact 与 held-out separation score。
- 验收：合成数据恢复已知方向；不得使用 test split 拟合。

## M12 — Activation add/remove hook

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：M10
- 独占路径：`src/refusal_geometry/interventions.py`、`tests/test_interventions.py`
- 工作：实现方向加法、投影消融、top-k 子空间消融和 intervention scope 控制。
- 产物：支持 layer/token/strength 参数的统一 hook。
- 验收：消融后投影分量接近零；strength=0 与原模型一致；hook 可完全卸载。

## M13 — 行为评测适配层

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：P03、P04
- 独占路径：`src/refusal_geometry/evaluation.py`、`tests/test_evaluation.py`
- 工作：统一安全、拒绝、XSTest/over-refusal 和 benign utility 的调用与聚合。
- 产物：逐样本匿名结果和聚合 JSON；记录 evaluator 版本。
- 验收：同一缓存输入重复评分一致；异常与缺失样本不被静默丢弃。

## M14 — 显微镜集成 smoke test

- 状态：TODO
- 预计：0.5–1 agent-day
- 依赖：M10、M11、M12、M13
- 独占路径：`configs/M14_smoke.yaml`、`reports/M14.md`、`runs/M14/`
- 工作：在 toy fixture 和一个小型真实 aligned model 子集上串联 capture、extract、intervene、evaluate。
- 产物：端到端命令、运行时/显存记录和结果 JSON。
- 验收：一条命令可复跑；所有 artifact 符合 P02 schema。

---

# Wave 2：Arditi-style 基线复现

## B20 — Harmful/harmless extraction set

- 状态：TODO
- 预计：1 agent-day
- 依赖：P04
- 独占路径：`data/manifests/B20_*.jsonl`、`reports/B20.md`
- 工作：选择平衡的 harmful/harmless prompts，按主题、长度、模板做匹配，并建立独立 held-out split。
- 产物：manifest、统计表、重复/近重复审计。
- 验收：类别不能被长度、固定前缀或来源数据集轻易区分。

## B21 — Layer separation sweep

- 状态：TODO
- 预计：1 agent-day
- 依赖：B20、M10、M11
- 独占路径：`configs/B21.yaml`、`runs/B21/`、`reports/B21.md`
- 工作：逐层提取方向并测 held-out harmful/harmless separation。
- 产物：`layer → separation` 曲线及候选层列表。
- 验收：报告 extraction split bootstrap CI；候选层选择规则不使用行为干预结果。

## B22 — Layer-wise ablation experiment

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：B21、M12、M13
- 独占路径：`configs/B22.yaml`、`runs/B22/`、`reports/B22.md`
- 工作：对候选层分别做单方向消融，测 safety、over-refusal 和 benign utility。
- 产物：baseline vs ablation 表、layer-effect 曲线。
- 验收：至少有一个 held-out 数据集；报告能力损失而非只报告 refusal 降幅。

## B23 — Steering dose-response

- 状态：TODO
- 预计：1 agent-day
- 依赖：B21、M12、M13
- 独占路径：`configs/B23.yaml`、`runs/B23/`、`reports/B23.md`
- 工作：在固定候选层扫描正负 steering strength。
- 产物：`strength → refusal/safety/utility` 曲线。
- 验收：包含 strength=0；顺序随机化或证明无缓存/批次顺序影响。

## B24 — Direction 稳定性控制

- 状态：TODO
- 预计：1 agent-day
- 依赖：B20、B21
- 独占路径：`configs/B24.yaml`、`runs/B24/`、`reports/B24.md`
- 工作：比较 prompt bootstrap、split、seed、token position 对方向夹角与行为效应的影响。
- 产物：稳定性矩阵和推荐 extraction protocol。
- 验收：结论不能依赖单一 prompt 子集或单个 token position。

## B25 — Go/No-Go 1：基线复现审查

- 状态：TODO
- 预计：0.5 agent-day
- 依赖：B22、B23、B24
- 独占路径：`reports/B25_decision.md`
- 工作：只汇总已有 artifacts，判断显微镜是否可靠。
- 通过条件：方向在 held-out prompts 上稳定；add/remove 有因果效应；正常能力损失有界。
- 未通过动作：回到数据平衡、token position、evaluator 或 intervention 实现，不启动训练矩阵。

---

# Wave 3：Geometry 与 RGRC

## G30 — Activation spectrum 与有效维度

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：B25
- 独占路径：`src/refusal_geometry/spectrum.py`、`tests/test_spectrum.py`、`runs/G30/`、`reports/G30.md`
- 工作：构造 harmful/harmless difference matrix，计算 singular spectrum、stable rank、participation ratio、spectral entropy。
- 产物：逐层 spectrum artifact 和指标表。
- 验收：合成矩阵的 rank 指标正确；报告样本量和中心化/标准化选择。

## G31 — Principal angles 与 Grassmann distance

- 状态：TODO
- 预计：1 agent-day
- 依赖：G30
- 独占路径：`src/refusal_geometry/grassmann.py`、`tests/test_grassmann.py`、`reports/G31.md`
- 工作：实现正交基、principal angles、projection/chordal/geodesic distance。
- 产物：可比较不同 layer/checkpoint/model 的统一接口。
- 验收：对基旋转不变；相同子空间距离为零；正交子空间接近理论值。

## G32 — Layer localization 指标

- 状态：TODO
- 预计：1 agent-day
- 依赖：G30、B22
- 独占路径：`src/refusal_geometry/localization.py`、`runs/G32/`、`reports/G32.md`
- 工作：量化 safety carrier 在层间的集中度、有效层数和因果效应分布。
- 产物：layer concentration/localization score。
- 验收：区分“一个强层”和“多个弱但合计相当的层”；与单纯 stable rank 分开报告。

## G33 — RGRC 与 k50

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：G30、M12、M13、P03
- 独占路径：`src/refusal_geometry/rgrc.py`、`tests/test_rgrc.py`、`runs/G33/`、`reports/G33.md`
- 工作：按预注册顺序扫描消融维度 k，计算剩余安全分数、RGRC-AUC 和 k50。
- 产物：带 bootstrap CI 的 RGRC 曲线和摘要指标。
- 验收：方向排序规则固定；包含 benign utility 约束；未达到 50% 时不伪造 k50。

## G34 — Harmfulness/refusal probe 原型

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：B20、M10、M13
- 独占路径：`src/refusal_geometry/decomposition.py`、`configs/G34.yaml`、`runs/G34/`、`reports/G34.md`
- 工作：用独立 labels/probes 区分 harmfulness recognition 与 refusal execution 表示。
- 产物：逐层 probe、subspace angle 和干预前后结果。
- 验收：probe 使用独立训练/测试 split；不能用输出拒绝字符串充当 harmfulness 真值。

## G35 — Geometry measurement robustness

- 状态：TODO
- 预计：1 agent-day
- 依赖：G30、G31、G32、G33
- 独占路径：`configs/G35.yaml`、`runs/G35/`、`reports/G35.md`
- 工作：改变样本量、中心化、token position、subspace dimension selection，检查指标结论稳定性。
- 产物：敏感性表和推荐默认值。
- 验收：默认参数在看见 objective 对比结果前冻结。

---

# Wave 4A：受控数据

## D40 — 同源 prompt/preference 母集

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：P04
- 独占路径：`data/manifests/D40_*.jsonl`、`reports/D40.md`
- 工作：建立可映射到 SFT、DPO、RL 的共同 prompt ID 和监督来源。
- 产物：母集 manifest、topic/length/severity 分布及 split hash。
- 验收：三种 objective 使用相同 prompt 分布；评测集无泄漏。

## D41 — Low-diversity refusal completions

- 状态：TODO
- 预计：1 agent-day
- 依赖：D40
- 独占路径：`data/manifests/D41_*.jsonl`、`reports/D41.md`
- 工作：构造低前缀/轨迹多样性的安全回复版本。
- 产物：completion manifest 与 diversity 统计。
- 验收：安全语义、长度和质量与 high-diversity 条件尽量匹配；只系统改变 diversity。

## D42 — High-diversity refusal completions

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：D40
- 独占路径：`data/manifests/D42_*.jsonl`、`reports/D42.md`
- 工作：构造多种前缀、论证顺序和安全替代建议的回复版本。
- 产物：completion manifest 与 diversity 统计。
- 验收：prompt ID 与 D41 一一对应；人工抽检或独立 grader 确认质量不劣于 D41。

## D43 — Objective adapters 与数据等价审计

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：D41、D42
- 独占路径：`src/refusal_geometry/data_adapters.py`、`tests/test_data_adapters.py`、`reports/D43.md`
- 工作：将同源样本转换为 SFT records、DPO pairs 和 RL prompt/reward inputs；审计有效样本和主题分布。
- 产物：三个 adapter、转换统计、hash 对照表。
- 验收：转换不会让某个 objective 丢失特定主题；每条训练记录可追溯母集 prompt ID。

---

# Wave 4B：受控训练与行为匹配

## T44 — SFT smoke runs

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：D43、P02、B25
- 独占路径：`configs/T44_*.yaml`、`runs/T44/`、`reports/T44.md`
- 工作：同一 base checkpoint 上训练 low/high diversity SFT，各 1 seed，保存 0/10/25/50/75/100% checkpoint。
- 产物：模型 revision、训练曲线、checkpoint manifest。
- 验收：所有 checkpoint 可加载；日志含 token 数、optimizer steps、学习率和 KL/model drift。

## T45 — DPO smoke runs

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：D43、P02、B25
- 独占路径：`configs/T45_*.yaml`、`runs/T45/`、`reports/T45.md`
- 工作：同一 base checkpoint 上训练 low/high diversity DPO，各 1 seed，并保存同阶段 checkpoint。
- 产物与验收：同 T44；额外记录 reference model、beta 和 pair filtering。

## T46 — RL smoke runs

- 状态：TODO
- 预计：2 agent-days + compute
- 依赖：D43、P02、P03、B25
- 独占路径：`configs/T46_*.yaml`、`runs/T46/`、`reports/T46.md`
- 工作：实现并冻结机制简单的 policy-gradient baseline，训练 low/high diversity 各 1 seed。
- 产物：reward 定义、KL 控制、rollout 配置、checkpoint manifest。
- 验收：reward hacking/长度偏置有检查；训练预算能与 SFT/DPO 明确比较。

## T47 — 全 checkpoint 行为评测

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：T44、T45、T46、M13
- 独占路径：`configs/T47.yaml`、`runs/T47/`、`reports/T47.md`
- 工作：盲于 geometry，对全部 checkpoint 运行统一 safety、over-refusal、utility、KL 评测。
- 产物：长表格式 checkpoint × metric 数据。
- 验收：评测版本一致；失败样本和置信区间完整。

## T48 — Behavior matching 与 Go/No-Go 2

- 状态：TODO
- 预计：1 agent-day
- 依赖：T47、P05
- 独占路径：`runs/T48/`、`reports/T48_decision.md`
- 工作：按预注册规则匹配 SFT/DPO/RL checkpoint，并绘制完整 behavior trajectory。
- 通过条件：至少存在一组 objective × diversity 的可比 checkpoints；匹配不依赖 geometry 结果。
- 未通过动作：调整训练强度或数据，不扩 seeds，不做 objective 几何结论。

---

# Wave 5：机制实验

## C50 — Sample-gradient spectrum

- 状态：TODO
- 预计：2 agent-days + compute
- 依赖：T48
- 独占路径：`src/refusal_geometry/gradients.py`、`configs/C50.yaml`、`runs/C50/`、`reports/C50.md`
- 工作：在固定参数子集/模块上估计 sample-gradient covariance/eigenspectrum；记录近似方法。
- 产物：objective × diversity × checkpoint 的 gradient spectrum。
- 验收：显存可控；近似误差或稳定性经过小样本验证；参数子集在各模型一致。

## C51 — Gradient subspace → refusal subspace

- 状态：TODO
- 预计：1 agent-day
- 依赖：C50、G30、G31、T48
- 独占路径：`runs/C51/`、`reports/C51.md`
- 工作：计算 gradient 与 activation/refusal subspace 的 principal angles，并检验早期 gradient 是否预测最终 geometry。
- 产物：跨 checkpoint 关联与预测表。
- 验收：区分同时测量相关性和时间领先预测；报告 seed/条件不确定性。

## C52 — Cross-objective intervention matrix

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：T48、G30、M12、M13
- 独占路径：`configs/C52.yaml`、`runs/C52/`、`reports/C52.md`
- 工作：分别用 `U_SFT/U_DPO/U_RL` 干预三类 behavior-matched 模型。
- 产物：3×3 causal transfer matrix，按 diversity 分层。
- 验收：self-transfer 与 cross-transfer 使用相同 k、层和强度；同时报告 utility 损失。

## C53 — Checkpoint Grassmann trajectory

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：T47、G30、G31
- 独占路径：`runs/C53/`、`reports/C53.md`
- 工作：追踪 0/10/25/50/75/100% checkpoint 的 subspace path length、速度和转向。
- 产物：trajectory 图与 behavior 同步图。
- 验收：同一 k 选择规则；不把 basis rotation 当作真实移动。

## C54 — Harmfulness/refusal decomposition 主实验

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：G34、T48
- 独占路径：`configs/C54.yaml`、`runs/C54/`、`reports/C54.md`
- 工作：比较不同 objective 改变 detector、refusal policy 还是二者 coupling。
- 产物：probe/subspace/intervention 三类证据。
- 验收：结论至少由一种因果干预支持，不能只依赖线性 probe accuracy。

## C55 — Mechanism decision report

- 状态：TODO
- 预计：1 agent-day
- 依赖：C51、C52、C53、C54、G32、G33
- 独占路径：`reports/C55_decision.md`
- 工作：在 H1 objective、H2 diversity、H3 organization 三条解释中判断当前证据最支持哪一条。
- 产物：预先列明支持/反对证据、效应量、失败实验与 defense lever 排序。
- 验收：只选择一个主 defense 方向；若没有稳定机制信号，停止扩张，不用 topology/MoE“救故事”。

---

# Wave 6：攻击成本

## A60 — 固定 weight orthogonalization baseline

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：B25、P01、P03
- 独占路径：`src/refusal_geometry/attacks/fixed_ablation.py`、`tests/test_fixed_ablation.py`、`runs/A60/`、`reports/A60.md`
- 工作：实现受约束的 residual-writer 正交化和 rank 扫描，保留原权重校验信息。
- 产物：A1 攻击曲线、weight drift、utility 与 safety 指标。
- 验收：只作用于明确列出的模块；可从原 checkpoint 重建；不得覆盖原始权重。

## A61 — Heretic-style 自动搜索适配

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：A60、P01、P03
- 独占路径：`src/refusal_geometry/attacks/search.py`、`configs/A61.yaml`、`runs/A61/`、`reports/A61.md`
- 工作：在固定预算下搜索 layer/component/strength，目标同时包含 safety loss 与 benign-model KL/utility 约束。
- 产物：搜索空间、预算、Pareto frontier 和最佳可复现配置。
- 验收：攻击调参集与最终测试集隔离；搜索预算完整计入成本。

## A62 — Short adversarial fine-tuning baseline

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：T48、P01、P03
- 独占路径：`src/refusal_geometry/attacks/short_ft.py`、`configs/A62.yaml`、`runs/A62/`、`reports/A62.md`
- 工作：在预注册 steps/tokens/learning-rate 网格下做短程 tampering，记录能力与权重漂移。
- 产物：A3 budget → safety/utility 曲线。
- 验收：训练数据与最终 attack test 隔离；禁止只挑最佳 seed。

## A63 — Tamper Cost Curve 与 MTC50

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：A60、A61、A62、P03
- 独占路径：`src/refusal_geometry/tamper_cost.py`、`tests/test_tamper_cost.py`、`runs/A63/`、`reports/A63.md`
- 工作：统一 rank、steps、tokens、compute、weight drift 和 utility penalty，生成分攻击类型的成本曲线。
- 产物：Tamper Cost Curve、MTC50、未达阈值标记和置信区间。
- 验收：不把不同单位直接无解释相加；至少提供原始预算轴和一个预注册归一化轴。

## A64 — Geometry 对跨攻击 durability 的预测

- 状态：TODO
- 预计：1 agent-day
- 依赖：A63、G30、G31、G32、G33
- 独占路径：`runs/A64/`、`reports/A64.md`
- 工作：检验 rank、orientation、localization、RGRC 能否预测 A1/A2/A3 的 MTC50。
- 产物：单变量、增量预测和 leave-one-condition-out 结果。
- 验收：避免在极小样本上宣称泛化；明确区分描述性与预测性结论。

---

# Wave 7：Defense 与复验

## F70 — Defense 选择与预注册

- 状态：TODO
- 预计：0.5 agent-day
- 依赖：C55、A64
- 独占路径：`docs/contracts/defense_preregistration.md`
- 工作：只从 response diversity、subspace dropout、objective mixing、layer redundancy 中选择一个主方案；冻结超参预算和成功标准。
- 产物：选择理由、baseline、公平计算预算和 held-out attack 列表。
- 验收：选择必须由 C55/A64 支持，不能同时开四条 defense 支线。

## F71 — Defense 最小实现

- 状态：TODO
- 预计：1–2 agent-days
- 依赖：F70
- 独占路径：`src/refusal_geometry/defenses/` 中与所选方案同名的单文件、`tests/test_defense.py`
- 工作：实现所选训练干预，确保可开关且不会改变 serving architecture。
- 产物：实现、单元测试、计算开销估计。
- 验收：关闭开关时退化为普通训练；训练时额外开销有记录。

## F72 — Defense pilot

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：F71、T48
- 独占路径：`configs/F72.yaml`、`runs/F72/`、`reports/F72.md`
- 工作：在一个 objective、一个 diversity 条件、一个 seed 上验证训练稳定性和 clean endpoint。
- 产物：clean safety/utility、geometry、RGRC 与训练开销。
- 验收：若 clean safety 或 utility 无法匹配 baseline，先修 defense，不扩 seeds。

## F73 — Defense 主实验

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：F72
- 独占路径：`configs/F73_*.yaml`、`runs/F73/`、`reports/F73.md`
- 工作：扩充预注册 seeds，与等计算量普通训练 baseline 对比。
- 产物：clean metrics、geometry、RGRC、训练成本和 seed-level 结果。
- 验收：clean safety 与 benign utility 匹配；RGRC/k50 提升需报告效应量和 CI。

## F74 — Held-out attack 复验

- 状态：TODO
- 预计：1–2 agent-days + compute
- 依赖：F73、A61、A62、A63
- 独占路径：`configs/F74.yaml`、`runs/F74/`、`reports/F74.md`
- 工作：用未参与 defense 调参的 Heretic-style 配置和 short-FT 条件攻击 defense/baseline。
- 产物：MTC50、Pareto frontier、能力损失与攻击迁移结果。
- 验收：成功标准为 clean endpoint 近似匹配且 MTC50 显著提高；只提高已知攻击上的分数不算完成。

## F75 — 第二 backbone 最小复现

- 状态：TODO
- 预计：2 agent-days + compute
- 依赖：F74
- 独占路径：`configs/F75_*.yaml`、`runs/F75/`、`reports/F75.md`
- 工作：只复制主结论所需的最小条件，不重跑全部 factorial matrix。
- 产物：第二 backbone 上 baseline vs defense 的 clean、RGRC、MTC50 结果。
- 验收：预先规定复制方向与容差；失败结果同样完整报告。

---

# 暂不进入主线的任务

只有在 F74 完成且能加强主结论时再创建具体任务：

- persistent homology 的增量预测；
- LoRA vs full fine-tuning；
- MoE expert-level geometry；
- OrcaRouter/公开 abliterated checkpoint OOD case study；
- Grassmann curvature/phase transition；
- Fisher/information geometry；
- A4 adaptive tampering；
- pretraining-level capability suppression。

这些任务不能用于替代 B25、T48、C55 或 F74 的失败。

# 项目级完成定义

主线完成需要同时满足：

- [ ] 单方向 add/remove 在 held-out prompts 上可复现；
- [ ] SFT/DPO/RL × diversity 存在 behavior-matched 比较；
- [ ] 至少一个 geometry 指标通过因果干预验证；
- [ ] 至少一个 Heretic-style 自动攻击和一个 short-FT 攻击完成；
- [ ] RGRC/k50 与 Tamper Cost Curve/MTC50 可复现；
- [ ] 一个由机制选择的 defense 完成 clean 与 held-out attack 测试；
- [ ] 第二 backbone 至少复验主结论；
- [ ] 所有主结论具有 seed-level 结果、置信区间、失败条件和可复现配置。
