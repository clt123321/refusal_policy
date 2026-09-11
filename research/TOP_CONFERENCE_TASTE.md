# Top-Conference Taste Review

## Thesis

Strong papers in this neighborhood usually do not win by adding a metric. They
invalidate a trusted proxy, replace it with one simple object, and make that object
predict an intervention outside the measurement pipeline. Their first figure is a
counterexample or frontier, not a taxonomy.

## Fifteen useful exemplars

| Paper | One-sentence insight | Surprise and simplification | Strongest experiment / Figure 1 | Why it generalizes; restraint | Why a reviewer can believe it |
|---|---|---|---|---|---|
| Arditi et al., NeurIPS 2024[^1] | A single residual direction causally mediates much refusal. | A complex policy compresses to add/remove one vector. | Cross-model bidirectional addition/ablation; Fig. 1 makes the manipulation visible. | Spans many open model families; does not claim all safety is one-dimensional. | One object, two-sided causal intervention, broad replication. |
| Concept Cones, ICML 2025[^2] | Refusal is multidirectional, and orthogonality is not functional independence. | The trusted proxy—one direction or orthogonal directions—fails. | Intervention matrix over optimized multiple directions. | The distinction applies beyond refusal; no attempt to turn every geometric statistic into a contribution. | It contains a decisive counterexample to the previous simplification. |
| Zhao et al., NeurIPS 2025[^3] | Recognizing harm and choosing to refuse are different causal variables. | A model can know without acting. | Position-aware steering and reply-inversion; fine-tuning erases refusal while recognition survives. | Explains jailbreak and latent monitoring with the same distinction. | Multiple interventions separate two constructs cleanly. |
| Beyond *I’m Sorry*, AAAI 2026[^4] | Refusal comes from interacting sparse features, including dormant backups. | Features invisible in the intact model become causal after a primary path is suppressed. | Minimal interacting set plus conditional backup discovery. | Connects SAE features to circuit redundancy; stays at activation-level claims. | Conditional interventions expose why one-shot attribution is incomplete. |
| TAR, ICLR 2025[^5] | Train directly against future tampering if tamper resistance is the objective. | Standard alignment strength is not durability. | Inner-loop attack curves comparing ordinary and meta-trained safeguards. | Applies to multiple safeguarded behaviors; threat model is explicit. | The training objective and evaluation endpoint match. |
| Durability Audit, ICLR 2025[^6] | Small attack implementation choices can reverse safeguard rankings. | Published robustness may be optimizer fragility. | Case studies where shuffling/trainer/schedule changes defeat defenses. | General methodological lesson; intentionally does not invent a mechanism. | Reproducible falsification of strong claims is itself the contribution. |
| TamperBench, KDD 2026 D&B[^7] | No single attack ranking transfers across open-weight safeguards. | “Strongest attack” is model-specific. | Model × attack heatmap and utility-constrained envelope. | Broad panel and per-pair tuning; refrains from claiming a universal internal cause. | Standardized adversarial comparison exposes interaction effects. |
| Deep Ignorance, ICLR 2026[^8] | Never learning a capability is much harder to reverse than suppressing it later. | Training provenance dominates superficial endpoint matching. | Long 10k-step / 300M-token recovery frontier. | A training-origin principle, not a refusal benchmark trick. | Large compute, matched models and a hard boundary condition. |
| Any-Depth Alignment, ICLR 2026[^9] | Safety can be re-triggered after harmful generation has already begun. | Alignment is temporally front-loaded but not irrecoverable. | Sweep intervention depth over harmful continuations. | One temporal insight explains prefilling and mid-generation failure; no broad white-box claim. | The intervention directly manipulates the proposed depth variable. |
| Circuit Breakers, NeurIPS 2024[^10] | Rerouting harmful internal trajectories can generalize beyond refusal strings. | The target is representation trajectory, not the output token template. | Unseen text, multimodal and agent attack panel. | One mechanism objective crosses modalities; “circuit” remains operational, not overformalized. | Transfer beyond the trained attack supports the mechanism. |
| Hase et al., NeurIPS 2023[^11] | Where information is causally expressed need not be where it is best edited. | Causal localization fails as an editing prescription. | Layerwise localization-versus-edit-success mismatch. | General warning across editing methods; no replacement metric proliferation. | The negative result is controlled and attacks a widespread inference. |
| Mechanistic Unlearning, ICML 2025[^12] | High-level mechanism localization can improve robust knowledge removal. | Localization can help when it targets a predictive process rather than an activation peak. | Paraphrase and relearning robustness after mechanism-targeted edits. | Reconciles negative localization results through a sharper construct. | Intervention, generalization and attack all correspond to the same mechanism. |
| Unlearning or Obfuscating?, ICLR 2025[^13] | Many unlearning methods hide knowledge that benign tuning can recover. | “Forgotten” benchmark behavior is reversible access suppression. | Recovery curve under small, loosely related benign data. | Separates erasure from accessibility across benchmarks. | A cheap, simple attack invalidates a comfortable endpoint. |
| Erase or Hide?, ICLR 2026[^14] | Spurious negative inhibitors can mimic durable unlearning. | Successful suppression can preserve the underlying capability. | Identify/suppress inhibitor neurons and test reappearance. | A mechanism explains multiple relearning failures; avoids claiming all unlearning is identical. | The proposed latent cause is directly intervened on. |
| Adversarial Parameter Attack, ICML 2023[^15] | Tiny weight perturbations can selectively destroy robustness while preserving accuracy. | Behavioral utility is compatible with severe property loss. | Worst-case parameter perturbation versus random/noise controls. | The principle extends beyond LLMs; constrained threat model is explicit. | A clean utility–robustness dissociation establishes security relevance. |

## Storytelling techniques that recur

### 1. Kill a trusted proxy

The memorable distinction is usually a negation:

- orthogonality ≠ functional independence;
- localization ≠ editability;
- behavioral forgetting ≠ knowledge erasure;
- clean safety ≠ tamper durability;
- recognizing harm ≠ acting safely.

For this project, `representation redundancy ≠ parameter fault independence` is
plausible only if a real ranking reversal is shown. Without the reversal it is a
reasonable analogy, not new knowledge.

### 2. One abstraction, one key operation

The best papers make the noun executable: a refusal direction can be added or
removed; a harmfulness representation can be inverted; a safeguard can be attacked
for a stated budget. `writer-cut × (1-CC)` fails this taste test because it combines
two partly arbitrary constructs. A joint finite-edit frontier has a direct
operation: spend attack resources, suppress k independently validated components,
and constrain held-out benign change.

### 3. Figure 1 is the paper, not the pipeline

The strongest Figure 1 for this project is a four-panel matched counterexample:

1. two checkpoints match on clean refusal and benign utility;
2. they match on activation rank and restricted causal cut;
3. one carrier-blind finite parameter edit jointly suppresses the apparent writers
   in only one checkpoint;
4. an independently optimized adaptive attack yields separated safety–utility
   frontiers in the predicted direction.

A workflow DAG, a PCA plot or a list of metrics belongs later.

### 4. Leave the measurement distribution

Representation evidence becomes mechanistic when it predicts a new operator,
prompt family, attack objective or model. The carrier projector must not define the
writer, the common-mode edit and the validating attack. Otherwise “prediction” is
repeated measurement of the same loss.

### 5. Security results are frontiers

A point estimate hides the trade-off. Strong security work plots harmful capability
or compliance against benign utility and actual attacker budget, and reports the
best-found envelope. It does not call parameter L2 a real-world work factor or an
unsuccessful search a certificate.

### 6. Generality comes from prediction, not benchmark count

One mechanism predicting activation faults, carrier-blind low-rank edits and short
fine-tuning is stronger than ten benchmark tables using the same refusal judge. A
second lightweight backbone is useful; a second safeguard domain belongs only in a
future paper unless it is needed to support the title.

### 7. Restraint earns trust

The project should explicitly decline to claim global minimum cuts, intrinsic
control energy, SFT/DPO/RL causal effects, general learned-safeguard laws or a
certified defense. Stating those boundaries will make the narrow result more
credible.

## Taste verdict on the present story

`Objective → geometry → robustness` reads like a concatenation of recent papers.
`Many writers share one fuse` is vivid but, alone, resembles Arditi plus a shared
Jacobian or NeuroStrike. The main-conference version needs one decisive surprise:

> At matched behavior, activation rank and functional cut, the “more redundant”
> model is easier to tamper with; a carrier-blind common-cause measurement predicts
> the reversal and competing geometry/Fisher/routing measures do not.

The recipe should be a variation generator. The paper should be about the failed
proxy and the cross-space mechanism.

## Sources

[^1]: [Arditi et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html).
[^2]: [Wollschläger et al., ICML 2025](https://proceedings.mlr.press/v267/wollschlager25a.html).
[^3]: [Zhao et al., NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html).
[^4]: [Prakash et al., AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/41119).
[^5]: [Tamirisa et al., ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html).
[^6]: [Qi et al., ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html).
[^7]: [Hossain et al., KDD 2026 Datasets & Benchmarks](https://doi.org/10.1145/3770855.3817557).
[^8]: [O’Brien et al., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html).
[^9]: [Zhang et al., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html).
[^10]: [Zou et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97ca7168c2c333df5ea61ece3b3276e1-Abstract-Conference.html).
[^11]: [Hase et al., NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html).
[^12]: [Guo et al., ICML 2025](https://proceedings.mlr.press/v267/guo25k.html).
[^13]: [Hu et al., ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html).
[^14]: [Yang et al., ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html).
[^15]: [Yu et al., ICML 2023](https://proceedings.mlr.press/v202/yu23f.html).
