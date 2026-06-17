# Cloud Linux Deployment Plan

Use this template for production deployment of an engineering calculation web application.

## Runtime Target

| Item | Selected Value | Notes |
| --- | --- | --- |
| Application entrypoint | `webapp.app:create_app()` | Must call the same `run_book()` path as local/API/batch. |
| Server | gunicorn / uvicorn / platform WSGI-ASGI server | Use production server, not Flask debug server. |
| Reverse proxy | nginx / platform proxy / none | Required when exposing to public internet. |
| Host binding | `127.0.0.1` behind proxy or `0.0.0.0` in container | Avoid unintended exposure. |
| Port | to_be_defined | Record firewall and proxy routing. |
| OS | Linux | Record distro/version when known. |

## Required Files

```text
deploy/env.example
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

## Deployment Sequence

```text
prepare Linux host or container runtime
copy release package or pull repository
create virtualenv or build container image
install dependencies
configure environment variables
start gunicorn service
configure nginx or platform proxy when public
run health check
run known POST /api/calculate smoke case
record release status
```

## Health and Smoke Tests

```text
curl -fsS http://127.0.0.1:5000/health
curl -fsS http://127.0.0.1:5000/
curl -fsS -X POST http://127.0.0.1:5000/api/calculate \
  -H "Content-Type: application/json" \
  --data @tests/smoke/example_input.json
```

## Production Rules

```text
debug mode disabled
secrets not committed
logs routed to journald, container logs, or configured log path
generated outputs written to configured persistent directory
calculation modules remain independent from web/deploy layers
deployment smoke test result recorded in release/release_checklist.md
```
