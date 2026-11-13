"""NIMO Engineering design tokens and native Qt theme.

The application shell consumes this module; application logic never owns colors
or a second copy of the stylesheet. Surfaces are opaque for cheap native paints.
"""

from __future__ import annotations

import platform

# --------------------------------------------------------------------------- #
# NIMO color system
# --------------------------------------------------------------------------- #

# Primary palette
PRIMARY = "#E58A24"
PRIMARY_DARK = "#CB7419"
PRIMARY_LIGHT = "#F0AE60"
ACCENT_PALE = "#FFF1DF"
SIDEBAR = "#202B36"

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
SURFACE_ALT = "#F5F6F8"
BORDER = "#E2E6EB"
BORDER_HOVER = PRIMARY           # Border on hover

# Text colors
TEXT_PRIMARY = "#202B36"
TEXT_SECONDARY = "#64717D"
TEXT_TERTIARY = "#82909C"
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
CARD_RADIUS = 10
BUTTON_RADIUS = 8
TAG_RADIUS = 2

# Border widths
BORDER_W = 1
BORDER_W_THICK = 3               # Left accent bar

# Top bar
TOPBAR_HEIGHT = 82
TOPBAR_FG = PRIMARY
TOPBAR_FG_DARK = PRIMARY_DARK

# --------------------------------------------------------------------------- #
# Window
# --------------------------------------------------------------------------- #

WINDOW_TITLE = "NIMO Engineering"
WINDOW_MIN_W = 1200
WINDOW_MIN_H = 800


def theme_colors(dark: bool) -> dict[str, str]:
    """Return one opaque palette for all native controls."""
    return {
        "window": "#151E27" if dark else SURFACE_ALT,
        "surface": "#202B36" if dark else SURFACE_WHITE,
        "input": "#18222D" if dark else SURFACE_WHITE,
        "subtle": "#263440" if dark else "#F7F8FA",
        "border": "#364450" if dark else BORDER,
        "text": "#F0F3F6" if dark else TEXT_PRIMARY,
        "muted": "#AFBBC5" if dark else TEXT_SECONDARY,
        "selection": "#4B3925" if dark else ACCENT_PALE,
        "hover": "#30404F" if dark else "#F0F2F5",
        "disabled": "#26313B" if dark else "#F0F2F4",
        "disabledText": "#778692" if dark else "#8C99A4",
    }


def stylesheet(dark: bool) -> str:
    """Render the shared theme without animation, gradients or glass layers."""
    c = theme_colors(dark)
    return f"""
        QMainWindow, QWidget#workspace {{ background: {c['window']}; }}
        QWidget {{ color: {c['text']}; font-family: "{FONT_FAMILY}"; font-size: 12px; }}
        QFrame#topbar {{ background: {c['surface']}; border-bottom: 1px solid {c['border']}; }}
        QLabel {{ background: transparent; }}
        QLabel#topbarTitle {{ color: {c['text']}; font-size: 24px; font-weight: 700; }}
        QLabel#topbarSubtitle {{ color: {c['muted']}; font-size: 12px; }}
        QLabel#versionTag {{ color: {c['muted']}; padding: 3px 8px; }}
        QFrame#sidebar {{ background: {SIDEBAR}; border: none; }}
        QFrame#sidebar QLabel {{ color: #DDE3E9; background: transparent; }}
        QLabel#sidebarBrand {{ color: #FFFFFF; font-size: 22px; font-weight: 800; }}
        QLabel#sidebarProduct {{ color: #A8B5C1; font-size: 11px; }}
        QLabel#sidebarSection {{ color: #8D9DAA; font-size: 10px; padding-top: 18px; }}
        QLabel#sidebarHelper {{ color: #CDD5DC; font-size: 11px; line-height: 1.7; }}
        QFrame#sidebar QPushButton {{
            color: #D8E0E6; background: transparent; border: none;
            border-radius: 7px; text-align: left; padding: 12px; font-size: 13px;
        }}
        QFrame#sidebar QPushButton:hover {{ background: #2D3B47; }}
        QFrame#sidebar QPushButton:checked {{ background: {PRIMARY}; color: #202B36; font-weight: 700; }}
        QFrame#sidebar QToolButton {{ background: #293743; color: #DDE3E9; border: 1px solid #43515D; }}
        QFrame#sidebar QToolButton:hover {{ background: #354551; }}
        QScrollArea {{ background: {c['window']}; border: none; }}
        QFrame#panel, QFrame#workflowPanel {{ background: {c['surface']}; border: 1px solid {c['border']}; border-radius: 10px; }}
        QLabel#sectionTitle, QLabel#detailTitle {{ font-size: 17px; font-weight: 700; color: {c['text']}; }}
        QLabel#muted, QLabel#fieldCaption {{ color: {c['muted']}; font-size: 11px; }}
        QLabel#rootHint {{ background: {c['selection']}; color: {c['muted']}; border-radius: 6px; padding: 9px; }}
        QLabel#fieldValue {{ color: {c['text']}; font-size: 11px; }}
        QLabel#agentIcon {{ background: {c['subtle']}; border: 1px solid {c['border']}; border-radius: 8px; }}
        QLabel#metric {{ color: {c['muted']}; padding: 7px 10px; font-size: 11px; }}
        QLabel#workflowNumber {{ color: {PRIMARY_DARK}; font-size: 19px; font-weight: 700; }}
        QLabel#workflowHeading {{ color: {c['text']}; font-size: 16px; font-weight: 700; }}
        QLabel#workflowDescription {{ color: {c['muted']}; font-size: 12px; }}
        QFrame#actionStrip {{ background: {c['selection']}; border: none; border-radius: 9px; }}
        QLabel#actionHelper {{ color: {c['text']}; font-size: 16px; font-weight: 700; }}
        QTableView {{ font-size: 14px; }}
        QLineEdit, QComboBox {{
            background: {c['input']}; color: {c['text']}; border: 1px solid {c['border']};
            border-radius: 6px; padding: 7px 9px; min-height: 18px; font-size: 12px;
            selection-background-color: {c['selection']};
        }}
        QLineEdit:focus, QComboBox:focus {{ border: 1px solid {PRIMARY}; }}
        QComboBox::drop-down {{ border: none; width: 20px; }}
        QComboBox QAbstractItemView {{ background: {c['surface']}; color: {c['text']}; selection-background-color: {c['selection']}; }}
        QTableView {{
            background: {c['surface']}; alternate-background-color: {c['subtle']}; color: {c['text']};
            border: 1px solid {c['border']}; border-radius: 7px;
            selection-background-color: {c['selection']}; selection-color: {c['text']};
        }}
        QTableView::item {{ padding: 6px; border: none; }}
        QHeaderView::section {{
            background: {c['subtle']}; color: {c['muted']}; border: none;
            border-bottom: 1px solid {c['border']}; padding: 11px 8px; font-weight: 600; font-size: 11px;
        }}
        QTextEdit {{ background: {c['input']}; color: {c['text']}; border: 1px solid {c['border']}; border-radius: 7px; padding: 8px; }}
        QProgressBar {{ background: {c['subtle']}; border: none; border-radius: 3px; }}
        QProgressBar::chunk {{ background: {PRIMARY}; border-radius: 3px; }}
        QPushButton, QToolButton {{
            background: {c['surface']}; color: {c['text']}; border: 1px solid {c['border']};
            border-radius: 6px; padding: 8px 11px; font-size: 12px;
        }}
        QPushButton:hover, QToolButton:hover {{ background: {c['hover']}; }}
        QPushButton[variant="primary"], QToolButton[variant="primary"] {{ background: {PRIMARY}; color: #202B36; border-color: {PRIMARY}; font-weight: 700; }}
        QPushButton[variant="primary"]:hover, QToolButton[variant="primary"]:hover {{ background: {PRIMARY_LIGHT}; border-color: {PRIMARY_LIGHT}; }}
        QPushButton[variant="danger"], QToolButton[variant="danger"] {{ background: {c['surface']}; color: #C3473C; border-color: {c['border']}; }}
        QPushButton[variant="danger"]:hover, QToolButton[variant="danger"]:hover {{ background: #FFE7E2; color: #8F2A20; }}
        QPushButton:disabled, QToolButton:disabled {{ color: {c['disabledText']}; background: {c['disabled']}; border-color: {c['border']}; }}
        QSplitter::handle {{ background: {c['window']}; }}
        QScrollBar:vertical {{ width: 9px; background: {c['subtle']}; }}
        QScrollBar::handle:vertical {{ background: #A9B3BC; border-radius: 4px; min-height: 24px; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QToolTip {{ background: {c['surface']}; color: {c['text']}; border: 1px solid {c['border']}; padding: 6px; }}
    """
