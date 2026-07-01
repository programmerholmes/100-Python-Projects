# PDF to Audiobook Converter

This project converts a PDF file into an audiobook audio file.

It includes:

- PDF text extraction using `pypdf`
- Online MP3 text-to-speech using `gTTS`
- Offline WAV text-to-speech using `pyttsx3`
- Desktop Tkinter GUI
- Command-line version
- Extracted `.txt` file output for checking what text was read aloud

## Install

Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements.txt
```

## Run the desktop app

```bash
python pdf_to_audiobook_app.py
```

Then:

1. Click **Browse** and choose a PDF file.
2. Choose the TTS engine:
   - `gtts` creates an MP3 file and needs internet.
   - `pyttsx3` creates a WAV file and works offline.
3. Optional: enter a start page and end page.
4. Click **Convert PDF to Audiobook**.

## Run from the command line

Online MP3 mode:

```bash
python pdf_to_audiobook.py my_book.pdf
```

Offline WAV mode:

```bash
python pdf_to_audiobook.py my_book.pdf --engine offline
```

Convert only pages 2 to 5:

```bash
python pdf_to_audiobook.py my_book.pdf --start-page 2 --end-page 5
```

Choose an output file:

```bash
python pdf_to_audiobook.py my_book.pdf --output audiobook.mp3
```

## Important notes

This project extracts text from normal text-based PDFs. If the PDF is scanned or image-only, there may be no readable text to extract. In that case, the PDF would need OCR first.

The `gtts` engine requires internet access. The `pyttsx3` engine works offline, but the voice quality depends on the voices installed on your computer.
