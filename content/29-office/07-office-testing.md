---
title: Тестирование офисной автоматизации
summary: pytest для xlsx/docx/pdf: фикстуры, tmp_path, параметризация, проверка содержимого артефактов.
order: 7
duration: 50 мин
difficulty: advanced
tags: pytest, тесты, tmp_path, артефакты, conftest
---

Когда код создаёт файлы — xlsx, docx, pdf — обычной «print-проверки» мало. Нужны автоматические тесты, которые генерируют артефакты в чистую временную папку и проверяют их содержимое. Этот урок — про pytest и офисные файлы.

## Почему не сравнивать файлы побайтово

`.xlsx` и `.docx` — это zip-архивы с XML внутри. В них хранятся идентификаторы, метки времени и прочие метаданные, которые меняются от запуска к запуску. Поэтому сравнивать файлы побайтово нельзя — тесты будут падать без причины. Вместо этого сравнивают смысл: значения ячеек, тексты параграфов, число страниц.

## tmp_path: временная папка

Встроенная фикстура `tmp_path` даёт каждому тесту уникальную временную папку, которая автоматически очищается после теста:

```python
def test_write_xlsx(tmp_path):
    path = tmp_path / "out.xlsx"
    wb = Workbook()
    wb.active["A1"] = 42
    wb.save(path)
    assert path.exists()
```

Никакого мусора в рабочей директории — тесты повторяемы и изолированы.

## Фикстуры

Фикстура — функция, подготовливающая данные или файлы. Она может использовать другие фикстуры — pytest сам разрешает зависимости:

```python
import pytest
from openpyxl import Workbook

@pytest.fixture
def sample_xlsx(tmp_path):
    path = tmp_path / "sample.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Город", "Население"])
    ws.append(["Москва", 13_000_000])
    ws.append(["Санкт-Петербург", 5_600_000])
    wb.save(path)
    return path
```

Общие фикстуры кладут в `conftest.py` — тогда они видны всем тестам пакета.

## Параметризация

`@pytest.mark.parametrize` запускает один тест с разными наборами данных:

```python
@pytest.mark.parametrize("expected", [("Москва",), ("Санкт-Петербург",)])
def test_contains_city(sample_xlsx, expected):
    ...
```

## Проверка xlsx

После генерации загружаем книгу обратно и проверяем значения и стили:

```python
from openpyxl import load_workbook

def test_xlsx_content(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    ws = wb.active
    assert ws["A1"].value == "Город"
    assert ws["B2"].value == 13_000_000
    assert ws["A1"].font.bold is True
    assert len(ws._charts) == 0
```

## Проверка docx и pdf

Аналогично для Word и PDF — открываем и читаем содержимое:

```python
from docx import Document
from pypdf import PdfReader

def test_docx(path):
    doc = Document(path)
    assert doc.paragraphs[0].text == "Отчёт"
    assert len(doc.tables) == 1

def test_pdf(path):
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    assert "Отчёт" in reader.pages[0].extract_text()
```

## Отрицательные тесты

Функция должна корректно реагировать на ошибки — например, на отсутствие файла:

```python
import pytest

def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_workbook("nonexistent.xlsx")
```

## Золотые файлы

Для текстовых отчётов удобен паттерн «золотой файл»: эталонный результат заранее сохраняется в репозитории, а тест сравнивает с ним вывод функции. Это удобно для текстов документов, но не для бинарников xlsx/docx — там сравнивай значения.

## Полный пример

Соберём тест-набор для модуля, который создаёт отчёт:

```python
import pytest
from openpyxl import Workbook, load_workbook

@pytest.fixture
def out_dir(tmp_path):
    return tmp_path

def build_report(path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Показатель", "Значение"])
    ws.append(["Выручка", 1_200_000])
    wb.save(path)
    return path

def test_report_file_exists(out_dir):
    path = build_report(out_dir / "report.xlsx")
    assert path.exists()

def test_report_values(out_dir):
    path = build_report(out_dir / "report.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws["A2"].value == "Выручка"
    assert ws["B2"].value == 1_200_000
```

Запуск: `python -m pytest tests/ -q`.

<!--TASK-->
### Задача 1
Напиши pytest-тест с фикстурой. Создай модуль `test_fixtures.py`, где фикстура `sample_xlsx(tmp_path)` создаёт книгу с листом «Данные» и тремя строками (шапка + две строки данных). Напиши два теста: первый проверяет, что файл существует и в нём один лист; второй — что `ws["B2"].value` равно ожидаемому числу. Запусти `python -m pytest test_fixtures.py -q`.
### Задача 2
Напиши параметризованный тест. Функция `city_population(path, city)` возвращает население города из листа «Город, Население». С помощью `@pytest.mark.parametrize` проверь её на трёх городах (включая тот, которого нет в данных — пусть вернёт None). Данные для книги создавай в фикстуре.
### Задача 3
Напиши pytest-тест, который проверяет xlsx-артефакт целиком: значения, стиль шапки (жирный шрифт), ширину колонки и отсутствие диаграмм. Функция `build_sales(path)` создаёт лист «Продажи» с шапкой и двумя строками, стилизует шапку. Тест загружает файл и проверяет все четыре пункта.
### Задача 4
Напиши pytest-тест для docx-артефакта. Функция `build_doc(path)` создаёт документ с заголовком «Отчёт» и таблицей 2×2. Тест: загружает docx, проверяет, что первый параграф — заголовок уровня 1 (там `p.style.name == "Heading 1"`), таблица одна, а `table.cell(1, 1).text` содержит ожидаемое значение.
### Задача 5
Напиши pytest-тест для pdf-артефакта и отрицательный тест. Функция `build_pdf(path)` создаёт PDF с текстом «Квартальный отчёт». Тест 1: проверяет, что у PDF есть страница и текст извлекается. Тест 2: функция `load_any(path)` (просто `load_workbook(path)`) при передаче несуществующего пути поднимает `FileNotFoundError` — проверь через `pytest.raises`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Фикстура: `@pytest.fixture def sample_xlsx(tmp_path): ... return path`. Обрати внимание: имя фикстуры передаётся как аргумент теста. `tmp_path` — тоже фикстура, её можно использовать внутри другой фикстуры.
### Подсказка 2
Параметризация: `@pytest.mark.parametrize("city, expected", [("Москва", 13_000_000), ("Казань", None)])`. В теле теста вызывай `city_population(sample_xlsx, city)` и сравнивай с expected.
### Подсказка 3
Жирность шрифта: `ws["A1"].font.bold is True`. Ширина: `ws.column_dimensions["A"].width`. Диаграммы: `len(ws._charts) == 0`. Значения — обычные ассерты на ячейки.
### Подсказка 4
Заголовок уровня 1: `doc.paragraphs[0].style.name == "Heading 1"`. Проверяй `len(doc.tables) == 1` и текст ячейки. Если в документе есть пустой первый параграф — учти это: начальный `Document()` содержит один пустой абзац, лучше добавляй заголовок первым и проверяй `paragraphs[0]`.
### Подсказка 5
Для PDF используй `PdfReader` и `extract_text()`. Для отрицательного теста: `with pytest.raises(FileNotFoundError): load_workbook(tmp_path / "no.xlsx")`. Путь к несуществующему файлу тоже строй через `tmp_path`, чтобы не трогать диск.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `test_fixtures.py`:

```python
import pytest
from openpyxl import Workbook, load_workbook

@pytest.fixture
def sample_xlsx(tmp_path):
    path = tmp_path / "sample.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Данные"
    ws.append(["Город", "Население"])
    ws.append(["Москва", 13_000_000])
    ws.append(["Санкт-Петербург", 5_600_000])
    wb.save(path)
    return path

def test_file_exists_and_one_sheet(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    assert len(wb.sheetnames) == 1
    assert wb.sheetnames[0] == "Данные"

def test_sheet_value(sample_xlsx):
    wb = load_workbook(sample_xlsx)
    ws = wb.active
    assert ws["B2"].value == 13_000_000
```

Что здесь происходит? Фикстура `sample_xlsx` принимает `tmp_path` и возвращает путь к готовому файлу. Каждый тест получает свежую книгу — данные изолированы. `load_workbook` открывает артефакт, и мы проверяем и имя листа, и значение. Это фундамент всех дальнейших проверок.
### Разбор 2
Модуль проверки и тест:

```python
from openpyxl import load_workbook

def city_population(path, city):
    wb = load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == city:
            return row[1]
    return None
```

```python
import pytest
from city_utils import city_population

@pytest.mark.parametrize("city, expected", [
    ("Москва", 13_000_000),
    ("Санкт-Петербург", 5_600_000),
    ("Казань", None),
])
def test_city_population(sample_xlsx, city, expected):
    assert city_population(sample_xlsx, city) == expected
```

Что здесь происходит? Один тест выполняется трижды — с разными городами. Это пример параметризации: данные приходят из декоратора, а `sample_xlsx` подставляется фикстурой. Случай «города нет» — важный краевой случай, он проверяет возврат `None`.
### Разбор 3
Функция:

```python
from openpyxl import Workbook
from openpyxl.styles import Font

def build_sales(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Продажи"
    ws.append(["Месяц", "Сумма"])
    ws.append(["Январь", 120])
    ws.append(["Февраль", 150])
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 15
    wb.save(path)
    return path
```

Тест:

```python
def test_build_sales(tmp_path):
    path = build_sales(tmp_path / "sales.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws["A1"].value == "Месяц"
    assert ws["B3"].value == 150
    assert ws["A1"].font.bold is True
    assert ws.column_dimensions["A"].width == 15
    assert len(ws._charts) == 0
```

Что здесь происходит? Мы проверяем артефакт с четырёх сторон: содержимое ячеек, стиль, ширину колонки и отсутствие диаграмм. Это комплексный «снимок» файла: если любая часть генерации сломается, тест упадёт.
### Разбор 4
Функция:

```python
from docx import Document

def build_doc(path):
    doc = Document()
    doc.add_heading("Отчёт", level=1)
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Показатель"
    table.cell(0, 1).text = "Значение"
    table.cell(1, 0).text = "Выручка"
    table.cell(1, 1).text = "1 200 000"
    doc.save(path)
    return path
```

Тест:

```python
def test_build_doc(tmp_path):
    path = build_doc(tmp_path / "report.docx")
    doc = Document(path)
    assert doc.paragraphs[0].text == "Отчёт"
    assert doc.paragraphs[0].style.name == "Heading 1"
    assert len(doc.tables) == 1
    table = doc.tables[0]
    assert table.cell(1, 1).text == "1 200 000"
```

Что здесь происходит? `doc.paragraphs[0]` — первый параграф, заголовок уровня 1. Проверка `style.name` подтверждает, что это именно заголовок, а не обычный текст. Таблица проверяется и по количеству, и по содержимому ячейки.
### Разбор 5
Функции и тесты:

```python
def build_pdf(path):
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    doc = SimpleDocTemplate(str(path))
    doc.build([Paragraph("Квартальный отчёт", getSampleStyleSheet()["Title"])])
    return path
```

```python
import pytest
from openpyxl import load_workbook
from pypdf import PdfReader
from pdf_gen import build_pdf

def test_build_pdf(tmp_path):
    path = build_pdf(tmp_path / "report.pdf")
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    assert "Квартальный отчёт" in reader.pages[0].extract_text()

def test_load_any_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_workbook(tmp_path / "no.xlsx")
```

Что здесь происходит? Первый тест проверяет, что PDF реально содержит текст — извлечение через pypdf. Второй — отрицательный: передача несуществующего пути должна привести к `FileNotFoundError`, и `pytest.raises` это фиксирует. Такие тесты защищают код от тихих падений в проде.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое tmp_path в pytest?
- Встроенная фикстура, дающая временную папку для теста
- Путь до рабочей директории
- Пакет для работы с файлами
* Правильный ответ: Встроенная фикстура, дающая временную папку для теста
Каждый тест получает уникальную папку, которая очищается после завершения.

Почему нельзя сравнивать xlsx-файлы побайтово?
- Внутри метаданные и идентификаторы, меняющиеся от запуска к запуску
- Файлы слишком большие
- Формат не поддерживается Python
* Правильный ответ: Внутри метаданные и идентификаторы, меняющиеся от запуска к запуску
Поэтому сравнивают смысл: значения ячеек, тексты, число страниц.

Где хранят общие фикстуры?
- В conftest.py
- В любом файле теста
- В pytest.ini
* Правильный ответ: В conftest.py
conftest.py делает фикстуры видимыми всем тестам пакета.

Как запустить один тест с разными наборами данных?
- @pytest.mark.parametrize(...)
- @pytest.mark.data(...)
- @pytest.test_cases(...)
* Правильный ответ: @pytest.mark.parametrize(...)
Декоратор parametrize передаёт в тест разные аргументы по очереди.

Как проверить, что функция подняла исключение?
- with pytest.raises(...)
- try/except в тесте
- assert raises(...)
* Правильный ответ: with pytest.raises(...)
Контекстный менеджер pytest.raises ловит ожидаемое исключение.

Как проверить текст внутри PDF?
- reader.pages[i].extract_text()
- pdf.text()
- reader.contents
* Правильный ответ: reader.pages[i].extract_text()
PdfReader извлекает текст страницы методом extract_text().

Как проверить, что текст в ячейке жирный?
- ws["A1"].font.bold is True
- ws["A1"].bold
- cell.bold == True
* Правильный ответ: ws["A1"].font.bold is True
Свойство font — объект Font, у него есть флаг bold.

Что проверяет len(ws._charts) == 1?
- Что на листе ровно одна диаграмма
- Что есть одна ячейка
- Что файл сохранён
* Правильный ответ: Что на листе ровно одна диаграмма
_charts — список диаграмм листа.

Зачем фикстуре принимать tmp_path?
- Чтобы писать файлы только во временную папку
- Чтобы ускорить тесты
- Это обязательно для всех фикстур
* Правильный ответ: Чтобы писать файлы только во временную папку
Так тесты не трогают рабочие файлы проекта и изолированы друг от друга.

Какой командой запускается pytest?
- python -m pytest
- python test.py
- pytest run
* Правильный ответ: python -m pytest
Стабильный способ запуска: python -m pytest <путь> -q.
<!--/QUIZ-->
