# Attack Taxonomy for Open-Weight Safeguards

## Threat model

The attacker may read and modify weights, inspect/patch activations, change prompts and chat templates, alter decoding and inference code, fine-tune with arbitrary objectives, and add external context/tools. The defender may bound compute, data, time, or acceptable utility loss, but must state those bounds.

The taxonomy uses **intervention locus × optimization signal × persistence**. Attack names alone are misleading: LoRA and full fine-tuning may share a loss but impose different subspace constraints; activation ablation and weight orthogonalization may implement the same projection transiently or persistently.

## 1. Input and context attacks

| Class | Intervention | Inductive bias | Current evidence | Open-weight relevance |
|---|---|---|---|---|
| Manual jailbreak/role play | natural-language prompt | exploit policy ambiguity and learned personas | systematically benchmarked in HarmBench/JailbreakBench | lower-bound baseline; no weight access needed |
| Optimized suffix (GCG/AutoDAN) | discrete input tokens | exploit local input gradients/search | extensively studied | white-box gradients make search stronger |
| Multi-turn persuasion/PAIR/TAP | dialogue trajectory | exploit context accumulation and self-consistency | extensively studied | useful held-out family; expensive judge loop |
| Prefill/forced continuation | assistant-prefix tokens | bypass front-loaded refusal | strong 2025–26 evidence, including Any-Depth and DeepRefusal | trivial when serving stack permits prefix control |
| System/template override | header, roles, tokens | exploit format dependence | known but inconsistently swept | required because durability results change with template[^durability] |
| Retrieval/context injection | documents, RAG, tools | supply missing knowledge instead of restoring weights | decisive counterexample in Deep Ignorance[^deep] | separates capability absence from contextual access |

## 2. Activation and latent-space attacks

| Class | Intervention | Inductive bias | Evidence status |
|---|---|---|---|
| Refusal-direction removal/addition | project residual stream at layers/tokens | linear compact control | archival causal evidence; widely replicated[^arditi] |
| Optimized soft embedding | continuous input embedding | smooth local search in latent input space | used in Circuit Breaker critique and TamperBench[^cb][^tb] |
| Activation surgery/patching | layer/token/component hooks | causal localization and propagation blocking | growing 2026 preprint evidence[^surgery] |
| Head/neuron/MLP scaling or pruning | component outputs | sparse safety specialization | NeuroStrike reports <0.6% neuron removal and 76.9% average ASR[^neuro] |
| Nullspace/subspace steering | multi-direction constrained latent edit | preserve task features while moving safety state | active 2025–26 research; not yet standardized |
| Runtime state overwrite | KV cache, residuals, router/expert state | attack generation dynamics | technically feasible, under-benchmarked |

Activation attacks are usually cheap and diagnostic. They are not automatically durable: a defender might regenerate the state later. Conversely, an attacker controlling the inference loop can keep applying the intervention at every step.

## 3. Direct weight edits

| Class | Intervention | Inductive bias | Evidence status |
|---|---|---|---|
| Directional weight orthogonalization / abliteration | rank-one or low-rank projection of writer matrices | assumes a known refusal direction | strong archival/engineering evidence[^arditi] |
| Projected/norm-preserving abliteration | restrict edit to relevant column space or preserve norms | minimize collateral utility loss | primarily practitioner implementations; formal comparison sparse |
| Automated abliteration (Heretic) | optimize direction/layer/component kernel against refusal and benign KL | black-box hyperparameter optimization around Arditi-style edit | mature engineering tool; not a peer-reviewed completeness result[^heretic] |
| Multi-direction/cone edit | remove several causal directions | richer low-dimensional geometry | supported by Concept Cones/SOM-style literature |
| Safety-neuron pruning | zero/scaling selected FFN units | sparse component hypothesis | NDSS 2026 NeuroStrike[^neuro] |
| Head/MLP scaling | targeted weights/components | circuit bottleneck hypothesis | recent mechanism papers; limited standardized attack evaluation |
| Targeted model editing | ROME-like or gradient-constrained local update | local factual/behavioral editability | mature adjacent literature; safety-target benchmarks immature |
| Model arithmetic/merge/subtract | merge base, chat, or unsafe deltas | safety as a removable post-training delta | common engineering operation, weak formal coverage |

### Heretic's exact position

Heretic is a realistic, automated **direct weight-edit optimizer**. Its official repository combines directional ablation with Optuna/TPE search, varying direction index and separate component-wise layer kernels while co-minimizing refusals and benign KL.[^heretic] It is valuable because it lowers skill and tuning cost and exposes defenses to an automated practitioner.

It is **not threat-space completeness**:

- its extraction remains contrastive and predominantly low-dimensional;
- its objective uses refusal count and benign KL rather than downstream misuse capability;
- it does not jointly optimize fine-tuning, retrieval, architecture, and activation interventions;
- unsupported architectures and hidden/covert noncompliance can evade its assumptions;
- its headline results are repository self-evaluation, not an independent security benchmark.

Treat Heretic as one must-run attack implementation, never as the white-box adversary.

## 4. Fine-tuning attacks

| Class | Data/objective | Inductive bias | Current evidence |
|---|---|---|---|
| Harmful full-parameter FT | explicit harmful instruction–response pairs | unrestricted gradient update | systematically studied; often very strong |
| Harmful LoRA/PEFT | same, restricted low-rank adapters | cheap accessible update subspace | systematically studied |
| Benign FT | ordinary instruction/domain data | catastrophic forgetting / routing drift | established accidental failure mode |
| 10-shot overfitting attack | benign repeated/refusal then ordinary answers | sensitivity induced without overt harmful data | NeurIPS 2025 across ten models[^overfit] |
| Multilingual FT | harmful data in another language | shared multilingual safety features | present in TamperBench |
| Jailbreak-tuning | train susceptibility to jailbreak patterns | combine input and parameter attack | strongest family in many TamperBench pairs[^tb] |
| Backdoor FT | rare trigger plus unsafe behavior | conditional covert behavior | systematically studied, but trigger families narrow |
| Competing-objective/style FT | 98% benign, 2% poisoned in TamperBench | hide malicious signal in benign context | standardized in TamperBench[^tb-details] |
| Preference/DPO attack | chosen/rejected pairs favor harmful compliance | exploit preference-objective geometry | under-studied versus SFT |
| RL/reward attack | optimize a harmfulness/compliance reward | exploration and long-horizon behavior | emerging; not in standard tamper suites |
| Continued pretraining | raw domain corpus | capability acquisition rather than instruction policy | central to Deep Ignorance evaluation; expensive |

TamperBench’s nine-paper suite covers benign full/LoRA, harmful full/LoRA, multilingual FT, three covert jailbreak-tuning attacks, and a continuous embedding attack. Its live code has since added refusal ablation and prompt/GCG integrations, but paper claims should be tied to the paper version.[^tb-code]

## 5. Capability restoration attacks

| Class | What is restored | Evidence |
|---|---|---|
| Benign related relearning | hidden/memorized knowledge access | ICLR 2025 shows forgotten content returns after benign related data[^relearn] |
| Few-shot malicious relearning | explicit target capability | TMLR 2025 undoes tested unlearning within 16 gradient steps[^tamper-eval] |
| Quantization recovery | suppressed content after BF16→low-bit conversion | multiple 2025–26 studies expose recovery; deployment transformation is an attack surface[^quant] |
| Retrieval/tool augmentation | knowledge supplied at inference | defeats pure knowledge-prevention under staged attacks[^deep] |
| Distillation from a capable teacher | behavior/capability copied into defended student/checkpoint | feasible and important, scarcely evaluated as a defense attack |
| Model merging/base-delta restoration | unsafe/base capability merged back | common open-model operation, little adaptive defense evaluation |

## 6. Architecture and inference tampering

| Attack | Why it matters | Coverage |
|---|---|---|
| Remove guard adapters/classifier heads | any separable guard can be deleted | obvious but rarely included because it trivially wins |
| Change chat template/system tokens | safety can be format-dependent | durability audit demonstrates evaluation sensitivity |
| Modify decoding/logit processors | bypass runtime refusal/safety steering | poorly covered in model-defense papers |
| Disable mid-generation reinjection/hooks | defeats Any-Depth/activation guards | trivial under full inference control |
| Swap/tokenizer remap special tokens | removes header-triggered policy signals | plausible, under-studied |
| Prune/quantize/compress | can erase small safety updates or restore hidden behavior | emerging unlearning evidence |
| Replace/route MoE experts | exploit sparse expert specialization | MoE-specific safety work exists, adaptive tampering sparse |
| Wrap model with tools/RAG | bypass lack of internal knowledge | directly demonstrated for filtering-based capability safeguards |

## 7. Distinct attack inductive biases

A robust suite needs attacks that fail for different reasons:

1. **Semantic/context bias:** manual, multi-turn and retrieval attacks search meanings and policies.
2. **Discrete-gradient bias:** GCG-like attacks exploit token-level local gradients.
3. **Continuous-state bias:** embedding/activation attacks assume smooth latent controllability.
4. **Sparse-localization bias:** neuron/head pruning assumes concentrated components.
5. **Low-rank weight bias:** abliteration/LoRA assumes cheap linear parameter modes.
6. **Unrestricted update bias:** full FT can reorganize representations beyond local edits.
7. **Optimization-dynamics bias:** benign FT, preference attacks and RL exploit forgetting/trajectory effects.
8. **Capability-supply bias:** retrieval/distillation avoids undoing a safeguard and replaces what it withheld.
9. **Infrastructure bias:** templates, tokenizers, decoding and guard removal attack the serving composition.

Counting ten variants from one category does not substitute for crossing these biases.

## 8. Under-studied adaptive attackers

At least the following should be treated as plausible gaps, not speculative fantasy:

1. **Alternating latent-edit + fine-tuning attacker:** re-estimate a failure direction after every short FT burst, then train through the edited state.
2. **Defense-aware re-extraction:** infer new refusal/safety directions after each ablation rather than reuse a baseline projector.
3. **Joint sparse structured edit:** optimize neuron pruning, head scaling and low-rank matrix edits together under a utility Lagrangian.
4. **Template/tokenizer/decoding co-search:** jointly search chat format, assistant prefill, temperature/top-p and logit processors before touching weights.
5. **Quantize–merge–repair pipeline:** quantize the defense, merge a base/unsafe delta, then use a short utility-repair FT.
6. **Recognition/action decoupler:** preserve a model’s harm classification while directly training or editing the response policy to comply.
7. **Retrieval-assisted relearning:** provide missing knowledge in context while fine-tuning only policy/usefulness, attacking filtering and unlearning simultaneously.
8. **Distillation attacker:** use any accessible stronger/unsafe model or corpus to distill target behavior under a fixed compute budget.
9. **RL attacker:** optimize actual harmful task completion rather than imitation loss or refusal strings.
10. **Model-family transfer attacker:** learn attack priors on related public checkpoints, then spend the target budget only on refinement.
11. **Utility-metric gaming attacker:** preserve MMLU-Pro while selectively degrading unmeasured helpfulness or exploiting judge weaknesses.
12. **Long-horizon agentic attacker:** optimize tool-use success over trajectories where refusal on any single turn is not the endpoint.

## 9. Is the taxonomy close to exhaustive?

No. It is structurally incomplete because an open-weight adversary can compose operations. The relevant search space is a program over model/data/inference transformations, not a flat list. A useful benchmark can cover major inductive biases and enforce budgets, but cannot claim completeness.

## 10. Minimum reporting standard for an attack

- exact checkpoint hash and tokenizer/template;
- attacker knowledge and defender disclosure;
- data provenance and number of unique target-relevant examples;
- trainable parameters, optimizer, steps, tokens, precision, hardware and trials;
- search objective separated from final evaluation;
- actual harmful task success plus refusal and judge diagnostics;
- utility frontier, over-refusal and parameter/function drift;
- all failed, OOM, diverged and censored runs;
- at least three seeds for stochastic training attacks;
- whether the attack was adapted after inspecting defense results.

## Sources

[^arditi]: Arditi et al., [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html).
[^durability]: Qi et al., [ICLR 2025 durability audit](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html).
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^cb]: Schwinn & Geisler, [Circuit Breaker reevaluation](https://arxiv.org/abs/2407.15902).
[^tb]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 D&B.
[^tb-details]: TamperBench, [paper PDF](https://openreview.net/pdf?id=urjPCYZt0I), Appendix attack suite.
[^tb-code]: CriticalML, [official TamperBench repository](https://github.com/criticalml-uw/TamperBench), inspected at `ca4fade`.
[^surgery]: [*Activation Surgery*](https://arxiv.org/abs/2603.14278), arXiv 2026.
[^neuro]: Wu et al., [*NeuroStrike*](https://www.ndss-symposium.org/ndss-paper/neurostrike-neuron-level-attacks-on-aligned-llms/), NDSS 2026.
[^heretic]: Weidmann, [Heretic official repository](https://github.com/p-e-w/heretic), engineering artifact, 2025–2026.
[^overfit]: Xie et al., [*Attack via Overfitting*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/2cb880950081ceb85100951b0ad0d542-Abstract-Conference.html), NeurIPS 2025.
[^relearn]: Hu et al., [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html).
[^tamper-eval]: Che et al., [TMLR 2025](https://openreview.net/forum?id=E6OYbLnQd2).
[^quant]: Zhang et al., [quantization recovery in LLM unlearning](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ba79fb5c4fe70050752f20c90c5f07ca-Abstract-Conference.html), ICLR 2025.
