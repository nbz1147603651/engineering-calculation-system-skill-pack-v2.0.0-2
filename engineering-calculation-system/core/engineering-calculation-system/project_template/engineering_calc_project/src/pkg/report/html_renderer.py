from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import math
from typing import Any

from .latex_renderer import (
    report_assumptions_from_context,
    report_figures_from_context,
    report_sources_from_checks,
    to_plain,
)


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
    figures = report_figures_from_context(plain_report, plain_result)
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
        "figures": figures,
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
        return f"<section class=\"section report-section\"><h1>{escape(title)}</h1><p class=\"muted\">No data recorded.</p></section>"
    rows = "\n".join(
        f"<tr><th>{escape(str(key))}</th><td>{_fmt(value)}</td></tr>"
        for key, value in data.items()
    )
    return f"""
    <section class="section report-section">
        <h1>{escape(title)}</h1>
        <table class="kv-table"><tbody>{rows}</tbody></table>
    </section>
    """


def _warnings_errors(warnings: list[Any], errors: list[Any]) -> str:
    warning_items = "".join(f"<li>{_fmt(item)}</li>" for item in warnings) or "<li>None</li>"
    error_items = "".join(f"<li>{_fmt(item)}</li>" for item in errors) or "<li>None</li>"
    return f"""
    <section class="section report-section">
        <h1>Warnings and Errors</h1>
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
    <section class="section report-section">
        <h1>Sources</h1>
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
    <section class="section report-section">
        <h1>Assumptions</h1>
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
    <section class="section report-section">
        <h1>Calculation Checks</h1>
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
        <section class="section report-section">
            <h1>Engineering Charts</h1>
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
    <section class="section report-section">
        <h1>Engineering Charts</h1>
        <p class="section-note">Charts are rendered from trusted BookResult chart specifications only. They visualize recorded values and do not recalculate engineering outcomes.</p>
        {''.join(cards)}
    </section>
    """


def _trace_mapping_table(title: str, data: dict[str, Any] | None) -> str:
    if not data:
        return ""
    rows = "\n".join(
        f"<tr><th>{_fmt(key)}</th><td>{_fmt(value)}</td></tr>"
        for key, value in data.items()
    )
    return f"""
    <h4>{escape(title)}</h4>
    <table class="data-table trace-data">
        <tbody>{rows}</tbody>
    </table>
    """


def _trace_formula_box(trace: dict[str, Any]) -> str:
    expression = trace.get("expression_tex") or trace.get("expression_plain")
    if not expression:
        return '<div class="formula-box muted">Formula expression not recorded in FormulaTrace.</div>'
    return f'<div class="formula-box">{_fmt(expression)}</div>'


def _formula_logic_trace(checks: list[dict[str, Any]]) -> str:
    trace_blocks: list[str] = []
    for check in checks:
        for trace in check.get("formula_traces", []) or []:
            explanation = trace.get("engineering_explanation")
            explanation_block = (
                f'<p class="explanation">{_fmt(explanation)}</p>'
                if explanation
                else ""
            )
            result_path = trace.get("result_path")
            result_path_block = (
                f'<p><strong>Result path:</strong> <code>{_fmt(result_path)}</code></p>'
                if result_path
                else ""
            )
            trace_blocks.append(
                f"""
                <article class="trace-block">
                    <h3>{_fmt(trace.get('formula_id'))} - {_fmt(trace.get('formula_name'))}</h3>
                    <p><strong>Check:</strong> {_fmt(check.get('check_id'))} |
                    <strong>Status:</strong> {_fmt(check.get('status'))} |
                    <strong>Source:</strong> {_fmt(trace.get('source_reference'))}</p>
                    {explanation_block}
                    {_trace_formula_box(trace)}
                    {_trace_mapping_table('Variables', trace.get('variable_definitions'))}
                    {_trace_mapping_table('Inputs', trace.get('inputs'))}
                    {_trace_mapping_table('Substitutions', trace.get('substitutions'))}
                    {_trace_mapping_table('Intermediates', trace.get('intermediates'))}
                    <p><strong>Result:</strong> {_fmt(trace.get('result_symbol'))} = {_fmt(trace.get('result_value'))} {_fmt(trace.get('unit'))}</p>
                    {result_path_block}
                    <p><strong>Notes:</strong> {_fmt(trace.get('notes'))}</p>
                </article>
                """
            )
    content = "\n".join(trace_blocks) or "<p class=\"muted\">No formula traces were recorded for this scaffold result.</p>"
    return f"""
    <section class="section report-section">
        <h1>Formula Logic Trace</h1>
        <p class="section-note">This section displays source-backed formula traces from BookResult only. It does not recalculate engineering outcomes.</p>
        {content}
    </section>
    """


def _table_of_contents(has_figures: bool) -> str:
    items = [
        "Control Results and Governing Summary",
        "Input Summary",
    ]
    if has_figures:
        items.append("Engineering Figures")
    items.extend([
        "Engineering Charts",
        "Calculation Checks",
        "Formula Logic Trace",
        "Sources",
        "Assumptions",
        "Warnings and Errors",
        "Traceability",
        "Template Boundary Statement",
    ])
    body = "\n".join(f"<li>{escape(item)}</li>" for item in items)
    return f"""
    <section class="section toc-section">
        <h1>Table of Contents</h1>
        <ol class="toc-list">{body}</ol>
    </section>
    """


def _figure_location(figure: dict[str, Any]) -> str:
    return str(
        figure.get("recommended_report_location")
        or figure.get("placement")
        or figure.get("location")
        or "after_input_summary"
    )


def _figure_src(figure: dict[str, Any]) -> str:
    return str(
        figure.get("src")
        or figure.get("html_src")
        or figure.get("path")
        or figure.get("url")
        or figure.get("data_uri")
        or ""
    )


def _figures_for(figures: list[dict[str, Any]], *locations: str) -> list[dict[str, Any]]:
    return [figure for figure in figures if _figure_location(figure) in locations]


def _figure_card(figure: dict[str, Any]) -> str:
    src = _figure_src(figure)
    image = (
        f'<img src="{escape(src, quote=True)}" alt="{_fmt(figure.get("alt"))}" />'
        if src
        else '<p class="muted">Image source not recorded.</p>'
    )
    caption = figure.get("caption")
    caption_block = f"<span>{_fmt(caption)}</span>" if caption else ""
    notes = figure.get("notes") or []
    note_items = "".join(f"<li>{_fmt(note)}</li>" for note in notes) if isinstance(notes, list) else ""
    note_block = f"<ul class=\"figure-notes\">{note_items}</ul>" if note_items else ""
    source = figure.get("source_reference") or figure.get("source")
    source_block = (
        f'<p class="figure-meta"><strong>Source:</strong> {_fmt(source)}</p>'
        if source
        else ""
    )
    result_path = figure.get("result_path") or figure.get("source_result_path")
    result_path_block = (
        f'<p class="figure-meta"><strong>Result path:</strong> <code>{_fmt(result_path)}</code></p>'
        if result_path
        else ""
    )
    return f"""
    <figure class="report-figure">
        {image}
        <figcaption>
            <strong>{_fmt(figure.get('figure_id'))} - {_fmt(figure.get('title'))}</strong>
            {caption_block}
        </figcaption>
        {source_block}
        {result_path_block}
        {note_block}
    </figure>
    """


def _engineering_figures(figures: list[dict[str, Any]], *locations: str, title: str = "Engineering Figures") -> str:
    selected = _figures_for(figures, *locations)
    if not selected:
        return ""
    cards = "\n".join(_figure_card(figure) for figure in selected)
    return f"""
    <section class="section figures-section">
        <h1>{escape(title)}</h1>
        <p class="section-note">Figures are report assets supplied through ReportContext or BookResult metadata. They support review and do not perform engineering calculations.</p>
        {cards}
    </section>
    """


def _cover_page(project: dict[str, Any], context: dict[str, Any], title: str, generated_at: str) -> str:
    traceability = context.get("traceability", {})
    return f"""
    <section class="cover-page">
        <h1>Engineering Calculation Book</h1>
        <h2>{title}</h2>
        <hr>
        <div class="project-info">
            <p><strong>{_fmt(project.get('project_name') or project.get('title') or title)}</strong></p>
            <p>Calculation report generated from trusted BookInput, BookResult, and ReportContext data.</p>
            <p>Formula traces, checks, charts, and figures are presentation-only views of recorded results.</p>
        </div>
        <div class="meta">
            <table class="cover-meta">
                <tbody>
                    <tr><td><strong>Project ID</strong></td><td>{_fmt(project.get('project_id'))}</td></tr>
                    <tr><td><strong>Case ID</strong></td><td>{_fmt(project.get('case_id'))}</td></tr>
                    <tr><td><strong>Report Status</strong></td><td>{_fmt(context.get('report_status'))}</td></tr>
                    <tr><td><strong>Generated At</strong></td><td>{generated_at}</td></tr>
                    <tr><td><strong>Template</strong></td><td>{_fmt(context.get('template_version'))}</td></tr>
                    <tr><td><strong>Formula Registry</strong></td><td>{_fmt(traceability.get('formula_registry_version'))}</td></tr>
                </tbody>
            </table>
        </div>
    </section>
    """


def render_a4_html_report(context: dict[str, Any]) -> str:
    """Render a rigorous A4 calculation report HTML document."""
    project = context.get("project", {})
    checks = context.get("checks", [])
    warnings = context.get("warnings", [])
    errors = context.get("errors", [])
    charts = context.get("charts", [])
    figures = context.get("figures", [])
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
            margin: 20mm 15mm 25mm 20mm;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        html {{
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        body {{
            background: #fff;
            color: #1a1a1a;
            font-family: "Times New Roman", Times, serif;
            font-size: 11pt;
            line-height: 1.5;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20mm 15mm 25mm 20mm;
        }}
        h1 {{
            margin: 20px 0 10px;
            color: #1a3a5c;
            font-size: 18pt;
            line-height: 1.2;
            text-align: center;
        }}
        h2 {{
            margin: 25px 0 10px;
            color: #1a3a5c;
            font-size: 14pt;
            border-bottom: 2px solid #1a3a5c;
            padding-bottom: 5px;
        }}
        h3 {{
            margin: 15px 0 8px;
            color: #2c5282;
            font-size: 12pt;
        }}
        h4 {{
            margin: 10px 0 5px;
            color: #333;
            font-size: 11pt;
        }}
        p {{
            margin: 5px 0;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 10pt;
            page-break-inside: auto;
        }}
        th, td {{
            border: 1px solid #666;
            padding: 4px 8px;
            text-align: left;
            vertical-align: top;
            word-break: break-word;
        }}
        th {{
            background: #e8f0f8;
            color: #1a3a5c;
            font-weight: 700;
        }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        ul, ol {{ margin: 5px 0 5px 20px; }}
        li {{ margin: 3px 0; }}
        .cover-page {{
            text-align: center;
            padding: 60px 20px;
            page-break-after: always;
        }}
        .cover-page h1 {{
            margin-top: 80px;
            font-size: 24pt;
            text-transform: uppercase;
        }}
        .cover-page h2 {{
            border: none;
            color: #333;
            font-size: 16pt;
        }}
        .cover-page hr {{
            width: 80%;
            margin: 30px auto;
            border: 1px solid #1a3a5c;
        }}
        .cover-page .project-info {{
            margin: 40px 0;
            font-size: 12pt;
        }}
        .cover-page .meta {{
            margin-top: 60px;
            color: #555;
            font-size: 11pt;
        }}
        .cover-meta {{
            width: 68%;
            margin: 0 auto;
        }}
        .cover-meta td:first-child {{
            width: 44%;
            text-align: right;
        }}
        .cover-meta td {{
            border: none;
            background: none;
            text-align: left;
        }}
        .section {{
            page-break-before: always;
        }}
        .toc-list {{
            font-size: 12pt;
            line-height: 2;
        }}
        .kv-table th {{ width: 34%; }}
        .summary-table td:first-child {{ width: 45%; font-weight: 700; }}
        .data-table th, .data-table td {{ font-size: 9.5pt; }}
        .summary-grid, .two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 5mm;
        }}
        .status {{
            display: inline-block;
            font-weight: 700;
        }}
        .status-pass, .status-ok {{ color: #16a34a; }}
        .status-fail, .status-error {{ color: #dc2626; }}
        .status-warning, .status-warn {{ color: #d97706; }}
        .note {{
            margin: 8px 0;
            padding: 6px 10px;
            border: 1px solid #fbbf24;
            background: #fffbeb;
            font-size: 10pt;
        }}
        .result-box {{
            margin: 10px 0;
            padding: 8px 12px;
            border: 2px solid #1a3a5c;
            background: #f8fafc;
        }}
        .trace-block {{
            margin: 8px 0;
            padding: 8px 12px;
            border: 1px solid #c0d0e0;
            border-left: 4px solid #1a3a5c;
            background: #f8fafc;
            page-break-inside: avoid;
        }}
        .formula-box {{
            margin: 8px 0;
            padding: 8px 12px;
            border: 1px solid #c0d0e0;
            border-left: 4px solid #1a3a5c;
            background: #f0f4f8;
            color: #1a1a1a;
            font-family: "Cambria Math", "Times New Roman", serif;
            font-size: 11pt;
            overflow-x: auto;
            word-break: break-word;
        }}
        .explanation {{
            color: #333;
        }}
        .trace-data th {{
            width: 30%;
        }}
        code {{
            color: #1a3a5c;
            font-family: "Courier New", monospace;
        }}
        .section-note, .muted {{
            color: #666;
            font-size: 10pt;
        }}
        .chart-card {{
            margin: 10px 0;
            padding: 8px 12px;
            border: 1px solid #c0d0e0;
            background: #f8fafc;
            page-break-inside: avoid;
        }}
        .chart-svg {{
            width: 100%;
            max-width: 170mm;
            height: auto;
            margin: 8px 0;
            background: #fff;
            border: 1px solid #c0d0e0;
        }}
        .chart-data th, .chart-data td {{
            font-size: 8.5pt;
        }}
        .chart-meta, .chart-notes, .figure-meta, .figure-notes {{
            color: #555;
            font-size: 9pt;
        }}
        .report-figure {{
            margin: 12px 0 16px;
            padding: 8px 10px;
            border: 1px solid #c0d0e0;
            background: #f8fafc;
            page-break-inside: avoid;
        }}
        .report-figure img {{
            display: block;
            max-width: 100%;
            max-height: 135mm;
            margin: 0 auto 8px;
            border: 1px solid #d6dde8;
            background: #fff;
            object-fit: contain;
        }}
        .report-figure figcaption {{
            color: #333;
            font-size: 10pt;
            text-align: center;
        }}
        .report-figure figcaption span {{
            display: block;
            margin-top: 2px;
        }}
        .report-section {{
            page-break-inside: auto;
        }}
        .report-end {{
            margin: 30px 0;
            border: none;
            border-top: 1px solid #999;
        }}
        .end-note {{
            color: #666;
            font-size: 10pt;
            text-align: center;
        }}
        @media print {{
            html, body {{
                width: 210mm;
                min-height: 297mm;
            }}
            body {{
                max-width: none;
                margin: 0;
                padding: 0;
                background: #fff;
            }}
            thead {{ display: table-header-group; }}
            tr, .trace-block, .chart-card, .report-figure {{
                break-inside: avoid;
                page-break-inside: avoid;
            }}
            .chart-svg, .report-figure img {{
                max-width: 100%;
                break-inside: avoid;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
<main class="calc-book">
    {_cover_page(project, context, title, generated_at)}
    {_engineering_figures(figures, 'after_cover', 'front_matter', title='Project Figures')}
    {_table_of_contents(bool(figures))}
    {_kv_table(context.get('governing', {}), title='Control Results and Governing Summary')}
    {_kv_table(context.get('input', {}).get('inputs', {}), title='Input Summary')}
    {_engineering_figures(figures, 'after_input_summary', 'before_charts')}
    {_engineering_charts(charts)}
    {_engineering_figures(figures, 'after_charts', 'before_checks', title='Supplementary Figures')}
    {_checks_table(checks)}
    {_formula_logic_trace(checks)}
    {_sources_section(sources)}
    {_assumptions_section(assumptions)}
    {_warnings_errors(warnings, errors)}
    {_kv_table(context.get('traceability', {}), title='Traceability')}
    <section class="section report-section">
        <h1>Template Boundary Statement</h1>
        <p>This HTML template references trusted BookInput, BookResult, ReportContext, warnings, errors, and formula traces only. It must not contain engineering formulas, lookup rules, unit conversion for official results, load-combination generation, optimization logic, or pass/fail recalculation.</p>
    </section>
    {_engineering_figures(figures, 'appendix', 'appendix_figures', title='Appendix Figures')}
    <hr class="report-end">
    <p class="end-note">End of Engineering Calculation Book<br>{title}<br>Generated: {generated_at}</p>
</main>
</body>
</html>
"""
