---
name: implementation-handoff-contract
description: Convert the source-backed Calculation Logic Blueprint, semantic closure artifacts, formula/lookup/branch inventories, validation rules, risk register, and test requirements into a formal Implementation Handoff Contract for downstream engineering calculation book software.
---

# Implementation Handoff Contract

## When to use

After the analysis artifacts (skills 04-06) are complete enough to guide implementation. Create a
hard interface between reference analysis and coding so the downstream implementation skill does
not need to reinterpret raw references.

## Inputs

```text
references/acquisition/acquisition_handoff.yaml
analysis/01_source_inventory/source_inventory.yaml
analysis/02_logic_blueprint/calculation_blueprint.md, calculation_intent_contract.md,
                      method_selection_matrix.csv, input_semantics_ledger.csv,
                      calculation_nodes.csv
analysis/03_logic_details/formula_inventory.csv, lookup_inventory.csv, branch_inventory.csv,
                      computation_graph_coverage.csv, applicability_limits.csv,
                      unit_and_sign_conventions.md
analysis/05_risks_and_questions/risk_register.csv, open_questions.csv
```

## Steps

1. Author `handoff/implementation_handoff.yaml` (use `shared/handoff-contract-template.yaml`)
   with: handoff_id, book_name, version, status, source_basis, evidence_library_status,
   calculation_scope, runtime_stack (default Python-first: primary_language python, python_version
   ">=3.9", calculation_runtime python_package, backend_runtime flask_or_fastapi,
   frontend_format jinja2_bootstrap5_vanilla_js, review_runtime marimo_optional), input/result
   model_groups, runner_sequence, module_candidates, calculation_module_contract,
   book_runner_contract, backend_api_contract, frontend_contract, operator_workflow_contract,
   release_contract, semantic_closure_contract, formula/lookup/branch_inventory_refs,
   validation_rules, test_requirements, report_sections, traceability_requirements,
   open_questions, coding_gate. Record any deviation from the default runtime stack with a reason
   and an adapter boundary.
2. Write `handoff/implementation_handoff.md` (use `templates/handoff/implementation_handoff.md`)
   as the human-readable summary, and `handoff/coding_go_no_go.md`
   (`templates/handoff/coding_go_no_go.md`) plus `handoff/unresolved_items_before_coding.md`.
3. Build `handoff/artifact_index.yaml` (use `shared/artifact-index-template.yaml`).
4. Set the coding gate: `no_go` (critical formula/lookup/governing-code/unit missing, major
   source conflict unresolved, or semantic closure open) | `prototype_allowed` (formulas clear
   but regression references/closure checks incomplete, or explicit prototype request) |
   `production_allowed` (all critical formulas, units, branches, method selections, input
   semantics, graph coverage, runner targets, and tests defined). For a single static `.html` /
   exported report HTML / mockup request, set the gate to `prototype_allowed` or
   `not_production_ready`; it is never a complete implementation contract.
5. Run the semantic production-gate check before setting `production_allowed`: acquisition status
   is `analysis_allowed`; critical/high coverage rows that block coding are covered with stable
   `current_source_id`; calculation intent is production-ready; method selection rows exist;
   input semantics rows define units/sign/default/validation behavior; formula rows have
   `source_reference` + `test_requirement`; lookup rows define interpolation + out-of-range
   behavior; branch rows define source + true/false paths + required tests; computation graph rows
   close formula/lookup/branch/input IDs to module, runner, result path, and tests; blocking open
   questions, source conflicts, and production-blocking assumptions are resolved. Downgrade to
   `prototype_allowed` or `no_go` if any fail.
6. When the validation script is available, run
   `python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --profile core --project <project-root>`
   and treat failures as blockers (unless the user asks for a draft/prototype).

## Artifacts

```text
handoff/implementation_handoff.yaml   (shared/handoff-contract-template.yaml)
handoff/implementation_handoff.md     (templates/handoff/implementation_handoff.md)
handoff/artifact_index.yaml           (shared/artifact-index-template.yaml)
handoff/coding_go_no_go.md            (templates/handoff/coding_go_no_go.md)
handoff/unresolved_items_before_coding.md
```

## Exit gate

`production_allowed` for production completion; otherwise `prototype_allowed` or `no_go`. See
`shared/lifecycle.md` row 07. Next path: 08 for architecture (if gate allows). Production is not
allowed unless semantic closure artifacts agree with the implementation handoff.
