import time
from turtle import Screen, Turtle

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_BG,
    SCREEN_TITLE,
    PADDLE_STRETCH_LEN,
    PADDLE_STRETCH_WID,
    WELCOME_LINE_DELAY,
)


class Display:
    """Owns every turtle object and all rendering.  No game logic lives here."""

    def __init__(self) -> None:
        self.screen: Screen = Screen()
        self.screen.bgcolor(SCREEN_BG)
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.title(SCREEN_TITLE)
        self.screen.tracer(0)

        self._paddle_a: Turtle = self._make_paddle()
        self._paddle_b: Turtle = self._make_paddle()
        self._ball: Turtle = self._make_ball()
        self._writer: Turtle = self._make_writer()

        self._draw_center_line()

    # ------------------------------------------------------------------
    # Factory helpers
    # ------------------------------------------------------------------

    def _make_paddle(self) -> Turtle:
        t = Turtle()
        t.shape("square")
        t.color("white")
        t.shapesize(stretch_len=PADDLE_STRETCH_LEN, stretch_wid=PADDLE_STRETCH_WID)
        t.penup()
        return t

    def _make_ball(self) -> Turtle:
        t = Turtle()
        t.shape("circle")
        t.color("white")
        t.penup()
        return t

    def _make_writer(self) -> Turtle:
        t = Turtle()
        t.hideturtle()
        t.penup()
        t.color("white")
        return t

    def _draw_center_line(self) -> None:
        line = Turtle()
        line.hideturtle()
        line.penup()
        line.color("white")
        line.goto(0, SCREEN_HEIGHT // 2)
        line.setheading(270)
        line.pendown()
        for _ in range(SCREEN_HEIGHT // 20):
            line.forward(10)
            line.penup()
            line.forward(10)
            line.pendown()

    # ------------------------------------------------------------------
    # Per-frame render calls (called every tick from main)
    # ------------------------------------------------------------------

    def render_ball(self, x: float, y: float) -> None:
        self._ball.goto(x, y)

    def render_paddle(self, side: str, x: float, y: float) -> None:
        if side == "a":
            self._paddle_a.goto(x, y)
        else:
            self._paddle_b.goto(x, y)

    def render_score(self, score: tuple[int, int]) -> None:
        self._writer.clear()
        self._writer.color("white")
        self._writer.goto(-100, 200)
        self._writer.write(score[0], align="center", font=("Courier", 80, "normal"))
        self._writer.goto(100, 200)
        self._writer.write(score[1], align="center", font=("Courier", 80, "normal"))

    # ------------------------------------------------------------------
    # Welcome screen — returns "auto" or "manual"
    # ------------------------------------------------------------------

    def show_welcome(self) -> str:
        self._ball.hideturtle()
        self._paddle_a.hideturtle()
        self._paddle_b.hideturtle()

        lines: list[tuple[str, int, str, int]] = [
            # (text, font_size, style, y_position)
            ("P O N G",               48, "bold",    140),
            ("",                        0, "normal",   90),
            ("Left Player",            18, "normal",   60),
            ("  Move up:    W",        16, "normal",   35),
            ("  Move down:  S",        16, "normal",   10),
            ("",                        0, "normal",  -15),
            ("Right Player",           18, "normal",  -40),
            ("  Move up:    \u2191",   16, "normal",  -65),
            ("  Move down:  \u2193",   16, "normal",  -90),
            ("",                        0, "normal", -115),
            ("[ SPACE ]  pause anytime", 14, "normal", -135),
            ("",                        0, "normal", -160),
            ("Next point starts:",      16, "normal", -178),
            ("[ A ]  auto     [ M ]  manual (Space to serve)", 15, "bold", -210),
        ]

        for text, size, style, y in lines:
            if text:
                self._writer.goto(0, y)
                self._writer.write(text, align="center", font=("Courier", size, style))
            time.sleep(WELCOME_LINE_DELAY)
            self.screen.update()

        _choice: dict[str, str | None] = {"value": None}

        def _on_a() -> None:
            _choice["value"] = "auto"

        def _on_m() -> None:
            _choice["value"] = "manual"

        self.screen.onkeypress(_on_a, "a")
        self.screen.onkeypress(_on_m, "m")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "a")
        self.screen.onkeypress(None, "m")
        self._ball.showturtle()
        self._paddle_a.showturtle()
        self._paddle_b.showturtle()

        return _choice["value"]

    # ------------------------------------------------------------------
    # Pause overlay
    # ------------------------------------------------------------------

    def show_pause(self) -> bool:
        """Overlay PAUSED on the frozen game state.

        Returns True  → resume.
        Returns False → quit.
        """
        self._writer.goto(0, 30)
        self._writer.color("white")
        self._writer.write(
            "PAUSED",
            align="center",
            font=("Courier", 50, "bold"),
        )

        self._writer.goto(0, -30)
        self._writer.write(
            "[ SPACE ]  resume        [ Q ]  quit",
            align="center",
            font=("Courier", 16, "normal"),
        )

        self.screen.update()

        _choice: dict[str, bool | None] = {"value": None}

        def _on_space() -> None:
            _choice["value"] = True

        def _on_q() -> None:
            _choice["value"] = False

        self.screen.onkeypress(_on_space, "space")
        self.screen.onkeypress(_on_q, "q")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "space")
        self.screen.onkeypress(None, "q")

        return bool(_choice["value"])

    # ------------------------------------------------------------------
    # Manual-mode serve prompt
    # ------------------------------------------------------------------

    def wait_for_serve(self) -> None:
        """Show 'Space to serve' prompt and block until Space is pressed."""
        self._writer.goto(0, -200)
        self._writer.color("white")
        self._writer.write(
            "[ SPACE ]  to serve",
            align="center",
            font=("Courier", 16, "normal"),
        )
        self.screen.update()

        _pressed: dict[str, bool] = {"space": False}

        def _on_space() -> None:
            _pressed["space"] = True

        self.screen.onkeypress(_on_space, "space")
        self.screen.listen()

        while not _pressed["space"]:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "space")

    # ------------------------------------------------------------------
    # Game-over overlay
    # ------------------------------------------------------------------

    def show_game_over(self) -> bool:
        """Overlay GAME OVER on the frozen game state.

        Returns True  → play again.
        Returns False → quit.
        """
        self._writer.goto(0, 50)
        self._writer.color("red")
        self._writer.write(
            "GAME OVER",
            align="center",
            font=("Courier", 50, "bold"),
        )

        self._writer.goto(0, -30)
        self._writer.color("white")
        self._writer.write(
            "[ SPACE ]  play again        [ Q ]  quit",
            align="center",
            font=("Courier", 16, "normal"),
        )

        self.screen.update()

        _choice: dict[str, bool | None] = {"value": None}

        def _on_space() -> None:
            _choice["value"] = True

        def _on_q() -> None:
            _choice["value"] = False

        self.screen.onkeypress(_on_space, "space")
        self.screen.onkeypress(_on_q, "q")
        self.screen.listen()

        while _choice["value"] is None:
            time.sleep(0.05)
            self.screen.update()

        self._writer.clear()
        self.screen.onkeypress(None, "space")
        self.screen.onkeypress(None, "q")

        return bool(_choice["value"])

    # ------------------------------------------------------------------
    # Teardown
    # ------------------------------------------------------------------

    def close(self) -> None:
        self.screen.bye()
