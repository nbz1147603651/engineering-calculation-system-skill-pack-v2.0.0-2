---
name: cloud-web-release-deployment
description: Package and verify a production-ready engineering calculation web application for local operation and Linux cloud deployment. Use after implementation and verification, or when the user asks for a runnable online calculator, cloud deployment, Linux server deployment, Docker/systemd/nginx packaging, release artifacts, operations runbook, local client package, or final deployable delivery.
---

# Cloud Web Release and Deployment

## When to use

Final delivery stage. Produce a runnable, traceable, reviewable, modifiable, and Linux-deployable
web calculation program. The release is not complete until a fresh operator can run the app
locally, inspect traces and source basis, modify decoupled calculation modules, and deploy the
same calculation path to a Linux server. Default runtime: Python 3.9+ with Flask/FastAPI app
factory, gunicorn (or equivalent WSGI/ASGI), a `webapp/` browser frontend, optional Marimo review
service. The static-HTML guard and `run_book()` contract live in `shared/lifecycle.md`.

## Inputs

```text
handoff/implementation_handoff.yaml
implementation/00_architecture/dependency_rules.md
implementation/02_modules/module_asset_registry.csv
verification/acceptance_checklist.md
webapp/ or src/<pkg>/interfaces/webapp/
tests/
```

Do not package as production-ready if verification failed, source basis is missing, or the web/API
layer calculates outside `run_book()`.
If the project has no `webapp/app.py`, no `webapp/routes.py`, or no web smoke test, stop and route
back to 12b/13. A generated report HTML file is an output artifact, not a release target.

## Steps

1. Provide both release targets unless the user narrows scope: a local web client (runs on the
   user's machine, opens in a browser) and a cloud Linux web service (behind gunicorn on a Linux
   server, optionally nginx/systemd/Docker). For a desktop installer add Electron/Tauri/PyInstaller
   only when a true desktop client is requested.
2. Build the production-web minimum: application factory `create_app()`; `GET /health` for
   deployment smoke; thin API routes calling `run_book()`; explicit `form_to_model` and
   `result_to_ui` mapping; static/templates or SPA bundle for the browser UI; Chinese/English
   language switch with `/api/i18n/<lang>`, persisted selection, selected-language report calls;
   environment-based configuration; non-debug production defaults; structured error responses that
   preserve server logs.
3. When Marimo admin review is embedded, deploy it as separate services proxied under
   `/admin/review/` and `/admin/formulas/`, with the Flask password-gated admin shell at
   `/admin/`: Docker Compose services for the main web app,
   Marimo calculation review, and Marimo formula publishing, shared `data/formula_registry/`
   volume, admin-password env var for the Flask shell, admin-token env var for Marimo, nginx
   proxy rules for websocket/long sessions, and Marimo ports bound to localhost or an internal
   network. If Marimo is not installed on a Linux host, the
   admin shell must show the install prompt rather than silently hiding review.
4. Create/update deployment files: `deploy/env.example`, `deploy/Dockerfile` or
   `deploy/systemd/*.service`, `deploy/nginx/*.conf` when reverse-proxying, `deploy/docker-compose.yml`,
   `deploy/one_click_deploy.sh`
   when Docker is used, `apps/review/admin_formula_review.py` when embedded admin review is used,
   `release/release_checklist.md`, `release/runbook.md` when operational handoff is needed. Document:
   local run command, Linux production run command, required env vars, port/host binding,
   data/output persistence paths, log location, backup/export strategy, health-check command,
   rollback/stop command.
5. Confirm module assets are release-ready: each module has stable module_id + public function,
   typed inputs/options/results, owns formulas/lookup behavior only, no web/report/batch/FS/DB
   dependency, source references + formula traces recorded, unit + regression tests cover it,
   reuse status in `module_asset_registry.csv`.
6. Apply Linux deployment rules: gunicorn or equivalent production WSGI/ASGI; bind to internal
   host/port unless intentionally exposed; TLS/compression/public routing in nginx or platform
   proxy; secrets from env or server secret storage; outputs only to configured data/output dirs;
   logs to journald/container logs/configured files; debug off.
7. Run smoke tests: `python -m webapp.app` (or equivalent local start); `GET /health`; `GET /`;
   `POST /api/calculate` with a known input; `GET /api/i18n/en` and `GET /api/i18n/zh` + main-page
   language-toggle shell; report preview/export when present; admin shell `/admin/`; Marimo admin
   `/admin/review/` when present; formula admin `/admin/formulas/` when present; `bash deploy/one_click_deploy.sh`
   syntax or dry-run inspection when possible; Docker build/run or systemd command syntax when
   provided; artifact-validation script.
   If the environment cannot start Docker/systemd/nginx, still validate file presence and command
   syntax where possible, and provide the exact unrun command plus the reason it was not executed.

## Artifacts

```text
deploy/{env.example, one_click_deploy.sh, Dockerfile, docker-compose.yml, systemd/*.service, nginx/*.conf}
apps/review/admin_formula_review.py   (when embedded admin review used)
release/{release_checklist.md, runbook.md}
```

## Exit gate

Runnable local + Linux-cloud path exists; deployment artifacts present for production completion.
See `shared/lifecycle.md` row 14. Next path: none — delivery closes at the Web-Complete Exit Gate.
