---
title: PyQt6: widgets and layouts
summary: Common widgets, arrangement.
order: 1
duration: 45 min
difficulty: intermediate
tags: pyqt, widgets
---

PyQt6 builds rich desktop UIs.

## Widgets

```python
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.label = QLabel("Name:")
        self.edit = QLineEdit()
        self.button = QPushButton("OK")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        print(self.edit.text())

app = QApplication([])
form = Form()
form.show()
app.exec()
```

## Lesson summary

Widgets + layouts + signals.

<!--TASK-->
### Task 1 — Window
Create a QWidget form.

### Task 2 — Label
Add QLabel.

### Task 3 — Edit
Add QLineEdit.

### Task 4 — Button
Add QPushButton.

### Task 5 — Layout
Arrange vertically.

### Task 6 — Signal
Print on click.

### Task 7 — Run
Run the app.
<!--/TASK-->

<!--HINT-->
### Hint 1
QWidget.

### Hint 2
QLabel.

### Hint 3
QLineEdit.

### Hint 4
QPushButton.

### Hint 5
QVBoxLayout.

### Hint 6
clicked.

### Hint 7
app.exec.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from PyQt6.QtWidgets import QWidget

class Form(QWidget):
    def __init__(self):
        super().__init__()
```

### Solution 2
```python
self.label = QLabel("Name:")
```

### Solution 3
```python
self.edit = QLineEdit()
```

### Solution 4
```python
self.button = QPushButton("OK")
```

### Solution 5
```python
layout = QVBoxLayout()
layout.addWidget(self.label)
layout.addWidget(self.edit)
layout.addWidget(self.button)
self.setLayout(layout)
```

### Solution 6
```python
self.button.clicked.connect(self.on_click)

def on_click(self):
    print(self.edit.text())
```

### Solution 7
```python
app = QApplication([])
form = Form()
form.show()
app.exec()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a widget?
- UI element
- Event
- Layout
- None
* Correct answer: UI element
Control.

What is QLabel?
- Text
- Input
- Button
- None
* Correct answer: Text
Label.

What is QLineEdit?
- Text input
- Label
- Layout
- None
* Correct answer: Text input
Field.

What is QPushButton?
- Button
- Input
- Label
- None
* Correct answer: Button
Click.

What is a layout?
- Arrangement
- Widget
- Signal
- None
* Correct answer: Arrangement
VBox.

What is addWidget?
- Adds to layout
- Removes
- Shows
- None
* Correct answer: Adds to layout
Insert.

What is setLayout?
- Applies layout
- Creates
- Deletes
- None
* Correct answer: Applies layout
Parent.

What is clicked?
- Signal
- Widget
- Layout
- None
* Correct answer: Signal
Event.

What is connect?
- Binds handler
- Draws
- Stops
- None
* Correct answer: Binds handler
Slot.

What is text()?
- Reads input
- Sets
- Clears
- None
* Correct answer: Reads input
Getter.

What is show?
- Displays
- Hides
- Closes
- None
* Correct answer: Displays
Window.

What is exec?
- Event loop
- Start
- Stop
- None
* Correct answer: Event loop
Run.
<!--/QUIZ-->
