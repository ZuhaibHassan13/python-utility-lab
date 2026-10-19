"""A tiny to-do list saved as JSON in the data/ folder."""
from __future__ import annotations

import json
from pathlib import Path

from utility_lab.core import ui

DEFAULT_FILE = Path(__file__).resolve().parents[2] / "data" / "todos.json"


def load_tasks(path: str | Path = DEFAULT_FILE) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_tasks(tasks: list[dict], path: str | Path = DEFAULT_FILE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def add_task(title: str, path: str | Path = DEFAULT_FILE) -> dict:
    if not title.strip():
        raise ValueError("Task title cannot be empty.")
    tasks = load_tasks(path)
    task = {"id": max((t["id"] for t in tasks), default=0) + 1,
            "title": title.strip(), "done": False}
    tasks.append(task)
    save_tasks(tasks, path)
    return task


def complete_task(task_id: int, path: str | Path = DEFAULT_FILE) -> bool:
    tasks = load_tasks(path)
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks, path)
            return True
    return False


def remove_task(task_id: int, path: str | Path = DEFAULT_FILE) -> bool:
    tasks = load_tasks(path)
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    save_tasks(remaining, path)
    return True


def format_tasks(tasks: list[dict]) -> str:
    if not tasks:
        return "  (no tasks yet)"
    return "\n".join(f"  [{'x' if t['done'] else ' '}] {t['id']}. {t['title']}" for t in tasks)


def run() -> None:
    ui.header("To-Do Manager")
    while True:
        print("\n" + format_tasks(load_tasks()))
        print("\n a) add   d) done   r) remove   q) back")
        choice = ui.ask("Choice").lower()
        if choice == "a":
            try:
                add_task(ui.ask("Task"))
            except ValueError as exc:
                print(exc)
        elif choice in ("d", "r"):
            task_id = ui.ask_int("Task number")
            action = complete_task if choice == "d" else remove_task
            if not action(task_id):
                print("No task with that number.")
        elif choice == "q":
            return
