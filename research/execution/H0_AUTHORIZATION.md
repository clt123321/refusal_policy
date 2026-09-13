# H0 — Authorized Execution Path

**Status:** AUTHORIZED (granted 2026-09-13 by project owner)
**Scope:** frozen V5 replication/harness scope — Phase 1 harness implementation (H1–H7) and Phase 2 replication chain (R0a → R0b → R1/R2/R3), using the frozen V4 harness specification, evaluator definitions, cost accounting and restricted-artifact path. Phase 3+ mechanism screening and all novel-defense/attack-readiness work remain **outside** this authorization and require a separate HARNESS_VALIDATED gate.

## 1. Authorization record

- **Authorizer:** project owner (human decision, stated in the H0 grant message).
- **Authorized executor:** project owner / designated research executor.
- **Boundary:** this agents' role is machine-actionable preparation, harness implementation, deterministic smoke tests, lineage/cost/governance bookkeeping and replication plumbing. Execution of harmful-task evaluation (AHC-type scoring, raw harmful generation) is performed by the authorized executor, not by the research agent, per the H0 rule: *"If an agent cannot execute a required evaluation, hand off to the authorized executor; do not substitute a safe proxy."*
- **Not authorized:** R0a may not start until H0–H7 all pass; Phase 3 mechanism screening may not start until `HARNESS_VALIDATED`; no novel defense training; no 32-checkpoint panel; no large GPU matrix.

## 2. Agent → authorized-executor handoff procedure

For every scientific gate that requires harmful-task evaluation or raw harmful generation:

1. Agent prepares the frozen manifest: prompt IDs, model/revision hashes, generation config, evaluator config, cost ledger schema and output card template, all machine-readable under `research/protocols/V4_PROTOCOL_SCHEMA.json` / `V4_RESULT_SCHEMA.json`.
2. Agent hands the manifest to the authorized executor with the exact command and expected artifact set.
3. Executor runs the evaluation under the restricted-artifact path (below) and returns only aggregate/minimal per-sample fields plus content hashes; raw harmful generations stay in the restricted store.
4. Agent records the returned results in the frozen result card, validates schema, and updates gate status — without having accessed raw harmful outputs.

## 3. Raw-output access / retention policy

- Raw harmful generations are **research artifacts only**, stored only in the approved restricted store (`artifacts/restricted/`, outside git; access-controlled at OS level).
- They are exposed only to authorized evaluators/reviewers; never committed to git; never posted to corp relays, GitHub, or any public transport path.
- Ordinary result artifacts contain only minimum aggregate/per-sample fields allowed by the approved handling protocol.
- Retention: keep through publication review; destroy or archive per project-owner instruction afterward.

## 4. End-to-end dry-run receipt

A formal (benign-content) end-to-end pipeline dry run was executed as part of H0/H1 to validate the harness plumbing:

- **Run:** `harness_dry_run` (see `artifacts/harness/dry_run/`)
- **What ran:** environment lock capture → model adapter load (small public cached model) on benign prompts → deterministic generation check → utility smoke → cost ledger (FLOPs/accelerator-seconds/tokens/trials/peak memory) → artifact store (content-addressed) → run manifest validated against `V4_PROTOCOL_SCHEMA.json`.
- **Content:** fully benign prompts only; no harmful task, no raw harmful generation, no safety mechanism modification.
- **Status:** PASS (receipt in `artifacts/harness/dry_run/DRY_RUN_RECEIPT.json` plus manifest row in `research/execution/`).
- **Purpose:** demonstrates the formal execution path (manifest → execute → record → store → validate) without crossing the harmful-content boundary; it is not a scientific result and proves nothing about the research question.

## 5. Escalation rule

If any gate requires handling disallowed outputs or an unapproved protocol substitution, the agent marks the gate `BLOCKED` (not failed, not silently passed) and escalates to the authorized executor. No safety gate becomes `DECLINED_BY_AGENT_POLICY`; it is `BLOCKED` and handed off per section 2.
