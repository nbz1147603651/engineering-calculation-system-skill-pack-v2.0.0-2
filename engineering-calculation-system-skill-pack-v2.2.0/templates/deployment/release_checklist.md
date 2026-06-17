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
- [ ] Calculation modules are decoupled and listed in `module_asset_registry.csv`.
- [ ] Official calculation path is `run_book(BookInput) -> BookResult`.
- [ ] Web/API/report/batch layers do not implement formulas or independent pass/fail logic.
- [ ] Unit, regression, integration, interface, and smoke tests pass or blockers are recorded.
- [ ] Traceability metadata includes source basis, input hash, result hash, runner version, and report/template version when present.
- [ ] Local web client run command is documented and tested.
- [ ] Cloud Linux deployment files are present.
- [ ] `/health` endpoint passes.
- [ ] `POST /api/calculate` smoke test passes with known input.
- [ ] Production debug mode is disabled.
- [ ] Secrets are environment-based and not committed.
- [ ] Data and output persistence paths are documented.

## Release Artifacts

| Artifact | Path | Required | Status |
| --- | --- | --- | --- |
| Local run instructions | README.md | true | to_be_defined |
| Environment example | deploy/env.example | true | to_be_defined |
| Dockerfile | deploy/Dockerfile | Docker path | to_be_defined |
| systemd service | deploy/systemd/*.service | systemd path | to_be_defined |
| nginx site config | deploy/nginx/*.conf | public Linux path | to_be_defined |
| Release runbook | release/runbook.md | when operational handoff needed | to_be_defined |
| Acceptance checklist | verification/acceptance_checklist.md | true | to_be_defined |

## Smoke Test Record

| Test | Command | Result | Notes |
| --- | --- | --- | --- |
| Local app start | `python -m webapp.app` | to_be_defined |  |
| Health | `curl -fsS http://127.0.0.1:5000/health` | to_be_defined |  |
| Main page | `curl -fsS http://127.0.0.1:5000/` | to_be_defined |  |
| Calculate API | `curl -fsS -X POST ... /api/calculate` | to_be_defined |  |
| Docker build | `docker build -f deploy/Dockerfile .` | to_be_defined |  |

## Remaining Assumptions

| Assumption | Risk | Owner | Resolution |
| --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined |
