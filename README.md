## Command Memo

### Compile UI File
```bash
pyside6-uic src/ui/project_fab_windows.ui -o src/windows/ui_project_fab_windows.py
```

### Translate one file
```bash
pyside6-lupdate . -recursive -source-language en -ts i18n/app_fr.ts
```