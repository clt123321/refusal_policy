# Round 5 — Geometry Candidates

## Rule

Geometry is admitted only when it predicts a utility-qualified attack outcome that did not define the geometry. Raw parameter norm, rank, cosine and attractive plots are not mechanisms.

## Candidate audit

| Candidate | Decision | Why it is not decoration—or why it is | Measurement | Prediction beyond rank | Cheapest falsification |
|---|---|---|---|---|---|
| Activation anisotropy | **MERGE** | A dominant direction matters only if it is causally used and cheaply editable | causal-effect-weighted activation spectrum | concentration of worst functional mode | no gain beyond top causal effect/clean margin |
| Safety/utility subspace overlap | **CONDITIONAL primary proxy** | Tests local functional inseparability, but resembles the local relaxation of the attack objective | utility-conditioned generalized response spectrum with data- and objective-level isolation | unseen-operator global breach cost | fails on A3/A4/composed attacks or changes under equivalent parameterization |
| Fisher concentration | **BASELINE** | Localizes parameters important to a sampled loss but is data and objective dependent | blockwise empirical Fisher with frozen prompts | early FT-sensitive support | full GFS/gradient norm predicts equally or better |
| Local curvature | **CONDITIONAL** | Can turn initially harmless gradients toward safety-sensitive modes | HVP/Lanczos or finite-difference turning on attack-dev only | short LoRA/full-FT time-to-breach beyond first-order slope | no improvement for 16/32/64/128-step trajectories |
| Distance to unsafe-capable boundary | **DELETE as mechanism** | Estimating it requires solving nearly the same constrained attack | registered attack frontier | none independent of outcome | estimator cost/evidence is the attack itself |
| Raw safety-loss sharpness | **DELETE** | Scale and parameterization dependent; ignores utility | raw Hessian eigenvalues | none reliable | ranking changes under function-preserving reparameterization |
| Low-loss path connectivity | **EXPLORATORY** | Could expose a global detour missed by local sensitivity | function-space safety/utility along permutation-aligned linear/Bézier paths | existence of nonlinear unsafe-useful corridors | all checkpoints have similar paths but different cost |
| Trajectory geometry | **MERGE with curvature/persistence** | Early turning may matter, but raw weight path length does not | benign-function KL path length and mode persistence | whether local mode survives optimization | first 10% of path does not forecast held-out continuation |
| Parameter sensitivity spectrum | **KEEP** | Shows whether one parameter mode jointly controls many safety outputs | randomized JVP/VJP plus utility whitening | common-mode concentration and operator transfer | predicts A1 only, not A3/A4 |
| Static controllability spectrum | **DELETE standalone** | Feed-forward transformers have no canonical control-time system | only defensible as the generalized response spectrum above | no unique prediction | no gain over sensitivity spectrum |
| Token-time response Gramian | **DIAGNOSTIC** | Gives a finite-horizon intervention response for temporal recovery | pulse at token/layer, observe later causal safety states | recovery horizon and bootloader reach | does not predict pulse outcome or needs post-hoc positions |
| Attack-transfer geometry | **DIAGNOSTIC** | Rows decompose security outcomes but do not identify an internal cause | 4×4 domain attack-transfer matrix plus joint-domain attack | number of separate edits needed for joint domain breach | cover number invariantly one, partition unstable or joint objective bypasses it |

## Primary geometric proxy: utility-conditioned safety response

Let `s(θ)` be a vector of safety-stage outputs on mechanism-dev prompts and `u(θ)` a vector of benign functional outputs on a disjoint utility set. Within a frozen parameter operator class `V`, estimate

\[
G_s = \mathbb{E}[J_s^\top W_s J_s],\qquad
G_u = \mathbb{E}[J_u^\top W_u J_u],
\]

and solve

\[
G_s v = \lambda (G_u + \rho G_0)v.
\]

`G0` is a declared function-space/Fisher damping metric, not raw Euclidean norm; `ρ` is selected on mechanism-dev only. The leading `λ`, spectral concentration and cross-step mode persistence are **proxies** for the existence of a safety-changing, utility-cheap direction. They are not breach cost and not certificates.

Required protections against a metric paper:

1. safety and utility prompts used to estimate the spectrum never enter the confirming attacks;
2. predictor safety outputs differ from the confirming attack objective: use held-out hazard domains/stages and content-level harmful-task success for confirmation, so prompt disjointness alone cannot masquerade as independence;
3. freeze the operator class, damping `ρ` and utility panel before any confirming outcome; test nullspace stability on a second utility suite;
4. compare full Skin-Deep GFS, Fisher concentration, clean margin, gradient norm and OAFT;
5. compute within at least low-rank, sparse-block and unrestricted tangent classes rather than claim one universal spectrum;
6. verify finite perturbations change content-level behavior, not only logits;
7. predict first-passage cost under A3/A4 and an edit→repair→cleanup composition before viewing those results;
8. causally manipulate the spectrum only after natural-experiment support, with overall learning plasticity matched.

## Mechanism × attack interaction

| Mechanism property | Weight edit | Heretic | LoRA | Full FT | Sparse edit |
|---|---|---|---|---|---|
| Utility-conditioned safety response | **Strong**: direct local mode | **Strong** if search can find mode | **Medium–strong** in LoRA tangent | **Medium** early; curvature later | **Strong** after sparse restriction |
| Finite fault-domain overlap | **Strong** | **Strong** | **Medium** | **Weak–medium** | **Strong** |
| Autonomous recovery/bootloader | **Weak–medium** | **Weak–medium** | **Unknown** | **Unknown/weak** | **Medium** |
| Stage-survival matrix | **Strong diagnostic** | **Strong diagnostic** | **Medium** | **Medium–weak** | **Strong diagnostic** |
| Cross-domain transfer isolation | **Strong** | **Strong** | **Strong** | **Strong** | **Medium–strong** |
| Local curvature | **Weak** | **Weak** | **Strong early** | **Strong early** | **Weak** |
| OAFT/rank | **Same-operator only until proven** | **Weak** | **Unknown** | **Unknown** | **Weak–medium** |

The primary candidate must predict at least two genuinely different parameter biases. A property that only predicts the diagonal cell is attack-specific diagnostics.

## Geometry deliberately excluded from the first round

- Grassmann trajectories and principal-angle atlases;
- raw Hessian spectra;
- parameter-space interpolation pictures without functional alignment;
- module-distance or layer-count scores;
- a product such as `writer-cut × (1−CC)`;
- high-dimensional mutual information;
- error-correcting-code distance without stable symbols and a recovery map.

These may return only after a concrete failure makes a new prediction that the retained measurements cannot make.
