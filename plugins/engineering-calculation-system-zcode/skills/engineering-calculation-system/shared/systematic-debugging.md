# Systematic Debugging

Use this file before fixing bugs, failing tests, inconsistent reports, unexpected UI results, or
deployment/runtime issues in an engineering calculation project.

## Root-Cause Chain

Trace the issue through the lowest applicable layer:

```text
source/evidence
-> formula_inventory / lookup_inventory / branch_inventory / unit conventions
-> reusable module
-> run_book(BookInput) -> BookResult
-> API / batch / import-export
-> report / UI / Marimo review
```

Fix the first layer that is wrong. Do not hide formula, unit, branch, lookup, or source problems
in UI JavaScript, report templates, batch scripts, CSV/XLSX inputs, or static HTML.

## Debug Record

Record this before implementation:

```text
observed_failure:
reproduction:
first_bad_layer:
source_or_handoff_impact:
root_cause_hypothesis:
test_or_smoke_to_prove_fix:
```

If the first bad layer is source, authority, formula, lookup, branch, unit, semantic closure, or
handoff status, route upstream through the matching 04-07 or 10-11 path before touching interface
layers.

## Condition-Based Waiting

For web, API, Marimo, deployment, and review readiness checks, wait for the condition that proves
readiness instead of guessing with sleep:

- health route returns expected status
- API route returns a valid `BookResult`-backed payload
- review session state is written and readable
- Marimo/admin route exists or reports the documented missing-install fallback
- report artifact exists and contains required sections

Use a bounded timeout with a clear error. Old output, arbitrary delay, or a page opening once is not
fresh validation evidence.

## Defense-In-Depth Validation

When a bug is caused by bad data or unsafe state, add checks at every layer it crosses:

- input/model boundary rejects invalid or ambiguous values
- reusable module preserves units, signs, formulas, lookups, and branch rules
- `run_book()` preserves warnings/errors and governing status
- API, batch, import/export, UI, report, and review layers remain thin over `BookResult`
- deployment/admin routes expose explicit health or fallback states

The goal is not one guard that hides the symptom; it is a path where the same bad value cannot
silently reach a misleading engineering result.

## Completion

A bug is fixed only when `shared/completion-evidence.md` has `bug fixed` evidence: root cause
trace, minimal reproduction, lowest-layer fix, and fresh validation.
