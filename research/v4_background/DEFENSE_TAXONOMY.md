# Safeguard and Defense Taxonomy

## 1. “Safety” is not one endpoint

| Safeguard object | Desired property | Failure evidence | Appropriate endpoint |
|---|---|---|---|
| Refusal behavior | decline disallowed requests | compliance after attack | content-level harmful compliance, not refusal strings |
| Safe completion | provide useful bounded help | refusal or actionable harmful detail | policy rubric + helpfulness |
| Policy following | obey contextual rules/authority | policy override or inconsistent decisions | scenario-specific violation rate |
| Over-refusal control | answer benign/dual-use requests | indiscriminate refusal | XSTest/OR-Bench plus human rubric |
| Capability suppression | cannot perform a dangerous task | task success after elicitation | domain task success, not conversational tone |
| Knowledge removal | information not internally recoverable | relearning, probing, quantization recovery | multi-path extraction and relearning frontier |
| Integrity | unauthorized changes do not silently remove safeguards | weight/activation/config tampering | attack cost + detectability + utility |
| Misuse reduction | lower real cyber/bio/fraud/persuasion uplift | successful end-to-end task | domain-specific controlled evaluation |

Refusal is therefore one model behavior, not the definition of defense.

## 2. Model-level versus system-level controls

### Model-internal

- pretraining data filtering or safety pretraining;
- unlearning/capability suppression;
- robust post-training and adversarial/meta training;
- representation/circuit rerouting and reconstruction;
- weight-space regularization/projection;
- architectural redundancy or self-degradation behavior.

These remain in the artifact after release, so they are the correct scope for open-weight tamper-resistance research.

### Trusted-runtime or system-level

- input/output classifiers and policy engines;
- controlled API, rate limits, identity and abuse monitoring;
- signed checkpoints, attestation, TEE/encrypted execution;
- tool permissions, sandboxes, human approval and audit logs;
- external retrieval filtering and action validation.

These can be highly effective in deployments with an enforceable boundary. They are **not properties of a public checkpoint**. They should be discussed as defense-in-depth, not counted as evidence that the released weights remain safeguarded.

## 3. Defense mechanisms

### Type I — Ordinary post-training alignment

**Mechanism:** SFT/DPO/RL teaches refusal or safe completion.
**Strength:** cheap, direct, high clean safety.
**Weakness:** often produces a thin behavioral wrapper; susceptible to prompt, prefill, activation, weight edit and short fine-tuning.
**Open-weight claim ceiling:** baseline safeguard, not tamper-resistant defense.

### Type II — Alignment-stage perturbation robustness

Representative methods: Vaccine, Booster, RepNoise.

- Vaccine adversarially perturbs hidden embeddings during alignment.[^vaccine]
- Booster simulates harmful weight perturbations and penalizes resulting harmful-loss reduction.[^booster]
- RepNoise removes/noises harmful representations across layers.[^repnoise]

These methods are genuine model-internal retrofits, but the ICLR 2025 audit shows durability can collapse under minor attacker/evaluator changes.[^audit]

### Type III — Bilevel/meta tamper-aware training

Representative methods: TAR and AntiDote.

- TAR differentiates approximately through inner-loop tampering trajectories using first-order meta-learning.[^tar]
- AntiDote uses an activation-conditioned hypernetwork to generate adversarial LoRA weights while a defender LoRA learns to nullify them.[^antidote]

**Promise:** train directly for post-attack safety.
**Risk:** the inner adversary defines the invariance learned; full-weight, new-data, direct-edit and composed attacks may lie outside it.
**Cost:** more than ordinary SFT; TAR’s public implementation recommends 8×A100-80GB for 8B full-parameter training, while AntiDote reports lower PEFT-based costs.[^tar-code]

### Type IV — Representation/circuit rerouting and contrastive separation

Representative methods: Circuit Breakers, LAT, Triplet/CRL, ReFAT.

- Circuit Breakers reroute harmful internal trajectories instead of merely fitting refusal strings.[^cb]
- LAT trains against optimized residual perturbations.
- ReFAT uses refusal-feature ablation as an adversarial training perturbation.[^refat]
- Triplet/CRL separates benign, harmful and adversarial representations with hard negatives.[^triplet]

These can transfer across input/latent attacks, but an independent Circuit Breaker reevaluation obtained 100% ASR with simple embedding-attack changes.[^cb-audit] TamperBench finds substantial remaining vulnerability under broader sweeps.[^tb]

### Type V — Internal fault injection and reconstruction

Representative methods: DeepRefusal, NeuronGuard, SafeNeuron.

- DeepRefusal randomly ablates refusal directions across layers/tokens during LoRA safety training, forcing re-triggering.[^deeprefusal]
- NeuronGuard and SafeNeuron aim to redistribute or preserve safety under neuron faults; both are very recent and require independent validation.

**Key distinction:** surviving the injected fault does not establish independent failure domains. Evaluation must re-extract attack features after defense and include a non-neuron, non-directional attack.

### Type VI — Make malicious modification destroy utility

Representative methods: SDD and SEAM.

- SDD trains high-quality irrelevant responses so malicious FT degrades general capability.[^sdd]
- SEAM couples harmful and benign optimization trajectories to create a “no-win” utility collapse under stronger attacks.[^seam]

This family directly targets the attacker’s utility constraint and is conceptually aligned with work-factor evaluation. The unresolved question is whether the coupling survives a defense-aware attacker who changes objective, layers, optimizer, initialization, or repairs utility afterward.

### Type VII — Constrain or repair downstream adaptation

Representative methods: SafeLoRA, Lisa, Antibody, Antidote (ICML 2025), SDD as service deployment.

- SafeLoRA projects LoRA updates into a safety-aligned subspace and is training/data-free once base and aligned checkpoints exist.[^safelora]
- Lisa alternates safety and user-data optimization with a proximal term.[^lisa]
- Antibody reweights harmful gradients during provider-controlled fine-tuning.[^antibody]
- ICML Antidote prunes harmful parameters after fine-tuning.[^prune]

These are valuable for **fine-tuning-as-a-service**, where the defender controls training or post-FT repair. They are not standalone protection after unconditional open-weight release because the attacker can omit the procedure.

### Type VIII — Generation-depth/runtime recovery

Representative methods: Any-Depth Alignment, DeepRefusal, decoding-time steering, latent guards.

Any-Depth Alignment reintroduces safety-associated assistant header tokens during generation and reports near-100% refusal under long prefills with negligible overhead.[^ada] Latent Guard uses internal harmfulness representation for detection.[^harm]

These clarify mechanisms and can protect trusted inference. Under full inference control, the attacker can disable the hook, so they are not persistent checkpoint integrity measures.

### Type IX — Capability prevention/removal

Representative methods: unlearning, Safety Pretraining, Deep Ignorance.

- Unlearning aims to remove selected data/knowledge after training, but many methods are vulnerable to benign relearning and activation/weight recovery.[^relearn][^hide]
- Safety Pretraining filters/rephrases unsafe data and adds native refusal/tags, improving input robustness in smaller pretraining experiments.[^safety-pre]
- Deep Ignorance filters dual-use biology data before matched 6.9B, 550B-token pretraining and obtains the strongest long-horizon tamper-resistance evidence in that narrow setting.[^deep]

This family changes the object from “will not answer” to “does not internally possess enough capability.” It is expensive, domain-dependent, hard to retrofit, and bypassable when knowledge is supplied in context.

### Type X — Obfuscation/aliasing against a known edit

AMRA applies rank-k updates to writer matrices, substitutes random aliases for refusal activations, and corrects downstream readers, improving resistance to standard abliteration with mixed utility tradeoffs.[^amra]

This is a valid narrow defense but should be evaluated against defense-aware re-extraction and multi-direction/automated edits. Hiding a coordinate system is not the same as increasing functional attack cost.

## 4. Cross-family comparison

| Family | Works after unrestricted weight release? | Retrofit? | Zero inference overhead? | Strongest supported threat | Central caveat |
|---|---:|---:|---:|---|---|
| Ordinary alignment | yes | yes | yes | weak prompt baseline | easily removed |
| Perturbation robustness | yes | yes | yes | matched/nearby FT or latent attacks | evaluation sensitivity |
| Bilevel/meta | yes | yes | yes | trained update families | expensive; adversary mismatch |
| Rerouting/contrastive | yes | yes | yes | several input/latent families | adaptive embedding/FT breaks |
| Fault reconstruction | yes | yes | yes | direction/neuron/prefill faults | overfit to injected fault |
| Self-degradation | yes | yes | yes | malicious FT under utility constraint | repair/decoupling attack |
| Controlled adaptation | no, if attacker omits it | yes | yes | provider-controlled FT | wrong threat model for public weights |
| Runtime recovery | no, if runtime untrusted | yes | no/low | prefill/decoding attacks | removable hook |
| Capability prevention | yes | mostly no | yes | long domain relearning | high cost; context supply |
| Alias/obfuscation | yes | yes | yes | standard abliteration | adaptive re-extraction |

## 5. What “generalization” must mean

Four different claims are often collapsed:

1. **Data generalization:** new prompts from the same harm distribution.
2. **Model generalization:** another checkpoint/family/scale.
3. **Attack generalization:** a distinct intervention locus or optimization bias.
4. **Adaptive robustness:** an attacker sees the defense and changes the attack.

Only 3 and 4 materially support attack-family-general model defense. Reporting 52 prompt variants may establish data breadth while leaving the intervention bias nearly unchanged.

## 6. Defense evaluation rules

A defense card must state:

- safeguard target and whether capability remains;
- exact attacker privileges and what the attacker knows;
- whether evaluation attacks differ from training adversaries;
- strongest attack found under a public search budget;
- clean safety, over-refusal and actual harmful-task score;
- utility-constrained frontier over several thresholds;
- defender and attacker cost using identical accounting;
- model-family, scale and seed coverage;
- independent versus author-only validation;
- inference assumptions and removable external components.

The normalized cards are in [DEFENSE_EVIDENCE_TABLE.csv](DEFENSE_EVIDENCE_TABLE.csv).

## 7. Recommended scope judgment

The scope `model-internal tamper resistance for open-weight models` is appropriate only if it is phrased as **bounded, comparative resistance**, not permanent safety. The primary object should include behavior and capability safeguards; refusal can remain the cheapest experimental proxy, but conclusions must not silently generalize to cyber/bio/fraud task capability.

## Sources

[^vaccine]: Huang et al., [Vaccine](https://proceedings.neurips.cc/paper_files/paper/2024/hash/873c86d9a979ab80d8e2919510d4446b-Abstract-Conference.html), NeurIPS 2024.
[^booster]: Huang et al., [Booster](https://proceedings.iclr.cc/paper_files/paper/2025/hash/a7ac8a21e5a27e7ab31a5f42a0117bdb-Abstract-Conference.html), ICLR 2025.
[^repnoise]: Rosati et al., [RepNoise](https://proceedings.neurips.cc/paper_files/paper/2024/hash/172be8b0b88fc2b4aee74237d43f8c04-Abstract-Conference.html), NeurIPS 2024.
[^audit]: Qi et al., [durability audit](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^tar]: Tamirisa et al., [TAR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025.
[^antidote]: Sanyal et al., [AntiDote](https://ojs.aaai.org/index.php/AAAI/article/view/40570), AAAI 2026.
[^tar-code]: [TAR official code](https://github.com/rishub-tamirisa/tamper-resistance).
[^cb]: Zou et al., [Circuit Breakers](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97ca7168c2c333df5ea61ece3b3276e1-Abstract-Conference.html), NeurIPS 2024.
[^refat]: Yu et al., [ReFAT](https://arxiv.org/abs/2409.20089), arXiv 2024–2025.
[^triplet]: Simko et al., [Triplet/CRL](https://arxiv.org/abs/2506.11938), 2025.
[^cb-audit]: Schwinn & Geisler, [independent Circuit Breaker evaluation](https://arxiv.org/abs/2407.15902), 2024.
[^tb]: Hossain et al., [TamperBench](https://arxiv.org/abs/2602.06911), KDD 2026 D&B.
[^deeprefusal]: Xie et al., [DeepRefusal](https://aclanthology.org/2025.findings-emnlp.956/), Findings EMNLP 2025.
[^sdd]: Chen et al., [SDD](https://aclanthology.org/2025.acl-long.1412/), ACL 2025.
[^seam]: Wang et al., [SEAM](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1abb0e7bd62ba80610798dee81950522-Abstract-Conference.html), ICLR 2026.
[^safelora]: Hsu et al., [SafeLoRA](https://proceedings.neurips.cc/paper_files/paper/2024/hash/77baa7c2a3a675823e89131698fd6e19-Abstract-Conference.html), NeurIPS 2024.
[^lisa]: Huang et al., [Lisa](https://proceedings.neurips.cc/paper_files/paper/2024/hash/bcfdaf04b54a69f47623c973c864ee8d-Abstract-Conference.html), NeurIPS 2024.
[^antibody]: Nguyen et al., [Antibody](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c5d822eeba0e87592d8ed1d2168a62f0-Abstract-Conference.html), ICLR 2026.
[^prune]: Huang et al., [Antidote post-FT pruning](https://proceedings.mlr.press/v267/huang25b.html), ICML 2025.
[^ada]: Zhang et al., [Any-Depth Alignment](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2bb0db7d7081037aada48aafbeae717d-Abstract-Conference.html), ICLR 2026.
[^harm]: Zhao et al., [harmfulness/refusal separation](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025.
[^relearn]: Hu et al., [Unlearning or Obfuscating?](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^hide]: Yang et al., [Erase or Hide?](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^safety-pre]: Maini et al., [Safety Pretraining](https://proceedings.neurips.cc/paper_files/paper/2025/hash/3e84c4e0acee2be072571fedc70700a9-Abstract-Conference.html), NeurIPS 2025.
[^deep]: O'Brien et al., [Deep Ignorance](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^amra]: Truong, [Abliteration Mitigation via Refusal Aliases](https://arxiv.org/abs/2608.18093), arXiv 2026.
