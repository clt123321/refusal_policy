# Round 2 Decision

## Decision

### PRIMARY BET — Heterogeneous parameter fault domains

Train at least two individually sufficient safety pathways with deliberately different parameter sensitivity, then optimize and evaluate the **minimum adaptive joint cut** required to remove both while retaining benign utility.

This is selected after comparison, not inherited from the prior writer/common-mode framing. The bet survives because the reviewed literature now heavily occupies refusal rank, response diversity, recognition–refusal coupling, temporal reconstruction, Fisher routing, ordinary cross-perturbation training and capability suppression. It does **not** yet establish or train parameter-level fault independence.

The central prediction is simple:

> At matched clean safety, utility and defender cost, a model with verified heterogeneous safety fault domains requires more attacker work under at least two held-out intervention families than a model with equally many but co-sensitive safety carriers.

The defense fails if “two pathways” reduce to one shared output route. Activation orthogonality, component count, stable rank and separate layer locations are diagnostics only; the security object is the post-defense, utility-constrained adaptive joint cut.

### BACKUP BET — Cross-operator adversarial retrofit

Train against a minimal set of distinct intervention operators—activation faults, direct parameter edits and short gradient updates—and judge success only by transfer to a fully held-out operator class.

This is more plausible and easier to implement than the primary bet, but less novel. TAR, AntiDote, ART, Booster, LAT and DeepRefusal already occupy adjacent designs. It earns a paper only if the off-diagonal transfer matrix is unexpectedly strong; diagonal robustness is not enough.

### WILDCARD — Repair-closed safety–utility coupling

Train so that any low-cost update that repairs benign utility after a safety breach also reconstructs safety.

SDD and SEAM already establish the initial “break safety, lose utility” idea. The unclaimed step is closure under a defense-aware two-stage breach→repair attack. If real, this is a memorable and general security distinction; if not, the program should die quickly.

## Scorecard

All scores are 0–10; for **cost**, 10 means cheaper.

| Program | Novelty | Plausibility | Attack coverage | Adaptive robustness | Practicality | Cost | Falsifiability | Main-conference ceiling |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Primary: heterogeneous fault domains** | 8 | 6 | 7 | 6 | 6 | 6 | 9 | 9 |
| **Backup: cross-operator retrofit** | 5 | 8 | 8 | 6 | 7 | 5 | 9 | 7 |
| **Wildcard: repair-closed coupling** | 7 | 5 | 5 | 7 | 4 | 3 | 9 | 9 |

These are research-prioritization judgments, not empirical results.

## Why the primary bet wins

1. **Sharper distinction:** multiple representations are not the same as multiple failure domains. The claim is security-relevant only when a joint attacker must cross them separately.
2. **Less occupied:** HARC already couples recognition and refusal; DeepRefusal/Any-Depth already reconstruct safety; diverse-prefix training already raises stable rank; Skin-Deep already predicts LoRA fragility; SEAM already entangles safety and utility. Parameter fault independence remains comparatively open.
3. **Attack relevance:** the primary outcome is attacker work at fixed utility, not a geometry score.
4. **Cross-attack prediction:** if fault domains are real, cost should rise for both post-defense direct edits and held-out update attacks.
5. **Cheap rejection:** one small-model prototype and a strong joint edit can kill the idea before a large training matrix.
6. **Reasonable engineering envelope:** it can be attempted as a retrofit with zero inference overhead; unlike capability prevention, it need not retrain from scratch.

The primary loses to the backup on near-term implementation certainty and to the wildcard on surprise if successful. It wins the current portfolio because it offers the best combination of novelty, falsifiability, retrofit scope and direct relevance to the unsafe-but-useful attack frontier.

## Closest prior work and exact residual gap

- [Concept Cones](https://proceedings.mlr.press/v267/wollschlager25a.html) tests multiple causal directions and representational independence. It does not establish distinct parameter failure domains or train them.
- [DeepRefusal](https://aclanthology.org/2025.findings-emnlp.956/) trains recovery from refusal-direction faults across layer/token depth. Fine-tuning attacks are excluded, and the injected fault remains direction-family specific.
- [Refusal Geometry Reflects Refusal Training](https://arxiv.org/abs/2608.25390) shows diverse refusal starts can raise activation/gradient stable rank and weaken one same-set vector ablation attack. It does not test adaptive joint edits or parameter independence.
- [Safety Neurons](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html) provides sparse causal carriers but not failure-domain independence.
- Reliability engineering supplies the common-cause/fault-domain concept. The potential contribution is not renaming it; it is demonstrating that this distinction can be trained and prospectively predicts utility-constrained white-box attack cost in neural networks.

If the last empirical clause fails, the novelty collapses to an analogy and the program stops.

## Cheapest falsification experiment

No experiment is launched in this round. The first approved test should be:

1. **Model:** one 1.5–3B aligned checkpoint.
2. **Controls:** ordinary matched safety SFT and an equal-cost diverse-refusal/multi-direction control.
3. **Prototype:** two disjoint trainable layer bands; alternate complete masking/ablation of one band while teaching the surviving band the same safety endpoint; add a parameter-sensitivity separation constraint only if the masking control is insufficient.
4. **Verification:** show each path is individually sufficient through ablation and rescue; do not count representation orthogonality as success.
5. **Primary attack:** after defense, re-extract a joint rank-constrained direct edit over all layers, optimize harmful success plus benign KL/task retention, and sweep rank/budget.
6. **Held-out attack:** short LoRA with unseen rank/target modules, followed by a short full-parameter check.
7. **Outcome:** minimum discovered GPU-time/FLOPs/tokens and parameter/function drift needed to cross a fixed harmful-task threshold at <1% utility loss.
8. **Killer figure:** three attack-cost frontiers—ordinary SFT, equal-cost multi-direction control, heterogeneous-domain prototype. Geometry appears only as a mechanism inset.

This is the cheapest discriminating test because a strong joint edit can reject fake independence without building the complete training or model matrix.

## Immediate stop conditions

Stop the primary program before scaling if any occurs:

- the two paths are not separately sufficient under ablation/rescue;
- a post-defense re-extracted joint edit breaches at ≤1.25× the matched baseline cost while utility loss stays <1%;
- held-out LoRA or short full FT erases the gain at baseline-level cost;
- apparent robustness disappears with a stronger or derivative-free edit search;
- the gain requires >1% clean utility loss or comes from broad capability collapse;
- the same gain is reproduced by the equal-cost diverse-refusal control, leaving no fault-domain-specific effect.

The scale-up gate is stronger: require ≥2× median independently measured breach cost on **two distinct held-out intervention families**, with <1% clean utility loss and no material over-refusal increase.

## Harness reproduction order

### Attacks first

1. **Arditi-style refusal ablation** as a deterministic unit test.
2. **Heretic/direct low-rank edit** with post-defense direction/layer re-extraction and benign-KL constraint.
3. **Benign and harmful LoRA** with rank/module/optimizer sweeps.
4. **Jailbreak-tuning**, because TamperBench often finds it strongest.
5. **Short full-parameter fine-tuning** to detect PEFT-only security.
6. **Breach→benign-utility repair** for every utility-coupled claim.
7. **Prefill/prompt attack** as an orthogonal behavior control, not the primary durability endpoint.

### Defenses first

1. Ordinary matched safety SFT.
2. Diverse refusal-prefix training as the cheapest rank/multi-direction control.
3. DeepRefusal or HARC as a reconstruction/coupling specialist; HARC’s reported 160-example FT collapse is a required sanity target.
4. Triplet/CRL and one practical tamper-aware baseline—Booster or AntiDote—through TamperBench.
5. SDD or SEAM only before testing the wildcard.
6. TAR after the small-model pipeline is stable; its full-parameter implementation is too expensive for initial harness debugging.

The harness should extend TamperBench, preserve its registry and sweep semantics, and add direct-edit, lineage and normalized cost APIs. A defense implementation must not begin until baseline attacks reproduce their expected qualitative ordering.

## What is not selected

- **Route reconstruction:** retained as a baseline family, not a primary novelty claim.
- **Capability prevention:** strongest narrow durability evidence, but incompatible with cheap retrofit and vulnerable to external capability supply.
- **Functional safety margin:** adopted as the common evaluation object only if it predicts held-out attacks; not promoted as a defense by itself.
- **Attack-program training:** postponed until a two-stage repair attack first demonstrates that program composition changes conclusions.
- **Writer-cut/common-mode terminology:** not required. Minimum joint cut is useful only if operationally estimated; otherwise delete it.

## Sources

- Wollschläger et al., [Concept Cones](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
- Xie et al., [DeepRefusal](https://aclanthology.org/2025.findings-emnlp.956/), Findings EMNLP 2025.
- Labunets, [Refusal Geometry Reflects Refusal Training](https://arxiv.org/abs/2608.25390), arXiv 2026.
- Chua et al., [HARC](https://arxiv.org/abs/2607.00572), arXiv 2026.
- Qi et al., [Durability Audit](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
- Hossain et al., [TamperBench](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
- Wang et al., [SEAM](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1abb0e7bd62ba80610798dee81950522-Abstract-Conference.html), ICLR 2026.

ROUND2_DEFENSE_PROGRAMS_SELECTED
