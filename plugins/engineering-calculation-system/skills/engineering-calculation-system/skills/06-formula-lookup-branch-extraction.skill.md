---
name: formula-lookup-branch-extraction
description: Extract and normalize engineering formulas, design methods, lookup tables, charts, interpolation rules, branch conditions, unit/sign conventions, assumptions, applicability limits, warnings, errors, computation graph closure, and test requirements from inventoried sources and the Calculation Logic Blueprint.
---

# Formula, Lookup, and Branch Extraction

## When to use

After the high-level Calculation Logic Blueprint exists (skill 05). Freeze the high-risk
calculation details that software implementation must not reinterpret later.

## Steps

For each formula, lookup, branch, and high-risk node, record the fields below in the matching
template CSV, then record units/signs, applicability limits, assumptions, risks, open questions,
and computation graph coverage.

1. **Formulas / named methods** -> `templates/analysis/formula_inventory.csv`: formula_id, name,
   purpose, inputs, outputs, units, source_reference, applicability, branch_dependencies,
   lookup_dependencies, implementation_note, test_requirement, risk_level. Classify source type:
   code-defined | manual-defined | spreadsheet-derived | empirical | project-specific |
   engineering assumption | needs confirmation.
2. **Lookup tables / charts / nomograms** -> `templates/analysis/lookup_inventory.csv`: lookup_id,
   name, inputs, outputs, source_reference, interpolation_rule, out_of_range_behavior,
   implementation_note, test_requirement, risk_level. Behaviors: exact lookup | range lookup |
   linear/bilinear/log interpolation | nearest conservative value | chart digitization |
   manual selection | not specified.
3. **Branch / decision rules** -> `templates/analysis/branch_inventory.csv`: branch_id, condition,
   engineering_meaning, source_reference, path_if_true, path_if_false, not_applicable_behavior,
   program_representation, required_tests, risk_level.
4. **Computation graph closure** -> `templates/analysis/computation_graph_coverage.csv`:
   coverage_id, node_id, node_type, check_id, formula_ids, lookup_ids, branch_ids, input_ids,
   source_reference, module_id, public_function, runner_step, result_path, test_ids,
   report_visibility, closure_status. Every production formula, lookup, branch, and high-risk
   node must have a future module target, runner step, result path, and test target before coding
   is allowed.
5. **Unit & sign rules** -> `templates/analysis/unit_and_sign_conventions.md`: input/internal/
   output units, angle units, force/moment sign conventions, coordinate directions, pressure/stress
   conventions, settlement/displacement sign conventions. Mark unclear items `needs confirmation`.
   Use `shared/unit-convention.md` as the default internal system.
6. **Applicability limits** -> `templates/analysis/applicability_limits.csv`; **assumptions** ->
   `templates/analysis/assumption_register.csv`; **risks** ->
   `templates/analysis/risk_register.csv`; **open questions** ->
   `templates/analysis/open_questions.csv` (classify by coding impact).

## Artifacts

```text
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
analysis/03_logic_details/computation_graph_coverage.csv
analysis/03_logic_details/applicability_limits.csv
analysis/03_logic_details/unit_and_sign_conventions.md   (templates/analysis/unit_and_sign_conventions.md)
analysis/03_logic_details/assumption_register.csv
analysis/05_risks_and_questions/risk_register.csv
analysis/05_risks_and_questions/open_questions.csv
```

## Exit gate

Every production rule has a source reference, test requirement, module target, runner target, and
result path. See `shared/lifecycle.md` row 06. Next path: 07 for the implementation handoff.
