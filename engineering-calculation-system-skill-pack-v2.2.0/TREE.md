# Package Tree

```text
engineering-calculation-system-skill-pack-v2.2.0/
├── .qoder
│   ├── agents
│   │   ├── engineering-calc-system.md
│   │   └── reference.md
│   └── skills
│       └── engineering-calc-system
│           ├── SKILL.md
│           ├── assets
│           │   └── lifecycle-console.html
│           └── reference.md
├── .trae
│   └── rules
│       └── engineering-calc-system.md
├── CHANGELOG.md
├── INSTALL.md
├── MIGRATION_NOTES.md
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── SKILL_PACKAGE_SUMMARY.md
├── adapters
│   └── agent-entrypoints.md
├── agents
│   └── openai.yaml
├── examples
│   ├── example_acquisition_handoff.yaml
│   ├── example_artifact_index.yaml
│   └── example_source_card.md
├── original_sources
│   ├── engineering-calculation-book.original.skill.md
│   └── engineering-calculation-logic-architecture.original.skill.md
├── parent
│   ├── engineering-calculation-book.skill.md
│   ├── engineering-calculation-logic-architecture.skill.md
│   └── engineering-calculation-reference-acquisition.skill.md
├── project_template
│   └── engineering_calc_project
│       ├── README.md
│       ├── analysis
│       │   ├── 01_source_inventory
│       │   │   └── .gitkeep
│       │   ├── 02_logic_blueprint
│       │   │   └── .gitkeep
│       │   ├── 03_logic_details
│       │   │   └── .gitkeep
│       │   ├── 04_diagrams
│       │   │   └── .gitkeep
│       │   └── 05_risks_and_questions
│       │       └── .gitkeep
│       ├── apps
│       │   └── review
│       │       └── .gitkeep
│       ├── data
│       │   ├── imported
│       │   │   ├── references
│       │   │   │   └── .gitkeep
│       │   │   └── reports
│       │   │       └── .gitkeep
│       │   ├── input
│       │   │   └── .gitkeep
│       │   ├── normalized
│       │   │   └── cases
│       │   │       └── .gitkeep
│       │   ├── packages
│       │   │   └── .gitkeep
│       │   └── staging
│       │       └── .gitkeep
│       ├── deploy
│       │   ├── Dockerfile
│       │   ├── docker-compose.yml
│       │   ├── env.example
│       │   ├── nginx
│       │   │   └── engineering-calc.conf
│       │   └── systemd
│       │       └── engineering-calc.service
│       ├── handoff
│       │   ├── .gitkeep
│       │   ├── artifact_index.yaml
│       │   └── implementation_handoff.yaml
│       ├── implementation
│       │   ├── 00_architecture
│       │   │   └── .gitkeep
│       │   ├── 01_core_models
│       │   │   └── .gitkeep
│       │   ├── 02_modules
│       │   │   ├── .gitkeep
│       │   │   └── module_asset_registry.csv
│       │   ├── 03_book_runner
│       │   │   └── .gitkeep
│       │   ├── 04_interfaces
│       │   │   └── .gitkeep
│       │   └── 05_acceptance
│       │       └── .gitkeep
│       ├── logs
│       │   └── .gitkeep
│       ├── outputs
│       │   ├── batch_summaries
│       │   │   └── .gitkeep
│       │   ├── logs
│       │   │   └── .gitkeep
│       │   ├── normalized_inputs_json
│       │   │   └── .gitkeep
│       │   ├── reports_docx
│       │   │   └── .gitkeep
│       │   ├── reports_html
│       │   │   └── .gitkeep
│       │   ├── reports_pdf
│       │   │   └── .gitkeep
│       │   ├── results_json
│       │   │   └── .gitkeep
│       │   └── upload_packages
│       │       └── .gitkeep
│       ├── pyproject.toml
│       ├── references
│       │   ├── acquisition
│       │   │   ├── .gitkeep
│       │   │   ├── acquisition_handoff.yaml
│       │   │   ├── acquisition_plan.yaml
│       │   │   ├── candidate_sources.csv
│       │   │   ├── search_log.csv
│       │   │   └── source_coverage_matrix.csv
│       │   ├── evidence_library_manifest.yaml
│       │   ├── extracted
│       │   │   └── notes
│       │   │       └── .gitkeep
│       │   ├── raw
│       │   │   └── .gitkeep
│       │   ├── snapshots
│       │   │   └── .gitkeep
│       │   ├── source_cards
│       │   │   └── .gitkeep
│       │   └── source_registry.yaml
│       ├── release
│       │   └── release_checklist.md
│       ├── src
│       │   └── pkg
│       │       ├── __init__.py
│       │       ├── books
│       │       │   ├── __init__.py
│       │       │   └── book_name
│       │       │       ├── __init__.py
│       │       │       ├── book_models.py
│       │       │       ├── book_runner.py
│       │       │       ├── report_context.py
│       │       │       └── templates
│       │       │           └── .gitkeep
│       │       ├── core
│       │       │   ├── .gitkeep
│       │       │   ├── __init__.py
│       │       │   ├── checks.py
│       │       │   ├── enums.py
│       │       │   └── sanitize.py
│       │       ├── interfaces
│       │       │   ├── .gitkeep
│       │       │   └── __init__.py
│       │       ├── libraries
│       │       │   ├── __init__.py
│       │       │   └── geotech
│       │       │       ├── __init__.py
│       │       │       └── shallow_foundation
│       │       │           ├── .gitkeep
│       │       │           └── __init__.py
│       │       └── report
│       │           ├── .gitkeep
│       │           └── __init__.py
│       ├── tests
│       │   ├── conftest.py
│       │   ├── integration
│       │   │   ├── .gitkeep
│       │   │   └── test_book_runner.py
│       │   ├── regression
│       │   │   └── .gitkeep
│       │   ├── smoke
│       │   │   ├── .gitkeep
│       │   │   └── example_input.json
│       │   └── unit
│       │       └── .gitkeep
│       ├── verification
│       │   └── .gitkeep
│       └── webapp
│           ├── .gitkeep
│           ├── __init__.py
│           ├── app.py
│           ├── config.py
│           ├── form_utils.py
│           ├── i18n.py
│           ├── routes.py
│           ├── static
│           │   ├── css
│           │   │   └── style.css
│           │   └── js
│           │       ├── forms.js
│           │       ├── i18n.js
│           │       ├── main.js
│           │       └── results.js
│           └── templates
│               ├── base.html
│               └── index.html
├── schemas
│   └── artifact_contracts.json
├── scripts
│   ├── build_package_index.py
│   └── validate_artifacts.py
├── shared
│   ├── artifact-index-template.yaml
│   ├── contracts.md
│   ├── copyright-and-access-policy.md
│   ├── file-naming-convention.md
│   ├── handoff-contract-template.yaml
│   ├── id-convention.md
│   ├── local-persistence-contract.md
│   ├── quality-gates.md
│   ├── result-path-convention.md
│   ├── source-acquisition-contract.md
│   ├── status-semantics.md
│   └── unit-convention.md
├── skills
│   ├── 00-engineering-calculation-router.skill.md
│   ├── 01-reference-adequacy-and-gap-assessment.skill.md
│   ├── 02-reference-discovery-and-acquisition.skill.md
│   ├── 03-reference-persistence-and-local-library.skill.md
│   ├── 04-source-intake-and-authority.skill.md
│   ├── 05-engineering-logic-blueprint.skill.md
│   ├── 06-formula-lookup-branch-extraction.skill.md
│   ├── 07-implementation-handoff-contract.skill.md
│   ├── 08-calculation-book-architecture.skill.md
│   ├── 09-core-and-data-models.skill.md
│   ├── 10-reusable-calculation-modules.skill.md
│   ├── 11-book-runner-and-governing-summary.skill.md
│   ├── 12-report-review-batch-interfaces.skill.md
│   ├── 12a-report-context-and-rendering.skill.md
│   ├── 12b-frontend-and-review-interfaces.skill.md
│   ├── 12c-batch-import-export-packages.skill.md
│   ├── 13-verification-regression-traceability.skill.md
│   └── 14-cloud-web-release-deployment.skill.md
├── templates
│   ├── acquisition
│   │   ├── acquisition_handoff.yaml
│   │   ├── acquisition_notes.md
│   │   ├── acquisition_plan.yaml
│   │   ├── candidate_sources.csv
│   │   ├── evidence_library_manifest.yaml
│   │   ├── local_persistence_log.csv
│   │   ├── open_reference_questions.md
│   │   ├── reference_gap_assessment.md
│   │   ├── retrieval_decisions.csv
│   │   ├── search_log.csv
│   │   ├── source_card_template.md
│   │   ├── source_coverage_matrix.csv
│   │   └── source_registry.yaml
│   ├── analysis
│   │   ├── applicability_limits.csv
│   │   ├── assumption_register.csv
│   │   ├── branch_inventory.csv
│   │   ├── calculation_blueprint.md
│   │   ├── calculation_nodes.csv
│   │   ├── concept_map.csv
│   │   ├── formula_inventory.csv
│   │   ├── global_flowchart.mmd
│   │   ├── input_inventory.csv
│   │   ├── intermediate_inventory.csv
│   │   ├── lookup_inventory.csv
│   │   ├── open_questions.csv
│   │   ├── output_inventory.csv
│   │   ├── risk_register.csv
│   │   ├── source_authority_table.csv
│   │   ├── source_conflicts.csv
│   │   ├── source_intake_notes.md
│   │   ├── source_inventory.yaml
│   │   └── unit_and_sign_conventions.md
│   ├── deployment
│   │   ├── cloud_linux_deployment.md
│   │   ├── release_checklist.md
│   │   └── runtime_env.example
│   ├── handoff
│   │   ├── artifact_index.yaml
│   │   ├── coding_go_no_go.md
│   │   ├── implementation_handoff.md
│   │   ├── implementation_handoff.yaml
│   │   └── unresolved_items_before_coding.md
│   ├── implementation
│   │   ├── api_route_skeleton.md
│   │   ├── batch_flow.md
│   │   ├── chart_integration.md
│   │   ├── core_model_plan.md
│   │   ├── data_model_spec.md
│   │   ├── data_package_manifest.yaml
│   │   ├── dependency_rules.md
│   │   ├── feature_classification.csv
│   │   ├── form_mapping_spec.md
│   │   ├── formula_trace_spec.md
│   │   ├── frontend_fields.csv
│   │   ├── governing_summary_spec.md
│   │   ├── i18n_pattern.md
│   │   ├── import_export_contract.md
│   │   ├── input_mapping_spec.md
│   │   ├── lookup_module_spec.md
│   │   ├── marimo_review_spec.md
│   │   ├── module_asset_registry.csv
│   │   ├── module_interface_spec.md
│   │   ├── module_review_log.csv
│   │   ├── package_layout.md
│   │   ├── project_structure.md
│   │   ├── report_context_spec.md
│   │   ├── result_path_registry.csv
│   │   ├── review_readability_checklist.md
│   │   ├── review_schema.csv
│   │   ├── runner_sequence.md
│   │   ├── status_semantics.md
│   │   ├── ui_layout_spec.md
│   │   └── unit_system.md
│   └── verification
│       ├── acceptance_checklist.md
│       ├── regression_references.md
│       ├── test_matrix.csv
│       └── tolerance_policy.md
└── workflow_diagrams
    └── full_lifecycle.mmd
```
