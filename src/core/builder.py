# builder.py
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from typing import Iterable, Optional, Sequence, Tuple


# --------------------------- Data models --------------------------- #

@dataclass
class BuildSelection:
    """A single UE target to build."""
    version_id: str  # e.g. "ue54"
    version_label: str  # e.g. "UE 5.4" (used for {ueversion} name formatting)
    engine_path: str  # path to Unreal Engine root for this version (not strictly needed here)


# --------------------------- Helpers ------------------------------- #

DEFAULT_EXCLUDES: tuple[str, ...] = (
    "Binaries", "Build", "Intermediate", "Saved", "DerivedDataCache",
    ".git", ".gitattributes", ".gitignore", ".github", ".gitlab", ".vs", ".idea", "__pycache__",
)


def _is_7z_available(explicit_path: Optional[Path]) -> Optional[Path]:
    """Return a 7-Zip executable path if available."""
    if explicit_path and explicit_path.exists():
        return explicit_path
    which = shutil.which("7z") or shutil.which("7z.exe")
    return Path(which) if which else None


def _find_uproject(root: Path) -> Path:
    """Find the first .uproject file in the project root."""
    for p in root.glob("*.uproject"):
        if p.is_file():
            return p
    raise FileNotFoundError("No .uproject found in project root.")


def _load_uproject(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump_uproject(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _sanitize_version_label_to_token(label: str) -> str:
    """Turn 'UE 5.4' into '5_4' (remove 'UE' and replace '.' with '_')."""
    return label.replace("UE", "").strip().replace(".", "_")


def _format_zip_basename(pattern: str, template_dir: Path, version_label: str) -> str:
    """Format the base name (without extension) from the naming pattern."""
    project = template_dir.name or "Project"
    ueversion = _sanitize_version_label_to_token(version_label)
    try:
        base = pattern.format(project=project, ueversion=ueversion)
    except Exception:
        base = f"{project}_{ueversion}"
    return base


def _iter_project_files(src_root: Path, excludes: Iterable[str]) -> Iterable[Path]:
    """Yield files under src_root excluding top-level folders in `excludes`."""
    exclude_set = set(excludes)
    for child in src_root.iterdir():
        if child.name in exclude_set:
            continue
        # Always skip hidden VCS metadata at root if not already excluded
        if child.name.startswith(".") and child.name not in (".config",):
            if child.name not in exclude_set:
                continue
        if child.is_dir():
            for p in child.rglob("*"):
                if p.is_file():
                    yield p
        elif child.is_file():
            yield child


def _relative_to_root(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


# --------------------------- Base ZIP creation ---------------------- #

def create_base_zip(
        project_root: Path,
        out_dir: Path,
        base_name: str,
        seven_zip: Optional[Path],
        excludes: Sequence[str] = DEFAULT_EXCLUDES,
) -> Path:
    """
    Create a base ZIP of the project root excluding heavy/dev folders.
    Returns the path to the created base ZIP (without engine association tweaks).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    base_zip = out_dir / f"{base_name}_BASE.zip"

    seven = _is_7z_available(seven_zip)
    if seven:
        # Use 7-Zip with exclude rules (-xr!) for each top-level folder
        # We run from project_root so patterns like * match relative content.
        args = [str(seven), "a", "-tzip", "-mx=5", "-y", str(base_zip)]
        for ex in excludes:
            args += [f"-xr!{ex}"]
        # Add everything under project root
        args += ["*"]
        subprocess.run(args, cwd=str(project_root), check=True)
    else:
        # Python fallback using zipfile
        with zipfile.ZipFile(base_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in _iter_project_files(project_root, excludes):
                arc = _relative_to_root(file, project_root)
                zf.write(file, arc)
    return base_zip


# --------------------------- Uproject mutation ---------------------- #

def build_mutated_uproject_bytes(
        original_uproject_path: Path,
        engine_association: str,
        plugins_to_strip=set[str],
) -> bytes:
    """
    Return bytes of a mutated .uproject:
    - sets EngineAssociation to engine_association
    - drops "Plugins" key (or empties it) when remove_plugins is True
    """
    data = _load_uproject(original_uproject_path)
    data["EngineAssociation"] = engine_association

    if plugins_to_strip and "Plugins" in data and isinstance(data["Plugins"], list):
        filtered = []
        for entry in data["Plugins"]:
            name = str(entry.get("Name", "")).strip()
            # keep plugin if not in the removal set
            if not name or name not in plugins_to_strip:
                filtered.append(entry)
        if filtered:
            data["Plugins"] = filtered
        else:
            # remove key entirely if nothing left
            del data["Plugins"]

    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


# --------------------------- Apply version to ZIP ------------------- #

def update_zip_uproject_with_7z(
        src_zip: Path,
        dst_zip: Path,
        uproject_relpath: str,
        new_uproject_bytes: bytes,
        seven_zip: Path,
) -> None:
    """
    Copy src_zip to dst_zip and replace the .uproject entry using 7-Zip 'u' (update).
    We write the modified .uproject to a temp file and update the archive.
    """
    shutil.copy2(src_zip, dst_zip)
    with tempfile.TemporaryDirectory() as td:
        tmp_uproject = Path(td) / Path(uproject_relpath).name
        tmp_uproject.write_bytes(new_uproject_bytes)
        # Update the entry at path uproject_relpath; 7z requires a relative path, so we pass the file
        # and use -up0q3r2x2y2z0!pattern to control; simpler approach: run from temp and target rel path
        # Easiest: use 7z u dst_zip tmp_uproject -spf2 and specify archive path with -ir!<arcpath>
        # But -ir is for include; 7z can't directly map a different file path to arc path without -si/-so.
        # So we do: 7z u dst_zip <tmp_path> -snl -spf2, then rename entry if necessary.
        # Simpler robust route: extract the original .uproject to temp path with the same name, then update it.
        # However, most 7z builds will update by filename only (no folder). We'll instead use python fallback if arc path differs.
        # For reliable behavior, we fallback to Python replace when arc path != file name:
        if Path(uproject_relpath).name != uproject_relpath:
            # Fallback to Python replace to preserve exact arc path
            update_zip_uproject_python(src_zip, dst_zip, uproject_relpath, new_uproject_bytes)
            return
        # If the .uproject sits at archive root, we can update by filename:
        subprocess.run([str(seven_zip), "u", "-y", str(dst_zip), str(tmp_uproject)], check=True)


def update_zip_uproject_python(
        src_zip: Path,
        dst_zip: Path,
        uproject_relpath: str,
        new_uproject_bytes: bytes,
) -> None:
    """
    Copy src_zip to dst_zip while replacing the .uproject entry using Python's zipfile.
    """
    # Write to a temp then move to dst_zip to avoid partial files on error
    with tempfile.TemporaryDirectory() as td:
        tmp_zip = Path(td) / "new.zip"
        with zipfile.ZipFile(src_zip, "r") as zin, zipfile.ZipFile(tmp_zip, "w",
                                                                   compression=zipfile.ZIP_DEFLATED) as zout:
            # Copy all entries except the .uproject we are replacing
            for item in zin.infolist():
                arcname = item.filename
                if arcname.replace("\\", "/") == uproject_relpath.replace("\\", "/"):
                    continue
                # Preserve original compression/mtime when possible
                data = zin.read(item.filename)
                zout.writestr(item, data)
            # Add the new .uproject
            zout.writestr(uproject_relpath, new_uproject_bytes)
        shutil.copy2(tmp_zip, dst_zip)


# --------------------------- Orchestrator --------------------------- #
def check_cancel(on_check_cancel: Optional[Callable[[], bool]], on_log: Optional[Callable[[str], None]] = None):
    """Raise RuntimeError('Canceled') if cancel was requested."""
    if on_check_cancel and on_check_cancel():
        if on_log:
            on_log("Canceled.")
        raise RuntimeError("Canceled")


def build_zip_set(
        project_root: Path,
        out_dir: Path,
        pattern: str,
        selections: Sequence[Tuple[str, str, str]],
        # selections: list of (version_id, version_label, engine_path)
        seven_zip: Optional[Path] = None,
        remove_plugins: bool = True,
        excludes: set[str] | None = None,  # default None,
        plugins_to_strip=set[str],
        on_log: Optional[Callable[[str], None]] = None,
        on_progress: Optional[Callable[[int], None]] = None,
        on_check_cancel: Optional[Callable[[], bool]] = None,
) -> list[Path]:
    """
    End-to-end build:
      1) Create a base ZIP once from project_root (excluding heavy/dev folders).
      2) For each selected version, produce a final ZIP by replacing the .uproject inside with a mutated one.

    Returns list of final zip paths.
    """
    # Start Progress 0%
    on_log("Starting build...")
    on_progress(0)

    project_root = project_root.resolve()
    out_dir = out_dir.resolve()
    uproject_path = _find_uproject(project_root)
    uproject_relpath = _relative_to_root(uproject_path, project_root)

    check_cancel(on_check_cancel, on_log)

    on_log("Creating base zip (excluding heavy/dev folders)...")

    if excludes is None:
        # caller did not override, use defaults only
        excludes = DEFAULT_EXCLUDES
    else:
        # caller provided something → merge with defaults
        excludes = tuple(set(DEFAULT_EXCLUDES) | set(excludes))

    # Create base archive once
    base_zip = create_base_zip(project_root, out_dir, base_name="__UE_BASE__", seven_zip=seven_zip, excludes=excludes)

    check_cancel(on_check_cancel, on_log)

    seven = _is_7z_available(seven_zip)
    results: list[Path] = []

    # For progression
    total = len(selections)

    for idx, (version_id, version_label, _engine_path) in enumerate(selections, 1):

        check_cancel(on_check_cancel, on_log)
        on_log(f"[{version_label}] Mutating .uproject (EngineAssociation)...")

        # Prepare mutated .uproject bytes
        engine_association = version_label.replace("UE", "").strip()  # store as "5.4" etc. (leave dot here)

        mutated = build_mutated_uproject_bytes(
            original_uproject_path=uproject_path,
            engine_association=engine_association,
            plugins_to_strip=plugins_to_strip
        )
        # Compute final name from pattern (with dots -> underscores already handled)
        final_base = _format_zip_basename(pattern, project_root, version_label)
        dst_zip = out_dir / f"{final_base}.zip"

        check_cancel(on_check_cancel, on_log)
        on_log(f"[{version_label}] Writing final zip: {dst_zip.name}")

        if seven:
            # Use 7-Zip update when the .uproject sits at archive root; otherwise fallback to Python replace
            try:
                update_zip_uproject_with_7z(base_zip, dst_zip, uproject_relpath, mutated, seven)
            except Exception:
                update_zip_uproject_python(base_zip, dst_zip, uproject_relpath, mutated)
        else:
            update_zip_uproject_python(base_zip, dst_zip, uproject_relpath, mutated)

        percent = int(idx / total * 100)
        on_progress(percent)

        results.append(dst_zip)

    # Optionally remove the base zip to keep output clean
    try:
        base_zip.unlink(missing_ok=True)
    except Exception:
        pass

    on_log("All done.")
    on_progress(100)

    return results
