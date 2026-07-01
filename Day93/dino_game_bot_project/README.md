# Dino Game Bot 🦖

Automatically plays the Chrome Dinosaur game — jumping over cacti and ducking
under birds — so you don't have to press the keys yourself.

## Run it

```bash
pip install -r requirements.txt
python dino_bot.py
```

That's it. A Chrome window opens on the game (https://elgoog.im/t-rex/) and the
dino starts playing on its own.

**Stop:** close the Chrome window, or press `Ctrl + C` in the terminal.

*(Optional: `python dino_bot.py 60` plays for 60 seconds and then stops — handy
for a quick demo.)*

## How it works

Selenium opens the game in a real Chrome window. Many times a second the script
reads the game's own state — the dinosaur, the current speed, and the position
of every obstacle on screen — and works out what's about to hit the dino. If a
cactus (or low bird) is close, it jumps; if a high bird is close, it ducks. The
look-ahead distance grows with the game's speed, so it keeps reacting in time as
the game gets faster.

Reading the game's real state (instead of trying to read screen pixels) is what
makes it reliable: there are no screen coordinates to calibrate and nothing
breaks if the window moves.

In testing it reached a score of **~29,000+** in a single run.

## Requirements

- Google Chrome installed.
- `selenium` (in `requirements.txt`). Selenium downloads the matching driver
  automatically the first time you run it.

## Files

```
dino_bot.py        the bot
requirements.txt   selenium
reflection.md      project notes
```
