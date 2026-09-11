# Paper notes — model editing and unlearning robustness

## Hase et al. — *Does Localization Inform Editing?*

- **Authors / status / date:** Hase et al.; NeurIPS 2023 main conference; December 2023.
- **Question:** Does a causal activation-localization peak identify where parameters should be edited?
- **Mechanism:** Compare causal tracing with layer-restricted editing efficacy and specificity.
- **Result:** Localization and editability can be statistically unrelated.
- **Strongest evidence:** Cross-layer scatter/ranking mismatch between causal tracing and edit success.
- **Limitation:** Factual editing, not safety; exact result depends on editing algorithms and facts.
- **Relation:** The most important methodological collision: where refusal acts need not be where it is cheapest to break.
- **Source:** [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html).

## Lee et al. — *Does Localization Inform Unlearning?*

- **Authors / status / date:** Lee et al.; EMNLP 2025 main conference; November 2025.
- **Question:** Does parameter attribution uniquely locate where knowledge must be changed for unlearning?
- **Mechanism:** Controlled localized-update experiments.
- **Result:** Effective unlearning is not uniquely determined by the parameter set identified by localization.
- **Endpoint:** Forgetting with utility retention.
- **Limitation:** Knowledge forgetting differs from behavioral safeguards.
- **Relation:** Extends the localization/editability warning to a safeguard-like setting.
- **Source:** [ACL Anthology](https://aclanthology.org/2025.emnlp-main.1109/).

## Guo et al. — *Mechanistic Unlearning*

- **Authors / status / date:** Guo et al.; ICML 2025 main conference; July 2025.
- **Question:** Can high-level mechanism localization improve durable knowledge removal?
- **Mechanism:** Target fact-lookup mechanisms with predictable intermediate states.
- **Result / endpoint:** Better paraphrase generalization and resistance to relearning than shallower localization baselines.
- **Strongest evidence:** Robustness comparison under paraphrase and relearning attacks.
- **Limitation:** It supports the value of correct mechanism localization, not a generic equivalence between localization and editability.
- **Relation:** Positive counterweight to the two negative localization papers; motivates explicit cross-space tests.
- **Source:** [PMLR](https://proceedings.mlr.press/v267/guo25k.html).

## Hu et al. — *Unlearning or Obfuscating?*

- **Authors / status / date:** Hu et al.; ICLR 2025 main conference; April 2025.
- **Question:** Do unlearning methods erase knowledge or suppress access?
- **Mechanism:** Benign, loosely related relearning attacks across unlearning benchmarks.
- **Result:** Apparently forgotten knowledge often reappears after benign fine-tuning.
- **Endpoint:** Relearning durability under utility-preserving updates.
- **Strongest evidence:** Recovery curves under innocuous data.
- **Limitation:** Access suppression and refusal are analogous but not identical.
- **Relation:** Strong prior for “behavioral success can be a shallow inhibitor.”
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html).

## Yang et al. — *Erase or Hide?*

- **Authors / status / date:** Yang et al.; ICLR 2026 main conference; April 2026.
- **Question:** Why does forgotten knowledge reappear?
- **Mechanism:** Attribution separates knowledge-bearing influence from learned negative inhibitors.
- **Result:** Many methods hide knowledge with spurious suppressors; suppressor-avoiding training improves robustness.
- **Endpoint:** Adversarial and benign retraining durability.
- **Strongest evidence:** Identification and suppression of unlearning neurons followed by recovery tests.
- **Limitation:** A neuron-level inhibitor in unlearning is not automatically a refusal writer.
- **Relation:** Close conceptual collision with “one shared safety fuse,” while also offering a cross-domain natural test.
- **Source:** [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html).

## Yu et al. — *Adversarial Parameter Attack on Deep Neural Networks*

- **Authors / status / date:** Yu et al.; ICML 2023 main conference; July 2023.
- **Question:** Can small parameter perturbations stealthily destroy a robustness property?
- **Mechanism:** Norm-constrained adversarial parameter optimization.
- **Result:** Small edits preserve standard accuracy while collapsing adversarial robustness.
- **Endpoint:** Utility-preserving parameter tampering in classifiers.
- **Limitation:** Parameter norm is coordinate-dependent; classification threat models differ from open-weight LLM training.
- **Relation:** Generic prior for common-mode parameter attacks and constrained editability.
- **Source:** [PMLR](https://proceedings.mlr.press/v202/yu23f.html).
