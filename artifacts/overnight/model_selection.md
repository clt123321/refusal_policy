# Model Selection

## Scope

This is infrastructure profiling only. No model is capability-qualified for the scientific protocol, and no result here is safety evidence.

## DEV_ONLY_MODEL

- `sshleifer/tiny-gpt2`
- Role: `DEV_ONLY_MODEL`
- Use: load, tokenization, hook shape, streaming capture, proxy operators
- Not instruction-tuned and not eligible for C01/C03
- Status: loaded successfully on GPU0; layer-0 capture completed on `PIPELINE_VALIDATION_ONLY` proxy assay

## Candidate configurations

| Model | Family | Config probe | Role |
|---|---|---|---|
| `Qwen/Qwen2.5-1.5B-Instruct` | Qwen2.5 | available; hidden size 1536; 28 layers | primary feasibility candidate, pending human capability review and full load/profile |
| `Qwen/Qwen2.5-0.5B-Instruct` | Qwen2.5 | available; hidden size 896; 24 layers | fallback / lower-memory candidate, pending human capability review |
| `HuggingFaceTB/SmolLM2-1.35B-Instruct` | SmolLM2 | identifier probe failed | dropped as unavailable identifier; no download attempted |

## Recommendation

- Primary candidate: `Qwen/Qwen2.5-1.5B-Instruct`, only after human approval of model/data/evaluator contract.
- Fallback: `Qwen/Qwen2.5-0.5B-Instruct` if primary load, memory, or benign capability smoke fails.
- Infrastructure model: `sshleifer/tiny-gpt2`, permanently marked `DEV_ONLY_MODEL`.

## Limitations

No checkpoint was treated as aligned or capability-qualified. No harmful prompts, safety endpoints, tampering, adaptive search, or fine-tuning were run.
