from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REVIEW_ROOT = PROJECT_ROOT / "outputs" / "review"
SESSION_ID_RE = re.compile(r"^[a-f0-9]{16,64}$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(item) for key, item in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(item) for item in value]
    return value


def stable_json(value: Any) -> str:
    return json.dumps(to_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def review_root(root: Path | None = None) -> Path:
    return Path(root or DEFAULT_REVIEW_ROOT).resolve()


def session_dir(session_id: str, root: Path | None = None) -> Path:
    if not SESSION_ID_RE.match(session_id):
        raise ValueError("Invalid review session id.")
    return review_root(root) / "sessions" / session_id


def session_id_for(book_input: Any, book_result: Any) -> str:
    digest = hashlib.sha256()
    digest.update(stable_json(book_input).encode("utf-8"))
    digest.update(stable_json(book_result).encode("utf-8"))
    return digest.hexdigest()[:24]


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_plain(data), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_review_session(
    book_input: Any,
    book_result: Any,
    report_context: dict[str, Any] | None = None,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    sid = session_id_for(book_input, book_result)
    target = session_dir(sid, root)
    state = {
        "session_id": sid,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "status": "ready_for_review",
        "review_decision": "pending",
    }
    _write_json(target / "input.json", book_input)
    _write_json(target / "result.json", book_result)
    _write_json(target / "report_context.json", report_context or {})
    _write_json(target / "review_state.json", state)
    return {
        **state,
        "session_dir": str(target),
        "input_path": str(target / "input.json"),
        "result_path": str(target / "result.json"),
        "report_context_path": str(target / "report_context.json"),
        "review_state_path": str(target / "review_state.json"),
    }


def read_review_session(session_id: str, *, root: Path | None = None) -> dict[str, Any]:
    target = session_dir(session_id, root)
    return {
        "state": _read_json(target / "review_state.json"),
        "input": _read_json(target / "input.json"),
        "result": _read_json(target / "result.json"),
        "report_context": _read_json(target / "report_context.json"),
    }


def list_review_sessions(*, root: Path | None = None) -> list[dict[str, Any]]:
    sessions_root = review_root(root) / "sessions"
    if not sessions_root.exists():
        return []
    sessions: list[dict[str, Any]] = []
    for state_path in sorted(sessions_root.glob("*/review_state.json"), reverse=True):
        try:
            sessions.append(_read_json(state_path))
        except (OSError, json.JSONDecodeError):
            continue
    return sessions


def append_review_decision(
    session_id: str,
    *,
    reviewer: str,
    decision: str,
    notes: str,
    root: Path | None = None,
) -> dict[str, Any]:
    if decision not in {"accepted", "needs_change", "rejected"}:
        raise ValueError("review decision must be accepted, needs_change, or rejected")

    target = session_dir(session_id, root)
    state_path = target / "review_state.json"
    state = _read_json(state_path)
    row = {
        "timestamp": utc_now(),
        "session_id": session_id,
        "reviewer": reviewer or "reviewer",
        "decision": decision,
        "notes": notes or "",
    }
    log_path = review_root(root) / "review_decisions.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    state.update({
        "updated_at": row["timestamp"],
        "status": "reviewed",
        "review_decision": decision,
        "reviewer": row["reviewer"],
        "review_notes": row["notes"],
    })
    _write_json(state_path, state)
    return state
