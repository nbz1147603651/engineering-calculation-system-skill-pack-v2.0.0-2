# Tolerance Policy

Define absolute/relative tolerances per formula, lookup, branch, and integration result before
claiming formula verification.

## Required Fields

For each result path covered by `golden_case_registry.csv` or regression tests, record:

| Field | Meaning |
| --- | --- |
| result_path | Stable `BookResult` path, for example `checks[0].utilization` |
| quantity | Engineering meaning and source equation/table/branch |
| comparison_mode | `exact`, `absolute`, `relative`, or `absolute_and_relative` |
| abs_tolerance | Maximum absolute difference, with unit |
| rel_tolerance | Maximum relative difference, dimensionless |
| rounding_policy | Whether the source rounds inputs, intermediates, or final values |
| source_reference | Source ID plus clause/table/equation/example |
| blocks_production | `true` when failure prevents production use |

## Registry Syntax

Use explicit key-value expectations in `golden_case_registry.csv`:

```text
expected_value=0.5; expected_status=PASS; status_path=checks[0].status
```

Supported tolerance values for the template runner:

```text
exact
0.001
abs:0.001
rel:1e-6
abs=0.001; rel=1e-6
```

`exact` is appropriate only for discrete statuses, branch choices, IDs, or simple decimal cases
that are not affected by floating-point roundoff. Prefer explicit absolute/relative tolerances for
engineering formulas, lookup interpolation, and integration results.

## Minimum Coverage

- One golden case for each high-risk check/method family.
- At least one boundary case for each branch condition.
- At least one out-of-range or invalid-input case for each lookup or required input group.
- Regression references prioritized as: design-code examples, manual examples, approved historical
  reports, verified legacy spreadsheets, independent hand calculations, then synthetic edge cases.

Run the project template command before verification claims:

```bash
python scripts/verify_golden_cases.py --project-root .
```
