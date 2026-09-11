DATA_SYNC_COMPLETE

## Verified synchronization state

GitHub integrated-data HEAD (verified before this completion-record commit):
`87345435ddd0787309083f55f707fe3f3ebadffc`

KML experiment HEAD:
`9372e36930c9d759027debaba05225af271525da`

GitHub research baseline:
`e63c83a635cb5d5ec7187cbe0abb1cc36fe74029`

The completion record necessarily advances `main` by one documentation commit;
after pushing it, local `HEAD` and `origin/main` are verified again. Full history and
source-to-integrated commit mapping are recorded in `research/SYNC_RECONCILIATION.md`.

## Integrated experiment commits

```text
dd5b7eb infra: bootstrap feasibility experiment pipeline
1735c15 exp: add benign HxP policy assay
11c0d8c exp: validate causal policy carrier on benign task
7f684aa exp: probe benign policy writer redundancy
65ee6e7 exp: audit policy-direction intervention semantics
bb7b4ed exp: decompose benign policy writers
7630c40 exp: diagnose add-remove causal asymmetry
6eecd42 exp: close benign proxy mechanistic diagnosis
22aaef2 exp: archive public-safe mechanistic feasibility results
a36549a fix: track model runtime source excluded by gitignore
```

Reconciliation documentation:

```text
19687ac chore: reconcile KML experiment history
8734543 docs: finalize KML reconciliation after runtime recovery
```

## Artifacts now available

- `src/`, `scripts/`, `configs/feasibility/` and `tests/` experiment infrastructure;
- `artifacts/safe_mech/SAFE_MECH_REPORT.md`;
- `artifacts/safe_mech/ASYMMETRY_DIAGNOSIS.md`;
- `artifacts/safe_mech/SAFE_PROXY_CLOSEOUT.md`;
- safe-mech CSV/JSON/JSONL result tables and benign raw generations;
- ten PNG figures under `artifacts/safe_mech/figures/`;
- feasibility and overnight environment/decision records;
- GitHub research audit, evidence base, novelty collisions and candidate stories.

## Excluded files

- `artifacts/sync/KML_SYNC_MANIFEST.md`: internal relay URL and source-host path;
- `artifacts/sync/KML_RELAY_HANDOFF.md`: internal GitLab/SSH/credential-transfer metadata;
- relay-only commits `02c7bc8`, `bee82f9`, `9372e36`: transport records, no scientific content;
- `artifacts/safe_mech/raw_layer_examples.pt`: 22 MB reproducible raw activation cache;
- `artifacts/safe_mech/writer_scan_state.pt`: 22 MB reproducible raw writer cache.

Machine-local absolute paths in `artifacts/overnight/environment_report.md` were
redacted while retaining hardware and software versions.

## Validation

**PASS**

- `HEAD == origin/main` at integrated-data verification: PASS;
- required code, research files, reports, CSV/JSON and figures in `origin/main`: PASS;
- GitHub raw visibility for code, research report, safe-mech report and representative figure: HTTP 200;
- Python syntax compilation: 44 files passed;
- repository tests: 10/10 pytest-style assertion functions passed using the local
  PyTorch environment and a model-loading dependency stub; `pytest` and
  `transformers` themselves are not installed on this Mac, so model-loading tests
  were not attempted;
- artifact parsing: 26 JSON, 14 JSONL and 16 CSV files passed;
- report artifact references: 41 checked, zero missing;
- files over 20 MB: none;
- credential/private-key/internal-path scan: no included matches;
- `TODO.md` and the `e63c83a` research audit state were not overwritten;
- force push: not used.
