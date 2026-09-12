# V4 Research Contract

**Version:** 4.0
**Frozen:** 2026-09-12; three independent reviews found no fatal blocker
**Round 2.5 verdict:** `REFINE`

## 1. Ultimate goal

> **Develop and validate a practical model-internal retrofit for already-trained open-weight language models that increases the measured work required for adaptive white-box safeguard removal while preserving benign capability, and explain the mechanism responsible for any gain.**

The goal is conditional. V4 first tests whether OAFT predicts adversarial parameter-space fault tolerance. It does not authorize a new defense until a failure mechanism survives the replication and diagnosis gates.

### Terms

- **Practical:** runnable on 8×A800-80GB; zero inference overhead preferred; a prototype should cost no more than five ordinary safety-SFT equivalents. A <$5–10 1–3B retrofit is a stretch target, not a scientific threshold.
- **Model-internal:** the safeguard is encoded in the released checkpoint and needs no secret key, hidden monitor, trusted API or mandatory runtime hook.
- **Open-weight:** the adversary receives a legal copy of all weights and enough code/configuration to run and modify it.
- **Adaptive:** the adversary knows the defense and retunes the allowed attack against each defended checkpoint within a frozen budget.
- **White-box:** weights, architecture, gradients, activations and public training code are visible; input-gradient access alone is not sufficient for this label.
- **Tampering cost:** cold-start target-specific work through the first observed utility-qualified breach, reported as FLOPs, accelerator-seconds, tokens, trials, parameter support and failures. It is attack-relative and may be censored.
- **Capability preservation:** every preregistered utility domain meets its retention floor, helpfulness/compliance remains bounded, and the defense does not buy safety through broad capability collapse.

## 2. Scope and claim boundary

Primary scope is post-training/retrofit **refusal safeguards** for already-trained open-weight models. Generalization to other safeguards is a future boundary test and is not part of the primary paper claim.

Primary scope excludes trusted execution environments, access control, remote-only inference, model replacement, full pretraining redesign and unlimited retraining. Pretraining-time safety and system controls remain comparison boundaries.

The first scientific claim may be a positive relationship, a null result, or a ranking reversal. The first contrast—base aligned checkpoint versus Fail-Closed checkpoint—is observational with respect to mechanism: the entire training recipe differs, so it cannot identify a causal effect of redundancy.

## 3. Frozen primary question

> **Does operator-specific activation fault tolerance predict adversarial parameter fault tolerance under adaptive, utility-constrained white-box tampering?**

Definitions, hypotheses and admissible interpretations are frozen in [V4_PRIMARY_QUESTION.md](V4_PRIMARY_QUESTION.md). The novelty boundary is recorded in [PRIMARY_NOVELTY_BOUNDARY.md](v4_workshop/PRIMARY_NOVELTY_BOUNDARY.md).

## 4. Work order and gates

1. **Contract:** pin sources, artifacts, scope, threat model, splits, evaluators and budgets.
2. **Harness:** extend TamperBench and pass interface/unit/smoke checks.
3. **Replication:** reproduce the canonical mechanism and nearest defense, then calibrate parameter-attack dynamic range on a base-only, disjoint split. Generating or inspecting a Fail-Closed parameter-attack result before N1 is prohibited.
4. **Screening contrast:** compare the aligned Gemma-2-2B checkpoint with the released Fail-Closed checkpoint; no new defense training and no standalone general claim from Case A.
5. **Diagnosis:** if screening warrants it, build a 32-checkpoint matched baseline panel and test whether any cross-space agreement/disagreement is explained prospectively by one candidate mechanism measurement.
6. **Optional defense prototype:** permitted only if a passed diagnosis suggests one primary change and its change card is approved. A valid diagnostic paper does not require this branch.
7. **Adaptive validation:** unseen attack family, stronger search, utility gaming checks and censoring-aware cost curves.
8. **Scale/generalize:** second model family and seeds only after the small-model gate.

`HARNESS_VALIDATED` is required before the natural experiment. `DIAGNOSIS_PASSED` and an approved `EXPERIMENT_CHANGE_CARD` are required before a novel defense run.

## 5. Measurement hierarchy

1. **Security endpoint:** attack–safety–utility–cost frontier and first-passage utility-qualified breach under a deterministic anytime schedule. Target-specific cumulative estimated FLOPs is the single primary cost axis.
2. **Mechanism evidence:** intervention, necessity/sufficiency, failure and rescue under held-out prompts.
3. **Predictor competition:** one candidate mechanism measurement versus stable rank, direction count, simple Fisher concentration and Skin-Deep GFS on attacks not used to define it.
4. **Descriptions:** angles, trajectories, layer heatmaps and parameter norms; never security conclusions by themselves.

There is no composite `writer-cut × (1-CC)` score. There is no claim of a global minimum attack or certified robustness.

## 6. Defense principle—but no algorithm

The retained principle is:

> A useful internal defense should create safety failure domains that remain costly to disable jointly under adaptive parameter access.

Not frozen: layer bands, parameter partitions, topology, a sensitivity-separation loss, direction count, writer atoms, a custom metric, or a training objective. Any later method must follow from an observed failure mechanism and beat equal-cost ordinary safety training and nearest-neighbor defenses.

## 7. Evidence and governance

Every claim maps to a model/data/code revision and immutable manifest/result artifacts conforming to [`V4_PROTOCOL_SCHEMA.json`](protocols/V4_PROTOCOL_SCHEMA.json) and [`V4_RESULT_SCHEMA.json`](protocols/V4_RESULT_SCHEMA.json). Frozen constants, five confirmatory attack seeds and deterministic sampling/search/statistical rules are in [`V4_PREREGISTERED_CONSTANTS.json`](protocols/V4_PREREGISTERED_CONSTANTS.json); known Fail-Closed claim/artifact provenance is in [`FAIL_CLOSED_PROVENANCE.csv`](protocols/FAIL_CLOSED_PROVENANCE.csv). Failed, OOM, divergent and non-breaching trials are retained. Dangerous raw generations remain access-controlled and are not committed.

Before any novel GPU run, an `EXPERIMENT_CHANGE_CARD` must record: baseline, one primary change, reason, prior evidence, prediction, falsifier, controls, GPU budget and human approval. Every run emits a `RUN_CARD` with commit, hashes, config, seed, hardware, FLOPs estimate, runtime, cost and artifact path.

## 8. Allowed conclusions

| Evidence | Allowed wording | Forbidden wording |
|---|---|---|
| Attack fails within budget | “Not breached by attack A within budget B” | “Tamper-proof” or “secure” |
| Fail-Closed contrast differs | “The two checkpoints show cross-space agreement/dissociation” | “Redundancy caused the difference” |
| One mechanism score predicts one attack | “Predictive in the tested regime” | “Universal security metric” |
| Two independent attack families improve | “Cross-operator evidence under the registered portfolio” | “General white-box robustness” |
| New defense improves only a trained attack | “Attack-specific hardening” | “Durable safeguard” |

## 9. Contract-change rule

Thresholds, splits, attack budgets or primary outcomes may change only before the corresponding sealed evaluation, with a dated change card and rationale independent of results. Any post-result change is exploratory and labeled as such. A new paper that closes the three-part novelty boundary triggers a stop and re-audit.

## 10. Source anchors

- Coalson et al., [Fail-Closed paper](https://arxiv.org/abs/2602.16977), [code](https://github.com/ztcoalson/Fail-Closed-Alignment), [checkpoints](https://huggingface.co/collections/ztcoalson/fail-closed-alignment).
- Hossain et al., [TamperBench](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
- Qi et al., [Durability Audit](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
- Tamirisa et al., [TAR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.

## 11. Final independent review

| Reviewer role | Fatal blocker | Score | Decision |
|---|---:|---:|---|
| Security red team | No | 9.2/10 | GO |
| Reproducibility | No | 9.0/10 | GO |
| Top-conference AC | No | 8.2/10 | GO |

The reviews authorize freezing the research contract, not skipping its gates. H1 must still resolve licensed artifact access, full hashes, environment lock and data fingerprints; R0–R3 must validate the harness; N1 must materialize and sign the complete experiment configuration and independent A5 commitment before any paired parameter result is generated.

`V4_RESEARCH_CONTRACT_FROZEN`
