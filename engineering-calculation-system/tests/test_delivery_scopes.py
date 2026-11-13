from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import sys
import tomllib
from pathlib import Path

import pytest

CORE = Path(__file__).resolve().parents[1] / "core/engineering-calculation-system"
TEMPLATE = CORE / "project_template/engineering_calc_project"
CONTRACT = json.loads((CORE / "schemas/artifact_contracts.json").read_text(encoding="utf-8"))


def load_module(name: str, path: Path):
    # Keep importlib's loader from creating build residue in canonical sources.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load_module("nimo_scope_validator", CORE / "scripts/validate_artifacts.py")
policy = load_module("nimo_delivery_policy", CORE / "scripts/delivery_policy.py")


def project_fixture(tmp_path: Path, mode: str, *, notebook_files: bool = False) -> Path:
    project = tmp_path / "project"
    shutil.copytree(TEMPLATE, project, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    for relative in ("handoff/implementation_handoff.yaml", "handoff/coding_go_no_go.md"):
        path = project / relative
        text = path.read_text(encoding="utf-8").replace("prototype_allowed", "production_allowed")
        text = text.replace("delivery_mode: web-complete", f"delivery_mode: {mode}")
        path.write_text(text, encoding="utf-8")
    removals = []
    if not notebook_files:
        removals.extend(("apps", "tests/unit/test_marimo_review.py", "webapp/templates/admin_review.html",
                         "deploy/systemd/engineering-calc-review.service", "deploy/systemd/engineering-calc-formula-admin.service"))
    if mode in {"core-only", "report-only"}:
        removals.extend(("webapp", "deploy", "release", "latex", "src/pkg/review", "src/pkg/core/capabilities.py",
                         "src/pkg/report/latex_renderer.py", "src/pkg/report/report_selector.py",
                         "tests/smoke/test_web_routes.py", "tests/smoke/test_latex_report.py"))
    if mode == "core-only":
        removals.extend(("src/pkg/report", "src/pkg/books/example_book/report_context.py"))
    for relative in removals:
        path = project / relative
        assert path.resolve().is_relative_to(project.resolve())
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)
    return project


def update_csv(path: Path, **changes: str) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields, rows = reader.fieldnames, list(reader)
    assert fields and rows
    rows[0].update(changes)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize(("outputs", "expected"), [
    (["module"], "core-only"), (["batch"], "core-only"), (["cli"], "core-only"),
    (["report"], "report-only"), (["report", "batch"], "report-only"),
    (["web", "prototype"], "prototype-web"), (["online-calculator"], "web-complete"),
    ([], "web-complete"),
])
def test_explicit_deliverables_select_their_scope(outputs, expected) -> None:
    assert policy.select_delivery(outputs) == expected
    assert policy.select_delivery(outputs, "core-only") == "core-only"


@pytest.mark.parametrize("mode", ["core-only", "report-only"])
def test_production_scope_validates_without_web_notebooks_or_deployment(tmp_path: Path, mode: str) -> None:
    project = project_fixture(tmp_path, mode)
    assert not (project / "webapp").exists()
    assert not (project / "apps").exists()
    assert validator.validate_project(project, CONTRACT, delivery=mode) == []
    # Replay compares actual numeric results via pkg.interfaces, with no web package.
    errors = []
    validator.check_web_complete_runtime_closure(project, errors, delivery=mode)
    assert errors == []


@pytest.mark.parametrize("mode", ["core-only", "report-only"])
def test_production_scope_cannot_bypass_no_go(tmp_path: Path, mode: str) -> None:
    project = project_fixture(tmp_path, mode)
    for relative in ("handoff/implementation_handoff.yaml", "handoff/coding_go_no_go.md"):
        path = project / relative
        path.write_text(path.read_text(encoding="utf-8").replace("production_allowed", "no_go"), encoding="utf-8")
    errors = validator.validate_project(project, CONTRACT, delivery=mode)
    assert any("coding_gate.status='production_allowed'" in error for error in errors)


@pytest.mark.parametrize("mode", ["core-only", "report-only"])
def test_verified_label_does_not_hide_wrong_golden_number(tmp_path: Path, mode: str) -> None:
    project = project_fixture(tmp_path, mode)
    update_csv(project / "verification/golden_case_registry.csv",
               expected_behavior="expected_value=99; expected_status=PASS; status_path=checks[0].status", status="verified")
    errors = validator.validate_project(project, CONTRACT, delivery=mode)
    assert any("golden-case replay failed" in error for error in errors)


@pytest.mark.parametrize(("relative", "changes", "message"), [
    ("references/acquisition/source_coverage_matrix.csv", {"covered": "no", "current_source_id": ""}, "source requirement"),
    ("analysis/02_logic_blueprint/input_semantics_ledger.csv", {"unit": "", "blocks_production": "true"}, "input semantics ledger"),
])
def test_scope_keeps_source_and_unit_gates(tmp_path: Path, relative: str, changes: dict, message: str) -> None:
    project = project_fixture(tmp_path, "core-only")
    update_csv(project / relative, **changes)
    errors = validator.validate_project(project, CONTRACT, delivery="core-only")
    assert any(message in error for error in errors)


def test_scope_keeps_formula_trace_and_real_input_requirements(tmp_path: Path) -> None:
    project = project_fixture(tmp_path, "core-only")
    runner = project / "src/pkg/books/example_book/book_runner.py"
    original = runner.read_text(encoding="utf-8")
    assert "formula_traces=[trace]" in original
    runner.write_text(original.replace("formula_traces=[trace]", "formula_traces=[]"), encoding="utf-8")
    errors = validator.validate_project(project, CONTRACT, delivery="core-only")
    assert any("requires formula traces" in error for error in errors)
    data = json.loads((project / "tests/smoke/example_input.json").read_text(encoding="utf-8"))
    data["inputs"]["checks"] = []
    (project / "tests/smoke/example_input.json").write_text(json.dumps(data), encoding="utf-8")
    errors = validator.validate_project(project, CONTRACT, delivery="core-only")
    assert any("requires non-empty inputs.checks" in error for error in errors)


def test_web_complete_without_notebooks_retains_replay_and_json_evidence(tmp_path: Path) -> None:
    project = project_fixture(tmp_path, "web-complete")
    assert validator.validate_project(project, CONTRACT, delivery="web-complete") == []
    (project / "src/pkg/review/bridge.py").unlink()
    errors = validator.validate_project(project, CONTRACT, delivery="web-complete")
    assert any("src/pkg/review/bridge.py" in error for error in errors)


def test_requested_marimo_still_requires_its_adapter(tmp_path: Path) -> None:
    project = project_fixture(tmp_path, "web-complete")
    errors = validator.validate_project(project, CONTRACT, delivery="web-complete", review_adapter="marimo")
    assert any("apps/review/calculation_review.py" in error for error in errors)


def test_prototype_scope_needs_a_gate_and_does_not_require_deployment(tmp_path: Path) -> None:
    project = project_fixture(tmp_path, "prototype-web")
    shutil.rmtree(project / "deploy")
    shutil.rmtree(project / "release")
    for relative in ("handoff/implementation_handoff.yaml", "handoff/coding_go_no_go.md"):
        path = project / relative
        path.write_text(path.read_text(encoding="utf-8").replace("production_allowed", "prototype_allowed"), encoding="utf-8")
    assert validator.validate_project(project, CONTRACT, delivery="prototype-web") == []
    handoff = project / "handoff/implementation_handoff.yaml"
    handoff.write_text(handoff.read_text(encoding="utf-8").replace("prototype_allowed", "no_go"), encoding="utf-8")
    assert any("prototype-web requires" in error for error in validator.validate_project(project, CONTRACT, delivery="prototype-web"))


def test_marimo_is_opt_in_for_runtime_dependencies_and_services() -> None:
    dependencies = tomllib.loads((TEMPLATE / "pyproject.toml").read_text(encoding="utf-8"))["project"]["optional-dependencies"]
    assert not any(item.startswith("marimo") for item in dependencies["web"])
    assert any(item.startswith("marimo") for item in dependencies["review"])
    compose = (TEMPLATE / "deploy/docker-compose.yml").read_text(encoding="utf-8")
    assert compose.count('profiles: ["review"]') == 2
    assert "ARG ENABLE_MARIMO_REVIEW=false" in (TEMPLATE / "deploy/Dockerfile").read_text(encoding="utf-8")
    assert "if ! review_enabled; then" in (TEMPLATE / "deploy/one_click_deploy.sh").read_text(encoding="utf-8")
