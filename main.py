"""Python Utility Lab - entry point.

Run without arguments for the interactive menu:
    python main.py

Or use quick command-line shortcuts:
    python main.py password --length 20
    python main.py convert 10 km mi
    python main.py slug "Hello World!"
    python main.py organize examples/messy_folder          (preview only)
    python main.py organize examples/messy_folder --apply
    python main.py duplicates .
    python main.py csv examples/sample_data.csv
"""
from __future__ import annotations

import argparse
import sys

from utility_lab import __version__
from utility_lab.core import ui
from utility_lab.tools import (bulk_renamer, csv_summary, duplicate_finder, file_organizer,
                               password_generator, text_tools, todo_manager, unit_converter)

TOOLS = [
    ("Password Generator", "Random passwords & passphrases", password_generator.run),
    ("File Organizer", "Sort a messy folder by file type", file_organizer.run),
    ("Bulk Renamer", "Rename many files at once", bulk_renamer.run),
    ("Text Tools", "Stats, snake_case, slugs, palindromes", text_tools.run),
    ("Unit Converter", "Length, weight, volume, temperature", unit_converter.run),
    ("Duplicate Finder", "Find identical files in a folder", duplicate_finder.run),
    ("To-Do Manager", "Simple saved task list", todo_manager.run),
    ("CSV Summary", "Instant overview of a CSV file", csv_summary.run),
]


def menu() -> None:
    while True:
        ui.header(f"Python Utility Lab v{__version__}")
        for i, (name, desc, _) in enumerate(TOOLS, 1):
            print(f"  {i}) {name:20} {desc}")
        print("  0) Exit")
        choice = input("\nSelect a tool: ").strip()
        if choice in ("0", "q", "quit", "exit"):
            print("Goodbye!")
            return
        if choice.isdigit() and 1 <= int(choice) <= len(TOOLS):
            try:
                TOOLS[int(choice) - 1][2]()
            except (KeyboardInterrupt, EOFError):
                print("\n(cancelled)")
            ui.pause()
        else:
            print("Invalid choice, try again.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="utility-lab", description="Python Utility Lab")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command")

    pw = sub.add_parser("password", help="generate a password")
    pw.add_argument("--length", type=int, default=16)
    pw.add_argument("--no-symbols", action="store_true")

    cv = sub.add_parser("convert", help="convert units")
    cv.add_argument("value", type=float)
    cv.add_argument("src")
    cv.add_argument("dst")

    sl = sub.add_parser("slug", help="slugify text")
    sl.add_argument("text")

    org = sub.add_parser("organize", help="organize a folder (preview unless --apply)")
    org.add_argument("folder")
    org.add_argument("--apply", action="store_true")

    dup = sub.add_parser("duplicates", help="find duplicate files")
    dup.add_argument("folder")

    csvp = sub.add_parser("csv", help="summarize a CSV file")
    csvp.add_argument("path")
    return p


def run_command(args: argparse.Namespace) -> int:
    try:
        if args.command == "password":
            pw = password_generator.generate_password(args.length, symbols=not args.no_symbols)
            print(pw, f"({password_generator.strength(pw)})")
        elif args.command == "convert":
            print(f"{args.value:g} {args.src} = "
                  f"{unit_converter.convert(args.value, args.src, args.dst):.6g} {args.dst}")
        elif args.command == "slug":
            print(text_tools.slugify(args.text))
        elif args.command == "organize":
            moves = file_organizer.organize_directory(args.folder, dry_run=not args.apply)
            for src, dst in moves:
                print(f"{src.name} -> {dst.parent.name}/{dst.name}")
            print(f"\n{len(moves)} file(s) {'moved' if args.apply else 'would be moved (use --apply)'}.")
        elif args.command == "duplicates":
            groups = duplicate_finder.find_duplicates(args.folder)
            for i, g in enumerate(groups, 1):
                print(f"Group {i}:", *map(str, g), sep="\n  ")
            print(f"{len(groups)} duplicate group(s).")
        elif args.command == "csv":
            s = csv_summary.summarize_csv(args.path)
            print(f"{s['rows']} rows")
            for name, info in s["columns"].items():
                print(f"- {name}: {info}")
    except (ValueError, OSError) as exc:
        print("Error:", exc, file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command is None:
        menu()
        return 0
    return run_command(args)


if __name__ == "__main__":
    sys.exit(main())
