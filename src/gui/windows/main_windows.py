# main_windows.py
import logging

from PySide6.QtCore import QThreadPool, Qt, QSettings
from PySide6.QtWidgets import QMainWindow

from src.gui.core.json_settings import Settings
from src.gui.windows.functions_main_window import MainFunctions
from src.gui.windows.setup_main_window import SetupMainWindow
from src.gui.page_one.setup_page_1 import SetupPageOne
from src.gui.windows.ui_main import UI_MainWindow

logger = logging.getLogger(__name__)

from src.core.profiles import (
    Profile, )

USERROLE_VERSION_ID = Qt.ItemDataRole.UserRole
USERROLE_ENGINE_PATH = Qt.ItemDataRole.UserRole + 1

# Roles for plugin list items
USERROLE_PLUGIN_NAME = Qt.ItemDataRole.UserRole + 100
USERROLE_PLUGIN_ENABLED = Qt.ItemDataRole.UserRole + 101


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_profile: Profile | None = None

        # SETUP MAIN WINDOW
        # Load widgets from "gui\uis\main_window\ui_main.py"
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        self.app_settings = QSettings("somndus_studio", "UETemplatePackager")

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # ///////////////////////////////////////////////////////////////
        # Page One Setup
        self.page_one = SetupPageOne(self)
        self.page_one.setup_gui()

        self.thread_pool = QThreadPool.globalInstance()

    def ui_page_one(self):
        """
        Accessor of loaded page on ui elements
        """
        return self.ui.load_pages

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

            # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


