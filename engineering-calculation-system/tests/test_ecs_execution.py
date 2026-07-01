from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "engineering-calculation-system" / "core" / "engineering-calculation-system" / "scripts" / "ecs_execution.py"


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )


def test_plan_check_accepts_concrete_plan(tmp_path: Path) -> None:
    plan = tmp_path / "plan.md"
    plan.write_text(
        "\n".join(
            [
                "goal: harden 2.6.0 release behavior",
                "global_constraints: lifecycle remains in shared/lifecycle.md",
                "exact_files: shared/planning-discipline.md, scripts/ecs_execution.py",
                "interfaces: plan-check CLI",
                "artifact_outputs: behavior scenarios and platform matrix",
                "validation_commands: python scripts/ecs_execution.py plan-check --plan plan.md",
                "expected_outputs: PASS: plan-check",
                "stop_conditions: missing canonical docs or failing validator",
            ]
        ),
        encoding="utf-8",
    )

    completed = run_command("plan-check", "--plan", str(plan))

    assert completed.returncode == 0, completed.stderr
    assert "PASS: plan-check" in completed.stdout


def test_plan_check_rejects_placeholders(tmp_path: Path) -> None:
    plan = tmp_path / "plan.md"
    plan.write_text(
        "\n".join(
            [
                "goal: release",
                "global_constraints: TBD",
                "exact_files: TODO",
                "interfaces: CLI",
                "artifact_outputs: docs",
                "validation_commands: write tests for the above",
                "expected_outputs: pass",
                "stop_conditions: blockers",
            ]
        ),
        encoding="utf-8",
    )

    completed = run_command("plan-check", "--plan", str(plan))

    assert completed.returncode == 1
    assert "placeholder" in completed.stderr


def test_review_feedback_check_accepts_decision_card(tmp_path: Path) -> None:
    feedback = tmp_path / "feedback.md"
    feedback.write_text(
        "\n".join(
            [
                "feedback_source: reviewer",
                "requested_change: change a coefficient",
                "affected_layer: formula_inventory",
                "source_authority_impact: conflicts with S01",
                "unit_or_formula_impact: formula coefficient changes",
                "lifecycle_gate_impact: route_upstream",
                "decision: reject pending source authority resolution",
                "validation_needed: review-feedback-check and source conflict update",
            ]
        ),
        encoding="utf-8",
    )

    completed = run_command("review-feedback-check", "--feedback", str(feedback))

    assert completed.returncode == 0, completed.stderr
    assert "PASS: review-feedback-check" in completed.stdout


def test_platform_matrix_check_finds_targets_and_docs() -> None:
    completed = run_command("--root", str(REPO_ROOT), "platform-matrix", "check")

    assert completed.returncode == 0, completed.stderr
    assert "PASS: platform-matrix check" in completed.stdout
