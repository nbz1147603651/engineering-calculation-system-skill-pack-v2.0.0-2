# Merge Review

## Context

| Item | Value |
| --- | --- |
| Plan ID | PWP-001 |
| Task ID | TASK-001 |
| Worker role | to_be_defined |
| Task brief | `.engineering-calc/work/task-TASK-001-brief.md` |
| Worker report | `templates/orchestration/agent_result_packet.yaml` |
| Review package | `.engineering-calc/work/review-BASE..HEAD.diff` |
| Reviewer | supervisor |
| Review status | draft / accepted / needs_changes / rejected |

## Spec Compliance

- [ ] Worker only changed declared owned paths.
- [ ] Result packet is present and complete.
- [ ] No worker made final evidence, coding, production, or release gate decisions.
- [ ] No worker changed source IDs, formula IDs, lookup IDs, branch IDs, module IDs, or result paths outside its assignment.
- [ ] No engineering formulas were added to UI, report templates, batch scripts, CSV/XLSX input files, or presentation-only code.
- [ ] Official calculation flow still uses `run_book(BookInput) -> BookResult`.
- [ ] Source references and formula traces are stable.
- [ ] Requested shared file changes are listed for supervisor action instead of applied out of scope.

Spec verdict: draft # pass | issues | block

## Engineering Quality

- [ ] The implementation changes the lowest correct layer for the task.
- [ ] Tests, validation commands, or blockers are recorded.
- [ ] Validation evidence is fresh enough to support the claimed completion category.
- [ ] Shared contracts and public interfaces remain coherent.
- [ ] No unrelated refactor or metadata churn is mixed into the worker output.

Engineering verdict: draft # pass | issues | block

## Merge Decision

Decision: draft # accepted | needs_changes | rejected

Reviewer notes:

- to_be_defined
