# Cloud Linux Deployment Plan

Use this template for production deployment of an engineering calculation web application.

## Runtime Target

| Item | Selected Value | Notes |
| --- | --- | --- |
| Primary runtime | Python >=3.9 | Default calculation and web runtime. |
| Application entrypoint | `webapp.app:create_app()` | Must call the same `run_book()` path as local/API/batch. |
| Server | gunicorn / uvicorn / platform WSGI-ASGI server | Use production server, not Flask debug server. |
| Frontend format | Jinja2 + Bootstrap 5 + vanilla JavaScript modules | Served from `webapp/templates` and `webapp/static`. |
| Reverse proxy | nginx / platform proxy / none | Required when exposing to public internet. |
| Host binding | `127.0.0.1` behind proxy or `0.0.0.0` in container | Avoid unintended exposure. |
| Port | to_be_defined | Record firewall and proxy routing. |
| Flask admin shell | `/admin/` | Password-gated setup and launch page. |
| Marimo review | `/admin/review/` | Separate service behind the same domain when admin review is enabled. |
| Formula publisher | `/admin/formulas/` | Separate Marimo service for declaration-based formula registry publishing. |
| OS | Linux | Record distro/version when known. |

## Required Files

```text
deploy/env.example
deploy/one_click_deploy.sh
deploy/Dockerfile or deploy/systemd/<service>.service
deploy/nginx/<site>.conf when nginx is used
deploy/docker-compose.yml when Docker is used
release/release_checklist.md
```

## Environment Variables

| Variable | Required | Example | Purpose |
| --- | --- | --- | --- |
| `APP_HOST` | true | `0.0.0.0` | Service bind host. |
| `APP_PORT` | true | `5000` | Service bind port. |
| `FLASK_DEBUG` | true | `0` | Must be `0` in production. |
| `SECRET_KEY` | true | server secret | Never commit real production secret. |
| `DATA_DIR` | false | `/var/lib/engineering-calc/data` | Persistent inputs/imports. |
| `OUTPUT_DIR` | false | `/var/lib/engineering-calc/outputs` | Persistent results/reports/packages. |
| `FORMULA_REGISTRY_DIR` | when formula registry used | `/app/data/formula_registry` | Shared active formula versions. |
| `FORMULA_PUBLISH_LOG` | when formula registry used | `/app/outputs/logs/formula_publish_log.csv` | Admin publish audit log. |
| `MARIMO_BASE_URL` | when Marimo admin used | `/admin/review` | Reverse-proxied admin route. |
| `MARIMO_PORT` | when Marimo admin used | `2718` | Marimo service port. |
| `FORMULA_ADMIN_BASE_URL` | when formula publisher used | `/admin/formulas` | Reverse-proxied formula admin route. |
| `FORMULA_ADMIN_PORT` | when formula publisher used | `2719` | Formula admin service port. |
| `ADMIN_REVIEW_PASSWORD` | when admin shell used | server secret | Password for entering the Flask admin shell. |
| `ADMIN_REVIEW_TOKEN` | when Marimo admin used | server secret | Token/password for Marimo review and formula services. |

## Deployment Sequence

```text
prepare Linux host or container runtime
copy release package or pull repository
create virtualenv or build container image
install dependencies
configure environment variables
run bash deploy/one_click_deploy.sh when using the scaffolded one-click path
start gunicorn service
start marimo run calculation review service when enabled
start marimo run formula publisher service when enabled
configure nginx or platform proxy when public
run health check
run known POST /api/calculate smoke case
run /admin/ smoke check for the Flask admin shell
run /admin/review/ smoke check when Marimo admin is enabled
run /admin/formulas/ smoke check when formula publisher is enabled
record release status
```

## Health and Smoke Tests

```text
curl -fsS http://127.0.0.1:5000/health
curl -fsS http://127.0.0.1:5000/
curl -fsS -X POST http://127.0.0.1:5000/api/calculate \
  -H "Content-Type: application/json" \
  --data @tests/smoke/example_input.json
curl -fsS http://127.0.0.1:2718/ # or proxied /admin/review/ when Marimo admin is enabled
curl -fsS http://127.0.0.1:2719/ # or proxied /admin/formulas/ when formula publisher is enabled
```

## Production Rules

```text
debug mode disabled
secrets not committed
logs routed to journald, container logs, or configured log path
generated outputs written to configured persistent directory
formula registry shared between web and Marimo services when admin review is enabled
Flask admin shell protected by ADMIN_REVIEW_PASSWORD
Marimo admin protected by ADMIN_REVIEW_TOKEN, localhost service binding, and HTTPS reverse proxy
calculation modules remain independent from web/deploy layers
deployment smoke test result recorded in release/release_checklist.md
```
