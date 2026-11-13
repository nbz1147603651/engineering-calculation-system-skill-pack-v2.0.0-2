from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import Any
import shutil
import subprocess
import zipfile

from jinja2 import Environment, FileSystemLoader

from .context_helpers import (
    report_assumptions_from_context,
    report_figures_from_context,
    report_sources_from_checks,
    to_plain,
)


LATEX_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return "".join(LATEX_ESCAPE_MAP.get(char, char) for char in text)


def flatten_dict(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    """Recursively flatten a nested dict/list into (path, leaf_value) pairs.

    Used by report templates to avoid dumping Python ``str(dict)`` repr into
    table cells. Dicts/lists are expanded into dotted paths (e.g.
    ``intersection.cycle_s``); scalars become a single pair with the given
    prefix as the path.
    """
    if isinstance(value, dict):
        pairs: list[tuple[str, Any]] = []
        for key, item in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            pairs.extend(flatten_dict(item, child_prefix))
        return pairs
    if isinstance(value, (list, tuple)):
        pairs = []
        for index, item in enumerate(value):
            child_prefix = f"{prefix}[{index}]" if prefix else f"[{index}]"
            pairs.extend(flatten_dict(item, child_prefix))
        return pairs
    return [(prefix, value)]


def join_list(value: Any, separator: str = "; ") -> str:
    """Render a value for LaTeX display; lists become separator-joined strings."""
    if isinstance(value, (list, tuple)):
        return separator.join(str(item) for item in value)
    return "" if value is None else str(value)


def build_latex_report_context(
    book_input: Any,
    book_result: Any,
    report_context: dict[str, Any] | None = None,
    *,
    lang: str = "en",
    report_status: str = "review",
    template_version: str = "default_engineering_calcbook-v1",
) -> dict[str, Any]:
    """Build presentation-only LaTeX context from trusted calculation outputs."""
    plain_input = to_plain(book_input)
    plain_result = to_plain(book_result)
    plain_report = to_plain(report_context or {})
    charts = plain_report.get("charts") or plain_result.get("charts", [])
    checks = plain_result.get("checks", [])
    sources = plain_report.get("sources") or report_sources_from_checks(checks)
    assumptions = report_assumptions_from_context(plain_input, plain_report)
    figures = report_figures_from_context(plain_report, plain_result)
    intermediate_values = plain_result.get("intermediate_values", {}) or {}
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
        "intermediate_values": intermediate_values,
        # Domain-specific traffic-signal fields are optional. Downstream books
        # populate them inside intermediate_values; the example scaffold does
        # not, so templates guard with {% if intersection %} and degrade to the
        # generic sections when absent.
        "intersection": intermediate_values.get("intersection"),
        "lane_groups": intermediate_values.get("lane_groups"),
        "phases": intermediate_values.get("phases"),
        "approaches": intermediate_values.get("approaches"),
        "traceability": {
            "formula_registry_version": plain_result.get("formula_registry_version", "unversioned"),
            "formula_hash": plain_result.get("formula_hash") or "untracked",
            "formula_published_at": plain_result.get("formula_published_at") or "not published",
            "report_template_version": template_version,
        },
    }


def _environment(template_dir: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["latex_escape"] = latex_escape
    env.filters["flatten_dict"] = flatten_dict
    env.filters["join_list"] = join_list
    return env


def detect_latex_toolchain() -> dict[str, Any]:
    """Detect a local LaTeX compiler suitable for strict PDF validation."""
    latexmk = shutil.which("latexmk")
    if latexmk:
        return {"available": True, "tool": "latexmk", "path": latexmk}

    pdflatex = shutil.which("pdflatex")
    if pdflatex:
        return {"available": True, "tool": "pdflatex", "path": pdflatex}

    return {"available": False, "tool": None, "path": None}


def render_latex_project_files(context: dict[str, Any], template_dir: Path, output_dir: Path) -> None:
    """Render a complete LaTeX project directory for local compilation."""
    if not template_dir.exists():
        raise FileNotFoundError(f"LaTeX template directory not found: {template_dir}")

    env = _environment(template_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(template_dir.rglob("*")):
        if path.is_dir():
            continue
        rel_path = path.relative_to(template_dir)
        target = output_dir / rel_path
        if path.suffix == ".j2":
            target = output_dir / Path(rel_path.as_posix()[:-3])
            rendered = env.get_template(rel_path.as_posix()).render(**context)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())


def compile_latex_project(context: dict[str, Any], template_dir: Path, output_dir: Path) -> dict[str, Any]:
    """Render and compile a LaTeX project. Success requires a generated main.pdf."""
    toolchain = detect_latex_toolchain()
    if not toolchain["available"]:
        raise RuntimeError("No local LaTeX compiler found. Install latexmk or pdflatex.")

    render_latex_project_files(context, template_dir, output_dir)
    if toolchain["tool"] == "latexmk":
        command = [
            str(toolchain["path"]),
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "main.tex",
        ]
    else:
        command = [
            str(toolchain["path"]),
            "-interaction=nonstopmode",
            "-halt-on-error",
            "main.tex",
        ]

    passes = 1 if toolchain["tool"] == "latexmk" else 2
    combined_output: list[str] = []
    for _ in range(passes):
        completed = subprocess.run(
            command,
            cwd=output_dir,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        combined_output.append(completed.stdout)
        combined_output.append(completed.stderr)
        if completed.returncode != 0:
            log = "\n".join(part for part in combined_output if part).strip()
            raise RuntimeError(f"LaTeX compilation failed:\n{log[-4000:]}")

    pdf_path = output_dir / "main.pdf"
    if not pdf_path.exists():
        log = "\n".join(part for part in combined_output if part).strip()
        raise RuntimeError(f"LaTeX compilation did not produce main.pdf:\n{log[-4000:]}")

    archive_path = _archive_compiled_pdf(pdf_path, context)

    return {
        "status": "ok",
        "tool": toolchain["tool"],
        "tool_path": toolchain["path"],
        "pdf_path": pdf_path,
        "archive_path": archive_path,
        "log": "\n".join(part for part in combined_output if part),
    }


def _archive_compiled_pdf(pdf_path: Path, context: dict[str, Any]) -> str | None:
    """Copy the compiled PDF into reports_pdf/ for retrieval. Best-effort.

    Archiving must never block the response: on any failure it returns ``None``
    and leaves a warning in the result dict rather than raising. The file is
    named ``<project_id>_<case_id>_<timestamp>.pdf`` when those fields are
    available, falling back to a generic timestamped name.
    """
    import os
    import time

    output_dir = os.environ.get("OUTPUT_DIR")
    if not output_dir:
        return None

    project = context.get("project") or {}
    project_id = str(project.get("project_id") or "calc").strip() or "calc"
    case_id = str(project.get("case_id") or "case").strip() or "case"
    safe_project = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in project_id)
    safe_case = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in case_id)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_project}_{safe_case}_{stamp}.pdf"

    archive_dir = Path(output_dir) / "reports_pdf"
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        target = archive_dir / filename
        shutil.copy2(pdf_path, target)
        return str(target)
    except OSError:
        return None


def render_latex_project_zip(context: dict[str, Any], template_dir: Path) -> bytes:
    """Render a complete LaTeX project as a zip file for Overleaf import."""
    if not template_dir.exists():
        raise FileNotFoundError(f"LaTeX template directory not found: {template_dir}")

    env = _environment(template_dir)
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(template_dir.rglob("*")):
            if path.is_dir():
                continue
            rel_path = path.relative_to(template_dir).as_posix()
            if path.suffix == ".j2":
                rendered = env.get_template(rel_path).render(**context)
                archive.writestr(rel_path[:-3], rendered.encode("utf-8"))
            else:
                archive.writestr(rel_path, path.read_bytes())
    return buffer.getvalue()
