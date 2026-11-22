---
title: "Word: Advanced Reports and Templates"
summary: Working with docx templates, placeholders, headers and footers, sections, dynamic tables, and merging.
order: 5
duration: 50 min
difficulty: advanced
tags: python-docx, word, templates, reports, sections
---

In this lesson we move from individual blocks to real production reports: templates with placeholders, headers and footers, sections with different orientations, and dynamic tables. All of this is what you need to generate dozens of similar documents.

## Templates and placeholders

Instead of building a document from scratch, you can take a ready-made `.docx` with corporate styling and fill it with data. `Document("template.docx")` opens any existing file, and all `add_*` methods append at the end. To insert data in the middle, use "placeholders" — markers like `{{name}}` that are replaced later:

```python
from docx import Document

doc = Document("template.docx")
for p in doc.paragraphs:
    if "{{company}}" in p.text:
        p.text = "Romashka LLC"
    if "{{date}}" in p.text:
        p.text = "November 1, 2026"
doc.save("report.docx")
```

Assigning `p.text` replaces the whole paragraph text with a single run — simple and reliable. If you need to keep the formatting of part of the text, work with runs individually.

## Headers and footers

Headers and footers live in the section: `section.header` and `section.footer`. By default there is one empty paragraph:

```python
section = doc.sections[0]
header = section.header
header.paragraphs[0].text = "Report | 2026"
footer = section.footer
footer.paragraphs[0].text = "Page "
```

You can also add new paragraphs: `header.add_paragraph("...")`. For different first/even/odd pages there is `section.different_first_page_header_footer`.

## Sections

A section is a "piece" of the document with its own page settings. `doc.add_section(WD_SECTION.NEW_PAGE)` starts a new section on a new page:

```python
from docx.enum.section import WD_SECTION, WD_ORIENT

sec = doc.add_section(WD_SECTION.NEW_PAGE)
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = sec.page_height, sec.page_width
```

When changing orientation, width and height must be swapped — otherwise the page simply "will not turn". This is how a landscape page for a wide table is inserted into a portrait report.

## Dynamic tables

The number of rows is often known only at runtime. `table.add_row()` adds a row at the end:

```python
data = [("Moscow", 13_000_000), ("Saint Petersburg", 5_600_000)]
table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
table.cell(0, 0).text = "City"
table.cell(0, 1).text = "Population"
for city, pop in data:
    row = table.add_row()
    row.cells[0].text = city
    row.cells[1].text = str(pop)
```

Merging cells — the `merge` method:

```python
table.cell(0, 0).merge(table.cell(0, 1))   # merge A1 and B1
```

After merging, `row.cells` gives unique cells: a merged row will have fewer of them — handy to check in tests.

## Merging documents

To glue several reports together, we transfer the source's contents into the target:

```python
def append_document(target, source_path):
    src = Document(source_path)
    for p in src.paragraphs:
        target.add_paragraph(p.text)
    for table in src.tables:
        new_table = target.add_table(rows=len(table.rows), cols=len(table.columns))
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                new_table.cell(r, c).text = cell.text
```

This is a "conveyor belt": several documents are assembled into one final document.

## Checking the result

After generation, always open the result with the same python-docx and check the composition: `doc.paragraphs`, `doc.tables`, `doc.sections`. In template systems, verifying the artifact is what guarantees that no marker was left unreplaced.

<!--TASK-->
### Task 1
Create a template `template.docx` with the text "Company: {{company}}, date: {{date}}, manager: {{manager}}". Then write a script that opens the template, replaces the markers with real values (for example, "Romashka LLC", "2026-11-01", "Ivan Petrov") and saves a new file `filled.docx`. After that, print all paragraphs of `filled.docx`. Expected output: one line without markers with the substituted values.
### Task 2
Write a pytest test for placeholder replacement. The function `render_template(template_path, out_path, replacements)` takes the template path, the result path, and a dictionary `{marker: value}`, replaces all occurrences of the form `{{key}}` in paragraphs, and saves the result. Test: create a template with three markers, call the function, load the result and check that the paragraph text contains the values and the markers are gone.
### Task 3
Write a pytest test for headers and footers. The function `add_header_footer(doc, header_text, footer_text)` writes text into the first paragraph of the first section's header and footer. Test: create a document, call the function, save, load, and check `doc.sections[0].header.paragraphs[0].text` and likewise for the footer.
### Task 4
Write a pytest test for a landscape section. The function `add_landscape_section(doc)` adds a new section starting on a new page, switches it to landscape orientation, and swaps width/height. Test: check that `len(doc.sections) == 2`, `doc.sections[1].orientation == WD_ORIENT.LANDSCAPE` and the width of the second section is greater than its height.
### Task 5
Write a pytest test for a dynamic table with merging. The function `build_report_table(doc, data)` creates a table: the first row is a merged header "Regional totals" via `merge`, the second row has the headers "City, Population", followed by rows from `data`. Test: check `len(doc.tables) == 1`, the number of rows equals `2 + len(data)`, the merged row has `len(table.rows[0].cells) == 1`, and the text of the first cell of the second row is "City".
<!--/TASK-->

<!--HINT-->
### Hint 1
Placeholders are just text, so replacement is iterating over `doc.paragraphs` and `str.replace`. Create the template with the same python-docx: `doc.add_paragraph("Company: {{company}}, date: {{date}}, manager: {{manager}}")`. After replacement, save the result to a new file.
### Hint 2
The `replacements` dictionary holds `{"company": "Romashka LLC", ...}`. In the loop over paragraphs, for each key/value pair do `p.text = p.text.replace("{{" + key + "}}", value)`. In the test, after loading, check: `"{{" not in p.text` and `"Romashka LLC" in p.text`.
### Hint 3
Headers and footers: `doc.sections[0].header.paragraphs[0].text = header_text`. Don't forget to save and reload the document before checking — the header/footer text is read from the file. For the footer: `doc.sections[0].footer.paragraphs[0].text`.
### Hint 4
`doc.add_section(WD_SECTION.NEW_PAGE)` returns the new section. After assigning `sec.orientation = WD_ORIENT.LANDSCAPE`, swap `sec.page_width` and `sec.page_height`. In the test, compare `sec.page_width > sec.page_height`. Import: `from docx.enum.section import WD_SECTION, WD_ORIENT`.
### Hint 5
Merging: `table.cell(0, 0).merge(table.cell(0, 1))`. After that, `table.rows[0].cells` will contain one cell. Add rows with `table.add_row()` and fill them with `row.cells[0].text = ...`. Number of rows: 1 (header) + 1 (column headers) + len(data).
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from docx import Document

doc = Document()
doc.add_paragraph("Company: {{company}}, date: {{date}}, manager: {{manager}}")
doc.save("template.docx")

doc2 = Document("template.docx")
for p in doc2.paragraphs:
    p.text = (p.text.replace("{{company}}", "Romashka LLC")
                   .replace("{{date}}", "2026-11-01")
                   .replace("{{manager}}", "Ivan Petrov"))
doc2.save("filled.docx")

doc3 = Document("filled.docx")
for p in doc3.paragraphs:
    print(p.text)
```

Output:

```
Company: Romashka LLC, date: 2026-11-01, manager: Ivan Petrov
```

What's happening here? The template is an ordinary document with markers. Replacement goes through the text of each paragraph: `str.replace` changes occurrences, and assigning `p.text` rewrites the text as a single run. This approach lets you keep the styling in the template and substitute data programmatically.
### Walkthrough 2
Function:

```python
from docx import Document

def render_template(template_path, out_path, replacements):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, value in replacements.items():
            p.text = p.text.replace("{{" + key + "}}", value)
    doc.save(out_path)
    return out_path
```

Test:

```python
from docx import Document
from reports_word import render_template

def test_render_template(tmp_path):
    tpl = tmp_path / "template.docx"
    doc = Document()
    doc.add_paragraph("{{company}} / {{date}} / {{manager}}")
    doc.save(tpl)

    out = render_template(tpl, tmp_path / "out.docx",
                          {"company": "Romashka LLC", "date": "2026",
                           "manager": "Ivan Petrov"})
    result = Document(out)
    text = result.paragraphs[0].text
    assert "Romashka LLC" in text
    assert "2026" in text
    assert "Ivan Petrov" in text
    assert "{{" not in text
```

What's happening here? The function is universal: it takes a replacement dictionary, so it is easy to extend. The test creates a template, runs the render, and verifies the artifact: values are substituted, no markers remain. This is the key check of template systems — "no placeholder left behind".
### Walkthrough 3
Function:

```python
def add_header_footer(doc, header_text, footer_text):
    section = doc.sections[0]
    section.header.paragraphs[0].text = header_text
    section.footer.paragraphs[0].text = footer_text
    return doc
```

Test:

```python
from docx import Document
from reports_word import add_header_footer

def test_add_header_footer(tmp_path):
    doc = Document()
    add_header_footer(doc, "Report 2026", "Page ?")
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    section = doc2.sections[0]
    assert section.header.paragraphs[0].text == "Report 2026"
    assert section.footer.paragraphs[0].text == "Page ?"
```

What's happening here? Headers and footers are tied to the section: `section.header` and `section.footer` are objects with paragraphs. The first paragraph is empty by default — we write the text into it. Checking after reloading confirms the headers and footers were saved in the file.
### Walkthrough 4
Function:

```python
from docx.enum.section import WD_SECTION, WD_ORIENT

def add_landscape_section(doc):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    return sec
```

Test:

```python
def test_add_landscape_section(tmp_path):
    doc = Document()
    add_landscape_section(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    assert len(doc2.sections) == 2
    sec = doc2.sections[1]
    assert sec.orientation == WD_ORIENT.LANDSCAPE
    assert sec.page_width > sec.page_height
```

What's happening here? The new section starts on a new page. After changing the orientation, width and height are swapped — otherwise `orientation` alone would do nothing. The test checks both the number of sections and the orientation and page geometry.
### Walkthrough 5
Function:

```python
def build_report_table(doc, data):
    table = doc.add_table(rows=2, cols=2)
    table.style = "Table Grid"
    table.cell(0, 0).merge(table.cell(0, 1))
    table.cell(0, 0).text = "Regional totals"
    table.cell(1, 0).text = "City"
    table.cell(1, 1).text = "Population"
    for city, pop in data:
        row = table.add_row()
        row.cells[0].text = city
        row.cells[1].text = str(pop)
    return table
```

Test:

```python
def test_build_report_table(tmp_path):
    doc = Document()
    data = [("Moscow", 13_000_000), ("Saint Petersburg", 5_600_000)]
    build_report_table(doc, data)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    table = doc2.tables[0]
    assert len(doc2.tables) == 1
    assert len(table.rows) == 2 + len(data)
    assert len(table.rows[0].cells) == 1   # merged header
    assert table.cell(1, 0).text == "City"
```

What's happening here? `merge` joins the two cells of the first row — so `table.rows[0].cells` contains one cell. Rows are added dynamically, and the total number of rows is 2 + len(data). The test checks both structure and data — exactly what you need for verifying complex tables.
<!--/SOLUTION-->

<!--QUIZ-->
How do you open an existing document as a template?
- Document("template.docx")
- Template("template.docx")
- OpenTemplate("template.docx")
* Correct answer: Document("template.docx")
The Document constructor opens any .docx, and all add_* calls append at the end.

What is a placeholder in a template?
- A marker like {{company}} that gets replaced with data
- A ready-made document style
- A table with data
* Correct answer: A marker like {{company}} that gets replaced with data
Placeholders are text labels; the program replaces them with real values.

What happens after assigning p.text = "..."?
- The paragraph text is replaced with a single run
- A new paragraph is added
- Nothing; p.text is read-only
* Correct answer: The paragraph text is replaced with a single run
Assigning p.text overwrites the paragraph contents with a single run.

Where do headers and footers live in python-docx?
- In the section: section.header and section.footer
- In a separate file
- In every run
* Correct answer: In the section: section.header and section.footer
Headers and footers are tied to the document section.

How do you add a new section starting on a new page?
- doc.add_section(WD_SECTION.NEW_PAGE)
- doc.new_page()
- doc.add_page_section()
* Correct answer: doc.add_section(WD_SECTION.NEW_PAGE)
add_section creates a section; WD_SECTION.NEW_PAGE means it starts on a new page.

What must you do when switching a section to landscape orientation?
- Swap page_width and page_height
- Nothing; orientation is enough
- Delete the section
* Correct answer: Swap page_width and page_height
Otherwise the page keeps portrait geometry.

How do you add a row to an existing table?
- table.add_row()
- table.append_row()
- row = table.new_row()
* Correct answer: table.add_row()
add_row appends a row at the end of the table and returns it.

How do you merge cells A1 and B1 of a table?
- table.cell(0, 0).merge(table.cell(0, 1))
- table.merge("A1:B1")
- cell.join(0, 1)
* Correct answer: table.cell(0, 0).merge(table.cell(0, 1))
merge is called on a cell and takes the partner cell.

What will table.rows[0].cells return after merging cells in the first row?
- A list with one cell
- A list of two cells
- An error
* Correct answer: A list with one cell
row.cells returns unique cells — merged ones are not duplicated.

How do you check that a document has exactly one table?
- len(doc.tables) == 1
- doc.table_count() == 1
- doc.tables == 1
* Correct answer: len(doc.tables) == 1
doc.tables is the list of all tables in the document.
<!--/QUIZ-->
