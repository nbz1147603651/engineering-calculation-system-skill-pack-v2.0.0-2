# Marimo Frontend Bridge Specification

Use this contract when a production web calculator needs Python-native review that stays connected to the browser UI.

## Goal

The browser creates review sessions; Marimo reviews them. The web page remains a thin interface over `run_book()`, while Marimo provides live Python cells for engineering review, draft investigation, trace inspection, and review decisions.

## Required Flow

```text
frontend form data
-> POST /api/review/session
-> build BookInput
-> run_book(BookInput)
-> build ReportContext
-> save outputs/review/sessions/<session_id>/{input,result,report_context,review_state}.json
-> open /admin/review/?session_id=<session_id>
-> Marimo reads the session and appends review decisions
```

## Required Artifacts

```text
src/<pkg>/review/bridge.py
apps/review/calculation_review.py
outputs/review/.gitkeep
webapp/routes.py              # /api/review/session and /api/review/state/<session_id>
webapp/static/js/main.js      # button creates a session before opening Marimo
```

## Bridge Data

The session folder must contain:

| File | Purpose |
| --- | --- |
| `input.json` | Plain `BookInput` used for the official run |
| `result.json` | Plain `BookResult` including checks, charts, warnings, errors, formula traces |
| `report_context.json` | Report context built from trusted results |
| `review_state.json` | Session status and latest review decision |

Review decisions should append to:

```text
outputs/review/review_decisions.jsonl
```

## Marimo Responsibilities

- Load saved sessions and display governing summary, checks, warnings/errors, and FormulaTrace cards.
- Allow draft Python investigation in `marimo edit` during engineering development.
- Save reviewer decision and notes without overwriting final inputs or production formula selections.
- Keep draft edits labeled as draft/review/prototype until implemented in source modules and rerun through official verification.
- Use `marimo run` behind `/admin/review/` for controlled deployed review.

## Boundaries

- Frontend does not calculate engineering values or perform review decisions.
- Marimo review sessions do not silently mutate production inputs, active formula registry versions, or report templates.
- Formula rule publishing remains a separate declaration-based admin flow that validates declarations, runs smoke tests, and updates `active_versions.yaml` only after success.
- Quarto may be used only as a reference for readable presentation patterns; it is not the review runtime or required dependency.
