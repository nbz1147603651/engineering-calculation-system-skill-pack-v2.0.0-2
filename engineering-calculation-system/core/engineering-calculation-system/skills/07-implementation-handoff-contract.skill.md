---
name: implementation-handoff-contract
description: Convert the source-backed Calculation Logic Blueprint, formula/lookup/branch inventories, validation rules, risk register, and test requirements into a formal Implementation Handoff Contract for downstream engineering calculation book software.
---

# Implementation Handoff Contract

Use this skill after the analysis artifacts are complete enough to guide implementation.

## Goal

Create a hard interface between reference analysis and coding.

The downstream implementation skill should not need to reinterpret raw references to understand the intended software architecture.

## Required Inputs

```text
references/acquisition/acquisition_handoff.yaml
analysis/01_source_inventory/source_inventory.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/02_logic_blueprint/calculation_nodes.csv
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
analysis/03_logic_details/applicability_limits.csv
analysis/03_logic_details/unit_and_sign_conventions.md
analysis/05_risks_and_questions/risk_register.csv
analysis/05_risks_and_questions/open_questions.csv
```

## Required Outputs

```text
handoff/implementation_handoff.yaml
handoff/implementation_handoff.md
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
handoff/unresolved_items_before_coding.md
```

## Contract Sections

The YAML contract should include:

```text
handoff_id
book_name
version
status
source_basis
evidence_library_status
calculation_scope
runtime_stack
input_model_groups
result_model_groups
runner_sequence
module_candidates
calculation_module_contract
book_runner_contract
backend_api_contract
frontend_contract
operator_workflow_contract
release_contract
formula_inventory_refs
lookup_inventory_refs
branch_inventory_refs
validation_rules
test_requirements
report_sections
traceability_requirements
open_questions
coding_gate
```

## Delivery Contract Rule

The handoff must distinguish calculation code, backend/API code, frontend assets, report outputs, and release artifacts.

The handoff must declare the runtime stack. The default is Python-first:

```text
primary_language: python
python_version: ">=3.9"
calculation_runtime: python_package
backend_runtime: flask_or_fastapi
frontend_format: jinja2_bootstrap5_vanilla_js
review_runtime: marimo_optional
```

If any item differs from the default, record why and define the adapter boundary before implementation.

For runnable web calculation systems, a single static `.html` file, exported report HTML, or screenshot-style mockup is never a complete implementation contract. If the user requests only a static prototype, set the coding gate or release status to `prototype_allowed`, `not_production_ready`, or an equivalent non-final status.

The handoff must also record operation-quality decisions: what makes the tool convenient for repeated engineering use, review, report production, batch work, and later formula maintenance.

## Coding Gate

Use one of:

```text
no_go
prototype_allowed
production_allowed
```

Default gate rules:

```text
critical formula missing -> no_go
critical lookup rule missing -> no_go
governing code basis missing -> no_go
unit system unclear -> no_go
major source conflict unresolved -> no_go
missing regression references but formulas are clear -> prototype_allowed
all critical formulas, units, branches, and tests defined -> production_allowed
```

## Semantic Gate Validation

Before setting `production_allowed`, verify the handoff is semantically
consistent:

```text
acquisition status is analysis_allowed
critical/high source coverage rows that block coding are covered
critical/high rows have current_source_id values
formula rows have source_reference and test_requirement values
lookup rows define interpolation and out-of-range behavior
branch rows define source references, paths, and required tests
blocking open questions, source conflicts, and production-blocking assumptions are resolved
```

When the validation script is available, run:

```bash
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --profile core --project <project-root>
```

Treat semantic validation failures as blockers unless the user explicitly asks
for a draft or prototype.

## Required Final Response

Provide:

```text
handoff status
what implementation may start
what implementation must not start
required modules
runner sequence
model groups
runtime stack
calculation module contract
backend API contract
frontend contract
operator workflow contract
release contract
report sections
test requirements
remaining blockers
next skill path
```
