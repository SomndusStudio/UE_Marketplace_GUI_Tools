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

from src.core.qt_core import *

from src.gui.core.functions import *
from src.gui.core.theme import Theme


# CUSTOM LEFT MENU
# ///////////////////////////////////////////////////////////////
class PyLeftMenuButton(QPushButton):
    def __init__(
            self,
            app_parent,
            text,
            theme: Theme = None,
            btn_id=None,
            tooltip_text="",
            margin=4,
            icon_path="icon_add_user.svg",
            icon_active_menu="active_menu.svg",
            is_active=False,
            is_active_tab=False,
            is_toggle_active=False
    ):
        super().__init__()

        self.theme = theme
        self.setText(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(btn_id)

        # APP PATH
        self._icon_path = Functions.set_svg_icon(icon_path)
        self._icon_active_menu = Functions.set_svg_icon(icon_active_menu)

        # PROPERTIES
        self._margin = margin

        self._dark_one = self.theme.get("dark_one")
        self._dark_three = self.theme.get("dark_three")
        self._dark_four = self.theme.get("dark_four")
        self._bg_one = self.theme.get("bg_one")

        self._icon_color = self.theme.get("icon_color")
        self._icon_color_hover = self.theme.get("icon_hover")
        self._icon_color_pressed = self.theme.get("icon_pressed")
        self._icon_color_active = self.theme.get("icon_active")

        self._context_color = self.theme.get("context_color")
        self._set_icon_color = self.theme.get("icon_color")  # Set icon color
        self._set_bg_color = self.theme.get("dark_one")  # Set BG color
        self._set_text_foreground = self.theme.get("text_foreground")
        self._set_text_active = self.theme.get("text_active")
        self._parent = app_parent
        self._is_active = is_active
        self._is_active_tab = is_active_tab
        self._is_toggle_active = is_toggle_active

        # TOOLTIP
        self._tooltip_text = tooltip_text
        self.tooltip = _ToolTip(
            app_parent,
            tooltip_text
        )
        self.tooltip.hide()

    # PAINT EVENT
    # ///////////////////////////////////////////////////////////////
    def paintEvent(self, event):
        # PAINTER
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setFont(self.font())

        # RECTANGLES
        rect_inside = QRect(4, 5, self.width() - 8, self.height() - 10)
        rect_icon = QRect(0, 0, 50, self.height())
        rect_blue = QRect(4, 5, 20, self.height() - 10)
        rect_inside_active = QRect(7, 5, self.width(), self.height() - 10)
        rect_text = QRect(45, 0, self.width() - 50, self.height())

        if self._is_active:
            # DRAW BG BLUE
            p.setBrush(QColor(self._context_color))
            p.drawRoundedRect(rect_blue, 8, 8)

            # BG INSIDE
            p.setBrush(QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)

            # DRAW ACTIVE
            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())

            # DRAW TEXT
            p.setPen(QColor(self._set_text_active))
            p.drawText(rect_text, Qt.AlignmentFlag.AlignVCenter, self.text())

            # DRAW ICONS
            self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        elif self._is_active_tab:
            # DRAW BG BLUE
            p.setBrush(QColor(self._dark_four))
            p.drawRoundedRect(rect_blue, 8, 8)

            # BG INSIDE
            p.setBrush(QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)

            # DRAW ACTIVE
            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())

            # DRAW TEXT
            p.setPen(QColor(self._set_text_active))
            p.drawText(rect_text, Qt.AlignmentFlag.AlignVCenter, self.text())

            # DRAW ICONS
            self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        # NORMAL BG
        else:
            if self._is_toggle_active:
                # BG INSIDE
                p.setBrush(QColor(self._dark_three))
                p.drawRoundedRect(rect_inside, 8, 8)

                # DRAW TEXT
                p.setPen(QColor(self._set_text_foreground))
                p.drawText(rect_text, Qt.AlignmentFlag.AlignVCenter, self.text())

                # DRAW ICONS
                if self._is_toggle_active:
                    self.icon_paint(p, self._icon_path, rect_icon, self._context_color)
                else:
                    self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)
            else:
                # BG INSIDE
                p.setBrush(QColor(self._set_bg_color))
                p.drawRoundedRect(rect_inside, 8, 8)

                # DRAW TEXT
                p.setPen(QColor(self._set_text_foreground))
                p.drawText(rect_text, Qt.AlignmentFlag.AlignVCenter, self.text())

                # DRAW ICONS
                self.icon_paint(p, self._icon_path, rect_icon, self._set_icon_color)

        p.end()

        # SET ACTIVE MENU
        # ///////////////////////////////////////////////////////////////

    def set_active(self, is_active):
        self._is_active = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    # SET ACTIVE TAB MENU
    # ///////////////////////////////////////////////////////////////
    def set_active_tab(self, is_active):
        self._is_active_tab = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    # RETURN IF IS ACTIVE MENU
    # ///////////////////////////////////////////////////////////////
    def is_active(self):
        return self._is_active

    # RETURN IF IS ACTIVE TAB MENU
    # ///////////////////////////////////////////////////////////////
    def is_active_tab(self):
        return self._is_active_tab

    # SET ACTIVE TOGGLE
    # ///////////////////////////////////////////////////////////////
    def set_active_toggle(self, is_active):
        self._is_toggle_active = is_active

    # SET ICON
    # ///////////////////////////////////////////////////////////////
    def set_icon(self, icon_path):
        self._icon_path = icon_path
        self.repaint()

    # DRAW ICON WITH COLORS
    # ///////////////////////////////////////////////////////////////
    def icon_paint(self, qp, image, rect, color):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

    # DRAW ACTIVE ICON / RIGHT SIDE
    # ///////////////////////////////////////////////////////////////
    def icon_active(self, qp, image, width):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), self.theme.get("bg_one"))
        qp.drawPixmap(width - 5, 0, icon)
        painter.end()

    # CHANGE STYLES
    # Functions with custom styles
    # ///////////////////////////////////////////////////////////////
    def change_style(self, event):
        if event == QEvent.Type.Enter:
            if not self._is_active:
                self._set_icon_color = self.theme.get("icon_hover")
                self._set_bg_color = self.theme.get("dark_three")
            self.repaint()
        elif event == QEvent.Type.Leave:
            if not self._is_active:
                self._set_icon_color = self.theme.get("icon_color")
                self._set_bg_color = self.theme.get("dark_one")
            self.repaint()
        elif event == QEvent.Type.MouseButtonPress:
            if not self._is_active:
                self._set_icon_color = self.theme.get("context_color")
                self._set_bg_color = self.theme.get("dark_four")
            self.repaint()
        elif event == QEvent.Type.MouseButtonRelease:
            if not self._is_active:
                self._set_icon_color = self.theme.get("icon_hover")
                self._set_bg_color = self.theme.get("dark_three")
            self.repaint()

    # MOUSE OVER
    # Event triggered when the mouse is over the BTN
    # ///////////////////////////////////////////////////////////////
    def enterEvent(self, event):
        self.change_style(QEvent.Type.Enter)
        if self.width() == 50 and self._tooltip_text:
            self.move_tooltip()
            self.tooltip.show()

    # MOUSE LEAVE
    # Event fired when the mouse leaves the BTN
    # ///////////////////////////////////////////////////////////////
    def leaveEvent(self, event):
        self.change_style(QEvent.Type.Leave)
        self.tooltip.hide()

    # MOUSE PRESS
    # Event triggered when the left button is pressed
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_style(QEvent.Type.MouseButtonPress)
            self.tooltip.hide()
            return self.clicked.emit()
        return None

    # MOUSE RELEASED
    # Event triggered after the mouse button is released
    # ///////////////////////////////////////////////////////////////
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.change_style(QEvent.Type.MouseButtonRelease)
            return self.released.emit()
        return None

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
        pos_x = pos.x() + self.width() + 5
        pos_y = pos.y() + (self.width() - self.tooltip.height()) // 2

        # SET POSITION TO WIDGET
        # Move tooltip position
        self.tooltip.move(pos_x, pos_y)


class _ToolTip(QLabel):
    def __init__(
            self,
            parent,
            tooltip
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
