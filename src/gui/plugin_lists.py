# gui/plugin_lists.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Set

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel

# Roles
USERROLE_PLUGIN_NAME = Qt.ItemDataRole.UserRole + 100
USERROLE_PLUGIN_ENABLED = Qt.ItemDataRole.UserRole + 101


def scan_project_plugins(project_root: Path) -> list[tuple[str, bool]]:
    """Return list of (plugin_name, enabled) from <root>/*.uproject."""
    uproject = next(project_root.glob("*.uproject"), None)
    if not uproject or not uproject.is_file():
        return []
    try:
        data = json.loads(uproject.read_text(encoding="utf-8"))
    except Exception:
        return []
    plugins = data.get("Plugins", []) or []
    out: list[tuple[str, bool]] = []
    for entry in plugins:
        name = str(entry.get("Name", "")).strip()
        if not name:
            continue
        enabled = bool(entry.get("Enabled", True))
        out.append((name, enabled))
    # sort by name
    out.sort(key=lambda t: t[0].lower())
    return out


def populate_plugins_model(
        plugins_model: QStandardItemModel,
        project_root: Path,
        preselected_to_remove: Set[str] | None = None,
) -> None:
    """Fill plugins_model with checkable items; checked == remove on build."""
    plugins_model.clear()
    if not project_root.exists():
        return
    pre = set(preselected_to_remove or [])
    for name, enabled in scan_project_plugins(project_root):
        it = QStandardItem(name)
        it.setEditable(False)
        it.setCheckable(True)
        # Checked == remove on build (user intent)
        it.setCheckState(Qt.CheckState.Checked if name in pre else Qt.CheckState.Unchecked)
        # Store metadata
        it.setData(name, USERROLE_PLUGIN_NAME)
        it.setData(enabled, USERROLE_PLUGIN_ENABLED)
        plugins_model.appendRow(it)


def selected_plugins_to_strip(plugins_model: QStandardItemModel) -> list[str]:
    """Return plugin names checked to be removed."""
    out: list[str] = []
    for row in range(plugins_model.rowCount()):
        it = plugins_model.item(row)
        if it.checkState() == Qt.CheckState.Checked:
            out.append(str(it.data(USERROLE_PLUGIN_NAME)))
    return out
