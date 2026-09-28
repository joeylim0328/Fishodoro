# Fishodoro

Fishodoro is a cozy, fish-themed Pomodoro timer built with Python and PySide6. It turns focused work sessions into a gentle fishing trip: complete a focus session to "reel in" a random fish, then relax with a customizable break.

## Documentation

- 📘 [User Manual](user_manual.md): download, install, use the app, and back up your fih (no technical knowledge needed).
- 🛠️ [Technical Manual](technical_manual.md): run from source, change the code, build a Windows release, and manage `database.json`.

## Features

- **Focus Timer**: Choose a focus duration (15, 20, 25, or 30 minutes; default is 15).
- **Break Timer**: Choose a break duration from 1 to 20 minutes (default is 5).
- **Fih Catching**: Every completed focus session rewards a randomly chosen fish.
- **Special Fih Rule**: Every 4th catch has a small chance of being a rare or legendary fish.
- **My Pond**: Watch your caught fish swim in a virtual pond.
- **Stats / Fih-tribution Graph**: Track daily catches on a heatmap-style graph.
- **Local Storage**: Caught fish are saved to `database.json` with timestamps.

## Installation

1. Make sure Python is installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application with:

```bash
python main.py
```

## Controls

- **Cast Line**: Start the focus timer.
- **Pack up gear**: Stop the current session (asks for confirmation during focus).
- **Pull in Line**: Appears when a focus session finishes; claim your fish and start the break.

## Credits

- App icon: <a target="_blank" href="https://icons8.com/icon/OClCFhCarb8m/fish">Fish</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>

