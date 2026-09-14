# R0a — Faithful Arditi Reproduction Manifest

Status: **PREPARATION** (R0a itself remains `BLOCKED by H0–H7`; this manifest prepares immediate execution once H-gates pass and official artifacts are available).
External-info note: GitHub (web and git) and arXiv are unreachable from the KML IDC segment at preparation time; every cell whose ground truth requires consulting an external page is marked `EXTERNAL_VERIFY` and must be confirmed against the official repository/paper before running. Unknowns are not assumed.

## 1. Target protocol (frozen protocol cells)

| Item | Value | Source | Verify status |
|---|---|---|---|
| Official repo | `github.com/andyrdt/refusal_direction` | R0a task text | `EXTERNAL_VERIFY` (need exact commit SHA) |
| Target model(s) for canonical cell | reported models from Arditi et al. (2024); **Gemma-2-2B / Qwen3-4B and Fail-Closed pair are the V5 cells, not necessarily the canonical cell** | V5 TODO / constants | split literal vs local use |
| Direction construction | `harmful_minus_harmless_difference_in_means` | `V4_PREREGISTERED_CONSTANTS.json` `r0_direction` | local frozen |
| Hook position | `post_transformer_block_residual` | constants | local frozen |
| Token position | `last_non_padding_prompt_token` | constants | local frozen |
| Selection rule | `argmax_score_with_lowest_layer_index_tie_break`; selection on `mechanism_dev` only | constants | local frozen |
| Selection score | `l2_norm(mean_diff) / sqrt(pooled_diag_variance + 1e-6)` | constants | local frozen |
| Interventions | add / remove / patch-rescue; directional weight orthogonalization | V4 threat model A0/A1 + TODO R0a | local frozen |
| Generation | `do_sample=false, temperature=0.0, top_p=1.0, max_new_tokens=256` | constants `generation` | local frozen |
| Evaluator | sealed harmful-task success (ASR), StrongREJECT/MMLU-Pro for R3 | V4 constants / R3 | local frozen |
| Expected published result | qualitative causal signs for direction addition (refusal ↑), removal (refusal ↓ / compliance ↑), weight orthogonalization (refusal removal) | R0a pass criteria; exact table/figure TBD | `EXTERNAL_VERIFY` |

## 2. Deviation table (pre-registered, `unknown` never auto-filled)

| Item | Official | Local planned | Exact match? | Reason / action |
|---|---|---|---|---|
| Direction extraction dataset | `EXTERNAL_VERIFY` (Arditi used harmful/harmless prompt sets) | 200 salted-hash HarmBench validation IDs (R0b cell) / mechanism-dev split | TBD once official dataset confirmed | R0b uses HarmBench per frozen cell; R0a must use author dataset if available |
| Model | `EXTERNAL_VERIFY` (paper models) | listed V5 cells | TBD | canonical cell ≠ V5 transfer cell; record both |
| Tokenizer/chat template | `EXTERNAL_VERIFY` | model-native chat template (`use_model_chat_template=true`) | TBD | verify official template used |
| Candidate selection | `EXTERNAL_VERIFY` (paper reports a specific layer) | deterministic argmax rule on mechanism_dev | TBD | if official layer differs, record as planned deviation before outcome inspection |
| Weight matrices edited | `EXTERNAL_VERIFY` | all regex-matched residual-writing matrices (`a1_directional_edit.eligible_module_regex`) | TBD | constrains to known V4 cell |
| Evaluator | `EXTERNAL_VERIFY` | sealed V4 evaluator | TBD | R0a result must be stated against exact author table/estimator |

## 3. Runner engineering status

- Deterministic runner skeleton: interface complete (`ModelAdapter`, intervention math unit tests, artifact store, manifest, cost ledger; `tests/test_v4_intervention_math.py`).
- Scope: `ENGINEERING_VALIDATED` only (pure math + benign fixtures 38/38 tests pass). Not `R0A_PASS`.
- Remaining for actual R0a: licensed/harmful-data eval path (authorized executor), official repo/data pinning, sealed evaluator run, human audit at boundary.

## 4. Stop rules

- No direction extraction, add/remove, or weight edit on real models until H0–H7 pass and executor is in place.
- Unknown official detail → `EXTERNAL_VERIFY`, never silently assumed.
