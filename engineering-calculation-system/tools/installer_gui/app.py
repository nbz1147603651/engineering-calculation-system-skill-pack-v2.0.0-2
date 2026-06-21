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

from . import agents, deployer, detector, styles, widgets
from .agents import AgentSpec
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
        self.title(f"{styles.WINDOW_TITLE}  v{self.version}")
        self.minsize(styles.WINDOW_MIN_W, styles.WINDOW_MIN_H)

        # In frozen (exe) mode the deployer cannot locate the skill-pack repo
        # from its own __file__, so ask the user up front (or honor ECS_REPO_ROOT).
        # In source mode the deployer auto-detects it.
        self._init_repo_root()
        ctk.set_appearance_mode("system")
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
        Frozen mode: honor ECS_REPO_ROOT, else prompt the user to pick the
        skill-pack repo folder. If the user cancels, the UI still opens but
        every deploy will fail with a clear message until a root is chosen.
        """
        if not deployer.is_frozen():
            return
        env_root = os.environ.get("ECS_REPO_ROOT")
        if env_root:
            try:
                deployer.set_repo_root(Path(env_root))
                return
            except deployer.DeployError:
                pass  # env value was stale; fall through to prompt
        # Defer the prompt until the window is fully up so the dialog is modal
        # to a real window. Use a short after() to let __init__ finish layout.
        self.after(50, self._prompt_for_repo_root)

    def _prompt_for_repo_root(self) -> None:
        chosen = filedialog.askdirectory(
            title="Select the Engineering Calculation System skill-pack repository folder"
            "\n(contains tools/build_release.py)"
        )
        if not chosen:
            self._log and self._log.append(
                "[warn] no repo root selected. Pick one with the 'Repo…' button before deploying."
            )
            return
        try:
            deployer.set_repo_root(Path(chosen))
        except deployer.DeployError as exc:
            messagebox.showerror("Invalid repo folder", str(exc))
            self.after(50, self._prompt_for_repo_root)
            return
        if self._repo_root_label is not None:
            self._repo_root_label.configure(text=f"repo: {chosen}")
        if hasattr(self, "_log") and self._log is not None:
            self._log.append(f"[repo] skill-pack root set to {chosen}")

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
            text=f"  Engineering Calculation System — Deployment Console",
            font=styles.FONT_TITLE,
            text_color="white",
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="w", padx=styles.PAD)

        version = ctk.CTkLabel(
            bar, text=f"v{self.version}", font=styles.FONT_SUBTITLE, text_color="#D9EAE5"
        )
        version.grid(row=0, column=1, sticky="e", padx=styles.PAD)

        self._theme_switch = ctk.CTkSegmentedButton(
            bar,
            values=["Light", "Dark", "System"],
            command=self._on_theme,
            height=26,
            font=styles.FONT_SMALL,
        )
        self._theme_switch.set("System")
        self._theme_switch.grid(row=0, column=2, padx=(0, styles.PAD))

    def _build_main(self, *, row: int) -> None:
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=row, column=0, sticky="nsew", padx=styles.PAD, pady=styles.PAD)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Scrollable card grid.
        scroll = ctk.CTkScrollableFrame(
            main, label_text="Target Agents", fg_color="transparent"
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
            actions, text="Re-scan", width=110, command=self._refresh_all_detection,
            fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
        ).grid(row=0, column=0, padx=(0, 6))
        ctk.CTkButton(
            actions, text="Build all profiles", width=160, command=self._on_build_all,
            fg_color=styles.ACCENT, hover_color=styles.ACCENT_HOVER,
        ).grid(row=0, column=1, padx=6)
        # In frozen (exe) mode the repo root is chosen by the user, so surface a
        # button to set/inspect it. Source mode hides this (auto-detected).
        if deployer.is_frozen():
            self._repo_root_label = ctk.CTkLabel(
                actions, text="repo: (not set)", font=styles.FONT_SMALL, anchor="e",
                text_color=("#6B7480", "#9AA5B1"),
            )
            self._repo_root_label.grid(row=0, column=2, sticky="e", padx=(6, 6))
            ctk.CTkButton(
                actions, text="Repo…", width=80, command=self._change_repo_root,
                fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
            ).grid(row=0, column=3, padx=(0, 6))
            if deployer.REPO_ROOT is not None:
                self._repo_root_label.configure(text=f"repo: {deployer.REPO_ROOT}")
        self._status_label = ctk.CTkLabel(
            actions, text="ready", font=styles.FONT_SMALL, anchor="e", text_color=("#6B7480", "#9AA5B1")
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
            ctrl, text="Clear log", width=100, command=self._log.clear,
            fg_color=("#5B6B79", "#3F4753"), hover_color=("#4A5865", "#343B45"),
        ).grid(row=0, column=0, padx=(0, 6))

        self._stop_btn = ctk.CTkButton(
            ctrl, text="Stop", width=100, state="disabled",
            fg_color=styles.DANGER, hover_color=styles.DANGER_HOVER,
            command=self._on_stop,
        )
        self._stop_btn.grid(row=0, column=2, sticky="e")

    # ------------------------------------------------------------------ #
    # Theme
    # ------------------------------------------------------------------ #

    def _on_theme(self, value: str) -> None:
        ctk.set_appearance_mode(value.lower())

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
        chosen = filedialog.askdirectory(title=f"Select project root for {spec.display_name}")
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
            self._log.append("[warn] a job is already running; wait for it to finish.")
            return False
        self._stop_btn.configure(state="normal")
        self._progress.set_ok()
        self._progress.reset("starting…")
        self._status_label.configure(text=job.title)
        if busy_card:
            self._cards[busy_card].set_busy(True)
        ok = self._worker.submit(job)
        if not ok:
            self._log.append("[warn] worker rejected the job.")
            if busy_card:
                self._cards[busy_card].set_busy(False)
            self._stop_btn.configure(state="disabled")
        return ok

    def _on_deploy(self, spec: AgentSpec) -> None:
        if spec.kind == "project" and self._roots.get(spec.name) is None:
            messagebox.showinfo(
                "Select project root",
                f"Pick a project root for {spec.display_name} first (Folder… button).",
            )
            return
        self._log.append(f"=== Deploy {spec.display_name} ===")
        self._submit(
            make_deploy_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_verify(self, spec: AgentSpec) -> None:
        self._log.append(f"=== Verify {spec.display_name} ===")
        self._submit(
            make_verify_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_uninstall(self, spec: AgentSpec) -> None:
        if not messagebox.askyesno(
            "Confirm uninstall",
            f"Remove the Engineering Calculation System files for {spec.display_name}?\n"
            f"Existing files are backed up; only this package's managed files are removed.",
        ):
            return
        self._log.append(f"=== Uninstall {spec.display_name} ===")
        self._submit(
            make_uninstall_job(spec, self._root_provider(spec)),
            busy_card=spec.name,
        )

    def _on_build_all(self) -> None:
        self._log.append("=== Build all release profiles ===")
        self._submit(make_build_all_job(self.profiles))

    def _on_stop(self) -> None:
        self._worker.request_cancel()
        self._log.append("[warn] cancel requested; finishing current step…")

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
                self._progress.set(1.0, f"done — {message}")
                self._status_label.configure(text=f"done — {message}")
                self._log.append(f"[done] {message}")
            else:
                self._progress.set_error(f"failed — {message}")
                self._status_label.configure(text=f"failed — {message}")
                self._log.append(f"[error] {message}")


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
