---
title: PDF: reading with PyPDF2
summary: Extract text, pages, metadata.
order: 3
duration: 40 min
difficulty: intermediate
tags: pdf, pypdf
---

PyPDF2 works with existing PDFs.

## Read

```python
from pypdf import PdfReader

reader = PdfReader("file.pdf")
print(len(reader.pages))
page = reader.pages[0]
print(page.extract_text())
```

## Metadata

```python
print(reader.metadata.title)
```

## Lesson summary

PdfReader → pages → text.

<!--TASK-->
### Task 1 — Reader
Create PdfReader.

### Task 2 — Count
Print the page count.

### Task 3 — Extract
Text from page 0.

### Task 4 — Loop
Loop over all pages.

### Task 5 — Metadata
Print the title.

### Task 6 — Save text
Write all text to a file.

### Task 7 — Scanned
What if text is empty?
<!--/TASK-->

<!--HINT-->
### Hint 1
PdfReader.

### Hint 2
len(pages).

### Hint 3
extract_text().

### Hint 4
for.

### Hint 5
metadata.

### Hint 6
write.

### Hint 7
OCR.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```

### Solution 2
```python
print(len(reader.pages))
```

### Solution 3
```python
text = reader.pages[0].extract_text()
print(text)
```

### Solution 4
```python
for i, page in enumerate(reader.pages):
    print(i, page.extract_text()[:100])
```

### Solution 5
```python
print(reader.metadata.title)
```

### Solution 6
```python
with open("out.txt", "w", encoding="utf-8") as f:
    for page in reader.pages:
        f.write(page.extract_text() + "\n")
```

### Solution 7
```text
Сканированные PDF — это изображения;
нужен OCR (например, Tesseract)
```
<!--/SOLUTION-->

<!--QUIZ-->
What is PyPDF2?
- PDF library
- Word
- Image
- None
* Correct answer: PDF library
pypdf.

What is PdfReader?
- Opens PDF
- Creates
- Saves
- None
* Correct answer: Opens PDF
Read.

What is pages?
- Page list
- Text
- Metadata
- None
* Correct answer: Page list
Count.

What is extract_text?
- Gets text
- Gets image
- Gets size
- None
* Correct answer: Gets text
Page.

What is metadata?
- Document info
- Text
- Pages
- None
* Correct answer: Document info
Title.

What is a scanned PDF?
- Image pages
- Text pages
- Empty
- None
* Correct answer: Image pages
OCR.

What is OCR?
- Recognizes text
- Reads text
- Converts
- None
* Correct answer: Recognizes text
Tesseract.

What is a page?
- One sheet
- File
- Text
- None
* Correct answer: One sheet
Index.

What is the loop?
- All pages
- First only
- Last
- None
* Correct answer: All pages
Process.

What is encoding?
- utf-8
- Format
- Size
- None
* Correct answer: utf-8
Write.

What is a reader?
- Parses file
- Writes
- Draws
- None
* Correct answer: Parses file
Object.

What is the limitation?
- Complex layouts
- Simple text
- None
- Always
* Correct answer: Complex layouts
Order.
<!--/QUIZ-->
