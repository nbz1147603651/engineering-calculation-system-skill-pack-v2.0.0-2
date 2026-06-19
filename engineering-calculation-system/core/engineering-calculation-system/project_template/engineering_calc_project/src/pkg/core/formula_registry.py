from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY_DIR = PROJECT_ROOT / "data" / "formula_registry"
PUBLISH_LOG_DEFAULT = PROJECT_ROOT / "outputs" / "logs" / "formula_publish_log.csv"

SAFE_FUNCTIONS = {
    "abs": abs,
    "max": max,
    "min": min,
    "pow": pow,
    "round": round,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
}
SAFE_CONSTANTS = {"pi": math.pi, "e": math.e}
ALLOWED_AST_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.USub,
    ast.UAdd,
    ast.Load,
    ast.Name,
    ast.Constant,
    ast.Call,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def registry_root() -> Path:
    return Path(os.environ.get("FORMULA_REGISTRY_DIR", DEFAULT_REGISTRY_DIR)).resolve()


def read_json_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    return json.loads(text)


def write_json_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_eval_expression(expression: str, variables: dict[str, float]) -> float:
    tree = ast.parse(expression, mode="eval")
    names = set(variables) | set(SAFE_CONSTANTS) | set(SAFE_FUNCTIONS)
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_AST_NODES):
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in names:
            raise ValueError(f"Unknown variable or function: {node.id}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_FUNCTIONS:
                raise ValueError("Only whitelisted math functions may be called")
    scope = dict(SAFE_CONSTANTS)
    scope.update(SAFE_FUNCTIONS)
    scope.update(variables)
    return float(eval(compile(tree, "<formula>", "eval"), {"__builtins__": {}}, scope))


def safe_eval_condition(expression: str, variables: dict[str, float]) -> bool:
    tree = ast.parse(expression, mode="eval")
    names = set(variables) | set(SAFE_CONSTANTS) | set(SAFE_FUNCTIONS)
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_AST_NODES):
            raise ValueError(f"Unsupported expression element: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id not in names:
            raise ValueError(f"Unknown variable or function: {node.id}")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in SAFE_FUNCTIONS:
                raise ValueError("Only whitelisted math functions may be called")
    scope = dict(SAFE_CONSTANTS)
    scope.update(SAFE_FUNCTIONS)
    scope.update(variables)
    return bool(eval(compile(tree, "<formula-condition>", "eval"), {"__builtins__": {}}, scope))


def validate_formula_rule(rule: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ["module_id", "version_id", "formulas"]
    for key in required:
        if not rule.get(key):
            errors.append(f"missing required field: {key}")

    formulas = rule.get("formulas")
    if not isinstance(formulas, list) or not formulas:
        errors.append("formulas must be a non-empty list")
        return errors

    for index, formula in enumerate(formulas):
        prefix = f"formulas[{index}]"
        expression = formula.get("expression")
        if not expression:
            errors.append(f"{prefix}.expression is required")
            continue
        variables = formula.get("variables") or []
        variable_names = [item.get("name") for item in variables if isinstance(item, dict)]
        if not all(variable_names):
            errors.append(f"{prefix}.variables must define names")
            continue
        sample_values = {name: 1.0 for name in variable_names}
        try:
            safe_eval_expression(expression, sample_values)
        except Exception as exc:
            errors.append(f"{prefix}.expression is invalid: {exc}")

        test_cases = formula.get("test_cases") or []
        if not isinstance(test_cases, list) or not test_cases:
            errors.append(f"{prefix}.test_cases must contain at least one executable case")
            continue

        limits = formula.get("limits") or []
        if not isinstance(limits, list):
            errors.append(f"{prefix}.limits must be a list when provided")
            limits = []
        for limit_index, limit in enumerate(limits):
            if not isinstance(limit, dict):
                errors.append(f"{prefix}.limits[{limit_index}] must be an object")
                continue
            condition = limit.get("condition")
            behavior = limit.get("behavior")
            if not condition:
                errors.append(f"{prefix}.limits[{limit_index}].condition is required")
                continue
            if behavior not in {"error_if_false", "warning_if_false"}:
                errors.append(f"{prefix}.limits[{limit_index}].behavior must be error_if_false or warning_if_false")
            try:
                safe_eval_condition(str(condition), sample_values)
            except Exception as exc:
                errors.append(f"{prefix}.limits[{limit_index}].condition is invalid: {exc}")

        for case_index, case in enumerate(test_cases):
            inputs = case.get("inputs") or {}
            expected = case.get("expected")
            tolerance = float(case.get("tolerance", 1e-9))
            if expected is None:
                errors.append(f"{prefix}.test_cases[{case_index}].expected is required")
                continue
            try:
                actual = safe_eval_expression(expression, {k: float(v) for k, v in inputs.items()})
            except Exception as exc:
                errors.append(f"{prefix}.test_cases[{case_index}] failed to run: {exc}")
                continue
            if abs(actual - float(expected)) > tolerance:
                errors.append(
                    f"{prefix}.test_cases[{case_index}] expected {expected}, got {actual}"
                )
            numeric_inputs = {k: float(v) for k, v in inputs.items()}
            for limit_index, limit in enumerate(limits):
                if not isinstance(limit, dict) or limit.get("behavior") != "error_if_false":
                    continue
                condition = str(limit.get("condition", ""))
                try:
                    condition_ok = safe_eval_condition(condition, numeric_inputs)
                except Exception as exc:
                    errors.append(f"{prefix}.test_cases[{case_index}].limits[{limit_index}] failed to run: {exc}")
                    continue
                if not condition_ok:
                    errors.append(
                        f"{prefix}.test_cases[{case_index}] limit condition failed: {condition}"
                    )
    return errors


def run_book_smoke_check() -> list[str]:
    """Run the official book entry point once before publishing active rules."""
    try:
        from pkg.books.example_book.book_models import BookInput, ProjectInfo
        from pkg.books.example_book.book_runner import run_book

        book_input = BookInput(
            project=ProjectInfo(
                project_id="FORMULA_PUBLISH_SMOKE",
                case_id="SMOKE",
                title="Formula publish smoke",
            )
        )
        result = run_book(book_input)
        if result.governing is None:
            return ["run_book smoke did not return a governing summary"]
        return []
    except Exception as exc:
        return [f"run_book smoke failed: {exc}"]


def active_versions_path(root: Path | None = None) -> Path:
    return (root or registry_root()) / "active_versions.yaml"


def load_active_versions(root: Path | None = None) -> dict[str, Any]:
    return read_json_yaml(active_versions_path(root))


def get_active_module(root: Path | None, module_id: str) -> dict[str, Any] | None:
    active = load_active_versions(root).get("active", {})
    module_ref = active.get(module_id)
    if not module_ref:
        return None
    path = (root or registry_root()) / module_ref["path"]
    rule = read_json_yaml(path)
    rule["_registry_path"] = str(path)
    rule["_registry_sha256"] = sha256_file(path)
    return rule


def active_registry_metadata(root: Path | None = None) -> dict[str, Any]:
    data = load_active_versions(root)
    active = data.get("active", {})
    digest_source = json.dumps(active, sort_keys=True, ensure_ascii=False)
    return {
        "formula_registry_version": data.get("registry_version", "unversioned"),
        "formula_hash": sha256_text(digest_source) if active else None,
        "formula_published_at": data.get("published_at"),
        "active_modules": sorted(active),
    }


def publish_formula_rule(
    rule: dict[str, Any],
    *,
    root: Path | None = None,
    admin: str = "admin",
    notes: str = "",
    require_smoke: bool = True,
) -> dict[str, Any]:
    root = root or registry_root()
    errors = validate_formula_rule(rule)
    if not errors and require_smoke:
        errors.extend(run_book_smoke_check())
    status = "failed" if errors else "published"
    module_id = str(rule.get("module_id", "unknown"))
    version_id = str(rule.get("version_id", datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")))
    rule = dict(rule)
    rule["module_id"] = module_id
    rule["version_id"] = version_id
    rule["published_at"] = utc_now()
    rule["published_by"] = admin
    rule["status"] = status
    rule["validation_errors"] = errors

    version_rel = Path("modules") / module_id / "versions" / f"{version_id}.yaml"
    version_path = root / version_rel
    write_json_yaml(version_path, rule)
    digest = sha256_file(version_path)

    if not errors:
        active_path = active_versions_path(root)
        active = read_json_yaml(active_path) or {"schema_version": "1.0", "active": {}}
        active["registry_version"] = version_id
        active["published_at"] = rule["published_at"]
        active.setdefault("active", {})[module_id] = {
            "version_id": version_id,
            "path": version_rel.as_posix(),
            "sha256": digest,
            "published_at": rule["published_at"],
        }
        write_json_yaml(active_path, active)

    append_publish_log(
        {
            "timestamp": rule["published_at"],
            "admin": admin,
            "module_id": module_id,
            "version_id": version_id,
            "status": status,
            "sha256": digest,
            "notes": notes or "; ".join(errors),
        }
    )
    return {"status": status, "errors": errors, "path": str(version_path), "sha256": digest}


def append_publish_log(row: dict[str, Any], path: Path | None = None) -> None:
    path = path or Path(os.environ.get("FORMULA_PUBLISH_LOG", PUBLISH_LOG_DEFAULT))
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    fieldnames = ["timestamp", "admin", "module_id", "version_id", "status", "sha256", "notes"]
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in fieldnames})
