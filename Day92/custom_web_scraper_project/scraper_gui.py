"""
Optional Tkinter GUI for the Custom Web Scraper project.
Run with:
    python scraper_gui.py
"""

from __future__ import annotations

import os
import sys
import threading
from pathlib import Path


def configure_tcl_tk_paths() -> None:
    """
    Helps Tkinter find Tcl/Tk on some Windows + PyCharm setups.

    The command-line scraper does not need this, but the optional GUI uses
    Tkinter. If Python is launched from a virtual environment, Tkinter can
    sometimes search the wrong folder for init.tcl. This function points it
    back to the Tcl/Tk folders that ship with the main Python installation.
    """
    possible_roots = [
        sys.base_prefix,
        sys.prefix,
        os.path.dirname(os.path.dirname(sys.executable)),
    ]

    for root in possible_roots:
        tcl_library = os.path.join(root, "tcl", "tcl8.6")
        tk_library = os.path.join(root, "tcl", "tk8.6")

        if os.path.exists(os.path.join(tcl_library, "init.tcl")):
            os.environ["TCL_LIBRARY"] = tcl_library

            if os.path.exists(os.path.join(tk_library, "tk.tcl")):
                os.environ["TK_LIBRARY"] = tk_library

            return


configure_tcl_tk_paths()

import tkinter as tk
from tkinter import filedialog, messagebox

from scraper import ScraperError, scrape_books


class ScraperApp:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.window.title("Custom Web Scraper")
        self.window.geometry("650x520")
        self.window.config(padx=20, pady=20)

        self.output_path = tk.StringVar(value="data/books.csv")
        self.pages = tk.IntVar(value=3)
        self.delay = tk.DoubleVar(value=0.5)
        self.include_details = tk.BooleanVar(value=False)

        self.build_layout()

    def build_layout(self) -> None:
        title = tk.Label(
            self.window,
            text="Books to Scrape CSV Generator",
            font=("Helvetica", 20, "bold"),
        )
        title.pack(pady=(0, 8))

        subtitle = tk.Label(
            self.window,
            text="Scrape book titles, prices, ratings, availability, and links into a CSV file.",
            font=("Helvetica", 11),
            wraplength=580,
        )
        subtitle.pack(pady=(0, 18))

        form = tk.Frame(self.window)
        form.pack(fill="x")

        tk.Label(form, text="Pages to scrape:", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        tk.Spinbox(form, from_=1, to=50, textvariable=self.pages, width=10).grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(form, text="Delay between requests:", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        tk.Spinbox(form, from_=0.1, to=5.0, increment=0.1, textvariable=self.delay, width=10).grid(row=1, column=1, sticky="w", pady=6)

        tk.Checkbutton(
            form,
            text="Include detail pages (slower, more data)",
            variable=self.include_details,
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=6)

        tk.Label(form, text="Output CSV:", anchor="w").grid(row=3, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=self.output_path, width=45).grid(row=3, column=1, sticky="w", pady=6)
        tk.Button(form, text="Browse", command=self.choose_output).grid(row=3, column=2, padx=8, pady=6)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=16)

        self.start_button = tk.Button(
            button_frame,
            text="Start Scraping",
            command=self.start_scraping,
            width=18,
            font=("Helvetica", 11, "bold"),
        )
        self.start_button.grid(row=0, column=0, padx=8)

        tk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            width=12,
        ).grid(row=0, column=1, padx=8)

        self.log_box = tk.Text(self.window, height=16, wrap="word")
        self.log_box.pack(fill="both", expand=True)
        self.log("Ready. Click Start Scraping to create your CSV file.")

    def choose_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )

        if filename:
            self.output_path.set(filename)

    def log(self, message: str) -> None:
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def clear_log(self) -> None:
        self.log_box.delete("1.0", "end")

    def start_scraping(self) -> None:
        if self.pages.get() < 1:
            messagebox.showerror("Invalid input", "Pages must be at least 1.")
            return

        self.start_button.config(state="disabled")
        self.log("Starting scraper...")

        worker = threading.Thread(target=self.run_scraper, daemon=True)
        worker.start()

    def run_scraper(self) -> None:
        try:
            books = scrape_books(
                max_pages=self.pages.get(),
                output_path=Path(self.output_path.get()),
                include_details=self.include_details.get(),
                delay=self.delay.get(),
            )
            self.window.after(0, lambda: self.finish_success(len(books)))
        except (ScraperError, ValueError, OSError) as error:
            self.window.after(0, lambda: self.finish_error(str(error)))

    def finish_success(self, count: int) -> None:
        self.log(f"Finished. Saved {count} books to {self.output_path.get()}")
        messagebox.showinfo("Done", f"Scraping finished. Saved {count} books.")
        self.start_button.config(state="normal")

    def finish_error(self, error_message: str) -> None:
        self.log(f"Error: {error_message}")
        messagebox.showerror("Scraper error", error_message)
        self.start_button.config(state="normal")


def main() -> None:
    window = tk.Tk()
    ScraperApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
