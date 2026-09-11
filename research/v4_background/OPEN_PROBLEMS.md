# Open Problems and Candidate Defense Principles

**Purpose:** identify testable phenomena that could support future defenses. These are not algorithms, project commitments, or a final paper story.

## 1. The central unsolved problem

The field has many ways to improve clean refusal and several ways to slow a known attack. It does not yet know how to predict, before a broad adaptive evaluation, whether a safeguard will survive an **unseen intervention bias** while preserving useful capability. That gap has three parts:

- mechanism: which internal objects recognize harm, choose policy, execute behavior, or suppress capability;
- robustness: which of those objects share a removable failure mode;
- measurement: how to estimate the best attack frontier rather than the outcome of one recipe.

The principles below survive only if their cheapest falsification tests reveal attack-family transfer. A result confined to the fault injected during training is not enough.

## Principle 1 — Reconstruct safety throughout generation

**Phenomenon:** A refusal policy can be strong at the prompt boundary and disappear after unsafe prefilling, while safety cues injected later can recover it.

**Existing evidence:** DeepRefusal trains with refusal-feature ablation across layers/tokens and transfers to prompt and prefill attacks; Any-Depth Alignment repeatedly injects safety-associated assistant tokens and restores refusal at arbitrary depth.[^deeprefusal][^ada]

**Potential defense principle:** Train the policy to recompute a safe action from local context at many generation depths instead of relying on one early state.

**Why it might generalize:** Prompt suffixes, prefills and some activation perturbations all exploit temporal dependence on an early decision.

**Why it might fail:** An owner can disable runtime reinjection, fine-tune away reconstruction, or preserve refusal while restoring dangerous capability through tools/context.

**Cheapest falsification experiment:** Compare a standard aligned small model with a depth-randomized safety retrofit under unseen prefill lengths and one direct weight edit; reject the principle if gains vanish outside prefill-like attacks.

## Principle 2 — Preserve recognition and diversify policy readouts

**Phenomenon:** Harmfulness recognition and refusal execution can be linearly and causally dissociated.

**Existing evidence:** NeurIPS 2025 reports separate harmfulness and refusal directions; some attacks suppress refusal while harmfulness remains represented.[^separate]

**Potential defense principle:** Preserve a robust harm-recognition signal and train several functionally distinct readouts from recognition to safe actions.

**Why it might generalize:** Different attacks may break one policy readout while leaving the upstream evidence available for another.

**Why it might fail:** Apparently distinct readouts may share a downstream gate or parameter control mode; recognition may itself be spoofed by obfuscated intent.

**Cheapest falsification experiment:** Ablate or edit each learned readout separately and jointly while probing recognition; reject if one low-cost re-extracted edit disables all outputs without harming recognition or utility.

## Principle 3 — Train across intervention bases, not named attacks

**Phenomenon:** Robustness often tracks the perturbation family used in training; simple changes to embedding or fine-tuning attacks overturn headline results.

**Existing evidence:** The Circuit Breaker reevaluation obtains 100% ASR after small attack changes; the ICLR durability audit shows sensitivity to trainer, shuffling and formatting.[^cb][^audit]

**Potential defense principle:** Sample perturbations across activation, direct-weight and gradient-update bases, with held-out bases for validation.

**Why it might generalize:** It targets local functional invariance rather than a named implementation.

**Why it might fail:** A finite basis cannot span staged retraining, retrieval, architecture changes, or nonlinear attack programs; excessive invariance may damage learnability.

**Cheapest falsification experiment:** Train against two bases on a 1–4B model and test a third held-out basis at matched compute; reject if robustness is no better than single-family training.

## Principle 4 — Create heterogeneous safety fault domains

**Phenomenon:** Multiple activation features need not be independent failures if one shared parameter change controls them.

**Existing evidence:** Concept Cones shows multiple causal refusal directions and warns that Euclidean orthogonality is not functional independence; direct rank-one edits can suppress refusal in many models.[^cones][^arditi]

**Potential defense principle:** Encode safety paths in components with deliberately different parameter support, training signals and computation stages.

**Why it might generalize:** Heterogeneity can reduce common-cause failure across direct edits, neuron faults and localized fine-tuning.

**Why it might fail:** End-to-end optimization may recreate a shared bottleneck, and arbitrary fine-tuning may still alter all paths cheaply.

**Cheapest falsification experiment:** Train two equal-cost safety heads attached at separated layers versus two same-layer heads; compare the minimum joint edit under equal utility constraints. Reject if physical separation does not change the attack frontier.

## Principle 5 — Couple safeguard removal to useful capability loss

**Phenomenon:** Some methods make malicious fine-tuning degrade general utility, changing the attacker’s feasible set rather than merely lowering ASR.

**Existing evidence:** SDD and SEAM report utility collapse under selected malicious fine-tuning protocols.[^sdd][^seam]

**Potential defense principle:** Arrange shared functional dependencies so edits that increase dangerous task success also damage capabilities the attacker wants to retain.

**Why it might generalize:** The objective directly matches utility-constrained tampering, regardless of whether the attack is called fine-tuning or editing.

**Why it might fail:** A defense-aware attacker may localize the coupling, repair utility afterward, change parameter support, or start from another base model.

**Cheapest falsification experiment:** Attack a small defended model with a joint objective that explicitly restores benign utility after breach; reject if a short two-stage repair recovers both harmful and benign performance.

## Principle 6 — Flatten safety loss in a functional metric

**Phenomenon:** Local parameter flatness is coordinate-dependent, while small function-preserving weight changes can have very different behavioral effects.

**Existing evidence:** Booster and smoothness-aware unlearning seek local robustness; model-editing work shows localization and editability do not coincide.[^booster][^smooth][^localize]

**Potential defense principle:** Optimize low safety sensitivity under perturbations normalized by benign functional change or a Fisher-like metric, not raw parameter norm.

**Why it might generalize:** It measures attacker movement in the same safety–utility space used for evaluation.

**Why it might fail:** Local curvature need not predict long-horizon fine-tuning; estimating the metric can be expensive and gameable.

**Cheapest falsification experiment:** Compare raw-norm and function-normalized sharpness against held-out low-rank edits and short FT across existing checkpoints; reject if neither predicts the utility-constrained breach order.

## Principle 7 — Prevent acquisition instead of suppressing access

**Phenomenon:** Post-training “unlearning” often hides retrievable knowledge; filtering risky pretraining data can make reacquisition much slower.

**Existing evidence:** Unlearning or Obfuscating and Erase or Hide report recovery/suppression phenomena; Deep Ignorance resists much longer relearning than post-training baselines in matched biology models.[^unlearn][^hide][^deep]

**Potential defense principle:** For narrow, identifiable high-risk domains, prevent internal acquisition and separately harden policy behavior.

**Why it might generalize:** An attacker cannot reveal a compact behavior policy for capability the model never learned.

**Why it might fail:** General reasoning transfers, data boundaries leak, and context/retrieval can supply missing knowledge; it is costly and not a general retrofit.

**Cheapest falsification experiment:** On an existing filtered checkpoint, compare context-free, context-supplied and lightweight-retrieval task success; reject model-only durability if context closes most of the gap.

## Principle 8 — Evaluate the capability supply chain

**Phenomenon:** A model’s dangerous competence can come from weights, context, retrieval, tools, or later training.

**Existing evidence:** Deep Ignorance’s strongest failure modes include in-context search and staged fine-tuning plus retrieval; unlearning evaluations show relearning can rapidly restore access.[^deep][^tamper-eval]

**Potential defense principle:** Allocate defenses to each source of capability and measure substitution between sources, rather than treating the checkpoint as closed.

**Why it might generalize:** It applies across bio, cyber and agentic misuse where external information/tools are part of task execution.

**Why it might fail:** It becomes a system-security program rather than a model-internal defense and may require a trusted runtime.

**Cheapest falsification experiment:** Measure one dangerous task under a 2×2 design of internal capability present/absent and retrieval present/absent. Reject a model-only principle if retrieval dominates checkpoint state.

## Principle 9 — Make safety robust to continued benign learning

**Phenomenon:** Benign or related downstream training can erode alignment or revive supposedly removed knowledge without an explicitly malicious loss.

**Existing evidence:** Fine-tuning-safety work and unlearning reevaluations show safety erosion and benign relearning; invariant unlearning improves transfer to some held-out downstream environments.[^invariant][^unlearn]

**Potential defense principle:** Treat the distribution of plausible future updates as environments and preserve safety invariants across them.

**Why it might generalize:** It addresses ordinary adaptation and malicious updates that masquerade as useful learning.

**Why it might fail:** The chosen environments may encode only superficial variation; invariance can prevent legitimate learning or fail under direct editing.

**Cheapest falsification experiment:** Train on two benign update environments and test a held-out domain plus a maliciously mixed domain; reject if safety transfer is no stronger than ordinary replay.

## Principle 10 — Optimize against staged repair attacks

**Phenomenon:** An attack that first removes safety and then repairs utility or supplies knowledge can outperform any single-stage attack.

**Existing evidence:** Deep Ignorance reports staged fine-tuning-plus-retrieval failures; TamperBench shows attack ranking varies by model and that jailbreak-tuning is often stronger than nominally more direct attacks.[^deep][^tb]

**Potential defense principle:** Train and evaluate against short attack programs whose later stages repair the side effects of earlier stages.

**Why it might generalize:** Real attackers optimize a goal, not loyalty to one published attack recipe.

**Why it might fail:** The program space is combinatorial, training becomes unstable, and attackers can always add another stage.

**Cheapest falsification experiment:** For one defense that appears to trade safety for utility damage, compare its best single-stage attack with edit→utility-repair and FT→retrieval. Reject the claimed tradeoff if composition cheaply dominates.

## Principle 11 — Use tamper evidence only with an enforceable boundary

**Phenomenon:** Cryptographic hashes, signatures and latent integrity monitors can detect changes but cannot force an owner of public weights to honor the alarm.

**Existing evidence:** This follows from the deployment boundary: an attacker controlling execution can disable both the safeguard and its detector. TEEs, attestation and controlled APIs move enforcement outside the artifact.

**Potential defense principle:** Pair model-internal tamper evidence with attested execution or deny that it is an open-weight persistence guarantee.

**Why it might generalize:** Integrity verification is mature when a verifier or hardware root of trust exists.

**Why it might fail:** It does not protect freely executable weights and may reduce accessibility or privacy.

**Cheapest falsification experiment:** Give a red team the checkpoint and monitor code; if bypassing the monitor while preserving model utility is trivial, classify the method as system-level only.

## Principle 12 — Compose defenses only across genuinely different failure modes

**Phenomenon:** Stacking two defenses can add cost without adding robustness when both target the same representation or attack bias.

**Existing evidence:** Deep Ignorance shows combinations can still fail under staged attacks; TamperBench finds no uniformly strongest alignment-stage defense across models/attacks.[^deep][^tb]

**Potential defense principle:** Select defense components by complementary failure matrices, then evaluate their interaction rather than summing individual scores.

**Why it might generalize:** Heterogeneous layers—capability prevention, policy robustness, utility coupling and trusted runtime—make different attacker routes costly.

**Why it might fail:** Shared optimization dependencies create common-mode failure; composition can harm utility or reveal new gradients.

**Cheapest falsification experiment:** Measure two defenses alone and combined against one attack held out from both. Reject synergy if combined robustness is no better than the stronger component at matched clean utility and total defender cost.

## 2. Cross-cutting open questions

1. **Predictive quantity:** Is there any pre-attack statistic that predicts the budgeted safety–utility frontier across direct edits, activation attacks and fine-tuning?
2. **Attack basis:** What is the smallest set of intervention biases whose held-out transfer is informative rather than benchmark-specific?
3. **Functional distance:** Which metric reflects the attacker’s real objective better than parameter norm, steps or tokens alone?
4. **Adaptive evaluation:** How can an evaluation team search broadly without turning every defense paper into an unbounded red-team project?
5. **Capability endpoint:** How do we measure actual dangerous-task competence safely and reproducibly, rather than refusal style?
6. **Scope transfer:** Which results survive model family, scale, safety objective, language, and reasoning-time changes?
7. **Retrofit limit:** How close can a low-cost post-training defense get to the durability of pretraining-time capability prevention?
8. **Composition:** When are two defenses complementary versus two parameterizations of the same failure mode?
9. **Owner advantage:** What defender preparation can increase the marginal cost relative to downloading or adapting a different open model?
10. **Stopping rule:** At what attacker cost does a model defense stop being operationally meaningful because substitution is cheaper?

## 3. Triage criteria for future work

Advance a principle only if it supplies all four:

- a distinction not reducible to a new metric name;
- a falsifiable prediction on a held-out attack family;
- an endpoint tied to harmful task success and benign utility;
- a defender/attacker cost comparison with an explicit substitution baseline.

Deprioritize any proposal whose only evidence is higher clean refusal, a larger representational rank, survival of the same perturbation used in training, or resistance without a defense-aware attacker.

## Sources

[^deeprefusal]: Xie et al., [*DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings EMNLP 2025.
[^ada]: Zhang et al., [*Any-Depth Alignment*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^separate]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^cb]: Schwinn & Geisler, [*Revisiting the Robust Alignment of Circuit Breakers*](https://arxiv.org/abs/2407.15902), 2024 preprint.
[^audit]: Qi et al., [*On Evaluating the Durability of Safeguards*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^cones]: Wollschläger et al., [*The Geometry of Refusal*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^arditi]: Arditi et al., [*Refusal Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^sdd]: Chen et al., [*SDD*](https://aclanthology.org/2025.acl-long.1412/), ACL 2025.
[^seam]: Wang et al., [*Self-Destructive Language Models*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1abb0e7bd62ba80610798dee81950522-Abstract-Conference.html), ICLR 2026.
[^booster]: Huang et al., [*Booster*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a7ac8a21e5a27e7ab31a5f42a0117bdb-Abstract-Conference.html), ICLR 2025.
[^smooth]: Fan et al., [*Towards LLM Unlearning Resilient to Relearning Attacks*](https://proceedings.mlr.press/v267/fan25e.html), ICML 2025.
[^localize]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^unlearn]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^hide]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^tamper-eval]: Che et al., [*Model Tampering Attacks Enable More Rigorous Evaluations*](https://openreview.net/forum?id=E6OYbLnQd2), TMLR 2025.
[^invariant]: Wang et al., [*Invariance Makes LLM Unlearning Resilient*](https://proceedings.mlr.press/v267/wang25en.html), ICML 2025.
[^tb]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
