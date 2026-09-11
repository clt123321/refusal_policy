# Cost and Practicality Review

## 1. Decision constraints

The preferred program is a post-training retrofit with zero inference overhead, <1% degradation on a predeclared utility panel, and at least a 2× increase in independently measured breach cost. The <$5–10 small-model target is a stretch engineering check, not a scientific threshold.

The decisive quantities are:

\[
\text{attack amplification}(\epsilon)=
\frac{C_{breach}^{defended}(\epsilon)}{C_{breach}^{base}(\epsilon)}
\]

and

\[
\text{defense leverage}(\epsilon)=
\frac{C_{breach}^{defended}(\epsilon)-C_{breach}^{base}(\epsilon)}{C_{defense}+C_{infer}(N)}.
\]

Both are empirical and right-censored by the search budget. Report the whole budget curve at 0%, 2%, 5%, and 10% utility-loss tolerances.

## 2. Cost accounting

Dollar cost is secondary. Primary records must include:

- model size, trainable parameters, tokens and sequence length;
- forward/backward passes and estimated FLOPs;
- GPU type/count, precision, GPU-hours and peak memory;
- attack/defense hyperparameter trials, including OOM and failed runs;
- activation/checkpoint storage;
- judge API and human-review cost;
- added latency, throughput and memory at inference.

Use one ordinary safety-SFT pass on the same model/data as a local cost unit. This makes 2× or 4× overhead comparable before converting to hardware-specific dollars.

## 3. Five philosophies plus retained sixth direction

| Philosophy | Retrofit | Inference overhead | Indicative defender cost | Utility risk | Cross-attack prospect | Practical verdict |
|---|---:|---:|---:|---|---|---|
| Safety reconstruction / self-repair | yes | zero if trained-in; nonzero for runtime injection | 1.5–3 SFT-equivalents | over-refusal | moderate for prompt/prefill; unknown for weight attacks | cheap but crowded and narrow |
| Independent parameter fault domains | yes | ideally zero | 2–4 SFT-equivalents plus discovery | capacity/optimization interference | high if joint-cut cost transfers | viable primary feasibility bet |
| Safety–utility entanglement | yes | zero | 3–6+ SFT-equivalents for break/repair loops | high; blocks useful adaptation | FT/edit only | high-upside wildcard |
| Capability prevention/suppression | usually no | zero model-side | pretraining-scale for strongest evidence | domain knowledge loss | strong for relearning, weak to context | not a low-cost v4 primary |
| Cross-perturbation adversarial training | yes | zero | 2–5 SFT-equivalents | reduced plasticity; masking | medium–high if off-diagonal transfer appears | practical backup |
| Functional safety margin | diagnostic first | zero | several attack sweeps; training 2–5+ SFT-equivalents | utility-set overfit | definition broad, estimator bounded | common objective, not standalone bet |

These ranges are design estimates for relative planning, not measured results.

## 4. Candidate implementation envelopes on 8×A800

### Primary: heterogeneous parameter fault domains

- **Small feasibility scale:** 1.5–3B, LoRA or selected-module retrofit, two path/fault passes.
- **Parallelism:** distribute attack extraction and sweep trials across GPUs; do not require eight-way model parallelism at this scale.
- **Memory:** activations dominate if all layers/tokens are retained; stream summaries and retain only selected-layer tensors.
- **Likely bottleneck:** differentiating or searching for a joint parameter edit after defense, not the retrofit itself.
- **<$5–10 stretch:** possible only for a minimal PEFT run under low marginal cluster pricing and excluding broad attack search; it should not be advertised without measured accounting.

### Backup: cross-operator adversarial retrofit

- **Small feasibility scale:** 1.5–3B PEFT defender with two inexpensive inner operators.
- **Parallelism:** operators can run on separate workers; synchronize defender updates or alternate operators.
- **Memory:** activation inner loops and full-gradient direct edits should not coexist on one device without checkpointing/offload.
- **Likely bottleneck:** stronger held-out attack sweeps needed to rule out gradient masking.
- **<$5–10 stretch:** unlikely for the complete evidence package; possibly attainable for one training run, which is not the relevant total cost.

### Wildcard: repair-closed safety–utility coupling

- **Small feasibility scale:** 1.5–3B, first-order LoRA break→repair approximation.
- **Parallelism:** parallel attacker trajectories; sequential dependency within each two-stage trajectory.
- **Memory:** moderate under PEFT; full-weight unrolling is impractical for a first test.
- **Likely bottleneck:** nested attack plus repair search and credible utility evaluation.
- **<$5–10 stretch:** not realistic for a discriminating study.

## 5. Hidden costs

### Attack search dominates headline credibility

A cheap defense with an underpowered attack is not cheap evidence. The complete cost includes post-defense re-extraction, multiple ranks/layers, FT learning-rate and optimizer sweeps, utility repair, and at least one held-out operator.

### Activation storage can be avoided

Do not dump every token at every layer. Online means/covariances, randomized sketches, selected layers and prompt subsets are sufficient for screening. Persist only artifacts required to reproduce the chosen intervention.

### Full fine-tuning is an evaluation requirement, not necessarily a defense-training requirement

PEFT is appropriate for feasibility and may be the intended retrofit. At least one short full-parameter attack is still required, because resistance to a LoRA attacker can arise from adapter support restrictions.

### Inference overhead is a lifetime cost

Runtime reinjection, classifiers or duplicate branches can dominate at deployment volume. A trained-in defense with zero inference overhead is preferred, but a low-overhead method should be compared through \(C_{infer}(N)\), not labeled “free.”

## 6. Practical selection

| Program | Cost score (10 = cheapest) | Practicality score | Main constraint |
|---|---:|---:|---|
| Heterogeneous fault domains | 6 | 6 | joint-cut search and proving true independence |
| Cross-operator adversarial retrofit | 5 | 7 | multiple inner passes and held-out attacks |
| Repair-closed coupling | 3 | 4 | nested repair trajectories |
| Route reconstruction | 8 | 8 | novelty and FT robustness, not engineering |
| Capability prevention | 1 | 2 | requires pretraining for strongest form |
| Functional-margin diagnostic | 5 | 6 | attack search and utility-set coverage |

The practical winner is not automatically the scientific winner. Route reconstruction is cheapest but crowded; capability prevention has strong durability evidence but violates retrofit cost. Heterogeneous fault domains and cross-operator training occupy the best current cost/novelty compromise.

Evidence sources for the defense families are consolidated in [DEFENSE_PROGRAMS.md](DEFENSE_PROGRAMS.md) and the normalized [defense evidence table](../v4_background/DEFENSE_EVIDENCE_TABLE.csv).
