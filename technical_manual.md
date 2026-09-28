# Fishodoro Technical Manual 🛠️

This guide is for developers who want to run Fishodoro from source, change the code, and build a new Windows release.

For end-user instructions, see [user_manual.md](user_manual.md).

---

## 1. Requirements

| Tool | Version | Notes |
|---|---|---|
| Windows | 10 / 11 | Builds are Windows-only. PyInstaller builds for the OS it runs on |
| Python | 3.12 (tested with 3.12.10) | Tick **"Add Python to PATH"** when installing |
| Git | Any recent version | To clone the repo |
| PySide6 | 6.11.1 | Installed from `requirements.txt` |
| PyInstaller | 6.x (tested with 6.22.3) | Build only |
| Pillow | Any recent version | Build only. Lets PyInstaller convert the PNG icon to `.ico` |

---

## 2. Set Up the Project

All commands are for **PowerShell**.

```powershell
git clone https://github.com/joeylim0328/Fishodoro.git
cd Fishodoro
```

### (Recommended) Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activate script, run this once:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

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

## 4. Project Structure

```
Fishodoro/
├── main.py                      # Entry point: logging setup, taskbar app ID, starts QApplication
├── Fishodoro.spec               # PyInstaller build recipe (commit this)
├── requirements.txt             # Runtime dependencies (PySide6)
├── assets/
│   └── icons8-fish-96.png       # App / window / tray icon
├── src/
│   ├── core_logic.py            # Fih lists + random fih / rarity logic
│   ├── database.py              # FihDatabase: reads/writes database.json
│   └── ui/
│       ├── main_window.py       # Main window, tabs, tray icon, notifications
│       └── widgets/
│           ├── timer_widget.py  # Fishing Deck: timer, buttons, catch flow
│           ├── pond_widget.py   # My Pond: animated swimming fih
│           └── stats_widget.py  # Stats: monthly heatmap + recent logbook
├── README.md
├── DESIGN.md                    # Original design document
├── user_manual.md
└── technical_manual.md
```

---

## 5. Where Data Is Stored

Both files are resolved relative to the code's own location (`__file__`), not the current working directory.

| File | Created by | From source | In a PyInstaller build |
|---|---|---|---|
| `database.json` | `src/database.py` | `<project root>\database.json` | `dist\Fishodoro\_internal\database.json` |
| `fishodoro.log` | `main.py` | `<project root>\fishodoro.log` | `dist\Fishodoro\_internal\fishodoro.log` |

**Things to keep in mind:**
- **Source and build use separate databases.** Catches made with `python main.py` do not appear in the `.exe`, and catches made in the `.exe` do not appear when running from source.
- **Rebuilding wipes the build's data.** PyInstaller deletes `dist\Fishodoro\` on every build, including `database.json` (see Section 7).
- **Do not use `--onefile`.** A one-file build unpacks to a temporary folder (`%TEMP%\_MEIxxxxx`) that is deleted on exit, so all data would be lost every time the app closes.
- **Do not install to `C:\Program Files`.** Normal users can't write there, so saving fails.

### `database.json` format

A JSON list of catch records, appended one per catch:

```json
[
    {
        "emoji": "🦐",
        "name": "Grandpa Shrimp",
        "is_special": false,
        "focus_start": "2026-09-28T14:20:01.964806",
        "focus_end": "2026-09-28T14:35:06.318623",
        "focus_end_btn_pressed": "2026-09-28T14:35:07.298002"
    }
]
```

- `focus_end_btn_pressed` is the timestamp the Pond and Stats tabs use to decide which day and month a fih belongs to.
- Some older records may be missing fields (e.g. they have `timestamp` instead). Code reading records should use `.get()` defaults.
- If the file is missing or corrupted, `load_data()` returns an empty list. **The next catch then overwrites the file**, so back it up before editing it by hand.

---

## 6. Common Code Changes

| I want to... | Edit |
|---|---|
| Add or rename fih | `COMMON_FIH` / `SPECIAL_FIH` in `src/core_logic.py` |
| Change special fih odds | `generate_random_fih()` in `src/core_logic.py`. Currently every 4th catch has a 15% chance (`random.random() < 0.15`) |
| Change focus / break options or defaults | `focus_combo` / `break_combo` in `src/ui/widgets/timer_widget.py` (`addItems` / `setCurrentIndex`) |
| Change button colours | `BTN_STYLE_NORMAL`, `BTN_STYLE_RED`, `BTN_STYLE_GREEN` at the top of `timer_widget.py` |
| Change button behaviour per state | `start_timer()`, `on_timer_complete()`, `claim_fih_and_start_break()`, `reset_timer()` in `timer_widget.py` |
| Change how many logbook entries are shown | `month_history[-5:]` in `refresh_stats()`, `src/ui/widgets/stats_widget.py` |
| Change the app icon | Replace the PNG in `assets/` and update `ICON_PATH` in `src/ui/main_window.py` plus `--icon` / `icon=` in the build |

### Adding new asset files

Everything in `assets/` is bundled by the `datas=[('assets', 'assets')]` line in `Fishodoro.spec`. Load assets relative to the code (like `ICON_PATH` in `main_window.py`), never relative to the current working directory.

After any change, test with `python main.py` before building.

---

## 7. Build a Windows Release

### 7.1 Install build tools (once)

```powershell
python -m pip install pyinstaller pillow
```

### 7.2 Back up the build's `database.json`

Skip this if you have never run the built `.exe` or don't care about its test data.

```powershell
Copy-Item dist\Fishodoro\_internal\database.json database_backup.json
```

### 7.3 Build

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

### 7.4 Restore the backup

```powershell
Copy-Item database_backup.json dist\Fishodoro\_internal\database.json
```

### 7.5 Test the build

```powershell
.\dist\Fishodoro\Fishodoro.exe
```

Check that:
- the app opens with the fish icon on the window, taskbar and tray
- a focus session can be completed (use the shortest focus time) and the fih appears in Pond and Stats
- `dist\Fishodoro\_internal\database.json` is updated

**Debugging a build that crashes on launch:** a `--windowed` build hides errors. Temporarily set `console=True` in `Fishodoro.spec`, rebuild, and run the `.exe` from PowerShell to see the traceback. Set it back to `False` afterwards.

---

## 8. Publish a Release

1. **Remove personal data before packaging.** Delete `dist\Fishodoro\_internal\database.json` and `fishodoro.log`, so users start with an empty pond and don't receive your catches.
2. Right-click `dist\Fishodoro` → **Compress to ZIP file** → name it `Fishodoro.zip`.
3. On GitHub, go to **Releases** → **Draft a new release**:
   - Tag: e.g. `v1.0.0`
   - Attach `Fishodoro.zip`
   - Link to `user_manual.md` in the release notes
4. Publish.

---

## 9. Backing Up `database.json`

| Where you run the app | File to back up |
|---|---|
| From source (`python main.py`) | `<project root>\database.json` |
| Built app (`Fishodoro.exe`) | `dist\Fishodoro\_internal\database.json`, or `<install folder>\_internal\database.json` on a user's PC |

### Manual backup (PowerShell)

Close the app first, then:

```powershell
# From source
Copy-Item database.json "database_backup_$(Get-Date -Format yyyy-MM-dd).json"

# Built app
Copy-Item dist\Fishodoro\_internal\database.json "database_backup_$(Get-Date -Format yyyy-MM-dd).json"
```

### Restore

Close the app, then copy the backup over the live file:

```powershell
Copy-Item database_backup_2026-09-28.json dist\Fishodoro\_internal\database.json
```

### Moving data between source and build

`database.json` is plain JSON with the same format in both, so you can copy it between the project root and `_internal\` freely (with the app closed).

### Keep backups out of Git

`database.json` and `fishodoro.log` are already in `.gitignore`. Backup files are not. Add this line to `.gitignore` so personal data never gets committed:

```
database_backup*.json
```

---

## 10. Git Notes

`.gitignore` currently covers `database.json`, `fishodoro.log`, `build/` and `dist/`.

**Commit:**
- `Fishodoro.spec` (the build recipe)
- the `assets/` folder

**Clean-up recommended:** `__pycache__/` folders are currently tracked. To stop tracking them (the files stay on disk):

```powershell
git rm -r --cached src/__pycache__ src/ui/__pycache__ src/ui/widgets/__pycache__
```

Then add `__pycache__/` to `.gitignore`.

---

## 11. Troubleshooting

| Problem | Fix |
|---|---|
| `pyinstaller is not recognized` | Use `python -m PyInstaller` (capital P and I) |
| Built app has no fish icon on window / taskbar / tray | `datas=[('assets', 'assets')]` is missing from `Fishodoro.spec`. Add it back and rebuild from the spec |
| `.exe` icon wrong in File Explorer | Windows icon cache. Run `ie4uinit.exe -show`, or move the folder |
| `ModuleNotFoundError` in the built app | Add the module to `hiddenimports=[...]` in `Fishodoro.spec` |
| Antivirus flags the `.exe` | Known PyInstaller false positive. Exclude `dist\` while developing |
| Catches missing after rebuild | Rebuilding deletes `dist\Fishodoro\`. Restore from backup (Section 9) |
| Catches from source missing in `.exe` (or vice versa) | They use separate `database.json` files (Section 5). Copy the file across |
| `QFont::setPointSize: Point size <= 0` in logs | Harmless Qt warning |

---

## Credits

App icon: [Fish](https://icons8.com/icon/OClCFhCarb8m/fish) icon by [Icons8](https://icons8.com)
