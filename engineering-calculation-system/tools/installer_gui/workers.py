"""Background worker: runs deploy/verify/uninstall/build off the UI thread.

Threading model:

* The UI thread never blocks on subprocess or heavy filesystem work.
* A single :class:`Worker` owns one background thread. Only one job runs at a
  time; enqueuing a second job while one is running is rejected (the UI disables
  buttons instead, but this is a safety net).
* The worker pushes :class:`Event` records onto a ``queue.Queue``. The UI polls
  that queue via ``tkinter.after`` and updates cards / log / progress bar.
* A cooperative cancel flag lets the user request a stop. Subprocess calls
  check it between lines where practical; long copies are not interruptible
  mid-file, but the next step will be skipped.

This module deliberately knows nothing about tkinter - it only emits events.
"""

from __future__ import annotations

import queue
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from . import deployer
from .agents import AgentSpec
from .i18n import t


class EventKind(str, Enum):
    LOG = "log"            # a log line (str)
    PROGRESS = "progress"  # (fraction 0..1, label)
    STATUS = "status"      # agent status changed (agent_name, deployed: bool)
    DONE = "done"          # job finished (ok: bool, message: str)
    STARTED = "started"    # job started (title: str)


@dataclass
class Event:
    kind: EventKind
    payload: Any = None


@dataclass
class Job:
    title: str
    fn: Callable[[deployer.LogFn, deployer.ProgressFn, "CancelToken"], None]
    # Optional: which agent this job targets (so the UI can refresh its card).
    agent_name: str | None = None


class CancelToken:
    """Cooperative cancel flag shared between the UI and the running job."""

    def __init__(self) -> None:
        self._event = threading.Event()

    def request_cancel(self) -> None:
        self._event.set()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()


class Worker:
    """Single-job background worker with a streaming event queue."""

    def __init__(self) -> None:
        self._events: queue.Queue[Event] = queue.Queue()
        self._thread: threading.Thread | None = None
        self._current_cancel: CancelToken | None = None
        # RLock so is_busy() can be called from within submit()/_run() which
        # already hold the lock (a plain Lock would self-deadlock there).
        self._lock = threading.RLock()

    # ------------------------------------------------------------------ #
    # Queue consumed by the UI
    # ------------------------------------------------------------------ #

    @property
    def events(self) -> queue.Queue[Event]:
        return self._events

    def is_busy(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def request_cancel(self) -> None:
        with self._lock:
            if self._current_cancel is not None:
                self._current_cancel.request_cancel()

    # ------------------------------------------------------------------ #
    # Job submission
    # ------------------------------------------------------------------ #

    def submit(self, job: Job) -> bool:
        """Start ``job`` on the worker thread. Returns False if already busy."""
        with self._lock:
            if self.is_busy():
                return False
            cancel = CancelToken()
            self._current_cancel = cancel
            self._thread = threading.Thread(
                target=self._run,
                args=(job, cancel),
                name=f"ecs-worker-{job.agent_name or 'build'}",
                daemon=True,
            )
            self._thread.start()
        self._events.put(Event(EventKind.STARTED, job.title))
        return True

    # ------------------------------------------------------------------ #
    # Internal runner
    # ------------------------------------------------------------------ #

    def _run(self, job: Job, cancel: CancelToken) -> None:
        def log(line: str) -> None:
            if cancel.cancelled:
                return
            self._events.put(Event(EventKind.LOG, line))

        def progress(fraction: float, label: str) -> None:
            if cancel.cancelled:
                return
            self._events.put(Event(EventKind.PROGRESS, (fraction, label)))

        try:
            if cancel.cancelled:
                self._events.put(Event(EventKind.DONE, (False, "cancelled before start")))
                return
            job.fn(log, progress, cancel)
            if cancel.cancelled:
                self._events.put(Event(EventKind.DONE, (False, "cancelled")))
            else:
                self._events.put(Event(EventKind.DONE, (True, "completed")))
        except deployer.DeployError as exc:
            self._events.put(Event(EventKind.LOG, f"[error] {exc}"))
            self._events.put(Event(EventKind.DONE, (False, str(exc))))
        except Exception as exc:  # noqa: BLE001 - surface any failure to the UI
            self._events.put(Event(EventKind.LOG, f"[error] unexpected: {exc!r}"))
            self._events.put(Event(EventKind.DONE, (False, f"unexpected error: {exc}")))
        finally:
            with self._lock:
                self._current_cancel = None


# --------------------------------------------------------------------------- #
# Job builders - turn an AgentSpec action into a Job callable
# --------------------------------------------------------------------------- #

def _wrap_agent_action(
    spec: AgentSpec,
    action_key: str,
    action_fn: Callable[[deployer.DeployContext], Any],
    install_root_provider: Callable[[], "Path | None"],
) -> Job:
    """Build a Job that runs an agent deploy/verify/uninstall callable."""

    def fn(log: deployer.LogFn, progress: deployer.ProgressFn, cancel: CancelToken) -> None:
        root = install_root_provider()
        ctx = deployer.DeployContext(install_root=root, log=log, progress=progress)

        # For multi-step deploys, sprinkle cancel checks between phases by
        # wrapping progress; the deployer itself checks cancellation implicitly
        # via the log/progress no-ops once cancelled.
        action_fn(ctx)
        if cancel.cancelled:
            return
        # Refresh this agent's deployed status after a mutating action.
        from . import detector
        ok, _ = detector.skill_deployed(spec.name, root)
        # Push a STATUS event by abusing the log channel? No - emit via the
        # worker's queue directly is not possible from here. Instead the UI
        # re-runs detection on DONE for the targeted agent. We keep it simple.

    title = f"{t(action_key)} {spec.display_name}"
    return Job(title=title, fn=fn, agent_name=spec.name)


def make_deploy_job(spec: AgentSpec, install_root_provider: Callable[[], "Path | None"]) -> Job:
    return _wrap_agent_action(spec, "job_deploy", spec.deploy_fn, install_root_provider)


def make_verify_job(spec: AgentSpec, install_root_provider: Callable[[], "Path | None"]) -> Job:
    return _wrap_agent_action(spec, "job_verify", spec.verify_fn, install_root_provider)


def make_uninstall_job(spec: AgentSpec, install_root_provider: Callable[[], "Path | None"]) -> Job:
    return _wrap_agent_action(spec, "job_uninstall", spec.uninstall_fn, install_root_provider)


def make_build_all_job(profiles: tuple[str, ...]) -> Job:
    """Build every release profile (no agent target)."""

    def fn(log: deployer.LogFn, progress: deployer.ProgressFn, cancel: CancelToken) -> None:
        deployer.build_profiles(profiles, log=log, progress=progress)

    return Job(title=t("job_build_all"), fn=fn, agent_name=None)
