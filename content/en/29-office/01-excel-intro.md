---
title: "openpyxl in Depth: Workbooks, Styles, Formulas"
summary: Creating Excel workbooks, working with sheets and cells, styling, formulas, and saving files.
order: 1
duration: 45 min
difficulty: intermediate
tags: openpyxl, excel, workbook, styles, formulas
---

openpyxl is a library for reading and writing Excel files (`.xlsx`) in pure Python. It does not need Excel installed: creating workbooks, editing cells, styles, and formulas are all handled by the library itself. Installation:

```bash
pip install openpyxl
```

## Workbook and sheets

The main object is `Workbook` (a workbook). `Workbook()` creates a new workbook with one empty sheet.

```python
from openpyxl import Workbook

wb = Workbook()               # new workbook
ws = wb.active                # active (by default the first) sheet
ws.title = "Goods"           # rename the sheet
ws2 = wb.create_sheet("Warehouse")  # new sheet at the end
ws3 = wb["Goods"]            # access by name
```

A sheet is a `Worksheet` object. A workbook can have any number of sheets; you access them via `wb["Name"]` or `wb.worksheets`.

## Cells

You can refer to a cell in two ways: by name (as in Excel) or by coordinates.

```python
ws["A1"] = "hello"                    # write by name
ws.cell(row=1, column=2, value=42)     # write by coordinates

print(ws["A1"].value)                  # read the value
print(ws.cell(row=1, column=2).value)  # 42
```

To iterate over ranges, `iter_rows` is handy — it returns rows one by one. The `values_only=True` parameter immediately turns rows into tuples of values:

```python
for row in ws.iter_rows(min_row=1, max_row=3, min_col=1, max_col=2, values_only=True):
    print(row)
```

The properties `ws.max_row` and `ws.max_column` tell how many rows and columns are occupied by data. A workbook is saved with `wb.save("name.xlsx")`.

## Formulas

openpyxl writes a formula as a string, but **does not calculate it** — the calculation happens in Excel when the file is opened.

```python
ws["D2"] = "=B2*C2"   # cell D2 stores a formula
```

When you read the file again without the `data_only` flag, you will see the string itself, `=B2*C2`. If you open the file with `data_only=True`, openpyxl returns the cached formula result — but it appears only if the file was previously opened and saved in Excel. Otherwise, it will be `None`. So when your program needs the data, it is often simpler to calculate it yourself: `ws["D2"] = ws["B2"].value * ws["C2"].value`.

## Styles

Formatting is handled by classes from `openpyxl.styles`: `Font` (font), `PatternFill` (fill), `Alignment` (alignment), `Border` and `Side` (borders).

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

font = Font(bold=True, size=12, color="FFFFFF")          # white bold font
fill = PatternFill(fill_type="solid", fgColor="4472C4")  # blue fill
al = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

cell = ws["A1"]
cell.font = font
cell.fill = fill
cell.alignment = al
cell.border = border
```

The number format is set with a string: `cell.number_format = "#,##0.00"` — numbers will then show thousands separators and two decimal places.

## Organizing the sheet

You often need merged cells, a frozen header, and column sizes:

```python
ws.merge_cells("A1:C1")          # merge three cells
ws.unmerge_cells("A1:C1")        # undo the merge
ws.freeze_panes = "A2"           # freeze row 1 (the area above and to the left of A2)
ws.column_dimensions["A"].width = 30   # width of column A
ws.row_dimensions[1].height = 24       # height of row 1
```

## Complete example

Let's put it all together: a workbook with a header, styles, data, and a formula.

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Goods"

# header styles
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(fill_type="solid", fgColor="4472C4")
header_al = Alignment(horizontal="center", vertical="center")
thin = Side(style="thin", color="BFBFBF")
header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

headers = ["Name", "Price", "Quantity", "Cost"]
for col, name in enumerate(headers, start=1):
    c = ws.cell(row=1, column=col, value=name)
    c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_al, header_border

rows = [("Laptop", 79990, 3), ("Mouse", 1290, 15), ("Keyboard", 3490, 8)]
for r, (name, price, qty) in enumerate(rows, start=2):
    ws["A"].cell(row=r, column=1, value=name)  # this is wrong — read below!
```

Stop! There is an error in the last line: `ws["A"]` is not a column, it is a lookup of a sheet by name. The right way is `ws.cell(row=r, column=1, ...)`. The fixed version:

```python
for r, (name, price, qty) in enumerate(rows, start=2):
    ws.cell(row=r, column=1, value=name)
    ws.cell(row=r, column=2, value=price)
    ws.cell(row=r, column=3, value=qty)
    ws.cell(row=r, column=4, value=f"=B{r}*C{r}")

for col, width in zip("ABCD", [20, 10, 12, 14]):
    ws.column_dimensions[col].width = width

wb.save("shop.xlsx")
print("Saved: shop.xlsx")
```

Now let's read the file back:

```python
from openpyxl import load_workbook

wb = load_workbook("shop.xlsx")
ws = wb["Goods"]
for row in ws.iter_rows(min_row=1, max_row=5, values_only=True):
    print(row)
```

In column D you will see formula strings: `('Laptop', 79990, 3, '=B2*C2')` — this is expected behavior. Formulas live in the file as text, and Excel calculates them.

<!--TASK-->
### Task 1
Create a file `budget.xlsx` with a sheet named "Budget". The first row is a header: "Category", "Plan", "Actual", "Difference" — with styles (bold white font, blue fill `4472C4`, center alignment, borders). Then add four categories: Products (plan 20000, actual 18500), Transportation (5000, 6200), Communications (1500, 1500), Entertainment (8000, 7200). In column D, write the formula `=B-C` for each row (for example, `=B2-C2`). Save the workbook, then load it again and print all rows via `iter_rows(values_only=True)`. Expected output: five rows, with the formula texts visible in column D (not numbers).
### Task 2
Write a pytest test that checks the contents of the xlsx artifact. Create a module `inventory.py` with a function `create_inventory(path)` that builds a workbook as in Task 1 (sheet "Goods", header, three products, formula in D), saves it to the given path, and returns the path. Then create a file `test_inventory.py`: the test calls `create_inventory(tmp_path / "inv.xlsx")`, loads the workbook back via `load_workbook` and checks: the sheet name is "Goods", `ws["A1"].value == "Name"`, `ws["B2"].value == 79990`, and `ws["D2"].value` is a string starting with `"="`. Run `python -m pytest test_inventory.py -q` and get a green result.
### Task 3
Write a pytest test for styles. The function `style_header(ws)` in the same module `inventory.py` applies to row 1: bold font, blue fill `4472C4`, center alignment, and thin borders. The test in `test_inventory.py`: creates a workbook, calls `style_header`, then checks `ws["A1"].font.bold is True`, `ws["A1"].fill.fill_type == "solid"`, that the color string `str(ws["A1"].fill.fgColor.rgb).endswith("4472C4")`, `ws["A1"].alignment.horizontal == "center"` and `ws["A1"].border.left.style == "thin"`. Remember: it is better to check the background with `endswith`, because openpyxl stores colors in 8-character ARGB format.
### Task 4
Write a pytest test for merged cells and frozen panes. The function `make_report_sheet(wb)` creates a sheet "Report" in the workbook, merges cells `A1:C1`, writes the heading "Sales report" into `A1`, and freezes the first row (`ws.freeze_panes = "A2"`). The test: creates a workbook, calls the function, saves to `tmp_path / "report.xlsx"`, loads the file and checks: `str(list(ws.merged_cells.ranges)[0]) == "A1:C1"`, `ws.freeze_panes == "A2"` and `ws["A1"].value == "Sales report"`.
### Task 5
Write a pytest test for the number format and column widths. The function `format_money(ws)` in module `inventory.py`: for column B (rows 2–4) sets `number_format = "#,##0.00"`, and sets column B's width to 14. The test: creates a workbook with data, calls `format_money`, saves, loads, and checks `ws["B2"].number_format == "#,##0.00"` and `ws.column_dimensions["B"].width == 14`.
<!--/TASK-->

<!--HINT-->
### Hint 1
To write cells, use `ws.cell(row=r, column=c, value=...)` in a loop over the data, or assign directly: `ws["D2"] = "=B2-C2"`. After `wb.save("budget.xlsx")`, reopen the file with `load_workbook("budget.xlsx")` and go through the rows with `iter_rows(values_only=True)` — then you will see that openpyxl stores the formula as a string.
### Hint 2
The function should accept a path and return it — this is convenient for tests. In the test, use pytest's built-in `tmp_path` fixture: it gives a temporary folder that is cleaned up automatically. Formula check: `assert isinstance(ws["D2"].value, str) and ws["D2"].value.startswith("=")`.
### Hint 3
Styles are assigned to the cell object: `cell.font = Font(bold=True)`, `cell.fill = PatternFill(fill_type="solid", fgColor="4472C4")`, `cell.alignment = Alignment(horizontal="center")`, `cell.border = Border(left=Side(style="thin"), right=Side(style="thin"), ...)`. In the test, compare the properties of the selected cell, not whole objects.
### Hint 4
`ws.merged_cells.ranges` is a collection of merged ranges. Check its size `len(...) == 1` and the string representation of the first element. `freeze_panes` is assigned a cell reference: `ws.freeze_panes = "A2"` freezes everything above and to the left of cell A2, i.e., the first row.
### Hint 5
`number_format` is an ordinary string: `cell.number_format = "#,##0.00"`. The column width lives in `ws.column_dimensions["B"].width`. For the test to be truthful, be sure to save the workbook and load it again — this way you verify the real file, not an in-memory object.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Budget"

header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(fill_type="solid", fgColor="4472C4")
header_al = Alignment(horizontal="center", vertical="center")
thin = Side(style="thin", color="BFBFBF")
header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

for col, name in enumerate(["Category", "Plan", "Actual", "Difference"], start=1):
    c = ws.cell(row=1, column=col, value=name)
    c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_al, header_border

data = [("Products", 20000, 18500), ("Transportation", 5000, 6200),
        ("Communications", 1500, 1500), ("Entertainment", 8000, 7200)]
for r, (cat, plan, fact) in enumerate(data, start=2):
    ws.cell(row=r, column=1, value=cat)
    ws.cell(row=r, column=2, value=plan)
    ws.cell(row=r, column=3, value=fact)
    ws.cell(row=r, column=4, value=f"=B{r}-C{r}")

wb.save("budget.xlsx")

wb2 = load_workbook("budget.xlsx")
ws2 = wb2["Budget"]
for row in ws2.iter_rows(min_row=1, max_row=5, values_only=True):
    print(row)
```

Output:

```
('Category', 'Plan', 'Actual', 'Difference')
('Products', 20000, 18500, '=B2-C2')
('Transportation', 5000, 6200, '=B3-C3')
('Communications', 1500, 1500, '=B4-C4')
('Entertainment', 8000, 7200, '=B5-C5')
```

What's happening here? We built a workbook: created a sheet, wrote the header styles in a loop, filled in the data, and wrote formulas as strings. When reopening without `data_only`, openpyxl returns the original formula text — this is normal behavior and the main takeaway of the lesson: the library does not calculate formulas itself.
### Walkthrough 2
Module `inventory.py`:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def create_inventory(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Goods"

    font = Font(bold=True, color="FFFFFF")
    fill = PatternFill(fill_type="solid", fgColor="4472C4")
    al = Alignment(horizontal="center")
    thin = Side(style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col, name in enumerate(["Name", "Price", "Quantity", "Cost"], start=1):
        c = ws.cell(row=1, column=col, value=name)
        c.font, c.fill, c.alignment, c.border = font, fill, al, border

    rows = [("Laptop", 79990, 3), ("Mouse", 1290, 15), ("Keyboard", 3490, 8)]
    for r, (name, price, qty) in enumerate(rows, start=2):
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=price)
        ws.cell(row=r, column=3, value=qty)
        ws.cell(row=r, column=4, value=f"=B{r}*C{r}")

    wb.save(path)
    return path
```

Test `test_inventory.py`:

```python
from openpyxl import load_workbook
from inventory import create_inventory

def test_create_inventory_contents(tmp_path):
    path = create_inventory(tmp_path / "inv.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws.title == "Goods"
    assert ws["A1"].value == "Name"
    assert ws["B2"].value == 79990
    assert ws["D2"].value.startswith("=")
```

What's happening here? The function accepts a path and saves the workbook exactly there — the test can put it in the temporary folder `tmp_path` without cluttering the working directory. Then the test opens the file again: this verifies the real artifact on disk. `startswith("=")` confirms that D2 holds a formula.
### Walkthrough 3
Function and test:

```python
def style_header(ws):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    font = Font(bold=True)
    fill = PatternFill(fill_type="solid", fgColor="4472C4")
    al = Alignment(horizontal="center", vertical="center")
    thin = Side(style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col in range(1, ws.max_column + 1):
        c = ws.cell(row=1, column=col)
        c.font, c.fill, c.alignment, c.border = font, fill, al, border
    return ws
```

```python
from openpyxl import Workbook
from inventory import style_header

def test_style_header(tmp_path):
    wb = Workbook()
    ws = wb.active
    for col, name in enumerate(["A", "B", "C"], start=1):
        ws.cell(row=1, column=col, value=name)
    ws = style_header(ws)
    c = ws["A1"]
    assert c.font.bold is True
    assert c.fill.fill_type == "solid"
    assert str(c.fill.fgColor.rgb).endswith("4472C4")
    assert c.alignment.horizontal == "center"
    assert c.border.left.style == "thin"
```

What's happening here? Styles are applied to each header cell. The test checks properties rather than whole objects: `c.fill.fgColor.rgb` returns the color in ARGB format (for example, `004472C4`), so we compare with `endswith`. If we compared the whole string, the test would be brittle.
### Walkthrough 4
Function and test:

```python
def make_report_sheet(wb):
    ws = wb.create_sheet("Report")
    ws.merge_cells("A1:C1")
    ws["A1"] = "Sales report"
    ws.freeze_panes = "A2"
    return ws
```

```python
from openpyxl import Workbook, load_workbook
from inventory import make_report_sheet

def test_make_report_sheet(tmp_path):
    wb = Workbook()
    make_report_sheet(wb)
    path = tmp_path / "report.xlsx"
    wb.save(path)

    wb2 = load_workbook(path)
    ws = wb2["Report"]
    assert len(ws.merged_cells.ranges) == 1
    assert str(list(ws.merged_cells.ranges)[0]) == "A1:C1"
    assert ws.freeze_panes == "A2"
    assert ws["A1"].value == "Sales report"
```

What's happening here? `merge_cells` merges a range, and `merged_cells.ranges` stores the list of merged areas — it survives saving and loading. `freeze_panes` becomes the string `"A2"`, which means "freeze everything above and to the left of A2" (i.e., the header). The test verifies the file after a round-trip, so it guarantees the settings were actually written.
### Walkthrough 5
Function and test:

```python
def format_money(ws):
    for r in range(2, 5):
        ws.cell(row=r, column=2).number_format = "#,##0.00"
    ws.column_dimensions["B"].width = 14
    return ws
```

```python
from openpyxl import Workbook, load_workbook
from inventory import format_money, create_inventory

def test_format_money(tmp_path):
    path = create_inventory(tmp_path / "inv.xlsx")
    wb = load_workbook(path)
    ws = format_money(wb.active)
    wb.save(path)

    wb2 = load_workbook(path)
    ws2 = wb2.active
    assert ws2["B2"].number_format == "#,##0.00"
    assert ws2.column_dimensions["B"].width == 14
```

What's happening here? We took the real file, applied formatting, and saved it again. `number_format` is a string, and comparing it with `"#,##0.00"` is exact. The column width is stored in `column_dimensions`. Again the test works with the file, not an in-memory object — this is the main principle behind verifying office artifacts.
<!--/SOLUTION-->

<!--QUIZ-->
Which object represents an Excel workbook in openpyxl?
- Workbook
- Worksheet
- Cell
* Correct answer: Workbook
You create a workbook with Workbook(); the sheets inside it are Worksheet objects.

How do you add a new sheet to a workbook?
- wb.add_sheet("Name")
- wb.create_sheet("Name")
- wb.new_sheet("Name")
* Correct answer: wb.create_sheet("Name")
create_sheet adds a sheet at the end of the workbook; you access a sheet via wb["Name"].

Can openpyxl calculate formulas itself?
- Yes, always
- No, it stores them as a string
- Yes, but only simple expressions
* Correct answer: No, it stores them as a string
openpyxl writes a formula as text; Excel does the calculation when the file is opened.

What will load_workbook("f.xlsx", data_only=True) return for a cell with a formula if the file was never opened in Excel?
- The formula itself
- 0
- None
* Correct answer: None
A cached formula value appears only after the file has been saved in Excel. If there is none, it returns None.

How do you apply a bold white font to a cell?
- cell.font = Font(bold=True, color="FFFFFF")
- cell.bold = True
- cell.style = "bold white"
* Correct answer: cell.font = Font(bold=True, color="FFFFFF")
The Font class describes a font: weight, size, color, and so on.

How do you merge cells A1:C1?
- ws.merge("A1:C1")
- ws.merge_cells("A1:C1")
- ws.combine("A1:C1")
* Correct answer: ws.merge_cells("A1:C1")
merge_cells takes a range as a string; you can check the merge via ws.merged_cells.ranges.

What does the line ws.freeze_panes = "A2" do?
- Freezes column A
- Freezes everything above and to the left of A2 (the first row)
- Nothing, it is just text
* Correct answer: Freezes everything above and to the left of A2 (the first row)
The frozen region is set by a cell: everything above and to the left of it stays on screen when scrolling.

How do you save a workbook to a file?
- wb.write("file.xlsx")
- wb.save("file.xlsx")
- wb.export("file.xlsx")
* Correct answer: wb.save("file.xlsx")
save writes the workbook to disk; the path is passed as a string or Path.

Which fill sets a solid color?
- PatternFill(fill_type="solid", fgColor="4472C4")
- Fill(color="4472C4")
- PatternFill(fgColor="4472C4")
* Correct answer: PatternFill(fill_type="solid", fgColor="4472C4")
For a solid fill, fill_type="solid" and the fgColor color are required.

How is ws["A1"] different from ws.cell(row=1, column=1)?
- They are different cells
- They are the same way to access A1
- ws.cell does not exist
* Correct answer: They are the same way to access A1
Both expressions return the Cell object for cell A1 — which writing style you choose is a matter of taste.
<!--/QUIZ-->
