# Round 5 Decision

## Decision in one paragraph

The primary bet is a deliberately narrow **local-to-global functional-inseparability hypothesis**: a pre-attack local property may predict whether global adaptive optimization can change safety without changing benign function. It is not yet a mechanism and is close to the attack objective, so it must pass objective-level isolation, nonlinear/composed attacks and a later matched causal manipulation. OAFT and direction count remain baselines; finite parameter fault overlap is the secondary competing mechanism.

## Selected hypotheses

### PRIMARY MECHANISM BET — Local safety–utility inseparability

> **Testable sentence:** Local safety–utility inseparability predicts global tamper resistance across unseen attack operators.

The proposed internal property is the strength and persistence of safety-changing parameter modes after normalizing by benign functional change. The utility-conditioned response spectrum is a local pre-attack proxy, not the contribution or an explanation of why the mode exists. Only prospective off-operator prediction plus a mediated causal manipulation can promote it from security regularity to mechanism.

### SECONDARY BET — Finite parameter fault-domain overlap

> **Memorable sentence:** Many safety effects can still share one finite parameter fuse.

This asks whether several separately causal safety effects can be jointly suppressed by one carrier-blind, utility-qualified finite edit for approximately the price of the cheapest individual edit. It is distinct from the primary: the shared mode may exist but be utility-expensive, or components may be fault-independent yet each individually cheap to remove. Gradient cosine and module overlap do not qualify.

### HIGH-RISK WILDCARD — Common safety bootloader

> **Memorable sentence:** Many repair paths may all depend on one reboot signal.

This temporal mechanism predicts persistent multi-token rescue from one transient upstream patch and simultaneous loss of all recovery after one parameter lesion. It is more specific than “self-repair,” but may fail because transformers need repeated external retriggering rather than an autonomous source.

## Scorecard

Scores are 0–10; higher experimental tractability means cheaper/easier.

| Bet | Novelty | Explanatory power | Falsifiability | Cross-attack relevance | Beyond refusal | Tractability | Defense connection | Main-conference ceiling |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Local functional inseparability | 8 | 8 | 9 | 9 | 9 | 6 | 8 | 9 |
| Finite parameter fault overlap | 8 | 9 | 9 | 8 | 8 | 7 | 8 | 8.5 |
| Common safety bootloader | 8 | 8 | 9 | 6 | 7 | 6 | 8 | 9 |

Cross-domain attack transfer remains a useful endpoint decomposition, not a selected internal mechanism. Autonomous recovery without a bootloader test, generic basin geometry, module diversity, static controllability and rank are not selected.

## Required answers

### 1. What most likely determines tamper margin?

Most plausibly, whether the model exposes a **utility-cheap safety-changing parameter mode** that persists far enough for a nonlinear attacker to reach content-level breach. This is a hypothesis to test, not a reformulation accepted as fact.

### 2. Why?

The attacker must solve “change safety while retaining useful function.” Fault overlap matters only if the shared fault is utility-feasible; regeneration matters only if it survives a persistent edit. The nontrivial claim is not that the global margin exists, but that a local, independently measured functional property predicts global best responses.

### 3. Closest prior work

Skin-Deep proposes an activation-geometry fragility score; safety/utility gradient work studies conflict; When Safety Routing Breaks and Geometry of Alignment Collapse study Fisher concentration and curvature; TAR/TamperBench evaluate weight-update durability.[^skin][^routing][^collapse][^tar][^tamperbench]

### 4. Genuine novelty gap

No reviewed work constructs an operator-conditioned local response with both data- and objective-level isolation, prospectively predicts direct, sparse, nonlinear-gradient and composed tampering beyond the nearest baselines, and then causally moves that property under a matched training intervention with general plasticity controlled. Without all three, this becomes another metric paper.

### 5. Second explanation

Finite parameter fault overlap: several apparent safety effects may share one upstream parameter cause. It explains why activation redundancy can fail, but must be distinguished from the utility price of exploiting that cause.

### 6. Cheapest killer experiment

The cheapest falsifier is the Gemma-2-2B vanilla/Fail-Closed screen, followed by verified same-base Llama-3-8B vanilla, Fail-Closed, DeepRefusal and TAR-Refusal checkpoints. Freeze one local predictor and baselines before A3/A4; a clear wrong ordering kills universality. This panel cannot prove prediction. Confirmation requires the matched 32-checkpoint design with independent training seeds before any predictor or causal claim.

### 7. Immediate falsifier

Stop the primary hypothesis if the pre-attack response spectrum fails to predict both independently implemented A3 and A4 beyond gradient norm, clean margin, full GFS, Fisher and OAFT—or if nonlinear conditional FT or `edit→benign repair→cleanup` breaches a favorable checkpoint at baseline cost under a second sealed utility/capability panel.

### 8. Defense implication if true

If the mediated manipulation succeeds, make safety-changing updates functionally expensive across multiple parameter operator classes while preserving legitimate adaptation. The first causal test rotates matched safety updates toward versus away from utility-essential functional modes and controls overall plasticity. This is a conditional principle, not a frozen algorithm.

### 9. Why this could be top-conference work

It establishes a new distinction with operational consequences:

> **Local safety–utility inseparability can predict global white-box durability—or fail decisively under an off-operator best response.**

The claim would establish a local-to-global law, explain why rank/reconstruction can fail, predict several unseen white-box attacks and yield a causal defense test. A four-point correlation, a new scalar, or same-objective attack prediction has no main-conference story.

## Primary bet one level deeper

### Definition

For a fixed checkpoint, predictor-stage safety output vector `s`, benign functional output vector `u` and declared parameter operator class, local separability is the achievable change in `s` per unit benign functional displacement. It is summarized by the generalized spectrum of `Gs` relative to `Gu`. Global tamper margin remains a separate attack outcome.

### Measurement

Estimate JVP/VJP sketches on predictor-only hazard domains/stage outputs and utility data, solve the damped generalized eigenproblem within low-rank, sparse-block and unrestricted tangent classes, and record leading gain, spectral concentration and mode persistence across small finite steps. Freeze the operator and damping before attacks; verify nullspace stability on a second utility suite. Use function-space/Fisher normalization, never raw parameter norm.

### Causal intervention

After natural support and matched-panel confirmation, train matched arms whose safety updates are constrained toward versus away from utility-essential functional/Fisher modes, with identical base, data, target tokens, optimizer, FLOPs and fixed final dose. Match clean margin, capability access, overall Fisher/update spectrum and legitimate-adaptation performance; verify the intended local change and mediation before viewing attacks.

### Prediction

Stronger local inseparability should increase A1, A3 and A4 first-passage breach cost, survive nonlinear/composed best responses and a second utility suite, and make durability decay more slowly as the utility cap is relaxed.

### Alternative explanations

1. parameter common-cause/fault overlap creates the apparent mode;
2. a late recognition→execution bottleneck explains editability;
3. local curvature or a global low-loss detour defeats the tangent estimate;
4. missing harmful capability creates false durability;
5. the utility panel fails to observe real capability damage.

### Natural experiment

Use the released same-base checkpoint panel described above. Treat every defense pair as observational, freeze predictors before attacks, and require cross-attack rather than within-operator prediction.

### Manipulation experiment

Run only after natural screening and matched-panel confirmation: one 1–3B common base, high-inseparability versus low-inseparability safety-update constraint plus ordinary matched SFT. Reject if clean behavior/dose/plasticity mismatch, intended geometry does not mediate the effect, or only the construction attack improves.

### Defense implication

The conditional defense principle is **cross-operator functional inseparability**: removing the safeguard should require changing computations that benign capability also needs, without merely collapsing or freezing the model. Legitimate-adaptation cost is therefore a mandatory negative control.

## Harness implication

Add only batched safety/utility JVP-VJP sketches, randomized generalized eigensolver, finite-step mode-persistence logging, pulse/window activation traces, stage patch hooks, composed-attack accounting, second utility/capability panels and domain-transfer tables. Do not add full Hessians, exhaustive trajectories, Grassmann analyses or a new composite security score.

## Independent taste review

| Reviewer | Primary verdict | Key objection | Decision impact |
|---|---|---|---|
| Mechanistic Scientist | **REFINE** | local generalized response is the linear relaxation of the attack objective, not yet an explanation | require objective-level isolation, mediation and an account of why the mode exists |
| Security Scientist | **CONDITIONAL GO for screening** | nonlinear, conditional and composed attacks can bypass a favorable local spectrum | add independent A4/A5, adaptive FT, repair composition, second utility/capability panel |
| Top-conference AC | **CONDITIONAL GO** | four observational checkpoints cannot support predictor selection or causality | use them only to kill; require matched independent checkpoints and manipulation for a main claim |

All three retain the refined primary. Mechanistic and AC reviewers prefer finite parameter fault overlap as the secondary; two of three retain the bootloader as the most mechanistic high-risk wildcard. Cross-domain transfer is downgraded to diagnostic. Current status is `CONDITIONAL GO`: the measurement-only screen is worth doing, but a defense or general durability claim is not authorized.

## Stop boundary

Round 5 selects hypotheses, not a paper conclusion and not a defense. Do not modify the frozen V4 TODO or start large training from this document. The next authorized action is artifact verification and a separately approved measurement-only screen.

## Sources

[^skin]: Lee et al., [*Skin-Deep*](https://arxiv.org/abs/2606.22676), arXiv 2026.
[^routing]: Guo et al., [*When Safety Routing Breaks*](https://arxiv.org/abs/2609.01455), Findings of EMNLP 2026 per arXiv record.
[^collapse]: Springer et al., [*The Geometry of Alignment Collapse*](https://arxiv.org/abs/2602.15799), arXiv 2026.
[^tar]: Tamirisa et al., [*Tamper-Resistant Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^tamperbench]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.

`ROUND5_MECHANISM_HYPOTHESES_SELECTED`
