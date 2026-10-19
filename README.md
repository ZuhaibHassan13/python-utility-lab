<div align="center">

# 🧰 Python Utility Lab

**A place for small Python tools, experiments, and beginner-friendly automation scripts.**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Tests](https://img.shields.io/badge/tests-18%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

`Python` · `Functions` · `Automation`

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [The Tools](#-the-tools)
- [Command-Line Usage](#-command-line-usage)
- [Try It With the Example Files](#-try-it-with-the-example-files)
- [Running the Tests](#-running-the-tests)
- [Project Structure](#-project-structure)
- [Adding Your Own Tool](#-adding-your-own-tool)
- [Safety Notes](#-safety-notes)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 About

**Python Utility Lab** is a collection of small, useful command-line tools written in plain Python.
It is designed for people learning Python: every tool is a short, readable module that shows how to use
functions, file handling, the standard library, and basic testing, while also solving real everyday problems
like organizing a messy Downloads folder or generating a strong password.

Everything uses only Python's **standard library**, so there is nothing to install and no virtual environment required.

## ✨ Features

- 🔧 **8 ready-to-use tools** in one interactive menu
- ⌨️ **Command-line shortcuts** for quick, scriptable use
- 🛡️ **Safe by default**: file-changing tools show a preview and ask before doing anything
- 🧪 **18 automated tests** using the built-in `unittest` module
- 📦 **Zero dependencies**: works on Windows, macOS, and Linux
- 🧩 **Easy to extend**: add a new tool in one file and one line
- 🎓 **Beginner-friendly code**: small functions, clear names, and docstrings

## 📋 Requirements

| Requirement | Version |
|-------------|---------|
| Python      | 3.9 or newer |
| Extra packages | None |

Check your Python version:

```bash
python --version
```

## 🔧 Installation

**1. Clone the repository**

```bash
git clone https://github.com/ZuhaibHassan13/python-utility-lab.git
cd python-utility-lab
```

**2. (Optional) Open it in VS Code**

```bash
code .
```

Install the official **Python** extension from the VS Code marketplace if you haven't already.

That's it. There is no `pip install` step.

> **Don't have Git?** On the repository page click **Code → Download ZIP**, unzip it, and open the folder.

## 🚀 Quick Start

Start the interactive menu:

```bash
python main.py
```

> On macOS/Linux, use `python3` if `python` is not found.

You will see:

```
=============================
  Python Utility Lab v1.0.0
=============================
  1) Password Generator   Random passwords & passphrases
  2) File Organizer       Sort a messy folder by file type
  3) Bulk Renamer         Rename many files at once
  4) Text Tools           Stats, snake_case, slugs, palindromes
  5) Unit Converter       Length, weight, volume, temperature
  6) Duplicate Finder     Find identical files in a folder
  7) To-Do Manager        Simple saved task list
  8) CSV Summary          Instant overview of a CSV file
  0) Exit

Select a tool:
```

Type a number and press **Enter**. In VS Code you can also press **F5** and choose **Run Utility Lab (menu)**.

---

## 🧰 The Tools

### 1. 🔐 Password Generator
Creates secure random passwords using Python's `secrets` module (cryptographically safe, unlike `random`).

- Choose the length and whether to include uppercase letters, digits, and symbols
- Every selected character type is guaranteed to appear at least once
- Each password gets a **Weak / Medium / Strong** rating
- Or generate memorable **passphrases** such as `maple-orbit-tiger-coral`

```
   )#I;*0tUVs313PnLAm4f   (Strong)
```

### 2. 📁 File Organizer
Sorts the files in a folder into sub-folders by type.

| Folder | Extensions (examples) |
|--------|-----------------------|
| Images | `.jpg` `.png` `.gif` `.svg` `.webp` |
| Documents | `.pdf` `.docx` `.txt` `.md` |
| Spreadsheets | `.xlsx` `.csv` `.ods` |
| Presentations | `.pptx` `.ppt` |
| Audio | `.mp3` `.wav` `.flac` |
| Video | `.mp4` `.mkv` `.mov` |
| Archives | `.zip` `.rar` `.7z` |
| Code | `.py` `.js` `.html` `.json` |
| Other | everything else |

- Shows a **preview** of every move first
- Never overwrites: name clashes become `photo (1).jpg`
- Ignores hidden files and existing sub-folders

### 3. ✏️ Bulk Renamer
Renames many files in one go, with a preview.

- **Numbered mode:** `IMG_4821.jpg`, `IMG_4822.jpg` → `trip_001.jpg`, `trip_002.jpg`
- **Find & replace mode:** change `draft_report.txt` → `final_report.txt`
- Optional filter by extension (e.g. only `.jpg`)
- Refuses to run if a rename would overwrite an existing file

### 4. 📝 Text Tools
Type any text and instantly get:

```
  Characters : 11
  Words      : 2 (2 unique)
  snake_case : hello_world
  camelCase  : helloWorld
  Title Case : Hello World
  slug       : hello-world
  Palindrome : no
```

### 5. 📏 Unit Converter
Converts between common units.

| Category | Units |
|----------|-------|
| Length | `m` `km` `cm` `mm` `mi` `yd` `ft` `in` |
| Weight | `kg` `g` `mg` `lb` `oz` |
| Volume | `l` `ml` `gal` `qt` `cup` `floz` |
| Temperature | `c` `f` `k` |

```
  10 km = 6.21371 mi
```

### 6. 🔍 Duplicate Finder
Scans a folder (including sub-folders) and lists files with identical content.
It groups files by size first, then compares SHA-256 hashes, which keeps it fast.
Names do not matter, only content.

```
Group 1:
    examples/messy_folder/holiday.jpg
    examples/messy_folder/holiday_copy.jpg

Found 1 duplicate group(s), ~0.0 KB reclaimable.
```

### 7. ✅ To-Do Manager
A small task list saved to `data/todos.json`, so your tasks are still there next time.

```
  [ ] 1. Buy milk
  [x] 2. Finish README

 a) add   d) done   r) remove   q) back
```

### 8. 📊 CSV Summary
Gives an instant overview of any CSV file: row count, each column's type (numeric or text),
missing values, min / max / mean for numbers, and the most common values for text.

```
  6 rows, 4 columns
  - name [text] missing=0  6 unique, top=[...]
  - age [numeric] missing=0  min=26 max=35 mean=30.33
  - salary [numeric] missing=1  min=52000 max=88000 mean=69400.00
```

---

## ⌨️ Command-Line Usage

Skip the menu and run a tool directly:

| Command | What it does |
|---------|--------------|
| `python main.py password --length 20` | Generate a 20-character password |
| `python main.py password --no-symbols` | Password without symbols |
| `python main.py convert 100 c f` | Convert 100 °C to °F |
| `python main.py convert 5 km mi` | Convert 5 km to miles |
| `python main.py slug "My Blog Post!"` | Prints `my-blog-post` |
| `python main.py organize <folder>` | **Preview** how a folder would be organized |
| `python main.py organize <folder> --apply` | Actually move the files |
| `python main.py duplicates <folder>` | List duplicate files |
| `python main.py csv <file.csv>` | Summarize a CSV file |
| `python main.py --version` | Show the version |
| `python main.py --help` | Show all commands |

## 🎮 Try It With the Example Files

The `examples/` folder gives you safe files to experiment with:

- `examples/messy_folder/` contains mixed files (images, a PDF, audio, video, a zip, and more),
  including a duplicate pair: `holiday.jpg` and `holiday_copy.jpg`
- `examples/sample_data.csv` is a small employee dataset with one missing value

```bash
python main.py duplicates examples/messy_folder      # finds the duplicate pair
python main.py organize examples/messy_folder        # preview only
python main.py csv examples/sample_data.csv          # column summary
```

## 🧪 Running the Tests

```bash
python -m unittest discover -s tests -v
```

Expected result:

```
Ran 18 tests in 0.0xs

OK
```

In VS Code you can also use the **Testing** sidebar (flask icon). The project is pre-configured for `unittest`.

## 🗂️ Project Structure

```
python-utility-lab/
├── main.py                      # Entry point: interactive menu + CLI commands
├── requirements.txt             # (no third-party packages needed)
├── README.md
├── LICENSE
├── utility_lab/
│   ├── __init__.py              # Package version
│   ├── core/
│   │   └── ui.py                # Input helpers: ask, ask_int, ask_yes_no, ...
│   └── tools/
│       ├── password_generator.py
│       ├── file_organizer.py
│       ├── bulk_renamer.py
│       ├── text_tools.py
│       ├── unit_converter.py
│       ├── duplicate_finder.py
│       ├── todo_manager.py
│       └── csv_summary.py
├── tests/
│   └── test_tools.py            # 18 unit tests
├── examples/
│   ├── sample_data.csv
│   └── messy_folder/            # sample files for experimenting
├── data/                        # runtime data (your to-do list)
└── .vscode/                     # F5 run config + test settings
```

### Design idea

Each tool separates **logic** from **interaction**:

- **Pure functions** (e.g. `convert()`, `slugify()`, `find_duplicates()`) take inputs and return results, which makes them easy to test and reuse in your own scripts.
- A **`run()` function** handles `input()` and `print()` for the menu.

You can import the functions directly:

```python
from utility_lab.tools.unit_converter import convert
from utility_lab.tools.text_tools import slugify

print(convert(100, "c", "f"))      # 212.0
print(slugify("Hello, World!"))    # hello-world
```

## ➕ Adding Your Own Tool

**1. Create the module** `utility_lab/tools/stopwatch.py`:

```python
"""A simple example tool."""
from utility_lab.core import ui


def format_time(seconds: int) -> str:
    """Turn 125 into '02:05'."""
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def run() -> None:
    ui.header("Stopwatch")
    seconds = ui.ask_int("Seconds", 125, minimum=0)
    print("Formatted:", format_time(seconds))
```

**2. Register it** in `main.py`:

```python
from utility_lab.tools import stopwatch          # add to the imports

TOOLS = [
    ...
    ("Stopwatch", "Format and time durations", stopwatch.run),   # add a line
]
```

**3. Test it** by adding a test to `tests/test_tools.py`:

```python
def test_format_time(self):
    from utility_lab.tools import stopwatch
    self.assertEqual(stopwatch.format_time(125), "02:05")
```

**4. Run the tests and push:**

```bash
python -m unittest discover -s tests
git add .
git commit -m "Add stopwatch tool"
git push
```

## 🛡️ Safety Notes

- **File Organizer** and **Bulk Renamer** always show a preview and default to **No**.
- Existing files are never overwritten.
- Neither tool has an undo feature. Try them on the `examples/` folder, or a copy of your files, before using them on important data.
- Passwords are generated locally and never stored or sent anywhere.
- `data/todos.json` is listed in `.gitignore`, so your personal tasks are not uploaded to GitHub.

## 🩺 Troubleshooting

| Problem | Fix |
|---------|-----|
| `'python' is not recognized` | Install Python from [python.org](https://www.python.org/downloads/) and tick **"Add Python to PATH"**. On macOS/Linux use `python3`. |
| `ModuleNotFoundError: utility_lab` | Run commands from the project's root folder (the one containing `main.py`). |
| `git is not recognized` | Install [Git for Windows](https://git-scm.com/download/win) and restart VS Code. |
| CSV shows only one column | The file probably uses `;` as a separator. Only commas are supported at the moment. |
| Folder not found | Check the path, or use quotes if it contains spaces: `"C:\My Files"`. |

## 🗺️ Roadmap

- [ ] Stopwatch and countdown timer
- [ ] Expense tracker
- [ ] Folder backup tool with timestamps
- [ ] Date calculator
- [ ] Log file analyzer
- [ ] CSV delimiter auto-detection
- [ ] Undo support for the File Organizer

## 🤝 Contributing

Contributions, ideas, and bug reports are welcome.

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-new-tool`
3. Make your changes and add tests
4. Run `python -m unittest discover -s tests`
5. Commit and push your branch, then open a Pull Request

Please keep tools small, standard-library-only, and beginner-friendly.

## 📄 License

Released under the [MIT License](LICENSE). You are free to use, modify, and share this project.

## 👤 Author

**Zuhaib Hassan**
GitHub: [@ZuhaibHassan13](https://github.com/ZuhaibHassan13)

---

<div align="center">

If you found this useful, consider giving the repo a ⭐

</div>
