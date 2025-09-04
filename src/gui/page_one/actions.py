# actions.py
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, TYPE_CHECKING

from PySide6.QtCore import Qt, QTimer, Slot, QObject
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QFileDialog, QMessageBox, QInputDialog
)

from src.gui.page_one.folder_lists import selected_root_excludes
from src.gui.page_one.plugin_lists import selected_plugins_to_strip
from src.gui.windows.ui_main import UI_MainWindow
from src.gui.workers import BuildParams, BuildWorker, BuildController
from src.core.config import get_seven_zip_path
from src.gui.page_one.ui_bridge import UiBridge

logger = logging.getLogger(__name__)

from src.core.profiles import (
    AppVersion,
    Profile, ProfileVersionRef,
    load_profile, save_profile, list_profile_names,
    resolve_profile_versions_for_ui, rename_profile, remove_profile,
)

from src.gui.ui_helpers import USERROLE_PREVIEW
from src.core.utils import build_zip_preview

# Custom roles for model data
USERROLE_VERSION_ID = Qt.ItemDataRole.UserRole
USERROLE_ENGINE_PATH = Qt.ItemDataRole.UserRole + 1

# Typage checking for IDE
if TYPE_CHECKING:
    from src.gui.windows.main_windows import MainWindow  # imported only for type hints


@dataclass
class AppContext:
    """Light-weight container passed to Actions to avoid circular imports."""
    main_window: MainWindow  # for dialogs/parent
    ui: UI_MainWindow  # Ui_MainWindow instance (has the widgets)
    versions_model: QStandardItemModel
    catalog: List[AppVersion]

    def ui_page_one(self):
        """
        Accessor of loaded page on ui elements
        """
        return self.main_window.ui_page_one()


class Actions(QObject):
    """All UI event handlers live here (button clicks, menu actions, etc.)."""

    def __init__(self, ctx: AppContext):
        self.build_ctrl = None
        self.ctx = ctx
        super().__init__(ctx.main_window)

    # ---------- Public handlers ----------

    def on_browse_template(self):
        """Let the user pick the UE project directory."""
        d = QFileDialog.getExistingDirectory(self.ctx.main_window, "Select UE project root")
        if d:
            self.ctx.ui_page_one().edTemplate.setText(d)

    def on_browse_out(self):
        """Let the user pick the output directory."""
        d = QFileDialog.getExistingDirectory(self.ctx.main_window, "Select output directory")
        if d:
            self.ctx.ui_page_one().edOut.setText(d)

    def on_open_out(self):
        """Open output directory if it exists."""
        p = Path(self.ctx.ui_page_one().edOut.text().strip())
        if not p.exists():
            QMessageBox.warning(self.ctx.main_window, "Output", "Output directory does not exist.")
            return
        from PySide6.QtGui import QDesktopServices
        from PySide6.QtCore import QUrl
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))

    # Slots
    def on_profile_changed(self, name: str):
        try:
            prof = load_profile(name)
            self._apply_profile_to_ui(prof)

            # persist last selected profile
            self.ctx.main_window.app_settings.setValue("last_profile", name)

        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Profiles", f"Failed to load profile '{name}': {e}")

    def on_save_profile_clicked(self):
        prof = self._build_profile_from_ui()  # keep current combo name
        try:
            save_profile(prof)
        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Profiles", f"Failed to save profile: {e}")
            return
        QMessageBox.information(self.ctx.main_window, "Profiles", f"Profile '{prof.name}' saved.")
        self.refresh_profiles_combo(select_name=prof.name)

    def on_new_profile_clicked(self):
        name, ok = QInputDialog.getText(self.ctx.main_window, "New Profile", "Profile name:")
        if not ok or not name.strip():
            return
        new_prof = Profile(
            name=name.strip(),
            template_dir="",
            output_dir="",
            zip_pattern="{project}_{ueversion}",
            versions=[],  # start empty; user can tick versions and paths will come from catalog
        )
        try:
            save_profile(new_prof)
        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Profiles", f"Failed to create profile: {e}")
            return
        self.refresh_profiles_combo(select_name=new_prof.name)

    def on_delete_profile_clicked(self):
        prof = self._build_profile_from_ui()  # keep current combo name

        # Guard clause: do not allow deleting the default profile
        if prof.name == "default":
            QMessageBox.warning(
                self.ctx.main_window,
                "Profiles",
                "The default profile cannot be deleted."
            )
            return

        try:
            remove_profile(prof.name)
        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Profiles", f"Failed to remove profile: {e}")
            return
        QMessageBox.information(self.ctx.main_window, "Profiles", f"Profile '{prof.name}' removed.")
        self.refresh_profiles_combo(select_name=prof.name)

    # ---------- Profiles combo refresh ----------

    def refresh_profiles_combo(self, select_name: str | None = None):
        """Reload profiles combo and re-apply the current profile to UI."""
        names = list_profile_names()
        self.ctx.ui_page_one().cmbProfile.blockSignals(True)
        self.ctx.ui_page_one().cmbProfile.clear()
        self.ctx.ui_page_one().cmbProfile.addItems(names)
        self.ctx.ui_page_one().cmbProfile.blockSignals(False)

        target = select_name or (names[0] if names else "Default")
        idx = self.ctx.ui_page_one().cmbProfile.findText(target)
        if idx >= 0:
            self.ctx.ui_page_one().cmbProfile.setCurrentIndex(idx)

        # Trigger applying selected profile
        self.on_profile_changed(self.ctx.ui_page_one().cmbProfile.currentText())

    # ---------- Helpers (private) ----------

    def _apply_profile_to_ui(self, profile: Profile):
        """Fill text fields and the list view from the joined data."""
        self.ctx.main_window.current_profile = profile

        self.ctx.ui_page_one().edTemplate.setText(profile.template_dir)
        self.ctx.ui_page_one().edOut.setText(profile.output_dir)
        self.ctx.ui_page_one().edPattern.setText(profile.zip_pattern or "{project}_{ueversion}")

        # Build items: one per catalog entry; fallback to catalog path if profile has empty override
        self.ctx.versions_model.clear()
        joined = resolve_profile_versions_for_ui(profile, self.ctx.catalog)
        for appv, ref in joined:
            eff_path = ref.engine_path if ref.engine_path else appv.engine_path
            self._append_version_item(appv.id, appv.label, eff_path, ref.checked)

        # Refresh plugin checked
        # TODO : Only when path not change but profile yes so maybe another checked
        self.ctx.main_window.page_one.check_profile_state()

    def _append_version_item(self, version_id: str, label: str, engine_path: str, checked: bool):
        """Append a single checkable row into the list model."""
        it = QStandardItem(label)
        it.setEditable(False)
        it.setCheckable(True)
        it.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)
        it.setData(version_id, USERROLE_VERSION_ID)
        it.setData(engine_path, USERROLE_ENGINE_PATH)

        # NEW: compute and store the preview text
        pattern = self.ctx.ui_page_one().edPattern.text().strip() or "{project}_{ueversion}"
        template_dir = self.ctx.ui_page_one().edTemplate.text().strip()
        preview = build_zip_preview(pattern, template_dir, label)
        it.setData(preview, USERROLE_PREVIEW)

        self.ctx.versions_model.appendRow(it)

    def _build_profile_from_ui(self, name: str | None = None) -> Profile:
        """Serialize current UI state into a Profile object."""
        refs: list[ProfileVersionRef] = []
        for row in range(self.ctx.versions_model.rowCount()):
            it = self.ctx.versions_model.item(row)
            refs.append(ProfileVersionRef(
                version_id=str(it.data(USERROLE_VERSION_ID)),
                engine_path=str(it.data(USERROLE_ENGINE_PATH) or ""),
                checked=(it.checkState() == Qt.CheckState.Checked),
            ))

        plugins_to_strip = selected_plugins_to_strip(self.ctx.main_window.page_one.plugins_model)
        root_excludes = selected_root_excludes(self.ctx.main_window.page_one.root_entries_model)

        return Profile(
            name=name or self.ctx.ui_page_one().cmbProfile.currentText() or "Default",
            template_dir=self.ctx.ui_page_one().edTemplate.text().strip(),
            output_dir=self.ctx.ui_page_one().edOut.text().strip(),
            zip_pattern=self.ctx.ui_page_one().edPattern.text().strip() or "{project}_{ueversion}",
            versions=refs,
            plugins_to_strip=plugins_to_strip,
            root_excludes=root_excludes
        )

    def get_checked_versions(self) -> List[Tuple[str, str]]:
        """Return checked rows as (version_id, engine_path)."""
        out: list[tuple[str, str]] = []
        for row in range(self.ctx.versions_model.rowCount()):
            it = self.ctx.versions_model.item(row)
            if it.checkState() == Qt.CheckState.Checked:
                vid = str(it.data(USERROLE_VERSION_ID))
                ep = str(it.data(USERROLE_ENGINE_PATH) or "")
                out.append((vid, ep))
        return out

    def _label_for_id(self, version_id: str) -> str:
        """Find display label for a catalog id (fallback to id if missing)."""
        for v in self.ctx.catalog:
            if v.id == version_id:
                return v.label
        return version_id

    def update_version_previews(self):
        """Recompute preview filenames for all rows when pattern or project path changes."""
        pattern = self.ctx.ui_page_one().edPattern.text().strip() or "{project}_UE{ueversion}_{date}"
        template_dir = self.ctx.ui_page_one().edTemplate.text().strip()

        for row in range(self.ctx.main_window.page_one.versions_model.rowCount()):
            it = self.ctx.main_window.page_one.versions_model.item(row)
            label = it.text()
            preview = build_zip_preview(pattern, template_dir, label)
            it.setData(preview, USERROLE_PREVIEW)

        # Trigger repaint so VersionPreviewDelegate updates immediately
        self.ctx.ui_page_one().listVersions.viewport().update()

    def on_rename_profile_clicked(self):
        """Prompt user for a new profile name and rename the JSON file."""
        old_name = self.ctx.ui_page_one().cmbProfile.currentText()
        if not old_name:
            return
        new_name, ok = QInputDialog.getText(
            self.ctx.main_window, "Rename Profile", f"New name for '{old_name}':"
        )
        if not ok or not new_name.strip():
            return

        try:
            rename_profile(old_name, new_name.strip())
        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Profiles", f"Failed to rename: {e}")
            return

        QMessageBox.information(self.ctx.main_window, "Profiles", f"Profile renamed to '{new_name.strip()}'.")
        self.refresh_profiles_combo(select_name=new_name.strip())

    def on_cancel_clicked(self):
        if getattr(self, "build_ctrl", None):
            self.build_ctrl.cancel()
            self.ctx.ui_page_one().txtLogs.appendPlainText("Cancel requested…")

    def on_build_clicked(self):
        """Collect checked versions and kick off the build pipeline (placeholder)."""
        template_dir = Path(self.ctx.ui_page_one().edTemplate.text().strip())
        output_dir = Path(self.ctx.ui_page_one().edOut.text().strip())
        pattern = self.ctx.ui_page_one().edPattern.text().strip() or "{project}_{ueversion}"

        # Guard clause: validate template_dir and output_dir
        if not template_dir.exists() or not template_dir.is_dir():
            QMessageBox.critical(
                self.ctx.main_window,
                "Build",
                f"Invalid template directory: {template_dir}"
            )
            return

        if not output_dir.exists() or not output_dir.is_dir():
            QMessageBox.critical(
                self.ctx.main_window,
                "Build",
                f"Invalid output directory: {output_dir}"
            )
            return

        # collect checked versions with labels
        checked: list[tuple[str, str, str]] = []  # (version_id, version_label, engine_path)

        for row in range(self.ctx.versions_model.rowCount()):
            it = self.ctx.versions_model.item(row)
            if it.checkState() == Qt.CheckState.Checked:
                vid = str(it.data(USERROLE_VERSION_ID))
                ep = str(it.data(USERROLE_ENGINE_PATH) or "")
                label = it.text()  # display label from catalog, e.g. "UE 5.4"
                checked.append((vid, label, ep))

        # Guard clause: must have at least one version checked
        if not checked:
            QMessageBox.critical(
                self.ctx.main_window,
                "Error",
                "You must select at least one UE5 Version before continuing."
            )
            return

        # Get seven zip path from config
        seven_zip_path = get_seven_zip_path(self.ctx)

        # Guard clause: if seven_zip_path doesn't exist → show error and exit
        if not seven_zip_path.exists():
            QMessageBox.critical(
                self.ctx.main_window,
                "Error",
                f"7-Zip path not found: {seven_zip_path}"
            )
            return

        plugins_to_strip = set(selected_plugins_to_strip(self.ctx.main_window.page_one.plugins_model))
        root_excludes = set(selected_root_excludes(self.ctx.main_window.page_one.root_entries_model))

        logger.info("Plugins marked for removal: %s", plugins_to_strip)
        logger.info("Root files/directories marked for exclude: %s", root_excludes)

        # Worker Builder
        params = BuildParams(
            project_root=template_dir,
            output_dir=output_dir,
            pattern=pattern,
            selections=checked,  # list of (version_id, version_label, engine_path)
            seven_zip_path=seven_zip_path,
            plugins_to_strip=plugins_to_strip,
            root_excludes=root_excludes,
        )
        worker = BuildWorker(params)
        self.build_ctrl = BuildController(worker, parent_thread_parent=self.ctx.main_window)

        # créé dans le thread GUI
        self.ui_bridge = UiBridge(self.ctx.ui_page_one(), parent=self)

        # wire signals to UI
        self.build_ctrl.connect_signals(
            ui_bridge=self.ui_bridge,
        )

        # UI state
        self.ctx.ui_page_one().txtLogs.clear()
        self.ctx.ui_page_one().progressBar.setValue(0)
        self.ctx.ui_page_one().btnBuild.setEnabled(False)
        self.ctx.ui_page_one().btnCancel.setEnabled(True)

        self.build_ctrl.start()

    @Slot(str)
    def _on_build_log(self, text: str):
        logger.info("_on_build_log")

        self.ctx.ui_page_one().txtLogs.appendPlainText(text)

    @Slot(int)
    def _on_build_progress(self, value: int):
        logger.info(f'_on_build_progress : {value}')
        self.ctx.ui_page_one().progressBar.setValue(value)

    @Slot(list)
    def _on_build_done(self):
        logger.info("_on_build_done")

        self.ctx.ui_page_one().progressBar.setValue(100)

        self.ctx.ui_page_one().txtLogs.appendPlainText("Done.")
        self._restore_idle_state()

    @Slot(str)
    def _on_build_error(self, msg: str):
        logger.info("_on_build_error")

        self.ctx.ui_page_one().txtLogs.appendPlainText(f"ERROR: {msg}")
        self._restore_idle_state()

    @Slot()
    def _on_build_canceled(self):
        logger.info("_on_build_canceled")

        self.ctx.ui_page_one().txtLogs.appendPlainText("Canceled.")
        self._restore_idle_state()

    def _restore_idle_state(self):
        logger.info("_restore_idle_state")

        # UI state
        self.ctx.ui_page_one().btnBuild.setEnabled(True)
        self.ctx.ui_page_one().btnCancel.setEnabled(False)

        ctrl = getattr(self, "build_ctrl", None)
        if not ctrl:
            return

        # Request thread end
        if ctrl.thread.isRunning():
            ctrl.thread.quit()

        # Avoid calling .wait() directly here (risk of crash/delays)
        # Defer the wait to the next event loop iteration.
        def _finalize():
            try:
                if ctrl.thread.isRunning():
                    ctrl.thread.wait(5000)  # timeout de sécurité
            except Exception:
                pass
            # Free memory ref
            if getattr(self, "build_ctrl", None) is ctrl:
                self.build_ctrl = None

        QTimer.singleShot(0, _finalize)
