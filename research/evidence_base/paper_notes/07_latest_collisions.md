# Paper notes — September 2026 collision sweep

These papers were searched because they cite or extend the refusal-geometry,
fine-tuning fragility and circuit-redundancy lines. They substantially narrow the
available novelty.

## Malla et al. — *The Geometry of Refusal: Why Post-Hoc Safety Is Fragile and Pretraining-Time Safety Persists*

- **Status/date:** arXiv preprint, 7 September 2026.
- **Question:** Why does post-hoc refusal disappear under benign fine-tuning while pretraining-time safety persists?
- **Claim/mechanism:** Post-hoc safety is a thin, sharp suppression relative to capability empirical-Fisher geometry; sustained safety co-training is harder to erase.
- **Intervention/security endpoint:** Benign fine-tuning over several model families and scratch co-training; refusal retention with capability matching.
- **Strongest evidence:** A combined training-origin, geometry and 100-step collapse result, plus larger scratch-trained comparisons.
- **Crucial internal counterexample:** Compute-matched continuous and windowed schedules reportedly have similar proposed scalar geometry yet very different durability. Thus the scalar does not fully determine security.
- **Collision:** Extremely high for any generic parameter-geometry headline. The residual gap is whether a common-cause/intervention statistic explains the mismatch and predicts a different attack family.
- **Source:** [arXiv](https://arxiv.org/abs/2609.06934).

## Guo et al. — *When Safety Routing Breaks*

- **Status/date:** Findings of EMNLP 2026 accepted, according to the arXiv record; 1 September 2026.
- **Question:** Why can benign tuning destroy safety while preserving utility?
- **Claim/mechanism:** Safety representations remain accessible, while late output-side MLP routing becomes fragile; small benign tuning re-sharpens those paths.
- **Intervention/security endpoint:** Benign fine-tuning, Fisher decomposition, logit lens and cross-condition patching; safety/utility change.
- **Strongest evidence:** Layer/module-level curvature movement localized to late output routing.
- **Limitation:** One primary attack family and no operational minimum cut.
- **Collision:** A simpler competitor to “shared gate” or late-writer concentration. If common-mode editability reduces to this module score, the project adds little.
- **Source:** [arXiv](https://arxiv.org/abs/2609.01455).

## Lee et al. — *Skin-Deep*

- **Status/date:** arXiv preprint, June 2026.
- **Question:** Can a model’s pre-attack activation geometry diagnose alignment fragility?
- **Claim/mechanism:** A cPCA safety subspace and depth-weighted Geometry Fragility Score track limited-model refusal retention under rank-8 benign LoRA.
- **Strongest evidence:** Pre-attack ranking of a small panel of safety-tuned models.
- **Limitation:** Limited independent safety-model sample, one central attack family, scalar activation metric and refusal-heavy endpoint.
- **Collision:** Directly occupies “activation geometry predicts tampering.” Any new predictor must beat GFS under held-out attacks and runs.
- **Source:** [arXiv](https://arxiv.org/abs/2606.22676).

## Lan et al. — *Dynamic Adversarial Fine-Tuning Reorganizes Refusal Geometry*

- **Status/date:** arXiv preprint v3, May 2026.
- **Question:** How does dynamic adversarial training reorganize refusal?
- **Claim/mechanism:** Carrier location and utility coupling change substantially while stable rank remains near-constant; late adaptive attacks recover.
- **Strongest evidence:** A joint robustness–utility–carrier trajectory under SFT/R2D2.
- **Limitation:** Narrow backbone and attack portfolio.
- **Collision:** A clean counterexample to “higher rank is the explanation.”
- **Source:** [arXiv](https://arxiv.org/abs/2604.27019).

## Gao et al. — *NeuronGuard*

- **Status/date:** arXiv preprint reporting Findings of EMNLP 2026; August 2026.
- **Question:** Can repeated neuron fault injection redistribute safety mechanisms?
- **Mechanism:** Refreshed safety-neuron probes, deliberate ablation, KL consistency and randomized gradient projection.
- **Endpoint:** Jailbreak and iterative neuron-pruning robustness plus task accuracy.
- **Limitation:** Adaptive evaluation remains close to the defense’s neuron fault model rather than unconstrained target-specific fine-tuning.
- **Collision:** Near-fatal for a defense based on deliberately disabling known safety units during training.
- **Source:** [arXiv](https://arxiv.org/abs/2608.23959).

## Wang et al. — *SafeNeuron*

- **Status/date:** arXiv preprint, February 2026.
- **Question:** Can freezing safety neurons during DPO force redundant safety representation?
- **Mechanism/endpoint:** Effect-size neuron selection, selected-neuron freezing, pruning attacks and utility evaluation.
- **Limitation:** Neuron construct may mix recognition/action; defense and evaluation share an operator.
- **Collision:** Occupies “freeze the original fuse so training creates backup carriers.”
- **Source:** [arXiv](https://arxiv.org/abs/2602.12158).

## Wu et al. — *NeuroStrike*

- **Status/date:** NDSS 2026 main conference.
- **Question:** Can pruning a tiny set of safety neurons remove alignment and transfer to descendants?
- **Claim:** Sub-percent targeted pruning reportedly yields high attack success across more than twenty models and transfers across fine-tuned descendants.
- **Security endpoint:** Harmful compliance with utility evaluation.
- **Limitation:** Sparse neuron zeroing is still one attack primitive; some utility loss is nontrivial.
- **Collision:** The most dangerous existing “shared fuse” result. Main-conference novelty requires going beyond sparse bottleneck existence to a cross-space, prospective prediction of adaptive cost.
- **Sources:** [NDSS paper](https://www.ndss-symposium.org/wp-content/uploads/2026-s660-paper.pdf), [arXiv](https://arxiv.org/abs/2509.11864).
