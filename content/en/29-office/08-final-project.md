---
title: "Final Project: Report Generator"
summary: We assemble a full pipeline: data → Excel, Word, and PDF, with unit and integration tests.
order: 8
duration: 60 min
difficulty: advanced
tags: project, generator, integration, pytest, reports
---

The final project brings together everything we have learned: the same data must turn into an Excel workbook, a Word document, and a PDF report. The key to success is modularity: split the program into parts, each of which can be tested separately.

## Package architecture

Let's build a package `reports` with this layout:

```
reports/
├── __init__.py
├── core.py          # data model
├── excel_report.py  # xlsx generation
├── word_report.py   # docx generation
├── pdf_report.py    # pdf generation
└── generate_all.py  # single entry point
```

Each module exports a function of the form `build_x(sales, path) -> Path` that creates a file and returns the path. Then a test simply calls the function and checks the artifact.

## Data model

For sales, we use a `dataclass`:

```python
from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return self.price * self.qty
```

`dataclass` itself generates `__init__`, `__repr__`, and comparison — convenient both for code and for tests.

## Excel module

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def build_excel(sales, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Product", "Price", "Quantity", "Cost"])
    for s in sales:
        ws.append([s.product, s.price, s.qty, s.total])
    ws["A1"].font = Font(bold=True)
    ws["A1"].fill = PatternFill(fill_type="solid", fgColor="4472C4")
    wb.save(path)
    return path
```

## Word module

```python
from docx import Document

def build_word(sales, path):
    doc = Document()
    doc.add_heading("Sales report", level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    for col, name in enumerate(["Product", "Price", "Quantity", "Cost"]):
        table.cell(0, col).text = name
    for s in sales:
        row = table.add_row()
        row.cells[0].text = s.product
        row.cells[1].text = str(s.price)
        row.cells[2].text = str(s.qty)
        row.cells[3].text = str(s.total)
    doc.save(path)
    return path
```

## PDF module

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(sales, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    data = [["Product", "Price", "Quantity", "Cost"]]
    for s in sales:
        data.append([s.product, s.price, s.qty, s.total])
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    doc.build([Paragraph("Sales report", styles["Title"]), table])
    return path
```

## Single entry point

```python
from pathlib import Path
from reports.excel_report import build_excel
from reports.word_report import build_word
from reports.pdf_report import build_pdf

def generate_all(sales, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    paths = {
        "xlsx": build_excel(sales, out_dir / "report.xlsx"),
        "docx": build_word(sales, out_dir / "report.docx"),
        "pdf": build_pdf(sales, out_dir / "report.pdf"),
    }
    return paths
```

`out_dir.mkdir(exist_ok=True)` guarantees the folder exists. A repeated run overwrites the files — that is fine (idempotence).

## Integration test

```python
def test_generate_all(tmp_path):
    sales = [Sale("Laptop", 79990, 3), Sale("Mouse", 1290, 15)]
    paths = generate_all(sales, tmp_path)
    assert paths["xlsx"].exists()
    assert paths["docx"].exists()
    assert paths["pdf"].exists()
    # then — checking the contents of each format
```

Such a test verifies the chain of modules: if one generator breaks, the whole pipeline fails.

<!--TASK-->
### Task 1
Create a package `reports` with a module `core.py`: a `dataclass Sale` (product, price, qty) and a `total` property. Write a pytest test: create an instance `Sale("Laptop", 79990, 3)`, check that `s.total == 239970.0`, and the `product`/`qty` fields are accessible. Run `python -m pytest -q`.
### Task 2
Implement `excel_report.py` with the function `build_excel(sales, path)` following the theory example. Write a pytest test: generate a workbook in the temporary folder, load it and check: the sheet name is "Sales", three data rows plus the header, `ws["D2"].value == 239970.0` (the value of the first item) and `ws["A1"].font.bold is True`.
### Task 3
Implement `word_report.py` with the function `build_word(sales, path)`. Write a pytest test: load the docx and check: the first paragraph is a level-1 heading "Sales report", there is one table with `1 + len(sales)` rows and 4 columns, and `table.cell(1, 3).text == "239970.0"`.
### Task 4
Implement `pdf_report.py` with the function `build_pdf(sales, path)`. Write a pytest test: open the PDF with `PdfReader` and check: there is at least one page, and the text of the first page contains "Sales report" and the name of the first product.
### Task 5
Implement `generate_all.py` and write an integration test: generate all three files in `tmp_path`, check that all paths exist, and then check the contents of each format (the xlsx value, the docx text, the pdf text). Run the whole test suite with `python -m pytest -q` and make all tests pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
`@dataclass` is imported from `dataclasses`. A property is an ordinary method with the `@property` decorator. Compare `total` with `==` against a float literal; for precision you can use `round(s.total, 2)`.
### Hint 2
The value of the first item: `Sale("Laptop", 79990, 3).total == 239970.0`. In `build_excel`, use `ws.append([s.product, s.price, s.qty, s.total])`. The test loads the file via `load_workbook(path)` and checks `ws["D2"]`.
### Hint 3
In `build_word`, after `doc.add_heading`, create the table via `doc.add_table(rows=1, cols=4)`, then add rows with `table.add_row()`. Don't forget the style `"Table Grid"`. Test: `doc.paragraphs[0].style.name == "Heading 1"` and `len(table.rows) == 1 + len(sales)`.
### Hint 4
In `build_pdf`, collect the table data from `sales`: the first row is the header. Test: `PdfReader(str(path))`, then `text = reader.pages[0].extract_text()` and `assert "Sales report" in text`.
### Hint 5
`generate_all` returns a dictionary of paths. The integration test calls it once and checks the three files. For docx use `Document(path)`, for pdf — `PdfReader`, for xlsx — `load_workbook`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
`core.py`:

```python
from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return self.price * self.qty
```

Test:

```python
from reports.core import Sale

def test_sale_total():
    s = Sale("Laptop", 79990, 3)
    assert s.total == 239970.0
    assert s.product == "Laptop"
    assert s.qty == 3
```

What's happening here? `dataclass` reduces boilerplate: the constructor, repr, and comparison are generated automatically. The `total` property is computed on the fly. The test checks both the calculation and field access — the foundation on which all generators stand.
### Walkthrough 2
`excel_report.py` (fragment):

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def build_excel(sales, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Product", "Price", "Quantity", "Cost"])
    for s in sales:
        ws.append([s.product, s.price, s.qty, s.total])
    ws["A1"].font = Font(bold=True)
    ws["A1"].fill = PatternFill(fill_type="solid", fgColor="4472C4")
    wb.save(path)
    return path
```

Test:

```python
from openpyxl import load_workbook
from reports.core import Sale
from reports.excel_report import build_excel

def test_build_excel(tmp_path):
    sales = [Sale("Laptop", 79990, 3), Sale("Mouse", 1290, 15)]
    path = build_excel(sales, tmp_path / "report.xlsx")

    wb = load_workbook(path)
    ws = wb.active
    assert ws.title == "Sales"
    assert ws.max_row == 3          # header + 2 products
    assert ws["D2"].value == 239970.0
    assert ws["A1"].font.bold is True
```

What's happening here? The generator is independent of the data source: it takes a list of `Sale` and a path. The test verifies the artifact: the number of rows (3 = 1 + 2), the value of the first item (79990 × 3), and the header style. The module can be used both in the pipeline and standalone.
### Walkthrough 3
`word_report.py`:

```python
from docx import Document

def build_word(sales, path):
    doc = Document()
    doc.add_heading("Sales report", level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    for col, name in enumerate(["Product", "Price", "Quantity", "Cost"]):
        table.cell(0, col).text = name
    for s in sales:
        row = table.add_row()
        row.cells[0].text = s.product
        row.cells[1].text = str(s.price)
        row.cells[2].text = str(s.qty)
        row.cells[3].text = str(s.total)
    doc.save(path)
    return path
```

Test:

```python
from docx import Document
from reports.word_report import build_word

def test_build_word(tmp_path):
    sales = [Sale("Laptop", 79990, 3)]
    path = build_word(sales, tmp_path / "report.docx")

    doc = Document(path)
    assert doc.paragraphs[0].text == "Sales report"
    assert doc.paragraphs[0].style.name == "Heading 1"
    table = doc.tables[0]
    assert len(table.rows) == 2                  # header + 1 product
    assert len(table.columns) == 4
    assert table.cell(1, 3).text == "239970.0"
```

What's happening here? The table is built dynamically: one header row plus one row per product. The test checks both structure (number of rows/columns) and data (the value cell). `str(s.total)` turns the number into text for Word.
### Walkthrough 4
`pdf_report.py`:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(sales, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    data = [["Product", "Price", "Quantity", "Cost"]]
    for s in sales:
        data.append([s.product, s.price, s.qty, s.total])
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    doc.build([Paragraph("Sales report", styles["Title"]), table])
    return path
```

Test:

```python
from pypdf import PdfReader
from reports.pdf_report import build_pdf

def test_build_pdf(tmp_path):
    sales = [Sale("Laptop", 79990, 3)]
    path = build_pdf(sales, tmp_path / "report.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    text = reader.pages[0].extract_text()
    assert "Sales report" in text
    assert "Laptop" in text
```

What's happening here? The data becomes a PDF table. The test checks that text is extracted and contains both the title and the product name. If generation silently failed or produced an empty file, the test would catch it.
### Walkthrough 5
`generate_all.py`:

```python
from pathlib import Path
from reports.excel_report import build_excel
from reports.word_report import build_word
from reports.pdf_report import build_pdf

def generate_all(sales, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    return {
        "xlsx": build_excel(sales, out_dir / "report.xlsx"),
        "docx": build_word(sales, out_dir / "report.docx"),
        "pdf": build_pdf(sales, out_dir / "report.pdf"),
    }
```

Integration test:

```python
from docx import Document
from openpyxl import load_workbook
from pypdf import PdfReader
from reports.core import Sale
from reports.generate_all import generate_all

def test_generate_all(tmp_path):
    sales = [Sale("Laptop", 79990, 3), Sale("Mouse", 1290, 15)]
    paths = generate_all(sales, tmp_path)

    assert paths["xlsx"].exists()
    assert paths["docx"].exists()
    assert paths["pdf"].exists()

    wb = load_workbook(paths["xlsx"])
    assert wb.active["D2"].value == 239970.0

    doc = Document(paths["docx"])
    assert doc.tables[0].cell(2, 3).text == "19350.0"   # 1290 × 15

    reader = PdfReader(str(paths["pdf"]))
    assert "Sales report" in reader.pages[0].extract_text()
```

What's happening here? The integration test runs the whole pipeline and verifies each artifact. This is the project's "smoke test": if the assembly works, you can safely extend the functionality. This approach is the standard for report generators in production.
<!--/SOLUTION-->

<!--QUIZ-->
What is a dataclass in Python?
- A class with automatically generated __init__, __repr__, and comparison
- A class for working with dates
- A special Excel data container
* Correct answer: A class with automatically generated __init__, __repr__, and comparison
@dataclass removes the boilerplate of declaring fields.

Why should a generator function take a path as a parameter?
- So it can be tested and reused
- To speed things up
- It is an openpyxl requirement
* Correct answer: So it can be tested and reused
A path parameter lets tests use tmp_path instead of cluttering the disk.

What does out_dir.mkdir(exist_ok=True) do?
- Creates the folder if it does not exist yet
- Deletes the folder
- Checks whether a file exists
* Correct answer: Creates the folder if it does not exist yet
exist_ok=True prevents a crash if the folder already exists.

What does idempotence of generation mean?
- A repeated run gives the same correct result
- Files cannot be overwritten
- Each run creates unique files
* Correct answer: A repeated run gives the same correct result
A repeated run overwrites the files with the same content — that is fine.

How is an integration test different from a unit test?
- An integration test checks a chain of modules; a unit test checks one module
- Integration tests are faster
- They are no different
* Correct answer: An integration test checks a chain of modules; a unit test checks one module
A unit test is isolated; integration checks how parts work together.

What will build_excel(sales, path) return?
- The path to the created file
- A Workbook object
- The list of sales
* Correct answer: The path to the created file
All generators return a path — a unified contract for the pipeline.

How do you check a level-1 heading in docx?
- doc.paragraphs[0].style.name == "Heading 1"
- doc.title == "Report"
- doc.heading == 1
* Correct answer: doc.paragraphs[0].style.name == "Heading 1"
The style.name property returns the paragraph style name.

How do you find the number of rows in a docx table?
- len(table.rows)
- table.row_count()
- table.size
* Correct answer: len(table.rows)
table.rows is a collection of rows; len(...) gives their count.

Why is checking the contents of all three artifacts useful?
- It confirms the whole pipeline works
- It speeds up generation
- It is mandatory for openpyxl
* Correct answer: It confirms the whole pipeline works
Checking all formats fully guarantees the report's integrity.

How do you run all project tests?
- python -m pytest -q
- python run_tests.py
- pytest --all
* Correct answer: python -m pytest -q
The command collects all package tests; -q shortens the output.
<!--/QUIZ-->
