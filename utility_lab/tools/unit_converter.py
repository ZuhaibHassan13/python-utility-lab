"""Convert between common units of length, weight, volume and temperature."""
from __future__ import annotations

from utility_lab.core import ui

# factor = how many base units in 1 of this unit
LENGTH = {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mi": 1609.344,
          "yd": 0.9144, "ft": 0.3048, "in": 0.0254}
WEIGHT = {"kg": 1, "g": 0.001, "mg": 1e-6, "lb": 0.45359237, "oz": 0.028349523125}
VOLUME = {"l": 1, "ml": 0.001, "gal": 3.785411784, "qt": 0.946352946,
          "cup": 0.2365882365, "floz": 0.0295735295625}
TEMPERATURE = {"c", "f", "k"}
TABLES = {"length": LENGTH, "weight": WEIGHT, "volume": VOLUME}


def _convert_temperature(value: float, src: str, dst: str) -> float:
    celsius = {"c": value, "f": (value - 32) * 5 / 9, "k": value - 273.15}[src]
    return {"c": celsius, "f": celsius * 9 / 5 + 32, "k": celsius + 273.15}[dst]


def convert(value: float, src: str, dst: str) -> float:
    src, dst = src.lower().strip(), dst.lower().strip()
    if src in TEMPERATURE and dst in TEMPERATURE:
        return _convert_temperature(value, src, dst)
    for table in TABLES.values():
        if src in table and dst in table:
            return value * table[src] / table[dst]
    raise ValueError(f"Cannot convert '{src}' to '{dst}'. Check the unit names.")


def supported_units() -> dict[str, list[str]]:
    units = {name: sorted(t) for name, t in TABLES.items()}
    units["temperature"] = sorted(TEMPERATURE)
    return units


def run() -> None:
    ui.header("Unit Converter")
    for name, units in supported_units().items():
        print(f"  {name:12}: {', '.join(units)}")
    value = ui.ask_float("\nValue")
    src, dst = ui.ask("From unit"), ui.ask("To unit")
    try:
        print(f"\n  {value:g} {src} = {convert(value, src, dst):.6g} {dst}")
    except ValueError as exc:
        print("Error:", exc)
