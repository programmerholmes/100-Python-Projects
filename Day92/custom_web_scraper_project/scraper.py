"""
Custom Web Scraper Project
--------------------------
This program scrapes book information from Books to Scrape and saves the
results into a CSV file.

Website used:
https://books.toscrape.com/

Books to Scrape is a practice website made for web scraping projects.
"""

from __future__ import annotations

import argparse
import csv
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
DEFAULT_OUTPUT = Path("data/books.csv")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


@dataclass
class Book:
    """Stores one scraped book record."""

    title: str
    price_gbp: str
    rating: int
    availability: str
    detail_url: str
    image_url: str
    category: str = ""
    upc: str = ""
    number_of_reviews: str = ""
    description: str = ""


class ScraperError(Exception):
    """Custom error used when scraping fails."""


# Books to Scrape uses words inside CSS classes, e.g. class="star-rating Three".
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def fetch_page(url: str, timeout: int = 15) -> BeautifulSoup:
    """Downloads a web page and returns BeautifulSoup parsed HTML."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ScraperError(f"Could not download page: {url}\n{error}") from error

    return BeautifulSoup(response.text, "html.parser")


def get_rating(card: BeautifulSoup) -> int:
    """Converts the book rating class into a number from 1 to 5."""
    rating_tag = card.select_one("p.star-rating")

    if not rating_tag:
        return 0

    for class_name in rating_tag.get("class", []):
        if class_name in RATING_MAP:
            return RATING_MAP[class_name]

    return 0


def clean_text(text: str) -> str:
    """Normalizes whitespace."""
    return " ".join(text.split())


def parse_book_card(card: BeautifulSoup, page_url: str) -> Book:
    """Extracts basic book information from one product card."""
    title_tag = card.select_one("h3 a")
    price_tag = card.select_one("p.price_color")
    availability_tag = card.select_one("p.instock.availability")
    image_tag = card.select_one("img")

    title = title_tag.get("title", "").strip() if title_tag else "Unknown Title"
    detail_url = urljoin(page_url, title_tag.get("href", "")) if title_tag else ""
    image_url = urljoin(page_url, image_tag.get("src", "")) if image_tag else ""

    price = price_tag.get_text(strip=True).replace("Â", "") if price_tag else ""
    availability = clean_text(availability_tag.get_text(" ", strip=True)) if availability_tag else ""
    rating = get_rating(card)

    return Book(
        title=title,
        price_gbp=price,
        rating=rating,
        availability=availability,
        detail_url=detail_url,
        image_url=image_url,
    )


def parse_detail_page(book: Book, delay: float = 0.25) -> Book:
    """Visits a book detail page and adds extra fields."""
    time.sleep(delay)
    soup = fetch_page(book.detail_url)

    # Category is usually the second-to-last breadcrumb before the book title.
    breadcrumb_links = soup.select("ul.breadcrumb li a")
    if len(breadcrumb_links) >= 3:
        book.category = breadcrumb_links[-1].get_text(strip=True)

    # Product information table contains UPC and reviews.
    table_rows = soup.select("table.table.table-striped tr")
    product_info = {}

    for row in table_rows:
        heading = row.select_one("th")
        value = row.select_one("td")
        if heading and value:
            product_info[heading.get_text(strip=True)] = value.get_text(strip=True)

    book.upc = product_info.get("UPC", "")
    book.number_of_reviews = product_info.get("Number of reviews", "")

    description_heading = soup.find("div", id="product_description")
    if description_heading:
        description_paragraph = description_heading.find_next_sibling("p")
        if description_paragraph:
            book.description = clean_text(description_paragraph.get_text(" ", strip=True))

    return book


def get_next_page_url(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """Finds the URL of the next listing page, if one exists."""
    next_link = soup.select_one("li.next a")
    if not next_link:
        return None

    return urljoin(current_url, next_link.get("href", ""))


def scrape_books(
    max_pages: int = 3,
    output_path: Path = DEFAULT_OUTPUT,
    include_details: bool = False,
    delay: float = 0.5,
    start_url: str = BASE_URL,
) -> list[Book]:
    """Scrapes book data and saves it into a CSV file."""
    if max_pages < 1:
        raise ValueError("max_pages must be at least 1")

    books: list[Book] = []
    current_url: Optional[str] = start_url
    page_count = 0

    while current_url and page_count < max_pages:
        page_count += 1
        print(f"Scraping page {page_count}: {current_url}")

        soup = fetch_page(current_url)
        book_cards = soup.select("article.product_pod")

        if not book_cards:
            print("No book cards found on this page.")
            break

        for card in book_cards:
            book = parse_book_card(card, current_url)

            if include_details and book.detail_url:
                book = parse_detail_page(book, delay=delay)

            books.append(book)

        current_url = get_next_page_url(soup, current_url)
        time.sleep(delay)

    save_to_csv(books, output_path)
    return books


def save_to_csv(books: list[Book], output_path: Path) -> None:
    """Saves the scraped book records into a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(asdict(Book("", "", 0, "", "", "")).keys())

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            writer.writerow(asdict(book))

    print(f"\nSaved {len(books)} books to {output_path}")


def build_parser() -> argparse.ArgumentParser:
    """Creates the command-line argument parser."""
    parser = argparse.ArgumentParser(description="Scrape book data and save it to CSV.")

    parser.add_argument(
        "--pages",
        type=int,
        default=3,
        help="Number of listing pages to scrape. Default: 3",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="CSV output file path. Default: data/books.csv",
    )

    parser.add_argument(
        "--details",
        action="store_true",
        help="Also visit each book's detail page for category, UPC, reviews, and description.",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds. Default: 0.5",
    )

    parser.add_argument(
        "--start-url",
        default=BASE_URL,
        help="Starting URL. Default: https://books.toscrape.com/",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        scrape_books(
            max_pages=args.pages,
            output_path=args.output,
            include_details=args.details,
            delay=args.delay,
            start_url=args.start_url,
        )
    except (ScraperError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
