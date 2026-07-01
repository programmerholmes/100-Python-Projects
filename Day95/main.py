"""
Pokedex -- a Flask website powered by the free PokeAPI (https://pokeapi.co).

Search for any Pokemon by name or number and the site shows its official
artwork, types, height/weight, abilities, base stats, a short description and
its full evolution chain -- all fetched live from a public REST API. No API key
required. Responses are cached in memory, so repeat lookups are instant, and the
search box has name autocomplete.

Run it:
    python main.py
Then it opens http://127.0.0.1:5000 in your browser automatically.

Needs: flask, requests   (pip install -r requirements.txt)
"""

import os
import random
import threading
import webbrowser

import requests
from flask import Flask, redirect, render_template, request, url_for

API = "https://pokeapi.co/api/v2"
ARTWORK = ("https://raw.githubusercontent.com/PokeAPI/sprites/master/"
           "sprites/pokemon/other/official-artwork/{id}.png")
MAX_DEX = 1025            # highest Pokemon id currently in the API

app = Flask(__name__)

# Official Pokemon type colours, used for the coloured type badges.
TYPE_COLORS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0",
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6",
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65",
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC",
    "dark": "#705746", "steel": "#B7B7CE", "fairy": "#D685AD",
}
STAT_LABELS = {
    "hp": "HP", "attack": "Attack", "defense": "Defense",
    "special-attack": "Sp. Atk", "special-defense": "Sp. Def", "speed": "Speed",
}

# ---------------------------------------------------------------------------
# Cached HTTP helper: every successful response is kept in memory, so looking
# up the same Pokemon (or a shared evolution) again doesn't re-hit the network.
# ---------------------------------------------------------------------------
_CACHE = {}


def fetch_json(url):
    """GET `url` and return parsed JSON (cached). Returns None on a 404."""
    if url in _CACHE:
        return _CACHE[url]
    resp = requests.get(url, timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    _CACHE[url] = resp.json()
    return _CACHE[url]


def _id_from_url(url):
    """'.../pokemon-species/6/' -> 6"""
    return int(url.rstrip("/").split("/")[-1])


def evolution_levels(chain):
    """Turn the nested evolution-chain tree into a list of levels (each a list
    of Pokemon), so a linear line renders left-to-right and a branching one
    (e.g. Eevee) stacks the options. Artwork is built from the species id, so no
    extra API calls are needed per stage."""
    levels = []
    current = [chain]
    while current:
        level = []
        for node in current:
            slug = node["species"]["name"]
            sid = _id_from_url(node["species"]["url"])
            level.append({
                "slug": slug,
                "name": slug.replace("-", " ").title(),
                "image": ARTWORK.format(id=sid),
            })
        levels.append(level)
        nxt = []
        for node in current:
            nxt.extend(node["evolves_to"])
        current = nxt
    return levels


def get_pokemon(query):
    """Fetch and tidy one Pokemon. Returns (pokemon_dict, error_message)."""
    query = query.strip().lower()
    if not query:
        return None, None
    try:
        data = fetch_json(f"{API}/pokemon/{query}")
    except requests.RequestException:
        return None, "Couldn't reach PokeAPI - please check your internet connection."
    if data is None:
        return None, f"No Pokemon found for “{query}”. Try another name or number."

    sprites = data["sprites"]
    image = sprites["other"]["official-artwork"]["front_default"] or sprites["front_default"]

    # A description and the evolution chain live on the "species" endpoint.
    flavor, evolution = "", []
    try:
        species = fetch_json(data["species"]["url"])
        if species:
            for entry in species.get("flavor_text_entries", []):
                if entry["language"]["name"] == "en":
                    flavor = entry["flavor_text"].replace("\n", " ").replace("\f", " ").strip()
                    break
            evo_url = (species.get("evolution_chain") or {}).get("url")
            if evo_url:
                evo = fetch_json(evo_url)
                if evo:
                    evolution = evolution_levels(evo["chain"])
    except requests.RequestException:
        pass

    pokemon = {
        "id": data["id"],
        "slug": data["name"],
        "name": data["name"].replace("-", " ").title(),
        "image": image,
        "types": [t["type"]["name"] for t in data["types"]],
        "height": data["height"] / 10,     # decimetres -> metres
        "weight": data["weight"] / 10,     # hectograms -> kilograms
        "abilities": [a["ability"]["name"].replace("-", " ").title() for a in data["abilities"]],
        "stats": [
            {"name": STAT_LABELS.get(s["stat"]["name"], s["stat"]["name"]), "value": s["base_stat"]}
            for s in data["stats"]
        ],
        "flavor": flavor,
        "evolution": evolution,
    }
    return pokemon, None


def all_pokemon_names():
    """All Pokemon names, for the search box autocomplete (fetched once, cached)."""
    try:
        data = fetch_json(f"{API}/pokemon?limit=100000")
        return sorted(p["name"] for p in data["results"])
    except requests.RequestException:
        return []


@app.route("/")
def index():
    query = request.args.get("name", "").strip()
    pokemon, error = (None, None)
    if query:
        pokemon, error = get_pokemon(query)
    return render_template(
        "index.html", pokemon=pokemon, error=error, query=query,
        type_colors=TYPE_COLORS, names=all_pokemon_names(),
    )


@app.route("/random")
def random_pokemon():
    return redirect(url_for("index", name=random.randint(1, MAX_DEX)))


def _open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Open the browser once, only in the main process (not the reloader child).
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.0, _open_browser).start()
    app.run(debug=True)
