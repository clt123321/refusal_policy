# Round 1 Synthesis: Open-Weight Defense Landscape

**Evidence cutoff:** 2026-09-11
**Decision status:** background map complete; no experiment or final paper story selected

## Bottom line

The target is scientifically meaningful only in bounded form:

> Given a declared white-box attacker, search budget and benign-utility constraint, how much does a model-internal intervention move the best discovered safety–utility attack frontier, and at what defender cost?

An unremovable safeguard in freely executable weights is not a credible target. An owner can replace arbitrary components or retrain from another initialization. What remains useful is comparative **work-factor amplification** against multiple non-equivalent attack families, stopping where attacking a different model becomes cheaper.

This review does not select a mechanism, defense, experiment, or paper narrative. It establishes the problem boundary and evidence gaps needed for that later choice.

## 1. How much do we know about safety mechanisms?

**Answer: enough to reject a single-layer story; not enough to specify a durable mechanism.**

### WE KNOW

- In many tested aligned transformer families, compact residual interventions can causally add or suppress refusal; rank-one weight orthogonalization can reproduce the suppression.[^arditi]
- Multiple causal refusal directions can coexist, and geometric orthogonality does not imply functional independence.[^cones]
- Harm recognition and refusal can be represented separately; some attacks weaken action while recognition remains measurable.[^separate]
- Sparse neurons and localized components can mediate safety behavior in tested models, but causal localization does not automatically identify the cheapest durable edit target.[^neurons][^editing]
- Generation depth matters: unsafe prefilling can bypass an early decision, and safety behavior can be retriggered later.[^deeprefusal][^ada]
- Post-training refusal and many unlearning results can suppress access while underlying capability or knowledge remains recoverable.[^unlearn][^hide]

### PLAUSIBLE

- Safety behavior is a pipeline from recognition → policy decision → execution, with several partially redundant implementations.
- Training procedure changes how concentrated or distributed the causal control is.
- Reconstruction across layers/tokens may improve robustness to more than the exact fault used in training.
- Coupling safety removal to valued capability loss may be more durable than maximizing clean refusal.

### SPECULATIVE

- Any activation geometry statistic is a general predictor of white-box breach cost.
- Multiple writers constitute independent security redundancy.
- A stable, model-family-independent “safety circuit” exists.
- Local weight flatness, controllability rank, or a common-mode score alone determines long-horizon robustness.

The conflicts are informative: single-direction causal results and multidirectional results can both hold because they identify effective control handles, not a unique complete mechanism. Refusal, recognition and capability must therefore remain separate measurements.

## 2. How complete is our knowledge of the attack space?

**Answer: major families are known; the space is nowhere near exhausted.**

Systematic work covers prompt jailbreaks, prefilling, optimized embeddings, directional ablation, harmful/benign/jailbreak fine-tuning and relearning. TamperBench is the broadest current public substrate, with nine attack classes across 21 models and explicit hyperparameter sweeps.[^tb]

But attacks are programs, not a closed list. Understudied adaptive classes include:

- defense-aware re-extraction after the defense changes representations;
- neuron/head/MLP and structured sparse edits;
- norm-, KL- or utility-constrained model editing;
- mixed full-weight/PEFT updates and optimizer/layer schedules;
- preference optimization or RL as the attacker objective;
- quantization, merging, pruning and architecture replacement;
- edit→utility-repair and fine-tune→retrieval compositions;
- context/tool-supplied capability restoration;
- attacks on runtime safety-token injection or guard modules;
- automated multi-objective searches that jointly choose locus, rank and layer.

Heretic is a strong engineering instance of automated Arditi-style directional search. It makes a realistic direct-edit baseline; it is not a complete threat model and currently is not an archival security evaluation.[^heretic]

## 3. What is the most defensible scope of “model defense”?

**Answer:**

> Model-internal, bounded tamper resistance for open-weight models, evaluated across attack families as the utility-constrained increase in attacker work factor.

This scope includes refusal, safe completion, policy following, capability suppression and knowledge removal, but demands an endpoint appropriate to each. It excludes claims that a public checkpoint can enforce access control or prevent its owner from disabling an external monitor.

Two boundaries are essential:

1. **Model-internal versus system-level.** Runtime classifiers, APIs, TEEs and attestation matter operationally but are not persistent properties of untrusted public weights.
2. **Behavior versus capability.** A model that will not answer may still know; a model without internally stored knowledge may regain it from context or tools.

Absolute safety is the wrong objective. A work-factor result is meaningful only relative to an attack budget, utility threshold, attack portfolio and substitution cost.

## 4. How strong are the best current defenses?

**Answer: strong inside specific threat models, not generally strong.**

| Scope | Strong evidence | What it does not establish |
|---|---|---|
| Prompt/prefill/activation robustness | DeepRefusal; Any-Depth Alignment | malicious FT or untrusted-runtime durability |
| Alignment-stage resistance to FT | TAR; RepNoise; Booster; AntiDote; Triplet | broad direct-edit/composed robustness; independent replication is sparse |
| Utility-coupled resistance | SDD; SEAM | resistance to adaptive decoupling and repair |
| Controlled customization | SafeLoRA; Lisa; Antibody; post-FT Antidote | persistence when the checkpoint owner ignores the procedure |
| Narrow capability durability | Deep Ignorance | cheap retrofit, general domains, or resistance to supplied context/retrieval |

The most sobering evidence comes from evaluations rather than defenses. The ICLR durability audit found that small changes in trainers, randomness and formatting reverse conclusions for TAR and RepNoise.[^audit] TamperBench’s revised study finds current alignment-stage defenses largely fail under broader sweeps, with attack ranking dependent on model and jailbreak-tuning often strongest.[^tb] Cheap abliteration/prefilling also substantially raises ASR against recent fine-tuning defenses.[^simple]

Thus “best” must always be qualified by safeguard, attacker and budget. There is no defensible universal winner.

## 5. What do the defenses cost?

**Answer: published reporting is too inconsistent for a clean ranking.**

- DeepRefusal reports roughly one epoch/45 minutes on one A100-80GB for 7–8B LoRA retrofits.[^deeprefusal]
- Vaccine reports about 2× alignment step time and about 0.11GB additional memory in its setup.[^vaccine]
- AntiDote reports 0.69, 1.97 and 3.17 hours for 3B, 7B and 12B configurations, with peak memory of 32.4, 51.2 and 73.6GB; these are author-side setup-specific numbers.[^antidote]
- TAR’s public 8B full-parameter implementation recommends 8×A100-80GB, making it materially heavier than PEFT retrofits.[^tar-code]
- Deep Ignorance says filtering itself is under 1% of pretraining FLOPs, but its evidence relies on matched 6.9B models trained for 550B tokens, so it is not a cheap retrofit.[^deep]

Dollar cost should be secondary and dated. A credible comparison reports tokens, forward/backward passes, FLOPs estimate, GPU-hours/hardware/precision, peak memory, search trials, failed runs, evaluator costs and lifetime inference overhead. Zero inference overhead is desirable, not mandatory; it must be included in the denominator for long-lived deployments.

No evidence currently supports a portable claim such as “open-weight defense under $5” without many qualifiers.

## 6. Is a general defense realistic?

**Answer: unconditional general defense, no; attack-family-general robustness, plausibly; defense-in-depth, most credible.**

Three levels should not be conflated:

1. **Unconditional artifact integrity:** not meaningful once the attacker may arbitrarily modify or replace the artifact.
2. **Cross-attack empirical robustness:** possible if distinct attacks share a functional vulnerability, but must be demonstrated on held-out intervention families.
3. **Defense-in-depth:** likely necessary—combine capability prevention where feasible, robust policy reconstruction, several perturbation families, utility coupling, and trusted system boundaries when available.

Even composition is not automatically monotonic. Deep Ignorance reports staged attacks that restore capability despite tested combinations, so every stack needs adaptive evaluation.[^deep]

## 7. What is the largest evaluation gap?

**Answer:** an attack-blind, cost-accounted, staged white-box evaluation that measures actual harmful capability and benign utility across non-equivalent intervention biases.

The recommended path is to **extend TamperBench**, not recreate loaders and sweep machinery. Add:

- activation hooks and direct structured weight edits, including Heretic;
- post-defense feature re-extraction;
- staged/composed attack programs;
- capability restoration through context, retrieval and relearning;
- recognition/action/capability-separated endpoints;
- multiple utility constraints (0%, 2%, 5%, 10%);
- complete attack/defense cost ledgers;
- immutable artifact lineage, preregistered thresholds and censoring rules;
- one evaluator-held attack family followed by a fully informed adaptive phase;
- blinded human review for ambiguous harmful-task outcomes.

Headline output should be a breach frontier over budget and utility tolerance. “No breach observed” is right-censored evidence, not proof of robustness.

## 8. Which open problems are genuinely worth studying?

The following are high-value problem classes, not selected stories:

1. **Predicting attack-family transfer:** find a quantity that predicts held-out edit/activation/FT robustness, not just the trained perturbation.
2. **Recognition-to-action durability:** test whether preserving recognition with heterogeneous policy readouts improves the breach frontier.
3. **Functional fault independence:** determine whether safety paths can be made independent under parameter interventions, not merely orthogonal in activation space.
4. **Utility-coupled tampering:** test whether safety removal can remain inseparable from capability damage under adaptive two-stage repair.
5. **Temporal reconstruction:** determine whether repeatedly rebuilding safe policy across generation transfers beyond prefill-like attacks.
6. **Functional-metric robustness:** ask whether benign-function-normalized curvature predicts attacks better than raw parameter norms.
7. **Retrofit versus pretraining frontier:** quantify how much durability cheap post-training can recover relative to capability prevention.
8. **Capability-source substitution:** study when missing internal knowledge is replaced by context, retrieval, tools or relearning.
9. **Attack-program composition:** model adversaries that remove a safeguard, repair utility and restore capability in stages.
10. **Defense composition:** identify complementary failure modes and test whether combined defenses give super-additive, additive or illusory gains.

These should be triaged using the cheapest discriminating tests in [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md). None should advance merely because it yields an elegant geometry metric.

## Decisions established by Round 1

- **Keep:** the final operational question—difficulty of removing a safeguard while preserving useful capability.
- **Broaden:** safeguard endpoints beyond refusal to safe action, knowledge and actual domain capability.
- **Narrow claims:** from “tamper resistant” to budgeted, attack-relative frontier movement.
- **Separate:** model-internal durability from system enforcement; recognition from action; access suppression from capability absence.
- **Extend:** TamperBench as the initial harness substrate.
- **Require:** held-out attack bias, adaptive evaluation, staged attacks and normalized cost accounting.
- **Do not select yet:** writer-cut, common-mode failure, controllability, temporal reconstruction, utility coupling, or any other central mechanism/story.

## Evidence map

- Review and threat boundary: [OPEN_WEIGHT_DEFENSE_REVIEW.md](OPEN_WEIGHT_DEFENSE_REVIEW.md)
- Mechanism claims and certainty: [SAFETY_MECHANISM_MAP.md](SAFETY_MECHANISM_MAP.md)
- Attack families and blind spots: [ATTACK_TAXONOMY.md](ATTACK_TAXONOMY.md)
- Safeguard and defense classes: [DEFENSE_TAXONOMY.md](DEFENSE_TAXONOMY.md)
- Normalized defense cards: [DEFENSE_EVIDENCE_TABLE.csv](DEFENSE_EVIDENCE_TABLE.csv)
- Harness decision: [HARNESS_LANDSCAPE.md](HARNESS_LANDSCAPE.md)
- Testable principles: [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md)

## Sources

[^arditi]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^cones]: Wollschläger et al., [*The Geometry of Refusal*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^separate]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^neurons]: Chen et al., [*Safety Neurons*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html), NeurIPS 2025.
[^editing]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^deeprefusal]: Xie et al., [*DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings EMNLP 2025.
[^ada]: Zhang et al., [*Any-Depth Alignment*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^unlearn]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^hide]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^tb]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^heretic]: p-e-w, [Heretic](https://github.com/p-e-w/heretic), engineering tool; no archival-paper status claimed.
[^audit]: Qi et al., [*On Evaluating the Durability of Safeguards*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^simple]: Kuo et al., [*Open-Weight LLM Fine-Tuning Defenses are Susceptible to Simple Attacks*](https://arxiv.org/abs/2605.26526), 2026 preprint.
[^vaccine]: Huang et al., [*Vaccine*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/873c86d9a979ab80d8e2919510d4446b-Abstract-Conference.html), NeurIPS 2024.
[^antidote]: Sanyal et al., [*AntiDote*](https://ojs.aaai.org/index.php/AAAI/article/view/40570), AAAI 2026.
[^tar-code]: Tamirisa et al., [TAR official repository](https://github.com/rishub-tamirisa/tamper-resistance).
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.

ROUND1_LANDSCAPE_COMPLETE
