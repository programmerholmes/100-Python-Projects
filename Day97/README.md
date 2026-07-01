# Downloads Organizer 🗂️

A little Python automation that tidies a messy folder — your **Downloads** by
default — by moving every loose file into a subfolder for its type: **Images,
Documents, Spreadsheets, Video, Audio, Archives, Installers, Code**, and more.

Built to be **safe**: it previews by default and never deletes anything, and you
can undo any run.

## Safety first

- **Dry run by default.** Just running it *shows you what it would do* and moves
  nothing. You must add `--apply` to actually move files.
- **Never deletes.** Files are only *moved*; a name clash becomes `file (1).ext`.
- **Undo.** Every real run is logged, so `--undo` puts everything back.
- It skips folders, hidden files, and OS junk (`desktop.ini`, `Thumbs.db`).

## Usage

```bash
python main.py                      # PREVIEW tidying your Downloads (safe)
python main.py --apply              # actually organise Downloads
python main.py --undo               # undo the last real run

python main.py "D:\path\to\folder"        # work on a different folder
python main.py "D:\path\to\folder" --apply
python main.py --apply --watch      # keep tidying new files as they arrive
```

Running it with no arguments (e.g. clicking **Run** in your IDE) is always the
safe preview.

## Example

```
Dry run - 10 file(s) would be organised (nothing has been moved):

  Archives         1   backup.zip
  Audio            1   mixtape.mp3
  Code             1   main.py
  Documents        2   invoice.pdf, report.docx
  Images           2   cat.png, holiday.jpg
  Installers       1   app-setup.exe
  Other            1   mystery.dat
  Spreadsheets     1   budget.xlsx

Run again with  --apply  to actually move them (then --undo to reverse).
```

## How it works

- Each file's extension is looked up in a category table (`.jpg` → Images,
  `.pdf` → Documents, …); anything unknown goes to **Other**.
- `--apply` moves the files with `shutil.move`, creating category folders as
  needed, resolving name clashes, and appending the run to a small
  `.organizer_log.json` in that folder.
- `--undo` reads that log and moves the files back, then removes any empty
  category folders it had created.
- `--watch` just re-runs the organise step on a timer, so a folder stays tidy on
  its own.

## Files

```
main.py            the whole tool
requirements.txt   (none — standard library only)
reflection.md      project notes
```
