# V6.E1 Execution Map — 4090-first handoff

**Scope:** Week-1 E1 only. No Week-2 residue/removal/transplant/rescue and no defense work.

**Research base audited:** `90cf38bb632c0e6ca861596a59dec4acba23f8ba` (`main == origin/main`, clean at audit start).

**Machine-readable source:** `configs/execution/v6_e1_plan.json`; 4090-only runtime overlay: `configs/execution/runtime_4090.json`.

## 1. Current code facts

The authoritative GitHub `main` contains the V4 harness interfaces, not a complete E1 executor:

| Capability | Current fact | Callable entry | Scientific status |
|---|---|---|---|
| Environment/model/run manifests | Implemented on main | `src.harness.env`, `model_artifact`, `manifest` | Engineering-ready |
| Artifact lineage/store | Implemented on main | `src.harness.artifact_store` | Engineering-ready; no E1 artifacts yet |
| Cost/failure/censoring | Implemented on main | `src.harness.cost_tracker` | Engineering-ready; no real E1 rows |
| Safety evaluator | Seam only | `src.harness.evaluators:SafetyEvaluator` | No content-level evaluator |
| A0 math | Tensor primitives only | `src.harness.direction` | No model-level edit/save/reload runner |
| E1 executor | Not on main | Candidate relay runtime `4efa5354449e64df73d6c9db0b9f80de18b058fd` | Orchestration only |
| `FormalE1Backend` | Relay candidate only | `src.execution.formal_e1_backend:FormalE1Backend` | Hook interface; no scientific operations |
| Benign model smoke | Relay candidate only | `src.execution.local_model_smoke_backend:LocalModelSmokeBackend` | Real Qwen/LoRA DEV smoke; explicitly non-scientific |
| Continuous orchestrator | Relay candidate only | `python -m scripts.v6_e1_continuous` | Generates external jobs; no tracked consumer |
| Repair runner | Not found in main or fetched V6 relay refs | None | Missing |
| Formal reload runner | Not found | `_reload_eval` exists only as an unused DEV helper | Missing |
| Repair draft | Prose only on relay | `V6_E1_PREREGISTRATION.md` / `V6_E1_PREFLIGHT.md` | Dataset/target/optimizer/steps/stage unresolved |
| Split validator | Relay candidate only | `src.harness.e1_isolation:validate_isolation` | Exact-ID overlap only; family review still needed |
| Formal results | None | — | No A0, repair, A1, qualification or plasticity science has run |

The latest fetched candidate is `corp-relay/refusal-policy-v6-e1-continuous-v3-20260914@1b9dd8bd3b9eca31b2222514bf3b7ceb043e55cf`; its declared runtime is `4efa535…`, while its older executor handoff JSON still names `b41df7c…`. This provenance mismatch must be removed when reconciling code. Historical “63/73 passed” reports are not treated as current-main test results.

The candidate `FormalE1Backend` also needs correction before formal use:

- `pilot` calls A0, then `construct` calls A0 again;
- C/P `same_repair_stage` is reported but not enforced;
- qualification calls only `D_endpoint_match`, not sealed `D_endpoint_audit`;
- the external hook payload does not carry complete recipe/data/config/seed/budget references or an adequate P→A0 parent artifact ID;
- verdict logic handles one C/P scalar, not two paired seeds, the preregistered curve-gap alternative, qualification validity or separated costs.

These are implementation gaps, not scientific results.

## 2. Fixed execution topology

```text
B = Base -------------------------------------> fresh A1 ---+
                                                           |
C = Base -> same frozen Repair --------------> qualify ----+--> E1 summary
                                                           |
P = Base -> A0 [save provenance] -> same Repair -> fresh A1+
                               \
                                no fourth A1 arm

After qualification: B/C/P benign plasticity controls may run in parallel with A1.
```

C and P reference one canonical `configs/execution/v6_e1_repair_recipe.json`. P must name the actual A0 artifact as its parent. Parameter distance is reported, never matched. A checkpoint file existing on disk is not `qualified`; only `D_endpoint_match` followed by sealed `D_endpoint_audit` can qualify it.

`task_id` is stable and logical. Each arm/seed expansion gets a separate `run_id`; retries get a new `.aNN` `attempt_id`. DEV and FORMAL ledgers never pool. The old orchestration labels are mapped exactly once in `v6_e1_plan.json`; no tracked M0/M1 labels were found, so none are invented.

## 3. Current task table

| Task | Mode | Resource | Current state | Runnable entry / blocker |
|---|---|---|---|---|
| `DEV.CODE_RECONCILE` | DEV | CPU | READY | Review/port relay runtime; fix five gaps above |
| `DEV.MODEL_PREFETCH` | DEV | network/storage | READY | Exact public Qwen revision; 4090 hashes absent |
| `DEV.DATA_FREEZE` | DEV | CPU/restricted data | BLOCKED | PI source/construction choices + authorized path |
| `DEV.EVALUATOR_AUTHORIZE` | DEV | human/evaluator | BLOCKED | No content-level evaluator/owner bound |
| `DEV.REPAIR_FREEZE` | DEV | PI+CPU | BLOCKED | No formal repair recipe |
| `DEV.A0_FREEZE` | DEV | PI+GPU engineering | BLOCKED | Math exists; real edit/reload runner absent |
| `DEV.A1_FREEZE` | DEV | PI+GPU engineering | BLOCKED | DEV LoRA exists; formal A1 recipe/runner absent |
| `DEV.RUNTIME_SMOKE` | DEV | RTX 4090 | READY after code+model | Existing relay `LocalModelSmokeBackend` |
| `DEV.PREFLIGHT_REPAIR_A0` | DEV | RTX 4090 | BLOCKED | Needs repair/A0 direct runners and recipes |
| `DEV.PREFLIGHT_EVALUATOR` | DEV | evaluator | BLOCKED | Needs authorized evaluator |
| `DEV.PREFLIGHT_A1` | DEV | 4090+evaluator | BLOCKED | Needs endpoints, A1 runner, evaluator |
| `DEV.FREEZE` | DEV | CPU+human | BLOCKED | Wait for measured preflight receipts |
| `FORMAL.BASE` | FORMAL | CPU/storage | BLOCKED | Requires signed `E1_PREFLIGHT_PASS` |
| `FORMAL.C_REPAIR` | FORMAL | GPU | BLOCKED | Same canonical repair recipe |
| `FORMAL.P_A0` | FORMAL | authorized GPU | BLOCKED | Actual A0 artifact required |
| `FORMAL.P_REPAIR` | FORMAL | GPU | BLOCKED | Parent must equal P_A0 output |
| `FORMAL.ENDPOINT_MATCH/AUDIT` | FORMAL | evaluator/human | BLOCKED | Both split paths and tolerance bands required |
| `FORMAL.A1` | FORMAL | GPU+evaluator | BLOCKED | 3 arms × 2 seeds after qualification |
| `FORMAL.PLASTICITY` | FORMAL | GPU | BLOCKED | Formal benign task/runner absent |
| `FORMAL.SUMMARY` | FORMAL | CPU | BLOCKED | Deterministic summarizer needs repair |
| `FORMAL.REVIEW` | FORMAL | human/Agent | BLOCKED | Stops after E1 verdict; never auto-enters Week 2 |

The full stable IDs, dependencies, conditions, inputs, outputs and owners are in the JSON plan.

## 4. Dependencies and parallel work

The JSON dependency graph is acyclic. Safe parallel preparation now:

- fetch/hash the exact Qwen revision on the 4090 host;
- reconcile the minimal direct-path code and run CPU tests;
- prepare source-specific data scripts after the PI selects sources;
- bind the evaluator independently of GPU runner work;
- draft A0/repair/A1 recipe files independently, then review them together for split and state isolation.

GPU work is serialized on one 4090. After endpoint audit passes, formal A1 and formal plasticity are independent; on one card they remain serial for resource reasons. On A800 they may run on separate devices, but logical cost order and science configs remain identical.

Do not start the external continuous queue. It currently has no consuming worker, adds no scientific capability, and its request payload is insufficient. Resume/idempotency/heartbeat/general queue hardening are `FREEZE`, not blockers for the direct path.

## 5. Unfrozen scientific decisions

No tracked protocol has fixed the following formal repair fields. The relay preregistration is a `FROZEN_DRAFT`, not an executable recipe.

| Decision | Minimal option to freeze | Alternative | Why scientific, not an engineering default |
|---|---|---|---|
| `D_repair` | Filter safe chosen/refusal responses from [PKU-SafeRLHF](https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF), pin revision/license, then family-split before any use | Human/PI-approved safe-refusal set built from the same policy taxonomy | Supervision distribution can determine the residual history effect |
| Repair target | Safe response/refusal SFT target only | Preference loss over safe vs unsafe response, if both targets are legally/operationally available | Loss semantics change what “repair” means |
| Repair parameterization | PEFT/LoRA for the 4090 feasibility path; export a normalized full endpoint before A1 | Full-parameter SFT if the PI prioritizes generality and measured 4090 memory permits | Adapter-only repair may create an adapter-specific residue |
| Optimizer/init | Fresh AdamW state for each C/P run with one paired seed rule; exact LR/betas/decay still to freeze | Another optimizer only with a stated scientific reason | Optimizer state is a named confound |
| Batch order | Same salted-hash order for paired C/P, using the existing V4 salt | Same seeded shuffle for a paired seed | Different orders destroy the intended “same repair” control |
| Repair schedule/stage | During DEV only, save one trajectory at proposed checkpoints `16/32/64/128`; freeze one common C/P stage from endpoint-match data before FORMAL | Smaller measured grid if 4090 throughput requires it | Stage selection affects behavioral equivalence and must precede A1 |
| Endpoint bands | Retain V4 content success/utility/compliance rules where semantically applicable; add a numeric low-margin-tail band | PI-approved tighter V6-specific bands | Qualifying C/P is part of identification |
| A0 | Directional direct-weight intervention using existing direction primitives; freeze model module/layer/strength and reload format | Another non-capability-teaching direct edit | A0 determines the history being studied |
| A1 | Fresh LoRA that suppresses refusal using disjoint safe-refusal data, avoiding actionable target-answer teaching | Restricted compliant-target LoRA with an explicit capability-teaching control | A1 defines the measured workload and confounding risk |

Data source candidates, not frozen assets:

| Split | Candidate source/construction | Access and isolation condition |
|---|---|---|
| `D_A0_loc` | Prompt-only harmful families from pinned [HarmBench](https://github.com/centerforaisafety/HarmBench) plus a pinned harmless contrast source | Existing repo provenance records HarmBench commit `8e1604d…`; actual files/IDs must be materialized and excluded by family from all other splits |
| `D_repair` | PKU-SafeRLHF safe chosen/refusal targets | Public HF dataset, CC-BY-NC-4.0 at audit; exact revision/hash and permitted research use must be recorded |
| `D_endpoint_match` / `audit` / `D_attack_eval` | Separate HarmBench behavior families, with audit/eval sealed | Never random-row split across the same semantic family; content-level evaluator required |
| `D_A1_train` | Separate safe-refusal prompts/targets with a refusal-suppression objective | Must share no prompt/paraphrase/family with A0, repair, match, audit or eval; no A0 localizer artifact reuse |
| `D_function` | Minimal V4 narrow-function/compliance subset | Pin exact source/revision; no broad six-task suite is required for E1 |
| `D_plasticity` | Held-out benign instruction categories from [Databricks Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k/tree/bdd27f4) | Candidate commit `bdd27f4`, CC-BY-SA-3.0; select categories absent from repair/function data and pin IDs |

Do not create hashes until files exist. Do not use the benign smoke's `r=2`, `lr=1e-4`, two-step training or prompt fixtures as formal defaults.

### What formal C still lacks

The PI must freeze exactly: `D_repair` revision/IDs and target construction; PEFT versus full-parameter repair; module/rank/alpha if PEFT; optimizer/LR/betas/decay and fresh-init rule; paired batch-order rule; effective batch/tokens; repair checkpoints and the single formal checkpoint stage; endpoint tolerance bands including low-margin tail; normalized full-checkpoint/adapter export format. Luna should encode this one time in `v6_e1_repair_recipe.json` and make both C and P reference its hash.

## 6. First 4090 task

The first currently evidenced GPU entry is `V6.E1.DEV.RUNTIME_SMOKE`. It produces real Qwen benign generation and tiny LoRA training artifacts but **no E1 scientific data**. It becomes runnable after the relay candidate files are reconciled to a clean commit and the exact model is cached:

```bash
python -m scripts.v6_e1_executor \
  --execution-sha <CLEAN_RECONCILED_COMMIT> \
  --research-base-sha 90cf38bb632c0e6ca861596a59dec4acba23f8ba \
  --run-dir artifacts/v6_e1/DEV/runtime_smoke \
  --backend src.execution.local_model_smoke_backend:LocalModelSmokeBackend \
  pilot

python -m scripts.v6_e1_executor \
  --execution-sha <CLEAN_RECONCILED_COMMIT> \
  --research-base-sha 90cf38bb632c0e6ca861596a59dec4acba23f8ba \
  --run-dir artifacts/v6_e1/DEV/runtime_smoke \
  --backend src.execution.local_model_smoke_backend:LocalModelSmokeBackend \
  construct
```

These commands are **planned, not verified on the 4090 and not present on current GitHub main**. The first E1-relevant training task is `DEV.PREFLIGHT_REPAIR_A0`; it is not runnable until the direct repair/A0 runners and frozen recipes exist.

## 7. Luna's bounded implementation list

Luna should not reread the whole TODO or build a platform. Implement only:

1. Reconcile the relay E1 CLI, `FormalE1Backend`, split validator and benign smoke backend onto the current authoritative main; keep exact source/runtime provenance.
2. Replace the coarse stage backend with direct task calls carrying `task_id`, `run_id`, `attempt_id`, seed, config/data hashes, parent artifact ID and resource/cost fields.
3. Implement one `repair_runner` that accepts only the canonical repair recipe; C takes Base, P takes the actual A0 artifact. Add save/reload and identical-recipe-hash tests.
4. Implement one model-level A0 runner around existing direction math; emit a reloadable A0 provenance checkpoint. Do not create an A0 A1 arm.
5. Implement one fresh A1 LoRA runner with fresh adapter/state/RNG and no A0 search inputs; emit every frozen checkpoint plus token/time/failure/censoring records.
6. Implement endpoint match and sealed audit as separate calls to the authorized evaluator. Enforce common C/P repair stage; file existence is never qualification.
7. Implement the formal benign-plasticity runner and deterministic E1 summarizer for paired seeds and both continuation criteria.
8. Run CPU tests, then `DEV.RUNTIME_SMOKE`; stop and request the missing scientific/evaluator decisions before `DEV.PREFLIGHT_REPAIR_A0`.

No continuous queue, generalized scheduler, Week-2 code, defense code or broad data platform is in scope.

## 8. KEEP / FREEZE / CHANGE

**KEEP**

- V4 manifest/result schemas and preregistered constants;
- `EnvironmentLock`, `ModelArtifact`, content-addressed `ArtifactStore`;
- `CostTracker` failure/OOM/right-censor accounting;
- `RunCard`, `ExperimentChangeCard`, H0 raw-output boundary;
- direction tensor primitives and benign smoke backend as DEV-only validation.

**FREEZE**

- continuous polling/external-job queue and any unassigned pending job;
- generic orchestration DSL/queue, heartbeat, multi-worker scheduler and dashboard;
- V5 R0–R3/Fail-Closed/TamperBench expansion;
- every Week-2 or defense task.

**CHANGE**

- reconcile the minimal E1 direct path to GitHub main;
- add the three canonical A0/repair/A1 recipe files only after PI freeze;
- add direct A0/repair/A1/formal-plasticity runners and separate match/audit calls;
- correct parent lineage, same-stage enforcement, per-seed aggregation and cost separation.

## 9. Validation status

Independently verified on the Mac authoritative main:

```text
python -m pytest -q tests                  -> 48 passed, 1 warning
python -m compileall -q src tests scripts -> PASS
git merge-base / cat-file provenance      -> PASS
```

Verified for the new handoff after creation: JSON parsing, unique task IDs, dependency references, acyclic DAG, required task fields, local document references and `git diff --check`.

Not implemented or not independently verified:

- relay candidate's 73-test report on its original A800 environment;
- any RTX 4090 command or throughput number;
- model/data cache and hashes on the 4090;
- `repair_runner`, formal reload, A0 runner, A1 runner, content evaluator and formal plasticity runner;
- endpoint qualification, real E1 training data or scientific verdict.

## 10. Handoff stop

The next legal sequence is: `DEV.CODE_RECONCILE` and `DEV.MODEL_PREFETCH` in parallel → CPU tests → `DEV.RUNTIME_SMOKE` → stop at the first unresolved scientific/evaluator decision. Do not launch formal E1, do not create an unconsumed job queue, and do not enter Week 2.
