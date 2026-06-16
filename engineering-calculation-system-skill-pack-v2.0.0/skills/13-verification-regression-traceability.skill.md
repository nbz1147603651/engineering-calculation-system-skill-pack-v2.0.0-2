---
name: verification-regression-traceability
description: Design and implement verification, regression tests, tolerance policy, formula trace checks, input/result hashes, report smoke tests, Marimo review smoke tests, upload package checks, batch summary checks, and acceptance gates for engineering calculation book systems.
---

# Verification, Regression, and Traceability

Use this skill throughout implementation and before release.

## Goal

Verify formulas, lookups, branches, book orchestration, report context, interfaces, and traceability.

## Test Categories

```text
unit tests for isolated formulas
lookup tests for tables and interpolation
branch tests for method selection
edge case tests for boundary conditions
invalid input tests
regression tests against references
integration tests for complete run_book workflows
report smoke tests
Marimo review smoke tests
upload/import package manifest and hash tests
batch smoke tests
serialization and hash tests
```

## Regression Reference Priority

```text
design code examples
published design manual examples
approved historical reports
verified legacy spreadsheets
independent hand calculations
synthetic edge cases
```

## Traceability Metadata

For production results, include where feasible:

```text
book_type
book_name
case_id
project_id
design_code and version
run_timestamp
package version
input_hash
result_hash
python_version
git_commit if available
formula registry version if used
runner version
report template version
```

## Required Output Artifacts

```text
verification/test_matrix.csv
verification/regression_references.md
verification/tolerance_policy.md
verification/acceptance_checklist.md
tests/unit/
tests/regression/
tests/integration/
tests/smoke/
```

## Acceptance Checklist

Verify:

```text
source basis is recorded
features are classified into layers
formulas live only in reusable calculation modules
book runner is the official calculation entry point
CSV/JSON/frontend/API inputs map to the same BookInput
unit conversions happen only at input/output boundaries
templates do not calculate
frontend/review does not calculate
Marimo review pages do not calculate outside trusted modules or run_book
upload packages preserve manifests, hashes, normalized inputs, and trusted results
batch does not calculate independently
units are explicit
result objects include intermediate values
warnings and errors are preserved
status semantics are defined
governing summary exists
tests cover reusable modules
book integration test exists
report rendering smoke test exists when reports exist
traceability metadata exists for production outputs
run commands are documented
```

## Required Final Response

Provide:

```text
test matrix summary
regression references
tolerance policy
traceability plan
acceptance result
remaining verification risks
```
