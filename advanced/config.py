# ---------------------------------------------------------------------------
# Screen
# ---------------------------------------------------------------------------
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 760          # court (600) + 80px score strip above + 80px padding below
SCORE_DIVIDER_Y: int = 285        # horizontal line separating score strip from court
SCORE_Y: int = 318                # y-position of score numerals inside the strip
SCORE_FONT_SIZE: int = 40         # font size for HUD scores (was 80, court-embedded)
SCREEN_BG: str = "black"
SCREEN_TITLE: str = "Pong"

# ---------------------------------------------------------------------------
# Paddle geometry & movement
# ---------------------------------------------------------------------------
PADDLE_STRETCH_LEN: int = 1
PADDLE_STRETCH_WID: int = 5
PADDLE_SPEED: int = 20
PADDLE_BOUNDARY_TOP: int = 245
PADDLE_BOUNDARY_BOTTOM: int = -240
LEFT_PADDLE_X: int = -350
RIGHT_PADDLE_X: int = 350
PADDLE_HALF_HEIGHT: int = 50  # half of shapesize stretch_wid * 10

# ---------------------------------------------------------------------------
# Ball movement & collision
# ---------------------------------------------------------------------------
BALL_INITIAL_SPEED: float = 0.025
BALL_X_MOVE: int = 10
BALL_Y_MOVE: int = 10
BALL_SPEED_FACTOR: float = 0.95   # multiply move_speed each paddle hit
WALL_BOUNDARY_Y: int = 280
PADDLE_HIT_INNER: int = 320       # x-zone start (inner edge of paddle hit zone)
PADDLE_HIT_OUTER: int = 350       # x-zone end   (paddle face)
BALL_OUT_X: int = 380             # ball has escaped past a paddle

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
WIN_SCORE: int = 10

# ---------------------------------------------------------------------------
# Display timings
# ---------------------------------------------------------------------------
WELCOME_LINE_DELAY: float = 0.25  # seconds between each welcome-screen line
POINT_PAUSE: float = 1.0          # pause after a point is scored
