# Round 5 — Candidate Mechanism Space

## Scientific boundary

The outcome is always **utility-constrained tamper margin / first-passage breach cost**. A mechanism variable is retained only if it predicts an attack family that was not used to construct it and admits an intervention that can change the variable without defining success by the same attack. Refusal is the first test case, not the universal claim.

Evidence labels below mean: `KEEP` = enters the common experiment; `DIAGNOSTIC` = explains a failure but is not a headline; `MERGE` = has no independent prediction; `DELETE` = currently mathematical or positional decoration.

## Candidate decisions

| Candidate property | Decision | Reason |
|---|---|---|
| A. Parameter fault-domain overlap | **KEEP — secondary** | A single finite edit may jointly disable many activation effects; raw gradient cosine is insufficient |
| B. Safety regeneration / self-repair | **DIAGNOSTIC** | Has a unique pulse-versus-sustained prediction, but DeepRefusal/Any-Depth occupy the broad claim |
| C. Safety–utility entanglement | **KEEP — primary hypothesis, not yet a mechanism** | Tests a local-to-global regularity; objective-level as well as data-level separation is required |
| D. Parameter controllability | **MERGE into C** | The useful part is a local estimator of selective editability, not a separate control-theory story |
| E. Safety basin / barrier | **DELETE generic form** | Distance to the unsafe-useful set restates the outcome; raw weight geometry is coordinate dependent |
| E2. Local curvature | **DIAGNOSTIC** | May predict early LoRA/full-FT turning when first-order sensitivity fails |
| F. Recognition→policy→execution coupling | **DIAGNOSTIC** | The decomposition is prior work; attack-conditioned failure order could explain a breach |
| G. Module heterogeneity | **MERGE into A** | Different layers/modules do not imply different functional fault domains |
| H. Dynamic/temporal persistence | **DIAGNOSTIC** | Autonomous recovery is distinct from static depth coverage, but may only govern transient attacks |
| I. Cross-domain attack-transfer isolation | **DIAGNOSTIC** | Useful endpoint decomposition, but the transfer matrix is defined by attack outcomes rather than an internal cause |
| J. Common safety bootloader | **KEEP — high-risk wildcard** | Predicts that one upstream state regenerates many later safety states and is a common-cause target |
| K. Breach-channel volume | **DIAGNOSTIC / missing variable** | Can explain search work at fixed minimum distance, but is hard to estimate without outcome leakage |
| L. Signed causal compensation | **FALSIFICATION CONTROL** | Explains non-monotonic ablation without pretending antagonistic writers are redundant |

### Independent new candidates

- Researcher 1 proposed **signed causal compensation**: opposing causal effects can mimic redundancy and explain non-monotonic multi-direction ablation.
- Researcher 2 proposed **cross-domain attack-transfer isolation**: one attack's functional coverage can differ radically from activation diversity.
- Researcher 3 proposed the **common safety bootloader**: many later recovery paths may share one upstream restart source.

### One-sentence taste test for every candidate

| Candidate | Sentence worth remembering if true |
|---|---|
| A | Many safety effects can still share one finite parameter fuse. |
| B | A representation has not repaired safety until the recovered state causally repairs behavior. |
| C | Local safety–utility inseparability predicts global tamper resistance across unseen operators. |
| D | The easiest local control mode matters only if it remains useful on the path to breach. |
| E/E2 | Curvature matters only when it predicts when a seemingly benign update turns into a safety failure. |
| F | A model can still recognize harm after the recognition-to-action link is gone. |
| G | Different modules are not different fault domains unless their failures stop transferring. |
| H | Safety that recovers after a pulse may still fail under a persistent edit. |
| I | Safety is not domain-isolated if one edit breaks every policy. |
| J | Many repair paths may all depend on one reboot signal. |
| K | Equal nearest breach distance need not mean equal search work when escape channels have different width. |
| L | Non-monotonic ablation can be cancellation, not backup safety. |

## Hypothesis cards

### A — Finite parameter fault-domain overlap

**Hypothesis.** When separately validated safety effects can be jointly suppressed by one carrier-blind finite parameter intervention at approximately the price of the cheapest single suppression, they share a parameter fault domain; greater overlap predicts lower breach cost under a different parameter-attack bias.

**Why it could be causal.** Several activation effects may be downstream images of one upstream parameter cause. Editing that cause removes all of them without paying once per apparent carrier.

**Existing evidence.** Concept Cones shows that geometric orthogonality is not functional independence; CoAx and SAE work expose backups; NeuroStrike finds sparse transferable safety bottlenecks. Localization-editability work warns that the causal activation site need not be the cheapest parameter edit.[^cones][^coax][^neuro][^localedit]

**Genuinely unknown.** No reviewed work establishes a finite, utility-qualified joint-edit discount and then uses it to predict a carrier-blind LoRA, full-FT or sparse attack.

**Unique prediction.** At matched OAFT, behavior and utility, checkpoints with a large joint-edit discount fail earlier under sealed A3/A4. The joint edit should suppress multiple independently scored safety effects at once.

**Counterexample / falsifier.** High gradient overlap among non-causal features, projector-dependent overlap, no finite joint-cost discount, or no held-out attack prediction. Any of these rejects the mechanism rather than merely its metric.

### B — Autonomous causal regeneration

**Hypothesis.** After a transient internal fault is removed, downstream layers/tokens recompute a safety state that is itself causally necessary for recovered safe behavior; faster recovery predicts pulse-fault tolerance.

**Why it could be causal.** A conditional backup computation can be dormant in the intact run and activated only after a fault. Blocking the recovered state should eliminate behavioral recovery.

**Existing evidence.** DeepRefusal trains reconstruction under direction faults; Any-Depth shows that safety can be externally re-triggered during generation.[^deeprefusal][^anydepth]

**Genuinely unknown.** External retriggering and reappearance of a readout do not establish autonomous causal repair, nor do they imply resistance to permanent parameter edits.

**Unique prediction.** Pulse recovery disappears when the newly recovered state is blocked, while a sustained intervention separates genuine redundancy from transient repair.

**Counterexample / falsifier.** The readout returns but has no causal effect; LayerNorm or prompt leakage explains recovery; recovery predicts pulse attacks but not parameter attacks. In the last case retain it only as a runtime mechanism.

### C — Safety-only parameter editability

**Hypothesis.** Operator-conditioned local safety–utility inseparability predicts global tamper resistance across unseen attack operators. Models with a strong local **utility-conditioned safety mode** should have lower cross-attack breach cost, regardless of activation rank or OAFT.

**Why it could be causal.** A white-box attack is a constrained intervention: it succeeds only if it moves safety behavior while staying inside an acceptable benign-function neighborhood. If all safety-changing directions also move utility-essential functions, the attacker must pay more or find a nonlinear detour.

**Existing evidence.** Safety/utility gradient-conflict work, Skin-Deep, Fisher/routing analyses and curvature accounts show that local geometry can track some fine-tuning failures; TAR and TamperBench make utility-qualified parameter attack the relevant endpoint.[^skin][^routing][^collapse][^tar][^tamperbench]

**Genuinely unknown.** No reviewed work prospectively tests whether a utility-conditioned parameter response spectrum predicts direct edit, sparse edit, nonlinear/conditional malicious FT and composed repair attacks on checkpoints unseen during construction, then causally changes that spectrum while matching training dose, behavior and overall plasticity.

**Unique prediction.** The largest utility-conditioned safety response predicts attack initial slope and inverse first-passage cost across A1, A3 and A4. Relaxing the utility cap should collapse durability fastest in models whose safety-changing modes were previously utility-expensive.

**Counterexample / falsifier.** The statistic only predicts the attack whose gradients built it; ordinary gradient norm, GFS or clean margin predicts equally well; ranking changes under functionally equivalent parameterization; or nonlinear, conditional or edit→repair→cleanup attacks find low-cost paths despite a benign local spectrum. Until these tests and a mediated manipulation pass, this is a security regularity—not a full mechanistic explanation of why the mode exists.

### D — Parameter controllability

**Hypothesis.** A low-dimensional parameter input can steer the safe model to unsafe behavior at low functional cost.

**Why it could be causal.** The leading generalized response mode is an explicit intervention direction.

**Evidence and gap.** Rank-one ablation and small edits show local controllability, but a feed-forward Transformer does not supply a canonical dynamical control system, and Euclidean control energy is parameterization dependent.[^arditi][^reparam]

**Unique prediction.** None beyond C once utility-conditioned reachability is used.

**Counterexample / falsifier.** A steep first step hits a utility barrier or rotates before breach. **Decision: MERGE** into C as a local measurement; delete standalone control-language claims.

### E — Basin, barrier and curvature

**Hypothesis.** A local second-order coupling bends apparently benign update trajectories into safety-sensitive directions, shortening early fine-tuning time-to-breach.

**Why it could be causal.** Curvature changes the future direction of a fixed optimizer even when the initial safety/utility gradients appear orthogonal.

**Evidence and gap.** Recent curvature and late-routing studies motivate this for short fine-tuning, but not for direct jumps or long adaptive optimization.[^collapse][^routing]

**Unique prediction.** Hessian-vector-product predictions beat first-order gradients specifically for the first 16–128 LoRA/full-FT steps, not for direct edits.

**Counterexample / falsifier.** No early-trajectory improvement beyond gradient norm. Generic “distance to unsafe-capable basin,” linear interpolation barriers and raw sharpness are **deleted** because they either restate the attack or vary under reparameterization.

### F — Attack-conditioned stage survival

**Hypothesis.** Different parameter attacks breach refusal by first breaking a particular causal interface—recognition→policy or policy→execution—and the weakest interface predicts attack-specific cost.

**Why it could be causal.** Preserved recognition cannot enforce policy if its downstream influence is severed; patching the broken interface should rescue behavior.

**Existing evidence.** Harm recognition and refusal are separable; HARC couples them; When Safety Routing Breaks finds preserved intermediate signal with damaged late routing.[^separate][^harc][^routing]

**Genuinely unknown.** Whether a stable stage-failure order predicts adaptive direct, sparse and gradient attacks rather than merely describing them afterward.

**Unique prediction.** A1/A4 preserve recognition and first reduce policy→execution transfer, whereas sufficiently long full FT can alter recognition. Pre-breach interface decline should forecast the later endpoint.

**Counterexample / falsifier.** All stages change together, patching cannot rescue, or stage order varies idiosyncratically. Then this remains a postmortem, not a law.

### G — Functional module heterogeneity

**Hypothesis.** Safety effects implemented in different modules raise sparse/local edit cost only when lesions fail to transfer and one module can rescue another.

**Why it could be causal.** True fault containment forces a local attacker to cover more support.

**Evidence and gap.** Safety signals and neurons span attention/MLP and depth, but residual mixing creates common causes; location counts are not independence.[^neurons]

**Unique prediction.** Low cross-module lesion transfer raises A4 cost but need not raise unrestricted full-FT cost.

**Counterexample / falsifier.** A joint edit costs no more than the cheapest single-module edit. **Decision: MERGE** into A; delete layer/module diversity as a standalone variable.

### H — Temporal persistence

**Hypothesis.** Safety that is repeatedly and autonomously reconstructed across generation is harder to defeat with bounded-duration input/activation faults.

**Why it could be causal.** The attacker must maintain the fault until harmful commitment rather than win once at the prompt boundary.

**Existing evidence and gap.** Any-Depth and DeepRefusal occupy depth/retriggering; the open part is autonomous impulse response and its limited transfer to persistent parameter attacks.[^anydepth][^deeprefusal]

**Unique prediction.** Recovery half-life predicts pulse/prefill robustness but can be orthogonal to permanent weight-attack cost.

**Counterexample / falsifier.** Recovery is absent, non-causal or has no relation even to pulse attacks. Do not promote temporal persistence to the main white-box story without persistent-attack prediction.

### I — Cross-domain attack-transfer isolation

**Hypothesis.** Tamper margin rises when an attack optimized on one hazard domain does not transfer to other domains, forcing the attacker to pay for multiple functionally distinct edits.

**Why it could be causal.** A universal safety-policy fuse lets one update disable many policies. Domain-isolated failure surfaces require several attacks or a more expensive joint objective.

**Existing evidence.** Universal refusal directions and sparse bottlenecks suggest common transfer, while concept-specific refusal suppression suggests the opposite can occur. Current defense work rarely makes attack-transfer structure the mechanism.[^arditi][^neuro]

**Genuinely unknown.** Whether a precommitted 4×4 hazard-domain transfer matrix predicts multi-domain joint breach cost across attack families and beyond activation rank.

**Unique prediction.** The minimum number of domain-optimized attacks needed to cover all domains predicts joint breach work; high OAFT can coexist with cover number one.

**Counterexample / falsifier.** Every row transfers broadly, the cover number is always one, the value changes arbitrarily with domain partition, or an adaptive joint-domain objective bypasses apparent isolation at the cost of one attack. Even on success this is an attack-outcome decomposition until an internal cause is separately identified.

### J — Common safety bootloader

**Hypothesis.** Apparently multiple safety states and recovery paths depend on one compact upstream state that repeatedly regenerates them; destroying that state stops both recovery and refusal across stages.

**Why it could be causal.** A one-time clean patch at the upstream state should launch persistent downstream recovery, while a targeted parameter lesion should abolish every later recovery signature.

**Existing evidence and gap.** Fail-Closed/DeepRefusal show fault tolerance and reconstruction, and routing work suggests bottlenecks, but no reviewed work identifies an autonomous upstream “restart source” with temporal necessity, sufficiency and parameter vulnerability.[^failclosed][^deeprefusal][^routing]

**Unique prediction.** One transient upstream patch rescues multiple later states for several tokens; a carrier-blind lesion at the source simultaneously removes OAFT and recovery.

**Counterexample / falsifier.** Recovery requires repeated external injection, several independent patches, or the effect lasts only one token. This is a high-risk mechanism, not terminology to assume.

### K — Breach-channel volume

**Hypothesis.** At the same best attainable functional distance, models with more or wider unsafe-useful attraction corridors require fewer search trials and lower operational breach work.

**Why it could be causal.** Optimization cost depends on discoverability as well as existence; broad basins capture more initializations and tolerate noisier update rules.

**Existing evidence / unknown.** TamperBench and durability audits show attack ranking and seed sensitivity, but do not identify an internal, attack-independent channel-volume law.[^tamperbench]

**Unique prediction.** Two checkpoints can have the same best-found edit size yet different first-passage trial distributions across independent optimizers.

**Counterexample / falsifier.** Estimated volume changes with arbitrary initialization coordinates, requires the full attack portfolio to define, or fails to transfer across optimizers. Keep as a missing-variable diagnostic, not a selected mechanism.

### L — Signed causal compensation

**Hypothesis.** Some high-rank or non-monotonic safety systems contain opposing causal safety and anti-safety effects whose joint removal cancels, rather than redundant paths whose removal accumulates.

**Why it could be causal.** If individual interventions have opposite content-level effects, their combined intervention can restore the baseline even though each alone moves behavior strongly.

**Existing evidence / unknown.** Non-monotonic multi-direction ablations motivate the alternative, but current proxy behavior also shows how normalization artifacts can imitate it. No reviewed result establishes stable antagonistic refusal pathways.

**Unique prediction.** Individual effects have opposite signs, joint removal is sub-additive toward baseline, and reciprocal patch/rescue restores the cancellation pattern.

**Counterexample / falsifier.** Signed projections lack causal behavioral effects or fixed-displacement controls remove non-monotonicity. Retain only as a falsification control.

## Innovation pressure tests

### Inversions that could change the story

1. More activation carriers increase OAFT but make the leading safety-only parameter mode stronger.
2. The fastest self-repairing checkpoint is the easiest to break permanently because every repair path shares one bootloader.
3. Strong safety–utility entanglement raises tamper cost but makes legitimate benign adaptation more likely to disturb safety.
4. A sharp local safety region can resist direct edits if every steep direction is also utility-expensive; flatness alone is not protection.
5. High clean refusal margin can be a thin late-output inhibitor and predict lower, not higher, tamper margin.
6. Module diversity can coexist with cover number one because one cross-module edit transfers everywhere.
7. A model can retain perfect harm recognition after its safeguard is behaviorally gone.
8. Two models with the same closest breach distance can have very different attacker work because one has many wide escape channels and the other a narrow one.

### Cross-field abstractions retained only for their predictions

| Field | Retained abstraction | Prediction | Deletion condition |
|---|---|---|---|
| Reliability engineering | common-cause factor vs independent failures | random/local-fault survival overstates adaptive joint-fault survival | gap does not predict a sealed attack |
| Control theory | generalized reachability under a utility metric | top response mode predicts early attack slope | no gain over gradient norm or unstable to reparameterization |
| Dynamical systems | impulse vs step response | transient recovery can coexist with persistent vulnerability | no causal recovery after the pulse |
| Coding theory | erasure threshold plus explicit reconstruction | arbitrary-erasure tolerance has a reproducible threshold and decoder-like recovery | no stable symbols/threshold/recovery map |
| Adversarial robustness | best-response gap and local-to-global failure | training-attack robustness vanishes under an independent best response | no off-diagonal loss |
| Fault-tolerant systems | fault containment and N-version diversity | independent functional origins, not copies, raise local joint-cut cost | shared fault remains as cheap as one local fault |

### Missing-variable hypotheses

1. **Safety-only mode persistence:** attack gradients that remain aligned across steps yield low long-horizon cost even if the initial slope is modest.
2. **Policy-margin tail density:** many near-boundary prompts cause abrupt population breach under a small edit despite the same mean margin.
3. **Output-routing concentration:** a small late routing support predicts A1/A4 vulnerability after controlling activation complexity.
4. **Hazard-capability accessibility:** absence of the underlying capability can masquerade as durable policy.
5. **Cross-prompt/domain stability:** a fault domain found on one prompt family may disappear out of distribution.
6. **Breach-channel volume:** the fraction of initializations entering unsafe-useful corridors may determine search work independently of the best norm.
7. **Backup wake-up latency:** recovery after the first harmful commitment token is operationally useless.
8. **Utility observability gap:** an incomplete benign panel creates false entanglement and false breach qualification.
9. **Signed causal compensation:** opposing safety and anti-safety effects can create non-monotonic ablation without redundancy.
10. **Legitimate-adaptation plasticity:** a mechanism that raises tamper cost may simply make all future learning expensive.

## Sources

[^arditi]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^cones]: Wollschläger et al., [*The Geometry of Refusal in Large Language Models*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^coax]: Gong et al., [*Conditional Co-Ablation*](https://arxiv.org/abs/2607.01940), arXiv 2026.
[^neuro]: [*NeuroStrike*](https://www.ndss-symposium.org/ndss-paper/neurostrike-breaking-llm-safety-via-sub-percent-neuron-pruning/), NDSS.
[^localedit]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^deeprefusal]: Xie et al., [*DeepRefusal*](https://aclanthology.org/2025.findings-emnlp.956/), Findings of EMNLP 2025.
[^anydepth]: Zhang et al., [*Any-Depth Alignment*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^skin]: Lee et al., [*Skin-Deep*](https://arxiv.org/abs/2606.22676), arXiv 2026.
[^routing]: Guo et al., [*When Safety Routing Breaks*](https://arxiv.org/abs/2609.01455), Findings of EMNLP 2026 per arXiv record.
[^collapse]: Springer et al., [*The Geometry of Alignment Collapse*](https://arxiv.org/abs/2602.15799), arXiv 2026.
[^tar]: Tamirisa et al., [*Tamper-Resistant Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^tamperbench]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^reparam]: Dinh et al.-style parameterization warning, operationalized here through function-space rather than raw weight norms; see [reparameterization study](https://proceedings.neurips.cc/paper_files/paper/2023/hash/395371f778ebd4854b88521100af30ad-Abstract-Conference.html).
[^separate]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^harc]: Chua et al., [*HARC*](https://arxiv.org/abs/2607.00572), arXiv 2026.
[^neurons]: Chen et al., [*Safety Neurons*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html), NeurIPS 2025.
[^failclosed]: Coalson et al., [*Fail-Closed Alignment for Large Language Models*](https://arxiv.org/abs/2602.16977), arXiv 2026.
