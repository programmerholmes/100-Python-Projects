"""
Core helper functions for the PDF to Audiobook project.

This file keeps the PDF extraction and text-to-speech code separate from
Tkinter so it can be reused by both the desktop app and the command-line app.
"""

import os
import re
import tempfile
from pathlib import Path

from pypdf import PdfReader


class AudiobookError(Exception):
    """Custom error used for clean user-facing error messages."""


def clean_text(text):
    """Clean extracted PDF text so it sounds better when read aloud."""
    if not text:
        return ""

    # Join words that were split across lines with a hyphen.
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Convert line breaks and repeated whitespace into simple spaces.
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n ", "\n", text)

    return text.strip()


def extract_text_from_pdf(pdf_path, start_page=None, end_page=None, log_func=None):
    """
    Extract text from a PDF file.

    Page numbers are 1-based for the user. For example, start_page=1 means
    the first page of the PDF.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise AudiobookError(f"PDF file not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise AudiobookError("Please choose a file ending in .pdf")

    try:
        reader = PdfReader(str(pdf_path))
    except Exception as error:
        raise AudiobookError(f"Could not open the PDF file. Details: {error}")

    total_pages = len(reader.pages)
    if total_pages == 0:
        raise AudiobookError("This PDF does not contain any pages.")

    start = 1 if start_page is None else int(start_page)
    end = total_pages if end_page is None else int(end_page)

    if start < 1 or end < 1 or start > end:
        raise AudiobookError("Invalid page range. Start page must be before end page.")

    if start > total_pages:
        raise AudiobookError(f"Start page is too high. This PDF only has {total_pages} pages.")

    end = min(end, total_pages)

    extracted_pages = []

    for page_number in range(start, end + 1):
        if log_func:
            log_func(f"Extracting text from page {page_number} of {total_pages}...")

        page = reader.pages[page_number - 1]
        page_text = page.extract_text() or ""
        page_text = clean_text(page_text)

        if page_text:
            extracted_pages.append(page_text)

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise AudiobookError(
            "No readable text was found in this PDF. It may be a scanned PDF/image-only file, "
            "which would need OCR before it can be converted to audio."
        )

    return full_text


def split_text_for_tts(text, max_chars=2800):
    """
    Split a long text into smaller chunks for online TTS services.

    The split tries to keep sentences together, and if a sentence is too long,
    it falls back to splitting by words.
    """
    text = clean_text(text)
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(sentence) > max_chars:
            # Save the current chunk first.
            if current:
                chunks.append(current.strip())
                current = ""

            words = sentence.split()
            word_chunk = ""
            for word in words:
                possible = f"{word_chunk} {word}".strip()
                if len(possible) <= max_chars:
                    word_chunk = possible
                else:
                    if word_chunk:
                        chunks.append(word_chunk.strip())
                    word_chunk = word

            if word_chunk:
                chunks.append(word_chunk.strip())
            continue

        possible = f"{current} {sentence}".strip()
        if len(possible) <= max_chars:
            current = possible
        else:
            if current:
                chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


def save_text_file(text, output_path):
    """Save extracted text next to the audio file for easy checking."""
    output_path = Path(output_path)
    text_path = output_path.with_suffix(".txt")
    text_path.write_text(text, encoding="utf-8")
    return text_path


def make_mp3_with_gtts(text, output_path, language="en", log_func=None):
    """
    Convert text to an MP3 using gTTS.

    gTTS uses an online text-to-speech service, so this mode needs internet.
    No API key is required.
    """
    try:
        from gtts import gTTS
    except ImportError as error:
        raise AudiobookError(
            "gTTS is not installed. Run: python -m pip install -r requirements.txt"
        ) from error

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() != ".mp3":
        output_path = output_path.with_suffix(".mp3")

    chunks = split_text_for_tts(text)

    if not chunks:
        raise AudiobookError("There is no text to convert to audio.")

    if log_func:
        log_func(f"Creating MP3 audiobook in {len(chunks)} audio section(s)...")

    with tempfile.TemporaryDirectory() as temp_dir:
        part_files = []

        for index, chunk in enumerate(chunks, start=1):
            if log_func:
                log_func(f"Generating audio section {index} of {len(chunks)}...")

            part_path = Path(temp_dir) / f"part_{index:04d}.mp3"

            try:
                tts = gTTS(text=chunk, lang=language, slow=False)
                tts.save(str(part_path))
            except Exception as error:
                raise AudiobookError(
                    "Could not create audio with gTTS. Check your internet connection, "
                    f"then try again. Details: {error}"
                )

            part_files.append(part_path)

        # MP3 files can usually be concatenated safely enough for simple projects.
        # This keeps the project beginner-friendly and avoids requiring ffmpeg.
        with output_path.open("wb") as final_audio:
            for part_path in part_files:
                final_audio.write(part_path.read_bytes())

    if log_func:
        log_func(f"Saved MP3 audiobook: {output_path}")

    return output_path


def make_wav_with_pyttsx3(text, output_path, rate=170, voice_id=None, log_func=None):
    """
    Convert text to a WAV file using pyttsx3.

    This mode works offline on most Windows computers, but the exact voice
    depends on what voices are installed on the user's system.
    """
    try:
        import pyttsx3
    except ImportError as error:
        raise AudiobookError(
            "pyttsx3 is not installed. Run: python -m pip install -r requirements.txt"
        ) from error

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() != ".wav":
        output_path = output_path.with_suffix(".wav")

    if log_func:
        log_func("Starting offline text-to-speech engine...")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", int(rate))

        if voice_id:
            engine.setProperty("voice", voice_id)

        if log_func:
            log_func("Saving WAV audiobook. This can take a little while for long PDFs...")

        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        engine.stop()
    except Exception as error:
        raise AudiobookError(f"Could not create offline WAV audio. Details: {error}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise AudiobookError("The offline engine did not create a valid audio file.")

    if log_func:
        log_func(f"Saved WAV audiobook: {output_path}")

    return output_path


def convert_pdf_to_audiobook(
    pdf_path,
    output_path,
    engine="gtts",
    start_page=None,
    end_page=None,
    language="en",
    rate=170,
    save_text=True,
    log_func=None,
):
    """Full pipeline: PDF -> extracted text -> audio file."""
    text = extract_text_from_pdf(
        pdf_path=pdf_path,
        start_page=start_page,
        end_page=end_page,
        log_func=log_func,
    )

    if save_text:
        text_path = save_text_file(text, output_path)
        if log_func:
            log_func(f"Saved extracted text for review: {text_path}")

    if engine == "gtts":
        return make_mp3_with_gtts(text, output_path, language=language, log_func=log_func)
    if engine == "pyttsx3":
        return make_wav_with_pyttsx3(text, output_path, rate=rate, log_func=log_func)

    raise AudiobookError("Unknown engine. Use 'gtts' or 'pyttsx3'.")
