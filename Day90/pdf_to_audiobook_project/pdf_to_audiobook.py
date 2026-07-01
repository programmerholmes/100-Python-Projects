"""
Command-line version of the PDF to Audiobook project.

Examples:
    python pdf_to_audiobook.py book.pdf
    python pdf_to_audiobook.py book.pdf --engine offline --output my_book.wav
    python pdf_to_audiobook.py book.pdf --start-page 2 --end-page 5
"""

import argparse
from pathlib import Path

from pdf_tools import AudiobookError, convert_pdf_to_audiobook


def print_log(message):
    print(message)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert a PDF into an audiobook audio file.")

    parser.add_argument("pdf", help="Path to the PDF file to convert.")
    parser.add_argument(
        "--output",
        "-o",
        help="Output audio file path. Default: same folder/name as the PDF.",
    )
    parser.add_argument(
        "--engine",
        choices=["gtts", "offline"],
        default="gtts",
        help="TTS engine. gtts creates MP3 using internet. offline creates WAV using pyttsx3.",
    )
    parser.add_argument("--start-page", type=int, help="First page to convert, starting at 1.")
    parser.add_argument("--end-page", type=int, help="Last page to convert, starting at 1.")
    parser.add_argument("--language", default="en", help="Language code for gTTS. Default: en")
    parser.add_argument("--rate", type=int, default=170, help="Speech rate for offline mode. Default: 170")
    parser.add_argument(
        "--no-text-file",
        action="store_true",
        help="Do not save the extracted text as a separate .txt file.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    pdf_path = Path(args.pdf)

    if args.output:
        output_path = Path(args.output)
    else:
        extension = ".mp3" if args.engine == "gtts" else ".wav"
        output_path = pdf_path.with_suffix(extension)

    engine_name = "pyttsx3" if args.engine == "offline" else "gtts"

    try:
        final_path = convert_pdf_to_audiobook(
            pdf_path=pdf_path,
            output_path=output_path,
            engine=engine_name,
            start_page=args.start_page,
            end_page=args.end_page,
            language=args.language,
            rate=args.rate,
            save_text=not args.no_text_file,
            log_func=print_log,
        )
        print("\nDone!")
        print(f"Audiobook saved to: {final_path}")
    except AudiobookError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
