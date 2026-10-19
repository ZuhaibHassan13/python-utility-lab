"""Quick summary of any CSV file: columns, types, min/max/mean, common values."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from utility_lab.core import ui


def _to_float(value: str):
    try:
        return float(value)
    except ValueError:
        return None


def summarize_csv(path: str | Path) -> dict:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        columns = reader.fieldnames or []
    summary = {"rows": len(rows), "columns": {}}
    for col in columns:
        values = [(r.get(col) or "").strip() for r in rows]
        filled = [v for v in values if v]
        info = {"missing": len(values) - len(filled)}
        numbers = [_to_float(v) for v in filled]
        if filled and all(n is not None for n in numbers):
            info.update(type="numeric", min=min(numbers), max=max(numbers),
                        mean=sum(numbers) / len(numbers))
        else:
            info.update(type="text", unique=len(set(filled)),
                        top=Counter(filled).most_common(3))
        summary["columns"][col] = info
    return summary


def run() -> None:
    ui.header("CSV Summary")
    path = ui.ask("CSV file", "examples/sample_data.csv")
    try:
        s = summarize_csv(path)
    except FileNotFoundError as exc:
        print(exc)
        return
    print(f"\n  {s['rows']} rows, {len(s['columns'])} columns")
    for name, info in s["columns"].items():
        if info["type"] == "numeric":
            detail = f"min={info['min']:g} max={info['max']:g} mean={info['mean']:.2f}"
        else:
            detail = f"{info['unique']} unique, top={info['top']}"
        print(f"  - {name} [{info['type']}] missing={info['missing']}  {detail}")
