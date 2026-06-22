# LaTeX Calculation Report Specification

Use this template when the user asks for calculation-book export, LaTeX export, Overleaf-compatible output, PDF-ready reports, or a reusable report template.

## Interaction Gate

Before project initialization or first report generation, ask:

```text
Do you have a preferred LaTeX/Overleaf template, .cls/.sty file, company cover, page format, or required report section order? If not, use the default engineering calculation book template.
```

This is a required interaction gate for agents generating a project. If the
user does not answer, answers "no", or supplies no usable template files, do
not block export. Record the interaction result as `no_response_default` or
`user_declined`, record the template ID as `default_engineering_calcbook`, and use:

```text
latex/templates/default_engineering_calcbook/
```

For generated web apps, expose a stable template selector backed by
`GET /api/report/templates`. Pass the selected template as `latex_template_id`
to `POST /api/report/latex`. If `latex_template_id` is missing or empty, the
backend must fall back to `default_engineering_calcbook`.

If the user supplies a reusable template, place it under:

```text
latex/templates/<template_id>/
```

The folder must contain `main.tex.j2`; it may also contain `.cls`, `.sty`,
images, fonts, and section templates needed by Overleaf.

## Required Project Shape

```text
latex/
  templates/
    default_engineering_calcbook/
      main.tex.j2
      template_manifest.yaml
      cover.tex.j2
      page_style.sty
      latexmkrc
      sections/
        01_summary.tex.j2
        02_inputs.tex.j2
        03_results.tex.j2
        90_traceability.tex.j2
  generated/
  output/
outputs/reports_latex/
outputs/reports_pdf/
src/pkg/report/latex_renderer.py
tests/smoke/test_latex_report.py
```

## Export Model

Generate an Overleaf-compatible zip package by default. Do not require a self-hosted Overleaf server for normal exports.

Required flow:

```text
BookInput + BookResult + ReportContext
-> build_latex_report_context()
-> render_latex_project_zip()
-> GET /api/report/templates for available template choices
-> /api/report/latex
-> outputs/reports_latex or browser download
```

## Template Boundary

LaTeX templates may contain:

```text
value references
loops
conditionals
formatting
section visibility logic
source and formula trace display
formula expression display from `FormulaTrace.expression_tex`
cross-references
```

LaTeX templates must not contain:

```text
engineering formulas
lookup rules
load-combination generation
optimization logic
official unit conversion
pass/fail recalculation
warning/error suppression
```

## Default Template Minimum

The default template must provide:

```text
cover page
table of contents
governing summary
input summary
calculation checks table
engineering charts when BookResult.charts is present
formula logic trace
calculation review cards or sections with formula expression, explanation, variable definitions, substitutions, source reference, and result path
sources
assumptions
warnings and errors
traceability metadata
template boundary statement
page header/footer
latexmkrc
```

## Optional PDF Compilation

For final calculation-book delivery, PDF compilation is not optional when a
local TeX toolchain exists. Detect `latexmk` first, then `pdflatex`.

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If only `pdflatex` exists, run it twice with `-interaction=nonstopmode` and
`-halt-on-error`. Completion requires exit code 0 and a generated `main.pdf`.
If compilation fails, do not mark the report complete. If no local TeX toolchain
is available, choose the A4 HTML report path from `html_report_spec.md`.

Still provide an Overleaf-compatible zip for collaborative editing/import when
requested.

## Replaceable Template Contract

Every report style is a folder under `latex/templates/<template_id>/`. A style
change should replace files in that folder, not report renderer code. The
folder may include `template_manifest.yaml` with:

```text
template_id
label
version
owner
required_assets
section_order
supports_formula_trace: true
```

Template sections must render the same `ReportContext` fields used by the web
and HTML preview. Formula displays must read `FormulaTrace.expression_tex` or
`FormulaTrace.expression_plain`; domain formulas must not be hardcoded in
template files.

## Overleaf Use

Use Overleaf as a collaborative editor/import target for the generated project, not as the default rendering dependency. If a deployment explicitly uses self-hosted Overleaf, document trust boundaries, compile permissions, storage, and operations separately from the calculation app.

## Validation Targets

The project validator should require:

```text
latex/templates/default_engineering_calcbook/main.tex.j2
latex/templates/default_engineering_calcbook/template_manifest.yaml
latex/templates/default_engineering_calcbook/cover.tex.j2
latex/templates/default_engineering_calcbook/page_style.sty
src/pkg/report/latex_renderer.py
tests/smoke/test_latex_report.py
/api/report/latex
```
