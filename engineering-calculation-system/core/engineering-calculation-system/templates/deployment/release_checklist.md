# Release Checklist

## Release Identity

| Item | Value |
| --- | --- |
| Release ID | to_be_defined |
| Project/book | to_be_defined |
| Version | to_be_defined |
| Git commit or source snapshot | to_be_defined |
| Release status | draft / review / production_ready / blocked |

## Required Gates

- [ ] Source basis and implementation handoff are recorded.
- [ ] Runtime stack is recorded: Python 3.9+ primary runtime unless an explicit adapter plan exists.
- [ ] Frontend format is recorded: Jinja2 + Bootstrap 5 + vanilla JavaScript modules unless explicitly overridden.
- [ ] Operator workflow quality is not reduced merely to minimize dependencies.
- [ ] Calculation modules are decoupled and listed in `module_asset_registry.csv`.
- [ ] Official calculation path is `run_book(BookInput) -> BookResult`.
- [ ] Web/API/report/batch layers do not implement formulas or independent pass/fail logic.
- [ ] Unit, regression, integration, interface, and smoke tests pass or blockers are recorded.
- [ ] Traceability metadata includes source basis, input hash, result hash, runner version, and report/template version when present.
- [ ] Local web client run command is documented and tested.
- [ ] Cloud Linux deployment files are present.
- [ ] `deploy/one_click_deploy.sh` exists and is documented for `auto`, `compose`, and `local` modes.
- [ ] `/health` endpoint passes.
- [ ] `POST /api/calculate` smoke test passes with known input.
- [ ] `GET /api/report/decision` records `html_a4` as the default final report output; `latex_pdf` is explicit or handoff-required.
- [ ] `POST /api/report/final` passes: A4 HTML contains `@page size: A4`, print-safe CSS, and chart data tables/source result paths when charts are emitted.
- [ ] Chinese/English UI switch is present, persisted, and smoke-tested through `/api/i18n/en` and `/api/i18n/zh`.
- [ ] Delivery is not only a static `.html` file, exported report HTML, or mockup unless explicitly labeled as a non-production prototype.
- [ ] Production debug mode is disabled.
- [ ] Secrets are environment-based and not committed.
- [ ] Data and output persistence paths are documented.
- [ ] Formula registry path is shared by web and Marimo services when admin review is enabled.
- [ ] `/admin/` is protected by `ADMIN_REVIEW_PASSWORD` before modification controls are shown.
- [ ] Marimo review and formula publishing services are protected by `ADMIN_REVIEW_TOKEN`.
- [ ] Marimo review and formula publishing ports bind to localhost or an internal network, not the public interface.
- [ ] Formula publisher is proxied under `/admin/formulas/` when enabled.
- [ ] Formula publish failures do not change `active_versions.yaml`.

## Release Artifacts

| Artifact | Path | Required | Status |
| --- | --- | --- | --- |
| Local run instructions | README.md | true | to_be_defined |
| Environment example | deploy/env.example | true | to_be_defined |
| One-click deploy script | deploy/one_click_deploy.sh | true | to_be_defined |
| Dockerfile | deploy/Dockerfile | Docker path | to_be_defined |
| systemd service | deploy/systemd/*.service | systemd path | to_be_defined |
| nginx site config | deploy/nginx/*.conf | public Linux path | to_be_defined |
| Marimo admin app | apps/review/admin_formula_review.py | when admin review enabled | to_be_defined |
| Formula registry | data/formula_registry/active_versions.yaml | when editable formulas enabled | to_be_defined |
| Release runbook | release/runbook.md | when operational handoff needed | to_be_defined |
| Acceptance checklist | verification/acceptance_checklist.md | true | to_be_defined |

## Smoke Test Record

| Test | Command | Result | Notes |
| --- | --- | --- | --- |
| Local app start | `python -m webapp.app` | to_be_defined |  |
| Health | `curl -fsS http://127.0.0.1:5000/health` | to_be_defined |  |
| Main page | `curl -fsS http://127.0.0.1:5000/` | to_be_defined |  |
| i18n EN/ZH | `curl -fsS http://127.0.0.1:5000/api/i18n/en && curl -fsS http://127.0.0.1:5000/api/i18n/zh` | to_be_defined |  |
| Calculate API | `curl -fsS -X POST ... /api/calculate` | to_be_defined |  |
| Report decision | `curl -fsS http://127.0.0.1:5000/api/report/decision` | to_be_defined |  |
| Final report | `curl -fsS -X POST ... /api/report/final` | to_be_defined |  |
| Marimo admin | `curl -fsS http://127.0.0.1:2718/` | to_be_defined |  |
| Formula admin | `curl -fsS http://127.0.0.1:2719/` | to_be_defined |  |
| One-click deploy | `bash deploy/one_click_deploy.sh auto` | to_be_defined |  |
| Docker build | `docker build -f deploy/Dockerfile .` | to_be_defined |  |

## Remaining Assumptions

| Assumption | Risk | Owner | Resolution |
| --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined |
