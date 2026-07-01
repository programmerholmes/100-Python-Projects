# Custom Web Scraper Project

This project scrapes book data from [Books to Scrape](https://books.toscrape.com/) and saves the results into a CSV file.

Books to Scrape is a practice website designed for scraping projects, which makes it a good choice for a class assignment.

## What the scraper collects

The basic scraper collects:

- Book title
- Price
- Star rating
- Availability
- Book detail URL
- Image URL

If you use the `--details` option, it also collects:

- Category
- UPC
- Number of reviews
- Description

## Project files

```text
custom_web_scraper_project/
├── scraper.py
├── scraper_gui.py
├── requirements.txt
├── README.md
├── reflection.md
├── run_windows.bat
└── data/
```

## Setup

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run the command-line scraper

Scrape the first 3 pages:

```bash
python scraper.py
```

Scrape the first 5 pages:

```bash
python scraper.py --pages 5
```

Save to a custom CSV file:

```bash
python scraper.py --pages 5 --output data/my_books.csv
```

Collect extra information from each book's detail page:

```bash
python scraper.py --pages 2 --details
```

## Run the GUI version

```bash
python scraper_gui.py
```

The GUI lets you choose how many pages to scrape, where to save the CSV file, and whether to include detail page data.

## Output

The default CSV file is saved here:

```text
data/books.csv
```

You can open the CSV file in Excel, Google Sheets, or any text editor.

## Important scraping notes

This project includes a small delay between requests so it does not send too many requests too quickly. For real-world websites, always check the website's terms of service and robots.txt file before scraping.

## Troubleshooting

If you see an import error, install the requirements again:

```bash
python -m pip install -r requirements.txt
```

If no data is saved, check your internet connection and make sure the website is accessible.
