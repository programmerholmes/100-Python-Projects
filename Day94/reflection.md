# Reflection

This project was a change of pace from the last one: instead of automating an
existing game, I had to *build* one from nothing using Python's `turtle` module.
I approached it by splitting the game into its pieces — the player ship, the
bullets, the alien fleet, the barriers — getting each working on its own, and
then wiring them together in a single game loop. Once the core played well, I
built it up into a full arcade version: aliens that shoot back, three lives,
endless rising levels, and sound.

The easiest part was the player: a turtle that moves left/right and fires. The
part that took the most thought was making it feel smooth. Turtle redraws slowly
if you animate every little step, so the key was `tracer(0)` plus a single manual
`update()` per frame in a fixed ~60 FPS loop, and tracking which keys are *held*
rather than moving one step per key press.

The alien fleet was the most interesting logic. The classic behaviour — march
sideways, and when the group hits an edge, drop a row and reverse — is a property
of the *whole fleet*, so I check whether *any* alien would cross the edge and then
move them all together. Letting only the front alien in a column drop a bomb, and
speeding the march up as the fleet thins and as levels climb, brought back that
trademark rising tension.

Two things surprised me with how simple they turned out to be. Collisions are
just bounding-box overlap checks — no need for anything fancier. And I got real
arcade sound with **no sound files**: I synthesise a short square-wave blip into
an in-memory WAV and play it asynchronously, so it never stalls the game loop and
degrades gracefully to silence on non-Windows machines.

My biggest takeaway is how far small, clear ideas go when they're composed in a
tidy loop — read input, move things, check collisions, redraw. Structuring the
game as "play a session of rising levels until you die" made lives and levels
fall out naturally. If I did it again I'd add an object pool for aliens and
barrier blocks so restarts don't rebuild them, and maybe a high-score file so
your best run persists between sessions.
