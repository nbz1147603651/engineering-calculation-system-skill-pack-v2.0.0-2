"""Persistent configuration for the deployment console.

Stores user preferences (language, repo root, per-platform install roots) in a
JSON file under the user's home directory so they survive across launches. This
fixes the issue where the exe always prompts for a folder on every startup and
keeps project-level deployments from stealing user-level install roots.

Config file location:
  - Windows: %APPDATA%/engineering-calc-system/config.json
  - macOS/Linux: ~/.config/engineering-calc-system/config.json
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path

from .i18n import Language


def _config_dir() -> Path:
    """Return the platform-appropriate config directory."""
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "engineering-calc-system"


_CONFIG_FILE = _config_dir() / "config.json"


@dataclass
class AppConfig:
    """All persisted user preferences."""

    language: Language = "en"
    repo_root: str = ""  # empty = not set
    theme: str = "System"
    agent_roots: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls) -> "AppConfig":
        """Load config from disk. Returns defaults if file is missing/corrupt."""
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            raw_agent_roots = data.get("agent_roots", {})
            agent_roots = (
                {str(name): root for name, root in raw_agent_roots.items() if isinstance(root, str)}
                if isinstance(raw_agent_roots, dict)
                else {}
            )
            return cls(
                language=data.get("language", "en"),
                repo_root=data.get("repo_root", ""),
                theme=data.get("theme", "System"),
                agent_roots=agent_roots,
            )
        except (OSError, ValueError, TypeError):
            return cls()

    def save(self) -> None:
        """Persist config to disk. Creates the config directory if needed."""
        _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CONFIG_FILE.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
