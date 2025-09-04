# main.py
import logging
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.core.version import APP_VERSION, APP_NAME
from src.gui.windows.main_windows import MainWindow

# important: this registers the compiled resources in Qt
# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more verbosity
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    app = QApplication(sys.argv)

    # App icon
    icon = QIcon(":/app.ico")
    app.setWindowIcon(icon)

    w = MainWindow()
    w.setWindowIcon(icon)

    # Num version
    w.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")

    w.show()

    w.ui.theme.apply(app)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
