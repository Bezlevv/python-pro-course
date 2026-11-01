---
title: Интеграция: конвертация и PDF-отчёты
summary: Генерация PDF через reportlab, конвертация xlsx в PDF, извлечение текста из PDF для проверок.
order: 6
duration: 50 мин
difficulty: advanced
tags: reportlab, pdf, конвертация, отчёты, pypdf
---

PDF — конечный формат для отчётов: он одинаково выглядит на любом устройстве. Библиотека `reportlab` — стандарт генерации PDF на Python. Установка: `pip install reportlab`.

## Platypus: история из «флоуаблов»

Высокоуровневый каркас reportlab называется Platypus. Ты собираешь «историю» (story) из плавающих элементов — флоуаблов (flowables): `Paragraph`, `Spacer`, `Table`, `Image`, `PageBreak` — и передаёшь её в документ:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

doc = SimpleDocTemplate("report.pdf", pagesize=A4, title="Отчёт")
styles = getSampleStyleSheet()

story = [
    Paragraph("Годовой отчёт", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Выручка компании выросла на 15%.", styles["BodyText"]),
]

data = [["Показатель", "Значение"], ["Выручка", "1 200 000"], ["Расходы", "980 000"]]
table = Table(data)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(table)

doc.build(story)
print("Готово: report.pdf")
```

`SimpleDocTemplate` описывает документ (путь, размер страницы, поля). `doc.build(story)` собирает PDF. Таблица стилизуется через `TableStyle`: координаты указываются как `(колонка, строка, колонка, строка)`, где `-1` — последняя.

## Стили параграфов

Базовые стили даёт `getSampleStyleSheet()`: `"Title"`, `"Heading1"`, `"BodyText"`. Чтобы создать свой стиль, используй `ParagraphStyle`:

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

`leading` — межстрочный интервал, `fontSize` — размер шрифта.

## Изображения

`Image` вставляет картинку; можно задать размеры:

```python
from reportlab.platypus import Image

story.append(Image("logo.png", width=3 * cm, height=1.5 * cm))
```

## Номера страниц

Номера страниц добавляются через колбэк на отрисовку страницы:

```python
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 1 * cm, f"Стр. {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("report.pdf", pagesize=A4, onLaterPages=footer, onFirstPage=footer)
```

`doc.page` — номер текущей страницы.

## Конвертация xlsx → PDF

Прямой конвертации openpyxl → PDF нет. Два рабочих пути: (1) прочитать данные через openpyxl и собрать отчёт в reportlab — мы так и делаем; (2) отправить `.xlsx` в LibreOffice: `soffice --headless --convert-to pdf file.xlsx` — внешний инструмент, вызываемый через `subprocess.run`.

## Проверка PDF

Чтобы тестировать PDF, нужен инструмент извлечения текста. `pypdf` (ставь `pip install pypdf`) читает страницы и текст:

```python
from pypdf import PdfReader

reader = PdfReader("report.pdf")
print(len(reader.pages))            # число страниц
print(reader.pages[0].extract_text())  # текст первой страницы
```

Важно: PDF не обязан содержать текстовый слой (например, при сканах). Но для отчётов, которые мы генерируем сами, извлечение работает — и это основа тестов.

<!--TASK-->
### Задача 1
Создай файл `income.pdf` с помощью reportlab: заголовок «Отчёт о доходах» (стиль Title), абзац-описание, таблица 3×2 (шапка «Показатель, Сумма» и две строки данных) с рамками и синей шапкой. Добавь номер страницы снизу по центру. Сохрани PDF, затем открой его через `PdfReader` и выведи на экран количество страниц и текст первой страницы.
### Задача 2
Напиши pytest-тест для PDF-артефакта. Функция `build_pdf(data, path)` создаёт PDF с заголовком, таблицей из `data` и сохраняет по пути. Тест: передай данные с ключевыми словами (например, «Выручка»), затем открой файл через `PdfReader` и проверь: существует хотя бы одна страница, а текст первой страницы содержит слово «Выручка».
### Задача 3
Напиши pytest-тест для структуры документа. Функция `build_story(data)` возвращает список флоуаблов (историю): `Paragraph` заголовка и `Table` из данных. Тест: убедись, что в списке есть хотя бы один `Table` и хотя бы один `Paragraph`, а данные таблицы содержат шапку.
### Задача 4
Напиши pytest-тест для конвертации xlsx → PDF. Функция `xlsx_to_pdf(xlsx_path, pdf_path)` читает весь лист первой книги через openpyxl (все строки, включая шапку) и строит PDF с таблицей из этих данных. Тест: создай xlsx во временной папке (шапка и две строки), вызови функцию, затем `PdfReader` и проверь, что текст содержит значения из xlsx (например, первое значение шапки).
### Задача 5
Напиши pytest-тест для многостраничного PDF. Функция `build_multipage_pdf(rows, path)` создаёт PDF, где каждая строка из `rows` оформлена как абзац, и после каждых трёх абзацев вставлен `PageBreak`. Тест: передай 7 строк, проверь, что `len(reader.pages) >= 2`, и что текст последней страницы содержит последнюю строку данных.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Импорты: `from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle`, `from reportlab.lib.styles import getSampleStyleSheet`, `from reportlab.lib import colors`. Номер страницы: функция `footer(canvas, doc)` и параметры `onFirstPage`/`onLaterPages` в `SimpleDocTemplate`.
### Подсказка 2
Функция `build_pdf` возвращает путь. В тесте: `reader = PdfReader(path)`, затем `text = reader.pages[0].extract_text()` и `assert "Выручка" in text`. Помни: если текст не извлёкся — проверь, что ты используешь `Paragraph` для текста, а не просто рисуешь на canvas.
### Подсказка 3
`build_story` должна вернуть список — проверяй через `any(isinstance(x, Table) for x in story)`. Данные таблицы: `table._cellvalues` — неформальное, но рабочее поле; проще проверить, что story содержит Table, а отдельная проверка значений — через сгенерированный PDF (Задача 2).
### Подсказка 4
Читай xlsx через `load_workbook(xlsx_path, data_only=True)` и `ws.iter_rows(values_only=True)` — получишь список кортежей. Передай его в `Table(list_of_rows)`. В тесте создай xlsx через `Workbook()` и `ws.append(...)`, сохрани в `tmp_path`.
### Подсказка 5
`PageBreak` — ещё один флоуабл: добавляй его в story после каждого третьего абзаца. Число страниц: `len(reader.pages)`. Последняя страница: `reader.pages[-1].extract_text()`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(A4[0] / 2, 1 * cm, f"Стр. {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("income.pdf", pagesize=A4, onFirstPage=footer, onLaterPages=footer)
styles = getSampleStyleSheet()

story = [
    Paragraph("Отчёт о доходах", styles["Title"]),
    Spacer(1, 12),
    Paragraph("Помесячные данные за 2026 год.", styles["BodyText"]),
]
data = [["Показатель", "Сумма"], ["Выручка", "1 200 000"], ["Расходы", "980 000"]]
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
print("Страниц:", len(reader.pages))
print(reader.pages[0].extract_text())
```

Что здесь происходит? `SimpleDocTemplate` получает колбэки `onFirstPage` и `onLaterPages` — функция `footer` рисует номер страницы внизу. История собирается из заголовка, отступа, абзаца и таблицы с рамками. После сборки `PdfReader` извлекает текст — так мы видим, что именно попало в PDF.
### Разбор 2
Функция:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(data, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    story = [Paragraph("Отчёт", styles["Title"])]
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

Тест:

```python
from pypdf import PdfReader
from pdf_reports import build_pdf

def test_build_pdf(tmp_path):
    data = [["Показатель", "Значение"], ["Выручка", "1 200 000"]]
    path = build_pdf(data, tmp_path / "report.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    text = reader.pages[0].extract_text()
    assert "Выручка" in text
```

Что здесь происходит? Функция генерирует PDF из таблицы. Тест проверяет артефакт «снаружи»: есть страница, а текст извлёкся и содержит ключевое слово. Такой тест ловит и отсутствие файла, и пустые страницы, и поломанную сборку.
### Разбор 3
Функция:

```python
def build_story(data):
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Отчёт", styles["Title"]),
        Table(data),
    ]
    return story
```

Тест:

```python
from reportlab.platypus import Table, Paragraph
from pdf_reports import build_story

def test_build_story():
    story = build_story([["A", "B"], [1, 2]])
    assert any(isinstance(x, Table) for x in story)
    assert any(isinstance(x, Paragraph) for x in story)
    assert any(isinstance(x, Table) for x in story)
```

Что здесь происходит? Мы проверяем логику сборки истории до генерации PDF: в ней есть и `Paragraph`, и `Table`. Это быстрый юнит-тест — он не создаёт файлы, а проверяет структуру документа. Удобно комбинировать с тестом из Разбора 2: быстрый юнит + медленный интеграционный.
### Разбор 4
Функция:

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

Тест:

```python
from openpyxl import Workbook
from pypdf import PdfReader
from pdf_reports import xlsx_to_pdf

def test_xlsx_to_pdf(tmp_path):
    xlsx = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Город", "Население"])
    ws.append(["Москва", 13_000_000])
    wb.save(xlsx)

    pdf = xlsx_to_pdf(xlsx, tmp_path / "out.pdf")
    reader = PdfReader(str(pdf))
    text = reader.pages[0].extract_text()
    assert "Город" in text
    assert "Москва" in text
```

Что здесь происходит? Мы читаем xlsx и переносим его содержимое в таблицу PDF. Тест создаёт исходный xlsx, конвертирует и проверяет, что значения попали в PDF. Это «мостик» между двумя форматами — автоматизация, которая экономит часы ручной работы.
### Разбор 5
Функция:

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

Тест:

```python
def test_build_multipage_pdf(tmp_path):
    rows = [f"Строка {i}" for i in range(1, 8)]
    path = build_multipage_pdf(rows, tmp_path / "multi.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 2
    last_text = reader.pages[-1].extract_text()
    assert "Строка 7" in last_text
```

Что здесь происходит? После каждых трёх абзацев вставляется `PageBreak` — поэтому 7 строк дают минимум 3 страницы. Тест проверяет и количество страниц, и что последняя строка данных оказалась на последней странице. Это контроль многостраничных документов: ничего не потерялось и ничего не склеилось.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает SimpleDocTemplate?
- Описывает документ PDF: путь, размер страницы, поля
- Рисует таблицу
- Конвертирует docx в pdf
* Правильный ответ: Описывает документ PDF: путь, размер страницы, поля
SimpleDocTemplate — каркас документа, в который передаётся история флоуаблов.

Что такое «история» (story) в reportlab?
- Список флоуаблов: абзацев, таблиц, картинок
- Текстовый файл
- Папка с ресурсами
* Правильный ответ: Список флоуаблов: абзацев, таблиц, картинок
doc.build(story) собирает PDF из элементов списка.

Как добавить абзац в историю?
- Paragraph("текст", styles["BodyText"])
- add_paragraph("текст")
- Text("текст")
* Правильный ответ: Paragraph("текст", styles["BodyText"])
Paragraph — флоуабл; обязателен второй аргумент — стиль.

Как задать рамки таблицы в reportlab?
- TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.grey)])
- Table.border(1)
- Style.grid(True)
* Правильный ответ: TableStyle([("GRID", (0,0), (-1,-1), 0.5, colors.grey)])
Операция GRID рисует сетку; координаты — колонка/строка начала и конца.

Как добавить номер страницы в PDF?
- Через колбэк onFirstPage/onLaterPages с canvas.drawCentredString
- Через поле page в Table
- Номер страницы добавить нельзя
* Правильный ответ: Через колбэк onFirstPage/onLaterPages с canvas.drawCentredString
Функция-колбэк получает canvas, на котором рисуется текст номера.

Какая библиотека извлекает текст из PDF?
- pypdf (PdfReader)
- openpyxl
- python-docx
* Правильный ответ: pypdf (PdfReader)
PdfReader открывает PDF, reader.pages[i].extract_text() возвращает текст страницы.

Чем полезен data_only=True при конвертации xlsx в PDF?
- Возвращает вычисленные значения формул, если они сохранены
- Ускоряет работу PDF
- Отключает Excel
* Правильный ответ: Возвращает вычисленные значения формул, если они сохранены
Если файл пересчитывался в Excel, data_only вернёт значения вместо строк формул.

Что делает PageBreak?
- Начинает новую страницу в PDF
- Добавляет пустой абзац
- Закрывает документ
* Правильный ответ: Начинает новую страницу в PDF
PageBreak — флоуабл, разрывающий страницу в месте вставки.

Как задать свой стиль абзаца в reportlab?
- ParagraphStyle("Имя", parent=..., fontSize=..., leading=...)
- Style("Имя", size=12)
- Paragraph.set_style("Имя")
* Правильный ответ: ParagraphStyle("Имя", parent=..., fontSize=..., leading=...)
ParagraphStyle создаёт стиль; parent задаёт базовый стиль.

Какой метод завершает сборку PDF?
- doc.build(story)
- doc.save(story)
- story.build(doc)
* Правильный ответ: doc.build(story)
build принимает список флоуаблов и пишет готовый PDF на диск.
<!--/QUIZ-->
