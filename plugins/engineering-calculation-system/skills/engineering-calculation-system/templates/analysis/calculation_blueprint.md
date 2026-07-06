# Calculation Logic Blueprint

## Scope and purpose

Fill this blueprint after source intake. It is the human-readable index for the structured
calculation package; the CSV ledgers are the source of truth for implementation. Do not start
production calculation modules until the blueprint validation matrix has no blocking rows.

- calculation_object:
- governing_question:
- intended_decision:
- delivery_mode:
- production_readiness: needs_confirmation # needs_confirmation | analysis_ready | production_ready

## Source basis

- accepted_source_ids:
- rejected_or_superseded_source_ids:
- authority_ranking_artifact: analysis/01_source_inventory/source_authority_table.csv
- unresolved_source_conflicts:

## Engineering concept map summary

Summarize only the concepts that drive calculation logic. Keep full rows in `concept_map.csv`.

## Calculation stages

```text
input
-> validation
-> normalization
-> method selection
-> lookup / formula computation
-> branch and special-condition handling
-> check
-> governing summary
-> output
```

## Typed calculation graph

The implementation source of truth is `calculation_nodes.csv`. Use stable IDs:

```text
IN-###   input or user-provided value
VAL-###  validation rule
NORM-### normalization or unit conversion
SEL-###  method selection
LKP-###  lookup/table/chart selection
CAL-###  formula or computation
BR-###   branch/decision
CHK-###  check result
AGG-###  governing aggregation
OUT-###  output/result path
WARN-### warning or limitation
ERR-###  blocking error
```

Every high-risk node must have source_reference, module_candidate, result_visibility,
report_visibility, and test_requirement.

## Input / intermediate / output mapping

Keep detailed rows in:

- `input_semantics_ledger.csv`
- `input_inventory.csv`
- `intermediate_inventory.csv`
- `output_inventory.csv`

Each required BookInput path must map to at least one node and one future test target.

## Method and branch selection

Keep method selection in `method_selection_matrix.csv`; keep branch rules in `branch_inventory.csv`.
Do not let the UI, report template, or runner reinterpret method choice.

## Module candidates

- candidate_modules:
- reusable_library_boundary:
- official_runner_boundary:
- formulas_not_allowed_in:

## Diagrams

Mermaid diagrams are generated views of the structured node model, not the source of truth.

- `analysis/04_diagrams/global_flowchart.mmd`
- `analysis/04_diagrams/data_flow.mmd`
- `analysis/04_diagrams/branch_logic.mmd`
- `analysis/04_diagrams/module_dependency.mmd`

## Source-backed blueprint validation

Fill `blueprint_validation_matrix.csv` after the node graph is drafted and update it again after
formula/lookup/branch extraction. Required checks, required inputs, high-risk nodes, method choices,
formula candidates, lookup candidates, branch rules, and report-visible outputs must be verified
against accepted source material.

```text
ready_for_formula_extraction: no
blocking_validation_rows:
next_route_if_blocked:
```

## Verification targets

- unit_tests:
- golden_cases:
- branch_tests:
- lookup_tests:
- report_trace_tests:

## Open questions

List only blocking or decision-changing questions here. Put machine-checkable rows in
`open_questions.csv` and user decisions in `user_interaction_decisions.csv`.
