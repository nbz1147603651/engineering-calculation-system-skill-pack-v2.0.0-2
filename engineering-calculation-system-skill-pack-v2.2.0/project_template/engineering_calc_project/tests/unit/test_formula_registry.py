from pkg.core.formula_registry import (
    active_registry_metadata,
    publish_formula_rule,
    safe_eval_expression,
    validate_formula_rule,
)


def _rule(version_id: str = "v1"):
    return {
        "module_id": "bearing",
        "version_id": version_id,
        "formulas": [
            {
                "formula_id": "F001",
                "name": "utilization",
                "expression": "demand / capacity",
                "variables": [
                    {"name": "demand", "unit": "kN"},
                    {"name": "capacity", "unit": "kN"},
                ],
                "test_cases": [
                    {
                        "inputs": {"demand": 25, "capacity": 100},
                        "expected": 0.25,
                        "tolerance": 1e-9,
                    }
                ],
            }
        ],
    }


def test_safe_eval_rejects_unknown_functions():
    try:
        safe_eval_expression("__import__('os').system('echo unsafe')", {})
    except ValueError:
        return
    raise AssertionError("unsafe expression should be rejected")


def test_validate_formula_rule_runs_declared_test_cases():
    assert validate_formula_rule(_rule()) == []


def test_publish_formula_rule_updates_active_registry(tmp_path, monkeypatch):
    monkeypatch.setenv("FORMULA_PUBLISH_LOG", str(tmp_path / "publish_log.csv"))
    result = publish_formula_rule(_rule("v2"), root=tmp_path, admin="tester")
    assert result["status"] == "published"

    metadata = active_registry_metadata(tmp_path)
    assert metadata["formula_registry_version"] == "v2"
    assert metadata["formula_hash"]
