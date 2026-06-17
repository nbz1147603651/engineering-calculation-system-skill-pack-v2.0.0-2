---
description: Inspect the Engineering Calculation System OpenCode installation
agent: build
---

Run the OpenCode plugin doctor if available:

```text
engineering_calc_doctor profile=core validate=true
```

If the plugin tool is unavailable, inspect these paths manually:

```text
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/SKILL.md
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/skills/00-engineering-calculation-router.skill.md
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/shared/multi-agent-orchestration.md
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/parallel_work_plan.yaml
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/agent_result_packet.yaml
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/templates/orchestration/merge_review.md
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/schemas/artifact_contracts.json
{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/scripts/validate_artifacts.py
```

Then run:

```bash
python {{SKILL_ROOT_RELATIVE_FROM_COMMAND}}/scripts/validate_artifacts.py --package-root {{SKILL_ROOT_RELATIVE_FROM_COMMAND}} --profile core
```
