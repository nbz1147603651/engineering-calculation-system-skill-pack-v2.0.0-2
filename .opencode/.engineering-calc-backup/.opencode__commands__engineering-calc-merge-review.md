<!-- engineering-calc-opencode-managed -->
---
description: Draft a supervisor merge review for worker outputs
agent: build
---

Run Engineering Calculation System supervisor merge review for:

```text
$ARGUMENTS
```

If available, call `engineering_calc_orchestration` with strict JSON object arguments `{"artifact":"merge_review","phase":"implementation"}`.

Check that the worker respected owned paths, returned a complete result packet, did not make supervisor-only decisions, preserved IDs and source traces, kept formulas out of UI/report/batch/input files, preserved `run_book(BookInput) -> BookResult`, and recorded tests or blockers.
