---
name: report-review-batch-interfaces
description: Route and govern report, frontend, review, API, import/export, upload-package, batch, LaTeX/Overleaf calculation-book export, and deployable-web interface work over a trusted engineering calculation book runner and BookResult. Use when the task needs presentation, review, report rendering, operational UI, data package, API, CLI, batch workflows, or a final runnable online web calculator while keeping formulas and independent pass/fail logic out of interface layers.
---

# Report, Review, Batch, and Interface Router

## When to use

After `run_book()` and `BookResult` exist or are specified (skill 11). This skill selects the
correct interface subskill and enforces the shared interface rules. Load only the subskill needed
by the user request. When the interface must become a deployable online web calculator, route to
skill 14 after frontend/API verification.

## Core principle

Interfaces consume trusted calculation outputs; they do not become calculation engines. The
formula-placement rule, the `run_book(BookInput) -> BookResult` contract, and the static-HTML
guard all live in `shared/lifecycle.md` (single source — do not restate).

## Step 1 — select subskill(s)

```text
12a-report-context-and-rendering        ReportContext design, report-production decisions, renderer
                                        choice, templates, preview, HTML/LaTeX/PDF/DOCX/XLSX/JSON
                                        exports, report status, template boundaries.
12b-frontend-and-review-interfaces      Production web UI, form-to-model mapping, API route shape,
                                        frontend JS structure, i18n, charts, numeric sanitization,
                                        Marimo review apps.
12c-batch-import-export-packages        Managed data areas, report import, upload packages,
                                        import/export manifests, hashes, package validation,
                                        CLI/API batch runs, batch summaries.
14-cloud-web-release-deployment         After 12b and 13, when a runnable local + cloud-deployable
                                        online web calculator is expected.
```

If the request spans all three families, read in this order: `12a -> 12b -> 12c -> 13 -> 14`.
If the project already has only a report generator or exported HTML calculation book and the user
expects a runnable calculator, select all three interface families plus 13 and 14. Treat the
existing report as review evidence or a visual reference, not as the application runtime.

## Step 2 — record the interface decision

Before implementation, record: requested interface family; consumed BookInput/BookResult/
ReportContext; runner entrypoint; source of saved input/result; report/interface status; chosen
templates or UI pattern; import/export or batch scope; release/deployment scope when final web
delivery is expected; verification method; known limitations; selected subskills.

## Shared interface contract (every family preserves)

BookInput path mapping; BookResult/ReportContext result paths; source basis and limitations;
warnings, errors, assumptions, prototype status; input hash and result hash when persisted; runner
version and report/template version when available; stable export paths; smoke tests for each
user-facing path.

## Report status labels

`draft | review | final | superseded | prototype | not_for_construction`. Do not label an output
`final` unless the coding gate allows production, the source basis is sufficient, the output is
generated from saved final input or trusted saved `BookResult`, and verification has passed.

## Templates available

```text
templates/implementation/{input_mapping_spec, ui_layout_spec, ui_design_system, report_context_spec,
  latex_report_spec, import_export_contract, marimo_review_spec, batch_flow}.md
templates/implementation/data_package_manifest.yaml
templates/deployment/{cloud_linux_deployment, release_checklist}.md
```

## Exit gate

Required subskills are selected; every interface is a thin layer over `run_book`. See
`shared/lifecycle.md` row 12. Next path: the selected subskill(s), then 13.
