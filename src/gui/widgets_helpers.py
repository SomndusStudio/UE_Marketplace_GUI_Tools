from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QPushButton

from src.gui.core.functions import Functions


def apply_btn_svg_icon(btn: QPushButton, icon_name):
    btn.setIcon(QIcon(Functions.set_svg_icon(icon_name)))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn
