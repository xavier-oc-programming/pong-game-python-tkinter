from config import (
    BALL_INITIAL_SPEED,
    BALL_X_MOVE,
    BALL_Y_MOVE,
    BALL_SPEED_FACTOR,
    WALL_BOUNDARY_Y,
    PADDLE_HIT_INNER,
    PADDLE_HIT_OUTER,
    BALL_OUT_X,
    PADDLE_HALF_HEIGHT,
)


class Ball:
    """Pure ball logic — no UI, no turtle, no print()."""

    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.x_move: int = BALL_X_MOVE
        self.y_move: int = BALL_Y_MOVE
        self.move_speed: float = BALL_INITIAL_SPEED

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move(self) -> None:
        self.x += self.x_move
        self.y += self.y_move

    def bounce_y(self) -> None:
        self.y_move *= -1

    def bounce_x(self) -> None:
        self.x_move *= -1

    def increase_speed(self) -> None:
        self.move_speed *= BALL_SPEED_FACTOR

    def reset_position(self) -> None:
        self.x = 0.0
        self.y = 0.0
        self.move_speed = BALL_INITIAL_SPEED
        self.bounce_x()

    # ------------------------------------------------------------------
    # Collision predicates
    # ------------------------------------------------------------------

    def hits_wall(self) -> bool:
        return self.y > WALL_BOUNDARY_Y or self.y < -WALL_BOUNDARY_Y

    def hits_right_paddle(self, paddle_y: float) -> bool:
        in_y_range = paddle_y - PADDLE_HALF_HEIGHT < self.y < paddle_y + PADDLE_HALF_HEIGHT
        in_x_zone = PADDLE_HIT_INNER < self.x < PADDLE_HIT_OUTER
        return in_y_range and in_x_zone and self.x_move > 0

    def hits_left_paddle(self, paddle_y: float) -> bool:
        in_y_range = paddle_y - PADDLE_HALF_HEIGHT < self.y < paddle_y + PADDLE_HALF_HEIGHT
        in_x_zone = -PADDLE_HIT_OUTER < self.x < -PADDLE_HIT_INNER
        return in_y_range and in_x_zone and self.x_move < 0

    def out_right(self) -> bool:
        return self.x > BALL_OUT_X

    def out_left(self) -> bool:
        return self.x < -BALL_OUT_X
