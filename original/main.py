from turtle import Screen
from ball_file import Ball
from paddles import RightPaddle, LeftPaddle
import time
from scoreboard_file import Scoreboard

# Screen setup
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

# Game elements
score = Scoreboard()
right_paddle = RightPaddle((350, 0))  # Right paddle's x position is 350
left_paddle = LeftPaddle((-350, 0))  # Left paddle's x position is -350
ball = Ball()

# Key state tracking
keys_pressed = {
    "w": False,
    "s": False,
    "Up": False,
    "Down": False
}


# Functions to update key press status
def press_w():
    keys_pressed["w"] = True


def release_w():
    keys_pressed["w"] = False


def press_s():
    keys_pressed["s"] = True


def release_s():
    keys_pressed["s"] = False


def press_up():
    keys_pressed["Up"] = True


def release_up():
    keys_pressed["Up"] = False


def press_down():
    keys_pressed["Down"] = True


def release_down():
    keys_pressed["Down"] = False


# Bind keys to press and release events
screen.listen()
screen.onkeypress(press_w, "w")
screen.onkeyrelease(release_w, "w")
screen.onkeypress(press_s, "s")
screen.onkeyrelease(release_s, "s")
screen.onkeypress(press_up, "Up")
screen.onkeyrelease(release_up, "Up")
screen.onkeypress(press_down, "Down")
screen.onkeyrelease(release_down, "Down")


# Game over function
def check_game_over():
    if score.l_score >= 10 or score.r_score >= 10:
        ball.hideturtle()
        screen.clear()
        screen.bgcolor("black")
        screen.title("Pong")
        score.goto(0, 0)
        score.write("Game Over", align="center", font=("Courier", 50, "normal"))
        return True
    return False


# Function to check if the ball collides with the paddle
def is_collision_with_paddle(ball, paddle):
    # Check if ball's y-coordinate is within the paddle's y-range
    if paddle.ycor() - 50 < ball.ycor() < paddle.ycor() + 50:
        # Check if the ball is exactly at the paddle's front face
        if (ball.xcor() > 320 and ball.xcor() < 350 and ball.x_move > 0) or (
                ball.xcor() < -320 and ball.xcor() > -350 and ball.x_move < 0):
            return True
    return False


# Game loop
game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()

    # Ball movement
    ball.move()

    # Paddle movement
    if keys_pressed["w"]:
        left_paddle.move_up()
    if keys_pressed["s"]:
        left_paddle.move_down()
    if keys_pressed["Up"]:
        right_paddle.move_up()
    if keys_pressed["Down"]:
        right_paddle.move_down()

    # Detect collision with the top and bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with the paddles (using precise detection)
    if is_collision_with_paddle(ball, right_paddle):
        ball.bounce_x()
        ball.increase_speed()

    if is_collision_with_paddle(ball, left_paddle):
        ball.bounce_x()
        ball.increase_speed()

    # Detect when right paddle misses
    if ball.xcor() > 380:
        ball.reset_position()
        score.l_point()
        time.sleep(1)  # Wait 1 second before starting next round
        if check_game_over():
            game_is_on = False  # End the game if game over

    # Detect when left paddle misses
    if ball.xcor() < -380:
        ball.reset_position()
        score.r_point()
        time.sleep(1)  # Wait 1 second before starting next round
        if check_game_over():
            game_is_on = False  # End the game if game over

screen.exitonclick()
