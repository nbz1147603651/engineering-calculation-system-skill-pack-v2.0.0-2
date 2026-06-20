---
name: reusable-calculation-modules
description: Implement or design decoupled reusable engineering calculation modules from the implementation handoff, with typed inputs/outputs, stable public functions, module asset registration, formula traces, lookup behavior, warnings/errors, no file I/O, no UI/report/deployment dependency, and unit/regression tests.
---

# Reusable Calculation Modules

## When to use

To implement domain formulas and lookup logic. Each module is an accumulating engineering asset
reused by later books, web apps, batch jobs, and reports through the same public interface.

## Steps

1. Implement each module as a Python package (default: language Python 3.9+, location
   `src/<pkg>/libraries/<domain>/<category>/`, public API = typed input/options/result models +
   one stable public function, tests = pytest unit/regression). Use a non-Python module only when
   explicitly requested and the handoff defines a Python wrapper / CLI adapter / API adapter for
   `run_book()` and review.
2. Enforce module rules: typed input + typed output; one stable public function; no hidden global
   state; no file I/O; no UI/report/batch/web-framework/env-var dependencies; validate
   module-specific assumptions; return intermediate values needed for audit; return warnings
   instead of silently clipping values; independently testable; recorded in
   `module_asset_registry.csv`. Example: `def check_bearing_capacity(input_data: BearingInput,
   options: BearingOptions) -> BearingResult: ...`.
3. When admin-editable formulas are required, expose them through a declaration-based formula
   registry (not editable Python code); the module loads only the active validated registry
   version and preserves registry version/hash in results.
4. Write the module interface spec, formula-trace spec, lookup-module spec, and formula-registry
   spec from `templates/implementation/`.
5. Add unit tests `tests/unit/test_<module>.py` and regression tests
   `tests/regression/test_<module>_<reference>.py` where references exist.
6. Record each module in `module_asset_registry.csv`: module_id, domain & category, module name,
   stable public function, input/options/result models, source references, formula-trace path,
   unit/regression test paths, reuse status (draft/reviewed/stable/deprecated), asset owner.

## Forbidden

Reading CSV, rendering reports, accessing UI state, writing batch summaries, calling a book
runner, opening deployment files, reading env vars, or depending on a web framework from a
reusable formula module.

## Artifacts

```text
implementation/02_modules/module_interface_spec.md   (templates/implementation/module_interface_spec.md)
implementation/02_modules/module_asset_registry.csv  (templates/implementation/module_asset_registry.csv)
implementation/02_modules/formula_trace_spec.md      (templates/implementation/formula_trace_spec.md)
implementation/02_modules/lookup_module_spec.md      (templates/implementation/lookup_module_spec.md)
implementation/02_modules/formula_registry_spec.md   (templates/implementation/formula_registry_spec.md)
data/formula_registry/active_versions.yaml
data/formula_registry/modules/<module_id>/versions/<version_id>.yaml
src/<pkg>/libraries/<domain>/<category>/
tests/unit/test_<module>.py
tests/regression/test_<module>_<reference>.py
```

## Exit gate

Modules are independently testable and traceable; formula traces and module tests exist. See
`shared/lifecycle.md` row 10. Next path: 11 for the book runner.
