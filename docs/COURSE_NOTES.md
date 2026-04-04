# Course Notes — Day 22: Pong

## Exercise description

**Course:** 100 Days of Code: The Complete Python Pro Bootcamp (Udemy — Dr. Angela Yu)
**Day:** 22
**Topic:** Building Pong — the final project for the Object-Oriented Programming section

---

## Brief

Recreate the classic arcade game Pong using Python's `turtle` module.
This was the capstone project for the OOP section of the course, bringing together
class design, inheritance, and event-driven programming.

### Requirements set by the course

1. **Screen setup** — 800 × 600 black window, tracer off for manual refresh control.
2. **Two paddles** — left and right, controlled independently via keyboard.
3. **Ball** — moves continuously; bounces off top/bottom walls and paddles.
4. **Scoreboard** — displays each player's score at the top; updates on every point.
5. **Collision detection** — ball reverses x-direction when it hits a paddle face.
6. **Speed increase** — ball speeds up by 5 % after every paddle hit.
7. **Reset on miss** — ball returns to centre when it passes a paddle; score increments.
8. **Game over** — first player to 10 points ends the game.

### Key OOP concepts practised

- Class inheritance (`Ball`, `Paddle`, `Scoreboard` all extend `Turtle`)
- Encapsulation — each class owns its own state and behaviour
- Separation of concerns across multiple files
- Event-driven input with `onkeypress` / `onkeyrelease`

---

## Original file layout (course state)

```
main.py            — screen setup, game loop, collision logic
ball_file.py       — Ball class (movement, bounce, speed)
paddles.py         — Paddle, LeftPaddle, RightPaddle classes
scoreboard_file.py — Scoreboard class (display, point tracking)
```

---

## Notes on deviations from the course

The files in `original/` are kept as close as possible to the course state.
The only permitted change was fixing any hard-coded file paths to use
`Path(__file__).parent` so the game can be launched from the root `menu.py`
without breaking relative imports or data reads.
In practice the original has no file I/O, so **no changes were needed**.
