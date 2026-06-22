# Admin Marimo Review Specification

Use this template for the embedded-admin Marimo formula-publishing surface deployed behind the main site. General calculation review uses `marimo_frontend_bridge_spec.md` and `apps/review/calculation_review.py`.

## Deployment Shape

```text
web app: /
Marimo admin app: /admin/review/
shared registry: data/formula_registry/
publish log: outputs/logs/formula_publish_log.csv
```

Run production review apps with `marimo run`, not `marimo edit`.

## Required Controls

The admin page should provide:

```text
module selector
active formula version display
declaration editor
validation result
publish notes
publish button disabled until validation passes
production effect notice
```

Protect access with:

```text
ADMIN_REVIEW_TOKEN
nginx HTTPS
optional internal network or VPN restriction
```

## Publish Rule

Saving a draft must not affect production. Publishing may update production only after:

```text
formula declaration validates
test cases pass
run_book smoke test passes
publish log row is written
active_versions.yaml is updated
```
