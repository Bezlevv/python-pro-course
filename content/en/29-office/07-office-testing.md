---
title: Testing Office Automation
summary: pytest for xlsx/docx/pdf: fixtures, tmp_path, parametrization, artifact content checks.
order: 7
duration: 50 min
difficulty: advanced
tags: pytest, tests, tmp_path, artifacts, conftest
---

When code creates files — xlsx, docx, pdf — a plain "print check" is not enough. You need automated tests that generate artifacts into a clean temporary folder and verify their contents. This lesson is about pytest and office files.

## Why not compare files byte by byte

`.xlsx` and `.docx` are zip archives with XML inside. They store identifiers, timestamps, and other metadata that change from run to run. So files cannot be compared byte by byte — tests would fail for no reason. Instead, compare the meaning: cell values, paragraph texts, page counts.

## tmp_path: the temporary folder

The built-in `tmp_path` fixture gives each test a unique temporary folder that is automatically cleaned up after the test:

```python
def test_write_xlsx(tmp_path):
    path = tmp_path / "out.xlsx"
    wb = Workbook()
    wb.active["A1"] = 42
    wb.save(path)
    assert path.exists()
```

No garbage in the working directory — tests are repeatable and isolated.

## Fixtures

A fixture is a function that prepares data or files. It can use other fixtures — pytest resolves dependencies itself:

```python
import pytest
from openpyxl import Workbook

@pytest.fixture
def sample_xlsx(tmp_path):
    path = tmp_path / "sample.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["City", "Population"])
    ws.append(["Moscow", 13_000_000])
    ws.append(["Saint Petersburg", 5_600_000])
    wb.save(path)
    return path
```

Shared fixtures go into `conftest.py` — then they are visible to all tests in the package.

## Parametrization

`@pytest.mark.parametrize` runs one test with different data sets:

```python
@pytest.mark.parametrize("expected", [("Moscow",), ("Saint Petersburg",)])
def test_contains_city(sample_xlsx, expected):
    ...
```

## Checking xlsx

After generation, load the workbook back and check values and styles:

```python
from openpyxl import load_workbook

def test_xlsx_content(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    ws = wb.active
    assert ws["A1"].value == "City"
    assert ws["B2"].value == 13_000_000
    assert ws["A1"].font.bold is True
    assert len(ws._charts) == 0
```

## Checking docx and pdf

Likewise for Word and PDF — open and read the contents:

```python
from docx import Document
from pypdf import PdfReader

def test_docx(path):
    doc = Document(path)
    assert doc.paragraphs[0].text == "Report"
    assert len(doc.tables) == 1

def test_pdf(path):
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    assert "Report" in reader.pages[0].extract_text()
```

## Negative tests

A function should react correctly to errors — for example, a missing file:

```python
import pytest

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_workbook("nonexistent.xlsx")
```

## Golden files

For text reports, the "golden file" pattern is convenient: a reference result is saved in the repository in advance, and the test compares the function's output with it. This works well for document texts, but not for xlsx/docx binaries — there, compare values.

## Complete example

Let's assemble a test suite for a module that creates a report:

```python
import pytest
from openpyxl import Workbook, load_workbook

@pytest.fixture
def out_dir(tmp_path):
    return tmp_path

def build_report(path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Indicator", "Value"])
    ws.append(["Revenue", 1_200_000])
    wb.save(path)
    return path

def test_report_file_exists(out_dir):
    path = build_report(out_dir / "report.xlsx")
    assert path.exists()

def test_report_values(out_dir):
    path = build_report(out_dir / "report.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws["A2"].value == "Revenue"
    assert ws["B2"].value == 1_200_000
```

Run: `python -m pytest tests/ -q`.

<!--TASK-->
### Task 1
Write a pytest test with a fixture. Create a module `test_fixtures.py` where the fixture `sample_xlsx(tmp_path)` creates a workbook with a sheet "Data" and three rows (header + two data rows). Write two tests: the first checks that the file exists and has one sheet; the second — that `ws["B2"].value` equals the expected number. Run `python -m pytest test_fixtures.py -q`.
### Task 2
Write a parametrized test. The function `city_population(path, city)` returns the population of a city from the sheet "City, Population". Using `@pytest.mark.parametrize`, check it on three cities (including one that is not in the data — let it return None). Create the workbook data in a fixture.
### Task 3
Write a pytest test that checks an xlsx artifact as a whole: values, header style (bold font), column width, and the absence of charts. The function `build_sales(path)` creates a sheet "Sales" with a header and two rows, styling the header. The test loads the file and checks all four points.
### Task 4
Write a pytest test for a docx artifact. The function `build_doc(path)` creates a document with a heading "Report" and a 2×2 table. Test: load the docx, check that the first paragraph is a level-1 heading (there `p.style.name == "Heading 1"`), there is one table, and `table.cell(1, 1).text` contains the expected value.
### Task 5
Write a pytest test for a pdf artifact and a negative test. The function `build_pdf(path)` creates a PDF with the text "Quarterly report". Test 1: check that the PDF has a page and text is extracted. Test 2: the function `load_any(path)` (simply `load_workbook(path)`) raises `FileNotFoundError` when given a nonexistent path — check it with `pytest.raises`.
<!--/TASK-->

<!--HINT-->
### Hint 1
Fixture: `@pytest.fixture def sample_xlsx(tmp_path): ... return path`. Note: the fixture name is passed as a test argument. `tmp_path` is also a fixture; it can be used inside another fixture.
### Hint 2
Parametrization: `@pytest.mark.parametrize("city, expected", [("Moscow", 13_000_000), ("Kazan", None)])`. In the test body, call `city_population(sample_xlsx, city)` and compare with expected.
### Hint 3
Bold font: `ws["A1"].font.bold is True`. Width: `ws.column_dimensions["A"].width`. Charts: `len(ws._charts) == 0`. Values — ordinary asserts on cells.
### Hint 4
Level-1 heading: `doc.paragraphs[0].style.name == "Heading 1"`. Check `len(doc.tables) == 1` and the cell text. If the document has an empty first paragraph, take it into account: an initial `Document()` contains one empty paragraph, so it is better to add the heading first and check `paragraphs[0]`.
### Hint 5
For PDF, use `PdfReader` and `extract_text()`. For the negative test: `with pytest.raises(FileNotFoundError): load_workbook(tmp_path / "no.xlsx")`. Build the path to a nonexistent file via `tmp_path` too, so as not to touch the disk.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
File `test_fixtures.py`:

```python
import pytest
from openpyxl import Workbook, load_workbook

@pytest.fixture
def sample_xlsx(tmp_path):
    path = tmp_path / "sample.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws.append(["City", "Population"])
    ws.append(["Moscow", 13_000_000])
    ws.append(["Saint Petersburg", 5_600_000])
    wb.save(path)
    return path

def test_file_exists_and_one_sheet(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    assert len(wb.sheetnames) == 1
    assert wb.sheetnames[0] == "Data"

def test_sheet_value(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    ws = wb.active
    assert ws["B2"].value == 13_000_000
```

What's happening here? The fixture `sample_xlsx` takes `tmp_path` and returns the path to a ready file. Each test gets a fresh workbook — data is isolated. `load_workbook` opens the artifact, and we check both the sheet name and the value. This is the foundation of all further checks.
### Walkthrough 2
Check module and test:

```python
from openpyxl import load_workbook

def city_population(path, city):
    wb = load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == city:
            return row[1]
    return None
```

```python
import pytest
from city_utils import city_population

@pytest.mark.parametrize("city, expected", [
    ("Moscow", 13_000_000),
    ("Saint Petersburg", 5_600_000),
    ("Kazan", None),
])
def test_city_population(sample_xlsx, city, expected):
    assert city_population(sample_xlsx, city) == expected
```

What's happening here? One test runs three times — with different cities. This is an example of parametrization: data comes from the decorator, and `sample_xlsx` is injected by the fixture. The "city absent" case is an important edge case; it checks the `None` return.
### Walkthrough 3
Function:

```python
from openpyxl import Workbook
from openpyxl.styles import Font

def build_sales(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Month", "Amount"])
    ws.append(["January", 120])
    ws.append(["February", 150])
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 15
    wb.save(path)
    return path
```

Test:

```python
def test_build_sales(tmp_path):
    path = build_sales(tmp_path / "sales.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws["A1"].value == "Month"
    assert ws["B3"].value == 150
    assert ws["A1"].font.bold is True
    assert ws.column_dimensions["A"].width == 15
    assert len(ws._charts) == 0
```

What's happening here? We check the artifact from four sides: cell contents, style, column width, and the absence of charts. This is a comprehensive "snapshot" of the file: if any part of the generation breaks, the test fails.
### Walkthrough 4
Function:

```python
from docx import Document

def build_doc(path):
    doc = Document()
    doc.add_heading("Report", level=1)
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Indicator"
    table.cell(0, 1).text = "Value"
    table.cell(1, 0).text = "Revenue"
    table.cell(1, 1).text = "1 200 000"
    doc.save(path)
    return path
```

Test:

```python
def test_build_doc(tmp_path):
    path = build_doc(tmp_path / "report.docx")
    doc = Document(path)
    assert doc.paragraphs[0].text == "Report"
    assert doc.paragraphs[0].style.name == "Heading 1"
    assert len(doc.tables) == 1
    table = doc.tables[0]
    assert table.cell(1, 1).text == "1 200 000"
```

What's happening here? `doc.paragraphs[0]` is the first paragraph, a level-1 heading. The `style.name` check confirms it is a heading, not plain text. The table is checked both by count and by cell contents.
### Walkthrough 5
Functions and tests:

```python
def build_pdf(path):
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    doc = SimpleDocTemplate(str(path))
    doc.build([Paragraph("Quarterly report", getSampleStyleSheet()["Title"])])
    return path
```

```python
import pytest
from openpyxl import load_workbook
from pypdf import PdfReader
from pdf_gen import build_pdf

def test_build_pdf(tmp_path):
    path = build_pdf(tmp_path / "report.pdf")
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    assert "Quarterly report" in reader.pages[0].extract_text()

def test_load_any_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_workbook(tmp_path / "no.xlsx")
```

What's happening here? The first test verifies the PDF actually contains text — extraction via pypdf. The second is negative: passing a nonexistent path must raise `FileNotFoundError`, and `pytest.raises` fixes that. Such tests protect code from silent failures in production.
<!--/SOLUTION-->

<!--QUIZ-->
What is tmp_path in pytest?
- A built-in fixture providing a temporary folder for the test
- The path to the working directory
- A package for working with files
* Correct answer: A built-in fixture providing a temporary folder for the test
Each test gets a unique folder that is cleaned up after completion.

Why can't xlsx files be compared byte by byte?
- Inside there are metadata and identifiers that change from run to run
- The files are too large
- The format is not supported by Python
* Correct answer: Inside there are metadata and identifiers that change from run to run
So you compare meaning: cell values, texts, page counts.

Where are shared fixtures stored?
- In conftest.py
- In any test file
- In pytest.ini
* Correct answer: In conftest.py
conftest.py makes fixtures visible to all tests in the package.

How do you run one test with different data sets?
- @pytest.mark.parametrize(...)
- @pytest.mark.data(...)
- @pytest.test_cases(...)
* Correct answer: @pytest.mark.parametrize(...)
The parametrize decorator passes different arguments to the test one by one.

How do you check that a function raised an exception?
- with pytest.raises(...)
- try/except in the test
- assert raises(...)
* Correct answer: with pytest.raises(...)
The pytest.raises context manager catches the expected exception.

How do you check text inside a PDF?
- reader.pages[i].extract_text()
- pdf.text()
- reader.contents
* Correct answer: reader.pages[i].extract_text()
PdfReader extracts the page text with extract_text().

How do you check that cell text is bold?
- ws["A1"].font.bold is True
- ws["A1"].bold
- cell.bold == True
* Correct answer: ws["A1"].font.bold is True
The font property is a Font object, which has a bold flag.

What does len(ws._charts) == 1 check?
- That the sheet has exactly one chart
- That there is one cell
- That the file is saved
* Correct answer: That the sheet has exactly one chart
_charts is the list of charts on the sheet.

Why should a fixture accept tmp_path?
- To write files only into the temporary folder
- To speed up tests
- It is mandatory for all fixtures
* Correct answer: To write files only into the temporary folder
This way tests do not touch project working files and are isolated from each other.

Which command runs pytest?
- python -m pytest
- python test.py
- pytest run
* Correct answer: python -m pytest
A stable way to run: python -m pytest <path> -q.
<!--/QUIZ-->
