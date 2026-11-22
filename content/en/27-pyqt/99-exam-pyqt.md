---
title: Exam: PyQt6 and PySide6
summary: Final exam for the "PyQt6 and PySide6" module: widgets, signals, layouts, dialogs, models, styles and threads.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: PyQt6, PySide6, exam
---

<!--QUIZ-->
What must be created before any widgets in PyQt6?
- QMainWindow
- QApplication
- QLabel
* Correct answer: QApplication
QApplication manages the application; widgets are created after it.

What does the app.exec() method do?
- Shows all windows
- Starts the event loop and returns control only on exit
- Terminates the program instantly
* Correct answer: Starts the event loop and returns control only on exit
exec() processes events until the application closes.

How to correctly connect the function handle_click to a button press?
- button.clicked.connect(handle_click())
- button.clicked.connect(handle_click)
- button.clicked = handle_click
* Correct answer: button.clicked.connect(handle_click)
The function is passed without parentheses — otherwise it runs immediately.

How to declare a custom signal that passes a string in PyQt6?
- signal = Signal(str)
- greeted = pyqtSignal(str)
- self.signal = str()
* Correct answer: greeted = pyqtSignal(str)
In PyQt6 signals are declared as a class attribute via pyqtSignal; in PySide6 — via Signal.

Which layout is best for a "label → field" form?
- QVBoxLayout
- QFormLayout
- QGridLayout
* Correct answer: QFormLayout
QFormLayout aligns labels and fields into columns itself.

What does QInputDialog.getText return?
- Only a string
- A tuple (text, ok)
- A list of options
* Correct answer: A tuple (text, ok)
The second element indicates whether the user confirmed the input.

Which signal does QAction emit on activation?
- clicked
- triggered
- activated
* Correct answer: triggered
triggered fires when an action is chosen from a menu, toolbar, or by a key.

What does the model store in the Model/View architecture?
- The appearance
- Data and access rules
- The window position
* Correct answer: Data and access rules
The model is responsible for data; the view for displaying it.

Why is QSortFilterProxyModel needed?
- To speed up rendering
- To filter and sort without changing the source model
- To create new windows
* Correct answer: To filter and sort without changing the source model
The proxy sits between the model and the view.

How in QSS to address a widget with objectName="okButton"?
- QPushButton.okButton
- #okButton
- .okButton
* Correct answer: #okButton
The selector with a hash # selects a widget by objectName.
<!--/QUIZ-->
