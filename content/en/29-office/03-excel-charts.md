---
title: "Excel: Charts and Report Styling"
summary: Building charts with openpyxl.chart, customizing the look, preparing a sheet for printing.
order: 3
duration: 45 min
difficulty: intermediate
tags: openpyxl, charts, chart, reports, printing
---

Charts are the best way to make a report visual. openpyxl can build standard chart types: bar, line, and pie. All you need is to describe the data with references to worksheet ranges, and the library itself packs them into a chart object that Excel will show when the file is opened.

## The basics: Reference and add_chart

Chart work goes through the submodule `openpyxl.chart`. First, create a chart object, then describe a reference to the data (`Reference`) and place the chart on the sheet:

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active
ws.append(["Month", "Sales", "Profit"])
ws.append(["January", 120, 30])
ws.append(["February", 150, 40])
ws.append(["March", 90, 20])

chart = BarChart()
data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "E2")
wb.save("sales.xlsx")
```

Breakdown: `Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)` — a data rectangle of two columns (Sales and Profit) together with the header. `add_data(data, titles_from_data=True)` understands that the first row contains the series names. `set_categories(cats)` supplies the categories for the X-axis (months). The result: `ws.add_chart(chart, "E2")` attaches the chart to the sheet, starting at cell E2.

## Configuring the chart

A chart object has many properties:

```python
chart.title = "Sales by Month"
chart.style = 10            # built-in palette (0–48)
chart.y_axis.title = "thousand RUB"
chart.x_axis.title = "Month"
chart.width = 20            # width in centimeters
chart.height = 10
chart.legend.position = "bottom"
```

Value labels are enabled via `DataLabelList`:

```python
from openpyxl.chart.label import DataLabelList

chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True
```

A series color is changed via `graphicalProperties`:

```python
chart.series[0].graphicalProperties.solidFill = "4472C4"
```

## Pie chart

`PieChart` works almost the same, but it has no axes, and the data is a single series:

```python
from openpyxl.chart import PieChart

pie = PieChart()
data = Reference(ws, min_col=2, min_row=1, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
pie.add_data(data, titles_from_data=True)
pie.set_categories(cats)
pie.title = "Sales Structure"
ws.add_chart(pie, "E18")
```

A sheet can hold any number of charts — each is attached with its own coordinate.

## Styling and printing

Before sending a report, it is worth configuring the sheet: hide the grid, set the print area and page orientation:

```python
ws.sheet_view.showGridLines = False
ws.print_area = "A1:F15"
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.sheet_properties.tabColor = "4472C4"   # tab color
```

`print_area` limits printing to a range; `fitToWidth`/`fitToHeight` fit the sheet onto one printed page; `showGridLines = False` removes the gray grid from the screen.

## Checking charts

Charts are stored in the list `ws._charts`. Although the attribute is semi-official (it has an underscore), this is exactly how they are read in tests:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active
print(len(ws._charts))       # number of charts
print(ws._charts[0].title)   # title of the first chart
```

This lets you write pytest tests that verify a report really contains a chart with the required title.

<!--TASK-->
### Task 1
Create a file `sales_chart.xlsx`: sheet "Sales" with a header "Month, Sales, Profit" and six months (January–June) with arbitrary numbers. Add a bar chart titled "Sales by Month", with value labels, a legend at the bottom, and the first series in blue. Save the file, then load it again and print the number of charts on the sheet and the title of the first one. Expected output: `1` and `Sales by Month`.
### Task 2
Write a pytest test that checks for a chart in the xlsx artifact. The function `make_sales_chart(path)` creates a workbook with sales data (as in Task 1) and a bar chart titled "Sales by Month", saves it to the path and returns the path. Test: call the function with `tmp_path / "sales.xlsx"`, load the workbook, check that `len(ws._charts) == 1` and that `ws._charts[0].title == "Sales by Month"`.
### Task 3
Write a pytest test for a pie chart. The function `make_pie_chart(path)` creates a workbook with category data (name and value) and a pie chart titled "Structure". Test: after saving and loading, check that the sheet has exactly one chart, it is an instance of `PieChart` (import it from `openpyxl.chart.pie_chart`), and its title equals "Structure".
### Task 4
Write a pytest test for print settings. The function `setup_print(ws)` configures the sheet: hides the grid (`showGridLines = False`), sets the print area `A1:F15`, orientation `landscape`, and tab color `4472C4`. Test: create a workbook, call the function, save to `tmp_path`, load, and check: `ws.page_setup.orientation == "landscape"`, `ws.sheet_view.showGridLines is False`, `ws.sheet_properties.tabColor.rgb` ends with `4472C4`, and `ws.print_area` contains `A1:F15` (after loading it may become `$A$1:$F$15` — allow both forms).
### Task 5
Write a pytest test for a complete report. The function `build_report(path)` creates a sheet "Report" with data, a bar chart, and print settings (everything from Tasks 2 and 4). The test loads the artifact and checks everything at once: there is one chart with the title, orientation `landscape`, the grid is hidden, the print area is set.
<!--/TASK-->

<!--HINT-->
### Hint 1
It is convenient to add data with `ws.append([...])` in a loop over a list of months. Build data references with `Reference(ws, min_col=2, max_col=3, min_row=1, max_row=7)` (header + 6 months). Value labels: `chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True`. First series color: `chart.series[0].graphicalProperties.solidFill = "4472C4"`.
### Hint 2
The function should save the workbook to the given path and return it. In the test, just check `ws._charts`: it is a list of chart objects. A chart has a `title` property — compare it with the expected title. Don't forget to import `BarChart` and `Reference`.
### Hint 3
`PieChart` is imported from `openpyxl.chart.pie_chart`. Type check: `isinstance(chart, PieChart)`. A pie chart is created the same way as a bar chart, but without axes. `add_data` with `titles_from_data=True` and `set_categories` are required.
### Hint 4
The tab color after loading: `ws.sheet_properties.tabColor.rgb` — compare with `endswith("4472C4")` to avoid depending on the ARGB format. `print_area` may become `$A$1:$F$15` when reopened — use `in ("A1:F15", "$A$1:$F$15")` or check `"A1:F15" in ws.print_area`.
### Hint 5
Assemble `build_report` from ready-made functions: `make_sales_chart` (without saving — return the workbook) and `setup_print`. To do this, split the functions so that `make_sales_chart` returns `(wb, ws)`, and `setup_print` takes `ws`. In the test, check all settings with a single call.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

wb = Workbook()
ws = wb.active
ws.title = "Sales"
ws.append(["Month", "Sales", "Profit"])
months = [("January", 120, 30), ("February", 150, 40), ("March", 90, 20),
          ("April", 170, 45), ("May", 200, 55), ("June", 180, 50)]
for row in months:
    ws.append(row)

chart = BarChart()
data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=7)
cats = Reference(ws, min_col=1, min_row=2, max_row=7)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.title = "Sales by Month"
chart.legend.position = "bottom"
chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True
chart.series[0].graphicalProperties.solidFill = "4472C4"
ws.add_chart(chart, "E2")

wb.save("sales_chart.xlsx")

wb2 = load_workbook("sales_chart.xlsx")
ws2 = wb2["Sales"]
print(len(ws2._charts))
print(ws2._charts[0].title)
```

Output:

```
1
Sales by Month
```

What's happening here? The data is written with `append`. The chart is assembled from references: `data` covers both numeric columns with the header, and `cats` covers the months. Value labels, the legend, and the series color are configured with chart properties. After saving, `ws._charts` contains one chart with the required title — this is how we verify the chart actually made it into the file.
### Walkthrough 2
Module (fragment):

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

def make_sales_chart(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales"
    ws.append(["Month", "Sales", "Profit"])
    for name, s, p in [("January", 120, 30), ("February", 150, 40), ("March", 90, 20)]:
        ws.append([name, s, p])

    chart = BarChart()
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = "Sales by Month"
    chart.dataLabels = DataLabelList()
    chart.dataLabels.showVal = True
    ws.add_chart(chart, "E2")

    wb.save(path)
    return path
```

Test:

```python
from openpyxl import load_workbook
from report_charts import make_sales_chart

def test_make_sales_chart(tmp_path):
    path = make_sales_chart(tmp_path / "sales.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert len(ws._charts) == 1
    assert ws._charts[0].title == "Sales by Month"
```

What's happening here? The function encapsulates report creation, and the test verifies the artifact on disk. `ws._charts` is the list of the sheet's charts; it contains exactly one, and its title matches. This test catches regressions: if someone removes the chart or changes the title, the test fails.
### Walkthrough 3
Function:

```python
from openpyxl.chart import PieChart, Reference

def make_pie_chart(path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Category", "Share"])
    ws.append(["Laptops", 45])
    ws.append(["Mice", 25])
    ws.append(["Keyboards", 30])

    pie = PieChart()
    data = Reference(ws, min_col=2, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(cats)
    pie.title = "Structure"
    ws.add_chart(pie, "D2")

    wb.save(path)
    return path
```

Test:

```python
from openpyxl.chart.pie_chart import PieChart
from report_charts import make_pie_chart

def test_make_pie_chart(tmp_path):
    path = make_pie_chart(tmp_path / "pie.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert len(ws._charts) == 1
    chart = ws._charts[0]
    assert isinstance(chart, PieChart)
    assert chart.title == "Structure"
```

What's happening here? `PieChart` is a separate class (not a subclass of `BarChart`), so the `isinstance` check is precise. A pie chart has no axes: one data series and categories are enough. The title is saved in the file and read back.
### Walkthrough 4
Function:

```python
def setup_print(ws):
    ws.sheet_view.showGridLines = False
    ws.print_area = "A1:F15"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.sheet_properties.tabColor = "4472C4"
    return ws
```

Test:

```python
from openpyxl import Workbook, load_workbook
from report_charts import setup_print

def test_setup_print(tmp_path):
    wb = Workbook()
    ws = wb.active
    setup_print(ws)
    path = tmp_path / "print.xlsx"
    wb.save(path)

    wb2 = load_workbook(path)
    ws2 = wb2.active
    assert ws2.page_setup.orientation == "landscape"
    assert ws2.sheet_view.showGridLines is False
    assert str(ws2.sheet_properties.tabColor.rgb).endswith("4472C4")
    assert "A1:F15" in ws2.print_area
```

What's happening here? Print settings are saved to the file and read back. `print_area` becomes an absolute reference `$A$1:$F$15` when reopened, so we check with `in`. The tab color is compared with `endswith` — the ARGB format adds transparency to the beginning of the string.
### Walkthrough 5
Assembly:

```python
def build_report(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Report"
    ws.append(["Month", "Sales"])
    for name, s in [("January", 120), ("February", 150), ("March", 90)]:
        ws.append([name, s])

    chart = BarChart()
    data = Reference(ws, min_col=2, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = "Sales"
    ws.add_chart(chart, "D2")
    setup_print(ws)

    wb.save(path)
    return path
```

Test:

```python
def test_build_report(tmp_path):
    path = build_report(tmp_path / "report.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert len(ws._charts) == 1
    assert ws._charts[0].title == "Sales"
    assert ws.page_setup.orientation == "landscape"
    assert ws.sheet_view.showGridLines is False
    assert "A1:F15" in ws.print_area
```

What's happening here? `build_report` combines data, a chart, and print settings into one report. The integration test verifies the artifact as a whole: the chart is in place, the page is landscape, the grid is hidden, the print area is set. This is exactly what should be automated when shipping regular reports.
<!--/SOLUTION-->

<!--QUIZ-->
From which submodule is BarChart imported?
- openpyxl.chart
- openpyxl.styles
- openpyxl.cell
* Correct answer: openpyxl.chart
All charts live in openpyxl.chart: BarChart, LineChart, PieChart and others.

What does the Reference object describe?
- A reference to a range of worksheet cells
- A cell style
- A number format
* Correct answer: A reference to a range of worksheet cells
Reference(ws, min_col=..., min_row=..., max_col=..., max_row=...) defines the data rectangle for a chart.

What does add_data(data, titles_from_data=True) do?
- Adds a data series, treating the first row as series titles
- Adds categories
- Saves the workbook
* Correct answer: Adds a data series, treating the first row as series titles
The titles_from_data flag tells the library that the header row contains series labels.

Why is set_categories(cats) needed?
- To set the X-axis labels
- To set the chart color
- To add value labels
* Correct answer: To set the X-axis labels
Categories are the X-axis labels (for example, months or categories).

How do you attach a chart to a sheet?
- ws.add_chart(chart, "E2")
- chart.attach(ws)
- ws.charts.append(chart)
* Correct answer: ws.add_chart(chart, "E2")
add_chart places the chart on the sheet, starting at the given cell.

How do you turn on value labels on a chart?
- chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True
- chart.values = True
- chart.labels = True
* Correct answer: chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True
DataLabelList controls labels: showVal shows the values themselves.

How do you change a series color on a chart?
- chart.series[0].graphicalProperties.solidFill = "4472C4"
- chart.series[0].color = "4472C4"
- chart.fill = "4472C4"
* Correct answer: chart.series[0].graphicalProperties.solidFill = "4472C4"
The series fill color is set via graphicalProperties.solidFill.

How do you hide the sheet gridlines?
- ws.sheet_view.showGridLines = False
- ws.hide_grid()
- ws.gridlines = False
* Correct answer: ws.sheet_view.showGridLines = False
The showGridLines property in sheet_view controls gridline display.

What does ws.print_area = "A1:F15" do?
- Limits printing to the range A1:F15
- Prints all sheets
- Saves only the selection
* Correct answer: Limits printing to the range A1:F15
print_area sets the sheet area that will be printed.

Where are a sheet's charts stored for checking in tests?
- In the ws._charts list
- In ws.diagrams
- They cannot be read back
* Correct answer: In the ws._charts list
This is a semi-official but working attribute; len(ws._charts) gives the number of charts.
<!--/QUIZ-->
