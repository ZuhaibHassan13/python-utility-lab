"""Handy text utilities: stats, case conversion, slugify, palindrome check."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

from utility_lab.core import ui


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def text_stats(text: str) -> dict:
    words = re.findall(r"\b\w+\b", text.lower())
    return {
        "characters": len(text),
        "words": len(words),
        "lines": len(text.splitlines()) if text else 0,
        "unique_words": len(set(words)),
        "top_words": Counter(words).most_common(5),
    }


def _split_words(text: str) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)     # split camelCase
    return [w for w in re.split(r"[^A-Za-z0-9]+", text) if w]


def to_snake_case(text: str) -> str:
    return "_".join(w.lower() for w in _split_words(text))


def to_camel_case(text: str) -> str:
    words = [w.lower() for w in _split_words(text)]
    return (words[0] + "".join(w.title() for w in words[1:])) if words else ""


def to_title_case(text: str) -> str:
    return " ".join(w.capitalize() for w in _split_words(text))


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def is_palindrome(text: str) -> bool:
    cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
    return bool(cleaned) and cleaned == cleaned[::-1]


def run() -> None:
    ui.header("Text Tools")
    text = ui.ask("Enter some text")
    if not text:
        return
    stats = text_stats(text)
    print(f"\n  Characters : {stats['characters']}")
    print(f"  Words      : {stats['words']} ({stats['unique_words']} unique)")
    print(f"  snake_case : {to_snake_case(text)}")
    print(f"  camelCase  : {to_camel_case(text)}")
    print(f"  Title Case : {to_title_case(text)}")
    print(f"  slug       : {slugify(text)}")
    print(f"  Palindrome : {'yes' if is_palindrome(text) else 'no'}")
