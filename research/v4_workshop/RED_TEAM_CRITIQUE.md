# Red-Team Critique

## Decision rule

- **DEAD:** no distinct defense contribution or incompatible with the open-weight/retrofit target.
- **NARROW:** useful under a declared attack or deployment boundary, but not a primary general-defense bet.
- **PROMISING:** credible, testable and practical enough to retain, with meaningful prior collision.
- **HIGH-UPSIDE:** a sharp open distinction with a killer falsification test and main-conference ceiling, despite substantial failure risk.

## Forced review of every proposal

| Proposal | Adaptive bypass | Attack-specific? | Full FT / LoRA | Gradient masking? | Capability-collapse confound | Refusal-only? | Pretrain required? | Low-cost retrofit? | Prior collision | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| **M1 Route reconstruction** | re-extract route; edit late output; delete runtime logic | likely unless unseen faults transfer | LoRA may be slowed; full FT likely breaks | possible if trained cuts share gradients | moderate | evidence mostly refusal | no | yes | HARC/DeepRefusal/Any-Depth/DeRTa nearly cover it | **NARROW** |
| **M2 Heterogeneous fault domains** | global output edit; optimize all paths jointly | less tied to one attack, but partitions can be artificial | local LoRA may slow; unrestricted FT wins eventually | high risk if joint edit optimizer is weak | moderate | prototype may be refusal-only | no | plausible, not yet cheap | Concept Cones/DeepRefusal/diverse-prefix are close but not parameter independence | **HIGH-UPSIDE** |
| **A1 Cross-operator AT** | choose an untrained operator, longer horizon or composition | yes unless off-diagonal transfer is strong | both can be included; held-out full FT remains essential | central risk | high if invariance makes model inert | need dangerous-task endpoint | no | medium-cost | TAR/AntiDote/ART/LAT | **PROMISING** |
| **A2 Attack-program AT** | add stage, reverse order, repair optimizer | bounded grammar is necessarily specific | short paths only; long full FT exceeds inner loop | possible but less than single-gradient AT | explicit repair helps expose it | no in principle | no | no | TAR trajectories; Deep Ignorance staged attacks | **PROMISING**, engineering-heavy |
| **R1 Minimum joint cut** | shared head or a reparameterized global edit | principle is attack-agnostic; estimator is not | LoRA/local edits may slow; full FT remains ceiling | central if cut search is differentiable only | moderate | can generalize, first test likely refusal | no | plausible | same program as M2 | **HIGH-UPSIDE**, merge with M2 |
| **R2 Repair-closed coupling** | joint optimize breach+utility; distill or merge | FT/edit family only | explicitly test both; long FT can decouple | lower if derivative-free repair included | central and must be ruled out | not necessarily | no | expensive | SDD/SEAM/TAR | **HIGH-UPSIDE**, high risk |
| **C1 Reacquisition-invariant suppression** | new optimizer, rank, representation or supplied context | yes: update-environment family | directly targets both, but context trivially bypasses | possible | forgetting can be general degradation | no | no | medium–high cost | invariant/smooth unlearning largely occupy it | **NARROW** |
| **C2 Capability-supply closure** | delete context gate or use external executor | model-only version cannot close all channels | both restore capability eventually | not primary risk | very high | no | strong form yes | no | Deep Ignorance already exposes boundary | **DEAD** as retrofit model defense |
| **S1 Adaptive-repair resistance** | stronger repair, selective layers, merge/distill | it is an evaluation requirement, not defense alone | both required in audit | use non-gradient repair controls | designed to reveal confound | no | no | audit is cheap; training is not | durability audit/SEAM/SDD | **PROMISING** as mandatory test; **NARROW** as program |
| **S2 Two-resource safeguard** | one joint FT may supply capability and remove policy | broad but depends on genuine resource separation | full FT likely crosses both; LoRA is empirical | low | capability absence is intended, not collapse | no | strong version yes | no | Deep Ignorance + Any-Depth | **NARROW** |
| **T1 Functional safety margin** | exploit omitted utility dimensions or stronger inner search | definition general; approximation attack-specific | both estimate the margin | severe if inner search weak | controlled by multi-task utility set, never eliminated | no in definition | no | diagnostic first; training expensive | robust optimization/TAR/AntiDote | **HIGH-UPSIDE** as object, not yet a defense |
| **T2 Operator-basis training** | nonlinear/staged/derivative-free operator | yes unless basis has measurable coverage | held-out LoRA/full FT necessary | central | high | no in principle | no | medium-cost | same program as A1 | **PROMISING**, merge with A1 |

## Strongest attacks against the retained ideas

### Heterogeneous parameter fault domains

The obvious attack is not to remove each advertised path. It is to optimize the final harmful-task loss jointly over all parameters while penalizing benign-function drift. A shared unembedding, final normalization, late MLP, or compliant-prefix mode may bypass every path at once. A convincing test must re-extract the joint edit **after** defense and compare with equal-capacity same-domain controls. Counting modules, heads or orthogonal activations is insufficient.

### Cross-operator adversarial training

The likely failure is diagonal robustness: each training operator becomes harder while a held-out operator is unchanged. A weak gradient attack may also mistake loss-surface distortion for robustness. Require stronger/longer inner optimization, a derivative-free or search-based direct edit, and a fully held-out operator class. If only the average of trained attacks improves, the program is incremental attack augmentation.

### Repair-closed safety–utility coupling

The attacker first maximizes dangerous task success, then restores utility using benign replay, base-model KL, selective layers, adapter merge or distillation. The defense survives only if utility recovery causally restores safety—not merely if repair is difficult. Clean utility and legal downstream fine-tunability must also remain high. Otherwise the method protects safety by making the model unusable.

### Functional safety margin

The nearest unsafe model depends on which benign behaviors are measured. An attacker can preserve MMLU while degrading capabilities omitted from the calibration set, or exploit judge errors and over-refusal. The margin is worth retaining only if a cheap estimate prospectively ranks models under attacks implemented after the score is frozen. Without prospective prediction it is metric proliferation.

## Merged program set after red team

| Merged program | Inputs | Status | Why retained or cut |
|---|---|---|---|
| Heterogeneous parameter fault domains / minimum joint cut | M2 + R1 | **HIGH-UPSIDE** | only candidate with a relatively unoccupied security distinction and a direct joint-edit falsifier |
| Cross-operator adversarial retrofit | A1 + T2 | **PROMISING** | practical, clean transfer matrix, but crowded and vulnerable to diagonal-only gains |
| Repair-closed safety–utility coupling | R2 + S1 | **HIGH-UPSIDE** | sharp adaptive prediction beyond SDD/SEAM, but expensive and FT-centric |
| Attack-program training | A2 | **PROMISING** | realistic but combinatorial; better as later extension of repair-closed evaluation |
| Route reconstruction | M1 | **NARROW** | HARC/DeepRefusal/Any-Depth collision and HARC’s 160-example FT failure |
| Reacquisition invariance | C1 | **NARROW** | strong existing unlearning collision and no context defense |
| Capability-supply closure / two-resource stack | C2 + S2 | **DEAD/NARROW** | strong version requires pretraining/system enforcement; weak retrofit likely bypassed |
| Functional safety margin | T1 | **HIGH-UPSIDE diagnostic** | retained as common evaluation object; not counted as a standalone defense program yet |

## Non-negotiable controls

Every retained program must include:

1. post-defense attack re-extraction;
2. at least one optimizer/intervention family absent from defense training;
3. short LoRA and full-parameter FT;
4. a derivative-free or discrete-search check where practical;
5. actual harmful-task/compliance success, not refusal strings alone;
6. several benign utility endpoints and over-refusal;
7. explicit utility-repair attack;
8. attack and defense compute including search failures;
9. right-censoring language—“not breached within budget,” never “secure.”

Primary publication references for the reviewed programs are consolidated in [DEFENSE_PROGRAMS.md](DEFENSE_PROGRAMS.md).
