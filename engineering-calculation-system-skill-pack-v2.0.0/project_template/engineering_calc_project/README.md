# Engineering Calculation Project Scaffold

This scaffold supports the full v2 lifecycle:

```text
references -> analysis -> handoff -> implementation -> src -> tests -> outputs
```

Start with `references/acquisition/` when materials are missing or insufficient.

## Validate

From this directory:

```bash
python3 -m pytest -q
```

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```
