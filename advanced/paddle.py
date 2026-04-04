from config import (
    LEFT_PADDLE_X,
    RIGHT_PADDLE_X,
    PADDLE_SPEED,
    PADDLE_BOUNDARY_TOP,
    PADDLE_BOUNDARY_BOTTOM,
)


class Paddle:
    """Pure paddle logic — no UI, no turtle, no print()."""

    def __init__(self, x: int) -> None:
        self.x: int = x
        self.y: int = 0

    def move_up(self) -> None:
        if self.y < PADDLE_BOUNDARY_TOP:
            self.y += PADDLE_SPEED

    def move_down(self) -> None:
        if self.y > PADDLE_BOUNDARY_BOTTOM:
            self.y -= PADDLE_SPEED

    def reset(self) -> None:
        self.y = 0


class LeftPaddle(Paddle):
    def __init__(self) -> None:
        super().__init__(LEFT_PADDLE_X)


class RightPaddle(Paddle):
    def __init__(self) -> None:
        super().__init__(RIGHT_PADDLE_X)
