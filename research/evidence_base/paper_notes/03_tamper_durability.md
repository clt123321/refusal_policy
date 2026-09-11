# Paper notes — open-weight tamper durability

## Tamirisa et al. — *Tamper-Resistant Safeguards for Open-Weight LLMs*

- **Authors / status / date:** Tamirisa et al.; ICLR 2025 main conference; April 2025.
- **Question:** Can safeguards resist adversarial parameter updates?
- **Mechanism:** First-order meta-learning against inner-loop tampering.
- **Result / endpoint:** Tested tamper resistance can be materially increased under utility-constrained adversarial fine-tuning.
- **Strongest evidence:** Safety-versus-attack-training curves for hardened and baseline models under several attacks.
- **Limitation:** Durability remains threat-model and optimizer dependent; later evaluation work shows rankings can change.
- **Relation:** Defines the target endpoint and collides with a generic bilevel defense.
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html).

## Qi et al. — *On Evaluating the Durability of Safeguards for Open-Weight LLMs*

- **Authors / status / date:** Qi et al.; ICLR 2025 main conference; April 2025.
- **Question:** How stable are durability conclusions under stronger evaluation?
- **Mechanism:** Adaptive replication over seeds, trainers, schedules and data formats.
- **Result:** Small implementation changes overturn several reported robustness conclusions.
- **Endpoint:** Worst-found safety under bounded adaptive attacks.
- **Strongest evidence:** Re-ranking of safeguards after modest attack adaptation.
- **Limitation:** An attack suite gives an upper bound on the unknown minimum breach cost, not a certificate.
- **Relation:** Fatal to a generic BreachCost-evaluation novelty and imposes an adaptive-evaluation standard.
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html).

## Hossain et al. — *TamperBench*

- **Authors / status / date:** Hossain et al.; KDD 2026 Datasets & Benchmarks track, oral; August 2026.
- **Question:** Can fine-tuning/tampering evaluation be standardized across attacks and models?
- **Mechanism:** Nine attacks × 21 models with pair-specific hyperparameter search and utility ceilings.
- **Result:** Attack rankings are model-specific; jailbreak tuning is often strongest.
- **Endpoint:** Worst-found utility-constrained safety over an attack portfolio.
- **Strongest evidence:** Model-by-attack matrix and adaptive frontier.
- **Limitation:** It diagnoses robustness but does not explain internal mechanisms; the minimum cost remains attack-relative.
- **Relation:** Fatal to “another tamper benchmark”; ideal held-out security endpoint for a mechanism predictor.
- **Sources:** [paper](https://arxiv.org/abs/2602.06911), [code](https://github.com/criticalml-uw/TamperBench), [DOI](https://doi.org/10.1145/3770855.3817557).

## O’Brien et al. — *Deep Ignorance*

- **Authors / status / date:** O’Brien et al.; ICLR 2026 main conference; April 2026.
- **Question:** Is never learning hazardous knowledge more durable than suppressing access later?
- **Mechanism:** Matched 6.9B models with filtered pretraining and long adaptive fine-tuning attacks.
- **Result:** Pretraining exclusion is substantially harder to reverse than post-hoc safeguards, although context can restore some access.
- **Endpoint:** Up to 10k attack steps / 300M tokens with utility controls.
- **Strongest evidence:** Long-horizon relearning/tamper frontier separating deep ignorance from post-hoc suppression.
- **Limitation:** Expensive and specific to hazardous capability access rather than refusal alone.
- **Relation:** Counterexample to refusal-only generalization and evidence that safeguard provenance matters.
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html).

## Sanyal et al. — *AntiDote*

- **Authors / status / date:** Sanyal et al.; AAAI 2026 main conference; March 2026.
- **Question:** Can bilevel training harden models against malicious fine-tuning?
- **Mechanism:** Hypernetwork-generated LoRA attacks inside bilevel optimization.
- **Result / endpoint:** Reported robustness improvements under weight, latent and input red-team attacks with small measured utility cost.
- **Limitation:** Robustness is conditional on the learned inner attacker and test portfolio.
- **Relation:** High collision with any proposed low-cost adversarial-training defense.
- **Source:** [AAAI paper](https://ojs.aaai.org/index.php/AAAI/article/download/40570/44531).

## Kuo et al. — *Open-Weight LLM Fine-Tuning Defenses Are Susceptible to Simple Attacks*

- **Authors / status / date:** Kuo et al.; arXiv preprint; May 2026.
- **Question:** Do sophisticated fine-tuning defenses survive cheap non-training attacks?
- **Mechanism:** Abliteration and prefilling against defended checkpoints.
- **Result:** Simple attacks reportedly raise attack success sharply; representation adversarial training only partly mitigates them.
- **Endpoint:** Cheap activation/weight-derived and prefill attacks.
- **Limitation:** Preprint; endpoint and model coverage must be checked against formal benchmarks.
- **Relation:** Forces cheap attacks into the earliest feasibility gate.
- **Source:** [arXiv](https://arxiv.org/abs/2605.26526).
