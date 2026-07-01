"""Visual constants for the deployment console.

Kept in one place so the whole app restyles from a single source.
Design language follows the ZJIC International / NHS.UK design system:
  - NHS Blue primary (#005EB8)
  - Minimal border-radius (2-4px) for a formal engineering feel
  - Border-based hierarchy (no shadows)
  - High contrast, information-dense layouts
  - Left accent bars for panels
"""

from __future__ import annotations

import platform

# --------------------------------------------------------------------------- #
# NHS.UK / ZJIC Color System
# --------------------------------------------------------------------------- #

# Primary palette
PRIMARY = "#005EB8"              # NHS Blue - primary actions, accents
PRIMARY_DARK = "#003087"         # Deep blue - hover states, dark bg
PRIMARY_LIGHT = "#418ED8"        # Light blue - secondary elements
ACCENT_PALE = "#E8F1F8"          # Very pale blue - tag bg, panel bg

# Legacy aliases for backward compatibility
ACCENT = PRIMARY
ACCENT_HOVER = PRIMARY_DARK
ACCENT_SOFT = ACCENT_PALE

# Semantic colors
DANGER = "#DA291C"               # NHS Red - errors, uninstall
DANGER_HOVER = "#A81E14"
WARNING = "#FFB81C"              # Warm amber - warnings, focus ring
WARNING_HOVER = "#D99B15"
SUCCESS = "#007F3B"              # NHS Green - installed, deployed
SUCCESS_HOVER = "#006630"
NEUTRAL = "#768692"              # Muted grey - idle, not installed

# Status badge dot colors
COLOR_INSTALLED = SUCCESS
COLOR_NOT_INSTALLED = NEUTRAL
COLOR_DEPLOYED = PRIMARY
COLOR_NOT_DEPLOYED = NEUTRAL
COLOR_ERROR = DANGER

# Surface colors
SURFACE_WHITE = "#FFFFFF"
SURFACE_ALT = "#F0F4F5"          # Alternating section bg
BORDER = "#D8DDE0"               # Card/panel borders
BORDER_HOVER = PRIMARY           # Border on hover

# Text colors
TEXT_PRIMARY = "#212B32"          # Main text
TEXT_SECONDARY = "#4C6272"        # Secondary text (grey-blue)
TEXT_TERTIARY = "#768692"         # Tertiary text (lightest)
TEXT_ON_PRIMARY = "#FFFFFF"       # Text on primary bg

# Dark mode surfaces
DARK_SURFACE = "#1B2D4A"          # Dark navy bg
DARK_SURFACE_CARD = "#1E3350"     # Card bg in dark mode
DARK_BORDER = "#2C4A6E"           # Borders in dark mode
DARK_TEXT = "#E8EDF2"             # Primary text in dark mode

# --------------------------------------------------------------------------- #
# Typography
# --------------------------------------------------------------------------- #

def _get_font_family() -> str:
    """Return a font family that supports both Latin and CJK characters."""
    system = platform.system()
    if system == "Windows":
        return "Microsoft YaHei"  # 微软雅黑
    elif system == "Darwin":
        return "PingFang SC"      # 苹方
    else:
        return "Noto Sans CJK SC"  # Linux

FONT_FAMILY = _get_font_family()
FONT_TITLE = (FONT_FAMILY, 20, "bold")
FONT_HEADING = (FONT_FAMILY, 14, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_SMALL = (FONT_FAMILY, 11)
FONT_TAG = (FONT_FAMILY, 10, "bold")
FONT_MONO = ("Consolas", 11)     # log panel (monospace)

# --------------------------------------------------------------------------- #
# Layout & geometry
# --------------------------------------------------------------------------- #

PAD = 16
PAD_SM = 8
PAD_XS = 4
CARD_W = 280
CARD_H = 180
CARD_RADIUS = 4                  # Minimal radius - NHS.UK style
BUTTON_RADIUS = 4
TAG_RADIUS = 2

# Border widths (simulated via CTk border_width)
BORDER_W = 1
BORDER_W_THICK = 3               # Left accent bar

# Top bar
TOPBAR_HEIGHT = 52
TOPBAR_FG = PRIMARY
TOPBAR_FG_DARK = PRIMARY_DARK

# --------------------------------------------------------------------------- #
# Window
# --------------------------------------------------------------------------- #

WINDOW_TITLE = "Engineering Calculation System - Deployment Console"
WINDOW_MIN_W = 1140
WINDOW_MIN_H = 800
