from turtle import Turtle

class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=1, stretch_wid=5)
        self.penup()

    def move_up(self):
        if self.ycor() < 245:  # Check if the paddle is within the top boundary
            new_y = self.ycor() + 20
            self.goto(self.xcor(), new_y)

    def move_down(self):
        if self.ycor() > -240:  # Check if the paddle is within the bottom boundary
            new_y = self.ycor() - 20
            self.goto(self.xcor(), new_y)

class RightPaddle(Paddle):
    def __init__(self, position):
        super().__init__()
        self.goto(position)

class LeftPaddle(Paddle):
    def __init__(self, position):
        super().__init__()
        self.goto(position)
