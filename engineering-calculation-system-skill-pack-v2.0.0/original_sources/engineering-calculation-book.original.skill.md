---
name: engineering-calculation-book
description: Build, refactor, extend, review, or test reusable engineering calculation book systems with typed inputs/results, separated formula modules, official book runners, review UIs, report generation, traceability, batch execution, and regression tests. Use for geotechnical, foundation, settlement, retaining wall, pile, bridge substructure, structural, hydraulic, pavement, drainage, or similar formal engineering calculation reports; for converting manual or spreadsheet calculations into Python; for creating marimo/web review workflows; for generating batch reports; or for designing a reusable engineering calculation framework.
---

# Engineering Calculation Book

Build engineering calculation books as reusable, auditable software systems, not disposable scripts.

The highest-priority goal is correctness and traceability. The second priority is reuse. The third priority is presentation.

## Scope

Use this skill when the task involves any of the following:

- Designing a new formal engineering calculation book.
- Refactoring an existing script, notebook, spreadsheet, or report workflow into reusable calculation software.
- Building reusable engineering calculation modules.
- Creating a book runner that composes multiple checks into one formal calculation result.
- Creating CSV, JSON, frontend, or review-app input flows.
- Creating HTML, PDF, DOCX, Typst, LaTeX, or other report outputs.
- Creating batch calculation and report-generation workflows.
- Adding tests, regression references, traceability, or review workflows.

Do not use this skill for one-off numerical answers unless the user wants a reusable calculation book or auditable calculation workflow.

## Non-Negotiable Rules

Never put engineering formulas in UI code, frontend code, review apps, report templates, batch scripts, or CSV/Excel inputs.

Never allow different execution paths to implement different calculation logic for the same book.

Never round internal values for calculation convenience. Round only at presentation boundaries unless a design code explicitly requires a rounded value.

Never silently assume missing design-code parameters, units, load cases, material properties, soil parameters, geometry, or safety factors. Either validate, use an explicit default recorded in options, or raise a clear error.

Never treat a generated report as authoritative unless it comes from saved final input or a trusted saved `BookResult`.

## Dependency Direction

Use inward/lower-level dependencies only:

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

Meaning:

```text
presentation imports books
report imports book result or report context
batch imports books
books import libraries and core
libraries import core
core imports only domain-independent utilities
```

Forbidden dependencies:

```text
core imports libraries, books, UI, report, or app code
libraries import books, UI, report, marimo, Flask, FastAPI, Streamlit, Jinja2, Typst, LaTeX, or renderers
books import UI pages or report templates
frontend/review implements engineering formulas
batch runner implements separate engineering formulas
templates recalculate capacities, demands, settlements, reinforcement, or optimization logic
CSV/Excel inputs contain formulas that affect official calculations
```

## Architecture Layers

Classify every non-trivial feature before implementation.

| Layer | Purpose | Typical Location | May Contain | Must Not Contain |
| --- | --- | --- | --- | --- |
| Core platform | Domain-independent types, checks, units, validation, metadata, hashing, serialization | `src/<pkg>/core/` | Base models, status enums, unit helpers, errors | Domain formulas, book-specific orchestration, UI/report code |
| Reusable libraries | Engineering formulas and reusable calculation modules | `src/<pkg>/libraries/<domain>/<category>/` | Bearing, sliding, settlement, reinforcement, hydraulics, load-combination modules | File I/O, UI state, report rendering, batch workflows |
| Calculation books | Compose modules into one formal calculation book | `src/<pkg>/books/<book_name>/` | Book input/result models, runner, governing summary, report context builder | UI widgets, template rendering, duplicated formulas |
| Interfaces and presentation | Review UI, CLI, API, batch, report rendering, templates | `review/`, `webapp/`, `src/<pkg>/interfaces/`, `src/<pkg>/report/` | Field mapping, input editing, runner calls, rendering | Engineering formulas or independent calculation logic |

## Source-of-Truth Hierarchy

For engineering logic, prefer sources in this order:

```text
project-specific design basis and contract documents
applicable design code, national annex, local standard, or client standard
approved historical calculation book or verified legacy spreadsheet
published textbook or code example
independent hand calculation
engineering judgment explicitly recorded as an assumption
```

For every design-code-dependent formula or factor, record at least one of:

```text
code name
code version/year
clause/table/equation identifier
project assumption identifier
internal formula identifier
```

Do not copy long copyrighted code passages into source files or reports. Reference clauses and paraphrase where needed.

## Default Project Structure

Prefer this structure for new systems:

```text
engineering_calc_project/
  pyproject.toml
  README.md
  input/
    projects.csv
    book_cases.csv
    design_options.csv
    batch_control.csv
    domain_specific_files.csv
  src/<pkg>/
    core/
      __init__.py
      checks.py
      enums.py
      errors.py
      units.py
      validators.py
      metadata.py
      hashing.py
      serialization.py
      io_csv.py
      io_json.py
    libraries/
      geotech/
        shallow_foundation/
          __init__.py
          models.py
          bearing_hansen.py
          sliding.py
          uplift.py
          settlement.py
      structural/
      hydraulic/
    books/
      <book_name>/
        __init__.py
        book_models.py
        book_runner.py
        governing.py
        report_context.py
        input_mapping.py
        frontend_fields.csv
        review_schema.csv
        templates/
        tests/
    interfaces/
      cli.py
      batch_runner.py
      review_app.py
      api.py
    report/
      render_html.py
      render_pdf.py
      render_docx.py
      render_typst.py
  outputs/
    inputs_draft/
    inputs_final/
    normalized_inputs_json/
    results_json/
    reports_pdf/
    reports_html/
    reports_docx/
    batch_summaries/
    logs/
  tests/
    unit/
    integration/
    regression/
    smoke/
```

For existing projects, migrate incrementally. Inspect the current tree, imports, tests, and execution flow before proposing restructuring. Do not perform a large restructure unless the user explicitly asks.

## Implementation Protocol

For any non-trivial coding or design task, produce a feature classification table before implementation:

| Feature | Layer | Existing module? | New module needed? | Reusable? | Location | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Then proceed in this order:

1. Identify the calculation book type, report purpose, design code basis, and design stage.
2. Identify required checks, design combinations, and report chapters.
3. Classify features into layers.
4. Reuse existing calculation modules where possible.
5. Define typed input and result models.
6. Define one internal unit system.
7. Define design options, assumptions, and default policy.
8. Define reusable module interfaces.
9. Define the official book runner.
10. Define CSV, JSON, frontend, or API input mapping.
11. Define result serialization.
12. Define report context.
13. Define review or frontend flow when needed.
14. Add focused unit, regression, integration, and smoke tests.
15. Add run commands and an acceptance checklist.

For bug fixes, first identify whether the bug belongs to:

```text
input parsing
validation
unit conversion
formula module
book orchestration
governing summary
report context
template rendering
review/frontend state
batch workflow
```

Fix the lowest correct layer. Do not patch symptoms in report templates or UI code.

## Minimum Viable System

For small or first-version books, require only:

```text
typed BookInput
typed BookResult
independent calculation modules
one official run_book() entry point
explicit units
validated design options and assumptions
report context builder
one report renderer if reporting is required
unit or regression tests for formulas
integration test for run_book()
```

Avoid adding registries, approval workflows, multi-format reports, databases, or complex frontend state unless they provide immediate value.

## Extended Platform Features

Add these only when the system becomes reusable across multiple books or projects:

```text
module registry
formula registry
design-code registry
input hashing
result hashing
run metadata
frontend override audit trail
batch summary CSV
marimo or web review app
multi-format report rendering
approved/final input workflow
role-based review status
golden report regression tests
```

## Input Contract

CSV, JSON, frontend, API, or spreadsheet-derived input must all produce the same typed `BookInput`.

Default flow:

```text
raw input source
-> parsing
-> validation
-> unit normalization
-> BookInput
-> normalized input JSON
-> run_book()
-> BookResult
-> BookResult JSON
-> report context
-> formal report
```

Validation must stop execution before calculation when required files, required columns, required values, units, numeric values, booleans, IDs, relationships, design options, or load combinations are invalid.

Input validation should distinguish:

```text
missing required value
invalid type
invalid unit
out-of-range value
inconsistent relationship
unsupported design option
unsupported code version
warning-level unusual value
```

### CSV Rules

```text
UTF-8 encoding
header row required
snake_case columns
unit suffixes for dimensional quantities
stable ID columns
explicit cross-table IDs
one logical table per CSV
decimal separator "."
booleans as true/false
dates as YYYY-MM-DD
no merged cells
no hidden rows
no formulas that affect official calculations
no implicit row-order relationships unless documented
```

Common CSV files:

```text
projects.csv
book_cases.csv
design_options.csv
batch_control.csv
```

Typical domain CSV files:

```text
load_cases.csv
load_combinations.csv
foundations.csv
soil_profiles.csv
soil_layers.csv
materials.csv
geometry.csv
reinforcement.csv
hydraulic_parameters.csv
pavement_layers.csv
retaining_wall_geometry.csv
pile_groups.csv
```

## Unit Contract

Define one internal unit system per project or package.

Default internal units:

```text
length: m
area: m2
volume: m3
force: kN
stress/pressure: kPa
unit_weight: kN/m3
moment: kNm
settlement/displacement: mm
angle_input: degree
angle_internal: radian
time: s or day, explicitly defined per domain
```

Use explicit field names:

```text
width_m
area_m2
vertical_load_kN
moment_kNm
pressure_kPa
unit_weight_kN_m3
settlement_mm
phi_deg
phi_rad
```

Rules:

```text
convert units at input boundaries
use internal units inside calculation modules
format units only at presentation boundaries
store unit metadata in public input/result models
reject ambiguous unitless engineering quantities unless clearly dimensionless
avoid mixing degree and radian fields
```

## Numerical Contract

Calculation modules must define numerical behavior explicitly:

```text
internal precision policy
tolerance for comparisons
tolerance for regression tests
handling of zero, near-zero, negative, infinite, or NaN values
status behavior at exact boundary conditions
rounding policy for reports
```

Recommended status comparison:

```text
PASS: utilization <= limit + tolerance
FAIL: utilization > limit + tolerance
NOT_APPLICABLE: check does not apply to this case
ERROR: required calculation could not be completed
WARNING: result exists but input or assumptions require attention
```

## Data Model Contract

Use Pydantic models for public input/output when practical. Dataclasses are acceptable for small internal immutable helpers.

Recommended base concepts:

```text
ProjectInfo
DesignBasis
DesignOptions
Assumption
RunMetadata
FormulaTrace
CheckResult
ModuleResultBase
BookInputBase
BookResultBase
ReviewMetadata
ReportMetadata
```

Every public result should expose, where applicable:

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
code_references
governing_reason
```

Use stable result paths for report templates and regression tests, for example:

```text
bearing.status
bearing.utilization
settlement.maximum_settlement_mm
governing.overall_status
```

## Formula Trace Contract

Use formula traces when the calculation is intended for audit, review, or formal reporting.

A formula trace should contain:

```text
formula_id
formula_name
code_reference or internal_reference
input_symbols and values
intermediate_symbols and values
result_symbol and value
unit
notes or assumptions
```

Formula traces should be machine-readable. The report layer may decide how much trace detail to display.

## Calculation Module Contract

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

Example interface:

```python
def check_bearing_hansen(
    input_data: BearingInput,
    options: BearingOptions,
) -> BearingResult:
    ...
```

Keep helper functions private unless they are intentionally reusable and tested.

Calculation modules may call lower-level helper modules, but they must not import a calculation book.

## Book Runner Contract

Each calculation book must define one official runner:

```python
def run_book(book_input: BookInput) -> BookResult:
    ...
```

The runner must:

```text
validate book-level input
prepare shared state
apply design options and assumptions
call reusable calculation modules
collect module results
preserve warnings and errors
summarize governing checks
create run metadata
return structured BookResult
```

Batch processing, review pages, frontend APIs, notebooks, and report generation must all call the same runner or consume its saved result.

The runner should not render reports, read raw CSV files, manage UI state, or write batch summaries. Put those responsibilities in interface or report layers.

## Governing Summary Contract

Every formal calculation book should expose a governing summary containing:

```text
overall_status
governing_check_id
governing_check_name
governing_utilization or margin
governing_limit
critical_load_case or combination
controlling_location/member/foundation if applicable
warnings_count
errors_count
```

If multiple checks govern different design aspects, expose a list rather than hiding secondary failures.

## Report Contract

Formal reports must be generated from saved final input or a trusted `BookResult`.

Preferred flow:

```text
final_input.json
-> run_book()
-> BookResult
-> save BookResult JSON
-> build_report_context()
-> template/render function
-> HTML/PDF/DOCX/Typst/LaTeX report
```

Report templates may contain:

```text
value references
loops
conditionals
section visibility logic
formatting filters
unit formatting
cross-references
```

Report templates must not contain:

```text
engineering formulas
unit conversion for calculation
capacity calculation
settlement calculation
reinforcement calculation
hydraulic calculation
load-combination generation
optimization logic
independent pass/fail logic
```

Build a `ReportContext` containing:

```text
project information
design basis
assumptions
input summary
module summaries
governing summary
intermediate calculation tables
warnings and errors
formula references or traces
report metadata
appendix data when needed
```

Reports should clearly distinguish:

```text
draft report
review report
final report
superseded report
```

## Review UI Contract

A review UI may be marimo, Flask, Streamlit, Panel, FastAPI with a frontend, or a custom frontend.

The review UI may:

```text
display input fields
edit parameters
validate input
call run_book()
show intermediate values
show OK/NG results
show warnings and errors
save draft input
save final input
generate report
export result JSON
```

The review UI must not contain formulas.

Clearly distinguish:

```text
imported input
draft input
current UI state
calculated result
saved final input
approved result
formal report
```

When frontend edits override imported values, record:

```text
field_path
original_value
new_value
unit
edited_by
edited_at
reason
source
```

## Batch Contract

Batch processing must call the same `run_book()`.

Recommended flow:

```text
read batch_control.csv
-> load each case input
-> validate each case
-> run_book()
-> save normalized input JSON
-> save BookResult JSON
-> render report if requested
-> write batch summary CSV
-> write logs
```

Batch summary should include:

```text
case_id
project_id
input_hash
result_hash
overall_status
governing_check
governing_utilization
warnings_count
errors_count
report_path
result_json_path
run_timestamp
```

Batch behavior for failed cases must be explicit:

```text
fail fast
continue and record error
skip dependent cases
```

## Traceability Contract

For production reports and saved results, include metadata when feasible:

```text
book_type
book_name
case_id
project_id
design_code and version
run_timestamp
package version
input_hash
result_hash
python_version
git_commit if available
formula registry version if used
runner name/version
report template version
```

Use deterministic serialization for hashes:

```text
stable key order
normalized units
stable numeric formatting policy
exclude volatile metadata from input hash
```

## Testing Contract

Every reusable calculation module should have:

```text
unit tests
regression tests
edge case tests
status tests
invalid input tests
```

Every calculation book should have an integration test:

```text
sample input
-> run_book()
-> BookResult exists
-> governing summary exists
-> result serializes
-> report context builds
```

Every report renderer should have a smoke test:

```text
sample input/result
-> render report
-> output exists
-> key project/case identifiers appear
```

Regression references should be prioritized:

```text
design code examples
published textbook examples
verified historical reports
independent hand calculations
legacy spreadsheet outputs
```

Use explicit tolerances and explain tolerance choice for sensitive formulas.

Recommended test organization:

```text
tests/unit/test_<module>.py
tests/regression/test_<domain>_<reference>.py
tests/integration/test_<book_name>_runner.py
tests/smoke/test_<report_renderer>.py
```

## Refactoring Existing Calculations

When converting manual calculations, spreadsheets, notebooks, or legacy scripts:

1. Preserve a reference copy of the original calculation.
2. Identify inputs, formulas, intermediate values, outputs, and statuses.
3. Separate formulas from presentation.
4. Define typed models and internal units.
5. Reproduce one reference case before generalizing.
6. Add regression tests against the reference case.
7. Replace duplicated formulas with reusable modules.
8. Build the official `run_book()` path.
9. Migrate reporting and UI last.

Do not optimize or reorganize heavily until a reference case passes.

## Recommended Stack

Default stack:

```text
Python
Pydantic or dataclasses
numpy
pandas
pytest
CSV for structured input
JSON for normalized input/results
marimo, Streamlit, Flask, or FastAPI for review/frontends
Jinja2/HTML, Typst, LaTeX, DOCX, or PDF tools for reports
```

Technology may change, but these rules must remain:

```text
calculation core stays independent
typed input/output exists
units are explicit
frontend and review call book runner
reports do not calculate
batch uses book runner
tests exist
traceability exists for production outputs
```

## Required Output for New Calculation Book Requests

When creating a new calculation book system, provide:

```text
feature classification table
project structure
input files and schemas
typed data models
design basis and assumptions model
unit system
calculation module interfaces
book runner design
governing summary design
example normalized input JSON
example BookResult JSON
review/frontend flow if needed
report context design
report template skeleton
batch flow if needed
test plan and skeleton
run commands
acceptance checklist
```

## Required Output for Module-Only Requests

When creating or refactoring a reusable calculation module, provide:

```text
module location
input model
options model if needed
result model
public function signature
formula/source references
intermediate values returned
warnings/errors behavior
unit tests
regression tests if references exist
example usage
```

## Required Output for Report/UI Requests

When creating a report or UI, provide:

```text
which BookInput or BookResult it consumes
which runner it calls, if any
field mapping or display schema
report context fields
template skeleton or UI flow
proof that formulas are not in template/UI
smoke test
run command
```

## Acceptance Checklist

Before finalizing, verify:

```text
features classified into layers
source-of-truth and design basis identified
formulas live only in reusable calculation modules
book runner is the official calculation entry point
CSV/JSON/frontend/API inputs map to the same BookInput
unit conversions happen only at input/output boundaries
templates do not calculate
frontend/review does not calculate
batch does not calculate independently
units are explicit
result objects include intermediate values
warnings and errors are preserved
status semantics are defined
governing summary exists
tests cover reusable modules
book integration test exists
report rendering smoke test exists when reports exist
batch uses the same runner if present
traceability metadata exists for production outputs
run commands are documented
```

## Final Principle

Each calculation book should strengthen the future calculation platform.

Build reusable modules, typed models, standard runners, structured results, reviewable inputs, formal reports, traceability, and regression tests.
