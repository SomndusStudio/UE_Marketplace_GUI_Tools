# ---------- Paths helpers ----------
from pathlib import Path


def get_project_root() -> Path:
    """Return project root (parent of src/)."""
    return Path(__file__).resolve().parents[1]

def get_configs_dir() -> Path:
    """Return <project_root>/configs."""
    p = get_project_root() / "configs"
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_catalog_path() -> Path:
    """Return <project_root>/configs/versions_catalog.json."""
    return get_configs_dir() / "ue_versions.json"

def get_profiles_dir() -> Path:
    """Return <project_root>/configs/profiles."""
    p = get_configs_dir() / "profiles"
    p.mkdir(parents=True, exist_ok=True)
    return p

def profile_path(name: str) -> Path:
    """Return path for a given profile JSON file."""
    safe = name.strip().replace("/", "_").replace("\\", "_")
    return get_profiles_dir() / f"{safe}.json"