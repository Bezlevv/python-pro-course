---
title: Model/View Architecture and Delegates
summary: The Model/View architecture: QListView and QTableView, QStandardItemModel, item roles, selection, and custom delegates via QStyledItemDelegate.
order: 5
duration: 45 min
difficulty: advanced
tags: PyQt6, PySide6, QListView, QTableView, QStandardItemModel, QStyledItemDelegate, delegates, model-view
---

`QListWidget` and `QTableWidget` are convenient but store data inside themselves. In real applications data often lives separately — in a database, an API, a large list of objects. For this Qt has the **Model/View** architecture: the **model** stores data, while the **view** displays it and lets the user edit it. One view can show one model, and one model can be shown by several views at once.

## How it works

Three participants:

1. **Model** (`QStandardItemModel` and similar) — data and access rules;
2. **View** (`QListView`, `QTableView`, `QTreeView`) — how data looks on screen;
3. **Delegate** (`QStyledItemDelegate`) — how individual cells are drawn and edited.

Code links the model and the view:

```python
view.setModel(model)
```

## QStandardItemModel — universal model

`QStandardItemModel` is a general-purpose model that stores `QStandardItem` elements:

```python
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QListView

model = QStandardItemModel()
for name in ["Anna", "Peter", "Olga"]:
    item = QStandardItem(name)
    model.appendRow(item)

view = QListView()
view.setModel(model)
```

Each element is a `QStandardItem` object. It has text, an icon, permission flags, and **roles**.

## Roles

Data in an item is stored under "roles" — named slots for different purposes. The main ones:

- `Qt.ItemDataRole.DisplayRole` — the text that is shown;
- `Qt.ItemDataRole.EditRole` — the text for editing;
- `Qt.ItemDataRole.ToolTipRole` — a tooltip;
- `Qt.ItemDataRole.CheckStateRole` — the checkbox state;
- `Qt.ItemDataRole.ForegroundRole` — the text color;
- `Qt.ItemDataRole.FontRole` — the font.

```python
item = QStandardItem("Important")
item.setToolTip("This item is important")
item.setForeground(QBrush(QColor("red")))
item.setCheckable(True)          # enable checkbox
```

Values can be read via `item.data(role)` or the short methods `item.text()`, `item.isCheckable()`.

## QTableView and QStandardItemModel

For a table the model is built via `setItem(row, col, item)`:

```python
from PyQt6.QtWidgets import QTableView, QHeaderView

model = QStandardItemModel(0, 3)   # 0 rows, 3 columns
model.setHorizontalHeaderLabels(["Name", "Grade", "Status"])

model.appendRow([
    QStandardItem("Anna"),
    QStandardItem("5"),
    QStandardItem("Excellent"),
])
model.appendRow([
    QStandardItem("Peter"),
    QStandardItem("4"),
    QStandardItem("Good"),
])

table = QTableView()
table.setModel(model)
table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
```

`appendRow` takes a list of items — one per column. Headers are set via `setHorizontalHeaderLabels`.

## Selection and current item

The view manages selection itself. The current item is accessible via `selectionModel` and `currentIndex`:

```python
def on_current_changed(current, previous):
    if current.isValid():
        print("Selected:", current.data())

table.selectionModel().currentChanged.connect(on_current_changed)
```

`QModelIndex` is the "address" of a cell. `isValid()` tells whether a real item lies behind the index; `data()` reads DisplayRole. For tables an index has `row()` and `column()`.

## Sorting and proxy models

The model can be sorted, and a **proxy model** can be inserted between the model and the view to filter or sort without touching the source data:

```python
from PyQt6.QtCore import QSortFilterProxyModel, Qt

proxy = QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
proxy.setFilterFixedString("A")

view.setModel(proxy)
```

`QSortFilterProxyModel` is a basic filter: `setFilterFixedString` keeps rows containing the substring. The view now works with the proxy while the source model remains unchanged.

## Delegates: how cells are drawn

A delegate handles cell rendering and editing. By default `QStyledItemDelegate` is used, but it can be overridden. A custom delegate is a class inheriting `QStyledItemDelegate` that overrides methods:

- `paint()` — how to draw the cell;
- `sizeHint()` — what size the cell needs;
- `createEditor()` — which widget to use for editing.

A classic example — a column with progress bars:

```python
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle, QApplication
from PyQt6.QtCore import Qt

class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        progress = int(index.data()) or 0
        # draw the standard cell frame
        super().paint(painter, option, index)
        # and on top — a progress scale
        opt = QStyleOptionProgressBar()
        opt.rect = option.rect.adjusted(4, 4, -4, -4)
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        QApplication.style().drawControl(
            QStyle.ControlElement.CE_ProgressBar, opt, painter
        )

table.setItemDelegateForColumn(2, ProgressDelegate(table))
```

`setItemDelegateForColumn(col, delegate)` assigns a delegate to a specific column. Note: `index.data()` returns the value from the model, and `option.rect` is the cell rectangle. Custom delegates are a powerful tool: you can draw charts, photos, and colored indicators in them.

## Lesson summary

- The model stores data, the view displays it; the link is `view.setModel(model)`;
- `QStandardItemModel` — a universal model; data lies under roles (`DisplayRole` and others);
- `QListView` and `QTableView` — views; selection is read via `selectionModel`;
- `QSortFilterProxyModel` filters and sorts without modifying the model;
- delegates (`QStyledItemDelegate`) override cell rendering and editing.

Now tasks.

<!--TASK-->
### Task 1
Create a `QListView` with a `QStandardItemModel` filled with five programming languages (Python, Java, C++, JavaScript, Go). When the selection changes, print the text of the selected item to the console. Make sure nothing prints on the first launch until you click an item.

### Task 2
Create a `QTableView` with a model of 5 rows and 3 columns: Name, City, Age. Fill it with any data. Column headers — "Name", "City", "Age". Make it so that clicking a cell prints `Row 2, column 1: Moscow` to the console (with the actual numbers and text).

### Task 3
Add sorting to the table from task 2: make the column headers clickable (sort on click). Use `setSortingEnabled(True)` on the view — the model itself must be sorted. Verify that clicking the "Age" header orders the rows by age.

### Task 4
Place a `QSortFilterProxyModel` between the model and the view. Add a `QLineEdit` input field to the window; as text is typed, the model must filter rows whose name contains the typed substring (case-insensitive). For example, typing "an" leaves only rows with "Anna", "Anne", etc.

### Task 5
Create a table with numbers 0–100 in the third column and a custom delegate `ProgressDelegate` that draws progress bars in that column (as in the theory example). The other columns must look standard. Make sure the progress bars are visible and stretch with the window.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create a model `QStandardItemModel()`, for each language — `QStandardItem(lang)` and `model.appendRow(item)`. Then `view.setModel(model)`. Selection: `view.selectionModel().currentChanged.connect(handler)`, where handler takes `(current, previous)` and prints `current.data()` when `current.isValid()`.

### Hint 2
Create a model `QStandardItemModel(0, 3)` and set headers via `setHorizontalHeaderLabels(["Name", "City", "Age"])`. Add rows via `model.appendRow([QStandardItem(...), ...])`. Read the current cell via `table.selectionModel().currentChanged.connect(handler)`; inside — `current.row()`, `current.column()`, `current.data()`.

### Hint 3
Call `table.setSortingEnabled(True)` on the view. Clicking a header enables sorting. Important: when filling the model **after** enabling sorting, rows may jump around — fill the model before `setSortingEnabled(True)`, or sort manually via `model.sort(...)`.

### Hint 4
Create `proxy = QSortFilterProxyModel()`, then `proxy.setSourceModel(model)` and `view.setModel(proxy)`. In the slot `edit.textChanged.connect(handler)` call `proxy.setFilterFixedString(text)`. If the text is empty — the filter disables itself (an empty string excludes nothing).

### Hint 5
Define the class `ProgressDelegate(QStyledItemDelegate)` with a `paint` method as in the theory: `super().paint(...)`, then `QStyleOptionProgressBar`, `opt.progress = int(index.data())`, and `QApplication.style().drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter)`. Connect it: `table.setItemDelegateForColumn(2, ProgressDelegate(table))`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QListView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Languages")
window.resize(300, 250)

model = QStandardItemModel()
for lang in ["Python", "Java", "C++", "JavaScript", "Go"]:
    model.appendRow(QStandardItem(lang))

view = QListView()
view.setModel(model)

def on_current_changed(current, previous):
    if current.isValid():
        print("Selected:", current.data())

view.selectionModel().currentChanged.connect(on_current_changed)

layout = QVBoxLayout(window)
layout.addWidget(view)

window.show()
sys.exit(app.exec())
```

What's happening here? The model lives separately from the view: we fill it with items without touching `QListView`. `view.setModel(model)` links them. The `currentChanged` signal fires when the current item changes and passes two `QModelIndex` objects — the new and the old one. `current.isValid()` checks that the index points to an existing cell, and `current.data()` returns the text (DisplayRole). Nothing prints at startup because the current item isn't selected yet — the signal will fire only after a click.

### Walkthrough 2
Solution:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Table")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Name", "City", "Age"])

rows = [
    ("Anna", "Moscow", "25"),
    ("Peter", "Kazan", "30"),
    ("Olga", "Sochi", "22"),
    ("Igor", "Pskov", "35"),
    ("Marina", "Yekaterinburg", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

table = QTableView()
table.setModel(model)

def on_current_changed(current, previous):
    if current.isValid():
        print(f"Row {current.row()}, column {current.column()}: "
              f"{current.data()}")

table.selectionModel().currentChanged.connect(on_current_changed)

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Clicking the "Moscow" cell prints:

```
Row 0, column 1: Moscow
```

What's happening here? `QStandardItemModel(0, 3)` creates a model with 0 rows and 3 columns. Each `appendRow` adds a row of three `QStandardItem`s. `setHorizontalHeaderLabels` sets the headers. The cell position is `current.row()` and `current.column()`: indexes start at zero, so the "Anna" row has number 0.

### Walkthrough 3
Solution:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Sorting")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Name", "City", "Age"])

rows = [
    ("Anna", "Moscow", "25"),
    ("Peter", "Kazan", "30"),
    ("Olga", "Sochi", "22"),
    ("Igor", "Pskov", "35"),
    ("Marina", "Yekaterinburg", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

table = QTableView()
table.setModel(model)
table.setSortingEnabled(True)   # clicking a header sorts

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

What's happening here? `setSortingEnabled(True)` gives the view the right to sort the model when a column header is clicked. Qt builds an invisible "sorting" memory and rearranges the model's rows. An important nuance: items are stored as strings, so sorting by "Age" will be **lexicographic** — "22", "25", "28", "30", "35" match the numeric order, but three-digit numbers would land incorrectly. For honest numeric sorting you need to store numbers via `item.setData(value, Qt.ItemDataRole.EditRole)` or use `QSortFilterProxyModel.setSortRole`.

### Walkthrough 4
Solution:

```python
import sys
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QWidget, QTableView,
                             QLineEdit, QVBoxLayout)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Filter")
window.resize(400, 300)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Name", "City", "Age"])

rows = [
    ("Anna", "Moscow", "25"),
    ("Peter", "Kazan", "30"),
    ("Olga", "Sochi", "22"),
    ("Anne", "Pskov", "35"),
    ("Marina", "Yekaterinburg", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

proxy = QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

table = QTableView()
table.setModel(proxy)

edit = QLineEdit()
edit.setPlaceholderText("Filter by name…")

def apply_filter(text):
    proxy.setFilterFixedString(text)

edit.textChanged.connect(apply_filter)

layout = QVBoxLayout(window)
layout.addWidget(edit)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Type "an" — "Anna" and "Anne" remain. What's happening here? The proxy model stands between the model and the view: `table.setModel(proxy)`, and `proxy` wraps the source `model`. `setFilterFixedString` enables a filter by exact substring match in DisplayRole — by default the first column is checked. `setFilterCaseSensitivity(CaseInsensitive)` makes the search case-insensitive. An empty filter string excludes nothing, so clearing the field returns all rows. The proxy doesn't touch the source model — an important property of the architecture.

### Walkthrough 5
Solution:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QWidget, QTableView,
                             QVBoxLayout, QStyledItemDelegate,
                             QStyleOptionProgressBar, QStyle, QApplication as QtApp)

class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        progress = int(index.data() or 0)
        if not 0 <= progress <= 100:
            return
        opt = QStyleOptionProgressBar()
        opt.rect = option.rect.adjusted(4, 4, -4, -4)
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        QtApp.style().drawControl(
            QStyle.ControlElement.CE_ProgressBar, opt, painter
        )

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Progress delegate")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Task", "Owner", "Progress"])

tasks = [
    ("Parsing", "Anna", 80),
    ("UI", "Peter", 45),
    ("Tests", "Olga", 100),
    ("Documentation", "Igor", 15),
]
for task, owner, progress in tasks:
    model.appendRow([QStandardItem(task),
                     QStandardItem(owner),
                     QStandardItem(str(progress))])

table = QTableView()
table.setModel(model)
table.setItemDelegateForColumn(2, ProgressDelegate(table))

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

What's happening here? `ProgressDelegate.paint` is called for every visible cell of the third column. First `super().paint(...)` draws the standard background and frame, then on `option.rect` (the cell rectangle) with 4-pixel insets a styled progress bar is overlaid: `QStyleOptionProgressBar` describes the desired state, and `drawControl(CE_ProgressBar, opt, painter)` renders it using the current style theme. The value is read from the model via `index.data()`. For the other columns no delegate is assigned, so they render by default.
<!--/SOLUTION-->

<!--QUIZ-->
What does the model store in the Model/View architecture?
- Only the appearance
- Data and access rules
- The window position
* Correct answer: Data and access rules
The model is responsible for data; the view for displaying it.

How to link a model with a view?
- view.addWidget(model)
- view.setModel(model)
- model.setView(view)
* Correct answer: view.setModel(model)
The view receives the model via setModel.

Which class is a universal model of standard items?
- QTableWidget
- QStandardItemModel
- QModelIndex
* Correct answer: QStandardItemModel
QStandardItemModel stores QStandardItem elements and can hand them to views.

What does index.data() return (item index)?
- An address string
- The DisplayRole value
- A widget object
* Correct answer: The DisplayRole value
data() without arguments reads DisplayRole — the text shown in the cell.

What does item.setCheckable(True) mean?
- The item cannot be deleted
- The item gets a checkbox
- The item becomes invisible
* Correct answer: The item gets a checkbox
The checkbox is stored in the CheckStateRole role and is controlled by the user.

How to get the row number of the current cell?
- index.row()
- index.line()
- index.number()
* Correct answer: index.row()
QModelIndex.row() returns the row number, column() — the column.

Why is QSortFilterProxyModel needed?
- To speed up rendering
- To filter and sort without changing the source model
- To merge several windows
* Correct answer: To filter and sort without changing the source model
The proxy sits between the model and the view and modifies the "view" of the data.

What does table.setSortingEnabled(True) do?
- Enables sorting by clicking a column header
- Forbids changing the row order
- Sorts at startup
* Correct answer: Enables sorting by clicking a column header
Clicking a header sorts the rows by that column.

Which methods does a custom delegate override?
- paint, sizeHint, createEditor
- draw, resize, move
- update, insert, delete
* Correct answer: paint, sizeHint, createEditor
paint draws the cell, sizeHint sets the size, createEditor creates the editor.

How to assign a delegate to only the third column?
- table.setDelegate(delegate)
- table.setItemDelegateForColumn(2, delegate)
- table.setColumnDelegate(3, delegate)
* Correct answer: table.setItemDelegateForColumn(2, delegate)
setItemDelegateForColumn(column_index, delegate) applies a delegate to one column.
<!--/QUIZ-->
