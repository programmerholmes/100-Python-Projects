from turtle import Turtle, Screen
import time
import paddle
from scoreboard import ScoreBoard
from ball import Ball
import line

screen = Screen()

screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

# Creating objects
r_paddle = paddle.Paddle((350, 0))
l_paddle = paddle.Paddle((-350, 0))
ball = Ball()
score = ScoreBoard()
line = line.Line()

screen.listen()

screen.onkey(key="Up", fun=r_paddle.go_up)
screen.onkey(key="Down", fun=r_paddle.go_down)
screen.onkey(key="w", fun=l_paddle.go_up)
screen.onkey(key="s", fun=l_paddle.go_down)


game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with paddle
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # Detect right paddle missed
    if ball.xcor() > 380:
        ball.reset_position()
        score.l_point()

    # Detect left paddle missed
    if ball.xcor() < -380:
        ball.reset_position()
        score.r_point()


screen.exitonclick()
