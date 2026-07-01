# Pokédex 🔴 — an API-powered website

A small **Flask** website that lets you search any Pokémon and see its details,
pulled live from the free public **[PokéAPI](https://pokeapi.co)** — no API key
needed.

Search by name or number and you get the Pokémon's official artwork, its
type(s), a short description, height, weight, abilities, and base-stat bars —
all styled in the colours of its primary type.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

It starts a local server and opens **http://127.0.0.1:5000** in your browser
automatically. Stop it with `Ctrl + C`.

## Features

- 🔎 Search any Pokémon by **name** or **number** (`pikachu`, `25`, `charizard`…).
- ⌨️ **Autocomplete** — the search box suggests from every Pokémon name.
- 🎲 **Surprise me** button that jumps to a random Pokémon.
- 🎨 Type-coloured badges, card accent, and stat bars.
- 📊 Base stats shown as proportional bars (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed).
- 🧬 **Evolution chain** — each stage is clickable, and branching lines (e.g. Eevee) are handled.
- 🖼️ Official artwork + a short Pokédex description.
- ⚡ **Caching** — responses are kept in memory, so repeat lookups are instant.
- 🙂 Friendly message when a name/number isn't found.

## How it works

- `main.py` is the Flask app. When you search, `get_pokemon()` calls
  `GET .../pokemon/<name>`, tidies the JSON (converts the API's
  decimetres/hectograms to metres/kilograms, picks the official artwork, labels
  the stats), then follows the linked **`pokemon-species`** endpoint for a
  description and the **`evolution-chain`** endpoint for the evolution line —
  a small example of chaining several API calls together.
- Every request goes through `fetch_json()`, which **caches** successful
  responses in memory, so re-looking-up a Pokémon (or a shared evolution) is
  instant instead of re-hitting the network.
- The full list of names (`.../pokemon?limit=…`) is fetched once and rendered
  into an HTML `<datalist>`, giving the search box native **autocomplete**.
- The result is rendered by `templates/index.html` (Bootstrap 5 + a little custom
  CSS in `static/style.css`), which colours everything by the Pokémon's type.
- Bad input and network errors are caught and shown as a friendly notice instead
  of crashing.

## Files

```
main.py                the Flask app + PokéAPI calls
templates/index.html   the page
static/style.css       styling (type colours, stat bars, card)
requirements.txt       flask, requests
reflection.md          project notes
```

## Requirements

Python with `flask` and `requests` (see `requirements.txt`), and an internet
connection (the data — and Bootstrap's CSS — load from the web).
