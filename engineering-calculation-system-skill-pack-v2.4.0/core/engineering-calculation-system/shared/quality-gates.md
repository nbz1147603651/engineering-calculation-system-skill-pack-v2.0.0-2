# Quality Gates

## Evidence gate

```text
evidence_no_go
search_required
partial_analysis_allowed
analysis_allowed
```

`analysis_allowed` requires:

```text
minimum governing or reference basis exists
source IDs are stable
coverage matrix exists
major unresolved gaps are recorded
copyright/access limitations are recorded
```

## Handoff gate

```text
no_go
prototype_allowed
production_allowed
```

`production_allowed` requires:

```text
critical formulas source-backed
critical lookup/interpolation rules defined
major branch rules defined
unit and sign conventions defined
source conflicts resolved or explicitly handled
test requirements defined
```

## Semantic production gate

When `handoff/implementation_handoff.yaml` or `coding_go_no_go.md` claims
`production_allowed`, the artifact set must also pass semantic consistency
checks, not only file-existence checks:

```text
acquisition_handoff.yaml status is analysis_allowed
critical/high source coverage rows that block coding are covered
critical/high coverage rows have stable current_source_id values
formula inventory rows have actionable source_reference and test_requirement values
lookup rows define interpolation_rule, out_of_range_behavior, source_reference, and test_requirement
branch rows define source_reference, true/false paths, and required_tests
open questions with blocks_coding=true are resolved or gate is downgraded
source conflicts with blocks_coding=true are resolved or gate is downgraded
assumptions with blocks_production=true are resolved or gate is downgraded
```

If these checks fail, downgrade the gate to `prototype_allowed` or `no_go`.

## Implementation gate

Before release:

```text
formulas only in calculation modules/books
one official run_book()
typed input/result models
unit conversion only at boundaries
warnings/errors preserved
result paths stable
reusable modules are decoupled and registered as assets
UI and review apps follow the unified layout when present
upload/import packages have manifests and hashes when present
unit, branch, lookup, regression, integration, and smoke tests pass
traceability metadata saved
```

## Report production gate

Before labeling any report or export as final or production-ready:

```text
report production decision recorded
report status explicit
source basis and coding gate allow production
report generated from saved final input or trusted saved BookResult
ReportContext includes source basis, assumptions, limitations, warnings, errors, and traceability metadata
unified UI layout is documented when frontend exists
UI design system assets exist when production frontend exists
automatic report output decision is recorded when calculation-book export exists
LaTeX/Overleaf template decision is recorded when calculation-book export exists, including user selection/decline/no-response default and the resolved `latex_template_id`
LaTeX/PDF output compiles with exit code 0 and `main.pdf` exists when `latexmk` or `pdflatex` is available
A4 HTML report with `@page size: A4` is used when no local LaTeX compiler is available
Marimo review app is documented when module review exists
data package manifest exists when import/export packages exist
templates, UI, Marimo apps, and batch flows do not calculate or override status
renderer/export smoke test passes
run command documented
```

If any item is missing, use a non-final status such as `draft`, `review`, `prototype`, or `not_for_construction`.

## Release and deployment gate

Before labeling an online web calculation program as complete, production-ready, or deployable:

```text
local web client run command documented and smoke-tested
cloud Linux deployment path documented
web app exposes a health endpoint
production server entrypoint exists
environment variables control secrets, debug mode, host, port, data, and output paths
delivery is not only a static HTML file, exported report HTML, or mockup unless explicitly labeled as a non-production prototype
Dockerfile or systemd service exists when cloud deployment is required
nginx or platform proxy guidance exists when the app is internet-facing
calculation modules remain independent from web, report, batch, and deployment layers
module_asset_registry.csv records reusable calculation assets
release checklist records smoke tests and remaining assumptions
```

If any release item is missing, use `review`, `deployment_blocked`, or `not_production_ready`.
