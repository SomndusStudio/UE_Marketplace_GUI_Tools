# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from src.core.qt_core import *
from src.gui.core.theme import Theme
from src.gui.widgets_helpers import apply_colorize_svg_icon


# PY TITLE BUTTON
# ///////////////////////////////////////////////////////////////
class PyTitleButton(QPushButton):
    def __init__(
        self,
        parent,
        app_parent = None,
        theme: Theme = None,
        tooltip_text = "",
        btn_id = None,
        width = 30,
        height = 30,
        icon_path = "no_icon.svg",
        is_active = False
    ):
        super().__init__()

        self.theme = theme

        if (btn_id is None):
            self.setObjectName("title_button")
        else :
            self.setObjectName(btn_id)

        # SET DEFAULT PARAMETERS
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._top_margin = self.height() + 6
        self._is_active = is_active
        # Set Parameters
        self._set_icon_path = icon_path
        self._set_icon_color = self.theme.get("icon_color")
        # Parent
        self._parent = parent
        self._app_parent = app_parent

        # Icon
        self.refresh()

        # TOOLTIP
        self._tooltip_text = tooltip_text
        self._tooltip = _ToolTip(
            app_parent,
            tooltip_text
        )
        self._tooltip.hide()

    def refresh(self):
        apply_colorize_svg_icon(self, self._set_icon_path, QColor(self._set_icon_color))

    def set_icon(self, icon_path):
        self._set_icon_path = icon_path
        self.refresh()

    # SET ACTIVE MENU
    # ///////////////////////////////////////////////////////////////
    def set_active(self, is_active):
        self._is_active = is_active
        if self._is_active:
            apply_colorize_svg_icon(self, self._set_icon_path, QColor(self.theme.get("context_color")))
        else:
            apply_colorize_svg_icon(self, self._set_icon_path, QColor(self.theme.get("bg_two")))

        self.repaint()

    # RETURN IF IS ACTIVE MENU
    # ///////////////////////////////////////////////////////////////
    def is_active(self):
        return self._is_active

    # CHANGE STYLES
    # Functions with custom styles
    # ///////////////////////////////////////////////////////////////
    def change_style(self, event):
        if event == QEvent.Type.Enter:
            self._set_icon_color = self.theme.get("icon_hover")
            self.refresh()
        elif event == QEvent.Type.Leave:
            self._set_icon_color = self.theme.get("icon_color")
            self.refresh()
        elif event == QEvent.Type.MouseButtonPress:
            self._set_icon_color = self.theme.get("icon_pressed")
            self.refresh()
        elif event == QEvent.Type.MouseButtonRelease:
            self._set_icon_color = self.theme.get("icon_hover")
            self.refresh()

    # MOUSE OVER
    # Event triggered when the mouse is over the BTN
    # ///////////////////////////////////////////////////////////////
    def enterEvent(self, event):
        self.change_style(QEvent.Type.Enter)
        self.move_tooltip()
        self._tooltip.show()

    # MOUSE LEAVE
    # Event fired when the mouse leaves the BTN
    # ///////////////////////////////////////////////////////////////
    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.change_style(QEvent.Type.Leave)
        self.move_tooltip()
        self._tooltip.hide()

    # MOUSE PRESS
    # Event triggered when the left button is pressed
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_style(QEvent.Type.MouseButtonPress)
            self.setFocus()
        return super().mousePressEvent(event)

    # MOUSE RELEASED
    # Event triggered after the mouse button is released
    # ///////////////////////////////////////////////////////////////
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_style(QEvent.Type.MouseButtonRelease)
        return super().mouseReleaseEvent(event)

    # MOVE TOOLTIP
    # ///////////////////////////////////////////////////////////////
    def move_tooltip(self):
        # GET MAIN WINDOW PARENT
        gp = self.mapToGlobal(QPoint(0, 0))

        # SET WIDGET TO GET POSTION
        # Return absolute position of widget inside app
        pos = self._parent.mapFromGlobal(gp)

        # FORMAT POSITION
        # Adjust tooltip position with offset
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin

        # SET POSITION TO WIDGET
        # Move tooltip position
        self._tooltip.move(pos_x, pos_y)

# TOOLTIP
# ///////////////////////////////////////////////////////////////
class _ToolTip(QLabel):
    def __init__(
        self,
        parent, 
        tooltip,
    ):
        QLabel.__init__(self)

        # LABEL SETUP
        self.setObjectName(u"label_tooltip")
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()
        self.setMinimumWidth(self.width() + 40)

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
