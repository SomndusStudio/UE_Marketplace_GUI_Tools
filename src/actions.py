# actions.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PySide6.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QInputDialog
)
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt, QObject

import logging
logger = logging.getLogger(__name__)

from profiles import (
    AppVersion,
    Profile, ProfileVersionRef,
    load_profile, save_profile, list_profile_names,
    resolve_profile_versions_for_ui, rename_profile,
)
from src.builder import build_zip_set
from src.ui_helpers import USERROLE_PREVIEW
from src.utils import build_zip_preview

# Custom roles for model data
USERROLE_VERSION_ID = Qt.UserRole
USERROLE_ENGINE_PATH = Qt.UserRole + 1


@dataclass
class AppContext:
    """Light-weight container passed to Actions to avoid circular imports."""
    main_window: QMainWindow          # for dialogs/parent
    ui: QObject                       # Ui_MainWindow instance (has the widgets)
    versions_model: QStandardItemModel
    catalog: List[AppVersion]


class Actions:
    """All UI event handlers live here (button clicks, menu actions, etc.)."""

    def __init__(self, ctx: AppContext):
        self.ctx = ctx

    # ---------- Public handlers (connect these to signals) ----------

    def on_browse_template(self):
        """Let the user pick the UE project directory."""
        d = QFileDialog.getExistingDirectory(self.ctx.main_window, "Select UE project root")
        if d:
            self.ctx.ui.edTemplate.setText(d)

    def on_browse_out(self):
        """Let the user pick the output directory."""
        d = QFileDialog.getExistingDirectory(self.ctx.main_window, "Select output directory")
        if d:
            self.ctx.ui.edOut.setText(d)

    def on_open_out(self):
        """Open output directory if it exists."""
        p = Path(self.ctx.ui.edOut.text().strip())
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
            self.ctx.main_window.settings.setValue("last_profile", name)

        except Exception as e:
            QMessageBox.critical(self, "Profiles", f"Failed to load profile '{name}': {e}")

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
    # ---------- Profiles combo refresh ----------

    def refresh_profiles_combo(self, select_name: str | None = None):
        """Reload profiles combo and re-apply the current profile to UI."""
        names = list_profile_names()
        self.ctx.ui.cmbProfile.blockSignals(True)
        self.ctx.ui.cmbProfile.clear()
        self.ctx.ui.cmbProfile.addItems(names)
        self.ctx.ui.cmbProfile.blockSignals(False)

        target = select_name or (names[0] if names else "Default")
        idx = self.ctx.ui.cmbProfile.findText(target)
        if idx >= 0:
            self.ctx.ui.cmbProfile.setCurrentIndex(idx)

        # Trigger applying selected profile
        self.on_profile_changed(self.ctx.ui.cmbProfile.currentText())

    # ---------- Helpers (private) ----------

    def _apply_profile_to_ui(self, profile: Profile):
        """Fill text fields and the list view from the joined data."""
        self.ctx.main_window.current_profile = profile

        self.ctx.ui.edTemplate.setText(profile.template_dir)
        self.ctx.ui.edOut.setText(profile.output_dir)
        self.ctx.ui.edPattern.setText(profile.zip_pattern or "{project}_{ueversion}")

        # Build items: one per catalog entry; fallback to catalog path if profile has empty override
        self.ctx.versions_model.clear()
        joined = resolve_profile_versions_for_ui(profile, self.ctx.catalog)
        for appv, ref in joined:
            eff_path = ref.engine_path if ref.engine_path else appv.engine_path
            self._append_version_item(appv.id, appv.label, eff_path, ref.checked)

        # Refresh plugin checked
        self.ctx.main_window.rescan_plugins_from_project()

    def _append_version_item(self, version_id: str, label: str, engine_path: str, checked: bool):
        """Append a single checkable row into the list model."""
        it = QStandardItem(label)
        it.setEditable(False)
        it.setCheckable(True)
        it.setCheckState(Qt.Checked if checked else Qt.Unchecked)
        it.setData(version_id, USERROLE_VERSION_ID)
        it.setData(engine_path, USERROLE_ENGINE_PATH)

        # NEW: compute and store the preview text
        pattern = self.ctx.ui.edPattern.text().strip() or "{project}_{ueversion}"
        template_dir = self.ctx.ui.edTemplate.text().strip()
        preview = build_zip_preview(pattern, template_dir, label, id)
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
                checked=(it.checkState() == Qt.Checked),
            ))

        plugins_to_strip = self.ctx.main_window.selected_plugins_to_strip()

        return Profile(
            name=name or self.ctx.ui.cmbProfile.currentText() or "Default",
            template_dir=self.ctx.ui.edTemplate.text().strip(),
            output_dir=self.ctx.ui.edOut.text().strip(),
            zip_pattern=self.ctx.ui.edPattern.text().strip() or "{project}_{ueversion}",
            versions=refs,
            plugins_to_strip=plugins_to_strip
        )

    def get_checked_versions(self) -> List[Tuple[str, str]]:
        """Return checked rows as (version_id, engine_path)."""
        out: list[tuple[str, str]] = []
        for row in range(self.ctx.versions_model.rowCount()):
            it = self.ctx.versions_model.item(row)
            if it.checkState() == Qt.Checked:
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
        pattern = self.ctx.ui.edPattern.text().strip() or "{project}_UE{ueversion}_{date}"
        template_dir = self.ctx.ui.edTemplate.text().strip()

        for row in range(self.ctx.main_window.versions_model.rowCount()):
            it = self.ctx.main_window.versions_model.item(row)
            label = it.text()
            vid = str(it.data(USERROLE_VERSION_ID))
            preview = build_zip_preview(pattern, template_dir, label, vid)
            it.setData(preview, USERROLE_PREVIEW)

        # Trigger repaint so VersionPreviewDelegate updates immediately
        self.ctx.ui.listVersions.viewport().update()

    def on_rename_profile_clicked(self):
        """Prompt user for a new profile name and rename the JSON file."""
        old_name = self.ctx.ui.cmbProfile.currentText()
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

    def on_build_clicked(self):
        """Collect checked versions and kick off the build pipeline (placeholder)."""
        template_dir = Path(self.ctx.ui.edTemplate.text().strip())
        output_dir = Path(self.ctx.ui.edOut.text().strip())
        pattern = self.ctx.ui.edPattern.text().strip() or "{project}_{ueversion}"

        # clean ui
        self.ctx.ui.txtLogs.clear()
        self.ctx.ui.progressBar.setValue(0)

        # collect checked versions with labels
        checked: list[tuple[str, str, str]] = []  # (version_id, version_label, engine_path)

        for row in range(self.ctx.versions_model.rowCount()):
            it = self.ctx.versions_model.item(row)
            if it.checkState() == Qt.CheckState.Checked:
                vid = str(it.data(USERROLE_VERSION_ID))
                ep = str(it.data(USERROLE_ENGINE_PATH) or "")
                label = it.text()  # display label from catalog, e.g. "UE 5.4"
                checked.append((vid, label, ep))

        # Todo from auto/config file
        seven_zip_path = Path("C:/Program Files/7-Zip/7z.exe")

        plugins_to_strip = set(self.ctx.main_window.selected_plugins_to_strip())

        logger.info("Plugins marked for removal: %s", plugins_to_strip)

        try:
            outputs = build_zip_set(
                project_root=template_dir,
                out_dir=output_dir,
                pattern=pattern,
                selections=checked,
                seven_zip=seven_zip_path,
                remove_plugins=True,  # per your requirement
                plugins_to_strip=plugins_to_strip,
                on_log=lambda msg: self.ctx.ui.txtLogs.appendPlainText(msg),
                on_progress=lambda p: self.ctx.ui.progressBar.setValue(p),
            )
        except Exception as e:
            QMessageBox.critical(self.ctx.main_window, "Build", f"Build failed:\n{e}")
            return

        #QMessageBox.information(self.ctx.main_window, "Build done", "Created:\n" + "\n".join(map(str, outputs)))