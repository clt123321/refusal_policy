# Round 2.5 — Fail-Closed Novelty Audit

## Executive verdict

`ROUND2_5_VERDICT = REFINE`

Fail-Closed is a **fatal collision** for the story “create several independent refusal directions and obtain fail-closed safety.” It is **not** a fatal collision for the narrower question of whether operator-specific activation fault tolerance predicts adaptive parameter-space fault tolerance. The project therefore changes from a proposed redundancy defense to a cross-space diagnostic study. No novel defense algorithm is authorized before that diagnostic produces a specific failure mechanism.

> **Open problem:** Does tolerance to a registered activation intervention predict the work required for adaptive, utility-preserving parameter tampering, or can the two orderings dissociate?

## 1. Evidence inspected

This audit used the February 19, 2026 arXiv v1 paper and appendices, the official code repository at commit `892e99b2db2c98f4ecd9b81e414088e15ae7f035`, and the four checkpoints in the authors' Hugging Face collection. Fail-Closed is currently an **arXiv preprint**; the HTML keyword “ICML” is not evidence of conference acceptance.[^fc-paper]

The source repository is MIT licensed, contains the trainer, RDO/DIM extraction, utility and over-refusal evaluation, model-specific generated training data, and fixed software versions. It does **not** contain the paper's HarmBench attack runner, exact published attack artifacts, selected-checkpoint manifest, direction tensors, per-run logs, seeds beyond the hard-coded seed 42, or a script that reproduces every table. The authors instead refer users to HarmBench.[^fc-code]

The four released full-weight checkpoints are public and ungated, but their generated model cards leave license, base model, training recipe, evaluation, hashes of training data and limitations unspecified. The code license does not license the model weights; downstream use must respect the relevant Llama or Gemma terms.[^fc-models]

## 2. Q1 — Novelty overlap

| Claim | Fail-Closed | Our proposed question | Overlap |
|---|---|---|---|
| Multiple refusal directions | Iteratively extracts up to ten orthogonalized RDO directions; at least five can induce refusal in Llama-3-8B | Not a contribution; only a measured antecedent | **FATAL_COLLISION** |
| “Causal independence” | Direction addition can induce refusal; cumulative removal of learned directions leaves refusal intact. Orthogonality is imposed during extraction | Does not claim natural pathway independence; operationalizes only fault tolerance to a registered operator | **FATAL_COLLISION** for broad redundancy language; **CLEAR GAP** for prospective cross-space prediction |
| Activation redundancy | Trains while cumulatively ablating previous directions; all ten can be removed with only 1% ASR on one analyzed model | Treats redundancy as a candidate explanatory variable, not the endpoint | **FATAL_COLLISION** |
| Activation-level fault tolerance | Tests DIM/RDO residual-stream ablation and safety-neuron activation ablation | Reproduce as the left side of a cross-space comparison | **FATAL_COLLISION** |
| Prompt-jailbreak robustness | Tests GCG, AutoDAN, PAIR and HumanJailbreaks on four 2–9B models | Orthogonal control, not primary white-box endpoint | **FATAL_COLLISION** |
| Direct parameter-edit robustness | Not evaluated | Tests defended-model-specific directional/low-rank edits and automated abliteration | **CLEAR_GAP** |
| Malicious fine-tuning robustness | Not evaluated; LoRA is used to *train the defense*, not attack it | Tests harmful/jailbreak LoRA and short full fine-tuning | **CLEAR_GAP** |
| Adaptive white-box parameter robustness | “White-box” in the paper means gradient-informed **prompt** search; no defense-aware weight attacker | Attacker knows the defense and re-extracts/re-optimizes against each checkpoint | **CLEAR_GAP** |
| Activation fault tolerance predicts parameter fault tolerance | Not asked or tested | Primary scientific question | **CLEAR_GAP** |
| Utility-qualified parameter breach cost | Neuron ablation reports an ASR–accuracy frontier; no parameter-attack work ledger | Minimum found attack work subject to per-domain utility and over-refusal constraints | **PARTIAL_COLLISION** on endpoint shape; **CLEAR_GAP** on parameter attack and work factor |

### What Fail-Closed actually establishes

The method applies a QR-derived multi-feature projection at every layer and token position on harmful training inputs, then trains a refusal target while preserving benign outputs using KL. It reports four prompt-attack results across Llama-2-7B, Llama-3-8B, Gemma-2-2B and Gemma-2-9B, plus DIM/RDO feature ablation and neuron-ablation frontiers. The average clean utility drop is reported as 0.8 percentage points; average benign compliance is 86.4%. Training costs about two forward and two backward passes per step, excluding amortized RDO, for ten epochs.[^fc-paper]

The mechanism evidence is meaningful but narrower than the wording “independent causal pathways” suggests:

- Euclidean independence is imposed by projection; it is not discovered functional independence.
- Addition shows that several directions are individually sufficient to trigger some refusal, but not that they correspond to disjoint computations.
- Cumulative ablation showing continued refusal establishes fault tolerance to that operator. It does not show that the surviving computation is a distinct parameter fault domain.
- Directions 6–10 have near-zero measured activation; the authors explicitly suggest later safety may be nonlinear and leave it unresolved.
- The same all-layer/all-token projection family is used during training and feature-ablation evaluation, although DIM provides a useful extraction-method holdout.
- Checkpoint selection uses prompt-jailbreak ASR over all iterations, so its headline prompt result includes selection on related post-treatment outcomes.

This is enough to reject our former “many writers/fail-closed redundancy” novelty, but not enough to infer parameter-space security.

## 3. Comparison with the nearest work

| Work | What it already settles | Parameter-tampering coverage | Remaining relevance to our question |
|---|---|---|---|
| **DeepRefusal** (Findings EMNLP 2025) | Refusal can be reconstructed under probabilistic direction faults across layers/tokens; transfers to prompt/prefill attacks | Explicitly excludes fine-tuning attacks | Nearest reconstruction baseline; generic fault-injection training is not novel[^deep] |
| **HARC** (arXiv 2026) | Separates and couples harm recognition/refusal at prompt and response positions | Appendix reports collapse after roughly 160 harmful FT examples | Natural negative example: activation mechanism improves prompt safety but is not durable under FT[^harc] |
| **TAR** (ICLR 2025) | Meta-trains safeguards against bounded parameter-update trajectories | Yes: malicious full-parameter fine-tuning; later audits find schedule sensitivity | Security baseline and evaluation precedent; it does not test activation-path independence as an explanation[^tar] |
| **AntiDote** (AAAI 2026) | Bilevel training against activation-conditioned adversarial LoRA; broad reported red-team suite | Yes: learned LoRA/direct weight families, conditional on its inner attacker | Strong low-cost tamper-aware baseline; fatal to generic bilevel-defense novelty[^antidote] |
| **Skin-Deep** (arXiv 2026) | Proposes a pre-attack geometry score for benign rank-8 LoRA fragility | One bounded benign-LoRA setting | Any predictor must beat GFS prospectively; scalar geometry alone is not our novelty[^skin] |
| **TamperBench** (KDD 2026 D&B) | Standardizes pair-specific attack search and utility-constrained worst-found robustness | Nine attack families over 21 models; attack ranking is model-specific | Harness substrate and security endpoint; fatal to a new benchmark-only contribution[^tb] |
| **Refusal Geometry Reflects Refusal Training** (arXiv 2026) | Refusal-prefix diversity raises gradient/activation stable rank and weakens one vector ablation in an OLMo-2-1B case study | No malicious FT, Heretic or multi-operator parameter attack | Rank/diversity are controls, not a new defense or security certificate[^rgrt] |
| **Fail-Closed** (arXiv 2026) | Multiple causally active directions, cumulative direction-fault tolerance and prompt robustness | No direct edit, malicious FT or adaptive weight attack | Supplies the strongest public cross-space natural experiment[^fc-paper] |

The combined literature leaves a narrow but real gap: tamper-resistance work measures parameter attacks without testing whether a preregistered activation-fault response predicts outcomes, while mechanism work constructs activation redundancy without defense-aware parameter tampering.

## 4. Q2 — Public-checkpoint natural experiment

### Candidate checkpoint ledger

| Field | Recommended pair | Notes |
|---|---|---|
| Model family | Gemma 2 | Also released: Llama-2-7B, Llama-3-8B and Gemma-2-9B |
| Baseline checkpoint | `google/gemma-2-2b-it` | Exact base named by paper/code |
| Defended checkpoint | `ztcoalson/gemma-2-2b-it-FC@03fb41ec87b9ba82c690b60331e5c60b67f6b106` | Full BF16 weights; 2,614,341,888 parameters; 5.27 GB stored |
| Training recipe | Ten-epoch full-parameter safety training under cumulative RDO-direction ablation plus benign KL, batch 32, LR `5e-6`, λ=1 | This describes the paper's main recipe; the sparse model card does not independently bind the released artifact to a run manifest |
| Availability | Public and ungated on 2026-09-11 | Base-model terms may still require acceptance for a clean baseline download |
| License | Code: MIT. Released weight card: unspecified. Base: Gemma terms | Do not infer MIT for weights or redistribute them |
| Reproducibility | **Moderate for inference; low–moderate for exact training/table replication** | Fixed code/data exist, but no table runner, attack artifacts, selected-run manifest or complete model card |
| Published base metrics | average prompt ASR 54.8%; benign CR 97.8%; utility accuracy 61.2%; DIM/RDO ablation ASR average 92.0% | Six zero-shot utility tasks; XSTest + Alpaca compliance |
| Published defended metrics | average prompt ASR 1.7%; benign CR 92.6%; utility accuracy 60.3%; DIM/RDO ablation ASR average 0.8% | All are author-reported and must be reproduced before interpretation |
| 8×A800 fit | **High** for inference and bounded attacks | 2.6B BF16 is the cheapest pair; trials can be parallelized. This is an engineering estimate, not a completed run |

### Minimal natural experiment — no defense training

1. **Artifact pinning:** pin the two model revisions, tokenizer/chat template, generation parameters, HarmBench commit, data splits and evaluator versions. Record legal access and hashes.
2. **Author-result check:** reproduce clean/no-attack ASR, six-task accuracy, XSTest/Alpaca compliance, DIM ablation and RDO ablation. Attempt a small fixed subset of one prompt jailbreak only as a qualitative ordering check; do not spend the first run recreating the whole paper.
3. **OAFT verification:** independently re-extract at most ten directions and apply the same all-layer/all-token projection family. Test addition, cumulative removal and rescue on disjoint prompts. Report “fault tolerance under operator O and discovered set P”; do not equate QR orthogonality with natural pathway independence.
4. **Attack family A:** re-extract an Arditi-style direction per checkpoint and apply the corresponding directional weight orthogonalization/rank-constrained direct edit. Sweep strength and rank under a frozen search budget.
5. **Attack family B:** run Heretic or a compatible automated abliteration search with target-specific layer/component selection and benign-KL penalty.
6. **Independent parameter biases:** run malicious/jailbreak LoRA plus the unconditional fixed-budget full-FT sentinel, and separately test sparse structured MLP/channel removal or scaling. A1/A2 count as one family; an embedding attack is only a distinct-bias control.
7. **Outcome:** for each family, plot harmful-task success against each benign utility domain, over-refusal and cumulative attack FLOPs/GPU-seconds. Report the first observed utility-qualified breach as interval/right-censored—not as a global minimum.
8. **Blinding:** freeze mechanism labels and attack budgets before parameter-attack results are revealed. Use the same search allocation per checkpoint; allow checkpoint-specific adaptation inside that allocation.

Interpretation is deliberately asymmetric:

- **A:** activation tolerance ↑ and parameter breach work ↑ — redundancy may contribute to durability; still not causal because the checkpoints differ by an entire training recipe.
- **B:** activation tolerance ↑ and parameter breach work ≈ baseline — direct cross-space dissociation and the cleanest paper-worthy counterexample.
- **C:** activation tolerance ↑ and parameter breach work ↓ — ranking reversal; strongest evidence that activation redundancy can create or coexist with a parameter common cause.
- **D:** published activation/behavior result cannot be reproduced — stop; repair artifacts/evaluators before any novelty claim.

This is a screening contrast, not an identified treatment effect. Extra safety training, data, KL, alignment strength and checkpoint selection all differ. It can expose a counterexample or motivate a mechanism; even Case A cannot establish a relationship. Confirmation requires independent final checkpoints from matched training conditions.

## 5. Q3 — Did Fail-Closed already survive parameter attacks?

No. The paper's white-box GCG and AutoDAN optimize **input tokens**, its direction intervention changes **runtime activations**, and its neuron analysis zeros **neuron activations**. The LoRA section trains the defender; it does not use LoRA as an attack. The official repository contains no malicious-FT/direct-edit attack implementation and delegates prompt attacks to HarmBench.

Therefore `PRIMARY_BET_REJECTED` is **not** triggered. The admissible claim is narrowed to:

> Fail-Closed establishes activation-level redundancy under specified interventions; we test whether that ordering transfers to independently optimized, utility-constrained parameter attacks and explain any disagreement.

If a later version or hidden artifact demonstrates defense-aware direct edits, malicious LoRA/full FT and a utility-qualified cost frontier, novelty must be re-audited before execution. If it also connects activation independence to those outcomes with held-out attacks, the primary question is abandoned rather than renamed.

## 6. Operational definitions admitted to Round 3

### Operator-specific activation fault tolerance

For a preregistered operator `O`, extraction rule, maximum discovered set `K`, token/layer scope and held-out distribution, OAFT is the safety retained as increasingly many extracted components are removed while utility and generation-validity sentinels remain satisfied. It is an intervention response curve, not a count of natural pathways. V4 uses RDO initialized by DIM, at most ten directions and orthogonal projection at all transformer layers and token positions; no `K` is chosen after sealed outcomes.

### Causal pathway independence

This stronger term is reserved for localized computations with separately sufficient effects, subset-specific failure and pathway-specific rescue. QR directions, orthogonality, probe accuracy and direction count do not qualify. The primary study does not require or claim it.

### Parameter fault independence

Adversarial parameter fault tolerance at budget `B` is the absence of a utility-qualified breach by the registered, defense-aware parameter portfolio through `B`, together with the first-passage cost when breached. “Independent parameter faults” additionally requires at least two intervention biases—directional/low-rank versus gradient-update or sparse-structured—whose construction and optimization were not used to define OAFT. This is empirical and censored, never a certificate.

### Utility-preserving breach

A checkpoint is breached when preregistered actual harmful-task success crosses threshold `q`, every required benign domain retains at least `1-δ` of its clean score (with absolute floors where ratios are unstable), and over-refusal/compliance remains within its bound. Prefix changes or refusal-keyword disappearance alone are insufficient. Headline thresholds are frozen before attack results; alternative thresholds are sensitivity curves.

### Independent attack

An attack is independent when its intervention operator and objective were not used to train, select or tune the defense or the mechanism score, and its test data remain sealed until configs and budgets are frozen. Sharing a generic optimizer is allowed; a differently named attack sharing the same intervention bias and objective is not an independent family.

### Adaptive attacker

The attacker knows weights, architecture, defense, code, metrics and the non-secret evaluation protocol; may re-extract directions, select layers/modules/rank, retune objectives and optimization within a preregistered resource envelope; and is evaluated on held-out prompts. “Adaptive” never means unlimited, and a failed attack only establishes non-breach within that envelope.

## 7. Design changes forced by this audit

- **Delete as novelty:** “many writers,” fail-closed activation redundancy, direction reconstruction and higher stable rank.
- **Downgrade to diagnostics:** writer count, stable rank, principal angles, Fisher concentration and local Jacobian coupling.
- **Do not freeze:** fixed disjoint layer bands, predefined sensitivity-separation losses, a writer-cut matrix or any custom defense implementation.
- **Delete:** the arbitrary `writer-cut × (1-CC)` composite score. Security is represented by attack–utility–cost frontiers; mechanism measurements compete prospectively as predictors.
- **Retain only as a principle:** a durable defense should create failure domains that remain costly to disable jointly under adaptive parameter access. The method must be derived from an observed failure, not selected in advance.
- **First experiment:** public baseline versus Fail-Closed checkpoint as screening. A matched 32-checkpoint panel and the full Skin-Deep GFS baseline are required before a paper-level predictive claim. Diagnosis precedes intervention.

## Sources

[^fc-paper]: Coalson et al., [*Fail-Closed Alignment for Large Language Models*](https://arxiv.org/abs/2602.16977), arXiv v1, 19 February 2026; especially §§3–4 and Appendices A–C.
[^fc-code]: Coalson et al., [official code](https://github.com/ztcoalson/Fail-Closed-Alignment), inspected at `892e99b2db2c98f4ecd9b81e414088e15ae7f035`; MIT License.
[^fc-models]: Coalson et al., [official checkpoint collection](https://huggingface.co/collections/ztcoalson/fail-closed-alignment), inspected 11 September 2026.
[^deep]: Xie et al., [*Beyond Surface Alignment / DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings of EMNLP 2025.
[^harc]: Chua and Wu, [*HARC*](https://arxiv.org/abs/2607.00572), arXiv v3, 2026.
[^tar]: Tamirisa et al., [*Tamper-Resistant Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^antidote]: Sanyal et al., [*AntiDote*](https://ojs.aaai.org/index.php/AAAI/article/view/40570), AAAI 2026; [official code](https://github.com/respailab/Antidote).
[^skin]: Lee et al., [*Skin-Deep*](https://arxiv.org/abs/2606.22676), arXiv 2026.
[^tb]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks; [code](https://github.com/criticalml-uw/TamperBench).
[^rgrt]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv v2, 2026.
