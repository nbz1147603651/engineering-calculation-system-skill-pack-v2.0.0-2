# Merge Review

## Context

| Item | Value |
| --- | --- |
| Plan ID | PWP-001 |
| Task ID | TASK-001 |
| Worker role | to_be_defined |
| Reviewer | supervisor |
| Review status | draft / accepted / needs_changes / rejected |

## Required Checks

- [ ] Worker only changed declared owned paths.
- [ ] Result packet is present and complete.
- [ ] No worker made final evidence, coding, production, or release gate decisions.
- [ ] No worker changed source IDs, formula IDs, lookup IDs, branch IDs, module IDs, or result paths outside its assignment.
- [ ] No engineering formulas were added to UI, report templates, batch scripts, CSV/XLSX input files, or presentation-only code.
- [ ] Official calculation flow still uses `run_book(BookInput) -> BookResult`.
- [ ] Source references and formula traces are stable.
- [ ] Tests, validation commands, or blockers are recorded.

## Merge Decision

Decision: draft # accepted | needs_changes | rejected

Reviewer notes:

- to_be_defined
