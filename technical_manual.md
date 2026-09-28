# Fishodoro Technical Manual 🛠️

This guide is for developers who want to run Fishodoro from source, change the code, and build a new Windows release.

For end-user instructions, see [user_manual.md](user_manual.md).

---

## 1. Set Up the Project


```powershell
git clone https://github.com/joeylim0328/Fishodoro.git
cd Fishodoro
```

### (Recommended) Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 3. Run From Source

```powershell
python main.py
```

Logs print to the terminal and are also written to `fishodoro.log`.


---

## 4. Build a Windows Release

### 4.1 Install build tools (once)

```powershell
python -m pip install pyinstaller pillow
```

### 4.2 Back up the build's `database.json`

Skip this if you have never run the built `.exe` or don't care about its test data.

```powershell
Copy-Item dist\Fishodoro\_internal\database.json database_backup.json
```

### 4.3 Build

**Always build from the spec file:**

```powershell
python -m PyInstaller --noconfirm Fishodoro.spec
```

The spec already contains the right settings:
- `console=False`: no console window
- `icon=['assets/icons8-fish-96.png']`: the `.exe` icon
- `datas=[('assets', 'assets')]`: bundles the icon so the window, taskbar and tray icons work

> ⚠️ **Do not rebuild with a plain `python -m PyInstaller ... main.py` command.** It **overwrites `Fishodoro.spec`**, and any option you leave out (for example the assets `datas` line) is lost, so the icon disappears from the window, taskbar and tray. If you must regenerate the spec, use the full command:
> ```powershell
> python -m PyInstaller --name Fishodoro --windowed --icon assets\icons8-fish-96.png --add-data "assets;assets" --noconfirm main.py
> ```

Output:

```
dist\Fishodoro\
├── Fishodoro.exe
└── _internal\
    └── assets\icons8-fish-96.png
```

### 4.4 Restore the backup

```powershell
Copy-Item database_backup.json dist\Fishodoro\_internal\database.json
```

### 4.5 Test the build

```powershell
.\dist\Fishodoro\Fishodoro.exe
```
