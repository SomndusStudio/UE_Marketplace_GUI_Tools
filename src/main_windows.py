# windows.py
import json
from pathlib import Path

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem, QFileDialog, QInputDialog
from PySide6.QtCore import QThreadPool, Qt, QSettings

from src.ui_helpers import VersionPreviewDelegate
from src.utils import UEVersion, load_ue_versions
from windows.ui_project_fab_windows import Ui_MainWindow

import logging
logger = logging.getLogger(__name__)

from profiles import (
    AppVersion,
    Profile, ProfileVersionRef,
    load_versions_catalog, resolve_profile_versions_for_ui,
    list_profile_names, load_profile, save_profile, ensure_default_profile_exists,
)

from actions import Actions, AppContext

USERROLE_VERSION_ID = Qt.UserRole
USERROLE_ENGINE_PATH = Qt.UserRole + 1

# Roles for plugin list items
USERROLE_PLUGIN_NAME = Qt.UserRole + 100
USERROLE_PLUGIN_ENABLED = Qt.UserRole + 101

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_profile: Profile | None = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Model for QListView
        self.versions_model = QStandardItemModel(self)  # holds checkable items
        self.ui.listVersions.setModel(self.versions_model)

        # Model for the Plugins QListView (checkable items: checked == remove on build)
        self.plugins_model = QStandardItemModel(self)
        self.ui.listPlugins.setModel(self.plugins_model)

        # Re-scan plugins whenever the project path changes
        self.ui.edTemplate.textChanged.connect(self.rescan_plugins_from_project)

        # Initial scan (if a path is already filled)
        self.rescan_plugins_from_project()

        # Delegate for version zip name display
        self.preview_delegate = VersionPreviewDelegate(self.ui.listVersions)
        self.ui.listVersions.setItemDelegate(self.preview_delegate)

        # Resolve project root and config file
        ROOT_DIR = Path(__file__).resolve().parent.parent
        CONFIG_FILE = ROOT_DIR / "configs" / "ue_versions.json"

        print("ROOT_DIR =", ROOT_DIR)
        print("CONFIG_FILE =", CONFIG_FILE, "exists?", CONFIG_FILE.exists())

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

        ensure_default_profile_exists()

        # store app settings under your org/app name
        self.settings = QSettings("YourOrg", "UETemplatePackager")
        last_profile = self.settings.value("last_profile", "Default", type=str)

        # Initial load of profiles into combo + apply "Default"
        self.actions.refresh_profiles_combo(select_name=last_profile)

        self.thread_pool = QThreadPool.globalInstance()

    def rescan_plugins_from_project(self):
        """Scan the .uproject under the selected project root and populate the plugins list."""

        project_root = Path(self.ui.edTemplate.text().strip())
        preselected_to_remove = set(self.current_profile.plugins_to_strip or []) if self.current_profile else set()

        self.populate_plugins_from_project(project_root, preselected_to_remove=preselected_to_remove)

    def populate_plugins_from_project(self, project_root: Path, preselected_to_remove: set[str] | None = None):
        """Fill listPlugins with detected plugins. Checked == 'remove on build'."""
        self.plugins_model.clear()
        if not project_root.exists():
            return

        uproject = None
        for p in project_root.glob("*.uproject"):
            if p.is_file():
                uproject = p
                break
        if not uproject:
            return

        try:
            data = json.loads(uproject.read_text(encoding="utf-8"))
        except Exception:
            return

        plugins = data.get("Plugins", []) or []
        pre = set(preselected_to_remove or [])

        # Sort by name for stable display
        def _name(e): return str(e.get("Name", "")).strip().lower()
        for entry in sorted(plugins, key=_name):
            name = str(entry.get("Name", "")).strip()
            if not name:
                continue
            enabled = bool(entry.get("Enabled", True))

            it = QStandardItem(name)
            it.setEditable(False)
            it.setCheckable(True)
            # Checked == remove on build (user intent)
            it.setCheckState(Qt.CheckState.Checked if name in pre else Qt.CheckState.Unchecked)
            # Store metadata
            it.setData(name, USERROLE_PLUGIN_NAME)
            it.setData(enabled, USERROLE_PLUGIN_ENABLED)
            self.plugins_model.appendRow(it)

    def selected_plugins_to_strip(self) -> list[str]:
        """Return the list of plugin names the user marked for removal (checked rows)."""
        out: list[str] = []
        for row in range(self.plugins_model.rowCount()):
            it = self.plugins_model.item(row)
            if it.checkState() == Qt.CheckState.Checked:
                out.append(str(it.data(USERROLE_PLUGIN_NAME)))
        return out