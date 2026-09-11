# Shared-Gate Diagnostic

Role: `SAFE_MECH_BENIGN_PROXY`. Actively tried to falsify a shared-gate story rather than assume one.

## Evidence gathered

1. **Full ablation-scope sweep** (`c05_full_depth_necessity.json`, `intervention_audit_layerwise_projection.csv`): residual-level linear-direction removal at 1 layer, 6 layers (18–23), and all 28 layers all show null necessity (0, 0, and −3.1pp respectively), even though the intervention is numerically verified to zero the signal exactly at every targeted layer (see `intervention_audit.md`).
2. **Module writer scan** (`module_writer_scan.csv`): of 8 top candidates (top-4 attention-output, top-4 MLP-output writers by |projection strength| onto their own layer's residual P-direction), exactly one — **L27 mlp_output** — shows a non-null causal effect (21.9pp [9.4, 37.5]) when its raw output is surgically ablated before being added to the residual. The other 7 show exactly 0pp individually.
3. **Exhaustive subset test on m=4** (`writer_subset_removal.csv`, Figure C): every one of the 15 subsets of `{L20_attn, L24_attn, L27_mlp, L26_mlp}` shows ~0pp if it excludes L27_mlp, and ~18.75–25pp if it includes L27_mlp, regardless of what else is combined with it. No pairwise or higher-order synergy among the other three; L27_mlp alone accounts for 21.875/25.0 ≈ 88% of the best achievable effect in this candidate set.
4. **Residual-level ablation at L27 alone** (`residual_removal_L27_only.json`, run as a targeted follow-up once the module-level finding above was seen): 3.1pp [−9.4, 18.75] — null. This uses the *same* direction and the *same* layer as the module-level test above, but removes it from the **full residual** (which fully zeroes the projection at that point) instead of from **only the MLP's own contribution** (which leaves roughly 70% of the original projection magnitude intact, per `backup_writer_test.csv` baseline scores). Full removal at this exact location is null; partial, module-specific removal at the same location is not.
5. **Backup writer test** (`backup_writer_test.csv`): after full 28-layer residual ablation, only 4/56 (layer, module) writer scores increase in magnitude, and all four increases are small (max 1.6) relative to what the top writers (10+, 5+) lost. No writer emerges at comparable strength.
6. **Parameter co-sensitivity** (`writer_parameter_sensitivity.csv`): L20_attn, L24_attn, and L26_mlp show consistent *positive* cosine similarity (0.4–0.6) in their gradients with respect to shared early parameter blocks — a `LOCAL_CO-SENSITIVITY` signature among themselves. L27_mlp's sensitivity to the same blocks is near-zero or weakly negative relative to the other three. L27_mlp looks parametrically distinct from the other three, not part of the same co-sensitive group.

## Classification

**Pattern: none of A/B/C cleanly fits; closest is a qualified `NO_IDENTIFIABLE_GATE`, but not for the reason "the decision is highly nonlinear with no causal writer at all" — a real, reproducible, substantial single writer (L27 mlp_output) was found. The reason no clean gate pattern fits is that this writer's effect is *not* reproducible by removing the equivalent signal at the residual-stream level, at any scope, from 1 layer to all 28 layers.**

Formal answer: **`UNDECIDABLE`**, with the following qualification for anyone extending this work:

- Not `INDEPENDENT_PATHWAYS`: only one of the 8 scanned candidate writers has any individual effect; there is no evidence of multiple independently-sufficient pathways.
- Not `SHARED_BOTTLENECK_SIGNAL` in the classic sense: a shared bottleneck story predicts that diverse upstream writers converge on one downstream chokepoint that *reads the same information they wrote*. Here, residual-level ablation at the alleged chokepoint's own layer (L27) — which should be the most direct way to cut a shared downstream bottleneck — is null. That is evidence *against* a simple downstream residual-projection bottleneck at L27, even though L27's MLP submodule output is clearly doing something causally important.
- Not `NO_IDENTIFIABLE_GATE` in the strong sense ("no writer matters"): one writer clearly and reproducibly matters (point 2–3 above).

The data are most consistent with: the true decision-relevant computation happens *inside* a nonlinear module (L27's MLP), in a way that depends on receiving its *normal, unperturbed* input, and is not well summarized by "how much this fixed linear direction is present in the residual stream at this point." This is a distinct, fourth possibility that the four preset categories do not name.
