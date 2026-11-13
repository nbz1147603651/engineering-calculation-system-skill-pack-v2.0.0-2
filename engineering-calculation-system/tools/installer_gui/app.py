"""Entry point for the Engineering Calculation System deployment console.

Run with:

    python engineering-calculation-system/tools/installer_gui/app.py
    python -m installer_gui.app

The UI implementation lives in qt_app.py so this wrapper can check the Qt
dependency before importing PySide6-heavy modules.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _ensure_package_importable() -> None:
    """Allow direct execution from tools/installer_gui/app.py."""

    if __package__:
        return
    tools_dir = Path(__file__).resolve().parents[1]
    tools_dir_str = str(tools_dir)
    if tools_dir_str not in sys.path:
        sys.path.insert(0, tools_dir_str)


def _ensure_pyside6() -> None:
    try:
        import PySide6  # noqa: F401
        return
    except ImportError:
        pass

    print("PySide6 is not installed. It is required for the deployment console.")
    answer = input("Install it now with `pip install PySide6`? [Y/n] ").strip().lower()
    if answer in ("", "y", "yes"):
        subprocess.run([sys.executable, "-m", "pip", "install", "PySide6"], check=True)
        return
    print("Aborting. Install PySide6 and re-run.")
    raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    _ensure_package_importable()
    args = list(sys.argv[1:] if argv is None else argv)
    if "--self-test-runtime" in args:
        from installer_gui.service import runtime_self_test
        index = args.index("--self-test-runtime")
        if index + 1 >= len(args):
            raise SystemExit("--self-test-runtime requires an empty sandbox path")
        runtime_self_test(Path(args[index + 1]))
        return 0
    _ensure_pyside6()

    if __package__:
        from .qt_app import main as qt_main
    else:
        from installer_gui.qt_app import main as qt_main

    return qt_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
