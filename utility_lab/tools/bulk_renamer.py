"""Rename many files at once (numbering or find/replace) with a safe preview."""
from __future__ import annotations

from pathlib import Path

from utility_lab.core import ui


def _files(folder: Path, extension: str | None) -> list[Path]:
    files = [p for p in sorted(folder.iterdir()) if p.is_file() and not p.name.startswith(".")]
    if extension:
        ext = extension.lower() if extension.startswith(".") else "." + extension.lower()
        files = [p for p in files if p.suffix.lower() == ext]
    return files


def plan_numbered(folder: str | Path, prefix: str, start: int = 1, pad: int = 3,
                  extension: str | None = None) -> list[tuple[Path, Path]]:
    """photo.jpg, a.jpg -> prefix001.jpg, prefix002.jpg ..."""
    folder = Path(folder)
    plan = []
    for i, f in enumerate(_files(folder, extension), start=start):
        plan.append((f, f.with_name(f"{prefix}{str(i).zfill(pad)}{f.suffix}")))
    return plan


def plan_replace(folder: str | Path, find: str, replace: str,
                 extension: str | None = None) -> list[tuple[Path, Path]]:
    folder = Path(folder)
    if not find:
        raise ValueError("'find' text cannot be empty.")
    plan = []
    for f in _files(folder, extension):
        if find in f.stem:
            plan.append((f, f.with_name(f.stem.replace(find, replace) + f.suffix)))
    return plan


def apply_plan(plan: list[tuple[Path, Path]], dry_run: bool = True) -> int:
    """Apply renames. Refuses to overwrite files. Returns number renamed."""
    sources = {src for src, _ in plan}
    targets = [dst for _, dst in plan]
    if len(set(targets)) != len(targets):
        raise FileExistsError("Two files would get the same new name.")
    for dst in targets:
        if dst.exists() and dst not in sources:
            raise FileExistsError(f"Would overwrite existing file: {dst.name}")
    if dry_run:
        return len(plan)
    # two-phase rename avoids clashes when names shuffle among themselves
    temps = []
    for i, (src, dst) in enumerate(plan):
        tmp = src.with_name(f".__tmp_{i}_{src.name}")
        src.rename(tmp)
        temps.append((tmp, dst))
    for tmp, dst in temps:
        tmp.rename(dst)
    return len(plan)


def run() -> None:
    ui.header("Bulk Renamer")
    folder = ui.ask("Folder", ".")
    if not Path(folder).is_dir():
        print("Not a folder.")
        return
    ext = ui.ask("Only files with extension (blank = all)", "") or None
    print("1) Numbered names (prefix001.ext)\n2) Find & replace in names")
    if ui.ask("Choose", "1") == "2":
        try:
            plan = plan_replace(folder, ui.ask("Find"), ui.ask("Replace with", ""), ext)
        except ValueError as exc:
            print("Error:", exc)
            return
    else:
        plan = plan_numbered(folder, ui.ask("Prefix", "file_"), ui.ask_int("Start at", 1, 0),
                             ui.ask_int("Digits of padding", 3, 1), ext)
    if not plan:
        print("No matching files.")
        return
    for src, dst in plan:
        print(f"  {src.name}  ->  {dst.name}")
    if ui.ask_yes_no("\nApply?", default=False):
        try:
            print(f"Renamed {apply_plan(plan, dry_run=False)} file(s).")
        except FileExistsError as exc:
            print("Error:", exc)
