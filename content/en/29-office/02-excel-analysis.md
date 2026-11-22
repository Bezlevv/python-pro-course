---
title: "Excel: Reading and Analyzing Data"
summary: Loading workbooks, reading cells and ranges, aggregating data, and writing results back to Excel.
order: 2
duration: 45 min
difficulty: intermediate
tags: openpyxl, excel, data analysis, load_workbook, reading
---

Reading data is the second half of working with Excel. Most often, workbooks are opened not for editing but to pull data out and analyze it. In this lesson, we will learn to load files, carefully iterate over ranges, and collect meaningful totals from raw cells.

## Loading a workbook

For reading, use `load_workbook`. The function returns a `Workbook`, from which we take the sheet we need:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb["Sales"]
print(ws["A1"].value)   # first cell
```

An important nuance: if the file contains formulas and you want their calculated values, use the `data_only=True` flag:

```python
wb = load_workbook("sales.xlsx", data_only=True)
```

But remember from the previous lesson: if the file was never opened in Excel, there are no cached values, and formula cells will return `None`. In that case, you have to do the calculations yourself.

## Read-only mode

Large files (tens of thousands of rows) are better opened in `read_only=True` mode. In this mode, sheets are read in a streaming fashion, without loading the entire workbook into memory:

```python
wb = load_workbook("big.xlsx", read_only=True)
```

Drawbacks: in this mode you cannot modify cells, and some settings (for example, styles) are unavailable. But speed and memory use are excellent.

## Bounds and iteration

The number of filled rows and columns is reported by `ws.max_row` and `ws.max_column`. Iterate over the table conveniently with an `iter_rows` loop:

```python
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
    print(row)
```

`values_only=True` immediately turns a row into a tuple of values. You can get all sheet data as one list like this:

```python
data = list(ws.iter_rows(values_only=True))
```

## Working with headers

Almost always, the first row contains the field names. Reliable code first builds a "name → column index" dictionary and then accesses data by name rather than by magic numbers:

```python
header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
# now header["Amount"] gives the column number
```

This way the analysis does not break if the column order changes. `ws[1]` is the first row of the sheet, iterated over cells.

## Aggregation

Sums, averages, maximums — plain loops. Let's look at an example: we'll compute revenue by category and find the best-selling product.

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx", data_only=True)
ws = wb["Sales"]

header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
by_category = {}
total = 0.0
count = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is None:          # skip empty rows
        continue
    category = row[header["Category"] - 1]
    amount = row[header["Amount"] - 1]
    by_category[category] = by_category.get(category, 0.0) + amount
    total += amount
    count += 1

print("Data rows:", count)
print("Total revenue:", round(total, 2))
for cat, s in sorted(by_category.items()):
    print(f"{cat}: {s:.2f}")
```

Note: `row` is a tuple, so indices are counted from zero, while `header` gives the column number from one — hence the `- 1`.

Data types matter: numbers come as `int`/`float`, dates as `datetime`, text as `str`. If the data has gaps, they become `None` — check before arithmetic.

## Writing results back

Analysis usually ends with a report. Results can be written to a new sheet of the same workbook or to a separate file:

```python
from openpyxl import Workbook

out = Workbook()
ws_out = out.active
ws_out.title = "Summary"
ws_out.append(["Category", "Amount"])
for cat, s in sorted(by_category.items()):
    ws_out.append([cat, s])
out.save("summary.xlsx")
```

`ws.append(...)` adds a row at the end — the shortest way to fill a sheet with data.

<!--TASK-->
### Task 1
Write a script `read_shop.py` that loads the file `shop.xlsx` (create it yourself: sheet "Goods", header "Name, Price, Quantity, Cost", and three products with prices and quantities). The program should print all rows of the sheet and calculate the total warehouse value. Important: column D in the file contains formulas, so do not rely on `data_only` — calculate the value yourself: price × quantity. Expected output: the table rows and a line like `Total warehouse value: 123.45` (the number depends on your data).
### Task 2
Write a pytest test for a reading function. The function `load_rows(path)` in module `sales_utils.py` returns a list of tuples of all sheet rows without the header (meaning the first row is skipped). The test in `test_sales_utils.py`: first creates a workbook with data (a sheet with headers and three rows of values), saves it to `tmp_path`, then calls `load_rows` and compares the result with the expected list of tuples. Run `python -m pytest test_sales_utils.py -q`.
### Task 3
Write a parametrized pytest test. The function `top_product(path)` returns the name of the product with the maximum value (value = price × quantity, calculate it yourself). Using `@pytest.mark.parametrize`, check it on two different data sets: in the first, "Laptop" is the maximum; in the second, "Monitor" is. To do this, create different workbooks in the test and pass their paths to the parametrized test.
### Task 4
Write a pytest test for aggregation by category. The function `summarize_by_category(path)` returns a dictionary `{category: sum}`, where the sum is calculated as price × quantity over all rows. Test: create a workbook with three categories and several products, save it to `tmp_path`, call the function and check that the dictionary contains the expected sums. Then add a check for an empty workbook: if there is no data, the function returns an empty dictionary.
### Task 5
Write a script `make_summary.py` that reads `sales.xlsx` and creates a new file `summary.xlsx` with a sheet "Summary". It should contain the rows: "Total revenue", "Average order value", "Maximum value", "Number of items" — each with its value. Then write a pytest test that checks the contents of the `summary.xlsx` artifact: it loads it and verifies that the cell with "Total revenue" contains the correct number (calculate it in advance in the test from the same data).
<!--/TASK-->

<!--HINT-->
### Hint 1
Create the file via `Workbook()` + `ws.append(...)`, as at the end of the theory section. For reading, use `ws.iter_rows(values_only=True)`; skip the header (for example, with `next(...)` or a list slice). The value of an item is `price * quantity`; sum it up in a loop.
### Hint 2
The test builds the input file right in the test body: `Workbook()`, `ws.append(["Product", "Price"])`, then data rows, `wb.save(tmp_path / "data.xlsx")`. The function `load_rows` reads `ws.iter_rows(min_row=2, values_only=True)` and returns `list(...)`. Compare with a plain `assert result == expected`.
### Hint 3
Parametrization: `@pytest.mark.parametrize("rows, expected", [...])`, where `rows` is a list of tuples for the workbook, and `expected` is the expected product name. Inside the test, create a workbook from `rows`, save it to the temporary folder, and call `top_product`. Don't forget that the test must create a file for each data set.
### Hint 4
In the function, use `dict.get(key, 0.0)` or `collections.defaultdict(float)` to accumulate sums. For the empty-workbook test, simply do not add data rows to the sheet — only the header. Then `summarize_by_category` must return `{}`.
### Hint 5
Fix the expected values in the test by recalculating them from the same data you write into `sales.xlsx`. For example, pass the data to a helper that creates the file, and compute the totals in the test the same way. After creating `summary.xlsx`, load it and compare the cell values.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from openpyxl import Workbook, load_workbook

# create the input file if it does not exist
wb = Workbook()
ws = wb.active
ws.title = "Goods"
ws.append(["Name", "Price", "Quantity", "Cost"])
ws.append(["Laptop", 79990, 3])
ws.append(["Mouse", 1290, 15])
ws.append(["Keyboard", 3490, 8])
wb.save("shop.xlsx")

wb2 = load_workbook("shop.xlsx")
ws2 = wb2["Goods"]
total = 0.0
for row in ws2.iter_rows(values_only=True):
    print(row)
    if row[0] == "Name":
        continue
    total += row[1] * row[2]
print(f"Total warehouse value: {total:.2f}")
```

Output:

```
('Name', 'Price', 'Quantity', 'Cost')
('Laptop', 79990, 3, None)
('Mouse', 1290, 15, None)
('Keyboard', 3490, 8, None)
Total warehouse value: 286810.00
```

What's happening here? We do not rely on column D with formulas (it would return `None` without `data_only`), and instead calculate the value ourselves: `row[1] * row[2]`. The header is skipped by comparing with its first value. This approach always works, regardless of whether the file was opened in Excel.
### Walkthrough 2
Module `sales_utils.py`:

```python
from openpyxl import load_workbook

def load_rows(path):
    wb = load_workbook(path)
    ws = wb.active
    return list(ws.iter_rows(min_row=2, values_only=True))
```

Test:

```python
from openpyxl import Workbook
from sales_utils import load_rows

def test_load_rows(tmp_path):
    path = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Product", "Price"])
    ws.append(["Laptop", 79990])
    ws.append(["Mouse", 1290])
    wb.save(path)

    assert load_rows(path) == [("Laptop", 79990), ("Mouse", 1290)]
```

What's happening here? `load_rows` skips the first row (`min_row=2`) and returns a list of tuples. The test itself creates the input file in the temporary folder — this is a clean unit test: it does not depend on foreign files on disk, and `tmp_path` guarantees cleanup.
### Walkthrough 3
Function:

```python
def top_product(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.active
    best_name, best_total = None, -1.0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        total = row[1] * row[2]
        if total > best_total:
            best_name, best_total = row[0], total
    return best_name
```

Test:

```python
import pytest
from openpyxl import Workbook
from sales_utils import top_product

def make_book(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.append(["Product", "Price", "Quantity"])
    for r in rows:
        ws.append(r)
    wb.save(path)

@pytest.mark.parametrize("rows, expected", [
    ([("Laptop", 79990, 3), ("Mouse", 1290, 15)], "Laptop"),
    ([("Keyboard", 3490, 8), ("Monitor", 25000, 2)], "Monitor"),
])
def test_top_product(tmp_path, rows, expected):
    path = tmp_path / "data.xlsx"
    make_book(path, rows)
    assert top_product(path) == expected
```

What's happening here? `@pytest.mark.parametrize` runs one test with different data sets. The helper `make_book` builds a workbook from a list of tuples. We compare only the product name — the function's result. This way we verify the logic on two different "input worlds" without duplicating test code.
### Walkthrough 4
Function:

```python
from collections import defaultdict

def summarize_by_category(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.active
    header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
    sums = defaultdict(float)
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        cat = row[header["Category"] - 1]
        sums[cat] += row[header["Price"] - 1] * row[header["Quantity"] - 1]
    return dict(sums)
```

Test:

```python
def test_summarize_by_category(tmp_path):
    path = tmp_path / "sales.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Category", "Price", "Quantity"])
    ws.append(["Electronics", 1000, 2])
    ws.append(["Electronics", 500, 4])
    ws.append(["Stationery", 200, 10])
    wb.save(path)

    assert summarize_by_category(path) == {"Electronics": 4000.0, "Stationery": 2000.0}

def test_summarize_empty(tmp_path):
    path = tmp_path / "empty.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Category", "Price", "Quantity"])
    wb.save(path)
    assert summarize_by_category(path) == {}
```

What's happening here? The `defaultdict(float)` dictionary conveniently accumulates sums: a missing key automatically gets `0.0`. Indices are taken from the header, so the column order does not matter. An empty workbook (header only) yields an empty dictionary — the second test fixes this edge case.
### Walkthrough 5
Script `make_summary.py`:

```python
from openpyxl import Workbook, load_workbook

def make_summary(source_path, out_path):
    wb = load_workbook(source_path, data_only=True)
    ws = wb.active
    totals, count, max_total = 0.0, 0, 0.0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        t = row[1] * row[2]
        totals += t
        max_total = max(max_total, t)
        count += 1

    out = Workbook()
    out_ws = out.active
    out_ws.title = "Summary"
    out_ws.append(["Indicator", "Value"])
    out_ws.append(["Total revenue", round(totals, 2)])
    out_ws.append(["Average order value", round(totals / count, 2)])
    out_ws.append(["Maximum value", round(max_total, 2)])
    out_ws.append(["Number of items", count])
    out.save(out_path)
    return out_path
```

Test:

```python
def test_make_summary(tmp_path):
    src = tmp_path / "sales.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Product", "Price", "Quantity"])
    ws.append(["Laptop", 79990, 3])
    ws.append(["Mouse", 1290, 15])
    wb.save(src)

    out = make_summary(src, tmp_path / "summary.xlsx")
    wb2 = load_workbook(out)
    ws2 = wb2["Summary"]
    rows = {r[0]: r[1] for r in ws2.iter_rows(min_row=2, values_only=True)}
    assert rows["Total revenue"] == 79990 * 3 + 1290 * 15
    assert rows["Number of items"] == 2
```

What's happening here? `make_summary` reads the source, computes the totals, and writes a new file. The test independently recalculates the expected revenue from the same data and compares it with the artifact contents — that is, it verifies the real file, not the function's internal logic.
<!--/SOLUTION-->

<!--QUIZ-->
How do you load a workbook from disk?
- Workbook("file.xlsx")
- load_workbook("file.xlsx")
- open("file.xlsx")
* Correct answer: load_workbook("file.xlsx")
load_workbook reads the file and returns a Workbook object.

What does the read_only=True flag do in load_workbook?
- Speeds up reading and saves memory, but forbids changes
- Allows editing cells
- Enables formula highlighting
* Correct answer: Speeds up reading and saves memory, but forbids changes
In read_only mode, sheets are read in a streaming fashion, but you cannot write to the workbook.

What does ws.max_row return?
- The number of the last row with data
- The number of columns
- A list of all rows
* Correct answer: The number of the last row with data
ws.max_row is the number of filled rows (the last row with data).

What does the values_only=True parameter do in iter_rows?
- Returns tuples of values instead of Cell objects
- Returns only non-empty cells
- Returns column headers
* Correct answer: Returns tuples of values instead of Cell objects
This makes the data ready to use: tuples of values instead of cell objects.

Why can formula cells be None with data_only=True?
- The file has no formulas
- The file was not recalculated and saved in Excel
- openpyxl cannot read formulas
* Correct answer: The file was not recalculated and saved in Excel
Cached formula values appear only after the file has been opened and saved in Excel.

How do you find a column index by its header name?
- Read the first row and build a name → index dictionary
- Use ws.column("Name")
- It is impossible
* Correct answer: Read the first row and build a name → index dictionary
A dictionary like {cell.value: idx for idx, cell in enumerate(ws[1], start=1)} makes the code robust to column reordering.

How do you skip empty rows during analysis?
- Check that the row's first value is not None
- Call skip()
- Empty rows never occur
* Correct answer: Check that the row's first value is not None
Empty cells become None, so the condition if row[0] is None: continue reliably filters out empty rows.

What type does a date read from an Excel cell have?
- str
- datetime.datetime
- float
* Correct answer: datetime.datetime
Excel stores dates as numbers with a format; openpyxl converts them to datetime.

How do you append a row to the end of a sheet?
- ws.append([...])
- ws.add_row([...])
- ws.insert([...])
* Correct answer: ws.append([...])
append adds a row of values to the end of the sheet — convenient when building reports.

What does list(ws.iter_rows(values_only=True)) return?
- A list of tuples of all sheet rows
- A list of Cell objects
- The number of rows
* Correct answer: A list of tuples of all sheet rows
iter_rows with values_only=True generates tuples of values, and list(...) collects them into a list.
<!--/QUIZ-->
