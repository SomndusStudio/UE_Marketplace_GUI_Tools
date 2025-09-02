from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from src.gui.windows.ui_main import *
from src.core.profiles import AppVersion, load_versions_catalog, ensure_default_profile_exists
from src.core.version import APP_VERSION, APP_NAME
from src.gui.page_one.actions import AppContext, Actions
from src.gui.page_one.folder_lists import populate_root_entries_model
from src.gui.page_one.plugin_lists import populate_plugins_model
from src.gui.ui_helpers import VersionPreviewDelegate
from src.gui.widgets_helpers import apply_btn_svg_icon

# Typage checking for IDE
if TYPE_CHECKING:
    from src.gui.windows.main_windows import MainWindow  # imported only for type hints


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupPageOne(QObject):

    def __init__(self, w: MainWindow):
        super().__init__()
        self.w = w
        self.ui = self.w.ui

        # Model for QListView
        self.versions_model = QStandardItemModel(self.w)  # holds checkable items
        self.ui_page_one().listVersions.setModel(self.versions_model)

        # Model for the Plugins QListView (checkable items: checked == remove on build)
        self.plugins_model = QStandardItemModel(self.w)
        self.ui_page_one().listPlugins.setModel(self.plugins_model)

        # Model for the root entries (checked == exclude from zip)
        self.root_entries_model = QStandardItemModel(self.w)
        self.ui_page_one().listFolders.setModel(self.root_entries_model)

        # Refresh when project root changes
        self.ui_page_one().edTemplate.textChanged.connect(self._on_project_path_changed)

        # Initial fill
        self._on_project_path_changed()

        # Delegate for version zip name display
        self.preview_delegate = VersionPreviewDelegate( self.ui_page_one().listVersions)
        self.ui_page_one().listVersions.setItemDelegate(self.preview_delegate)

        # UE Versions Catalog loading
        try:
            self.catalog: list[AppVersion] = load_versions_catalog()
        except Exception as e:
            QMessageBox.critical(self.w, "Catalog", f"Failed to load versions catalog: {e}")
            self.catalog = []

        # Build actions controller with a light-weight context
        ctx = AppContext(
            main_window=self.w,
            ui=self.ui,
            versions_model=self.versions_model,
            catalog=self.catalog,
        )
        self.actions = Actions(ctx)

        ensure_default_profile_exists()

    def ui_page_one(self):
        """
        Accessor of loaded page on ui elements
        """
        return self.w.ui_page_one()
    
    def setup_gui(self):
        # Icons
        apply_btn_svg_icon(self.ui_page_one().btnNewProfile, "icon_plus_circle.svg")
        apply_btn_svg_icon(self.ui_page_one().btnRenameProfile, "icon_edit.svg")
        apply_btn_svg_icon(self.ui_page_one().btnRemoveProfile, "icon_delete.svg")
        apply_btn_svg_icon(self.ui_page_one().btnSaveProfile, "icon_save.svg")

        apply_btn_svg_icon(self.ui_page_one().btnBrowseOut, "icon_folder.svg")
        apply_btn_svg_icon(self.ui_page_one().btnBrowseTemplate, "icon_folder.svg")

        apply_btn_svg_icon(self.ui_page_one().btnBuild, "icon_package.svg")
        apply_btn_svg_icon(self.ui_page_one().btnCancel, "icon_cancel.svg")

        apply_btn_svg_icon(self.ui_page_one().btnOpenOut, "icon_folder_open.svg")

        # Listen pattern change
        self.ui_page_one().edPattern.textChanged.connect(self.actions.update_version_previews)

        # Connect UI signals to action methods
        self.ui_page_one().btnBrowseTemplate.clicked.connect(self.actions.on_browse_template)
        self.ui_page_one().btnBrowseOut.clicked.connect(self.actions.on_browse_out)
        self.ui_page_one().btnOpenOut.clicked.connect(self.actions.on_open_out)

        self.ui_page_one().btnNewProfile.clicked.connect(self.actions.on_new_profile_clicked)
        self.ui_page_one().btnRenameProfile.clicked.connect(self.actions.on_rename_profile_clicked)
        self.ui_page_one().btnRemoveProfile.clicked.connect(self.actions.on_delete_profile_clicked)
        self.ui_page_one().btnSaveProfile.clicked.connect(self.actions.on_save_profile_clicked)
        self.ui_page_one().cmbProfile.currentTextChanged.connect(self.actions.on_profile_changed)

        # Build button
        self.ui_page_one().btnBuild.clicked.connect(self.actions.on_build_clicked)
        self.ui_page_one().btnCancel.clicked.connect(self.actions.on_cancel_clicked)

        ensure_default_profile_exists()

        # store app settings under your org/app name
        last_profile = self.w.app_settings.value("last_profile", "Default", type=str) or "Default"

        # Initial load of profiles into combo + apply "Default"
        self.actions.refresh_profiles_combo(select_name=last_profile)

    def _on_project_path_changed(self):
        project_root = Path( self.ui_page_one().edTemplate.text().strip())

        # plugins: use current_profile if you keep it in memory
        pre_plugins = set(getattr(self.w, "current_profile", None).plugins_to_strip or []) \
            if getattr(self.w, "current_profile", None) else set()
        populate_plugins_model(self.plugins_model, project_root, preselected_to_remove=pre_plugins)

        # root entries: if you persist them in profile, pass them here
        pre_excludes = set(getattr(self.w, "current_profile", None).root_excludes or []) \
            if getattr(self.w, "current_profile", None) else set()
        populate_root_entries_model(self.root_entries_model, project_root, preselected_excludes=pre_excludes)

    def check_profile_state(self):
        self._on_project_path_changed()

    def show_about(self):
        """Show About dialog with app name, version, and project link."""
        QMessageBox.about(
            self.w,
            "About",
            f"{APP_NAME} v{APP_VERSION}\n\nUE5 Fab Packaging Tool\n© 2025 SCHARTIER Isaac trading as Somndus Studio\n\nhttps://github.com/SomndusStudio/UE_Marketplace_GUI_Tools",
        )
