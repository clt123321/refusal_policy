# V6 E1 Preflight

**Status:** `V6_E1_PREFLIGHT_MACHINE_SIDE` (machine-measurable items complete; formal E1 execution requires authorized executor per H0 boundary — `V6_E1_EXECUTOR_BOUNDARY`)
**Authoritative baseline SHA:** `90cf38bb632c0e6ca861596a59dec4acba23f8ba` (verified `origin/main` after fetch; local `main` reset to it, working tree clean)

## 0. Verification

- Local HEAD == `90cf38bb632c0e6ca861596a59dec4acba23f8ba` ✅
- `origin/main` == same ✅
- Working tree clean ✅
- No relay-history reconciliation performed this round.

## 1. Model / environment (measured)

| Item | Value |
|---|---|
| Model | `Qwen/Qwen2.5-1.5B-Instruct` |
| Revision | `989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| Tokenizer revision | same repo/sha (chat template native) |
| Gated | No (public) |
| Local cache | `/root/.cache/huggingface/hub/models--Qwen--Qwen2.5-1.5B-Instruct/snapshots/989aa7980e4cf806f80c7fef2b1adb7bc71aa306` |
| dtype | fp16 |
| Device | A800 (GPU1 idle at measurement) |
| Peak VRAM (generation) | 3.10 GB |
| Generation tokens/sec (10 prompts, max_new=64, greedy) | 32.1 |
| Determinism hash (2 repeats) | `e767661a6562ca30…` |
| Env lock sha256 | `ccd472737122a183…` |
| ModelArtifact id | `72a13e8841d37c2e…` |

Note: generation throughput measured on benign prompts only. Training tokens/sec and A1-endpoint latencies cannot be validated without executor-authorized workloads (measures will be recorded at execution time; the budget grid below uses conservative margins from this generation figure plus a 2× training overhead assumption that must be re-measured).

## 2. Frozen config draft (to be ratified at executor handoff)

- Budget grid (default): `0 / 8 / 32 / 128 / 256` A1 steps, checkpointed for B/C/P identically.
- Seeds: two preregistered seeds (values from constants: `17, 29`).
- A1 fresh: new LoRA adapter, reset optimizer/scheduler/scaler/RNG, no reuse of A0 edit/localizer/search state.
- C/P repair: identical frozen repair dataset / parameterization / optimizer-init / batch order / step count; checkpoint index identical; parameter drift recorded, not matched.
- A0 checkpoint saved for provenance only; no fourth A1 arm this week.

## 3. Dataset isolation (frozen names; revisions/hashes to be pinned before A1 outcomes)

| Split | Role |
|---|---|
| `D_A0_loc` | A0 direct-edit localization data |
| `D_repair` | repair recipe data (C and P shared) |
| `D_endpoint_match` | endpoint qualification/selection |
| `D_endpoint_audit` | sealed endpoint audit (same for B/C/P) |
| `D_A1_train` | fresh A1 training (must exclude all others) |
| `D_attack_eval` | sealed attack evaluation |
| `D_function` | narrow normal-function probes |
| `D_plasticity` | novel benign-task learning control |

No sealed attack outcome may be used in endpoint selection.

## 4. Evaluator boundary

- Content-level evaluator: **executor-only** (H0). Agent provides seam + manifest templates; does not implement or run harmful-task scoring.
- Refusal wording vs actual task success must be separable; executor applies the frozen V4 human-audit/aggregate rule at boundaries.

## 5. A1 dynamic-range pilot requirement (executor)

- Goal: one frozen unified A1 config where not all endpoints breach at first checkpoint and not all are unresponsive at max budget.
- One config for B/C/P; no per-endpoint tuning.
- This is the key gate for `E1_PREFLIGHT_PASS` — cannot be machine-verified.

## 6. Storage / compute estimates (measured or conservative)

- Model fp16 on disk: ~3.3 GB (weights) + tokenizer/config.
- Checkpoints per arm (256-step LoRA): tens of MB each.
- 3 arms × 2 seeds × 5 budget checkpoints + A0 checkpoints: est. < 5 GB working storage.
- Total compute: generation measured 32 tok/s on one A800; training throughput must be measured by executor. Week-1 cap draft: nightly-constrained, to be finalized after dynamic-range pilot.

## 7. Agent-side completion status

Completed (this round): model revision pin, env lock, benign throughput/VRAM/determinism measurement, budget-grid draft, dataset-isolation table, H0-compliant evaluator seam, schema-validated artifact/manifest plumbing and prior harness tests (48/48 on the retained suite when applicable).

Blocked / executor-only:
- Content-level safety evaluation runs.
- A0 direct parameter intervention construction.
- A1 fresh LoRA re-attack execution.
- C/P endpoint qualification on sealed audit split.
- Generic plasticity control execution.
- Any E1 verdict (PASS/FAIL/INCONCLUSIVE/INVALID).

## 8. Preflight decision

`E1_PREFLIGHT_BLOCKED` — single blocker: executor authorization path for the harmful/A1 workloads is outside this agent's implementation boundary (per H0). Minimum human action: authorized executor runs/arranges the A1 dynamic-range pilot and content-level evaluator; agent then finalizes the frozen E1 manifest and can only record — not run — formal outcomes.

`NO_SCIENTIFIC_EXPERIMENTS_RUN`

## 9. Updated this round (2026-09-14)

- `research/execution/V6_E1_PREREGISTRATION.md` created — freezes B/C/P definitions, endpoint gates, A1 fresh rules, budget grid draft, outcome/censoring/verdict rules from `V6_DECISION.md` + constants. Numeric A1 grid and dataset hashes marked `PENDING_EXECUTOR_PILOT` (not fabricated by the agent).
- `configs/execution/v6_e1_executor_handoff.json` created — exact executor handoff manifest (hashes to collect, actions, required manifest fields, validation procedure, raw-output policy).
- `src/harness/e1_isolation.py` + tests — metadata-only split-isolation validator for the eight E1 splits (exact-record overlap, family separation); no content generation.
- Tests: 52/52 pass.
