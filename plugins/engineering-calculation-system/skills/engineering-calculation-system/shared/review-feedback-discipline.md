# Review Feedback Discipline

Use this file before applying user review, external reviewer feedback, worker reports, or tool
diagnostics that request changes to engineering calculation artifacts.

## Feedback Card

Record the decision before editing:

```text
feedback_source:
requested_change:
affected_layer:
source_authority_impact:
unit_or_formula_impact:
lifecycle_gate_impact:
decision: accept | reject | escalate | route_upstream
validation_needed:
```

## Decision Rules

- Accept feedback when it preserves source authority, unit semantics, formula boundaries, lifecycle
  gates, and the public `run_book(BookInput) -> BookResult` contract.
- Reject or push back with evidence when the feedback asks for a formula, lookup, branch, unit,
  pass/fail rule, or production status to be changed in UI, report, batch, template, or adapter
  layers.
- Escalate to the user when feedback conflicts with a source-backed requirement, a frozen handoff,
  a platform constraint, or another reviewer finding.
- Route upstream when the requested change affects source sufficiency, authority priority,
  formula inventory, lookup/branch inventory, input semantics, semantic closure, or coding gate.

Apply multi-item feedback one item at a time. Clarify blocking ambiguity before editing. Run focused
validation after each accepted fix and record the evidence category from
`shared/completion-evidence.md`.

## Weak Evidence

A reviewer report, worker summary, UI screenshot, static HTML file, or old test output is not enough
to support a completion claim. Treat it as a lead to verify against files, commands, source IDs, and
fresh validator output.
