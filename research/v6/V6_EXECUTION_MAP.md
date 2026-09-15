# V6.E1 direct execution map — 4090 first

**Scope:** Week-1 E1 only: B, C, P construction; endpoint qualification; fresh A1; benign plasticity; E1 comparison. Week-2 and defense work remain frozen.

**Machine-readable plan:** `configs/execution/v6_e1_plan.json`

**4090 runtime overlay:** `configs/execution/runtime_4090.json`
**Independent repair DEV recipe:** `configs/execution/v6_repair_dev.json`

## 1. Source and implementation audit

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
| Repair runner | Implemented; parameterized CLI, target-only loss, checkpoints and identity receipt | Independent 4090 GPU validation pending |
| Repair reload | Implemented; base/adapter/device/receipt are explicit CLI arguments | GPU validation pending |
| Formal repair recipe | Not frozen | Blocked on PI/preflight choices |
| A0 model runner | Not implemented | Authorized A0-capable executor required |
| A1 runner | Not implemented | Authorized A1-capable executor required |
| Content evaluator | Interface only | Authorized evaluator required |
| Formal plasticity runner | Not implemented | Luna may implement after data freeze |
| Scientific data | None | No E1 claim |

“此前未取得代码”“实现缺失”“正式 recipe 未冻结” are now separate states. Repair is the first; A0/A1/evaluator are the second; formal repair configuration is the third.

## 2. Fixed E1 topology

```text
B = Base -------------------------------------> fresh A1 ---+
                                                           |
C = Base -> same frozen Repair --------------> qualify ----+--> E1 summary
                                                           |
P = Base -> A0 [saved parent] -> same Repair -> fresh A1 --+
```

A0 is provenance only, never a fourth A1 arm. C/P must reference the same final recipe hash and repair stage. Parameter distance is recorded, not matched. Checkpoint existence never implies qualification.

## 3. Current task table

| Task/group | State | Independent next action or blocker |
|---|---|---|
| `DEV.CODE_RECONCILE` | Integrated, validation pending | Run CPU tests and commit a clean traceable code SHA |
| `DEV.MODEL_PREFETCH` | Ready, network required | Cache/hash exact Qwen revision; existing cache may be reused |
| Eight `DEV.DATA.*` tasks | Independently blocked/ready by source | Prepare only the selected split; no split waits for all others |
| `DEV.DATA_FREEZE` | Blocked by eight split rows | Final exact-ID and family-isolation aggregation only |
| `DEV.EVALUATOR_AUTHORIZE` | Blocked | Authorized evaluator/handler not bound |
| `DEV.REPAIR_FREEZE` | Blocked scientific choice | Lock candidate envelope and stage-selection rule, not final stage |
| `DEV.A0_FREEZE` | Blocked science + capable executor | Lock candidate envelope; no Luna default |
| `DEV.A1_FREEZE` | Blocked science + capable executor | Lock candidate grid/rule; final grid comes after preflight |
| `DEV.RUNTIME_SMOKE` | Ready after code/model | Benign Qwen/LoRA executor smoke |
| `DEV.REPAIR_GPU_SMOKE` | First direct repair GPU task | Depends only on code, exact model and tracked benign DEV config/data |
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

## 7. First 4090 repair command

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
  --receipt artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/reload_receipt.json
```

Completion requires zero exit status, finite losses, step-0/1/2 adapters, `execution_completed=true`, `scientific_evidence=false`, distinct task/run/attempt identity, and `reload_pass=true`. CUDA tensor validation alone does not satisfy this task.

## 8. Formal C decisions still missing

The PI must freeze after the bounded pilot:

- exact `D_repair` revision, IDs and target construction;
- LoRA versus full-parameter repair, and modules/rank/alpha if LoRA;
- optimizer, LR/betas/decay, fresh-init and identical C/P batch-order rule;
- effective batch/tokens, candidate checkpoints and the one common formal stage;
- endpoint equivalence bands including low-margin tail;
- normalized export/reload format.

Luna encodes these once in `v6_e1_repair_recipe.json`; C and P consume its identical hash. The DEV fixture is not that file.

## 9. Execution responsibility

- **Luna:** CPU tests; asset preparation; benign runtime/repair DEV tasks; manifests; deterministic summary implementation.
- **Authorized A0 executor:** real model intervention and A0 artifact.
- **Authorized A1 executor:** fresh parameter attack.
- **Authorized content evaluator:** content scoring and restricted raw-output handling.

Missing capability is a local blocker. Do not change model, introduce a generic trainer, or spawn an external process to bypass H0.

## 10. KEEP / FREEZE / CHANGE

**KEEP:** V4 manifests, artifact lineage/store, cost/failure/OOM/censoring, H0 boundary, direction math, exact-ID isolation, direct executor, existing repair runner and reload path.

**FREEZE:** continuous/external-job queue, scheduler/heartbeat/dashboard, V5 replication expansion, Week-2, defense and new attack implementations.

**CHANGE completed in this integration:** parameterized repair reload; traceable task/run/attempt identity; independent repair DEV path; candidate-versus-final freeze; per-split dependencies; task-local blocking; common-stage enforcement; match/audit terminal INVALID path; truthful executor capability labels.

## 11. Validation boundary

Mac validation covers unit/integration tests, JSON parsing, DAG/ID checks, candidate→preflight→final-freeze semantics, local-blocker independence, terminal INVALID behavior, compileall and diff/security inspection.

Still pending on the development machine: exact model cache manifest, actual 4090 repair/reload receipt, throughput/VRAM/storage, all formal data, A0/A1/evaluator/plasticity execution and every scientific E1 result.
