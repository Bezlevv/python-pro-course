---
title: Excel: openpyxl formulas and styles
summary: Cells, formulas, formatting.
order: 2
duration: 50 min
difficulty: intermediate
tags: openpyxl, excel
---

openpyxl reads and writes .xlsx.

## Workbook

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sales"
```

## Values and formulas

```python
ws["A1"] = "Product"
ws["B1"] = "Amount"
ws["A2"] = "Pens"
ws["B2"] = 100
ws["B3"] = "=SUM(B2:B2)"
```

## Style

```python
from openpyxl.styles import Font, PatternFill

ws["A1"].font = Font(bold=True)
ws["A1"].fill = PatternFill(start_color="FFFF00", fill_type="solid")
```

## Lesson summary

Cells, formulas, styles.

<!--TASK-->
### Task 1 — Workbook
Create and name a sheet.

### Task 2 — Values
Write a header row.

### Task 3 — Formula
Add SUM.

### Task 4 — Read
Load and print values.

### Task 5 — Bold
Bold header.

### Task 6 — Fill
Color a cell.

### Task 7 — Save
Save the workbook.
<!--/TASK-->

<!--HINT-->
### Hint 1
Workbook.

### Hint 2
Cells.

### Hint 3
=SUM.

### Hint 4
load_workbook.

### Hint 5
Font.

### Hint 6
PatternFill.

### Hint 7
save.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "Sales"
```

### Solution 2
```python
ws["A1"] = "Product"
ws["B1"] = "Amount"
ws["A2"] = "Pens"
ws["B2"] = 100
```

### Solution 3
```python
ws["B3"] = "=SUM(B2:B2)"
```

### Solution 4
```python
from openpyxl import load_workbook
wb = load_workbook("sales.xlsx")
ws = wb["Sales"]
print(ws["A2"].value)
```

### Solution 5
```python
from openpyxl.styles import Font
ws["A1"].font = Font(bold=True)
```

### Solution 6
```python
from openpyxl.styles import PatternFill
ws["A1"].fill = PatternFill(start_color="FFFF00", fill_type="solid")
```

### Solution 7
```python
wb.save("sales.xlsx")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is openpyxl?
- Excel library
- Word
- PDF
- None
* Correct answer: Excel library
xlsx.

What is Workbook?
- File object
- Sheet
- Cell
- None
* Correct answer: File object
Create.

What is ws?
- Sheet
- Workbook
- Cell
- None
* Correct answer: Sheet
Active.

What is a cell?
- One box
- Sheet
- Workbook
- None
* Correct answer: One box
A1.

What is a formula?
- =SUM(...)
- Value
- Style
- None
* Correct answer: =SUM(...)
Calculated.

What is value?
- Content
- Style
- Formula only
- None
* Correct answer: Content
Read.

What is Font?
- Text formatting
- Fill
- Border
- None
* Correct answer: Text formatting
Bold.

What is PatternFill?
- Cell color
- Font
- Number
- None
* Correct answer: Cell color
Fill.

What is bold?
- Weight
- Size
- Color
- None
* Correct answer: Weight
Font.

What is save?
- Writes file
- Opens
- Closes
- None
* Correct answer: Writes file
Name.

What is load_workbook?
- Opens file
- Creates
- Deletes
- None
* Correct answer: Opens file
Read.

What is the benefit?
- Office automation
- Manual
- Required
- None
* Correct answer: Office automation
Reports.
<!--/QUIZ-->
