# Novelty Collisions and Current-Story Autopsy

## Bottom line

The vocabulary is newer than most of the science. `writer-cut`,
`co-controllability` and `BreachCost` should not be presented as contributions by
themselves. The only credible novelty is a prospective cross-space dissociation:

> Functionally redundant activation mechanisms can share a low-cost parameter
> failure cause, and a carrier-blind measure of that cause predicts a separately
> optimized white-box attack frontier.

The full collision table is in
[`evidence_base/collision_matrix.md`](evidence_base/collision_matrix.md).

## Three strongest collisions

### 1. Minimal writers and backups are already occupied

AAAI 2026 identifies interacting minimal SAE refusal-feature sets and dormant
backups.[^1] Concept Cones rejects the equivalence of orthogonality and functional
independence,[^2] while CoAx formalizes conditional discovery of hidden backup
components.[^3] Thus `writer-cut` cannot be sold as the first minimal causal set,
and backup re-extraction cannot be a headline.

### 2. Training-to-geometry and geometry-to-fragility are already occupied

Labunets connects repeated refusal openings to gradient/activation rank and fixed
ablation robustness.[^4] Skin-Deep already proposes an activation-geometry
fragility score,[^5] while very recent work proposes Fisher/curvature and output
routing as explanations of fine-tuning collapse.[^6][^7] A new rank or trajectory
metric is therefore a fatal novelty failure.

### 3. Sparse common bottlenecks and fault-trained defenses are already occupied

NeuroStrike reports that pruning a sub-percent safety-neuron set can break many
models and transfer to fine-tuned descendants.[^8] DeepRefusal, SafeNeuron and
NeuronGuard train against removal/freeze of identified refusal or safety units to
induce robustness.[^9][^10][^11] “One fuse” and “force the model to create backups”
are not new without a stronger cross-operator result.

## Autopsy by concept

### `causal carrier`

- **Prior synonym:** causal direction, safety neuron, SAE refusal feature, circuit node.
- **Keep?** Yes, as a construct with removal/addition/patch/rescue evidence.
- **Artifact risk:** harmfulness topic, refusal prefix and output style can all load on the same contrast.
- **Prediction:** a carrier intervention changes content-level harmful compliance while preserving matched benign behavior.
- **If deleted:** there is no mechanism paper, only attack benchmarking.
- **Decision:** **KEEP, rename only when a precise operator is specified.**

### `writer`

- **Prior synonym:** residual writer, circuit component, neuron/head/MLP attribution.
- **Keep?** Only as a module that makes a measurable causal contribution to a separately validated policy carrier.
- **Artifact risk:** all writer scores may be projections onto the same policy vector, manufacturing apparent co-control.
- **Prediction:** atom-local interventions and an independently fitted readout reproduce the writer’s effect.
- **If deleted:** the common-cause question can still be asked at module/layer level.
- **Decision:** **MERGE into causal component; do not claim a new primitive.**

### `writer-cut`

- **Prior synonym:** minimal SAE feature set, circuit knockout, restricted causal cut.
- **Need for a new name:** low.
- **Artifact risk:** top-m intact attribution misses Hydra/CoAx backups; the cut changes with atomization and operator.
- **Prediction:** within a frozen, preregistered intervention library, a larger restricted cut predicts survival under independent component faults.
- **If deleted:** little is lost; report the intervention-response curve directly.
- **Decision:** **DEMOTE to restricted empirical cut; never call it a global min-cut.**

### `shared gate`

- **Prior synonym:** downstream bottleneck, output routing, common-cause component.
- **Need for a new name:** none.
- **Artifact risk:** expected because multiple upstream components feed one readout; a common projector can make the result tautological.
- **Prediction:** a carrier-blind edit to the candidate gate suppresses multiple independently read out carriers and changes behavior under a utility ceiling.
- **If deleted:** no loss; use it as one null explanation.
- **Decision:** **DELETE as a named contribution; preregister as a simpler baseline.**

### `co-controllability`

- **Prior synonym:** Jacobian coupling, joint editability, shared gradient/control mode.
- **Need for a new name:** weak; classical controllability has stronger assumptions than the project satisfies.
- **Artifact risk:** infinitesimal Jacobian correlation may not extrapolate to a behavior-changing finite edit; raw parameter norm is coordinate-dependent.
- **Prediction:** a finite carrier-blind parameter edit jointly suppresses several causal components with bounded held-out benign functional change, and its ordering transfers to another attack family.
- **If deleted:** replace with an explicit **joint finite-edit frontier**.
- **Decision:** **RENAME and operationalize; do not invoke Kalman controllability.**

### `breach cost`

- **Prior synonym:** adaptive tamper budget, attack-success/utility frontier, durability.
- **Need for a new name:** none.
- **Artifact risk:** “minimum” is only the best found attack; GPU time, tokens, queries and parameter norms are not interchangeable.
- **Prediction:** model ordering remains stable across at least two independently optimized attack families or else is declared attack-specific.
- **If deleted:** use the operational adversarial value surface from existing durability methodology.
- **Decision:** **MERGE into attack-relative operational frontier.**

## Claims that must not appear

- first evidence that refusal is low dimensional;
- first multidimensional refusal geometry or backup refusal feature;
- first minimal causal refusal set;
- first link from refusal training to geometry;
- first mechanism-based defense or fault-injection defense;
- first utility-constrained white-box tamper benchmark;
- global neural-network min-cut or true minimum attack cost;
- parameter L2 as intrinsic control energy;
- SFT/DPO/RL as randomized causal treatments;
- learned-safeguard generality without a non-refusal safeguard.

## Surviving gap against five nearest neighbors

| Neighbor | What it solves | What it does not solve |
|---|---|---|
| Concept Cones | Multiple directions and functional dependence | Parameter common cause and adaptive attack cost |
| Beyond *I’m Sorry* / CoAx | Minimal causal set and dormant backups | Cross-space parameter editability |
| Labunets | Training diversity → rank → fixed ablation | Carrier-blind adaptive tamper frontier |
| Skin-Deep / Fisher / routing work | Scalar pre-attack fragility diagnostics | Validated multi-carrier common-cause mechanism with ranking reversal |
| NeuroStrike | Tiny sparse-neuron common bottleneck | General finite-edit frontier and incremental prediction beyond neuron concentration |
| TamperBench | Broad adaptive security endpoint | An internal mechanism that prospectively predicts its frontier |

## The fatal test

The main claim dies if the common-mode statistic fails to improve held-out attack
prediction beyond rank, GFS, Fisher/curvature, late-routing concentration, clean
refusal, benign utility, KL drift and training dose—or if the effect vanishes when
the attack does not reuse the carrier projector.

## Sources

[^1]: Prakash et al., [AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/41119).
[^2]: Wollschläger et al., [ICML 2025](https://proceedings.mlr.press/v267/wollschlager25a.html).
[^3]: Gong et al., [arXiv 2026](https://arxiv.org/abs/2607.01940).
[^4]: Labunets, [arXiv 2026](https://arxiv.org/abs/2608.25390).
[^5]: Lee et al., [arXiv 2026](https://arxiv.org/abs/2606.22676).
[^6]: Malla et al., [arXiv 2026](https://arxiv.org/abs/2609.06934).
[^7]: Guo et al., [arXiv 2026](https://arxiv.org/abs/2609.01455).
[^8]: Wu et al., [NDSS 2026 paper](https://www.ndss-symposium.org/wp-content/uploads/2026-s660-paper.pdf).
[^9]: Xie et al., [Findings of EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.956/).
[^10]: Wang et al., [SafeNeuron preprint](https://arxiv.org/abs/2602.12158).
[^11]: Gao et al., [NeuronGuard preprint](https://arxiv.org/abs/2608.23959).
