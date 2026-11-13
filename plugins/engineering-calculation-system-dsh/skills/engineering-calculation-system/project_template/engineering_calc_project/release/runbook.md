# Engineering Calculation Release Runbook

## Scope

This runbook covers the generated web-complete calculator:

- Flask/gunicorn main web app at `/`
- Calculation APIs that call `run_book(BookInput) -> BookResult`
- A4 HTML / LaTeX calculation-book preview and export APIs
- Password-gated admin shell at `/admin/`
- Marimo calculation review service at `/admin/review/`
- Marimo formula publishing service at `/admin/formulas/`

## Required Environment

Copy `deploy/env.example` to `deploy/.env` before production deployment and set:

```text
SECRET_KEY
ADMIN_REVIEW_PASSWORD
ADMIN_REVIEW_TOKEN
DATA_DIR
OUTPUT_DIR
FORMULA_REGISTRY_DIR
```

`ADMIN_REVIEW_PASSWORD` protects the Flask admin shell. `ADMIN_REVIEW_TOKEN` protects
the Marimo services. If Marimo is not installed, the main calculator still runs and
the admin page displays the install prompt.

## One-Click Deployment

From the project root:

```bash
bash deploy/one_click_deploy.sh
```

Modes:

```bash
bash deploy/one_click_deploy.sh auto
bash deploy/one_click_deploy.sh compose
bash deploy/one_click_deploy.sh local
```

`auto` uses Docker Compose when available and falls back to a local Python virtual
environment plus gunicorn. Local mode writes process IDs and logs under
`outputs/logs/`.

## Smoke Checks

```bash
curl -fsS http://127.0.0.1:5000/health
curl -fsS http://127.0.0.1:5000/api/capabilities
curl -fsS http://127.0.0.1:5000/admin/
```

Run the project tests:

```bash
python -B -m pytest -q -p no:cacheprovider
```

Run skill-pack validation from the skill root:

```bash
python scripts/validate_artifacts.py --package-root . --profile core --project project_template/engineering_calc_project --delivery web-complete
```

## Formula Publishing Effect

Formula changes are declaration-based. A publish through `apps/review/admin_formula_review.py`
must validate the rule, run the `run_book()` smoke check, write the versioned rule,
update `data/formula_registry/active_versions.yaml`, and append
`outputs/logs/formula_publish_log.csv`.

The next `/api/calculate` request loads the active formula registry metadata. The
interactive UI displays the active formula version, hash, and publish timestamp in
the result status strip.

## Stop and Rollback

Docker Compose:

```bash
cd deploy
docker compose down
```

Local mode:

```bash
kill "$(cat outputs/logs/web.pid)"
test -f outputs/logs/marimo-review.pid && kill "$(cat outputs/logs/marimo-review.pid)"
test -f outputs/logs/marimo-formula-admin.pid && kill "$(cat outputs/logs/marimo-formula-admin.pid)"
```

Rollback formula changes by restoring the previous entry in
`data/formula_registry/active_versions.yaml` and rerunning the smoke checks.
