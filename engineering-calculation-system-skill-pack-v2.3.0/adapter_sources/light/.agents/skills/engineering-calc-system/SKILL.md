---
name: engineering-calc-system
description: Portable engineering calculation system skill wrapper for agents that support .agents/skills. Use for reference acquisition, engineering formula extraction, calculation logic blueprints, implementation handoff, auditable calculation software, reports, batch execution, verification, and deployment.
compatibility: generic-agent
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: ../../../SKILL.md
version: 2.4.0
---

# Engineering Calculation System

This is a portable wrapper for agents that discover skills from `.agents/skills`.

## Start Here

Read the root package entrypoint:

```text
../../../SKILL.md
../../../skills/00-engineering-calculation-router.skill.md
```

Then read only the parent and child skill files selected by the router.

Before implementation or release work, also read:

```text
../../../shared/delivery-contract.md
```

If the package shape does not include `skills/`, `shared/`, `templates/`,
`schemas/`, `scripts/validate_artifacts.py`, and `project_template/`, treat the
current install as a lightweight entrypoint and use the full project/root package
or single-file fallback before claiming `web-complete` delivery.

For explicit multi-agent or parallel work, also read:

```text
../../../shared/multi-agent-orchestration.md
../../../templates/orchestration/parallel_work_plan.yaml
../../../templates/orchestration/agent_result_packet.yaml
../../../templates/orchestration/merge_review.md
```

If the target agent cannot access multiple files reliably, use:

```text
the generated dist/singlefile/engineering-calculation-system.all-in-one.md release artifact
```

## Hard Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not skip evidence and handoff gates.
- Keep all official calculations in reusable calculation modules and `run_book(BookInput) -> BookResult`.
- Keep UI, reports, batch scripts, and review tools as thin consumers of trusted results.
- Declare delivery mode before implementation: `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete`; its path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
- Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
- Split parallel work only by disjoint owned paths.
- Keep gate decisions, source authority, ID allocation, handoff freeze, public runner contracts, and final acceptance with the supervisor.
- Validate generated project artifacts with `scripts/validate_artifacts.py --profile core --delivery web-complete`.

## Tooling

MCP servers are optional. Read `../../../adapters/mcp-recommendations.md` before enabling them, and keep source authority, copyright, and access-control rules above tool convenience.
