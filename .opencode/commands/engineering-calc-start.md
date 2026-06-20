<!-- engineering-calc-opencode-managed -->
---
description: Route an engineering calculation task through the skill pack
agent: build
---

Use the Engineering Calculation System workflow for this request:

```text
$ARGUMENTS
```

If available, call `engineering_calc_route` with strict JSON object arguments `{"phase":"router"}`. Then load:

```text
../../engineering-calculation-system/core/engineering-calculation-system/SKILL.md
../../engineering-calculation-system/core/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md
```

Let the router select the parent and child skills. Do not load all child skills at once.

For explicit multi-agent or parallel work, call `engineering_calc_route` with `{"phase":"orchestration","parallel":true}`, then call `engineering_calc_orchestration` with `{"artifact":"parallel_work_plan","phase":"implementation"}` for draft planning artifacts.
