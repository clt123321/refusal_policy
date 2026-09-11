# Concept map: from representations to durability

Audit cutoff: 2026-09-11. Status labels in `papers.csv` are authoritative for this audit; arXiv papers are not silently promoted to conference papers.

## The map

```text
training data / objective / optimizer
        │
        ├── creates or masks harmful capability
        │       ├── pretraining filtering / deep ignorance
        │       └── post-hoc suppression / unlearning inhibitors
        │
        ├── creates recognition signals
        │       └── harmfulness / semantic safety features
        │
        ├── creates action policy
        │       └── refusal decision and response execution
        │
        └── creates attack dynamics
                ├── safety-gradient rank and curvature
                ├── utility-gradient conflict
                └── optimizer/data-dependent routes through function space

activation evidence                         parameter/security evidence
-------------------                         ---------------------------
decodability                                finite weight edit
direction/subspace/cone      ─────X────▶     editability
causal add/remove/patch                      adaptive fine-tuning
conditional backup discovery                utility-constrained attack frontier
temporal recovery                           operational work factor
```

The `X` is the audit's central methodological warning: causal activation localization need not locate the cheapest parameter edit.[^1] The same non-uniqueness has now been reported for localized unlearning.[^2]

## Four evidence levels

| Level | A valid statement | What it does not license |
|---|---|---|
| Correlation | A direction, feature or checkpoint statistic covaries with refusal. | The model uses it; it is a safeguard; it predicts attack cost. |
| Representation evidence | The signal is decodable, stable across prompts or geometrically structured. | Causal mediation or mechanism identity. |
| Causal mediation | Add/remove/patch/rescue changes actual behavior under controlled interventions. | Parameter fault independence, global circuit completeness or tamper durability. |
| Security evidence | A defended checkpoint resists an adaptive, utility-constrained, held-out attack at declared operational budgets. | A global lower bound on attacker cost or robustness outside that threat model. |

## Collision clusters

### Cluster 1 — Direction → cone → sparse circuit

Arditi et al. established a powerful single-direction intervention.[^3] Concept Cones replaced the line with multiple interventionally meaningful directions and explicitly warned that orthogonality is not representational independence.[^4] SAE/circuit work then identified interacting minimal feature sets and dormant backups.[^5] Therefore, `writer`, `writer-cut` and `backup` are not new principles by themselves.

### Cluster 2 — Recognition is not action

Harmfulness/refusal separation, Knowing without Acting, HARC and Detection-to-Refusal collectively occupy the distinction between recognizing harm, deciding to refuse and executing refusal.[^6] A new paper may use this distinction for construct validity, but cannot claim it as a discovery.

### Cluster 3 — Static geometry is not dynamic durability

Labunets links refusal-prefix diversity to gradient/activation rank and fixed vector ablation.[^7] Alignment Collapse instead predicts second-order entry into sharp safety regions; SPF studies safety/utility gradient conflict.[^8] These works imply that a first-order `co-control` snapshot can miss attack dynamics.

### Cluster 4 — Durability is attack-relative

TAR shows that adversarial meta-training can move a bounded tamper frontier, while the ICLR durability audit shows that seeds, trainers and schedules can overturn the apparent result.[^9] TamperBench makes per-model/per-attack search a baseline expectation.[^10] Any observed BreachCost is thus a best-found attack upper bound on the true minimum cost, not a certificate.

### Cluster 5 — Hide, erase, or never learn

Benign relearning and Erase-or-Hide show that zero forget performance may reflect a learned inhibitor rather than erased knowledge.[^11] Deep Ignorance shows a much harder-to-reverse regime when hazardous knowledge is withheld during pretraining, while also disclosing an in-context retrieval bypass.[^12] A refusal-only theory cannot automatically generalize to learned safeguards.

## Surviving novelty wedge

No located work jointly tests all three:

1. several held-out, causally validated activation writers under a frozen operator;
2. their shared suppression by a finite utility-constrained parameter intervention;
3. incremental prediction of independently optimized adaptive weight-tampering cost beyond rank, clean safety, utility and capability accessibility.

This is a narrow empirical gap, not a new general theory of reliability or controllability.

## Recommended replacement objects

- Final outcome: an **operational adversarial value surface** over actual harm, benign utility and declared budgets.
- Mechanism hypothesis: **common-cause failure across frozen fault domains**.
- Construct discipline: **intervention equivalence**, not geometric angle alone.
- Optional high-risk pilot: a locally linear, utility-conditioned generalized control mode, validated by finite edits.
- Delete as headlines: reliability polynomial, global neural min-cut, coding distance, mutual information, raw parameter norm and composite `writer-cut × (1−CC)`.

## Sources

[^1]: Hase et al., [*Does Localization Inform Editing?*](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html), NeurIPS 2023.
[^2]: Lee et al., [*Does Localization Inform Unlearning?*](https://aclanthology.org/2025.emnlp-main.1109/), EMNLP 2025.
[^3]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^4]: Wollschläger et al., [*The Geometry of Refusal in Large Language Models*](https://proceedings.mlr.press/v267/wollschlager25a.html), ICML 2025.
[^5]: Prakash et al., [*Beyond I’m Sorry, I Can’t*](https://ojs.aaai.org/index.php/AAAI/article/view/41119), AAAI 2026; Gong et al., [*Conditional Co-Ablation*](https://arxiv.org/abs/2607.01940), arXiv preprint.
[^6]: Zhao et al., [*LLMs Encode Harmfulness and Refusal Separately*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/cd18539787d90e1d682d557c2c71b534-Abstract-Conference.html), NeurIPS 2025; Chua and Wu, [HARC](https://arxiv.org/abs/2607.00572), arXiv preprint; Chu et al., [*From Detection to Refusal*](https://arxiv.org/abs/2609.00051), arXiv preprint.
[^7]: Labunets, [*Refusal Geometry Reflects Refusal Training*](https://arxiv.org/abs/2608.25390), arXiv preprint v2.
[^8]: Springer et al., [*The Geometry of Alignment Collapse*](https://arxiv.org/abs/2602.15799), arXiv preprint; Zhang et al., [*Understanding and Preserving Safety in Fine-Tuned LLMs*](https://arxiv.org/abs/2601.10141), arXiv preprint.
[^9]: Tamirisa et al., [*Tamper-Resistant Safeguards*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/fc49a629d33bc2461ed7a715ce44da68-Abstract-Conference.html), ICLR 2025; Qi et al., [*On Evaluating the Durability of Safeguards*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^10]: Hossain et al., [TamperBench](https://doi.org/10.1145/3770855.3817557), KDD 2026 Datasets & Benchmarks.
[^11]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025; Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^12]: O’Brien et al., [*Deep Ignorance*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/3bf80b34f731313b8292f4578e820c90-Abstract-Conference.html), ICLR 2026.
