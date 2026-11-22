---
title: Dialogs and file dialogs
summary: QFileDialog, QMessageBox.
order: 3
duration: 45 min
difficulty: intermediate
tags: pyqt, dialogs
---

Dialogs ask the user for decisions.

## File open

```python
from PyQt6.QtWidgets import QFileDialog

filename, _ = QFileDialog.getOpenFileName(
    self, "Open file", "", "Text files (*.txt)"
)
if filename:
    with open(filename, encoding="utf-8") as f:
        text = f.read()
```

## Warning

```python
from PyQt6.QtWidgets import QMessageBox

QMessageBox.warning(self, "Error", "File not found")
```

## Lesson summary

Standard dialogs for files and messages.

<!--TASK-->
### Task 1 — Open
Open a file dialog.

### Task 2 — Read
Read the chosen file.

### Task 3 — Save
Save dialog.

### Task 4 — Write
Write text to a file.

### Task 5 — Info
Show an info box.

### Task 6 — Question
Ask yes/no.

### Task 7 — Error
Show a warning.
<!--/TASK-->

<!--HINT-->
### Hint 1
getOpenFileName.

### Hint 2
open().

### Hint 3
getSaveFileName.

### Hint 4
write().

### Hint 5
information.

### Hint 6
question.

### Hint 7
warning.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from PyQt6.QtWidgets import QFileDialog

filename, _ = QFileDialog.getOpenFileName(self, "Open file")
```

### Solution 2
```python
if filename:
    with open(filename, encoding="utf-8") as f:
        text = f.read()
```

### Solution 3
```python
filename, _ = QFileDialog.getSaveFileName(self, "Save file")
```

### Solution 4
```python
if filename:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
```

### Solution 5
```python
QMessageBox.information(self, "Done", "Saved")
```

### Solution 6
```python
answer = QMessageBox.question(self, "Quit", "Really quit?")
if answer == QMessageBox.StandardButton.Yes:
    self.close()
```

### Solution 7
```python
QMessageBox.warning(self, "Error", "File not found")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a dialog?
- Popup window
- Main window
- Layout
- None
* Correct answer: Popup window
Ask.

What is QFileDialog?
- File picker
- Message box
- Font
- None
* Correct answer: File picker
Open.

What is getOpenFileName?
- Choose file
- Choose folder
- Save
- None
* Correct answer: Choose file
Read.

What is getSaveFileName?
- Choose save path
- Open
- Delete
- None
* Correct answer: Choose save path
Write.

What is a filter?
- Extensions
- Size
- Path
- None
* Correct answer: Extensions
*.txt.

What is QMessageBox?
- Message popup
- File dialog
- Layout
- None
* Correct answer: Message popup
Info.

What is warning?
- Alert
- Info
- Question
- None
* Correct answer: Alert
Red.

What is information?
- Notice
- Warning
- Error
- None
* Correct answer: Notice
Blue.

What is question?
- Yes/no
- Info
- Open
- None
* Correct answer: Yes/no
Choice.

What is StandardButton?
- Yes/No enum
- Dialog
- File
- None
* Correct answer: Yes/No enum
Answer.

What is filename?
- Chosen path
- Text
- Dialog
- None
* Correct answer: Chosen path
Result.

What is the tuple?
- (path, filter)
- (user, pass)
- (x, y)
- None
* Correct answer: (path, filter)
Unpack.
<!--/QUIZ-->
