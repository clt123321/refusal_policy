# SAFE_PROXY_CLOSEOUT

Role: `SAFE_MECH_BENIGN_PROXY`. This closes the benign mechanistic-diagnosis branch. No real harmful data, no safety attacks, no parameter-space attack optimization were used anywhere in this branch.

## 1. Final verdict

**PRIMARY: `POLICY_EFFECT_IS_LOCUS_SPECIFIC`. SECONDARY: `LINEAR_REPRESENTATION_IS_STEERABLE_BUT_NOT_NECESSARY`.** The behavioral effect is real, non-artifactual, dose-graded, and replicates, but it is tied to *which tensor's own current content* is projected and removed (the L27 MLP's raw output specifically) rather than to *where in the computation graph* the subtraction happens (pre- vs post-residual-sum vs pre- vs post-final-norm all behave identically for a fixed displacement) — so the mechanism is best described as a specific, steerable linear lever anchored to one reference vector, not as evidence of decision-critical nonlinear computation inside that module.

## 2. What we actually established

- The 21.9pp single-writer effect (L27 MLP output, previous round) is **not** a hook/cache/generation-implementation artifact: replacing the MLP-hook with an entirely independent mechanism (directly overwriting the decoder-layer's output with the same resulting value) gives logits identical to ~1e-5 and identical top-1/argmax decisions on 8/8 held-out examples (`exact_state_equivalence.json`).
- The effect is **dose-graded and monotonic**, not a threshold artifact: scaling the same MLP-27 removal from α=−2 (extra addition) to α=+2 (2× overshoot removal) moves both the continuous policy logit margin (+0.95 → −1.12) and the discrete abstain rate (100% → 56%) smoothly and monotonically through the α=0 baseline (`l27_dose_response.csv`, Figure Final-A).
- **Normalization does not explain the earlier MLP-vs-residual asymmetry.** Applying the *same fixed displacement* (equal to L27 MLP's own natural projection) at three loci — before the residual sum (MLP output), after the residual sum but before final RMSNorm, and after final RMSNorm — produces essentially identical behavior (62.5% abstain, all three) and near-identical logit margins (`normalization_localization.csv`). Pre- and post-residual-sum loci are in fact algebraically identical for a fixed vector (linearity), which the data confirm exactly.
- Given that finding, the real explanation for "MLP-27-output removal works, full-residual-at-L27 removal does not" (previous round) is that these two operations subtract **different reference quantities** — the MLP's own current projection vs. the full residual's own current projection (which also includes ~upstream, pre-MLP-27 signal) — not that one locus is anatomically or normalization-wise special.
- The effect **replicates** under an independently reshuffled construct-fit/carrier-dev/carrier-test question partition (different seed): 21.9pp [9.4, 37.5], same direction, same magnitude as the original split (`l27_replication.json`).

## 3. What we did NOT establish

- This is **not** evidence about real refusal/safety mechanisms in any deployed model. The task (astronomy/cooking content × explicit answer/abstain instruction) is a synthetic, fully benign structural analog.
- We did **not** establish a common-mode failure: only one candidate writer, at one layer, in one small scanned set, showed this behavior; we did not search exhaustively over all layers/modules for other loci with the same property.
- We did **not** establish anything about parameter-space vulnerability. The only parameter-level work in this branch was a bounded gradient/co-sensitivity diagnostic (previous round), explicitly not an attack, edit, or optimization.
- We did **not** establish, and make no claim about, whether modern aligned models are more or less robust than 2024-era models to any kind of tampering. Nothing here touched a safety-trained model or safety-relevant content.

## 4. Exact-state sanity check

`STATE_EQUIVALENCE_CONFIRMED`. Max logits difference across 8 held-out examples: 1.05e-5. Top-1 token agreement: 8/8. See `exact_state_equivalence.json`.

## 5. Dose-response

`MONOTONIC`. See `l27_dose_response.csv` and Figure Final-A (`figures/figure_final_a_dose_response.png`). Behavior spans a wide, graded range (100%→56% abstain rate) as α goes from −2 to +2; the policy logit margin crosses zero right around α=0, consistent with the margin proxy tracking the actual decision.

## 6. RMSNorm localization

`NORMALIZATION_MEDIATED`: not supported. Pre-sum (A), post-sum-pre-norm (B), and post-norm (C) loci give the same behavioral outcome (62.5% abstain, all three) for the same fixed displacement; A and B are algebraically identical by linearity of the residual sum, and C — genuinely a different, nonlinear-normalized space — still lands at the same behavior and a very close margin (−0.93 vs −0.98). See `normalization_localization.csv`. This directly implies the original MLP-vs-residual asymmetry is about *which vector's own content defines the removed quantity*, not about normalization geometry.

## 7. Replication

Confirmed, same direction and magnitude, independent construct-fit/dev/test partition (shuffle seed 42): 21.875pp [9.375, 37.5] vs. original 21.875pp [9.375, 37.5]. See `l27_replication.json`.

## 8. Implication for main project

This is a **methodology** finding, not a safety finding: a causal-carrier / writer-analysis pipeline of this kind can (a) correctly rule out its own implementation artifacts when it finds a locus-specific effect, (b) correctly detect that a *representation* (the residual-stream linear direction) can be fully steerable and dose-graded for sufficiency while *not* being the necessary substrate the model actually used for a related but distinct decision, and (c) correctly distinguish "the effect depends on where you intervene in the compute graph" (not what happened here — ruled out by the RMSNorm test) from "the effect depends on which reference tensor's own content you use to define the intervention" (what actually happened here). For the main project, the practical lesson is: **necessity testing at the residual-stream level, alone, can systematically under-detect a real causal writer if that writer's own local contribution is smaller than — and not a fixed multiple of — the full residual's own alignment with the same nominal direction.** A construct/writer-cut methodology that only ever ablates "the residual's own projection" (rather than also probing specific module outputs) could report a false necessity-null even when a real, dose-graded, replicable causal writer exists. Representation ≠ computation: the axis is real and steerable; which tensor you read it off of is not interchangeable.

## 9. Closeout status

```text
SAFE_PROXY_CLOSED_USEFUL
```
