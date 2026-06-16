# Formula Trace Specification

Each source-backed formula result should expose:

| Field | Meaning |
| --- | --- |
| formula_id | stable ID from `formula_inventory.csv` |
| formula_name | human-readable formula or method name |
| source_reference | source ID plus clause/table/equation/page |
| inputs | values used by the formula |
| intermediates | audit values needed for review |
| result_symbol | engineering symbol |
| result_value | computed value |
| unit | result unit |
| notes | warnings, assumptions, or implementation comments |

