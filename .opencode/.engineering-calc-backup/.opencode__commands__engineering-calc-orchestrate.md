<!-- engineering-calc-opencode-managed -->
---
description: Draft a supervisor-owned multi-agent orchestration plan
agent: build
---

Use the Engineering Calculation System v2.4.0 orchestration workflow for:

```text
$ARGUMENTS
```

If available, call `engineering_calc_route` with strict JSON object arguments `{"phase":"orchestration","parallel":true}`, then call `engineering_calc_orchestration` with `{"artifact":"parallel_work_plan","phase":"implementation"}`.

Load:

```text
../../engineering-calculation-system/core/engineering-calculation-system/shared/multi-agent-orchestration.md
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/parallel_work_plan.yaml
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/agent_result_packet.yaml
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/merge_review.md
```

The supervisor owns lifecycle routing, gate decisions, source authority, ID allocation, handoff freeze, public runner contract changes, production/release labels, merge review, validation, and final acceptance.
