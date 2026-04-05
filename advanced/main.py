import time

from ball import Ball
from paddle import LeftPaddle, RightPaddle
from scores import ScoreTracker
from display import Display
from config import POINT_PAUSE


class GameState:
    """Holds all mutable game objects; reset() returns them to start positions."""

    def __init__(self) -> None:
        self.ball: Ball = Ball()
        self.paddle_a: LeftPaddle = LeftPaddle()
        self.paddle_b: RightPaddle = RightPaddle()

    def reset(self) -> None:
        self.ball.reset_position()
        self.paddle_a.reset()
        self.paddle_b.reset()


def main() -> None:
    state = GameState()
    tracker = ScoreTracker()
    display = Display()

    # Position all objects at their starting coordinates before welcome screen.
    display.render_ball(state.ball.x, state.ball.y)
    display.render_paddle("a", state.paddle_a.x, state.paddle_a.y)
    display.render_paddle("b", state.paddle_b.x, state.paddle_b.y)
    display.render_score(tracker.score)
    display.screen.update()

    mode: str = display.show_welcome()  # "auto" or "manual"

    # ------------------------------------------------------------------
    # Key state — track hold, not single press
    # ------------------------------------------------------------------
    keys: dict[str, bool] = {
        "w": False, "s": False, "Up": False, "Down": False, "pause": False,
    }

    def press_w() -> None:     keys["w"] = True
    def release_w() -> None:   keys["w"] = False
    def press_s() -> None:     keys["s"] = True
    def release_s() -> None:   keys["s"] = False
    def press_up() -> None:    keys["Up"] = True
    def release_up() -> None:  keys["Up"] = False
    def press_dn() -> None:    keys["Down"] = True
    def release_dn() -> None:  keys["Down"] = False
    def trigger_pause() -> None: keys["pause"] = True

    display.screen.onkeypress(press_w,       "w")
    display.screen.onkeyrelease(release_w,   "w")
    display.screen.onkeypress(press_s,       "s")
    display.screen.onkeyrelease(release_s,   "s")
    display.screen.onkeypress(press_up,      "Up")
    display.screen.onkeyrelease(release_up,  "Up")
    display.screen.onkeypress(press_dn,      "Down")
    display.screen.onkeyrelease(release_dn,  "Down")
    display.screen.onkeypress(trigger_pause, "space")
    display.screen.listen()

    # ------------------------------------------------------------------
    # Game loop
    # ------------------------------------------------------------------
    while True:
        time.sleep(state.ball.move_speed)
        display.screen.update()

        # --- pause --------------------------------------------------
        if keys["pause"]:
            keys["pause"] = False
            display.screen.onkeypress(None, "space")  # yield Space to pause overlay
            if not display.show_pause():
                display.close()
                return
            display.screen.onkeypress(trigger_pause, "space")
            display.screen.listen()

        # --- logic --------------------------------------------------
        state.ball.move()

        if keys["w"]:    state.paddle_a.move_up()
        if keys["s"]:    state.paddle_a.move_down()
        if keys["Up"]:   state.paddle_b.move_up()
        if keys["Down"]: state.paddle_b.move_down()

        if state.ball.hits_wall():
            state.ball.bounce_y()

        if state.ball.hits_right_paddle(state.paddle_b.y):
            state.ball.bounce_x()
            state.ball.increase_speed()

        if state.ball.hits_left_paddle(state.paddle_a.y):
            state.ball.bounce_x()
            state.ball.increase_speed()

        # --- render -------------------------------------------------
        display.render_ball(state.ball.x, state.ball.y)
        display.render_paddle("a", state.paddle_a.x, state.paddle_a.y)
        display.render_paddle("b", state.paddle_b.x, state.paddle_b.y)

        # --- scoring ------------------------------------------------
        point_scored = False

        if state.ball.out_right():
            tracker.left_point()
            state.ball.reset_position()
            display.render_score(tracker.score)
            point_scored = True

        elif state.ball.out_left():
            tracker.right_point()
            state.ball.reset_position()
            display.render_score(tracker.score)
            point_scored = True

        if point_scored:
            if tracker.is_game_over():
                tracker.reset()
                display.render_score(tracker.score)  # update BEFORE overlay
                if not display.show_game_over():
                    display.close()
                    return                    # subprocess ends cleanly → menu reappears
                state.reset()
                # re-render all objects before resuming loop
                display.render_ball(state.ball.x, state.ball.y)
                display.render_paddle("a", state.paddle_a.x, state.paddle_a.y)
                display.render_paddle("b", state.paddle_b.x, state.paddle_b.y)
                display.render_score(tracker.score)
                display.screen.update()
                display.screen.onkeypress(trigger_pause, "space")
                display.screen.listen()
            elif mode == "auto":
                time.sleep(POINT_PAUSE)
                keys["pause"] = False  # discard any Space pressed during the delay
            else:
                # manual mode — yield Space to serve prompt then reclaim for pause
                display.screen.onkeypress(None, "space")
                if not display.wait_for_serve():
                    display.close()
                    return
                display.screen.onkeypress(trigger_pause, "space")
                display.screen.listen()


if __name__ == "__main__":
    main()
