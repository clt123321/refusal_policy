# V6 4090 Code Handoff

- Snapshot date: 2026-09-15
- Source HEAD before handoff: `d8bbb01c52a7b6ec2a02e11f89431e5b93976a37`
- Working tree before handoff: clean
- Scientific status: formal recipe is not frozen; no formal C or safety result
- Code status: repair runner, CLI, target-only loss masking, reload helper, draft config, and unit tests are present
- Commit provenance: `7f590e2ee0e955acec34243e1a9fe0f30887c70d` and `d8bbb01c52a7b6ec2a02e11f89431e5b93976a37` are present and reachable from this snapshot
- GPU status before execution: RTX 4090, approximately 24214 MiB free, no compute process
- Isolated environment: `.venv-v6`, Python 3.10.21, torch 2.10.0+cu128
- Model status at snapshot: required Qwen revision was not cached
- Validation status at snapshot: CPU/GPU repair execution and reload validation pending; existing unit tests are the only completed validation for these files
- Excluded from handoff: virtual environments, model weights, checkpoints, large data, restricted raw outputs, credentials, and unrelated project code
- Formal recipe status: `DRAFT_REQUIRES_EXECUTOR_FREEZE`
