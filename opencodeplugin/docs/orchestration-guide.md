# Orchestration Guide

Use multi-agent orchestration only when the user explicitly asks for multiple agents, subagents, delegation, or parallel work.

## Flow

1. Supervisor routes lifecycle phase.
2. Supervisor creates or reviews a `parallel_work_plan`.
3. Workers receive read-only inputs and disjoint `owned_paths`.
4. Workers return `agent_result_packet` fields.
5. Supervisor runs `merge_review`.
6. Supervisor runs validation and decides final acceptance.

## OpenCode Commands

```text
/engineering-calc-orchestrate
/engineering-calc-worker-packet
/engineering-calc-merge-review
```

## Supervisor-Only Decisions

- lifecycle routing when material state is unclear
- evidence gate status
- source authority priority and conflict resolution
- ID namespace allocation
- coding gate status
- handoff freeze
- `BookInput -> run_book() -> BookResult` contract changes
- production, release, and final acceptance labels

## Worker Rules

Workers edit only declared `owned_paths`, keep formulas out of UI/report/batch/input files, and return result packets before their work is accepted.

