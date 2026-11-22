---
title: Excel and Word: Reports Automatically
summary: Let's automate office routine: create and format Excel spreadsheets with openpyxl, and Word documents with python-docx.
order: 4
duration: 35 min
difficulty: intermediate
tags: openpyxl, python-docx, excel, word, reports
---

"Report by Monday" — the phrase that makes any office worker flinch. Yet these are exactly the tasks Python handles perfectly: collect data, calculate totals, format the table. In this lesson we'll meet two libraries: `openpyxl` (Excel) and `python-docx` (Word).

## Installation

```bash
pip install openpyxl python-docx
```

## Creating an Excel File

Working with `openpyxl` starts with a workbook (`Workbook`) and a worksheet (`Worksheet`):

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sales"
```

You can add data cell by cell or as a whole row via `append()`:

```python
ws.append(["Product", "Quantity", "Price"])      # header
ws.append(["Laptop", 12, 75000])
ws.append(["Mouse", 48, 1500])
ws.append(["Keyboard", 20, 3500])
wb.save("sales.xlsx")
```

Formatting goes through styles: `Font` for the typeface, `PatternFill` for fills:

```python
from openpyxl.styles import Font, PatternFill

bold = Font(bold=True)
fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
for cell in ws[1]:                 # first row — header
    cell.font = bold
    cell.fill = fill
```

Column width is set with the `column_dimensions` attribute:

```python
ws.column_dimensions["A"].width = 15
```

## Reading Excel

Reading is no harder than writing:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
```

`iter_rows(values_only=True)` returns values row by row — convenient for summing.

## Creating a Word Document

`python-docx` builds a document from paragraphs and tables. Start with a heading:

```python
from docx import Document

doc = Document()
doc.add_heading("Sales Report", level=1)
doc.add_paragraph("Compiled automatically.")
doc.save("report.docx")
```

Tables are added with the `add_table` method:

```python
table = doc.add_table(rows=1, cols=3)
hdr = table.rows[0].cells
hdr[0].text = "Product"
hdr[1].text = "Quantity"
hdr[2].text = "Price"
```

As you can see, the principle is the same: create an object, fill it with data, save. Now let's build a real auto-report.

<!--TASK-->
### Task 1
Create an Excel file `sales.xlsx` with three columns: `Product`, `Quantity`, `Price`. Name the sheet `Sales`, add a header and three data rows (invent products yourself). Save the file via `wb.save("sales.xlsx")`. Expected result: the file appears next to the script and opens in Excel or LibreOffice.

### Task 2
Add formatting to the file from task 1: make the header bold with `Font(bold=True)`, add a yellow fill with `PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")`, and set column `A` width to 15. Expected result: when the file opens, the header is highlighted yellow and bold.

### Task 3
Read `sales.xlsx` back with `load_workbook` and print all data rows without the header (via `iter_rows(min_row=2, values_only=True)`), then the sum of the "Quantity" column. Expected result: three data rows in the console and a line `Total quantity: <sum>`.

### Task 4
Create a Word document `report.docx`: a heading `Sales Report` (level 1), an introductory paragraph, and a list of three items (you can use three `add_paragraph` calls with a hyphen at the start). Save the document. Expected result: an opening `report.docx` with a heading, text, and a list.

### Task 5
Write an auto-report program: read `sales.xlsx`, for each row compute revenue (`Quantity × Price`), build a Word table with `Product`, `Quantity`, `Revenue` columns and a total row `TOTAL` with the grand sum. Save as `report.docx`. Expected result: a document with a table and a total, and the total revenue in the console.
<!--/TASK-->

<!--HINT-->
### Hint 1
`wb = Workbook(); ws = wb.active; ws.title = "Sales"`. Add rows with `ws.append([...])`: header first, then data. At the end `wb.save("sales.xlsx")` — without saving, there is no file.

### Hint 2
After `from openpyxl.styles import Font, PatternFill`, create `bold = Font(bold=True)` and `fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")`. Walk over the header: `for cell in ws[1]: cell.font = bold; cell.fill = fill`. Width: `ws.column_dimensions["A"].width = 15`.

### Hint 3
`wb = load_workbook("sales.xlsx")`, `ws = wb.active`. Accumulate the sum while iterating `ws.iter_rows(min_row=2, values_only=True)`: in each row the element at index 1 is "Quantity". Print rows and the total after the loop.

### Hint 4
`doc = Document()`; `doc.add_heading("Sales Report", level=1)`; `doc.add_paragraph("Introduction...")`; list items are just paragraphs: `doc.add_paragraph("- item 1")` and so on; at the end `doc.save("report.docx")`.

### Hint 5
Assemble the algorithm: read Excel → create `Document()` → `add_heading` → `add_table(rows=1, cols=3)` → fill the table header → for each Excel row add a table row via `table.add_row().cells` → total row. Compute revenue as `qty * price`, accumulate the grand sum in a variable.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Sales"

ws.append(["Product", "Quantity", "Price"])
ws.append(["Laptop", 12, 75000])
ws.append(["Mouse", 48, 1500])
ws.append(["Keyboard", 20, 3500])

wb.save("sales.xlsx")
print("File sales.xlsx created")
```

What's going on here? `Workbook()` creates a new workbook with one empty sheet, and `wb.active` returns that sheet. `ws.title` changes its name. `append()` adds a whole row — values are distributed across cells left to right. Finally, `wb.save("sales.xlsx")` writes the workbook to disk. Note: without `save()` there will be no file — this is the most common beginner mistake.

### Solution 2
Solution:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Sales"

ws.append(["Product", "Quantity", "Price"])
ws.append(["Laptop", 12, 75000])
ws.append(["Mouse", 48, 1500])
ws.append(["Keyboard", 20, 3500])

bold = Font(bold=True)
fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for cell in ws[1]:
    cell.font = bold
    cell.fill = fill

ws.column_dimensions["A"].width = 15

wb.save("sales.xlsx")
```

What's going on here? Styles in openpyxl are objects assigned to cells. `Font(bold=True)` makes text bold, `PatternFill` fills a cell with color: `start_color` and `end_color` are colors in RRGGBB format (no hash), and `fill_type="solid"` means a solid fill. `ws[1]` accesses the first row (XLSX coordinates start at 1). Looping over the header cells is the simplest way to style a whole row. `column_dimensions["A"].width = 15` sets the width of column A.

### Solution 3
Solution:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active

total_qty = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    item, qty, price = row
    print(item, qty, price)
    total_qty += qty

print("Total quantity:", total_qty)
```

Result (example):

```
Laptop 12 75000
Mouse 48 1500
Keyboard 20 3500
Total quantity: 80
```

What's going on here? `load_workbook` opens an existing file. `iter_rows(min_row=2, values_only=True)` iterates rows starting from the second (the first is the header) and returns cell values as tuples. Unpacking `item, qty, price = row` is a clean way to split a tuple. In the loop we immediately accumulate the sum into `total_qty`. `values_only=True` is an important parameter: without it you'd get cell objects instead of their values.

### Solution 4
Solution:

```python
from docx import Document

doc = Document()
doc.add_heading("Sales Report", level=1)
doc.add_paragraph("This report was compiled automatically by a Python program.")
doc.add_paragraph("- Laptops")
doc.add_paragraph("- Mice")
doc.add_paragraph("- Keyboards")

doc.save("report.docx")
print("Document report.docx created")
```

What's going on here? `Document()` creates an empty Word document. `add_heading("...", level=1)` adds a level-1 heading — it gets the standard "Heading 1" style with a large font. `add_paragraph` adds ordinary paragraphs; list items here are simply formatted with hyphens at the start of the text (for a real bulleted list you could use the `List Bullet` style, but this variant also opens fine in Word). Everything is saved via `doc.save()`.

### Solution 5
Solution:

```python
from openpyxl import load_workbook
from docx import Document

wb = load_workbook("sales.xlsx")
ws = wb.active

doc = Document()
doc.add_heading("Sales Report", level=1)

table = doc.add_table(rows=1, cols=3)
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text = "Product", "Quantity", "Revenue"

total = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    item, qty, price = row
    revenue = qty * price
    total += revenue
    cells = table.add_row().cells
    cells[0].text = item
    cells[1].text = str(qty)
    cells[2].text = f"{revenue:.0f} rub."

row = table.add_row().cells
row[0].text = "TOTAL"
row[2].text = f"{total:.0f} rub."

doc.save("report.docx")
print("Done! Total revenue:", total)
```

What's going on here? This is a real auto-report. We read Excel, create a Word document and a one-row header table. For each data row we add a table row `table.add_row().cells`, fill the cells with text: revenue is quantity times price. The "TOTAL" row sums it up. One script run replaces an hour of manual office work — that's exactly what office automation is for.
<!--/SOLUTION-->

<!--QUIZ-->
How do you create a new Excel file in openpyxl?
- openpyxl.file()
- Workbook() and wb.save("file.xlsx")
- xl.create()
- sheet.make()
* Correct answer: Workbook() and wb.save("file.xlsx")
Workbook creates the workbook, and save writes it to disk.

What does ws.append([...]) do?
- Adds a row of values to the end of the sheet
- Deletes a row
- Renames the sheet
- Changes a cell color
* Correct answer: Adds a row of values to the end of the sheet
append() takes a list or tuple and writes it as the next row.

How is load_workbook different from Workbook?
- load_workbook reads an existing file, while Workbook creates a new one
- They are the same
- load_workbook creates a new workbook
- Workbook reads a file
* Correct answer: load_workbook reads an existing file, while Workbook creates a new one
load_workbook("file.xlsx") opens a file from disk; Workbook() starts from a blank sheet.

How do you make a cell's text bold?
- cell.bold = True
- Assign Font(bold=True) to the cell
- cell.style = "bold"
- cell.font_size = 14
* Correct answer: Assign Font(bold=True) to the cell
Styles in openpyxl are objects: create Font(bold=True) and assign it to cell.font.

How do you add a table to a Word document?
- doc.table.append(...)
- doc.add_table(rows=1, cols=3)
- doc.insert_table(...)
- table = doc.new_table(...)
* Correct answer: doc.add_table(rows=1, cols=3)
add_table creates a table with the given number of rows and columns.

How do you add a heading in python-docx?
- doc.add_title("...")
- doc.add_heading("...", level=1)
- doc.header("...")
- doc.add_text("...", style="heading")
* Correct answer: doc.add_heading("...", level=1)
add_heading adds a heading with the desired level, from 1 to 9.

What does ws[1] return in openpyxl?
- The first row of the sheet — all its cells
- The first column of the sheet
- The number of the active sheet
- The name of the first cell
* Correct answer: The first row of the sheet — all its cells
Row indexes in openpyxl start at 1, so ws[1] is the header, which is convenient to loop over.

How is add_heading different from add_paragraph in python-docx?
- add_heading creates a heading with a level, add_paragraph creates an ordinary paragraph
- They are synonyms
- add_paragraph adds a table
- add_heading inserts a picture
* Correct answer: add_heading creates a heading with a level, add_paragraph creates an ordinary paragraph
Level level=1..9 assigns the "Heading N" style, while ordinary text is added with add_paragraph.
<!--/QUIZ-->
