---
title: Финальный проект: генератор отчётов
summary: Собираем полный конвейер: данные → Excel, Word и PDF, с юнит- и интеграционными тестами.
order: 8
duration: 60 мин
difficulty: advanced
tags: проект, генератор, интеграция, pytest, отчёты
---

Финальный проект объединяет всё, что мы изучили: одни и те же данные должны превратиться в Excel-книгу, Word-документ и PDF-отчёт. Ключ к успеху — модульность: раздели программу на части, каждую из которых можно тестировать отдельно.

## Архитектура пакета

Соберём пакет `reports` с таким составом:

```
reports/
├── __init__.py
├── core.py          # модель данных
├── excel_report.py  # генерация xlsx
├── word_report.py   # генерация docx
├── pdf_report.py    # генерация pdf
└── generate_all.py  # единая точка входа
```

Каждый модуль экспортирует функцию вида `build_x(sales, path) -> Path`, которая создаёт файл и возвращает путь. Тогда тест просто вызывает функцию и проверяет артефакт.

## Модель данных

Для продаж используем `dataclass`:

```python
from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return self.price * self.qty
```

`dataclass` сам генерирует `__init__`, `__repr__` и сравнение — удобно и для кода, и для тестов.

## Модуль Excel

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def build_excel(sales, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Продажи"
    ws.append(["Товар", "Цена", "Количество", "Стоимость"])
    for s in sales:
        ws.append([s.product, s.price, s.qty, s.total])
    ws["A1"].font = Font(bold=True)
    ws["A1"].fill = PatternFill(fill_type="solid", fgColor="4472C4")
    wb.save(path)
    return path
```

## Модуль Word

```python
from docx import Document

def build_word(sales, path):
    doc = Document()
    doc.add_heading("Отчёт о продажах", level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    for col, name in enumerate(["Товар", "Цена", "Количество", "Стоимость"]):
        table.cell(0, col).text = name
    for s in sales:
        row = table.add_row()
        row.cells[0].text = s.product
        row.cells[1].text = str(s.price)
        row.cells[2].text = str(s.qty)
        row.cells[3].text = str(s.total)
    doc.save(path)
    return path
```

## Модуль PDF

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(sales, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    data = [["Товар", "Цена", "Количество", "Стоимость"]]
    for s in sales:
        data.append([s.product, s.price, s.qty, s.total])
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    doc.build([Paragraph("Отчёт о продажах", styles["Title"]), table])
    return path
```

## Единая точка входа

```python
from pathlib import Path
from reports.excel_report import build_excel
from reports.word_report import build_word
from reports.pdf_report import build_pdf

def generate_all(sales, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    paths = {
        "xlsx": build_excel(sales, out_dir / "report.xlsx"),
        "docx": build_word(sales, out_dir / "report.docx"),
        "pdf": build_pdf(sales, out_dir / "report.pdf"),
    }
    return paths
```

`out_dir.mkdir(exist_ok=True)` гарантирует, что папка существует. Повторный запуск перезаписывает файлы — это нормально (идемпотентность).

## Интеграционный тест

```python
def test_generate_all(tmp_path):
    sales = [Sale("Ноутбук", 79990, 3), Sale("Мышь", 1290, 15)]
    paths = generate_all(sales, tmp_path)
    assert paths["xlsx"].exists()
    assert paths["docx"].exists()
    assert paths["pdf"].exists()
    # дальше — проверка содержимого каждого формата
```

Такой тест проверяет связку модулей: если один из генераторов сломается, падёт весь конвейер.

<!--TASK-->
### Задача 1
Создай пакет `reports` с модулем `core.py`: `dataclass Sale` (product, price, qty) и свойством `total`. Напиши pytest-тест: создай экземпляр `Sale("Ноутбук", 79990, 3)`, проверь, что `s.total == 239970.0`, а поля `product`/`qty` доступны. Запусти `python -m pytest -q`.
### Задача 2
Реализуй `excel_report.py` с функцией `build_excel(sales, path)` по образцу из теории. Напиши pytest-тест: сгенерируй книгу во временной папке, загрузи её и проверь: имя листа «Продажи», три строки данных плюс шапка, `ws["D2"].value == 239970.0` (стоимость первой позиции) и `ws["A1"].font.bold is True`.
### Задача 3
Реализуй `word_report.py` с функцией `build_word(sales, path)`. Напиши pytest-тест: загрузи docx и проверь: первый параграф — заголовок «Отчёт о продажах» уровня 1, таблица одна, в ней `1 + len(sales)` строк и 4 колонки, а `table.cell(1, 3).text == "239970.0"`.
### Задача 4
Реализуй `pdf_report.py` с функцией `build_pdf(sales, path)`. Напиши pytest-тест: открой PDF через `PdfReader` и проверь: есть хотя бы одна страница, а текст первой страницы содержит «Отчёт о продажах» и название первого товара.
### Задача 5
Реализуй `generate_all.py` и напиши интеграционный тест: сгенерируй все три файла в `tmp_path`, проверь, что все пути существуют, и затем проверь содержимое каждого формата (значение xlsx, текст docx, текст pdf). Запусти весь набор тестов командой `python -m pytest -q` и добейся, чтобы все тесты прошли.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`@dataclass` импортируется из `dataclasses`. Свойство — обычный метод с декоратором `@property`. Сравнивай `total` через `==` с float-литералом; для точности можно `round(s.total, 2)`.
### Подсказка 2
Стоимость первой позиции: `Sale("Ноутбук", 79990, 3).total == 239970.0`. В `build_excel` используй `ws.append([s.product, s.price, s.qty, s.total])`. Тест загружает файл через `load_workbook(path)` и проверяет `ws["D2"]`.
### Подсказка 3
В `build_word` после `doc.add_heading` создай таблицу через `doc.add_table(rows=1, cols=4)`, затем добвляй строки `table.add_row()`. Не забудь стиль `"Table Grid"`. Тест: `doc.paragraphs[0].style.name == "Heading 1"` и `len(table.rows) == 1 + len(sales)`.
### Подсказка 4
В `build_pdf` собери данные для таблицы из `sales`: первая строка — шапка. Тест: `PdfReader(str(path))`, затем `text = reader.pages[0].extract_text()` и `assert "Отчёт о продажах" in text`.
### Подсказка 5
`generate_all` возвращает словарь путей. Интеграционный тест вызывает её один раз и проверяет три файла. Для проверки docx используй `Document(path)`, для pdf — `PdfReader`, для xlsx — `load_workbook`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
`core.py`:

```python
from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    price: float
    qty: int

    @property
    def total(self) -> float:
        return self.price * self.qty
```

Тест:

```python
from reports.core import Sale

def test_sale_total():
    s = Sale("Ноутбук", 79990, 3)
    assert s.total == 239970.0
    assert s.product == "Ноутбук"
    assert s.qty == 3
```

Что здесь происходит? `dataclass` сокращает boilerplate: конструктор, repr и сравнение генерируются автоматически. Свойство `total` вычисляется на лету. Тест проверяет и вычисление, и доступ к полям — фундамент, на котором стоят все генераторы.
### Разбор 2
`excel_report.py` (фрагмент):

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def build_excel(sales, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Продажи"
    ws.append(["Товар", "Цена", "Количество", "Стоимость"])
    for s in sales:
        ws.append([s.product, s.price, s.qty, s.total])
    ws["A1"].font = Font(bold=True)
    ws["A1"].fill = PatternFill(fill_type="solid", fgColor="4472C4")
    wb.save(path)
    return path
```

Тест:

```python
from openpyxl import load_workbook
from reports.core import Sale
from reports.excel_report import build_excel

def test_build_excel(tmp_path):
    sales = [Sale("Ноутбук", 79990, 3), Sale("Мышь", 1290, 15)]
    path = build_excel(sales, tmp_path / "report.xlsx")

    wb = load_workbook(path)
    ws = wb.active
    assert ws.title == "Продажи"
    assert ws.max_row == 3          # шапка + 2 товара
    assert ws["D2"].value == 239970.0
    assert ws["A1"].font.bold is True
```

Что здесь происходит? Генератор независим от источника данных: принимает список `Sale` и путь. Тест проверяет артефакт: число строк (3 = 1 + 2), стоимость первой позиции (79990 × 3) и стиль шапки. Модуль можно использовать и в конвейере, и отдельно.
### Разбор 3
`word_report.py`:

```python
from docx import Document

def build_word(sales, path):
    doc = Document()
    doc.add_heading("Отчёт о продажах", level=1)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    for col, name in enumerate(["Товар", "Цена", "Количество", "Стоимость"]):
        table.cell(0, col).text = name
    for s in sales:
        row = table.add_row()
        row.cells[0].text = s.product
        row.cells[1].text = str(s.price)
        row.cells[2].text = str(s.qty)
        row.cells[3].text = str(s.total)
    doc.save(path)
    return path
```

Тест:

```python
from docx import Document
from reports.word_report import build_word

def test_build_word(tmp_path):
    sales = [Sale("Ноутбук", 79990, 3)]
    path = build_word(sales, tmp_path / "report.docx")

    doc = Document(path)
    assert doc.paragraphs[0].text == "Отчёт о продажах"
    assert doc.paragraphs[0].style.name == "Heading 1"
    table = doc.tables[0]
    assert len(table.rows) == 2                  # шапка + 1 товар
    assert len(table.columns) == 4
    assert table.cell(1, 3).text == "239970.0"
```

Что здесь происходит? Таблица строится динамически: одна строка шапки плюс строка на каждый товар. Тест проверяет и структуру (число строк/колонок), и данные (ячейка стоимости). `str(s.total)` превращает число в текст для Word.
### Разбор 4
`pdf_report.py`:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf(sales, path):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    styles = getSampleStyleSheet()
    data = [["Товар", "Цена", "Количество", "Стоимость"]]
    for s in sales:
        data.append([s.product, s.price, s.qty, s.total])
    table = Table(data)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]))
    doc.build([Paragraph("Отчёт о продажах", styles["Title"]), table])
    return path
```

Тест:

```python
from pypdf import PdfReader
from reports.pdf_report import build_pdf

def test_build_pdf(tmp_path):
    sales = [Sale("Ноутбук", 79990, 3)]
    path = build_pdf(sales, tmp_path / "report.pdf")

    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    text = reader.pages[0].extract_text()
    assert "Отчёт о продажах" in text
    assert "Ноутбук" in text
```

Что здесь происходит? Данные превращаются в таблицу PDF. Тест проверяет, что текст извлекается и содержит и заголовок, и название товара. Если бы генерация молча падала или создавала пустой файл — тест бы это поймал.
### Разбор 5
`generate_all.py`:

```python
from pathlib import Path
from reports.excel_report import build_excel
from reports.word_report import build_word
from reports.pdf_report import build_pdf

def generate_all(sales, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    return {
        "xlsx": build_excel(sales, out_dir / "report.xlsx"),
        "docx": build_word(sales, out_dir / "report.docx"),
        "pdf": build_pdf(sales, out_dir / "report.pdf"),
    }
```

Интеграционный тест:

```python
from docx import Document
from openpyxl import load_workbook
from pypdf import PdfReader
from reports.core import Sale
from reports.generate_all import generate_all

def test_generate_all(tmp_path):
    sales = [Sale("Ноутбук", 79990, 3), Sale("Мышь", 1290, 15)]
    paths = generate_all(sales, tmp_path)

    assert paths["xlsx"].exists()
    assert paths["docx"].exists()
    assert paths["pdf"].exists()

    wb = load_workbook(paths["xlsx"])
    assert wb.active["D2"].value == 239970.0

    doc = Document(paths["docx"])
    assert doc.tables[0].cell(2, 3).text == "19350.0"   # 1290 × 15

    reader = PdfReader(str(paths["pdf"]))
    assert "Отчёт о продажах" in reader.pages[0].extract_text()
```

Что здесь происходит? Интеграционный тест запускает весь конвейер и проверяет каждый артефакт. Это «дымовой тест» проекта: если сборка работает, можно смело расширять функциональность. Такой подход — стандарт для генераторов отчётов в продакшене.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое dataclass в Python?
- Класс с автоматически генерируемым __init__, __repr__ и сравнением
- Класс для работы с датами
- Специальный контейнер данных Excel
* Правильный ответ: Класс с автоматически генерируемым __init__, __repr__ и сравнением
@dataclass убирает шаблонный код объявления полей.

Зачем функции-генератору принимать путь наружу?
- Чтобы её можно было тестировать и переиспользовать
- Чтобы ускорить работу
- Это требование openpyxl
* Правильный ответ: Чтобы её можно было тестировать и переиспользовать
Путь как параметр позволяет тестам использовать tmp_path, а не засорять диск.

Что делает out_dir.mkdir(exist_ok=True)?
- Создаёт папку, если её ещё нет
- Удаляет папку
- Проверяет наличие файла
* Правильный ответ: Создаёт папку, если её ещё нет
exist_ok=True не даёт упасть, если папка уже существует.

Что означает идемпотентность генерации?
- Повторный запуск даёт тот же корректный результат
- Файлы нельзя перезаписывать
- Каждый запуск создаёт уникальные файлы
* Правильный ответ: Повторный запуск даёт тот же корректный результат
Повторный прогон перезаписывает файлы тем же содержимым — это нормально.

Чем интеграционный тест отличается от юнит-теста?
- Интеграционный проверяет связку модулей, юнит — один модуль
- Интеграционный быстрее
- Они ничем не отличаются
* Правильный ответ: Интеграционный проверяет связку модулей, юнит — один модуль
Юнит изолирован, интеграция проверяет совместную работу частей.

Что вернёт build_excel(sales, path)?
- Путь к созданному файлу
- Объект Workbook
- Список sales
* Правильный ответ: Путь к созданному файлу
Все генераторы возвращают путь — единый контракт для конвейера.

Как проверить заголовок уровня 1 в docx?
- doc.paragraphs[0].style.name == "Heading 1"
- doc.title == "Отчёт"
- doc.heading == 1
* Правильный ответ: doc.paragraphs[0].style.name == "Heading 1"
Свойство style.name отдаёт имя стиля параграфа.

Как узнать число строк таблицы в docx?
- len(table.rows)
- table.row_count()
- table.size
* Правильный ответ: len(table.rows)
table.rows — коллекция строк; len(...) даёт их количество.

Чем полезна проверка содержимого всех трёх артефактов?
- Она подтверждает, что конвейер работает целиком
- Она ускоряет генерацию
- Она обязательна для openpyxl
* Правильный ответ: Она подтверждает, что конвейер работает целиком
Полная проверка всех форматов — гарантия целостности отчёта.

Как запустить все тесты проекта?
- python -m pytest -q
- python run_tests.py
- pytest --all
* Правильный ответ: python -m pytest -q
Команда собирает все тесты пакета; -q сокращает вывод.
<!--/QUIZ-->
