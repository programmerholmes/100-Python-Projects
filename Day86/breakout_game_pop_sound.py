import os
import sys
import random

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

# ---------------------------------------------------------
# Optional Windows sound support.
# The earlier version used Windows notification sounds, which
# can feel harsh. This version creates tiny custom WAV files
# at startup and plays those instead. No downloads needed.
# ---------------------------------------------------------
try:
    import winsound
    import math
    import struct
    import tempfile
    import wave

    SOUND_AVAILABLE = True
except ImportError:
    winsound = None
    SOUND_AVAILABLE = False


SOUND_FILES = {}


def make_arcade_sound(file_path, notes, volume=0.22, sample_rate=44100):
    """
    Creates a small WAV file from simple sine-wave notes.

    notes should be a list of tuples:
        (frequency, duration_in_seconds)

    A short attack and fade-out are added so the sound feels like
    a soft arcade pop instead of a sharp computer notification.
    """
    samples = []

    for frequency, duration in notes:
        total_samples = int(sample_rate * duration)
        attack_samples = max(1, int(sample_rate * 0.006))
        release_samples = max(1, int(sample_rate * 0.025))

        for i in range(total_samples):
            t = i / sample_rate

            # Smooth fade in.
            if i < attack_samples:
                envelope = i / attack_samples
            # Smooth fade out.
            elif i > total_samples - release_samples:
                envelope = max(0, (total_samples - i) / release_samples)
            else:
                envelope = 1

            # Exponential decay gives it a pop/coin sound.
            decay = math.exp(-5 * (i / max(1, total_samples)))
            sample = math.sin(2 * math.pi * frequency * t) * envelope * decay
            samples.append(int(sample * volume * 32767))

    with wave.open(file_path, "w") as sound_file:
        sound_file.setnchannels(1)
        sound_file.setsampwidth(2)
        sound_file.setframerate(sample_rate)
        sound_file.writeframes(b"".join(struct.pack("<h", sample) for sample in samples))


def prepare_sound_files():
    """Creates the sound files used by the game."""
    if not SOUND_AVAILABLE:
        return {}

    sound_folder = os.path.join(tempfile.gettempdir(), "breakout_arcade_sounds")
    os.makedirs(sound_folder, exist_ok=True)

    sounds = {
        # Short bright pop for every brick hit.
        "brick": [(720, 0.035), (960, 0.055)],

        # Softer low pop for paddle hit.
        "paddle": [(380, 0.035), (520, 0.040)],

        # Tiny launch sound.
        "start": [(520, 0.045), (660, 0.045)],

        # Gentle descending sound for losing a life.
        "life": [(330, 0.080), (240, 0.100)],

        # Small victory arpeggio.
        "win": [(523, 0.070), (659, 0.070), (784, 0.080), (1046, 0.120)],

        # Softer game-over sound.
        "game_over": [(392, 0.090), (330, 0.100), (262, 0.130)],
    }

    created_files = {}

    try:
        for name, notes in sounds.items():
            file_path = os.path.join(sound_folder, f"{name}.wav")
            make_arcade_sound(file_path, notes)
            created_files[name] = file_path
    except OSError:
        return {}

    return created_files


if SOUND_AVAILABLE:
    SOUND_FILES = prepare_sound_files()
    SOUND_AVAILABLE = len(SOUND_FILES) > 0


# -----------------------------
# Game settings
# -----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_DELAY = 20  # 20 ms is about 50 FPS and is smoother for Turtle than 60 FPS.

PADDLE_WIDTH = 110
PADDLE_HEIGHT = 20
PADDLE_Y = -250
PADDLE_MOVE_DISTANCE = 45

BALL_RADIUS = 10
BALL_START_SPEED_X = 4
BALL_START_SPEED_Y = 5
BALL_MAX_SPEED = 7.5

BRICK_ROWS = 5
BRICK_COLUMNS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 22
BRICK_GAP = 10
BRICK_START_Y = 215

STARTING_LIVES = 3


# -----------------------------
# Helper functions
# -----------------------------
def clamp(value, minimum, maximum):
    """Keeps a value inside a minimum and maximum range."""
    return max(minimum, min(value, maximum))


def play_sound(sound_name):
    """Plays a custom arcade sound without slowing the game down."""
    if not sound_enabled or not SOUND_AVAILABLE:
        return

    sound_file = SOUND_FILES.get(sound_name)
    if sound_file is None:
        return

    try:
        winsound.PlaySound(
            sound_file,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )
    except RuntimeError:
        # If the sound file cannot be played, ignore it and keep the game running.
        pass


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
            self.x_move *= 1.01
        if abs(self.y_move) < BALL_MAX_SPEED:
            self.y_move *= 1.01


# -----------------------------
# Brick data class
# -----------------------------
class Brick:
    def __init__(self, x, y, color, points):
        self.x = x
        self.y = y
        self.color = color
        self.points = points
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.alive = True


# -----------------------------
# Brick manager class
# -----------------------------
class BrickManager:
    """
    Stores bricks as normal Python objects instead of making each brick a Turtle.
    This is much faster because the screen only has to update a few Turtle objects.
    """
    def __init__(self):
        self.drawer = Turtle()
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.speed("fastest")
        self.bricks = []

    def create_bricks(self):
        self.bricks = []
        colors = ["red", "orange", "yellow", "green", "cyan"]

        total_width = BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP
        start_x = -total_width / 2 + BRICK_WIDTH / 2

        for row in range(BRICK_ROWS):
            y = BRICK_START_Y - row * (BRICK_HEIGHT + BRICK_GAP)
            color = colors[row]
            points = (BRICK_ROWS - row) * 10

            for column in range(BRICK_COLUMNS):
                x = start_x + column * (BRICK_WIDTH + BRICK_GAP)
                self.bricks.append(Brick(x, y, color, points))

        self.draw_bricks()

    def draw_bricks(self):
        """Redraws the remaining bricks. This only runs after a brick is removed."""
        self.drawer.clear()
        self.drawer.setheading(0)

        for brick in self.bricks:
            if brick.alive:
                self.draw_one_brick(brick)

    def draw_one_brick(self, brick):
        left = brick.x - brick.width / 2
        bottom = brick.y - brick.height / 2

        self.drawer.penup()
        self.drawer.goto(left, bottom)
        self.drawer.color(brick.color)
        self.drawer.begin_fill()

        for _ in range(2):
            self.drawer.forward(brick.width)
            self.drawer.left(90)
            self.drawer.forward(brick.height)
            self.drawer.left(90)

        self.drawer.end_fill()

    def remove_brick(self, brick):
        brick.alive = False
        self.draw_bricks()

    def remaining_bricks(self):
        return sum(1 for brick in self.bricks if brick.alive)


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
        sound_text = "ON" if sound_enabled and SOUND_AVAILABLE else "OFF"
        self.score_writer.clear()
        self.score_writer.write(
            f"Score: {score}    Lives: {lives}    Bricks Left: {bricks_left}    Sound: {sound_text}",
            align="center",
            font=("Courier", 14, "normal"),
        )

    def show_message(self, message):
        self.message_writer.clear()
        self.message_writer.write(
            message,
            align="center",
            font=("Courier", 18, "bold"),
        )

    def clear_message(self):
        self.message_writer.clear()


# -----------------------------
# Collision helper functions
# -----------------------------
def ball_hits_rectangle(ball, rectangle_x, rectangle_y, rectangle_width, rectangle_height):
    """Checks whether the ball overlaps a rectangular object."""
    return (
        rectangle_x - rectangle_width / 2 - BALL_RADIUS
        <= ball.xcor()
        <= rectangle_x + rectangle_width / 2 + BALL_RADIUS
        and rectangle_y - rectangle_height / 2 - BALL_RADIUS
        <= ball.ycor()
        <= rectangle_y + rectangle_height / 2 + BALL_RADIUS
    )


def ball_hits_paddle(ball, paddle):
    return ball_hits_rectangle(
        ball,
        paddle.xcor(),
        paddle.ycor(),
        paddle.width,
        paddle.height,
    )


def ball_hits_brick(ball, brick):
    return brick.alive and ball_hits_rectangle(
        ball,
        brick.x,
        brick.y,
        brick.width,
        brick.height,
    )


def bounce_ball_from_rectangle(ball, rectangle_x, rectangle_y, rectangle_width, rectangle_height):
    """Bounces the ball from the correct side of a rectangle."""
    distance_x = ball.xcor() - rectangle_x
    distance_y = ball.ycor() - rectangle_y

    overlap_x = (rectangle_width / 2 + BALL_RADIUS) - abs(distance_x)
    overlap_y = (rectangle_height / 2 + BALL_RADIUS) - abs(distance_y)

    if overlap_x < overlap_y:
        ball.bounce_x()

        if distance_x > 0:
            ball.setx(rectangle_x + rectangle_width / 2 + BALL_RADIUS + 1)
        else:
            ball.setx(rectangle_x - rectangle_width / 2 - BALL_RADIUS - 1)
    else:
        ball.bounce_y()

        if distance_y > 0:
            ball.sety(rectangle_y + rectangle_height / 2 + BALL_RADIUS + 1)
        else:
            ball.sety(rectangle_y - rectangle_height / 2 - BALL_RADIUS - 1)


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
brick_manager = BrickManager()
scoreboard = Scoreboard()

score = 0
lives = STARTING_LIVES
playing = False
game_finished = False
sound_enabled = SOUND_AVAILABLE


# -----------------------------
# Game setup functions
# -----------------------------
def restart_game():
    """Resets the whole game after winning or losing."""
    global score, lives, playing, game_finished

    brick_manager.create_bricks()
    score = 0
    lives = STARTING_LIVES
    playing = False
    game_finished = False

    paddle.goto(0, PADDLE_Y)
    ball.reset_position(paddle.xcor())

    scoreboard.update_score(score, lives, brick_manager.remaining_bricks())
    scoreboard.show_message(
        "BREAKOUT\n\nPress SPACE to launch\nMove with Left/Right or A/D\nPress P to pause\nPress S to turn sound on/off"
    )


def space_action():
    """Starts the ball, or restarts the game after win/loss."""
    global playing

    if game_finished:
        restart_game()
    elif not playing:
        playing = True
        scoreboard.clear_message()
        play_sound("start")


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


def toggle_sound():
    """Turns sound on or off."""
    global sound_enabled

    if not SOUND_AVAILABLE:
        sound_enabled = False
    else:
        sound_enabled = not sound_enabled

    scoreboard.update_score(score, lives, brick_manager.remaining_bricks())


def lose_life():
    """Handles what happens when the ball falls below the paddle."""
    global lives, playing, game_finished

    lives -= 1
    playing = False
    ball.reset_position(paddle.xcor())
    scoreboard.update_score(score, lives, brick_manager.remaining_bricks())

    if lives > 0:
        play_sound("life")
        scoreboard.show_message(f"Life lost!\n\nLives left: {lives}\nPress SPACE to continue")
    else:
        game_finished = True
        play_sound("game_over")
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
            if ball.y_move < 0 and ball_hits_paddle(ball, paddle):
                ball.sety(PADDLE_Y + PADDLE_HEIGHT / 2 + BALL_RADIUS + 1)
                ball.y_move = abs(ball.y_move)

                # Change the x direction depending on where the ball hits the paddle.
                hit_position = (ball.xcor() - paddle.xcor()) / (paddle.width / 2)
                ball.x_move = clamp(hit_position * 7, -BALL_MAX_SPEED, BALL_MAX_SPEED)

                # Avoid a perfectly vertical ball.
                if abs(ball.x_move) < 1:
                    ball.x_move = random.choice([-1.5, 1.5])

                play_sound("paddle")

            # Brick collision
            for brick in brick_manager.bricks:
                if ball_hits_brick(ball, brick):
                    bounce_ball_from_rectangle(ball, brick.x, brick.y, brick.width, brick.height)
                    brick_manager.remove_brick(brick)
                    score += brick.points
                    ball.speed_up()
                    scoreboard.update_score(score, lives, brick_manager.remaining_bricks())
                    play_sound("brick")
                    break

            # Player wins when all bricks are gone
            if brick_manager.remaining_bricks() == 0:
                playing = False
                game_finished = True
                play_sound("win")
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
screen.onkeypress(toggle_sound, "s")
screen.onkeypress(toggle_sound, "S")

# Start the game
restart_game()
game_loop()
screen.mainloop()
