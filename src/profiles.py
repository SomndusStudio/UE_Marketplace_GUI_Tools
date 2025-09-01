# profiles.py
from __future__ import annotations

import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json

from src.path_helpers import get_catalog_path, get_profiles_dir, profile_path


# ---------- Data models ----------

@dataclass(frozen=True)
class AppVersion:
    """App-level version descriptor with a stable ID, display label, and default engine path."""
    id: str              # e.g., "ue54"
    label: str           # e.g., "UE 5.4"
    engine_path: str     # default engine path from catalog

@dataclass
class ProfileVersionRef:
    """Profile mapping to an app version ID with optional engine path override and checked state."""
    version_id: str
    engine_path: str = ""   # if empty, UI should fallback to catalog's engine_path
    checked: bool = True

@dataclass
class Profile:
    """Profile payload saved to disk (JSON)."""
    name: str
    template_dir: str
    output_dir: str
    zip_pattern: str
    versions: List[ProfileVersionRef]
    plugins_to_strip: List[str] = None

# ---------- Catalog API ----------

def load_versions_catalog() -> List[AppVersion]:
    """Load the app versions catalog (id + label + engine_path)."""
    p = get_catalog_path()
    if not p.exists():
        raise FileNotFoundError(f"Catalog not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    out: List[AppVersion] = []
    for it in data.get("versions", []):
        vid = str(it.get("id", "")).strip()
        label = str(it.get("label", "")).strip()
        ep = str(it.get("engine_path", "")).strip()
        if vid and label:
            out.append(AppVersion(id=vid, label=label, engine_path=ep))
    # Ensure unique IDs
    seen = set()
    for v in out:
        if v.id in seen:
            raise ValueError(f"Duplicate version id in catalog: {v.id}")
        seen.add(v.id)
    return out

def catalog_by_id(catalog: List[AppVersion]) -> Dict[str, AppVersion]:
    """Map version_id -> AppVersion for quick lookups."""
    return {v.id: v for v in catalog}

# ---------- Profiles API ----------

def list_profile_names() -> List[str]:
    """List available profile names (without .json)."""
    return sorted([p.stem for p in get_profiles_dir().glob("*.json")])

def default_profile() -> Profile:
    """Return in-memory default profile."""
    return Profile(
        name="Default",
        template_dir="",
        output_dir="",
        zip_pattern="{project}_{ueversion}",
        versions=[],  # empty until user adds/migrates
    )

def ensure_default_profile_exists() -> Path:
    """Create Default.json if missing and return its path."""
    p = profile_path("Default")
    if not p.exists():
        p.write_text(json.dumps(asdict(default_profile()), indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def load_profile(name: str) -> Profile:
    """Load a profile by name (fallback to Default)."""
    p = profile_path(name)
    if not p.exists():
        p = ensure_default_profile_exists()
    data = json.loads(p.read_text(encoding="utf-8"))
    refs: List[ProfileVersionRef] = []
    for it in data.get("versions", []):
        vid = str(it.get("version_id", "")).strip()
        ep = str(it.get("engine_path", "")).strip()  # may be empty -> fallback to catalog at runtime
        chk = bool(it.get("checked", True))
        if vid:
            refs.append(ProfileVersionRef(version_id=vid, engine_path=ep, checked=chk))
    return Profile(
        name=str(data.get("name", name)),
        template_dir=str(data.get("template_dir", "")),
        output_dir=str(data.get("output_dir", "")),
        zip_pattern=str(data.get("zip_pattern", "{project}_{ueversion}")),
        versions=refs,
        plugins_to_strip=list(data.get("plugins_to_strip", []) or []),
    )

def save_profile(profile: Profile) -> Path:
    """Save a profile to <profiles>/<name>.json and return its path."""
    p = profile_path(profile.name)
    p.write_text(json.dumps(asdict(profile), indent=2, ensure_ascii=False), encoding="utf-8")
    return p

# ---------- Join / merge helpers ----------

def resolve_profile_versions_for_ui(
    profile: Profile,
    catalog: List[AppVersion],
) -> List[Tuple[AppVersion, ProfileVersionRef]]:
    """
    Join profile refs with catalog to get display info.
    For each catalog version, return (AppVersion, ProfileVersionRef or a synthetic default ref).
    """
    by_id = catalog_by_id(catalog)
    pref_by_id: Dict[str, ProfileVersionRef] = {ref.version_id: ref for ref in profile.versions}
    out: List[Tuple[AppVersion, ProfileVersionRef]] = []

    for appv in catalog:
        ref = pref_by_id.get(appv.id)
        if ref is None:
            # synthetic un-checked ref; engine_path empty -> UI falls back to catalog engine_path
            ref = ProfileVersionRef(version_id=appv.id, engine_path="", checked=False)
        out.append((appv, ref))
    return out

def upsert_profile_version(
    profile: Profile,
    version_id: str,
    engine_path: str,
    checked: bool = True,
) -> None:
    """Add or update a version ref in the profile by version_id."""
    for ref in profile.versions:
        if ref.version_id == version_id:
            ref.engine_path = engine_path
            ref.checked = checked
            return
    profile.versions.append(ProfileVersionRef(version_id=version_id, engine_path=engine_path, checked=checked))

def rename_profile(old_name: str, new_name: str) -> Path:
    """Rename a profile JSON file and return the new path.
    Handles case-only renames on case-insensitive filesystems by using a temp hop.
    """
    old_p = profile_path(old_name)
    new_p = profile_path(new_name)
    if not old_p.exists():
        raise FileNotFoundError(f"Profile not found: {old_name}")

    # If paths are identical (same file) and only case differs on a case-insensitive FS,
    # do a two-step rename via a unique temp file.
    same_ignoring_case = old_p.name.lower() == new_p.name.lower() and old_p.parent == new_p.parent

    if new_p.exists() and not same_ignoring_case:
        raise FileExistsError(f"Profile '{new_name}' already exists.")

    if same_ignoring_case and old_p != new_p:
        # temp hop: <name>.tmp-<uuid>.json
        tmp_p = old_p.with_name(f"{old_p.stem}.tmp-{uuid.uuid4().hex}{old_p.suffix}")
        old_p.rename(tmp_p)   # step 1
        tmp_p.rename(new_p)   # step 2
    else:
        old_p.rename(new_p)

    return new_p