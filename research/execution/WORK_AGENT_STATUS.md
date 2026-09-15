# Work Agent Status — V6.E1 direct path

**Gate:** `DIRECT_REPAIR_CODE_INTEGRATED / 4090_REPAIR_GPU_SMOKE_COMPLETE / FORMAL_RECIPE_PENDING`

## Source

- GitHub execution branch: `work/4090-e1-67c90f0`
- Verified execution SHA: `67c90f05f788a549f4abb1489989c47a25a995be`
- Repair commits present in source history: `7f590e2ee0e955acec34243e1a9fe0f30887c70d`, `d8bbb01c52a7b6ec2a02e11f89431e5b93976a37`
- Continuous/external-job orchestration remains frozen.

## Implemented

- Direct E1 executor CLI and coarse `FormalE1Backend` hook seam.
- Exact-ID split-isolation validator.
- DEV-only local model smoke backend.
- Parameterized repair runner with target-only loss, step checkpoints, explicit task/run/attempt/code/input identity and collision protection.
- Parameterized repair reload CLI; no development-machine paths are implicit.
- Tracked benign `v6_repair_dev.json` and fixture for independent 4090 runner validation.
- Terminal `MATCHING_FAILED → INVALID` path without waiting for A1/plasticity.

## DEV GPU result

- Task: `V6.E1.DEV.REPAIR_GPU_SMOKE`
- Run/attempt: `V6.E1.DEV.REPAIR_GPU_SMOKE.s17` / `V6.E1.DEV.REPAIR_GPU_SMOKE.s17.a01`
- Device: RTX 4090, `cuda`, torch `2.10.0+cu128`; post-run `nvidia-smi`: 2 MiB used, 24214 MiB free. PyTorch peak VRAM was not instrumented by this runner.
- Model: Qwen/Qwen2.5-1.5B-Instruct revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`; manifest: `artifacts/v6_e1_model_manifest.json`.
- Config/data SHA256: `fd151c627030ea7407a82c9e1d3b6e156e18b411019a94b7ee9b0ecb6475bc46` / `6ac5be0d282dda07cddfab3cb0a97b6eaa5189eb45f174ad32e06890a9c8e3a6`.
- Steps/tokens/wall: `2` / `79` complete input-sequence tokens / `22.79592990875244` seconds.
- Losses: `0.017715321853756905`, `0.5359166264533997`; loss increase is recorded, not treated as a scientific outcome.
- Checkpoints: `artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/checkpoints/step_000000/adapter`, `step_000001/adapter`, `step_000002/adapter`; final: `artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/adapter`.
- Step-0 to final: 112/112 tensors changed; max absolute difference `0.00020013423636555672`.
- Existing reload receipt: `reload_pass=true` means load succeeded and parameters were finite only: `artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/reload_receipt.json`.
- Additional reload acceptance: fixed input outputs exact-match (`SAFE`/`SAFE`), logits max absolute difference `0.0` with tolerance `1e-5`: `artifacts/v6_e1/DEV/repair_gpu_smoke/s17/a01/acceptance_receipt.json`.
- `scientific_evidence=false`; this is engineering validation only.

## Pilot data and recipe status

- Stable task: `V6.E1.DEV.REPAIR_PILOT`
- State: `READY_FOR_PI_DECISION`
- Candidate config: `configs/execution/v6_repair_pilot_candidate.json`
- Decision package: `research/execution/V6_E1_REPAIR_PILOT_DECISION_PACKAGE.md`
- No real pilot data was materialized: repository has no authorized, source-pinned safety repair corpus. The DEV fixture and HarmBench evaluation assets are explicitly excluded from promotion.
- Required before execution: PI/data-owner source and revision, target construction approval, candidate envelope approval, real file/ID hashes, length-policy receipt, then a new frozen config commit.


| Decision | Current engineering candidate | Required formal decision |
|---|---|---|
| D_repair | Tracked DEV fixture only | Exact revision, IDs, target construction and split hash |
| Parameterization | LoRA, q_proj/v_proj, rank 2, alpha 4, dropout 0 | LoRA versus full parameters; modules/rank/alpha |
| Optimizer | AdamW, lr 1e-4, zero decay, betas 0.9/0.999 | Optimizer, LR/betas/decay, fresh state and batch order |
| Schedule | Two DEV steps, batch 1, checkpoints 0/1/2 | Effective batch/tokens, candidate checkpoints and common C/P stage |
| Endpoint gate | Not evaluated in DEV | Equivalence bands, low-margin tail and sealed audit |
| Export/reload | PEFT adapter; finite/load and fixed-input replay validated | Final normalized export/reload format and tolerance |

## Next task

DEV GPU repair is complete. Formal C/P and E1 science remain blocked on PI recipe/data freeze and authorized A0/A1/evaluator capabilities. Do not infer scientific conclusions from this DEV result.

## Collaboration transport (current)

- GitHub `clt123321/refusal_policy` is the authoritative repository.
- The development machine publishes ordinary GitHub work branches; Mac Codex reviews and integrates them into GitHub `main`.
- The `diagon-python` relay is retired from daily `refusal_policy` synchronization.
