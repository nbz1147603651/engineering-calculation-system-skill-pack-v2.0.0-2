"""Engineering Calculation System - one-click deployment console (CustomTkinter GUI).

This package provides a clean desktop UI to:
  * detect whether each target agent program is installed on the machine
  * detect whether the skill/plugin is already deployed to each agent
  * build release profiles by reusing the existing ``build_release.py``
  * copy the right overlay into each agent's install root (with backup)
  * verify and uninstall deployments

The package only imports existing tools (``build_release.py`` /
``install_qoder_user.py``) and never mutates them.
"""

from __future__ import annotations

# Mirrors release_config.json "version"; kept in sync by sync_versions.py.
# Exposed so the PyInstaller-bundled exe can report its build version without
# reading release_config.json (which is not shipped inside the exe).
__version__ = "2.4.5"

