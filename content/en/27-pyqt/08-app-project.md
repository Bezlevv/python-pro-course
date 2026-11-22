---
title: Final Project and Publishing with PyInstaller
summary: How to assemble a full application from modules, where to keep logic and data, and how to package it into a runnable .exe with PyInstaller.
order: 8
duration: 50 min
difficulty: advanced
tags: PyQt6, PySide6, PyInstaller, project, publishing, exe
---

You've come a long way: widgets, signals, layouts, dialogs, models, styles, and threads. Now let's assemble it all into a real project — and package it into a file that can run on any Windows computer without installing Python.

## Project structure

A good project shouldn't be one giant file. The standard structure of a PyQt6 application:

```
notes_app/
├── main.py            # entry point: QApplication + main window
├── main_window.py     # main window class
├── dialogs.py         # dialogs (if any)
├── storage.py         # data handling (files, database)
└── requirements.txt   # dependencies
```

Separate logic (data storage, computations) from the interface. This makes the app easier to test and modify.

## Entry point

`main.py` is always minimal — it initializes the application, shows the main window, and starts the event loop:

```python
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Notes")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

The `if __name__ == "__main__":` block lets you import the module without launching the app — useful for tests.

## Main window as a class

Move the main window logic into a class inheriting `QMainWindow`. All construction goes into `__init__` or a separate `_setup_ui()` method:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.resize(600, 400)
        self._setup_ui()
        self._connect_signals()
```

This keeps the code readable: the constructor is small, and each step lives in its own method.

## Data storage

Data can be stored in a file. For example, a minimal "data layer" for notes:

```python
import json

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
```

Note: if the file doesn't exist, `load()` returns an empty list — so the app starts "with a clean slate".

## Building the final application

Let's build the mini-app "Notes": a `QListWidget` on the left, an input field with "Add" and "Delete" buttons on the right, all saving via `NoteStorage`.

```python
import sys, json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QListWidget, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.storage = NoteStorage()
        self.setWindowTitle("Notes")
        self.resize(500, 350)

        self.list_widget = QListWidget()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("New note…")
        self.add_btn = QPushButton("Add")
        self.del_btn = QPushButton("Delete")

        right = QVBoxLayout()
        right.addWidget(self.edit)
        right.addWidget(self.add_btn)
        right.addWidget(self.del_btn)
        right.addStretch()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.list_widget, 1)   # the list stretches
        layout.addLayout(right)
        self.setCentralWidget(central)

        self.add_btn.clicked.connect(self.add_note)
        self.del_btn.clicked.connect(self.delete_note)
        self.edit.returnPressed.connect(self.add_note)

        self.notes = self.storage.load()
        self.list_widget.addItems(self.notes)

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()
        self.storage.save(self.notes)

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(self, "Delete", "Delete this note?")
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
            self.storage.save(self.notes)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Here's how all the topics you've learned connect: layouts (lesson 3), dialogs (lesson 4), signals (lesson 2), the `QMainWindow` class (lesson 4). The program is fully functional — run it and check.

## PyInstaller: packaging into .exe

**PyInstaller** is a tool that bundles a Python script and all libraries into a single executable file. Installation:

```bash
pip install pyinstaller
```

Building:

```bash
pyinstaller --onefile --windowed --name NotesApp main.py
```

What each flag means:

- `--onefile` — a single `.exe` file (everything inside);
- `--windowed` — no console window (for GUI applications);
- `--name NotesApp` — the final file name;
- `--icon app.ico` — application icon (optional).

The result appears in the `dist/` folder — the ready `NotesApp.exe` is there. You can copy it to another machine and run it: no Python needed.

## Common PyInstaller issues

1. **Missing hidden imports.** If the app uses modules PyInstaller didn't find statically, add:

   ```bash
   pyinstaller --hidden-import=module --onefile --windowed main.py
   ```

2. **Resource files (icons, fonts, data).** With `--onefile` resources are extracted to a temporary folder. Its path is available via `sys._MEIPASS`:

```python
import sys
import os


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)
```

   Use `resource_path("notes.json")` to access files next to the program.

3. **Run from dist, not from the project.** Test the built `.exe` from `dist/` itself, as if it were someone else's computer.

## Lesson summary

- A project is split into modules: entry point, main window, data layer;
- data storage — via simple files (JSON) with missing-file handling;
- PyInstaller: `pyinstaller --onefile --windowed --name App main.py`;
- for resources in `--onefile` use `sys._MEIPASS`;
- the final `.exe` is tested independently of the development environment.

Now final tasks.

<!--TASK-->
### Task 1
Create the project structure `notes_app`: files `main.py`, `main_window.py`, `storage.py` and `requirements.txt` (with the line `PyQt6` in it). In `storage.py` implement the class `NoteStorage` with methods `load()` and `save(notes)`, as in the theory. Verify that `load()` works correctly when the file doesn't exist yet.

### Task 2
Write the class `MainWindow(QMainWindow)` in the file `main_window.py`: on the left — a `QListWidget`, on the right — a `QLineEdit` and "Add" and "Delete" buttons. Import this class from `main.py` and show the window. Make sure the program starts and shows a window with the title "Notes".

### Task 3
Connect the logic: the "Add" button adds the text from the field to the list (empty strings are ignored), and the field clears. The "Delete" button asks for confirmation via `QMessageBox.question` and deletes the selected note. Test adding several notes and deleting with confirmation.

### Task 4
Connect saving: on add and delete call `storage.save(self.notes)`, and at startup — `storage.load()`. Close the application, run it again and verify the notes were saved (a `notes.json` file appeared nearby).

### Task 5
Build the application with PyInstaller: `pyinstaller --onefile --windowed --name NotesApp main.py`. Run `dist/NotesApp.exe` (or the equivalent for your OS) and verify the window appears, notes work, and the `notes.json` file is created next to the executable. If there are build errors — write them down and try adding `--hidden-import` for the problematic module.
<!--/TASK-->

<!--HINT-->
### Hint 1
In `storage.py` import `json`. The `load()` method: `try: open(...) except FileNotFoundError: return []`. The `save()` method: `json.dump(notes, f, ensure_ascii=False, indent=2)`. In `requirements.txt` write `PyQt6`.

### Hint 2
In `main_window.py` import `QMainWindow` and the widgets. In `__init__` set `setWindowTitle`, `resize`, build a `QHBoxLayout` layout with a `QListWidget` on the left and a `QVBoxLayout` on the right, and call `setCentralWidget`. In `main.py` create `MainWindow()`, `show()`, `sys.exit(app.exec())`.

### Hint 3
Create methods `add_note` and `delete_note`. In `add_note` use `self.edit.text().strip()` — empty values are ignored. In `delete_note` — `self.list_widget.currentRow()`, exit when `row < 0`; confirmation — `QMessageBox.question`; removing the item — `takeItem(row)`.

### Hint 4
Store `self.notes` in `__init__`: `self.notes = self.storage.load()`, then `self.list_widget.addItems(self.notes)`. In `add_note` and `delete_note`, after changing the list call `self.storage.save(self.notes)`.

### Hint 5
Run the build from the root of the `notes_app` project. If after launching `dist/NotesApp.exe` an error about a missing module appears — rebuild with `--hidden-import=module_name`. Remember: you must run from `dist/`, not from the sources.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
# storage.py
import json

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
```

```text
# requirements.txt
PyQt6
```

What's happening here? `load()` reads JSON from the file; if the file doesn't exist (`FileNotFoundError`), it returns an empty list — the app starts "from scratch". `save()` writes the list preserving Cyrillic (`ensure_ascii=False`) with readable formatting (`indent=2`). Specifying `encoding="utf-8"` is mandatory — without it, Windows may have problems with Russian letters. This class is a simple and reliable data layer: it can be tested separately from the interface.

### Walkthrough 2
Solution:

```python
# main_window.py
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QListWidget,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.resize(500, 350)

        self.list_widget = QListWidget()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("New note…")
        self.add_btn = QPushButton("Add")
        self.del_btn = QPushButton("Delete")

        right = QVBoxLayout()
        right.addWidget(self.edit)
        right.addWidget(self.add_btn)
        right.addWidget(self.del_btn)
        right.addStretch()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.list_widget, 1)
        layout.addLayout(right)
        self.setCentralWidget(central)
```

```python
# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

What's happening here? `main.py` is a minimal entry point: `QApplication`, window, `show()`, `exec()`. All interface construction is moved into `MainWindow.__init__`. `layout.addWidget(self.list_widget, 1)` — the second argument is the "stretch factor": the list gets all the free space, while the right column stays compact. Splitting into modules lets you run and test `MainWindow` independently.

### Walkthrough 3
Solution:

```python
class NotesWindow(QMainWindow):
    def __init__(self):
        self.notes = []
        self.edit = None
        self.list_widget = None

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(
            self, "Delete", "Delete this note?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
```

In `__init__` add `self.notes = []` and the connections: `self.add_btn.clicked.connect(self.add_note)`, `self.del_btn.clicked.connect(self.delete_note)`, `self.edit.returnPressed.connect(self.add_note)`.

What's happening here? `add_note` takes the text, strips extra spaces (`strip()`) and ignores empty strings. Adding happens in two places: into the `self.notes` list and into the `QListWidget`. `returnPressed` is the field's signal that fires on Enter: entering a note doesn't require the mouse. `delete_note` first checks `currentRow()`: if nothing is selected, it returns `-1`, and the method exits. Confirmation via `QMessageBox.question` protects against accidental deletion. `takeItem(row)` removes the item from the list widget.

### Walkthrough 4
Solution:

```python
    def __init__(self):
        ...
        self.storage = NoteStorage()
        self.notes = self.storage.load()
        self.list_widget.addItems(self.notes)
        ...

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()
        self.storage.save(self.notes)

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(self, "Delete", "Delete this note?")
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
            self.storage.save(self.notes)
```

What's happening here? At startup `storage.load()` reads the saved notes and fills the list with them. Every change (adding or deleting) is immediately written via `storage.save(self.notes)`. If you close the app and run it again — the notes are in place. The `notes.json` file appears in the working folder after the first change. This is the simplest but working persistence scheme: data survives program restarts.

### Walkthrough 5
Solution:

```bash
cd notes_app
pip install pyinstaller
pyinstaller --onefile --windowed --name NotesApp main.py
```

After building:

```bash
./dist/NotesApp.exe    # Windows
./dist/NotesApp        # Linux/macOS
```

What's happening here? PyInstaller analyzes the imports, and bundles the interpreter, libraries, and the script into one file in `dist/`. `--windowed` hides the console. On the first launch of `NotesApp.exe`, notes are written to `notes.json` next to the executable — not into the sources. If the build fails with `ModuleNotFoundError`, add `--hidden-import=module_name`. Tips: test the `.exe` from `dist/`, not from the sources; the icon is added via `--icon app.ico`. The finished file can be copied to any Windows computer — Python isn't needed there.
<!--/SOLUTION-->

<!--QUIZ-->
What is the file main.py for in a project?
- For storing data
- It is the entry point: QApplication, main window and exec()
- For styles
* Correct answer: It is the entry point: QApplication, main window and exec()
main.py launches the application and the event loop.

Why the if __name__ == "__main__" block?
- So the file cannot be imported
- So the code runs only on direct run, not on import
- To speed up the program
* Correct answer: So the code runs only on direct run, not on import
This allows importing the module (e.g., in tests) without side effects.

Which PyInstaller flag creates a single file?
- --onefile
- --single
- --bundle
* Correct answer: --onefile
--onefile packages everything into one executable file.

What does the --windowed flag do?
- Opens a window at launch
- Hides the console window
- Adds an icon
* Correct answer: Hides the console window
GUI applications don't need a console — it is hidden with --windowed.

What is sys._MEIPASS?
- The executable file name
- The path to the temporary folder with resources in --onefile mode
- The Python version
* Correct answer: The path to the temporary folder with resources in --onefile mode
In --onefile resources are extracted to a temporary folder; its path is in sys._MEIPASS.

How to handle a missing data file on load?
- Raise an error
- Return an empty list/default value
- Restart the application
* Correct answer: Return an empty list/default value
We catch FileNotFoundError and return an empty list — the application starts "from scratch".

Why separate data storage from the interface?
- So the code is shorter
- Logic is easier to test and change independently of the UI
- It is a PyInstaller requirement
* Correct answer: Logic is easier to test and change independently of the UI
The data and interface layers are independent modules: they can be developed and checked separately.

What does takeItem(row) do on QListWidget?
- Returns the item's text
- Removes the item at the given position
- Adds an item
* Correct answer: Removes the item at the given position
takeItem(row) removes the item from the list widget.

Why is --hidden-import needed?
- To speed up the build
- To add a module PyInstaller didn't find statically
- To hide the code
* Correct answer: To add a module PyInstaller didn't find statically
Sometimes imports are dynamic — PyInstaller doesn't see them, and the module is added manually.

Where does PyInstaller put the ready file?
- In the build/ folder
- In the dist/ folder
- In the project root
* Correct answer: In the dist/ folder
The ready executable appears in dist/.
<!--/QUIZ-->
