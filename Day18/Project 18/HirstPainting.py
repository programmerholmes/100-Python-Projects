from turtle import Turtle, Screen
import turtle as t
import random


t.colormode(255)
# import colorgram
#
# rgb_color = []
#
# colors = colorgram.extract('hirst-pic.jpg', 45)
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_color.append(new_color)
#
# print(rgb_color)
colors_list = [(233, 239, 246), (246, 239, 242), (132, 166, 205), (221, 148, 106), (32, 42, 61), (199, 135, 148),
               (166, 58, 48), (141, 184, 162), (39, 105, 157), (237, 212, 90), (150, 59, 66), (216, 82, 71),
               (168, 29, 33), (235, 165, 157), (51, 111, 90), (35, 61, 55), (156, 33, 31), (17, 97, 71), (52, 44, 49),
               (230, 161, 166), (170, 188, 221), (57, 51, 48), (184, 103, 113), (32, 60, 109), (105, 126, 159),
               (175, 200, 188), (34, 151, 210), (65, 66, 56), (106, 140, 124), (153, 202, 227), (48, 69, 71),
               (131, 128, 121)]

turtle = Turtle()
turtle.speed(0)
turtle.setheading(225)
turtle.penup()
turtle.hideturtle()
turtle.forward(300)
turtle.setheading(0)
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):

    # turtle.pendown()
    turtle.dot(20, random.choice(colors_list))
    # turtle.penup()
    turtle.forward(50)

    if dot_count % 10 == 0:
        turtle.setheading(90)
        turtle.forward(50)
        turtle.setheading(180)
        turtle.forward(500)
        turtle.setheading(0)


screen = Screen()
screen.exitonclick()
