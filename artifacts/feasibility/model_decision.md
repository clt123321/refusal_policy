# Model Decision (Capability-Only)

## What was tested

Both candidates were loaded in fp16 on a single A800 GPU each, chat-template applied, and given three clearly benign prompts (factual question, creative writing, code explanation). Both loaded successfully, produced non-empty valid completions, and ran at reasonable throughput/memory for this hardware.

| Model | Layers | Hidden size | Peak memory | Load time | Chat template |
|---|---:|---:|---:|---:|---|
| Qwen/Qwen2.5-0.5B-Instruct | 24 | 896 | ~1.0 GB | 12.5 s | OK |
| Qwen/Qwen2.5-1.5B-Instruct | 28 | 1536 | ~3.1 GB | 15.0 s | OK |

## What was NOT tested

Refusal dynamic range and baseline safety behavior were not measured. Doing so as specified requires real harmful prompts and an "actual harmful compliance" evaluator, which this session will not construct or run (see `artifacts/feasibility/DECISION_NOTE.md`). Model selection therefore remains **capability-only qualified**; it is not "capability-qualified aligned checkpoint" in the full TODO P04 sense until a human-approved harmful-prompt/evaluator contract exists and is run under appropriate review.

## Recommendation

- If/when a human-approved P03 data and evaluator contract exists: profile refusal dynamic range on both before final selection.
- Until then: `Qwen/Qwen2.5-1.5B-Instruct` is the tentative primary (more capability headroom), `Qwen/Qwen2.5-0.5B-Instruct` the fallback (lower memory/compute). Both are cached locally.
