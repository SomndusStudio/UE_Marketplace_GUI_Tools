# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import os
from src.gui.core.json_settings import Settings

# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class Functions:

    @staticmethod
    def set_svg_icon(icon_name):
        """
        Return absolute path to an SVG icon that works in dev and in PyInstaller onefile.
        """
        # Build relative path inside the project/bundle
        rel = os.path.join("assets", "images", "svg_icons", icon_name)
        # Resolve using PyInstaller-aware helper
        icon_abs = Settings.resource_path(rel)
        return icon_abs

    @staticmethod
    def set_svg_image(icon_name):
        # Build relative path inside the project/bundle
        rel = os.path.join("assets", "images", "svg_images", icon_name)
        # Resolve using PyInstaller-aware helper
        icon_abs = Settings.resource_path(rel)
        return icon_abs

    @staticmethod
    def set_image(image_name: str) -> str:
        """
        Return absolute path to an image that works in dev and in PyInstaller onefile.
        """
        # Build relative path inside the project/bundle
        rel = os.path.join("assets", image_name)
        # Resolve using PyInstaller-aware helper
        image_abs = Settings.resource_path(rel)
        return image_abs