---
name: formula-lookup-branch-extraction
description: Extract and normalize engineering formulas, design methods, lookup tables, charts, interpolation rules, branch conditions, unit/sign conventions, assumptions, applicability limits, warnings, errors, and test requirements from inventoried sources and the Calculation Logic Blueprint.
---

# Formula, Lookup, and Branch Extraction

Use this skill after the high-level Calculation Logic Blueprint exists.

## Goal

Freeze the high-risk calculation details that software implementation must not reinterpret later.

## Required Extraction Targets

```text
formulas and named methods
coefficients and factors
lookup tables and charts
interpolation and out-of-range rules
branch conditions and method selection rules
applicability limits
unit and sign conventions
safety formats
status rules
warnings and errors
assumptions and engineering judgment
```

## Formula Inventory

For each formula/method record:

```text
formula_id
name
purpose
inputs
outputs
units
source_reference
applicability
branch_dependencies
lookup_dependencies
implementation_note
test_requirement
risk_level
```

Classify source type:

```text
code-defined
manual-defined
spreadsheet-derived
empirical
project-specific
engineering assumption
needs confirmation
```

## Lookup Inventory

For each table/chart/nomogram record:

```text
lookup_id
name
inputs
outputs
source_reference
interpolation_rule
out_of_range_behavior
implementation_note
test_requirement
risk_level
```

Lookup behaviors:

```text
exact lookup
range lookup
linear interpolation
bilinear interpolation
log interpolation
nearest conservative value
chart digitization
manual selection
not specified / needs confirmation
```

## Branch Inventory

For each decision record:

```text
branch_id
condition
engineering_meaning
source_reference
path_if_true
path_if_false
not_applicable_behavior
program_representation
required_tests
risk_level
```

## Unit and Sign Rules

Record:

```text
input units
internal units
output units
angle units
force/moment sign conventions
coordinate directions
pressure/stress conventions
settlement/displacement sign conventions
```

Mark unclear items as `needs confirmation`.

## Required Output Artifacts

```text
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
analysis/03_logic_details/applicability_limits.csv
analysis/03_logic_details/unit_and_sign_conventions.md
analysis/03_logic_details/assumption_register.csv
analysis/05_risks_and_questions/risk_register.csv
analysis/05_risks_and_questions/open_questions.csv
```

## Required Final Response

Provide:

```text
formula inventory summary
lookup and interpolation summary
branch logic summary
unit and sign convention summary
applicability limits
high-risk uncertainties
test requirements
whether implementation handoff can proceed
```
