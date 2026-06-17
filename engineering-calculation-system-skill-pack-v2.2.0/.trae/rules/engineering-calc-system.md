# Engineering Calculation System Rules

Use these project rules when working on engineering calculation software in Trae or another rules-based AI IDE.

## Entrypoint

Use the Engineering Calculation System skill pack.

Start with:

```text
skills/00-engineering-calculation-router.skill.md
```

Do not load every child skill at once. Load only the parent and child skills selected by the router.

## Lifecycle

Route work through:

```text
reference acquisition and persistence
-> reference analysis and Calculation Logic Blueprint
-> implementation, interfaces, verification, and traceability
```

## Required Gates

Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.

Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

Do not put formulas in UI, report templates, frontend JavaScript, review notebooks, batch scripts, or CSV/XLSX input files.

Official calculations must flow through:

```text
run_book(BookInput) -> BookResult
```

## Interface Routing

For report, UI, import/export, and batch work:

```text
12-report-review-batch-interfaces.skill.md
12a-report-context-and-rendering.skill.md
12b-frontend-and-review-interfaces.skill.md
12c-batch-import-export-packages.skill.md
```

Use only the subskills required by the task.

## Search and Evidence

During reference discovery, use available internet search or browser tools for missing, insufficient, stale, or jurisdiction-specific references. Log meaningful searches in:

```text
references/acquisition/search_log.csv
```

Record accepted and rejected candidates before analysis proceeds.

## Completion

Use templates from `templates/` for artifacts.

Run validation before considering the work complete:

```bash
python scripts/validate_artifacts.py --package-root .
```
