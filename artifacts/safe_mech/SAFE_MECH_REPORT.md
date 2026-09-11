# SAFE_MECH_REPORT

Role: `SAFE_MECH_BENIGN_PROXY`. This report validates the C01–C05 causal-carrier / writer-analysis methodology on a fully harmless, structurally analogous policy task. It contains **no real harmful prompts, no harmful-compliance scoring, no safety-mechanism removal, and no fine-tuning**. Results say nothing about real safety alignment; they only say whether this measurement pipeline works, and what it finds on this specific benign task.

## Status

**SAFE_MECH_WEAK**

Construct validity is strong (clean H/P separation, near-zero leakage, good bootstrap/leave-one-family-out stability). The causal battery is **asymmetric**: sufficiency (ADD) shows a robust, control-differentiated effect; necessity (REMOVE) is a robust null even under maximal intervention scope (all 28 layers). This does not meet the PASS bar ("add/remove 有方向一致 causal effect"), but it is clearly not FAIL either — the main intervention is far from indistinguishable from controls on the axis where it has any effect at all (sufficiency), and the null on necessity is itself informative (see Shared gate).

## Model

- `Qwen/Qwen2.5-1.5B-Instruct`, snapshot `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`
- 28 layers, hidden size 1536, fp16, single A800 GPU
- Frozen as `SAFE_MECH_MODEL` in `configs/feasibility/safe_mech_model.json` (distinct from, and not a substitute for, the still-pending TODO P04 capability-qualified aligned-checkpoint decision)

## Task

Fully benign 2×2 H×P design, `src/data/safe_mech.py`:

- H (content): astronomy vs cooking, 48 factual/how-to questions per topic, split 16/16/16 into construct-fit / carrier-dev / carrier-test with no question reused across splits.
- P (policy): explicit "answer" vs "abstain" instruction wrapped around the same question, 4 wording families per policy (for leave-one-family-out).
- A third "natural" arm (bare question, no policy instruction) is used only for the ADD/sufficiency test, since there is no organic reason for the model to decline a bare astronomy/cooking question.
- One engineering fix was made before any confirmatory run: the first ABSTAIN_TEMPLATES wording only reliably elicited decline behavior in 1/4 families (smoke-tested on 3 questions); templates were rewritten to a more directive phrasing (verified 3/4 families reliable) and C01–C05 below all use the corrected templates. This is the one permitted pre-registration-equivalent repair; no further template tuning was done after seeing causal results.

## Representation (C01–C02)

Full-layer scan: `safe_hxp_layer_scan.csv`, Figure S1.

- P separation (dev, standardized effect size) rises from ~1.4–3 in early/mid layers to a plateau of ~5.8–6.5 around layers 17–26, then drops at layer 27.
- H leakage onto the P direction stays within ±0.35 across all 28 layers (near zero for the selected candidates) — P and H are cleanly separable throughout.
- Candidate layers (selection rule: top-4 by `|dev P separation| − |dev H leakage|`, construct-fit + carrier-dev only): **18, 17, 23, 19**.

| Layer | Dev P separation | Dev H leakage | Bootstrap mean cosine | Bootstrap ≥0.8 frac | Leave-one-family-out mean/min cosine |
|---|---:|---:|---:|---:|---:|
| 18 (primary) | 6.52 | −0.016 | 0.85 | 0.885 | 0.95 / 0.92 |
| 17 | 6.43 | −0.127 | 0.84 | 0.805 | 0.95 / 0.92 |
| 23 | 6.26 | 0.117 | 0.92 | 1.00 | 0.94 / 0.91 |
| 19 | 6.36 | 0.263 | 0.88 | 0.98 | 0.94 / 0.90 |

Layer 18 was frozen as the primary candidate before any carrier-test data was examined (`safe_candidate_carriers.json`).

## Causal evidence (C03)

All effects are on carrier-test, held out from candidate selection. "Necessity" = increase in compliant (non-abstain) rate when REMOVE is applied to abstain-instructed prompts; "sufficiency" = increase in abstain rate when ADD is applied to natural (uninstructed) prompts; both vs. their own no-intervention baseline, paired cluster bootstrap, 95% CI.

| Intervention | Scope | Effect | 95% CI | n |
|---|---|---:|---:|---:|
| Remove (necessity) | 1 layer (L18) | 0.0 pp | [0.0, 0.0] | 32 |
| Remove (necessity) | 6 layers (L18–23) | 0.0 pp | [0.0, 0.0] | 32 |
| Remove (necessity) | 28 layers (all) | −3.1 pp | [−15.6, 6.3] | 32 |
| Add (sufficiency) | 6 layers (L18–23) | **25.0 pp** | **[12.5, 40.6]** | 32 |
| Rescue | remove(L18–23) + patch(L26) | not interpretable | — | 32 |

- Baseline abstain-rate on abstain-instructed prompts: 90.6% [81.3, 100].
- Baseline on-topic answer rate: 75.0% (instructed-answer prompts), 87.5% (natural prompts) — the rule-based topic-keyword classifier under-counts some valid on-topic answers; this affects the descriptive on-topic rate, not the abstain/compliant binary used for necessity/sufficiency.
- Rescue is not interpretable because REMOVE produced no degradation to rescue from (remove_abstain_rate = baseline_abstain_rate = 90.6%); rescue_abstain_rate (93.75%) cannot be attributed to patching.
- Text-level check (not just label-level) confirms the hook is active: 6/32 REMOVE completions and 26/32 ADD completions differ verbatim from their baseline counterparts, so the necessity null is a real null, not a non-firing hook.

## Negative controls (C04)

`safe_negative_controls.csv`, Figure S2. Same layers (18–23), same norm-matching (unit direction × that layer's own raw P-contrast norm), same evaluation as the main intervention.

| Control | Necessity pp [CI] | Sufficiency pp [CI] |
|---|---|---|
| **main** | 0.0 [0.0, 0.0] | **25.0 [12.5, 40.6]** |
| random_norm_matched | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| orthogonal | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| h_content_direction | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| shuffled_label | 6.25 [0.0, 15.6] | 0.0 [0.0, 0.0] |
| wrong_layer | −3.1 [−9.4, 0.0] | 0.0 [0.0, 0.0] |
| wrong_token | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |

On the axis where main has any effect (sufficiency), all six controls are exactly flat while main is 25 pp with a CI that excludes zero — a clean specificity result. On necessity, main and all controls are statistically indistinguishable from zero (main isn't special there, but neither is any control — this is a shared null, not main losing to a control).

## Writer evidence (C05)

- Ablation-scope sweep (Figure S3): necessity stays at/near 0 pp whether removing 1 layer, 6 layers, or **all 28 layers** of the model (−3.1 pp, CI crosses zero even at full depth). Broader removal does not rescue necessity.
- Module-level (attention-output vs MLP-output) writer atoms and the pairwise/backup-rediscovery grid from the original plan were **not run** — time budget was spent on the scope sweep and the shared-gate sentinel below, which were judged more directly informative given the necessity null. Flagged as a recommended follow-up, not fabricated.

## Shared gate (C05)

`c05_shared_gate_sentinel.json`, Figure S4. A late-layer (L27) residual P-direction, fit only from construct-fit and never touched by the ablation, is used as a downstream sentinel.

- Baseline sentinel separation (abstain vs answer, carrier-test): effect size 2.95.
- After removing the P-direction at layers 18–23 (the same ablation that produced a null necessity effect): sentinel separation drops to 0.83 — a **72% reduction** (retention fraction 0.28).

Interpretation: ablating layers 18–23 does substantially damage the linear P-signal measurable downstream, so the intervention is not inert. Yet this large representational disruption produces **no behavioral change**. The evidence favors "the instructed-abstain decision is not bottlenecked on this single linear direction at these layers" over "the direction has no causal role at all" (which the sufficiency result already rules out). Given the tools run here, this is **undecided between two explanations**: (a) genuinely redundant/overdetermined pathways (multiple mechanisms independently sufficient to produce the instructed decision), or (b) the true causal driver is a higher-rank/nonlinear feature of which our mean-difference direction captures only a correlated slice. Distinguishing (a) from (b) needs the module-level writer grid that was not run this round.

## Methodological conclusion

The C01→C05 pipeline (controlled H×P assay, layer scan, candidate extraction with bootstrap/leave-one-family-out, generation-time causal add/remove/rescue, matched negative controls, scope sweep, downstream sentinel) **runs correctly end-to-end and is sensitive enough to detect a real, nuanced causal asymmetry** (clean sufficiency, robust necessity null, partial representational disruption without behavioral change) on this benign task. It also correctly produced clean nulls across all six negative controls on the axis where main had no effect, and a clean positive-vs-null separation on the axis where main did — i.e., the statistics and control battery behave as designed rather than rubber-stamping every intervention as "significant."

This says nothing about whether real refusal-policy mechanisms are similarly overdetermined; it only shows that *if* such an asymmetry exists, this measurement pipeline would detect it rather than average it away or silently fail.

## Engineering notes

- One dataset fix (abstain-template wording) made before any causal run; documented above, not repeated afterward.
- Single-layer ablation was extended to multi-layer ablation using each layer's own fitted direction, matching standard directional-ablation practice (a single-layer implementation is a known-weaker special case, not a separate "failed" method).
- Rule-based policy/topic classifier (`src/eval/policy_classifier.py`) is a transparent keyword heuristic, not a trained judge; it is adequate for the abstain-vs-compliant binary used in all effect sizes, but under-counts on-topic answers by roughly 12–25% (visible in baseline on-topic rates below 90% despite qualitatively correct answers on manual inspection of `raw_completions*.jsonl`).
- No raw generation is withheld from this report's underlying artifacts: all completions in this task are benign (astronomy/cooking Q&A or polite declines) and are kept in `raw_completions*.jsonl` for auditability.

## Artifacts

- `safe_mech_assay.jsonl`, `safe_hxp_layer_scan.csv`, `safe_candidate_carriers.json`
- `causal_policy_intervention.json/csv` (1-layer), `causal_policy_intervention_multilayer.json/csv` (6-layer)
- `safe_negative_controls.json/csv`
- `c05_full_depth_necessity.json`, `c05_shared_gate_sentinel.json`
- `raw_completions.jsonl`, `raw_completions_multilayer.jsonl`, `raw_completions_controls.jsonl`, `raw_completions_full_depth.jsonl`
- `figures/figure_s1_layer_hxp.png`, `figure_s2_causal_vs_controls.png`, `figure_s3_writer_scope.png`, `figure_s4_shared_gate.png`
