# Formula Trace Specification

Each source-backed formula result should expose:

| Field | Meaning |
| --- | --- |
| formula_id | stable ID from `formula_inventory.csv` |
| formula_name | human-readable formula or method name |
| source_reference | source ID plus clause/table/equation/page |
| expression_tex | TeX expression for display; sourced from formula inventory/registry |
| expression_plain | plain-text fallback expression |
| engineering_explanation | short reviewer-facing explanation of the calculation purpose |
| variable_definitions | symbol-to-meaning map, including units where helpful |
| inputs | values used by the formula |
| substitutions | display-ready substitution values, if different from raw inputs |
| intermediates | audit values needed for review |
| result_symbol | engineering symbol |
| result_value | computed value |
| unit | result unit |
| result_path | stable `BookResult` path for UI/report references |
| display_icon | design-system icon for the check family |
| notes | warnings, assumptions, or implementation comments |

Presentation layers may render these fields but must not hardcode domain formulas or recalculate values. See `calculation_review_card_spec.md`.
