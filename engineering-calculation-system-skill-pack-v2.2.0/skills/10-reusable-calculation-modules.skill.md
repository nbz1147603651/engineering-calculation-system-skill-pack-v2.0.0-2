---
name: reusable-calculation-modules
description: Implement or design decoupled reusable engineering calculation modules from the implementation handoff, with typed inputs/outputs, stable public functions, module asset registration, formula traces, lookup behavior, warnings/errors, no file I/O, no UI/report/deployment dependency, and unit/regression tests.
---

# Reusable Calculation Modules

Use this skill to implement domain formulas and lookup logic.

## Goal

Build reusable, independently testable engineering modules.

Treat each module as an accumulating engineering asset that can be reused by later books, web apps, batch jobs, and reports through the same public interface.

## Primary Runtime

Reusable calculation modules are Python modules by default.

```text
language: Python 3.9+
location: src/<pkg>/libraries/<domain>/<category>/
public API: typed Python input/options/result models plus one stable public function
tests: pytest unit/regression tests
review: Marimo can inspect Python modules directly when review apps are enabled
```

Use a non-Python calculation module only when explicitly requested and when the handoff defines a Python wrapper, CLI adapter, or API adapter for `run_book()` and review workflows.

## Module Rules

Every reusable module must:

```text
have typed input
have typed output
expose one stable public function
avoid hidden global state
avoid file I/O
avoid UI dependencies
avoid report dependencies
avoid batch-specific behavior
validate module-specific assumptions
return intermediate values needed for audit
return warnings instead of silently clipping values
be independently testable
be recorded in module_asset_registry.csv
```

When administrator-editable formulas are required, expose formulas through a declaration-based formula registry instead of editable Python code. The reusable module should load only the active, validated registry version and preserve registry version/hash metadata in results.

## Forbidden

Do not read CSV, render reports, access UI state, write batch summaries, call a book runner, open deployment files, read environment variables, or depend on a web framework from a reusable formula module.

## Asset Registry

Record every reusable module with:

```text
module_id
domain and category
module name
stable public function
input/options/result models
source references
formula trace path
unit and regression test paths
reuse status: draft / reviewed / stable / deprecated
asset owner or maintainer
```

## Example Interface

```python
def check_bearing_capacity(
    input_data: BearingInput,
    options: BearingOptions,
) -> BearingResult:
    ...
```

## Required Output Artifacts

```text
implementation/02_modules/module_interface_spec.md
implementation/02_modules/module_asset_registry.csv
implementation/02_modules/formula_trace_spec.md
implementation/02_modules/lookup_module_spec.md
implementation/02_modules/formula_registry_spec.md
data/formula_registry/active_versions.yaml
data/formula_registry/modules/<module_id>/versions/<version_id>.yaml
src/<pkg>/libraries/<domain>/<category>/
tests/unit/test_<module>.py
tests/regression/test_<module>_<reference>.py
```

## Required Final Response

Provide:

```text
module location
input/options/result models
public function signatures
formula and source references
active formula registry version and hash when used
intermediate values returned
warning/error behavior
unit tests
regression tests if references exist
example usage
asset registry row
```
