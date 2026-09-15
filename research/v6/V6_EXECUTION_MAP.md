# Current execution map — V7 screen primary, V6 tail only

## Current program routing (2026-09-15)

- **Primary next 3–5 day effort:** V7 same-checkpoint scoring-manipulation monitor screen. Protocol: `research/v7/V7_SCREEN_PROTOCOL.md`; five-task config: `configs/execution/v7_screen.json`.
- **V6 allowed tail:** verify reusable Base/environment/repair receipts and rerun the invalidated B/R_cal DEV generation+scoring with isolated model instances.
- **V6 paused:** formal E1 expansion, final repair/A0/A1 freeze, Week-2 and defense work. These are not V7 prerequisites.
- V7 is `COMPILED_NOT_READY`: asset fetching can start, but label/sandbox, rollout/activation and monitor entrypoints are not implemented. Do not call it READY from file presence.

The remainder of this document preserves the V6 execution path for provenance and eventual resumption.

# V6.E1 direct execution map — 4090 first

**Scope:** Week-1 E1 only: B, C, P construction; endpoint qualification; fresh A1; benign plasticity; E1 comparison. Week-2 and defense work remain frozen.

**Machine-readable plan:** `configs/execution/v6_e1_plan.json`

**4090 runtime overlay:** `configs/execution/runtime_4090.json`
**Independent repair DEV recipe:** `configs/execution/v6_repair_dev.json`

**Source-audit snapshot:** GitHub `main` was `67c90f05f788a549f4abb1489989c47a25a995be`; development branch `work/4090-e1-67c90f0` was fixed at `742e0f7bbf742010d824e4255d8dd4cd794a8602`. Later commits on that branch are outside this audit.

## 0. Start here

| Question | Authoritative source |
|---|---|
| Scientific question, arms, gates, outcomes | `TODO.md`, then `research/v6/V6_DECISION.md` and `research/execution/V6_E1_PREREGISTRATION.md` |
| Stable task IDs, dependencies, inputs and completion predicates | `configs/execution/v6_e1_plan.json` |
| What one attempt actually did | its immutable `repair_result.json`, `repair_failure.json`, evaluator receipt, manifest and cost ledger under `artifacts/`; a prose status page is not a run record |
| Current human navigation and capability audit | this file |

The task JSON is a definition/snapshot, not a mutable run database. Do not change a task definition after a failed attempt; create a new `attempt_id`, retain the prior receipt, and update only a human status summary if needed.

### Current runnable entrypoints

- Repair training (DEV now; FORMAL only after freeze): `python -m src.execution.repair_runner --help`.
- Repair reload verification: `python -m scripts.reload_repair_artifact --help`; pass `--reference` for a meaningful round-trip check.
- HarmBench DEV precheck: `python -m scripts.run_harmbench_classifier_precheck --help`.
- Paired B/R_cal DEV generation: `python -m scripts.generate_harmbench_checkpoints --help`. The pre-audit receipt is invalid for arm comparison and must not be reused.
- DEV checkpoint scoring: `python -m scripts.score_harmbench_checkpoints --help`.
- Coarse orchestration seam: `python -m scripts.v6_e1_executor --help`; this does not supply A0/A1/evaluator implementations.

Every command is run from the repository root at a clean committed checkout. Developer-machine caches may be reused; personal absolute paths are passed as CLI arguments, never committed.

For failures: repair writes `<output>/repair_failure.json`; the stage executor writes `<run-dir>/gate_state.json` plus content-addressed stage artifacts; successful evaluator scripts write the requested `--output`. HarmBench scripts currently leave pre-output failures in the invoking job's stderr/log, so that log must be retained with the attempt rather than represented as a successful JSON result.

### Recommended shortest path

1. On the 4090, verify the existing DEV repair result/reload receipt against its recorded execution SHA; do not rerun if the immutable files validate.
2. If a corrected content diagnostic is useful for the endpoint preflight, rerun B/R_cal generation at this audited code state, then score it. It remains DEV-only.
3. The next scientific step is not another DEV repair: the PI/executor must freeze `D_repair`, endpoint bands and the bounded A0/A1 preflight recipes, then bind authorized A0/A1/content-evaluator implementations. Only descendants of a missing item are blocked.

The first useful GPU command on this audited code is the corrected, **DEV-only** B/R_cal generation (set the three paths to existing on-host assets; use the cleanup commit as `EXECUTION_SHA`):

```bash
python -m scripts.generate_harmbench_checkpoints \
  --base "$V6_MODEL_PATH" \
  --adapter "$V6_REPAIR_ADAPTER" \
  --samples "$V6_HARMBENCH_SAMPLES" \
  --output artifacts/restricted/v6_e1/harmbench/checkpoint_generation_isolated.json \
  --device cuda --repo . --execution-sha "$EXECUTION_SHA"
```

It deliberately loads B and R_cal from separate base-model instances. Do not promote its output to FORMAL or endpoint-qualified data.

## 1. Historical integration provenance

- Relay branch: `refusal-policy-handoff-4090-20260915-d8bbb01`
- Verified remote/head SHA: `77ed1780f56affc6ee6af5e73b20f2cce22cefba`
- Common project ancestor: `90cf38bb632c0e6ca861596a59dec4acba23f8ba`
- Required repair ancestors are present:
  - `7f590e2ee0e955acec34243e1a9fe0f30887c70d` — parameterized repair runner, draft config and tests;
  - `d8bbb01c52a7b6ec2a02e11f89431e5b93976a37` — runner CLI, target-only loss and reload helper.
- The relay branch does not contain the later `45f9f4b…` execution plan. Merging the complete branch would delete that plan, so only reviewed refusal-policy commits were integrated with original-SHA provenance.
- Continuous orchestration commits were inspected and excluded: they create external jobs but provide no tracked consumer or new scientific capability.

### Current capability facts

| Capability | Actual state after integration | Scientific state |
|---|---|---|
| V4 manifests/artifacts/cost/censoring | Implemented | Reused unchanged |
| Direct E1 stage CLI | Implemented; coarse stage runner | Engineering seam, not a formal result |
| Split exact-ID isolation | Implemented | Family-level review still required |
| Qwen benign runtime smoke | Implemented | DEV-only |
| Repair runner | Real CLI→config/data validation→LoRA training→checkpoint/save chain; fresh optimizer per invocation; C/P `training_recipe_sha256` recorded separately from lineage | DEV GPU success is developer-reported; receipts absent from Git checkout; FORMAL recipe pending |
| Repair reload | Real CLI; adapter reload, finite-parameter check and optional logits-reference check; a reference mismatch now fails | DEV GPU success is developer-reported, not independently verified here |
| Formal repair recipe | Not frozen | Blocked on PI/preflight choices |
| A0 model runner | Not implemented | Authorized A0-capable executor required |
| A1 runner | Not implemented | Authorized A1-capable executor required |
| Content evaluator | HarmBench DEV classifier/generation/scoring scripts exist; formal endpoint hook is not bound | Reference token-ID equivalence is unproven; authorized evaluator and endpoint bands required |
| Formal plasticity runner | Not implemented | Luna may implement after data freeze |
| Scientific data | None in Git; named DEV/restricted receipts are development-machine reports | No formal E1 claim |

“已有实现”“执行端报告但仓库无产物”“实现缺失”“正式 recipe 未冻结” are separate states. Repair is implemented; reported DEV receipts are not in Git; A0/A1/formal evaluator are missing; formal repair configuration is not frozen.

## 2. Fixed E1 topology

```text
B = Base -------------------------------------> fresh A1 ---+
                                                           |
C = Base -> same frozen Repair --------------> qualify ----+--> E1 summary
                                                           |
P = Base -> A0 [saved parent] -> same Repair -> fresh A1 --+
```

A0 is provenance only, never a fourth A1 arm. C/P must have the same final `training_recipe_sha256` and repair stage; their full config hashes differ because lineage differs. Parameter distance is recorded, not matched. Checkpoint existence never implies qualification.

## 3. Current task table

| Task/group | State | Independent next action or blocker |
|---|---|---|
| `DEV.CODE_RECONCILE` | Integrated; audited at fixed branch SHA | Run affected CPU tests on the cleanup commit |
| `DEV.MODEL_PREFETCH` | Developer reports cached; not independently verified | Validate the existing manifest/files in place; do not redownload if hashes pass |
| Eight `DEV.DATA.*` tasks | Independently blocked/ready by source | Prepare only the selected split; no split waits for all others |
| `DEV.DATA_FREEZE` | Blocked by eight split rows | Final exact-ID and family-isolation aggregation only |
| `DEV.EVALUATOR_AUTHORIZE` | Blocked | Authorized evaluator/handler not bound |
| `DEV.REPAIR_FREEZE` | Blocked scientific choice | Lock candidate envelope and stage-selection rule, not final stage |
| `DEV.A0_FREEZE` | Blocked science + capable executor | Lock candidate envelope; no Luna default |
| `DEV.A1_FREEZE` | Blocked science + capable executor | Lock candidate grid/rule; final grid comes after preflight |
| `DEV.RUNTIME_SMOKE` | Ready after code/model | Benign Qwen/LoRA executor smoke |
| `DEV.REPAIR_GPU_SMOKE` | Developer reports complete; receipt absent from Git | Verify the existing receipt on 4090; rerun only if it is missing/invalid |
| Three `DEV.PREFLIGHT_*` | Locally blocked | Each waits only for its required splits/capabilities |
| `DEV.FREEZE` | Blocked by all preflights and aggregate isolation | Select/freeze final recipes, stage, grid, seeds and compute cap |
| Formal construction/qualification | Blocked by `E1_PREFLIGHT_PASS` | Existing scientific gates unchanged |
| Formal A1/plasticity | Conditional | Run only after `QUALIFIED` endpoint audit |
| `FORMAL.SUMMARY` | Conditional terminal | `MATCHING_FAILED` goes directly to INVALID without A1/plasticity |

Full task IDs, commands, dependencies, inputs, outputs, owners and completion criteria are in the JSON plan. `task_id`, `run_id` and `attempt_id` are distinct; retrying requires a new attempt/output path. Configuration, data, parent artifact and execution SHA are included in the repair receipt identity.

## 4. Candidate lock → preflight → final freeze

The old semantic loop is removed:

```text
bounded candidate envelope + pilot-only data + deterministic selection rule
                              ↓
                    measured DEV preflight
                              ↓
final A0/repair/A1 recipe + common repair stage + A1 grid + seeds + cap
                              ↓
                          FORMAL E1
```

- `DEV.REPAIR_FREEZE`, `DEV.A0_FREEZE`, and `DEV.A1_FREEZE` lock candidate ranges and selection rules before pilot outcomes.
- `DEV.FREEZE` is the only final-freeze task and runs after preflight.
- The tracked `v6_repair_dev.json` is a benign engineering fixture. Its rank/LR/two steps may not enter the final recipe by default.

## 5. Split-local preparation and readiness

Each of `D_A0_loc`, `D_repair`, `D_endpoint_match`, `D_endpoint_audit`, `D_A1_train`, `D_attack_eval`, `D_function`, and `D_plasticity` has its own task and manifest row. A DEV task depends only on the rows it consumes. `DEV.DATA_FREEZE` later performs the full cross-split exact-ID/family audit.

A blocked evaluator does not block model prefetch, code validation, benign runtime smoke, independent repair smoke, or source-approved split preparation. Work stops only when there are no dependency-satisfied tasks and no task is running. This is a human/Work-Agent readiness rule, not a new scheduler.

## 6. Completed operation versus passed gate

Every result records execution completion separately from scientific validity.

- Endpoint audit `QUALIFIED`: enable A1 and plasticity, then normal summary.
- Endpoint audit `MATCHING_FAILED`: persist all endpoint receipts, mark A1/plasticity `SKIPPED_BY_MATCHING_FAILED`, and emit E1 `INVALID` immediately.
- Infrastructure failure: retain/charge the attempt and classify it separately; do not convert it into scientific failure.

The coarse `FormalE1Backend` now reuses the pilot A0 artifact, enforces common C/P repair stage, evaluates match before sealed audit, and supports the terminal INVALID path. It remains a hook seam, not proof that A0/A1/evaluation are executable.

## 7. Repair DEV command (rerun only if the existing receipt cannot be verified)

Prerequisites:

1. clean checkout at the exact execution SHA;
2. `.venv-v6` has `torch`, `transformers`, `peft`;
3. `V6_MODEL_PATH` points to the exact pinned Qwen snapshot;
4. no existing result with a different run identity at the selected output path.

```bash
python -m src.execution.repair_runner \
  --config configs/execution/v6_repair_dev.json \
  --parent-model "$V6_MODEL_PATH" \
  --output artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01 \
  --device cuda \
  --execution-sha "<clean-checkout-full-sha>" \
  --task-id V6.E1.DEV.REPAIR_GPU_SMOKE \
  --run-id V6.E1.DEV.REPAIR_GPU_SMOKE.s17 \
  --attempt-id V6.E1.DEV.REPAIR_GPU_SMOKE.s17.a01

python -m scripts.reload_repair_artifact \
  --base "$V6_MODEL_PATH" \
  --adapter artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/adapter \
  --device cuda --dtype float16 \
  --reference artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/memory_reference_logits.pt \
  --receipt artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/reload_receipt.json
```

Completion requires zero exit status, finite losses, step-0/1/2 adapters, `execution_completed=true`, `scientific_evidence=false`, distinct task/run/attempt identity, and `reload_pass=true`. Pass `--reference artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/memory_reference_logits.pt` to reload; without a reference, reload only checks finite parameters. CUDA tensor validation alone does not satisfy this task.

## 8. Formal C decisions still missing

The PI must freeze after the bounded pilot:

- exact `D_repair` revision, IDs and target construction (the PKU candidate pool is materialized only on the developer machine and has not passed full split isolation);
- LoRA versus full-parameter repair, and modules/rank/alpha if LoRA;
- optimizer, LR/betas/decay, fresh-init and identical C/P batch-order rule;
- effective batch/tokens, candidate checkpoints and the one common formal stage;
- endpoint equivalence bands including low-margin tail;
- normalized export/reload format.

The executor freezes one training recipe, then materializes lineage-specific C/P configs whose recorded `training_recipe_sha256` is identical. The DEV fixture is not that recipe.

## 9. Execution responsibility

- **Work Agent/Luna:** CPU tests; asset verification; benign runtime/repair DEV tasks; manifests; deterministic summary implementation.
- **Authorized A0 executor:** real model intervention and A0 artifact.
- **Authorized A1 executor:** fresh parameter attack.
- **Authorized content evaluator:** content scoring and restricted raw-output handling.

Missing capability is a local blocker. Do not change model, introduce a generic trainer, or spawn an external process to bypass H0.

## 10. KEEP / FREEZE / CHANGE

**KEEP:** V4 manifests, artifact lineage/store, cost/failure/OOM/censoring, H0 boundary, direction math, exact-ID isolation, direct executor, existing repair runner and reload path.

**FREEZE:** continuous/external-job queue, scheduler/heartbeat/dashboard, V5 replication expansion, Week-2, defense and new attack implementations.

**CHANGE completed in this audit:** strict reload-reference failure; fresh-base isolation for B/R_cal DEV generation; one shared classifier tokenizer implementation; classifier context/provenance checks; separate full-config and common C/P training-recipe hashes; truthful evidence boundaries and navigation.

## 11. Validation boundary

Mac validation covers unit/integration tests, JSON parsing, DAG/ID checks, candidate→preflight→final-freeze semantics, local-blocker independence, terminal INVALID behavior, compileall and diff/security inspection.

Not independently verified on the Mac: the reported model cache, repair/reload receipts, restricted pilot/candidate data, throughput/VRAM/storage, and HarmBench receipts. Still unimplemented or unfrozen: formal data isolation, A0, A1, authorized endpoint evaluator, plasticity execution, deterministic multi-seed summary and every scientific E1 result.
