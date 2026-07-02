#!/usr/bin/env python3
"""Validate the engineering calculation skill pack and generated project artifacts."""

from __future__ import annotations

import argparse
import csv
import importlib
import importlib.util
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory


sys.dont_write_bytecode = True

FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
YAML_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")

PROFILE_CHOICES = {"core", "adapters-light", "qoder-addon", "singlefile"}
DELIVERY_CHOICES = {"standard", "web-complete"}
QODER_AGENT_FILES = [
    ".qoder/agents/engineering-calc-system.md",
    ".qoder/agents/engineering-calc-reference-acquirer.md",
    ".qoder/agents/engineering-calc-source-intake.md",
    ".qoder/agents/engineering-calc-logic-extractor.md",
    ".qoder/agents/engineering-calc-module-worker.md",
    ".qoder/agents/engineering-calc-interface-worker.md",
    ".qoder/agents/engineering-calc-verification-worker.md",
    ".qoder/agents/engineering-calc-release-worker.md",
]
PRODUCTION_ALLOWED = "production_allowed"
ANALYSIS_ALLOWED = "analysis_allowed"
BLOCKING_COVERAGE_VALUES = {"", "not_covered", "partially_covered", "conflicting", "unknown"}
PLACEHOLDER_VALUES = {
    "",
    "-",
    "n/a",
    "na",
    "none",
    "todo",
    "tbd",
    "to be defined",
    "to_be_defined",
    "needs confirmation",
    "needs_confirmation",
    "not specified",
    "not_specified",
    "unknown",
}
TRUTHY_VALUES = {"1", "true", "yes", "y", "blocking", "blocks"}
CLOSURE_PASS_VALUES = {"closed", "covered", "complete", "verified", "production_ready"}
GOLDEN_CASE_PASS_VALUES = {"verified", "approved", "passed", "passing", "production_ready"}
CORE_FORBIDDEN_ROOT_PATHS = {
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "INSTALL.md",
    "CHANGELOG.md",
    "MIGRATION_NOTES.md",
    "SKILL_PACKAGE_SUMMARY.md",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
    "engineering-calculation-system.all-in-one.md",
    ".agents",
    ".opencode",
    ".qoder",
    ".trae",
    "adapters",
    "examples",
    "workflow_diagrams",
    "original_sources",
}
FORBIDDEN_CACHE_NAMES = {".pytest_cache", "__pycache__"}
FORBIDDEN_CACHE_SUFFIXES = {".pyc", ".pyo"}
TEXT_FILE_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".j2",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sty",
    ".tex",
    ".txt",
    ".yaml",
    ".yml",
}
MOJIBAKE_MARKERS = ("\u922b", "\u9225")
LIFECYCLE_REDIRECT_PATHS = [
    "shared/delivery-contract.md",
    "shared/lifecycle-matrix.md",
    "shared/quality-gates.md",
]
BEHAVIOR_ENGINEERING_DOCS = [
    "shared/execution-discipline.md",
    "shared/planning-discipline.md",
    "shared/review-feedback-discipline.md",
    "shared/version-control-discipline.md",
    "shared/completion-evidence.md",
    "shared/systematic-debugging.md",
]
SINGLEFILE_ALLOWED_FILES = {
    "engineering-calculation-system.all-in-one.md",
    "MANIFEST.yaml",
    "CHECKSUMS.txt",
    "TREE.md",
}
PRODUCTION_REQUIRED_PROJECT_ARTIFACTS = {
    "source registry": ["references/source_registry.yaml"],
    "evidence library manifest": ["references/evidence_library_manifest.yaml"],
    "acquisition handoff": ["references/acquisition/acquisition_handoff.yaml"],
    "source coverage matrix": ["references/acquisition/source_coverage_matrix.csv"],
    "source inventory": [
        "analysis/01_source_inventory/source_inventory.yaml",
        "analysis/source_inventory.yaml",
    ],
    "source authority table": [
        "analysis/01_source_inventory/source_authority_table.csv",
        "analysis/source_authority_table.csv",
    ],
    "source conflicts": [
        "analysis/01_source_inventory/source_conflicts.csv",
        "analysis/source_conflicts.csv",
    ],
    "calculation intent contract": [
        "analysis/02_logic_blueprint/calculation_intent_contract.md",
        "analysis/calculation_intent_contract.md",
    ],
    "method selection matrix": [
        "analysis/02_logic_blueprint/method_selection_matrix.csv",
        "analysis/method_selection_matrix.csv",
    ],
    "input semantics ledger": [
        "analysis/02_logic_blueprint/input_semantics_ledger.csv",
        "analysis/input_semantics_ledger.csv",
    ],
    "formula inventory": [
        "analysis/03_logic_details/formula_inventory.csv",
        "analysis/formula_inventory.csv",
    ],
    "lookup inventory": [
        "analysis/03_logic_details/lookup_inventory.csv",
        "analysis/lookup_inventory.csv",
    ],
    "branch inventory": [
        "analysis/03_logic_details/branch_inventory.csv",
        "analysis/branch_inventory.csv",
    ],
    "computation graph coverage": [
        "analysis/03_logic_details/computation_graph_coverage.csv",
        "analysis/02_logic_blueprint/computation_graph_coverage.csv",
        "analysis/computation_graph_coverage.csv",
    ],
    "unit and sign conventions": [
        "analysis/03_logic_details/unit_and_sign_conventions.md",
        "analysis/unit_and_sign_conventions.md",
    ],
    "assumption register": [
        "analysis/03_logic_details/assumption_register.csv",
        "analysis/assumption_register.csv",
    ],
    "open questions": [
        "analysis/05_risks_and_questions/open_questions.csv",
        "analysis/open_questions.csv",
    ],
    "user interaction decisions": [
        "analysis/06_user_interaction/user_interaction_decisions.csv",
        "analysis/user_interaction_decisions.csv",
    ],
    "module asset registry": [
        "implementation/02_modules/module_asset_registry.csv",
        "implementation/module_asset_registry.csv",
    ],
    "chart candidate inventory": [
        "implementation/03_book_runner/chart_candidate_inventory.csv",
        "implementation/chart_candidate_inventory.csv",
    ],
    "runner closure map": [
        "implementation/03_book_runner/runner_closure_map.csv",
        "implementation/runner_closure_map.csv",
    ],
    "test matrix": [
        "verification/test_matrix.csv",
        "tests/test_matrix.csv",
    ],
    "golden case registry": [
        "verification/golden_case_registry.csv",
        "verification/golden_cases.csv",
    ],
}
WEB_COMPLETE_REQUIRED_PROJECT_PATHS = [
    "webapp/app.py",
    "webapp/routes.py",
    "webapp/form_utils.py",
    "webapp/i18n.py",
    "webapp/templates/base.html",
    "webapp/templates/index.html",
    "webapp/templates/admin_review.html",
    "webapp/templates/partials/_topbar.html",
    "webapp/templates/partials/_report_modal.html",
    "webapp/static/js/main.js",
    "webapp/static/js/forms.js",
    "webapp/static/js/results.js",
    "webapp/static/js/i18n.js",
    "webapp/static/css/tokens.css",
    "webapp/static/css/components.css",
    "webapp/static/css/style.css",
    "src/pkg/core/capabilities.py",
    "src/pkg/review/bridge.py",
    "src/pkg/report/latex_renderer.py",
    "src/pkg/report/html_renderer.py",
    "src/pkg/report/report_selector.py",
    "latex/templates/default_engineering_calcbook/main.tex.j2",
    "latex/templates/default_engineering_calcbook/cover.tex.j2",
    "latex/templates/default_engineering_calcbook/page_style.sty",
    "latex/templates/default_engineering_calcbook/latexmkrc",
    "latex/templates/default_engineering_calcbook/sections/04_figures.tex.j2",
    "apps/review/calculation_review.py",
    "apps/review/admin_formula_review.py",
    "deploy/env.example",
    "deploy/one_click_deploy.sh",
    "deploy/Dockerfile",
    "deploy/docker-compose.yml",
    "deploy/systemd/engineering-calc.service",
    "deploy/systemd/engineering-calc-review.service",
    "deploy/systemd/engineering-calc-formula-admin.service",
    "deploy/nginx/engineering-calc.conf",
    "release/release_checklist.md",
    "release/runbook.md",
    "tests/smoke/test_web_routes.py",
    "tests/unit/test_marimo_review.py",
    "outputs/results_json/.gitkeep",
    "outputs/normalized_inputs_json/.gitkeep",
    "outputs/upload_packages/.gitkeep",
    "outputs/batch_summaries/.gitkeep",
    "outputs/reports_html/.gitkeep",
    "outputs/reports_latex/.gitkeep",
    "outputs/reports_pdf/.gitkeep",
    "outputs/logs/.gitkeep",
    "outputs/review/.gitkeep",
    "tests/smoke/test_latex_report.py",
    "analysis/06_user_interaction/user_interaction_decisions.csv",
    "implementation/03_book_runner/chart_candidate_inventory.csv",
]
WEB_COMPLETE_TEXT_REQUIRED_PHRASES = {
    "webapp/app.py": [
        "def create_app",
        "/health",
    ],
    "webapp/routes.py": [
        "/api/calculate",
        "/api/i18n/<lang>",
        "/api/report/preview",
        "/api/report/html",
        "/api/report/decision",
        "/api/report/final",
        "/api/report/templates",
        "/api/report/latex",
        "/api/capabilities",
        "/api/review/session",
        "/api/review/state/<session_id>",
        "/admin/",
        "/admin/review/",
        "admin_review",
        "detect_capabilities",
        "write_review_session",
        "read_review_session",
        "admin_url",
        "review_url",
        "_resolve_latex_template_dir",
        "latex_template_id",
        "select_report_output",
        "compile_latex_project",
        "render_a4_html_report",
        "/api/import/json",
        "/api/export/json",
        "/api/batch/run",
        "run_book",
        "build_case_input_from_form",
        "case_result_to_ui",
    ],
    "webapp/i18n.py": [
        "I18N",
        "english, chinese",
        "language_english",
        "language_chinese",
        "get_translations",
    ],
    "webapp/templates/base.html": [
        "url_for('static'",
        "filename='css/tokens.css'",
        "filename='css/components.css'",
        "partials/_topbar.html",
        "partials/_report_modal.html",
        "filename='js/i18n.js'",
    ],
    "webapp/templates/admin_review.html": [
        "id=\"adminReviewPage\"",
        "Marimo Calculation Review",
        "ADMIN_REVIEW_PASSWORD",
        "ADMIN_REVIEW_TOKEN",
        "review.run_command",
        "review.formula_admin_run_command",
        "review.install_command",
        "Marimo is not installed in this runtime",
        "apps/review/calculation_review.py",
        "/api/review/session",
        "/admin/formulas",
        "active_versions.yaml",
        "run_book()",
    ],
    "webapp/templates/partials/_topbar.html": [
        "id=\"langToggle\"",
        "data-lang=\"en\"",
        "data-lang=\"zh\"",
        "data-i18n-title=\"language_label\"",
        "id=\"latexTemplateSelect\"",
        "id=\"btnDownloadLatex\"",
        "id=\"btnAdminReview\"",
        "id=\"adminReviewStatus\"",
    ],
    "webapp/templates/partials/_report_modal.html": [
        "id=\"reportModal\"",
        "id=\"btnDownloadReport\"",
        "id=\"reportFrame\"",
    ],
    "webapp/static/css/tokens.css": [
        "--ecs-color-primary",
        "--ecs-color-surface",
        "--ecs-radius-md",
    ],
    "webapp/static/css/components.css": [
        ".app-topbar",
        ".metric-grid",
        ".report-frame",
        ".topbar-template-select",
    ],
    "webapp/static/js/main.js": [
        "/api/calculate",
        "/api/report/preview",
        "/api/report/final",
        "/api/report/templates",
        "/api/report/latex",
        "/api/review/session",
        "/api/capabilities",
        "renderCapabilities",
        "getSelectedLatexTemplateId",
        "latex_template_id",
        "/api/import/json",
        "/api/export/json",
        "getCurrentLang",
        "data.lang = getCurrentLang()",
        "btnDownloadLatex",
    ],
    "webapp/static/js/results.js": [
        "renderCapabilities",
        "renderCharts",
        "renderChecksTable",
        "renderFormulaTraces",
        "configureReviewAdmin",
    ],
    "src/pkg/core/capabilities.py": [
        "detect_capabilities",
        "marimo_review",
        "admin_password_set",
        "formula_admin_url",
        "calculation_review.py",
        "latex",
        "docker",
    ],
    "src/pkg/review/bridge.py": [
        "write_review_session",
        "read_review_session",
        "append_review_decision",
        "outputs",
        "review",
    ],
    "src/pkg/report/html_renderer.py": [
        "build_html_report_context",
        "render_a4_html_report",
        "@page",
        "size: A4",
        "print-color-adjust",
        "Engineering Charts",
        "chart-data",
        "Formula Logic Trace",
        "Control Results and Governing Summary",
        "Sources",
        "Assumptions",
        "Template Boundary Statement",
    ],
    "src/pkg/report/latex_renderer.py": [
        "build_latex_report_context",
        "report_sources_from_checks",
        "report_assumptions_from_context",
        "render_latex_project_zip",
        "detect_latex_toolchain",
        "compile_latex_project",
        "main.pdf",
        "latex_escape",
        "Overleaf import",
    ],
    "src/pkg/report/report_selector.py": [
        "select_report_output",
        "latex_pdf",
        "html_a4",
        "detect_latex_toolchain",
        "print-ready A4 HTML",
    ],
    "webapp/static/js/i18n.js": [
        "localStorage",
        "document.documentElement.lang",
        "data-i18n",
        "setLanguage",
        "data-lang",
        "languagechange",
    ],
    "tests/smoke/test_web_routes.py": [
        "/health",
        "/api/i18n/en",
        "/api/i18n/zh",
        "/api/calculate",
        "/api/import/json",
        "/api/export/json",
        "/api/report/preview",
        "/api/report/html",
        "/api/report/decision",
        "/api/capabilities",
        "/api/review/session",
        "/api/batch/run",
        "langToggle",
        "capabilityStrip",
        "btnAdminReview",
        "chartsSection",
        "size: A4",
        "print-color-adjust",
        "Engineering Charts",
        "chart-data",
        "Formula Logic Trace",
        "Sources",
        "Assumptions",
        "test_deploy_artifacts_present",
    ],
    "deploy/one_click_deploy.sh": [
        "docker compose up -d --build",
        "ECS_ENV_FILE=\"$ENV_FILE\"",
        "ADMIN_REVIEW_PASSWORD",
        "ADMIN_REVIEW_TOKEN",
        "marimo run apps/review/calculation_review.py",
        "marimo run apps/review/admin_formula_review.py",
    ],
    "deploy/docker-compose.yml": [
        "marimo-review",
        "marimo-formula-admin",
        "ADMIN_REVIEW_TOKEN",
        "FORMULA_ADMIN_BASE_URL",
        "127.0.0.1:2718:2718",
        "127.0.0.1:2719:2719",
    ],
    "deploy/nginx/engineering-calc.conf": [
        "location /admin/review/",
        "location /admin/formulas/",
        "proxy_http_version 1.1",
    ],
    "release/runbook.md": [
        "bash deploy/one_click_deploy.sh",
        "/admin/",
        "ADMIN_REVIEW_PASSWORD",
        "ADMIN_REVIEW_TOKEN",
        "Formula Publishing Effect",
    ],
    "apps/review/calculation_review.py": [
        "marimo.App",
        "_MissingMarimoApp",
        "Marimo is not installed",
        "list_review_sessions",
        "read_review_session",
        "append_review_decision",
        "FormulaTrace",
        "review_decisions.jsonl",
    ],
    "apps/review/admin_formula_review.py": [
        "marimo.App",
        "_MissingMarimoApp",
        "Marimo is not installed",
        "publish_formula_rule",
        "active_versions.yaml",
        "run_book()",
    ],
    "tests/unit/test_marimo_review.py": [
        "calculation_review.py",
        "admin_formula_review.py",
        "Marimo is not installed",
    ],
    "tests/smoke/test_latex_report.py": [
        "/api/report/latex",
        "/api/report/final",
        "/api/report/templates",
        "latex_template_id",
        "ReportRenderDecision",
        "html_a4",
        "print-ready A4 HTML",
        "size: A4",
        "print-color-adjust",
        "application/zip",
        "main.tex",
        "page_style.sty",
        "Formula Logic Trace",
        "Sources",
        "Assumptions",
        "Template Boundary Statement",
    ],
    "release/release_checklist.md": [
        "web-complete",
        "/api/import/json",
        "/api/export/json",
        "/api/report/preview",
        "/api/report/html",
        "GET /api/report/decision",
        "POST /api/report/final",
        "@page size: A4",
        "/api/batch/run",
        "CLI runner",
    ],
}
WEB_COMPLETE_PLACEHOLDER_SCAN_PATHS = [
    "README.md",
    "handoff/implementation_handoff.yaml",
    "handoff/coding_go_no_go.md",
    "tests/smoke/example_input.json",
    "webapp/config.py",
    "webapp/templates/index.html",
    "references/source_registry.yaml",
    "references/evidence_library_manifest.yaml",
    "references/acquisition/acquisition_handoff.yaml",
    "references/acquisition/source_coverage_matrix.csv",
    "analysis/01_source_inventory/source_inventory.yaml",
    "analysis/01_source_inventory/source_authority_table.csv",
    "analysis/03_logic_details/formula_inventory.csv",
    "analysis/02_logic_blueprint/calculation_intent_contract.md",
    "analysis/02_logic_blueprint/method_selection_matrix.csv",
    "analysis/02_logic_blueprint/input_semantics_ledger.csv",
    "analysis/03_logic_details/computation_graph_coverage.csv",
    "analysis/03_logic_details/unit_and_sign_conventions.md",
    "analysis/03_logic_details/assumption_register.csv",
    "analysis/05_risks_and_questions/open_questions.csv",
    "analysis/06_user_interaction/user_interaction_decisions.csv",
    "implementation/03_book_runner/chart_candidate_inventory.csv",
    "implementation/03_book_runner/runner_closure_map.csv",
    "verification/golden_case_registry.csv",
]
WEB_COMPLETE_FORBIDDEN_PROJECT_TOKENS = [
    "Example Project",
    "EXAMPLE_001",
    "<book_name>",
    "<example_book>",
    "to_be_defined",
    "needs_confirmation",
]
WEB_COMPLETE_REQUIRED_REPORT_SECTIONS = [
    "Control Results and Governing Summary",
    "Input Summary",
    "Engineering Charts",
    "Calculation Checks",
    "Formula Logic Trace",
    "Sources",
    "Assumptions",
    "Traceability",
    "Template Boundary Statement",
]
WEB_COMPLETE_FORBIDDEN_REPORT_PHRASES = [
    "No checks recorded.",
    "No sources recorded.",
    "No assumptions recorded.",
    "Example Project",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_contract(package_root: Path) -> dict:
    path = package_root / "schemas" / "artifact_contracts.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def manifest_version(package_root: Path) -> str | None:
    path = package_root / "MANIFEST.yaml"
    if not path.exists():
        return None
    pattern = re.compile(r"^version:\s*(.+)$")
    for line in read_text(path).splitlines():
        match = pattern.match(line)
        if match:
            return clean_scalar(match.group(1))
    return None


def check_exists(root: Path, rel_path: str, errors: list[str]) -> None:
    if not (root / rel_path).exists():
        errors.append(f"missing required path: {rel_path}")


def check_absent(root: Path, rel_path: str, errors: list[str]) -> None:
    if (root / rel_path).exists():
        errors.append(f"forbidden path present: {rel_path}")


def check_no_cache_artifacts(root: Path, errors: list[str]) -> None:
    try:
        paths = list(root.rglob("*"))
    except OSError as exc:
        errors.append(f"could not scan package for forbidden cache artifacts: {exc}")
        return

    for path in paths:
        rel = path.relative_to(root).as_posix()
        if path.name in FORBIDDEN_CACHE_NAMES or path.suffix in FORBIDDEN_CACHE_SUFFIXES:
            errors.append(f"forbidden cache artifact present: {rel}")


def first_csv_line(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        row = next(reader, [])
    return ",".join(row)


def clean_scalar(value: object) -> str:
    text = "" if value is None else str(value)
    if "#" in text:
        text = text.split("#", 1)[0]
    return text.strip().strip('"').strip("'")


def normalize_token(value: object) -> str:
    return clean_scalar(value).strip().lower()


def is_truthy(value: object) -> bool:
    return normalize_token(value) in TRUTHY_VALUES


def has_actionable_text(value: object) -> bool:
    return normalize_token(value) not in PLACEHOLDER_VALUES


def read_csv_rows(path: Path, errors: list[str], *, label: str) -> list[dict[str, str]]:
    if not path.exists():
        errors.append(f"missing CSV artifact for semantic gate: {path.as_posix()}")
        return []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    except csv.Error as exc:
        errors.append(f"could not parse {label}: {exc}")
        return []


def row_identifier(row: dict[str, str], fallback_index: int) -> str:
    for key in (
        "formula_id",
        "lookup_id",
        "branch_id",
        "coverage_id",
        "method_id",
        "input_id",
        "case_id",
        "test_id",
        "module_id",
        "question_id",
        "conflict_id",
        "assumption_id",
        "requirement_id",
    ):
        if has_actionable_text(row.get(key)):
            return str(row.get(key))
    return f"row {fallback_index}"


def split_reference_values(value: object) -> set[str]:
    text = clean_scalar(value)
    if not text:
        return set()
    cleaned = text.strip().strip("[]")
    return {
        token.strip().strip("'\"")
        for token in re.split(r"[;,|]", cleaned)
        if has_actionable_text(token)
    }


def collect_reference_values(rows: list[dict[str, str]], field: str) -> set[str]:
    values: set[str] = set()
    for row in rows:
        values.update(split_reference_values(row.get(field)))
    return values


def actionable_row_ids(rows: list[dict[str, str]], field: str) -> set[str]:
    return {
        clean_scalar(row.get(field))
        for row in rows
        if has_actionable_text(row.get(field))
    }


def first_existing(root: Path, candidates: list[str]) -> Path | None:
    for rel_path in candidates:
        path = root / rel_path
        if path.exists():
            return path
    return None


def yaml_top_scalar(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*)$")
    for line in read_text(path).splitlines():
        match = pattern.match(line)
        if match:
            return clean_scalar(match.group(1))
    return ""


def yaml_nested_scalar(path: Path, parent_key: str, child_key: str) -> str:
    if not path.exists():
        return ""
    lines = read_text(path).splitlines()
    parent_re = re.compile(rf"^(?P<indent>\s*){re.escape(parent_key)}:\s*(?:#.*)?$")
    child_re = re.compile(rf"^(?P<indent>\s*){re.escape(child_key)}:\s*(?P<value>.*)$")
    parent_indent: int | None = None
    for line in lines:
        if parent_indent is None:
            match = parent_re.match(line)
            if match:
                parent_indent = len(match.group("indent"))
            continue

        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent <= parent_indent:
            break
        match = child_re.match(line)
        if match and len(match.group("indent")) > parent_indent:
            return clean_scalar(match.group("value"))
    return ""


def project_coding_gate_status(project_root: Path) -> str:
    handoff_path = project_root / "handoff" / "implementation_handoff.yaml"
    return normalize_token(
        yaml_nested_scalar(handoff_path, "coding_gate", "status")
        or yaml_top_scalar(handoff_path, "status")
    )


def markdown_gate_status(path: Path) -> str:
    if not path.exists():
        return ""
    pattern = re.compile(r"^\s*status:\s*(.*)$")
    for line in read_text(path).splitlines():
        match = pattern.match(line)
        if match:
            return normalize_token(match.group(1))
    return ""


def check_production_required_artifacts(project_root: Path, errors: list[str]) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for label, candidates in PRODUCTION_REQUIRED_PROJECT_ARTIFACTS.items():
        path = first_existing(project_root, candidates)
        if path is None:
            errors.append(
                "production gate requires "
                f"{label}: expected one of {', '.join(candidates)}"
            )
            continue
        found[label] = path
    return found


def check_source_coverage_for_production(path: Path, errors: list[str]) -> None:
    rows = read_csv_rows(path, errors, label="source coverage matrix")
    if not rows:
        errors.append("production gate requires at least one source coverage row")
        return
    for index, row in enumerate(rows, start=2):
        importance = normalize_token(row.get("importance"))
        covered = normalize_token(row.get("covered"))
        blocks_coding = is_truthy(row.get("blocks_coding"))
        must_be_covered = importance in {"critical", "high"} and (blocks_coding or importance == "critical")
        if must_be_covered and covered in BLOCKING_COVERAGE_VALUES:
            errors.append(
                "production gate blocked by uncovered critical/high source requirement "
                f"{row_identifier(row, index)}: covered={row.get('covered')!r}"
            )
        if must_be_covered and not has_actionable_text(row.get("current_source_id")):
            errors.append(
                "production gate requires a current_source_id for critical/high source "
                f"requirement {row_identifier(row, index)}"
            )


def check_csv_required_fields(
    path: Path,
    label: str,
    required_fields: list[str],
    errors: list[str],
    *,
    require_rows: bool = False,
) -> None:
    rows = read_csv_rows(path, errors, label=label)
    if require_rows and not rows:
        errors.append(f"production gate requires at least one {label} row")
    for index, row in enumerate(rows, start=2):
        row_id = row_identifier(row, index)
        for field in required_fields:
            if not has_actionable_text(row.get(field)):
                errors.append(
                    f"production gate requires actionable {field!r} in {label} {row_id}"
                )


def check_blocking_csv_flags(
    path: Path,
    label: str,
    flag_field: str,
    errors: list[str],
) -> None:
    rows = read_csv_rows(path, errors, label=label)
    for index, row in enumerate(rows, start=2):
        if is_truthy(row.get(flag_field)):
            errors.append(
                f"production gate blocked by {label} {row_identifier(row, index)} "
                f"with {flag_field}=true"
            )


def check_calculation_intent_contract(path: Path, errors: list[str]) -> None:
    status = markdown_gate_status(path)
    if status != "production_ready":
        errors.append(
            "production gate requires calculation intent contract "
            f"status='production_ready', got {status or 'missing'}"
        )
    text = read_text(path) if path.exists() else ""
    for phrase in ("governing_question", "intended_decision", "excluded_scope"):
        if phrase not in text:
            errors.append(f"calculation intent contract is missing {phrase}")


def check_status_field(
    path: Path,
    label: str,
    status_field: str,
    pass_values: set[str],
    errors: list[str],
    *,
    require_rows: bool = True,
) -> list[dict[str, str]]:
    rows = read_csv_rows(path, errors, label=label)
    if require_rows and not rows:
        errors.append(f"production gate requires at least one {label} row")
    for index, row in enumerate(rows, start=2):
        status = normalize_token(row.get(status_field))
        if status not in pass_values:
            errors.append(
                f"production gate requires {label} {row_identifier(row, index)} "
                f"{status_field} in {sorted(pass_values)}, got {status or 'missing'}"
            )
    return rows


def check_input_semantics_ledger(path: Path, errors: list[str]) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "input semantics ledger",
        [
            "input_id",
            "book_input_path",
            "meaning",
            "unit",
            "sign_convention",
            "source_reference",
            "required",
            "default_policy",
            "validation_rule",
            "used_by_nodes",
        ],
        errors,
        require_rows=True,
    )
    rows = read_csv_rows(path, errors, label="input semantics ledger")
    for index, row in enumerate(rows, start=2):
        if is_truthy(row.get("blocks_production")):
            errors.append(
                "production gate blocked by input semantics ledger "
                f"{row_identifier(row, index)} with blocks_production=true"
            )
    return rows


def check_method_selection_matrix(path: Path, errors: list[str]) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "method selection matrix",
        [
            "method_id",
            "check_id",
            "method_name",
            "source_reference",
            "applicability",
            "selection_condition",
            "required_inputs",
            "required_outputs",
            "test_requirement",
            "risk_level",
        ],
        errors,
        require_rows=True,
    )
    return read_csv_rows(path, errors, label="method selection matrix")


def check_module_asset_registry(path: Path, errors: list[str]) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "module asset registry",
        [
            "module_id",
            "module_name",
            "public_function",
            "input_model",
            "result_model",
            "source_references",
            "formula_trace_path",
            "unit_tests",
            "reuse_status",
        ],
        errors,
        require_rows=True,
    )
    return read_csv_rows(path, errors, label="module asset registry")


def check_test_matrix(path: Path, errors: list[str]) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "test matrix",
        ["test_id", "target", "type", "reference_basis", "input_case", "expected_result", "tolerance"],
        errors,
        require_rows=True,
    )
    return read_csv_rows(path, errors, label="test matrix")


def check_computation_graph_coverage(
    path: Path,
    errors: list[str],
    *,
    formula_rows: list[dict[str, str]],
    lookup_rows: list[dict[str, str]],
    branch_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    module_ids: set[str],
    test_ids: set[str],
) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "computation graph coverage",
        [
            "coverage_id",
            "node_id",
            "node_type",
            "source_reference",
            "module_id",
            "public_function",
            "runner_step",
            "result_path",
            "test_ids",
            "closure_status",
        ],
        errors,
        require_rows=True,
    )
    rows = check_status_field(
        path,
        "computation graph coverage",
        "closure_status",
        CLOSURE_PASS_VALUES,
        errors,
        require_rows=False,
    )

    coverage_formula_ids = collect_reference_values(rows, "formula_ids")
    for formula_id in actionable_row_ids(formula_rows, "formula_id") - coverage_formula_ids:
        errors.append(f"production gate requires computation graph coverage for formula {formula_id}")

    coverage_lookup_ids = collect_reference_values(rows, "lookup_ids")
    for lookup_id in actionable_row_ids(lookup_rows, "lookup_id") - coverage_lookup_ids:
        errors.append(f"production gate requires computation graph coverage for lookup {lookup_id}")

    coverage_branch_ids = collect_reference_values(rows, "branch_ids")
    for branch_id in actionable_row_ids(branch_rows, "branch_id") - coverage_branch_ids:
        errors.append(f"production gate requires computation graph coverage for branch {branch_id}")

    required_input_ids = {
        clean_scalar(row.get("input_id"))
        for row in input_rows
        if has_actionable_text(row.get("input_id")) and is_truthy(row.get("required"))
    }
    coverage_input_ids = collect_reference_values(rows, "input_ids")
    for input_id in required_input_ids - coverage_input_ids:
        errors.append(f"production gate requires computation graph coverage for required input {input_id}")

    for index, row in enumerate(rows, start=2):
        module_id = clean_scalar(row.get("module_id"))
        if has_actionable_text(module_id) and module_ids and module_id not in module_ids:
            errors.append(
                f"computation graph coverage {row_identifier(row, index)} "
                f"references unknown module_id {module_id!r}"
            )
        for test_id in split_reference_values(row.get("test_ids")):
            if test_ids and test_id not in test_ids:
                errors.append(
                    f"computation graph coverage {row_identifier(row, index)} "
                    f"references unknown test_id {test_id!r}"
                )
    return rows


def check_runner_closure_map(
    path: Path,
    errors: list[str],
    *,
    module_ids: set[str],
    test_ids: set[str],
) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "runner closure map",
        [
            "runner_step",
            "check_id",
            "module_id",
            "public_function",
            "input_paths",
            "result_paths",
            "test_ids",
            "closure_status",
        ],
        errors,
        require_rows=True,
    )
    rows = check_status_field(
        path,
        "runner closure map",
        "closure_status",
        CLOSURE_PASS_VALUES,
        errors,
        require_rows=False,
    )
    for index, row in enumerate(rows, start=2):
        module_id = clean_scalar(row.get("module_id"))
        if has_actionable_text(module_id) and module_ids and module_id not in module_ids:
            errors.append(
                f"runner closure map {row_identifier(row, index)} "
                f"references unknown module_id {module_id!r}"
            )
        for test_id in split_reference_values(row.get("test_ids")):
            if test_ids and test_id not in test_ids:
                errors.append(
                    f"runner closure map {row_identifier(row, index)} "
                    f"references unknown test_id {test_id!r}"
                )
    return rows


def check_golden_case_registry(path: Path, errors: list[str]) -> list[dict[str, str]]:
    check_csv_required_fields(
        path,
        "golden case registry",
        [
            "case_id",
            "purpose",
            "reference_basis",
            "input_path",
            "expected_behavior",
            "expected_result_path",
            "tolerance",
            "status",
        ],
        errors,
        require_rows=True,
    )
    rows = check_status_field(
        path,
        "golden case registry",
        "status",
        GOLDEN_CASE_PASS_VALUES,
        errors,
        require_rows=False,
    )
    for index, row in enumerate(rows, start=2):
        if is_truthy(row.get("blocks_production")):
            errors.append(
                "production gate blocked by golden case registry "
                f"{row_identifier(row, index)} with blocks_production=true"
            )
    return rows


def check_project_semantic_gates(project_root: Path, errors: list[str]) -> None:
    """Validate gate consistency that cannot be caught by file/header checks."""
    gate_statuses = {
        project_coding_gate_status(project_root),
        markdown_gate_status(project_root / "handoff" / "coding_go_no_go.md"),
    }
    if PRODUCTION_ALLOWED not in gate_statuses:
        return

    acquisition_path = project_root / "references" / "acquisition" / "acquisition_handoff.yaml"
    acquisition_status = normalize_token(yaml_top_scalar(acquisition_path, "status"))
    if acquisition_status != ANALYSIS_ALLOWED:
        errors.append(
            "production gate requires references/acquisition/acquisition_handoff.yaml "
            f"status={ANALYSIS_ALLOWED!r}, got {acquisition_status or 'missing'}"
        )

    found = check_production_required_artifacts(project_root, errors)
    if "source coverage matrix" in found:
        check_source_coverage_for_production(found["source coverage matrix"], errors)
    if "calculation intent contract" in found:
        check_calculation_intent_contract(found["calculation intent contract"], errors)
    method_rows: list[dict[str, str]] = []
    if "method selection matrix" in found:
        method_rows = check_method_selection_matrix(found["method selection matrix"], errors)
    input_rows: list[dict[str, str]] = []
    if "input semantics ledger" in found:
        input_rows = check_input_semantics_ledger(found["input semantics ledger"], errors)
    module_rows: list[dict[str, str]] = []
    if "module asset registry" in found:
        module_rows = check_module_asset_registry(found["module asset registry"], errors)
    module_ids = actionable_row_ids(module_rows, "module_id")
    test_rows: list[dict[str, str]] = []
    if "test matrix" in found:
        test_rows = check_test_matrix(found["test matrix"], errors)
    test_ids = actionable_row_ids(test_rows, "test_id")
    formula_rows: list[dict[str, str]] = []
    if "formula inventory" in found:
        check_csv_required_fields(
            found["formula inventory"],
            "formula inventory",
            ["formula_id", "name", "inputs", "outputs", "units", "source_reference", "test_requirement"],
            errors,
            require_rows=True,
        )
        formula_rows = read_csv_rows(found["formula inventory"], errors, label="formula inventory")
    lookup_rows: list[dict[str, str]] = []
    if "lookup inventory" in found:
        check_csv_required_fields(
            found["lookup inventory"],
            "lookup inventory",
            ["lookup_id", "name", "inputs", "outputs", "source_reference", "interpolation_rule", "out_of_range_behavior", "test_requirement"],
            errors,
        )
        lookup_rows = read_csv_rows(found["lookup inventory"], errors, label="lookup inventory")
    branch_rows: list[dict[str, str]] = []
    if "branch inventory" in found:
        check_csv_required_fields(
            found["branch inventory"],
            "branch inventory",
            ["branch_id", "condition", "source_reference", "path_if_true", "path_if_false", "required_tests"],
            errors,
        )
        branch_rows = read_csv_rows(found["branch inventory"], errors, label="branch inventory")
    if method_rows and formula_rows:
        method_test_requirements = collect_reference_values(method_rows, "test_requirement")
        if not method_test_requirements:
            errors.append("production gate requires method selection rows to reference test requirements")
    if "computation graph coverage" in found:
        check_computation_graph_coverage(
            found["computation graph coverage"],
            errors,
            formula_rows=formula_rows,
            lookup_rows=lookup_rows,
            branch_rows=branch_rows,
            input_rows=input_rows,
            module_ids=module_ids,
            test_ids=test_ids,
        )
    if "runner closure map" in found:
        check_runner_closure_map(
            found["runner closure map"],
            errors,
            module_ids=module_ids,
            test_ids=test_ids,
        )
    if "chart candidate inventory" in found:
        check_csv_required_fields(
            found["chart candidate inventory"],
            "chart candidate inventory",
            ["chart_id", "title", "decision", "reason"],
            errors,
            require_rows=True,
        )
    if "golden case registry" in found:
        check_golden_case_registry(found["golden case registry"], errors)
    if "open questions" in found:
        check_blocking_csv_flags(found["open questions"], "open question", "blocks_coding", errors)
    if "user interaction decisions" in found:
        check_csv_required_fields(
            found["user interaction decisions"],
            "user interaction decisions",
            ["decision_id", "lifecycle_step", "decision_topic", "decision_status", "affected_artifacts"],
            errors,
        )
        check_blocking_csv_flags(
            found["user interaction decisions"],
            "user interaction decision",
            "blocks_progress",
            errors,
        )
    if "source conflicts" in found:
        check_blocking_csv_flags(found["source conflicts"], "source conflict", "blocks_coding", errors)
    if "assumption register" in found:
        check_blocking_csv_flags(found["assumption register"], "assumption", "blocks_production", errors)


def check_csv_headers(root: Path, headers: dict[str, str], errors: list[str]) -> None:
    for rel_path, expected in headers.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing CSV template: {rel_path}")
            continue
        actual = first_csv_line(path)
        if actual != expected:
            errors.append(f"CSV header mismatch in {rel_path}: expected {expected!r}, got {actual!r}")


def simple_yaml_top_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        match = YAML_KEY_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def check_yaml_required_keys(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, keys in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing YAML template: {rel_path}")
            continue
        present = simple_yaml_top_keys(read_text(path))
        for key in keys:
            if key not in present:
                errors.append(f"missing top-level key {key!r} in {rel_path}")


def check_text_required_phrases(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, phrases in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing text artifact: {rel_path}")
            continue
        text = read_text(path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"missing required phrase {phrase!r} in {rel_path}")


def check_lifecycle_single_source(root: Path, errors: list[str]) -> None:
    lifecycle_path = root / "shared" / "lifecycle.md"
    if not lifecycle_path.exists():
        errors.append("missing lifecycle single source: shared/lifecycle.md")
        return

    for rel_path in LIFECYCLE_REDIRECT_PATHS:
        path = root / rel_path
        if not path.exists():
            continue
        text = read_text(path)
        non_blank_lines = [line for line in text.splitlines() if line.strip()]
        if len(non_blank_lines) > 5:
            errors.append(
                f"{rel_path} must stay a short redirect; move lifecycle rules to shared/lifecycle.md"
            )
        if "shared/lifecycle.md" not in text or "consolidated" not in text.lower():
            errors.append(f"{rel_path} must redirect readers to shared/lifecycle.md")


def check_no_mojibake_markers(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_FILE_SUFFIXES:
            continue
        if any(part in FORBIDDEN_CACHE_NAMES for part in path.parts):
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        if any(marker in text for marker in MOJIBAKE_MARKERS):
            rel_path = path.relative_to(root).as_posix()
            errors.append(f"mojibake marker found in {rel_path}")


def check_static_html_delivery_guard(project_root: Path, errors: list[str]) -> None:
    """Catch static HTML/report-only projects before they are called web apps."""
    html_files = [
        path for path in project_root.rglob("*.html")
        if ".pytest_cache" not in path.parts and "__pycache__" not in path.parts
    ]
    if not html_files:
        return

    runtime_paths = [
        "webapp/app.py",
        "webapp/routes.py",
        "webapp/form_utils.py",
        "src/pkg/books/example_book/book_runner.py",
        "tests/smoke/test_web_routes.py",
    ]
    missing = [rel_path for rel_path in runtime_paths if not (project_root / rel_path).exists()]
    if missing:
        errors.append(
            "material state static_report_or_cli_only: report-only output is not a deployable "
            "web system; static HTML/report HTML alone is not a production-ready web calculation "
            f"system; missing runtime artifacts: {', '.join(missing)}. Remediate through "
            "08->09->10->11->12a->12b->12c->13->14 and add webapp, report renderers, "
            "mandatory Marimo review/admin bridge, import/export outputs, deployment files, and "
            "smoke tests."
            )


def check_web_complete_gate_status(project_root: Path, errors: list[str]) -> None:
    handoff_path = project_root / "handoff" / "implementation_handoff.yaml"
    handoff_status = normalize_token(yaml_top_scalar(handoff_path, "status"))
    coding_status = project_coding_gate_status(project_root)
    markdown_status = markdown_gate_status(project_root / "handoff" / "coding_go_no_go.md")
    if handoff_status == "prototype_allowed" or coding_status == "prototype_allowed" or markdown_status == "prototype_allowed":
        errors.append(
            "web-complete cannot be claimed while handoff or coding gate is prototype_allowed"
        )
    if coding_status != PRODUCTION_ALLOWED:
        errors.append(
            "web-complete requires handoff/implementation_handoff.yaml "
            f"coding_gate.status={PRODUCTION_ALLOWED!r}, got {coding_status or 'missing'}"
        )
    if markdown_status and markdown_status != PRODUCTION_ALLOWED:
        errors.append(
            "web-complete requires handoff/coding_go_no_go.md "
            f"status={PRODUCTION_ALLOWED!r}, got {markdown_status}"
        )


def check_web_complete_placeholders(project_root: Path, errors: list[str]) -> None:
    for rel_path in WEB_COMPLETE_PLACEHOLDER_SCAN_PATHS:
        path = project_root / rel_path
        if not path.exists():
            continue
        text = read_text(path)
        for token in WEB_COMPLETE_FORBIDDEN_PROJECT_TOKENS:
            if token in text:
                errors.append(
                    f"web-complete project artifact contains unresolved placeholder "
                    f"{token!r}: {rel_path}"
                )


def load_json_object(path: Path, errors: list[str], *, label: str) -> dict:
    if not path.exists():
        errors.append(f"missing {label}: {path.as_posix()}")
        return {}
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"could not parse {label}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{label} must be a JSON object")
        return {}
    return data


def check_example_input_payload(project_root: Path, errors: list[str]) -> dict:
    data = load_json_object(
        project_root / "tests" / "smoke" / "example_input.json",
        errors,
        label="web-complete example input",
    )
    project = data.get("project")
    if not isinstance(project, dict):
        errors.append("web-complete example input requires a project object")
    else:
        for key in ("project_id", "case_id"):
            if not has_actionable_text(project.get(key)):
                errors.append(f"web-complete example input requires actionable project.{key}")
        if any(str(project.get(key, "")).startswith("EXAMPLE") for key in ("project_id", "case_id")):
            errors.append("web-complete example input still uses EXAMPLE placeholder IDs")

    inputs = data.get("inputs")
    if not isinstance(inputs, dict) or not inputs:
        errors.append("web-complete example input requires a non-empty inputs object")
        return data
    checks = inputs.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("web-complete example input requires non-empty inputs.checks")
    return data


def project_book_name(project_root: Path) -> str:
    handoff_path = project_root / "handoff" / "implementation_handoff.yaml"
    book_name = yaml_top_scalar(handoff_path, "book_name")
    if book_name:
        return book_name
    books_root = project_root / "src" / "pkg" / "books"
    if books_root.exists():
        for path in sorted(books_root.iterdir()):
            if (path / "book_runner.py").exists():
                return path.name
    return ""


def purge_project_modules() -> None:
    for name in list(sys.modules):
        if name == "webapp" or name.startswith("webapp.") or name == "pkg" or name.startswith("pkg."):
            sys.modules.pop(name, None)


def status_value(value: object) -> str:
    if hasattr(value, "value"):
        return normalize_token(getattr(value, "value"))
    return normalize_token(value)


def object_field(value: object, name: str, default: object = None) -> object:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def check_chart_contract(charts: list[object], errors: list[str]) -> None:
    """Validate emitted charts generically without requiring a fixed chart set."""
    for index, chart in enumerate(charts):
        context = f"BookResult.charts[{index}]"
        if not object_field(chart, "chart_id"):
            errors.append(f"{context} is missing chart_id")
        if not object_field(chart, "title"):
            errors.append(f"{context} is missing title")

        series_list = list(object_field(chart, "series", []) or [])
        if not series_list:
            errors.append(f"{context} is missing data series")

        source_paths = list(object_field(chart, "source_result_paths", []) or [])
        series_paths: list[object] = []
        for series in series_list:
            series_paths.extend(list(object_field(series, "result_paths", []) or []))
        if not source_paths and not series_paths:
            errors.append(f"{context} must include source_result_paths or per-series result_paths")


def check_marimo_review_app_imports(project_root: Path, errors: list[str]) -> None:
    previous_path = list(sys.path)
    purge_project_modules()
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "src"))
    try:
        for rel_path in (
            "apps/review/calculation_review.py",
            "apps/review/admin_formula_review.py",
        ):
            path = project_root / rel_path
            if not path.exists():
                continue
            module_name = f"ecs_validator_{Path(rel_path).stem}"
            spec = importlib.util.spec_from_file_location(module_name, path)
            if spec is None or spec.loader is None:
                errors.append(f"web-complete Marimo review app is not importable: {rel_path}")
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            app = getattr(module, "app", None)
            if app is None:
                errors.append(f"web-complete Marimo review app missing app object: {rel_path}")
            message = getattr(app, "message", "")
            if message and "Marimo is not installed" not in message:
                errors.append(
                    f"web-complete Marimo fallback message is incomplete in {rel_path}"
                )
    except Exception as exc:  # pragma: no cover - validator reports import failures.
        errors.append(f"web-complete Marimo review app import failed: {exc}")
    finally:
        sys.path[:] = previous_path
        purge_project_modules()


def check_web_complete_runtime_closure(project_root: Path, errors: list[str]) -> None:
    example_data = check_example_input_payload(project_root, errors)
    if not example_data:
        return

    book_name = project_book_name(project_root)
    if not book_name:
        errors.append("web-complete runtime closure could not determine book_name")
        return

    previous_path = list(sys.path)
    purge_project_modules()
    sys.path.insert(0, str(project_root))
    sys.path.insert(0, str(project_root / "src"))
    try:
        form_utils = importlib.import_module("webapp.form_utils")
        book_runner = importlib.import_module(f"pkg.books.{book_name}.book_runner")
        report_context_module = importlib.import_module(f"pkg.books.{book_name}.report_context")
        html_renderer = importlib.import_module("pkg.report.html_renderer")
        review_bridge = importlib.import_module("pkg.review.bridge")

        book_input = form_utils.build_case_input_from_form(example_data)
        result = book_runner.run_book(book_input)
        checks = list(getattr(result, "checks", []) or [])
        if not checks:
            errors.append("web-complete runtime closure requires non-empty BookResult.checks")
        elif not any(status_value(getattr(check, "status", "")) not in {"", "not_evaluated", "needs_confirmation"} for check in checks):
            errors.append("web-complete runtime closure requires at least one evaluated CheckResult")

        if not any(getattr(check, "formula_traces", None) for check in checks):
            errors.append("web-complete runtime closure requires formula traces on BookResult.checks")
        for check_index, check in enumerate(checks):
            traces = list(getattr(check, "formula_traces", []) or [])
            if not traces:
                errors.append(f"web-complete runtime closure requires formula traces on BookResult.checks[{check_index}]")
            for trace_index, trace in enumerate(traces):
                context = f"BookResult.checks[{check_index}].formula_traces[{trace_index}]"
                if not object_field(trace, "formula_id"):
                    errors.append(f"{context} is missing formula_id")
                if not object_field(trace, "source_reference"):
                    errors.append(f"{context} is missing source_reference")
                if not object_field(trace, "result_path"):
                    errors.append(f"{context} is missing result_path")

        charts = list(getattr(result, "charts", []) or [])
        check_chart_contract(charts, errors)

        report_context = report_context_module.build_report_context(result)
        html_context = html_renderer.build_html_report_context(book_input, result, report_context)
        html = html_renderer.render_a4_html_report(html_context)
        for section in WEB_COMPLETE_REQUIRED_REPORT_SECTIONS:
            if section not in html:
                errors.append(f"web-complete report is missing required section: {section}")
        for phrase in WEB_COMPLETE_FORBIDDEN_REPORT_PHRASES:
            if phrase in html:
                errors.append(f"web-complete report contains incomplete placeholder phrase: {phrase}")

        with TemporaryDirectory(prefix="ecs_review_validator_") as tmp_dir:
            review_root = Path(tmp_dir)
            session = review_bridge.write_review_session(
                book_input,
                result,
                report_context,
                root=review_root,
            )
            if session.get("status") != "ready_for_review":
                errors.append("web-complete review session must be ready_for_review")
            for key in (
                "input_path",
                "result_path",
                "report_context_path",
                "review_state_path",
            ):
                path_value = session.get(key)
                if not path_value or not Path(path_value).exists():
                    errors.append(f"web-complete review session did not write {key}")
            loaded_session = review_bridge.read_review_session(
                session["session_id"],
                root=review_root,
            )
            if loaded_session["state"].get("review_decision") != "pending":
                errors.append("web-complete review session state must start pending")
            decision_state = review_bridge.append_review_decision(
                session["session_id"],
                reviewer="validator",
                decision="accepted",
                notes="validator smoke",
                root=review_root,
            )
            if decision_state.get("review_decision") != "accepted":
                errors.append("web-complete review decision append did not update state")
            if not (review_root / "review_decisions.jsonl").exists():
                errors.append("web-complete review decision log was not written")
    except Exception as exc:  # pragma: no cover - validator must report import/runtime failures cleanly.
        errors.append(f"web-complete runtime closure failed: {exc}")
    finally:
        sys.path[:] = previous_path
        purge_project_modules()


def check_web_complete_delivery(project_root: Path, errors: list[str]) -> None:
    """Validate the strict web-complete delivery shape."""
    for rel_path in WEB_COMPLETE_REQUIRED_PROJECT_PATHS:
        check_exists(project_root, rel_path, errors)
    check_text_required_phrases(project_root, WEB_COMPLETE_TEXT_REQUIRED_PHRASES, errors)
    check_marimo_review_app_imports(project_root, errors)
    check_web_complete_gate_status(project_root, errors)
    check_web_complete_placeholders(project_root, errors)
    check_web_complete_runtime_closure(project_root, errors)



def check_skill_frontmatter(
    root: Path,
    rel_path: str,
    errors: list[str],
    *,
    expected_version: str | None = None,
) -> None:
    path = root / rel_path
    if not path.exists():
        errors.append(f"missing skill file: {rel_path}")
        return
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"missing YAML frontmatter in {rel_path}")
        return
    body = match.group("body")
    if not re.search(r"^name:\s*\S+", body, re.MULTILINE):
        errors.append(f"missing frontmatter name in {rel_path}")
    if not re.search(r"^description:\s*.+", body, re.MULTILINE):
        errors.append(f"missing frontmatter description in {rel_path}")
    version_match = re.search(r"^version:\s*(.+)", body, re.MULTILINE)
    if expected_version and version_match:
        actual = clean_scalar(version_match.group(1))
        if actual != expected_version:
            errors.append(
                f"frontmatter version mismatch in {rel_path}: "
                f"expected {expected_version!r}, got {actual!r}"
            )


def check_qoder_agent_frontmatter(root: Path, rel_path: str, errors: list[str]) -> None:
    path = root / rel_path
    if not path.exists():
        errors.append(f"missing Qoder agent file: {rel_path}")
        return
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"missing YAML frontmatter at file start in Qoder agent: {rel_path}")
        return
    body = match.group("body")
    for key in ("name", "description", "tools"):
        if not re.search(rf"^{key}:\s*.+", body, re.MULTILINE):
            errors.append(f"missing frontmatter {key} in Qoder agent: {rel_path}")


def check_qoder_agents(root: Path, errors: list[str]) -> None:
    agents_dir = root / ".qoder" / "agents"
    if not agents_dir.exists():
        errors.append("missing Qoder agents directory: .qoder/agents")
        return
    expected = set(QODER_AGENT_FILES)
    found = {
        path.relative_to(root).as_posix()
        for path in agents_dir.glob("*.md")
        if path.is_file()
    }
    for rel_path in sorted(expected - found):
        errors.append(f"missing Qoder agent file: {rel_path}")
    for rel_path in sorted(found - expected):
        errors.append(f"unexpected Qoder agent Markdown file: {rel_path}")
    for rel_path in sorted(found & expected):
        check_qoder_agent_frontmatter(root, rel_path, errors)


def validate_package(package_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    expected_version = clean_scalar(contract.get("version"))
    for rel_path in contract["package_required_paths"]:
        check_exists(package_root, rel_path, errors)
    for rel_path in contract["skill_files"]:
        check_skill_frontmatter(package_root, rel_path, errors, expected_version=expected_version)
    check_csv_headers(package_root, contract["csv_headers"], errors)
    check_yaml_required_keys(package_root, contract["yaml_required_keys"], errors)
    check_text_required_phrases(package_root, contract.get("text_required_phrases", {}), errors)
    check_lifecycle_single_source(package_root, errors)
    check_no_mojibake_markers(package_root, errors)
    return errors


def validate_core_profile(package_root: Path, contract: dict) -> list[str]:
    errors = validate_package(package_root, contract)
    for rel_path in sorted(CORE_FORBIDDEN_ROOT_PATHS):
        check_absent(package_root, rel_path, errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_adapters_light_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    expected_version = manifest_version(package_root)
    required = [
        "AGENTS.md",
        "adapters/agent-entrypoints.md",
        "adapters/mcp-recommendations.md",
        ".agents/skills/engineering-calc-system/SKILL.md",
        ".opencode/skills/engineering-calc-system/SKILL.md",
        ".trae/project_rules.md",
        ".trae/rules/engineering-calc-system.md",
    ]
    for rel_path in required:
        check_exists(package_root, rel_path, errors)
    for rel_path in [
        ".agents/skills/engineering-calc-system/SKILL.md",
        ".opencode/skills/engineering-calc-system/SKILL.md",
    ]:
        check_skill_frontmatter(package_root, rel_path, errors, expected_version=expected_version)
    check_text_required_phrases(
        package_root,
        {
            "AGENTS.md": ["Chinese/English interactive UI switch", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress.md", "dual closure", "Marimo review/admin pages", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            "adapters/agent-entrypoints.md": ["Chinese/English switching", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress_ledger.md", "dual closure", "Marimo review/admin closure", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".agents/skills/engineering-calc-system/SKILL.md": ["Chinese/English interactive UI switch", "lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress.md", "dual closure", "Marimo review/admin pages", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".opencode/skills/engineering-calc-system/SKILL.md": ["Chinese/English interactive UI switch", "lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress.md", "dual closure", "Marimo review/admin pages", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".trae/project_rules.md": ["Chinese/English interactive UI switch", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress.md", "dual closure", "Marimo review/admin pages", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".trae/rules/engineering-calc-system.md": ["Chinese/English interactive UI switch", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "progress.md", "dual closure", "Marimo review/admin pages", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
        },
        errors,
    )
    check_absent(package_root, ".qoder", errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_qoder_addon_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    expected_version = manifest_version(package_root)
    required = [
        ".qoder/skills/engineering-calc-system/SKILL.md",
        ".qoder/skills/engineering-calc-system/reference.md",
        ".qoder/skills/engineering-calc-system/qoder_quickstart.md",
        ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html",
        ".qoder/references/engineering-calc-system.md",
        *QODER_AGENT_FILES,
    ]
    for rel_path in required:
        check_exists(package_root, rel_path, errors)
    check_qoder_agents(package_root, errors)
    check_skill_frontmatter(
        package_root,
        ".qoder/skills/engineering-calc-system/SKILL.md",
        errors,
        expected_version=expected_version,
    )
    check_text_required_phrases(
        package_root,
        {
            ".qoder/skills/engineering-calc-system/SKILL.md": ["Qoder Architecture", "agent-first", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "task_brief.md", "progress.md", "dual closure", "qoder_quickstart.md", "Static Report Triage", "static_report_or_cli_only", "A4 HTML First", "print-ready A4 HTML", "calculation semantic closure", "calculation_intent_contract.md", "runner_closure_map.csv", "golden_case_registry.csv", "Marimo Review Closure", "/api/review/session", "apps/review/admin_formula_review.py", "ADMIN_REVIEW_TOKEN"],
            ".qoder/skills/engineering-calc-system/reference.md": ["/api/i18n/<lang>", "Marimo Review Closure", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/skills/engineering-calc-system/qoder_quickstart.md": ["Qoder Package Self-Check", "Direct QODER Skill", "QODER Project overlay", "Complete core project", *BEHAVIOR_ENGINEERING_DOCS, "route card", "progress.md", "validate_artifacts.py --package-root", "Static Report Triage", "static_report_or_cli_only", "A4 HTML First", "print-ready A4 HTML", "calculation semantic closure", "input_semantics_ledger.csv", "computation_graph_coverage.csv", "Marimo Review Closure", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/skills/engineering-calc-system/assets/lifecycle-console.html": [f"v{expected_version}", "12a", "12b", "12c", "14", "route_confirmed", "batch_import"],
            ".qoder/agents/engineering-calc-system.md": ["Qoder Architecture", "agent-first", "Stable ASCII Contract", "shared/lifecycle.md", *BEHAVIOR_ENGINEERING_DOCS, "task brief", "progress.md", "dual closure", "static_report_or_cli_only", "A4 HTML first", "print-ready A4 HTML", "calculation semantic closure", "method_selection_matrix.csv", "golden_case_registry.csv", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/agents/engineering-calc-reference-acquirer.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file"],
            ".qoder/agents/engineering-calc-source-intake.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file"],
            ".qoder/agents/engineering-calc-logic-extractor.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file"],
            ".qoder/agents/engineering-calc-module-worker.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file", "run_book(BookInput) -> BookResult"],
            ".qoder/agents/engineering-calc-interface-worker.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file", "/api/i18n/<lang>", "reports/*.html", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/agents/engineering-calc-verification-worker.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file", "web-complete", "static_report_or_cli_only", "html_a4", "chart data tables", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/agents/engineering-calc-release-worker.md": ["Qoder Worker Contract", "task brief", "completion evidence category", "requested shared file", "/health", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
            ".qoder/references/engineering-calc-system.md": [*BEHAVIOR_ENGINEERING_DOCS, "progress.md", "/api/i18n/<lang>", "static_report_or_cli_only", "A4 HTML first", "BookResult.charts", "calculation semantic closure", "runner_closure_map.csv", "Marimo Review Closure", "/api/review/session", "ADMIN_REVIEW_TOKEN"],
        },
        errors,
    )
    check_absent(package_root, "SKILL.md", errors)
    check_absent(package_root, "core", errors)
    check_absent(package_root, ".qoder/agents/reference.md", errors)
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_singlefile_profile(package_root: Path) -> list[str]:
    errors: list[str] = []
    check_exists(package_root, "engineering-calculation-system.all-in-one.md", errors)
    for path in package_root.iterdir():
        if path.name not in SINGLEFILE_ALLOWED_FILES:
            errors.append(f"unexpected singlefile profile path: {path.name}")
    text_path = package_root / "engineering-calculation-system.all-in-one.md"
    if text_path.exists():
        text = read_text(text_path)
        for phrase in [
            "Engineering Calculation System - All-in-One Skill Pack",
            "## SKILL.md",
            "## skills/00-engineering-calculation-router.skill.md",
            "## shared/multi-agent-orchestration.md",
            "## shared/lifecycle.md",
            "## shared/execution-discipline.md",
            "## shared/planning-discipline.md",
            "## shared/review-feedback-discipline.md",
            "## shared/version-control-discipline.md",
            "## shared/completion-evidence.md",
            "## shared/systematic-debugging.md",
            "## shared/copyright-and-access-policy.md",
            "## scripts/ecs_execution.py",
        ]:
            if phrase not in text:
                errors.append(f"singlefile output missing phrase: {phrase!r}")
    check_no_cache_artifacts(package_root, errors)
    return errors


def validate_profile(package_root: Path, profile: str, contract: dict | None) -> list[str]:
    if profile == "core":
        if contract is None:
            return ["core profile requires schemas/artifact_contracts.json"]
        return validate_core_profile(package_root, contract)
    if profile == "adapters-light":
        return validate_adapters_light_profile(package_root)
    if profile == "qoder-addon":
        return validate_qoder_addon_profile(package_root)
    if profile == "singlefile":
        return validate_singlefile_profile(package_root)
    return [f"unknown profile: {profile}"]


def validate_project(project_root: Path, contract: dict, *, delivery: str = "standard") -> list[str]:
    errors: list[str] = []
    for rel_path in contract["project_required_paths"]:
        check_exists(project_root, rel_path, errors)
    check_csv_headers(project_root, contract["project_csv_headers"], errors)
    check_yaml_required_keys(project_root, contract.get("project_yaml_required_keys", {}), errors)
    check_text_required_phrases(project_root, contract.get("project_text_required_phrases", {}), errors)
    check_no_mojibake_markers(project_root, errors)
    check_static_html_delivery_guard(project_root, errors)
    if delivery == "web-complete":
        check_web_complete_delivery(project_root, errors)
    check_project_semantic_gates(project_root, errors)
    return errors


def capability_report_lines() -> list[str]:
    """Summarize optional host capabilities without making them validation blockers."""
    marimo_available = importlib.util.find_spec("marimo") is not None
    marimo_configured = marimo_available and bool(os.environ.get("ADMIN_REVIEW_TOKEN"))
    latex_tool = shutil.which("latexmk") or shutil.which("pdflatex")
    docker_tool = shutil.which("docker")
    if marimo_configured:
        marimo_line = "marimo_review: configured"
    elif marimo_available:
        marimo_line = "marimo_review: available (set ADMIN_REVIEW_TOKEN to enable review)"
    else:
        marimo_line = "marimo_review: disabled (install with: python -m pip install marimo)"

    return [
        f"python: available ({platform.python_version()})",
        marimo_line,
        f"latex: available ({Path(latex_tool).name})" if latex_tool else "latex: missing (final report falls back to HTML A4)",
        "docker: available" if docker_tool else "docker: missing (optional)",
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", default=".", help="Skill pack root directory")
    parser.add_argument("--profile", default="core", choices=sorted(PROFILE_CHOICES), help="Release profile to validate")
    parser.add_argument("--project", help="Generated engineering calculation project root")
    parser.add_argument(
        "--delivery",
        default="standard",
        choices=sorted(DELIVERY_CHOICES),
        help="Generated project delivery contract to validate",
    )
    args = parser.parse_args(argv)

    package_root = Path(args.package_root).resolve()
    contract = load_contract(package_root) if (package_root / "schemas" / "artifact_contracts.json").exists() else None
    errors = validate_profile(package_root, args.profile, contract)

    if args.project:
        if contract is None:
            errors.append("--project validation requires schemas/artifact_contracts.json under --package-root")
        else:
            errors.extend(
                validate_project(
                    Path(args.project).resolve(),
                    contract,
                    delivery=args.delivery,
                )
            )

    if errors:
        print("Artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Artifact validation passed.")
    if args.project:
        print("Capability report:")
        for line in capability_report_lines():
            print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
