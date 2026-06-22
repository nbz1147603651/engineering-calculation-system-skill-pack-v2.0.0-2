# UI Design System Contract

Use this contract whenever generating or modifying the production web UI for an engineering calculation book.

## Purpose

Reduce UI randomness by keeping the layout, tokens, and reusable component patterns stable across books. Vary only the engineering fields, result sections, charts, and trace content.

## Required Asset Shape

```text
webapp/templates/base.html
webapp/templates/index.html
webapp/templates/partials/_topbar.html
webapp/templates/partials/_report_modal.html
webapp/static/css/tokens.css
webapp/static/css/components.css
webapp/static/css/style.css
webapp/static/js/i18n.js
webapp/static/js/forms.js
webapp/static/js/results.js
webapp/static/js/main.js
```

## Low-Freedom Rules

- Keep the global page zones fixed: top bar, left input panel, right review workbench, modal/drawer, status strip.
- Keep import/export/report/language actions in the top bar.
- Keep a visible review-admin entry in the top bar; it creates a review session and opens
  the password-gated `/admin/` shell, which can launch the token-protected Marimo services.
- Keep `tokens.css` as the only color, radius, spacing, and shadow token layer.
- Keep reusable structure in `components.css`.
- Use `style.css` only for book-specific additive styles.
- Use Bootstrap utility classes only for local spacing, responsive grids, and simple alignment.
- Do not create a landing page, marketing hero, unrelated dashboard layout, or decorative theme.
- Do not introduce a frontend framework unless the handoff records a justified stack change.
- Do not calculate engineering values in templates or JavaScript.
- Render calculation formulas, explanations, substitutions, and source references through
  `calculation_review_card_spec.md`; do not hardcode domain formulas in UI files.

## Component Patterns

| Component | Required behavior | Files |
| --- | --- | --- |
| Top bar | project/book title, import/export, A4 HTML final report download, report preview, LaTeX template selector/export, language switch | `_topbar.html`, `main.js`, `i18n.py` |
| Review admin entry | create review session, open `/admin/`, surface missing Marimo/password/token setup | `_topbar.html`, `results.js`, `admin_review.html` |
| Input card | grouped BookInput fields, units, inline validation, conditional visibility | `index.html`, `forms.js` |
| Result card | conclusion first, status badge, trace expansion, stable result path | `index.html`, `results.js` |
| Calculation review card | check icon, engineering explanation, formula box, variable/substitution tables, result path, source reference | `results.js`, `components.css` |
| Status strip | input hash, result hash, runner version, template version, package id, timestamp | `index.html`, `results.js` |
| Report modal | preview frame and renderer-specific downloads | `_report_modal.html`, `main.js` |

## Field-Driven Generation

Prefer generating input and result sections from:

```text
templates/implementation/frontend_fields.csv
templates/implementation/review_schema.csv
templates/implementation/result_path_registry.csv
```

When adding a field, record the field path, label, unit, group, editability, source, and validation note. When adding a result card, record the BookResult path, purpose, display values, trace visibility, report visibility, Marimo review section, and display icon. Do not put project-specific icon or label mappings directly in JavaScript.

## Visual Guardrails

- Use a restrained operational palette from `tokens.css`. Default to the ZJIC-style
  engineering portal tokens unless a project design overrides them: white surfaces,
  `#005EB8` primary blue, `#003087` dark blue, `#FFB81C` warm action/focus color,
  pale blue information panels, compact 2-4px radii, and no decorative gradients.
- Keep cards to individual input/result/review units only.
- Keep compact tables for comparable checks.
- Use metric boxes for headline values.
- Keep warnings and errors visible and textual, not color-only.
- Keep long formula traces behind expansion or a drawer, but each production check must expose a
  readable formula card with icon, explanation, source, expression, variables, substitutions, and
  stable result path.
- On mobile, stack input first, governing summary second, result details third.

## Validation Targets

The project validator should require:

```text
tokens.css
components.css
partials/_topbar.html
partials/_report_modal.html
id="langToggle"
id="latexTemplateSelect"
id="btnDownloadLatex"
id="btnAdminReview"
/admin/
/admin/review/
ADMIN_REVIEW_PASSWORD
GET /api/report/templates
/api/report/latex
/api/report/decision
/api/report/final
latex_template_id
calculation_review_card_spec.md
formula-box
review-icon
expression_tex
result_path
```

Treat missing UI kit files as a `prototype` or `incomplete` delivery.
