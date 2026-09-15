# V6 E1 Repair Pilot Decision Package

## Status

`READY_FOR_PI_DECISION_NOT_EXECUTABLE`

The independent 4090 DEV repair smoke is complete. A real repair pilot is not started because the repository contains no authorized, source-pinned safety repair corpus and the existing protocol explicitly marks `D_repair` as `PENDING_EXECUTOR_PILOT` / `BLOCKED_SOURCE_FREEZE`.

## Completed independently

- Execution branch: `work/4090-e1-67c90f0`
- Code state commit: `3f788de1354b59a1d1e633af4e97c0e0693191b9`
- Local state commit exists; GitHub push was attempted but the current non-interactive session lacks GitHub HTTPS credentials.
- Model is cached and manifested at `artifacts/.model_cache/qwen25-1.5b-instruct-989aa798`.
- Existing DEV smoke remains separate from this pilot and from formal C/P.

## Data decision

### Recommended source

Use one authorized, source-controlled safety-supervision corpus whose records explicitly contain refusal/safety targets, a pinned revision, stable source IDs, and semantic-family metadata. The PI/data owner must provide the source URL or local authorized path and revision. Materialization must preserve source provenance without placing restricted raw content in Git or ordinary logs.

### Rejected shortcuts

- Do not promote `tests/fixtures/v6_repair_dev.jsonl`; it is a two-row benign engineering fixture.
- Do not use HarmBench evaluation IDs as repair supervision; current records identify them as evaluation assets, not a repair corpus.
- Do not use arbitrary benign instruction data as safety repair data.
- Do not fabricate file or ID hashes before materialization.

### Required construction

1. Read only the approved source revision.
2. Convert each approved record to stable `id`, `prompt`, `target` fields.
3. Require non-empty prompt and target strings.
4. Preserve source ID and semantic-family labels in a restricted manifest.
5. Exact-deduplicate records and reject duplicate IDs.
6. Audit near-duplicate and family overlap against all future split manifests.
7. Validate target token count is positive and record prompt/target/full length percentiles.
8. Choose and record a max-length policy before training; recommended pilot policy is reject-and-report overlength records rather than silent truncation.
9. Compute real `file_sha256` and `ids_sha256` after construction.

No pilot data has been materialized in this round; no claim of formal split isolation is made.

## Recommended bounded candidate

The executable candidate is recorded in `configs/execution/v6_repair_pilot_candidate.json` and is intentionally not a formal recipe:

- LoRA on `q_proj`, `v_proj`, rank 8, alpha 16, dropout 0.
- AdamW, learning rate `2e-5`, zero weight decay, betas `(0.9, 0.999)`, fresh optimizer state.
- Stable source-ID order, no shuffle, batch size 2, accumulation 4.
- Candidate steps `512`, checkpoints `0/64/128/256/512`.
- Seed 17 for the bounded pilot.
- One common C/P rule: select one stage using endpoint-match preflight only; do not inspect A1 outcomes or tune C/P independently.
- PEFT adapter export; no raw harmful output in ordinary artifacts.

These values are recommendations, not scientific freeze. They deliberately do not inherit the DEV smoke's rank 2, learning rate `1e-4`, two steps, or two samples.

## Expected cost

The previous smoke consumed 79 full-sequence input tokens in 22.796 seconds, but that is not a reliable estimate for a larger corpus. The candidate must first be tokenized on CPU to obtain row count and length percentiles; then run one small throughput preflight on the approved data. GPU cap is one serialized job and two hours maximum for this pilot window. Final C/P and E1 caps remain pending P5.

## Exact launch command after PI/data approval

```bash
export V6_MODEL_PATH="$PWD/artifacts/.model_cache/qwen25-1.5b-instruct-989aa798"
CUDA_VISIBLE_DEVICES=0 .venv-v6/bin/python -m src.execution.repair_runner \
  --config configs/execution/v6_repair_pilot_candidate.json \
  --parent-model "$V6_MODEL_PATH" \
  --output artifacts/v6_e1/DEV/repair_pilot/C/s17/a01 \
  --device cuda --repo . \
  --execution-sha 3f788de1354b59a1d1e633af4e97c0e0693191b9 \
  --task-id V6.E1.DEV.REPAIR_PILOT \
  --run-id V6.E1.DEV.REPAIR_PILOT.C.s17 \
  --attempt-id V6.E1.DEV.REPAIR_PILOT.C.s17.a01
```

Before launch, replace the candidate config's data path and hashes with the materialized approved pilot data and freeze the config in a new commit. The same config/hash and stage-selection rule must be used for P; no arm-specific tuning.

## Specific PI decisions required once

1. Approved D_repair source, revision, and access path.
2. Target construction rule and allowed refusal target families.
3. Candidate envelope approval or replacement: LoRA fields, optimizer, effective batch, 512-step cap and checkpoint grid.
4. Pilot pass/selection rule for choosing one common C/P repair stage from endpoint-match preflight.
5. Maximum source record count and overlength policy.

## Capability blockers kept separate

- A0: missing implementation and authorized executor; blocks P endpoint construction only.
- A1: missing implementation and authorized executor; blocks fresh re-attack only.
- Content evaluator: interface seam exists, but authorized implementation/handler and restricted raw-output path are missing; blocks endpoint qualification and all scientific verdicts.
- D_repair: missing source/revision/target decision and authorized data location; blocks this repair pilot execution.

These blockers do not invalidate the completed model/runtime preparation or DEV smoke.
