"""UI-independent application boundary for NIMO Engineering operations.

The desktop worker and JSON CLI call the same actions and platform contracts.
No HTTP daemon, database, Qt, Tk, or model SDK is imported by this layer.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from threading import RLock
from typing import Callable

from . import agents, deployer, detector, workflow

_OPERATIONS = RLock()


def catalog() -> list[dict]:
    return [{"id": spec.name, "name": spec.display_name, "scope": spec.kind,
             "summary": spec.summary, "profiles": list(spec.needs_profiles),
             "default_root": str(root) if (root := spec.default_root_fn()) else None}
            for spec in agents.all_agents()]


def inspect(agent: str, root: Path | None = None) -> dict:
    spec = agents.get(agent)
    if spec is None:
        raise ValueError(f"Unknown agent: {agent}")
    selected = root if root is not None else spec.default_root_fn()
    return {"agent": agent, "root": str(selected) if selected else None,
            **asdict(detector.detect(agent, selected))}


def execute(agent: str, action: str, root: Path | None, log: Callable[[str], None],
            progress: Callable[[float, str], None], cancelled: Callable[[], bool] = lambda: False) -> dict:
    spec = agents.get(agent)
    if spec is None:
        raise deployer.DeployError(f"Unknown agent: {agent}")
    actions = {"install": spec.deploy_fn, "verify": spec.verify_fn, "uninstall": spec.uninstall_fn}
    if action not in actions:
        raise deployer.DeployError(f"Unknown action: {action}")
    selected = root if root is not None else spec.default_root_fn()
    if cancelled():
        raise deployer.DeployError("Operation cancelled before start")

    def checked_progress(fraction: float, label: str) -> None:
        if cancelled():
            raise deployer.DeployError("Operation cancelled")
        progress(fraction, label)

    # Legacy release paths are process-global; serialize actions across consumers.
    with _OPERATIONS:
        result = actions[action](deployer.DeployContext(selected, log, checked_progress, cancelled))
        if result is False:
            raise deployer.DeployError(f"{spec.display_name} verification failed")
    return {"agent": agent, "action": action, "ok": True, "root": str(selected) if selected else None}


def runtime_self_test(target: Path) -> dict:
    """Exercise the packaged install boundary in a fresh, explicitly supplied sandbox."""
    target = target.expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        raise deployer.DeployError("Runtime self-test requires a new or empty sandbox directory")
    target.mkdir(parents=True, exist_ok=True)
    status = deployer.runtime_status()
    if not deployer.using_bundled_runtime() or not status["ready"]:
        raise deployer.DeployError("Standalone engineering runtime is unavailable")
    log: list[str] = []
    deployer.build_profiles(tuple(status["profiles"]), log=log.append, progress=lambda *_: None)
    project = target / "project"
    operations = [execute("agents-generic", action, project, log.append, lambda *_: None)
                  for action in ("install", "verify", "uninstall")]
    result = {"ok": True, "runtime": status, "operations": operations,
              "sourceCheckoutRequired": False, "externalPythonRequired": False, "log": log}
    (target / "NIMO-SELF-TEST.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NIMO Engineering headless JSON service")
    parser.add_argument("command", choices=("catalog", "inspect", "install", "verify", "uninstall", "workflow"))
    parser.add_argument("--agent")
    parser.add_argument("--root", type=Path)
    parser.add_argument("--task-type", default="new-system")
    parser.add_argument("--delivery", default="web-complete")
    parser.add_argument("--evidence-gate", default="search_required")
    parser.add_argument("--coding-gate", default="no_go")
    parser.add_argument("--changed-layer", action="append", default=[])
    parser.add_argument("--baseline-verified", action="store_true")
    args = parser.parse_args(argv)
    messages = []
    try:
        if args.command == "catalog":
            result = {"product": "NIMO Engineering", "agents": catalog(), "workflow": workflow.overview()}
        elif args.command == "workflow":
            result = workflow.route(args.task_type, args.delivery, args.evidence_gate, args.coding_gate,
                                    tuple(args.changed_layer), args.baseline_verified)
        else:
            if not args.agent:
                parser.error("--agent is required for this command")
            if args.command == "inspect":
                result = inspect(args.agent, args.root)
            else:
                result = execute(args.agent, args.command, args.root, messages.append, lambda _n, label: messages.append(label))
                result["log"] = messages
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (deployer.DeployError, OSError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error), "log": messages}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
