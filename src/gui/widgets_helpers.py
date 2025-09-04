from PySide6.QtGui import QIcon, Qt, QPixmap, QPainter, QColor
from PySide6.QtWidgets import QPushButton

from src.gui.core.functions import Functions


def apply_btn_svg_icon(btn: QPushButton, icon_name):
    btn.setIcon(QIcon(Functions.set_svg_icon(icon_name)))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    return btn

def apply_colorize_svg_icon(btn: QPushButton, icon_name, color: QColor):
    pixmap = QPixmap(Functions.set_svg_icon(icon_name))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    btn.setIcon(QIcon(pixmap))
    btn.setCursor(Qt.CursorShape.PointingHandCursor)