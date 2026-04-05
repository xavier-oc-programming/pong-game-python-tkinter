from config import WIN_SCORE


class ScoreTracker:
    """Tracks left/right scores for a single match."""

    def __init__(self) -> None:
        self.left: int = 0
        self.right: int = 0

    @property
    def score(self) -> tuple[int, int]:
        return (self.left, self.right)

    def left_point(self) -> None:
        self.left += 1

    def right_point(self) -> None:
        self.right += 1

    def is_game_over(self) -> bool:
        return self.left >= WIN_SCORE or self.right >= WIN_SCORE

    def reset(self) -> None:
        self.left = 0
        self.right = 0
