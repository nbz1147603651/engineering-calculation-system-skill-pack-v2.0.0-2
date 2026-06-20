---
name: engineering-calc-system
description: Full lifecycle engineering calculation system workflow for OpenCode. Use for reference discovery, source authority review, formula and branch extraction, logic blueprints, implementation handoff, auditable calculation software, reports, batch flows, verification, traceability, and deployable web calculators.
compatibility: opencode
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: "{{SKILL_ROOT_RELATIVE}}/SKILL.md"
  plugin: engineering-calculation-system-opencode-plugin
---

# Engineering Calculation System

This OpenCode wrapper points to the installed Engineering Calculation System skill pack.

## Load Order

1. Read `{{SKILL_ROOT_RELATIVE}}/SKILL.md`.
2. Read `{{SKILL_ROOT_RELATIVE}}/skills/00-engineering-calculation-router.skill.md`.
3. Read only the parent and child skill files selected by the router.
4. For explicit multi-agent or parallel work, read `{{SKILL_ROOT_RELATIVE}}/shared/multi-agent-orchestration.md` and use `{{SKILL_ROOT_RELATIVE}}/templates/orchestration/`.
5. Use `{{SKILL_ROOT_RELATIVE}}/templates/`, `{{SKILL_ROOT_RELATIVE}}/shared/`, and `{{SKILL_ROOT_RELATIVE}}/schemas/` only when generating or validating artifacts.

If the plugin tool is available, call `engineering_calc_route` with strict JSON object arguments before loading detailed files, for example `{"phase":"router"}`. Do not use shorthand such as `phase=router`, comments, trailing commas, or single-quoted JSON. For explicit parallel work, call `engineering_calc_route` with `{"phase":"orchestration","parallel":true}` or use `engineering_calc_orchestration` with JSON object arguments to generate draft orchestration artifacts as text.

## Non-Negotiable Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.
- Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Parallel workers must have disjoint `owned_paths`, return an agent result packet, and wait for supervisor merge review before their output is accepted.
- Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, public runner contracts, production labels, release acceptance, or final acceptance.
- Run `python scripts/validate_artifacts.py --package-root . --profile core` before calling the package complete.

## Optional MCPs

Before enabling MCP servers, read `{{SKILL_ROOT_RELATIVE}}/adapters/mcp-recommendations.md` when that adapter file is present. Use MCPs as optional accelerators for search, docs lookup, public code search, diagnostics, and UI testing; never treat MCP output as authoritative engineering evidence without citation and validation.
