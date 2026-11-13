# HTML A4 Calculation Report Specification

Use this template as the default final calculation-book format unless the user
or governing handoff explicitly requires a compiled PDF. The HTML book should
look like an A4 engineering calculation sheet on screen and print cleanly from a
browser without extra manual styling.

## Automatic Output Decision

The report agent must choose print-ready A4 HTML first:

```text
default:
  render A4 HTML calculation report
  include @page size: A4, print-safe margins, and page-like screen preview
when the user explicitly requests LaTeX/PDF or the handoff requires it:
  render LaTeX or Overleaf zip
  compile to PDF only when a local compiler is available
  accept PDF completion only when compilation exits 0 and main.pdf exists
```

The generated project should expose this decision through:

```text
GET /api/report/decision
POST /api/report/final
POST /api/report/final with report_format=latex_pdf only when PDF is explicitly requested
lang=en|zh|bilingual for report preview/final when multilingual reporting is in scope
```

## A4 Layout Minimum

HTML reports must be formatted as formal A4 calculation books:

```text
@page size: A4
print-safe margins
page-like screen preview with 210mm width
@media print removes backgrounds, shadows, and browser-only chrome
cover or title block
table of contents
major sections start on new print pages
control results and governing summary
input summary
engineering figures when ReportContext.figures or BookResult.figures is present
engineering charts when BookResult.charts is present, with chart data tables
calculation checks
formula logic trace
calculation review cards with formula boxes, explanations, variables, substitutions, result paths, and source references
sources
assumptions
warnings and errors
traceability metadata
template boundary statement
language/template decision statement when user_interaction_decisions.csv records defaults or user selections
```

## Default Style Template

The default HTML style should follow a traditional engineering calculation
book, not a dashboard:

```text
Times New Roman or equivalent serif body text
formal cover page
centered calculation-book title
blue engineering section headings
light-blue table headers
thin bordered tables
formula boxes with a blue left rule
result boxes for governing values
yellow note boxes for limitations or review notes
page breaks before major sections
end-of-report footer
```

This style is based on the accepted geotechnical calculation book pattern:
cover, table of contents, introduction/design basis, geometry/input data,
subsoil or model conditions when relevant, detailed calculations, checks,
settlement/stability or module-specific result sections, summary,
recommendations, sources, and appendices.

## Report Figures

Images are presentation assets, not calculation logic. The preferred
ReportContext field is:

```yaml
figures:
  - figure_id: FIG-001
    title: Foundation layout
    caption: Plan view used for reviewer orientation.
    src: data:image/png;base64,...   # or relative/static browser path
    latex_path: figures/foundation-layout.png
    recommended_report_location: after_input_summary
    source_reference: S-FIG-001
    result_path: report.figures[0]
    notes:
      - Supplied as a report illustration only.
```

Recommended `recommended_report_location` values:

```text
after_cover | front_matter | after_input_summary | before_charts |
after_charts | before_checks | appendix | appendix_figures
```

Use figures for cover/context images, site plans, geometry diagrams, soil
profiles, load arrangement diagrams, result contour images, chart companions,
or appendix evidence. Do not place figures inside templates as a substitute for
source-backed formula traces or official result values.

## Presentation Boundary

HTML templates may contain formatting, tables, value references, loops, and
visibility logic. They must not contain engineering formulas, lookup rules,
official unit conversion, load-combination generation, optimization logic, or
independent pass/fail recalculation.

Formula expressions shown in HTML must come from `FormulaTrace.expression_tex`
or `FormulaTrace.expression_plain` and follow `calculation_review_card_spec.md`.

## Required Project Shape

```text
src/pkg/report/html_renderer.py
src/pkg/report/report_selector.py
report template metadata exposed by /api/report/templates when a template library is used
outputs/reports_html/
tests/smoke/test_web_routes.py
tests/smoke/test_latex_report.py
```

## Replaceable Template Library

HTML styles should be treated as replaceable template-library entries even when
the default implementation is a Python renderer. Each reusable style needs a
stable template ID, label, version, supported features, and boundary statement.
Future file-based HTML templates should live under a template-library folder
such as `html/templates/<template_id>/` or an equivalent project-approved
location. Style replacement must not require changes to `run_book()` or
formula modules.
Record user-supplied or defaulted style/template choices in
`analysis/06_user_interaction/user_interaction_decisions.csv`.

## Validation Targets

Generated projects should verify:

```text
/api/report/decision defaults to html_a4
/api/report/final returns A4 HTML by default
/api/report/latex returns an Overleaf-compatible zip when LaTeX export is in scope
HTML contains @page size: A4
HTML print CSS removes screen-only decoration
HTML contains Table of Contents
HTML contains Engineering Figures when figure specs exist
HTML contains Engineering Charts when chart specs exist
HTML chart section includes a data table and source result paths
HTML contains Formula Logic Trace
HTML contains formula-box
HTML contains engineering explanation
HTML contains result_path
HTML contains Sources
HTML contains Assumptions
HTML contains Template Boundary Statement
HTML respects lang=en|zh|bilingual when multilingual reporting is in scope
report output records template ID and user/default decision source
```
