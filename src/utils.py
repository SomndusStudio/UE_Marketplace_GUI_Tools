# utils.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class UEVersion:
    label: str
    engine_path: str

def load_ue_versions(json_path: Path) -> list[UEVersion]:
    """Charge les versions UE depuis un fichier JSON et fait un peu de validation."""
    if not json_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {json_path}")
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"JSON invalide ({json_path}): {e}") from e

    items = data.get("versions", [])
    out: list[UEVersion] = []
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            continue
        label = str(it.get("label", "")).strip()
        path  = str(it.get("engine_path", "")).strip()
        if not label or not path:
            # on ignore les entrées incomplètes
            continue
        out.append(UEVersion(label=label, engine_path=path))
    return out

def build_zip_preview(pattern: str, template_dir: str, version_label: str, version_id: str) -> str:
    """Build a preview filename from the naming pattern."""
    # project = last folder name of the UE project root
    project = Path(template_dir).name or "Project"
    # try to get "5.x" from a label like "UE 5.4" and replace '.' with '_'
    ueversion = version_label.replace("UE", "").strip().replace(".", "_")
    try:
        base = pattern.format(project=project, ueversion=ueversion)
    except Exception:
        # safe fallback if user typed a wrong placeholder
        base = f"{project}_{ueversion}"
    return f"{base}.zip"