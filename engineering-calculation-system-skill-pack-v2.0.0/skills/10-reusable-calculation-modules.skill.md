---
name: reusable-calculation-modules
description: Implement or design reusable engineering calculation modules from the implementation handoff, with typed inputs/outputs, formula traces, lookup behavior, warnings/errors, no file I/O, no UI/report dependency, and unit/regression tests.
---

# Reusable Calculation Modules

Use this skill to implement domain formulas and lookup logic.

## Goal

Build reusable, independently testable engineering modules.

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
```

## Forbidden

Do not read CSV, render reports, access UI state, write batch summaries, or call a book runner from a reusable formula module.

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
implementation/02_modules/formula_trace_spec.md
implementation/02_modules/lookup_module_spec.md
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
intermediate values returned
warning/error behavior
unit tests
regression tests if references exist
example usage
```
