from turtle import Turtle, Screen
import random

shapes = Turtle()

colours = ["moccasin", "turquoise", "sienna", "medium slate blue", "light yellow", "lime", "forest green", "teal",
           "violet", "red", "green", "blue", "dark orange", "olive", "light sky blue", "dodger blue"]

def shape(sides):
    angle = 360 / sides
    for _ in range(sides):
        shapes.forward(100)
        shapes.right(angle)

for shapey in range(3, 11):
    shapes.color(random.choice(colours))
    shape(shapey)

screen = Screen()
screen.exitonclick()