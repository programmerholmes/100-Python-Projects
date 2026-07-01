"""
Dino Game Bot
=============
Automatically plays the Chrome Dinosaur game (https://elgoog.im/t-rex/).

When you run this file it opens the game in a Chrome window and plays it on its
own -- jumping over cacti and ducking under birds -- instead of you pressing the
keys. It does this by reading the game's own state (where every obstacle is and
how fast the game is going) and reacting at the right moment.

Run it:
    python dino_bot.py

Stop it:
    Close the Chrome window, or press Ctrl + C in the terminal.

Needs:  selenium  (pip install -r requirements.txt)  and Google Chrome installed.
Selenium downloads the matching driver automatically the first time.
"""

import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

GAME_URL = "https://elgoog.im/t-rex/"

# One snippet of JavaScript reads everything the bot needs in a single call:
# whether we're playing, the current speed, the dino's pose, and the list of
# obstacles on screen (each with its position, size and type).
READ_STATE = """
const R = window.Runner && Runner.instance_;
if (!R) return null;
return {
    playing:   R.playing,
    crashed:   R.crashed,
    speed:     R.currentSpeed,
    score:     Math.floor(R.distanceRan || 0),
    dinoRight: R.tRex.xPos + 44,          // right edge of the dinosaur
    jumping:   R.tRex.jumping,
    obstacles: R.horizon.obstacles.map(o => ({
        x: o.xPos, y: o.yPos, w: o.width, type: o.typeConfig.type
    })),
};
"""


def make_driver():
    """Launch a Chrome window set up so the game keeps running smoothly."""
    options = Options()
    options.add_argument("--start-maximized")
    # Keep the game's animation loop running even when the window isn't focused.
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-features=CalculateNativeWinOcclusion")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    return webdriver.Chrome(options=options)


def load_game(driver):
    """(Re)load the game page and get it ready for a fresh run.

    We reload the page for every new life instead of calling the game's own
    restart(): an in-place restart leaves the game in a subtly degraded state
    where the timing drifts and the dino keeps dying early, whereas a clean page
    load behaves perfectly every time.
    """
    driver.get(GAME_URL)
    for _ in range(100):  # wait up to ~10s for the game object to load
        if driver.execute_script("return !!(window.Runner && Runner.instance_);"):
            break
        time.sleep(0.1)
    # Tell the page it is always visible, so the game never pauses itself.
    driver.execute_script(
        "Object.defineProperty(document,'hidden',{get:()=>false,configurable:true});"
        "Object.defineProperty(document,'visibilityState',{get:()=>'visible',configurable:true});"
    )
    # A Space key event "activates" and begins the game from its start screen.
    driver.execute_script(
        "for (const el of [document, window]) el.dispatchEvent("
        "new KeyboardEvent('keydown',{code:'Space',keyCode:32,which:32,bubbles:true}));"
    )


def main():
    run_seconds = float(sys.argv[1]) if len(sys.argv) > 1 else None  # optional: stop after N s

    print("Opening the dino game...")
    driver = make_driver()
    load_game(driver)

    jump = lambda: driver.execute_script("Runner.instance_.tRex.startJump(Runner.instance_.currentSpeed);")
    duck = lambda on: driver.execute_script("Runner.instance_.tRex.setDuck(arguments[0]);", on)

    print("Bot is playing! Close the window or press Ctrl+C to stop.")

    ducking = False
    best = 0
    started = time.time()

    try:
        while True:
            if run_seconds and time.time() - started >= run_seconds:
                break

            state = driver.execute_script(READ_STATE)
            if not state:
                time.sleep(0.05)
                continue

            best = max(best, state["score"])

            if state["crashed"]:
                # Reload for a clean slate (see load_game) and play on.
                ducking = False
                load_game(driver)
                continue

            speed = state["speed"]
            dino_right = state["dinoRight"]
            # How far ahead (in game units) to react. The faster the game, the
            # earlier we must act, so the look-ahead grows with the speed.
            reach = speed * 9 + 12

            # Find the closest obstacle that is still in front of the dino.
            nearest = None
            for o in state["obstacles"]:
                if o["x"] + o["w"] < dino_right:      # already behind us
                    continue
                if nearest is None or o["x"] < nearest["x"]:
                    nearest = o

            if nearest and (nearest["x"] - dino_right) <= reach:
                is_bird = "PTERODACTYL" in (nearest["type"] or "")
                if is_bird and nearest["y"] <= 60:    # a high bird -> duck under it
                    if not ducking:
                        duck(True); ducking = True
                else:                                  # cactus or low bird -> jump over it
                    if ducking:
                        duck(False); ducking = False
                    if not state["jumping"]:
                        jump()
            elif ducking:
                duck(False); ducking = False

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    except WebDriverException:
        print("Browser was closed.")
    finally:
        print(f"\nBest score this run: {best}")
        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()
