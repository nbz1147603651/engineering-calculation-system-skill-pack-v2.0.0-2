"""Reusable CustomTkinter widgets: status badge, agent card, log panel.

All widgets are theme-aware (they read CTk's current appearance mode) and keep
their styling from :mod:`styles`. Callbacks are passed in by the controller
(:mod:`app`) so widgets stay free of business logic.
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
# Status badge: a small pill showing program + deployment state
# --------------------------------------------------------------------------- #

class StatusBadge(ctk.CTkFrame):
    """Two-dot badge: [program] [deployed] with labels."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._prog_dot = ctk.CTkLabel(self, text="●", width=14, font=styles.FONT_SMALL)
        self._prog_label = ctk.CTkLabel(self, text=t("checking"), font=styles.FONT_SMALL, anchor="w")
        self._dep_dot = ctk.CTkLabel(self, text="●", width=14, font=styles.FONT_SMALL)
        self._dep_label = ctk.CTkLabel(self, text="—", font=styles.FONT_SMALL, anchor="w")
        self._prog_dot.grid(row=0, column=0, padx=(0, 2))
        self._prog_label.grid(row=0, column=1, padx=(0, styles.PAD))
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
# Agent card
# --------------------------------------------------------------------------- #

class AgentCard(ctk.CTkFrame):
    """A single agent tile: icon, name, summary, badge, action buttons."""

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
            fg_color=(styles.ACCENT_SOFT, "#2A2F38"),
            **kwargs,
        )
        self._spec = spec
        self._on_deploy = on_deploy
        self._on_verify = on_verify
        self._on_uninstall = on_uninstall
        self._on_pick_root = on_pick_root

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)

        # Header: icon + name + kind tag
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=styles.PAD, pady=(styles.PAD, 2))
        header.grid_columnconfigure(1, weight=1)

        icon = ctk.CTkLabel(
            header,
            text=spec.icon,
            width=32,
            height=32,
            corner_radius=16,
            fg_color=styles.ACCENT,
            text_color="white",
            font=(styles.FONT_FAMILY, 14, "bold"),
        )
        icon.grid(row=0, column=0, padx=(0, styles.PAD_SM))
        name = ctk.CTkLabel(header, text=spec.display_name, font=styles.FONT_SUBTITLE, anchor="w")
        name.grid(row=0, column=1, sticky="ew")
        kind_text = t("kind_project") if spec.kind == "project" else t("kind_user")
        kind_tag = ctk.CTkLabel(
            header,
            text=kind_text,
            width=56,
            corner_radius=8,
            fg_color=("#D7DEE6", "#3A3F4B"),
            text_color=("#41505E", "#C7CED6"),
            font=(styles.FONT_FAMILY, 10),
        )
        kind_tag.grid(row=0, column=2)

        summary = ctk.CTkLabel(
            self, text=spec.summary, font=styles.FONT_SMALL, anchor="w", justify="left"
        )
        summary.grid(row=1, column=0, sticky="ew", padx=styles.PAD)

        self._badge = StatusBadge(self)
        self._badge.grid(row=2, column=0, sticky="w", padx=styles.PAD, pady=(2, 2))

        self._root_label = ctk.CTkLabel(
            self, text=t("root_not_set"), font=styles.FONT_SMALL, anchor="w",
            text_color=("#6B7480", "#9AA5B1"),
        )
        self._root_label.grid(row=3, column=0, sticky="ew", padx=styles.PAD)

        # Action row
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=4, column=0, sticky="ew", padx=styles.PAD, pady=(2, styles.PAD))
        actions.grid_columnconfigure(0, weight=1)

        self._deploy_btn = ctk.CTkButton(
            actions, text=t("btn_deploy"), height=28, font=styles.FONT_SMALL,
            fg_color=styles.ACCENT, hover_color=styles.ACCENT_HOVER,
            command=self._do_deploy,
        )
        self._deploy_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self._verify_btn = ctk.CTkButton(
            actions, text=t("btn_verify"), height=28, width=64, font=styles.FONT_SMALL,
            fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
            command=self._do_verify,
        )
        self._verify_btn.grid(row=0, column=1, padx=2)

        if spec.kind == "project":
            self._root_btn = ctk.CTkButton(
                actions, text=t("btn_folder"), height=28, width=68, font=styles.FONT_SMALL,
                fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
                command=self._do_pick_root,
            )
            self._root_btn.grid(row=0, column=2, padx=(2, 0))
            self._uninstall_btn = None
        else:
            self._uninstall_btn = ctk.CTkButton(
                actions, text=t("btn_remove"), height=28, width=68, font=styles.FONT_SMALL,
                fg_color=styles.DANGER, hover_color=styles.DANGER_HOVER,
                command=self._do_uninstall,
            )
            self._uninstall_btn.grid(row=0, column=2, padx=(2, 0))
            self._root_btn = None

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
        # Update kind tag
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkFrame) and child.grid_info().get("row") == 0:
                for sub in child.winfo_children():
                    if isinstance(sub, ctk.CTkLabel) and sub.cget("width") == 56:
                        sub.configure(text=kind_text)
                        break
                break
        # Update buttons
        self._deploy_btn.configure(text=t("btn_deploy"))
        self._verify_btn.configure(text=t("btn_verify"))
        if self._uninstall_btn is not None:
            self._uninstall_btn.configure(text=t("btn_remove"))
        if self._root_btn is not None:
            self._root_btn.configure(text=t("btn_folder"))
        # Re-apply root label
        current_text = self._root_label.cget("text")
        if current_text == t("root_not_set"):
            pass  # already correct
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
# Log panel
# --------------------------------------------------------------------------- #

class LogPanel(ctk.CTkFrame):
    """Scrolling, read-only mono log with severity color hints."""

    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, corner_radius=styles.CARD_RADIUS, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._text = ctk.CTkTextbox(
            self,
            font=styles.FONT_MONO,
            wrap="word",
            state="disabled",
            fg_color=("white", "#1E222A"),
            text_color=("#2B333B", "#D7DEE6"),
            corner_radius=styles.CARD_RADIUS,
        )
        self._text.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        # Tag colors for severity hints. CTkTextbox forwards tag_config to the
        # underlying tk.Text, which needs a single color (not a light/dark
        # tuple), so resolve based on the current appearance mode.
        cmd_color = "#41505E" if ctk.get_appearance_mode().lower() == "light" else "#7E8A99"
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
# Progress bar with label
# --------------------------------------------------------------------------- #

class ProgressRow(ctk.CTkFrame):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self._bar = ctk.CTkProgressBar(self, height=10, progress_color=styles.ACCENT)
        self._bar.set(0.0)
        self._bar.grid(row=0, column=0, sticky="ew", padx=(0, styles.PAD))
        self._label = ctk.CTkLabel(self, text=t("progress_idle"), font=styles.FONT_SMALL, anchor="w", width=320)
        self._label.grid(row=0, column=1, sticky="w")

    def set(self, fraction: float, label: str) -> None:
        self._bar.set(max(0.0, min(1.0, fraction)))
        self._label.configure(text=label)

    def reset(self, text: str = "idle") -> None:
        self._bar.set(0.0)
        self._label.configure(text=text)

    def set_error(self, text: str) -> None:
        self._bar.configure(progress_color=styles.DANGER)
        self._label.configure(text=text)

    def set_ok(self) -> None:
        self._bar.configure(progress_color=styles.ACCENT)
