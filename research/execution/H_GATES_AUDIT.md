# H1–H7 Gate Audit (machine-side completion status)

Legend: `DONE_MACHINE_SIDE` = all agent-executable work complete (may still need executor for real-data execution); `BLOCKED_EXTERNAL` = needs human/executor action; `PARTIAL` = split.

## H0 — Authorized execution path
- Status: `DONE_MACHINE_SIDE` (authorization record + handoff procedure + raw-output policy + benign dry-run receipt; executor boundary explicit).
- Human action: none further; executor executes harmful-task evaluations.

## H1 — Pin substrate and environment
- DONE_MACHINE_SIDE: environment lock (container/py/torch/transformers/cuda/driver/hostname hash, `EnvironmentLock`); compatibility report (torch 2.10.0+cu128 / transformers 5.16.1 / CUDA 12.8 runtime / driver 535.129.03); deterministic inference smoke on benign fixture (Qwen-0.5B, hash stable).
- BLOCKED_EXTERNAL: licensed Gemma access + Fail-Closed provenance (see MODEL_ACCESS_BLOCKERS.md); TamperBench commit pin (GitHub unreachable from IDC); HarmBench/Fail-Closed benign data revision + hashes; HF LFS hashes materialization.
- Remaining before H1 PASS: full model/tokenizer revisions + LFS hashes + model-card/license snapshots + dataset fingerprints materialized; container/driver lock hashes committed.

## H2 — Model and artifact lineage
- DONE_MACHINE_SIDE: `ModelAdapter`-adjacent `ModelArtifact` (immutable id from repo/revision/tokenizer/config hash, parent links), `RunManifest` (jsonschema-validated 4.0.0), content-addressed `ArtifactStore` with alias/dedup, leakage tests (split hash discipline), manifest roundtrip + schema-reject tests.
- BLOCKED_EXTERNAL: edited-artifact reload equivalence on a real checkpoint (needs licensed model); full LFS hashes.
- Remaining for H2 PASS: schema/serialization tests ✅; one reload-equivalent edited artifact (executor).

## H3 — Evaluator boundary
- DONE_MACHINE_SIDE: `UtilityEvaluator` per-domain threshold logic (no weighted average; near-zero rule; per-task bool output), `SafetyEvaluator` seam (harmful scoring = authorized executor only; refusal-diagnostics fixture on benign text), sealed-ID/dedup helpers, evaluator card + leakage tests.
- BLOCKED_EXTERNAL: actual harmful-task scoring, six-task author-comparison utility runs, MMLU-Pro/XSTest/compliance/collapse sentinels on real data, human blind majority audit at boundaries.
- Remaining for H3 PASS: evaluator cards frozen + leakage tests on real IDs (executor).

## H4 — Attack and defense adapters
- DONE_MACHINE_SIDE: `AttackAdapter`/`DefenseAdapter` contracts, no-op round trips, `BoundaryGuard` (split discipline: dev-family data cannot enter sealed_test; illegal splits rejected).
- BLOCKED_EXTERNAL: real A1–A6 adapter implementations/execution (authorized executor); one no-op defense/attack round trip is machine-validated ✅.
- Remaining for H4 PASS: train/select/test boundaries machine-readable ✅; real registry tests under executor.

## H5 — Cost and censoring ledger
- DONE_MACHINE_SIDE: `CostTracker` primary FLOPs axis (schema-compliant key), secondary axes, logical trial-ID ordering (parallel completion ignored), FAILED/OOM charging, right-censoring, no composite scalar; unit tests incl. censoring + parallel-order.
- BLOCKED_EXTERNAL: real run ledger population.
- Remaining for H5 PASS: ledger schema + success/failure/OOM/right-censor unit tests ✅ (machine-validated); real ledger rows (executor).

## H6 — Direct-edit interfaces
- PARTIAL: interface/seam only; mathematical semantics of `(I−rrᵀ)W` (invariant `rᵀ(Wx)=0`, outer-equivalence, save/reload roundtrip) are unit-tested; a real directional weight edit/Heretic-compatible abliteration implementation is NOT included (boundary: authorized executor only).
- BLOCKED_EXTERNAL: reloadable edited checkpoint; fixed search config; equal max allocation base vs defended.
- Remaining for H6 PASS: executor provides/edit runs; agent keeps math-validated seam.

## H7 — Governance templates
- DONE_MACHINE_SIDE: `RunCard` / `ExperimentChangeCard` with required fields + hashes + approval requirement; `refuse_unapproved_novel_defense`; tests ✅.
- BLOCKED_EXTERNAL: none (machine-complete).
- Remaining for H7 PASS: execution refuses unapproved novel-defense configs ✅ + incomplete manifests ✅.

## Summary

- Machine-completable engineering: complete (38/38 tests, compileall OK, receipts/manifests materialized, audit docs written).
- Overall gate: `HARNESS_ENGINEERING_READY_PENDING_EXECUTOR` — H1/H3/H4/H6 real-data steps and R0a–R3 execution require the authorized executor (licensed artifacts, sealed evaluator, human audit). No `HARNESS_VALIDATED` is claimed.
