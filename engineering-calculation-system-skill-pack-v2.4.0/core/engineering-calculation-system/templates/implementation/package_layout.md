# Package Layout

| Package Or File | Layer | Responsibility | May Import | Must Not Import |
| --- | --- | --- | --- | --- |
| src/<pkg>/core/ | core platform | statuses, checks, traces, units, hashes | standard library | domain formulas |
| src/<pkg>/libraries/ | reusable engineering library | formulas, lookups, branch-local checks | core | books, UI, reports |
| src/<pkg>/books/<book_name>/ | book runner | official orchestration and BookResult | core, libraries | UI pages |
| src/<pkg>/interfaces/ | interface layer | CLI/API/batch adapters | books | formulas |
| src/<pkg>/report/ | report layer | render from ReportContext | books or report context | formulas |
| webapp/ or src/<pkg>/interfaces/webapp/ | production frontend | Jinja2 + Bootstrap 5 + vanilla JS web UI, import/export, report preview | books/API/report context | formulas |
| latex/ | report template assets | Overleaf-compatible LaTeX templates, page style, section templates | none at runtime | formulas |
| src/pkg/report/ | report renderers and selector | A4 HTML renderer, LaTeX renderer, automatic final report decision | books, UI routes | engineering formulas |
| apps/review/ | Marimo review apps | module review, editable draft inputs, traces, what-if exploration | books, libraries, report context | formulas not already in trusted modules |
| data/ | managed input area | input, imported reports, references, staging, normalized cases, packages | none | generated results |
| outputs/ | generated output area | BookResult JSON, reports, packages, logs | none | source inputs |
| deploy/ | deployment layer | Dockerfile, systemd service, nginx config, runtime env examples | app entrypoint only by command | formulas, reusable module internals |
| release/ | release handoff | release checklist, runbook, smoke records | none | formulas |
