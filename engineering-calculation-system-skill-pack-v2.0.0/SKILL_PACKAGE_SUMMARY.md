# Skill Package Summary

## Package purpose

Create a maintainable skill architecture for engineering calculation systems covering:

```text
1. reference discovery and local persistence
2. reference analysis and calculation logic modeling
3. implementation of auditable calculation book software
```

## Design decision

Use parent orchestrators plus specialized child skills:

```text
root SKILL.md entrypoint
3 parent skills
14 child skills
shared contracts
templates
artifact schemas
validation scripts
project scaffold
examples
```

## Main gates

```text
evidence gate
analysis gate
implementation handoff gate
coding gate
report production gate
verification gate
```

## Main artifacts

```text
reference_gap_assessment.md
acquisition_plan.yaml
source_coverage_matrix.csv
source_registry.yaml
acquisition_handoff.yaml
calculation_blueprint.md
formula_inventory.csv
implementation_handoff.yaml
BookInput / BookResult models
run_book()
unified UI layout spec
Marimo review spec
data_package_manifest.yaml
test_matrix.csv
```

## v2.1 hardening

```text
cross-agent entrypoints
closed template coverage for declared artifacts
artifact_contracts.json
scripts/validate_artifacts.py
pytest-ready project_template
separated evidence gate and coding gate semantics
```

## v2.1.1 acquisition rule

```text
reference discovery must actively use available internet search/browser/retrieval tools
every meaningful search must be logged
accepted and rejected candidates must be recorded
tool unavailability must be stated explicitly
```

## v2.1.1 report production rule

```text
report production decisions must be recorded without hard-coding one domain or report structure
report status must match evidence, coding gate, and verification state
final reports must come from saved final input or trusted BookResult
ReportContext must preserve warnings, errors, limitations, source basis, and traceability
templates, UI, and batch flows must not calculate or override engineering status
```

## v2.1.1 interface rule

```text
production frontends should use the unified top-bar / left-input / right-review layout
Marimo review apps should support module-level inspection, editable draft inputs, traces, and review logs
data/report imports should be staged, classified, hashed, and normalized before official calculation
upload/export packages should include manifest, inputs, trusted results, reports, hashes, and versions
```

## Best use

1. Start with the router.
2. Let the evidence gate decide whether new references must be gathered.
3. Persist gathered references locally before analysis.
4. Analyze persisted references into a Calculation Logic Blueprint.
5. Freeze the implementation handoff before coding.
6. Implement formulas only inside reusable calculation modules and book runners.
7. Build interfaces using the unified UI, Marimo review, and data package contracts when needed.
8. Verify with unit, branch, lookup, regression, integration, interface, package, and smoke tests.
