# File Naming Convention

## Source files

```text
S01_<short_source_name>.<ext>
S02_<short_source_name>.<ext>
CODE-01_<code_name>.<ext>
MANUAL-01_<manual_name>.<ext>
EXAMPLE-01_<worked_example>.<ext>
```

Use lowercase snake_case for generated artifacts.

## Analysis files

```text
source_inventory.yaml
calculation_blueprint.md
calculation_nodes.csv
formula_inventory.csv
lookup_inventory.csv
branch_inventory.csv
implementation_handoff.yaml
```

## Implementation files

```text
book_models.py
book_runner.py
governing.py
report_context.py
input_mapping.py
```

## Rule

Once a file path is referenced by `artifact_index.yaml`, do not rename it without updating the index.
