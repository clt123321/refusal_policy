# Work Agent Status — V6.E1 direct path

**Gate:** `DIRECT_REPAIR_CODE_INTEGRATED / 4090_REPAIR_GPU_SMOKE_COMPLETE / REPAIR_CALIBRATION_PILOT_COMPLETE / FORMAL_RECIPE_PENDING`

## Source

- GitHub execution branch: `work/4090-e1-67c90f0`
- Pilot execution SHA: `39251df2ec3676e39a0479af336f22e9ca5b66fa`
- Prior smoke/state commits remain in history: `3f788de1354b59a1d1e633af4e97c0e0693191b9`, `c9434417c2ddf3f344bbe41693cb3676669253c9`
- Repair commits present in source history: `7f590e2ee0e955acec34243e1a9fe0f30887c70d`, `d8bbb01c52a7b6ec2a02e11f89431e5b93976a37`
- Continuous/external-job orchestration remains frozen.

## Implemented

- Direct E1 executor CLI and coarse `FormalE1Backend` hook seam.
- Exact-ID split-isolation validator.
- DEV-only local model smoke backend.
- Parameterized repair runner with target-only loss, step checkpoints, explicit task/run/attempt/code/input identity and collision protection.
- Parameterized repair reload CLI with optional memory-reference comparison.
- Approved PKU-SafeRLHF DEV data materialization script and restricted manifest.
- Terminal `MATCHING_FAILED → INVALID` path without waiting for A1/plasticity.

## Repair calibration pilot

- Task: `V6.E1.DEV.REPAIR_CALIBRATION`
- Run/attempt: `V6.E1.DEV.REPAIR_CALIBRATION.PKU_SAFE_RLHF.s17` / `V6.E1.DEV.REPAIR_CALIBRATION.PKU_SAFE_RLHF.s17.a01`
- State: `DONE_DEV_ONLY`; no formal C/P or E1 scientific data.
- Source: `PKU-Alignment/PKU-SafeRLHF`, dataset revision `9421ffafec3fa40a1f1a7d567b4d525079477ecb`, `data/Alpaca3-8B/train.jsonl`; source file SHA256 `21c3b4f2572444e42d161f09166471d14208c9e153fcc0ec900ae05013e47d4c`.
- Selection: 20,950 source rows; 17,965 excluded because safe labels were not exactly one; 13 empty prompt/target rows excluded; 2,972 eligible before dedup; 42 duplicate IDs removed; 2,899 normalized-prompt-group-isolated rows available; zero overlength exclusions; seed 17 selected 512 train and 64 validation. Safe labels are dataset annotations, not independently audited truth.
- Data manifest: `artifacts/restricted/v6_e1/repair_pilot/pku_safe_rlhf_9421ffaf/manifest.json`; train SHA256 `8b609774bc2a46f69bab85121a9edcd66bf128270aa2bfd151f05c1a8017c89b`; validation SHA256 `0f3c759863cb2bfe894d597ac9b3e322887fdac9cf2763e424d7345aec4408aa`.
- Config: `configs/execution/v6_repair_pilot.json`; config SHA256 `eef6b7b65748286b51bacb117fe72bffd7bdd1c0d85647e1ed7f6385bd21f598`.
- Model: Qwen/Qwen2.5-1.5B-Instruct revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`, fp16, native chat template.
- Training: 64 optimizer steps, LoRA q_proj/v_proj rank 8 alpha 16, AdamW LR 2e-5, microbatch 2, accumulation 4, seed 17, fixed file order; wall `80.75621008872986` seconds.
- Tokens: full training sequence `72,329`; target/supervised training tokens `43,485`; validation per checkpoint `8,540` full and `4,950` target tokens.
- Train losses: recorded for all 64 steps in `repair_result.json`; first `1.8728000224`, final `1.7963272333`.
- Validation target NLL: step 0 `2.1746718440`; step 16 `2.1628486241`; step 32 `2.1482184608`; step 64 `2.1135325016`.
- Checkpoints: `artifacts/v6_e1/DEV/repair_calibration/pku_safe_rlhf/s17/a01/checkpoints/step_000000/adapter`, `step_000016/adapter`, `step_000032/adapter`, `step_000064/adapter`; final adapter: `artifacts/v6_e1/DEV/repair_calibration/pku_safe_rlhf/s17/a01/adapter`.
- PyTorch peak allocated memory: `6,677,236,736` bytes; post-run nvidia-smi sample: 2 MiB used / 24,214 MiB free. These are distinct measurements.
- Parameter update: 112/112 tensors changed from step 0 to final; max absolute difference `0.0015627401880919933`.
- Save/reload: training-end in-memory model reference saved to `memory_reference_logits.pt`; new process loaded final adapter and produced `SAFE`; logits max absolute difference `0.0` with tolerance `1e-5`; `reload_pass=true` and finite also passed. Receipt: `artifacts/v6_e1/DEV/repair_calibration/pku_safe_rlhf/s17/a01/acceptance_receipt.json`.
- Diagnostic boundary: NLL is training/fitting evidence only, not safety, utility, or tamper-resistance evidence.

## Formal data and recipe status

- Pilot IDs and normalized prompt groups are registered for future formal-split exclusion in the restricted manifest; complete eight-way formal semantic-family isolation is not established.
- Formal C/P endpoints and formal repair recipe/common stage remain unfrozen.
- A0/A1/content evaluator/formal plasticity have no capable implementation bound to Luna.
- No formal data or scientific E1 result exists.

## Next task

The approved repair calibration pilot is complete. Do not automatically enter formal C/P, A0/A1, content evaluation, or E1. Remaining work requires separate formal data/recipe gates and authorized capabilities.

## Collaboration transport (current)

- GitHub `clt123321/refusal_policy` is the authoritative repository.
- The development machine publishes ordinary GitHub work branches; Mac Codex reviews and integrates them into GitHub `main`.
- The `diagon-python` relay is retired from daily `refusal_policy` synchronization.
