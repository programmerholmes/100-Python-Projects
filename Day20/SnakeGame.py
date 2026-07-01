from turtle import Screen
import Snake
from Food import Food
from Scoreboard import Score
import time


screen = Screen()
screen.bgcolor("black")
screen.title("The nostalgic snake game")
screen.tracer(0)
screen.setup(width=600, height=600)

snake = Snake.Snake()
food = Food()
score = Score()

screen.listen()
screen.onkey(key="Up", fun=snake.up)
screen.onkey(key="Down", fun=snake.down)
screen.onkey(key="Left", fun=snake.left)
screen.onkey(key="Right", fun=snake.right)


game_is_on = True

while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()

    # Detect collision with food.
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        score.increase_scoreboard()

    # Detect collision with wall.
    if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -290:
        game_is_on = False
        score.game_over()

    # Detect collision with tail
    # for snakey_block in snake.snake_block:
    #     if snakey_block == snake.head:
    #         pass
    #     elif snake.head.distance(snakey_block) < 10:
    #         game_is_on = False
    #         score.game_over()

    # OR using slicing
    for snakey_block in snake.snake_block[1:]:
        if snake.head.distance(snakey_block) < 10:
            game_is_on = False
            score.game_over()
screen.exitonclick()
