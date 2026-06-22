# Qoder Quickstart

This is the short operator guide for the Engineering Calculation System in Qoder.

## Qoder Package Self-Check

Classify the current install before doing implementation or release work:

| Shape | Present files | What it can do |
| --- | --- | --- |
| Direct QODER Skill | `SKILL.md`, `reference.md`, `qoder_quickstart.md`, `assets/lifecycle-console.html` | Route, explain gates, guide work. Do not claim `web-complete` from this shape alone. |
| QODER Project overlay | `.qoder/agents/engineering-calc-system.md`, `.qoder/skills/engineering-calc-system/`, `.qoder/references/engineering-calc-system.md` | Agent-first supervision with worker agents and skill resources. |
| Complete core project | `SKILL.md`, `skills/`, `shared/`, `templates/`, `schemas/`, `scripts/validate_artifacts.py`, `project_template/` | Full source-backed implementation, validation, report, web, batch, and deployment closure. |

If the task asks for a deployable online calculator or `web-complete`, use the QODER Project package together with the complete core package. If only the direct skill is installed, label outputs as guidance, draft, or prototype until the core validator can run.

## First Prompt To Qoder

Use the supervisor agent when it exists:

```text
Use .qoder/agents/engineering-calc-system.md as supervisor. Classify the material state, delivery mode, required lifecycle path, gate status, and next artifacts before editing code.
```

For direct skill import only:

```text
Use the Engineering Calculation System skill as a lightweight router. Tell me whether my current files are enough for web-complete, and list the missing core package artifacts before implementation.
```

## Validation Commands

From a complete core skill root:

```bash
python scripts/validate_artifacts.py --package-root . --profile core
python scripts/validate_artifacts.py --package-root . --profile core --project <project-root> --delivery web-complete
```

From this repository source checkout:

```bash
python tools/build_release.py --profile qoder-addon
python core/engineering-calculation-system/scripts/validate_artifacts.py --package-root dist/qoder-addon --profile qoder-addon
python tools/install_qoder_user.py --audit
```

## Agent Routing

The supervisor keeps these decisions serial: lifecycle route, evidence gate, source authority, ID allocation, handoff freeze, `run_book(BookInput) -> BookResult`, production label, and release acceptance.

Delegate only bounded work to workers:

- `engineering-calc-reference-acquirer`: phases 01-03
- `engineering-calc-source-intake`: phase 04
- `engineering-calc-logic-extractor`: phases 05-07 draft artifacts
- `engineering-calc-module-worker`: phases 08-11 owned implementation slices
- `engineering-calc-interface-worker`: 12/12a/12b/12c thin interfaces
- `engineering-calc-verification-worker`: phase 13 checks
- `engineering-calc-release-worker`: phase 14 deployment artifacts

## Completion Bar

Do not say complete, production-ready, deployable, or `web-complete` unless:

- `shared/lifecycle.md` has been applied
- `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow production
- real input creates non-empty evaluated `BookResult.checks`
- API/UI, report, import/export, batch, deployment artifacts, and smoke tests exist
- `validate_artifacts.py --delivery web-complete` passes
