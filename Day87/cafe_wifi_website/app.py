from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "cafes.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-for-production"

FEATURES = {
    "has_wifi": "WiFi",
    "has_sockets": "Sockets",
    "has_toilet": "Toilets",
    "can_take_calls": "Call-friendly",
}

REQUIRED_FIELDS = ["name", "map_url", "img_url", "location"]


def get_db_connection() -> sqlite3.Connection:
    """Open a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    """Convert a database row into a normal dictionary."""
    cafe = dict(row)
    for field in FEATURES:
        cafe[field] = bool(cafe[field])
    return cafe


def bool_value(value: Any) -> int:
    """Convert checkbox, form, or JSON values into 1 or 0."""
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int):
        return 1 if value else 0
    if value is None:
        return 0
    return 1 if str(value).strip().lower() in {"1", "true", "yes", "y", "on"} else 0


def form_text(name: str) -> str:
    """Get a clean text value from a submitted form."""
    return request.form.get(name, "").strip()


def get_cafe_or_404(cafe_id: int) -> sqlite3.Row:
    """Return one cafe row or raise a 404 error."""
    with get_db_connection() as connection:
        cafe = connection.execute("SELECT * FROM cafe WHERE id = ?", (cafe_id,)).fetchone()

    if cafe is None:
        abort(404)

    return cafe


def get_locations() -> list[str]:
    """Return all unique cafe locations."""
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT location FROM cafe ORDER BY location COLLATE NOCASE"
        ).fetchall()
    return [row["location"] for row in rows]


def get_stats() -> dict[str, int]:
    """Return summary numbers for the homepage."""
    with get_db_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(has_wifi) AS wifi,
                SUM(has_sockets) AS sockets,
                SUM(has_toilet) AS toilets,
                SUM(can_take_calls) AS calls
            FROM cafe
            """
        ).fetchone()

    return {
        "total": row["total"] or 0,
        "wifi": row["wifi"] or 0,
        "sockets": row["sockets"] or 0,
        "toilets": row["toilets"] or 0,
        "calls": row["calls"] or 0,
    }


def build_search_query(args) -> tuple[str, list[Any]]:
    """Build a safe SQL query for search and filters."""
    sql = "SELECT * FROM cafe WHERE 1 = 1"
    params: list[Any] = []

    search = args.get("q", "").strip()
    location = args.get("location", "").strip()

    if search:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(location) LIKE ?)"
        search_value = f"%{search.lower()}%"
        params.extend([search_value, search_value])

    if location:
        sql += " AND location = ?"
        params.append(location)

    for field in FEATURES:
        if args.get(field) == "1":
            sql += f" AND {field} = 1"

    sql += " ORDER BY name COLLATE NOCASE"
    return sql, params


def read_cafe_form() -> tuple[dict[str, Any], list[str]]:
    """Read and validate data from the add/edit form."""
    data = {
        "name": form_text("name"),
        "map_url": form_text("map_url"),
        "img_url": form_text("img_url"),
        "location": form_text("location"),
        "seats": form_text("seats"),
        "coffee_price": form_text("coffee_price"),
        "has_wifi": bool_value(request.form.get("has_wifi")),
        "has_sockets": bool_value(request.form.get("has_sockets")),
        "has_toilet": bool_value(request.form.get("has_toilet")),
        "can_take_calls": bool_value(request.form.get("can_take_calls")),
    }

    errors = []
    for field in REQUIRED_FIELDS:
        if not data[field]:
            errors.append(f"{field.replace('_', ' ').title()} is required.")

    for field in ["map_url", "img_url"]:
        value = data[field]
        if value and not (value.startswith("http://") or value.startswith("https://")):
            errors.append(f"{field.replace('_', ' ').title()} should start with http:// or https://.")

    return data, errors


def insert_cafe(data: dict[str, Any]) -> int:
    """Insert a cafe and return its new id."""
    with get_db_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO cafe
            (name, map_url, img_url, location, has_sockets, has_toilet,
             has_wifi, can_take_calls, seats, coffee_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["name"],
                data["map_url"],
                data["img_url"],
                data["location"],
                data["has_sockets"],
                data["has_toilet"],
                data["has_wifi"],
                data["can_take_calls"],
                data["seats"],
                data["coffee_price"],
            ),
        )
        connection.commit()
        return cursor.lastrowid


@app.route("/")
def home():
    """Show all cafes with search and filtering."""
    sql, params = build_search_query(request.args)

    with get_db_connection() as connection:
        rows = connection.execute(sql, params).fetchall()

    cafes = [row_to_dict(row) for row in rows]
    active_filters = {field: request.args.get(field) == "1" for field in FEATURES}

    return render_template(
        "index.html",
        cafes=cafes,
        features=FEATURES,
        stats=get_stats(),
        locations=get_locations(),
        search_text=request.args.get("q", ""),
        selected_location=request.args.get("location", ""),
        active_filters=active_filters,
    )


@app.route("/cafe/<int:cafe_id>")
def cafe_detail(cafe_id: int):
    """Show one cafe in detail."""
    cafe = row_to_dict(get_cafe_or_404(cafe_id))
    return render_template("detail.html", cafe=cafe, features=FEATURES)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    """Add a cafe using a web form."""
    if request.method == "POST":
        data, errors = read_cafe_form()

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("form.html", cafe=data, features=FEATURES, mode="add"), 400

        try:
            new_id = insert_cafe(data)
        except sqlite3.IntegrityError:
            flash("A cafe with that name already exists.", "danger")
            return render_template("form.html", cafe=data, features=FEATURES, mode="add"), 409

        flash(f"{data['name']} was added successfully.", "success")
        return redirect(url_for("cafe_detail", cafe_id=new_id))

    empty_cafe = {
        "name": "",
        "map_url": "",
        "img_url": "",
        "location": "",
        "seats": "",
        "coffee_price": "",
        "has_wifi": False,
        "has_sockets": False,
        "has_toilet": False,
        "can_take_calls": False,
    }
    return render_template("form.html", cafe=empty_cafe, features=FEATURES, mode="add")


@app.route("/edit/<int:cafe_id>", methods=["GET", "POST"])
def edit_cafe(cafe_id: int):
    """Edit an existing cafe."""
    cafe = row_to_dict(get_cafe_or_404(cafe_id))

    if request.method == "POST":
        data, errors = read_cafe_form()
        data["id"] = cafe_id

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("form.html", cafe=data, features=FEATURES, mode="edit"), 400

        try:
            with get_db_connection() as connection:
                connection.execute(
                    """
                    UPDATE cafe
                    SET name = ?, map_url = ?, img_url = ?, location = ?,
                        has_sockets = ?, has_toilet = ?, has_wifi = ?,
                        can_take_calls = ?, seats = ?, coffee_price = ?
                    WHERE id = ?
                    """,
                    (
                        data["name"],
                        data["map_url"],
                        data["img_url"],
                        data["location"],
                        data["has_sockets"],
                        data["has_toilet"],
                        data["has_wifi"],
                        data["can_take_calls"],
                        data["seats"],
                        data["coffee_price"],
                        cafe_id,
                    ),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            flash("Another cafe already uses that name.", "danger")
            return render_template("form.html", cafe=data, features=FEATURES, mode="edit"), 409

        flash(f"{data['name']} was updated successfully.", "success")
        return redirect(url_for("cafe_detail", cafe_id=cafe_id))

    return render_template("form.html", cafe=cafe, features=FEATURES, mode="edit")


@app.route("/delete/<int:cafe_id>", methods=["POST"])
def delete_cafe(cafe_id: int):
    """Delete a cafe from the website."""
    cafe = row_to_dict(get_cafe_or_404(cafe_id))

    with get_db_connection() as connection:
        connection.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
        connection.commit()

    flash(f"{cafe['name']} was deleted.", "warning")
    return redirect(url_for("home"))


@app.route("/api-docs")
def api_docs():
    """Show a small API guide page."""
    return render_template("api_docs.html")


@app.route("/api/cafes", methods=["GET"])
def api_get_cafes():
    """Return cafes as JSON. Query parameters can filter the results."""
    sql, params = build_search_query(request.args)
    with get_db_connection() as connection:
        rows = connection.execute(sql, params).fetchall()
    cafes = [row_to_dict(row) for row in rows]
    return jsonify(count=len(cafes), cafes=cafes)


@app.route("/api/cafes/<int:cafe_id>", methods=["GET"])
def api_get_cafe(cafe_id: int):
    """Return one cafe as JSON."""
    cafe = row_to_dict(get_cafe_or_404(cafe_id))
    return jsonify(cafe=cafe)


@app.route("/api/random", methods=["GET"])
def api_random_cafe():
    """Return one random cafe as JSON."""
    with get_db_connection() as connection:
        cafe = connection.execute("SELECT * FROM cafe ORDER BY RANDOM() LIMIT 1").fetchone()

    if cafe is None:
        return jsonify(error="No cafes found."), 404

    return jsonify(cafe=row_to_dict(cafe))


@app.route("/api/search", methods=["GET"])
def api_search():
    """Search cafes by location, for example /api/search?location=Peckham."""
    location = request.args.get("location", "").strip()

    if not location:
        return jsonify(error="Please provide a location query parameter."), 400

    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM cafe WHERE LOWER(location) LIKE ? ORDER BY name COLLATE NOCASE",
            (f"%{location.lower()}%",),
        ).fetchall()

    cafes = [row_to_dict(row) for row in rows]

    if not cafes:
        return jsonify(error="No cafes were found for that location."), 404

    return jsonify(count=len(cafes), cafes=cafes)


@app.route("/api/cafes", methods=["POST"])
def api_add_cafe():
    """Add a cafe using JSON or form data."""
    payload = request.get_json(silent=True) or request.form.to_dict()
    data = {
        "name": str(payload.get("name", "")).strip(),
        "map_url": str(payload.get("map_url", "")).strip(),
        "img_url": str(payload.get("img_url", "")).strip(),
        "location": str(payload.get("location", "")).strip(),
        "seats": str(payload.get("seats", "")).strip(),
        "coffee_price": str(payload.get("coffee_price", "")).strip(),
        "has_wifi": bool_value(payload.get("has_wifi")),
        "has_sockets": bool_value(payload.get("has_sockets")),
        "has_toilet": bool_value(payload.get("has_toilet")),
        "can_take_calls": bool_value(payload.get("can_take_calls")),
    }

    missing = [field for field in REQUIRED_FIELDS if not data[field]]
    if missing:
        return jsonify(error=f"Missing required fields: {', '.join(missing)}"), 400

    try:
        new_id = insert_cafe(data)
    except sqlite3.IntegrityError:
        return jsonify(error="A cafe with that name already exists."), 409

    cafe = row_to_dict(get_cafe_or_404(new_id))
    return jsonify(message="Cafe added successfully.", cafe=cafe), 201


@app.route("/api/cafes/<int:cafe_id>", methods=["DELETE"])
def api_delete_cafe(cafe_id: int):
    """Delete one cafe using the API."""
    cafe = row_to_dict(get_cafe_or_404(cafe_id))

    with get_db_connection() as connection:
        connection.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
        connection.commit()

    return jsonify(message=f"{cafe['name']} was deleted successfully.")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
