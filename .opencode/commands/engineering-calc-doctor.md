<!-- engineering-calc-opencode-managed -->
---
description: Inspect the Engineering Calculation System OpenCode installation
agent: build
---

Run the OpenCode plugin doctor if available:

```text
engineering_calc_doctor {"mode":"verbose","validate":true}
```

If the plugin tool is unavailable, inspect these paths manually:

```text
../../engineering-calculation-system/core/engineering-calculation-system/SKILL.md
../../engineering-calculation-system/core/engineering-calculation-system/skills/00-engineering-calculation-router.skill.md
../../engineering-calculation-system/core/engineering-calculation-system/shared/multi-agent-orchestration.md
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/parallel_work_plan.yaml
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/agent_result_packet.yaml
../../engineering-calculation-system/core/engineering-calculation-system/templates/orchestration/merge_review.md
../../engineering-calculation-system/core/engineering-calculation-system/schemas/artifact_contracts.json
../../engineering-calculation-system/core/engineering-calculation-system/scripts/validate_artifacts.py
```

Then run:

```bash
python ../../engineering-calculation-system/core/engineering-calculation-system/scripts/validate_artifacts.py --package-root ../../engineering-calculation-system/core/engineering-calculation-system --profile core
```
