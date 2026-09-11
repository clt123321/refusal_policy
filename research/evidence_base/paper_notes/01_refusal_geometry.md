# Paper notes — refusal representations and geometry

## Arditi et al. — *Refusal in Language Models Is Mediated by a Single Direction*

- **Authors / status / date:** Arditi et al.; NeurIPS 2024 main conference; December 2024.
- **Question:** Can refusal across harmful prompts be causally mediated by one residual-stream direction?
- **Mechanism and intervention:** Harmful–harmless difference-in-means, activation addition/ablation, and a rank-one weight edit.
- **Central result / security endpoint:** One direction strongly controls refusal with limited measured broad-capability loss; the endpoint is activation-level refusal suppression, not adaptive tamper work factor.
- **Strongest figure-level evidence:** Layerwise addition and ablation show bidirectional behavioral control across model families.
- **Limitation:** The direction can mix harm recognition, policy choice, response prefix and topic; one successful edit is not a proof of global one-dimensionality.
- **Relation / collision:** Foundation for the project, but fatal to any “first low-dimensional refusal carrier” claim.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html).

## Wollschläger et al. — *The Geometry of Refusal in Large Language Models*

- **Authors / status / date:** Wollschläger et al.; ICML 2025 main conference; July 2025.
- **Question:** Is a single vector an adequate model of refusal?
- **Mechanism and intervention:** Concept cones, optimized multiple directions and functional intervention tests.
- **Central result:** Multiple causally effective directions exist; geometric orthogonality does not imply representational independence.
- **Endpoint:** Activation-level jailbreak/refusal control.
- **Strongest evidence:** Multiple vectors outperform a single direction and reveal a cone-like organization.
- **Limitation:** It does not establish parameter-space fault independence or adaptive white-box cost.
- **Relation / collision:** Fatal to broad multidimensional-geometry novelty; motivates, but does not prove, activation/parameter dissociation.
- **Source:** [PMLR](https://proceedings.mlr.press/v267/wollschlager25a.html).

## Prakash et al. — *Beyond I’m Sorry, I Can’t*

- **Authors / status / date:** Prakash et al.; AAAI 2026 main conference, AI Alignment special track; March 2026.
- **Question:** Which interacting sparse features causally produce refusal?
- **Mechanism and intervention:** Direction-seeded SAE search, greedy minimal feature set, factorization-machine interaction analysis and conditional suppression.
- **Central result:** A minimal interacting set can flip refusal; dormant redundant features appear after primary features are removed.
- **Endpoint:** Activation-level refusal knockout.
- **Strongest evidence:** The minimal-set intervention plus recovery of dormant backups.
- **Limitation:** The atomization depends on the SAE and intervention library; it does not measure adaptive weight-tamper cost.
- **Relation / collision:** Near-direct collision with `writer-cut`, backup writers and interaction-search novelty.
- **Source:** [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/41119).

## Piras et al. — *SOM Directions Are Better than One*

- **Authors / status / date:** Piras et al.; AAAI 2026 main conference; March 2026.
- **Question:** Do multiple extracted directions suppress refusal more effectively than one?
- **Mechanism and intervention:** Self-organizing-map directions and multi-direction ablation.
- **Central result:** Multi-direction ablation improves refusal suppression over the single-direction baseline and several jailbreaks.
- **Endpoint:** Activation-level refusal suppression.
- **Limitation:** Better attack efficacy is not a theory of security redundancy or parameter fault domains.
- **Relation / collision:** High collision with multi-direction attack and low-dimensional-manifold claims.
- **Source:** [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/40551).

## Joad et al. — *There Is More to Refusal … than a Single Direction*

- **Authors / status / date:** Joad et al.; arXiv preprint; February 2026.
- **Question:** Do different refusal categories share one representation and one behavioral control?
- **Mechanism and intervention:** Compare and steer directions across eleven refusal/non-compliance categories.
- **Central result:** Category directions differ geometrically, while steering behaves like a shared low-dimensional refusal/over-refusal control.
- **Endpoint:** Activation-level behavior.
- **Limitation:** Preprint; no adaptive parameter attack.
- **Relation / collision:** A direct natural counterexample to “more geometric directions imply more independent control.”
- **Source:** [arXiv](https://arxiv.org/abs/2602.02132).

## Labunets — *Refusal Geometry Reflects Refusal Training*

- **Authors / status / date:** Labunets; arXiv preprint v2; August/September 2026.
- **Question:** Why does refusal become low rank?
- **Mechanism and intervention:** Checkpoint study plus controlled synthetic fine-tuning; gradient and activation stable rank.
- **Central result:** Repeated refusal openings concentrate gradients and activations; diverse openings raise rank and weaken fixed-vector ablation.
- **Endpoint:** Fixed activation ablation, not adaptive weight tampering.
- **Strongest evidence:** Controlled manipulation of early response diversity links supervision to gradient rank and ablation sensitivity.
- **Limitation:** Surface diversity may change semantic supervision; security is evaluated with a fixed intervention.
- **Relation / collision:** Fatal to the broad `training signal → geometry` novelty. The remaining gap is `geometry → adaptive work factor`.
- **Source:** [arXiv](https://arxiv.org/abs/2608.25390).
