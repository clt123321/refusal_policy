# Environment Report Addendum

- Safe proxy E2E completed on GPU0 with `sshleifer/tiny-gpt2`.
- 32 proxy rows across four H×P cells.
- Activation output: layer 0, final non-pad token, hidden width 2.
- Model load and capture completed; Transformers emitted a non-fatal compatibility warning for `masked_bias`.
- Proxy evaluator metrics: policy_choice_rate 0.5, task_correctness 1.0, valid_output_rate 1.0, mean_generation_length 3.0.
- Qwen 0.5B and 1.5B config probes succeeded; full load/generation profiling exceeded the current command timeout and remains pending.
- No real safety data, safety intervention, tampering, adaptive attack, or fine-tuning executed.
