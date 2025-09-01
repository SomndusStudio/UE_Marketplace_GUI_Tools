# ui_helpers.py

from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QPainter, Qt, QPalette, QPen, QFontMetrics
from PySide6.QtWidgets import QStyledItemDelegate

USERROLE_PREVIEW = Qt.ItemDataRole.UserRole + 2  # holds the preview string


class VersionPreviewDelegate(QStyledItemDelegate):
    """Paints the normal checkbox + label, then a gray preview right below the label (not over the checkbox)."""

    def paint(self, painter: QPainter, option, index):
        # First draw the default item (checkbox + main text)
        super().paint(painter, option, index)

        preview = index.data(USERROLE_PREVIEW)
        if not preview:
            return

        # Font for the preview
        f = option.font
        f.setPointSizeF(max(8.0, f.pointSizeF() - 1))
        f.setItalic(True)

        fm = QFontMetrics(f)

        # Compute rect for preview: start after the checkbox and label baseline
        main_text = index.data(Qt.DisplayRole) or ""
        main_width = fm.horizontalAdvance(main_text)

        # Rough offset: checkbox width (approx 20) + text width
        x_offset = option.rect.x() + 120 + fm.horizontalAdvance(main_text) + 8
        rect = QRect(
            x_offset,
            option.rect.y(),
            option.rect.width() - (x_offset - option.rect.x()),
            option.rect.height()
        )

        # Gray disabled color
        pal: QPalette = option.palette
        pen = QPen(pal.color(QPalette.Disabled, QPalette.Text))

        painter.save()
        painter.setPen(pen)
        painter.setFont(f)

        elided = fm.elidedText(preview, Qt.ElideMiddle, rect.width())
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, elided)
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        # keep base height (no extra line, since we draw on same line)
        return super().sizeHint(option, index)
