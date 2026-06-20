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
   sections, verification method, known limitations.
2. Build `ReportContext` (wrap BookResult — do not recalculate): project/case metadata; report
   production decision + status + output target; design basis and source references; input
   summary; assumptions and limitations; module summaries; governing summary; checks and stable
   result paths; chart specs and recommended report locations; selected intermediate values for
   audit; warnings/errors; formula/source trace references; imported-report comparison metadata;
   data-package metadata; appendix data; traceability metadata.
3. Choose the simplest renderer that satisfies the output: HTML (preview/browser review) | LaTeX
   project zip (Overleaf-compatible + PDF-ready) | PDF (frozen deliverable) | DOCX (editable
   client/report) | XLSX (tabular audit) | JSON (machine-readable). The renderer must preserve
   warnings, limitations, source basis, report status, and traceability metadata.
4. Enforce template boundaries. Templates MAY contain value references, loops/conditionals,
   formatting filters, section-visibility logic, unit-display formatting, cross-references.
   Templates MUST NOT contain engineering formulas, lookup rules, load-combination generation,
   optimization logic, independent unit conversion, or independent pass/fail logic.
5. Make the automatic report-output decision before claiming completion:
   if `latexmk`/`pdflatex` is available locally → choose LaTeX/PDF, compile locally, completion
   requires exit code 0 AND `main.pdf` exists; else → choose A4 HTML (`templates/implementation/
   html_report_spec.md`, `@page size: A4`, print-safe margins, cover/title block, governing
   summary, input summary, charts when `BookResult.charts` present, check tables, formula-logic
   trace, warnings/errors, traceability metadata, template-boundary statement). A failed LaTeX
   compile is a blocking failure, not a silent downgrade to HTML.
6. For LaTeX/Overleaf export (`templates/implementation/latex_report_spec.md`): before first
   generation ask whether the user has a preferred template/`.cls`/`.sty`/cover/page format/
   section order; if none supplied use `latex/templates/default_engineering_calcbook/`. Record the
   interaction as `user_selected` / `user_declined` / `no_response_default`. Generate an
   Overleaf-compatible zip by default (no self-hosted Overleaf required). Generated web apps must
   expose `GET /api/report/decision`, `GET /api/report/templates`, `POST /api/report/latex`
   (sending `latex_template_id`, defaulting to `default_engineering_calcbook` when missing),
   `POST /api/report/final`. Required files: `src/pkg/report/{latex_renderer,html_renderer,
   report_selector}.py`, `latex/templates/default_engineering_calcbook/{main.tex.j2,cover.tex.j2,
   page_style.sty,sections/}`, `outputs/reports_latex/`, `tests/smoke/test_latex_report.py`.

## Production minimum

Recorded report-production decision; explicit report status; saved final input or trusted saved
BookResult; clear source basis and limitations; structured ReportContext; template-boundary proof;
warnings/errors preserved; traceability metadata preserved; smoke test per renderer/export path;
LaTeX compile test or explicit no-LaTeX HTML-fallback record; documented run command. If any item
is missing, label the report `draft`/`review`/`prototype`/`not_for_construction`.

## Artifacts

```text
implementation/04_interfaces/report_context_spec.md   (templates/implementation/report_context_spec.md)
src/<pkg>/report/{latex_renderer,html_renderer,report_selector}.py
latex/templates/default_engineering_calcbook/...
outputs/reports_{html,pdf,docx,latex}/
tests/smoke/test_latex_report.py
```

## Exit gate

Readable A4/LaTeX book with required sections (Formula Logic Trace + Template Boundary Statement +
input summary + governing result + detailed checks + charts + sources + assumptions). See
`shared/lifecycle.md` row 12a. Next path: 12b if a frontend/review UI is needed, else 12c/13.
