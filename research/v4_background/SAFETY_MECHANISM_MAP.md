# Safety Mechanism Map

**Question:** What model-internal mechanisms implement safety behavior, and what evidence level supports each claim?

## Evidence ladder

| Evidence type | What it establishes | What it does not establish |
|---|---|---|
| Observation/probe | information is linearly/nonlinearly recoverable | that the information is used |
| Steering | changing a representation changes behavior | necessity or natural mediation |
| Ablation | a component/direction is necessary in the tested state | uniqueness, sufficiency, or parameter durability |
| Patching/rescue | a clean state restores behavior in a corrupted run | complete algorithm or best edit location |
| Weight edit | parameters can causally control behavior | that the edit targets the natural mechanism |
| Adaptive security evaluation | a safeguard survives searched attacks at a budget | universal robustness |

## Stage map

```text
input semantics / context
        ↓
harm & policy-violation recognition
        ↓
policy selection: answer / refuse / redirect / abstain
        ↓
response planning and token-level execution
        ↓
observable output or tool action

underlying task knowledge/capability feeds planning but is not identical to policy selection
```

The stages are an experimental decomposition, not a claim that the transformer contains clean modules with these names.

## Hypothesis inventory

| Mechanism hypothesis | Status | Direct evidence | Main conflict/limit | Defense implication |
|---|---|---|---|---|
| A compact residual direction can causally control refusal | **WE KNOW** for many tested 2024-era chat models | Addition, ablation and rank-one weight edit across 13 models in Arditi et al.[^arditi] | Later work finds multiple directions/cones; direction depends on prompts/positions | Single-direction attack is mandatory baseline, not complete threat model |
| Refusal is universally one-dimensional | **REJECTED as a general claim** | Some models admit a strong first direction | Concept Cones and multi-direction/SAE studies find additional independent controls[^cones] | Do not equate first-PC dominance with mechanism completeness |
| Multiple activation directions are functionally independent | **PLAUSIBLE**, model/definition dependent | Joint interventions and representational-independence tests in Concept Cones[^cones] | Orthogonality alone fails; a shared downstream gate can make directions co-fail | Require conditional/joint interventions and re-extraction after ablation |
| Harm recognition and refusal action are distinct | **WE KNOW** in tested families | Position-aware directions plus steering/reversal and attack analyses[^harm] | Boundary between recognition, policy and execution is still operationalized by probes | Evaluate recognition after refusal is removed; build separate endpoints |
| Harm recognition can reappear during unsafe generation | **PLAUSIBLE across prompt attacks** | HARC finds prompt- and response-position harm/refusal directions across five families and observes response-side recognition after prompt-side bypass[^harc] | Difference-of-means axes may mix content and action; HARC targets prompt attacks and fails quickly under harmful FT | Test whether late recognition can causally interrupt generation and survive weight edits |
| Safety is localized to a sparse neuron set | **PLAUSIBLE** | ~5% neurons restore >90% reported safety via dynamic patching[^neurons] | Attribution thresholds, neuron basis and model family affect sparsity; overlap with helpfulness | Sparse pruning is a necessary attack; “sparse” does not mean cleanly separable |
| Safety is an MLP/head circuit from detection to execution | **PLAUSIBLE** | Head/neuron ablation, patching and circuit-guided scaling in recent work[^circuit] | Mostly recent, author-side and refusal-centric; circuit completeness is difficult | Test both upstream detection and downstream action nodes, plus bypass paths |
| Safety can be dynamically reconstructed after an internal fault | **PLAUSIBLE** | DeepRefusal trains under layer/token refusal-direction ablation and transfers to several attacks[^deeprefusal] | Fine-tuning attack explicitly out of scope; reconstruction may target trained fault | Fault-injection training is promising only if held-out fault families transfer |
| Alignment is front-loaded at the assistant boundary | **WE KNOW** as a recurrent empirical pattern | Prefill failures, token-depth analyses, Any-Depth re-triggering[^ada][^deeprefusal] | Not every policy/model uses the same template; reasoning models may differ | Include long-prefill and decoding/config attacks; test safety throughout generation |
| Benign FT primarily breaks an output-side safety route while preserving upstream signal | **PLAUSIBLE** in two 7–8B families | Fisher localization, logit lens and final-layer activation patching in When Safety Routing Breaks[^routing] | SFT/DPO, English, two families; Fisher sharpness is local and LoRA/ASAM only delay collapse | Protecting one late route is insufficient unless it predicts held-out direct-edit and FT cost |
| Refusal training data shape refusal geometry | **PLAUSIBLE**, narrow causal chain | Per-example first-token gradients align with refusal activation changes; controlled OLMo-2-1B training varies refusal-prefix support[^reflects] | First-token SFT approximation, one small family, same-set vector attack; DPO/RL not derived | Response diversity is a candidate lever, not a general defense principle |
| A pre-attack activation score predicts benign-LoRA fragility | **PLAUSIBLE**, weak prospective breadth | Skin-Deep studies 21 checkpoints; in a seven-model LoRA set, lowest-GFS Gemma alone retains substantial refusal at the largest update[^skin] | One salient outlier drives the ordering; only benign rank-8 LoRA and refusal endpoint | Require prospective model holdout and distinct attacks before using geometry for selection |
| Post-training safety can be masked rather than deleted | **PLAUSIBLE** | Safe suffixes, neuron interventions and LoRA reactivation restore hidden safety in post-trained models[^hidden] | Restoration does not prove the same natural mechanism remained untouched | Distinguish dormant safety from absent safety; evaluate reversibility both ways |
| Refusal is an inhibitor over retained capability | **PLAUSIBLE**, often true | Abliteration removes refusal with limited broad benchmark loss; unlearning work finds inhibitor-like suppression[^arditi][^hide] | Broad utility benchmarks can miss domain capability loss; some capability may truly be absent | Measure actual harmful task success, not only refusal/compliance |
| Pretraining filtering can prevent acquisition of narrow knowledge | **WE KNOW** for the Deep Ignorance bio proxy setting | Matched 6.9B/550B-token runs, long relearning attacks, capability controls[^deep] | Context/search restores use; one architecture/scale/domain | Capability prevention is qualitatively different from policy robustness |
| Safety exists as an attractor/basin with restoring dynamics | **SPECULATIVE** | Re-triggering and reconstruction are suggestive | No identified state variable, basin boundary or dynamical falsification | Keep only if trajectory perturbations predict recovery better than static probes |
| Safety is redundantly encoded like an error-correcting code | **SPECULATIVE** | Backup features and distributed neurons motivate analogy | No demonstrated code, decoder or minimum-distance law | Delete as explanation unless erasure threshold predicts held-out fault tolerance |
| Parameter-distributed safety is more durable | **SPECULATIVE** | Some distributed/noising/fault-injection defenses transfer | Distribution can still share a low-cost parameter control mode | Must test direct utility-constrained edits, not count components |

## Mechanism-by-stage assessment

### A. Harm recognition

**WE KNOW:** harmfulness-related information is decodable before generation in several aligned models, and a harmfulness direction can be causally manipulated separately from a refusal direction.[^harm]

**PLAUSIBLE:** recognition is comparatively stable under some jailbreaks and malicious fine-tuning, so it can support a latent detector. This has been shown in selected model/attack combinations, not against an attacker who edits the detector itself.

**SPECULATIVE:** a universal, policy-invariant “harm representation” exists. Harmfulness depends on policy, context, user authority and dual-use intent; benchmark labels can masquerade as semantic-topic features.

Minimum discriminating tests:

1. Harmful versus harmless prompts matched on topic, syntax and requested capability.
2. Same request with policy/authority/context changes.
3. Remove refusal while testing whether harm classification and calibrated confidence remain.
4. Patch recognition states without patching response-prefix states.

### B. Policy decision

**WE KNOW:** models can switch between refusal and compliance under small activation interventions, showing a causally controllable decision bottleneck in tested settings.[^arditi]

**PLAUSIBLE:** policy choice is downstream of recognition and upstream of stock refusal wording. Distinct action choices—refuse, safe-complete, redirect, abstain—are rarely separated in mechanism studies.

**SPECULATIVE:** one shared gate controls all safety policies. A shared direction can instead reflect common language style or output-template selection.

Minimum discriminating tests: preserve recognition, intervene on policy choice, then score content-level compliance, safe completion quality, redirect usefulness and over-refusal—not strings alone.

### C. Refusal execution

**WE KNOW:** early response tokens and assistant-header context carry strong leverage; prefilling can bypass refusal, and safety can sometimes be re-triggered at later depth.[^ada]

**PLAUSIBLE:** late layers/heads translate an upstream decision into refusal wording. Recent detection-to-refusal circuit work supports this, but needs independent replication.[^circuit]

**SPECULATIVE:** refusal execution is an attractor that continually corrects unsafe trajectories. DeepRefusal is evidence that such recovery can be trained, not that ordinary models already implement it robustly.

### D. Capability suppression or removal

**WE KNOW:** behavioral silence does not establish knowledge removal. Relearning, activation and quantization attacks can recover outputs from several “unlearned” models.[^relearn][^tamper][^quant]

**PLAUSIBLE:** targeting fact-retrieval mechanisms, smoothness or environment invariance can improve resistance to some relearning families.[^mech-unlearn][^smooth][^irm]

**WE KNOW, narrow scope:** preventing domain knowledge acquisition through filtered pretraining can be more resistant to relearning than post-hoc suppression, while remaining vulnerable to externally supplied information.[^deep]

### E. Localized versus distributed implementation

The evidence is not contradictory once intervention spaces are separated:

- A behavior may have a compact **control direction** while its computation is distributed.
- Multiple activation carriers may converge on one downstream gate.
- Sparse causal components may overlap heavily with general capability.
- Where an activation is causal need not be where a cheap parameter edit exists.
- “Distributed” by neuron count is basis-dependent and does not imply independent failure domains.

Therefore the defense-relevant object is not rank or component count alone; it is the empirical response to diverse, utility-constrained perturbations.

## Conflicts that must remain explicit

| Claim | Supporting evidence | Counterevidence | Current resolution |
|---|---|---|---|
| One refusal direction | Strong single-direction interventions | Concept cones, SAE feature sets, multi-direction attacks | Strong direction exists; completeness is false/unknown |
| Deeper/distributed representation means robustness | RepNoise/DeepRefusal motivation | adaptive reevaluation and cheap simple attacks | distribution is not a security certificate |
| Higher-dimensional refusal geometry means more durability | diverse-prefix training weakens one vector attack | Skin-Deep associates closeness to the canonical refusal direction with the sole benign-LoRA-resistant outlier | attack-specific: vector-ablation and benign-LoRA fragility need not rank models alike |
| Recognition→refusal coupling is durable | HARC strongly reduces four prompt-attack ASRs | HARC collapses under roughly 160 harmful fine-tuning examples | coupling is a prompt-defense mechanism, not open-weight persistence |
| Safety disappears during post-training | observed unsafe behavior | hidden-safety reactivation | behavior may reflect masking/routing, not deletion |
| Unlearning removes capability | low forget-set score | benign relearning, inhibitors, quantization recovery | behavior-only unlearning often suppresses access |
| Refusal robustness implies misuse reduction | lower ASR | capability can be recovered or supplied by context/tools | evaluate downstream task success and external augmentation |

## What a mechanism claim must contain

To graduate from representation correlation to a defense-relevant mechanism, require:

1. semantic/topic-matched contrasts;
2. necessity, sufficiency and rescue across held-out prompts;
3. distinction among recognition, choice, execution and capability;
4. joint/conditional perturbations and post-ablation re-extraction;
5. a prospective prediction about an attack family not used to discover the mechanism;
6. a utility-constrained security endpoint.

Without item 5, geometry remains explanation after the fact. Without item 6, it remains mechanistic interpretability rather than model defense.

## Sources

[^arditi]: Arditi et al., [NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html).
[^cones]: Wollschläger et al., [ICML 2025](https://proceedings.mlr.press/v267/wollschlager25a.html).
[^harm]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^neurons]: Chen et al., [*Safety Neurons*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html), NeurIPS 2025.
[^circuit]: Chu et al., [*From Detection to Refusal*](https://arxiv.org/abs/2609.00051), arXiv 2026.
[^deeprefusal]: Xie et al., [*DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings of EMNLP 2025.
[^ada]: Zhang et al., [*Any-Depth Alignment*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^hidden]: Li et al., [*Finding and Reactivating Post-Trained LLMs' Hidden Safety Mechanisms*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/4568accb98552886fdfceb194deee663-Abstract-Conference.html), NeurIPS 2025.
[^hide]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^relearn]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^tamper]: Che et al., [TMLR 2025](https://openreview.net/forum?id=E6OYbLnQd2).
[^quant]: Zhang et al., [quantization-recovery study](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ba79fb5c4fe70050752f20c90c5f07ca-Abstract-Conference.html), ICLR 2025.
[^mech-unlearn]: Guo et al., [*Mechanistic Unlearning*](https://proceedings.mlr.press/v267/guo25k.html), ICML 2025.
[^smooth]: Fan et al., [smoothness-aware unlearning](https://proceedings.mlr.press/v267/fan25e.html), ICML 2025.
[^irm]: Wang et al., [invariant unlearning](https://proceedings.mlr.press/v267/wang25en.html), ICML 2025.
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^harc]: Chua et al., [*HARC*](https://arxiv.org/abs/2607.00572), arXiv 2026 preprint, v3.
[^skin]: Lee et al., [*Skin-Deep*](https://arxiv.org/abs/2606.22676), arXiv 2026 preprint.
[^reflects]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv 2026 preprint, v2.
[^routing]: Guo et al., [*When Safety Routing Breaks*](https://arxiv.org/abs/2609.01455), Findings of EMNLP 2026 (per arXiv record).
