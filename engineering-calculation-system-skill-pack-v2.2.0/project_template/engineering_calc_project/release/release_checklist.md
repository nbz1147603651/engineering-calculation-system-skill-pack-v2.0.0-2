# Release Checklist

- [ ] Source basis and implementation handoff are recorded.
- [ ] Calculation modules are decoupled and listed in `implementation/02_modules/module_asset_registry.csv`.
- [ ] Official calculation path is `run_book(BookInput) -> BookResult`.
- [ ] Web/API/report/batch layers do not implement formulas.
- [ ] Unit, regression, integration, interface, and smoke tests pass or blockers are recorded.
- [ ] Local run command is tested: `python -m webapp.app`.
- [ ] Cloud Linux deployment files are present under `deploy/`.
- [ ] `/health` endpoint passes.
- [ ] `POST /api/calculate` smoke test passes with known input.
- [ ] Production debug mode is disabled.
- [ ] Secrets are environment-based and not committed.
- [ ] Data and output persistence paths are documented.
