# # gui/folder_lists.py
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Set

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

# Roles
USERROLE_ENTRY_NAME = Qt.ItemDataRole.UserRole + 200
USERROLE_ENTRY_IS_DIR = Qt.ItemDataRole.UserRole + 201

DEFAULT_HIDDEN_ROOT: set[str] = {
    "Binaries", "Build", "Intermediate", "DerivedDataCache", "Saved", "Content", "Config",
    ".git", ".gitattributes", ".gitignore",
}


def discover_root_entries(project_root: Path, extra_hidden: Iterable[str] = ()) -> list[Path]:
    """Return root-level paths to display (sorted: dirs first), excluding hidden."""
    if not project_root or not project_root.exists():
        return []

    hidden = set(DEFAULT_HIDDEN_ROOT) | set(extra_hidden)
    entries: list[Path] = []

    for child in project_root.iterdir():
        name = child.name
        if name in hidden:
            continue
        # hide the .uproject itself by name
        if name.endswith(".uproject"):
            continue
        entries.append(child)
    entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    return entries


def populate_root_entries_model(
        root_model: QStandardItemModel,
        project_root: Path,
        preselected_excludes: Set[str] | None = None,
) -> None:
    """Fill root_model with checkable items; checked == exclude from zip."""
    root_model.clear()
    if not project_root.exists():
        return
    pre = set(preselected_excludes or [])
    # also find a specific .uproject file to hide by exact name
    uproject = next(project_root.glob("*.uproject"), None)
    extra_hidden = {uproject.name} if uproject else set()
    for path in discover_root_entries(project_root, extra_hidden):
        name = path.name
        it = QStandardItem(name)
        it.setEditable(False)
        it.setCheckable(True)
        it.setCheckState(Qt.CheckState.Checked if name in pre else Qt.CheckState.Unchecked)
        it.setData(name, USERROLE_ENTRY_NAME)
        it.setData(path.is_dir(), USERROLE_ENTRY_IS_DIR)
        root_model.appendRow(it)


def selected_root_excludes(root_model: QStandardItemModel) -> list[str]:
    """Return names marked as excluded from zip."""
    out: list[str] = []
    for row in range(root_model.rowCount()):
        it = root_model.item(row)
        if it.checkState() == Qt.CheckState.Checked:
            out.append(str(it.data(USERROLE_ENTRY_NAME)))
    return out
