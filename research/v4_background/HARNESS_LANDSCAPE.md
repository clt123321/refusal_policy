# Open-Weight Defense Harness Landscape

**Decision:** extend TamperBench before building a new harness.  Treat it as an execution substrate, not as a complete scientific definition of durability.

## 1. What a research harness must make comparable

A defense result is interpretable only when the harness fixes or records five objects:

1. the released starting checkpoint and every transformation applied to it;
2. the attacker's information, interfaces, data, compute and utility constraint;
3. the safety target, including whether it is behavior or latent capability;
4. the defender's complete training, search and inference cost;
5. the attack search procedure, including unsuccessful and censored trials.

The output should be a **frontier**, not a pass/fail badge:

\[
F_D(b,\epsilon)=\max_{A:\,C_A\le b,\ U(A(M_D))\ge U(M_D)-\epsilon}
\operatorname{Harm}(A(M_D)).
\]

The empirical maximum is conditional on the registered attack set and search policy. It is never a robustness certificate.

## 2. Existing substrates

### TamperBench

TamperBench is the best starting point for this scope. Its public repository already separates attacks, defenses, and evaluations through typed registries; supports nested attack sweeps; records harmful and benign fine-tuning, LoRA/full fine-tuning, multilingual fine-tuning, jailbreak tuning, embedding attacks, refusal ablation, GCG, and prompt attacks; and aggregates bounded worst-case outcomes.[^tb-paper][^tb-code]

The paper evaluates 21 models, nine attack classes and 40 trials per model–attack pair using StrongREJECT and MMLU-Pro under a 10% utility-loss constraint. This is substantially stronger than bespoke one-defense scripts.[^tb-paper]

What it does **not** yet settle:

- direct neuron, head, MLP and arbitrary low-rank weight edits;
- Heretic-style automated direction/layer/component search;
- post-defense re-extraction of latent features;
- inference tampering such as prefilling, decoding changes and hook removal as first-class programs;
- knowledge restoration through context, retrieval, tools, quantization, merging and staged attacks;
- actual domain task success versus conversational refusal;
- safety recognition, policy choice, output execution and retained capability as distinct endpoints;
- normalized attack and defense cost ledgers;
- attack-blind evaluation and artifact-lineage enforcement.

### Unlearning benchmarks

WMDP, MUSE and related suites contribute forget/retain splits and relearning protocols. They are necessary for capability safeguards but insufficient for behavior safeguards: low multiple-choice accuracy can result from suppression, negative inhibitor features, or formatting changes rather than deletion.[^wmdp][^relearn][^hide]

### Prompt-robustness and refusal suites

StrongREJECT, JailbreakBench, XSTest and OR-Bench cover harmful compliance, jailbreaks and over-refusal. They are useful endpoints but do not themselves exercise weight ownership. A defense can score well while retaining the relevant dangerous capability or failing under a direct edit.

### Domain capability evaluations

Cyber, bio, fraud and agentic tasks are the closest endpoints to the final misuse question. They are expensive, may require restricted data or human review, and should not be replaced by a refusal judge. Deep Ignorance illustrates the difference: capability can be absent from weights yet supplied through context or retrieval.[^deep]

## 3. Build versus extend

| Criterion | Build a new harness | Extend TamperBench |
|---|---|---|
| Time to credible baseline | slow; repeats loaders, sweep logic and evaluators | fast; existing typed registries and recipes |
| Comparability | initially low | direct comparison with a public benchmark |
| Mechanistic hooks | fully controllable | requires a new intervention interface |
| Attack composition | can be designed cleanly | requires scheduler/state extensions |
| Maintenance | entirely local | upstream changes and compatibility work |
| Scientific novelty | almost none by itself | almost none by itself |
| Reproducibility | depends on new engineering | benefits from public configs and community use |

**Recommendation:** fork or pin TamperBench, add narrow modules, and submit generally useful changes upstream where practical. Build a fresh harness only if one of these becomes a hard blocker:

- its license or data provenance prevents release;
- its execution graph cannot represent staged/composed attacks without a breaking rewrite;
- activation hooks and artifact lineage cannot be added cleanly;
- restricted safety data require an isolated evaluation package;
- the benchmark's scoring semantics cannot represent capability rather than refusal.

## 4. Minimal model panel

The harness specification should support three roles; exact checkpoints should be pinned only when an experiment plan is approved.

| Role | Candidate scale/family | Purpose |
|---|---|---|
| Canonical small | Qwen3 1.7B/4B or Llama 3.2 3B | cheap full sweeps, unit tests, full-weight attack feasibility |
| Modern primary | Qwen3 8B or Llama 3.1 8B | realistic open-weight alignment and comparison to prior work |
| Second family | Gemma 2/3 or Mistral 7B-class | falsify architecture/family-specific conclusions |

A model is not a new family merely because it has a different safety fine-tune. Record base, instruct and defended lineage separately.

## 5. Dataset and endpoint panel

### Safety behavior

- StrongREJECT or an equivalent rubric-scored harmful prompt set;
- held-out harm categories and multilingual prompts;
- jailbreak and prefilling sets not seen by the defense;
- XSTest/OR-Bench for false refusals;
- safe-completion grading where refusal is not the desired policy.

### Dangerous capability

- at least one controlled cyber or bio task with task-success scoring;
- a knowledge probe plus a generative/application task;
- context-free, context-supplied, retrieval-assisted and relearning conditions;
- human review for ambiguous actionable outputs.

### Benign utility

- MMLU-Pro or comparable knowledge/reasoning suite;
- IFEval for instruction following;
- coding and math subsets where relevant;
- matched benign prompts near the safety decision boundary;
- perplexity or KL only as diagnostics, never the sole utility endpoint.

Prompt templates, chat templates, evaluator prompts and generation settings are versioned artifacts. The ICLR durability audit shows these details can reverse conclusions.[^audit]

## 6. Attack suite by inductive bias

Counting attacks is misleading; coverage should be by non-equivalent search bias.

| Family | Minimum registered attack | Distinct bias |
|---|---|---|
| Input | GCG or transfer jailbreak; prefill | optimize/control tokens with fixed model |
| Activation | residual steering/removal; optimized embedding | intervene on runtime states |
| Direct weight edit | abliteration; Heretic-style automated search | exploit local causal/low-rank structure without SGD on task data |
| Fine-tuning | harmful LoRA; harmful full FT; jailbreak-tuning | gradient adaptation with different parameter support/objective |
| Restoration | benign relearning; context/retrieval supply | recover capability rather than merely remove refusal |
| Architecture/inference | disable guard/hook; decoding change | remove trusted execution assumption |
| Composition | edit → FT; FT → retrieval; prefill → activation | exploit interactions and repair side effects |

At least one attack per family must be implemented by an evaluator who does not see the defense's training attack. Heretic is a useful realistic optimizer over Arditi-style edits, not evidence that the space is exhausted.[^heretic][^arditi]

## 7. Defense API

Every defense should implement a versioned contract conceptually equivalent to:

```text
prepare(base_artifact, defense_data, budget, seed) -> defended_artifact
runtime_adapter(optional_config) -> generation_wrapper | none
cost_report() -> normalized_cost_record
threat_claim() -> declared_capabilities_and_exclusions
```

Requirements:

- defense training and runtime code are separable;
- trainable parameter support is recorded;
- external classifiers or secret artifacts are explicit;
- attacks can obtain the exact defended checkpoint and public defense description;
- a white-box adaptive mode permits gradients and re-extraction after defense;
- no defense-specific evaluation shortcut can alter shared scoring.

## 8. Metrics

### Primary outcomes

- actual harmful task/compliance success after attack;
- safety–utility frontier at utility-loss allowances of 0%, 2%, 5% and 10%;
- minimum discovered cost to cross predeclared safety thresholds;
- attack success as a function of budget, not only final ASR.

### Required controls

- clean safety and clean utility;
- over-refusal and safe-completion quality;
- retained harmful recognition and latent capability;
- parameter \(L_2\), layerwise relative norm and function/KL drift;
- attack failure reason and censoring indicator;
- inference latency, memory and throughput overhead.

### Cost ledger

For defense and attack separately record:

- hardware, precision, sequence length and software commit;
- total tokens and examples seen;
- trainable/total parameters;
- forward/backward passes and estimated FLOPs;
- GPU-hours, peak memory and stored artifacts;
- number of hyperparameter/search trials;
- API/human evaluation cost;
- failed/OOM/preempted trials.

Dollar equivalents may be reported with date and provider, but are secondary. “Under $5” is not portable across hardware or search accounting.

## 9. Budgets, seeds and stopping rules

- Publish a discrete budget ladder, for example direct edit only; 10/100/1,000 update steps; and a fixed token/FLOP ladder.
- Use the same total search budget for defended and undefended checkpoints.
- Separate attack optimization data from safety evaluation and domain-held-out data.
- Use at least three training/attack seeds for headline comparisons; cheap deterministic edits should still repeat extraction/evaluation sampling.
- Do not substitute the best benign-utility checkpoint post hoc without reporting selection variables.
- A censored run means “not breached within tested budget,” not infinite cost.
- Predeclare breach and unacceptable-utility thresholds before inspecting the defense result.

## 10. Artifact lineage and reproducibility

Each run should produce a manifest with:

- immutable model/dataset/code identifiers and licenses;
- parent checkpoint hash and ordered transformations;
- defense and attack configuration hashes;
- random seeds, environment, tokenizer/chat template and generation config;
- evaluator model/version/prompt and human-review protocol;
- cost ledger and terminal status;
- links to checkpoints or weight deltas where release is safe.

The lineage should make it impossible to accidentally compare a contaminated TAR dataset revision, a different prompt template, or a separately quantized checkpoint as if only the defense changed.[^tar-code]

## 11. Pre-registration and attack blindness

Before headline evaluation, freeze:

- primary safety and utility outcomes;
- attack budgets and utility tolerances;
- selection rule for checkpoints and hyperparameters;
- known-attack development suite;
- at least one held-out intervention family;
- failure/censoring policy.

For attack-blind validation, package only the defended artifact and public threat claim for a separate evaluator. The evaluator may know the defense paper-level description but should not receive its private development attacks or tuning traces. After the blind phase, a fully informed adaptive phase is also required; secrecy is not a valid open-weight defense.

## 12. Human review and safe handling

- Run automated refusal/harm judges first, then stratified blinded human review around threshold cases.
- Report judge disagreement and category-specific false positives.
- Keep dangerous domain data access-controlled; release hashes, schemas and safe aggregates where raw release is inappropriate.
- Prevent generated harmful content from entering logs or artifacts beyond what analysis requires.
- Separate the team that proposes a defense from at least one person implementing the held-out attack.

## 13. What the harness can and cannot claim

If implemented, this harness can support: “under these declared budgets and independent attack families, defense D moves the discovered safety–utility frontier by X.” It cannot support: “D secures public weights,” “no cheap attack exists,” or “refusal robustness implies dangerous capability removal.”

## Sources

[^tb-paper]: Hossain et al., [*TamperBench*](https://arxiv.org/abs/2602.06911), KDD 2026 Datasets & Benchmarks.
[^tb-code]: CriticalML, [TamperBench official repository](https://github.com/criticalml-uw/TamperBench), inspected at commit `ca4fade`.
[^wmdp]: Li et al., [*The WMDP Benchmark*](https://proceedings.mlr.press/v235/li24bc.html), ICML 2024.
[^relearn]: Hu et al., [*Unlearning or Obfuscating?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/18fd48d9cbbf9a20e434c9d3db6973c5-Abstract-Conference.html), ICLR 2025.
[^hide]: Yang et al., [*Erase or Hide?*](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4aa3942a863aaf997053eee7b733f85-Abstract-Conference.html), ICLR 2026.
[^deep]: O'Brien et al., [*Deep Ignorance*](https://arxiv.org/abs/2508.06601), ICLR 2026.
[^audit]: Qi et al., [*On Evaluating the Durability of Safeguards for Open-Weight LLMs*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/9d3a4cdf6f70559e8c6fe02170fba568-Abstract-Conference.html), ICLR 2025.
[^heretic]: p-e-w, [Heretic](https://github.com/p-e-w/heretic), engineering attack tool; no archival-paper status claimed.
[^arditi]: Arditi et al., [*Refusal in Language Models Is Mediated by a Single Direction*](https://proceedings.neurips.cc/paper_files/paper/2024/hash/f545448535dfde4f9786555403ab7c49-Abstract-Conference.html), NeurIPS 2024.
[^tar-code]: Tamirisa et al., [TAR official repository](https://github.com/rishub-tamirisa/tamper-resistance), inspected at commit `19de233`.
