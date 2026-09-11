# Novelty collision matrix

This matrix is intentionally hostile to the current project. “Difference” means a
testable difference, not a change of vocabulary. Venue labels distinguish archival
main-conference work from preprints.

| Our concept or claim | Closest prior work | Overlap | Defensible difference | Is the difference scientifically meaningful? | Risk |
|---|---|---|---|---|---|
| Refusal is carried by a small causal set | Arditi et al., NeurIPS 2024; Prakash et al., AAAI 2026 | Activation addition/ablation and minimal causal refusal features | None if the result is only “a few directions/features matter” | No | **FATAL COLLISION** |
| Several refusal writers | Concept Cones, ICML 2025; SOM, AAAI 2026; Yeo et al., preprint | Multiple directions/features causally control refusal | Writers could be parameter-producing modules rather than activation directions | Only if module-level claims survive activation and weight interventions | **HIGH RISK** |
| Dormant backups appear after ablation | Prakash et al., AAAI 2026; CoAx, 2026 preprint; circuit-completeness work, NeurIPS 2025 | Conditional suppression exposes redundant features/OR-like paths | Safety-specific parameter common cause behind the backups | Yes, but backup discovery itself is not new | **FATAL** for backups; **DIFFERENTIATED** for common cause |
| `writer-cut` as a minimal knockout set | Prakash et al., AAAI 2026; sparse feature circuits, ICLR 2025; CoAx | Greedy minimal causal sets and circuit knockout | A restricted, utility-constrained cut over a preregistered intervention library | Modestly; it is an empirical attack statistic, not a global graph cut | **HIGH RISK** |
| Geometry reflects training | Labunets, 2026 preprint; Zhao et al., NeurIPS 2025 | Training signal shapes low-rank gradients/activations and separable safety axes | Whether the induced representation predicts adaptive white-box durability | Yes—the security endpoint is absent from the closest work | **FATAL** for broad claim; **DIFFERENTIATED** for bridge |
| `co-controllability` | Concept Cones; LLM-VA, ACL 2026; HARC and alignment-collapse preprints | Functional independence, vector coupling, shared control and gradient modes | A *finite*, utility-constrained parameter edit jointly suppresses several causally validated carriers | Yes only if it predicts an independently optimized attack; infinitesimal Jacobian correlation is insufficient | **HIGH RISK / DIFFERENTIATED** |
| Representation redundancy ≠ security redundancy | Concept Cones; CoAx; circuit completeness; generic reliability engineering | Orthogonality ≠ independence and redundancy can hide shared causes | Cross-space dissociation: many activation carriers but one cheap parameter fault under utility constraints | Potentially yes; the joint activation-to-parameter-to-security counterexample is not directly established | **DIFFERENTIATED**, conditional |
| Geometry predicts breach cost | Durability evaluation, ICLR 2025; TamperBench, KDD 2026 D&B; Adversarial Parameter Attack, ICML 2023 | Attack-relative utility-constrained robustness and small parameter perturbations | A pre-attack mechanism statistic predicts the held-out adaptive attack frontier | Yes if incremental and out-of-sample; no if post-hoc | **HIGH RISK / DIFFERENTIATED** |
| `BreachCost` or `MTC50` | Durability evaluation; TamperBench | Budgeted attacks with utility ceilings | None unless measurement is explicitly operational and attack-relative | No as a standalone contribution | **FATAL COLLISION** |
| Train against carrier failure | Circuit Breakers, NeurIPS 2024; ReFAT; DeepRefusal, Findings EMNLP 2025 | Representation perturbation during training to improve robustness | Target empirically independent fault domains or a measured common cause | Possibly, but only after the common-cause diagnosis predicts attack transfer | **FATAL** for generic defense |
| Couple detection to refusal | Zhao et al.; Knowing without Acting; HARC; Detection-to-Refusal; LLM-VA | Separate recognition/action representations and explicitly couple them | White-box durability of that coupling | Endpoint difference is meaningful, but decomposition/coupling is not new | **FATAL** for mechanism; **HIGH RISK** for defense |
| Low-rank writer/reader defense | AMRA, 2026 preprint; LLM-VA, ACL 2026 | Closed-form or rank-k writer edits plus reader correction | None yet | No | **FATAL COLLISION** |
| Objective × response diversity is the cause | Labunets preprint; broad alignment-objective literature | Data surface form and objective affect gradients/representations | A carefully randomized manipulation within one objective, followed by security outcomes | Yes, but SFT/DPO/RL “diversity” is not one common treatment | **HIGH RISK** |
| Safety depth/self-repair | Any-Depth, ICLR 2026; DeepRefusal, Findings EMNLP 2025 | Safety can be re-triggered/rebuilt at later depths | Recovery dynamics predict weight-tamper durability | Potentially, but only if the bridge holds | **HIGH RISK** |
| Refusal findings generalize to learned safeguards | Deep Ignorance; unlearning/relearning papers at ICLR/ICML/EMNLP 2025–26 | Suppression can hide rather than erase capability; durability varies by training origin | A shared, calibrated predictor across refusal and unlearning | High value but too broad for the present paper without a second task | **CLEARLY OPEN, HIGH COST** |

## Collision verdict

The individual building blocks are mostly occupied. The narrow surviving claim is:

> Conditional on a frozen carrier definition and an explicit attack family,
> activation-level functional redundancy can coexist with a finite,
> utility-preserving parameter common mode; that common-mode statistic—not rank or
> carrier count—predicts a held-out adaptive tamper frontier.

This is not established by renaming a Jacobian, finding a shared gate, or fitting a
composite score after seeing the attacks. It requires a crossed dissociation and an
out-of-sample prediction.

## Sources

1. [Arditi et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html)
2. [Concept Cones, ICML 2025](https://proceedings.mlr.press/v267/wollschlager25a.html)
3. [Beyond *I’m Sorry, I Can’t*, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/41119)
4. [CoAx, arXiv 2026](https://arxiv.org/abs/2607.01940)
5. [Refusal Geometry Reflects Refusal Training, arXiv 2026](https://arxiv.org/abs/2608.25390)
6. [Durability of Open-Weight Safeguards, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html)
7. [TamperBench, KDD 2026 Datasets & Benchmarks](https://doi.org/10.1145/3770855.3817557)
8. [DeepRefusal, Findings of EMNLP 2025](https://aclanthology.org/2025.findings-emnlp.956/)
9. [LLM-VA, ACL 2026](https://arxiv.org/abs/2601.19487)
10. [Deep Ignorance, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html)
