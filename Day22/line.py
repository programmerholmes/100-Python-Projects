from turtle import Turtle

class Line(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 280)
        self.right(90)
        self.pendown()
        self.forward(550)
