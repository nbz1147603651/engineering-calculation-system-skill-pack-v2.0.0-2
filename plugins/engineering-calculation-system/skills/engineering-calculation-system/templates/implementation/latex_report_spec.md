# LaTeX Calculation Report Specification

Use this template when the user explicitly asks for LaTeX export, Overleaf-compatible output,
PDF-ready reports, or a reusable report template. The default final calculation book remains
print-ready A4 HTML from `html_report_spec.md`.

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

Treat every folder under `latex/templates/<template_id>/` as a replaceable
template-library entry. Replacing a style means adding or replacing a template
folder and manifest, not changing calculation modules or `run_book()`.

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
        04_figures.tex.j2
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
engineering figures when ReportContext.figures or BookResult.figures is present
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

The default style should match the formal A4 engineering calculation-book
pattern also used by the HTML renderer: formal cover, table of contents,
major-section page breaks, blue engineering headings, light-blue table headers,
formula/result/note visual treatments, sources, assumptions, traceability, and
an explicit template-boundary statement.

## Report Figures

Use the same `figures` list as the HTML renderer:

```yaml
figures:
  - figure_id: FIG-001
    title: Foundation layout
    caption: Plan view used for reviewer orientation.
    src: /static/reports/foundation-layout.png
    latex_path: figures/foundation-layout.png
    recommended_report_location: after_input_summary
    source_reference: S-FIG-001
    result_path: report.figures[0]
```

For LaTeX/Overleaf, `latex_path` should be a relative path inside the generated
zip. The template may show HTML-only `src` values as metadata, but it should
only call `\includegraphics` for paths that are packaged into the LaTeX project.
Figures are report evidence or review aids only; they must not replace formulas,
source references, or checked result paths.

## Requested PDF Compilation

For explicit PDF delivery, compile locally when a TeX toolchain exists. Detect
`latexmk` first, then `pdflatex`.

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If only `pdflatex` exists, run it twice with `-interaction=nonstopmode` and
`-halt-on-error`. Completion requires exit code 0 and a generated `main.pdf`.
If compilation fails, do not mark the requested PDF export complete. If no local
TeX toolchain is available, keep the default A4 HTML final report path and
return an Overleaf-compatible zip when that satisfies the request.

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
supports_report_figures: true
replaceable_template: true
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
