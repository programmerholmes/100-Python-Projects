"""
Downloads Organizer
===================
Tidies a messy folder (your Downloads by default) by moving each file into a
subfolder for its type — Images, Documents, Video, Audio, Archives, Code, etc.

It's built to be SAFE:
  * By default it only does a **dry run** — it shows what it *would* move and
    changes nothing. You have to add `--apply` to actually move files.
  * It never deletes anything. Name clashes are renamed ("file (1).ext").
  * Every real run is logged, so `--undo` puts everything back where it was.

Usage:
    python main.py                 # preview tidying your Downloads folder
    python main.py --apply         # actually organise Downloads
    python main.py --undo          # undo the last real run
    python main.py "D:\\some\\folder"    # work on a different folder
    python main.py --apply --watch # keep tidying new files as they arrive

No third-party libraries — just the Python standard library.
"""

import argparse
import json
import shutil
import time
from datetime import datetime
from pathlib import Path

# extension -> category
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg",
               ".tiff", ".heic", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md", ".tex"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".tsv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp", ".key"],
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".wmv", ".m4v"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".appimage", ".apk"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".cs",
             ".go", ".rs", ".rb", ".php", ".sh", ".json", ".xml", ".yml",
             ".yaml", ".sql", ".ipynb"],
    "Ebooks": [".epub", ".mobi", ".azw3"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}
OTHER = "Other"
LOG_NAME = ".organizer_log.json"
# Files we never touch (our own log, OS junk, hidden files).
SKIP_NAMES = {LOG_NAME.lower(), "desktop.ini", "thumbs.db", ".ds_store"}

_EXT_TO_CATEGORY = {ext: cat for cat, exts in CATEGORIES.items() for ext in exts}
_CATEGORY_FOLDERS = set(CATEGORIES) | {OTHER}


def category_for(path: Path) -> str:
    return _EXT_TO_CATEGORY.get(path.suffix.lower(), OTHER)


def unique_destination(dest: Path) -> Path:
    """If `dest` already exists, return 'name (1).ext', 'name (2).ext', ..."""
    if not dest.exists():
        return dest
    stem, suffix, n = dest.stem, dest.suffix, 1
    while True:
        candidate = dest.with_name(f"{stem} ({n}){suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def plan_moves(folder: Path):
    """Return a list of (source, category) for the loose files in `folder`."""
    moves = []
    for item in sorted(folder.iterdir()):
        if item.is_dir():
            continue                                  # leave folders alone
        if item.name.lower() in SKIP_NAMES or item.name.startswith("."):
            continue
        moves.append((item, category_for(item)))
    return moves


def preview(folder: Path, moves):
    print(f"\nFolder: {folder}")
    if not moves:
        print("Nothing to organise - it's already tidy.\n")
        return
    by_cat = {}
    for src, cat in moves:
        by_cat.setdefault(cat, []).append(src.name)
    print(f"\nDry run - {len(moves)} file(s) would be organised "
          f"(nothing has been moved):\n")
    for cat in sorted(by_cat):
        names = by_cat[cat]
        shown = ", ".join(names[:4]) + (f" ... (+{len(names) - 4} more)" if len(names) > 4 else "")
        print(f"  {cat:<14} {len(names):>3}   {shown}")
    print("\nRun again with  --apply  to actually move them (then --undo to reverse).\n")


def apply_moves(folder: Path, moves):
    """Move the files and append the run to the undo log. Returns counts."""
    record = []
    counts = {}
    for src, cat in moves:
        target_dir = folder / cat
        target_dir.mkdir(exist_ok=True)
        dest = unique_destination(target_dir / src.name)
        try:
            shutil.move(str(src), str(dest))
        except (OSError, shutil.Error) as exc:
            print(f"  skipped {src.name} ({exc})")
            continue
        record.append({"from": str(src), "to": str(dest)})
        counts[cat] = counts.get(cat, 0) + 1

    if record:
        log_path = folder / LOG_NAME
        runs = _load_log(log_path)
        runs.append({"time": datetime.now().isoformat(timespec="seconds"), "moves": record})
        log_path.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    return counts


def _load_log(log_path: Path):
    if log_path.exists():
        try:
            return json.loads(log_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return []
    return []


def undo(folder: Path):
    """Reverse the most recent real run recorded in the log."""
    log_path = folder / LOG_NAME
    runs = _load_log(log_path)
    if not runs:
        print("Nothing to undo - no recorded runs for this folder.\n")
        return
    run = runs.pop()
    restored = 0
    for move in reversed(run["moves"]):
        src, dest = Path(move["to"]), Path(move["from"])
        if not src.exists():
            continue
        dest = unique_destination(dest)
        try:
            shutil.move(str(src), str(dest))
            restored += 1
        except (OSError, shutil.Error) as exc:
            print(f"  couldn't restore {src.name} ({exc})")

    # tidy up now-empty category folders we created
    for cat in _CATEGORY_FOLDERS:
        d = folder / cat
        if d.is_dir() and not any(d.iterdir()):
            d.rmdir()

    log_path.write_text(json.dumps(runs, indent=2), encoding="utf-8")
    print(f"\nUndid the run from {run['time']}: restored {restored} file(s).\n")


def report(counts):
    total = sum(counts.values())
    if not total:
        print("Nothing needed organising.\n")
        return
    print(f"\nOrganised {total} file(s):")
    for cat in sorted(counts):
        print(f"  {cat:<14} {counts[cat]:>3}")
    print("\nUndo any time with:  python main.py --undo\n")


def watch(folder: Path, interval: float):
    print(f"\nWatching {folder} - new files will be organised automatically.")
    print("Press Ctrl+C to stop.\n")
    try:
        while True:
            moves = plan_moves(folder)
            if moves:
                counts = apply_moves(folder, moves)
                stamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{stamp}] organised {sum(counts.values())} new file(s): "
                      + ", ".join(f"{c} {n}" for c, n in counts.items()))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped watching.\n")


def parse_args():
    downloads = str(Path.home() / "Downloads")
    p = argparse.ArgumentParser(description="Organise a folder's files into type-based subfolders.")
    p.add_argument("path", nargs="?", default=downloads,
                   help="Folder to organise (default: your Downloads folder).")
    p.add_argument("--apply", action="store_true",
                   help="Actually move files. Without this it's a safe dry-run preview.")
    p.add_argument("--undo", action="store_true",
                   help="Undo the most recent real run in this folder.")
    p.add_argument("--watch", action="store_true",
                   help="Keep running and organise new files as they arrive (implies --apply).")
    p.add_argument("--interval", type=float, default=5.0,
                   help="Seconds between checks in --watch mode (default: 5).")
    return p.parse_args()


def main():
    args = parse_args()
    folder = Path(args.path).expanduser()

    if not folder.is_dir():
        print(f"That folder doesn't exist: {folder}")
        return

    if args.undo:
        undo(folder)
        return

    if args.watch:
        watch(folder, args.interval)
        return

    moves = plan_moves(folder)
    if args.apply:
        print(f"\nOrganising: {folder}")
        report(apply_moves(folder, moves))
    else:
        preview(folder, moves)


if __name__ == "__main__":
    main()
