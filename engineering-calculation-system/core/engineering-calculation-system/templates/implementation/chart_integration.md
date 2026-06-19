# Chart and Visualization Integration

Use this template to document how engineering charts are produced, placed, and verified.

## Principle

Charts are part of the calculation result contract. Build chart specifications from already-computed `BookResult` values in the book layer, then let the UI and report renderers display those specifications.

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

## Chart Inventory

| Chart ID | Name | Type | Data source | Trigger | Placement |
| --- | --- | --- | --- | --- | --- |
| `check_utilization_summary` | Check utilization summary | bar | `BookResult.checks[*].utilization` | any check has utilization | after governing/input summary |
| `demand_capacity_comparison` | Demand and capacity comparison | grouped_bar | `BookResult.checks[*].demand/capacity` | demand and capacity are both present | before check table |
| `chart_stress_profile` | Stress distribution | line | module result profile values | settlement/stress profile exists | result detail or appendix |
| `chart_envelope` | Governing envelope | line/bar | envelope result paths | envelope values exist | after governing summary |
| `chart_soil_profile` | Soil profile schematic | schematic | normalized layer model | soil profile exists | input summary or appendix |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Builder Pattern

```python
# src/<pkg>/books/<book_name>/charts.py
from .book_models import BookResult, ChartAxis, ChartSeries, ChartSpec


def build_book_charts(result: BookResult) -> list[ChartSpec]:
    charts = []
    utilization_checks = [
        (index, check)
        for index, check in enumerate(result.checks)
        if check.utilization is not None
    ]
    if utilization_checks:
        charts.append(
            ChartSpec(
                chart_id="check_utilization_summary",
                title="Check Utilization Summary",
                chart_type="bar",
                purpose="Compare recorded utilization values across checks.",
                categories=[check.name for _, check in utilization_checks],
                series=[
                    ChartSeries(
                        label="Utilization",
                        values=[check.utilization for _, check in utilization_checks],
                        unit="ratio",
                        result_paths=[
                            f"checks[{index}].utilization"
                            for index, _ in utilization_checks
                        ],
                    )
                ],
                x_axis=ChartAxis(label="Check"),
                y_axis=ChartAxis(label="Utilization", unit="ratio"),
                source_result_paths=[
                    f"checks[{index}].utilization"
                    for index, _ in utilization_checks
                ],
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
frontend shell tests assert chartsSection exists
chart data includes source result paths
no UI/report template computes engineering formulas, utilization, or status
non-finite chart values are sanitized before JSON output
```
