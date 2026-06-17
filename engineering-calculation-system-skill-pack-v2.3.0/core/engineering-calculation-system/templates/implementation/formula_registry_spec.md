# Formula Registry Specification

Use this template when a calculation book supports admin-reviewed declaration-based formula rules.

## Registry Layout

```text
data/formula_registry/
  active_versions.yaml
  modules/<module_id>/versions/<version_id>.yaml
outputs/logs/formula_publish_log.csv
```

`active_versions.yaml` is the only production switch. Update it atomically only after validation passes.

## Rule Requirements

Each version file must record:

```text
schema_version
module_id
version_id
status
published_at
published_by
formulas
```

Each formula must record:

```text
formula_id
name
expression
variables
output
source_refs
limits
test_cases
```

## Safety Rules

Use declaration-based expressions only. Do not allow arbitrary Python execution from the admin UI.

Validate before publishing:

```text
required fields
safe expression AST
allowed math functions only
unit fields present
declared test cases pass
run_book smoke test passes
```

## Production Metadata

Every `BookResult` should expose:

```text
formula_registry_version
formula_hash
formula_published_at
```

Reports and frontends may display this metadata, but must not calculate formulas.
