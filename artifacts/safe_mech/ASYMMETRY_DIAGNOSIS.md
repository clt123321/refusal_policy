# ASYMMETRY_DIAGNOSIS

Role: `SAFE_MECH_BENIGN_PROXY`. Diagnoses why ADD (sufficiency, +25.0pp [12.5, 40.6], all 6 controls flat at 0) worked while REMOVE (necessity) stayed at 0pp across every residual-level scope tested (1 layer, 6 layers, all 28 layers, and k=1/2/4/8-dim subspaces).

## Best explanation of ADD/REMOVE asymmetry

**The residual-stream mean-difference P-direction is causally sufficient to push behavior toward "abstain" when added to a neutral context, but it is not the necessary substrate the model actually relies on when it has already been instructed to abstain — the real necessary component lives inside one specific module's raw output (the final layer's MLP, before it is summed into the residual), and is destroyed by removing that module's own contribution but is *not* reproduced by removing the equivalent linear signal from the full residual stream at any layer, depth, or subspace size we tested.**

## Hypothesis table

| Hypothesis | Evidence for | Evidence against | Verdict |
|---|---|---|---|
| **Implementation bug** | none found | Numerically exact removal at every targeted layer (≈0.000–0.010 residual mean\|projection\|, `intervention_audit.md` §A); effect correctly propagates downstream (values at non-ablated layers change vs baseline); text-level check shows the hook does alter generations (6/32 and 26/32 completions differ verbatim from baseline). One real audit-script bug *was* found and fixed (hook-ordering artifact in the diagnostic script itself), but it never touched the actual C03–C05 causal experiments. | **Ruled out** |
| **Rapid regeneration (single/partial scope only)** | Single-layer removal (L18) recovers to 54% of baseline by the very next layer and exceeds baseline two layers later; 6-layer removal (18–23) recovers to 7.6%→65%→36.5% of baseline by layers 24/26/27 (Figure A). | Full 28-layer removal has *nothing left to regenerate from* (every layer ≈0, Figure A) yet is still null — regeneration cannot explain this case. | **Partially true, not sufficient alone** |
| **Multidimensional policy carrier (linear subspace)** | k=2 gives 6.25pp [0, 15.6], k=4 gives 9.4pp [−6.25, 25.0] — nonzero point estimates | Not monotonic: k=8 drops back to −3.1pp [−9.4, 0] (Figure D); no k up to 8 approaches the 20pp+ magnitude seen for ADD or for the L27-MLP writer; token-locality sweep (5 scopes, all layers 18–23) is flat 0pp regardless of which token positions are touched, so it is not a coverage artifact either. | **Not supported** |
| **Writer redundancy (functional redundancy across m=4 module writers)** | none — no pair/triple/quad shows an effect beyond what L27_mlp alone gives (Figure C) | Every subset lacking L27_mlp is exactly 0pp; every subset containing it is ~18.75–25pp; no synergy pattern (single≈pair≈triple≈quad, ±3pp noise) | **Not supported for this m=4 set** |
| **Backup recruitment** | 4/56 scanned (layer, module) writers show a small increase in \|writer score\| after full ablation | All four increases are small (max 1.6) versus what the strongest original writers lost (10+, 5+); no writer reaches comparable strength (`backup_writer_test.csv`) | **Not supported** |
| **Shared downstream bottleneck** | One writer (L27 mlp_output) is uniquely, reproducibly causal | Residual-level ablation *at that same layer* (which should cut a shared bottleneck at least as effectively) is null (3.1pp [−9.4, 18.75], `residual_removal_L27_only.json`) — direct evidence against a simple shared-residual-projection bottleneck at L27 | **Not supported in the simple form; see shared_gate_diagnostic.md** |
| **Representation is not the (residual-level, linear) decision mechanism** | Every residual-level linear operationalization tested — 1/6/28 layers, k=1/2/4/8 subspace, 5 token-coverage scopes — is null for necessity, despite exact, verified removal | A real, substantial, reproducible module-level causal writer *was* found (L27 mlp_output, 21.9pp, robust across all subsets containing it) — so representation is not *irrelevant*, just not captured by the residual-projection framing | **Best-supported, with the module-level caveat below** |

## PRIMARY_DIAGNOSIS

```text
PRIMARY_DIAGNOSIS = REPRESENTATION_IS_NOT_THE_DECISION_MECHANISM
  (specifically: not at the residual-stream, linear-direction level, at any
   layer, depth, or subspace size tested — full removal of this exact
   signal from the residual stream leaves behavior unchanged)
```

## SECONDARY_EXPLANATION

A genuine, non-redundant, module-level causal writer exists — the last layer's raw MLP output (L27 mlp_output) — whose surgical removal produces a real 21.9pp necessity effect, robust across every writer-subset combination that includes it, and parametrically distinct (near-zero/negative co-sensitivity, `writer_parameter_sensitivity.csv`) from the other three scanned writers that show consistent positive co-sensitivity with each other but no behavioral effect. This writer's effect is **not** reproduced by removing the equivalent linear signal from the full residual at that same layer, which is the single most counterintuitive and important open finding of this round: **partial, module-specific removal (leaving ~70% of the nominal linear signal intact in the final residual) causes more behavior change than complete removal of the same signal (zeroing it exactly)**. This is not one of the 7 preset hypotheses; it points toward a nonlinear, input-regime-dependent mechanism inside the final MLP rather than a linear-direction story at any level tested here, and is the most promising lead for follow-up work (not chased further this round, per scope discipline).

## What this does and does not license

- Does **not** license calling the residual P-direction "the refusal mechanism" — necessity fails everywhere we can cleanly test it at that level.
- Does **not** license a "multiple redundant writers" story for this m=4 candidate set — the data show the opposite (one dominant, non-redundant writer).
- Does license: this benign-proxy methodology chain is sensitive enough to find a real, small, specific, reproducible causal module (not just noise), to correctly rule out a bug, and to detect a genuinely surprising non-monotonic dose-response pattern rather than smoothing it away.
