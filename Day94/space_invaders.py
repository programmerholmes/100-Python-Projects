"""
Space Invaders  (Python Turtle)
===============================
The classic shoot-'em-up, built with Python's standard `turtle` module.

Features:
    * Move your ship and shoot the alien fleet.
    * The aliens shoot back -- you have 3 lives.
    * Barriers give you cover (they wear down from shots on both sides).
    * Endless, rising levels: clear the fleet and the next wave is faster and
      fires more. See how far you can get.
    * Retro sound effects (Windows) -- generated in code, no sound files needed.

Controls:
    Left / Right arrows (or A / D) : move
    Spacebar                       : shoot
    Space on the title / game-over screen : start / play again

Run it:
    python space_invaders.py

Needs nothing but Python itself (turtle + tkinter ship with Python).
"""

import io
import math
import os
import random
import struct
import sys
import time
import wave


def _ensure_tcl():
    """Make turtle's Tcl/Tk backend findable before importing turtle.

    Some virtualenvs (including the kind PyCharm creates) don't expose Tcl's
    data files, so `import turtle` fails with "Can't find a usable init.tcl".
    Pointing at the base Python installation's Tcl/Tk folders fixes that.
    """
    tcl_root = os.path.join(sys.base_prefix, "tcl")
    if not os.path.isdir(tcl_root):
        return
    for name in sorted(os.listdir(tcl_root)):
        path = os.path.join(tcl_root, name)
        if name.startswith("tcl8") and os.path.isfile(os.path.join(path, "init.tcl")):
            os.environ.setdefault("TCL_LIBRARY", path)
        elif name.startswith("tk8") and os.path.isdir(path):
            os.environ.setdefault("TK_LIBRARY", path)


_ensure_tcl()

import turtle  # noqa: E402  -- imported after Tcl/Tk paths are set above

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 680
PLAYER_Y = -300
PLAYER_SPEED = 8
X_LIMIT = WIDTH // 2 - 30
START_LIVES = 3
RESPAWN_INVULN = 1.6          # seconds of blinking safety after being hit

BULLET_SPEED = 13
FIRE_COOLDOWN = 0.35
MAX_BULLETS = 5

BOMB_SPEED = 7                # alien shots (fall downward)
MAX_BOMBS = 6

ALIEN_ROWS, ALIEN_COLS = 5, 8
ALIEN_X_GAP, ALIEN_Y_GAP = 70, 44
ALIEN_TOP = 235
ALIEN_STEP = 14
ALIEN_DROP = 26
ALIEN_EDGE = WIDTH // 2 - 40
ALIEN_ROW_COLORS = ["#ff4d4d", "#ff9f43", "#feca57", "#1dd1a1", "#54a0ff"]

BARRIER_COUNT = 4
BARRIER_COLS, BARRIER_BLOCK_ROWS = 5, 3
BLOCK = 16
BARRIER_Y = -145          # a bit higher up, so barriers aren't crowding the ship

FRAME = 1 / 60

SHIP_SHAPE =((-20, -10), (20, -10), (20, -4), (6, -4), (6, 2), (3, 2),
              (3, 10), (-3, 10), (-3, 2), (-6, 2), (-6, -4), (-20, -4))
INVADER_SHAPE = ((-14, -4), (-14, 2), (-10, 2), (-10, 8), (-4, 8), (-4, 2),
                 (4, 2), (4, 8), (10, 8), (10, 2), (14, 2), (14, -4),
                 (10, -4), (10, -10), (4, -10), (4, -4), (-4, -4),
                 (-4, -10), (-10, -10), (-10, -4))
BULLET_SHAPE = ((-2, -9), (2, -9), (2, 9), (-2, 9))
BOMB_SHAPE = ((-2, -8), (2, -8), (2, 8), (-2, 8))


# ---------------------------------------------------------------------------
# Sound  (tiny square-wave blips generated in memory; Windows only, optional)
# ---------------------------------------------------------------------------
SOUND_ON = sys.platform.startswith("win")
try:
    import winsound
except Exception:
    SOUND_ON = False

_SOUNDS = {}


def _make_wav(freq, ms, volume=0.3):
    rate = 16000
    n = int(rate * ms / 1000)
    frames = bytearray()
    for i in range(n):
        val = volume if math.sin(2 * math.pi * freq * (i / rate)) >= 0 else -volume
        val *= 1 - i / n                      # fade out to avoid a click
        frames += struct.pack("<h", int(val * 32767))
    buf = io.BytesIO()
    w = wave.open(buf, "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(frames); w.close()
    return buf.getvalue()


def init_sounds():
    if not SOUND_ON:
        return
    try:
        _SOUNDS["shoot"] = _make_wav(880, 55)
        _SOUNDS["hit"] = _make_wav(200, 90)
        _SOUNDS["player"] = _make_wav(130, 300)
        _SOUNDS["level"] = _make_wav(660, 220)
    except Exception:
        pass


def play(name):
    if not SOUND_ON:
        return
    data = _SOUNDS.get(name)
    if not data:
        return
    try:
        winsound.PlaySound(data, winsound.SND_MEMORY | winsound.SND_ASYNC)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Screen + input
# ---------------------------------------------------------------------------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)
def _upright(shape):
    # Turtle renders a registered polygon rotated 90 deg from its coordinates,
    # so rotate the points to make each shape appear the way it's defined (facing up).
    return tuple((-y, x) for x, y in shape)


screen.register_shape("ship", _upright(SHIP_SHAPE))
screen.register_shape("invader", _upright(INVADER_SHAPE))
screen.register_shape("bullet", _upright(BULLET_SHAPE))
screen.register_shape("bomb", _upright(BOMB_SHAPE))

held = {"left": False, "right": False}


def make_turtle(shape, color):
    t = turtle.Turtle()
    t.shape(shape)
    t.color(color)
    t.penup()
    return t


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------
player = make_turtle("ship", "#6bf178")
player.goto(0, PLAYER_Y)

hud = turtle.Turtle()
hud.hideturtle(); hud.penup(); hud.color("white")

aliens = []
bullets, bullet_pool = [], []      # player shots
bombs, bomb_pool = [], []          # alien shots
blocks = []                        # barrier blocks
TOTAL_ALIENS = ALIEN_ROWS * ALIEN_COLS


def build_aliens():
    for a in aliens:
        a.hideturtle()
    aliens.clear()
    start_x = -((ALIEN_COLS - 1) / 2) * ALIEN_X_GAP
    for row in range(ALIEN_ROWS):
        for col in range(ALIEN_COLS):
            a = make_turtle("invader", ALIEN_ROW_COLORS[row % len(ALIEN_ROW_COLORS)])
            a.goto(start_x + col * ALIEN_X_GAP, ALIEN_TOP - row * ALIEN_Y_GAP)
            a.points = 10 + (ALIEN_ROWS - 1 - row) * 5
            aliens.append(a)


def build_barriers():
    for b in blocks:
        b.hideturtle()
    blocks.clear()
    spacing = WIDTH / (BARRIER_COUNT + 1)
    for i in range(BARRIER_COUNT):
        cx = -WIDTH / 2 + spacing * (i + 1)
        for col in range(BARRIER_COLS):
            for row in range(BARRIER_BLOCK_ROWS):
                blk = make_turtle("square", "#43d17a")
                blk.shapesize(BLOCK / 20, BLOCK / 20)
                blk.goto(cx + (col - (BARRIER_COLS - 1) / 2) * BLOCK,
                         BARRIER_Y - row * BLOCK)
                blocks.append(blk)


def clear_shots():
    while bullets:
        _retire(bullets[0], bullets, bullet_pool)
    while bombs:
        _retire(bombs[0], bombs, bomb_pool)


# ---------------------------------------------------------------------------
# Shots
# ---------------------------------------------------------------------------
_last_fire = 0.0


def fire():
    global _last_fire
    now = time.time()
    if now - _last_fire < FIRE_COOLDOWN or len(bullets) >= MAX_BULLETS:
        return
    _last_fire = now
    b = bullet_pool.pop() if bullet_pool else make_turtle("bullet", "#f5f36b")
    b.goto(player.xcor(), player.ycor() + 12)
    b.showturtle()
    bullets.append(b)
    play("shoot")


def alien_fire(level):
    if not aliens or len(bombs) >= MAX_BOMBS:
        return
    if random.random() >= min(0.05, 0.010 + 0.010 * level):
        return
    # only the front (lowest) alien in a randomly chosen column shoots
    columns = {}
    for a in aliens:
        key = round(a.xcor() / 10)
        if key not in columns or a.ycor() < columns[key].ycor():
            columns[key] = a
    shooter = random.choice(list(columns.values()))
    bomb = bomb_pool.pop() if bomb_pool else make_turtle("bomb", "#ff6b6b")
    bomb.goto(shooter.xcor(), shooter.ycor() - 14)
    bomb.showturtle()
    bombs.append(bomb)


def _retire(t, active, pool):
    t.hideturtle()
    active.remove(t)
    pool.append(t)


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
def bind_play_keys():
    for key in ("Left", "a"):
        screen.onkeypress(lambda: held.update(left=True), key)
        screen.onkeyrelease(lambda: held.update(left=False), key)
    for key in ("Right", "d"):
        screen.onkeypress(lambda: held.update(right=True), key)
        screen.onkeyrelease(lambda: held.update(right=False), key)
    screen.onkeypress(fire, "space")
    screen.listen()


def hit(a, b, dx, dy):
    return abs(a.xcor() - b.xcor()) < dx and abs(a.ycor() - b.ycor()) < dy


def draw_hud(game):
    hud.clear()
    hud.goto(-WIDTH / 2 + 20, HEIGHT / 2 - 35)
    hud.write(f"Score: {game['score']}    Lives: {game['lives']}    "
              f"Level: {game['level']}    Aliens: {len(aliens)}",
              font=("Courier", 15, "bold"))


# ---------------------------------------------------------------------------
# A full session: play levels until the player dies. Returns "dead" or "quit".
# ---------------------------------------------------------------------------
def play_session():
    game = {"score": 0, "lives": START_LIVES, "level": 1}
    build_aliens()
    build_barriers()
    clear_shots()
    player.goto(0, PLAYER_Y)
    player.showturtle()
    held["left"] = held["right"] = False

    fleet_dir = 1
    march_timer = 0.0
    wall_hits = 0
    invuln_until = time.time() + RESPAWN_INVULN
    draw_hud(game)
    bind_play_keys()
    last = time.time()

    while True:
        now = time.time()
        dt = now - last
        last = now

        # --- player movement ---
        if held["left"] and player.xcor() > -X_LIMIT:
            player.setx(player.xcor() - PLAYER_SPEED)
        if held["right"] and player.xcor() < X_LIMIT:
            player.setx(player.xcor() + PLAYER_SPEED)

        # --- blink while briefly invulnerable, otherwise stay visible ---
        safe = now < invuln_until
        player.showturtle() if not safe else (
            player.showturtle() if int(now * 10) % 2 else player.hideturtle())

        # --- player bullets: move, then hit aliens / barriers ---
        for b in list(bullets):
            b.sety(b.ycor() + BULLET_SPEED)
            if b.ycor() > HEIGHT / 2:
                _retire(b, bullets, bullet_pool)
                continue
            struck = False
            for a in list(aliens):
                if hit(b, a, 22, 16):
                    game["score"] += a.points
                    a.hideturtle(); aliens.remove(a)
                    _retire(b, bullets, bullet_pool)
                    play("hit"); draw_hud(game)
                    struck = True
                    break
            if struck:
                continue
            for blk in list(blocks):
                if hit(b, blk, 10, 10):
                    blk.hideturtle(); blocks.remove(blk)
                    _retire(b, bullets, bullet_pool)
                    break

        # --- alien bombs: spawn, move, then hit player / barriers ---
        alien_fire(game["level"])
        for bomb in list(bombs):
            bomb.sety(bomb.ycor() - BOMB_SPEED)
            if bomb.ycor() < -HEIGHT / 2:
                _retire(bomb, bombs, bomb_pool)
                continue
            if not safe and hit(bomb, player, 20, 18):
                _retire(bomb, bombs, bomb_pool)
                game["lives"] -= 1
                play("player"); draw_hud(game)
                if game["lives"] <= 0:
                    return "dead", game
                invuln_until = now + RESPAWN_INVULN
                player.goto(0, PLAYER_Y)
                continue
            for blk in list(blocks):
                if hit(bomb, blk, 10, 10):
                    blk.hideturtle(); blocks.remove(blk)
                    _retire(bomb, bombs, bomb_pool)
                    break

        # --- fleet march (faster as the fleet thins and as levels rise) ---
        if aliens:
            march_timer += dt
            base = max(0.11, 0.5 - (game["level"] - 1) * 0.06)
            if march_timer >= 0.06 + base * (len(aliens) / TOTAL_ALIENS):
                march_timer = 0.0
                at_edge = any(
                    not (-ALIEN_EDGE <= a.xcor() + fleet_dir * ALIEN_STEP <= ALIEN_EDGE)
                    for a in aliens)
                if at_edge:
                    fleet_dir *= -1
                    wall_hits += 1
                    if wall_hits % 2 == 0:        # drop only every 2nd wall hit
                        for a in aliens:
                            a.sety(a.ycor() - ALIEN_DROP)
                else:
                    for a in aliens:
                        a.setx(a.xcor() + fleet_dir * ALIEN_STEP)
                for a in aliens:                      # aliens grind down barriers
                    for blk in list(blocks):
                        if hit(a, blk, 20, 16):
                            blk.hideturtle(); blocks.remove(blk)
                if min(a.ycor() for a in aliens) <= PLAYER_Y + 24:
                    return "dead", game               # they reached you

        # --- level cleared -> next wave ---
        if not aliens:
            game["level"] += 1
            play("level")
            if not level_flash(game["level"]):
                return "quit", game
            build_aliens(); build_barriers(); clear_shots()
            player.goto(0, PLAYER_Y)
            fleet_dir = 1; march_timer = 0.0; wall_hits = 0
            invuln_until = time.time() + RESPAWN_INVULN
            draw_hud(game)
            bind_play_keys()
            last = time.time()
            continue

        try:
            screen.update()
        except turtle.Terminator:
            return "quit", game
        time.sleep(max(0, FRAME - (time.time() - now)))


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------
def banner(lines, color):
    hud.clear()
    y = 70
    for i, (text, size) in enumerate(lines):
        hud.color(color if i == 0 else "white")
        hud.goto(0, y)
        hud.write(text, align="center", font=("Courier", size, "bold"))
        y -= size + 18
    hud.color("white")


def level_flash(level):
    """Show 'LEVEL n' for a beat. Returns False if the window was closed."""
    banner([(f"LEVEL {level}", 34)], "#feca57")
    end = time.time() + 1.1
    while time.time() < end:
        try:
            screen.update()
        except turtle.Terminator:
            return False
        time.sleep(0.03)
    hud.clear()
    return True


def wait_for(*keys):
    chosen = {"key": None}
    for prev in ("Left", "Right", "a", "d", "space"):
        screen.onkeypress(None, prev)
        screen.onkeyrelease(None, prev)
    for k in keys:
        screen.onkey((lambda kk=k: chosen.update(key=kk)), k)
    screen.listen()
    while chosen["key"] is None:
        try:
            screen.update()
        except turtle.Terminator:
            return None
        time.sleep(0.05)
    return chosen["key"]


def start_screen():
    banner([("SPACE INVADERS", 34),
            ("Arrow keys move  -  Space shoots", 16),
            ("You have 3 lives.  Clear each wave to level up.", 14),
            ("Press SPACE to start", 18)], "#54a0ff")
    return wait_for("space") is not None


def end_screen(game):
    banner([("GAME OVER", 40),
            (f"Level {game['level']}    Score {game['score']}", 18),
            ("Press SPACE to play again", 16)], "#ff4d4d")
    return wait_for("space") is not None


# ---------------------------------------------------------------------------
def main():
    init_sounds()
    if not start_screen():
        return
    while True:
        outcome, game = play_session()
        if outcome == "quit":
            break
        if not end_screen(game):
            break
    try:
        screen.bye()
    except turtle.Terminator:
        pass


if __name__ == "__main__":
    main()
