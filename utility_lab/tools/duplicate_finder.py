"""Find duplicate files (same content) inside a folder tree."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

from utility_lab.core import ui


def file_hash(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder: str | Path) -> list[list[Path]]:
    """Return groups of files with identical content."""
    folder = Path(folder)
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")
    by_size = defaultdict(list)
    for p in folder.rglob("*"):
        if p.is_file():
            by_size[p.stat().st_size].append(p)
    by_hash = defaultdict(list)
    for files in by_size.values():
        if len(files) > 1:                       # only hash files that share a size
            for p in files:
                by_hash[file_hash(p)].append(p)
    return [sorted(g) for g in by_hash.values() if len(g) > 1]


def run() -> None:
    ui.header("Duplicate File Finder")
    folder = ui.ask("Folder to scan", ".")
    try:
        groups = find_duplicates(folder)
    except NotADirectoryError as exc:
        print(exc)
        return
    if not groups:
        print("No duplicates found.")
        return
    wasted = 0
    for i, group in enumerate(groups, 1):
        print(f"\nGroup {i}:")
        for p in group:
            print("   ", p)
        wasted += group[0].stat().st_size * (len(group) - 1)
    print(f"\nFound {len(groups)} duplicate group(s), ~{wasted / 1024:.1f} KB reclaimable.")
