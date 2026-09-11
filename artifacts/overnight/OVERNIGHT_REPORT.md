# Overnight Report

## Current status

- Gate 0: `BLOCKED_HUMAN_REVIEW`
- Gate 1: `NOT_YET_DECIDABLE`
- Pipeline: `ENGINEERING_READY_PENDING_HUMAN_GATE0`
- Final scientific status: not causal feasibility; no safety conclusion

## Human decisions required

1. **Decision:** approve/freeze P01 claim contract and literature-collision review.
   **Why required:** TODO permits implementation but does not delegate scientific claim approval.
   **Default recommendation:** approve only bounded claims in TODO; retain attack-family qualification.
   **What becomes unblocked:** formal Gate 0 P01 hash.

2. **Decision:** approve P03 data, split provenance, evaluator cards, and human calibration.
   **Why required:** no approved real safety dataset or evaluator calibration exists in the repository.
   **Default recommendation:** provide safe, licensed manifests; keep proxy artifacts separate and non-evidentiary.
   **What becomes unblocked:** formal C01/C03 data preparation.

3. **Decision:** approve primary model and capability-qualified common set.
   **Why required:** config availability is not capability qualification.
   **Default recommendation:** review Qwen/Qwen2.5-1.5B-Instruct first, Qwen/Qwen2.5-0.5B-Instruct as fallback.
   **What becomes unblocked:** P04 model hash and model smoke profile.

4. **Decision:** approve P02 attack permissions, budget schema, and sealed-A4 handling.
   **Why required:** these involve safety-policy removal and adaptive tampering and cannot be inferred as an engineering default.
   **Default recommendation:** keep A1–A4 blocked until explicit review and sealed manifests.
   **What becomes unblocked:** only the approved non-confirmatory feasibility scope.

5. **Decision:** sign Gate 0 after hashes, evaluator calibration, split isolation, FLOPs accounting, and power simulation are reviewed.
   **Why required:** this is the protocol gate, not a code readiness check.
   **Default recommendation:** do not treat proxy validation as Gate 0 or Gate 1 evidence.
   **What becomes unblocked:** approved C01–C03 feasibility execution.

## Engineering completed

- Safe proxy H×P dataset builder with four balanced cells and explicit `PIPELINE_VALIDATION_ONLY` label.
- Transformer runtime loader with padding-safe final non-pad token extraction.
- Layer activation capture with CPU streaming mean aggregation.
- Explicit H contrast, P contrast, and H×P interaction extraction.
- Proxy-only remove/add/patch tensor operators and norm-matched/orthogonal controls.
- Structured proxy evaluator separating policy choice, task correctness, validity, and length.
- Deterministic bootstrap utility and unit tests.
- CLI for proxy assay and activation capture.
- Run/config fields preserve seed, split, role, and revision intent; no raw dangerous text is stored.
- Gate blocker analysis and model-selection note.

## End-to-end validation

`dataset → activation → contrast → proxy intervention → evaluator` completed on `DEV_ONLY_MODEL=sshleifer/tiny-gpt2` with safe synthetic proxy data.

- Proxy assay: 32 rows, four H×P cells.
- Activation capture: GPU0, layer 0, final non-pad position.
- Proxy evaluator: valid output 1.0, task correctness 1.0, policy choice rate 0.5.
- Unit tests: 4 passed.
- Python compile check: passed.
- Proxy results are pipeline validation only and cannot support refusal-policy or Gate 1 claims.

## Model readiness

- Infrastructure: `sshleifer/tiny-gpt2`, loaded and captured successfully; `DEV_ONLY_MODEL`, not eligible for science.
- Primary candidate: `Qwen/Qwen2.5-1.5B-Instruct`, config available; full profile timed out during download/initialization, pending rerun.
- Fallback: `Qwen/Qwen2.5-0.5B-Instruct`, config available; full profile timed out during download/initialization, pending rerun.
- SmolLM2 candidate: identifier unavailable and dropped.

## GPU readiness

- Proxy capture used one GPU and completed without OOM.
- Formal C01/C03 estimates remain unmeasured because no approved aligned model/data contract exists.
- TODO feasibility budget remains the controlling estimate: one 80GB GPU and approximately 15–35 A100-hours; this is not a new measurement.

## Remaining blockers before real feasibility

- Human approval and hashes for P01–P04.
- Approved real data and split provenance.
- Human-calibrated AHC/utility/capability evaluator.
- Model capability qualification and full load/profile.
- Explicit P02 decision for any safety-policy intervention or attack work.
- Formal FLOPs ledger, sealed-A4 manifest, and power simulation review.

## Exact next command

After Gate 0 approval and after replacing placeholders with approved hashes/configs:

```bash
PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 python scripts/collect_activations.py \
  --model <APPROVED_MODEL_ID> \
  --data <APPROVED_CONSTRUCT_FIT_MANIFEST> \
  --output artifacts/feasibility/<RUN_ID>/construct_fit_activations.json \
  --device cuda --dtype bfloat16
```

Missing parameters: approved model ID, approved construct-fit manifest path, run ID, and the human-approved capture layer/token config. No command above should be run on real safety data before Gate 0 sign-off.
