# Paper notes — safety mechanism decomposition

## Zhao et al. — *LLMs Encode Harmfulness and Refusal Separately*

- **Authors / status / date:** Zhao et al.; NeurIPS 2025 main conference; December 2025.
- **Question:** Is harm recognition identical to refusal?
- **Mechanism:** Position-aware direction extraction, causal steering and reversal tests.
- **Result / endpoint:** Harmfulness and refusal are causally separable; harm recognition often survives tested jailbreaks/fine-tuning. Endpoints include internal recognition and refusal behavior.
- **Strongest evidence:** Interventions change refusal without equivalently changing harmfulness judgments.
- **Limitation:** It does not directly quantify utility-constrained white-box removal cost.
- **Relation:** Requires this project to separate detection, policy and execution; fatal to novelty of that distinction.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html).

## Wu et al. — *Knowing without Acting*

- **Authors / status / date:** Wu et al.; arXiv preprint; March 2026.
- **Question:** How do harm recognition and refusal execution separate across depth?
- **Mechanism:** Double-difference extraction and adaptive steering.
- **Result / endpoint:** Recognition and execution axes dissociate and permit refusal erasure while knowledge of harm remains.
- **Limitation:** Preprint and primarily activation-level; it does not establish the cheapest parameter-space attack.
- **Relation:** Direct collision with a new H→policy→execution decomposition.
- **Source:** [arXiv](https://arxiv.org/abs/2603.05773).

## Lan et al. — *From Refusal Geometry to Safety Geometry*

- **Authors / status / date:** Lan et al.; arXiv preprint; June 2026.
- **Question:** Does coupling between harmfulness and refusal geometry diagnose safety under fine-tuning?
- **Mechanism:** Dual-geometry measurements across SFT/R2D2 trajectories and interventions.
- **Result:** Coupling is informative in some regimes; low coupling is not by itself a security guarantee.
- **Endpoint:** Limited fine-tuning/transfer attack behavior.
- **Limitation:** Geometry remains regime-dependent and does not solve adaptive attack evaluation.
- **Relation:** Strong evidence against treating one geometry score as a universal endpoint.
- **Source:** [arXiv](https://arxiv.org/abs/2606.16349).

## Chua and Wu — *HARC*

- **Authors / status / date:** Chua and Wu; arXiv preprint; July 2026.
- **Question:** Can explicit harm-recognition/refusal coupling improve robustness?
- **Mechanism:** Prompt- and response-position coupling losses trained with LoRA.
- **Result / endpoint:** Reported gains in jailbreak robustness, capability and over-refusal trade-offs.
- **Limitation:** Preprint; white-box adaptive durability is not the main endpoint.
- **Relation:** Fatal to coupling-as-defense novelty, but useful as a model family for a natural experiment.
- **Source:** [arXiv](https://arxiv.org/abs/2607.00572).

## Chu et al. — *From Detection to Refusal*

- **Authors / status / date:** Chu et al.; arXiv preprint v1; September 2026.
- **Question:** Which circuit links harm detection to refusal?
- **Mechanism:** Head/neuron interventions and circuit-guided weight scaling.
- **Result / endpoint:** Detection heads feed safety neurons and refusal heads across six models; scaling improves input-attack safety in the reported setting.
- **Limitation:** Very recent preprint; no mature adaptive white-box attack suite.
- **Relation:** High collision with safety writers, shared gate and mechanism-derived weight scaling.
- **Source:** [arXiv](https://arxiv.org/abs/2609.00051).

## Chen et al. — *Safety Neurons*

- **Authors / status / date:** Chen et al.; NeurIPS 2025 main conference; December 2025.
- **Question:** Which neurons mediate safety alignment?
- **Mechanism:** Activation contrasting and dynamic patching.
- **Result:** A small neuron subset restores much safety and overlaps with helpfulness mechanisms.
- **Endpoint:** Safety restoration and detection before generation.
- **Limitation:** A causal neuron set is not necessarily the cheapest parameter edit locus.
- **Relation:** Collision with canonical writer localization; also a reason to test utility entanglement.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/12a00d85a76fe258e1242c3aced03250-Abstract-Conference.html).
