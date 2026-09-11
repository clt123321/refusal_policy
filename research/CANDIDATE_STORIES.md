# Competing Research Programs and Candidate Stories

## Evaluation scale

Scores are 0–10. For **compute cost**, 10 means most expensive. “Ceiling” is the
scientific ceiling if the central prediction is cleanly validated, not the expected
acceptance probability.

## Eight competing programs

### Program 1 — Representation redundancy versus parameter fault independence

- **Thesis:** Several independently causal activation carriers may still share a cheap parameter failure mode.
- **Novelty / prior relation:** The joint cross-space claim is open, but its pieces collide with Concept Cones, sparse refusal features, CoAx and NeuroStrike.
- **Killer experiment:** A preregistered matched pair with equal clean behavior, rank and restricted cut but reversed carrier-blind weight-attack durability.
- **Likely result:** Some high-dimensional models will still have a low-rank shared edit; whether this predicts independent attacks is unknown.
- **Failure mode:** The common mode is a shared-projector artifact or equivalent to late routing/neuron concentration.
- **Ceiling / cost:** 8 / 4.

### Program 2 — Safety as common-cause failure

- **Thesis:** Redundancy improves durability only when causal components occupy independently failing fault domains.
- **Novelty / prior relation:** Classical reliability supplies the distinction; the novel part would be operationalizing fault domains in LLM safety and predicting adaptive attacks.
- **Killer experiment:** Random single faults are tolerated, but a carrier-blind common-cause fault collapses all paths and predicts short fine-tuning.
- **Likely result:** Common-cause attacks will explain why in-family fault robustness overstates security.
- **Failure mode:** Fault domains are unstable across prompts/operators or do not predict another attack.
- **Ceiling / cost:** 8 / 4.

### Program 3 — Safety as adversarial controllability

- **Thesis:** The vulnerable mode is the one cheaply reachable in parameter/function space and strongly observable at the safety output, not the most decodable representation.
- **Novelty / prior relation:** Stronger theoretical object than rank; high collision risk with generic Jacobian, Fisher, curvature and control literature.
- **Killer experiment:** A preregistered generalized safety-versus-utility control spectrum predicts finite activation edits, low-rank weight edits and short FT on held-out data.
- **Likely result:** Local linear prediction will work for small interventions but may fail at behavior-changing scale.
- **Failure mode:** Coordinate dependence, poor nonlinear extrapolation, or no advantage over a gradient norm.
- **Ceiling / cost:** 9 if predictive, 4 if descriptive / 7.

### Program 4 — Safety circuit depth and self-repair

- **Thesis:** Durable refusal is repeatedly reconstructed across layers/tokens, rather than installed only at the prompt boundary.
- **Novelty / prior relation:** Any-Depth and DeepRefusal already establish depth/reconstruction; the open part is whether recovery dynamics predict weight-tamper durability.
- **Killer experiment:** Pulse versus sustained ablation maps recovery half-life, followed by a blinded persistent attack.
- **Likely result:** Some models re-form a refusal state after local disruption, but this may not survive weight edits.
- **Failure mode:** Recovery is LayerNorm rescaling, prompt-history leakage or unrelated to parameter attack cost.
- **Ceiling / cost:** 7 / 3.

### Program 5 — Recognition-to-action coupling

- **Thesis:** The critical vulnerability is separability between harm recognition and policy execution, not the number of refusal carriers.
- **Novelty / prior relation:** Zhao, Knowing without Acting, HARC, LLM-VA and Detection-to-Refusal substantially occupy the mechanism and defense.
- **Killer experiment:** A 2×2 harm/refusal intervention shows recognition survives carrier-blind tampering; coupling predicts attack cost after controlling rank.
- **Likely result:** Tampering often preserves recognition while disabling refusal.
- **Failure mode:** This reproduces existing work or coupling predicts input jailbreak but not white-box attack.
- **Ceiling / cost:** 6 / 3.

### Program 6 — Training-induced common-mode vulnerability

- **Thesis:** A training recipe can increase activation-level safety redundancy while *decreasing* the utility-constrained tamper margin by concentrating those mechanisms in one parameter fault domain.
- **Novelty / prior relation:** Labunets covers training→rank; Fisher/routing work covers training→fragility. The crossed redundancy/durability reversal under an independent attack remains open.
- **Killer experiment:** Randomize one narrow training factor, preregister matching criteria, and show higher causal cut but lower carrier-blind attack frontier across seeds.
- **Likely result:** Repetitive or strongly coupled supervision may create a common mode, but a reversal is far from guaranteed.
- **Failure mode:** Clean margin, M0 inheritance, KL drift or post-treatment checkpoint selection explains the ordering.
- **Ceiling / cost:** 9 / 6.

### Program 7 — Safety as an error-correcting code

- **Thesis:** A safeguard is durable if safety information can be reconstructed after arbitrary carrier erasures up to a measurable distance.
- **Novelty / prior relation:** Coding theory is old; no evidence yet identifies an encoder, symbols, channel and decoder in refusal.
- **Killer experiment:** An erasure threshold plus explicit downstream reconstruction that transfers to a persistent attack.
- **Likely result:** Effects will be continuous/operator-dependent rather than code-like.
- **Failure mode:** No stable symbols, threshold or reconstruction; the analogy adds no prediction.
- **Ceiling / cost:** 5 / 7. **Delete unless the prerequisite phenomenon appears.**

### Program 8 — Causal mediation versus adversarial editability

- **Thesis:** Where safety is causally expressed is not necessarily where an adversary can most cheaply edit it.
- **Novelty / prior relation:** Hase et al. established localization≠editability for facts; EMNLP 2025 extends the warning to unlearning. The open safety result is a prospective cross-operator law tied to adaptive work factor.
- **Killer experiment:** Across layers/modules, compare held-out activation mediation with a carrier-blind functional stability frontier; show a stable mismatch that predicts attack transfer.
- **Likely result:** Strong activation sites and cheap edit sites will only partially overlap.
- **Failure mode:** Safety behaves like ROME-style localized editing, or the mismatch does not generalize beyond one optimizer.
- **Ceiling / cost:** 8 / 4.

## Ranked story competition

### #1 — *More Safety Mechanisms, One Weaker Lock*

**One sentence:** Safety training can add independently causal refusal mechanisms
while making them jointly easier to disable through a shared parameter failure
mode.

**One year later:** “More safety mechanisms can mean one weaker lock.”

**Figure 1:** A preregistered matched pair: equal clean safety/utility and similar
activation rank/restricted cut, yet the apparently more redundant checkpoint is
broken by a cheaper carrier-blind attack.

**Figure 2:** Joint finite-edit frontier: attacker resources versus number of causal
components suppressed under a benign functional-change ceiling, followed by an
independently optimized attack frontier.

**Killer experiment:** Use an existing/short-trained checkpoint panel to find the
dissociation without post-hoc selection; validate it with two inductively different
attacks and one lightweight second family.

**Why surprising / general / now:** Reliability intuition predicts that more
independent mechanisms help; open-weight access exposes a common cause that random
component faults do not. The result connects mechanistic interpretability to the
new adaptive tamper benchmarks.

**Why not solved:** Prior work separately studies multiple carriers, sparse common
bottlenecks, training geometry and attack frontiers; it does not show the matched
cross-space reversal or prospective incremental prediction.

**Strongest objection:** A shared readout/projector or base-model margin makes the
common mode tautological.

**Falsifier:** After operator-independent controls and fair attack scaling, no
matched reversal exists or common-mode measures add no held-out predictive value.

### #2 — *Where Safety Acts Is Not Where Safety Breaks*

**One sentence:** Causal activation mediation does not identify the cheapest
parameter route for removing a refusal safeguard.

**One year later:** “Causal carrier ≠ adversarial edit target.”

**Figure 1:** Layer/module scatter: activation mediation versus minimum found
functional edit cost, with strong and reproducible disagreement.

**Figure 2:** The mismatched edit sites, not activation peaks, predict transfer to
short adversarial fine-tuning.

**Killer experiment:** Frozen extraction on held-out prompts, carrier-blind
structured edits and a second optimizer.

**Why surprising / general / now:** Mechanistic work often slides from “causes the
behavior” to “where the weights should be changed.” The distinction applies to
editing and unlearning as well as safety.

**Why not solved:** It is known for factual editing and suggested in unlearning, but
not established as a security law for adaptive open-weight safeguards.

**Strongest objection:** This is Hase et al. retold with refusal.

**Falsifier:** Activation mediation accurately predicts editability across operators
after utility and module-size controls.

### #3 — *The Common-Cause Gap in Neural Safeguards*

**One sentence:** Robustness to independent component failures systematically
overstates robustness to coordinated white-box faults.

**One year later:** “Random fault tolerance is not adversarial durability.”

**Figure 1:** Reliability curves for random independent faults and carrier-blind
common-cause faults, with their gap predicting the attack frontier.

**Figure 2:** Existing defenses such as fault-injection training shrink one side of
the gap but not the held-out common-cause side.

**Killer experiment:** Apply blinded independent/common faults to existing baseline
and defended checkpoints, then predict an unseen attack.

**Why surprising / general / now:** It explains why apparent redundancy and
in-family defense gains fail under adaptive attackers; reliability theory supplies a
clean language without pretending neural units are independent.

**Why not solved:** NeuroStrike finds a bottleneck and fault-trained methods harden
specific operators, but no work establishes a predictive common-cause gap.

**Strongest objection:** The chosen fault domains are arbitrary.

**Falsifier:** The gap changes sign across reasonable atomizations/operators or does
not predict a new attack.

### #4 — *Safety That Rebuilds Itself*

**One sentence:** Recovery after a transient internal fault, not static subspace
rank, predicts which refusal policies resist persistent tampering.

**One year later:** “Durable safety is a restoring process.”

**Figure 1:** Intervention-layer × downstream-layer/token recovery heatmap aligned
with content-level behavior.

**Figure 2:** Recovery half-life versus persistent edit/short-FT frontier, with rank
as a failing baseline.

**Killer experiment:** Pulse and sustained ablations plus a second-stage patch that
distinguishes true reconstruction from LayerNorm rescaling.

**Why surprising / general / now:** A static representation can disappear and
return; generation is a process. Any-Depth and DeepRefusal make the question timely.

**Why not solved:** Existing work shows re-triggering or trains for reconstruction,
but does not establish recovery dynamics as a white-box durability predictor.

**Strongest objection:** It is a repackaging of self-repair/Any-Depth.

**Falsifier:** Recovery is normalization-only or unrelated to persistent attacks.

### #5 — *A Functional Stability Frontier for Refusal Policies*

**One sentence:** Refusal durability should be compared by the maximum harmful
behavior reachable at each operational budget and benign functional displacement,
not by weight distance or a single attack.

**One year later:** “Weight distance is not attack work.”

**Figure 1:** Two defenses reverse ranking as attack budget and operator change.

**Figure 2:** Operational budget × harmful behavior × benign functional-change
surfaces with parameter norm shown to be coordinate-sensitive.

**Killer experiment:** Two reparameterization-equivalent models with different raw
weight norms but identical functional attack frontier, plus a real defense ranking.

**Why surprising / general / now:** It separates computational difficulty from
functional entanglement and applies to editing/unlearning.

**Why not solved:** Durability work already uses attack curves; the new contribution
would need a clean coordinate-invariance failure and a practical standard.

**Strongest objection:** This is evaluation hygiene, not a new mechanism.

**Falsifier:** Operational/frontier reporting never changes scientific conclusions
relative to existing evaluation.

## Final ranking

| Rank | Story | Novelty | Depth | Elegance | Falsifiability | Generality | Compute cost | Main-conference ceiling |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| #1 | More Safety Mechanisms, One Weaker Lock | 8 | 9 | 9 | 9 | 8 | 6 | 9 |
| #2 | Where Safety Acts Is Not Where Safety Breaks | 7 | 8 | 10 | 9 | 9 | 4 | 8 |
| #3 | The Common-Cause Gap in Neural Safeguards | 7 | 8 | 8 | 8 | 8 | 4 | 8 |
| #4 | Safety That Rebuilds Itself | 6 | 8 | 9 | 8 | 7 | 3 | 7 |
| #5 | A Functional Stability Frontier | 5 | 7 | 8 | 7 | 9 | 5 | 7 |

## Decision

Bet first on **#1**, but gate it using the cheaper #2/#3 dissociation tests. Do not
start with a full SFT/DPO/RL factorial. If the reversal does not exist, the honest
paper may become the negative version of #2: activation refusal geometry is an
unreliable proxy for white-box durability.
