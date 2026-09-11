# Intervention Audit

Role: `SAFE_MECH_BENIGN_PROXY`. This audits whether REMOVE actually does what we think, before interpreting the necessity-null result.

## 0. Baseline numbers and transition tables (not just aggregate pp)

From `baseline_transition_tables.json`, computed on the raw per-example labels behind the headline ±25.0pp / 0.0pp numbers (6-layer L18–23 scope):

**REMOVE condition** (n=32, abstain-instructed carrier-test prompts):
- baseline abstain rate: 29/32 = 90.6%; 3/32 already answered despite the instruction.
- after REMOVE: identically 29/32 abstain, 3/32 compliant.
- transitions: `abstain->abstain` = 29, `compliant->compliant` = 3, **`abstain->compliant` = 0, `compliant->abstain` = 0**. This is a hard null: not one individual example changed category, not just a net-zero aggregate.

**ADD condition** (n=32, natural bare-question carrier-test prompts):
- baseline abstain rate: 0/32 = 0% (no reason to decline a bare factual question).
- after ADD: 8/32 = 25.0%.
- transitions: `compliant->abstain` = 8, `compliant->compliant` = 24, **`abstain->compliant` = 0** (none possible, baseline was 0% abstain). All movement is one-directional, matching the 25.0pp headline exactly (8/32).

## A. Numerical removal (fixed a real audit-script bug first)

**Finding: a genuine bug was found and fixed, but it lived in this audit script, not in the C03/C04/C05 generation experiments.**

First attempt at this audit registered a read-only capture hook on every layer (for the layer-wise curve) *and separately* a remove-hook on the ablated layer(s) via the existing `steer_multi_layer` context manager, with the capture hook registered before the remove hook. Because PyTorch calls forward hooks on the same module in registration order and passes the (possibly already-modified) output along the chain, the capture hook fired *first* and snapshotted the pre-removal value, so the ablated layer's own recorded projection looked unchanged from baseline (misleading). Downstream layers were unaffected by this bug, because they only had a single (read-only) hook and their *input* tensor was still correctly the post-removal value produced by the actual forward computation graph — only the bookkeeping at the exact ablated layer was stale.


Fix (`scripts/run_intervention_audit.py`): one hook per layer that performs the removal (if that layer is targeted) and captures the *post*-removal value in the same function, removing any hook-ordering ambiguity.

This bug never affected the actual C03/C04/C05 causal experiments — those scripts only ever registered the steer hook itself during `generate()`, with no competing read-only hook on the same layer. It was isolated to this new diagnostic script and is reported for transparency.

### Corrected numbers (mean |projection| onto that layer's own frozen P-direction, carrier-test abstain-instructed prompts, n=32)

| Scope | At the ablated layer(s) | Immediately downstream |
|---|---|---|
| baseline | n/a | L18=2.57, L19=4.32, L26=55.6, L27=37.0 |
| remove L18 only | L18 = 0.001 (exact) | L19 = 2.33 (54% of baseline), L20 = 6.32 (**above** baseline) |
| remove L18–23 | all six ≈ 0.001–0.004 (exact) | L24 = 1.39 (7.6% of baseline), L26 = 36.2 (65%), L27 = 13.5 (36.5%) |
| remove all 28 layers | every layer ≈ 0.000–0.010 (exact) | — (nothing left downstream to regenerate from) |

**Conclusion for Case A (implementation bug): ruled out.** The removal is numerically exact at every layer we target it at (residual ≈0 along that layer's own direction), and the effect measurably propagates downstream (values at non-ablated layers change, they are not frozen at baseline). The mechanism is doing exactly what a mean-difference ablation is supposed to do.

## B. Token coverage

| Component | Coverage in C03/C04/C05 main experiments |
|---|---|
| Direction *extraction* (C01/C02) | assistant-boundary **final prompt token only** (one vector per example) |
| Direction *application* (REMOVE/ADD in C03/C04/C05) | **every prompt token position, every generated token position, every decode step** — `mask = ones(seq_len)` on every forward call during `generate()` |
| `wrong_token` control (C04) | only the first prompt token, never touched again |

This mismatch — extracted from one position, applied everywhere — is intentional (standard ablation practice) but is exactly why Section 8 below tests whether restricting application to specific token phases changes anything.

## C. Hook location

| Intervention | Hooked module | Position in block |
|---|---|---|
| `steer_layer` / `steer_multi_layer` (C03/C04/C05 main) | `model.model.layers[i]` (whole `Qwen2DecoderLayer`) | residual **post** (after attention-add and MLP-add; this is the layer's total output) |
| Writer atoms (this round, below) | `layer.self_attn` / `layer.mlp` | the **raw module output before the residual add** (i.e., what gets added to the residual, not the residual itself) |

Verified empirically (not just read from code): `self_attn` forward returns a tuple whose first element is `[batch, seq, hidden]`; `mlp` forward returns a bare `[batch, seq, hidden]` tensor; decoder-layer forward output composition was confirmed by the fact that ablating its output changes the *input* seen by the next layer (section A above).

## D. Regeneration

See table in section A. Layer-wise curves are in `intervention_audit_layerwise_projection.csv` (Figure A).

- Single-layer removal (L18): **`RAPID_REGENERATION`** — signal is already partially back one layer downstream (54% of baseline at L19) and *exceeds* baseline two layers downstream (L20).
- Six-layer removal (L18–23): **partial regeneration, not full** — L24 retains only ~7.6% of baseline, climbing back to ~65% by L26, ~36.5% by L27. Some but not complete recovery.
- Full 28-layer removal: **no downstream left to regenerate from** — every layer is ≈0, by construction. Necessity is still null here. This is the single most important audit fact: it is **not possible** to explain the full-depth necessity-null result as "regeneration masked the intervention," because there is nothing left to regenerate — the linear P-signal is exactly zero everywhere in the residual stream, at every layer, at the position we measure it, and behavior is unchanged anyway.

**This rules out the two cheapest explanations (bug, pure regeneration-at-partial-scope) as the *full* story**, and shifts weight toward: the true decision mechanism is not fully captured by (a) this single mean-difference direction, (b) at this one token position, or (c) in the residual stream at all (vs. attention/MLP module-internal computation). Sections 3, 7, and 8 test these directly.
