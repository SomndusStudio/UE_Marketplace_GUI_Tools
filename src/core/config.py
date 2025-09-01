# config.py
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "configs" / "app_config.json"

DEFAULT_APP_CONFIG = {
    "seven_zip_path": "7z"   # default: rely on PATH
}

def load_app_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            logger.info("Load app config file %s", CONFIG_FILE)
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error("Failed to read app config %s: %s", CONFIG_FILE, e)

    # if missing or invalid, create with defaults
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(DEFAULT_APP_CONFIG, indent=2), encoding="utf-8")
    logger.info("Created default app config at %s", CONFIG_FILE)
    return dict(DEFAULT_APP_CONFIG)


def get_seven_zip_path() -> Path:
    cfg = load_app_config()
    return Path(cfg.get("seven_zip_path", "7z"))
