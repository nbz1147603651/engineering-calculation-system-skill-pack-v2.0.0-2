# Multi-Agent Orchestration

Use this contract only when the user explicitly asks for multiple agents, parallel work,
delegation, or a platform provides custom worker agents. The same artifacts can also be used by a
single agent or human team to stage work without actual subagents.

## Supervisor Responsibilities

One supervisor owns coordination and final judgment. The supervisor must:

- classify the lifecycle phase with the router before splitting work
- create `templates/orchestration/parallel_work_plan.yaml` when work is split
- create a task brief file for every worker instead of pasting whole chat context
- assign non-overlapping `owned_paths` to every worker
- keep source IDs, node IDs, formula IDs, lookup IDs, branch IDs, module IDs, result paths, and
  test IDs stable
- make evidence gate, coding gate, production, and release decisions
- freeze `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md`
- integrate worker outputs through `templates/orchestration/task_review.md`,
  `templates/orchestration/merge_review.md`, and a review package
- resume long or compacted work from `.engineering-calc/work/progress.md`
- run validation before calling the work complete

Workers may produce drafts, extraction packets, modules, interface slices, or tests. Workers must
not make final gate decisions, rename referenced artifacts, change IDs owned by another task, or
change the official `run_book()` contract unless the supervisor explicitly assigns that integrator
role.

## Parallel-Friendly Work

Good parallel slices have clear inputs, clear output paths, and no shared write surface.

| Phase | Parallel-friendly slices | Supervisor-only merge |
| --- | --- | --- |
| 01-03 acquisition | separate gaps, jurisdictions, source families, source cards | source ID assignment, access decisions, acquisition handoff |
| 04 source intake | separate documents, tables, source cards, conflict candidates | authority ranking, conflict resolution |
| 05-06 logic | formulas, lookups, branches, units, examples, input/output inventory | normalized node graph, ID allocation, handoff readiness |
| 08-12 implementation | core utilities, typed models, independent reusable modules, thin interfaces, reports, batch flows | dependency contract, `run_book()` sequence, public API |
| 13-14 verification | unit tests, regression references, UI smoke, deployment checklist | production/release status and acceptance |

## Serial Gates

These decisions are intentionally serial:

- lifecycle routing when the material state is unclear
- evidence gate status
- source authority priority and conflict resolution
- ID namespace allocation after downstream references exist
- coding gate status
- `implementation_handoff.yaml` and `coding_go_no_go.md` freeze
- `BookInput -> run_book() -> BookResult` contract changes
- final report, production, and release readiness labels

## Ownership Rules

Each worker receives a task brief file with:

- `task_id`
- role
- read-only input paths
- owned write paths
- expected artifacts
- validation commands
- merge point

Workers must write only inside owned paths. Shared registries, handoff files, root README files,
release files, and public API contracts are supervisor-owned unless explicitly listed as the
worker's owned path. If a worker needs a shared file changed, it records the requested change in
its result packet instead of editing the file directly.

## Worker Result Packet

Every delegated task returns `templates/orchestration/agent_result_packet.yaml` or the same fields
in the final message:

- status: `complete`, `partial`, `blocked`, or `not_started`
- changed paths and artifacts created
- source IDs, formula IDs, module IDs, and result paths touched
- assumptions and open questions
- validation run and results
- review verdicts when a worker performed reviewer duties
- completion evidence category and supporting artifacts
- merge notes and conflicts

The supervisor treats missing result packets as incomplete work.

## Task-Scoped And Final Review

Task review is narrow. A task reviewer reads only the task brief, worker report, and review package
unless a concrete named risk requires one focused extra check. It verifies the task's spec
compliance and engineering quality; it does not perform a full release review or re-derive the
whole project state.

Final merge or release review is broad. It uses `templates/orchestration/merge_review.md`, the
progress ledger, and a review package for the full change range to check cross-task consistency,
platform packaging, public API stability, lifecycle gates, and completion evidence.

## Merge Review

Before accepting worker output, the supervisor reviews the worker report, task brief, and review
package in two stages.

Spec compliance:

- owned paths were respected
- no formulas moved into UI, report templates, batch scripts, or CSV/XLSX input
- no worker made gate, ID, authority, or production decisions
- source references and formula traces point to stable evidence
- public interfaces still flow through `run_book(BookInput) -> BookResult`

Engineering quality:

- tests or blockers are recorded for every accepted change
- implementation is local to the assigned layer
- shared contracts changed only through supervisor-owned files
- validation evidence is fresh enough to support the claimed status

When two worker outputs conflict, prefer the source-backed, smaller, and contract-preserving
change. If the conflict affects formula meaning, units, authority, gate status, or public API
shape, stop and resolve it through the normal source and handoff workflow before coding further.
