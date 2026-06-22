# Calculation Review Card Specification

Use this template whenever a web page, HTML A4 report, LaTeX report, or Marimo review app displays calculation checks.

## Purpose

Make calculation books readable without moving engineering logic into presentation layers. Each displayed formula, explanation, variable table, substitution, result path, and source reference must come from `BookResult`, `ReportContext`, or a source-backed formula registry. UI and report templates render the data only.

## Data Contract

Each important `CheckResult` should expose at least one `FormulaTrace` with the following display fields in addition to the core audit fields:

| Field | Meaning |
| --- | --- |
| `formula_id` | Stable ID from the formula inventory or formula registry |
| `formula_name` | Human-readable method name |
| `source_reference` | Source ID plus clause/table/equation/page |
| `expression_tex` | TeX expression for display in KaTeX/LaTeX; sourced from the formula inventory/registry |
| `expression_plain` | Plain-text fallback expression |
| `engineering_explanation` | Short reviewer-facing explanation of what the formula checks |
| `variable_definitions` | Symbol-to-meaning map, including units where helpful |
| `inputs` | Values used by the formula |
| `substitutions` | Display-ready substitution values, if different from raw inputs |
| `intermediates` | Audit values needed for review |
| `result_symbol` | Engineering symbol for the result |
| `result_value` | Computed result value from the calculation module |
| `unit` | Result unit |
| `result_path` | Stable `BookResult` path used by UI/report/template references |
| `display_icon` | Design-system icon class declared by `FormulaTrace`, `review_schema.csv`, or a review display registry |
| `notes` | Warnings, assumptions, or implementation comments |

If a production check has no source-backed expression, explanation, source reference, or result path, treat the interface/report as `prototype` or `incomplete` until the trace is fixed.

## Visual Skeleton

Render each calculation review card in this order:

1. Header: icon, check name, status, utilization/margin, source reference.
2. Engineering explanation: one short paragraph stating the check purpose and governing interpretation.
3. Formula box: TeX via KaTeX/MathJax in the web UI and `equation*`/display math in LaTeX.
4. Variable table: symbol, meaning, units/notes.
5. Substitution/input table: recorded input values and selected branch/lookup values.
6. Intermediate table: only values useful for audit, not every local variable.
7. Result row: symbol, value, unit, status, and stable result path.
8. Notes/warnings: visible text, not color-only.

## Display Registry

Do not hardcode project-specific icons, labels, formulas, section order, or check families in JavaScript, HTML, LaTeX, or Marimo apps. Seed projects may provide defaults through `review_schema.csv`, `result_path_registry.csv`, `FormulaTrace.display_icon`, or a book-specific review display registry. Generated code should render those fields and fall back to neutral audit labels such as `bi-braces` only when no display metadata exists.

## Rendering Boundary

- Web JS may call KaTeX/MathJax and format tables. It must not compute engineering values, perform official unit conversion, choose lookup branches, or override status.
- HTML and LaTeX templates may loop over traces and display `expression_tex`, variables, substitutions, sources, and result paths. They must not contain domain formulas hardcoded in the template.
- Marimo review apps are the primary interactive review surface. They may load frontend-created review sessions, run trusted Python modules, expose draft cells in `marimo edit`, and save review decisions. Official production output still goes through `run_book()` and validation; declaration-based formula publication remains a separate admin flow.

## Maintainability Pattern

- Add or change a formula display by updating the source-backed formula inventory/registry and the module-emitted `FormulaTrace`.
- Add a company or project report style by adding `latex/templates/<template_id>/main.tex.j2` plus optional section templates, assets, `.cls`, and `.sty` files. Do not branch report code for style-only changes.
- Keep UI card structure in `webapp/static/css/components.css` and renderer-neutral data in `ReportContext`.
- Keep book-specific labels and field visibility in `review_schema.csv`, `frontend_fields.csv`, and `result_path_registry.csv`.

## Validation Targets

Production projects should verify that at least one representative calculation check renders:

```text
formula-box
review-icon
engineering explanation
source_reference
expression_tex or expression_plain
variable_definitions
result_path
Formula Logic Trace
Template Boundary Statement
```
