# config.py
import json
import logging
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_APP_CONFIG = {
    "seven_zip_path": "7z"  # default: rely on PATH
}


def _dev_configs_dir() -> Path:
    """Resolve configs/ when running from source (not frozen)."""
    cwd = Path.cwd() / "configs"
    if cwd.exists():
        return cwd
    # Fall back to repository-relative path from this file
    # (adjust the number of parents if your layout differs)
    repo_configs = Path(__file__).resolve().parents[3] / "configs"
    return repo_configs


def _runtime_configs_dir() -> Path:
    """Resolve configs/ next to the executable when frozen, else dev location."""
    if getattr(sys, "frozen", False):
        # onefile/onedir: keep configs next to the .exe so users can edit it
        return Path(sys.executable).resolve().parent / "configs"
    return _dev_configs_dir()


CONFIG_FILE = _runtime_configs_dir() / "app_config.json"


def load_app_config() -> dict:
    """Load user-editable app config from configs/app_config.json (external)."""
    try:
        logger.debug("Trying app config at %s (exists=%s)", CONFIG_FILE, CONFIG_FILE.exists())
        if CONFIG_FILE.exists():
            logger.info("Load app config file %s", CONFIG_FILE)
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("Failed to read app config %s: %s", CONFIG_FILE, e)

    # If missing or invalid, (re)create with defaults next to the EXE/dev configs dir
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(DEFAULT_APP_CONFIG, indent=2), encoding="utf-8")
    logger.info("Created default app config at %s", CONFIG_FILE)
    return dict(DEFAULT_APP_CONFIG)


def get_seven_zip_path(context) -> Path:
    """Return the 7z executable path configured by the user (or resolve via PATH)."""
    raw = context.ui.cfg.get("seven_zip_path", "7z")
    p = Path(raw)

    # If user provided a real file path, use it
    if p.exists():
        return p

    # Otherwise, try PATH (handles '7z' without absolute path)
    found = shutil.which(raw)
    if found:
        return Path(found)

    # Fall back to raw (guard clause will show the error)
    return p
