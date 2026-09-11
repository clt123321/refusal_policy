# Timeline of the novelty boundary

This is a claim timeline, not a priority claim based only on arXiv timestamps. Main-conference, Findings/workshop and preprint status are kept separate.

| Date | Work and status | What changed | Consequence for `refusal_policy` |
|---|---|---|---|
| 2018 | Uesato et al., ICML | Weak attacks provide false security; adaptive evaluation is mandatory. | Every attack result is a lower bound on adversarial risk, not a certificate. |
| 2022 | ROME, NeurIPS | Causal activation localization can motivate a low-rank weight edit. | Established the activation→parameter bridge later used by refusal work. |
| 2022–2023 | Information-geometric sharpness; parameter reparametrization, NeurIPS | Raw parameter distance and Hessian geometry are coordinate dependent. | Do not call Euclidean weight norm “control energy.” |
| 2023 | Does Localization Inform Editing?, NeurIPS | Where a behavior is causally localized may not be where it is easiest to edit. | The project must demonstrate, not assume, a carrier→tamper link. |
| 2023 | Adversarial Parameter Attack, ICML | Small parameter changes can selectively destroy robustness while preserving normal accuracy. | Utility-preserving common-mode parameter attacks are not a new generic concept. |
| 2024 | Single refusal direction, NeurIPS | A direction can be necessary/sufficient for refusal and converted to a weight edit. | Baseline mechanism and attack primitive. |
| 2024 | Circuit Breakers, NeurIPS | Harmful trajectories can be rerouted rather than merely refused. | Representation-level defense predates writer-fault proposals. |
| 2024–2025 | ReFAT, arXiv preprint | Refusal-feature ablation is used as an adversarial training perturbation. | “Train under refusal ablation” is not a new defense principle. |
| 2025 | Concept Cones, ICML | Multiple interventionally meaningful directions replace the single-line account. | Multidimensional refusal geometry is already a main-conference result. |
| 2025 | Harmfulness/refusal separation, NeurIPS | Recognizing harm is causally distinct from executing refusal. | Harmful–harmless mean differences require construct controls. |
| 2025 | Safety Neurons, NeurIPS | A small neuron subset causally restores safety and overlaps with utility. | Module/neuron safety writers already have a strong prior. |
| 2025 | Hidden Safety Mechanisms, NeurIPS | Post-training can mask, rather than remove, safety mechanisms. | Behavioral collapse need not mean carrier destruction. |
| 2025 | TAR and durability audit, ICLR | Meta-training can move measured tamper resistance; small evaluator changes can reverse conclusions. | Defense/evaluation novelty is occupied; strict adaptive threat modeling is required. |
| 2025 | Sparse Feature Circuits, ICLR | Interpretable feature graphs support causal intervention and editing. | “Writer graph” is a measurement choice, not a new mechanism ontology. |
| 2025 | Mechanistic Unlearning, ICML | Mechanism-aware localization can improve relearning robustness. | A generalization beyond refusal must beat a strong mechanism-to-durability precedent. |
| 2025 | Unlearning or Obfuscating?, ICLR | Benign fine-tuning can revive apparently forgotten knowledge. | Suppression/accessibility is an essential counterexample class. |
| 2025 | Does Localization Inform Unlearning?, EMNLP | Effective unlearning updates are not uniquely determined by localized parameters. | Strengthens the localization≠editability warning. |
| 2025 | DeepRefusal, EMNLP Findings | Training across probabilistically ablated refusal states promotes self-repair. | Current targeted writer-fault defense has fatal novelty collision. |
| 2026 Q1 | Beyond I’m Sorry, AAAI | Minimal interacting SAE refusal feature sets and dormant backups are demonstrated. | Writer-cut/backups cannot be headline innovations. |
| 2026 Q1 | SOM Directions, AAAI | Multi-direction refusal suppression beats a single direction. | Multi-rank ablation is now a standard baseline. |
| 2026 Q1 | Any-Depth Alignment, ICLR | Safety is front-loaded but can be re-triggered mid-generation. | Static first-token geometry misses temporal safety renewal. |
| 2026 Q1 | Erase or Hide?, ICLR | Learned negative inhibitors can hide intact knowledge. | “More safety writers” may mean more suppressors, not more durable safety. |
| 2026 Q1 | Deep Ignorance, ICLR | Pretraining filtering survives vastly longer tampering than post-hoc safeguards, but retrieval bypasses it. | Refusal is only one safeguard regime; accessibility dominates some tasks. |
| 2026 Q1 | AntiDote, AAAI | Bi-level LoRA-adversarial defense is evaluated against a wide attack set. | Another direct collision with mechanism-derived tamper defense. |
| 2026 Q1–Q2 | Knowing without Acting; Safety Geometry; HARC, preprints | Detection/action coupling becomes a crowded explanatory object. | Use for controls, not central novelty. |
| 2026 Q1–Q2 | SPF; Alignment Collapse, preprints | First-order gradient conflict and second-order curvature are proposed as safety-failure mechanisms. | A static common gradient direction may miss the real dynamics. |
| 2026 Q1–Q2 | TamperBench, KDD D&B | Per-model/per-attack adaptive sweeps across 21 models and nine attacks become available. | “Benchmark + geometry” is insufficient; geometry must predict held-out attack behavior. |
| 2026 Q2 | Simple Attacks, preprint | Abliteration and prefilling defeat elaborate defenses; ART only partially repairs them. | Cheap attacks must precede expensive geometry pipelines. |
| 2026 Q2–Q3 | CoAx; AMRA, preprints | Conditional backups and residual writer/reader edits are explicit objects. | Remaining novelty narrows to common-cause parameter failure plus independent attack prediction. |
| 2026 Q3 | Refusal Geometry Reflects Training, preprint | Diverse refusal starts increase gradient/activation stable rank and weaken fixed vector ablation. | Training→rank→fixed attack is occupied; the adaptive weight-tamper endpoint remains open. |

## The remaining chronological gap

As of 2026-09-11, the audit did not find a paper that uses a frozen activation intervention ontology, measures finite utility-constrained simultaneous parameter suppression of its causal carriers, and prospectively predicts independent adaptive tampering cost. This is the only defensible opening found; it disappears if a new work supplies all three.

## Sources

- Venue/status and direct links are recorded row-by-row in [`papers.csv`](papers.csv).
- The highest-risk recent collisions are summarized in [`collision_matrix.md`](collision_matrix.md).
