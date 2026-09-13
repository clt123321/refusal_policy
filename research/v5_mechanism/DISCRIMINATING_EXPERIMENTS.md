# Round 5 — Discriminating Experiments

## Strategy

Use a gated common experiment rather than one bespoke matrix per hypothesis. No defense is trained in the first pass. Mechanism measurements are frozen before attack results, and every attack uses the V4 utility-qualified endpoint and work ledger.

An “independent attack” must differ in operator bias, objective, data and localizer; its implementation owner must not tune it from predictor or defense outcomes. A1/A2 count once, and LoRA/full FT count as one gradient-update family. A4 counts separately only with an independently frozen sparse localizer/objective. A5 is held by the V4 red-team custodian and revealed once after every predictor ranking, model artifact and analysis hash is committed.

## Natural-experiment assets

### Cheap screen

- `google/gemma-2-2b-it` versus released Fail-Closed Gemma-2-2B.
- Purpose: validate the measurement stack and look for a large inversion.
- Limitation: whole-recipe confounding and only two checkpoints; it cannot establish a population relationship.

### Minimum useful panel

Subject to an artifact/license/revision gate, use checkpoints derived from the same Llama-3-8B-Instruct upstream family:

1. vanilla aligned model;
2. [Fail-Closed checkpoint collection](https://huggingface.co/collections/ztcoalson/fail-closed-alignment);
3. [DeepRefusal checkpoint](https://huggingface.co/skysys00/Meta-Llama-3-8B-Instruct-DeepRefusal);
4. [TAR refusal checkpoint collection](https://huggingface.co/collections/lapisrocks/tamper-resistant-safeguards-for-open-weight-llms).

They are three pairwise natural contrasts, not randomized treatments. Before use, verify exact common base revision, tokenizer/template, license, objective domain, model hashes and author-reported behavior. A community “broken” DeepRefusal model is only an untrusted attack artifact to reproduce, never ground-truth evidence. AntiDote and diverse-refusal training are deferred because a sufficiently pinned official defended checkpoint has not yet been established in this project.

## E0 — Artifact and dynamic-range gate

- **Baseline:** exact vanilla upstream checkpoint.
- **One changed factor:** load one released defense delta/checkpoint at a time; no additional training.
- **Measurement:** hashes, clean harmful-task success, hazard-capability accessibility, per-domain utility, over-refusal, template sensitivity and author-result replication.
- **Independent outcome:** none; this is an admissibility gate.
- **Predictions:** no world model is credited for passing provenance.
- **Compute:** Gemma 4–8 A800-GPUh; Llama panel 12–24 A800-GPUh.
- **Confounders:** incompatible bases, defense target mismatch, hidden selection, quantization/dtype, judge drift.
- **Kill:** reject any pair whose lineage or clean behavior cannot be reconciled; stop the panel if every model is floor/ceiling saturated.

## E1 — Blind natural-checkpoint screen: the cheapest killer experiment

- **Baseline:** vanilla checkpoint in each valid pair.
- **One changed factor:** the complete released defense checkpoint; analyze each pair, never treat “defense type” as randomized.
- **Measurement before attack reveal:** OAFT, clean margin, full GFS, blockwise Fisher, utility-conditioned safety response spectrum, policy-margin tail density and hazard-capability access. Freeze code and rankings. The response spectrum uses different hazard domains, stage outputs and utility examples from the confirming attack objective—not merely different prompt IDs.
- **Independent outcome:** first-passage utility-qualified breach cost under A1 directional edit, A3 LoRA plus adaptive full-FT, and independently implemented/localized A4 sparse edit. A1 is developmental; A3/A4 and the custodian-sealed A5 are off-diagonal tests.
- **Compute:** Gemma screen 24–48 A800-GPUh; four-checkpoint Llama panel 120–220 A800-GPUh.
- **Confounders:** training dose/data, clean safety, checkpoint selection, incomplete utility, attack competence, censored cost, only four correlated natural units sharing a base.
- **Kill:** author ordering fails; all arms instantly breach or remain censored; the response spectrum cannot predict attack-dev initial slope beyond gradient norm; or any claimed ordering disappears under human audit/capability controls.

| World prediction in E1 | Expected result |
|---|---|
| W1 redundancy | OAFT is the best cross-attack ranker |
| W2 common cause | finite joint-cost discount beats OAFT; fault-trained checkpoints can invert |
| W3 safety-only editability | utility-conditioned response ranks A1/A3/A4 and predicts utility-cap relaxation |
| W4 regeneration source | recovery/bootloader evidence, not static OAFT, explains defended models |
| W5 stage/channel | no global ranking; attack- or domain-specific reversals dominate |

E1 may validate dynamic range, reveal a large counterexample or reject an asserted universal ordering. Four correlated checkpoints cannot estimate a reliable predictor relationship or choose among many metrics; attack seeds and prompts are repeated measurements, not independent models.

## E1.5 — Matched confirmation panel, only after E1 survives

- **Baseline:** two frozen 1–3B upstream backbones.
- **One changed factor:** four non-novel, fixed-dose safety-training conditions from a shared source: ordinary safety SFT, single-direction fault training, Fail-Closed-style multi-feature fault training and diverse-refusal-prefix SFT.
- **Units:** four independent training seeds per backbone/condition = 32 final checkpoints. Attack seeds are nested repeated measures.
- **Measurement:** freeze exactly one primary local-inseparability predictor plus GFS, Fisher, gradient norm, clean margin and OAFT; no metric selection on E1.5 attacks.
- **Independent outcome:** A3, independently implemented A4 and one custodian-sealed A5, with whole-checkpoint holdout and leave-one-backbone/condition-out tests.
- **Compute:** large conditional stage; requires a separate power/censoring gate and GPU approval. It is not authorized by Round 5.
- **Confounders:** realized behavior differences, optimizer dose, capability access, seed leverage, censoring.
- **Kill:** <80% design power at the target effect; predictor loses to prespecified baselines; one checkpoint drives the effect; or sign fails across backbone/condition holdouts.

| World prediction in E1.5 | Expected result |
|---|---|
| W1 redundancy | training-condition changes in OAFT mediate held-out cost |
| W2 common cause | finite fault overlap mediates cost after OAFT is controlled |
| W3 functional inseparability | the frozen local predictor mediates A3/A4/A5 cost across seeds/backbones |
| W4 regeneration source | recovery-source structure, not the local spectrum, explains fault-trained arms |
| W5 stage/channel | effects interact strongly with attack stage/domain and defeat one global predictor |

## E2 — Pulse versus sustained fault

- **Baseline:** a single-token, single-layer activation pulse at a preregistered functional dose.
- **One changed factor:** duration—pulse, fixed multi-token window, or sustained through generation; amplitude is held fixed and functional displacement reported.
- **Measurement:** token-by-layer recognition, policy margin, harmful-token probability and causal recovery after intervention removal.
- **Independent outcome:** E1 parameter-attack cost, not used to select pulse positions.
- **Compute:** 8–20 A800-GPUh per admitted checkpoint.
- **Confounders:** LayerNorm rescaling, direct logit effect, output length, prompt history, post-hoc layer/token choice.
- **Kill:** pulse has no immediate behavioral effect, or apparent recovery is refusal-string reappearance without content-level safety.

| World | Prediction |
|---|---|
| W1 | More paths increase sustained-fault tolerance |
| W2 | Local pulses recover but one common-cause lesion removes all recovery |
| W3 | Recovery is weakly related unless it also preserves utility coupling |
| W4 | Strong impulse recovery; pulse–step gap identifies source structure |
| W5 | Recovery depends sharply on recognition/policy/execution timing |

## E3 — Independent versus common finite fault

- **Baseline:** separately validated safety effects receive matched local lesions one at a time.
- **One changed factor:** optimize a carrier-blind shared-support edit with the same parameter count, functional dose and search budget.
- **Measurement:** individual and joint content-level effects, rescue, finite joint-cost discount, module transfer and whether recovery signatures disappear together.
- **Independent outcome:** sealed A3 or A4 family not used to construct the joint edit.
- **Compute:** 30–60 A800-GPUh per selected checkpoint; run only where E1/E2 establish more than one causal effect.
- **Confounders:** reusing the carrier projector, unequal parameter support/norm, non-causal writers, shared output head, search-quality asymmetry.
- **Kill:** effects are not individually causal; functional dose cannot be matched; or the joint discount fails to predict the sealed attack.

| World | Prediction |
|---|---|
| W1 | Cost grows with causal effect count |
| W2 | Shared edit is disproportionately cheap and jointly suppresses effects |
| W3 | Shared edit succeeds only when its utility price is low |
| W4 | Cheap edit targets the bootloader and stops recovery |
| W5 | Discount is stage/domain-specific, not global |

## E4 — Utility-cap sweep and composed repair attack

- **Baseline:** E1 attack candidates spanning harmless-to-breached states.
- **One changed factor:** utility allowance `0%, 1%, 2%, 5%, 10%`; separately run a charged sequence `direct or sparse removal → benign-only distillation/KL repair → adaptive conditional LoRA/full-FT cleanup`, with no refusal/safety examples in repair.
- **Measurement:** safety–utility frontier, whether utility repair restores safety, mode persistence and legitimate-adaptation performance.
- **Independent outcome:** sealed second utility suite, long-form/instruction-following and capability-access tests, plus sealed harmful prompts absent from predictor/repair data. All stages and failed trials count toward attacker FLOPs.
- **Compute:** 12–30 A800-GPUh per breached checkpoint.
- **Confounders:** benign data containing implicit safety cues, incomplete utility coverage, capability forgetting, repair-dose choice.
- **Kill:** utility cannot be restored, repair contains safety supervision, ranking is determined by missing dangerous capability, or the composed best response bypasses the local predictor at baseline cost.

| World | Prediction |
|---|---|
| W1 | No necessary cap/repair law |
| W2 | Utility repair can leave the common-cause breach intact |
| W3 | Relaxing the cap causes ordered frontier collapse; restoring utility also restores safety |
| W4 | Repair restores safety only if the regeneration source survives |
| W5 | Repair fixes the attacked stage while other stage signals remain unchanged |

## E5 — Stage and domain transfer audit

- **Baseline:** clean and successfully breached checkpoint with sham/wrong-stage patches.
- **One changed factor:** patch recognition, policy or execution states; separately optimize identical attack recipes on four preregistered hazard domains and compare with one joint-domain objective.
- **Measurement:** causal stage-transfer matrix and 4×4 attack-domain transfer matrix; report coverage threshold sensitivity rather than one arbitrary scalar.
- **Independent outcome:** repeat with a second parameter-attack bias.
- **Compute:** 24–50 A800-GPUh per inversion checkpoint.
- **Confounders:** semantic domain mismatch, direct logit leakage, stage-probe contamination, arbitrary coverage threshold.
- **Kill:** patching lacks rescue, domain partitions are unstable, the transfer pattern fails under the second attack, or the joint-domain objective defeats apparent isolation for the price of one single-domain attack.

| World | Prediction |
|---|---|
| W1 | Stage/domain matrices add little beyond path count |
| W2 | One common edit transfers broadly across stages/domains |
| W3 | Broad transfer follows the same low-utility-cost parameter mode |
| W4 | One upstream patch restarts several later states and tokens |
| W5 | Cheapest stage and domain coverage explain operator-specific rankings |

## Causal manipulation only after natural support

If E1 supports W3, train one 1–3B model from a common aligned base under equal data, tokens, FLOPs and final checkpoint dose:

- **high-inseparability arm:** constrain safety updates to utility-essential functional/Fisher modes;
- **low-inseparability arm:** constrain them toward a utility-null tangent;
- **control:** ordinary safety continuation with the same optimizer and dose.

Freeze the projected-update construction before attacks. Match clean margin, capability access, overall Fisher/update spectrum, training dose and a benign legitimate-adaptation task. The causal claim requires the manipulation to move the pre-attack spectrum in the intended direction, preserve clean behavior and general plasticity, mediate the effect, and order two unseen parameter-attack frontiers plus the composed attack. If it only makes all learning difficult, it is not a useful defense.

If W2, W4 or W5 wins instead, a different manipulation card is required; do not retrofit the W3 experiment after seeing outcomes.

## Minimal harness additions

Only add measurements shared by the discriminating experiments:

1. batched JVP/VJP on disjoint safety and utility outputs;
2. randomized generalized eigensolver with parameter-block restrictions;
3. token/layer activation traces plus pulse/window/sustained interventions;
4. recognition/policy/execution patch hooks;
5. per-block gradient/Fisher summaries and mode-persistence logging;
6. hazard-domain and capability-access labels in the evaluator;
7. attack-transfer, composed-attack and repair-trajectory result tables;
8. second sealed utility/capability panel and legitimate-adaptation evaluator.

Do not add full Hessians, exhaustive activation dumps, Grassmann trajectories, circuit graph discovery or a new dashboard in Round 5.
