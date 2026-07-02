#!/usr/bin/env python3
"""Execution helpers for deterministic engineering-calculation skill work."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import subprocess
import sys
from pathlib import Path


TASK_HEADING_RE = re.compile(r"^(#{1,6})\s+Task\s+([A-Za-z0-9_.-]+)\b", re.IGNORECASE)
PLAN_REQUIRED_FIELDS = {
    "goal": ("goal", "objective"),
    "global_constraints": ("global_constraints", "global constraints", "constraints"),
    "exact_files": ("exact_files", "exact files", "files:"),
    "interfaces": ("interfaces", "api", "contract"),
    "artifact_outputs": ("artifact_outputs", "artifact outputs", "artifacts"),
    "validation_commands": ("validation_commands", "validation commands", "commands"),
    "expected_outputs": ("expected_outputs", "expected outputs", "expected:"),
    "stop_conditions": ("stop_conditions", "stop conditions", "blockers"),
}
PLAN_PLACEHOLDERS = (
    "tbd",
    "todo",
    "fill in later",
    "appropriate error handling",
    "handle edge cases",
    "write tests for the above",
    "similar to previous task",
    "similar to task",
)
FEEDBACK_REQUIRED_FIELDS = (
    "feedback_source",
    "requested_change",
    "affected_layer",
    "source_authority_impact",
    "unit_or_formula_impact",
    "lifecycle_gate_impact",
    "decision",
    "validation_needed",
)
CANONICAL_DOCS = (
    "shared/lifecycle.md",
    "shared/execution-discipline.md",
    "shared/planning-discipline.md",
    "shared/review-feedback-discipline.md",
    "shared/version-control-discipline.md",
    "shared/completion-evidence.md",
    "shared/systematic-debugging.md",
    "shared/multi-agent-orchestration.md",
)
PLATFORM_TARGETS = (
    "CODEX",
    "MiniMaxCode",
    "ZCode",
    "QODER",
    "QODER Project",
    "QoderCN",
    "QoderCN Project",
    "TRAE",
    "OpenCode",
    "AGENTS Generic",
)


def run(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(args, cwd=str(cwd), text=True, capture_output=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or f"command failed: {' '.join(args)}")
    return completed.stdout.strip()


def repo_root(start: Path) -> Path:
    try:
        return Path(run(["git", "rev-parse", "--show-toplevel"], start))
    except SystemExit:
        return start.resolve()


def ensure_workspace(root: Path) -> Path:
    work = root / ".engineering-calc" / "work"
    work.mkdir(parents=True, exist_ok=True)
    gitignore = work / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*\n", encoding="utf-8", newline="\n")
    return work


def extract_task(plan: Path, task_id: str) -> str:
    lines = plan.read_text(encoding="utf-8").splitlines()
    selected: list[str] = []
    in_task = False
    in_fence = False
    target = str(task_id).lower()
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
        match = None if in_fence else TASK_HEADING_RE.match(line)
        if match:
            current = match.group(2).lower()
            if in_task and current != target:
                break
            in_task = current == target
        if in_task:
            selected.append(line)
    if not selected:
        raise SystemExit(f"task {task_id!r} not found in {plan}")
    return "\n".join(selected).rstrip() + "\n"


def command_workspace(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.root).resolve())
    print(ensure_workspace(root))
    return 0


def command_task_brief(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.root).resolve())
    work = ensure_workspace(root)
    plan = Path(args.plan).resolve()
    output = Path(args.output).resolve() if args.output else work / f"task-{args.task_id}-brief.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(extract_task(plan, args.task_id), encoding="utf-8", newline="\n")
    print(f"wrote {output}: {len(output.read_text(encoding='utf-8').splitlines())} lines")
    return 0


def command_review_package(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.root).resolve())
    work = ensure_workspace(root)
    base = run(["git", "rev-parse", "--verify", args.base], root)
    head = run(["git", "rev-parse", "--verify", args.head], root)
    short_base = run(["git", "rev-parse", "--short", base], root)
    short_head = run(["git", "rev-parse", "--short", head], root)
    output = Path(args.output).resolve() if args.output else work / f"review-{short_base}..{short_head}.diff"
    output.parent.mkdir(parents=True, exist_ok=True)
    body = "\n".join(
        [
            f"# Review package: {base}..{head}",
            "",
            "## Commits",
            run(["git", "log", "--oneline", f"{base}..{head}"], root),
            "",
            "## Files changed",
            run(["git", "diff", "--stat", f"{base}..{head}"], root),
            "",
            "## Diff",
            run(["git", "diff", "-U10", f"{base}..{head}"], root),
            "",
        ]
    )
    output.write_text(body, encoding="utf-8", newline="\n")
    print(f"wrote {output}: {output.stat().st_size} bytes")
    return 0


def ledger_path(root: Path) -> Path:
    return ensure_workspace(root) / "progress.md"


def command_ledger_status(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.root).resolve())
    path = ledger_path(root)
    if path.exists():
        print(path.read_text(encoding="utf-8").rstrip())
    else:
        print(f"no ledger at {path}")
    return 0


def command_ledger_append(args: argparse.Namespace) -> int:
    root = repo_root(Path(args.root).resolve())
    path = ledger_path(root)
    if not path.exists():
        path.write_text("# Progress Ledger\n\n", encoding="utf-8", newline="\n")
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = (
        f"- {stamp} | task={args.task_id} | status={args.status} | "
        f"route={args.route or ''} | gate={args.gate or ''} | "
        f"evidence={args.evidence or ''} | commits={args.commits or ''} | notes={args.notes or ''}\n"
    )
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    print(f"appended {path}")
    return 0


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").lower().replace("-", "_")


def command_plan_check(args: argparse.Namespace) -> int:
    plan = Path(args.plan).resolve()
    text = normalized_text(plan)
    missing = [
        field
        for field, markers in PLAN_REQUIRED_FIELDS.items()
        if not any(marker.lower().replace("-", "_") in text for marker in markers)
    ]
    placeholders = [token for token in PLAN_PLACEHOLDERS if token in text]
    if missing or placeholders:
        if missing:
            print("FAIL: plan missing fields: " + ", ".join(missing), file=sys.stderr)
        if placeholders:
            print("FAIL: plan contains placeholder patterns: " + ", ".join(placeholders), file=sys.stderr)
        return 1
    print(f"PASS: plan-check {plan}")
    return 0


def command_review_feedback_check(args: argparse.Namespace) -> int:
    path = Path(args.feedback).resolve()
    text = normalized_text(path)
    missing = [field for field in FEEDBACK_REQUIRED_FIELDS if field not in text]
    if missing:
        print("FAIL: review feedback card missing fields: " + ", ".join(missing), file=sys.stderr)
        return 1
    if "decision:" not in text:
        print("FAIL: review feedback card must record decision", file=sys.stderr)
        return 1
    print(f"PASS: review-feedback-check {path}")
    return 0


def find_workspace_root(root: Path) -> Path:
    current = root.resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / "engineering-calculation-system" / "tools" / "release_config.json").exists():
            return candidate
        if (candidate / "tools" / "release_config.json").exists() and (candidate / "core").exists():
            return candidate.parent
    return repo_root(current)


def command_platform_matrix_check(args: argparse.Namespace) -> int:
    workspace = find_workspace_root(Path(args.root).resolve())
    release_config = workspace / "engineering-calculation-system" / "tools" / "release_config.json"
    core_root = workspace / "engineering-calculation-system" / "core" / "engineering-calculation-system"
    errors: list[str] = []
    if not release_config.exists():
        errors.append(f"missing release_config.json: {release_config}")
    else:
        data = json.loads(release_config.read_text(encoding="utf-8"))
        targets = {target["name"] for target in data.get("classified_targets", [])}
        missing_targets = sorted(set(PLATFORM_TARGETS) - targets)
        if missing_targets:
            errors.append("missing platform targets: " + ", ".join(missing_targets))
    for rel in CANONICAL_DOCS:
        if not (core_root / rel).exists():
            errors.append(f"missing canonical doc: {rel}")
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    print(f"PASS: platform-matrix check ({len(PLATFORM_TARGETS)} targets, {len(CANONICAL_DOCS)} canonical docs)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository or project root. Defaults to cwd.")
    sub = parser.add_subparsers(dest="command", required=True)

    workspace = sub.add_parser("workspace", help="Print and create the scratch workspace.")
    workspace.set_defaults(func=command_workspace)

    brief = sub.add_parser("task-brief", help="Extract one task from a Markdown plan.")
    brief.add_argument("--plan", required=True)
    brief.add_argument("--task-id", required=True)
    brief.add_argument("--output")
    brief.set_defaults(func=command_task_brief)

    review = sub.add_parser("review-package", help="Write a git diff review package.")
    review.add_argument("--base", required=True)
    review.add_argument("--head", required=True)
    review.add_argument("--output")
    review.set_defaults(func=command_review_package)

    ledger = sub.add_parser("ledger", help="Inspect or append progress ledger entries.")
    ledger_sub = ledger.add_subparsers(dest="ledger_command", required=True)
    status = ledger_sub.add_parser("status")
    status.set_defaults(func=command_ledger_status)
    append = ledger_sub.add_parser("append")
    append.add_argument("--task-id", required=True)
    append.add_argument("--status", required=True)
    append.add_argument("--route")
    append.add_argument("--gate")
    append.add_argument("--evidence")
    append.add_argument("--commits")
    append.add_argument("--notes")
    append.set_defaults(func=command_ledger_append)

    plan_check = sub.add_parser("plan-check", help="Validate a plan has required execution fields.")
    plan_check.add_argument("--plan", required=True)
    plan_check.set_defaults(func=command_plan_check)

    feedback = sub.add_parser("review-feedback-check", help="Validate a review feedback decision card.")
    feedback.add_argument("--feedback", required=True)
    feedback.set_defaults(func=command_review_feedback_check)

    matrix = sub.add_parser("platform-matrix", help="Inspect platform acceptance metadata.")
    matrix_sub = matrix.add_subparsers(dest="matrix_command", required=True)
    matrix_check = matrix_sub.add_parser("check")
    matrix_check.set_defaults(func=command_platform_matrix_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
