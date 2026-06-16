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
input_model_groups
result_model_groups
runner_sequence
module_candidates
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

## Required Final Response

Provide:

```text
handoff status
what implementation may start
what implementation must not start
required modules
runner sequence
model groups
report sections
test requirements
remaining blockers
next skill path
```
