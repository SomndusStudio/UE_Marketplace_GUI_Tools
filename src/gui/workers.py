# workers.py
from __future__ import annotations

import threading
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence, Tuple

from PySide6.QtCore import QObject, Signal, Slot, QThread, Qt

# Import your build orchestrator and the cancel helper
from src.core.builder import build_zip_set
from src.gui.page_one.ui_bridge import UiBridge


@dataclass(frozen=True)
class BuildParams:
    """Immutable parameters for a build run."""
    project_root: Path
    output_dir: Path
    pattern: str
    # selections: list of (version_id, version_label, engine_path)
    selections: Sequence[Tuple[str, str, str]]
    seven_zip_path: Optional[Path] = None
    # optional: plugins to strip (names)
    plugins_to_strip: Optional[set[str]] = None
    # optional: root file/directories to excludes (names)
    root_excludes: Optional[set[str]] = None


class BuildWorker(QObject):
    """
    Cancellable worker that runs the build in a background thread.
    Emits logs, progress and completion/error signals.
    """
    sig_log = Signal(str)  # human-readable log line
    sig_progress = Signal(int)  # 0..100
    sig_finished = Signal(list)  # list[Path] of produced zips (as str)
    sig_error = Signal(str)  # error message + optional traceback
    sig_canceled = Signal()  # build was canceled cooperatively

    def __init__(self, params: BuildParams):
        super().__init__()
        self._params = params
        self._cancel_event = threading.Event()

    # -------- Public API -------- #

    @Slot()
    def run(self):
        """Entry point to start the build work (call when the QThread starts)."""
        try:
            outputs = build_zip_set(
                project_root=self._params.project_root,
                out_dir=self._params.output_dir,
                pattern=self._params.pattern,
                selections=self._params.selections,
                seven_zip=self._params.seven_zip_path,
                plugins_to_strip=self._params.plugins_to_strip,
                excludes=self._params.root_excludes,
                # wire callbacks to Qt signals
                on_log=self._on_log,
                on_progress=self._on_progress,
                on_check_cancel=self._on_check_cancel,

            )
        except RuntimeError as e:
            # Convention: builder raises RuntimeError("Canceled") on cancel
            if "Canceled" in str(e):
                self.sig_canceled.emit()
                return
            self.sig_error.emit(str(e))
            return
        except Exception as e:
            tb = traceback.format_exc()
            self.sig_error.emit(f"{e}\n{tb}")
            return

        # Success
        # Convert Path objects to str for signal serialization if needed
        self.sig_finished.emit([str(p) for p in outputs])

    def cancel(self):
        """Request cooperative cancellation."""
        self._cancel_event.set()
        # Note: actual process termination is handled inside builder via on_check_cancel.

    # -------- Callback bridges (builder -> Qt) -------- #

    def _on_log(self, msg: str):
        # Keep callbacks lightweight; Qt will queue the signal across threads
        self.sig_log.emit(msg)

    def _on_progress(self, value: int):
        # Clamp to 0..100 just in case
        v = 0 if value < 0 else 100 if value > 100 else value
        self.sig_progress.emit(v)

    def _on_check_cancel(self) -> bool:
        return self._cancel_event.is_set()


# -------- Helper to wire worker + thread easily -------- #

class BuildController:
    """
    Small helper to manage QThread lifecycle around BuildWorker.
    Usage:
        ctrl = BuildController(worker)
        ctrl.start()
        ...
        ctrl.cancel()
        ctrl.wait()
    """

    def __init__(self, worker: BuildWorker, parent_thread_parent: Optional[QObject] = None):
        self.thread = QThread(parent_thread_parent)
        self.worker = worker
        self.worker.moveToThread(self.thread)

        # Ensure cleanup when thread finishes
        self.thread.finished.connect(self.thread.deleteLater)

    def connect_signals(
            self,
            ui_bridge: UiBridge,
    ):
        self.worker.sig_log.connect(ui_bridge.log, Qt.ConnectionType.QueuedConnection)
        self.worker.sig_progress.connect(ui_bridge.progress, Qt.ConnectionType.QueuedConnection)
        self.worker.sig_finished.connect(ui_bridge.finished, Qt.ConnectionType.QueuedConnection)
        self.worker.sig_error.connect(ui_bridge.error, Qt.ConnectionType.QueuedConnection)
        self.worker.sig_canceled.connect(ui_bridge.canceled, Qt.ConnectionType.QueuedConnection)

    def start(self):
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def cancel(self):
        self.worker.cancel()

    def wait(self, msecs: int = -1):
        """Block until thread stops (msecs=-1 means forever)."""
        self.thread.quit()
        self.thread.wait(msecs)
