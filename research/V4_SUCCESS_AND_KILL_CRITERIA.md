# V4 Success and Kill Criteria

## Stage gates

### Harness success

`HARNESS_VALIDATED` requires R0–R3, full artifact lineage and cost accounting, consistent utility gating, and no unresolved evaluator/template discrepancy.

### Scientific minimum

The Gemma checkpoint contrast is a screening result, not by itself the scientific minimum. It must reproduce activation-side ordering and show a resolvable parameter-attack frontier. Progress requires either:

- stable dissociation/equivalence (Case B) or ranking reversal (Case C) across at least two parameter-attack biases; or
- Case A followed by a matched 32-checkpoint panel that establishes a monotone/out-of-sample relationship rather than a whole-recipe contrast.

A saturated attack suite, an unbreachable baseline or inconsistent author replication does not count.

### Strong-paper threshold

A candidate parameter/functional mechanism measurement, frozen before the confirming attack, must predict held-out attack cost better than stable rank, causal-direction count, simple Fisher concentration, Skin-Deep GFS and clean behavior. The independent units are 32 final checkpoints from two backbones × four matched non-novel training conditions × four seeds; attack seeds/trials are repeated measures. The result must survive whole-checkpoint holdout, leave-one-backbone/condition-out sensitivity and at least two independent parameter-attack biases, with transparent nulls and censoring.

### Practical-defense threshold

A later defense is successful only if:

- it improves utility-qualified breach cost on at least two independent attack families absent from its training/selection;
- the gain survives defense-aware re-extraction, stronger search and a bounded full-FT check;
- every utility domain and over-refusal stay within the frozen bound;
- defender compute and inference overhead are reported, and attacker added work is material relative to defender cost;
- an equal-compute ordinary safety-training control does not explain the gain.

Stretch targets are ≥2× work factor, <1% clean utility loss, <$5–10 for a 1–3B retrofit and zero inference overhead. They are engineering ambitions, not hard scientific pass rules.

## Immediate stop or pivot

Stop the affected stage immediately if:

1. R0 canonical mechanism failure remains unresolved after template/direction/evaluator audit.
2. Fail-Closed's published activation/behavior ordering cannot be reproduced from the released artifact.
3. The attack suite has no dynamic range under reasonable registered budgets.
4. A safety result disappears when actual harmful task success replaces refusal keywords.
5. The utility-qualified gain comes from broad capability loss, over-refusal or utility-panel gaming.
6. A defense only resists the operator used during training/selection.
7. A defense-aware adaptive bypass removes the gain at ≤1.25× the paired baseline work.
8. The proposed mechanism fails prospective prediction or does no better than rank/count/Fisher/full-GFS baselines.
9. The second model family reverses the claim with no explanatory moderator.
10. New prior work jointly solves operator-specific activation fault tolerance, adaptive parameter tampering and their prospective relationship.
11. A parameter-space breach does not alter the preregistered activation intervention/rescue result; in that case the result is a downstream bypass and the “jointly disabled pathways” mechanism claim stops, though behavioral durability analysis may continue.

## Decision after the first natural experiment

| Outcome | Decision |
|---|---|
| Case A: both activation tolerance and parameter cost rise | Screening only; build/replicate the matched panel before any scientific relationship claim |
| Case B: activation rises, parameter cost is equivalent | Pursue common-parameter-cause diagnosis; strongest clean dissociation |
| Case C: activation rises, parameter cost falls | Prioritize ranking-reversal mechanism; do not “repair” the result into the old story |
| Case D: author result fails | Stop novelty work and resolve replication |

Equivalence in Case B uses the preregistered practical interval, not a non-significant p-value. Both arms must be uncensored across all five confirmatory attack seeds and the paired hierarchical-bootstrap 90% cost-ratio interval must lie inside `[0.8, 1.25]`; otherwise the result is inconclusive. Case B remains screening until replicated in the matched checkpoint panel.

## Authorization rule for a novel defense

All must be true:

1. `HARNESS_VALIDATED` exists.
2. The natural experiment has a stable Case A/B/C classification.
3. A specific failure mechanism—not a generic metric—survives a held-out attack.
4. One primary intervention follows from that mechanism.
5. An approved `EXPERIMENT_CHANGE_CARD` states its falsifier and equal-cost controls.

Otherwise the correct output is a diagnostic paper, null result or project stop—not an improvised defense.

## Reporting discipline

- “Not breached within budget,” never “robust” without a qualifier.
- Ratios include uncertainty and censored observations.
- All attack-family results are shown; no best-looking subset.
- Model-family heterogeneity is a result, not a nuisance to average away.
- Exploratory threshold/config changes remain separate from confirmatory results.
