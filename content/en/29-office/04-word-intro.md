---
title: "python-docx: Documents, Styles, Tables"
summary: Creating Word documents: paragraphs, styles, tables, images, sections, and saving.
order: 4
duration: 45 min
difficulty: intermediate
tags: python-docx, word, documents, styles, tables
---

python-docx is a library for creating and editing Word documents (`.docx`) without Word itself. A `.docx` document is XML inside a zip archive, and python-docx works with this structure carefully. Installation:

```bash
pip install python-docx
```

## Basic objects

A document is built hierarchically: `Document` → `section` → `paragraph` → `run` (a text fragment with uniform formatting), and also `table` → `row` → `cell` → paragraphs.

```python
from docx import Document

doc = Document()               # new empty document
p = doc.add_paragraph("Hello!")  # paragraph
doc.save("hello.docx")
```

An empty `Document()` already contains one empty paragraph. Any text is a sequence of `run`s. Formatting properties — bold, italic, size, color — hang on `run`s.

```python
p = doc.add_paragraph()
run = p.add_run("Important message")
run.bold = True
run.italic = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

## Headings and styles

Headings are added with `add_heading`, styles by assigning `paragraph.style`:

```python
doc.add_heading("Report", level=1)          # level-1 heading
doc.add_heading("Subsection", level=2)

p = doc.add_paragraph("Normal text")
p.style = doc.styles["Heading 2"]          # apply a ready-made style
```

Built-in styles: `"Title"`, `"Heading 1"`, `"Heading 2"`, `"Normal"`, `"Quote"`, `"Intense Quote"` and others. `doc.styles` is the document's style collection.

## Paragraph alignment

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

p = doc.add_paragraph("Centered")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

## Tables

```python
table = doc.add_table(rows=2, cols=3)
table.cell(0, 0).text = "Cell A1"
table.cell(0, 1).text = "Cell B1"
table.add_row()                 # add a row
table.style = "Light Grid Accent 1"
```

A cell is a mini-document with its own paragraphs. `table.style` takes the name of a built-in Word table style.

## Images

`add_picture` inserts a picture into a new paragraph. Width and height can be set in inches (`Inches`) or centimeters (`Cm`):

```python
from docx.shared import Inches, Pt, Cm, RGBColor

doc.add_picture("logo.png", width=Inches(2))
```

If you need a picture inside a specific paragraph, add it via a run:

```python
p = doc.add_paragraph()
p.add_run().add_picture("logo.png", height=Cm(3))
```

For an example, let's generate an image with the Pillow library (installed with `pip install pillow`):

```python
from PIL import Image

img = Image.new("RGB", (200, 100), "steelblue")
img.save("logo.png")
```

## Sections and the page

A document has sections (`doc.sections`) — areas with their own page settings. By default there is one section:

```python
section = doc.sections[0]
print(section.page_width, section.page_height)
```

`doc.add_page_break()` inserts a page break into the current text flow.

## Reading a document

A finished document is opened with the same class:

```python
doc2 = Document("hello.docx")
for p in doc2.paragraphs:
    print(p.text)
print("Tables:", len(doc2.tables))
```

`doc.paragraphs` is all paragraphs, `doc.tables` is all tables. This is the basis for tests: generate a document, open it, and check the contents.

## Complete example

Let's assemble a mini-report: a heading, a paragraph, a table, and a picture.

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

Image.new("RGB", (200, 100), "steelblue").save("logo.png")

doc = Document()
doc.add_heading("Sales report", level=1)

p = doc.add_paragraph("Quarterly results.")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

table = doc.add_table(rows=2, cols=2)
table.style = "Light Grid Accent 1"
table.cell(0, 0).text = "Indicator"
table.cell(0, 1).text = "Value"
table.cell(1, 0).text = "Revenue"
table.cell(1, 1).text = "1 200 000"

doc.add_picture("logo.png", width=Inches(1.5))
doc.save("report.docx")
print("Done: report.docx")
```

<!--TASK-->
### Task 1
Create a file `resume.docx`: a level-1 heading "Resume", a paragraph with a name and position (for example, "Ivan Petrov — Python developer"), a list of three skills (paragraphs with bullets or plain paragraphs), and a 2×2 table "Language → Level" (Python → Advanced, SQL → Intermediate). Save the document, then load it again and print all paragraphs and the number of table rows. Expected output: the paragraph texts and the row count.
### Task 2
Write a pytest test for the contents of a docx artifact. The function `create_document(path)` creates a document with three paragraphs, the middle one being bold (a run with `bold=True`), saves it to the path and returns the path. Test: load the document via `Document(path)` and check that `len(doc.paragraphs) == 3`, the second paragraph contains text, and its first run has `bold is True`.
### Task 3
Write a pytest test for a table. The function `add_skills_table(doc)` adds a 3×2 table with the style `"Light Grid Accent 1"` to the document, filling it with headers and two data rows. Test: create a document, call the function, save to `tmp_path`, load, and check: `len(doc.tables) == 1`, `len(table.rows) == 3`, `len(table.columns) == 2` and `table.cell(0, 0).text == "Language"`.
### Task 4
Write a pytest test for inserting an image. The function `add_logo(doc, image_path)` inserts a picture 2 inches wide. Test: create an image with Pillow (for example, a red 100×50 rectangle) in `tmp_path`, call the function, save the document, load it and check: `len(doc.inline_shapes) == 1` and `doc.inline_shapes[0].width` is greater than zero.
### Task 5
Write a pytest test for run formatting. The function `style_summary(doc)` adds a paragraph with a run that is bold, italic, 14 pt, and red (`RGBColor(0xFF, 0, 0)`). Test: save the document, load it, find the last paragraph, take its first run and check all four properties.
<!--/TASK-->

<!--HINT-->
### Hint 1
Paragraphs are added with `doc.add_paragraph(...)`, a heading with `doc.add_heading("Resume", level=1)`. Table: `doc.add_table(rows=3, cols=2)` and filling via `table.cell(r, c).text`. After saving, reopen the document: `doc2 = Document("resume.docx")`, then `for p in doc2.paragraphs: print(p.text)` and `print(len(doc2.tables[0].rows))`.
### Hint 2
Bold is set on a run: `run.bold = True`. To check exactly that run, create the paragraph explicitly: `p = doc.add_paragraph(); run = p.add_run("text"); run.bold = True`. In the test: `p = doc.paragraphs[1]; assert p.runs[0].bold is True`.
### Hint 3
After loading the document, access the table with `table = doc.tables[0]`. The number of rows is `len(table.rows)`, columns — `len(table.columns)`. Cell text — `table.cell(0, 0).text`. Don't forget to assign the style `table.style = "Light Grid Accent 1"` before filling.
### Hint 4
`doc.inline_shapes` is the list of the document's inline images; each has a `width` (in EMU, a number). Checking `shape.width > 0` guarantees the picture was inserted with a non-zero size. Set the width like this: `doc.add_picture(image_path, width=Inches(2))`.
### Hint 5
Run properties: `bold`, `italic`, `font.size` (a Pt object — compare `run.font.size.pt == 14`), `font.color.rgb` (compare with `RGBColor(0xFF, 0, 0)`). Imports: `from docx.shared import Pt, RGBColor`. If the paragraph has one run, take `p.runs[0]`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from docx import Document

doc = Document()
doc.add_heading("Resume", level=1)
doc.add_paragraph("Ivan Petrov — Python developer")
for skill in ["Python", "SQL", "Git"]:
    doc.add_paragraph(f"- {skill}")

table = doc.add_table(rows=3, cols=2)
table.cell(0, 0).text = "Language"
table.cell(0, 1).text = "Level"
table.cell(1, 0).text = "Python"
table.cell(1, 1).text = "Advanced"
table.cell(2, 0).text = "SQL"
table.cell(2, 1).text = "Intermediate"

doc.save("resume.docx")

doc2 = Document("resume.docx")
for p in doc2.paragraphs:
    print(p.text)
table2 = doc2.tables[0]
print("Rows in table:", len(table2.rows))
```

The output contains the paragraph texts and the line `Rows in table: 3`. What's happening here? We assembled a document from standard blocks: a heading, paragraphs, a table. When reopened, `doc.paragraphs` yields all paragraphs (including the heading), and `doc.tables[0]` the first table. The row count `len(table2.rows)` confirms the table was written in full.
### Walkthrough 2
Function:

```python
from docx import Document

def create_document(path):
    doc = Document()
    doc.add_paragraph("First paragraph")
    p = doc.add_paragraph()
    run = p.add_run("Second, bold")
    run.bold = True
    doc.add_paragraph("Third paragraph")
    doc.save(path)
    return path
```

Test:

```python
from docx import Document
from word_docs import create_document

def test_create_document(tmp_path):
    path = create_document(tmp_path / "doc.docx")
    doc = Document(path)
    assert len(doc.paragraphs) == 3
    p = doc.paragraphs[1]
    assert p.text == "Second, bold"
    assert p.runs[0].bold is True
```

What's happening here? The function builds a document and returns the path — the test opens the artifact from disk. Paragraphs are counted via `doc.paragraphs`, and formatting is checked on a specific run. If the bold were not on the run but somewhere else, the test would catch it.
### Walkthrough 3
Function:

```python
def add_skills_table(doc):
    table = doc.add_table(rows=3, cols=2)
    table.style = "Light Grid Accent 1"
    table.cell(0, 0).text = "Language"
    table.cell(0, 1).text = "Level"
    table.cell(1, 0).text = "Python"
    table.cell(1, 1).text = "Advanced"
    table.cell(2, 0).text = "SQL"
    table.cell(2, 1).text = "Intermediate"
    return table
```

Test:

```python
from docx import Document
from word_docs import add_skills_table

def test_add_skills_table(tmp_path):
    doc = Document()
    add_skills_table(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    table = doc2.tables[0]
    assert len(doc2.tables) == 1
    assert len(table.rows) == 3
    assert len(table.columns) == 2
    assert table.cell(0, 0).text == "Language"
```

What's happening here? The test verifies the real file after a round-trip: one table, 3 rows, 2 columns, and the contents of the first cell. `table.cell(0, 0).text` reads the cell text — a reliable way to check document data.
### Walkthrough 4
Function and test:

```python
from docx.shared import Inches

def add_logo(doc, image_path):
    doc.add_picture(image_path, width=Inches(2))
    return doc
```

```python
from docx import Document
from PIL import Image
from word_docs import add_logo

def test_add_logo(tmp_path):
    img_path = tmp_path / "logo.png"
    Image.new("RGB", (100, 50), "red").save(img_path)

    doc = Document()
    add_logo(doc, img_path)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    assert len(doc2.inline_shapes) == 1
    assert doc2.inline_shapes[0].width > 0
```

What's happening here? The image is created with Pillow right in the temporary folder — the test does not depend on external files. `inline_shapes` contains inline images; the width is stored in EMU units, so we check "greater than zero". This confirms the picture actually made it into the document.
### Walkthrough 5
Function:

```python
from docx.shared import Pt, RGBColor

def style_summary(doc):
    p = doc.add_paragraph()
    run = p.add_run("Summary")
    run.bold = True
    run.italic = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0xFF, 0, 0)
    return p
```

Test:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from word_docs import style_summary

def test_style_summary(tmp_path):
    doc = Document()
    style_summary(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    run = doc2.paragraphs[-1].runs[0]
    assert run.bold is True
    assert run.italic is True
    assert run.font.size.pt == 14
    assert run.font.color.rgb == RGBColor(0xFF, 0, 0)
```

What's happening here? All four properties are set on one run. After loading, we take the document's last paragraph and its first run. `run.font.size.pt == 14` checks the size in points, and `run.font.color.rgb` the color. These are exactly the checks needed to control report formatting.
<!--/SOLUTION-->

<!--QUIZ-->
How do you create a new Word document in python-docx?
- Document()
- Word()
- Docx()
* Correct answer: Document()
The Document class opens a new document or an existing file.

What does a paragraph in python-docx consist of?
- Of runs (text fragments)
- Of cells
- Of sections
* Correct answer: Of runs (text fragments)
Each run is a piece of text with its own properties (bold, color, size).

How do you make text bold?
- run.bold = True
- paragraph.bold = True
- Text.bold = True
* Correct answer: run.bold = True
Bold is a property of the run, not of the whole paragraph.

How do you add a level-2 heading?
- doc.add_heading("Text", level=2)
- doc.add_title("Text", 2)
- doc.add_paragraph("Text", style="H2")
* Correct answer: doc.add_heading("Text", level=2)
add_heading creates a paragraph with the style of the corresponding level.

How do you add a 3×4 table?
- doc.add_table(rows=3, cols=4)
- doc.create_table(3, 4)
- doc.add_table(3, 4)
* Correct answer: doc.add_table(rows=3, cols=4)
add_table takes the number of rows and columns as keyword arguments.

How do you write text into a table cell?
- table.cell(0, 0).text = "Hello"
- table[0][0] = "Hello"
- cell.write("Hello")
* Correct answer: table.cell(0, 0).text = "Hello"
table.cell(r, c) returns the cell, which has a text property.

What does doc.add_picture("logo.png", width=Inches(2)) do?
- Inserts the image into a new paragraph with a width of 2 inches
- Inserts the image replacing text
- Saves the image as a separate file
* Correct answer: Inserts the image into a new paragraph with a width of 2 inches
add_picture adds the image as an inline shape; the size is set in Inches or Cm.

How do you open an existing document?
- Document("file.docx")
- open("file.docx")
- Load("file.docx")
* Correct answer: Document("file.docx")
Pass the path to the Document constructor — you get a document for reading and editing.

Where do you get the list of all paragraphs of a document?
- doc.paragraphs
- doc.runs
- doc.text
* Correct answer: doc.paragraphs
The paragraphs property returns all paragraphs of the document in order.

What is a section in python-docx?
- An area with its own page settings
- A separate paragraph
- A table
* Correct answer: An area with its own page settings
A document has at least one section; each has its own margins, orientation, and page size.
<!--/QUIZ-->
