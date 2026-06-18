from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any
import shutil
import subprocess
import zipfile

from jinja2 import Environment, FileSystemLoader


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


def to_plain(value: Any) -> Any:
    """Convert dataclasses and enums into Jinja-friendly plain values."""
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value


def latex_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return "".join(LATEX_ESCAPE_MAP.get(char, char) for char in text)


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
        "checks": plain_result.get("checks", []),
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


def _environment(template_dir: Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["latex_escape"] = latex_escape
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

    return {
        "status": "ok",
        "tool": toolchain["tool"],
        "tool_path": toolchain["path"],
        "pdf_path": pdf_path,
        "log": "\n".join(part for part in combined_output if part),
    }


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
