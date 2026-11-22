---
title: PyQt app: notes
summary: Widgets, signals, layouts.
order: 6
duration: 50 min
difficulty: advanced
tags: pyqt, gui
---

PyQt builds desktop applications.

## Window

```python
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class NotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        button = QPushButton("Add note")
        layout = QVBoxLayout()
        layout.addWidget(button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        button.clicked.connect(self.add_note)

    def add_note(self):
        print("clicked")

app = QApplication([])
win = NotesWindow()
win.show()
app.exec()
```

## Lesson summary

Widgets + layouts + signals build GUI.

<!--TASK-->
### Task 1 — Window
Create a window.

### Task 2 — Button
Add a button.

### Task 3 — Layout
Use QVBoxLayout.

### Task 4 — Signal
Connect clicked.

### Task 5 — List
Add QListWidget.

### Task 6 — Input
QLineEdit for text.

### Task 7 — Run
Run the app loop.
<!--/TASK-->

<!--HINT-->
### Hint 1
QMainWindow.

### Hint 2
QPushButton.

### Hint 3
QVBoxLayout.

### Hint 4
clicked.connect.

### Hint 5
QListWidget.

### Hint 6
QLineEdit.

### Hint 7
app.exec().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from PyQt6.QtWidgets import QApplication, QMainWindow

class NotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")

app = QApplication([])
win = NotesWindow()
win.show()
app.exec()
```

### Solution 2
```python
from PyQt6.QtWidgets import QPushButton
button = QPushButton("Add note")
```

### Solution 3
```python
layout = QVBoxLayout()
layout.addWidget(button)
container = QWidget()
container.setLayout(layout)
self.setCentralWidget(container)
```

### Solution 4
```python
button.clicked.connect(self.add_note)
```

### Solution 5
```python
from PyQt6.QtWidgets import QListWidget
self.list_widget = QListWidget()
layout.addWidget(self.list_widget)
```

### Solution 6
```python
from PyQt6.QtWidgets import QLineEdit
self.edit = QLineEdit()
layout.addWidget(self.edit)
```

### Solution 7
```python
app = QApplication([])
win = NotesWindow()
win.show()
app.exec()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is PyQt?
- GUI toolkit
- Web framework
- Database
- None
* Correct answer: GUI toolkit
Desktop.

What is a widget?
- UI element
- A signal
- A layout
- None
* Correct answer: UI element
Button.

What is a layout?
- Arranges widgets
- Draws
- Signals
- None
* Correct answer: Arranges widgets
VBox.

What is a signal?
- Event
- Widget
- Layout
- None
* Correct answer: Event
clicked.

What is connect?
- Binds handler
- Draws
- Stops
- None
* Correct answer: Binds handler
Slot.

What is QMainWindow?
- Main frame
- Button
- Layout
- None
* Correct answer: Main frame
Window.

What is setCentralWidget?
- Places main widget
- Adds layout
- Shows
- None
* Correct answer: Places main widget
Center.

What is app.exec?
- Event loop
- Starts only
- Stops
- None
* Correct answer: Event loop
Run.

What is show?
- Displays
- Hides
- Closes
- None
* Correct answer: Displays
Window.

What is QLineEdit?
- Text input
- Button
- List
- None
* Correct answer: Text input
Field.

What is QListWidget?
- Item list
- Input
- Layout
- None
* Correct answer: Item list
Notes.

What is a slot?
- Handler function
- Signal
- Widget
- None
* Correct answer: Handler function
Method.
<!--/QUIZ-->
