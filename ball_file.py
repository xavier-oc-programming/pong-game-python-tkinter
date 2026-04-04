from turtle import Turtle
MOVE_SPEED = 0.025

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = MOVE_SPEED  # Start with a faster ball speed

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = MOVE_SPEED  # Reset to the consistent initial speed
        self.bounce_x()

    def increase_speed(self):
        self.move_speed *= 0.95  # Speed up the ball by 5% after each paddle hit