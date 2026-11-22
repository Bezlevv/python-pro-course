---
title: Dialogs, Menus, and Toolbars
summary: The main window QMainWindow: menus, QAction actions, toolbars, status bar, and standard dialogs QMessageBox, QFileDialog and QInputDialog.
order: 4
duration: 40 min
difficulty: intermediate
tags: PyQt6, PySide6, QMainWindow, QAction, QMenu, QToolBar, QStatusBar, QMessageBox, QFileDialog, QInputDialog
---

So far we've only shown single `QWidget`s. But real applications have structure: a menu on top, a toolbar, a status bar at the bottom, and a central "workspace" area. The `QMainWindow` class provides all of that. We'll also need standard dialogs — windows for choosing files, entering text, and confirming actions.

## QMainWindow — the main application window

`QMainWindow` is a ready-made desktop application skeleton. It's divided into zones:

- **menu** — the bar on top (`menuBar()`);
- **toolbars** — panels with buttons (`addToolBar`);
- **central widget** — the main area (`setCentralWidget`);
- **status bar** — the strip at the bottom (`statusBar()`).

```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QToolBar, QStatusBar)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Main window")
window.resize(600, 400)

window.setCentralWidget(QLabel("Workspace"))

window.statusBar().showMessage("Ready")   # status bar

toolbar = QToolBar("Main")
window.addToolBar(toolbar)

window.show()
sys.exit(app.exec())
```

`setCentralWidget` is a required step: it defines what occupies the main area of the window.

## QAction — actions

`QAction` describes a single action: "Open", "Save", "Exit". One action can be placed in several places at once — in a menu, on a toolbar, and in a context menu — and it will work identically everywhere:

```python
from PyQt6.QtGui import QAction

open_action = QAction("Open", window)
open_action.setShortcut("Ctrl+O")          # shortcut
open_action.setStatusTip("Open a file")    # status bar hint
open_action.triggered.connect(open_file)    # execution signal

window.menuBar().addMenu("File").addAction(open_action)
toolbar.addAction(open_action)
```

The `triggered` signal fires when the action is activated — by a menu click, a toolbar click, or a shortcut. `setCheckable(True)` turns the action into a toggle, and `setIcon` adds an icon (needs an image file).

## Menus

Menus are built from `QMenu`. The `menuBar().addMenu("File")` method returns a menu into which actions, separators, and submenus are added:

```python
menu = window.menuBar().addMenu("File")
menu.addAction(open_action)
menu.addSeparator()                 # horizontal line
menu.addAction(exit_action)

edit_menu = window.menuBar().addMenu("Edit")
submenu = edit_menu.addMenu("Insert")   # submenu
submenu.addAction(QAction("From clipboard", window))
```

## QToolBar — toolbar

A toolbar is a row of buttons under the menu. Buttons can be dragged, and the panel can be hidden:

```python
toolbar = QToolBar("Main", window)
toolbar.addAction(open_action)
toolbar.addSeparator()
toolbar.addAction(exit_action)
window.addToolBar(toolbar)
```

## QStatusBar — status bar

The status strip at the bottom of the window. `showMessage` displays a temporary message; permanent widgets are added via `addWidget`:

```python
window.statusBar().showMessage("File saved", 3000)  # for 3 seconds
window.statusBar().addPermanentWidget(QLabel("v1.0"))
```

## QMessageBox — informational windows

`QMessageBox` shows standard message windows. These are static methods that return the user's answer:

```python
from PyQt6.QtWidgets import QMessageBox

QMessageBox.information(window, "Title", "Message text")
QMessageBox.warning(window, "Warning", "File not found")
QMessageBox.critical(window, "Error", "Failed to save")
QMessageBox.about(window, "About", "My application v1.0")
```

"Yes/No" button:

```python
answer = QMessageBox.question(
    window, "Confirm", "Delete file?",
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)
if answer == QMessageBox.StandardButton.Yes:
    print("Deleting")
```

`question` returns the pressed button; the set of buttons is specified via bitwise `|`.

## QFileDialog — file selection

```python
from PyQt6.QtWidgets import QFileDialog

# open a file (returns path and filter)
file_path, _ = QFileDialog.getOpenFileName(
    window, "Choose a file", "",
    "Text files (*.txt);;All files (*)"
)
if file_path:
    print("Opened:", file_path)

# save a file
save_path, _ = QFileDialog.getSaveFileName(window, "Save As", "untitled.txt")
```

`getOpenFileName` returns a tuple of the path and the chosen filter, so the path is unpacked into `file_path, _`.

## QInputDialog — data input

`QInputDialog` asks for a single string or number:

```python
from PyQt6.QtWidgets import QInputDialog

name, ok = QInputDialog.getText(window, "Name", "What is your name?")
if ok and name:
    print("Hello,", name)

age, ok = QInputDialog.getInt(window, "Age", "How old are you?", 18, 0, 120)
if ok:
    print("Age:", age)

city, ok = QInputDialog.getItem(
    window, "City", "Choose a city", ["Moscow", "Kazan", "Sochi"], 0, False
)
```

Each method returns a tuple `(value, ok)`, where `ok` indicates whether it was confirmed (`True`) or cancelled (`False`).

## Putting it all together

A small editor with a menu and dialogs:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QFileDialog, QMessageBox)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Editor")
window.resize(600, 400)

label = QLabel("No file opened")
window.setCentralWidget(label)

def open_file():
    path, _ = QFileDialog.getOpenFileName(window, "Open", "", "*.txt")
    if path:
        label.setText(f"Opened: {path}")
        window.statusBar().showMessage(f"Opened {path}")

def about():
    QMessageBox.about(window, "About", "A PyQt6 editor example")

open_action = QAction("Open", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

about_action = QAction("About", window)
about_action.triggered.connect(about)

exit_action = QAction("Exit", window)
exit_action.setShortcut("Ctrl+Q")
exit_action.triggered.connect(app.quit)

file_menu = window.menuBar().addMenu("File")
file_menu.addAction(open_action)
file_menu.addSeparator()
file_menu.addAction(exit_action)

help_menu = window.menuBar().addMenu("Help")
help_menu.addAction(about_action)

window.show()
sys.exit(app.exec())
```

## Lesson summary

- `QMainWindow` — skeleton: menu, toolbar, central widget, status bar;
- `QAction` — an action that lives in both the menu and the toolbar;
- `QMessageBox` — info, warnings, questions;
- `QFileDialog` — file selection; `QInputDialog` — text/number input;
- any dialog returns an answer or a cancel — check via `ok` and `answer`.

Now practice.

<!--TASK-->
### Task 1
Create a `QMainWindow` with a "File" menu containing three actions: "New", "Open…" and a separator with an "Exit" action (hotkey `Ctrl+Q`). When "New" is chosen, print `New file created` to the console; when "Exit" — end the application via `app.quit()`.

### Task 2
Add an exit confirmation to the window: when "Exit" is chosen, first show `QMessageBox.question` "Really exit?" with Yes/No buttons. Exit the application only if the user pressed "Yes". Test both branches.

### Task 3
Create a main window with a central label and an "Open…" action (File menu, hotkey `Ctrl+O`). When chosen, show `QFileDialog.getOpenFileName` with a filter for `.txt` only, and print the chosen path into the label: `File: <path>`. If the user cancelled — print `Cancelled` to the console.

### Task 4
Add a `QInputDialog.getText` dialog to the window: a "Rename" action in the "Edit" menu asks for a new window title. If the user entered text and pressed OK — set it as the title via `setWindowTitle`. If cancelled — change nothing.

### Task 5
Assemble a complete window: a "File" menu (Open, Exit), a toolbar with the same "Open" action, and a status bar showing the message `Ready` at startup and the file path when it is opened. Verify the "Open" action works from the menu, from the toolbar, and via `Ctrl+O`.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create `QAction("New", window)` and `QAction("Exit", window)`. For exit connect `exit_action.triggered.connect(app.quit)`. Get the menu like this: `menu = window.menuBar().addMenu("File")`, then `menu.addAction(...)`. The separator is `menu.addSeparator()`. The hotkey is `setShortcut("Ctrl+Q")`.

### Hint 2
In the exit slot call `QMessageBox.question(window, "Confirm", "Really exit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)`. Compare the result with `QMessageBox.StandardButton.Yes`. If it matches — only then `app.quit()`.

### Hint 3
Use `QFileDialog.getOpenFileName(window, "Open", "", "Text files (*.txt)")`. Unpack the result into `(path, _)`. If `path` is non-empty — `label.setText(f"File: {path}")`, otherwise `print("Cancelled")`.

### Hint 4
Call `QInputDialog.getText(window, "Rename", "New title:")` and unpack into `(text, ok)`. If `ok` — `window.setWindowTitle(text)`. Remember: the action goes into the "Edit" menu: `window.menuBar().addMenu("Edit").addAction(action)`.

### Hint 5
Create one action `open_action` and add it both to the menu (`menu.addAction(open_action)`) and to the toolbar (`toolbar.addAction(open_action)`). Status bar: `window.statusBar().showMessage("Ready")` at startup, and in the open slot — `window.statusBar().showMessage(f"Opened {path}")`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Menu")
window.resize(400, 300)
window.setCentralWidget(QLabel("Workspace"))

def new_file():
    print("New file created")

new_action = QAction("New", window)
new_action.triggered.connect(new_file)

exit_action = QAction("Exit", window)
exit_action.setShortcut("Ctrl+Q")
exit_action.triggered.connect(app.quit)

menu = window.menuBar().addMenu("File")
menu.addAction(new_action)
menu.addSeparator()
menu.addAction(exit_action)

window.show()
sys.exit(app.exec())
```

What's happening here? `menuBar().addMenu("File")` creates a menu and returns it. `addAction` puts actions into it, `addSeparator` — a separator line. `QAction` ties the "meaning of the action" to its display: one action can be added both to a menu and to a toolbar. The `triggered` signal fires when a menu item is chosen. `app.quit()` ends the event loop, and `exec()` returns control. Also try pressing `Ctrl+Q` — the hotkey works without touching the menu.

### Walkthrough 2
Solution:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QMessageBox)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Exit confirmation")
window.resize(400, 300)
window.setCentralWidget(QLabel("Workspace"))

def confirm_exit():
    answer = QMessageBox.question(
        window, "Confirm", "Really exit?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if answer == QMessageBox.StandardButton.Yes:
        app.quit()
    else:
        print("Exit cancelled")

exit_action = QAction("Exit", window)
exit_action.triggered.connect(confirm_exit)

window.menuBar().addMenu("File").addAction(exit_action)

window.show()
sys.exit(app.exec())
```

What's happening here? `QMessageBox.question` opens a modal window — the program "freezes" until the user presses a button. The set of buttons is composed from flags via `|`. The method returns the pressed button; if it's `Yes` — we call `app.quit()`, otherwise we just print "Exit cancelled". This pattern protects against accidentally closing the application with unsaved data.

### Walkthrough 3
Solution:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Open file")
window.resize(500, 300)

label = QLabel("No file opened")
window.setCentralWidget(label)

def open_file():
    path, _ = QFileDialog.getOpenFileName(
        window, "Open", "", "Text files (*.txt)"
    )
    if path:
        label.setText(f"File: {path}")
    else:
        print("Cancelled")

open_action = QAction("Open…", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

window.menuBar().addMenu("File").addAction(open_action)

window.show()
sys.exit(app.exec())
```

What's happening here? `getOpenFileName` returns a tuple `(path, filter)`. We unpack it into `path, _` — the underscore means "we don't need this value". If the user closed the dialog without choosing, `path` is an empty string, so we print "Cancelled". If a file is chosen — the path appears in the label. Note the filter `"Text files (*.txt)"`: only `.txt` files will be visible in the dialog, though typing a name manually is still possible.

### Walkthrough 4
Solution:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QInputDialog

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Original title")
window.resize(400, 300)
window.setCentralWidget(QLabel("Workspace"))

def rename():
    text, ok = QInputDialog.getText(window, "Rename", "New title:")
    if ok and text:
        window.setWindowTitle(text)

rename_action = QAction("Rename", window)
rename_action.triggered.connect(rename)

window.menuBar().addMenu("Edit").addAction(rename_action)

window.show()
sys.exit(app.exec())
```

What's happening here? `getText` returns a tuple `(text, ok)`. If the user pressed OK, `ok` is `True`, and `text` contains the entered string. We check both `ok` and a non-empty `text` — if the user pressed OK with an empty field, the title doesn't change. `setWindowTitle(text)` instantly updates the window title. Note: if we simply called `setWindowTitle(text)` without checking `ok`, on cancel the dialog would return an empty string and erase the title.

### Walkthrough 5
Solution:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QToolBar, QFileDialog)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Toolbar and status bar")
window.resize(500, 300)

label = QLabel("No file opened")
window.setCentralWidget(label)

window.statusBar().showMessage("Ready")

def open_file():
    path, _ = QFileDialog.getOpenFileName(window, "Open", "", "*.txt")
    if path:
        label.setText(f"File: {path}")
        window.statusBar().showMessage(f"Opened {path}")

open_action = QAction("Open", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

menu = window.menuBar().addMenu("File")
menu.addAction(open_action)

toolbar = QToolBar("Main")
window.addToolBar(toolbar)
toolbar.addAction(open_action)

window.show()
sys.exit(app.exec())
```

What's happening here? The same action `open_action` is added both to the menu and to the toolbar — so clicking either of them (and `Ctrl+O`) runs the same slot `open_file`. `QToolBar` is created and attached via `addToolBar`; it can be undocked and dragged. The status bar shows "Ready", and after opening a file — its path. Note that the action appears as a button with text on the toolbar, and as a menu item in the menu: the look depends on the place of placement.
<!--/SOLUTION-->

<!--QUIZ-->
Which class provides a ready skeleton with a menu and status bar?
- QWidget
- QMainWindow
- QDialog
* Correct answer: QMainWindow
QMainWindow has menuBar(), addToolBar, setCentralWidget and statusBar().

How to set the central widget of the main window?
- setCentralWidget(widget)
- addWidget(widget)
- setWidget(widget)
* Correct answer: setCentralWidget(widget)
The central widget occupies the main area between toolbars and the status bar.

What does the QAction class describe?
- The application window
- A single action that can be placed in a menu and toolbar
- A toggle button
* Correct answer: A single action that can be placed in a menu and toolbar
QAction is a unified "action" that works anywhere in the interface.

Which signal does QAction emit on activation?
- clicked
- triggered
- activated
* Correct answer: triggered
triggered fires when an action is chosen from a menu, toolbar, or by a shortcut.

How to add a separator to a menu?
- menu.addLine()
- menu.addSeparator()
- menu.insertSeparator()
* Correct answer: menu.addSeparator()
addSeparator adds a horizontal line between menu items.

What does QMessageBox.question return?
- Nothing
- The pressed button
- True always
* Correct answer: The pressed button
question returns the button the user pressed, e.g. StandardButton.Yes.

Which method shows the file selection dialog?
- QFileDialog.open()
- QFileDialog.getOpenFileName()
- QFileDialog.chooseFile()
* Correct answer: QFileDialog.getOpenFileName()
getOpenFileName shows the system dialog and returns the path to the chosen file.

What does QInputDialog.getText return?
- Only a string
- A tuple (text, ok), where ok indicates whether the user confirmed
- A list of strings
* Correct answer: A tuple (text, ok), where ok indicates whether the user confirmed
The tuple of a value and a success flag lets you distinguish input from cancel.

What is the method setShortcut("Ctrl+O") for?
- Setting the action text
- Assigning a hotkey
- Hiding the action
* Correct answer: Assigning a hotkey
By hotkey the action fires without opening the menu.

What does statusBar().showMessage("Ready", 3000) do?
- Shows a message in the status bar for 3 seconds
- Permanently pins the text
- Adds a panel
* Correct answer: Shows a message in the status bar for 3 seconds
The second argument is the display timeout in milliseconds.
<!--/QUIZ-->
