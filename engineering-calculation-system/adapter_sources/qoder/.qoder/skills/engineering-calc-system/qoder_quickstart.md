# Qoder Quickstart

This is the short operator guide for the Engineering Calculation System in Qoder.

## Qoder Package Self-Check

Classify the current install before doing implementation or release work:

| Shape | Present files | What it can do |
| --- | --- | --- |
| Direct QODER Skill | `SKILL.md`, `reference.md`, `qoder_quickstart.md`, `assets/lifecycle-console.html` | Route, explain gates, guide work. Do not claim `web-complete` from this shape alone. |
| QODER Project overlay | `.qoder/agents/engineering-calc-system.md`, `.qoder/skills/engineering-calc-system/`, `.qoder/references/engineering-calc-system.md` | Agent-first supervision with worker agents and skill resources. |
| Complete core project | `SKILL.md`, `skills/`, `shared/`, `templates/`, `schemas/`, `scripts/validate_artifacts.py`, `project_template/` | Full source-backed implementation, validation, report, web, batch, and deployment closure. |

If the task asks for a deployable online calculator or `web-complete`, use the QODER Project package together with the complete core package. If only the direct skill is installed, label outputs as guidance, draft, or prototype until the core validator can run.

## Static Report Triage

Before editing a generated project, check whether it only contains calculation scripts and
exported reports, for example `src/*.py` plus `reports/*.html`, but no `webapp/`, `apps/review/`,
`latex/templates/`, `src/pkg/report/`, `tests/smoke/`, `deploy/`, or `handoff/`.

If so, classify the project as `static_report_or_cli_only`, not `web-complete`. The next action is
to migrate the calculation logic into the complete project scaffold:

```text
run_book(BookInput) -> BookResult
src/pkg/report/{html_renderer,latex_renderer,report_selector}.py
webapp/{app.py,routes.py,form_utils.py,i18n.py}
webapp/templates/ and webapp/static/
apps/review/calculation_review.py and admin_formula_review.py when review is in scope
data/ + outputs/ import/export areas
tests/smoke/test_web_routes.py and tests/smoke/test_latex_report.py
deploy/ and release/
```

Do not make the static report prettier and call it a web app. Treat it as an imported visual
reference or regression comparison until the scaffold and validator pass.

## A4 HTML First

For calculation-book output, prefer print-ready A4 HTML as the default final report:
`@page size: A4`, print-safe margins, page-like browser preview, formula logic traces, chart data
tables, source paths, warnings/errors, sources, assumptions, and traceability. Keep LaTeX/Overleaf
zip and PDF as explicit exports when the user, client template, or handoff requires them.

When the current book's result-path registry or `ReportContext` exposes useful grouped numeric
outputs, repeated categories, ordered series, or other reviewer-useful chartable data, generate
`BookResult.charts` / `ChartSpec` in the book layer and render those charts in the UI and A4 HTML
report. Do not copy fixed chart IDs or paths from another project. Charts must visualize
already-computed values only.

## First Prompt To Qoder

Use the supervisor agent when it exists:

```text
Use .qoder/agents/engineering-calc-system.md as supervisor. Classify the material state, delivery mode, required lifecycle path, gate status, and next artifacts before editing code.
```

For direct skill import only:

```text
Use the Engineering Calculation System skill as a lightweight router. Tell me whether my current files are enough for web-complete, and list the missing core package artifacts before implementation.
```

## Validation Commands

From a complete core skill root:

```bash
python scripts/validate_artifacts.py --package-root . --profile core
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```

From this repository source checkout:

```bash
python tools/build_release.py --profile qoder-addon
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/qoder-addon --profile qoder-addon
python tools/install_qoder_user.py --audit
```

## Agent Routing

The supervisor keeps these decisions serial: lifecycle route, evidence gate, source authority, ID allocation, handoff freeze, `run_book(BookInput) -> BookResult`, production label, and release acceptance.

Delegate only bounded work to workers:

- `engineering-calc-reference-acquirer`: phases 01-03
- `engineering-calc-source-intake`: phase 04
- `engineering-calc-logic-extractor`: phases 05-07 draft artifacts
- `engineering-calc-module-worker`: phases 08-11 owned implementation slices
- `engineering-calc-interface-worker`: 12/12a/12b/12c thin interfaces
- `engineering-calc-verification-worker`: phase 13 checks
- `engineering-calc-release-worker`: phase 14 deployment artifacts

## Completion Bar

Do not say complete, production-ready, deployable, or `web-complete` unless:

- `shared/lifecycle.md` has been applied
- `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow production
- real input creates non-empty evaluated `BookResult.checks`
- API/UI, report, import/export, batch, deployment artifacts, and smoke tests exist
- `validate_artifacts.py --delivery web-complete` passes
