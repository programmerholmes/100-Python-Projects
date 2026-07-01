from turtle import Turtle, Screen
import turtle as t
import random

random_walk = Turtle()

t.colormode(255)

random_walk.speed("fastest")


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    random_color = (r, g, b)
    return random_color


def direction():
    sides = [0, 90, 180, 270]
    return random.choice(sides)


for _ in range(500):
    random_walk.color(random_color())
    random_walk.pensize(15)
    random_walk.forward(30)
    random_walk.setheading(direction())


screen = Screen()

screen.exitonclick()
