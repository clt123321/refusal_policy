# V4 Primary Novelty Boundary

## Frozen boundary after Round 2.5

### What is already known and cannot be claimed

- Refusal can be mediated by one or several activation directions.
- Several directions can be causally active and representationally independent.
- Training under direction ablation can reconstruct refusal and tolerate the trained activation fault.
- Activation redundancy can improve prompt-jailbreak and direction-ablation robustness.
- Refusal-prefix diversity can increase stable rank and weaken one vector attack.
- Harm recognition, refusal decision and refusal execution can dissociate and be explicitly coupled.
- Bilevel/adversarial post-training can increase resistance to bounded malicious fine-tuning.
- Utility-constrained attack portfolios and attack-specific durability measurement already exist.

These are controls and priors, not v4 contributions.

### The admissible primary question

> **Does operator-specific activation fault tolerance predict adversarial parameter fault tolerance under adaptive, utility-constrained white-box tampering?**

The null and alternative are symmetric:

- **H0 / no predictive relation:** once clean behavior and training dose are controlled, tolerance to the registered activation projection does not predict utility-qualified parameter breach work.
- **H1 / bounded predictive relation:** preregistered OAFT predicts greater breach work under at least two genuinely different adaptive parameter-attack biases and outperforms rank, direction-count, Fisher and Skin-Deep GFS baselines.

The project does not assume either answer.

### The contribution, if the phenomenon exists

The new knowledge is a **cross-space distinction**, not a new geometry metric:

> Tolerance to an activation intervention is not security evidence unless it predicts resistance to independently optimized parameter interventions.

A publishable result must supply:

1. reproducible OAFT under an explicitly named operator, without calling imposed directions natural pathways;
2. independently optimized utility-qualified parameter attack frontiers;
3. a 32-checkpoint matched panel across two model families, four non-novel training conditions and four training seeds;
4. a mechanism that predicts held-out parameter attacks better than rank, direction count, simple Fisher and full Skin-Deep GFS baselines;
5. optionally, only after the diagnostic claim succeeds, a defense derived from that mechanism. A valid diagnostic paper does not require a successful defense.

### Claims explicitly forbidden

- “We discovered fail-closed refusal / multiple safety writers.”
- “Orthogonal directions are independent pathways” or “OAFT proves causal pathway independence.”
- “Higher rank means more secure.”
- “A failed attack proves tamper resistance.”
- “The baseline-versus-Fail-Closed contrast identifies a causal treatment effect.”
- “A new scalar is a security metric” without prospective held-out prediction.
- “White-box robustness” without naming whether access is to inputs, activations or parameters.

### What could still kill novelty

Before every new experiment batch, check Fail-Closed revisions and papers citing it. Stop if prior work jointly supplies all three: (i) operator-specific activation fault tolerance, (ii) defense-aware direct edits or malicious fine-tuning with utility constraints, and (iii) an explicit prospective test of whether that activation property predicts parameter attack cost. A paper that provides only two of the three narrows our claim but does not automatically eliminate it.

### Defense status

The defense **principle** remains: seek model-internal failure domains that stay costly to disable jointly under adaptive parameter access. No layer partition, topology, sensitivity loss, writer-cut, composite score or algorithm is frozen. The released-checkpoint contrast is only screening; any paper-level relationship requires the matched panel, and a novel defense requires a preregistered change card tied to an observed failure mechanism.

`PRIMARY_NOVELTY_STATUS = CLEAR_GAP_WITH_HIGH_COLLISION_BOUNDARY`
