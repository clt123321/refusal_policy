# V6 Engineering Handoff

> **ARCHIVED TRANSPORT SNAPSHOT.** Kept in place because `TODO.md` links to it and it records historical provenance. GitHub work branches are now the collaboration path; this file is not an execution-status source.

## Authoritative GitHub base SHA

```text
4496694d9913cb27331ef8a26b0a31c55b3ca7cd
```
(Verified as `origin/main` at fetch time 2026-09-14; no newer upstream commits observed.)

## Clean relay branch

```text
refusal-policy-v6-engineering-handoff-20260914
```
Created by branching directly from `origin/main`; does not contain the historical KML relay transport branch, its merge commits, or duplicate reconciliation patches.

## Relay HEAD SHA

```text
849b1ddc40c18f2fdeb0a5017c64d217c9364795
```
Remote verification: `git ls-remote corp-relay refs/heads/refusal-policy-v6-engineering-handoff-20260914` == local HEAD. Corp `master` untouched.

## Ordered commit list (base..HEAD)

```text
8586459 chore: record v5 execution gate status
3bc1d4b feat: add V4 harness interfaces with schema-validated manifests
84897cf chore: record harness dry-run receipt
1279f18 test: validate intervention math and paired bootstrap
8b0ca48 feat: add R0 direction primitives and frozen schedules
849b1dd chore: update overnight work-agent status
```

## Files added/modified (29 files, +2131)

- `src/harness/` (env, model_artifact, manifest, artifact_store, cost_tracker, evaluators, adapters, governance, statistics, direction)
- `tests/` (test_harness, test_v4_intervention_math, test_statistics, test_direction_helpers)
- `scripts/` (harness_dry_run, gen_attack_schedules)
- `configs/execution/` (r2_a1_schedule, a3_lora_schedule)
- `research/execution/` (H0_AUTHORIZATION, H0_DRY_RUN_RECEIPT, H_GATES_AUDIT, R0A_REPRODUCTION_MANIFEST, R0B_R3_STAGING, MODEL_ACCESS_BLOCKERS, COMPUTE_READINESS, WORK_AGENT_STATUS)
- `artifacts/harness/dry_run/` (DRY_RUN_RECEIPT.json, DRY_RUN_SUMMARY.json)
- `.gitignore` (+ `.codeflicker/` local tool config exclusion)

Not included: earlier WIP `TODO.md` state edits (R0a–R3 BLOCKED flags) were intentionally omitted; the authoritative `TODO.md` and all `research/` documents outside `execution/` remain identical to base.

## Engineering content summary

- V4 harness interfaces: EnvironmentLock, ModelArtifact, RunManifest (jsonschema 4.0.0), content-addressed ArtifactStore, CostTracker (primary-FLOPs axis, logical trial order, failed/OOM charging, right-censoring, no composite scalar), UtilityEvaluator (per-domain thresholds), SafetyEvaluator seam (harmful scoring = authorized executor), Attack/Defense adapter contracts + BoundaryGuard, RunCard/ExperimentChangeCard governance.
- Intervention/selection mathematics validated by unit tests: remove/add operator exactness, `(I−rr^T)W` invariant with outer-equivalence, save/reload roundtrip, hook-ordering lesson, token-position convention, mean-difference-in-means + pooled-variance selection score, deterministic bootstrap.
- Frozen deterministic schedules generated from constants: R2 A1 35 candidates / 5 tiers; A3 LoRA 24 candidates; full-FT sentinel grid.
- Benign formal dry-run receipt (content-addressed, schema-validated, deterministic).

## Exact test command and result

```bash
python -m pytest -q tests
# 48 passed, 3 warnings
python -m compileall -q src tests scripts   # OK
```
Additional roundtrip checks on this branch: import, manifest schema build+validate, artifact-store dedup, cost-ledger failed/censor accounting, governance refusal, direction normalization and orthogonalize invariant — all PASS. Versions: Python 3.13, torch 2.10.0+cu128, transformers 5.16.1, jsonschema 4.25.0.

## Known external blockers

- Licensed `google/gemma-2-2b-it` (HF manual-gated) — executor must accept terms and provide access path.
- TamperBench `ca4fadea…` and Fail-Closed `892e99b2…` pinned commits (GitHub unreachable from KML IDC) — executor to fetch and pin.
- HarmBench/Fail-Closed benign data revisions and 200/200 ID sets not pinned locally.
- Harmful-task evaluation, raw harmful generation, real attack execution (A1–A6), directional weight-edit/abliteration implementation — authorized executor only (H0 boundary).

## Statement

```text
NO_SCIENTIFIC_EXPERIMENTS_RUN
SAFE_FOR_MAC_RECONCILIATION = YES
```
