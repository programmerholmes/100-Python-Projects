from __future__ import annotations

import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from color_tools import extract_palette


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "gif"}
MAX_FILE_SIZE_MB = 8

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE_MB * 1024 * 1024

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Return True only for supported image file extensions."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(uploaded_file) -> tuple[bool, str, str | None]:
    """
    Validate and save an uploaded image.

    Returns: success, message_or_filename, original_filename
    """
    if uploaded_file is None or uploaded_file.filename == "":
        return False, "Please choose an image file first.", None

    original_filename = secure_filename(uploaded_file.filename)

    if not allowed_file(original_filename):
        return False, "Unsupported file type. Please upload PNG, JPG, JPEG, WEBP, BMP, or GIF.", None

    extension = original_filename.rsplit(".", 1)[1].lower()
    saved_filename = f"{uuid.uuid4().hex}.{extension}"
    saved_path = UPLOAD_FOLDER / saved_filename
    uploaded_file.save(saved_path)

    return True, saved_filename, original_filename


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", palette=None, image_url=None, error=None)


@app.route("/upload", methods=["POST"])
def upload_image():
    success, result, original_filename = save_uploaded_image(request.files.get("image"))

    if not success:
        return render_template("index.html", palette=None, image_url=None, error=result)

    saved_filename = result
    saved_path = UPLOAD_FOLDER / saved_filename

    try:
        palette = extract_palette(str(saved_path), number_of_colours=10)
    except Exception as error:
        try:
            saved_path.unlink(missing_ok=True)
        except Exception:
            pass
        return render_template(
            "index.html",
            palette=None,
            image_url=None,
            error=f"The image could not be processed: {error}",
        )

    image_url = url_for("static", filename=f"uploads/{saved_filename}")
    return render_template(
        "index.html",
        palette=palette,
        image_url=image_url,
        error=None,
        original_filename=original_filename,
    )


@app.route("/api/palette", methods=["POST"])
def palette_api():
    """JSON API version of the colour palette extractor."""
    success, result, original_filename = save_uploaded_image(request.files.get("image"))

    if not success:
        return jsonify({"success": False, "error": result}), 400

    saved_filename = result
    saved_path = UPLOAD_FOLDER / saved_filename

    try:
        palette = extract_palette(str(saved_path), number_of_colours=10)
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500

    colours = [
        {
            "rank": index + 1,
            "hex": colour.hex_code,
            "rgb": colour.rgb,
            "percentage": colour.percentage,
            "pixel_count": colour.count,
        }
        for index, colour in enumerate(palette)
    ]

    return jsonify(
        {
            "success": True,
            "filename": original_filename,
            "image_url": url_for("static", filename=f"uploads/{saved_filename}"),
            "colours": colours,
        }
    )


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        palette=None,
        image_url=None,
        error=f"That image is too large. Please upload a file under {MAX_FILE_SIZE_MB} MB.",
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
