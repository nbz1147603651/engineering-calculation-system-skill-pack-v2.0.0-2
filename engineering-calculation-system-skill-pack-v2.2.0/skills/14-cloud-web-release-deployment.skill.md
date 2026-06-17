---
name: cloud-web-release-deployment
description: Package and verify a production-ready engineering calculation web application for local operation and Linux cloud deployment. Use after implementation and verification, or when the user asks for a runnable online calculator, cloud deployment, Linux server deployment, Docker/systemd/nginx packaging, release artifacts, operations runbook, local client package, or final deployable delivery.
---

# Cloud Web Release and Deployment

Use this skill as the final delivery stage for engineering calculation software.

## Goal

Produce a runnable, traceable, reviewable, modifiable, and Linux-deployable web calculation program.

The release is not complete until a fresh operator can run the app locally, inspect traces and source basis, modify decoupled calculation modules, and deploy the same calculation path to a Linux server.

## Required Inputs

```text
handoff/implementation_handoff.yaml
implementation/00_architecture/dependency_rules.md
implementation/02_modules/module_asset_registry.csv
verification/acceptance_checklist.md
webapp/ or src/<pkg>/interfaces/webapp/
tests/
```

Do not package as production-ready if verification failed, source basis is missing, or the web/API layer calculates outside `run_book()`.

## Release Targets

Provide both targets unless the user explicitly narrows scope:

```text
local web client: runs on the user's machine and opens in a browser
cloud Linux web service: runs behind gunicorn on a Linux server, optionally with nginx, systemd, or Docker
```

For a desktop installer, add Electron, Tauri, PyInstaller, or a native wrapper only when the user requests a true desktop client. Otherwise the local client is the same browser UI served locally.

## Production Web Minimum

The application must include:

```text
application factory such as create_app()
health endpoint for deployment smoke tests
thin API routes that call run_book()
explicit form_to_model and result_to_ui mapping
static/templates or SPA bundle needed by the browser UI
environment-based configuration
non-debug production defaults
structured error responses that preserve server logs
```

## Deployment Package Contents

Create or update:

```text
deploy/env.example
deploy/Dockerfile or deploy/systemd/*.service
deploy/nginx/*.conf when reverse proxy is expected
deploy/docker-compose.yml when Docker is used
release/release_checklist.md
release/runbook.md when operational handoff is needed
```

The release package must document:

```text
local run command
Linux production run command
required environment variables
port and host binding
data/output persistence paths
log location
backup/export strategy for inputs, results, reports, and packages
health check command
rollback or stop command
```

## Module Asset Requirements

Before release, confirm reusable calculation modules are asset-ready:

```text
each module has stable module_id and public function
inputs/options/results are typed
module owns formulas and lookup behavior only
module has no web, report, batch, file-system, or database dependency
source references and formula traces are recorded
unit and regression tests cover the module
reuse status is recorded in module_asset_registry.csv
```

## Linux Deployment Rules

For Linux server deployment:

```text
run with gunicorn or an equivalent production WSGI/ASGI server
bind the app service to an internal host/port unless intentionally exposed
put TLS, compression, and public routing in nginx or the platform proxy
read secrets from environment variables or server secret storage
write generated outputs only to configured data/output directories
make logs visible to journald, container logs, or configured log files
disable debug mode
```

## Smoke Tests

Run or define smoke tests for:

```text
python -m webapp.app or equivalent local start
GET /health
GET /
POST /api/calculate with a known input
report preview or export when present
Docker build/run or systemd command syntax when provided
artifact validation script
```

If the current environment cannot start Docker, systemd, or nginx, still validate file presence, command syntax where possible, and provide the exact unrun command plus the reason it was not executed.

## Required Final Response

Provide:

```text
release targets produced
local run command
cloud Linux deployment command
deployment files created or updated
module asset registry status
traceability and review evidence
smoke test results
remaining deployment assumptions
```
