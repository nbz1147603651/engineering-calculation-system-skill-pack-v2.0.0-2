from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import math
from typing import Any

from .latex_renderer import report_assumptions_from_context, report_sources_from_checks, to_plain


def build_html_report_context(
    book_input: Any,
    book_result: Any,
    report_context: dict[str, Any] | None = None,
    *,
    lang: str = "en",
    report_status: str = "review",
    template_version: str = "default_html_a4_calcbook-v1",
) -> dict[str, Any]:
    """Build presentation-only HTML context from trusted calculation outputs."""
    plain_input = to_plain(book_input)
    plain_result = to_plain(book_result)
    plain_report = to_plain(report_context or {})
    charts = plain_report.get("charts") or plain_result.get("charts", [])
    checks = plain_result.get("checks", [])
    sources = plain_report.get("sources") or report_sources_from_checks(checks)
    assumptions = report_assumptions_from_context(plain_input, plain_report)
    return {
        "lang": lang,
        "report_status": report_status,
        "template_version": template_version,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "project": plain_result.get("project") or plain_input.get("project", {}),
        "input": plain_input,
        "result": plain_result,
        "report": plain_report,
        "governing": plain_result.get("governing", {}),
        "checks": checks,
        "charts": charts,
        "sources": sources,
        "assumptions": assumptions,
        "warnings": plain_result.get("warnings", []),
        "errors": plain_result.get("errors", []),
        "intermediate_values": plain_result.get("intermediate_values", {}),
        "traceability": {
            "formula_registry_version": plain_result.get("formula_registry_version", "unversioned"),
            "formula_hash": plain_result.get("formula_hash") or "untracked",
            "formula_published_at": plain_result.get("formula_published_at") or "not published",
            "report_template_version": template_version,
        },
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4g}"
    if isinstance(value, (list, tuple)):
        return ", ".join(_fmt(item) for item in value) or "-"
    if isinstance(value, dict):
        return "; ".join(f"{escape(str(key))}: {_fmt(item)}" for key, item in value.items()) or "-"
    return escape(str(value))


def _project_title(project: dict[str, Any]) -> str:
    return _fmt(project.get("title") or project.get("project_name") or project.get("project_id") or "Calculation Report")


def _kv_table(data: dict[str, Any], *, title: str) -> str:
    if not data:
        return f"<section class=\"report-section\"><h2>{escape(title)}</h2><p class=\"muted\">No data recorded.</p></section>"
    rows = "\n".join(
        f"<tr><th>{escape(str(key))}</th><td>{_fmt(value)}</td></tr>"
        for key, value in data.items()
    )
    return f"""
    <section class="report-section">
        <h2>{escape(title)}</h2>
        <table class="kv-table"><tbody>{rows}</tbody></table>
    </section>
    """


def _warnings_errors(warnings: list[Any], errors: list[Any]) -> str:
    warning_items = "".join(f"<li>{_fmt(item)}</li>" for item in warnings) or "<li>None</li>"
    error_items = "".join(f"<li>{_fmt(item)}</li>" for item in errors) or "<li>None</li>"
    return f"""
    <section class="report-section">
        <h2>Warnings and Errors</h2>
        <div class="two-col">
            <div><h3>Warnings</h3><ul>{warning_items}</ul></div>
            <div><h3>Errors</h3><ul>{error_items}</ul></div>
        </div>
    </section>
    """


def _sources_section(sources: list[dict[str, Any]]) -> str:
    if not sources:
        body = "<tr><td colspan=\"3\">No sources recorded.</td></tr>"
    else:
        body = "\n".join(
            "<tr>"
            f"<td>{_fmt(source.get('source_reference'))}</td>"
            f"<td>{_fmt(source.get('role'))}</td>"
            f"<td>{_fmt(source.get('used_in'))}</td>"
            "</tr>"
            for source in sources
        )
    return f"""
    <section class="report-section">
        <h2>Sources</h2>
        <table class="data-table">
            <thead><tr><th>Source</th><th>Role</th><th>Used In</th></tr></thead>
            <tbody>{body}</tbody>
        </table>
    </section>
    """


def _assumptions_section(assumptions: list[dict[str, Any]]) -> str:
    if not assumptions:
        body = "<tr><td colspan=\"4\">No assumptions recorded.</td></tr>"
    else:
        body = "\n".join(
            "<tr>"
            f"<td>{_fmt(item.get('assumption_id'))}</td>"
            f"<td>{_fmt(item.get('assumption'))}</td>"
            f"<td>{_fmt(item.get('source_reference'))}</td>"
            f"<td>{_fmt(item.get('program_handling'))}</td>"
            "</tr>"
            for item in assumptions
        )
    return f"""
    <section class="report-section">
        <h2>Assumptions</h2>
        <table class="data-table">
            <thead><tr><th>ID</th><th>Assumption</th><th>Source</th><th>Handling</th></tr></thead>
            <tbody>{body}</tbody>
        </table>
    </section>
    """


def _checks_table(checks: list[dict[str, Any]]) -> str:
    if not checks:
        body = "<tr><td colspan=\"8\">No checks recorded.</td></tr>"
    else:
        body = "\n".join(
            "<tr>"
            f"<td>{_fmt(check.get('check_id'))}</td>"
            f"<td>{_fmt(check.get('name'))}</td>"
            f"<td><span class=\"status status-{escape(str(check.get('status', '')).lower())}\">{_fmt(check.get('status'))}</span></td>"
            f"<td>{_fmt(check.get('demand'))}</td>"
            f"<td>{_fmt(check.get('capacity'))}</td>"
            f"<td>{_fmt(check.get('utilization'))}</td>"
            f"<td>{_fmt(check.get('limit'))}</td>"
            f"<td>{_fmt(check.get('unit'))}</td>"
            "</tr>"
            for check in checks
        )
    return f"""
    <section class="report-section">
        <h2>Calculation Checks</h2>
        <table class="data-table">
            <thead>
                <tr>
                    <th>ID</th><th>Check</th><th>Status</th><th>Demand</th>
                    <th>Capacity</th><th>Utilization</th><th>Limit</th><th>Unit</th>
                </tr>
            </thead>
            <tbody>{body}</tbody>
        </table>
    </section>
    """


def _as_finite_number(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _chart_value(chart: dict[str, Any], series: dict[str, Any], index: int) -> Any:
    values = series.get("values") or []
    if index >= len(values):
        return None
    return values[index]


def _chart_unit(chart: dict[str, Any], series: dict[str, Any]) -> str:
    axis = chart.get("y_axis") or {}
    return str(series.get("unit") or axis.get("unit") or "")


def _chart_max_value(chart: dict[str, Any]) -> float:
    values: list[float] = []
    for series in chart.get("series", []) or []:
        for value in series.get("values", []) or []:
            number = _as_finite_number(value)
            if number is not None:
                values.append(abs(number))
    for threshold in chart.get("thresholds", []) or []:
        number = _as_finite_number(threshold.get("value"))
        if number is not None:
            values.append(abs(number))
    return max(values) if values else 1.0


def _chart_svg(chart: dict[str, Any]) -> str:
    categories = chart.get("categories") or []
    series_list = chart.get("series") or []
    if not categories or not series_list:
        return ""

    palette = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#f59e0b"]
    left = 185
    top = 40
    plot_width = 430
    bar_height = 12
    series_gap = 5
    row_gap = 18
    series_count = max(1, len(series_list))
    row_height = series_count * (bar_height + series_gap) + row_gap
    width = 680
    height = top + len(categories) * row_height + 38
    scale = plot_width / _chart_max_value(chart)
    axis = chart.get("y_axis") or {}
    axis_label = _fmt(axis.get("label") or "Value")

    parts = [
        f'<svg class="chart-svg" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{_fmt(chart.get("title"))}">',
        f'<line x1="{left}" y1="{top - 8}" x2="{left}" y2="{height - 30}" stroke="#94a3b8" stroke-width="1" />',
        f'<line x1="{left}" y1="{height - 30}" x2="{left + plot_width}" y2="{height - 30}" stroke="#94a3b8" stroke-width="1" />',
    ]

    for threshold in chart.get("thresholds", []) or []:
        value = _as_finite_number(threshold.get("value"))
        if value is None:
            continue
        x = left + min(abs(value) * scale, plot_width)
        parts.append(
            f'<line x1="{x:.2f}" y1="{top - 12}" x2="{x:.2f}" y2="{height - 30}" '
            'stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 3" />'
        )
        parts.append(
            f'<text x="{x + 4:.2f}" y="{top - 18}" font-size="10" fill="#991b1b">'
            f'{_fmt(threshold.get("label"))}: {_fmt(threshold.get("value"))}</text>'
        )

    legend_x = left
    for index, series in enumerate(series_list):
        color = series.get("color") or palette[index % len(palette)]
        x = legend_x + index * 120
        parts.append(f'<rect x="{x}" y="8" width="10" height="10" fill="{escape(str(color))}" />')
        parts.append(
            f'<text x="{x + 15}" y="17" font-size="10" fill="#334155">'
            f'{_fmt(series.get("label"))}</text>'
        )

    for category_index, category in enumerate(categories):
        y0 = top + category_index * row_height
        label_y = y0 + (series_count * (bar_height + series_gap)) / 2
        parts.append(
            f'<text x="8" y="{label_y:.2f}" font-size="10" fill="#334155">'
            f'{_fmt(category)}</text>'
        )
        for series_index, series in enumerate(series_list):
            value = _as_finite_number(_chart_value(chart, series, category_index))
            if value is None:
                continue
            color = series.get("color") or palette[series_index % len(palette)]
            y = y0 + series_index * (bar_height + series_gap)
            bar_width = min(abs(value) * scale, plot_width)
            parts.append(
                f'<rect x="{left}" y="{y:.2f}" width="{bar_width:.2f}" '
                f'height="{bar_height}" rx="2" fill="{escape(str(color))}" />'
            )
            parts.append(
                f'<text x="{left + bar_width + 5:.2f}" y="{y + 10:.2f}" '
                'font-size="10" fill="#334155">'
                f'{_fmt(value)} {_fmt(_chart_unit(chart, series))}</text>'
            )

    parts.append(
        f'<text x="{left + plot_width / 2:.2f}" y="{height - 8}" '
        f'font-size="10" text-anchor="middle" fill="#475569">{axis_label}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def _chart_data_table(chart: dict[str, Any]) -> str:
    categories = chart.get("categories") or []
    series_list = chart.get("series") or []
    rows: list[str] = []
    for category_index, category in enumerate(categories):
        for series in series_list:
            paths = series.get("result_paths") or []
            path = paths[category_index] if category_index < len(paths) else ""
            rows.append(
                "<tr>"
                f"<td>{_fmt(category)}</td>"
                f"<td>{_fmt(series.get('label'))}</td>"
                f"<td>{_fmt(_chart_value(chart, series, category_index))}</td>"
                f"<td>{_fmt(_chart_unit(chart, series))}</td>"
                f"<td>{_fmt(path)}</td>"
                "</tr>"
            )
    body = "\n".join(rows) or "<tr><td colspan=\"5\">No chart data recorded.</td></tr>"
    return f"""
    <table class="data-table chart-data">
        <thead>
            <tr><th>Category</th><th>Series</th><th>Value</th><th>Unit</th><th>Result Path</th></tr>
        </thead>
        <tbody>{body}</tbody>
    </table>
    """


def _engineering_charts(charts: list[dict[str, Any]]) -> str:
    if not charts:
        return """
        <section class="report-section">
            <h2>Engineering Charts</h2>
            <p class="muted">No chart specifications were exposed in the BookResult.</p>
        </section>
        """

    cards: list[str] = []
    for chart in charts:
        source_paths = chart.get("source_result_paths") or []
        notes = chart.get("notes") or []
        note_items = "".join(f"<li>{_fmt(note)}</li>" for note in notes)
        note_block = f"<ul class=\"chart-notes\">{note_items}</ul>" if note_items else ""
        source_text = ", ".join(str(path) for path in source_paths) or "not recorded"
        cards.append(
            f"""
            <article class="chart-card">
                <h3>{_fmt(chart.get('title'))}</h3>
                <p class="section-note">{_fmt(chart.get('purpose'))}</p>
                {_chart_svg(chart)}
                {_chart_data_table(chart)}
                <p class="chart-meta"><strong>Recommended placement:</strong>
                report={_fmt(chart.get('recommended_report_location'))};
                UI={_fmt(chart.get('recommended_ui_location'))}</p>
                <p class="chart-meta"><strong>Source result paths:</strong> {_fmt(source_text)}</p>
                {note_block}
            </article>
            """
        )
    return f"""
    <section class="report-section">
        <h2>Engineering Charts</h2>
        <p class="section-note">Charts are rendered from trusted BookResult chart specifications only. They visualize recorded values and do not recalculate engineering outcomes.</p>
        {''.join(cards)}
    </section>
    """


def _formula_logic_trace(checks: list[dict[str, Any]]) -> str:
    trace_blocks: list[str] = []
    for check in checks:
        for trace in check.get("formula_traces", []) or []:
            trace_blocks.append(
                f"""
                <article class="trace-block">
                    <h3>{_fmt(trace.get('formula_id'))} - {_fmt(trace.get('formula_name'))}</h3>
                    <p><strong>Source:</strong> {_fmt(trace.get('source_reference'))}</p>
                    <p><strong>Inputs:</strong> {_fmt(trace.get('inputs'))}</p>
                    <p><strong>Intermediates:</strong> {_fmt(trace.get('intermediates'))}</p>
                    <p><strong>Result:</strong> {_fmt(trace.get('result_symbol'))} = {_fmt(trace.get('result_value'))} {_fmt(trace.get('unit'))}</p>
                    <p><strong>Notes:</strong> {_fmt(trace.get('notes'))}</p>
                </article>
                """
            )
    content = "\n".join(trace_blocks) or "<p class=\"muted\">No formula traces were recorded for this scaffold result.</p>"
    return f"""
    <section class="report-section">
        <h2>Formula Logic Trace</h2>
        <p class="section-note">This section displays source-backed formula traces from BookResult only. It does not recalculate engineering outcomes.</p>
        {content}
    </section>
    """


def render_a4_html_report(context: dict[str, Any]) -> str:
    """Render a rigorous A4 calculation report HTML document."""
    project = context.get("project", {})
    checks = context.get("checks", [])
    warnings = context.get("warnings", [])
    errors = context.get("errors", [])
    charts = context.get("charts", [])
    sources = context.get("sources", [])
    assumptions = context.get("assumptions", [])
    generated_at = _fmt(context.get("generated_at"))
    title = _project_title(project)
    return f"""<!doctype html>
<html lang="{escape(str(context.get('lang', 'en')))}">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 18mm 16mm 18mm 16mm;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            background: #eef1f5;
            color: #1f2933;
            font-family: Arial, "Helvetica Neue", sans-serif;
            font-size: 10.5pt;
            line-height: 1.45;
        }}
        .a4-page {{
            width: 210mm;
            min-height: 297mm;
            margin: 12mm auto;
            padding: 18mm 16mm;
            background: #fff;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.16);
        }}
        .cover {{
            border-bottom: 2px solid #1d4ed8;
            margin-bottom: 12mm;
            padding-bottom: 10mm;
        }}
        .eyebrow {{
            color: #1d4ed8;
            font-size: 9pt;
            font-weight: 700;
            letter-spacing: 0;
            text-transform: uppercase;
        }}
        h1 {{
            margin: 4mm 0 6mm;
            font-size: 24pt;
            line-height: 1.15;
        }}
        h2 {{
            margin: 9mm 0 3mm;
            color: #12305c;
            font-size: 14pt;
            border-bottom: 1px solid #cbd5e1;
            padding-bottom: 1.5mm;
        }}
        h3 {{
            margin: 4mm 0 2mm;
            font-size: 11pt;
            color: #334155;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 3mm 0 5mm;
            page-break-inside: auto;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 2mm 2.5mm;
            vertical-align: top;
            word-break: break-word;
        }}
        th {{
            background: #f1f5f9;
            font-weight: 700;
            text-align: left;
        }}
        .kv-table th {{ width: 34%; }}
        .data-table th, .data-table td {{ font-size: 9pt; }}
        .summary-grid, .two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5mm;
        }}
        .summary-box {{
            border: 1px solid #cbd5e1;
            background: #f8fafc;
            padding: 4mm;
        }}
        .status {{
            display: inline-block;
            border-radius: 3px;
            padding: 0.5mm 1.5mm;
            font-weight: 700;
            background: #e2e8f0;
        }}
        .status-pass, .status-ok {{ color: #166534; background: #dcfce7; }}
        .status-fail, .status-error {{ color: #991b1b; background: #fee2e2; }}
        .trace-block {{
            border-left: 3px solid #2563eb;
            background: #f8fafc;
            margin: 4mm 0;
            padding: 3mm 4mm;
            page-break-inside: avoid;
        }}
        .section-note, .muted {{
            color: #64748b;
        }}
        .chart-card {{
            border: 1px solid #cbd5e1;
            background: #f8fafc;
            margin: 4mm 0;
            padding: 3mm 4mm;
            page-break-inside: avoid;
        }}
        .chart-svg {{
            width: 100%;
            max-width: 170mm;
            height: auto;
            margin: 2mm 0 3mm;
            background: #fff;
            border: 1px solid #e2e8f0;
        }}
        .chart-data th, .chart-data td {{
            font-size: 8.5pt;
        }}
        .chart-meta, .chart-notes {{
            color: #475569;
            font-size: 9pt;
        }}
        .report-section {{
            page-break-inside: auto;
        }}
        @media print {{
            body {{ background: #fff; }}
            .a4-page {{
                width: auto;
                min-height: auto;
                margin: 0;
                padding: 0;
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
<main class="a4-page">
    <section class="cover">
        <div class="eyebrow">A4 calculation report</div>
        <h1>{title}</h1>
        <div class="summary-grid">
            <div class="summary-box"><strong>Project ID</strong><br>{_fmt(project.get('project_id'))}</div>
            <div class="summary-box"><strong>Case ID</strong><br>{_fmt(project.get('case_id'))}</div>
            <div class="summary-box"><strong>Report Status</strong><br>{_fmt(context.get('report_status'))}</div>
            <div class="summary-box"><strong>Generated At</strong><br>{generated_at}</div>
        </div>
    </section>
    {_kv_table(context.get('governing', {}), title='Control Results and Governing Summary')}
    {_kv_table(context.get('input', {}).get('inputs', {}), title='Input Summary')}
    {_engineering_charts(charts)}
    {_checks_table(checks)}
    {_formula_logic_trace(checks)}
    {_sources_section(sources)}
    {_assumptions_section(assumptions)}
    {_warnings_errors(warnings, errors)}
    {_kv_table(context.get('traceability', {}), title='Traceability')}
    <section class="report-section">
        <h2>Template Boundary Statement</h2>
        <p>This HTML template references trusted BookInput, BookResult, ReportContext, warnings, errors, and formula traces only. It must not contain engineering formulas, lookup rules, unit conversion for official results, load-combination generation, optimization logic, or pass/fail recalculation.</p>
    </section>
</main>
</body>
</html>
"""
