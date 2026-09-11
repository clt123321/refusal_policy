# Excluded Large Files

Generated during experiment-artifact transfer. These files are intentionally excluded from the public repository and remain on the source experiment host.

| Path | Size | Why excluded | Reproducible from code? |
|---|---:|---|---|
| `artifacts/safe_mech/raw_layer_examples.pt` | 22M | Raw per-example residual-stream activation tensors (all 28 layers, construct-fit + carrier-dev), cached via `torch.save`. Falls under "raw activation tensors" / large binary artifact per sync policy. | Yes — regenerate via `scripts/run_safe_mech_c01_c02.py` against the same model/dataset config. |
| `artifacts/safe_mech/writer_scan_state.pt` | 22M | Cached per-module (attention/MLP) activation tensors and writer-score state from the module writer scan, via `torch.save`. Same category as above. | Yes — regenerate via `scripts/run_module_writer_scan.py`. |

## Notes

- Both files are `.pt` (PyTorch tensor pickle) and were already covered by the repository's own `.gitignore` (`*.pt` rule); this exclusion list documents that they were deliberately kept out of the public artifact commit, not just skipped by accident.
- No model weights, checkpoints, optimizer state, or HuggingFace cache content exist anywhere under this repository's working tree; only these two experiment-local activation caches were found above the 20M threshold (`find . -type f -size +20M -not -path './.git/*'`).
- All *derived* summary statistics computed from these tensors (layer scan CSVs, candidate-carrier JSON, writer-score CSVs, causal-intervention CSVs, all figures) are small and are included in the relay commit.
