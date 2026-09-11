# Round 1.5 Literature Patch

This patch adds only four close 2026 works, updates evidence provenance, and checks whether TamperBench is a suitable substrate. It does not select a defense program.

## 1. HARC

**Status:** arXiv preprint, v3, July 2026.

**Central claim:** Jailbreaks suppress harm recognition, refusal, or both at the prompt boundary, while harm recognition can reappear during unsafe generation; coupling harmfulness and refusal directions at prompt and response positions improves prompt-jailbreak robustness.

**Strongest evidence:** Across five model families the paper reports a similar four-direction structure. Its LoRA defense is evaluated on Llama-3.1-8B and Qwen-2.5-7B against PAP, PAIR, CodeAttack, and DeepInception, with five capability benchmarks and two over-refusal benchmarks. Mean ASR is reported as 4.67× and 4.75× lower than the respective base models.[^harc]

**Threat/defense relevance:** It is strong evidence for recognition/action and prompt/response-position separation. It is primarily a black-box prompt defense, not an open-weight tamper defense.

**Closest collision:** Directly collides with “couple recognition to action” and much of temporal safety reconstruction. It also shows why subspace-localized intervention can retain utility.

**What remains open:** The paper's own appendix reports that harmful fine-tuning returns HARC to baseline behavior with roughly 160 harmful examples. No HARC-aware weight edit, Heretic, full attack sweep, or independent validation is reported. CodeAttack remains the hardest prompt attack.

## 2. Skin-Deep

**Status:** arXiv preprint, June 2026.

**Central claim:** A pre-attack Geometric Fragility Score (GFS), computed from layerwise low-rank safety geometry, can flag refusal that will be fragile under small benign LoRA fine-tuning.

**Strongest evidence:** The diagnostic covers 21 instruction-tuned models from 3B–32B and six alignment-recipe labels. Direction ablations causally reduce refusal in four non-floor/non-ceiling models. In a seven-model benign-LoRA set, Gemma-2-9B has the lowest GFS and is the only model to retain substantial refusal at the largest update.[^skin]

**Threat/defense relevance:** A potentially cheap model-selection diagnostic could reduce defense-search cost. It is not itself a defense and predicts one bounded endpoint: refusal after small rank-8 benign LoRA.

**Closest collision:** Collides with any plan to claim that a new refusal-geometry score predicts fine-tuning durability. It also complicates “higher rank is safer”: the reported robust outlier is closer to the canonical Arditi direction.

**What remains open:** Prospective prediction on an independently selected model population; quantitative rather than outlier-driven forecasting; malicious FT, direct edits and actual dangerous-task endpoints; 70B+, MoE and multilingual validity.

## 3. Refusal Geometry Reflects Refusal Training

**Status:** arXiv preprint, v2, September 2026.

**Central claim:** In an OLMo-2-1B case study, first-refusal-token training gradients can explain the learned refusal direction/subspace; diverse refusal starts raise stable rank and weaken a single-vector ablation attack.

**Strongest evidence:** The paper traces target-token support through per-example gradients to realized activation updates, and then performs controlled synthetic fine-tuning. At behavior-matched checkpoints, broader refusal-start support increases residual stable rank and reduces the refusal drop caused by difference-in-means ablation.[^reflects]

**Threat/defense relevance:** Provides a concrete data→gradient→activation→attackability chain and a very cheap training-data lever.

**Closest collision:** Strong collision with objective/response-diversity experiments, stable-rank defenses, and claims that diverse refusal completions are a new hardening mechanism.

**What remains open:** The derivation covers first-token SFT, not DPO/RL. The experiment uses one small model family, non-harmful synthetic chemistry prompts and a target-set-adapted single-vector attack. Multi-direction, SAE, automated edit, Heretic, LoRA/full FT and actual utility-constrained breach cost remain untested.

## 4. When Safety Routing Breaks

**Status:** Findings of EMNLP 2026 according to the arXiv record.

**Central claim:** Benign fine-tuning fragility is better explained by disruption of a low-rank late output-routing pathway than by gradient conflict alone; upstream safety information remains but no longer controls output.

**Strongest evidence:** On Llama-3.1-8B and Qwen-2.5-7B, 100 benign examples raise ASR as high as 85.7%. Blockwise Fisher spectra, logit-lens evidence and final-layer activation patching converge on late MLP routing; gradient-low-conflict data still causes substantial collapse. LoRA and ASAM reduce early collapse but not the 5,000-example regime.[^routing]

**Threat/defense relevance:** Identifies a plausible benign-FT failure locus and rules out gradient conflict as a sufficient explanation. It motivates, but does not validate, routing protection or functional/Fisher flatness as defense principles.

**Closest collision:** Collides with shared-gate/common-mode and safety-flatness stories. A paper that merely finds a low-rank output route or applies ASAM would now be incremental.

**What remains open:** Only two 7–8B families, SFT/DPO alignment, English/refusal endpoints and two training seeds. Local Fisher geometry has not been shown to predict malicious FT, direct edits, activation attacks or adaptive breach cost.

## 5. Net change to the idea landscape

| Candidate idea | After patch | Reason |
|---|---|---|
| Safety reconstruction across token depth | **HIGH COLLISION** | DeepRefusal, Any-Depth, DeRTa and HARC cover most of the basic idea |
| Recognition→refusal coupling | **HIGH COLLISION** | HARC implements it directly and exposes its malicious-FT limit |
| Refusal-prefix diversity raises rank | **HIGH COLLISION** | Refusal Geometry Reflects Refusal Training is the direct result |
| Geometry predicts benign-FT fragility | **HIGH COLLISION** | Skin-Deep supplies a dedicated diagnostic |
| Protect a late safety route / flatten Fisher | **PARTIAL–HIGH COLLISION** | When Safety Routing Breaks localizes and partially mitigates it |
| Parameter-level independent fault domains | **PARTIAL COLLISION** | Nearby evidence exists, but no reviewed work trains and adaptively tests independent parameter failure domains |
| Held-out cross-operator robustness | **PARTIAL COLLISION** | TAR/AntiDote/ART are close; strict operator-basis transfer remains open |
| Repair-closed safety–utility coupling | **PARTIAL COLLISION** | SDD/SEAM create initial coupling; closure under adaptive utility repair remains untested |

## 6. Independent-evidence provenance patch

`DEFENSE_EVIDENCE_TABLE.csv` now has an `independent_evidence_provenance` field and 27 records. The field distinguishes:

- author-only evidence;
- an independent attack or durability audit;
- implementation within a later benchmark;
- absence of identified independent validation.

“Implemented by TamperBench” is not treated as a conceptual replication. “No independent validation identified” is an evidence-status statement, not evidence that the method fails.

## 7. TamperBench Fit Check

**Repository/license:** The public repository is MIT licensed. This permits modification and redistribution with the license notice retained. The review pins commit `ca4fadeaab00a72a2c0c87241aaf72807187b800` (2026-04-20).[^tb-code]

**Attack/defense registry extensibility:** **Good.** Attacks and defenses use typed config/classes plus decorator registries; evaluators are separately registered. Existing scripts already run Optuna and fixed-grid sweeps. Adding an ordinary checkpoint-to-checkpoint attack is straightforward.

**8×A800 feasibility:** **Likely good, not yet executed.** The Linux stack uses CUDA 12.8-era PyTorch, Transformers, Accelerate, PEFT, bitsandbytes and vLLM. Small-model sweeps can be distributed by trial; 7–8B PEFT and inference fit comfortably on A800-80GB. Full-parameter TAR already uses Accelerate/FSDP-style multi-GPU machinery. Remaining risks are cluster CUDA/NCCL compatibility, model licenses/download access, API judges, and the large storage/search multiplier. This is a code/config assessment, not a completed run.

**Heretic/direct-edit integration:** **Medium difficulty.** TamperBench already has refusal ablation and a generic `TamperAttack` lifecycle, so checkpoint-producing direct edits fit the abstraction. Heretic adds an inner Optuna search, model-specific direction/layer/component kernels, and benign-KL scoring. The main work is nested-search budget accounting, avoiding duplicate Optuna control, and converting in-memory edits to lineage-tracked artifacts.

**Cost-ledger integration:** **Medium difficulty.** Configs, results directories and study databases already retain much run state, but the base API does not expose a normalized cost schema. A shared callback/context should record GPU model/count, wall time, tokens, forward/backward passes, peak memory, search trials, failures and inference overhead. FLOP estimation and staged-attack attribution require new common fields rather than defense-specific logging.

**Decision:** **EXTEND TamperBench.** Do not build a new harness unless staged attacks, restricted evaluations, or lineage requirements prove structurally incompatible.

## Sources

[^harc]: Chua et al., [*HARC: Coupling Harmfulness and Refusal Directions for Robust Safety Alignment*](https://arxiv.org/abs/2607.00572), arXiv 2026, v3.
[^skin]: Lee et al., [*Skin-Deep: A Geometric Diagnostic for Alignment Fragility in Large Language Model Representations*](https://arxiv.org/abs/2606.22676), arXiv 2026.
[^reflects]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv 2026, v2.
[^routing]: Guo et al., [*When Safety Routing Breaks: Understanding Alignment Fragility under Benign Fine-Tuning*](https://arxiv.org/abs/2609.01455), Findings of EMNLP 2026 (per arXiv record).
[^tb-code]: CriticalML, [TamperBench repository](https://github.com/criticalml-uw/TamperBench), MIT License; inspected at commit `ca4fade`.

ROUND1_5_COMPLETE
