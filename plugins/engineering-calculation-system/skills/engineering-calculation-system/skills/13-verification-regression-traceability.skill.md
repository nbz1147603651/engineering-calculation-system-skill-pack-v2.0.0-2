---
name: verification-regression-traceability
description: Design and implement verification, golden-case regression tests, tolerance policy, formula trace checks, module asset checks, input/result hashes, report smoke tests, web/API smoke tests, Marimo review smoke tests, upload package checks, batch summary checks, deployment smoke tests, and acceptance gates for engineering calculation book systems.
---

# Verification, Regression, and Traceability

## When to use

Throughout implementation and before release. Verify formulas, lookups, branches, book
orchestration, report context, interfaces, and traceability.

## Steps

1. Build the test matrix (`templates/verification/test_matrix.csv`) covering: unit (isolated
   formulas), lookup (tables/interpolation), branch (method selection), edge-case (boundary),
   invalid-input, regression (against references), integration (full `run_book`), report smoke,
   web/API smoke, Chinese/English i18n + language-toggle smoke, Marimo review smoke, upload/import
   package manifest + hash, batch smoke, serialization + hash, formula-registry validation +
   publish-gate, and deployment smoke (local + Linux cloud).
2. Build the golden case registry (`templates/verification/golden_case_registry.csv`) with at
   least one production-relevant case for every high-risk check/method family. Golden cases verify
   module and runner behavior; they do not need to match a report verbatim, but must state
   reference basis, input path, expected behavior/result path, tolerance, status, and whether they
   block production.
3. Capture regression references (`templates/verification/regression_references.md`) in priority
   order: design-code examples -> published manual examples -> approved historical reports ->
   verified legacy spreadsheets -> independent hand calcs -> synthetic edge cases.
4. Define the tolerance policy (`templates/verification/tolerance_policy.md`).
5. Attach traceability metadata to production results: book_type, book_name, case_id, project_id,
   design_code + version, run_timestamp, package version, input_hash, result_hash, python_version,
   git_commit if available, formula-registry version if used, runner version, report-template
   version.
6. Run the acceptance checklist (`templates/verification/acceptance_checklist.md`): source basis
   recorded; features classified by layer; formulas only in reusable modules; modules listed in
   `module_asset_registry.csv`; `run_book` is the official entry point; CSV/JSON/frontend/API inputs
   map to the same BookInput; unit conversion only at boundaries; templates/UI/review/Marimo/batch
   do not calculate; upload packages preserve manifests/hashes/normalized inputs/trusted results;
   units explicit; result objects include intermediate values; warnings/errors preserved; status
   semantics defined; governing summary exists; tests cover modules; book integration test exists;
   report/web/i18n smoke tests exist when those layers exist; deployment smoke or recorded
   blockers when final delivery expected; traceability metadata on production outputs; formula-
   registry version/hash/published_at in BookResult when used; run commands documented.

## Artifacts

```text
verification/test_matrix.csv            (templates/verification/test_matrix.csv)
verification/golden_case_registry.csv   (templates/verification/golden_case_registry.csv)
verification/regression_references.md   (templates/verification/regression_references.md)
verification/tolerance_policy.md        (templates/verification/tolerance_policy.md)
verification/acceptance_checklist.md    (templates/verification/acceptance_checklist.md)
tests/{unit,regression,integration,smoke}/
release/release_checklist.md            (when final delivery expected)
```

## Exit gate

Hard blockers are fixed or delivery is downgraded; validator passes before any completion claim.
See `shared/lifecycle.md` row 13. Next path: 14 for release/deployment.
