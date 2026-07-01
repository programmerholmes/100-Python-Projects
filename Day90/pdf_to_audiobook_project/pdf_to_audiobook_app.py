"""
Desktop GUI version of the PDF to Audiobook project.

The app lets the user choose a PDF file, choose an output file, select a TTS
mode, and convert the PDF into an audiobook.
"""

import os
import sys
import threading
from pathlib import Path


# Tkinter/Turtle path helper for some Windows/PyCharm Python installs.
def configure_tcl_tk_paths():
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
from tkinter import filedialog, messagebox, ttk

from pdf_tools import AudiobookError, convert_pdf_to_audiobook


class PdfToAudiobookApp:
    def __init__(self, window):
        self.window = window
        self.window.title("PDF to Audiobook Converter")
        self.window.geometry("820x640")
        self.window.minsize(760, 560)

        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.engine = tk.StringVar(value="gtts")
        self.language = tk.StringVar(value="en")
        self.rate = tk.IntVar(value=170)
        self.start_page = tk.StringVar()
        self.end_page = tk.StringVar()
        self.save_text = tk.BooleanVar(value=True)

        self.build_layout()

    def build_layout(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="PDF to Audiobook Converter",
            font=("Helvetica", 22, "bold"),
        )
        title_label.pack(anchor="w")

        subtitle_label = ttk.Label(
            main_frame,
            text="Choose a PDF, extract its text, and convert it into an MP3 or WAV audiobook.",
            font=("Helvetica", 11),
        )
        subtitle_label.pack(anchor="w", pady=(4, 16))

        file_frame = ttk.LabelFrame(main_frame, text="Files", padding=12)
        file_frame.pack(fill="x", pady=8)
        file_frame.columnconfigure(1, weight=1)

        ttk.Label(file_frame, text="PDF file:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(file_frame, textvariable=self.pdf_path).grid(row=0, column=1, sticky="ew", pady=4)
        ttk.Button(file_frame, text="Browse", command=self.choose_pdf).grid(row=0, column=2, padx=(8, 0), pady=4)

        ttk.Label(file_frame, text="Output file:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
        ttk.Entry(file_frame, textvariable=self.output_path).grid(row=1, column=1, sticky="ew", pady=4)
        ttk.Button(file_frame, text="Save As", command=self.choose_output).grid(row=1, column=2, padx=(8, 0), pady=4)

        options_frame = ttk.LabelFrame(main_frame, text="Options", padding=12)
        options_frame.pack(fill="x", pady=8)

        ttk.Label(options_frame, text="TTS engine:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=5)
        engine_box = ttk.Combobox(
            options_frame,
            textvariable=self.engine,
            values=["gtts", "pyttsx3"],
            state="readonly",
            width=14,
        )
        engine_box.grid(row=0, column=1, sticky="w", pady=5)
        engine_box.bind("<<ComboboxSelected>>", self.engine_changed)

        ttk.Label(options_frame, text="gTTS language:").grid(row=0, column=2, sticky="w", padx=(25, 8), pady=5)
        ttk.Entry(options_frame, textvariable=self.language, width=10).grid(row=0, column=3, sticky="w", pady=5)

        ttk.Label(options_frame, text="Offline rate:").grid(row=0, column=4, sticky="w", padx=(25, 8), pady=5)
        ttk.Spinbox(options_frame, from_=100, to=250, textvariable=self.rate, width=8).grid(row=0, column=5, sticky="w", pady=5)

        ttk.Label(options_frame, text="Start page:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(options_frame, textvariable=self.start_page, width=10).grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(options_frame, text="End page:").grid(row=1, column=2, sticky="w", padx=(25, 8), pady=5)
        ttk.Entry(options_frame, textvariable=self.end_page, width=10).grid(row=1, column=3, sticky="w", pady=5)

        ttk.Checkbutton(
            options_frame,
            text="Save extracted text as .txt file",
            variable=self.save_text,
        ).grid(row=1, column=4, columnspan=2, sticky="w", padx=(25, 0), pady=5)

        explanation = (
            "gtts: online MP3, needs internet, no API key.    "
            "pyttsx3: offline WAV, uses voices installed on your computer."
        )
        ttk.Label(options_frame, text=explanation, foreground="#555555").grid(
            row=2, column=0, columnspan=6, sticky="w", pady=(8, 0)
        )

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=(14, 8))

        self.convert_button = ttk.Button(
            action_frame,
            text="Convert PDF to Audiobook",
            command=self.start_conversion_thread,
        )
        self.convert_button.pack(side="left")

        ttk.Button(action_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=8)

        self.status_label = ttk.Label(action_frame, text="Ready")
        self.status_label.pack(side="right")

        log_frame = ttk.LabelFrame(main_frame, text="Progress Log", padding=10)
        log_frame.pack(fill="both", expand=True, pady=8)

        self.log_text = tk.Text(log_frame, height=15, wrap="word", font=("Consolas", 10))
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        self.log("Ready. Choose a PDF file to begin.")

    def choose_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Choose PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )

        if file_path:
            self.pdf_path.set(file_path)
            self.suggest_output_path()

    def choose_output(self):
        engine = self.engine.get()
        default_extension = ".mp3" if engine == "gtts" else ".wav"
        filetypes = [("MP3 audio", "*.mp3")] if engine == "gtts" else [("WAV audio", "*.wav")]
        filetypes.append(("All files", "*.*"))

        file_path = filedialog.asksaveasfilename(
            title="Save audiobook as",
            defaultextension=default_extension,
            filetypes=filetypes,
        )

        if file_path:
            self.output_path.set(file_path)

    def suggest_output_path(self):
        pdf = self.pdf_path.get().strip()
        if not pdf:
            return

        extension = ".mp3" if self.engine.get() == "gtts" else ".wav"
        self.output_path.set(str(Path(pdf).with_suffix(extension)))

    def engine_changed(self, event=None):
        self.suggest_output_path()

    def log(self, message):
        def write_message():
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")

        self.window.after(0, write_message)

    def clear_log(self):
        self.log_text.delete("1.0", "end")

    def get_optional_page_number(self, value, field_name):
        value = value.strip()
        if not value:
            return None

        try:
            number = int(value)
        except ValueError as error:
            raise AudiobookError(f"{field_name} must be a number.") from error

        if number < 1:
            raise AudiobookError(f"{field_name} must be 1 or higher.")

        return number

    def start_conversion_thread(self):
        pdf = self.pdf_path.get().strip()
        output = self.output_path.get().strip()

        if not pdf:
            messagebox.showerror("Missing PDF", "Please choose a PDF file first.")
            return

        if not output:
            messagebox.showerror("Missing output", "Please choose where to save the audiobook.")
            return

        self.convert_button.config(state="disabled")
        self.status_label.config(text="Working...")
        self.log("\nStarting conversion...")

        thread = threading.Thread(target=self.convert_pdf, daemon=True)
        thread.start()

    def convert_pdf(self):
        try:
            start_page = self.get_optional_page_number(self.start_page.get(), "Start page")
            end_page = self.get_optional_page_number(self.end_page.get(), "End page")

            final_path = convert_pdf_to_audiobook(
                pdf_path=self.pdf_path.get().strip(),
                output_path=self.output_path.get().strip(),
                engine=self.engine.get(),
                start_page=start_page,
                end_page=end_page,
                language=self.language.get().strip() or "en",
                rate=self.rate.get(),
                save_text=self.save_text.get(),
                log_func=self.log,
            )

            self.log("Done!")
            self.log(f"Audiobook saved to: {final_path}")
            self.window.after(0, lambda: messagebox.showinfo("Done", f"Audiobook saved to:\n{final_path}"))
        except AudiobookError as error:
            self.log(f"Error: {error}")
            self.window.after(0, lambda: messagebox.showerror("Conversion Error", str(error)))
        except Exception as error:
            self.log(f"Unexpected error: {error}")
            self.window.after(0, lambda: messagebox.showerror("Unexpected Error", str(error)))
        finally:
            self.window.after(0, lambda: self.convert_button.config(state="normal"))
            self.window.after(0, lambda: self.status_label.config(text="Ready"))


def main():
    window = tk.Tk()
    app = PdfToAudiobookApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
