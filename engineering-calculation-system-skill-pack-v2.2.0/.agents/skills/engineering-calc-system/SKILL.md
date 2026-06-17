---
name: engineering-calc-system
description: Portable engineering calculation system skill wrapper for agents that support .agents/skills. Use for reference acquisition, engineering formula extraction, calculation logic blueprints, implementation handoff, auditable calculation software, reports, batch execution, verification, and deployment.
compatibility: generic-agent
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: ../../../SKILL.md
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

If the target agent cannot access multiple files reliably, use:

```text
../../../engineering-calculation-system.all-in-one.md
```

## Hard Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not skip evidence and handoff gates.
- Keep all official calculations in reusable calculation modules and `run_book(BookInput) -> BookResult`.
- Keep UI, reports, batch scripts, and review tools as thin consumers of trusted results.
- Validate the package and generated project artifacts with `scripts/validate_artifacts.py`.

## Tooling

MCP servers are optional. Read `../../../adapters/mcp-recommendations.md` before enabling them, and keep source authority, copyright, and access-control rules above tool convenience.
