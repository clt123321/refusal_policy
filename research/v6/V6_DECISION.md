# V6 Decision — Residual Breach Shortcut

**Status:** `V6_E1_CONDITIONAL_READY`

## Primary claim

Safety repair may restore current refusal while leaving a causally reusable residual computation that lowers the workload of a fresh, independent parameter attack.

The minimum mechanism claim requires behavior/margin-matched repaired and clean-history endpoints, a lower fresh re-attack workload after attack→repair history, causal removal that eliminates the advantage, and transplantation that induces it. The strong target adds rescue.

## Novelty boundary

**Assessment:** `PARTIAL_COLLISION`.

Persistent hidden policies, cyclic realignment history effects, faster relearning, incomplete repair, model-edit persistence and a faster second attack are prior-adjacent observations, not the contribution. V6 is distinct only if it identifies a latent computation and bidirectionally controls independent fresh-attack workload while current safety behavior, margin and narrow functionality remain matched.

## Threat-model scope

The repaired checkpoint is the later deployment/distribution target of a new white-box parameter attack. V6 does not address an attacker retaining an old compromised checkpoint, arbitrary model substitution, conditional routing, or external model/tool replacement. Reported workload is tied to the frozen attack procedure and is not a global minimum.

`W_A(θ)` is the charged cumulative estimated FLOPs through the first frozen A1 tier that crosses the content-level breach threshold while all narrow-functionality/capability/collapse gates pass; an unreached boundary is right-censored. A residual breach shortcut additionally requires causal removal and transplant, not only `W_A(P) < W_A(C)`.

## Week 1 — E1

- One pinned `Qwen/Qwen2.5-1.5B-Instruct` initialization, two preregistered seeds, target under one A800 GPU-day.
- `B`: untouched base → fresh A1, descriptive only.
- `C`: A0-matched benign/sham edit → same fixed repair budget as P → fresh A1.
- `P`: refusal-suppression direct edit A0 without target answers → fixed safety repair → fresh A1.
- Freeze and isolate `D_A0_loc`, `D_repair`, `D_A1_train`, `D_attack_eval`, `D_function`, and `D_plasticity` by semantic family and exact dedup.
- Admit C/P only when content safety, safety margin, over-refusal, narrow functionality and target-capability access fall within preregistered tolerance bands.
- A1 uses new data, operator/objective/localizer, adapter, optimizer/scheduler/scaler and RNG; one shared budget grid records first passage, curves, all failures and censoring.
- Run an unrelated benign unseen-task learning curve to test generic plasticity.

`PASS`: both valid-endpoint seeds and either `W_A(C)/W_A(P) >= 2` or P exceeds C by at least 20 points at the frozen intermediate budget, without a listed confound. `AMBIGUOUS`: one preregistered correction only. `KILL`: both seeds `<1.25×`, loss under independence controls, confound explanation, or unresolved floor/ceiling.

## Week 2 causal gate

Only after E1 `PASS`, localize one bounded candidate on discovery data. The entire parameter delta, a probe or representation correlation is inadmissible as a mechanism.

- Removal from P must reduce the re-attack advantage while preserving current endpoint behavior.
- Transplant into C must induce the advantage under a new sealed re-attack.
- Rescue is required when removal is not strictly local/reversible or may alter general plasticity.

Minimum gate: `removal + transplant`. Strong gate: `removal + transplant + rescue`. If bidirectional workload control fails, emit `KILL_MECHANISM_STORY`.

## Kill rules and frozen work

E1 `PASS` supports only the phenomenon. No defense, 32-checkpoint panel, large matrix, universal scalar, Gemma gate, full Fail-Closed/TamperBench replication, W3/OAFT/Fisher/GFS expansion or broad mechanism workshop is authorized before causal residue evidence. V4 authorization, threat-model, lineage, manifests, evaluator boundaries, cost/censoring, preregistration, ChangeCard/RunCard and adaptive red-team discipline remain frozen.
