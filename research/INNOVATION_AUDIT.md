# Innovation Audit / Research Taste Review

**Project:** `refusal_policy`
**Audit cutoff:** 2026-09-11
**Committee decision:** **C — PIVOT**
**Scope:** literature and idea audit only; no experiment was run and `TODO.md` was not modified.

## Executive decision

The original chain

```text
training objective
→ refusal geometry
→ writers / writer-cut
→ parameter co-controllability
→ breach cost
```

is not a sufficiently novel main-conference story. Recent work separately occupies
nearly every edge: multi-direction refusal, interacting minimal SAE feature sets,
dormant backups, training-induced low-rank geometry, geometry-based fragility
scores, sparse neuron bottlenecks, fault-injection defenses and adaptive tamper
evaluation.[^1][^2][^3][^4][^5][^6][^7]

The viable pivot is a narrower and more falsifiable distinction:

> **Causal redundancy in activation space does not imply independent failure in
> parameter space. Safety training can add apparent mechanisms while decreasing the
> utility-constrained tamper margin if those mechanisms inherit one common failure
> cause.**

This is not yet a result. Its value depends on a matched ranking reversal and
carrier-blind prediction of an independent attack. Without those, “many writers,
one fuse” is an expected shared-Jacobian observation already foreshadowed by Arditi,
Concept Cones, output-routing work and NeuroStrike.[^8][^9]

## 1. Current novelty score

### **4.5 / 10** for the current writer-cut / co-controllability story

- Individual ingredients: **3–5/10**; mostly occupied or renamed.
- Narrow joint cross-space hypothesis: **7.5/10 conditional ceiling**.
- Current evidence for that hypothesis: **0/10**, because the decisive experiment
  has not yet been run.

The score is deliberately lower than “no single paper did the whole pipeline.” A
pipeline assembled from known pieces is not automatically a new scientific insight.

## 2. Three strongest existing-work collisions

### Collision 1 — Minimal causal sets and backup mechanisms

*Beyond I’m Sorry, I Can’t* identifies an interacting minimal SAE feature set and
dormant redundant refusal features; CoAx independently develops conditional
co-ablation for hidden backups.[^1][^2] Concept Cones already states that geometric
orthogonality is not functional independence.[^3]

**Consequence:** `writer-cut`, minimal causal writer set and backup re-extraction are
not publishable novelty. At most they are diagnostics over a frozen intervention
library.

### Collision 2 — Training geometry and pre-attack fragility diagnostics

Labunets directly connects refusal-prefix diversity to gradient/activation rank and
fixed ablation sensitivity.[^4] Skin-Deep proposes a pre-attack activation Geometry
Fragility Score.[^5] New work proposes capability-Fisher overlap, curvature and late
output routing as explanations of fine-tuning failure.[^10][^11]

**Consequence:** “objectives shape geometry,” “diversity raises rank,” and “geometry
predicts fragility” are already occupied at the claim level. Our metric must beat
these competitors prospectively, not merely correlate with attacks.

### Collision 3 — Common safety bottlenecks and mechanism-targeted defenses

NeuroStrike reports that pruning a very small safety-neuron set breaks many models
and transfers to fine-tuned descendants.[^9] DeepRefusal, SafeNeuron and NeuronGuard
already train against refusal-direction or safety-neuron failure to promote
reconstruction/redistribution.[^6][^12][^13]

**Consequence:** “shared safety fuse” and “disable the fuse during training to force
redundancy” are not enough. A defense is derivative unless it follows from a newly
validated common-cause mechanism and survives independently optimized attacks.

## 3. Three genuinely open gaps

### Gap 1 — Cross-space dissociation under matched behavior

No located paper shows a preregistered pair of refusal-policy checkpoints matched on
clean safety, benign utility, decision margin, activation rank and restricted causal
cut, yet sharply separated in carrier-blind parameter-tamper cost.

**Why prior work does not solve it:** refusal geometry stays mostly in activation
space; tamper papers evaluate attacks without validating multiple causal carriers;
NeuroStrike shows one sparse fault but not a matched activation/parameter reversal.

### Gap 2 — Prospective mechanism prediction of an adaptive frontier

No located work shows that a finite common-cause response statistic improves
leave-run-out prediction of a separately optimized, utility-constrained attack
frontier beyond rank, GFS, Fisher/curvature, routing concentration, neuron
concentration and clean behavior.

**Why prior work does not solve it:** geometry papers often validate with a related
ablation; durability work warns that optimizer details re-rank defenses but does not
provide an internal predictive mechanism.[^7][^14]

### Gap 3 — Independent-fault robustness versus coordinated-fault durability

Fault-trained safety work tests operators close to those used in training. It is
still open whether a model can become robust to many independently applied carrier
faults while remaining easy to break by a carrier-blind common cause—and whether
the size of this gap predicts an adaptive attack.

**Why prior work does not solve it:** reliability theory predicts common-cause
failure in engineered systems, but LLM fault domains are not naturally given. The
scientific work is to define them operationally and validate them out of sample, not
to import a reliability polynomial.

## 4. Current story verdict

# **PIVOT**

Retain the experimental assets, causal-intervention discipline, explicit threat
model and utility-constrained endpoint. Change the central question from:

> Which objective/diversity recipe creates the best refusal geometry?

to:

> When does causal activation redundancy fail to provide independent protection
> against parameter tampering?

Training recipe becomes a controlled source of variation after the mechanism gate,
not the headline causal treatment. `Objective × Diversity` and a defense are not
part of the initial innovation test.

## 5. Best alternative story — one only

### *More Safety Mechanisms, One Weaker Lock*

> A post-training recipe can increase the number and functional independence of
> activation-level refusal mechanisms while decreasing the utility-constrained
> white-box stability margin, because those mechanisms inherit a shared parameter
> failure cause.

Why this one:

- **Simple distinction:** causal redundancy ≠ adversarial fault independence.
- **Surprise:** the “more redundant” model can be less durable.
- **Mechanism:** a finite, carrier-blind parameter intervention jointly changes
  independently validated components.
- **Security endpoint:** a separately optimized harmful-compliance/utility frontier,
  not refusal geometry.
- **Generality without overclaim:** the theory may extend to learned safeguards, but
  the paper should say *refusal-policy safeguards* until a second domain is tested.

The name `writer-cut` is unnecessary. `Co-controllability` should be replaced by a
**joint finite-edit frontier** or **common-mode susceptibility**, explicitly
conditioned on an attack family and utility ceiling. Do not multiply metrics into
`writer-cut × (1−CC)`.

## 6. Killer experiment on the existing 8×A800

### Question

Can two preregistered checkpoint conditions look equally safe and equally redundant
in activation space, yet differ strongly under carrier-blind parameter tampering in
a direction predicted by a common-cause measurement?

### Design

1. **Freeze a panel before attack results are opened.** Use current feasibility
   checkpoints plus same-family public baseline/defended checkpoints. Predefine a
   matching rule over clean harmful compliance, benign utility, refusal margin,
   dose/KL and activation rank/cut; analyze the whole panel so matching is not
   post-treatment cherry-picking.
2. **Separate data and operators.** Use disjoint sets for carrier extraction,
   causal validation, common-mode fitting and A3/A4 testing. The common-mode attack
   must not reuse the carrier projector or its loss.
3. **Validate components.** Separate harm recognition from policy execution; require
   held-out removal/addition plus patch/rescue. Add one conditional co-ablation pass
   so intact attribution does not miss backups.
4. **Measure candidate explanations blinded to attacks.** Effective rank, restricted
   cut, GFS, Fisher overlap/curvature, late-routing concentration, safety-neuron
   concentration, clean margin and a finite joint-edit frontier.
5. **Run two attacks with different inductive biases.** One carrier-blind structured
   low-rank/module edit and one short adversarial fine-tune, each with a small
   preregistered budget sweep and failed trials charged to cost.
6. **Evaluate the final object.** Content-level harmful compliance against benign
   utility and benign functional KL at each operational budget. Refusal substring
   is secondary.

### Killer figure

A four-panel figure:

1. clean safety and utility are matched;
2. activation rank/restricted cut are matched or favor model H;
3. a finite carrier-blind edit jointly suppresses more validated components in H;
4. the independent attack frontier shows H is cheaper to breach—the predicted
   ranking reversal.

### Minimal 72-hour envelope

- 1–2B model family for activation/weight access;
- 4–8 frozen checkpoints/conditions, at least two seeds where trained locally;
- 256 matched extraction/validation pairs;
- ≈300 family-held-out harmful prompts and ≈300 benign/XSTest prompts;
- 48–96 aggregate A800 GPU-hours, roughly 8–18 hours wall time after setup,
  leaving time for one attack-budget expansion and a failed-run audit.

The initial gate need only compare the joint-edit object with the strongest cheap
baseline plus rank/cut. The full paper must later include GFS, Fisher/curvature,
routing and NeuroStrike-style concentration baselines, leave-run-out prediction, a
lightweight second family and target-specific reoptimization.

## 7. What result would make us stop?

Stop the current mechanism story—not merely the current metric—if any of the first
four conditions replicate across two seeds or reasonable attack budgets:

1. **Geometry changes without security change:** rank/restricted cut changes
   materially, but carrier-blind attack frontiers remain within noise.
2. **No cross-space dissociation:** after matching clean margin and utility, no pair
   or panel exhibits a stable reversal between activation redundancy and tamper
   durability.
3. **Measurement leakage:** common-mode effects vanish when writers use atom-local
   readouts or when attacks stop reusing the policy projector.
4. **No incremental prediction:** joint-edit/common-cause measures do not beat rank,
   GFS, Fisher/curvature, routing/neuron concentration and baseline behavior on
   held-out A3/A4.
5. **Optimization-gap collapse:** apparent durability disappears after fair budget
   scaling or a second attack family.
6. **Wrong endpoint:** refusal falls but content-level harmful capability/compliance
   does not rise, or the attack “succeeds” only by degrading benign utility.
7. **No causal writers:** putative components fail removal/addition/patch/rescue or
   conditional discovery shows the frozen atom set was incomplete.

If 1–4 fail, the defensible negative paper is narrower:

> Activation-space refusal geometry is an unreliable proxy for white-box safeguard
> durability.

Do not rescue the original story by adding metrics, backbones or a defense.

## Counterexamples actively sought

| Counterexample | Candidate source | Consequence |
|---|---|---|
| Many directions, shared behavioral control | *There Is More to Refusal*; Concept Cones | Destroys “dimension = independent mechanisms” |
| Stable low rank while robustness moves | Dynamic adversarial-training geometry | Destroys “rank determines durability” |
| Similar scalar parameter geometry, different durability | Malla continuous/windowed schedules | Destroys one-number Fisher explanation |
| Strong causal activation site, different edit site | *Does Localization Inform Editing?* | Destroys activation→parameter inference |
| Self-repair under activation fault, cheap white-box break | DeepRefusal plus simple/community attacks | Destroys in-family fault robustness as security |
| Tiny common neuron bottleneck transfers across descendants | NeuroStrike | Makes “shared fuse” itself non-novel |
| Refusal removed while harm recognition remains | Zhao; Knowing without Acting | Forces recognition/action separation |
| Geometry improves without TamperBench improvement | TAR/defended checkpoint panel | Would kill geometry-as-explanation |

Community-modified checkpoints are discovery aids only. Their model-card claims must
be independently reproduced before entering evidence.

## Adversarial debate record

Five roles first worked independently: literature archaeology, novelty red team,
top-conference taste, theory exploration and experimental minimalism. Only after
their independent reports were frozen did they receive summaries of the others.

### Strong agreement

- `writer-cut` alone is a restricted assay, not a new theory.
- “many writers, one parameter direction” alone is expected Jacobian/shared-gate
  behavior and is not sufficient for a main conference.
- The carrier projector cannot be shared across discovery, common-mode fitting and
  attack validation.
- Raw parameter L2 is not an intrinsic control energy because of neural-network
  reparameterization.
- The title and claims must remain about refusal-policy safeguards unless a second
  safeguard domain is actually tested.
- The main-conference gate is a matched ranking reversal plus held-out adaptive
  prediction beyond strong baselines.

### Real disagreement retained

The Experimental Minimalist initially proposed `low/high refusal-start diversity ×
2 seeds` as the first 72-hour test. The archaeologist, red team, taste critic and
theory explorer rejected it as too close to Labunets and underpowered for novelty.
After cross-review, the minimalist revised the recommendation: use a preregistered
carrier-blind attack and matched dissociation first; reserve diversity manipulation
for mechanism variation after the gate.

The minimalist still objected to requiring every expensive baseline and both A3/A4
inside 72 hours: that can confuse a weak attack implementation with real durability.
The committee accepts this objection. The 72-hour gate uses one strong cheap
baseline and two attack inductive biases; the complete baseline race is a full-paper
requirement.

### Risks discovered only in cross-review

- **Construct–attack leakage:** a shared policy projector can make common control a tautology.
- **M0 domination:** short post-training may only change decision margin while all conditions inherit the base model’s carrier.
- **Optimization gap:** a measured minimum is partly the attack searcher’s competence.
- **Conditional backup omission:** intact-model top-k attribution misses Hydra-like paths.
- **Post-treatment matching:** hand-picking behavior-matched checkpoints after seeing attack outcomes creates selection bias.

## Innovation Committee vote

| Role | Revised recommendation | Main-conference ceiling |
|---|---|---|
| A — Literature Archaeologist | **PIVOT** | Conditional yes |
| B — Novelty Red Team | Keep causal controls; refine to finite frontier; pivot recipe/defense | Conditional yes |
| C — Taste Critic | Conditional go on matched ranking reversal | Conditional yes |
| D — Theory Explorer | Defer factorial/defense; common-cause + functional frontier | Conditional yes; subjective 40–55% if gate passes |
| E — Experimental Minimalist | Conditional main-conference go | Conditional yes; subjective ≈35% under stricter full conditions |

This is not consensus that the hypothesis is true. It is agreement that one narrow,
cheap and falsifiable bet survives novelty review. All five vote **NO-GO** if the
matched dissociation or carrier-blind out-of-sample prediction fails.

## Stopping-condition audit

- **No further major collision found after the final outward sweep:** satisfied for
  the *narrow revised claim*, not for the original story.
- **Differentiated from ≥5 nearest works:** satisfied in the comparison matrix,
  conditional on the cross-space/OOS result.
- **Simple falsifiable prediction:** satisfied.
- **One killer experiment on 8×A800:** specified.
- **≥3/5 high-ceiling votes:** satisfied, all conditional.
- **Skeptical reviewer has no fatal novelty objection:** satisfied only for the
  narrow preregistered claim; failure to beat strong baselines is explicitly fatal.

The innovation audit can therefore close. The research program itself remains
gated by evidence.

## Final answer

> **当前最值得下注的 research insight：安全机制的因果冗余，可能因共享参数失效模式而增加表面保护、却降低真实白盒篡改裕度。真正的新知识不是“有多少拒答方向”，而是何时更多安全机制反而只形成一把更弱的锁。**

`INNOVATION_AUDIT_COMPLETE`

## Sources

[^1]: Prakash et al., [*Beyond I’m Sorry, I Can’t*](https://ojs.aaai.org/index.php/AAAI/article/view/41119), AAAI 2026.
[^2]: Gong et al., [*Conditional Co-Ablation*](https://arxiv.org/abs/2607.01940), arXiv preprint, 2026.
[^3]: Wollschläger et al., [*The Geometry of Refusal in Large Language Models*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^4]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv preprint, 2026.
[^5]: Lee et al., [*Skin-Deep*](https://arxiv.org/abs/2606.22676), arXiv preprint, 2026.
[^6]: Xie et al., [*DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings of EMNLP 2025.
[^7]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^8]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^9]: Wu et al., [*NeuroStrike*](https://www.ndss-symposium.org/wp-content/uploads/2026-s660-paper.pdf), NDSS 2026.
[^10]: Malla et al., [*The Geometry of Refusal: Why Post-Hoc Safety Is Fragile and Pretraining-Time Safety Persists*](https://arxiv.org/abs/2609.06934), arXiv preprint, 2026.
[^11]: Guo et al., [*When Safety Routing Breaks*](https://arxiv.org/abs/2609.01455), arXiv record reporting Findings of EMNLP 2026.
[^12]: Wang et al., [*SafeNeuron*](https://arxiv.org/abs/2602.12158), arXiv preprint, 2026.
[^13]: Gao et al., [*NeuronGuard*](https://arxiv.org/abs/2608.23959), arXiv preprint reporting Findings of EMNLP 2026.
[^14]: Qi et al., [*On Evaluating the Durability of Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
