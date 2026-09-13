# H0 Dry-Run Receipt (formal pipeline dry run)

- **Run ID:** `harness.dry-run.0001`
- **Status:** `SUCCEEDED`
- **Date (UTC):** 2026-09-13
- **Repo commit:** `611a63fbf2567e872a46cb4c1c3b537212fc930f`
- **Environment lock SHA-256:** `ccd472737122a183f805ae65d11f52c4d474c6b8417976972655559b7d05ba0d`
- **Model:** `Qwen/Qwen2.5-0.5B-Instruct` @ `7ae557604adf67be50417f59c2c2f167def9a775` (local HF cache; DEV-ONLY fixture)
- **Device:** cpu (all 8 A800 GPUs were saturated by other jobs at run time; the dry run is intentionally content- and compute-minimal)
- **Content:** 5 benign prompts (capital city, haiku, Python loop, freezing point, planet names). No harmful task, no raw harmful generation, no safety-mechanism modification.

## What was exercised (H0/H1 harness plumbing)

1. Environment lock capture (`EnvironmentLock.capture`, lock hash recorded).
2. Model adapter load + deterministic generation (`ModelAdapter.generate`, `determinism_hash`).
3. Utility evaluator and safety-seam wiring (benign refusal diagnostics only).
4. Cost tracker fields (primary estimated FLOPs + secondary axes) via manifest.
5. Content-addressed artifact store (output + receipt hashed, no raw artifacts in git).
6. Run manifest schema validation against `research/protocols/V4_PROTOCOL_SCHEMA.json`.

## Results

- Determinism hash: `3f724e14a7a14b584f8d58b5e6d1cebb2d8b7cebdfa06326edfecda788e2a263`
- Valid outputs: 5/5
- Refusal diagnostics (benign fixture): refusal_rate 0.0
- Manifest: `artifacts/harness/dry_run/DRY_RUN_RECEIPT.json` (schema-validated)
- Unit tests: `tests/test_harness.py` 10/10 pass; full suite 20/20 pass.

## Limits

This receipt validates the formal execution path (manifest → execute → record → store → validate) on benign content. It is not a scientific result, does not establish any R0a–R3 finding, and proves nothing about the research question. Harmful-task evaluation and any raw harmful generation remain restricted to the authorized executor per `H0_AUTHORIZATION.md`.

## Handoff note (H1 license/artifact gates)

H1 additionally requires licensed Gemma access (`google/gemma-2-2b-it`) and Fail-Closed artifact provenance before R0b. Those are external-access gates to be satisfied via the authorized executor, not through a proxy substitution.
