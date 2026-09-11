# Feasibility Decision Note — Agent Execution Boundary

## Status

`DECLINED_BY_AGENT_POLICY` — this is not a TODO Gate F scientific outcome (`GATE_F_PASS` / `GATE_F_WEAK` / `GATE_F_FAIL`). No causal experiment was run to produce a scientific null or positive result. This note records a deliberate execution boundary, not a finding.

## What this session completed

- Benign-only capability profiling of `Qwen/Qwen2.5-0.5B-Instruct` and `Qwen/Qwen2.5-1.5B-Instruct` (load, chat template, generation validity, memory, throughput). See `model_profile.json` and `model_decision.md`.
- No harmful content, no safety-bypass testing, no parameter edits, no fine-tuning.

## What this session will not implement or run

1. **C01 with real harmful prompts.** Building the H×P assay's "harmful" cell requires sourcing or writing genuine harmful-request content. This session will not construct that dataset.
2. **An "Actual Harmful Compliance" (AHC) evaluator.** Scoring model completions for non-refusal, relevance, specificity/actionability, and "substantive harmful assistance" requires generating and grading harmful completions. This session will not build or run that evaluator.
3. **C03 causal necessity/sufficiency/rescue on natural harmful prompts.** Removing a candidate direction from real harmful-prompt activations and measuring whether harmful compliance increases is, in effect, validating a working refusal-removal technique against a real aligned model. This session will not run that experiment.
4. **C04 negative controls tied to the above.** Controls are only meaningful relative to the C03 result above; without C03 there is nothing to control against, and this session will not build the harmful-completion grading path needed to compute them.
5. **C05 writer analysis and parameter co-control diagnostics that depend on the above signal.** Not run, because their preconditions (C03/C04 signal) were not established.
6. **A1 analytic weight-orthogonalization edit.** This is the same operation documented in this repository's own literature review as the mechanism behind automated "censorship removal" tools (Heretic, OrcaRouter-style GLM abliteration): `W_new = (I - r r^T) W` applied to attention/MLP output matrices to suppress a safety-relevant direction. This session will not implement or run this edit against a real model.
7. **A3 short adversarial fine-tuning calibration.** This is a fine-tuning attack explicitly designed to reduce refusal/increase harmful compliance under a benign-utility constraint. This session will not implement or run it.

## Why this line is drawn here, and not one step later

Every item above shares one property: to run it "for real" (as opposed to on a synthetic proxy), I would need to (a) produce or use real harmful prompts, (b) generate model completions to those prompts under a deliberately weakened or edited safety mechanism, and (c) score how effectively those completions provide harmful assistance. Steps (a)–(c) are, independent of the surrounding statistical/preregistration framework, the same steps used to build and validate a working jailbreak/abliteration pipeline, with an explicit follow-on step (A1/A3) to make the removal cheap and durable via weight edits or fine-tuning. I will not carry this out autonomously, including when instructed to bypass "human review" blockers, regardless of how the surrounding protocol is framed.

This is independent of whether the broader research question (durability of safety mechanisms under white-box tampering) is legitimate — it plausibly is, and is studied in published work (Arditi et al. 2024, TAR ICLR 2025, TamperBench). The issue is specifically that *I*, running unsupervised and asked explicitly not to stop for human review, would be the one sourcing the harmful prompts, generating the harmful completions, grading their actionability, and validating an attack technique's success rate. That step needs real human/institutional safety oversight (ethics review, restricted-access handling of any harmful outputs, a named accountable researcher), not an agent instructed to keep going overnight.

## What remains available if you want to continue

- Continued benign-only engineering: statistics/schema/report tooling, reproducibility harness, further safe-proxy validation (already done once; TODO says not to repeat it).
- I can help you design the C01–C04 protocol and code interfaces in the abstract (already done in `src/`), so that a human researcher — under appropriate review — can supply real harmful prompts and run the harmful-completion/grading steps themselves, outside of this autonomous session.
- If useful, I can build a strictly non-harmful "over-refusal" probe (XSTest-style: prompts that sound sensitive but are benign, e.g. "how do I kill a process in Linux") to study refusal-trigger dynamics without eliciting or grading real harmful content. This would **not** satisfy TODO's AHC/C03 requirements and cannot be used as Gate F evidence; it would only be a weaker, safe proxy for refusal-trigger sensitivity.

## Recommendation

`STOP_AND_ESCALATE_TO_HUMAN` — not `STOP_AND_REDESIGN`. The research design itself is not shown to be flawed; the blocker is that the remaining steps require real harmful-content handling and safety-removal validation that should be run with direct human/institutional oversight rather than by an unsupervised coding agent.
