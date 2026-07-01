from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet!", prompt="Which turtle will win the race? Enter a colour: ")

colours = ["red", "green", "yellow", "orange", "blue", "purple", "pink"]
y_position = [-100, -70, -40, -10, 20, 50, 80]
all_turtles = []

race_is_on = False

for turtle_index in range(0, 7):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.goto(-230, y_position[turtle_index])
    new_turtle.color(colours[turtle_index])
    all_turtles.append(new_turtle)


if user_bet:
    race_is_on = True

while race_is_on:

    for turtle in all_turtles:
        if turtle.xcor() > 230:
            race_is_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")

        random_speed = random.randint(0, 10)
        turtle.forward(random_speed)


screen.exitonclick()
