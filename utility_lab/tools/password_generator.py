"""Secure password and passphrase generator."""
from __future__ import annotations

import secrets
import string

from utility_lab.core import ui

WORDS = (
    "apple river cloud tiger pencil orbit maple stone ember coral falcon garden "
    "harbor island jungle kettle lantern meadow nectar ocean pebble quartz rocket "
    "silver thunder umbrella velvet willow yonder zephyr bridge candle dragon forest "
    "glacier hammer iceberg jasmine koala lemon mirror nebula olive planet rabbit "
    "sunset turtle violet walnut"
).split()


def generate_password(length: int = 16, upper: bool = True, digits: bool = True,
                      symbols: bool = True) -> str:
    """Return a random password guaranteed to include each selected character class."""
    if length < 4:
        raise ValueError("Password length must be at least 4.")
    pools = [string.ascii_lowercase]
    if upper:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append("!@#$%^&*()-_=+[]{};:,.?")
    chars = [secrets.choice(pool) for pool in pools]          # one from each pool
    all_chars = "".join(pools)
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def generate_passphrase(words: int = 4, separator: str = "-") -> str:
    if words < 2:
        raise ValueError("Use at least 2 words.")
    return separator.join(secrets.choice(WORDS) for _ in range(words))


def strength(password: str) -> str:
    """Very simple strength rating: Weak / Medium / Strong."""
    score = 0
    score += len(password) >= 8
    score += len(password) >= 12
    score += any(c.islower() for c in password) and any(c.isupper() for c in password)
    score += any(c.isdigit() for c in password)
    score += any(not c.isalnum() for c in password)
    if score <= 2:
        return "Weak"
    return "Medium" if score <= 4 else "Strong"


def run() -> None:
    ui.header("Password Generator")
    print("1) Random password\n2) Passphrase")
    choice = ui.ask("Choose", "1")
    if choice == "2":
        n = ui.ask_int("Number of words", 4, minimum=2)
        for _ in range(5):
            print("  ", generate_passphrase(n))
        return
    length = ui.ask_int("Length", 16, minimum=4)
    upper = ui.ask_yes_no("Include uppercase?")
    digits = ui.ask_yes_no("Include digits?")
    symbols = ui.ask_yes_no("Include symbols?")
    for _ in range(5):
        pw = generate_password(length, upper, digits, symbols)
        print(f"   {pw}   ({strength(pw)})")
