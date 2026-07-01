from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from PIL import Image


@dataclass
class PaletteColor:
    """Stores one extracted colour from the image."""

    rgb: tuple[int, int, int]
    hex_code: str
    count: int
    percentage: float


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert an RGB tuple into a CSS-style HEX colour string."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def _prepare_image(image_path: str, max_size: int = 350) -> Image.Image:
    """
    Open the image, resize it for faster processing, and convert it to RGB.

    Resizing keeps the app quick even with large phone photos. The colour palette
    remains visually close to the original image because all major colours are
    still represented.
    """
    image = Image.open(image_path)

    # Respect phone-camera orientation data when possible.
    try:
        from PIL import ImageOps

        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    image.thumbnail((max_size, max_size))

    # If the image has transparency, place it on a white background first.
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        image = Image.alpha_composite(background, image.convert("RGBA"))

    return image.convert("RGB")


def extract_palette(
    image_path: str,
    number_of_colours: int = 10,
    bucket_size: int = 24,
    max_size: int = 350,
) -> list[PaletteColor]:
    """
    Extract the most common colours from an image.

    Exact pixel colours can be too specific because photos contain thousands of
    slightly different shades. To make a useful design palette, colours are
    grouped into buckets. For example, very similar blues are counted together.
    """
    image = _prepare_image(image_path, max_size=max_size)
    pixels = np.array(image)

    # Flatten from height x width x 3 into a long list of RGB pixels.
    flat_pixels = pixels.reshape(-1, 3)

    # Group similar colours together by rounding down to the nearest bucket.
    bucketed_pixels = (flat_pixels // bucket_size) * bucket_size

    # Use the middle of each bucket so the colour swatches look more natural.
    bucketed_pixels = np.clip(bucketed_pixels + bucket_size // 2, 0, 255)

    pixel_tuples: Iterable[tuple[int, int, int]] = map(tuple, bucketed_pixels.astype(int))
    colour_counts = Counter(pixel_tuples)

    total_pixels = len(flat_pixels)
    most_common = colour_counts.most_common(number_of_colours)

    palette: list[PaletteColor] = []
    for rgb, count in most_common:
        rgb_tuple = tuple(int(value) for value in rgb)
        palette.append(
            PaletteColor(
                rgb=rgb_tuple,
                hex_code=rgb_to_hex(rgb_tuple),
                count=count,
                percentage=round((count / total_pixels) * 100, 2),
            )
        )

    return palette
