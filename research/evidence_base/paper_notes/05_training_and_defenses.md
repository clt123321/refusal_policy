# Paper notes — training mechanisms and defenses

## Xie et al. — *DeepRefusal*

- **Authors / status / date:** Xie et al.; Findings of EMNLP 2025; November 2025.
- **Question:** Can a model learn to reconstruct refusal after its dominant direction is removed?
- **Mechanism:** Probabilistic refusal-direction ablation across layers/tokens during training.
- **Result / endpoint:** Models rebuild refusal from attacked internal states and resist tested input/activation attacks.
- **Strongest evidence:** Recovery under unseen ablation locations and jailbreaks.
- **Limitation:** It is not a certificate against cheap adaptive parameter edits; Findings, not EMNLP main.
- **Relation:** Fatal collision with generic “train under writer fault” and self-repair defense claims.
- **Source:** [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.956/).

## Zou et al. — *Circuit Breakers*

- **Authors / status / date:** Zou et al.; NeurIPS 2024 main conference; December 2024.
- **Question:** Can training reroute harmful internal trajectories rather than memorize refusal strings?
- **Mechanism:** Representation rerouting / circuit breaking.
- **Result / endpoint:** The learned rerouting generalizes across several attack modalities.
- **Limitation:** Generalization does not imply open-ended white-box durability.
- **Relation:** Prior for representation-level fault training and mechanism-guided defense.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97ca7168c2c333df5ea61ece3b3276e1-Abstract-Conference.html).

## Zhang et al. — *Any-Depth Alignment*

- **Authors / status / date:** Zhang et al.; ICLR 2026 main conference; April 2026.
- **Question:** Why does safety fail once a harmful continuation has begun?
- **Mechanism:** Reinject assistant safety tokens at intermediate generation depths, plus probing/lookahead.
- **Result / endpoint:** Safety is front-loaded but can be re-triggered at arbitrary generation depth.
- **Strongest evidence:** Intervention-depth curves over already-harmful continuations.
- **Limitation:** Input/prefill defense rather than weight-tamper durability.
- **Relation:** Disruptive temporal perspective; suggests recovery dynamics may matter more than static rank.
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html).

## Maini et al. — *Safety Pretraining*

- **Authors / status / date:** Maini et al.; NeurIPS 2025 main conference; December 2025.
- **Question:** Should safety be learned during pretraining rather than only post-training?
- **Mechanism:** Filtering, rephrasing, native refusal and harmfulness tags during pretraining.
- **Result / endpoint:** Reported gains against input attacks without observed general-task loss.
- **Limitation:** White-box adaptive removal is not the primary endpoint.
- **Relation:** Challenges the project’s post-training-only boundary and supplies a provenance contrast.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e84c4e0acee2be072571fedc70700a9-Abstract-Conference.html).

## Zhang et al. — *Understanding and Preserving Safety in Fine-Tuned LLMs*

- **Authors / status / date:** Zhang et al.; arXiv preprint; January 2026.
- **Question:** How do safety and utility gradients interact under fine-tuning?
- **Mechanism:** Low-rank safety-gradient subspace and conflict projection.
- **Result / endpoint:** Safety gradients are low rank and often conflict with utility gradients; projection improves tested safety preservation.
- **Limitation:** Preprint; gradient subspace is optimizer- and data-dependent.
- **Relation:** High collision with optimization-gradient subspace and utility-projection defense.
- **Source:** [arXiv](https://arxiv.org/abs/2601.10141).

## Springer et al. — *The Geometry of Alignment Collapse*

- **Authors / status / date:** Springer et al.; arXiv preprint; February 2026.
- **Question:** Why can initially orthogonal benign gradients later damage safety?
- **Mechanism:** Curvature-coupled gradient dynamics in sharp low-dimensional safety regions.
- **Result:** Second-order dynamics enter safety-sensitive regions despite first-order orthogonality.
- **Limitation:** Preprint; curvature estimates and claimed time law need broad replication.
- **Relation:** A warning that first-order co-control/common-gradient measures may miss the attack path.
- **Source:** [arXiv](https://arxiv.org/abs/2602.15799).

## Zhang et al. — *LLM-VA*

- **Authors / status / date:** Haonan Zhang et al.; ACL 2026 main conference; May/July 2026.
- **Question:** Can safety judgment and willingness to answer be causally coupled with a small weight update?
- **Mechanism:** SVM directions and closed-form minimum-norm weight alignment.
- **Result / endpoint:** Reported improvement to the jailbreak/over-refusal frontier over 12 models.
- **Limitation:** Input-attack safety rather than adaptive white-box removal; minimum norm is parameterization-specific.
- **Relation:** Direct collision with vector-coupling and principled low-rank safety weight-edit claims.
- **Source:** [arXiv record, marked ACL 2026 Main](https://arxiv.org/abs/2601.19487).
