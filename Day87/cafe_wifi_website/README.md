# Cafe & WiFi Finder

A Flask + SQLite website that displays laptop-friendly cafes from the provided `cafes.db` database.

## Features

- Displays all cafes in a responsive Bootstrap card layout.
- Search by cafe name or location.
- Filter by WiFi, sockets, toilets, and call-friendly cafes.
- View individual cafe detail pages.
- Add new cafes through a form.
- Edit existing cafes.
- Delete cafes.
- Includes a small REST-style JSON API.
- Includes basic 404 and 500 error pages.

## Project structure

```text
cafe_wifi_website/
├── app.py
├── cafes.db
├── requirements.txt
├── run_windows.bat
├── README.md
├── reflection.md
├── static/
│   ├── css/
│   │   └── styles.css
│   └── img/
│       └── cafe-placeholder.svg
└── templates/
    ├── 404.html
    ├── 500.html
    ├── api_docs.html
    ├── base.html
    ├── detail.html
    ├── form.html
    └── index.html
```

## How to run

Open a terminal inside the project folder and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open this address in your browser:

```text
http://127.0.0.1:5000
```

On Windows, you can also double-click `run_windows.bat` from the project folder.

## Useful website routes

```text
/                 homepage with all cafes
/add              add a new cafe
/cafe/<id>        cafe detail page
/edit/<id>        edit a cafe
/api-docs         API documentation page
```

## API routes

```text
GET     /api/cafes
GET     /api/cafes/<id>
GET     /api/random
GET     /api/search?location=Peckham
POST    /api/cafes
DELETE  /api/cafes/<id>
```

The website uses the original SQLite table:

```text
cafe(id, name, map_url, img_url, location, has_sockets, has_toilet,
     has_wifi, can_take_calls, seats, coffee_price)
```
