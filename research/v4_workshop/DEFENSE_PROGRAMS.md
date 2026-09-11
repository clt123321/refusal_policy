# Defense Program Workshop

Six roles independently proposed at most two programs each. Similar proposals remain separate here so agreement is not manufactured before red-team review.

## 1. Mechanistic Safety

### M1 — Perturb-and-reconstruct safety routing

- **problem:** Harm recognition can remain while prompt-boundary or late-output routing stops controlling generation.
- **one-sentence principle:** Damage safety routes at varied layers and token positions during training, and require later computation to reconstruct a safe action from surviving evidence.
- **why it may generalize:** The learned object is recovery after a route cut, potentially shared by prefill, activation and local-weight faults.
- **closest prior work:** DeepRefusal, Any-Depth Alignment, DeRTa, HARC, and When Safety Routing Breaks.[^deeprefusal][^ada][^derta][^harc][^routing]
- **expected attack coverage:** Prefill, prompt jailbreak, direction/late-MLP edits and small LoRA; not long full FT or runtime deletion.
- **defender cost:** Retrofit; roughly 1.5–3× safety tuning; potentially zero inference overhead.
- **utility risk:** Repeated safety checks can increase over-refusal and distort long-form generation.
- **killer experiment:** Train on three route-cut types and test held-out Heretic, late-MLP edit and benign LoRA frontiers.
- **falsifier:** Gains are diagonal-only, disappear under one held-out edit, or require >1% utility loss.

### M2 — Heterogeneous parameter fault domains

- **problem:** Many activation carriers can share one parameter-level failure mode.
- **one-sentence principle:** Train two individually sufficient safety paths with disjoint parameter sensitivity and require each to survive removal of the other.
- **why it may generalize:** An attacker must cross multiple functional fault domains rather than evade one named detector or direction.
- **closest prior work:** Concept Cones, Safety Neurons, DeepRefusal, and diverse-refusal training; none establishes parameter-level failure independence.[^cones][^neurons][^deeprefusal][^reflects]
- **expected attack coverage:** Directional, neuron/module, low-rank direct edits and local LoRA; bounded short full FT.
- **defender cost:** Retrofit; approximately 2–4× safety tuning; zero inference overhead if implemented without extra branches.
- **utility risk:** Capacity waste, shared-output-head collapse, and over-refusal through duplicated policies.
- **killer experiment:** Compare ordinary multi-direction safety with two parameter-separated paths under post-defense re-extracted joint edits and held-out LoRA.
- **falsifier:** One low-rank global mode still removes both paths at baseline cost.

## 2. Adversarial ML

### A1 — Functional-constrained cross-operator adversarial training

- **problem:** Robustness to the training-time attack often fails when the intervention basis changes.
- **one-sentence principle:** Optimize worst-case safety across activation, direct-weight and gradient-update operators subject to a benign-functional constraint.
- **why it may generalize:** The constraint matches the unsafe-but-useful endpoint and the operator set covers distinct local attack biases.
- **closest prior work:** TAR, AntiDote, ART, Booster and LAT; each emphasizes a narrower inner adversary.[^tar][^antidote][^art]
- **expected attack coverage:** Short LoRA/full FT, activation ablation, low-rank/sparse edit and some prefill; not retraining or architecture replacement.
- **defender cost:** Medium–high; several inner attack passes, but cheaper than full TAR in a PEFT prototype.
- **utility risk:** Reduced normal plasticity or broad functional flattening.
- **killer experiment:** Train on two operator classes; hold out Heretic/direct edit, jailbreak tuning and prefill; compare off-diagonal breach-cost gains with specialist defenses.
- **falsifier:** No ≥2× held-out breach-cost gain at <1% utility loss.

### A2 — Attack-program adversarial training

- **problem:** A real attacker composes breach, capability supply and utility repair rather than choosing one benchmark primitive.
- **one-sentence principle:** Optimize against bounded two-stage attack programs instead of isolated attack algorithms.
- **why it may generalize:** Composition exposes side-effect repair and operator interaction absent from single-stage robustness.
- **closest prior work:** TAR optimizes trajectories; TamperBench sweeps separate attacks; Deep Ignorance demonstrates staged FT-plus-retrieval failure.[^tar][^tb][^deep]
- **expected attack coverage:** Edit→repair, FT→retrieval and jailbreak-tuning sequences; not unbounded program length.
- **defender cost:** High due to discrete operator search and nested optimization.
- **utility risk:** Suppresses useful fine-tunability and overfits a small program grammar.
- **killer experiment:** At matched defender compute, compare defense against the strongest single attack with defense against two-stage programs, then reverse the held-out operator order.
- **falsifier:** Changing stage order or adding one unseen operator restores baseline attack success.

## 3. Reliability / Systems

### R1 — Minimum joint safety cut

- **problem:** Component count and activation rank do not measure how many independent changes are required to disable safety.
- **one-sentence principle:** Maximize the minimum utility-constrained joint cut across heterogeneous parameter and temporal fault domains.
- **why it may generalize:** Minimum cut concerns failure structure rather than attack implementation.
- **closest prior work:** Concept Cones supplies functional-independence tests; Refusal Geometry Reflects Refusal Training raises activation rank; neither trains a parameter joint cut.[^cones][^reflects]
- **expected attack coverage:** Re-extracted direction edits, sparse modules, local LoRA and route cuts; weak against unrestricted FT.
- **defender cost:** Medium; multiple fault passes and path-discovery overhead.
- **utility risk:** Artificial partitions can be coordinate artifacts or share a final output bottleneck.
- **killer experiment:** Compare equal-cost same-domain and heterogeneous-domain training using a post-defense adaptive rank-\(r\) joint edit.
- **falsifier:** A shared output edit defeats all domains without extra cost.

### R2 — Repair-closed safety–utility coupling

- **problem:** Self-degradation only helps if an attacker cannot repair utility while preserving the breach.
- **one-sentence principle:** Make every low-cost trajectory that restores benign utility also restore the safeguard.
- **why it may generalize:** It directly targets the attacker’s unsafe-and-useful feasible set, including multi-stage repair.
- **closest prior work:** SDD and SEAM create initial safety–utility coupling; neither establishes closure under adaptive utility repair.[^sdd][^seam]
- **expected attack coverage:** Harmful LoRA/full FT and direct-edit→benign-repair; not prompt-only attacks.
- **defender cost:** High; break→repair inner loops, initially approximated with first-order PEFT.
- **utility risk:** Legitimate adaptation may be blocked; “safety” may be capability collapse.
- **killer experiment:** Plot unsafe–utility repair trajectories for SFT, TAR, SDD, SEAM and repair-closed training.
- **falsifier:** ≤2× baseline attack cost recovers <1% utility loss while keeping high harmful task success.

## 4. Capability Control / Unlearning

### C1 — Reacquisition-invariant capability suppression

- **problem:** Many unlearning methods hide knowledge that reappears after small updates.
- **one-sentence principle:** Minimize dangerous capability and its fastest recovery direction across diverse downstream-update environments.
- **why it may generalize:** Different retraining methods share the need to rebuild a dangerous input–output mapping.
- **closest prior work:** Invariant unlearning, smoothness-aware unlearning and TAR already occupy much of this objective.[^invariant][^smooth][^tar]
- **expected attack coverage:** Relearning, benign/harmful LoRA and short full FT; not retrieval, context or activation bypass.
- **defender cost:** Medium–high; 2–5× ordinary unlearning.
- **utility risk:** Damage to adjacent scientific knowledge and normal learnability.
- **killer experiment:** Train with one update environment; test held-out optimizer, rank, full FT and model merge using recovery sample complexity.
- **falsifier:** A representation or optimizer change returns recovery cost to baseline.

### C2 — Capability-supply closure

- **problem:** Capability absent from weights can be supplied through context, retrieval, tools, merging or training.
- **one-sentence principle:** Close multiple capability-supply channels rather than treating the checkpoint as a closed system.
- **why it may generalize:** It evaluates actual task completion across weights, context, tools and gradients.
- **closest prior work:** Deep Ignorance demonstrates both durable pretraining filtering and failures under context/search/staged attacks.[^deep]
- **expected attack coverage:** Relearning, retrieval and context supply if runtime remains trusted; not arbitrary owner modification.
- **defender cost:** Very high; likely pretraining plus system controls, not a cheap retrofit.
- **utility risk:** Harms general retrieval, transfer and scientific reasoning.
- **killer experiment:** Measure equal-information capability supply via weights, context, retrieval and updates on filtered versus post-hoc-unlearned models.
- **falsifier:** A short context or small retrieval corpus restores task capability, or blocking it damages benign RAG.

## 5. Security Red Team

### S1 — Defense by adaptive-repair resistance

- **problem:** A first-stage attack may look costly only because it leaves easily repairable utility damage.
- **one-sentence principle:** Treat explicit utility repair as part of every breach attack and accept a defense only if the joint attack remains expensive.
- **why it may generalize:** Every utility-coupled defense faces the same attacker incentive independent of model geometry.
- **closest prior work:** SEAM, SDD, the durability audit and staged Deep Ignorance attacks.[^seam][^sdd][^audit][^deep]
- **expected attack coverage:** FT/edit defenses that claim a safety–utility trade-off; not an independent protection against prompt attacks.
- **defender cost:** Low as an evaluation principle; high if made a bilevel training objective.
- **utility risk:** None for auditing; training may destroy adaptability.
- **killer experiment:** Breach SDD/SEAM, then repair with benign replay, KL retention, layer-selective updates and adapter merge.
- **falsifier:** If repair trivially works, the defense program is rejected; if it never works, the training principle survives.

### S2 — Two-resource safeguard

- **problem:** Refusal and capability suppression each expose one cheap bypass route.
- **one-sentence principle:** Require an attacker to both supply missing dangerous capability and independently remove a safe-action policy.
- **why it may generalize:** The two costs consume different resources—knowledge/data versus policy editing—if their fault domains are truly separate.
- **closest prior work:** Deep Ignorance provides capability prevention; Any-Depth provides a policy layer; their combination and staged failure are already close.[^deep][^ada]
- **expected attack coverage:** Relearning/context supply plus prompt/prefill/edits; not model replacement.
- **defender cost:** Prohibitive for new pretraining; moderate only with weaker unlearning proxies.
- **utility risk:** Knowledge filtering and over-refusal compound.
- **killer experiment:** A 2×2 internal-capability × reconstructed-policy natural experiment with context supply × policy ablation attacks.
- **falsifier:** One lightweight update simultaneously restores capability and removes policy.

## 6. Top-conference AC

### T1 — Utility-constrained functional safety margin

- **problem:** Parameter norm, attack steps and attack count are coordinate- and implementation-dependent.
- **one-sentence principle:** Maximize distance in benign function space from a safe model to the nearest unsafe-but-useful model.
- **why it may generalize:** The object is defined by the behavioral endpoint rather than optimizer or parameterization.
- **closest prior work:** Durability Audit formalizes bounded claims; TAR, Booster and AntiDote approximate attack-specific inner maxima.[^audit][^tar][^antidote]
- **expected attack coverage:** Any parameter attack represented by the inner search; not model replacement or omitted utility dimensions.
- **defender cost:** High; constrained inner optimization over several utility batches.
- **utility risk:** Overfits the utility calibration set and can reward over-refusal.
- **killer experiment:** Before training, test whether estimated functional margin predicts held-out direct-edit/LoRA/full-FT breach ordering across checkpoints.
- **falsifier:** The estimated margin fails prospective attack ranking or vanishes with a stronger optimizer.

### T2 — Intervention-operator basis training

- **problem:** Many named attacks can share one optimization bias, so attack count exaggerates coverage.
- **one-sentence principle:** Train against a minimal basis of intervention operators and reserve a complete operator class as blind holdout.
- **why it may generalize:** Off-diagonal transfer would show shared local structure rather than memorization of attack recipes.
- **closest prior work:** Vaccine, Booster, TAR, DeepRefusal, AntiDote and Skin-Deep collectively cover the neighboring space.[^deeprefusal][^antidote][^skin]
- **expected attack coverage:** Local activation, direct-weight and gradient updates; not retrieval, long retraining or architecture changes.
- **defender cost:** Medium–high; multiple adversary passes, zero inference overhead.
- **utility risk:** Gradient masking or suppression of normal plasticity.
- **killer experiment:** A 3×3 train-operator/test-operator transfer matrix with stronger black-box/evolutionary verification.
- **falsifier:** Only diagonal robustness improves or a non-gradient optimizer removes the gain.

## Sources

[^deeprefusal]: Xie et al., [DeepRefusal](https://aclanthology.org/2025.findings-emnlp.956/), Findings EMNLP 2025.
[^ada]: Zhang et al., [Any-Depth Alignment](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^derta]: Yuan et al., [DeRTa](https://aclanthology.org/2025.acl-long.158/), ACL 2025.
[^harc]: Chua et al., [HARC](https://arxiv.org/abs/2607.00572), arXiv 2026.
[^routing]: Guo et al., [When Safety Routing Breaks](https://arxiv.org/abs/2609.01455), Findings EMNLP 2026.
[^cones]: Wollschläger et al., [Concept Cones](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^neurons]: Chen et al., [Safety Neurons](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html), NeurIPS 2025.
[^reflects]: Labunets, [Refusal Geometry Reflects Refusal Training](https://arxiv.org/abs/2608.25390), arXiv 2026.
[^tar]: Tamirisa et al., [TAR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^antidote]: Sanyal et al., [AntiDote](https://ojs.aaai.org/index.php/AAAI/article/view/40570), AAAI 2026.
[^art]: Kuo et al., [simple attacks and ART](https://arxiv.org/abs/2605.26526), arXiv 2026.
[^tb]: Hossain et al., [TamperBench](https://arxiv.org/abs/2602.06911), KDD 2026 D&B.
[^deep]: O'Brien et al., [Deep Ignorance](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^sdd]: Chen et al., [SDD](https://aclanthology.org/2025.acl-long.1412/), ACL 2025.
[^seam]: Wang et al., [SEAM](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1abb0e7bd62ba80610798dee81950522-Abstract-Conference.html), ICLR 2026.
[^invariant]: Wang et al., [Invariant Unlearning](https://proceedings.mlr.press/v267/wang25en.html), ICML 2025.
[^smooth]: Fan et al., [Smoothness-aware Unlearning](https://proceedings.mlr.press/v267/fan25e.html), ICML 2025.
[^audit]: Qi et al., [Durability Audit](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^skin]: Lee et al., [Skin-Deep](https://arxiv.org/abs/2606.22676), arXiv 2026.
