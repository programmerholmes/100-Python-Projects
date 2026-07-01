from turtle import Turtle, Screen
import turtle as t
import random

circle = Turtle()
t.colormode(255)
circle.speed(0)



def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color


def draw_spirograph(size_of_gap):
    for o in range(int(360 / size_of_gap)):
        circle.color(random_color())
        circle.circle(100)
        circle.left(size_of_gap)


draw_spirograph(5)





screen = Screen()

screen.exitonclick()
