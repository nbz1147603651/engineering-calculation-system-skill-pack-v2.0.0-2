# HTML A4 Calculation Report Specification

Use this template when the environment has no local LaTeX compiler, when the
user explicitly requests HTML, or when an HTML preview/download is required.

## Automatic Output Decision

The report agent must choose the strictest available calculation-book output:

```text
if latexmk or pdflatex is available:
  render LaTeX
  compile to PDF
  accept completion only when compilation exits 0 and main.pdf exists
else:
  render A4 HTML calculation report
```

The generated project should expose this decision through:

```text
GET /api/report/decision
POST /api/report/final
```

## A4 Layout Minimum

HTML reports must be formatted as formal A4 calculation books:

```text
@page size: A4
print-safe margins
cover or title block
governing summary
input summary
calculation checks
formula logic trace
warnings and errors
traceability metadata
template boundary statement
```

## Presentation Boundary

HTML templates may contain formatting, tables, value references, loops, and
visibility logic. They must not contain engineering formulas, lookup rules,
official unit conversion, load-combination generation, optimization logic, or
independent pass/fail recalculation.

## Required Project Shape

```text
src/pkg/report/html_renderer.py
src/pkg/report/report_selector.py
outputs/reports_html/
tests/smoke/test_web_routes.py
tests/smoke/test_latex_report.py
```

## Validation Targets

Generated projects should verify:

```text
/api/report/decision returns latex_pdf or html_a4
/api/report/final returns PDF when LaTeX compilation succeeds
/api/report/final returns A4 HTML when no LaTeX compiler is available
HTML contains @page size: A4
HTML contains Formula Logic Trace
HTML contains Template Boundary Statement
```
