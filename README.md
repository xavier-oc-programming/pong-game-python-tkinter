# Pong — Python / Turtle

A two-player Pong implementation built in Python using the `turtle` module.
Day 22 of my 100 Days of Code journey.

---

## Quick start

```bash
python menu.py
```

The menu lets you choose between two builds:

| Option | Description |
|--------|-------------|
| `1` | **Original** — close to the course state, procedural style |
| `2` | **Advanced** — full OOP rebuild with pause, manual-serve mode, and persistent HUD |

---

## Controls

### During gameplay

| Action | Left Player | Right Player |
|--------|-------------|--------------|
| Move up | `W` | `↑` |
| Move down | `S` | `↓` |
| Pause | `Space` | `Space` |

### Pause menu

| Key | Action |
|-----|--------|
| `Space` | Resume |
| `R` | Return to menu |

### Game over

| Key | Action |
|-----|--------|
| `Space` | Play again |
| `Q` | Return to menu |

### Manual-serve mode (if selected at start)

| Key | Action |
|-----|--------|
| `Space` | Serve next ball |
| `R` | Return to menu |

---

## Features

- Smooth key-hold movement (press/release tracking)
- Ball accelerates on every paddle hit
- First player to reach **10 points** wins
- **Advanced only:** always-visible score strip above the court with top and bottom boundary lines
- **Advanced only:** pause at any time with `Space` — resume or return to menu
- **Advanced only:** choose serve mode at the welcome screen — auto-start or manual `Space` to serve
- **Advanced only:** animated welcome screen with line-by-line reveal
- **Advanced only:** game-over overlay on frozen game state

---

## Architecture

```
pong-game-python-tkinter/
├── menu.py              # Version selector — launches original/ or advanced/
├── art.py               # ASCII LOGO constant
├── requirements.txt     # Standard library only
├── docs/
│   └── COURSE_NOTES.md  # Original course exercise description
├── original/            # Course build — procedural, minimal changes
│   ├── main.py
│   ├── ball_file.py
│   ├── paddles.py
│   └── scoreboard_file.py
└── advanced/            # OOP rebuild — modular, no magic numbers
    ├── main.py          # Orchestrator: input → logic → display
    ├── config.py        # All constants
    ├── ball.py          # Pure ball logic (no UI)
    ├── paddle.py        # Pure paddle logic (no UI)
    ├── scores.py        # Left/right score tracking
    ├── display.py       # All turtle rendering
    └── data.txt         # Persisted data file
```

### Module responsibilities (advanced)

| File | Responsibility |
|------|----------------|
| `config.py` | Every constant — zero magic numbers elsewhere |
| `ball.py` | Position, velocity, collision predicates — no turtle imports |
| `paddle.py` | Position, movement, boundary clamping — no turtle imports |
| `scores.py` | Left/right counters, game-over check, reset |
| `display.py` | Screen setup, court boundaries, score HUD, all overlays (welcome, pause, game-over, serve prompt) |
| `main.py` | Wires everything: reads keys → updates logic → drives display |

### Display layout (advanced)

```
┌─────────────────────────────────┐  ← top of window
│           3       7             │  score strip (always visible)
├─────────────────────────────────┤  ← SCORE_DIVIDER_Y  (top court boundary)
│                                 │
│   [A]      ·      ·      [B]    │  court — paddles, ball, centre line
│                                 │
├─────────────────────────────────┤  ← -SCORE_DIVIDER_Y (bottom court boundary)
└─────────────────────────────────┘  ← bottom of window
```

---

## Dependencies

Standard library only — no `pip install` required.  
Python 3.10+ recommended. `turtle` and `tkinter` ship with CPython.
