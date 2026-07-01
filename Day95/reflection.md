# Reflection

The brief was open-ended: pick a public API I find interesting and build a
website around it. I chose the PokéAPI because it's free, needs no API key, is
very reliable, and returns rich, visual data (official artwork, types, stats) —
which makes for a website that actually looks good, not just a wall of JSON.

I approached it by separating the two concerns: *getting the data* and *showing
it*. The data side is a single `get_pokemon()` function that calls the API,
handles the "not found" and network-error cases, and tidies the raw JSON into a
clean dictionary — converting the API's odd units (decimetres and hectograms)
into metres and kilograms, picking the official artwork out of the nested
`sprites` object, and giving the stats human-readable labels. Keeping all that
messiness in one place made the Flask routes and the template simple.

The easiest part was Flask routing — one page that optionally takes a `?name=`
query. The most fiddly part was reading the API's shape: the useful bits are
buried (artwork is at `sprites.other["official-artwork"].front_default`, and the
description isn't on the main endpoint at all — it's on a separate
`pokemon-species` endpoint). Reading the docs and poking at the JSON was most of
the work. Styling everything by the Pokémon's *type colour* was a small touch
that made the whole thing feel finished.

My biggest takeaway is that working with someone else's API is mostly about
*understanding and reshaping their data* into what your UI needs, and about
handling the unhappy paths (bad input, a request that fails) so the site stays
friendly instead of throwing a 500. Fetch, normalise, render — with the "what if
it fails?" question asked at every step.

I later added three touches that pushed it from "works" to "polished": in-memory
caching (so a repeat lookup drops from ~1s to ~10ms), name autocomplete via an
HTML datalist built from the full Pokémon list, and a full evolution chain. The
evolution chain was the most instructive — it meant *chaining* API calls
(pokemon → species → evolution-chain) and flattening the API's nested,
sometimes-branching tree (Eevee has eight evolutions) into something a template
can render. A neat trick was deriving each evolution's artwork URL straight from
its species id, which avoided an extra network call per stage.

If I did it again I'd persist the cache to disk (so it survives restarts) and add
a Pokémon-type filter or a "compare two Pokémon" view.
