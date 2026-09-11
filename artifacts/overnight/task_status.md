# Overnight Task Status

| Task | Status | Evidence / blocker |
|---|---|---|
| P01 | BLOCKED_HUMAN_REVIEW | No preregistration artifact or claim-contract freeze exists in repository. |
| P02 | BLOCKED_HUMAN_REVIEW | No attack matrix, cost ledger, or sealed A4 manifest exists; attack implementation cannot be executed here. |
| P03 | BLOCKED_HUMAN_REVIEW | No approved datasets, split manifests, evaluator cards, or human calibration records exist. |
| P04 | BLOCKED_HUMAN_REVIEW | No harness, smoke tests, model configuration, or model cache exists. |
| C01 | NOT RUN | Requires model, approved data, capture harness, and policy-mechanism experimentation. |
| C02 | NOT RUN | Depends on C01 and construct-fit data. |
| C03 | NOT RUN | Requires intervention that changes refusal-policy behavior. |
| C04 | NOT RUN | Requires intervention/control battery. |
| C05 | NOT RUN | Requires writer intervention and backup discovery. |
| A01 | NOT RUN | Requires restricted writer-cut attack experiment. |
| A02 | NOT RUN | No approved capability/hazard-accessibility datasets. |
| A03 | NOT RUN | Requires parameter-space safety-policy edit. |
| A04 | NOT RUN | Requires adaptive attack/fine-tuning calibration. |
| A05 | NOT DECIDABLE | No feasibility measurements available. |

## Gate state

- Gate 0: BLOCKED_HUMAN_REVIEW
- Gate 1: NOT_YET_DECIDABLE
- Recipe training: NOT AUTHORIZED / NOT RUN
- Sealed A4: NOT AUTHORIZED / NOT RUN
