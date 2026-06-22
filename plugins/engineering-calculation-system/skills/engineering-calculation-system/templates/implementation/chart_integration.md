# Chart and Visualization Integration

Use this template to document how engineering charts are produced, placed, and verified.

## Principle

Charts are part of the calculation result contract. Build chart specifications from
already-computed `BookResult` values in the book layer, then let the UI and report renderers
display those specifications. Chart selection must be generic and metadata-driven: inspect the
book's `result_path_registry`, `ReportContext`, review needs, and available result arrays/groups.
Do not hardcode a universal chart set, chart IDs, result paths, or domain-specific labels across
books. Include concise reviewer-useful charts when chartable data exists; otherwise record charts
as not applicable.

Charts must not compute engineering results, recalculate utilization, override status, choose design branches, perform official unit conversion, or suppress warnings/errors.

## Recommended Architecture

| Item | Selected value | Notes |
| --- | --- | --- |
| Chart contract | `BookResult.charts: list[ChartSpec]` | Stable data passed to UI, report, and export paths |
| Builder location | `src/<pkg>/books/<book_name>/charts.py` | Uses `CheckResult`, module results, and stable result paths only |
| UI placement | `recommended_ui_location` | Example: `after_governing_summary`, `before_checks`, `result_detail` |
| Report placement | `recommended_report_location` | Example: `after_input_summary`, `after_governing_summary`, `appendix` |
| Renderer | inline SVG / matplotlib SVG / Plotly / D3 | Renderer consumes ChartSpec values only |
| Accessibility | chart data table alongside visual | Required for review, testing, and non-visual export |
| Source trace | `source_result_paths` and per-series `result_paths` | Makes every chart value auditable |

## ChartSpec Fields

```python
@dataclass(frozen=True)
class ChartAxis:
    label: str
    unit: str | None = None


@dataclass(frozen=True)
class ChartSeries:
    label: str
    values: list[float | None]
    unit: str | None = None
    result_paths: list[str] = field(default_factory=list)
    color: str | None = None


@dataclass(frozen=True)
class ChartThreshold:
    label: str
    value: float
    unit: str | None = None
    source_result_path: str | None = None


@dataclass(frozen=True)
class ChartSpec:
    chart_id: str
    title: str
    chart_type: str
    purpose: str
    categories: list[str]
    series: list[ChartSeries]
    x_axis: ChartAxis
    y_axis: ChartAxis
    recommended_ui_location: str = "after_governing_summary"
    recommended_report_location: str = "after_input_summary"
    thresholds: list[ChartThreshold] = field(default_factory=list)
    source_result_paths: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
```

## Chart Candidate Inventory

This table is a project-specific decision record, not a global required chart list. Replace the
example rows with chart candidates derived from the current book.

| Chart ID | Name | Type | Data source | Trigger | Placement |
| --- | --- | --- | --- | --- | --- |
| `example_check_metric_summary` | Example check metric summary | bar | project-specific check metric path | repeated comparable metric exists | after governing/input summary |
| `example_pair_comparison` | Example paired result comparison | grouped_bar | project-specific paired paths | two comparable values share categories/units | before detail table |
| `example_profile` | Example profile or series | line | project-specific sequence/profile path | ordered numeric sequence exists | result detail or appendix |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

Recommended workflow: list candidate result paths, decide whether each would help engineering
review, and either emit a `ChartSpec` or record why it is not applicable. Common chart families
include comparable metrics, paired values, profiles, envelopes, distributions, or schematics, but
the actual charts must come from the current book's result data and stable paths.

## Builder Pattern

```python
# src/<pkg>/books/<book_name>/charts.py
from .book_models import BookResult, ChartAxis, ChartSeries, ChartSpec
from .result_path_registry import chart_candidates, resolve_result_path


def build_book_charts(result: BookResult) -> list[ChartSpec]:
    charts = []
    for candidate in chart_candidates():
        values = [
            resolve_result_path(result, result_path)
            for result_path in candidate.result_paths
        ]
        if not any(value is not None for value in values):
            continue

        charts.append(
            ChartSpec(
                chart_id=candidate.chart_id,
                title=candidate.title,
                chart_type=candidate.chart_type,
                purpose=candidate.purpose,
                categories=candidate.categories,
                series=[
                    ChartSeries(
                        label=candidate.series_label,
                        values=values,
                        unit=candidate.unit,
                        result_paths=candidate.result_paths,
                    )
                ],
                x_axis=ChartAxis(label=candidate.x_axis_label),
                y_axis=ChartAxis(label=candidate.y_axis_label, unit=candidate.unit),
                source_result_paths=candidate.result_paths,
            )
        )
    return charts
```

## Interface Rendering Pattern

```text
BookInput
-> run_book(BookInput)
-> BookResult(checks, governing, charts, warnings, errors)
-> result_to_ui() includes charts unchanged except JSON sanitization
-> results.js renders ChartSpec and a data table
```

The frontend may calculate SVG coordinates, bar widths, labels, and layout geometry. It must not calculate engineering outcomes, utilization, capacity, branch choice, or status.

## Report Rendering Pattern

```text
trusted BookResult
-> build_report_context() includes charts
-> HTML/LaTeX renderer displays chart visual and/or chart data table
-> chart section appears after governing/input summary and before detailed checks unless handoff overrides it
```

HTML can render inline SVG from `ChartSpec`. LaTeX/Overleaf exports should at minimum include the chart title, purpose, values, units, source result paths, thresholds, and placement notes. If graphic LaTeX charts are added, they must still consume `ChartSpec` values only.
For A4 HTML reports, render chart visuals in print-safe inline SVG and always include a data table
below the visual so printed copies remain auditable without interactive tooltips.

## Color and Style Conventions

| Element | Color | Notes |
| --- | --- | --- |
| Primary series | `#2563eb` | Main utilization or response |
| Capacity/pass reference | `#16a34a` | Display only |
| Demand/fail reference | `#dc2626` | Display only |
| Threshold line | `#ef4444` dashed | Use only when threshold is recorded in result data |
| Warning/caution | `#f59e0b` | Display only |

## Verification Rules

```text
unit/integration tests cover ChartSpec builders
API smoke tests assert "charts" is present
report smoke tests assert chart section is present when chart specs exist
report smoke tests assert A4 HTML includes chart data tables and source result paths when charts are emitted
frontend shell tests assert chartsSection exists
chart data includes source result paths
no UI/report template computes engineering formulas, utilization, or status
non-finite chart values are sanitized before JSON output
```
