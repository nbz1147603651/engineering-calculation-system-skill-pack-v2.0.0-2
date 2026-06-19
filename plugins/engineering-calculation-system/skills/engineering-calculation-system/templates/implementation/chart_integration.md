# Chart and Visualization Integration

Use this template to document the chart generation strategy for engineering calculation interfaces.

## Chart Generation Architecture

| Item | Selected value | Notes |
| --- | --- | --- |
| Chart library | matplotlib / plotly / D3.js | Server-side SVG generation |
| Output format | SVG string | Inline embeddable in HTML |
| i18n support | Bilingual SVG per chart | `{zh: svg_zh, en: svg_en}` dict |
| Delivery | Embedded in API response JSON | Via `result_to_ui()` converter |
| Frontend toggle | CSS class `.bi-zh` / `.bi-en` | JS hides/shows on language switch |

## Chart Inventory

| Chart ID | Name | Type | Data source | Trigger |
| --- | --- | --- | --- | --- |
| `chart_breakdown` | Result breakdown | horizontal bar | `BookResult.checks` | when > 1 check |
| `chart_stress` | Stress distribution | line (depth vs stress) | `SettlementResult.stress_profile` | when settlement exists |
| `chart_iz` | Influence factor Iz | line (depth vs Iz) | `SettlementResult.iz_profile` | when Iz method used |
| `chart_consol` | Consolidation curve | line (time vs U) | `ConsolidationResult` | when consolidation exists |
| `chart_soil` | Soil profile schematic | custom schematic | `SoilProfile.layers` | always available |
| `chart_util` | Utilization summary | horizontal bar | `BookResult.checks[*].utilization` | when > 1 check |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Chart Generation Pattern

```python
# src/<pkg>/report/charts.py
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO

def figure_to_svg(fig) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return buf.getvalue().decode("utf-8")

def plot_result_breakdown(checks: list, lang: str = "en") -> plt.Figure:
    """Horizontal bar chart of utilization for all checks."""
    fig, ax = plt.subplots(figsize=(8, 3))
    # ... plot logic using BookResult values only ...
    ax.set_xlabel("Utilization" if lang == "en" else "利用率")
    return fig
```

## Bilingual Chart Helper

```python
def _bilingual_svg(plot_fn, *args, **kwargs) -> dict | None:
    """Generate chart in both languages for i18n toggle."""
    try:
        fig_zh = plot_fn(*args, lang="zh", **kwargs)
        svg_zh = figure_to_svg(fig_zh)
        fig_en = plot_fn(*args, lang="en", **kwargs)
        svg_en = figure_to_svg(fig_en)
        return {"zh": svg_zh, "en": svg_en}
    except Exception:
        return None
```

## Frontend Rendering Pattern

```html
<!-- In results.js or result template -->
<div class="chart-container">
    <div class="bi-zh" style="display:none">{{ chart_svg_zh | safe }}</div>
    <div class="bi-en">{{ chart_svg_en | safe }}</div>
</div>
```

## Color and Style Conventions

| Element | Color | Notes |
| --- | --- | --- |
| PASS status | `#198754` (Bootstrap success green) | Utilization < 1.0 |
| FAIL status | `#dc3545` (Bootstrap danger red) | Utilization >= 1.0 |
| WARNING | `#ffc107` (Bootstrap warning amber) | Near limit |
| Utilization bar < 0.7 | green fill | Safe |
| Utilization bar 0.7–1.0 | amber fill | Caution |
| Utilization bar >= 1.0 | red fill | Fail |

## Rules

```text
charts visualize BookResult values — they must not compute engineering results
label all axes with units
keep SVG output under 50KB per chart
use matplotlib Agg backend for server-side rendering
close all figures after SVG export to prevent memory leaks
provide chart data as structured dicts alongside SVG for accessibility and testing
```
