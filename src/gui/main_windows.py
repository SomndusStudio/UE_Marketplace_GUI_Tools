# main_windows.py
import logging
from pathlib import Path

import qdarktheme
from PySide6.QtCore import QThreadPool, Qt, QSettings
from PySide6.QtGui import QStandardItemModel, QAction, QActionGroup
from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication

from src.core.version import APP_VERSION, APP_NAME
from src.gui.folder_lists import populate_root_entries_model
from src.gui.plugin_lists import populate_plugins_model
from src.gui.ui_helpers import VersionPreviewDelegate
from src.windows.ui_project_fab_windows import Ui_MainWindow

logger = logging.getLogger(__name__)

from src.core.profiles import (
    AppVersion,
    Profile, load_versions_catalog, ensure_default_profile_exists,
)

from src.gui.actions import Actions, AppContext

USERROLE_VERSION_ID = Qt.ItemDataRole.UserRole
USERROLE_ENGINE_PATH = Qt.ItemDataRole.UserRole + 1

# Roles for plugin list items
USERROLE_PLUGIN_NAME = Qt.ItemDataRole.UserRole + 100
USERROLE_PLUGIN_ENABLED = Qt.ItemDataRole.UserRole + 101


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_profile: Profile | None = None

        self.settings = QSettings("YourOrg", "UETemplatePackager")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionAbout.triggered.connect(self.show_about)

        # Settings to remember last theme
        self.settings = getattr(self, "settings", QSettings("YourOrg", "UETabTools"))

        # Create "Theme" menu in menubar (if not already in your .ui)
        self.menuTheme = self.ui.menuTheme

        self.actThemeLight = QAction("Light", self, checkable=True)
        self.actThemeDark = QAction("Dark", self, checkable=True)

        self.setup_theme()

        # Model for QListView
        self.versions_model = QStandardItemModel(self)  # holds checkable items
        self.ui.listVersions.setModel(self.versions_model)

        # Model for the Plugins QListView (checkable items: checked == remove on build)
        self.plugins_model = QStandardItemModel(self)
        self.ui.listPlugins.setModel(self.plugins_model)

        # Model for the root entries (checked == exclude from zip)
        self.root_entries_model = QStandardItemModel(self)
        self.ui.listFolders.setModel(self.root_entries_model)

        # Refresh when project root changes
        self.ui.edTemplate.textChanged.connect(self._on_project_path_changed)

        # Initial fill
        self._on_project_path_changed()

        # Delegate for version zip name display
        self.preview_delegate = VersionPreviewDelegate(self.ui.listVersions)
        self.ui.listVersions.setItemDelegate(self.preview_delegate)

        try:
            self.catalog: list[AppVersion] = load_versions_catalog()
        except Exception as e:
            QMessageBox.critical(self, "Catalog", f"Failed to load versions catalog: {e}")
            self.catalog = []

        # Build actions controller with a light-weight context
        ctx = AppContext(
            main_window=self,
            ui=self.ui,
            versions_model=self.versions_model,
            catalog=self.catalog,
        )
        self.actions = Actions(ctx)

        # Listen pattern change
        self.ui.edPattern.textChanged.connect(self.actions.update_version_previews)

        # Connect UI signals to action methods
        self.ui.btnBrowseTemplate.clicked.connect(self.actions.on_browse_template)
        self.ui.btnBrowseOut.clicked.connect(self.actions.on_browse_out)
        self.ui.btnOpenOut.clicked.connect(self.actions.on_open_out)

        self.ui.btnNewProfile.clicked.connect(self.actions.on_new_profile_clicked)
        self.ui.btnRenameProfile.clicked.connect(self.actions.on_rename_profile_clicked)
        self.ui.btnSaveProfile.clicked.connect(self.actions.on_save_profile_clicked)
        self.ui.cmbProfile.currentTextChanged.connect(self.actions.on_profile_changed)

        # Build button
        self.ui.btnBuild.clicked.connect(self.actions.on_build_clicked)
        self.ui.btnCancel.clicked.connect(self.actions.on_cancel_clicked)

        ensure_default_profile_exists()

        # store app settings under your org/app name
        last_profile = self.settings.value("last_profile", "Default", type=str) or "Default"

        # Initial load of profiles into combo + apply "Default"
        self.actions.refresh_profiles_combo(select_name=last_profile)

        self.thread_pool = QThreadPool.globalInstance()

    def setup_theme(self):
        grp = QActionGroup(self)
        grp.addAction(self.actThemeLight)
        grp.addAction(self.actThemeDark)
        grp.setExclusive(True)

        self.menuTheme.addAction(self.actThemeLight)
        self.menuTheme.addAction(self.actThemeDark)

        self.actThemeLight.triggered.connect(lambda: self.apply_theme("light"))
        self.actThemeDark.triggered.connect(lambda: self.apply_theme("dark"))

        # Restore last theme from settings (default: dark)
        last_theme = self.settings.value("theme", "dark", type=str) or "dark"
        self.apply_theme(last_theme)

    def apply_theme(self, mode: str):
        """Apply light/dark theme and persist selection."""
        app = QApplication.instance()
        if app is None:
            return

        # Try modern qdarktheme if available
        if qdarktheme:
            # load_palette + load_stylesheet handles both modes ("light"/"dark")
            try:
                app.setPalette(qdarktheme.load_palette(mode))
                app.setStyleSheet(qdarktheme.load_stylesheet(mode))
            except Exception:
                # minimal fallback: remove stylesheet, keep default palette
                app.setStyleSheet("")

        # Update action checks
        is_dark = (mode.lower() == "dark")
        self.actThemeDark.setChecked(is_dark)
        self.actThemeLight.setChecked(not is_dark)

        # Persist
        self.settings.setValue("theme", "dark" if is_dark else "light")

    def _on_project_path_changed(self):
        project_root = Path(self.ui.edTemplate.text().strip())

        # plugins: use current_profile if you keep it in memory
        pre_plugins = set(getattr(self, "current_profile", None).plugins_to_strip or []) \
            if getattr(self, "current_profile", None) else set()
        populate_plugins_model(self.plugins_model, project_root, preselected_to_remove=pre_plugins)

        # root entries: if you persist them in profile, pass them here
        pre_excludes = set(getattr(self, "current_profile", None).root_excludes or []) \
            if getattr(self, "current_profile", None) else set()
        populate_root_entries_model(self.root_entries_model, project_root, preselected_excludes=pre_excludes)

    def check_profile_state(self):
        self._on_project_path_changed()

    def show_about(self):
        """Show About dialog with app name, version, and project link."""
        QMessageBox.about(
            self,
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\nUE5 Fab Packaging Tool\n© 2025 SCHARTIER Isaac trading as Somndus Studio\n\nhttps://github.com/SomndusStudio/UE_Marketplace_GUI_Tools",
        )
