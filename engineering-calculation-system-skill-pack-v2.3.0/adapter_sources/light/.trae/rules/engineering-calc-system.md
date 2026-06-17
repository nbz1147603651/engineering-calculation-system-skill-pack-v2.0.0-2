# Engineering Calculation System Rules

Use these project rules when working on engineering calculation software in Trae or another rules-based AI IDE.

## Entrypoint

Use the Engineering Calculation System skill pack.

Start with:

```text
SKILL.md
skills/00-engineering-calculation-router.skill.md
```

Do not load every child skill at once. Load only the parent and child skills selected by the router.

For explicit multi-agent, delegated, or parallel work, also load:

```text
shared/multi-agent-orchestration.md
templates/orchestration/parallel_work_plan.yaml
templates/orchestration/agent_result_packet.yaml
templates/orchestration/merge_review.md
```

If the environment cannot read the package as multiple files, load:

```text
engineering-calculation-system.all-in-one.md
```

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

## Parallel Work

Parallel work is optional. Use it only after routing is clear.

Allowed: split source searches, document intake, formula/lookup/branch extraction, independent modules, thin interfaces, and tests by disjoint owned paths.

Forbidden: delegating evidence gates, coding gates, source authority, ID allocation, handoff freeze, `run_book()` contract changes, production labels, or release acceptance.

Each worker must return an agent result packet. Accept output only after supervisor merge review.

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

## Optional MCPs

MCP servers are optional accelerators, not required dependencies. Before enabling MCPs, read:

```text
adapters/mcp-recommendations.md
```

Prefer search/fetch, documentation lookup, LSP/diagnostics, authorized PDF extraction, and browser testing. Do not enable secret-bearing, broad external-system, or restricted-access MCPs unless the user confirms scope and credentials.

## Completion

Use templates from `templates/` for artifacts.

Run validation before considering the work complete:

```bash
python scripts/validate_artifacts.py --package-root .
```
