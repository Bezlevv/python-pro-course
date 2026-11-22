---
title: Word automation: python-docx
summary: Create and edit .docx.
order: 1
duration: 45 min
difficulty: intermediate
tags: docx, office
---

python-docx works with Word documents.

## Create

```python
from docx import Document

doc = Document()
doc.add_heading("Report", level=0)
doc.add_paragraph("Hello, world!")
doc.save("report.docx")
```

## Table

```python
table = doc.add_table(rows=2, cols=2)
table.cell(0, 0).text = "Name"
table.cell(0, 1).text = "Value"
```

## Lesson summary

Document → paragraphs → tables → save.

<!--TASK-->
### Task 1 — Document
Create a Document.

### Task 2 — Heading
Add a heading.

### Task 3 — Paragraph
Add text.

### Task 4 — Table
Add a table and fill cells.

### Task 5 — Read
Open and print paragraphs.

### Task 6 — Save
Save as .docx.

### Task 7 — Styles
Apply a built-in style.
<!--/TASK-->

<!--HINT-->
### Hint 1
Document().

### Hint 2
add_heading.

### Hint 3
add_paragraph.

### Hint 4
add_table.

### Hint 5
paragraphs.

### Hint 6
save.

### Hint 7
style.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from docx import Document
doc = Document()
```

### Solution 2
```python
doc.add_heading("Report", level=0)
```

### Solution 3
```python
doc.add_paragraph("Hello, world!")
```

### Solution 4
```python
table = doc.add_table(rows=2, cols=2)
table.cell(0, 0).text = "Name"
table.cell(0, 1).text = "Value"
table.cell(1, 0).text = "Alice"
table.cell(1, 1).text = "30"
```

### Solution 5
```python
doc = Document("report.docx")
for p in doc.paragraphs:
    print(p.text)
```

### Solution 6
```python
doc.save("report.docx")
```

### Solution 7
```python
p = doc.add_paragraph("Styled")
p.style = doc.styles["Intense Quote"]
```
<!--/SOLUTION-->

<!--QUIZ-->
What is python-docx?
- Word library
- Excel
- PDF
- None
* Correct answer: Word library
docx.

What is Document?
- File object
- Paragraph
- Table
- None
* Correct answer: File object
Create/open.

What is add_heading?
- Title
- Paragraph
- Table
- None
* Correct answer: Title
Level.

What is add_paragraph?
- Text block
- Heading
- Table
- None
* Correct answer: Text block
Paragraph.

What is add_table?
- Table
- Heading
- Text
- None
* Correct answer: Table
Rows/cols.

What is a cell?
- One box
- Row
- Document
- None
* Correct answer: One box
Text.

What is paragraphs?
- Text list
- Tables
- Styles
- None
* Correct answer: Text list
Read.

What is save?
- Writes file
- Opens
- Closes
- None
* Correct answer: Writes file
Name.

What is a style?
- Format preset
- Text
- Table
- None
* Correct answer: Format preset
Intense.

What is level?
- Heading depth
- Size
- Style
- None
* Correct answer: Heading depth
0–9.

What is .text?
- String content
- Object
- File
- None
* Correct answer: String content
Cell.

What is the benefit?
- Automated docs
- Manual
- Required
- None
* Correct answer: Automated docs
Reports.
<!--/QUIZ-->
