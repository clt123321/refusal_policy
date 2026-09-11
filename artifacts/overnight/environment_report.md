# Overnight Environment Report

- Date: 2026-09-10
- Repository: `[source experiment workspace path redacted before public sync]`
- Remote sync: `git pull origin main` completed successfully
- Commit: `6cb64ce5ab9d05e9729e9f0aa8b38b51ecb792f0`
- Branch: `main`
- Workspace: clean; tracking `origin/main`
- Git tree: `2745c800b09b9bf9cb8a28b5f17fa873e80ef84c`

## Hardware

- GPUs: 8
- GPU: NVIDIA A800-SXM4-80GB × 8
- VRAM: 81920 MiB per GPU
- Compute capability: 8.0
- Driver: 535.129.03
- CUDA toolkit: 12.9.41
- PyTorch CUDA runtime: 12.8

## Software

- Python package versions: torch 2.10.0; transformers 5.16.1; datasets 3.6.0; accelerate 1.11.0; safetensors 0.8.0
- Model/cache environment variables: HF_HOME, TRANSFORMERS_CACHE, HF_HUB_CACHE, TORCH_HOME unset
- Observed caches: Hugging Face cache 124K; PyTorch cache 168K (machine-local paths redacted)

## Storage

- Filesystem size: 391T
- Used: 355T
- Available: 37T
- Utilization: 91%

## Repository audit

- Tracked implementation files: none
- Tracked datasets/manifests/configs: none
- Existing artifacts: none before this audit
- Existing model checkpoints: none observed in repository or standard caches
- Existing experiment entrypoints: none

## Protocol status

`TODO.md` at the synced commit is the controlling protocol. It requires Gate 0 before Gate 1 and forbids recipe training, sealed A4, and full replication during feasibility.

## Safety boundary

No model tampering, refusal-removal, harmful-compliance optimization, attack calibration, or implementation of those capabilities was run or added. Consequently, C01–C05 and A01–A05 remain unmeasured.
