from pathlib import Path

from config import WIN_SCORE

_DATA_FILE = Path(__file__).parent / "data.txt"


class ScoreTracker:
    """Tracks left/right scores and persists the all-time high score."""

    def __init__(self) -> None:
        self.left: int = 0
        self.right: int = 0
        self.high_score: int = self._load()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def score(self) -> tuple[int, int]:
        return (self.left, self.right)

    def left_point(self) -> None:
        self.left += 1
        self._maybe_save(self.left)

    def right_point(self) -> None:
        self.right += 1
        self._maybe_save(self.right)

    def is_game_over(self) -> bool:
        return self.left >= WIN_SCORE or self.right >= WIN_SCORE

    def reset(self) -> None:
        """Reset round scores; high score is already persisted."""
        self.left = 0
        self.right = 0

    # ------------------------------------------------------------------
    # File I/O
    # ------------------------------------------------------------------

    def _load(self) -> int:
        try:
            return int(_DATA_FILE.read_text().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _maybe_save(self, value: int) -> None:
        if value > self.high_score:
            self.high_score = value
            _DATA_FILE.write_text(str(self.high_score))
