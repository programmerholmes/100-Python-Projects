# Reflection

The goal was to make the Chrome dinosaur game play itself instead of pressing
the keys by hand. My first instinct was the literal reading of the brief — take
screenshots and look at the pixels in front of the dino — but that turned out to
be the hard, fragile path: the web version of the game lives on a busy page that
scrolls and shifts, the right screen coordinates change with the window, and a
bot driven by OS key-presses keeps losing keyboard focus. I spent a lot of effort
fighting those problems before stepping back.

The breakthrough was realizing I didn't need to *guess* the game from the
outside at all — the game already knows everything, so I could just ask it.
The Chrome dino game keeps a `Runner` object in the page with the current speed,
the dinosaur, and the list of obstacles and their exact positions. By driving the
game with Selenium I can read that state directly and call the game's own
jump/duck, which made the bot both simpler and far more reliable: no pixels, no
coordinates to calibrate, nothing that breaks when a window moves.

The two bugs that taught me the most were quiet ones. First, the live obstacles
weren't in the array I assumed (`obstacles`) but in `horizon.obstacles` — so my
loop "worked" but never saw anything and never jumped. Second, the game would
silently freeze because Chrome pauses a page's animation when its window isn't in
front; the fix was a Chrome flag plus telling the page it's always visible.
Both were cases where nothing errored — the program ran fine and just did
nothing — which is the kind of bug you only catch by checking the actual state
rather than trusting your assumptions.

My biggest takeaway is that the best automation usually comes from finding the
cleanest source of truth, not from brute-forcing the messy one. Pixels were the
messy surface; the game's own state was the clean truth underneath. If I did it
again I'd reach for that level first. A next improvement would be to look two
obstacles ahead so it can plan a jump-then-duck combo at the very highest speeds.
