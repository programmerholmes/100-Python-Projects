from turtle import Turtle

STARTING_POSITION = [(0, 0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:

    def __init__(self):
        self.snake_block = []
        self.create_snake()
        self.head = self.snake_block[0]

    def create_snake(self):
        for position in STARTING_POSITION:
            self.add_snake_block(position)

    def add_snake_block(self, position):
        new_snake = Turtle(shape="square")
        new_snake.color("white")
        new_snake.penup()
        new_snake.goto(position)
        self.snake_block.append(new_snake)

    def extend(self):
        self.add_snake_block(self.snake_block[-1].position())

    def move(self):
        for num in range(len(self.snake_block) - 1, 0, -1):
            new_x = self.snake_block[num - 1].xcor()
            new_y = self.snake_block[num - 1].ycor()
            self.snake_block[num].goto(new_x, new_y)
        self.head.forward(MOVE_DISTANCE)


    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
