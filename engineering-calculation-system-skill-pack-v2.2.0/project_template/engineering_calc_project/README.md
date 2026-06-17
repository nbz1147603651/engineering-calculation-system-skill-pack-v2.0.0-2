# Engineering Calculation Project Scaffold

This scaffold supports the full v2 lifecycle:

```text
references -> analysis -> handoff -> implementation -> src -> tests -> deploy -> release
```

Start with `references/acquisition/` when materials are missing or insufficient.

## Validate

From this directory:

```bash
python3 -m pytest -q
```

## Run Locally

```bash
python3 -m pip install "flask>=3.0" "gunicorn>=21.2"
python3 -m webapp.app
```

Health check:

```bash
curl -fsS http://127.0.0.1:5000/health
```

## Deploy on Linux

Docker path:

```bash
docker compose -f deploy/docker-compose.yml up --build
```

systemd/gunicorn path:

```bash
gunicorn "webapp.app:create_app()" --bind 127.0.0.1:5000 --workers 2
```

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```
