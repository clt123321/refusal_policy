# Compute Readiness

Status: estimates only — no unauthorized runs were started. Local probes on 2026-09-13: 8× A800-SXM4-80GB free at audit time; disk overlay 7.0T total, 6.8T available; `/root/.cache` on overlay.

## 1. Per-cell estimates (fp16, single checkpoint)

| Cell | Model size (fp16) | Working VRAM (1×A800 unless noted) | Est. wall (single run) | Disk | Notes |
|---|---:|---:|---:|---:|---|
| R0a canonical add/remove/orthogonalization | per canonical model (e.g. 2B → ~4.5 GB) | ~8–16 GB | 1–4 GPU-h per checkpoint | 20–60 GB scratch | several seeds/directions; human-audit sample at boundary |
| R0b Gemma-2-2B transfer | ~5.1 GB | ~12–20 GB | 2–8 GPU-h | 40–120 GB | direction + add/remove/rescue + utility panel |
| R1 Fail-Closed pair (base+FC) | 2× ~5.1 GB | ~24 GB (two models) | 4–12 GPU-h | 100–200 GB | clean + DIM/RDO ablations + cheap prompt attack subset |
| R2 A1 rank grid (base only) | ~5.1 GB | ~16 GB | 8 A800-GPUh cap per constants | +20–60 GB | 35-candidate grid, deterministic trial order; failed trials charged |
| R3 TamperBench Qwen3-4B LoRA | ~8 GB | ~20 GB | 8–24 GPU-h | +40–80 GB | no-weight vs LoRA grids; seeds 17/29/43 records |
| Full harness acceptance | — | 1–2 GPUs | see cells | ≤0.4 TB working | intermediate checkpoints pruned; optimizer states not retained long-term |

## 2. Storage policy

- Manifests/aggregates/schemas → git.
- Weights/directions/large tensors/raw harmful generations → outside git, content-addressed store, restricted per H0.
- Artifact size estimates: single Gemma-2B direction tensors ~ tens of MB; edited checkpoints ~ model size; raw generation logs only for audit sample.

## 3. Retry / censoring policy

- Any trial at a budget tier that fails/OOM/diverges is retained and charged (CostTracker charges `FAILED`/`OOM`; summary marks right-censor).
- Deterministic logical trial order by integer trial ID; parallel completion order ignored.

## 4. GPU policy for tonight

- No GPU run started without an authorized cell: harness dry run used CPU with a benign fixture; math tests are CPU.
- When executor-authorised cells are confirmed, one GPU for simple inference; grids evaluate after smoke.
