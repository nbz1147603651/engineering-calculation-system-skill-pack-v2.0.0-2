---
name: engineering-logic-blueprint
description: Transform source-inventoried engineering references into a normalized Calculation Logic Blueprint with concept map, calculation nodes, input/intermediate/output inventories, diagrams, module candidates, validation needs, and traceability anchors.
---

# Engineering Logic Blueprint

Use this skill after source intake and authority classification.

## Core Principle

Do not treat Mermaid as the final product. Mermaid diagrams are views of the deeper calculation logic model.

The core deliverable is:

```text
analysis/02_logic_blueprint/calculation_blueprint.md
```

## Required Transformation

```text
source inventory
-> engineering concept map
-> calculation stages
-> normalized calculation node model
-> input / intermediate / output inventories
-> Mermaid views
-> software module candidates
```

## Engineering Concept Layer

Extract concepts such as:

```text
calculation object
design situation
limit state
load case
load combination
material model
soil model
water or environmental condition
geometry model
boundary condition
design method
checking method
safety format
failure mode
serviceability criterion
ultimate criterion
special condition
governing result
report output
```

## Normalized Node Model

Each node should include:

```text
node_id
node_type
node_name
engineering_meaning
inputs
outputs
units
formula_or_method
source_reference
branch_condition
applicability
assumptions
module_candidate
result_visibility
report_visibility
test_requirement
risk_level
```

Allowed node types:

```text
Input
Validate
Normalize
SelectMethod
Lookup
Compute
Branch
Check
Aggregate
Output
Report
Warning
Error
Redesign
```

## Required Output Artifacts

```text
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/02_logic_blueprint/concept_map.csv
analysis/02_logic_blueprint/calculation_nodes.csv
analysis/02_logic_blueprint/input_inventory.csv
analysis/02_logic_blueprint/intermediate_inventory.csv
analysis/02_logic_blueprint/output_inventory.csv
analysis/04_diagrams/global_flowchart.mmd
analysis/04_diagrams/data_flow.mmd
analysis/04_diagrams/branch_logic.mmd
analysis/04_diagrams/module_dependency.mmd
```

## Software Mapping Orientation

Every important node should map to at least one future artifact:

```text
input model field
validator
normalizer
lookup library
calculation module function
book runner step
CheckResult
GoverningSummary
BookResult field
ReportContext field
test target
```

## Required Final Response

Provide:

```text
scope and purpose
concept map summary
calculation logic summary
node inventory summary
input/intermediate/output inventory summary
Mermaid diagrams
module candidates
open issues for detailed formula extraction
```
