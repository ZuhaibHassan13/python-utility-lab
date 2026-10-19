# Python Utility Lab

A place for small Python tools, experiments, and beginner-friendly automation scripts.

**Tags:** Python · Functions · Automation

Pure standard library - **no installs needed**. Requires Python 3.9+.

## Quick start (VS Code)

1. Unzip the folder and open it in VS Code (`File > Open Folder...`).
2. Install the **Python** extension if you haven't already.
3. Open the integrated terminal (`Ctrl + ~`) and run:

   ```bash
   python main.py
   ```
   (On macOS/Linux you may need `python3`.)

Or press **F5** and choose *Run Utility Lab (menu)*.

## Tools

| # | Tool | What it does |
|---|------|--------------|
| 1 | Password Generator | Random passwords with strength rating, and word passphrases |
| 2 | File Organizer | Sorts a folder into Images/Documents/Audio/... (preview first) |
| 3 | Bulk Renamer | Number files (`trip_001.jpg`) or find/replace in names |
| 4 | Text Tools | Word stats, snake_case, camelCase, Title Case, slugs, palindromes |
| 5 | Unit Converter | Length, weight, volume, temperature |
| 6 | Duplicate Finder | Finds identical files using SHA-256 hashes |
| 7 | To-Do Manager | Saved task list (`data/todos.json`) |
| 8 | CSV Summary | Row count, column types, min/max/mean, top values |

## Command-line shortcuts

```bash
python main.py password --length 20
python main.py convert 100 c f
python main.py slug "My Blog Post Title!"
python main.py organize examples/messy_folder           # preview only
python main.py organize examples/messy_folder --apply   # actually move files
python main.py duplicates examples/messy_folder
python main.py csv examples/sample_data.csv
```

Try the **File Organizer** on `examples/messy_folder` - it contains sample files
(including a duplicate: `holiday.jpg` and `holiday_copy.jpg`, handy for the Duplicate Finder).
Destructive tools always show a preview and default to "no".

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

```
python_utility_lab/
├── main.py                  # menu + command-line entry point
├── utility_lab/
│   ├── core/ui.py           # input helpers (ask, ask_int, ask_yes_no...)
│   └── tools/               # one module per tool
├── tests/test_tools.py
├── examples/                # sample CSV + messy folder to play with
├── data/                    # saved to-do list lives here
└── .vscode/                 # F5 run/debug + test settings
```

## Adding your own tool

1. Create `utility_lab/tools/my_tool.py` with plain functions plus a `run()` that talks to the user.
2. Import it in `main.py` and add one line to the `TOOLS` list:
   ```python
   ("My Tool", "What it does", my_tool.run),
   ```
3. Add tests in `tests/` for your pure functions.

Tip: keep logic in small functions that take inputs and return outputs (easy to test),
and keep `input()`/`print()` inside `run()`.
