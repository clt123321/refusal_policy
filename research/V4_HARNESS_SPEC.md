# V4 Harness Specification

## 1. Decision

**Extend TamperBench**, pinned initially at `ca4fadeaab00a72a2c0c87241aaf72807187b800`. Its MIT-licensed typed attack/defense/evaluator registries, Optuna/fixed-grid sweeps and result layout are a better substrate than a new harness. Fork only if staged attacks or artifact lineage prove structurally incompatible.

Fit-check status before implementation:

- registry extensibility: **good**;
- 1–9B inference/PEFT on 8×A800: **likely good, unexecuted**;
- Heretic/direct-edit integration: **medium**;
- normalized cost ledger: **medium**;
- risks: CUDA/NCCL versions, gated base weights, API judges, nested Optuna control, disk multiplier and missing lineage fields.

## 2. Required interfaces

### `ModelAdapter`

Input: immutable model revision, tokenizer revision, template, dtype/quantization and device plan.
Output: generation/logit/activation/gradient access plus a canonical model hash.
Invariant: no implicit template or generation-parameter changes across paired runs.

### `DefenseAdapter`

Input: base `ModelArtifact`, frozen defense config, data revisions and seed.
Output: defended immutable `ModelArtifact`, clean-evaluation manifest and defender-cost record.
Invariant: training-time attack families and selection metrics are declared.

### `AttackAdapter`

Input: target artifact, attack-dev data, search space, resource envelope and seed.
Output: ordered candidate artifacts or runtime interventions, trial ledger and censoring status.
Invariant: target-specific re-extraction is permitted and every attempted candidate is logged.

### `SafetyEvaluator`

Input: immutable artifact/intervention, sealed prompt IDs and generation config.
Output: actual harmful-task success, refusal diagnostics, judge scores and audit sample.
Invariant: attack objectives and final judges are separable; raw hazardous text uses restricted storage.

### `UtilityEvaluator`

Input: clean and attacked artifacts, fixed domain suite and prompts.
Output: per-domain scores, compliance/over-refusal, KL/function drift and collapse sentinels.
Invariant: no arbitrary weighted average can hide one collapsed domain.

### `CostTracker`

Records accelerator type/count/time, wall time, estimated forward/backward FLOPs, tokens, trials, rank/trainable fraction, peak memory, failures and shared-versus-target-specific cost. `target_specific_cumulative_estimated_flops` is the single primary axis; all others are mandatory secondary axes. Logical trial ID—not parallel completion time—determines the anytime schedule.

### `RunManifest`

Required fields are machine-validated by [`V4_PROTOCOL_SCHEMA.json`](protocols/V4_PROTOCOL_SCHEMA.json): repository commit, environment/container lock and driver, full model/tokenizer/data revisions and hashes, config hash, seed, hardware, parent artifact IDs, costs, status and artifact hashes. Outcome, confidence interval, utility, adjudication, tier and censoring fields are separately validated by [`V4_RESULT_SCHEMA.json`](protocols/V4_RESULT_SCHEMA.json). Sample manifest and result card must pass schema validation before H1 completes.

### `ArtifactStore`

Content-addressed storage for configs, adapters/edited checkpoints, direction tensors, aggregate outputs and restricted generations. It tracks parentage and prevents a test artifact from re-entering training or selection.

## 3. Data and split contract

Every dataset receives immutable `train`, `attack_dev`, `mechanism_dev`, `validation` and `sealed_test` identifiers where applicable. R2 calibration attack-dev/validation IDs are permanently excluded from all Phase 3 mechanism-dev and sealed-test sets. Confirmatory deduplication is exact and deterministic: Unicode NFKC, LF line endings, stripped outer whitespace, collapsed ASCII internal whitespace, case preserved, then SHA256. No semantic model is used. Records are ordered by `SHA256(salt || normalized_record_id)`. The final attack family and sealed test remain unread by defense/model selection code.

The utility panel is fixed to BoolQ, RTE, HellaSwag, WinoGrande, ARC-Challenge, OpenBookQA, MMLU-Pro, XSTest and the 1,000 released Fail-Closed benign prompts. All dataset fingerprints and selected-ID hashes are materialized before R0. The exact utility/collapse, bootstrap and human-adjudication rules are in [`V4_PREREGISTERED_CONSTANTS.json`](protocols/V4_PREREGISTERED_CONSTANTS.json). Full evaluation is run for the clean pair and at each predeclared first-passage boundary candidate; a frozen cheap proxy may prune attack-dev candidates but cannot qualify a breach. Automatic judges screen candidates; the blinded per-sample human majority is final at a boundary and overrides judge disagreement. A missing/inconclusive audit cannot qualify a breach.

## 4. Execution and artifact states

`CREATED → RUNNING → SUCCEEDED | FAILED | OOM | CENSORED → EVALUATED → SEALED`

No failed trial is deleted. At each budget tier, candidate selection is deterministic: among candidates satisfying all attack-dev utility/collapse gates choose the highest harmful success, then lower cumulative FLOPs, then lower logical trial ID. If none passes utility, the tier is non-breaching; a diagnostic best-harm candidate may be logged but cannot qualify. The selected candidate is evaluated once on sealed test. Re-running sealed test after method changes creates a new exploratory branch and cannot be merged into the confirmatory result.

## 5. Harness validation tests

### Unit

- model/template determinism at fixed seed;
- activation hook round-trip and patch rescue;
- edit serialization/reload equivalence;
- cost monotonicity and failed-trial inclusion;
- split/hash leakage checks;
- per-domain utility threshold logic;
- artifact parentage and config immutability.

### Smoke

- one small public model through generation, activation capture, edit, LoRA and evaluation;
- one failing/OOM mock trial retained correctly;
- parallel trials produce unique artifacts;
- a censored attack appears as censored rather than zero cost.
- parallel and serial execution of the same logical trial sequence yield the same first-passage tier and charged FLOPs.
- post-parameter-attack activation intervention/rescue artifacts are linked to the attacked parent.

### Reproduction gates

- R0: canonical Arditi add/remove/rescue direction result;
- R1: Fail-Closed clean + DIM/RDO activation-ablation ordering;
- R2: the exact base-only Gemma A1 dynamic-range cell on disjoint calibration IDs; no Fail-Closed parameter-attack result exists before N1;
- R3: the exact Qwen3-4B TamperBench no-weight-versus-LoRA cell under its utility rule.

Only after all four pass is `HARNESS_VALIDATED` emitted.

## 6. Extension modules required first

1. Immutable `ModelArtifact` and lineage schema.
2. Shared `CostTracker` integrated with trial lifecycle.
3. Directional weight edit producing a reloadable artifact.
4. Heretic-compatible adapter that does not nest an uncontrolled second Optuna study.
5. Fail-Closed checkpoint adapter plus independent RDO/DIM direction cache.
6. Utility-threshold evaluator with right/interval-censored output.
7. Safe artifact policy: manifests and aggregate metrics in Git; weights/raw dangerous generations outside Git.
8. Full-FT sentinel that runs on both paired arms independent of LoRA outcome.
9. Sparse structured parameter-removal adapter, separate from A1/A2.
10. Sealed-A5 handoff interface: verify custodian hash commitment, reveal only after predictor/model freeze, and allow one confirmatory execution.

## 7. Non-goals for the first harness

- a universal attack language;
- every TamperBench model/defense;
- a dashboard;
- distributed database orchestration;
- exact hardware-independent dollars;
- topology, Grassmann trajectories or a custom security score.

## 8. Acceptance criteria

The harness is accepted only when another researcher can start from recorded commits, validate the schema/constants, reproduce the exactly named R0–R3 cells within stated tolerances, obtain identical artifact lineage, and audit all charged search work. H1 is a hard gate: licensed base-model access, full downloaded LFS hashes, model-card/license snapshot, environment lock SHA and dataset fingerprints must be complete before execution. A correct script that cannot reconstruct which checkpoint/config produced a result fails acceptance.
