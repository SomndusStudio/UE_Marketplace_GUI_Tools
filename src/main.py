# main.py
import sys
from PySide6.QtWidgets import QApplication
from main_windows import MainWindow
import qdarktheme

import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more verbosity
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

def main():
    app = QApplication(sys.argv)

    # Apply the complete dark theme to your Qt App.
    #qdarktheme.setup_theme()

    app.setStyle("Fusion")
    app.setPalette(qdarktheme.load_palette("dark"))
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
