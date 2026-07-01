# Execution Discipline

Use this file with the router for every non-trivial engineering calculation task. It does not
define lifecycle gates; `shared/lifecycle.md` remains the single source for the 01-14 gates and
delivery bar.

## Required Cards

Before analysis, coding, verification, release, or completion claims, write these four cards in
working notes or the final phase handoff.

### Route Card

```text
task_type:
material_state:
required_skill_path:
delivery_mode:
plan_required:
review_feedback_mode:
workspace_isolation:
parallel_suitability:
immediate_next_action:
```

### Gate Card

```text
evidence_gate:
coding_gate:
handoff_status:
blocking_gaps:
```

Use only the gate vocabulary from `shared/lifecycle.md`.

### Artifact Contract

```text
required_inputs:
artifacts_to_create_or_update:
owned_paths:
shared_paths_requiring_supervisor_review:
```

### Validation Evidence

```text
commands_run:
exit_status:
key_output:
remaining_blockers:
completion_evidence_category:
```

The completion evidence category must match `shared/completion-evidence.md`.

## Anti-Randomness Rules

- Do not start coding from chat memory. Start from the route card and gate card.
- Do not treat UI, static HTML, notebooks, old test output, or an agent report as completion
  evidence.
- For multi-step work, validate the plan against `shared/planning-discipline.md` before executing.
- For review feedback, classify the requested change with `shared/review-feedback-discipline.md`
  before editing.
- For package, plugin, adapter, or release work, record workspace state with
  `shared/version-control-discipline.md`.
- If context is compacted or resumed, rebuild state from artifacts and `.engineering-calc/work/`
  ledger files before continuing.
- If an input artifact is missing, label the gate as blocked or route upstream. Do not invent a
  source, formula, unit, coefficient, lookup, branch, or production status.
