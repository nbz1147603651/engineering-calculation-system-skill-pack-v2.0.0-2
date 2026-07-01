"""Reusable CustomTkinter widgets: status badge, agent card, log panel.

All widgets are theme-aware (they read CTk's current appearance mode) and keep
their styling from :mod:`styles`. Callbacks are passed in by the controller
(:mod:`app`) so widgets stay free of business logic.

Design language: ZJIC International / NHS.UK design system
  - NHS Blue primary (#005EB8) as primary accent
  - Border-based card hierarchy (no shadows)
  - Minimal border-radius for a formal engineering feel
  - Left accent bars on panels
  - Hover interaction: card border color changes on hover
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from . import styles
from .agents import AgentSpec
from .detector import Detection
from .i18n import t


# --------------------------------------------------------------------------- #
# Status badge: compact pill showing program + deployment state
# --------------------------------------------------------------------------- #

class StatusBadge(ctk.CTkFrame):
    """Two-dot badge: [program] [deployed] with labels. NHS.UK style."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._prog_dot = ctk.CTkLabel(
            self, text="●", width=12, font=(styles.FONT_FAMILY, 10),
        )
        self._prog_label = ctk.CTkLabel(
            self, text=t("checking"), font=styles.FONT_SMALL, anchor="w",
            text_color=(styles.TEXT_SECONDARY, "#9AA5B1"),
        )
        self._dep_dot = ctk.CTkLabel(
            self, text="●", width=12, font=(styles.FONT_FAMILY, 10),
        )
        self._dep_label = ctk.CTkLabel(
            self, text="—", font=styles.FONT_SMALL, anchor="w",
            text_color=(styles.TEXT_SECONDARY, "#9AA5B1"),
        )
        self._prog_dot.grid(row=0, column=0, padx=(0, 2))
        self._prog_label.grid(row=0, column=1, padx=(0, styles.PAD_SM))
        self._dep_dot.grid(row=0, column=2, padx=(0, 2))
        self._dep_label.grid(row=0, column=3, padx=0)

    def update(self, detection: Detection | None) -> None:  # type: ignore[override]
        if detection is None:
            self._prog_dot.configure(text_color=styles.NEUTRAL)
            self._prog_label.configure(text=t("checking"))
            self._dep_dot.configure(text_color=styles.NEUTRAL)
            self._dep_label.configure(text="—")
            return
        if detection.program:
            self._prog_dot.configure(text_color=styles.COLOR_INSTALLED)
            self._prog_label.configure(text=t("program_installed"))
        else:
            self._prog_dot.configure(text_color=styles.COLOR_NOT_INSTALLED)
            self._prog_label.configure(text=t("program_not_found"))
        if detection.deployed:
            self._dep_dot.configure(text_color=styles.COLOR_DEPLOYED)
            self._dep_label.configure(text=t("deployed"))
        else:
            self._dep_dot.configure(text_color=styles.COLOR_NOT_DEPLOYED)
            self._dep_label.configure(text=t("not_deployed"))


# --------------------------------------------------------------------------- #
# Agent card — NHS.UK glass-card style with border hover
# --------------------------------------------------------------------------- #

class AgentCard(ctk.CTkFrame):
    """A single agent tile: icon, name, summary, badge, action buttons.

    Uses border-based hierarchy per the NHS.UK design system.
    Hover: border changes from BORDER to PRIMARY.
    """

    def __init__(
        self,
        master: tk.Misc,
        spec: AgentSpec,
        *,
        on_deploy: Callable[[AgentSpec], None],
        on_verify: Callable[[AgentSpec], None],
        on_uninstall: Callable[[AgentSpec], None],
        on_pick_root: Callable[[AgentSpec], None],
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            width=styles.CARD_W,
            height=styles.CARD_H,
            corner_radius=styles.CARD_RADIUS,
            border_width=styles.BORDER_W,
            border_color=(styles.BORDER, styles.DARK_BORDER),
            fg_color=(styles.SURFACE_WHITE, styles.DARK_SURFACE_CARD),
            **kwargs,
        )
        self._spec = spec
        self._on_deploy = on_deploy
        self._on_verify = on_verify
        self._on_uninstall = on_uninstall
        self._on_pick_root = on_pick_root

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)

        # --- Left accent bar (narrow colored frame) ---
        accent_bar = ctk.CTkFrame(
            self, width=3,
            fg_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            corner_radius=0,
        )
        accent_bar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        # --- Main content area ---
        self.grid_rowconfigure(0, weight=1)
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        # Header: icon + name + kind tag
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=styles.PAD_SM, pady=(styles.PAD_SM, 2))
        header.grid_columnconfigure(1, weight=1)

        icon = ctk.CTkLabel(
            header,
            text=spec.icon,
            width=30,
            height=30,
            corner_radius=styles.BUTTON_RADIUS,
            fg_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            text_color=styles.TEXT_ON_PRIMARY,
            font=(styles.FONT_FAMILY, 13, "bold"),
        )
        icon.grid(row=0, column=0, padx=(0, styles.PAD_SM))

        name = ctk.CTkLabel(
            header, text=spec.display_name, font=styles.FONT_HEADING, anchor="w",
            text_color=(styles.TEXT_PRIMARY, styles.DARK_TEXT),
        )
        name.grid(row=0, column=1, sticky="ew")

        kind_text = t("kind_project") if spec.kind == "project" else t("kind_user")
        self._kind_tag = ctk.CTkLabel(
            header,
            text=kind_text,
            width=52,
            corner_radius=styles.TAG_RADIUS,
            fg_color=(styles.ACCENT_PALE, "#2A3A50"),
            text_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            font=styles.FONT_TAG,
        )
        self._kind_tag.grid(row=0, column=2)

        # Summary text
        summary = ctk.CTkLabel(
            content, text=spec.summary, font=styles.FONT_SMALL, anchor="w", justify="left",
            text_color=(styles.TEXT_SECONDARY, "#9AA5B1"),
        )
        summary.grid(row=1, column=0, sticky="ew", padx=styles.PAD_SM)

        # Status badge
        self._badge = StatusBadge(content)
        self._badge.grid(row=2, column=0, sticky="w", padx=styles.PAD_SM, pady=(4, 2))

        # Root path label
        self._root_label = ctk.CTkLabel(
            content, text=t("root_not_set"), font=styles.FONT_SMALL, anchor="w",
            text_color=(styles.TEXT_TERTIARY, "#768692"),
        )
        self._root_label.grid(row=3, column=0, sticky="ew", padx=styles.PAD_SM)

        # Action row
        actions = ctk.CTkFrame(content, fg_color="transparent")
        actions.grid(row=4, column=0, sticky="ew", padx=styles.PAD_SM, pady=(4, styles.PAD_SM))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        actions.grid_columnconfigure(2, weight=1)

        # Deploy button — primary solid
        self._deploy_btn = ctk.CTkButton(
            actions, text=t("btn_deploy"), height=28, font=styles.FONT_SMALL,
            corner_radius=styles.BUTTON_RADIUS,
            fg_color=(styles.PRIMARY, styles.PRIMARY_DARK),
            hover_color=(styles.PRIMARY_DARK, styles.PRIMARY),
            text_color=styles.TEXT_ON_PRIMARY,
            command=self._do_deploy,
        )
        self._deploy_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        # Verify button — secondary outline
        self._verify_btn = ctk.CTkButton(
            actions, text=t("btn_verify"), height=28, width=64, font=styles.FONT_SMALL,
            corner_radius=styles.BUTTON_RADIUS,
            fg_color=("transparent", "transparent"),
            hover_color=(styles.ACCENT_PALE, "#2A3A50"),
            text_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            border_width=1,
            border_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            command=self._do_verify,
        )
        self._verify_btn.grid(row=0, column=1, padx=2)

        if spec.kind == "project":
            self._root_btn = ctk.CTkButton(
                actions, text=t("btn_folder"), height=28, width=68, font=styles.FONT_SMALL,
                corner_radius=styles.BUTTON_RADIUS,
                fg_color=("transparent", "transparent"),
                hover_color=(styles.ACCENT_PALE, "#2A3A50"),
                text_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
                border_width=1,
                border_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
                command=self._do_pick_root,
            )
            self._root_btn.grid(row=0, column=2, padx=(2, 0))
            self._uninstall_btn = None
        else:
            self._uninstall_btn = ctk.CTkButton(
                actions, text=t("btn_remove"), height=28, width=68, font=styles.FONT_SMALL,
                corner_radius=styles.BUTTON_RADIUS,
                fg_color=(styles.DANGER, styles.DANGER_HOVER),
                hover_color=(styles.DANGER_HOVER, styles.DANGER),
                text_color=styles.TEXT_ON_PRIMARY,
                command=self._do_uninstall,
            )
            self._uninstall_btn.grid(row=0, column=2, padx=(2, 0))
            self._root_btn = None

        # Bind hover events for border color change
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event: tk.Event) -> None:
        """Hover effect: border changes to PRIMARY color."""
        self.configure(border_color=(styles.PRIMARY, styles.PRIMARY_LIGHT))

    def _on_leave(self, event: tk.Event) -> None:
        """Hover leave: border returns to default color."""
        self.configure(border_color=(styles.BORDER, styles.DARK_BORDER))

    # ----- public API used by the controller ----- #

    def set_detection(self, detection: Detection | None) -> None:
        self._badge.update(detection)

    def set_root_label(self, path: Path | None) -> None:
        if path is None:
            self._root_label.configure(text=t("root_not_set"))
        else:
            display = str(path)
            if len(display) > 42:
                display = "…" + display[-41:]
            self._root_label.configure(text=f"{t('root_prefix')}{display}")

    def set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self._deploy_btn.configure(state=state)
        self._verify_btn.configure(state=state)
        if self._uninstall_btn is not None:
            self._uninstall_btn.configure(state=state)
        if self._root_btn is not None:
            self._root_btn.configure(state=state)

    def refresh_texts(self) -> None:
        """Re-apply translated strings (called after language switch)."""
        kind_text = t("kind_project") if self._spec.kind == "project" else t("kind_user")
        self._kind_tag.configure(text=kind_text)
        self._deploy_btn.configure(text=t("btn_deploy"))
        self._verify_btn.configure(text=t("btn_verify"))
        if self._uninstall_btn is not None:
            self._uninstall_btn.configure(text=t("btn_remove"))
        if self._root_btn is not None:
            self._root_btn.configure(text=t("btn_folder"))
        current_text = self._root_label.cget("text")
        if current_text == t("root_not_set"):
            pass
        else:
            prefix = t("root_prefix")
            if current_text.startswith(prefix):
                path_str = current_text[len(prefix):]
                self._root_label.configure(text=f"{prefix}{path_str}")

    # ----- internal button handlers ----- #

    def _do_deploy(self) -> None:
        self._on_deploy(self._spec)

    def _do_verify(self) -> None:
        self._on_verify(self._spec)

    def _do_uninstall(self) -> None:
        self._on_uninstall(self._spec)

    def _do_pick_root(self) -> None:
        self._on_pick_root(self._spec)


# --------------------------------------------------------------------------- #
# Log panel — NHS.UK panel style with left accent bar
# --------------------------------------------------------------------------- #

class LogPanel(ctk.CTkFrame):
    """Scrolling, read-only mono log with severity color hints.

    Features a left accent bar per the NHS.UK panel system.
    """

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(
            master,
            corner_radius=styles.CARD_RADIUS,
            border_width=styles.BORDER_W,
            border_color=(styles.BORDER, styles.DARK_BORDER),
            **kwargs,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Left accent bar
        accent_bar = ctk.CTkFrame(
            self, width=3,
            fg_color=(styles.PRIMARY, styles.PRIMARY_LIGHT),
            corner_radius=0,
        )
        accent_bar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)

        self._text = ctk.CTkTextbox(
            self,
            font=styles.FONT_MONO,
            wrap="word",
            state="disabled",
            fg_color=(styles.SURFACE_WHITE, styles.DARK_SURFACE),
            text_color=(styles.TEXT_PRIMARY, styles.DARK_TEXT),
            corner_radius=0,
        )
        self._text.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        # Tag colors for severity hints
        cmd_color = styles.TEXT_SECONDARY if ctk.get_appearance_mode().lower() == "light" else "#7E8A99"
        self._text.tag_config("error", foreground=styles.DANGER)
        self._text.tag_config("ok", foreground=styles.SUCCESS)
        self._text.tag_config("warn", foreground=styles.WARNING)
        self._text.tag_config("cmd", foreground=cmd_color)

    def append(self, line: str) -> None:
        self._text.configure(state="normal")
        tag = self._tag_for(line)
        self._text.insert("end", line + "\n", tag or ())
        self._text.see("end")
        self._text.configure(state="disabled")

    def clear(self) -> None:
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")

    @staticmethod
    def _tag_for(line: str) -> str | None:
        lower = line.lower()
        if line.startswith("$ "):
            return "cmd"
        if "[error]" in lower or "traceback" in lower or "failed" in lower:
            return "error"
        if "[verify]" in lower or "[done]" in lower or "complete" in lower or "✓" in line:
            return "ok"
        if "[backup]" in lower or "[skip]" in lower or "warning" in lower or "[警告]" in line:
            return "warn"
        return None


# --------------------------------------------------------------------------- #
# Progress bar with label — slim, refined
# --------------------------------------------------------------------------- #

class ProgressRow(ctk.CTkFrame):
    """Slim progress bar with status label."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self._bar = ctk.CTkProgressBar(
            self, height=6, corner_radius=3,
            progress_color=styles.PRIMARY,
        )
        self._bar.set(0.0)
        self._bar.grid(row=0, column=0, sticky="ew", padx=(0, styles.PAD))

        self._label = ctk.CTkLabel(
            self, text=t("progress_idle"), font=styles.FONT_SMALL,
            anchor="w", width=320,
            text_color=(styles.TEXT_SECONDARY, "#9AA5B1"),
        )
        self._label.grid(row=0, column=1, sticky="w")

    def set(self, fraction: float, label: str) -> None:
        self._bar.set(max(0.0, min(1.0, fraction)))
        self._label.configure(text=label)

    def reset(self, text: str | None = None) -> None:
        self._bar.set(0.0)
        self._label.configure(text=text if text is not None else t("progress_idle"))

    def set_error(self, text: str) -> None:
        self._bar.configure(progress_color=styles.DANGER)
        self._label.configure(text=text, text_color=(styles.DANGER, styles.DANGER))

    def set_ok(self) -> None:
        self._bar.configure(progress_color=styles.PRIMARY)
        self._label.configure(text_color=(styles.TEXT_SECONDARY, "#9AA5B1"))
