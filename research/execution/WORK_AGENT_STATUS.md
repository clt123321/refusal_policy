# Work Agent Status — V6.E1 direct path

**Gate:** `DIRECT_REPAIR_CODE_INTEGRATED / DEVELOPER_REPORTED_DEV_RUNS / FORMAL_RECIPE_PENDING`

> Evidence boundary (source audit at `742e0f7bbf742010d824e4255d8dd4cd794a8602`): the GPU receipts and restricted artifacts named below are gitignored and were not present in the audited checkout. Their numbers are development-machine reports, not independently verified repository evidence. A config flag such as `scientific_evidence=true`, an import, or a checkpoint path is never completion evidence; only an immutable run/result record plus the applicable scientific gates is authoritative.

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

## Repair calibration pilot (development-machine report)

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

## HarmBench DEV evaluator and checkpoint diagnostic (development-machine report)

- Tokenizer root cause fixed in commit `18e8307ed733cd07e8d967759e7c7d0593dd3a2f`: Transformers 5.16 `LlamaTokenizer(vocab_file=...)` loaded the SentencePiece file as a 3-token special-token vocabulary. Native SentencePiece reported 32000 tokens and correctly encoded inputs; the evaluator now uses the pinned `tokenizer.model` directly with explicit Mistral BOS/EOS IDs and validates vocab size against model config.
- CPU validation: plain text encoded to 4 tokens; official prompt encoded to 310 tokens; IDs were within 32000 and masks had valid non-special positions.
- Fixed precheck attempt: execution SHA `18e8307ed733cd07e8d967759e7c7d0593dd3a2f`; 32/32 parsed, prediction counts yes=15/no=17/UNKNOWN=0; confusion matrix TP=15, TN=16, FP=0, FN=1; correct=31/32; gate passed. Peak classifier memory `14738422784` bytes; wall `3.2313098907470703` seconds; post-run GPU 2 MiB used / 24214 MiB free. Receipt: `artifacts/restricted/v6_e1/harmbench/precheck_result_fixed.json`.
- Original UNKNOWN receipt and failed tokenizer attempts remain at `precheck_result.json` and task logs; no sample, template, threshold or forced label was changed.
- Base/R_cal generation: 16 fixed behaviors, seed 17, Qwen native chat template, greedy, max_new_tokens=256. Receipt: `artifacts/restricted/v6_e1/harmbench/checkpoint_generation.json`; wall `83.02840638160706` seconds; peak memory `3113364480` bytes.
- The reported Base/R_cal generation and scoring receipt is **superseded and invalid for arm comparison**: the generating script constructed `R_cal` by wrapping the same Python model object already stored as `B`, so adapter-state isolation was not guaranteed. The audited implementation now generates B first and then loads a fresh base instance for R_cal. The corrected DEV diagnostic has not been run or independently verified.
- Even after rerun, this is only a small DEV behavior diagnostic. It cannot establish endpoint equivalence, repair success, E1, or tamper resistance.

## Formal preparation updates

- Phase: `4/7 — FORMAL E1 PREPARATION`.
- Corrected boundary: tokenizer validity is not reference equivalence; adapter file presence is not adapter activation; formal entry import is not formal training validation.
- Tokenizer reference check: native SentencePiece with the pinned `tokenizer.model` produced complete IDs for ordinary text, double spaces, newline text and the official HarmBench template; BOS=1, no synthetic EOS, non-special IDs were in `[0, 32000)`. This is a limited reference-path check, not a proof of full runtime equivalence.
- R_cal activation check: `PeftModel.from_pretrained` adapter enabled vs the same loaded base with adapter layers disabled on a fixed 36-token input gave logits max absolute difference `1.4765625`, L2 `124.43990325927734`; top ID was unchanged but adapter effect was nonzero. Adapter config SHA `4949e56a319b07ee0c40427f23af11a2d282c83f60447e9a71ec9ee97b410824`; adapter weights SHA `5cf034150d918da7bb92a7c71aaf366a4aafe3eff97ba3f3f1acb847ca89fd6a`. Receipt: `artifacts/v6_e1/DEV/repair_calibration/pku_safe_rlhf/s17/a01/adapter_identity_check.json`.
- Formal candidate pool materialized, not formal-frozen: `artifacts/restricted/v6_e1/repair_candidate_pool/candidate_pool.jsonl`; 2,323 rows; file SHA `34a198e2278b6214162c9ad54c97bed51b32ba6fa7fd619c08a68106c17ab361`; IDs SHA `2540eae087fa1c139244e8e71a4a28901b53fa81b1f65d61be243eceeea8e8a4`; source is PKU-SafeRLHF revision `9421ffafec3fa40a1f1a7d567b4d525079477ecb`. Excluded prior DEV IDs: 579; safe-label rule and normalized prompt grouping retained; formal eight-way isolation remains incomplete.
- Candidate config: `configs/execution/v6_e1_repair_candidate.json`; recommended split 2048 train / 256 validation / 19 reserve; recommended LoRA rank 8 alpha 16 q/v, AdamW 2e-5, batch 2 × accumulation 4, 512 steps, checkpoints 0/64/128/256/512. All remain `RECOMMENDED_PENDING_FREEZE` and no formal C/P was run.
- Formal repair after freeze uses the single `run_repair` training implementation. `formal_repair_entry.run_formal_repair` is an import-level contract adapter, not a standalone CLI. C/P have distinct full config hashes because lineage differs; equality is enforced with the recorded `training_recipe_sha256`, which excludes only lineage/output fields. The candidate remains intentionally rejected until the formal recipe and gates are frozen.

### V6 corrected DEV arm comparison

- Corrected generation execution SHA: `eeba9857342ec1a3ef1ad867db0a556d05ce5f0d`.
- Generation receipt: `artifacts/restricted/v6_e1/harmbench/checkpoint_generation_a02.json`; B was generated first from a base model, released, then R_cal was loaded from a distinct fresh base instance. Base and adapter file hashes are recorded in the receipt.
- Scoring receipt: `artifacts/restricted/v6_e1/harmbench/checkpoint_scoring_a03.json`; classifier ran after Qwen release.
- Corrected DEV summary: B `1 yes / 15 no / 0 UNKNOWN / 16 valid`, R_cal `3 yes / 13 no / 0 UNKNOWN / 16 valid`; max-length counts B=1 and R_cal=3; paired label changes=2/16. This remains DEV calibration, not formal E1.

## V7 asset readiness

- Countdown-Code fetched to restricted storage at revision `170ee8139cd836d6ab7b7b3a70c2063906363db0` (`Update citation information in README.md`).
- Its root license is absent; the embedded `verl/verl/LICENSE` does not license the project root. This remains `UNRESOLVED_NOT_USED`, not PASS. The fetched restricted copy is not an execution input and must not be committed.
- The authoritative protocol and task config are now `research/v7/V7_SCREEN_PROTOCOL.md` and `configs/execution/v7_screen.json`. They replace all upstream code/data/distillation dependencies with the independently specified deterministic generator `V7.ARITH.v1`; this is a self-built screen, not a Countdown-Code reproduction.
- No generated V7 split, label receipt or rollout exists yet. Real hashes are computed only after S0 materializes files.
- Development-machine implementation scope is limited to the planned `scripts.v7_generate_tasks`, `scripts.v7_validate_labels`, and `scripts.v7_run_rollouts` entrypoints. S0→S1→S2 does not depend on S3 monitor fitting or S4 decision implementation.
- V7 state: `INPUT_SPEC_FROZEN_RUNNER_MISSING`; protocol/file presence and the earlier clone are not runnable or scientific evidence.

## Collaboration transport (current)

- GitHub `clt123321/refusal_policy` is the authoritative repository.
- The development machine publishes ordinary GitHub work branches; Mac Codex reviews and integrates them into GitHub `main`.
- The `diagon-python` relay is retired from daily `refusal_policy` synchronization.
