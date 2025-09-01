# ui_bridge.py
from PySide6.QtCore import QObject, Slot, Qt, QMetaObject, Q_ARG


class UiBridge(QObject):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.ui = ui  # ui.txtLogs, ui.progressBar, etc. vivent dans le thread GUI

    @Slot(str)
    def log(self, text: str):
        # Call appendPlainText on *the widget* via a QueuedConnection
        QMetaObject.invokeMethod(
            self.ui.txtLogs, "appendPlainText",
            Qt.QueuedConnection,
            Q_ARG(str, text),
        )

    @Slot(int)
    def progress(self, value: int):
        QMetaObject.invokeMethod(
            self.ui.progressBar, "setValue",
            Qt.QueuedConnection,
            Q_ARG(int, value),
        )

    @Slot(list)
    def finished(self, paths: list):
        QMetaObject.invokeMethod(
            self.ui.progressBar, "setValue",
            Qt.QueuedConnection,
            Q_ARG(int, 100),
        )
        QMetaObject.invokeMethod(
            self.ui.txtLogs, "appendPlainText",
            Qt.QueuedConnection,
            Q_ARG(str, "Done."),
        )
        # If _restore_idle_state touches the UI, do it via invokeMethod as well
        QMetaObject.invokeMethod(self, "_restore_idle_state_proxy", Qt.QueuedConnection)

    @Slot(str)
    def error(self, msg: str):
        QMetaObject.invokeMethod(
            self.ui.txtLogs, "appendPlainText",
            Qt.QueuedConnection,
            Q_ARG(str, f"ERROR: {msg}"),
        )
        QMetaObject.invokeMethod(self, "_restore_idle_state_proxy", Qt.QueuedConnection)

    @Slot()
    def canceled(self):
        QMetaObject.invokeMethod(
            self.ui.txtLogs, "appendPlainText",
            Qt.QueuedConnection,
            Q_ARG(str, "Canceled."),
        )
        QMetaObject.invokeMethod(self, "_restore_idle_state_proxy", Qt.QueuedConnection)

    @Slot()
    def _restore_idle_state_proxy(self):
        self.parent()._restore_idle_state()
        pass
