# Space Invaders 👾

The classic arcade shoot-'em-up, built from scratch with Python's standard
**`turtle`** module — no external libraries or asset files needed.

## Run it

```bash
python space_invaders.py
```

A window opens with the title screen. Click the window so it has focus, then
press **Space** to begin.

## Controls

| Key | Action |
|-----|--------|
| ← / → (or A / D) | Move your ship left / right |
| Space | Shoot |

## The game

- **Shoot the fleet.** Clear every alien to advance to the next wave.
- **The aliens shoot back.** You have **3 lives**; after a hit you respawn with a
  brief moment of blinking invulnerability.
- **Barriers** give you cover — but your own shots, and the aliens' bombs, chew
  them away, and the descending fleet grinds through them too.
- **Endless, rising levels.** Each cleared wave brings a faster fleet that fires
  more often. The fleet also speeds up as you thin it out — that classic rising
  panic near the end of a wave.
- **Game over** if the aliens reach you or you run out of lives. Press **Space**
  to play again.
- **Retro sound effects** (on Windows) — short blips generated in code, so there
  are no sound files to ship. On other systems the game runs silently.

## How it works

It's one self-contained file, [space_invaders.py](space_invaders.py):

- A `turtle` `Screen` with animation batched via `tracer(0)` and a fixed ~60 FPS
  game loop, so everything moves smoothly.
- Ship, invader, bullet and bomb are registered as simple polygon shapes — no
  images.
- The alien fleet moves as a group: when any alien reaches a screen edge, the
  whole fleet drops a row and reverses (the classic march). Only the front alien
  in a column can drop a bomb.
- Collisions are fast bounding-box overlap checks between bullets, bombs, aliens
  and barrier blocks.
- Sound blips are tiny square waves synthesised into an in-memory WAV and played
  asynchronously with `winsound` (guarded so it never interrupts the game).

## Requirements

Just Python — `turtle` and `tkinter` ship with the standard install.
