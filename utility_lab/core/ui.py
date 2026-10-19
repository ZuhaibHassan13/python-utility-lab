"""Tiny helpers for friendly interactive prompts."""
from __future__ import annotations


def header(title: str) -> None:
    line = "=" * (len(title) + 4)
    print(f"\n{line}\n  {title}\n{line}")


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else (default or "")


def ask_int(prompt: str, default: int | None = None, minimum: int | None = None) -> int:
    while True:
        raw = ask(prompt, str(default) if default is not None else None)
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"  Please enter a number >= {minimum}.")
            continue
        return value


def ask_float(prompt: str) -> float:
    while True:
        try:
            return float(ask(prompt))
        except ValueError:
            print("  Please enter a number.")


def ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    raw = input(f"{prompt} ({hint}): ").strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


def pause() -> None:
    input("\nPress Enter to continue...")
