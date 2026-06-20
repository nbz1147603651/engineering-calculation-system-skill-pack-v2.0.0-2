---
name: engineering-logic-blueprint
description: Transform source-inventoried engineering references into a normalized Calculation Logic Blueprint with concept map, calculation nodes, input/intermediate/output inventories, diagrams, module candidates, validation needs, and traceability anchors.
---

# Engineering Logic Blueprint

## When to use

After source intake and authority classification (skill 04). The core deliverable is
`analysis/02_logic_blueprint/calculation_blueprint.md`. Mermaid diagrams are views of the deeper
node model, not the product.

## Steps

1. Extract the engineering concept layer into `templates/analysis/concept_map.csv`: calculation
   object, design situation, limit state, load case, load combination, material/soil/water/
   environmental model, geometry, boundary condition, design method, checking method, safety
   format, failure mode, serviceability/ultimate criterion, special condition, governing result,
   report output.
2. Define calculation stages and the normalized calculation node model. For each node record in
   `templates/analysis/calculation_nodes.csv`: node_id, node_type, node_name,
   engineering_meaning, inputs, outputs, units, formula_or_method, source_reference,
   branch_condition, applicability, assumptions, module_candidate, result_visibility,
   report_visibility, test_requirement, risk_level. Node types: Input, Validate, Normalize,
   SelectMethod, Lookup, Compute, Branch, Check, Aggregate, Output, Report, Warning, Error,
   Redesign.
3. Build the input / intermediate / output inventories
   (`templates/analysis/input_inventory.csv`, `intermediate_inventory.csv`,
   `output_inventory.csv`).
4. Generate Mermaid views from the normalized logic (not from raw prose):
   `analysis/04_diagrams/global_flowchart.mmd`, `data_flow.mmd`, `branch_logic.mmd`,
   `module_dependency.mmd`.
5. Map each important node to at least one future artifact: input model field, validator,
   normalizer, lookup library, calculation-module function, book-runner step, CheckResult,
   GoverningSummary, BookResult field, ReportContext field, test target.

## Artifacts

```text
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/02_logic_blueprint/concept_map.csv            (templates/analysis/concept_map.csv)
analysis/02_logic_blueprint/calculation_nodes.csv      (templates/analysis/calculation_nodes.csv)
analysis/02_logic_blueprint/input_inventory.csv        (templates/analysis/input_inventory.csv)
analysis/02_logic_blueprint/intermediate_inventory.csv (templates/analysis/intermediate_inventory.csv)
analysis/02_logic_blueprint/output_inventory.csv       (templates/analysis/output_inventory.csv)
analysis/04_diagrams/global_flowchart.mmd, data_flow.mmd, branch_logic.mmd, module_dependency.mmd
```

## Exit gate

Logic is traceable enough for extraction (input/output/node traceability present). See
`shared/lifecycle.md` row 05. Next path: 06 for formula/lookup/branch extraction.
