from __future__ import annotations

import importlib.metadata
import importlib.util
import os
import platform
import shutil
import sys
from typing import Any, Mapping


def _module_capability(module_name: str, package_name: str, install_command: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return {
            "status": "missing",
            "available": False,
            "version": None,
            "path": None,
            "install_command": install_command,
        }

    try:
        version = importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"

    return {
        "status": "available",
        "available": True,
        "version": version,
        "path": spec.origin,
        "install_command": install_command,
    }


def _tool_capability(names: list[str], install_hint: str) -> dict[str, Any]:
    for name in names:
        path = shutil.which(name)
        if path:
            return {
                "status": "available",
                "available": True,
                "tool": name,
                "path": path,
                "install_hint": install_hint,
            }
    return {
        "status": "missing",
        "available": False,
        "tool": None,
        "path": None,
        "install_hint": install_hint,
    }


def _path_url(value: str, fallback: str) -> str:
    candidate = (value or fallback).strip() or fallback
    if not candidate.startswith("/"):
        candidate = f"/{candidate}"
    if not candidate.endswith("/"):
        candidate = f"{candidate}/"
    return candidate


def _service_url(value: str, fallback: str) -> str:
    candidate = (value or fallback).strip() or fallback
    if not candidate.endswith("/"):
        candidate = f"{candidate}/"
    return candidate


def detect_capabilities(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Detect optional runtime capabilities without installing anything."""
    env = os.environ if env is None else env
    marimo = _module_capability("marimo", "marimo", "python -m pip install marimo")
    latex = _tool_capability(
        ["latexmk", "pdflatex"],
        "Install TeX Live, MiKTeX, or another distribution that provides latexmk or pdflatex.",
    )
    docker = _tool_capability(
        ["docker"],
        "Install Docker only when container deployment or local compose smoke tests are required.",
    )

    admin_token_set = bool(env.get("ADMIN_REVIEW_TOKEN"))
    review_shell_url = "/admin/review/"
    marimo_base_url = _path_url(env.get("MARIMO_BASE_URL", ""), review_shell_url)
    marimo_service_url = _service_url(env.get("MARIMO_SERVICE_URL", ""), "http://127.0.0.1:2718/")
    if marimo["available"] and admin_token_set:
        review_status = "configured"
    elif marimo["available"]:
        review_status = "available"
    else:
        review_status = "missing"

    if review_status == "configured":
        review_message = "Marimo review is configured. Start or proxy the calculation review service."
    elif marimo["available"]:
        review_message = "Marimo is installed. Set ADMIN_REVIEW_TOKEN and start the review service."
    else:
        review_message = "Install Marimo and set ADMIN_REVIEW_TOKEN to enable calculation review."

    return {
        "status": "ok",
        "capabilities": {
            "python": {
                "status": "available",
                "available": True,
                "version": platform.python_version(),
                "path": sys.executable,
                "implementation": platform.python_implementation(),
            },
            "marimo": marimo,
            "marimo_review": {
                "status": review_status,
                "available": marimo["available"],
                "configured": review_status == "configured",
                "admin_token_set": admin_token_set,
                "admin_url": marimo_base_url,
                "shell_url": review_shell_url,
                "service_url": marimo_service_url,
                "install_command": "python -m pip install marimo",
                "run_command": (
                    "marimo run apps/review/calculation_review.py "
                    f"--host 127.0.0.1 --port 2718 --base-url {marimo_base_url.rstrip('/')} "
                    "--headless --token --token-password <ADMIN_REVIEW_TOKEN>"
                ),
                "formula_admin_run_command": (
                    "marimo run apps/review/admin_formula_review.py "
                    f"--host 127.0.0.1 --port 2719 --base-url {marimo_base_url.rstrip('/')} "
                    "--headless --token --token-password <ADMIN_REVIEW_TOKEN>"
                ),
                "message": review_message,
            },
            "latex": latex,
            "docker": docker,
        },
    }
