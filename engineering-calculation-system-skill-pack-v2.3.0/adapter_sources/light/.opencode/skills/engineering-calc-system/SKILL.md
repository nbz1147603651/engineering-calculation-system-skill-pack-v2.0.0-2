---
name: engineering-calc-system
description: Full lifecycle engineering calculation system workflow. Use for engineering calculation reference discovery, formula/lookup/branch extraction, calculation logic blueprints, implementation handoff, auditable calculation-book software, reports, batch flows, verification, traceability, and deployable web calculators.
compatibility: opencode
metadata:
  package: engineering-calculation-system-skill-pack
  entrypoint: ../../../SKILL.md
version: 2.4.0
---

# Engineering Calculation System

This is an OpenCode wrapper for the root Engineering Calculation System skill pack.

## Load Order

1. Read `../../../SKILL.md`.
2. Read `../../../skills/00-engineering-calculation-router.skill.md`.
3. Read only the parent and child skill files selected by the router.
4. For explicit multi-agent or parallel work, read `../../../shared/multi-agent-orchestration.md` and use `../../../templates/orchestration/`.
5. Before implementation or release work, read `../../../shared/delivery-contract.md`.
6. Use `../../../templates/`, `../../../shared/`, and `../../../schemas/` only when generating or validating artifacts.

If relative file loading is unavailable, load the generated `dist/singlefile/engineering-calculation-system.all-in-one.md` release artifact.

If the package shape lacks `skills/`, `shared/`, `templates/`, `schemas/`,
`scripts/validate_artifacts.py`, or `project_template/`, treat the install as a
lightweight entrypoint and use the full project/root package or single-file
fallback before claiming `web-complete`.

## Non-Negotiable Rules

- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.
- Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.
- Keep formulas out of UI, report templates, frontend JavaScript, review notebooks, batch scripts, and CSV/XLSX input files.
- Route official calculations through `run_book(BookInput) -> BookResult`.
- Declare delivery mode before implementation: `core-only`, `report-only`, `prototype-web`, or `web-complete`.
- Default to `web-complete`; its path is `08 -> 09 -> 10 -> 11 -> 12a -> 12b -> 12c -> 13 -> 14`.
- Do not call CLI runners, static HTML, exported report HTML, notebooks, or UI mockups complete or deployable.
- Parallel workers must have disjoint `owned_paths`, return an agent result packet, and wait for supervisor merge review before their output is accepted.
- Do not delegate evidence gates, coding gates, source authority, ID allocation, handoff freeze, public runner contracts, or final acceptance.
- Run `python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete` before calling a generated project complete.

## Optional MCPs

Before enabling MCP servers, read `../../../adapters/mcp-recommendations.md`. Use MCPs as optional tools for search, docs lookup, public code search, diagnostics, and UI testing; never treat MCP output as authoritative engineering source material without citation and validation.
