# Post-training Objective × Refusal Geometry

> 研究问题：在模型、数据、最终安全行为尽可能匹配时，SFT、DPO 与 RL 是否会形成不同的拒绝机制；这种差异能否从优化几何解释，并预测安全机制对权重/激活篡改的脆弱性？
>
> **写作核心比喻：当前 safety alignment 可能给模型装上了一根“容易拔掉的保险丝”。我们要研究不同 post-training 方法，是把保险丝做粗了、做成了多路冗余，还是只是换了一个安装位置。**

本文所有公式均使用纯文本表达，不依赖 LaTeX 渲染。

---

## 1. 前提研究现状与研究动机

### 1.1 Safety alignment 是什么，为什么和本项目直接相关

**Safety alignment** 指通过训练或系统设计，让模型在保持正常能力的同时，对危险、越权或潜在滥用请求执行预期的安全策略。SFT、DPO、RLHF/RL、guard model、adversarial training 都属于常见手段。

本项目不研究全部 AI Safety，而研究其中一个足够窄、可以被机制化测量的问题：**refusal policy（拒绝策略）是怎样被 post-training 写进模型内部的。**

必须区分三个对象：

```text
harmfulness recognition  !=  refusal policy  !=  overall safety
识别“有害”                   决定“拒绝”            系统整体安全
```

NeurIPS 2025 的工作已经表明，模型内部的 harmfulness representation 与 refusal representation 可以被分离：模型仍可能“知道请求有害”，但拒绝通道已经被破坏。[3]

因此本项目更准确的定位是：

> **研究 post-training 如何塑造 safety policy 的内部表示几何，以及这种几何是否决定 open-weight safeguard 的可篡改性。**

### 1.2 关键论文线索

**Arditi et al., NeurIPS 2024 — Refusal in Language Models Is Mediated by a Single Direction.**

核心发现：在 13 个开源 chat model、最大 72B 上，refusal 可以被 residual stream 中一个低维方向强烈介导。删除该方向，危险问题更少被拒绝；加入该方向，正常问题也会出现拒绝。进一步可把运行时 activation ablation 转成 rank-one weight edit。[1]

这是“保险丝”直觉的来源：

```text
危险能力仍在
   |
   v
[低维 refusal mechanism]  <- 可能很容易被拔掉
   |
   v
拒绝输出
```

**Wollschläger et al., ICML 2025 — The Geometry of Refusal.**

后续发现 refusal 不一定只有一根方向，而可能包含多个 functionally independent directions，甚至形成 concept cone；并强调“向量正交”不等于“机制独立”。[2]

因此研究对象从：

```text
one direction
```

扩展为：

```text
subspace / cone / nonlinear geometry
```

**Refusal Geometry Reflects Refusal Training, 2026-08-26.**

这是目前离我们最近的工作。它发现，重复的 refusal 开头会让训练梯度与 activation update 集中到更低维的子空间；提高 refusal-prefix diversity 可以提高 stable rank，并让单方向 ablation 更难奏效。[4]

更重要的是，作者观察了 OLMo 的 Base -> SFT -> DPO -> RLVR -> Instruct checkpoints，却明确指出：这些 checkpoint 同时改变了 objective、data 与 optimization history，因此**不能得到“某一种 post-training objective 导致某种 refusal geometry”的因果结论。**

这正是本项目最清晰的研究空位。

### 1.3 OrcaRouter / GLM-5.3-Flash 为什么值得深挖

OrcaRouter 公开的 GLM-5.3-Flash modified checkpoint 是一个很好的大型自然实验。模型卡称其从第 22/45 层的 4096 维 residual stream 提取一个 refusal direction，再对 12,479 个 residual-writing matrices 做正交化处理。[5]

最有价值的不是“成功去掉大量拒绝”，而是它的失败模式：

- 单方向能显著降低 refusal；
- 加第二个方向不一定继续降低 refusal；
- 某些方向组合反而把 refusal 恢复到接近原水平；
- routed MoE experts 是主要 refusal writer。

这直接否定一个过度简单的假设：

```text
higher refusal rank  =>  necessarily more robust
```

更合理的研究对象至少应包含：

```text
dimension + orientation + layer localization + functional independence
```

公开的 uncensored / abliterated checkpoint 可作为 **external stress test**，但不能用于证明 SFT/DPO/RL 的因果差异；主实验必须从同一个 base checkpoint 受控训练。

---

## 2. 研究意义：从行为指标走向机制指标

传统 safety evaluation 主要回答：

```text
模型拒绝了多少？
攻击成功率多少？
是否过度拒绝？
正常能力损失多少？
```

它不能回答：

> **安全行为是通过一根脆弱的“保险丝”，还是多个冗余且分散的内部机制实现的？**

本项目希望建立下面这条因果链：

```text
Post-training objective
        |
        v
Gradient geometry
        |
        v
Refusal representation geometry
        |
        v
Tamper robustness
```

并把 **response / refusal-prefix diversity** 作为关键中介变量，而不是把所有差异都粗暴归因于 objective。

### 2.1 候选新指标：Refusal Geometry Robustness Curve（RGRC）

现有论文经常报告 stable rank，但 “rank = 2.7” 本身并没有直接安全含义。

我们的指标直接问：

> **需要移除多少个独立 refusal directions，安全行为才明显崩溃？**

设前 k 个 refusal directions 张成子空间 U_k，运行时做投影消融：

```text
h_new = (I - U_k U_k^T) h
```

然后画：

```text
x-axis : k，被消融的 refusal directions 数量
y-axis : 剩余 safety score
```

可定义两个摘要量：

```text
k50 = 让 safety score 下降 50% 所需的最小 k
AUC = 整条 ablation curve 的面积
```

它把三件事连接起来：

```text
representation geometry -> causal intervention -> security robustness
```

这比单独比较 stable rank 更有论文价值。

---

## 3. Grassmann manifold：为什么它自然地出现在这个问题里

### 3.1 从“一根方向”到“一个拒绝子空间”

假设 residual stream 是 d 维，例如 d = 4096。

Arditi 的最简单情形是一根 refusal direction：

```text
r in R^4096
```

后续工作提示 refusal 可能需要 k 根独立方向描述。把它们组成矩阵：

```text
Q = [r1, r2, ..., rk]
```

真正重要的并不是 r1、r2 的具体写法，而是它们共同张成的 k 维子空间：

```text
R = span(r1, r2, ..., rk)
```

因为同一个平面可以换无穷多组基。例如二维平面中的两根坐标轴旋转 30°，平面本身没有变。

### 3.2 Grassmann manifold 的定义

**Gr(k, d)** 就是：

> R^d 中所有 k 维线性子空间组成的空间。

因此：

```text
一个模型 + 一个 layer + 一个 checkpoint
              |
              v
       一个 refusal subspace
              |
              v
       Gr(k, d) 上的一个点
```

这一步非常关键：我们不再把 “SFT refusal direction” 和 “RL refusal direction” 当两堆没有结构的向量，而把它们当同一个数学空间上的两个点。

训练过程则变成一条轨迹：

```text
R_0 -> R_1 -> R_2 -> ... -> R_T
```

即 refusal mechanism 在 Grassmann manifold 上随训练移动。

### 3.3 如何测两个 refusal mechanism 是否相似

设两个模型的 refusal subspace 分别由正交基 Q_A、Q_B 表示。

对矩阵 `Q_A^T Q_B` 做 SVD，可以得到一组 **principal angles**：

```text
theta_1, theta_2, ..., theta_k
```

直觉：

```text
theta ~= 0°   -> 两个子空间几乎重合
theta ~= 90°  -> 两个子空间几乎独立
```

于是可以比较：

```text
SFT vs DPO
SFT vs RL
DPO vs RL
```

甚至比较同一模型训练过程：

```text
checkpoint 10% -> 25% -> 50% -> 100%
```

这让一个模糊问题被形式化：

> **两个行为上同样安全的模型，是否把“保险丝”安装在同一个内部位置？**

### 3.4 与其他数学对象的自然联系

**Projection matrix。** 若 Q 是 refusal subspace 的正交基，则：

```text
P = Q Q^T
```

P 是这个子空间唯一对应的投影算子。恰好 causal ablation 使用：

```text
(I - P) h
```

因此“描述几何的数学对象”和“实施因果干预的数学对象”是同一个 P。这是最干净的理论连接。

**Spectral geometry。** 对 harmful / harmless activation difference matrix 做 SVD，奇异值谱描述信息到底集中在前 1–2 个方向，还是平缓分散到很多方向。stable rank、participation ratio、spectral entropy 都可作为描述量。

**Dynamical systems。** 把训练 checkpoint 看作时间 t，refusal subspace `R_t` 是状态。可以研究 path length、移动速度、突然转向，以及安全行为是否伴随几何 phase transition。

**Information geometry。** SFT、DPO、RL 本质上以不同方式改变输出分布。可以进一步研究 policy-space 的 Fisher geometry 与 hidden-space refusal geometry 是否存在联系。这条线理论味很强，适合作为后续，而不是第一版主线。

结论：**Grassmann + spectrum 足以支撑首篇论文；高级数学必须服务于可检验命题，而不能只是包装。**

---

## 4. LLM representation 的拓扑研究：已经知道什么

### 4.1 最常见的形式化：persistent homology

把某一层的一组 hidden states 当成高维点云：

```text
X = {h1, h2, ..., hn}
```

然后不断增大距离阈值 epsilon，把距离足够近的点连接起来。

随着 epsilon 增大，观察：

```text
0-dimensional topology : 有多少个独立连通簇
1-dimensional topology : 是否形成稳定的环
higher dimensions       : 是否存在更高维“洞”
```

一个结构如果只在极短的 epsilon 区间出现，往往视作噪声；如果存在很久，则称为高 persistence structure。所有 birth/death 信息构成 persistence diagram。

### 4.2 现在研究出了什么

TAG-DS 2026 的工作在 1B–7B Transformer 上追踪 alignment fine-tuning，发现：**最大的拓扑重组往往发生在训练早期，随后迅速稳定；helpful、harmless 与 mixed alignment 会形成可区分的 topological trajectories。** 这些内部变化不完全能从普通行为指标看出来。[6]

ACL 2026 Findings 的 Topology-Enhanced Alignment 更进一步，不只是观测 topology，而把 0D persistent homology 产生的全局结构加入 SFT / DPO 的训练约束，并报告相对非拓扑 baseline 的改进。[7]

因此：

> “LLM representation 可以用 topology 描述”已经不是 novelty。

真正仍有空间的是：

> **某种 topological invariant 是否具有 mechanistic / causal meaning，能否预测 safety robustness？**

### 4.3 怎么把“形而上的拓扑描述”变成可证伪理论

一个理论至少需要三步：

```text
1. 定义对象
   hidden-state point cloud / refusal point cloud

2. 定义不变量
   persistence diagram / Betti numbers / topology distance

3. 给出可证伪预测
   topology metric 应预测某个未来或干预后的行为
```

例如可以提出：

> 若 safety representation 更分散、更具有多簇/多尺度结构，则单一低秩 ablation 应更难破坏它。

然后验证：在 SFT/DPO/RL 与不同 diversity 条件下，同时测：

```text
persistent-homology features
stable rank / principal angles
RGRC robustness
```

最后做增量预测：

```text
Does topology explain RGRC variance
beyond stable rank + subspace orientation?
```

若答案是否定的，topology 对本问题只是描述性工具；若显著提升预测力，再值得升级为主线。

这也是为什么首篇论文不应一开始就押注 topology。

---

## 5. 文章故事线

最流畅的 story 不是“我们算了很多几何量”，而是：

### Act I — 一个危险的现象

现有 safety alignment 可能把拒绝策略压缩成一根容易拔掉的“保险丝”；白盒攻击者可以移除 refusal，却保留大部分能力。[1][5]

### Act II — 一个没有被控制的问题

已有研究知道 refusal geometry 与训练有关，也知道 SFT/DPO/RL 会产生不同 representation dynamics，但尚缺少严格实验回答：

> **在模型、训练数据、最终安全行为匹配后，objective 本身是否决定 refusal mechanism？**

### Act III — 受控实验

采用同一 base model、同一 prompts，做：

```text
Objective x Refusal Diversity

             Low diversity   High diversity
SFT               x               x
DPO               x               x
RL                x               x
```

并选择 behavior-matched checkpoints，避免把“更安全”误当成“几何不同”。

### Act IV — 从相关性到机制

测量：

```text
gradient spectrum
      |
      v
refusal subspace / Grassmann trajectory
      |
      v
cross-objective causal ablation
      |
      v
RGRC / tamper robustness
```

### Act V — 结论可以有三种，都能成文

**IF A：objective 主导。**

```text
Same data + same behavior, but SFT/DPO/RL learn different safety mechanisms.
```

**IF B：diversity 主导。**

```text
Data, not objective, determines refusal geometry.
```

**IF C：rank 解释不了 robustness。**

```text
Safety robustness depends on orientation / layer localization /
functional independence rather than dimensionality alone.
```

第三种结果尤其能解释 OrcaRouter/GLM 的非单调 ablation 现象。

---

## 6. 研究方法论与实验设计

### 6.1 核心 RQ

**RQ1 — Objective effect**  
行为匹配后，SFT / DPO / RL 是否仍形成不同 refusal subspace？

**RQ2 — Objective vs data**  
response diversity 能解释多少 objective effect？是否存在 interaction？

**RQ3 — Optimization mechanism**  
gradient covariance / spectrum 是否预测最终 refusal geometry？

**RQ4 — Geometry -> robustness**  
哪些几何量真正预测 causal ablation 与 weight-space tampering 下的 safety loss？

**RQ5 — Harmfulness vs refusal**  
不同 objective 是改变“识别有害”的表示，还是主要改变“执行拒绝”的表示？

### 6.2 模型选型

第一阶段建议两条 backbone：

```text
OLMo-2 ~1B     : 开放训练生态，适合复用现有 checkpoints 做 pipeline sanity check
Qwen2.5 1.5B  : 工程成熟，适合自己做 controlled full-parameter post-training
```

首篇主实验避免 LoRA。因为 LoRA 本身强制低秩 weight update，会污染我们对“训练是否自然产生低秩 refusal geometry”的判断。

LoRA 可以作为探索性对照：

> PEFT 是否会系统性制造更容易拔掉的 safety fuse？

### 6.3 训练条件

最小 factorial design：

```text
2 backbones x 3 objectives x 2 diversity levels x 3 seeds
= 36 training runs
```

若资源不足，先做：

```text
1 backbone x 3 objectives x 2 diversity levels x 2 seeds
= 12 runs
```

确认 effect 后再扩展。

Objective：

```text
SFT
DPO
RL（优先选择机制简单、易控制的 policy-gradient baseline；
    第二阶段再增加 GRPO）
```

数据最好来自同一个 safety/preference dataset family，再人为控制 refusal response diversity，避免三个 objective 使用完全不同的数据分布。

### 6.4 Behavior matching 是必做控制

训练过程中密集保存 checkpoint：

```text
0%, 10%, 25%, 50%, 75%, 100%
```

不要只比较最终 checkpoint。

寻找同时满足下列条件的 checkpoint：

```text
harmful refusal / safety score   ~= matched
XSTest over-refusal              ~= matched
benign utility                   ~= matched
model drift / KL                 ~= approximately matched
```

否则 reviewer 可以合理地说：你比较到的只是 alignment strength，而不是 objective。

### 6.5 核心测量

**Geometry**

```text
stable rank
participation ratio / spectral entropy
principal angles
Grassmann distance
layer-wise localization
harmfulness-refusal subspace angle
```

**Causal tests**

```text
single-direction ablation
k-dimensional subspace ablation
activation steering
cross-objective transplantation
```

其中 cross-objective transplantation 是很有辨识度的实验：

```text
提取 U_SFT  -> 在 SFT / DPO / RL 三个模型上分别消融
提取 U_DPO  -> 同上
提取 U_RL   -> 同上
```

得到 3 x 3 intervention matrix。

若每个 subspace 只攻击自己的模型有效，说明不同 objective 学到 functionally different mechanisms；若高度 cross-transfer，说明存在更普适的 refusal circuit。

**Robustness**

```text
RGRC: safety score vs ablated dimension k
k50
RGRC-AUC
controlled weight perturbation / fine-tuning attack
```

### 6.6 必做实验 vs 探索实验

**必做：**

1. 复现 Arditi-style refusal direction 与 causal add/remove。
2. 3 objective x 2 diversity 的受控训练。
3. behavior-matched checkpoint comparison。
4. gradient spectrum -> activation spectrum 的关联。
5. principal-angle / Grassmann comparison。
6. RGRC。
7. cross-objective intervention matrix。
8. harmfulness vs refusal decomposition。

**探索性：**

- persistent homology 是否提供增量解释力；
- LoRA vs full FT；
- MoE expert-level safety geometry；
- GLM-5.3-Flash / OrcaRouter checkpoint 作为 OOD stress test；
- Grassmann trajectory 的 path length / curvature / phase transition；
- 信息几何或 Fisher metric。

---

## 7. 工程框架、资源与时间预算

### 7.1 工程栈

建议优先减少自研 trainer，把精力放在 measurement：

```text
PyTorch + Transformers
TRL: SFT / DPO / RL trainer
TransformerLens 或自定义 forward hooks: activation capture / intervention
NumPy / SciPy / PyTorch: SVD, principal angles, spectra
HarmBench + XSTest + benign benchmark: behavior evaluation
GUDHI / Ripser.py: 仅在 topology exploratory stage 使用
```

### 7.2 计算策略

第一阶段不要碰 320B GLM。

研究问题本质上是 representation measurement，1B–1.5B 已足够验证因果结构。GLM 公开权重的价值主要是：

```text
large-scale external validation
MoE-specific counterexample
non-monotonic ablation case study
```

而不是首轮训练对象。

### 7.3 12 周建议时间线

**Week 1–2：measurement pipeline**

- 跑通 OLMo/Qwen activation extraction；
- 复现单方向 add / ablate；
- 得到 layer sweep、stable rank、principal angles；
- 先复算一个现有 checkpoint chain，确认工具可信。

**Week 3–4：controlled dataset + SFT/DPO/RL smoke test**

- 构建 low/high refusal diversity；
- 三种 objective 数据尽量同源；
- 先各跑 1 seed；
- 检查是否能实现相似 safety endpoint。

**Week 5–7：主实验**

- 扩 seeds；
- 密集 checkpoint；
- behavior matching；
- gradient / activation spectra；
- Grassmann trajectory。

**Week 8–9：因果实验**

- RGRC；
- cross-objective transplantation；
- harmfulness/refusal separation；
- 小规模 weight-tamper test。

**Week 10：IF 决策**

```text
objective effect strong   -> 主打 objective-induced mechanism
objective effect weak     -> 主打 diversity-induced geometry
dimension weak predictor  -> 主打 functional geometry / localization
```

**Week 11–12：第二 backbone + 写作**

- 只扩展最关键的结论；
- topology / GLM 仅在能加强主故事时加入。

---

## 8. 顶会 deadline 与投稿策略

截至 2026-09-10，ICLR 2027 官方 deadline 为：

```text
Abstract : 2026-09-18, 23:59 AoE
Paper    : 2026-09-25, 23:59 AoE
```

从零启动本项目不应为了 ICLR 2027 强行赶工。[8]

建议：

- **第一目标：把项目按主会质量设计，而不是按 workshop 质量设计。**
- ICML 2027 / NeurIPS 2027 的正式截止日期尚应以官方后续 CFP 为准，本 memo 不提前写死未经确认的日期。
- 若 6–8 周后只有一个清晰但窄的现象，可先投 mech-interp / AI safety workshop 获取反馈，同时保留主会完整版本。

---

## 9. 判断项目是否值得继续的早期门槛

四周内至少应看到下面三个信号中的两个：

```text
A. SFT / DPO / RL 在 behavior-matched 条件下出现稳定的 subspace 差异
B. diversity 操作能可重复地改变 refusal spectrum / RGRC
C. geometry metric 能预测 causal ablation outcome，而不只是相关 behavior score
```

如果三个都没有，就应及时止损；不要靠加入 topology、MoE 或更多模型来“救故事”。

如果出现其中任意两个，项目就值得扩到第二 backbone。

---

## 10. 最终希望得到的一句话贡献

理想版本：

> **Post-training does not merely determine whether a model refuses; it determines how refusal is represented. By controlling behavior and data diversity, we show how optimization geometry shapes the internal safety subspace, and which geometric properties make the resulting safeguard easy—or difficult—to tamper with.**

对应中文直觉：

> **我们不只比较哪种 alignment 更安全，而是研究它把“安全保险丝”装成了什么形状，以及这根保险丝到底有多容易被拔掉。**

---

## References

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
