# main.py
import logging
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.core.version import APP_VERSION, APP_NAME
from src.gui.main_windows import MainWindow

# important: this registers the compiled resources in Qt
from src.gui import resources_rc

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

    app.setStyle("Fusion")

    w = MainWindow()
    w.setWindowIcon(icon)

    # Num version
    w.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")

    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
