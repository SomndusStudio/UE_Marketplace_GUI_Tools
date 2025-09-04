import os
import re
from typing import Dict, Optional
from PySide6.QtWidgets import QApplication

_VAR_DECL_RE = re.compile(r'^\s*\$([A-Za-z0-9_]+)\s*:\s*(.+?)\s*;\s*$', re.MULTILINE)

def _strip_comments(text: str) -> str:
    # removes /* ... */ and // ... end-of-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'//[^\n]*', '', text)
    return text

def _parse_vars(qsspp_text: str) -> Dict[str, str]:
    text = _strip_comments(qsspp_text)
    vars_found: Dict[str, str] = {}
    for m in _VAR_DECL_RE.finditer(text):
        name = m.group(1)
        value = m.group(2).strip()
        vars_found[name] = value
    return vars_found

def _resolve_vars(vars_map: Dict[str, str]) -> Dict[str, str]:
    # replaces $refs with their corresponding values, in multiple passes
    resolved = dict(vars_map)
    max_passes = 20
    ref_re = re.compile(r'\$([A-Za-z0-9_]+)')

    for _ in range(max_passes):
        changed = False
        for k, v in list(resolved.items()):
            def repl(m):
                ref = m.group(1)
                if ref in resolved:
                    return resolved[ref]
                # if the reference doesn't exist, leave it as is
                return m.group(0)
            new_v = ref_re.sub(repl, v)
            if new_v != v:
                resolved[k] = new_v
                changed = True
        if not changed:
            break
    return resolved

class Theme:
    """
    Loads a theme by name (e.g., 'light').

    Expected folder structure (can be changed via base_dir):
      assets/qss/
        light-theme.qsspp     # variable definitions (source)
        style-light.qss       # compiled QSS to apply to the app

    Exposes:
      .name -> theme name
      .vars -> dict of extracted and resolved variables
      .qss  -> content of the compiled QSS
    """
    def __init__(self, base_dir: str = "assets"):
        self.base_dir = base_dir
        self.name: Optional[str] = None
        self.vars: Dict[str, str] = {}
        self.qss: str = ""

    def load(self, theme_name: str):
        self.name = theme_name

        # 1) Fichier variables (qsspp)
        theme_vars_path = os.path.join(self.base_dir, "qsspp", "themes", f"{theme_name}-theme.qsspp")
        if not os.path.isfile(theme_vars_path):
            raise FileNotFoundError(f"Can't found theme: {theme_vars_path}")

        with open(theme_vars_path, "r", encoding="utf-8") as f:
            qsspp_text = f.read()

        raw_vars = _parse_vars(qsspp_text)
        self.vars = _resolve_vars(raw_vars)

        # Loading compiled wss
        compiled_qss_path = os.path.join(self.base_dir, "qss", f"style-{theme_name}.qss")
        if not os.path.isfile(compiled_qss_path):
            # fallback: default
            compiled_qss_path = os.path.join(self.base_dir, "qss", f"style-dark.qss")
        if not os.path.isfile(compiled_qss_path):
            raise FileNotFoundError(f"Compiled Stylesheet not found: {compiled_qss_path}")

        with open(compiled_qss_path, "r", encoding="utf-8") as f:
            self.qss = f.read()

        return self

    def apply(self, app: QApplication):
        if not self.qss:
            raise RuntimeError("Can't load QSS. Should call first .load(theme_name).")
        app.setStyleSheet(self.qss)

    def get(self, var_name: str, default: Optional[str] = None) -> Optional[str]:
        return self.vars.get(var_name, default)