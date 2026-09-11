# Open-Weight Model Defense: 2026 Landscape Review

**Evidence cutoff:** 2026-09-11
**Scope:** model-internal safeguards for language models released with weights
**Status:** background review, not a project hypothesis or paper story

## Executive assessment

The scientifically defensible target is **not an unremovable safeguard**. If an attacker may replace arbitrary weights, architecture, tokenizer, decoding code, and training data with unbounded compute, no behavior encoded only in the released artifact can be guaranteed to survive. The meaningful empirical target is narrower:

> Under a declared attacker capability, data-access regime, utility constraint, and operational budget, how much does a defense move the best-known safety–utility attack frontier?

This target is reasonable, measurable, and potentially useful, but every result is **attack-family relative**. A failed attack is not a certificate; a successful attack is an upper bound on the cost of breach. The ICLR 2025 durability audit showed why: data shuffling, trainer implementation, schedules, prompt templates, and side-effect measurement can reverse apparent conclusions.[^qi]

Three findings dominate the current landscape:

1. **Post-training refusal is usually an access policy, not capability deletion.** Refusal can be controlled by compact activation/weight interventions, while harmfulness recognition can remain present.[^arditi][^zhao]
2. **Adversarial training buys bounded robustness, not universality.** TAR, RepNoise, Circuit Breakers, DeepRefusal, ReFAT, Triplet/CRL and AntiDote each improve some evaluated frontier, but later adaptive or cross-family attacks expose substantial residual attack surface.[^tar][^cb-critique][^simple][^tamperbench]
3. **Preventing acquisition can be much more durable than suppressing access.** Deep Ignorance's matched 6.9B pretraining runs resist up to 10,000 fine-tuning steps/300M domain tokens, but supplied context and staged fine-tuning-plus-retrieval attacks still restore useful access.[^deep]

The practical conclusion is defense-in-depth: reduce dangerous capability where feasible, harden policy behavior against several non-equivalent perturbation families, and retain system controls when the deployment permits them. Once weights are public, the last layer cannot be assumed.

## 1. Review method and evidence policy

### Search

The review starts from archival proceedings and current arXiv records, then follows author repositories, citations, independent reevaluations, and adjacent work in unlearning, model editing, fine-tuning security, activation attacks, circuit analysis, and pretraining filtering. The priority window is 2024–2026, with 2025–2026 emphasized.

### Source hierarchy

1. Archival paper plus its methods/results/limitations.
2. Current paper version on arXiv for work not yet archival.
3. Official code/model repository as evidence that an artifact exists and what it implements.
4. Independent evaluation for robustness claims.
5. Community tooling only as evidence of a realistic engineering attack, never as peer-reviewed validation.

### Claim labels

- **WE KNOW:** replicated causal intervention, archival multi-model evidence, or direct benchmark evidence with a precisely bounded claim.
- **PLAUSIBLE:** supported by one or more serious studies but not independently established across model/training/attack regimes.
- **SPECULATIVE:** principled hypothesis with no direct discriminating evidence.

These labels apply to claims, not whole papers. Detailed mechanism labels are in [SAFETY_MECHANISM_MAP.md](SAFETY_MECHANISM_MAP.md).

## 2. What counts as a model defense?

Let a released checkpoint be \(M\), a defense procedure be \(D\), an attacker be \(A\), a safety loss be \(S\), useful capability be \(U\), and operational attack cost be \(C_A\). A model-internal defense produces \(M_D=D(M)\) and is evaluated by the strongest discovered attack subject to budget and utility constraints:

\[
R(D;\mathcal A,B,\epsilon)=
\max_{A\in\mathcal A,\,C_A\le B,\,U(A(M_D))\ge U(M_D)-\epsilon}
S(A(M_D)).
\]

This is an **empirical robust-risk estimate**, not the true maximum over all attacks. A useful defense should report the full curve over \(B\) and \(\epsilon\), not one endpoint.

The recommended scope for this project area is:

> **Model-internal, attack-family-general tamper resistance of open-weight models, measured as a utility-constrained increase in attacker work factor, with defender cost and inference overhead disclosed.**

This excludes claims about access control after public release, but permits comparative model-internal research. It also excludes a defense that merely detects that a checkpoint was modified unless detection can be enforced by a trusted runtime.

## 3. Threat-model boundary

| Attacker privilege | Meaningful model-internal question | Impossible or misleading claim |
|---|---|---|
| Prompt/API only | Robust behavior under bounded queries | Open-weight tamper resistance |
| Activation/inference control | Can internal safety be restored/reconstructed under hooks, prefills, decoding changes? | Integrity of any hook the attacker can disable |
| Weight edit | Cost of a direct utility-preserving edit | Permanent refusal guarantee |
| PEFT/full fine-tuning | Samples, steps, FLOPs and wall-clock to cross a safety threshold | Robustness to arbitrary retraining |
| Architecture/tokenizer replacement | Whether capability is absent enough that wrappers cannot restore it | Persistence of a removable module |
| Unbounded retraining/data | Marginal cost versus training an alternative model | Any unconditional model-only guarantee |

The open-weight setting therefore changes the unit of claim from “the model remains safe” to “this released starting point makes a specified misuse adaptation harder.”

## 4. What the literature establishes

### 4.1 Refusal mechanisms are causally manipulable but not uniquely characterized

Arditi et al. showed that adding/removing a residual-stream direction can cause or suppress refusal across 13 chat models, and translated the intervention into a rank-one weight orthogonalization.[^arditi] ICML 2025 Concept Cones finds several causally effective directions and shows Euclidean orthogonality is not functional independence.[^cones] NeurIPS 2025 finds a cross-lingually transferable refusal direction.[^universal] These results jointly establish compact causal control in tested models, not a universal single-vector mechanism.

Separate work identifies sparse neurons, SAE features and circuits that causally affect safe behavior.[^neurons] This does not imply that the cheapest parameter edit is localized at the same component; model-editing work explicitly warns that causal localization and editability can diverge.[^localize]

### 4.2 Recognition, policy and execution can dissociate

NeurIPS 2025 separates a harmfulness direction from a refusal direction: some jailbreak/fine-tuning attacks reduce refusal while leaving latent harmfulness recognition relatively intact.[^zhao] DeepRefusal and Any-Depth Alignment show that generation position matters: early refusal can collapse after an unsafe prefill, while reinjecting safety-associated assistant tokens or training under probabilistic refusal ablation can re-trigger refusal later.[^deeprefusal][^ada]

Thus a refusal-only score conflates at least four objects: detecting harm, selecting a policy, executing a refusal/safe completion, and possessing the underlying task capability.

### 4.3 Weight-space durability is brittle to evaluation choices

TAR uses first-order meta-learning against inner-loop weight tampering and demonstrated large gains in its original bio/cyber experiments.[^tar] RepNoise attempts to erase harmful information throughout layers.[^repnoise] The independent ICLR 2025 audit found both conclusions highly sensitive to attack randomness, trainer, schedules and evaluation formatting.[^qi] This is not evidence that the methods never help; it is evidence that “survives N steps” is not transportable without a full protocol.

TamperBench subsequently standardized 21 models, nine tampering threats, per model–attack hyperparameter sweeps, StrongREJECT, MMLU-Pro, and a 10% utility-loss constraint. Its revised abstract states that current alignment-stage defenses largely fail under sweeps; attack ranking is model-dependent and jailbreak-tuning is often strongest.[^tamperbench] The public toolkit already contains typed attack/defense/evaluation registries and bounded-worst-case aggregation.[^tb-code]

### 4.4 Strong results remain threat-specific

- **DeepRefusal:** about 45 minutes/one A100/one epoch of LoRA training; four 7–8B families; strong results on prompt, prefill and refusal-direction attacks. Its paper explicitly excludes fine-tuning attacks.[^deeprefusal]
- **Any-Depth Alignment:** inference-time safety-token reinjection with negligible reported overhead; broad model-family/prefill results, but an attacker controlling inference can remove the procedure.[^ada]
- **AntiDote (AAAI 2026):** a LoRA hypernetwork proposes adversarial LoRA updates in a bilevel game; ten reported model configurations and 52 red-team attacks; less than 0.5% claimed utility degradation. The method is promising but still author-evaluated, with attack-class generalization left open.[^antidote]
- **ART:** explicitly trains against abliteration and improves abliteration/prefill resistance by 10–20 points when layered onto existing defenses, but the motivating study still finds 16–96% ASR after cheap attacks.[^simple]
- **SEAM/SDD:** intentionally couple malicious fine-tuning to capability collapse. This changes the attacker’s utility tradeoff, but it requires careful verification that an adaptive attacker cannot decouple the trigger or use a new initialization.[^seam][^sdd]
- **Triplet/CRL:** contrastive separation of harmful/benign representations is a strong TamperBench-era baseline, but the paper’s core evaluations are input/embedding attacks and the benchmark still finds nonzero tamper vulnerability.[^triplet][^tamperbench]

### 4.5 Capability removal has the strongest durability evidence—and the highest defender cost

Unlearning studies repeatedly distinguish deletion from suppression. Benign related fine-tuning can revive apparently forgotten content; mechanistic work finds negative “inhibitor” neurons that hide rather than erase knowledge; a TMLR study undoes state-of-the-art unlearning within 16 steps in tested settings.[^relearn][^hide][^tamper-eval]

Deep Ignorance moves the intervention to pretraining. Multiple matched 6.9B models were trained for 550B tokens; filtering used under 1% additional FLOPs and produced far longer resistance to domain relearning than post-training baselines.[^deep] Its limitation is equally important: context/search can supply missing knowledge, and staged attacks defeat tested defense combinations. This is the clearest current evidence for **defense composition**, not a universal solution.

## 5. Defense families and supported scope

| Family | Representative work | What it can currently support | Main unresolved weakness |
|---|---|---|---|
| Alignment strengthening | safety SFT/DPO, Booster, Vaccine | Better initial safety; sometimes slower erosion under matched FT | Cheap direct elicitation/editing; service-controlled assumptions |
| Tamper-aware meta/adversarial training | TAR, AntiDote | Increased cost for trained/nearby update families | adaptive trainer/data/edit mismatch |
| Representation rerouting/reconstruction | Circuit Breakers, LAT, DeepRefusal, ReFAT, Triplet | Transfer across some prompt/latent attacks | direct FT, prefilling, re-extraction, inference disablement |
| Self-degradation/coupled utility | SDD, SEAM | Makes some malicious updates damage utility | attacker may decouple objectives or start elsewhere |
| Weight projection/pruning | SafeLoRA, Antidote (ICML), AMRA | Cheap repair or attack-specific hardening | narrow access/attack family; editable again |
| Capability prevention/removal | unlearning, Safety Pretraining, Deep Ignorance | Less internalized hazardous capability | expensive; context/retrieval/relearning; narrow domains |
| Runtime model-internal control | Any-Depth, decoding steering, latent guard | Low-cost safety while trusted runtime remains | attacker disables runtime component |
| System controls | API moderation, access control, TEE/attestation | Can enforce policy/integrity when trusted boundary exists | outside fully uncontrolled public-weight setting |

See [DEFENSE_TAXONOMY.md](DEFENSE_TAXONOMY.md) and [DEFENSE_EVIDENCE_TABLE.csv](DEFENSE_EVIDENCE_TABLE.csv) for normalized cards.

## 6. Cost: what should be measured

### 6.1 Do not lead with dollars

Dollar cost is hardware-region-contract-time dependent and quickly becomes stale. Report it only as a dated secondary conversion. Primary cost fields should be:

- model parameters and trainable parameters;
- training/evaluation tokens;
- forward and backward passes;
- measured GPU-hours by hardware and precision;
- estimated training FLOPs with the formula disclosed;
- peak accelerator memory and storage;
- inference latency/throughput and memory overhead;
- human/API judging cost;
- hyperparameter-search trials, including failed/censored runs.

### 6.2 Relative quantities

Recommended normalized measures:

\[
C_D^{rel}=\frac{\text{defense FLOPs}}{\text{original post-training FLOPs}},\qquad
A(B,\epsilon)=\frac{C_{breach}^{defended}}{C_{breach}^{base}}.
\]

Also report a **defense leverage curve**, not one scalar:

\[
L(B,\epsilon)=\frac{C_{breach}^{defended}-C_{breach}^{base}}{C_D+C_{infer}(N)}.
\]

Here \(N\) is expected lifetime inference volume. A method with nonzero per-token overhead may look cheap in training and expensive in deployment.

### 6.3 What is currently known

- DeepRefusal reports one A100-80GB, about 45 minutes per 7–8B model.[^deeprefusal]
- Vaccine reports roughly 2× alignment-step wall time and about 0.11GB additional memory in its setup.[^vaccine]
- AntiDote reports 0.69/1.97/3.17 hours for 3B/7B/12B configurations and 32.4/51.2/73.6GB peak memory, but these are author-side, setup-specific comparisons.[^antidote-cost]
- TAR’s official code recommends 8×A100-80GB for an 8B full-parameter implementation and does not provide a portable dollar cost.[^tar-code]
- Deep Ignorance’s filter itself is under 1% of pretraining FLOPs, but the retrofit question is unfavorable: validating the intervention required matched 550B-token pretraining runs.[^deep]

Claims such as “under $5” are only meaningful when the hardware, region, model, precision, token count, search budget and excluded human/API costs are fixed. For scientific comparison, model-token-equivalent FLOPs are preferable.

## 7. Is a general defense possible?

### Unconditional model-only defense: no meaningful guarantee

An attacker who can arbitrarily replace weights or train another model can remove any behavior stored solely in the artifact. This is a threat-model observation, not a formal impossibility theorem about all safeguards. A paper should state the boundary explicitly rather than advertise “unbreakable.”

### Attack-family-general robustness: plausible and testable

Training against one perturbation may transfer when several attacks exploit the same functional weakness. DeepRefusal reports transfer from refusal-ablation training to unseen prompt attacks; Triplet transfers across input and embedding attacks; smoothness/invariance objectives improve some unseen downstream fine-tuning resistance.[^deeprefusal][^triplet][^sam][^irm] But Circuit Breakers’ independent evaluation and the 2026 simple-attack study show why transfer must be tested adversarially, not assumed.[^cb-critique][^simple]

### Defense-in-depth: strongest current position

The most credible stack is heterogeneous:

1. prevent acquisition where a narrow high-risk capability can be filtered;
2. robustly couple recognition to safe action and reconstruct it across token/layer depth;
3. train against several weight/activation/update families;
4. make breach trade off against useful capability;
5. retain trusted runtime/access controls where possible.

This is not proof of compositional robustness. Deep Ignorance reports a staged attack that defeats tested filtering-plus-post-training combinations, so interactions must be evaluated rather than added rhetorically.[^deep]

## 8. What the best current defenses do—and do not show

There is no defensible single “winner” across all objectives.

- For **retrofit refusal robustness**, AntiDote, TAR and Triplet are serious baselines, with TamperBench currently the most comparable public evaluation substrate.
- For **cheap prompt/activation robustness**, DeepRefusal is attractive because its reported defender cost is low, but it is not a fine-tuning defense.
- For **dangerous capability durability**, Deep Ignorance has the strongest long-horizon evidence, but it is pretraining-time, domain-specific and bypassable with supplied context.
- For **adaptive-evaluation credibility**, the negative results in the durability audit and TamperBench are more important than any single headline score.

The field’s largest gap is not another refusal metric. It is a controlled, attack-blind, cost-accounted comparison that spans at least one prompt/prefill, one activation, one direct edit, and one fine-tuning family while measuring actual task capability and benign utility.

## 9. Review limitations

- Many 2026 papers are recent preprints with no independent replication.
- Compute reporting is inconsistent; `NR` in the evidence table means not reported or not verified, not zero.
- Safety endpoints are heterogeneous: refusal rate, harmfulness judges, WMDP accuracy and domain task success are not interchangeable.
- “52 attacks” can include variants within a shared inductive bias; attack count is not threat-space coverage.
- Published models are mostly 1–12B dense transformers; MoE, reasoning-model and multimodal generalization remains thin.

## Sources

[^arditi]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^cones]: Wollschläger et al., [*The Geometry of Refusal in Large Language Models*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^universal]: Wang et al., [*Refusal Direction is Universal Across Safety-Aligned Languages*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/2e94772e3c079d83f79c311d07456111-Abstract-Conference.html), NeurIPS 2025.
[^neurons]: Chen et al., [*Towards Understanding Safety Alignment: A Mechanistic Perspective from Safety Neurons*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html), NeurIPS 2025.
[^zhao]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^localize]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^tar]: Tamirisa et al., [*Tamper-Resistant Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^repnoise]: Rosati et al., [*Representation Noising*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/172be8b0b88fc2b4aee74237d43f8c04-Abstract-Conference.html), NeurIPS 2024.
[^qi]: Qi et al., [*On Evaluating the Durability of Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^tamperbench]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^tb-code]: CriticalML, [TamperBench official repository](https://github.com/criticalml-uw/TamperBench), inspected at commit `ca4fade`.
[^deeprefusal]: Xie et al., [*Beyond Surface Alignment / DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings of EMNLP 2025.
[^ada]: Zhang et al., [*Any-Depth Alignment*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^antidote]: Sanyal et al., [*AntiDote: Bi-level Adversarial Training*](https://ojs.aaai.org/index.php/AAAI/article/view/40570), AAAI 2026.
[^antidote-cost]: Sanyal et al., [AntiDote paper PDF](https://ojs.aaai.org/index.php/AAAI/article/download/40570/44531), Table 3.
[^simple]: Kuo et al., [*Open-Weight LLM Fine-Tuning Defenses are Susceptible to Simple Attacks*](https://arxiv.org/abs/2605.26526), arXiv 2026.
[^seam]: Wang et al., [*Self-Destructive Language Models*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1abb0e7bd62ba80610798dee81950522-Abstract-Conference.html), ICLR 2026.
[^sdd]: Chen et al., [*SDD: Self-Degraded Defense*](https://aclanthology.org/2025.acl-long.1412/), ACL 2025.
[^triplet]: Simko et al., [*Improving Large Language Model Safety with Contrastive Representation Learning*](https://arxiv.org/abs/2506.11938), 2025 preprint / EMNLP 2025 paper.
[^cb-critique]: Schwinn & Geisler, [*Revisiting the Robust Alignment of Circuit Breakers*](https://arxiv.org/abs/2407.15902), 2024 preprint.
[^vaccine]: Huang et al., [*Vaccine*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/873c86d9a979ab80d8e2919510d4446b-Abstract-Conference.html), NeurIPS 2024.
[^tar-code]: Tamirisa et al., [TAR official repository](https://github.com/rishub-tamirisa/tamper-resistance), inspected at commit `19de233`.
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^relearn]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^hide]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^tamper-eval]: Che et al., [*Model Tampering Attacks Enable More Rigorous Evaluations of LLM Capabilities*](https://openreview.net/forum?id=E6OYbLnQd2), TMLR 2025.
[^sam]: Fan et al., [*Towards LLM Unlearning Resilient to Relearning Attacks*](https://proceedings.mlr.press/v267/fan25e.html), ICML 2025.
[^irm]: Wang et al., [*Invariance Makes LLM Unlearning Resilient*](https://proceedings.mlr.press/v267/wang25en.html), ICML 2025.
