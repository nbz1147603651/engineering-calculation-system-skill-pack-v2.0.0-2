"""Internationalization (i18n) system for the web UI.

Scaffold: add book-specific translations while keeping the common patterns.
Master dictionary: key -> (english, chinese).
"""

from __future__ import annotations

# Master i18n dictionary — common keys shared across all calculation books.
# Add book-specific entries below the common section.
I18N: dict[str, tuple[str, str]] = {
    # ── Navigation & Layout ──────────────────────────────────────────
    "app_title": ("Engineering Calculator", "工程计算系统"),
    "app_subtitle": ("Source-Backed Calculation Book", "有据可查的计算书"),
    "nav_calculate": ("Calculate", "执行计算"),
    "nav_export_report": ("Export Report", "导出报告"),
    "nav_import": ("Import JSON", "导入配置"),
    "nav_export": ("Export JSON", "导出配置"),
    "nav_language": ("Language", "语言"),
    "language_label": ("Language", "语言"),
    "language_english": ("English", "英文"),
    "language_chinese": ("Chinese", "中文"),
    "nav_preview": ("Preview Report", "预览报告"),
    "nav_download": ("Download Report", "下载报告"),
    "nav_download_latex": ("LaTeX", "LaTeX"),
    "latex_template_label": ("LaTeX template", "LaTeX template"),
    "latex_template_default": ("Default template", "Default template"),
    "nav_admin_review": ("Marimo Review", "Marimo 审查"),

    # ── Section titles ───────────────────────────────────────────────
    "section_project": ("Project Information", "工程信息"),
    "section_options": ("Design Options", "设计参数"),
    "section_results": ("Calculation Results", "计算结果"),

    # ── Project form ─────────────────────────────────────────────────
    "project_id": ("Project ID", "项目编号"),
    "project_name": ("Project Name", "项目名称"),
    "case_id": ("Case ID", "工况编号"),

    # ── Buttons ──────────────────────────────────────────────────────
    "btn_calculate": ("Run Calculation", "执行计算"),
    "btn_import_json": ("Import JSON Config", "导入 JSON 配置"),
    "btn_export_json": ("Export Config", "导出配置"),
    "btn_preview_report": ("Preview Report", "预览报告"),
    "btn_download_report": ("Download Report", "下载报告"),
    "btn_close": ("Close", "关闭"),
    "btn_reset": ("Reset to Defaults", "恢复默认值"),
    "status_calculating": ("Calculating...", "正在计算..."),

    # ── Results display ──────────────────────────────────────────────
    "result_title": ("Calculation Results", "计算结果"),
    "result_placeholder": ("Click \"Run Calculation\" to see results.", "点击「执行计算」查看结果。"),
    "result_governing": ("Governing Check", "控制性验算"),
    "result_all_pass": ("All checks PASS", "所有验算通过"),
    "result_has_fail": ("Some checks FAILED", "部分验算未通过"),
    "result_utilization": ("Utilization", "利用率"),
    "result_status_ok": ("PASS", "满足要求"),
    "result_status_ng": ("FAIL", "不满足要求"),

    # ── Error messages ───────────────────────────────────────────────
    "error_calc_failed": ("Calculation failed. Please check your inputs.", "计算失败，请检查输入参数。"),
    "error_invalid_input": ("Invalid input value", "输入值无效"),
    "error_missing_field": ("Required field missing", "必填字段缺失"),
    "error_import_failed": ("Failed to import configuration.", "导入配置失败。"),
    "error_export_failed": ("Export failed.", "导出失败。"),
    "error_report_preview_failed": ("Report preview failed.", "报告预览失败。"),
    "error_report_download_failed": ("Report download failed.", "报告下载失败。"),
    "error_latex_download_failed": ("LaTeX export failed.", "LaTeX 导出失败。"),
    "error_network": ("Network error", "网络错误"),
    "error_no_result": ("Please run calculation first.", "请先执行计算。"),

    # ── Warning messages ─────────────────────────────────────────────
    "warn_invalid_values": (
        "Some computed values are invalid (Infinity/NaN) and have been replaced.",
        "部分计算结果无效(无穷大/非数值)，已替换。请检查输入参数。",
    ),

    # ── Report preview ───────────────────────────────────────────────
    "report_title": ("Calculation Report", "计算报告"),
    "report_generating": ("Generating report...", "正在生成报告..."),

    # ── Book-specific entries ────────────────────────────────────────
    # Add domain-specific translations below. Examples:
    # "section_soil": ("Soil Profile", "地基土层"),
    # "section_foundation": ("Foundation Geometry", "基础几何参数"),
    # "section_loads": ("Load Case", "荷载工况"),
    # "result_bearing": ("Bearing Capacity", "地基承载力"),
    # "result_settlement": ("Settlement", "沉降"),
}


def get_translations(lang: str = "en") -> dict[str, str]:
    """Return a flat dictionary of {key: translated_text} for the given language."""
    idx = 0 if lang == "en" else 1
    return {k: v[idx] for k, v in I18N.items()}


def t(key: str, lang: str = "en") -> str:
    """Get a single translated text."""
    entry = I18N.get(key)
    if entry is None:
        return key
    return entry[0] if lang == "en" else entry[1]
