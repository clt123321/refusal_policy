# Model Access Blockers

Status: `BLOCKED_EXTERNAL` for licensed artifact. Human action required; agent did not download.

## 1. Required cells and availability probe (2026-09-13, HF metadata API reachable; weights not downloaded)

| Artifact | Expected provenance (TODO) | Existence on HF | Gated | Local cache | Blocker | Minimum human action |
|---|---|---|---|---|---|---|
| `google/gemma-2-2b-it` | `299a8560bedf22ed1c72a8a11e7dce4a7f9f51f8` | YES | **manual (gate)** | NO | HF token + license acceptance required; IDC segment cannot complete manual gating | Authorized executor accepts Gemma terms and issues a token-protected download path; agent only records hashes afterward |
| `ztcoalson/gemma-2-2b-it-FC` | `03fb41ec87b9ba82c690b60331e5c60b67f6b106` | YES | NO | NO | none (public), but download deferred to executor to keep artifact lineage under authorized control; ~5–6 GB expected | Executor downloads and pins hash; pass path to harness |
| `Qwen/Qwen3-4B` | `1cfa9a7208912126459214e8b04321603b3df60c` | YES | NO | NO | none public; ~8 GB | Executor or agent download under tracked lineage |
| `Fail-Closed alignment code` | commit `892e99b2db2c98f4ecd9b81e414088e15ae7f035` | GitHub (unreachable from IDC) | — | NO | GitHub web+git tunnel blocked | Executor fetches/patches the pinned commit and stores a bundle |
| TamperBench | commit `ca4fadeaab00a72a2c0c87241aaf72807187b800` | GitHub (unreachable from IDC) | — | NO | same | Executor fetches and pins; record hash |
| HarmBench validation IDs | 200 salted-hash IDs per R0b | data repo TBD | — | NO | data revision not pinned locally | Executor pins data revision and hashes |
| Fail-Closed benign prompts (1,000) | released benign set | — | — | NO | as above | same |

## 2. Locally available (eligible for benign/engineering fixtures only)

- `Qwen/Qwen2.5-0.5B-Instruct` (954 MB) and `Qwen/Qwen2.5-1.5B-Instruct` (2.9 GB) — DEV-ONLY, used for harness dry run and math tests, never for scientific results.
- `sshleifer/tiny-gpt2` (6.2 MB) — plumbing fixture.

## 3. Policy note

No proxy mirror, no license bypass, no unauthorized image. Any missing artifact is `BLOCKED_EXTERNAL` until the authorized executor provides pinned, licensed access.
