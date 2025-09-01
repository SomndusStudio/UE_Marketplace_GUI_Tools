# path_helpers.py
import json
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Return directory where the exe (frozen) or project (dev) lives."""
    if getattr(sys, "frozen", False):
        # running from the packaged exe
        return Path(sys.executable).parent
    # dev mode
    return Path(__file__).resolve().parents[2]


def get_configs_dir() -> Path:
    """Return <project_root>/configs."""
    p = get_project_root() / "configs"
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_catalog_path() -> Path:
    """Return <project_root>/configs/ue_versions.json, creating it with defaults if missing."""
    cfg_dir = get_configs_dir()
    path = cfg_dir / "ue_versions.json"

    if not path.exists():
        default_data = {
            "versions": [
                {"id": "ue54", "label": "UE 5.4", "engine_path": "C:/Program Files/Epic Games/UE_5.4"},
                {"id": "ue55", "label": "UE 5.5", "engine_path": "C:/Program Files/Epic Games/UE_5.5"},
                {"id": "ue56", "label": "UE 5.6", "engine_path": "C:/Program Files/Epic Games/UE_5.6"},
            ]
        }
        # write JSON nicely formatted
        path.write_text(json.dumps(default_data, indent=2), encoding="utf-8")

    return path


def get_profiles_dir() -> Path:
    """Return <project_root>/configs/profiles."""
    p = get_configs_dir() / "profiles"
    p.mkdir(parents=True, exist_ok=True)
    return p


def profile_path(name: str) -> Path:
    """Return path for a given profile JSON file."""
    safe = name.strip().replace("/", "_").replace("\\", "_")
    return get_profiles_dir() / f"{safe}.json"
