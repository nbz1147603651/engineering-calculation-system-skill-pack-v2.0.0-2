---
name: core-and-data-models
description: Define core platform utilities and typed data models for engineering calculation books, including statuses, errors, units, validators, metadata, hashing, serialization, BookInput, BookResult, module inputs/results, formula traces, and report context models.
---

# Core and Data Models

Use this skill after the calculation book architecture is defined.

## Goal

Create stable typed contracts before implementing calculation modules.

## Core Platform Responsibilities

```text
status enums
CheckResult
FormulaTrace
RunMetadata
errors and warnings
validators
unit helpers
hashing
serialization
result path utilities
```

Core must not contain:

```text
domain formulas
book-specific runner logic
UI code
report rendering
batch workflow
```

## Data Models

Recommended public models:

```text
ProjectInfo
DesignBasis
DesignOptions
Assumption
BookInput
BookResult
ModuleInput
ModuleResult
CheckResult
GoverningSummary
ChartSpec / ChartSeries / ChartAxis / ChartThreshold when charts improve review
ReportContext
```

Every public result should expose where applicable:

```text
status
demand
capacity
utilization
limit
unit
warnings
errors
intermediate_values
formula_traces
chart specifications derived from already-computed result values
code_references
governing_reason
```

## Unit Contract

Define one internal unit system:

```text
length: m
force: kN
stress/pressure: kPa
unit_weight: kN/m3
moment: kNm
settlement/displacement: mm
angle_input: degree
angle_internal: radian
```

Convert units only at input/output boundaries.

## Required Output Artifacts

```text
implementation/01_core_models/core_model_plan.md
implementation/01_core_models/data_model_spec.md
implementation/01_core_models/status_semantics.md
implementation/01_core_models/unit_system.md
src/<pkg>/core/
src/<pkg>/books/<book_name>/book_models.py
```

## Required Final Response

Provide:

```text
core model plan
data model specification
status semantics
unit policy
result path plan
serialization and hash plan
```
