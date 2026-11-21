---
title: Working with Excel: openpyxl
summary: Creating workbooks, writing cells, styles, formulas and reading data.
order: 8
duration: 40 min
difficulty: intermediate
tags: excel, openpyxl, sheets
---

openpyxl reads and writes .xlsx files.

## Create workbook

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sales"
ws["A1"] = "Product"
ws["B1"] = "Price"
ws.append(["Pen", 10])
wb.save("book.xlsx")
```

## Load and read

```python
from openpyxl import load_workbook
wb = load_workbook("book.xlsx")
ws = wb["Sales"]
print(ws["A1"].value)
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
```

## Styles

```python
from openpyxl.styles import Font, PatternFill
ws["A1"].font = Font(bold=True)
ws["A1"].fill = PatternFill("solid", fgColor="FFFF00")
```

## Formulas

```python
ws["C1"] = "=SUM(B2:B10)"
```

## Lesson summary

openpyxl creates/reads Excel files: cells, rows, styles, formulas.

<!--TASK-->
### Task 1 — Create
Create a workbook, add a sheet "Data", write headers.

### Task 2 — Rows
Append 3 data rows using ws.append.

### Task 3 — Read
Load the file and read all rows with iter_rows.

### Task 4 — Cell access
Read a specific cell A1; set B2 and save.

### Task 5 — Bold header
Style headers with Font(bold=True).

### Task 6 — Fill color
Fill header cells with a color.

### Task 7 — Formula
Add a SUM formula and verify the saved value on reload.
<!--/TASK-->

<!--HINT-->
### Hint 1
wb = Workbook(); ws = wb.active.

### Hint 2
ws.append([...]).

### Hint 3
load_workbook; iter_rows(values_only=True).

### Hint 4
ws["B2"] = 5.

### Hint 5
Font(bold=True).

### Hint 6
PatternFill("solid", fgColor="FFFF00").

### Hint 7
ws["C1"] = "=SUM(B2:B10)".
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "Data"
ws["A1"] = "Name"
ws["B1"] = "Value"
wb.save("book.xlsx")
```

### Solution 2
```python
ws.append(["Anna", 10])
ws.append(["Boris", 20])
ws.append(["Vika", 30])
wb.save("book.xlsx")
```

### Solution 3
```python
from openpyxl import load_workbook
wb = load_workbook("book.xlsx")
ws = wb["Data"]
for row in ws.iter_rows(values_only=True):
    print(row)
```

### Solution 4
```python
print(ws["A1"].value)
ws["B2"] = 5
wb.save("book.xlsx")
```

### Solution 5
```python
from openpyxl.styles import Font
for cell in ws[1]:
    cell.font = Font(bold=True)
```

### Solution 6
```python
from openpyxl.styles import PatternFill
fill = PatternFill("solid", fgColor="FFFF00")
for cell in ws[1]:
    cell.fill = fill
```

### Solution 7
```python
ws["C1"] = "=SUM(B2:B10)"
wb.save("book.xlsx")
# при повторной загрузке формула сохраняется как строка/результат
```
<!--/SOLUTION-->

<!--QUIZ-->
What does openpyxl handle?
- .xlsx files
- CSV
- PDF
- JSON
* Correct answer: .xlsx files
Excel format.

What is Workbook?
- An Excel file object
- A sheet
- A cell
- A style
* Correct answer: An Excel file object
Root.

What is a worksheet?
- One sheet
- The file
- A cell
- A formula
* Correct answer: One sheet
ws.

How to set a cell?
- ws["A1"] = value
- ws.cell(1,1) both
- sheet.set
- cell.write
* Correct answer: ws["A1"] = value
Direct assignment.

What does append do?
- Adds a row at the end
- Overwrites
- Deletes
- Sorts
* Correct answer: Adds a row at the end
List of values.

How to load an existing file?
- load_workbook("file.xlsx")
- Workbook("file")
- open()
- read_excel
* Correct answer: load_workbook("file.xlsx")
Standard.

What does iter_rows do?
- Iterates over rows
- Writes rows
- Deletes
- Copies
* Correct answer: Iterates over rows
With values_only.

What is Font(bold=True)?
- A style
- A cell
- A sheet
- A formula
* Correct answer: A style
Formatting.

What is PatternFill?
- Cell fill color
- Font
- Border
- Align
* Correct answer: Cell fill color
Background.

Can cells hold formulas?
- Yes
- No
- Only text
- Only numbers
* Correct answer: Yes
"=SUM(...)".

What does save do?
- Writes the file
- Reads
- Deletes
- Prints
* Correct answer: Writes the file
Persist.

Which is a cell?
- ws["A1"]
- wb
- ws
- Workbook
* Correct answer: ws["A1"]
Coordinates.
<!--/QUIZ-->
