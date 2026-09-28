# Fishodoro User Manual 🐟

Fishodoro is a cozy Pomodoro timer. Focus for a while, catch a fih, then take a break. Your catches swim in your pond and fill up your stats calendar.

---

## 1. What You Need

- A **Windows 10 or Windows 11** computer.
- About **200 MB** of free space.
- **Nothing else.** You do not need to install Python or any other software.

---

## 2. Download & Install

1. Go to the Fishodoro **Releases** page on GitHub:
   https://github.com/joeylim0328/Fishodoro/releases
2. Under the latest release, download **`Fishodoro.zip`**.
3. Find the file in your **Downloads** folder.
4. **Right-click** `Fishodoro.zip` → **Extract All...** → choose where to put it (e.g. **Documents** or **Desktop**) → **Extract**.
5. Open the extracted **`Fishodoro`** folder and double-click **`Fishodoro.exe`**.

### "Windows protected your PC" warning

The first time you open Fishodoro, Windows may show a blue warning. This happens because the app is not signed by a paid certificate. It is safe to continue:

1. Click **More info**.
2. Click **Run anyway**.

You only need to do this once.

### Important things to note

- **Do not run the app from inside the zip file.** Always extract it first, or your fih will not be saved.
- **Keep the whole `Fishodoro` folder together.** `Fishodoro.exe` needs the `_internal` folder next to it to work. Do not move the `.exe` out on its own.
- **Do not put the folder in `C:\Program Files`.** Windows blocks the app from saving there. Documents or Desktop works best.
- **Want a desktop shortcut?** Right-click `Fishodoro.exe` → **Show more options** → **Send to** → **Desktop (create shortcut)**.

---

## 3. How to Use Fishodoro

### 🎣 Fishing Deck (Timer)

1. Choose your **Focus Time** (15, 20, 25 or 30 minutes; default is 15).
2. Choose your **Break Time** (1 to 20 minutes; default is 5).
3. Click **Cast Line 🎣** to start focusing.
4. When the timer ends, a fih bites! Click the green **Pull in Line! 🎣💦** button to reel it in. Your break starts automatically.
5. When the break ends, you are ready to cast again.

**Buttons at a glance:**

| Button | When you can press it | What it does |
|---|---|---|
| **Cast Line 🎣** | When idle | Starts a focus session |
| **Pack up gear 🎒** | During focus (turns red) | Stops the session. It asks you to confirm first, and you will not get a fih |
| **Pull in Line! 🎣💦** | When focus is done (green) | Catches your fih and starts your break |

### Special Fih ✨

Most catches are common sea creatures. Every **4th** fih has a small chance of being a **rare, special** fih. Keep fishing and you might get lucky!

### 🌊 My Pond

See the fih you caught swimming around. Use the date controls to look at the pond for other days. Hover over a fih to see its name and when it was caught.

### 📊 Stats

- A **calendar heatmap**: darker blue means more fih caught that day. Hover over a day to see which fih you caught. Use the arrows to switch months.
- **Recent Catches Logbook**: the last 5 fih caught in the selected month.

### Notifications

Fishodoro shows a Windows notification when a fih bites and when your break is over. The fish icon in your system tray (bottom-right, near the clock) lets you reopen or exit the app.

---

## 4. Where Your Fih Are Saved

All your catches are saved in one file called **`database.json`**, inside the app folder:

```
Fishodoro\
├── Fishodoro.exe
└── _internal\
    ├── database.json    <- your caught fih
    └── fishodoro.log    <- app log (for troubleshooting)
```

> `database.json` only appears after you catch your first fih.

⚠️ **If you delete the `Fishodoro` folder, your fih are deleted too.** Back them up (see below).

---

## 5. Backing Up Your Fih 💾

Do this regularly, and **always before updating or deleting the app**.

1. Close Fishodoro.
2. Open the `Fishodoro` folder → open the **`_internal`** folder.
3. Find **`database.json`**.
4. **Copy** it (right-click → **Copy**) and **paste** it somewhere safe, such as:
   - your Documents folder
   - OneDrive / Google Drive
   - a USB drive
5. Optional: rename the copy with the date, e.g. `database_backup_2026-09-28.json`.

### Restoring a backup

1. Close Fishodoro.
2. Copy your backup file into `Fishodoro\_internal\`.
3. Rename it to exactly **`database.json`**. If Windows asks, choose **Replace**.
4. Open Fishodoro. Your fih are back! 🐟

---

## 6. Updating to a New Version

1. **Back up `database.json`** (see Section 5).
2. Download the new `Fishodoro.zip` from the Releases page and extract it.
3. Copy your backed-up `database.json` into the new `Fishodoro\_internal\` folder.
4. Delete the old `Fishodoro` folder (only after step 3!).
5. Open the new `Fishodoro.exe`.

---

## 7. Uninstalling

1. **Back up `database.json`** if you want to keep your fih.
2. Close Fishodoro.
3. Delete the `Fishodoro` folder and any shortcuts you made.

Fishodoro does not install anything else on your computer.

---

## 8. Troubleshooting

| Problem | What to try |
|---|---|
| "Windows protected your PC" | Click **More info** → **Run anyway** |
| The app does not open | Make sure you extracted the zip and that `_internal` is next to `Fishodoro.exe` |
| My fih disappeared | Did you run it from inside the zip, move the `.exe` alone, or use a new download? Restore your `database.json` backup |
| My antivirus blocks or deletes it | This is a known false alarm for apps like this. Allow Fishodoro in your antivirus settings |
| The app will not save | Move the `Fishodoro` folder out of `C:\Program Files` into Documents or Desktop |
| Emojis look different | Emojis use your Windows emoji font, so they can look slightly different on each computer |

Still stuck? Open an issue on GitHub and attach `Fishodoro\_internal\fishodoro.log`.

---

## Credits

App icon: [Fish](https://icons8.com/icon/OClCFhCarb8m/fish) icon by [Icons8](https://icons8.com)
