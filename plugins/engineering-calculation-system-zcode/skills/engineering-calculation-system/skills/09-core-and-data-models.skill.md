---
name: core-and-data-models
description: Define core platform utilities and typed data models for engineering calculation books, including statuses, errors, units, validators, metadata, hashing, serialization, BookInput, BookResult, module inputs/results, formula traces, and report context models.
---

# Core and Data Models

## When to use

After the calculation-book architecture is fixed (skill 08). Create stable typed contracts before
implementing calculation modules.

## Steps

1. Implement core platform utilities (`src/<pkg>/core/`): status enums, CheckResult, FormulaTrace,
   RunMetadata, errors/warnings, validators, unit helpers, hashing, serialization, result-path
   utilities. Core must NOT contain domain formulas, book-specific runner logic, UI code, report
   rendering, or batch workflow.
2. Define the typed public models (use `templates/implementation/data_model_spec.md`):
   ProjectInfo, DesignBasis, DesignOptions, Assumption, BookInput, BookResult, ModuleInput,
   ModuleResult, CheckResult, GoverningSummary, ChartSpec/ChartSeries/ChartAxis/ChartThreshold
   (when charts improve review), ReportContext. Every public result exposes where applicable:
   status, demand, capacity, utilization, limit, unit, warnings, errors, intermediate_values,
   formula_traces, chart specs (from already-computed values), code_references, governing_reason.
3. Fix the unit contract (`shared/unit-convention.md` is the default internal system): convert
   units only at input/output boundaries. Record the policy in
   `templates/implementation/unit_system.md`.
4. Define status semantics (`shared/status-semantics.md`: PASS/FAIL/WARNING/ERROR/
   NOT_APPLICABLE/NEEDS_CONFIRMATION/NOT_EVALUATED) and result paths
   (`shared/result-path-convention.md`).
5. Write the core-model plan and data-model spec.

## Artifacts

```text
implementation/01_core_models/core_model_plan.md   (templates/implementation/core_model_plan.md)
implementation/01_core_models/data_model_spec.md   (templates/implementation/data_model_spec.md)
implementation/01_core_models/status_semantics.md  (templates/implementation/status_semantics.md)
implementation/01_core_models/unit_system.md       (templates/implementation/unit_system.md)
src/<pkg>/core/
src/<pkg>/books/<book_name>/book_models.py
```

## Exit gate

Models support `BookInput` and `BookResult`; stable public models exist. See
`shared/lifecycle.md` row 09. Next path: 10 for reusable calculation modules.
