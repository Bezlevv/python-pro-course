---
title: Excel/CSV report parser
summary: openpyxl, csv, aggregation.
order: 4
duration: 45 min
difficulty: intermediate
tags: excel, csv, openpyxl
---

Parse spreadsheets into useful results.

## CSV

```python
import csv
with open("sales.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
```

## Excel

```python
from openpyxl import load_workbook
wb = load_workbook("sales.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

## Aggregate

```python
total = sum(float(r["amount"]) for r in rows)
```

## Lesson summary

CSV/Excel → rows → analysis.

<!--TASK-->
### Task 1 — CSV read
Read CSV with DictReader.

### Task 2 — Excel read
Read xlsx.

### Task 3 — Sum
Sum amounts.

### Task 4 — Group
Sum by product.

### Task 5 — Filter
Rows over a threshold.

### Task 6 — Export
Write a summary CSV.

### Task 7 — Errors
Handle missing columns.
<!--/TASK-->

<!--HINT-->
### Hint 1
DictReader.

### Hint 2
load_workbook.

### Hint 3
sum.

### Hint 4
dict.

### Hint 5
Filter.

### Hint 6
writer.

### Hint 7
get.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import csv
with open("sales.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
```

### Solution 2
```python
from openpyxl import load_workbook
wb = load_workbook("sales.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

### Solution 3
```python
total = sum(float(r["amount"]) for r in rows)
```

### Solution 4
```python
by_product = {}
for r in rows:
    by_product[r["product"]] = by_product.get(r["product"], 0) + float(r["amount"])
```

### Solution 5
```python
big = [r for r in rows if float(r["amount"]) > 1000]
```

### Solution 6
```python
with open("summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["product", "total"])
    for product, total in by_product.items():
        w.writerow([product, total])
```

### Solution 7
```python
amount = float(r.get("amount", 0))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is CSV?
- Delimited text
- Binary
- Excel
- None
* Correct answer: Delimited text
Comma.

What is DictReader?
- Row as dict
- List only
- Excel
- None
* Correct answer: Row as dict
Header.

What is openpyxl?
- Excel library
- CSV
- Database
- None
* Correct answer: Excel library
xlsx.

What is load_workbook?
- Opens workbook
- Writes
- Parses
- None
* Correct answer: Opens workbook
File.

What is ws?
- Sheet
- Workbook
- Row
- None
* Correct answer: Sheet
Active.

What is iter_rows?
- Row generator
- Column
- Cell
- None
* Correct answer: Row generator
Values.

What is aggregation?
- Summary
- Raw rows
- Filter
- None
* Correct answer: Summary
Sum.

What is group by?
- Per key total
- Total only
- Sort
- None
* Correct answer: Per key total
Dict.

What is a header?
- Column names
- Data
- Sheet
- None
* Correct answer: Column names
First row.

What is filter?
- Condition
- Loop
- Sum
- None
* Correct answer: Condition
Where.

What is newline=""?
- CSV safety
- Empty
- Error
- None
* Correct answer: CSV safety
Windows.

What is a report?
- Result output
- Input
- Sheet
- None
* Correct answer: Result output
Summary.
<!--/QUIZ-->
