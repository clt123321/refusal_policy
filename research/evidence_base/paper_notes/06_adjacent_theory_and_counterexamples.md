# Paper notes — adjacent theory and candidate counterexamples

## Why the cross-domain evidence matters

The adjacent literatures do not prove the project’s hypothesis. They constrain what
can be claimed and identify natural counterexamples.

| Candidate natural experiment | What it could destroy | Public asset/status | Required comparison |
|---|---|---|---|
| Concept Cones / SOM checkpoints or reproducible setups | Many activation directions imply high durability | Published methods; code availability must be rechecked before execution | Multi-direction causal effect versus rank-1/shared-module tamper frontier |
| *There Is More to Refusal* | Geometric diversity implies distinct control modes | arXiv preprint | Category-specific subspaces versus cross-category common steering/edit |
| DeepRefusal | Self-repair under activation fault implies weight-tamper durability | [code/checkpoints](https://github.com/YuanBoXie/DeepRefusal); Findings EMNLP 2025 | Pulse/sustained ablation recovery versus adaptive weight/prefill attack |
| TAR checkpoints | A higher attack budget corresponds to distributed safety mechanisms | [official repository](https://github.com/rishub-tamirisa/tamper-resistance); ICLR 2025 | Same mechanism diagnostics on baseline and TAR, blinded to attack result |
| Deep Ignorance model suite | Refusal geometry generalizes to learned safeguards | [public model collection](https://huggingface.co/EleutherAI/deep-ignorance-unfiltered); ICLR 2026 | Access suppression versus never-learned models under calibrated functional displacement |
| HARC / LLM-VA | Strong recognition–action coupling yields white-box durability | Public code/model availability to verify; preprint/ACL 2026 | Input robustness versus utility-constrained parameter removal |
| AntiDote | Bilevel robustness creates independent fault domains | AAAI 2026 paper; code availability to verify | Independent faults, common-mode fault and held-out attack |
| Unlearning suppressor models | Refusal writers are a general form of negative inhibitor | Published unlearning setups | Same localization–editability dissociation under forgetting and refusal |

## Classical abstractions: admissible and inadmissible uses

### Reliability engineering

- **Admissible:** define fault domains operationally, test independent and common-cause faults, and ask whether those tests predict an independent attack.
- **Not admissible:** infer statistical independence from orthogonal directions.
- **Prediction:** a model can survive random single faults yet fail under one common-cause intervention.

### Control theory

- **Admissible:** a local linearized, safety-versus-utility generalized control mode that prospectively predicts effective interventions.
- **Not admissible:** raw parameter L2 called “control energy”; the value changes under benign reparameterizations.
- **Prediction:** equally decodable representations can differ in intervention energy.

### Coding theory

- **Admissible only after evidence:** identifiable symbols, arbitrary-erasure tolerance and reconstruction.
- **Not admissible:** calling several continuous directions an error-correcting code.
- **Prediction required:** a reproducible erasure threshold and recovery map.

### Information theory

- **Admissible:** functional divergence on a preregistered probe distribution as a coordinate-invariant displacement.
- **Not admissible:** high-dimensional mutual information estimates as a causal mechanism or Shannon “rate” without a code.

### Network science

- **Admissible:** a restricted empirical cut over a fixed intervention library.
- **Not admissible:** claiming a global neural min-cut or max-flow without stable nodes, edges and a conservation law.

### Causal inference

- **Admissible:** preregistered interventions, rescue/patching and intervention-equivalence classes.
- **Not admissible:** interpreting checkpoint correlations or behavior-matched selection as causal mediation.

### Dynamical systems

- **Admissible:** pulse perturbation followed by reproducible downstream/token recovery that predicts a persistent attack.
- **Not admissible:** calling any nonlinear training curve an energy barrier or attractor.

## Parameter-coordinate warning

Raw Euclidean weight distance, layerwise Frobenius norm, edit rank and LoRA factor
norm are not invariant under permutation, scaling, basis change or factor
reparameterization. Report real attack resources and a held-out functional
displacement; use parameter quantities only within a fixed architecture and attack
primitive.

Sources: [parameter-space reparameterization, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/395371f778ebd4854b88521100af30ad-Abstract-Conference.html); [information-geometric sharpness, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b2ba568effcc3ab221912db2fb095ea9-Abstract-Conference.html); [Does Localization Inform Editing?, NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/3927bbdcf0e8d1fa8aa23c26f358a281-Abstract-Conference.html).
