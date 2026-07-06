# Blueprint Review Checklist

Use this checklist before formula extraction, implementation handoff, or production coding.

## Source Closure

- [ ] Accepted source IDs are stable and recorded in the source registry.
- [ ] Authority ranking is complete for every source used by the blueprint.
- [ ] Source conflicts are resolved or explicitly block coding.
- [ ] Copyright/access limits are respected; no unauthorized source text is copied into artifacts.

## Calculation Intent

- [ ] `calculation_intent_contract.md` states the governing question, intended decision, excluded scope, checks, method families, units, sign conventions, and readiness status.
- [ ] Required checks have stable check IDs.
- [ ] The intended decision matches the requested deliverable.

## AI-Readable Node Graph

- [ ] `calculation_nodes.csv` has one row per input, validation, normalization, method selection, lookup, formula, branch, check, aggregate, output, warning, or error node.
- [ ] Every production node has source_reference, inputs, outputs, units where applicable, module_candidate, result_visibility, report_visibility, and test_requirement.
- [ ] Mermaid diagrams are generated from the node model and do not introduce extra logic.

## Input Semantics

- [ ] Every required BookInput field has unit, sign convention, coordinate direction, default policy, validation rule, and used_by_nodes.
- [ ] No silent defaults, clipping, absolute-value handling, sign flips, or unit conversions remain implicit.
- [ ] Any unresolved input semantic row with `blocks_production=true` is routed upstream.

## Method, Formula, Lookup, and Branch Closure

- [ ] Every method selection row has source_reference, applicability, selection condition, rejection conditions, inputs, outputs, branch link when applicable, and test requirement.
- [ ] Every formula, lookup, and branch candidate has a future inventory row or a validation row explaining why it is not applicable.
- [ ] Every lookup defines interpolation and out-of-range behavior before coding.
- [ ] Every branch defines true/false/not-applicable behavior before coding.

## Blueprint Validation Matrix

- [ ] `blueprint_validation_matrix.csv` verifies required checks, methods, required inputs, high-risk nodes, formula candidates, lookup candidates, branch candidates, and report-visible outputs against accepted sources.
- [ ] Every validation row has review_status `verified`, `accepted`, `not_applicable`, or `source_verified`.
- [ ] No validation row has `blocks_coding=true`.

## Implementation Readiness

- [ ] Module boundaries separate reusable calculation modules from `run_book()`.
- [ ] UI, reports, batch flows, CSV/XLSX files, and review notebooks contain no engineering formulas.
- [ ] Computation graph coverage seeds each production rule with module, runner, result path, and test targets.
- [ ] Open questions, source conflicts, assumptions, and user decisions have no production-blocking rows.
