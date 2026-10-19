"""Sort files in a folder into sub-folders by type (Images, Documents, ...)."""
from __future__ import annotations

import shutil
from pathlib import Path

from utility_lab.core import ui

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".odt", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "Video": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".sh"},
}


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def _unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize_directory(folder: str | Path, dry_run: bool = True) -> list[tuple[Path, Path]]:
    """Move top-level files into category folders. Returns list of (source, destination)."""
    folder = Path(folder)
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        dest = _unique_destination(folder / category_for(item) / item.name)
        moves.append((item, dest))
        if not dry_run:
            dest.parent.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest))
    return moves


def run() -> None:
    ui.header("File Organizer")
    folder = ui.ask("Folder to organize", "examples/messy_folder")
    try:
        preview = organize_directory(folder, dry_run=True)
    except NotADirectoryError as exc:
        print(exc)
        return
    if not preview:
        print("Nothing to organize.")
        return
    print("\nPlanned moves:")
    for src, dst in preview:
        print(f"  {src.name}  ->  {dst.parent.name}/{dst.name}")
    if ui.ask_yes_no("\nApply these changes?", default=False):
        organize_directory(folder, dry_run=False)
        print(f"Done. Moved {len(preview)} file(s).")
    else:
        print("No changes made.")
