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
| `2` | **Advanced** — full OOP rebuild with persistent HUD, pause, and serve mode |

---

## Controls

### Title screen

| Key | Action |
|-----|--------|
| `A` | Start — auto-serve (next round begins automatically) |
| `M` | Start — manual serve (`Space` to launch each ball) |
| `Q` | Quit |

### During gameplay

| Action | Left Player | Right Player |
|--------|-------------|--------------|
| Move up | `W` | `↑` |
| Move down | `S` | `↓` |
| Pause | `Space` | `Space` |

### Pause overlay

| Key | Action |
|-----|--------|
| `Space` | Resume |
| `R` | Return to title screen |

### Game over overlay

| Key | Action |
|-----|--------|
| `Space` | Play again |
| `R` | Return to title screen |

### Manual-serve prompt

| Key | Action |
|-----|--------|
| `Space` | Serve |
| `R` | Return to title screen |

---

## Features

- Smooth key-hold movement (press/release tracking)
- Ball accelerates on every paddle hit
- First player to reach **10 points** wins
- **Advanced only:** always-visible score strip above the court with top and bottom boundary lines
- **Advanced only:** pause at any time with `Space` — resume or return to title screen
- **Advanced only:** choose serve mode at the title screen — auto or manual `Space` to serve
- **Advanced only:** `R` on any in-game screen returns to the title screen without closing the window
- **Advanced only:** animated title screen with line-by-line reveal
- **Advanced only:** game-over overlay on frozen game state

---

## Navigation flow (advanced)

```
menu.py (terminal)
    └── advanced/main.py
            │
            ▼
      Title screen ◄──────────────────────────────┐
      [ A / M ] start                              │ R (from anywhere)
      [ Q ] quit ──► sys.exit                      │
            │                                      │
            ▼                                      │
       Game loop ──► Pause overlay ────────────────┤
            │        [ Space ] resume              │
            │                                      │
            ├──► Manual serve prompt ──────────────┤
            │        [ Space ] serve               │
            │                                      │
            └──► Game over overlay ────────────────┘
                     [ Space ] play again
```

---

## Architecture

```
pong-game-python-tkinter/
├── menu.py              # Terminal version selector
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
    ├── main.py          # Outer loop (title→game→title) + game loop
    ├── config.py        # All constants
    ├── ball.py          # Pure ball logic (no UI)
    ├── paddle.py        # Pure paddle logic (no UI)
    ├── scores.py        # Left/right score tracking, game-over check
    ├── display.py       # All turtle rendering and overlays
    └── data.txt         # Persisted data file
```

### Module responsibilities (advanced)

| File | Responsibility |
|------|----------------|
| `config.py` | Every constant — zero magic numbers elsewhere |
| `ball.py` | Position, velocity, collision predicates — no turtle imports |
| `paddle.py` | Position, movement, boundary clamping — no turtle imports |
| `scores.py` | Left/right counters, game-over check, reset |
| `display.py` | Screen setup, court boundaries, score HUD, all overlays |
| `main.py` | Outer title↔game loop; wires keys → logic → display |

### Display layout (advanced)

```
┌─────────────────────────────────┐  ← top of window
│           3       7             │  score strip (always visible)
├─────────────────────────────────┤  ← SCORE_DIVIDER_Y  (top court line)
│                                 │
│   [A]      ·      ·      [B]    │  court — paddles, ball, centre line
│                                 │
├─────────────────────────────────┤  ← -SCORE_DIVIDER_Y (bottom court line)
└─────────────────────────────────┘  ← bottom of window
```

---

## Dependencies

Standard library only — no `pip install` required.  
Python 3.10+ recommended. `turtle` and `tkinter` ship with CPython.
