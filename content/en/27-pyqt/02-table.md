---
title: Model/View: QTableWidget
summary: Tables, rows, data manipulation.
order: 2
duration: 50 min
difficulty: advanced
tags: pyqt, table
---

Tables display structured data.

## QTableWidget

```python
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(3, 2)
        self.table.setHorizontalHeaderLabels(["Name", "Age"])
        self.table.setItem(0, 0, QTableWidgetItem("Alice"))
        self.table.setItem(0, 1, QTableWidgetItem("30"))
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
```

## Read

```python
item = self.table.item(0, 0)
print(item.text())
```

## Lesson summary

QTableWidget gives a data grid quickly.

<!--TASK-->
### Task 1 — Table
Create 3×2 table.

### Task 2 — Headers
Set column labels.

### Task 3 — Items
Fill two cells.

### Task 4 — Read
Read a cell.

### Task 5 — Row
Add a row.

### Task 6 — Select
Get selected row.

### Task 7 — Save
Export to CSV.
<!--/TASK-->

<!--HINT-->
### Hint 1
QTableWidget.

### Hint 2
setHorizontalHeaderLabels.

### Hint 3
setItem.

### Hint 4
item().

### Hint 5
insertRow.

### Hint 6
currentRow.

### Hint 7
Writer.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
self.table = QTableWidget(3, 2)
```

### Solution 2
```python
self.table.setHorizontalHeaderLabels(["Name", "Age"])
```

### Solution 3
```python
self.table.setItem(0, 0, QTableWidgetItem("Alice"))
self.table.setItem(0, 1, QTableWidgetItem("30"))
```

### Solution 4
```python
item = self.table.item(0, 0)
print(item.text())
```

### Solution 5
```python
row = self.table.rowCount()
self.table.insertRow(row)
self.table.setItem(row, 0, QTableWidgetItem("Bob"))
```

### Solution 6
```python
row = self.table.currentRow()
```

### Solution 7
```python
import csv
with open("table.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for r in range(self.table.rowCount()):
        row = []
        for c in range(self.table.columnCount()):
            item = self.table.item(r, c)
            row.append(item.text() if item else "")
        w.writerow(row)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a table widget?
- Grid display
- Layout
- Input
- None
* Correct answer: Grid display
Rows.

What is a cell?
- One item
- Row
- Column
- None
* Correct answer: One item
Item.

What is QTableWidgetItem?
- Cell data
- Table
- Header
- None
* Correct answer: Cell data
Text.

What is setItem?
- Fills cell
- Reads
- Deletes
- None
* Correct answer: Fills cell
Write.

What is item()?
- Reads cell
- Writes
- Inserts
- None
* Correct answer: Reads cell
Text.

What is rowCount?
- Number of rows
- Columns
- Cells
- None
* Correct answer: Number of rows
Count.

What is insertRow?
- Adds row
- Removes
- Reads
- None
* Correct answer: Adds row
End.

What is currentRow?
- Selected row
- All rows
- First
- None
* Correct answer: Selected row
Index.

What is a header?
- Column/row label
- Data
- Item
- None
* Correct answer: Column/row label
Names.

What is CSV?
- Export format
- Binary
- Image
- None
* Correct answer: Export format
Table.

What is selection?
- Highlighted
- Added
- Deleted
- None
* Correct answer: Highlighted
Row.

What is the benefit?
- Fast data UI
- Drawing
- Audio
- None
* Correct answer: Fast data UI
Grid.
<!--/QUIZ-->
