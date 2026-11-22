---
title: "Exam: Office Automation"
summary: Final check of knowledge of openpyxl, python-docx, reportlab, and pytest.
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
Which class creates a new Excel workbook in openpyxl?
- Workbook
- Worksheet
- Cell
* Correct answer: Workbook
Workbook() creates a workbook; the sheets inside are Worksheet objects.

What will load_workbook("f.xlsx", data_only=True) return for a formula if the file was never opened in Excel?
- None
- The formula string
- 0
* Correct answer: None
Cached values appear only after recalculation and saving in Excel.

How do you set a bold font in a cell?
- cell.font = Font(bold=True)
- cell.bold = True
- cell.style = "bold"
* Correct answer: cell.font = Font(bold=True)
The font is set with a Font object via the cell's font property.

What does ws.merge_cells("A1:C1") do?
- Merges cells A1, B1, and C1
- Splits cells
- Hides column A
* Correct answer: Merges cells A1, B1, and C1
After merging, the range becomes one cell, and the data is stored in the top-left cell.

How do you add a bar chart to a sheet?
- Create a BarChart, describe a Reference, and call ws.add_chart(chart, "E2")
- Call ws.bar_chart("E2")
- Insert a picture with the sum
* Correct answer: Create a BarChart, describe a Reference, and call ws.add_chart(chart, "E2")
A chart is assembled from chart and Reference objects and attached with add_chart.

What does a paragraph in python-docx consist of?
- Of runs with uniform formatting
- Of cells
- Of sections
* Correct answer: Of runs with uniform formatting
Bold, size, and color are set on runs.

How do you add a 3×2 table to a Word document?
- doc.add_table(rows=3, cols=2)
- doc.table(3, 2)
- doc.add_rows(3, 2)
* Correct answer: doc.add_table(rows=3, cols=2)
add_table takes the number of rows and columns.

What is a story in reportlab?
- A list of flowables for building a PDF
- A text file
- A folder with pictures
* Correct answer: A list of flowables for building a PDF
doc.build(story) assembles the PDF from paragraphs, tables, and other elements.

How do you extract text from a PDF for verification?
- reader.pages[0].extract_text()
- pdf.text()
- reader.content
* Correct answer: reader.pages[0].extract_text()
PdfReader from the pypdf library returns the page text via extract_text().

Which tool gives a test a temporary folder?
- The tmp_path fixture in pytest
- os.mkdir
- tempfile, always automatically
* Correct answer: The tmp_path fixture in pytest
tmp_path is a built-in fixture; the folder is unique per test and cleaned up after it.
<!--/QUIZ-->
