# Unified UI Layout Specification

Use this template for production frontend, review UI, or app-like engineering calculation interfaces.

## Layout Decision

| Item | Selected value | Reason | Evidence |
| --- | --- | --- | --- |
| Interface family | production frontend / Marimo review / report preview / batch dashboard | to_be_defined | user request |
| Primary user | engineer / checker / approver / batch operator | to_be_defined | workflow |
| Data source | uploaded package / final_input.json / API / batch_control | to_be_defined | import contract |
| Calculation path | run_book(BookInput) -> BookResult | required | code |
| Report preview path | HTML / PDF / DOCX / other | to_be_defined | report context |

## Standard Page Zones

| Zone | Required content | Notes |
| --- | --- | --- |
| Top bar | project/book title, case selector, status, import, export, report preview | Keep actions predictable across projects. |
| Left input panel | collapsible BookInput groups, units, validation, sticky run/save controls | Do not place result logic here. |
| Right review workbench | governing summary, warnings/errors, result cards, charts, traces | Conclusion first, details below. |
| Modal/drawer | report preview, imported report preview, source trace, formula trace, package validation, diff | Use for deep review without losing context. |
| Status strip | input hash, result hash, runner version, report template version, package id, timestamp | Required for production review. |

## Input Card Pattern

| Card ID | BookInput group | Fields | Validation feedback | Conditional visibility | Notes |
| --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | inline / summary | to_be_defined |  |

## Result Card Pattern

| Card ID | BookResult path | Purpose | Displays | Trace expansion | Report visibility |
| --- | --- | --- | --- | --- | --- |
| governing | governing | conclusion first | status, governing check, utilization/margin | true | summary |
| warnings_errors | warnings/errors | review blockers | warnings, errors, unresolved assumptions | true | summary |

## Interaction States

| State | Required UI behavior |
| --- | --- |
| no_input | Show import/create options and disabled report export. |
| draft_input | Allow run, save draft, export draft package. |
| validation_error | Show field-level errors and keep run disabled or blocked. |
| calculation_error | Preserve input, show error, do not emit final output. |
| review_result | Show traces, warnings, export review package. |
| final_result | Require saved final input, trusted BookResult, verification evidence. |

## Visual Rules

- Keep the interface dense and work-focused.
- Put inputs on the left and results on the right for desktop layouts.
- On mobile, stack input first, then governing summary, then result details.
- Use clear status text in addition to color.
- Keep formulas and long traces behind expandable detail sections.
- Use tables for comparable engineering checks and compact metric boxes for headline values.
- Provide chart containers only when figures improve engineering review.

## Operator Convenience Decisions

| Workflow Need | Required Decision | Notes |
| --- | --- | --- |
| repeated data entry | keyboard-friendly forms / defaults / copy case / import package | optimize for engineers running many cases |
| review and approval | trace drawers / formula references / source references / comments | make checking faster and less error-prone |
| report production | preview / export / status labels / saved final input | prevent accidental finalization from draft data |
| batch or comparison work | import/export package / diff / saved BookResult JSON | keep results reproducible |
| complex interactions | keep default Jinja2 stack or upgrade to SPA | choose based on workflow quality, not minimalism |

## Frontend Stack Decision

| Item | Selected value | Reason |
| --- | --- | --- |
| Frontend format | Jinja2 + Bootstrap 5 + vanilla JavaScript modules | Default web format for this skill pack |
| Page model | server-rendered shell with API-driven interactions | Good default for maintainable engineering tools |
| Template engine | Jinja2 | Default; React/Vue is allowed when workflow complexity justifies it |
| CSS framework | Bootstrap 5 + `webapp/static/css/style.css` | Standard project scaffold |
| JS architecture | vanilla modules: `i18n.js`, `forms.js`, `results.js`, `main.js` | see `api_route_skeleton.md` |
| i18n strategy | data-i18n + `/api/i18n/<lang>` endpoint | see `i18n_pattern.md` |
| Chart library | matplotlib SVG / plotly / D3 | to_be_defined | see `chart_integration.md` |
| Formula rendering | KaTeX / MathJax / none | to_be_defined | for report preview |

## Frontend File Layout

```text
webapp/
  templates/
    base.html
    index.html
  static/
    css/style.css
    js/i18n.js
    js/forms.js
    js/results.js
    js/main.js
```

Do not introduce a separate SPA build directory, Node build step, or component framework by habit. Do introduce one when it clearly improves operator convenience, complex state handling, maintainability, or review quality, and record the decision in `frontend_format`.

## Deployment Entry

| Item | Selected value | Reason |
| --- | --- | --- |
| App factory | `webapp.app:create_app()` / other | Required for cloud runtime |
| Health endpoint | `/health` | Required for deployment smoke tests |
| Local run command | `python -m webapp.app` / other | Required for local client |
| Production run command | `gunicorn "webapp.app:create_app()" --bind 0.0.0.0:5000` / other | Required for Linux cloud |

## Related Templates

```text
form_mapping_spec.md    — form ↔ model bidirectional mapping
i18n_pattern.md         — internationalization strategy
chart_integration.md    — chart generation and embedding
api_route_skeleton.md   — Flask/FastAPI route architecture
```
