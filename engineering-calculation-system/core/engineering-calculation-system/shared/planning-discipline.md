# Planning Discipline

Use this file before executing any multi-step engineering calculation plan, release change, or
platform-package update. It defines plan quality; `shared/lifecycle.md` still defines lifecycle
gate status.

## Plan Card

Before implementation, the plan must state:

```text
goal:
global_constraints:
exact_files:
interfaces:
artifact_outputs:
validation_commands:
expected_outputs:
stop_conditions:
```

`global_constraints` must copy binding requirements exactly when they exist: source authority,
runtime stack, delivery mode, version/date, platform target, formula-boundary rule, and
`run_book(BookInput) -> BookResult` contract. If a constraint is unknown and blocks safe work,
route upstream or ask; do not fill it from memory.

## Plan Quality Gate

A plan is executable only when each task has:

- one independently reviewable deliverable
- read-only inputs and owned write paths
- the public interface or artifact shape it consumes and produces
- a command or validator to run, plus the expected result
- a stop condition for missing sources, failed gates, conflicting authority, or failed validation

These are plan failures: `TBD`, `TODO`, `fill in later`, `appropriate error handling`, `handle
edge cases`, `write tests for the above`, `similar to previous task`, or a reference to a function,
schema, ID, source, formula, lookup, branch, or result path not defined in the plan or current
artifacts.

## Handoff

Save long plans as artifacts, not only chat text. When subagents or parallel workers are used,
extract task briefs with `scripts/ecs_execution.py task-brief` and resume from the progress ledger
after compaction.
