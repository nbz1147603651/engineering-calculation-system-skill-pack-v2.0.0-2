from pkg.core.formula_registry import (
    active_registry_metadata,
    publish_formula_rule,
    run_book_smoke_check,
    safe_eval_condition,
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
                "limits": [
                    {"condition": "capacity > 0", "behavior": "error_if_false"},
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


def test_safe_eval_condition_supports_comparisons():
    assert safe_eval_condition("capacity > demand", {"capacity": 100, "demand": 25})


def test_validate_formula_rule_rejects_missing_test_cases():
    rule = _rule()
    rule["formulas"][0]["test_cases"] = []

    errors = validate_formula_rule(rule)

    assert any("test_cases" in item for item in errors)


def test_validate_formula_rule_rejects_failed_limits():
    rule = _rule()
    rule["formulas"][0]["test_cases"][0]["inputs"]["capacity"] = -100
    rule["formulas"][0]["test_cases"][0]["expected"] = -0.25

    errors = validate_formula_rule(rule)

    assert any("limit condition failed" in item for item in errors)


def test_run_book_smoke_check_passes_default_scaffold():
    assert run_book_smoke_check() == []


def test_publish_formula_rule_updates_active_registry(tmp_path, monkeypatch):
    monkeypatch.setenv("FORMULA_PUBLISH_LOG", str(tmp_path / "publish_log.csv"))
    result = publish_formula_rule(_rule("v2"), root=tmp_path, admin="tester")
    assert result["status"] == "published"

    metadata = active_registry_metadata(tmp_path)
    assert metadata["formula_registry_version"] == "v2"
    assert metadata["formula_hash"]
