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
| `2` | **Advanced** — full OOP rebuild, persistent high score |

---

## Controls

| Action | Left Player | Right Player |
|--------|-------------|--------------|
| Move up | `W` | `↑` |
| Move down | `S` | `↓` |
| Start / retry | `Space` | — |
| Quit game over | — | `Q` |

---

## Features

- Smooth key-hold movement (press/release tracking)
- Ball accelerates on every paddle hit
- First player to reach **10 points** wins
- **Advanced only:** persistent high score saved to `advanced/data.txt`
- **Advanced only:** animated welcome screen, game-over overlay

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
    ├── scores.py        # Score tracking + file I/O
    ├── display.py       # All turtle rendering
    └── data.txt         # Persisted high score
```

### Module responsibilities (advanced)

| File | Responsibility |
|------|----------------|
| `config.py` | Every constant — zero magic numbers elsewhere |
| `ball.py` | Position, velocity, collision predicates — no imports from turtle |
| `paddle.py` | Position, movement, boundary clamping — no imports from turtle |
| `scores.py` | Left/right counters, high-score persistence via `data.txt` |
| `display.py` | Screen setup, turtle objects, all rendering, welcome + game-over overlays |
| `main.py` | Wires everything: reads keys → updates logic → drives display |

---

## Dependencies

Standard library only — no `pip install` required.  
Python 3.10+ recommended. `turtle` and `tkinter` ship with CPython.
