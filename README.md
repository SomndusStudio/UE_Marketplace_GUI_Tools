# UEFabZipTools

A lightweight utility to package Unreal Engine 5 project templates into zip archives, with version switching and plugin exclusion support.

![UEFabZipTools screenshot](resources/app_gui_overview.png)

### Disclaimer !!!

This tool was originally built for my personal use.  
I’m sharing it in case others are curious or want to improve it with me.  
Please note that I provide **no guarantee of maintenance or long-term support**.

## Installation

Edit the `configs/app_config.json` file to point to your local `7z.exe` path.  
Example:

```json
{
  "seven_zip_path": "C:/Program Files/7-Zip/7z.exe"
}
```

## UE5 versions catalog

In `configs/ue_versions.json` you can edit/add the UE5 versions you want to use for multi-version packaging. Example:

⚠️ Note: `engine_path` does not need to exist (but fill them even if it's fake). It’s only there to anticipate possible future updates.  
In practice, I don’t use `Editor.exe` — only 7-Zip.

```json
{
  "versions": [
    { "id": "ue51", "label": "UE 5.1",   "engine_path": "C:/Program Files/Epic Games/UE_5.1" },
    { "id": "ue52", "label": "UE 5.2",   "engine_path": "C:/Program Files/Epic Games/UE_5.2" },
    { "id": "ue53", "label": "UE 5.3",   "engine_path": "C:/Program Files/Epic Games/UE_5.3" },
    { "id": "ue54", "label": "UE 5.4",   "engine_path": "C:/Program Files/Epic Games/UE_5.4" },
    { "id": "ue55","label": "UE 5.5",   "engine_path": "C:/Program Files/Epic Games/UE_5.5" },
    { "id": "ue56","label": "UE 5.6",   "engine_path": "D:/Programs/Epic Games/UE_5.6" }
  ]
}
```

## Command Reference

### Run the application

```bash
py -m src.main
```

Run with fault handler enabled:

```bash
py -X faulthandler -m src.main
```

### Style Preprocessor

I made a preprocessor to build my PySide6 Qt themes, similar to Sass.

You can find my tool here: [py-qss-preprocessor](https://github.com/SomndusStudio/py-qss-preprocessor)

Quick partial example in **dark-theme.qsspp** :

```css
$text_foreground_strong: #FFFFFF;
$text_foreground_disabled: #5a6270;
$form_radius: 8px;
$form_border_size: 2px;
$form_bg_color: #1b1e23;

$form_context_color: #568af2;
$selection_color: #f5f6f9;
...

@import "../base.qsspp";
@import "../style.qsspp";

// In style.qsspp
QScrollBar:horizontal {
    border: none;
    background: $scroll_bar_bg_color;
    height: 8px;
    margin: 0px 21px 0 21px;
	border-radius: 0px;
}
QScrollBar::handle:horizontal {
    background: $form_context_color;
    min-width: 25px;
	border-radius: 4px
}
```

And I compile it with my tool using:

```bash
ss-qssppc assets/qsspp/themes/dark-theme.qsspp -o assets/qss/style-dark.qss   
```

Then in my app.py

```py
from src.gui.core.json_settings import Settings

qss_path = Settings.resource_path("assets/qss/style-dark.qss")

with open(qss_path, "r", encoding="utf-8") as f:
    _style = f.read()
    app.setStyleSheet(_style)
```

### Update translations

Extract translatable strings into a `.ts` file:

```bash
pyside6-lupdate . -recursive -source-language en -ts i18n/app_fr.ts
```

## Build Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build a single-file Windows executable:

```bash
pyinstaller UEFabZipTools.spec
```

The output executable will be located in the `dist/` folder.

### Credits

This work is based on the theme from [PyOneDark_Qt_Widgets_Modern_GUI](https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI) by Wanderson-Magalhaes.  

I migrated the original implementation to a full style preprocessor (QSSPP).  
Currently, only 2–3 components still have their style defined in Python.  

Big thanks and credit to the original author for the inspiration and foundation!