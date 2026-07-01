# Image Colour Palette Generator

A Flask website that lets a user upload an image and extracts the top 10 most common colours from it.

## Features

- Upload an image through a web form
- Display the uploaded image
- Extract the top 10 colours using Pillow and NumPy
- Show HEX, RGB, and percentage values for every colour
- Click a HEX code to copy it
- Includes a JSON API route
- Uses a clean responsive design

## How to Run

Open a terminal inside this folder and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open this URL in your browser:

```text
http://127.0.0.1:5000
```

## API Route

You can also send a POST request to:

```text
/api/palette
```

The request should use form-data with an image field named:

```text
image
```

The API returns JSON with HEX values, RGB values, percentages, and pixel counts.

## How the Colour Extraction Works

The program opens the uploaded image with Pillow and resizes it so large photos process quickly. NumPy converts the image into an array of RGB pixel values. Similar colours are grouped together into colour buckets, and then the program counts the most common buckets. This gives a useful design palette instead of thousands of tiny colour variations.

## Notes

Uploaded images are saved in:

```text
static/uploads
```

This is fine for a school project. In a production app, old uploads should be cleaned up automatically and user uploads should be stored more carefully.
