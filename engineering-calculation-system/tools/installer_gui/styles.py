"""Visual constants for the deployment console.

Kept in one place so the whole app restyles from a single source. CustomTkinter
already provides a clean default appearance; we layer a small palette and shared
typography on top.
"""

from __future__ import annotations

import platform

# Accent palette - a single calm blue-green family so the UI reads as one product.
ACCENT = "#2E7D6B"          # primary action (deploy buttons, progress)
ACCENT_HOVER = "#246556"
ACCENT_SOFT = "#E4F1ED"     # card highlight background
DANGER = "#C0392B"          # uninstall / error
DANGER_HOVER = "#962D22"
WARNING = "#E08E0B"         # partial / needs attention
SUCCESS = "#2E8B57"         # installed / deployed / verified
NEUTRAL = "#9AA5B1"         # not installed / idle

# Status badge dot colors map cleanly onto semantic states above.
COLOR_INSTALLED = SUCCESS
COLOR_NOT_INSTALLED = NEUTRAL
COLOR_DEPLOYED = SUCCESS
COLOR_NOT_DEPLOYED = NEUTRAL
COLOR_ERROR = DANGER

# Typography - rely on system fonts; these are CTk font tuples (family, size, weight).
# Support Chinese characters on Windows/macOS/Linux.
def _get_font_family() -> str:
    """Return a font family that supports both Latin and CJK characters."""
    system = platform.system()
    if system == "Windows":
        return "Microsoft YaHei"  # 微软雅黑 - ships on all modern Windows
    elif system == "Darwin":
        return "PingFang SC"      # 苹方 - ships on macOS
    else:
        return "Noto Sans CJK SC"  # Linux - may need installation, falls back gracefully

FONT_FAMILY = _get_font_family()
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_SMALL = (FONT_FAMILY, 11)
FONT_MONO = ("Consolas", 11)    # log panel (monospace, Latin only)

# Layout spacing.
PAD = 12
PAD_SM = 6
CARD_W = 260
CARD_H = 160
CARD_RADIUS = 14

# Window.
WINDOW_TITLE = "Engineering Calculation System - Deployment Console"
WINDOW_MIN_W = 1100
WINDOW_MIN_H = 780
