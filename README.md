# Pong — Python / Turtle

> Day 22 of 100 Days of Code — the capstone project for the Object-Oriented Programming section.

A fully playable two-player Pong game built entirely with Python's standard library `turtle` / `tkinter` module. The repo ships two builds side by side: the **original** course version preserved as-written, and a from-scratch **advanced** rebuild that applies clean architecture, a persistent HUD, a pause system, and an in-window navigation flow.

---

## Table of contents

1. [Quick start](#quick-start)
2. [Builds](#builds)
3. [Controls](#controls)
4. [Gameplay rules](#gameplay-rules)
5. [Features](#features)
6. [Navigation flow](#navigation-flow)
7. [Architecture](#architecture)
8. [Module reference — advanced](#module-reference--advanced)
9. [Configuration reference](#configuration-reference)
10. [Display layout](#display-layout)
11. [Design decisions](#design-decisions)
12. [Course context](#course-context)
13. [Dependencies](#dependencies)

---

## Quick start

```bash
# Clone
git clone https://github.com/xavier-oc-programming/pong-game-python-tkinter.git
cd pong-game-python-tkinter

# Launch
python menu.py
```

The terminal menu appears. Press `1` for the original build or `2` for the advanced build. The game opens in a tkinter window. Press `q` in the terminal menu to exit the launcher entirely.

> **Python version:** 3.10 or later required (uses `tuple[int, int]` and `X | Y` type-union syntax).  
> **No pip install needed** — `turtle` and `tkinter` ship with CPython.

---

## Builds

|                          | Original                         | Advanced                                    |
| ------------------------ | -------------------------------- | ------------------------------------------- |
| **Style**                | Procedural                       | OOP — separated by responsibility           |
| **Magic numbers**        | In-file                          | Centralised in `config.py`                  |
| **Score display**        | Inside the court (large overlay) | Persistent HUD strip above court            |
| **Court boundary**       | None visible                     | Top and bottom lines                        |
| **Pause**                | No                               | Yes — `Space` at any time                   |
| **Serve mode**           | Auto only                        | Auto or manual (`Space` to serve)           |
| **Title screen**         | No                               | Animated line-by-line reveal                |
| **Game-over screen**     | Clears court                     | Overlaid on frozen game state               |
| **In-window navigation** | No                               | `R` returns to title screen without closing |
| **Quit**                 | Close window                     | `Q` on title screen                         |
| **Type hints**           | No                               | Throughout                                  |

---

## Controls

### Title screen

| Key | Action                                                              |
| --- | ------------------------------------------------------------------- |
| `A` | Start game — **auto-serve** (next round begins after a short pause) |
| `M` | Start game — **manual serve** (`Space` launches each ball)          |
| `Q` | Quit — closes the window and returns to the terminal menu           |

### During gameplay

| Action           | Left player | Right player |
| ---------------- | ----------- | ------------ |
| Move paddle up   | `W`         | `↑`          |
| Move paddle down | `S`         | `↓`          |
| Pause            | `Space`     | `Space`      |

### Pause overlay

| Key     | Action                 |
| ------- | ---------------------- |
| `Space` | Resume game            |
| `R`     | Return to title screen |

### Game over overlay

| Key     | Action                                           |
| ------- | ------------------------------------------------ |
| `Space` | Play again — resets scores, returns to live game |
| `R`     | Return to title screen                           |

### Manual-serve prompt

Appears after each point in manual-serve mode.

| Key     | Action                    |
| ------- | ------------------------- |
| `Space` | Serve — launches the ball |
| `R`     | Return to title screen    |

---

## Gameplay rules

- The court is **800 × 600 px** with a dashed centre line and solid top/bottom boundary lines.
- Each player controls a paddle on their side of the court.
- The ball launches from the centre at the start of each round.
- The ball **bounces** off the top and bottom walls and off paddle faces.
- Every time the ball hits a paddle, it **speeds up by 5 %**, making each rally progressively harder.
- If the ball passes a paddle and exits the court, the **opposing player scores a point**.
- The first player to reach **10 points** wins. A game-over overlay appears on the frozen court.
- After game over: play again (scores reset to 0–0) or return to the title screen.

---

## Features

### Both builds

- Two-player local multiplayer
- Smooth paddle movement using `onkeypress` / `onkeyrelease` (hold the key, paddle keeps moving)
- Ball speed increases 5 % per paddle hit — rally intensity escalates naturally
- Score display updates immediately on every point

### Advanced build only

**Persistent score HUD**
The score is displayed in a dedicated strip above the court at all times — during play, during overlays, and on the title screen. It never disappears mid-game.

**Court boundaries**
Solid white lines at the top and bottom edges of the playfield make the bounce zone visually explicit. The dashed centre line is clipped to the court area and does not extend into the score strip.

**Pause system**
Press `Space` during gameplay to freeze the ball and paddles instantly. The PAUSED overlay appears on top of the frozen frame. Resume with `Space` or return to the title screen with `R`. Space is carefully handed off between the game loop and each overlay so a single key is never double-registered.

**Serve mode selection**
At the title screen, choose how each new point starts:

- **Auto** — after a 1-second pause the ball relaunches automatically.
- **Manual** — after a point the game freezes and waits for `Space` to serve. Useful if players need a moment to reposition. `R` is also available here.

**Animated title screen**
Controls and options appear line by line with a configurable delay (`WELCOME_LINE_DELAY` in `config.py`), giving the screen a typewriter feel. The title screen is shown again in the same window every time `R` is pressed — no subprocess restart required.

**Game-over overlay**
When a player wins, `GAME OVER` appears in red directly over the frozen court state. The scoreboard resets to 0–0 before the overlay so the strip shows the starting score for the next match.

**In-window navigation**
Pressing `R` from pause, game over, or the serve prompt always returns to the title screen in the same tkinter window. The window never closes mid-session. The only path to closing the window is `Q` on the title screen.

---

## Navigation flow

### Terminal menu

```
python menu.py
  │
  ├── [1] ─────────────────────────────────► original/main.py
  │                                               (window closes when done)
  │
  ├── [2] ─────────────────────────────────► advanced/main.py  (see below)
  │
  └── [q] ─────────────────────────────────► exit
```

### Advanced build — in-window flow

Each box is a screen state. Arrows show which key causes the transition.

```
                    ┌─────────────────────────────┐
                    │         TITLE SCREEN        │
                    │                             │
                    │  [A] auto-serve             │
                    │  [M] manual serve           │
                    │  [Q] quit                   │
                    └─────────────────────────────┘
                         │           │         │
                        [A]         [M]       [Q]
                         │           │         │
                         ▼           ▼         ▼
                    ┌─────────────────────┐   exit
                    │      GAME LOOP       │
                    │   (ball in play)     │
                    └─────────────────────┘
                         │           │
                  point scored    [SPACE]
                         │           │
              ┌──────────┘           ▼
              │                ┌──────────────┐
              │                │    PAUSED    │
              │                │              │
              │                │ [SPACE] ──► resume (back to game loop)
              │                │ [R]     ──► title screen
              │                └──────────────┘
              │
              ├── auto mode  ──► 1 sec pause ──► back to game loop
              │
              └── manual mode ──► ┌───────────────────┐
                                  │   SERVE PROMPT    │
                                  │                   │
                                  │ [SPACE] ──► serve (back to game loop)
                                  │ [R]     ──► title screen
                                  └───────────────────┘
              │
        (after 10 points)
              │
              ▼
         ┌─────────────────────┐
         │      GAME OVER      │
         │                     │
         │ [SPACE] ──► play again (scores reset, back to game loop)
         │ [R]     ──► title screen
         └─────────────────────┘
```

> `[R]` from any overlay always returns to the **Title screen** in the same window — the window never closes mid-session.

---

## Architecture

```
pong-game-python-tkinter/
│
├── menu.py              # Terminal launcher — version selector, while True loop
├── art.py               # LOGO constant (printed by menu.py)
├── requirements.txt     # Standard library only — nothing to install
├── .gitignore
│
├── docs/
│   └── COURSE_NOTES.md  # Original course brief and exercise description
│
├── original/            # Course build — kept as close to course state as possible
│   ├── main.py          # Screen setup, game loop, collision + game-over logic
│   ├── ball_file.py     # Ball class (Turtle subclass) — movement and speed
│   ├── paddles.py       # Paddle / LeftPaddle / RightPaddle (Turtle subclasses)
│   └── scoreboard_file.py  # Scoreboard class (Turtle subclass) — display and counters
│
└── advanced/            # Full OOP rebuild — modular, no magic numbers
    ├── main.py          # Outer title↔game loop; orchestrates logic and display
    ├── config.py        # Every constant in one place
    ├── ball.py          # Pure ball logic — no turtle, no UI, no print()
    ├── paddle.py        # Pure paddle logic — no turtle, no UI, no print()
    ├── scores.py        # ScoreTracker — counters, game-over predicate, reset
    ├── display.py       # All turtle rendering, HUD, and every overlay
    └── data.txt         # Persisted data file
```

---

## Module reference — advanced

### `config.py`

Single source of truth for every numeric and string constant. No magic numbers anywhere else in the codebase. Changing a value here propagates everywhere automatically.

### `ball.py` — `class Ball`

Pure Python dataclass-style object. Tracks `x`, `y`, `x_move`, `y_move`, and `move_speed`. Exposes movement methods and collision predicates. **Zero imports from `turtle`, `tkinter`, or `display`.**

| Method                       | Description                                                              |
| ---------------------------- | ------------------------------------------------------------------------ |
| `move()`                     | Advances position by current velocity vector                             |
| `bounce_x()` / `bounce_y()`  | Inverts the corresponding velocity component                             |
| `increase_speed()`           | Multiplies `move_speed` by `BALL_SPEED_FACTOR` (< 1 = faster loop delay) |
| `reset_position()`           | Returns to centre, resets speed, flips x direction                       |
| `hits_wall()`                | True when `y` exceeds `±WALL_BOUNDARY_Y`                                 |
| `hits_right_paddle(y)`       | True when ball is in the right paddle's hit zone and moving right        |
| `hits_left_paddle(y)`        | True when ball is in the left paddle's hit zone and moving left          |
| `out_right()` / `out_left()` | True when ball has fully passed a paddle (`±BALL_OUT_X`)                 |

### `paddle.py` — `class Paddle`, `LeftPaddle`, `RightPaddle`

Pure logic. Tracks `x` (fixed) and `y` (mutable). Clamps movement to `PADDLE_BOUNDARY_TOP` / `PADDLE_BOUNDARY_BOTTOM`. `LeftPaddle` and `RightPaddle` are thin subclasses that set the correct starting `x`.

### `scores.py` — `class ScoreTracker`

Tracks `left` and `right` integer counters. Exposes a `score` property returning `tuple[int, int]`. `is_game_over()` checks against `WIN_SCORE`. `reset()` zeroes both counters.

### `display.py` — `class Display`

Owns all four turtle objects (`_paddle_a`, `_paddle_b`, `_ball`, `_writer`) and the `Screen`. The game loop calls `render_*` methods every tick; `main.py` never touches a turtle directly.

| Method                      | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `render_ball(x, y)`         | Moves ball turtle to given coordinates                                      |
| `render_paddle(side, x, y)` | Moves the named paddle turtle                                               |
| `render_score(score)`       | Clears writer, redraws both scores in the HUD strip                         |
| `show_welcome()`            | Animated title screen; returns `"auto"`, `"manual"`, or `None` (quit)       |
| `show_pause()`              | Pause overlay; returns `True` (resume) or `False` (return to title)         |
| `show_game_over()`          | Game-over overlay; returns `True` (play again) or `False` (return to title) |
| `wait_for_serve()`          | Manual-serve prompt; returns `True` (serve) or `False` (return to title)    |
| `close()`                   | Calls `sys.exit(0)` — clean subprocess termination                          |

All overlays use `onkeypress` bindings consistently. Before entering any overlay, the caller unregisters the gameplay Space binding so it cannot double-fire. After the overlay returns, Space is re-registered for pause.

### `main.py`

Contains `GameState` (wraps `Ball`, `LeftPaddle`, `RightPaddle` with a `reset()` method) and `main()`.

`main()` runs two nested loops:

- **Outer loop** — calls `show_welcome()`, then enters the game loop. When the game loop `break`s (on any `R` press), the outer loop resets state and reruns the title screen in the same window.
- **Inner loop** — the live game loop. Runs at `ball.move_speed` cadence. Checks pause flag → runs physics → renders → checks scoring → handles overlays.

---

## Configuration reference

All values live in `advanced/config.py`.

| Constant                 | Default | Description                                                           |
| ------------------------ | ------- | --------------------------------------------------------------------- |
| `SCREEN_WIDTH`           | `800`   | Window width in pixels                                                |
| `SCREEN_HEIGHT`          | `760`   | Window height — court (600) + score strip (80) + bottom padding (80)  |
| `SCORE_DIVIDER_Y`        | `285`   | Y-coordinate of the top court boundary line                           |
| `SCORE_Y`                | `318`   | Y-coordinate of the score numerals in the HUD strip                   |
| `SCORE_FONT_SIZE`        | `40`    | Font size for HUD score numbers                                       |
| `PADDLE_SPEED`           | `20`    | Pixels the paddle moves per key-held tick                             |
| `PADDLE_BOUNDARY_TOP`    | `245`   | Maximum Y the paddle centre can reach                                 |
| `PADDLE_BOUNDARY_BOTTOM` | `−240`  | Minimum Y the paddle centre can reach                                 |
| `LEFT_PADDLE_X`          | `−350`  | Fixed X position of the left paddle                                   |
| `RIGHT_PADDLE_X`         | `350`   | Fixed X position of the right paddle                                  |
| `PADDLE_HALF_HEIGHT`     | `50`    | Half the paddle's pixel height — used in collision maths              |
| `BALL_INITIAL_SPEED`     | `0.025` | Starting `time.sleep` delay (seconds) per game tick                   |
| `BALL_X_MOVE`            | `10`    | Horizontal pixels per tick                                            |
| `BALL_Y_MOVE`            | `10`    | Vertical pixels per tick                                              |
| `BALL_SPEED_FACTOR`      | `0.95`  | `move_speed` multiplier per paddle hit (< 1 = shorter sleep = faster) |
| `WALL_BOUNDARY_Y`        | `275`   | Y-coordinate at which the ball bounces vertically                     |
| `PADDLE_HIT_INNER`       | `320`   | Inner edge of the paddle collision zone                               |
| `PADDLE_HIT_OUTER`       | `350`   | Outer edge (paddle face) of the collision zone                        |
| `BALL_OUT_X`             | `380`   | X-coordinate at which a point is awarded                              |
| `WIN_SCORE`              | `10`    | Points needed to win a match                                          |
| `WELCOME_LINE_DELAY`     | `0.25`  | Seconds between each line appearing on the title screen               |
| `POINT_PAUSE`            | `1.0`   | Seconds the game pauses after a point in auto-serve mode              |

---

## Display layout

```
 y = +380 ┌──────────────────────────────────────────────┐
          │                                              │
          │               3            7                 │  ← score HUD
          │                                              │
 y = +285 ├──────────────────────────────────────────────┤  ← SCORE_DIVIDER_Y (top line)
          │                    ║                      ██ │
          │                    ║                      ██ │
          │  ██                ║                      ██ │
          │  ██     ·          ║                         │  ← live court
          │  ██                ║                         │
          │                    ║                         │
          │                    ║  (dashed centre line)   │
 y = −285 ├──────────────────────────────────────────────┤  ← bottom line
          │                                              │
 y = −380 └──────────────────────────────────────────────┘
```

- The score strip occupies `y = +285` to `y = +380` (~95 px).
- The court occupies `y = −285` to `y = +285` (570 px visible play area).
- The bottom padding occupies `y = −380` to `y = −285` (~95 px).
- Ball bounce triggers at `WALL_BOUNDARY_Y = 275` (5 px inside the line) to prevent clipping.

---

## Design decisions

**Why two nested loops instead of a state machine?**
The outer title↔game loop keeps the control flow readable without introducing an enum-driven state machine. The title screen and the game loop are distinct phases with no shared tick logic, so a simple loop-in-loop is clearer than routing through a state variable.

**Why `sys.exit(0)` instead of `screen.bye()`?**
`screen.bye()` triggers tkinter cleanup that can raise `turtle.Terminator` or `TclError` when called outside the mainloop, leaving the subprocess in a broken state. `sys.exit(0)` terminates the process immediately and cleanly; `subprocess.run()` in `menu.py` receives exit code 0 and the terminal menu reappears.

**Why is Space unregistered before every overlay?**
turtle only keeps one `onkeypress` handler per key. If the gameplay pause handler and an overlay's Space handler are both registered, whichever was registered last wins — which is non-deterministic during rapid key presses. Explicitly unregistering before handing off and re-registering on return guarantees predictable behaviour.

**Why are `ball.py` and `paddle.py` UI-free?**
Keeping logic objects free of turtle imports means they can be tested, reused, or ported without any GUI dependency. `display.py` is the only file that knows what a `Turtle` is.

**Why `onkeypress` everywhere instead of `onkey`?**
`onkey` is an alias for `onkeyrelease` in turtle, which fires on key-up. `onkeypress` fires on key-down, which feels more responsive for both movement and overlay interactions. Mixing the two on the same key creates two independent bindings that can fire simultaneously.

---

## Course context

This project is the Day 22 capstone of [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code/) by Dr. Angela Yu. The original exercise covered:

- Class inheritance with `turtle.Turtle` as the base class
- Separation of concerns across multiple files
- Event-driven input using `onkeypress` / `onkeyrelease`
- Game loop design with `tracer(0)` + manual `screen.update()`

The `original/` directory preserves that work unchanged. The `advanced/` directory is a personal rebuild applying software design principles learned beyond the course.

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for the original exercise brief.

---

## Dependencies

Standard library only — no `pip install` required.

| Module       | Used for                                        |
| ------------ | ----------------------------------------------- |
| `turtle`     | All graphics rendering                          |
| `tkinter`    | Underlying GUI (bundled with `turtle`)          |
| `time`       | `sleep()` for game tick cadence and delays      |
| `sys`        | `sys.exit(0)` for clean subprocess termination  |
| `os`         | `os.system("clear")` in terminal menu           |
| `subprocess` | Launching game builds from `menu.py`            |
| `pathlib`    | `Path(__file__).parent` for portable file paths |

Python 3.10+ recommended. `turtle` and `tkinter` ship with CPython on macOS, Windows, and most Linux distributions.
