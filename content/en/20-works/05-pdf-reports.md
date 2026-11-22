---
title: Automated PDF reports
summary: Generate PDFs with data.
order: 5
duration: 50 min
difficulty: advanced
tags: pdf, reportlab
---

Generate professional PDFs programmatically.

## ReportLab

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("report.pdf", pagesize=A4)
c.drawString(72, 800, "Sales report")
c.drawString(72, 780, f"Total: {total}")
c.save()
```

## Table

```python
from reportlab.platypus import SimpleDocTemplate, Table

doc = SimpleDocTemplate("table.pdf")
data = [["Product", "Total"], *rows]
doc.build([Table(data)])
```

## Lesson summary

canvas for basics; platypus for layouts.

<!--TASK-->
### Task 1 — Canvas
Create a PDF with a title.

### Task 2 — Text
Add data lines.

### Task 3 — Page size
Use A4.

### Task 4 — Table
Build a table.

### Task 5 — Save
Save and check.

### Task 6 — From data
Read CSV → PDF.

### Task 7 — Style
Style the table.
<!--/TASK-->

<!--HINT-->
### Hint 1
canvas.Canvas.

### Hint 2
drawString.

### Hint 3
A4.

### Hint 4
Table.

### Hint 5
save().

### Hint 6
CSV.

### Hint 7
TableStyle.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from reportlab.pdfgen import canvas
c = canvas.Canvas("report.pdf")
c.drawString(72, 800, "Sales report")
c.save()
```

### Solution 2
```python
c.drawString(72, 780, f"Total: {total}")
```

### Solution 3
```python
from reportlab.lib.pagesizes import A4
c = canvas.Canvas("report.pdf", pagesize=A4)
```

### Solution 4
```python
from reportlab.platypus import SimpleDocTemplate, Table
doc = SimpleDocTemplate("table.pdf")
data = [["Product", "Total"], ["A", 100], ["B", 200]]
doc.build([Table(data)])
```

### Solution 5
```python
c.save()
# файл создан рядом; открыть и проверить
```

### Solution 6
```python
import csv
from reportlab.platypus import SimpleDocTemplate, Table

rows = list(csv.reader(open("sales.csv", encoding="utf-8")))
SimpleDocTemplate("report.pdf").build([Table(rows)])
```

### Solution 7
```python
from reportlab.platypus import TableStyle
from reportlab.lib import colors

style = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
])
table = Table(data)
table.setStyle(style)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is ReportLab?
- PDF library
- Word
- Browser
- None
* Correct answer: PDF library
Generate.

What is canvas?
- Drawing surface
- A page
- A table
- None
* Correct answer: Drawing surface
Basic.

What is drawString?
- Draws text
- Draws image
- Saves
- None
* Correct answer: Draws text
At x,y.

What is A4?
- Page size
- Font
- Color
- None
* Correct answer: Page size
297×210.

What is save?
- Writes file
- Opens
- Draws
- None
* Correct answer: Writes file
Finish.

What is platypus?
- High-level layout
- Canvas
- Colors
- None
* Correct answer: High-level layout
SimpleDocTemplate.

What is a Table?
- Table object
- A page
- A canvas
- None
* Correct answer: Table object
Data.

What is SimpleDocTemplate?
- Document builder
- Canvas
- Table
- None
* Correct answer: Document builder
Build.

What is TableStyle?
- Formatting
- Data
- Page
- None
* Correct answer: Formatting
Grid.

What is colors.grey?
- Fill color
- Font
- Size
- None
* Correct answer: Fill color
Style.

What is build?
- Creates document
- Draws
- Saves
- None
* Correct answer: Creates document
Flowables.

What is a flowable?
- Layout element
- A page
- A file
- None
* Correct answer: Layout element
Table/Paragraph.
<!--/QUIZ-->
