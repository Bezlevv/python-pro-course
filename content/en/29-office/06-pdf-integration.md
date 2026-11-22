---
title: "Integration: Conversion and PDF Reports"
summary: Generating PDFs with reportlab, converting xlsx to PDF, extracting text from PDF for verification.
order: 6
duration: 50 min
difficulty: advanced
tags: reportlab, pdf, conversion, reports, pypdf
---

PDF is the final format for reports: it looks the same on any device. The `reportlab` library is the standard for generating PDFs in Python. Installation: `pip install reportlab`.

## Platypus: a story of "flowables"

The high-level framework of reportlab is called Platypus. You assemble a "story" from floating elements — flowables: `Paragraph`, `Spacer`, `Table`, `Image`, `PageBreak` — and pass it to the document:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

doc = SimpleDocTemplate("report.pdf", pagesize=A4, title="Report")
styles = getSampleStyleSheet()

story = [
    Paragraph("Annual report", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Company revenue grew by 15%.", styles["BodyText"]),
]

data = [["Indicator", "Value"], ["Revenue", "1 200 000"], ["Expenses", "980 000"]]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(table)

doc.build(story)
print("Done: report.pdf")
```

`SimpleDocTemplate` describes the document (path, page size, margins). `doc.build(story)` assembles the PDF. The table is styled with `TableStyle`: coordinates are given as `(column, row, column, row)`, where `-1` means the last one.

## Paragraph styles

Basic styles come from `getSampleStyleSheet()`: `"Title"`, `"Heading1"`, `"BodyText"`. To create your own style, use `ParagraphStyle`:

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

my_style = ParagraphStyle(
    "MyStyle",
    parent=styles["BodyText"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#333333"),
    spaceAfter=10,
)
```

`leading` is the line spacing, `fontSize` is the font size.

## Images

`Image` inserts a picture; you can set dimensions:

```python
from reportlab.platypus import Image

story.append(Image("logo.png", width=3 * cm, height=1.5 * cm))
```

## Page numbers

Page numbers are added via a callback that draws the page:

```python
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 1 * cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("report.pdf", pagesize=A4, onLaterPages=footer, onFirstPage=footer)
```

`doc.page` is the current page number.

## Converting xlsx → PDF

There is no direct openpyxl → PDF conversion. Two working paths: (1) read the data with openpyxl and build the report in reportlab — which is what we do; (2) send the `.xlsx` to LibreOffice: `soffice --headless --convert-to pdf file.xlsx` — an external tool invoked via `subprocess.run`.

## Checking a PDF

To test PDFs, you need a text-extraction tool. `pypdf` (install with `pip install pypdf`) reads pages and text:

```python
from pypdf import PdfReader

reader = PdfReader("report.pdf")
print(len(reader.pages))            # number of pages
print(reader.pages[0].extract_text())  # text of the first page
```

Important: a PDF does not have to contain a text layer (for example, scans). But for reports we generate ourselves, extraction works — and it is the basis of tests.

<!--TASK-->
### Task 1
Create a file `income.pdf` with reportlab: a title "Income report" (Title style), a description paragraph, a 3×2 table (header "Indicator, Amount" and two data rows) with borders and a blue header. Add a page number at the bottom center. Save the PDF, then open it with `PdfReader` and print the number of pages and the text of the first page.
### Task 2
Write a pytest test for a PDF artifact. The function `build_pdf(data, path)` creates a PDF with a title, a table from `data`, and saves it to the path. Test: pass data with keywords (for example, "Revenue"), then open the file with `PdfReader` and check: at least one page exists, and the text of the first page contains the word "Revenue".
### Task 3
Write a pytest test for the document structure. The function `build_story(data)` returns a list of flowables (a story): a title `Paragraph` and a `Table` from the data. Test: make sure the list contains at least one `Table` and at least one `Paragraph`, and the table data contains the header.
### Task 4
Write a pytest test for xlsx → PDF conversion. The function `xlsx_to_pdf(xlsx_path, pdf_path)` reads the entire first sheet of the workbook via openpyxl (all rows, including the header) and builds a PDF with a table from this data. Test: create an xlsx in the temporary folder (header and two rows), call the function, then `PdfReader` and check that the text contains values from the xlsx (for example, the first header value).
### Task 5
Write a pytest test for a multipage PDF. The function `build_multipage_pdf(rows, path)` creates a PDF where each row from `rows` is formatted as a paragraph, and after every three paragraphs a `PageBreak` is inserted. Test: pass 7 rows, check that `len(reader.pages) >= 2`, and that the text of the last page contains the last data row.
<!--/TASK-->

<!--HINT-->
### Hint 1
Imports: `from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle`, `from reportlab.lib.styles import getSampleStyleSheet`, `from reportlab.lib import colors`. Page number: a `footer(canvas, doc)` function and the `onFirstPage`/`onLaterPages` parameters in `SimpleDocTemplate`.
### Hint 2
The function `build_pdf` returns the path. In the test: `reader = PdfReader(path)`, then `text = reader.pages[0].extract_text()` and `assert "Revenue" in text`. Remember: if the text is not extracted, check that you use `Paragraph` for text rather than drawing directly on the canvas.
### Hint 3
`build_story` should return a list — check with `any(isinstance(x, Table) for x in story)`. The table data: `table._cellvalues` is an informal but working field; it is simpler to check that the story contains a Table, and check values separately via the generated PDF (Task 2).
### Hint 4
Read the xlsx via `load_workbook(xlsx_path, data_only=True)` and `ws.iter_rows(values_only=True)` — you get a list of tuples. Pass it to `Table(list_of_rows)`. In the test, create the xlsx with `Workbook()` and `ws.append(...)`, save it to `tmp_path`.
### Hint 5
`PageBreak` is another flowable: add it to the story after every third paragraph. Number of pages: `len(reader.pages)`. Last page: `reader.pages[-1].extract_text()`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 1 * cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("income.pdf", pagesize=A4, onFirstPage=footer, onLaterPages=footer)
styles = getSampleStyleSheet()

story = [
    Paragraph("Income report", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Monthly data for 2026.", styles["BodyText"]),
]
data = [["Indicator", "Amount"], ["Revenue", "1 200 000"], ["Expenses", "980 000"]]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(table)
doc.build(story)

from pypdf import PdfReader
reader = PdfReader("income.pdf")
print("Pages:", len(reader.pages))
print(reader.pages[0].extract_text())
```

What's happening here? `SimpleDocTemplate` receives the `onFirstPage` and `onLaterPages` callbacks — the `footer` function draws the page number at the bottom. The story is assembled from a title, a spacer, a paragraph, and a bordered table. After building, `PdfReader` extracts the text — so we see exactly what made it into the PDF.
### Walkthrough 2
Function:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(data, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph("Report", styles["Title"])]
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    story.append(table)
    doc.build(story)
    return path
```

Test:

```python
from pypdf import PdfReader
from pdf_reports import build_pdf

def test_build_pdf(tmp_path):
    data = [["Indicator", "Value"], ["Revenue", "1 200 000"]]
    path = build_pdf(data, tmp_path / "report.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    text = reader.pages[0].extract_text()
    assert "Revenue" in text
```

What's happening here? The function generates a PDF from a table. The test verifies the artifact "from the outside": a page exists, and the text is extracted and contains the keyword. This test catches a missing file, empty pages, and a broken build.
### Walkthrough 3
Function:

```python
def build_story(data):
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Report", styles["Title"]),
        Table(data),
    ]
    return story
```

Test:

```python
from reportlab.platypus import Table, Paragraph
from pdf_reports import build_story

def test_build_story():
    story = build_story([["A", "B"], [1, 2]])
    assert any(isinstance(x, Table) for x in story)
    assert any(isinstance(x, Paragraph) for x in story)
    assert any(isinstance(x, Table) for x in story)
```

What's happening here? We check the story-assembly logic before generating the PDF: it contains both a `Paragraph` and a `Table`. This is a fast unit test — it does not create files but verifies the document structure. It combines nicely with the test from Walkthrough 2: a fast unit test plus a slower integration test.
### Walkthrough 4
Function:

```python
from openpyxl import load_workbook

def xlsx_to_pdf(xlsx_path, pdf_path):
    wb = load_workbook(xlsx_path, data_only=True)
    ws = wb.active
    rows = [list(r) for r in ws.iter_rows(values_only=True) if any(v is not None for v in r)]

    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
    from reportlab.lib import colors
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    table = Table(rows)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    doc.build([table])
    return pdf_path
```

Test:

```python
from openpyxl import Workbook
from pypdf import PdfReader
from pdf_reports import xlsx_to_pdf

def test_xlsx_to_pdf(tmp_path):
    xlsx = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["City", "Population"])
    ws.append(["Moscow", 13_000_000])
    wb.save(xlsx)

    pdf = xlsx_to_pdf(xlsx, tmp_path / "out.pdf")
    reader = PdfReader(str(pdf))
    text = reader.pages[0].extract_text()
    assert "City" in text
    assert "Moscow" in text
```

What's happening here? We read the xlsx and transfer its contents into a PDF table. The test creates the source xlsx, converts it, and verifies the values made it into the PDF. This is a "bridge" between two formats — automation that saves hours of manual work.
### Walkthrough 5
Function:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def build_multipage_pdf(rows, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    for i, row in enumerate(rows):
        story.append(Paragraph(str(row), styles["BodyText"]))
        if (i + 1) % 3 == 0:
            story.append(PageBreak())
    doc.build(story)
    return path
```

Test:

```python
def test_build_multipage_pdf(tmp_path):
    rows = [f"Row {i}" for i in range(1, 8)]
    path = build_multipage_pdf(rows, tmp_path / "multi.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 2
    last_text = reader.pages[-1].extract_text()
    assert "Row 7" in last_text
```

What's happening here? A `PageBreak` is inserted after every three paragraphs — so 7 rows give at least 3 pages. The test checks both the number of pages and that the last data row landed on the last page. This is control over multipage documents: nothing is lost and nothing is glued together.
<!--/SOLUTION-->

<!--QUIZ-->
What does SimpleDocTemplate do?
- Describes a PDF document: path, page size, margins
- Draws a table
- Converts docx to pdf
* Correct answer: Describes a PDF document: path, page size, margins
SimpleDocTemplate is the document framework into which the story of flowables is passed.

What is a story in reportlab?
- A list of flowables: paragraphs, tables, images
- A text file
- A folder with resources
* Correct answer: A list of flowables: paragraphs, tables, images
doc.build(story) assembles the PDF from the list elements.

How do you add a paragraph to the story?
- Paragraph("text", styles["BodyText"])
- add_paragraph("text")
- Text("text")
* Correct answer: Paragraph("text", styles["BodyText"])
Paragraph is a flowable; the second argument — the style — is required.

How do you set table borders in reportlab?
- TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.grey)])
- Table.border(1)
- Style.grid(True)
* Correct answer: TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.grey)])
The GRID operation draws the grid; the coordinates are the start and end column/row.

How do you add a page number to a PDF?
- Via the onFirstPage/onLaterPages callback with canvas.drawCentredString
- Via the page field in Table
- A page number cannot be added
* Correct answer: Via the onFirstPage/onLaterPages callback with canvas.drawCentredString
The callback function receives the canvas, on which the page-number text is drawn.

Which library extracts text from a PDF?
- pypdf (PdfReader)
- openpyxl
- python-docx
* Correct answer: pypdf (PdfReader)
PdfReader opens a PDF; reader.pages[i].extract_text() returns the page text.

Why is data_only=True useful when converting xlsx to PDF?
- Returns calculated formula values if they are stored
- Speeds up PDF work
- Disables Excel
* Correct answer: Returns calculated formula values if they are stored
If the file was recalculated in Excel, data_only returns values instead of formula strings.

What does PageBreak do?
- Starts a new page in the PDF
- Adds an empty paragraph
- Closes the document
* Correct answer: Starts a new page in the PDF
PageBreak is a flowable that breaks the page where it is inserted.

How do you define your own paragraph style in reportlab?
- ParagraphStyle("Name", parent=..., fontSize=..., leading=...)
- Style("Name", size=12)
- Paragraph.set_style("Name")
* Correct answer: ParagraphStyle("Name", parent=..., fontSize=..., leading=...)
ParagraphStyle creates a style; parent sets the base style.

Which method finishes the PDF assembly?
- doc.build(story)
- doc.save(story)
- story.build(doc)
* Correct answer: doc.build(story)
build takes the list of flowables and writes the finished PDF to disk.
<!--/QUIZ-->
