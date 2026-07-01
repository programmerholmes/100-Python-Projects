import os
import sys

# ---------------------------------------------------------
# Tkinter/Turtle path fix for some Windows/PyCharm setups.
# Turtle uses Tkinter, and Tkinter needs the Tcl/Tk library
# folders before Turtle creates its screen.
# ---------------------------------------------------------
def configure_tcl_tk_paths():
    possible_roots = [
        sys.base_prefix,
        sys.prefix,
        os.path.dirname(os.path.dirname(sys.executable)),
    ]

    for root in possible_roots:
        tcl_library = os.path.join(root, "tcl", "tcl8.6")
        tk_library = os.path.join(root, "tcl", "tk8.6")

        if os.path.exists(os.path.join(tcl_library, "init.tcl")):
            os.environ["TCL_LIBRARY"] = tcl_library

            if os.path.exists(os.path.join(tk_library, "tk.tcl")):
                os.environ["TK_LIBRARY"] = tk_library

            return


configure_tcl_tk_paths()

from turtle import Screen, Turtle
import random

# -----------------------------
# Game settings
# -----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_DELAY = 16  # about 60 frames per second

PADDLE_WIDTH = 110
PADDLE_HEIGHT = 20
PADDLE_Y = -250
PADDLE_MOVE_DISTANCE = 40

BALL_RADIUS = 10
BALL_START_SPEED_X = 4
BALL_START_SPEED_Y = 5
BALL_MAX_SPEED = 9

BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 22
BRICK_GAP = 10
BRICK_START_Y = 215

STARTING_LIVES = 3


# -----------------------------
# Helper function
# -----------------------------
def clamp(value, minimum, maximum):
    """Keeps a value inside a minimum and maximum range."""
    return max(minimum, min(value, maximum))


# -----------------------------
# Paddle class
# -----------------------------
class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(stretch_wid=PADDLE_HEIGHT / 20, stretch_len=PADDLE_WIDTH / 20)
        self.goto(0, PADDLE_Y)
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT

    def move_left(self):
        left_limit = -SCREEN_WIDTH / 2 + self.width / 2
        new_x = clamp(self.xcor() - PADDLE_MOVE_DISTANCE, left_limit, -left_limit)
        self.setx(new_x)

    def move_right(self):
        right_limit = SCREEN_WIDTH / 2 - self.width / 2
        new_x = clamp(self.xcor() + PADDLE_MOVE_DISTANCE, -right_limit, right_limit)
        self.setx(new_x)


# -----------------------------
# Ball class
# -----------------------------
class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = BALL_START_SPEED_X
        self.y_move = BALL_START_SPEED_Y
        self.reset_position(0)

    def move(self):
        self.goto(self.xcor() + self.x_move, self.ycor() + self.y_move)

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def reset_position(self, paddle_x):
        """Places the ball above the paddle ready for launch."""
        self.goto(paddle_x, PADDLE_Y + PADDLE_HEIGHT / 2 + BALL_RADIUS + 8)
        self.x_move = random.choice([-BALL_START_SPEED_X, BALL_START_SPEED_X])
        self.y_move = BALL_START_SPEED_Y

    def speed_up(self):
        """Slightly increases ball speed, but keeps the game playable."""
        if abs(self.x_move) < BALL_MAX_SPEED:
            self.x_move *= 1.02
        if abs(self.y_move) < BALL_MAX_SPEED:
            self.y_move *= 1.02


# -----------------------------
# Brick class
# -----------------------------
class Brick(Turtle):
    def __init__(self, x, y, color, points):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.shapesize(stretch_wid=BRICK_HEIGHT / 20, stretch_len=BRICK_WIDTH / 20)
        self.goto(x, y)
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.points = points


# -----------------------------
# Scoreboard class
# -----------------------------
class Scoreboard:
    def __init__(self):
        self.score_writer = Turtle()
        self.message_writer = Turtle()

        for writer in [self.score_writer, self.message_writer]:
            writer.hideturtle()
            writer.penup()
            writer.color("white")

        self.score_writer.goto(0, 265)
        self.message_writer.goto(0, -40)

    def update_score(self, score, lives, bricks_left):
        self.score_writer.clear()
        self.score_writer.write(
            f"Score: {score}    Lives: {lives}    Bricks Left: {bricks_left}",
            align="center",
            font=("Courier", 16, "normal")
        )

    def show_message(self, message):
        self.message_writer.clear()
        self.message_writer.write(
            message,
            align="center",
            font=("Courier", 18, "bold")
        )

    def clear_message(self):
        self.message_writer.clear()


# -----------------------------
# Collision helper functions
# -----------------------------
def ball_hits_rectangle(ball, rectangle):
    """Checks whether the ball overlaps a rectangular object."""
    return (
        rectangle.xcor() - rectangle.width / 2 - BALL_RADIUS
        <= ball.xcor()
        <= rectangle.xcor() + rectangle.width / 2 + BALL_RADIUS
        and rectangle.ycor() - rectangle.height / 2 - BALL_RADIUS
        <= ball.ycor()
        <= rectangle.ycor() + rectangle.height / 2 + BALL_RADIUS
    )


def bounce_ball_from_rectangle(ball, rectangle):
    """
    Bounces the ball from the correct side of a rectangle.
    This makes brick collisions feel more natural.
    """
    distance_x = ball.xcor() - rectangle.xcor()
    distance_y = ball.ycor() - rectangle.ycor()

    overlap_x = (rectangle.width / 2 + BALL_RADIUS) - abs(distance_x)
    overlap_y = (rectangle.height / 2 + BALL_RADIUS) - abs(distance_y)

    if overlap_x < overlap_y:
        ball.bounce_x()

        if distance_x > 0:
            ball.setx(rectangle.xcor() + rectangle.width / 2 + BALL_RADIUS + 1)
        else:
            ball.setx(rectangle.xcor() - rectangle.width / 2 - BALL_RADIUS - 1)
    else:
        ball.bounce_y()

        if distance_y > 0:
            ball.sety(rectangle.ycor() + rectangle.height / 2 + BALL_RADIUS + 1)
        else:
            ball.sety(rectangle.ycor() - rectangle.height / 2 - BALL_RADIUS - 1)


# -----------------------------
# Build the game screen
# -----------------------------
screen = Screen()
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.title("Breakout")
screen.tracer(0)

paddle = Paddle()
ball = Ball()
scoreboard = Scoreboard()

bricks = []
score = 0
lives = STARTING_LIVES
playing = False
game_finished = False


# -----------------------------
# Game setup functions
# -----------------------------
def create_bricks():
    """Creates the wall of bricks and returns it as a list."""
    new_bricks = []
    colors = ["red", "orange", "yellow", "green", "cyan"]

    total_width = BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP
    start_x = -total_width / 2 + BRICK_WIDTH / 2

    for row in range(BRICK_ROWS):
        y = BRICK_START_Y - row * (BRICK_HEIGHT + BRICK_GAP)
        color = colors[row]
        points = (BRICK_ROWS - row) * 10

        for column in range(BRICK_COLUMNS):
            x = start_x + column * (BRICK_WIDTH + BRICK_GAP)
            brick = Brick(x, y, color, points)
            new_bricks.append(brick)

    return new_bricks


def restart_game():
    """Resets the whole game after winning or losing."""
    global bricks, score, lives, playing, game_finished

    for brick in bricks:
        brick.hideturtle()

    bricks = create_bricks()
    score = 0
    lives = STARTING_LIVES
    playing = False
    game_finished = False

    paddle.goto(0, PADDLE_Y)
    ball.reset_position(paddle.xcor())

    scoreboard.update_score(score, lives, len(bricks))
    scoreboard.show_message(
        "BREAKOUT\n\nPress SPACE to launch\nMove with Left/Right or A/D\nPress P to pause"
    )


def space_action():
    """Starts the ball, or restarts the game after win/loss."""
    global playing

    if game_finished:
        restart_game()
    elif not playing:
        playing = True
        scoreboard.clear_message()


def toggle_pause():
    """Pauses or resumes the game."""
    global playing

    if game_finished:
        return

    if playing:
        playing = False
        scoreboard.show_message("PAUSED\n\nPress P to resume")
    else:
        playing = True
        scoreboard.clear_message()


def lose_life():
    """Handles what happens when the ball falls below the paddle."""
    global lives, playing, game_finished

    lives -= 1
    playing = False
    ball.reset_position(paddle.xcor())
    scoreboard.update_score(score, lives, len(bricks))

    if lives > 0:
        scoreboard.show_message(f"Life lost!\n\nLives left: {lives}\nPress SPACE to continue")
    else:
        game_finished = True
        scoreboard.show_message(f"GAME OVER\n\nFinal Score: {score}\nPress SPACE to play again")


# -----------------------------
# Main game loop
# -----------------------------
def game_loop():
    global score, game_finished, playing

    if not game_finished:
        if not playing:
            # Keep the ball sitting on the paddle until the player launches it.
            ball.goto(paddle.xcor(), PADDLE_Y + PADDLE_HEIGHT / 2 + BALL_RADIUS + 8)
        else:
            ball.move()

            # Bounce off left and right walls
            if ball.xcor() >= SCREEN_WIDTH / 2 - BALL_RADIUS:
                ball.setx(SCREEN_WIDTH / 2 - BALL_RADIUS)
                ball.bounce_x()
            elif ball.xcor() <= -SCREEN_WIDTH / 2 + BALL_RADIUS:
                ball.setx(-SCREEN_WIDTH / 2 + BALL_RADIUS)
                ball.bounce_x()

            # Bounce off top wall
            if ball.ycor() >= SCREEN_HEIGHT / 2 - BALL_RADIUS:
                ball.sety(SCREEN_HEIGHT / 2 - BALL_RADIUS)
                ball.bounce_y()

            # Paddle collision
            if ball.y_move < 0 and ball_hits_rectangle(ball, paddle):
                ball.sety(PADDLE_Y + PADDLE_HEIGHT / 2 + BALL_RADIUS + 1)
                ball.y_move = abs(ball.y_move)

                # Change the x direction depending on where the ball hits the paddle.
                # Hitting the left side sends it left; hitting the right side sends it right.
                hit_position = (ball.xcor() - paddle.xcor()) / (paddle.width / 2)
                ball.x_move = clamp(hit_position * 7, -BALL_MAX_SPEED, BALL_MAX_SPEED)

                # Avoid a perfectly vertical ball that becomes too easy.
                if abs(ball.x_move) < 1:
                    ball.x_move = random.choice([-1.5, 1.5])

            # Brick collision
            for brick in bricks[:]:
                if ball_hits_rectangle(ball, brick):
                    bounce_ball_from_rectangle(ball, brick)
                    brick.hideturtle()
                    bricks.remove(brick)
                    score += brick.points
                    ball.speed_up()
                    scoreboard.update_score(score, lives, len(bricks))
                    break

            # Player wins when all bricks are gone
            if len(bricks) == 0:
                playing = False
                game_finished = True
                scoreboard.show_message(f"YOU WIN!\n\nFinal Score: {score}\nPress SPACE to play again")

            # Ball falls below the screen
            if ball.ycor() < -SCREEN_HEIGHT / 2 - BALL_RADIUS:
                lose_life()

    screen.update()
    screen.ontimer(game_loop, FRAME_DELAY)


# -----------------------------
# Keyboard controls
# -----------------------------
screen.listen()
screen.onkeypress(paddle.move_left, "Left")
screen.onkeypress(paddle.move_right, "Right")
screen.onkeypress(paddle.move_left, "a")
screen.onkeypress(paddle.move_left, "A")
screen.onkeypress(paddle.move_right, "d")
screen.onkeypress(paddle.move_right, "D")
screen.onkeypress(space_action, "space")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(toggle_pause, "P")

# Start the game
restart_game()
game_loop()
screen.mainloop()