# Evidence Map

**Audit cutoff:** 2026-09-11
**Question:** Does representation-level refusal organization explain how difficult it
is to remove a learned safeguard while preserving useful capability?

## Search and evidence policy

The search started from the required refusal-geometry and tamper-resistance seeds,
then followed author pages, reference lists, citing/related works and shared terms
through five adjacent literatures: safety circuits, adversarial fine-tuning,
model editing, unlearning/relearning and fault/control theory. The priority window
was 2025-01-01 through the audit date; earlier work was retained when it supplied a
methodological constraint.

Evidence was graded in this order:

1. archival conference proceedings and the paper itself;
2. official arXiv records for current preprints;
3. official code/model repositories as evidence of an artifact, not of a scientific claim;
4. community model cards only as candidate natural experiments.

The machine-readable index is [`evidence_base/papers.csv`](evidence_base/papers.csv).
Detailed cards are in [`evidence_base/paper_notes/`](evidence_base/paper_notes/),
with a chronological view in [`evidence_base/timeline.md`](evidence_base/timeline.md).

## The five converging literatures

### 1. Refusal changed from one vector to interacting causal sets

Arditi et al. showed that one residual-stream direction can causally control refusal
and can be translated into a rank-one weight edit.[^1] Concept Cones then showed
that multiple causally effective directions exist and that orthogonality is not
functional independence.[^2] AAAI 2026 work finds interacting minimal SAE feature
sets and dormant backups,[^3] while CoAx supplies a general conditional-ablation
method for discovering backups that intact-model attribution misses.[^4]

**Implication:** single direction, multiple directions, minimal feature set and
backup discovery are not available novelty claims. The open bridge is from
activation-level organization to a different intervention space: adaptive parameter
tampering.

### 2. Harm recognition is not refusal action

NeurIPS 2025 separates harmfulness encoding from refusal in position and causal
effect.[^5] Subsequent preprints elaborate recognition/execution axes, coupling and
detection-to-refusal circuits. LLM-VA already uses a small weight update to couple
safety judgment to willingness to answer.[^6]

**Implication:** harmful–harmless difference-in-means is not automatically a policy
carrier. Recognition, policy selection and response execution must be separately
validated. This distinction is a control, not our novelty.

### 3. Training already explains substantial geometry

Labunets directly links repeated early refusal tokens to concentrated gradients,
low-rank activations and sensitivity to a fixed direction ablation.[^7] Recent work
also proposes Fisher geometry, curvature and late output-routing explanations for
fine-tuning fragility.[^8][^9] One dynamic-training study reports large robustness
changes while stable rank remains nearly constant.[^10]

**Implication:** `objective/training → geometry` is occupied, and rank is already
known to be incomplete. SFT/DPO/RL labels should create variation, not serve as the
paper’s causal headline.

### 4. Durability is an adaptive, attack-relative frontier

TAR demonstrated that meta-adversarial training can improve resistance to tested
weight updates.[^11] The ICLR 2025 durability audit showed that small changes in
trainer, shuffling, templates and hyperparameters can reverse robustness
conclusions.[^12] TamperBench scales this to a model-by-attack panel and finds that
attack rankings are model-specific.[^13] Deep Ignorance shows that training origin
can change long-horizon recovery by orders of magnitude.[^14]

**Implication:** `BreachCost` is not a new endpoint, and a found attack is only an
upper bound on the unknown minimum. The outcome must be a utility-constrained,
operational budget frontier under a disclosed attack family.

### 5. Localization does not imply editability

The model-editing literature shows that causal activation localization can be
uncorrelated with the best parameter-edit location.[^15] Unlearning work likewise
shows that apparent removal can be an output inhibitor and that knowledge may
return under benign retraining.[^16][^17]

**Implication:** the activation-to-parameter link is neither automatic nor licensed
by causal mediation alone. This is the key unresolved scientific bridge.

## Evidence ladder for this project

| Level | What qualifies | What does not qualify |
|---|---|---|
| Correlation | Checkpoint rank correlates with refusal or attack outcome | Causal mechanism |
| Representation evidence | A direction/subspace decodes and generalizes OOD | Security relevance |
| Causal mediation | Remove/add, patch and rescue change content-level behavior on held-out prompts | Cheap parameter editability |
| Mechanistic explanation | A preregistered cross-space response model predicts a new intervention | Retrospective metric fitting |
| Security evidence | Carrier-blind adaptive attacks move an AHC–utility frontier at stated operational cost | Refusal keywords, one attack or raw weight norm |

## Explicitly conflicting results

| Apparent claim | Counterevidence | Audit interpretation |
|---|---|---|
| Refusal is one-dimensional | Concept Cones, SOM, SAE feature sets | A one-dimensional control can coexist with richer representation |
| More rank means more durability | Dynamic R2D2 work reports near-constant rank across changing robustness | Rank may be descriptive rather than explanatory |
| Geometry predicts fine-tuning fragility | Skin-Deep reports predictive GFS, but Malla reports schedules with similar scalar geometry and sharply different durability | No scalar has established regime-independent prediction |
| Where a behavior is caused is where it is editable | Localization–editing/unlearning studies find mismatch | Activation and parameter spaces require an explicit bridge |
| Fault-injection training creates durable redundancy | DeepRefusal/SafeNeuron/NeuronGuard improve in-family robustness; simple/adaptive attacks still break several defenses | Evaluate common-cause and held-out attacks, not only trained fault modes |
| Refusal removal means dangerous capability recovery | Deep Ignorance and unlearning distinguish access/policy from underlying capability | Claim only refusal-safeguard durability unless task success is measured |

## Most diagnostic public natural experiments

1. **DeepRefusal defended and community-tampered checkpoints:** cheap test of whether
   activation self-repair tracks weight/prefill durability; community cards are
   hypotheses only and require local re-evaluation.
2. **TAR checkpoints + TamperBench attacks:** blind mechanism measurements can be
   compared against a stronger attack portfolio than the defense was trained on.
3. **Concept Cones / multi-direction setups:** test whether more causal activation
   directions imply a higher parameter attack frontier.
4. **Deep Ignorance’s public model collection:** future boundary test between
   suppression and capability absence, not part of the current paper.
5. **NeuroStrike’s model/descendant panel:** test whether sparse-neuron transfer is a
   sufficient explanation for any measured common mode.

## Remaining evidence gap

No located paper jointly demonstrates all four of the following:

1. multiple carriers independently validated by removal, addition, patch and rescue;
2. a parameter edit learned without reusing the carrier projector that jointly
   suppresses those carriers with bounded benign functional change;
3. a matched ranking reversal where rank/cut and clean behavior point the wrong way;
4. prospective prediction of a separately optimized adaptive tamper frontier,
   beyond GFS, Fisher/curvature, routing concentration and baseline behavior.

That gap is narrow, falsifiable and worth a small gate. It is not yet evidence that
the proposed mechanism is true.

## Sources

[^1]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^2]: Wollschläger et al., [*The Geometry of Refusal in Large Language Models*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^3]: Prakash et al., [*Beyond I’m Sorry, I Can’t*](https://ojs.aaai.org/index.php/AAAI/article/view/41119), AAAI 2026.
[^4]: Gong et al., [*Conditional Co-Ablation*](https://arxiv.org/abs/2607.01940), arXiv preprint, 2026.
[^5]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^6]: Zhang et al., [*LLM-VA*](https://arxiv.org/abs/2601.19487), ACL 2026 main conference (status on arXiv record).
[^7]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv preprint, 2026.
[^8]: Malla et al., [*The Geometry of Refusal: Why Post-Hoc Safety Is Fragile and Pretraining-Time Safety Persists*](https://arxiv.org/abs/2609.06934), arXiv preprint, 2026.
[^9]: Guo et al., [*When Safety Routing Breaks*](https://arxiv.org/abs/2609.01455), arXiv record reporting Findings of EMNLP 2026.
[^10]: Lan et al., [*Dynamic Adversarial Fine-Tuning Reorganizes Refusal Geometry*](https://arxiv.org/abs/2604.27019), arXiv preprint, 2026.
[^11]: Tamirisa et al., [*Tamper-Resistant Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^12]: Qi et al., [*On Evaluating the Durability of Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^13]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^14]: O’Brien et al., [*Deep Ignorance*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html), ICLR 2026.
[^15]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^16]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^17]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
