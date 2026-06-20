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
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/shared/multi-agent-orchestration.md
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/parallel_work_plan.yaml
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/agent_result_packet.yaml
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/merge_review.md
```

The supervisor owns lifecycle routing, gate decisions, source authority, ID allocation, handoff freeze, public runner contract changes, production/release labels, merge review, validation, and final acceptance.
