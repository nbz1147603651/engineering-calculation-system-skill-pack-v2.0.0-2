# Calculation Intent Contract

## Status

status: production_ready

## Calculation Purpose

- calculation_object: template demand/capacity demonstration
- design_or_check_situation: validate the project scaffold can evaluate one source-backed check
- governing_question: is demand/capacity utilization within the stated limit
- intended_decision: prove the official run_book path returns traceable checks
- excluded_scope: real engineering design decisions

## Required Checks

| Check ID | Check name | Engineering purpose | Design situation | Required output | Pass/fail basis | Source reference | Risk level |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHK-001 | Template demand/capacity check | Demonstrate an evaluated check | Template scaffold smoke case | utilization and status | utilization <= limit | S01 | low |

## Method Families In Scope

| Method family | Applies to checks | Source reference | Selection basis | Rejection basis |
| --- | --- | --- | --- | --- |
| Demand/capacity ratio | CHK-001 | S01 | template check payload includes demand, capacity, and limit | missing capacity or non-finite values |

## Input Semantics Summary

- unit_system: project input units are passed through for display; utilization is a ratio
- sign_convention: demand and capacity magnitudes are compared by absolute value for this template demonstration
- coordinate_convention: not applicable to the template demonstration
- load_case_policy: one supplied check row is one evaluated case
- default_policy: no production engineering defaults; template fallbacks are scaffold behavior only

## Production Readiness

- All checks have a method in `method_selection_matrix.csv`.
- All BookInput fields have a row in `input_semantics_ledger.csv`.
- All formulas, lookups, branches, and high-risk nodes close through `computation_graph_coverage.csv`.
- All production defaults, estimates, clipping, absolute-value handling, and sign conversions are explicit.
