"""Main window for the Engineering Calculation System deployment console.

Run with::

    python -m engineering_calculation_system.tools.installer_gui.app
    # or, from this folder:
    python app.py

The window is split into three regions (top to bottom):
  1. Agent card grid (detection + per-agent Deploy/Verify/Remove)
  2. Install-root row (override user roots / pick project roots)
  3. Live log + progress bar + global Build-All / Stop

All heavy work runs on a single background :class:`Worker` thread; the UI polls
its event queue every 80ms via ``after``.
"""

from __future__ import annotations

import json
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Callable

import customtkinter as ctk

from . import agents, config, deployer, detector, styles, widgets
from .agents import AgentSpec
from .i18n import Language, t, set_language, get_i18n
from .workers import Event, EventKind, Worker, make_build_all_job, make_deploy_job, make_uninstall_job, make_verify_job


# --------------------------------------------------------------------------- #
# Release config (version + profile list) - read once at startup.
# --------------------------------------------------------------------------- #

def _load_release_meta() -> tuple[str, tuple[str, ...]]:
    """Read version + profile list from release_config.json.

    In frozen (exe) mode release_config.json is not bundled, so fall back to the
    ``__version__`` baked into the package and a default profile list.
    """
    config_path = Path(__file__).resolve().parents[1] / "release_config.json"
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        version = data.get("version", "0.0.0")
        profiles = tuple(data.get("default_all_profiles") or data.get("profiles") or ())
        return version, profiles
    except (OSError, ValueError):
        from . import __version__ as pkg_version
        return pkg_version, ("core", "adapters-light", "qoder-addon", "singlefile", "source-dev", "ui-client")


# --------------------------------------------------------------------------- #
# Main application
# --------------------------------------------------------------------------- #

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.version, self.profiles = _load_release_meta()

        # Load persisted config
        self._app_config = config.AppConfig.load()

        # Apply language from config
        set_language(self._app_config.language)

        self.title(f"{t('window_title')}  v{self.version}")
        self.minsize(styles.WINDOW_MIN_W, styles.WINDOW_MIN_H)

        # In frozen (exe) mode the deployer cannot locate the skill-pack repo
        # from its own __file__, so ask the user up front (or honor ECS_REPO_ROOT).
        # In source mode the deployer auto-detects it.
        self._init_repo_root()
        ctk.set_appearance_mode(self._app_config.theme.lower())
        ctk.set_default_color_theme("blue")

        # Per-agent chosen install root (overrides the default).
        self._roots: dict[str, Path | None] = {}
        for spec in agents.all_agents():
            self._roots[spec.name] = spec.default_root_fn()

        self._worker = Worker()
        self._cards: dict[str, widgets.AgentCard] = {}
        self._repo_root_label: ctk.CTkLabel | None = None

        self._build_layout()
        self._refresh_all_detection()
        self.after(80, self._drain_events)

    # ------------------------------------------------------------------ #
    # Repo-root resolution (frozen vs source mode)
    # ------------------------------------------------------------------ #

    def _init_repo_root(self) -> None:
        """Ensure deployer.REPO_ROOT is set before any deploy/verify runs.

        Source mode: deployer auto-detected it at import; nothing to do.
        Frozen mode: honor ECS_REPO_ROOT, then try exe directory, then persisted config, else prompt.
        """
        if not deployer.is_frozen():
            return
        # 1. Try environment variable
        env_root = os.environ.get("ECS_REPO_ROOT")
        if env_root:
            try:
                deployer.set_repo_root(Path(env_root))
                return
            except deployer.DeployError:
                pass  # env value was stale; fall through

        # 2. Try exe directory (default location when running from exe)
        exe_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else None
        if exe_dir:
            try:
                deployer.set_repo_root(exe_dir)
                # Successfully set from exe directory, save to config
                self._app_config.repo_root = str(exe_dir)
                self._app_config.save()
                return
            except deployer.DeployError:
                pass  # exe dir doesn't have the required files; fall through

        # 3. Try persisted config
        if self._app_config.repo_root:
            try:
                deployer.set_repo_root(Path(self._app_config.repo_root))
                return
            except deployer.DeployError:
                pass  # persisted path is stale; fall through to prompt

        # 4. Defer the prompt until the window is fully up
        self.after(50, self._prompt_for_repo_root)

    def _prompt_for_repo_root(self) -> None:
        chosen = filedialog.askdirectory(
            title=t("dlg_select_repo_title")
        )
        if not chosen:
            if self._log:
                self._log.append(t("dlg_no_repo_warn"))
            return
        try:
            deployer.set_repo_root(Path(chosen))
        except deployer.DeployError as exc:
            messagebox.showerror(t("dlg_invalid_repo"), str(exc))
            self.after(50, self._prompt_for_repo_root)
            return
        # Persist the choice
        self._app_config.repo_root = chosen
        self._app_config.save()
        if self._repo_root_label is not None:
            self._repo_root_label.configure(text=f"{t('repo_prefix')}{chosen}")
        if hasattr(self, "_log") and self._log is not None:
            self._log.append(t("log_repo_set", path=chosen))

    def _change_repo_root(self) -> None:
        """User-clicked button to re-pick the repo root (frozen mode)."""
        self._prompt_for_repo_root()


    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_topbar(row=0)
        self._build_main(row=1)
        self._build_bottom(row=2)

    def _build_topbar(self, *, row: int) -> None:
        bar = ctk.CTkFrame(self, height=56, corner_radius=0, fg_color=styles.ACCENT)
        bar.grid(row=row, column=0, sticky="ew")
        bar.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            bar,
            text=f"  {t('title')}",
            font=styles.FONT_TITLE,
            text_color="white",
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w", padx=styles.PAD)

        version = ctk.CTkLabel(
            bar, text=f"v{self.version}", font=styles.FONT_SUBTITLE, text_color="#D9EAE5"
        )
        version.grid(row=0, column=1, sticky="e", padx=styles.PAD)

        # Language switcher
        self._lang_switch = ctk.CTkSegmentedButton(
            bar,
            values=[t("lang_en"), t("lang_zh")],
            command=self._on_language,
            height=26,
            font=styles.FONT_SMALL,
        )
        current_lang_label = t("lang_zh") if self._app_config.language == "zh" else t("lang_en")
        self._lang_switch.set(current_lang_label)
        self._lang_switch.grid(row=0, column=2, padx=(0, 4))

        self._theme_switch = ctk.CTkSegmentedButton(
            bar,
            values=[t("theme_light"), t("theme_dark"), t("theme_system")],
            command=self._on_theme,
            height=26,
            font=styles.FONT_SMALL,
        )
        self._theme_switch.set(t(f"theme_{self._app_config.theme.lower()}"))
        self._theme_switch.grid(row=0, column=3, padx=(0, styles.PAD))

    def _build_main(self, *, row: int) -> None:
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=row, column=0, sticky="nsew", padx=styles.PAD, pady=styles.PAD)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Scrollable card grid.
        scroll = ctk.CTkScrollableFrame(
            main, label_text=t("target_agents"), fg_color="transparent"
        )
        scroll.grid(row=0, column=0, sticky="nsew")
        # 4 columns of cards.
        for col in range(4):
            scroll.grid_columnconfigure(col, weight=1, uniform="card")

        specs = agents.all_agents()
        for index, spec in enumerate(specs):
            r, c = divmod(index, 4)
            card = widgets.AgentCard(
                scroll,
                spec,
                on_deploy=self._on_deploy,
                on_verify=self._on_verify,
                on_uninstall=self._on_uninstall,
                on_pick_root=self._on_pick_root,
            )
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            card.set_root_label(self._roots.get(spec.name))
            self._cards[spec.name] = card

        # Refresh button row.
        actions = ctk.CTkFrame(main, fg_color="transparent")
        actions.grid(row=1, column=0, sticky="ew", pady=(styles.PAD, 0))
        actions.grid_columnconfigure(3, weight=1)

        ctk.CTkButton(
            actions, text=t("btn_rescan"), width=110, command=self._refresh_all_detection,
            fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
        ).grid(row=0, column=0, padx=(0, 6))
        ctk.CTkButton(
            actions, text=t("btn_build_all"), width=160, command=self._on_build_all,
            fg_color=styles.ACCENT, hover_color=styles.ACCENT_HOVER,
        ).grid(row=0, column=1, padx=6)
        # In frozen (exe) mode the repo root is chosen by the user, so surface a
        # button to set/inspect it. Source mode hides this (auto-detected).
        if deployer.is_frozen():
            self._repo_root_label = ctk.CTkLabel(
                actions, text=t("repo_not_set"), font=styles.FONT_SMALL, anchor="e",
                text_color=("#6B7480", "#9AA5B1"),
            )
            self._repo_root_label.grid(row=0, column=2, sticky="e", padx=(6, 6))
            ctk.CTkButton(
                actions, text=t("btn_repo"), width=80, command=self._change_repo_root,
                fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
            ).grid(row=0, column=3, padx=(0, 6))
            if deployer.REPO_ROOT is not None:
                self._repo_root_label.configure(text=f"{t('repo_prefix')}{deployer.REPO_ROOT}")
        self._status_label = ctk.CTkLabel(
            actions, text=t("status_ready"), font=styles.FONT_SMALL, anchor="e", text_color=("#6B7480", "#9AA5B1")
        )
        self._status_label.grid(row=0, column=4, sticky="e", padx=styles.PAD)

    def _build_bottom(self, *, row: int) -> None:
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=row, column=0, sticky="ew", padx=styles.PAD, pady=(0, styles.PAD))
        bottom.grid_columnconfigure(0, weight=1)

        self._progress = widgets.ProgressRow(bottom)
        self._progress.grid(row=0, column=0, sticky="ew", pady=(0, styles.PAD_SM))

        self._log = widgets.LogPanel(bottom, height=180)
        self._log.grid(row=1, column=0, sticky="ew")

        # Bottom control row.
        ctrl = ctk.CTkFrame(bottom, fg_color="transparent")
        ctrl.grid(row=2, column=0, sticky="ew", pady=(styles.PAD_SM, 0))
        ctrl.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            ctrl, text=t("btn_clear_log"), width=100, command=self._log.clear,
            fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
        ).grid(row=0, column=0, padx=(0, 6))

        self._stop_btn = ctk.CTkButton(
            ctrl, text=t("btn_stop"), width=100, state="disabled",
            fg_color=styles.DANGER, hover_color=styles.DANGER_HOVER,
            command=self._on_stop,
        )
        self._stop_btn.grid(row=0, column=2, sticky="e")

    # ------------------------------------------------------------------ #
    # Theme
    # ------------------------------------------------------------------ #

    def _on_theme(self, value: str) -> None:
        # Map translated label back to CTk mode
        label_to_mode = {
            t("theme_light"): "light",
            t("theme_dark"): "dark",
            t("theme_system"): "system",
        }
        mode = label_to_mode.get(value, "system")
        ctk.set_appearance_mode(mode)
        self._app_config.theme = mode.capitalize()
        self._app_config.save()

    # ------------------------------------------------------------------ #
    # Language
    # ------------------------------------------------------------------ #

    def _on_language(self, value: str) -> None:
        """Handle language switch."""
        lang: Language = "zh" if value == t("lang_zh") else "en"
        set_language(lang)
        self._app_config.language = lang
        self._app_config.save()
        # Rebuild the entire UI with new language
        self._rebuild_ui()

    def _rebuild_ui(self) -> None:
        """Rebuild the entire UI after language switch."""
        # Update window title
        self.title(f"{t('window_title')}  v{self.version}")

        # Reset specs with new language
        agents.rebuild_specs()

        # Destroy and rebuild all frames
        for widget in self.winfo_children():
            widget.destroy()

        # Reset card dict before rebuild
        self._cards = {}

        # Rebuild layout (includes card creation via _build_main)
        self._build_layout()

        # Refresh detection
        self._refresh_all_detection()

    # ------------------------------------------------------------------ #
    # Detection refresh
    # ------------------------------------------------------------------ #

    def _refresh_all_detection(self) -> None:
        for name, card in self._cards.items():
            root = self._roots.get(name)
            det = detector.detect(name, root)
            card.set_detection(det)

    def _refresh_one(self, spec: AgentSpec) -> None:
        card = self._cards.get(spec.name)
        if card is None:
            return
        det = detector.detect(spec.name, self._roots.get(spec.name))
        card.set_detection(det)

    # ------------------------------------------------------------------ #
    # Root selection
    # ------------------------------------------------------------------ #

    def _on_pick_root(self, spec: AgentSpec) -> None:
        chosen = filedialog.askdirectory(title=t("dlg_select_project_root", name=spec.display_name))
        if not chosen:
            return
        self._roots[spec.name] = Path(chosen)
        card = self._cards.get(spec.name)
        if card is not None:
            card.set_root_label(Path(chosen))
        self._refresh_one(spec)

    def _root_provider(self, spec: AgentSpec) -> Callable[[], "Path | None"]:
        return lambda: self._roots.get(spec.name)

    # ------------------------------------------------------------------ #
    # Job submission
    # ------------------------------------------------------------------ #

    def _submit(self, job, *, busy_card: str | None = None) -> bool:
        if self._worker.is_busy():
            self._log.append(t("log_job_busy"))
            return False
        self._stop_btn.configure(state="normal")
        self._progress.set_ok()
        self._progress.reset(t("progress_starting"))
        self._status_label.configure(text=job.title)
        if busy_card:
            self._cards[busy_card].set_busy(True)
        ok = self._worker.submit(job)
        if not ok:
            self._log.append(t("log_job_rejected"))
            if busy_card:
                self._cards[busy_card].set_busy(False)
            self._stop_btn.configure(state="disabled")
        return ok

    def _on_deploy(self, spec: AgentSpec) -> None:
        if spec.kind == "project" and self._roots.get(spec.name) is None:
            messagebox.showinfo(
                t("dlg_select_root_title"),
                t("dlg_select_root_msg", name=spec.display_name),
            )
            return
        self._log.append(t("log_deploy", name=spec.display_name))
        self._submit(
            make_deploy_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_verify(self, spec: AgentSpec) -> None:
        self._log.append(t("log_verify", name=spec.display_name))
        self._submit(
            make_verify_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_uninstall(self, spec: AgentSpec) -> None:
        if not messagebox.askyesno(
            t("dlg_confirm_uninstall"),
            t("dlg_confirm_uninstall_msg", name=spec.display_name),
        ):
            return
        self._log.append(t("log_uninstall", name=spec.display_name))
        self._submit(
            make_uninstall_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_build_all(self) -> None:
        self._log.append(t("log_build_all"))
        self._submit(make_build_all_job(self.profiles))

    def _on_stop(self) -> None:
        self._worker.request_cancel()
        self._log.append(t("log_cancel"))

    # ------------------------------------------------------------------ #
    # Event loop drain (UI thread)
    # ------------------------------------------------------------------ #

    def _drain_events(self) -> None:
        try:
            while True:
                event: Event = self._worker.events.get_nowait()
                self._handle_event(event)
        except Exception:  # queue.Empty
            pass
        self.after(80, self._drain_events)

    def _handle_event(self, event: Event) -> None:
        if event.kind is EventKind.LOG:
            self._log.append(event.payload)
        elif event.kind is EventKind.PROGRESS:
            fraction, label = event.payload
            self._progress.set(fraction, label)
        elif event.kind is EventKind.STARTED:
            self._status_label.configure(text=event.payload)
            self._progress.set(0.0, event.payload)
        elif event.kind is EventKind.DONE:
            ok, message = event.payload
            self._stop_btn.configure(state="disabled")
            # Re-enable all cards.
            for card in self._cards.values():
                card.set_busy(False)
            # Refresh detection for whichever agent (if any) the job touched.
            for name, card in self._cards.items():
                det = detector.detect(name, self._roots.get(name))
                card.set_detection(det)
            if ok:
                self._progress.set(1.0, f"{t('progress_done')} — {message}")
                self._status_label.configure(text=f"{t('progress_done')} — {message}")
                self._log.append(t("log_done", msg=message))
            else:
                self._progress.set_error(f"{t('progress_failed')} — {message}")
                self._status_label.configure(text=f"{t('progress_failed')} — {message}")
                self._log.append(t("log_error", msg=message))


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def _ensure_customtkinter() -> None:
    try:
        import customtkinter  # noqa: F401
        return
    except ImportError:
        pass
    # customtkinter missing - ask on the console (no root window exists yet).
    print("customtkinter is not installed. It is required for the deployment console.")
    answer = input("Install it now with `pip install customtkinter`? [Y/n] ").strip().lower()
    if answer in ("", "y", "yes"):
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "customtkinter"], check=True)
    else:
        print("Aborting. Install customtkinter and re-run.")
        sys.exit(1)


def main() -> int:
    _ensure_customtkinter()
    app = App()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
