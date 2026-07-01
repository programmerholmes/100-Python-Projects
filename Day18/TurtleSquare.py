from turtle import Turtle, Screen

square = Turtle()

# for _ in range(4):
#     square.right(90)
#     square.dot(15)
#     square.forward(100)



# Dashed lines
# for i in range(10):
#     square.forward(10)
#     square.pencolor("white")
#     square.forward(10)
#     square.pencolor("black")
#

# OR

for i in range(10):
    square.forward(10)
    square.penup()
    square.forward(10)
    square.pendown()


screen = Screen()
screen.exitonclick()