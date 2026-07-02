---
name: report-context-and-rendering
description: Design and implement source-backed engineering calculation report context, report production decisions, renderer choices, report templates, report preview, and HTML/LaTeX/PDF/DOCX/XLSX/JSON exports over trusted BookResult data. Use when building reports, calculation books, LaTeX/Overleaf-compatible exports, or report previews while keeping templates free of engineering formulas and independent pass/fail logic.
---

# Report Context and Rendering

## When to use

For report production after `run_book()` and `BookResult` exist. Reports are built from a
structured `ReportContext` that wraps trusted results without recalculating.

## Steps

1. Record the report-production decision (use `templates/implementation/report_context_spec.md`):
   purpose, audience, review depth, status, required output formats, governing source basis, saved
   input/result source, required traceability metadata, renderer choice + reason, required report
   sections, report language mode (`en`/`zh`/`bilingual`), template selection status, verification
   method, known limitations. Cross-reference
   `analysis/06_user_interaction/user_interaction_decisions.csv` for user-selected, declined, or
   defaulted report decisions.
   If a legacy `report_generator.py` or `reports/*.html` file exists, record it as imported
   comparison evidence only. Do not reuse it as the production renderer unless it has been refit
   to consume `ReportContext` from `BookResult` without recalculating.
2. Build `ReportContext` (wrap BookResult, do not recalculate): project/case metadata; report
   production decision + status + output target; design basis and source references; input
   summary; assumptions and limitations; module summaries; governing summary; checks and stable
   result paths; chart specs and recommended report locations; selected intermediate values for
   audit; report figures with source references and recommended report locations when useful;
   warnings/errors; formula/source trace references; imported-report comparison metadata;
   data-package metadata; appendix data; traceability metadata. For every production check, include
   reviewer-facing formula display data from `FormulaTrace`: `expression_tex` or `expression_plain`,
   engineering explanation, variable definitions, substitutions, source reference, display icon,
   and stable result path. Use `templates/implementation/calculation_review_card_spec.md`.
3. Choose print-ready A4 HTML as the primary/default calculation-book renderer
   (`templates/implementation/html_report_spec.md`). Use LaTeX project zip
   (Overleaf-compatible), compiled PDF, DOCX, XLSX, or JSON as explicit exports when the user,
   handoff, or client workflow requires them. The renderer must preserve warnings, limitations,
   source basis, report status, language mode, and traceability metadata.
4. Enforce template boundaries. Templates MAY contain value references, loops/conditionals,
   formatting filters, section-visibility logic, unit-display formatting, cross-references.
   Templates MUST NOT contain engineering formulas, lookup rules, load-combination generation,
   optimization logic, independent unit conversion, or independent pass/fail logic.
   Templates may render formula expressions only when the expression is supplied by
   source-backed `FormulaTrace`/formula-registry data.
5. Make the automatic report-output decision before claiming completion: default to A4 HTML
   (`@page size: A4`, print-safe margins, page-like screen preview, print CSS that removes
   backgrounds/shadows/chrome, formal cover page, table of contents, governing summary, input
   summary, figures when `ReportContext.figures` or `BookResult.figures` are present, charts when
   `BookResult.charts` present, chart data tables with source result paths for emitted charts,
   check tables, formula-logic trace with readable calculation review cards, warnings/errors, traceability
   metadata, template-boundary statement). If the user explicitly requests LaTeX/PDF or the
   handoff requires it, generate the LaTeX/Overleaf export and compile locally when
   `latexmk`/`pdflatex` is available; PDF completion requires exit code 0 AND `main.pdf` exists.
   A failed requested LaTeX compile is a blocking failure, not a silent downgrade to HTML.
6. For LaTeX/Overleaf export (`templates/implementation/latex_report_spec.md`): before first
   generation ask whether the user has a preferred template/`.cls`/`.sty`/cover/page format/
   section order; if none supplied use `latex/templates/default_engineering_calcbook/`. Record the
   interaction as `user_selected` / `user_declined` / `no_response_default` in the user interaction
   decisions ledger. Generate an Overleaf-compatible zip by default (no self-hosted Overleaf
   required). Keep each report style replaceable under `latex/templates/<template_id>/` with a
   `template_manifest.yaml`; style changes must not require report renderer code changes.
   Generated web apps must expose `GET /api/report/decision`,
   `GET /api/report/templates`, `POST /api/report/latex` (sending `latex_template_id`, defaulting
   to `default_engineering_calcbook` when missing), `POST /api/report/final`. Required files:
   `src/pkg/report/{latex_renderer,html_renderer,report_selector}.py`,
   `latex/templates/default_engineering_calcbook/{main.tex.j2,cover.tex.j2,page_style.sty,sections/}`,
   `outputs/reports_latex/`, `tests/smoke/test_latex_report.py`. When these files are missing in
   an existing project, create them from the project template pattern before claiming report
   completion.

## Production minimum

Recorded report-production decision; explicit report status; saved final input or trusted saved
BookResult; clear source basis and limitations; structured ReportContext; language/template
decision recorded; template-boundary proof; warnings/errors preserved; traceability metadata
preserved; smoke test per renderer/export path and selected language mode; default A4 HTML report
verified for browser printing; requested LaTeX/PDF exports compiled or packaged as required;
documented run command. If any item is missing, label the report
`draft`/`review`/`prototype`/`not_for_construction`.

## Artifacts

```text
implementation/04_interfaces/report_context_spec.md   (templates/implementation/report_context_spec.md)
src/<pkg>/report/{latex_renderer,html_renderer,report_selector}.py
latex/templates/default_engineering_calcbook/...
outputs/reports_{html,pdf,docx,latex}/
tests/smoke/test_latex_report.py
```

## Exit gate

Readable print-ready A4 HTML book by default, plus requested LaTeX/PDF exports, with required
sections (Formula Logic Trace with formula boxes/explanations + Template Boundary Statement +
input summary + governing result + detailed checks + charts + report figures when present +
sources + assumptions). See
`shared/lifecycle.md` row 12a. Next path: 12b if a frontend/review UI is needed, else 12c/13.
