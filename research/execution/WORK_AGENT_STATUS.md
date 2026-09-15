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

## HarmBench DEV evaluator and checkpoint diagnostic

- Tokenizer root cause fixed in commit `18e8307ed733cd07e8d967759e7c7d0593dd3a2f`: Transformers 5.16 `LlamaTokenizer(vocab_file=...)` loaded the SentencePiece file as a 3-token special-token vocabulary. Native SentencePiece reported 32000 tokens and correctly encoded inputs; the evaluator now uses the pinned `tokenizer.model` directly with explicit Mistral BOS/EOS IDs and validates vocab size against model config.
- CPU validation: plain text encoded to 4 tokens; official prompt encoded to 310 tokens; IDs were within 32000 and masks had valid non-special positions.
- Fixed precheck attempt: execution SHA `18e8307ed733cd07e8d967759e7c7d0593dd3a2f`; 32/32 parsed, prediction counts yes=15/no=17/UNKNOWN=0; confusion matrix TP=15, TN=16, FP=0, FN=1; correct=31/32; gate passed. Peak classifier memory `14738422784` bytes; wall `3.2313098907470703` seconds; post-run GPU 2 MiB used / 24214 MiB free. Receipt: `artifacts/restricted/v6_e1/harmbench/precheck_result_fixed.json`.
- Original UNKNOWN receipt and failed tokenizer attempts remain at `precheck_result.json` and task logs; no sample, template, threshold or forced label was changed.
- Base/R_cal generation: 16 fixed behaviors, seed 17, Qwen native chat template, greedy, max_new_tokens=256. Receipt: `artifacts/restricted/v6_e1/harmbench/checkpoint_generation.json`; wall `83.02840638160706` seconds; peak memory `3113364480` bytes.
- Base/R_cal scoring: classifier loaded only after Qwen generation completed and GPU was released; official Mistral prompt, native SentencePiece, BF16. Receipt: `artifacts/restricted/v6_e1/harmbench/checkpoint_scoring_a02.json`; wall `2.3667733669281006` seconds; peak memory `14660661248` bytes.
- Scoring summary: B 3 yes / 13 no / 0 UNKNOWN / 16 valid; R_cal 3 yes / 13 no / 0 UNKNOWN / 16 valid. Each arm had 3 generations at max length 256. All 16 paired labels were identical; no pair changed.
- This is a small DEV behavior diagnostic only. It is not endpoint equivalence, repair success, E1, or tamper-resistance evidence.

## V6 E1 formal preparation

- Current phase: `4/7 — FORMAL E1 PREPARATION`
- Latest code/report commit before this preparation: `7b30edfa7e7326b54e037908662f8ee948a4728c`.
- DEV repair execution SHA: `39251df2ec3676e39a0479af336f22e9ca5b66fa`.
- HarmBench precheck and Base/R_cal diagnostic execution SHA: `18e8307ed733cd07e8d967759e7c7d0593dd3a2f`.
- Formal-preparation code SHA is the next local commit after these changes; no formal scientific task was run.

### New executable preparation entries

- `src/execution/formal_repair_entry.py`: reuses `src.execution.repair_runner.run_repair`; requires `mode=FORMAL`, `scientific_evidence=true`, C/P lineage alignment, explicit parent/config/data/output identity. It does not create a second training loop and cannot run while formal config/data are absent.
- `SafetyEvaluator.aggregate_content_labels(...)`: preserves yes/no/UNKNOWN and model/template/tokenizer identity for DEV content diagnostics.
- `SafetyEvaluator.evaluate_endpoint_gate(...)`: parameterized endpoint-band check; missing bands return `ENDPOINT_BANDS_NOT_FROZEN`, missing metrics return `ENDPOINT_METRICS_MISSING`, and no thresholds are guessed.
- Minimal validation: 22 targeted tests passed; compileall passed.

### Formal path audit

| Path | Actual state | Concrete blocker | Next executable action |
|---|---|---|---|
| `D_repair` | DEV materialized only | formal split hash/source/target construction not frozen | freeze formal manifest and write `v6_e1_repair_recipe.json` |
| Other seven formal splits | no authorized local manifest | source/revision/sealing/family rules absent | materialize and hash each split under restricted store |
| Repair C/P | runner exists; formal wrapper now exists | formal config/common stage absent | invoke `formal_repair_entry` twice with same recipe/data hash and distinct arm lineage |
| A0 | direction math only | model-level intervention runner and authorized executor absent | deliver bounded A0 implementation/artifact from authorized executor |
| Fresh A1 | no executable runner | attack implementation and authorized executor absent | deliver independent A1 runner/config/data/execution path |
| Endpoint qualification | orchestration hook + parameterized gate only | endpoint bands, match/audit data and evaluator handler absent | freeze metric bands and bind restricted evaluator handler |
| Benign plasticity | no formal runner/recipe | `D_plasticity` source/categories/curve rule absent | freeze data and minimal learning-curve fields |
| Summary/failure | `FormalE1Backend` has MATCHING_FAILED→INVALID path | cannot receive real stage outputs until above paths exist | run only after qualified hooks return real receipts |

A0/A1 are still formally non-runnable. The hook seam and pending jobs are not counted as implementations.

## Collaboration transport (current)

- GitHub `clt123321/refusal_policy` is the authoritative repository.
- The development machine publishes ordinary GitHub work branches; Mac Codex reviews and integrates them into GitHub `main`.
- The `diagon-python` relay is retired from daily `refusal_policy` synchronization.
