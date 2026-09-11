# Sync Reconciliation — GitHub Research + KML Experiment History

Audit date: 2026-09-11

## History relationship

| Item | Commit |
|---|---|
| GitHub `main` before reconciliation | `e63c83a635cb5d5ec7187cbe0abb1cc36fe74029` |
| GitHub research baseline | `e63c83a` |
| KML relay branch head | `9372e36930c9d759027debaba05225af271525da` |
| Merge base | `6cb64ce5ab9d05e9729e9f0aa8b38b51ecb792f0` |

The histories diverged after `6cb64ce`. GitHub had one research-only commit,
`e63c83a`; the final KML branch had thirteen experiment/relay commits. `git log
--left-right --cherry-pick main...kml-experiment` found no apparent duplicate or
cherry-equivalent commits.

The KML changes did not modify `TODO.md` or the GitHub `research/` audit files, so
the research baseline was preserved without conflict.

## GitHub-only commit preserved

```text
e63c83a research: add innovation audit and candidate stories
```

## Integrated KML experiment commits

The first eight KML commits were cherry-picked in their original order. The artifact
archive was reconstructed without its internal transfer metadata.

| KML commit | Integrated commit | Subject |
|---|---|---|
| `95a36b8` | `dd5b7eb` | infra: bootstrap feasibility experiment pipeline |
| `8d42301` | `1735c15` | exp: add benign HxP policy assay |
| `4486ef3` | `11c0d8c` | exp: validate causal policy carrier on benign task |
| `040592f` | `7f684aa` | exp: probe benign policy writer redundancy |
| `24f2e1e` | `65ee6e7` | exp: audit policy-direction intervention semantics |
| `519cca0` | `bb7b4ed` | exp: decompose benign policy writers |
| `bc1b98b` | `7630c40` | exp: diagnose add-remove causal asymmetry |
| `05960d8` | `6eecd42` | exp: close benign proxy mechanistic diagnosis |
| `8ef64ab` | `22aaef2` | exp: archive public-safe mechanistic feasibility results |
| `0d46e8b` | `a36549a` | fix: track model runtime source excluded by gitignore |

## Commits intentionally not integrated

| KML commit | Reason |
|---|---|
| `02c7bc8` | Relay-only handoff document; contains internal GitLab routing, host-specific metadata and no scientific code/result. |
| `bee82f9` | Relay readiness update only; same public-synchronization concerns and no scientific content. |
| `9372e36` | Relay handoff update documenting runtime recovery; internal transport metadata only. |

## Incoming-file audit

- Incoming diff: 125 files before exclusions, approximately 1.8 MB of tracked data.
- No tracked file exceeds 1 MB; no model weights, checkpoints, optimizer states,
  `.pt`, `.npy` or `.npz` tensors were present.
- Credential-prefix and private-key scans found no secrets.
- Raw completions were sampled and verified as the documented benign
  astronomy/cooking answer-versus-abstain proxy.
- Source/config/tests, summary CSV/JSON, reports and figures were retained.
- Existing GitHub innovation-audit documents remain intact.

## Excluded or sanitized material

| Material | Action | Reason |
|---|---|---|
| `artifacts/sync/KML_SYNC_MANIFEST.md` | Excluded | Internal repository URL and source-host absolute path; transfer metadata, not scientific evidence. |
| `artifacts/sync/KML_RELAY_HANDOFF.md` | Excluded by skipping relay-only commits | Internal GitLab URL, SSH public key/email, host and credential-resolution details. |
| `artifacts/overnight/environment_report.md` source workspace/cache paths | Redacted | Absolute machine paths are unnecessary for public reproducibility. Hardware/software versions remain. |
| `artifacts/safe_mech/raw_layer_examples.pt` | Not present / documented exclusion | 22 MB raw activation cache; reproducible from committed code. |
| `artifacts/safe_mech/writer_scan_state.pt` | Not present / documented exclusion | 22 MB raw activation cache; reproducible from committed code. |

The last two exclusions were already absent from the relay branch and are recorded
in `artifacts/sync/EXCLUDED_LARGE_FILES.md`.

## Import-integrity finding

The first local import check found that every model-facing experiment imports
`src.models.runtime`, but that module was absent from the relay history. Root cause:
the original `.gitignore` rule `models/` matched nested `src/models/` as well as the
intended repository-root model directory. The public integration narrows the rule
to `/models/`.

The source experiment workspace subsequently published commit `0d46e8b` containing
the missing package and runtime module. The module was reviewed, integrated as
`a36549a`, and its imports and tests were rerun before public push. The later
`9372e36` transport-note commit was intentionally excluded.

## Reconciliation policy

The integration used commit history rather than a blind merge. No force push was
used or planned. The controlling combination is:

```text
latest GitHub TODO/research state
+ public-safe KML experiment code and empirical artifacts
```
