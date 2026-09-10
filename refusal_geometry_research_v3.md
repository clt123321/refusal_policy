# Post-training Objective × Refusal Geometry：研究立项草案 v3

> **核心问题**：在模型、数据和最终安全行为尽可能匹配时，SFT、DPO 与 RL 是否会形成不同的 refusal mechanism？这种差异能否从优化几何解释，并进一步指导一种低成本、可部署、对 Heretic / abliteration 一类 white-box tampering 更耐受的安全训练方法？
>
> **核心比喻**：当前 safety alignment 可能只是给模型装上了一根“容易拔掉的保险丝”。我们不仅要测保险丝有几根、装在哪里，更要理解它为什么容易被拔掉，并训练出多路冗余、难以一次性切断的安全电路。

本文公式均采用纯文本形式，避免依赖 Markdown 的 LaTeX 渲染。

---

## 0. 一句话定位

这不是一篇“再做一个 uncensored model”的论文，而是一篇 **open-weight alignment security / mechanistic interpretability** 工作：

```text
post-training
    ↓
optimization geometry
    ↓
refusal / harmfulness representation
    ↓
white-box tamperability
    ↓
defense design
```

目标不是证明某个模型“拒绝得更多”，而是解释：

> **为什么一些安全机制只需一次低秩权重编辑就能被移除；哪些训练因素决定这种脆弱性；能否用一个简单的训练 recipe 显著提高攻击成本。**

---

# 1. 前提研究现状与研究动机

## 1.1 Safety alignment 到底是什么

Safety alignment 是让模型在保持正常能力的同时，对危险、越权或明显滥用请求执行预期安全策略的一系列方法，包括安全 SFT、preference optimization、RLHF/RL、adversarial training，以及模型外的 moderation / access control。

本项目只研究其中一个狭窄但关键的问题：**安全策略如何被 post-training 写进模型内部，以及拿到权重后有多容易把它改掉。**

需要始终区分：

```text
harmfulness recognition  !=  refusal policy  !=  overall safety
识别“这很危险”               决定“因此拒绝”          完整系统安全
```

已有工作表明 harmfulness representation 与 refusal representation 可以被分离：模型可能仍然知道请求有害，但输出层面的拒绝策略已被破坏。[3]

所以我们的研究对象更准确地叫：

> **post-training 形成的 safety-policy representation，以及它在 open-weight threat model 下的 durability。**

---

## 1.2 从 Arditi 开始：为什么会出现“保险丝”

Arditi et al., NeurIPS 2024 发现，在多个 safety-aligned LLM 中，refusal 行为可以被 residual stream 中一个低维方向强烈介导。[1]

方法极简：对 harmful 与 harmless prompts 记录 activation，计算均值差：

```text
r = mean(harmful activations) - mean(harmless activations)
```

然后做两个因果干预：

```text
从 residual stream 中去掉 r  -> refusal 显著下降
向 residual stream 中加入 r  -> benign prompt 也更容易拒绝
```

更进一步，可以直接修改向 residual stream 写信息的权重矩阵。若 r 已归一化：

```text
W_new = (I - r r^T) W
```

因为任意模块输出为：

```text
y = W x
```

修改后满足近似：

```text
r^T W_new x = 0
```

也就是这个 writer 很难再向 refusal direction 写入信息。

这就是“容易拔掉的保险丝”：危险知识和大部分通用能力仍在，而负责把某些输入映射到“拒绝”的控制通路可能高度集中、低维、可直接编辑。

---

## 1.3 后续工作：保险丝不一定只有一根

ICML 2025 的 *The Geometry of Refusal* 将单方向扩展到多个 functionally independent directions 与 concept cone，并强调：

```text
Euclidean orthogonality  !=  mechanistic independence
```

两个向量数学上正交，不意味着删掉一个不会通过网络非线性影响另一个。[2]

2026 年 *Refusal Geometry Reflects Refusal Training* 又开始回答“为什么会低维”：重复、同质化的 refusal completion 会造成相似梯度，使 activation update 集中到低维子空间；增加 refusal-prefix diversity 可以提高 stable rank，并削弱单向量 ablation。[4]

这形成了一条很自然的链：

```text
training data / objective
        ↓
gradient geometry
        ↓
representation geometry
        ↓
tamperability
```

但该工作比较 OLMo 的 Base -> SFT -> DPO -> RLVR -> Instruct checkpoints 时，objective、data 和 optimization history 同时变化，因此不能隔离 “objective 本身” 的因果作用。[4]

这正是我们的主要空位。

---

## 1.4 OrcaRouter 的 GLM-5.3-Flash：一次大型 white-box 自然实验

OrcaRouter 发布的 GLM-5.3-Flash-Uncensored-FP8 本质上是 Arditi-style weight orthogonalization 在一个 320B-total / 18B-active MoE 上的工程化扩展。[5]

它的算法可压缩为四步：

```text
1. 用 harmful / harmless prompts 跑原模型
2. 在候选层 residual stream 中计算 mean-difference refusal direction r
3. 选择效果最好的 r
4. 对所有关键 residual writers 做 W <- (I - r r^T) W
```

OrcaRouter 的具体实现选择了 45 层中的第 22 层方向，并对 12,479 个 residual-writing matrices 做编辑，包括 attention o_proj、dense/shared MLP down_proj，以及数量最多的 routed MoE expert down_proj。[5]

GLM 原 checkpoint 是 block-FP8，因此其工程流程不是直接修改 FP8 code，而是：

```text
FP8 weight + scale
    ↓ dequantize
FP32 matrix
    ↓ orthogonal projection
edited FP32 matrix
    ↓ requantize
FP8 weight + new scale
```

由于重新量化会把一部分 refusal direction “漏回来”，他们又进行了迭代 refinement。[5]

### 这次攻击到底攻击了什么？

**核心攻击对象确实是 refusal policy，而不是“删除整个安全系统”。**

它没有直接做到：

```text
删除模型对 harmfulness 的识别
删除危险知识
删除外部 moderation
删除 API 权限控制
删除系统层 access control
```

它主要破坏的是：

```text
harmful / sensitive state
        ↓
refusal representation
        ↓
refusal output
```

中的中后段控制通路。

但这仍然严重，因为 refusal 往往是许多 aligned open-weight 模型最终阻止危险能力输出的最后一道模型内 gate。OrcaRouter 的评估显示，大量 harmful benchmark 的 refusal rate 从 90% 左右降到约 10%–30%，而通用 benchmark 变化很小。[5]

换句话说：

> **攻击并没有让模型获得新的危险能力，而是让原本已经存在、但被策略层压住的能力更容易暴露出来。**

同时，GLM 也给出了重要反例：单方向能破坏大部分 refusal，但并不能全部消除；加入第二个方向甚至可能让 refusal 恢复。这说明更深的 safety mechanism 不能简单归结为“多找几根向量继续删”。[5]

---

## 1.5 Heretic：把研究级攻击自动化

Heretic 可以把它看成 **自动化的 refusal-safeguard tampering 工具**。[11]

它不是重新训练模型，而是把 directional ablation 参数化，然后自动寻找“最少拒绝、最小模型损伤”的编辑方案。

其核心仍然是：

```text
A. 每层用 harmful / harmless first-token residuals 估计 refusal direction
B. 对 attention o_proj / MLP down_proj 等 residual writers 做方向正交化
C. 允许不同 layer / component 使用不同编辑强度
D. 用 Optuna/TPE 搜索参数
```

它的优化目标可以抽象为：

```text
minimize:
    RefusalRate(edited model)
    + lambda * KL(edited model || original model) on benign prompts
```

因此 Heretic 的危险之处不只是“它会 abliterate”，而是：

> **它把原本需要懂 Transformer internals 的 white-box attack，压缩成了近乎自动的模型转换过程，并显式优化“安全行为消失、能力尽量保留”的 Pareto frontier。**

这也是为什么我们应该把它视为一种 attack baseline，而不是仅仅一种“模型风格修改工具”。

---

# 2. 研究意义：从解释保险丝，到设计更难拔掉的安全机制

## 2.1 最核心的研究目标

我们最终不是为了回答：

```text
SFT rank = 1.8
DPO rank = 2.7
RL rank = 3.2
```

而是要回答：

> **什么训练条件会形成脆弱的低维 safety control？什么条件会让安全机制分散、冗余、可自恢复，从而提高 Heretic / weight orthogonalization / adversarial fine-tuning 的攻击成本？**

理想的贡献链是：

```text
发现规律
  ↓
提出可解释指标
  ↓
预测攻击脆弱性
  ↓
根据机理设计 defense
  ↓
验证 defense 对未知攻击也更耐久
```

---

## 2.2 “像密码一样上锁”的直觉很好，但要明确边界

一个完全公开的模型若同时满足：

```text
攻击者拥有全部 weights
攻击者可以任意修改 weights
攻击者控制 inference code
```

那么**纯模型内部机制几乎不可能获得密码学意义上的“没有钥匙就无法绕过”保证**。

原因很简单：钥匙、检查逻辑或秘密如果全部存在公开权重/代码里，白盒攻击者最终可以修改或跳过它。

因此 open-weight safety 更现实的目标是 **work factor / durability**：

```text
现在：一次低秩投影即可破坏 safeguard
希望：需要大量训练、数据、计算，甚至以明显能力损失为代价才能破坏
```

真正接近“只有钥匙才能打开”的保证，需要把秘密移出攻击者控制范围，例如远程服务、TEE / secure enclave、远程 attestation、加密权重或其他系统级访问控制；代价是它已经不再是“攻击者拥有完整可自由运行权重”的纯 open-weight threat model。

所以本项目的安全目标应写成：

> **提高 open-weight safeguard 的 tamper cost，而非宣称绝对不可绕过。**

这与 ICLR 2025 的 TAR 以及 safeguard durability 研究的 threat model 是一致的。[9][12]

---

## 2.3 两层指标：几何脆弱性 + 实际攻击成本

### 指标 A：Refusal Geometry Robustness Curve（RGRC）

对前 k 个 refusal directions 张成的子空间 U_k 做：

```text
h_new = (I - U_k U_k^T) h
```

画：

```text
x-axis : ablated dimension k
y-axis : remaining safety score
```

定义：

```text
k50      = 使 safety 降低 50% 所需的最小 k
RGRC-AUC = 整条曲线面积
```

它回答：**模型内的安全控制到底集中在多少个 causal directions 上。**

### 指标 B：Tamper Cost Curve（建议新增）

仅看 k 仍然太理想化。真正攻击还涉及计算、权重扰动、能力损失。

可进一步定义：

```text
x-axis : attacker budget
         (rank edited / FT steps / tokens / weight drift / compute)

y-axis : remaining safety
```

并约束 benign utility 不得下降超过阈值。

可定义：

```text
MTC50 = 在 benign utility 仍合格时，使 safety 降低 50% 的最小攻击成本
```

这样“安全保险丝”就有了近似密码学中的 **work factor** 概念：不是问“理论上能不能拆”，而是问“拆它到底要花多大代价”。

---

# 3. 我们真正要研究的因果链

主假设：

```text
Post-training objective
        +
Response diversity
        ↓
Gradient covariance / spectrum
        ↓
Refusal geometry
(rank + orientation + localization + redundancy)
        ↓
White-box tamper robustness
        ↓
Defense recipe
```

核心 competing hypotheses：

**H1 — Objective 主导。**

```text
same data + same safety endpoint
SFT / DPO / RL 仍形成不同 safety mechanisms
```

**H2 — Data diversity 主导。**

```text
控制 refusal-prefix / trajectory diversity 后
objective 差异显著减弱
```

**H3 — Rank 不是关键，组织方式才是。**

```text
stable rank 相近
但 layer localization / subspace orientation /
functional independence 不同
=> robustness 仍显著不同
```

**H4 — 可训练出更耐篡改的 safety circuit。**

如果脆弱性由单一 carrier / 单一 geometry 导致，那么训练时主动扰动这些 carriers，迫使模型在多个独立路径恢复 safety policy，应提高 Heretic-style attack 的 work factor。

DeepRefusal 已经提供了这个方向的重要先例：训练过程中概率性破坏 refusal direction，迫使模型重建安全机制；其后续项目页还报告了对 Heretic 的额外测试。[10]

---

# 4. Grassmann manifold：如何把“不同保险丝”变成数学对象

## 4.1 从向量到子空间

若 residual stream 维度为 d，refusal 不只由一个方向承担，而需要 k 个方向：

```text
Q = [r1, r2, ..., rk]
R = span(Q)
```

真正有意义的是 R 这个 k 维子空间，而不是某一组具体基向量。

所有 R^d 中的 k 维子空间组成：

```text
Gr(k, d)
```

即 Grassmann manifold。

因此：

```text
一个 checkpoint 的 refusal subspace = Gr(k,d) 上一个点
训练过程                         = manifold 上一条轨迹
不同 objective                   = 不同轨迹 / 不同终点
```

## 4.2 Principal angles：比较两个 safety mechanism

设 SFT 与 RL refusal subspace 的正交基分别为 Q_SFT 与 Q_RL。

对：

```text
Q_SFT^T Q_RL
```

做 SVD，可得到 principal angles：

```text
theta_1, ..., theta_k
```

解释：

```text
theta ~ 0°   -> 两个 subspace 高度重合
theta ~ 90°  -> 两个 subspace 几乎独立
```

这使问题从“两个模型都拒绝 90%”升级为：

> **它们是不是通过同一套内部安全机制实现这个行为？**

## 4.3 Projection matrix 是最漂亮的连接

若 Q 是 refusal subspace 的正交基：

```text
P = Q Q^T
```

P 唯一描述该子空间的正交投影。

而 causal ablation 恰好是：

```text
h_new = (I - P) h
```

因此：

```text
描述 geometry 的对象 P
        =
进行 causal intervention 的对象 P
```

这让 Grassmann geometry 不是数学装饰，而直接连接到实验操作。

---

# 5. 拓扑：作为技术储备，而不是首篇论文的主 novelty

## 5.1 已经被形式化到什么程度

LLM representation topology 常把某层 hidden states 视为高维 point cloud：

```text
X = {h1, h2, ..., hn}
```

对距离阈值逐渐扩大的邻接结构计算 persistent homology，得到：

```text
connected components
loops
higher-dimensional holes
persistence diagrams
Betti numbers
```

TAG-DS 2026 已经用 persistent homology 追踪 alignment fine-tuning 中 representation topology 的变化，并观察到 helpful / harmless / mixed objectives 产生可区分的 topological trajectories。[6]

ACL 2026 Findings 的 Topology-Enhanced Alignment 更进一步，把拓扑结构放进 SFT / DPO objective，而不只是做事后分析。[7]

所以：

> **“LLM representations 有 topology”不是新贡献；真正的新问题必须是 topology 是否具有 causal / predictive safety meaning。**

## 5.2 怎么让拓扑理论可证伪

不要停在“看起来形成了几个洞”。必须形成：

```text
定义对象
  ↓
定义 invariant
  ↓
提出预测
  ↓
做 intervention / OOD validation
```

例如：

> 若 refusal representation 在多尺度上具有更复杂、分散的拓扑结构，则低秩 tampering 应更难破坏 safety。

验证时问：

```text
Topology features
是否在 stable rank + principal angles 之外
继续解释 RGRC / MTC50 的 variance？
```

如果不能，topology 就只是描述性工具；如果能，它才值得升级到主故事。

---

# 6. 文章故事线

### Act I — 现有 safeguard 可能只是一根保险丝

Arditi 与公开 abliteration 工具说明，refusal policy 可以高度低维；Heretic 又把这种攻击自动化。OrcaRouter 的 320B GLM 案例表明，这已不是小模型玩具问题。[1][5][11]

### Act II — 但为什么有的保险丝更容易拔？

已有工作知道 refusal geometry 与训练有关，却还没有严格控制模型、数据和 safety endpoint，回答 SFT / DPO / RL objective 是否因果决定安全机制几何。[4]

### Act III — 做受控 post-training

```text
Objective × Refusal Diversity

             Low diversity   High diversity
SFT               x               x
DPO               x               x
RL                x               x
```

选 behavior-matched checkpoints，避免把“安全强度不同”误认为“机制不同”。

### Act IV — 从 optimization 到 mechanism

```text
gradient spectrum
      ↓
refusal / harmfulness subspace
      ↓
Grassmann trajectory
      ↓
causal ablation / cross-transfer
      ↓
RGRC + Tamper Cost Curve
```

### Act V — 根据机理设计一个简单 defense

如果某种训练条件显著提高 redundancy / MTC50，则把它压缩成一个实用 recipe，例如：

```text
ordinary safety training
+
representation perturbation / subspace dropout
+
response diversity
```

理想结果是只增加少量 post-training 成本，不改 serving architecture，却让 Heretic-style attack 必须付出明显更高的模型扰动或能力损失。

这会把论文从“解释性分析”升级成：

> **mechanism discovery -> metric -> defense。**

---

# 7. 研究方法与核心实验

## RQ1 — Objective effect

行为匹配后，SFT / DPO / RL 是否仍形成不同 refusal subspace？

## RQ2 — Objective vs data

response diversity 能解释多少 objective effect？是否存在 Objective × Diversity interaction？

## RQ3 — Optimization mechanism

gradient covariance / eigenspectrum 是否预测最终 refusal geometry？

## RQ4 — Geometry -> robustness

哪些量真正预测 Heretic-style ablation 与 short adversarial fine-tuning 下的 safety loss？

## RQ5 — Harmfulness vs refusal

objective 改的是“识别危险”，还是“执行拒绝”，还是二者之间的 coupling？

## RQ6 — Defense

在保持 benign capability 的前提下，能否用低成本训练操作显著提高 RGRC 与 MTC50？

---

# 8. 技术路线与实验矩阵

## 8.1 模型

建议：

```text
OLMo-2 ~1B     : 用现成 checkpoint chain 做 observational sanity check
Qwen2.5 1.5B  : 做 controlled full-parameter post-training
```

主实验避免 LoRA，因为 LoRA 本身人为限制 weight-update rank，会污染研究对象。

## 8.2 数据与训练

最小 factorial design：

```text
2 backbones × 3 objectives × 2 diversity levels × 3 seeds
```

资源不足先缩成：

```text
1 backbone × 3 objectives × 2 diversity levels × 2 seeds
```

所有 objective 尽量使用同源 prompt / preference 数据，确保真正比较 objective，而不是数据集。

## 8.3 Behavior matching

训练过程中保存：

```text
0%, 10%, 25%, 50%, 75%, 100%
```

选择满足近似相同：

```text
harmful safety score
XSTest over-refusal
benign utility
KL / model drift
```

的 checkpoints 做机制比较。

## 8.4 Geometry measurements

必测：

```text
stable rank
participation ratio / spectral entropy
principal angles / Grassmann distance
layer localization
harmfulness-refusal subspace angle
checkpoint trajectory
```

## 8.5 Causal tests

```text
single-direction ablation
k-dimensional subspace ablation
activation steering
cross-objective transplantation
```

Cross-objective transplantation：

```text
U_SFT -> attack SFT / DPO / RL
U_DPO -> attack SFT / DPO / RL
U_RL  -> attack SFT / DPO / RL
```

得到一个 3 × 3 causal transfer matrix。

它比单纯 cosine similarity 更强，因为它直接测试“几何相似是否意味着功能可替代”。

## 8.6 Attack ladder

把 threat model 分层，而不是只测一个 Heretic：

```text
A0 activation ablation
A1 fixed refusal-direction weight orthogonalization
A2 automated Heretic-style search
A3 short adversarial fine-tuning
A4 stronger / adaptive tampering（仅在主结论成立后）
```

这样可以研究：

> geometry metric 是否只预测某一种攻击，还是能预测更一般的 safeguard durability？

## 8.7 Defense candidates

**D1 — Response diversity。** 最低成本 baseline。

**D2 — Stochastic subspace dropout / internal perturbation。** 训练时随机削弱当前 refusal carrier，迫使网络建立备份机制；与 DeepRefusal 思路相近。[10]

**D3 — Objective mixing。** 若 SFT / DPO / RL 确实形成互补 subspace，可尝试混合 objective 构造多个 mechanistically distinct carriers。

**D4 — Layer / circuit redundancy regularization。** 若 robustness 主要来自多层 carrier，而不是 rank，可直接鼓励安全信号跨层存在。

**D5 — Pretraining-level capability suppression。** 不是首篇主线，但 Deep Ignorance 表明，如果危险能力根本没有被模型学到，单纯移除 refusal policy 的威胁会下降；代价是训练成本与适用范围更高。[13]

---

# 9. 公开“危险模型”如何加速研究

公开 abliterated / uncensored checkpoints 的正确用途是 **stress test / natural experiment**，而不是主训练数据。

它们提供：

```text
aligned checkpoint
      ↓ known tampering
abliterated checkpoint
```

我们可以验证：

```text
RGRC / MTC50 是否能识别它已被篡改？
哪些 layers / writers 的 geometry 发生了什么变化？
官方模型剩余 refusal 为什么没有被同一攻击移除？
```

尤其 OrcaRouter GLM 可以作为一个重要 OOD case：

```text
single direction effective
+
second direction non-monotonic
+
MoE routed experts dominate writing
```

如果我们的理论只能解释 dense 1B 模型，而解释不了这个案例，它就还不够成熟。

但不建议第一阶段自己处理 306 GiB GLM checkpoint；先用小模型形成规律，再把公开结果作为 external validation。

---

# 10. 后续行动项：每一步为什么存在

> 可并行、可验收的 agent 任务拆分见 [`TODO.md`](TODO.md)。本节保留研究阶段与因果依赖，`TODO.md` 作为执行状态的唯一来源。

## Phase 0 — 读懂研究对象

**读：**

1. Arditi 2024：direction extraction、residual stream、causal add/remove、weight orthogonalization。[1]
2. Geometry of Refusal 2025：subspace / concept cone / functional independence。[2]
3. Harmfulness vs Refusal 2025：识别危险与执行拒绝的解耦。[3]

**目的：**建立统一概念图。

```text
harmful input
   ↓
harmfulness representation
   ↓
refusal mechanism
   ↓
output behavior
```

---

## Phase 1 — 先造出“显微镜”

**实验：**在一个 1B–2B aligned model 上复现 Arditi。

```text
harmful / harmless dataset
      ↓
collect residual activations
      ↓
extract layer-wise directions
      ↓
add / remove direction
      ↓
measure refusal change
```

**必须得到：**

```text
layer -> separation curve
baseline vs ablation refusal
steering strength -> refusal curve
```

**目的：**证明自己的 measurement pipeline 能稳定连接 activation 与 behavior。

---

## Phase 2 — 从 direction 升级为 geometry

**读：**Refusal Geometry Reflects Refusal Training。[4]

**实验：**

```text
SVD spectrum
stable rank
principal angles
layer localization
RGRC
```

**目的：**得到后续比较 SFT / DPO / RL 所需的统一 dependent variables。

---

## Phase 3 — 做真正的 controlled objective experiment

从同一个 base checkpoint 训练：

```text
SFT / DPO / RL
×
Low / High refusal diversity
```

保存多阶段 checkpoint，并做 behavior matching。

**目的：**分离：

```text
objective effect
vs
data-diversity effect
vs
alignment-strength effect
```

---

## Phase 4 — 从现象升级成机制

**实验 A：gradient -> representation**

测 sample-gradient covariance / eigenspectrum，并比较 gradient subspace 与最终 refusal subspace。

**实验 B：cross-objective intervention**

用一个 objective 的 refusal subspace 去干预另一个 objective 的模型。

**实验 C：harmfulness / refusal decomposition**

检查真正变化的是 detector、policy，还是二者 coupling。

**目的：**让论文不止停留在“发现相关性”。

---

## Phase 5 — 引入攻击与 defense

**攻击：**

```text
fixed ablation
Heretic-style automated ablation
short adversarial fine-tuning
```

**指标：**

```text
RGRC
k50
Tamper Cost Curve
MTC50
```

**防御：**从 Phase 3–4 得到的机理中选择最简单的 lever：response diversity、stochastic subspace dropout、objective mixing 或 layer redundancy。

**目的：**完成：

```text
mechanism -> metric -> attack prediction -> defense
```

这是论文最有价值的闭环。

---

# 11. 必做实验与探索性实验

## 必做

1. Arditi-style direction + causal add/remove 复现。
2. Objective × Diversity 受控训练。
3. Behavior-matched checkpoint comparison。
4. Gradient spectrum -> activation spectrum。
5. Principal angles / Grassmann trajectory。
6. RGRC / k50。
7. Cross-objective intervention matrix。
8. Harmfulness / refusal decomposition。
9. 至少一个 Heretic-style automated tampering baseline。
10. 一个由机理直接启发的低成本 defense，并测 MTC50。

## 探索性

- persistent homology 的增量解释力；
- LoRA 是否制造更脆弱的低秩 safety update；
- MoE expert-level safety geometry；
- OrcaRouter GLM OOD validation；
- Grassmann path length / curvature / phase transition；
- Fisher / information geometry；
- 与 TEE / cryptographic system safeguard 的边界讨论。

---

# 12. 时间线与 IF 线

## Week 1–2：measurement pipeline

```text
复现 Arditi
+ layer sweep
+ single / top-k ablation
```

Go / No-Go：若 refusal direction 都无法稳定复现，先修数据、token position、evaluator，不进入训练。

## Week 3–4：controlled dataset + trainer smoke test

```text
Low / High diversity 数据
SFT / DPO / RL 各 1 seed
```

Go / No-Go：必须能找到大致 behavior-matched checkpoint。

## Week 5–7：主实验

```text
seeds
checkpoint trajectory
gradient / activation spectra
Grassmann geometry
```

IF：

```text
objective effect strong -> 主打 objective-induced mechanism
objective weak          -> 主打 data-diversity mechanism
rank weak predictor     -> 转 orientation / localization / redundancy
```

## Week 8–9：attack + causal mechanism

```text
RGRC
cross-transfer
Heretic baseline
short FT tampering
```

## Week 10：defense prototype

只做一个最有机制依据、实现最简单的 defense。

成功标准：

```text
safety endpoint ~= baseline
benign utility ~= baseline
但 RGRC / MTC50 显著提高
```

## Week 11–12：第二 backbone + 写作

只复制主结论，不扩张支线。

---

# 13. 投稿策略

截至 2026-09-10，ICLR 2027：

```text
Abstract deadline : 2026-09-18, 23:59 AoE
Paper deadline    : 2026-09-25, 23:59 AoE
```

不应从零强行赶 ICLR 2027。[8]

更合理的标准是：按主会问题强度设计；如果先得到一个窄但干净的机制发现，可用 mech-interp / AI-safety workshop 获取反馈，再扩展为主会版本。

---

# 14. 最终希望得到的论文贡献

理想版本不是：

> “我们发现 RL 的 stable rank 比 SFT 大 0.7。”

而是：

> **Current safety alignment can behave like an easily removable fuse. We show how post-training objective and response diversity shape the optimization geometry that creates this fuse, identify which geometric properties predict white-box tamperability, and derive a lightweight training intervention that substantially raises the cost of removing safeguards while preserving benign capability.**

中文可以压成：

> **我们研究的不是模型“会不会拒绝”，而是安全策略被写成了什么结构；为什么 Heretic 一类工具可以轻易拔掉这根保险丝；以及如何把它训练成多路冗余、难以低成本切断的安全电路。**

---

# References

[1] Arditi et al. *Refusal in Language Models Is Mediated by a Single Direction*. NeurIPS 2024.  
https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html

[2] Wollschläger et al. *The Geometry of Refusal in Large Language Models: Concept Cones and Representational Independence*. ICML 2025.  
https://proceedings.mlr.press/v267/wollschlager25a.html

[3] Zhao et al. *LLMs Encode Harmfulness and Refusal Separately*. NeurIPS 2025.  
https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html

[4] Labunets. *Refusal geometry reflects refusal training: diverse refusal prefixes can raise stable rank and weaken refusal vector ablation attacks*. arXiv, 2026-08-26.  
https://arxiv.org/abs/2608.25390

[5] OrcaRouter. *GLM-5.3-Flash-Uncensored-FP8 Model Card*. Hugging Face, accessed 2026-09-10.  
https://huggingface.co/orcarouter/GLM-5.3-Flash-Uncensored-FP8

[6] Malhotra et al. *Tracking Representation Dynamics in Large Language Models with Persistent Homology*. TAG-DS 2026.  
https://proceedings.mlr.press/v334/malhotra26a.html

[7] Pan, Xu, Peng. *Topology-Enhanced Alignment for Large Language Models: Trajectory Topology Loss and Topological Preference Optimization*. Findings of ACL 2026.  
https://aclanthology.org/2026.findings-acl.1242/

[8] ICLR 2027. *Call for Papers*.  
https://www.iclr.cc/Conferences/2027/CallForPapers

[9] Tamirisa et al. *Tamper-Resistant Safeguards for Open-Weight LLMs*. ICLR 2025.  
https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html

[10] Xie et al. *Beyond Surface Alignment: Rebuilding LLMs Safety Mechanism via Probabilistically Ablating Refusal Direction*. Findings of EMNLP 2025.  
https://aclanthology.org/2025.findings-emnlp.956/

[11] Philipp Emanuel Weidmann. *Heretic: Fully automatic censorship removal for language models*. GitHub, 2025–2026.  
https://github.com/p-e-w/heretic

[12] Qi et al. *On Evaluating the Durability of Safeguards for Open-Weight LLMs*. ICLR 2025.  
https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html

[13] O'Brien et al. *Deep Ignorance: Filtering Pretraining Data Builds Tamper-Resistant Safeguards into Open-Weight LLMs*. ICLR 2026.  
https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html
