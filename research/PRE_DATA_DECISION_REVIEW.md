# Pre-data decision review

**Status:** committee review complete; full training matrix not authorized

**Decision:** **CONDITIONAL GO** for one real-refusal, attack-blind 72-hour gate

**Evidence cutoff:** integrated repository state at `357e585`

**Scope:** decisions before further GPU evidence; `TODO.md` is intentionally unchanged

## Executive decision

The synchronized experiment history changes the project in an important way. The
safe proxy shows that the measurement and intervention stack can find a stable,
behaviorally active policy lever. It does **not** show a refusal safeguard, multiple
causal writers, a shared parameter failure mode, or tamper durability.

The committee therefore rejects immediate expansion into the SFT/DPO/RL recipe
matrix. The only authorized next step is a chained real-safety feasibility test:

```text
C0 natural-refusal construct validity
    -> H2 matched-operator mechanism audit
    -> freeze both sides independently
    -> carrier-blind finite parameter diagnostic + cheap A3
    -> decide whether H1 is identifiable
```

The eventual main-conference candidate is not “more refusal dimensions are safer.”
It is the much stricter possibility that **robustness to independent activation
faults and durability to parameter tampering can rank the same models in opposite
orders**. Training recipe is a later source of randomized variation, not the first
headline.

## What the synchronized evidence establishes

| Evidence level | Supported conclusion | Important boundary |
|---|---|---|
| Representation | The answer/abstain proxy has a stable late-layer policy contrast: peak separation is about 6.5 with little topic leakage. | This is an explicit benign instruction task, not natural harmful refusal. |
| Readout | The policy direction and first-token margin track the instructed policy. | Readout is not a natural decision mechanism; the first-token proxy is incompletely calibrated to completions. |
| Steering | Adding the direction over L18–23 changes abstention by about +25 percentage points; reported controls are near zero. | This establishes narrow sufficiency under an all-token intervention, not necessity or safety. |
| Residual necessity | Removing the residual direction at one, six, or all 28 layers has essentially no behavioral effect. | Zero-event bootstrap intervals were overconfident; this is still strong evidence against the tested necessity operator, not proof of universal non-necessity. |
| Module intervention | Removing the L27 MLP output's own projection changes the proxy classifier by 21.875 pp and shows a graded logit response. | L27 was selected after a scan; a reviewer spot-check indicates the binary effect may partly reflect refusal wording, but this was not a frozen semantic audit. The reshuffle is split sensitivity, not an independent model/prompt replication. |
| Intervention semantics | Hook equivalence is accurate, signal regeneration is not a complete explanation, and fixed displacement behaves similarly before/after residual addition and RMSNorm. | The MLP-own and residual-own interventions remove different state-dependent quantities. The evidence does not localize a special nonlinear computation to L27. |
| Writer organization | Of eight scanned writers, only L27 MLP has a reported behavioral effect; every effective subset contains it. | The proxy supplies negative evidence for multi-writer redundancy within the tested set. |
| Parameter sensitivity | Three behaviorally null writers have positive gradient cosine; the L27 writer is near-orthogonal or negative relative to them. | Four examples, three selected parameter blocks, no finite edit and no utility endpoint. This cannot support co-controllability and cautions that common gradients may track irrelevant readouts. |
| Security | None. | No harmful prompts, actual harmful compliance, capability qualification, utility-constrained edit, A3/A4, or BreachCost. |

Primary sources: [SAFE_MECH_REPORT](../artifacts/safe_mech/SAFE_MECH_REPORT.md),
[ASYMMETRY_DIAGNOSIS](../artifacts/safe_mech/ASYMMETRY_DIAGNOSIS.md), and
[SAFE_PROXY_CLOSEOUT](../artifacts/safe_mech/SAFE_PROXY_CLOSEOUT.md).

The strongest defensible proxy statement is:

> A linear policy coordinate can be readable and steerable without being necessary
> under the tested residual-removal operator; apparently conflicting causal results
> can arise because interventions use different reference tensors.

It is not yet defensible to say “representation is not computation,” “L27 is where
the policy is computed,” or “many writers share one parameter fuse.”

## Independent committee and cross-review

Five roles first reviewed the evidence independently: mechanistic interpretability,
security, causal/statistical, novelty, and a skeptical top-conference area chair.
Only after all five first-pass opinions were collected were their conclusions exposed
for cross-review.

### Durable agreements

1. The benign proxy is useful measurement debugging, not a safety result.
2. The current full recipe matrix is a **NO-GO**.
3. Natural refusal requires semantic actual-harmful-compliance outcomes, not keyword
   refusal scoring.
4. The MLP-versus-residual result must be retested with matched state displacement,
   token scope, dose, and reference tensor.
5. At least two independently validated causal components are required before
   “redundancy” or “common-cause failure” is identifiable.
6. A common-mode statistic may not reuse the carrier projector or attack objective;
   otherwise the result can become a shared-Jacobian tautology.
7. A finite search result is an attack-family-relative found-breach frontier, not a
   model's global minimum tamper cost.
8. Recipe effects require randomized fixed-dose runs. Behavior matching has a
   different, descriptive interpretation.

### Productive disagreements

- **H2 first versus security jointly:** the mechanism reviewer wants matched-state
  representation/computation tests first; the statistical reviewer wants a cheap A3
  early enough to prevent a mechanism-only curiosity. The resolution is operational,
  not rhetorical: run both inside the same 72-hour window, keep data and tuning
  firewalled, and merge only after both artifacts are frozen.
- **H2 as headline versus prerequisite:** H2 can provide genuine causal mediation
  evidence if a projection-only patch fails while an orthogonal/full-output patch
  succeeds. It still cannot carry a tamper-safety paper without an independent
  security endpoint. Treat it as a required mechanism result and a fallback story,
  not the default safety headline.
- **Carrier-blind attacks:** blindness is required for validation independence, but
  it is not a restriction on the real white-box adversary. A full paper must also
  include a mechanism-aware adaptive attack.

### Risks newly exposed by cross-review

- **Fault-dose non-comparability:** deleting each tensor's full self-projection gives
  different perturbation energy and behavioral dose across writers and runs.
- **Atomization-induced reversal:** writer count/cut can change with module grain,
  token scope, projector, or operator. A reversal that disappears under one
  preregistered reasonable atomization is not a scientific cross-space reversal.
- **Cross-run ruler drift:** choosing a different top-eight atom set per checkpoint
  can manufacture recipe differences. A shared canonical intervention library is
  primary; run-specific discovery is secondary.
- **Post-treatment qualification:** dropping trained runs that fail to yield two
  carriers conditions on a treatment-affected variable. Such failures remain part
  of recipe intention-to-treat outcomes and cannot be silently marked missing.

## Frozen names and hierarchy

To prevent label drift across reviews, this document uses one canonical hierarchy:

- **C0a — semantic construct gate:** actual harmful compliance, refusal action,
  harmfulness recognition, benign utility and capability access are validly separated.
- **C0b — causal-component gate:** at least one broader component passes a frozen
  causal intervention and rescue. A scalar direction is called a *causal carrier*
  only if scalar remove/add/patch/rescue itself succeeds.
- **H1 — cross-space fault independence:** independent activation-fault robustness
  can disagree with utility-constrained parameter-tamper durability.
- **H2 — representation versus causal computation:** a readable/steerable coordinate
  is not necessarily a sufficient mediator of natural policy computation.
- **H3 — training-induced common-mode vulnerability:** randomized post-training can
  increase activation-fault robustness while reducing parameter-tamper durability.

`writer-cut` is retained only as a descriptive restricted intervention curve, not a
new theoretical object. Infinitesimal gradient cosine is not called
`co-controllability`; the security-relevant object is a **finite joint-edit
frontier**, explicitly indexed by attack family, budget, and utility ceiling.

## The next 72-hour decision experiment

Use one capability-qualified 1–3B aligned open model; do not train recipes. This
single-checkpoint gate cannot estimate a ranking reversal or establish H1 predictive
validity. A later H1 pilot requires a preregistered panel of 2–4 existing frozen
checkpoints; full-paper prediction requires the larger powered panel.

### Mechanism lane — frozen before attack reveal

1. Create family-disjoint `construct-fit`, `carrier-dev`, and fresh `carrier-test`
   sets for harmfulness × policy action.
2. Evaluate natural harmful prompts with two automated semantic judges and a blinded
   human calibration subset.
3. Freeze layer, atom, dose, token scope, and evaluator on development data.
4. Test residual-own removal, module-own removal, and identical fixed displacement
   at matched graph locations.
5. Separate assistant-boundary-only, generation-only, and all-token interventions.
6. Run removal/necessity on naturally refusing harmful prompts; run
   addition/sufficiency on matched permissive or controlled prompts with verified
   dynamic range; run rescue on the naturally perturbed state. Compare
   projection-only and full-output rescue;
   measure harmfulness recognition, policy action, actual harmful compliance,
   over-refusal, benign utility, and capability access.
7. Search for conditional backups only after a genuinely effective primary fault.

### Attack lane — blind to mechanism artifacts

1. Freeze a carrier-blind A2 structured search and an A3 short malicious
   full-parameter fine-tuning attack with different inductive biases; retain the
   mechanism-aware A1 projector edit as calibration, not independent validation.
2. Tune on `attack-dev` only; charge failures and all search work.
3. Run a small non-degenerate utility-qualified frontier on `attack-test`.
4. Do not reveal attack outcomes to the mechanism lane until its definitions,
   thresholds, and hashes are frozen.

### Feasibility continuation criteria

Continue beyond 72 hours only if all three are observed:

1. **Natural construct:** semantic AHC changes in the predicted direction in the
   appropriate necessity and sufficiency prompt regimes, with specificity and a
   valid rescue; recognition and capability are not merely destroyed.
2. **Multiplicity:** at least two distinguishable causal components survive
   selection-aware testing and a fresh prompt-family replication.
3. **Security measurement:** a carrier-blind finite parameter intervention and A3
   produce a non-degenerate utility-qualified frontier. This is feasibility only;
   comparison against clean margin/rank and H1 prediction begin on the later frozen
   checkpoint panel.

If item 1 fails, stop the safety-mechanism route. If item 1 passes but item 2 fails,
pivot to localization/mediation versus editability and delete redundancy language.
If items 1–2 pass but item 3 fails, retain an activation-mechanism result but do not
claim durability relevance. None of these failures may be repaired by opening the
recipe matrix.

## Final vote and main-conference bar

| Scope | Vote |
|---|---|
| Existing benign proxy as a safety result | **NO-GO** |
| Full SFT/DPO/RL recipe matrix now | **NO-GO** |
| One real-refusal 72-hour chained gate | **CONDITIONAL GO** |
| H1 as headline | **GO only after** at least two causal carriers, atomization-stable panel-level reversal, carrier-blind out-of-sample A3 prediction, and A4/second-backbone confirmation |
| H3 recipe study | **Frozen until H1 passes** |
| Defense | **Move later; cannot rescue a failed mechanism** |

The minimum main-conference result is a preregistered cross-space reversal that is
stable to the frozen atomization sensitivity, reproduced by two attacks with
different inductive biases, predicts held-out attack cost beyond strong simple
baselines, and transfers directionally to a second backbone. Anything weaker should
be framed as a bounded mechanism or methodology result.

`RESEARCH_COMMITTEE_READY`
