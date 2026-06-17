# Core Model Plan

## Core Responsibilities

Define status enums, check results, formula traces, warnings/errors, metadata, hashing, serialization, and unit boundary helpers.

## Out Of Scope

Core must not contain domain formulas, book-specific orchestration, UI logic, report rendering, or batch workflow behavior.

## Planned Files

| File | Responsibility |
| --- | --- |
| src/<pkg>/core/enums.py | status and severity enums |
| src/<pkg>/core/checks.py | CheckResult and FormulaTrace |
| src/<pkg>/core/units.py | boundary conversions |
| src/<pkg>/core/hashing.py | stable input/result hashes |

