# Installation

For Codex-compatible environments, install the package root so `SKILL.md` is discoverable.

At minimum, copy these files and directories into the target skill environment:

```text
SKILL.md
agents/
adapters/
parent/
skills/
shared/
templates/
schemas/
scripts/
```

Optional directories:

```text
project_template/
examples/
workflow_diagrams/
original_sources/
```

If the target environment cannot reliably coordinate multiple skill files, load the single merged file:

```text
engineering-calculation-system.all-in-one.md
```

## Validate installation

Run:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

If using the included project scaffold, run:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
cd project_template/engineering_calc_project
python3 -m pytest -q
```

## Recommended usage

For a complete engineering calculation software project, start with the router:

```text
skills/00-engineering-calculation-router.skill.md
```

For no-material or insufficient-material cases, use:

```text
parent/engineering-calculation-reference-acquisition.skill.md
```

For reference-to-blueprint analysis, use:

```text
parent/engineering-calculation-logic-architecture.skill.md
```

For implementation, use:

```text
parent/engineering-calculation-book.skill.md
```
