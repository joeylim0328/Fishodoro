# Fishodoro 🐟⏳ (Design Document)

Fishodoro is a cozy, fish-themed desktop Pomodoro application written in Python and PySide6. It replaces stressful productivity timers with a gentle fishing trip, rewarding your focus sessions with various types of adorable aquatic creatures ("fih") that swim in your virtual "Pond" and build up your personal "Fih-tribution Graph."

---

## 1. Core Mechanics: "Casting & Catching"

*   **The Timer:** A customizable focus interval that transitions automatically into a customizable break interval. In Fishodoro, focus is styled as "Casting your line" (🎣).
*   **Focus Duration Settings:** Let the user select focus time:
    *   Range: 15 to 30 minutes, in 5-minute intervals (15, 20, 25, 30).
    *   Default: 15 minutes.
*   **Break Duration Settings:** Let the user select break time:
    *   Range: 2 to 20 minutes, in 1-minute intervals (2, 3, 4, ..., 20).
    *   Default: 5 minutes.
*   **The Reward:** Completing a focus session successfully reels in one random **fih** (fish).
*   **The 4th Fih Rule:**
    *   **Fih 1, 2, 3 (Common):** Generates standard sea life (e.g., 🐟, 🐠, 🐡, 🦀).
    *   **Fih 4 (Special/Legendary):** On every 4th consecutive or total completed session, you might catch a legendary or rare aquatic creature (e.g., 🐙, 🦑, 🐬, 🐳, 🦈, or even 🧜‍♂️ / 👑), or maybe a common sea life.
*   **Logging & Timestamps:** Every caught fih is logged in a local history database with:
    *   The fih emoji (e.g., `🐠`)
    *   A funny personalized name (e.g., `"Derpy Fih"`, `"Glub Glub"`, `"Snooty Fih"`)
    *   An exact timestamp (e.g., `2026-08-03 14:32:01`)

---

## 2. The "Pond" (Your Cozy Virtual Aquarium)

The application will feature a dedicated visual tab or area called **My Pond**:
*   **The Environment:** A beautiful, dark teal/aquamarine container representing a tranquil pond, decorated with underwater bubbles (`🫧`) and plants (`🌿`).
*   **Swimming Fih:** The fih you catch are added to your active Pond. They gently drift, float, and sway back and forth using smooth Python/PySide6 QTimer animations.
*   **Interaction:** Hovering over or clicking a swimming fih reveals its tooltip showing when it was caught and its custom name.

---

## 3. The "Fih-tribution Graph" (Heatmap Tracker)

Inspired by GitHub's contribution graph, this visualizer maps your productivity history:
*   **Watery Palette:** Instead of greens, it uses a calming shade of blues/teals:
    *   ⬜ *No fih (Resting day)*
    *   淡蓝 (`#DDEEFA`) *1-2 fih*
    *   天蓝 (`#85C1E9`) *3-4 fih*
    *   湖蓝 (`#3498DB`) *5-6 fih*
    *   深海蓝 (`#1F618D`) *7+ fih*
*   **Stats Log:** Hovering over any square on the grid displays your stats: `"March 14: 4 fih caught (including 1 Legendary Kraken 🐙!)"`.
*   **The "Fihdex" (Collection Log):** A neat checklist at the bottom showing how many unique species you have discovered out of the available set.

---

## 4. Cozy UI & Audio Design

To maintain a serene, stress-free vibe:
*   **No Aggressive Countdown:** We can choose to hide the ticking seconds, showing a slowly filling fish tank progress bar or a floating bubble countdown instead.
*   **Gentle Language & Action Control:**
    *   Start/Action button: `Cast Line 🎣`
    *   Timer run state: `"Waiting patiently for a fih... 🤫"`
    *   Cancel button: `Pack up gear 🎒` (Cancel with grace, no penalties! Act as a reset/stop button)
*   **Soft Alerts:** Instead of a jarring buzzer, a gentle water splash (`💦`), a bubble pop (`🫧`), or a soft chime signals that a fih is on the line.


---

## 5. Technical Architecture (Python + PySide6)

```
                       [ Main UI Window (QMainWindow) ]
                         /            |             \
                        /             |              \
                       v              v               v
           [ Timer Panel ]      [ Pond Panel ]   [ Stats Panel ]
           (QProgressBar &      (QGraphicsView   (Grid Layout /
             LCD/Labels)        & float QTimer)    Heatmap Grid)
                  |                   |                 |
                  +-------------------+-----------------+
                                      |
                                      v
                             [ Core App Logic ]
                             - QTimer (Countdown)
                             - Local Database (JSON-based)
                             - Native Sound & Notifications
```

1.  **`main.py`:** Entrypoint file initializing `QApplication` and launching the main window.
2.  **`database.json`:** Simple local storage capturing a list of dictionaries with fih types, custom names, and timestamps.
3.  **`widgets/` (Optional modular split):**
    *   `timer_tab.py`: The focus/timer interface.
    *   `pond_tab.py`: The graphic scene displaying aquatic life swimming about.
    *   `stats_tab.py`: Custom grid drawing the heatmap.

