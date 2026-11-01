---
title: openpyxl глубоко: книги, стили, формулы
summary: Создание книг Excel, работа с листами и ячейками, стилизация, формулы и сохранение файлов.
order: 1
duration: 45 мин
difficulty: intermediate
tags: openpyxl, excel, workbook, стили, формулы
---

openpyxl — это библиотека для чтения и записи файлов Excel (`.xlsx`) на чистом Python. Ей не нужен установленный Excel: создание книг, правка ячеек, стили и формулы выполняются самой библиотекой. Установка:

```bash
pip install openpyxl
```

## Книга и листы

Главный объект — `Workbook` (книга). `Workbook()` создаёт новую книгу с одним пустым листом.

```python
from openpyxl import Workbook

wb = Workbook()               # новая книга
ws = wb.active                # активный (по умолчанию первый) лист
ws.title = "Товары"           # переименование листа
ws2 = wb.create_sheet("Склад")  # новый лист в конце
ws3 = wb["Товары"]            # доступ по имени
```

Лист — это объект `Worksheet`. У книги может быть сколько угодно листов; доступ к ним — через `wb["Имя"]` или `wb.worksheets`.

## Ячейки

Обратиться к ячейке можно двумя способами: по имени (как в Excel) или по координатам.

```python
ws["A1"] = "привет"                    # запись по имени
ws.cell(row=1, column=2, value=42)     # запись по координатам

print(ws["A1"].value)                  # прочитать значение
print(ws.cell(row=1, column=2).value)  # 42
```

Для обхода диапазонов удобен `iter_rows` — он возвращает строку за строкой. Параметр `values_only=True` сразу превращает строки в кортежи значений:

```python
for row in ws.iter_rows(min_row=1, max_row=3, min_col=1, max_col=2, values_only=True):
    print(row)
```

Свойства `ws.max_row` и `ws.max_column` говорят, сколько строк и колонок занято данными. Сохраняется книга методом `wb.save("имя.xlsx")`.

## Формулы

openpyxl записывает формулу как строку, но **не вычисляет её** — расчёт происходит в Excel, когда файл открывают.

```python
ws["D2"] = "=B2*C2"   # ячейка D2 хранит формулу
```

При повторном чтении без флага `data_only` ты увидишь саму строку `=B2*C2`. Если открыть файл флагом `data_only=True`, openpyxl вернёт кэшированное значение формулы — но оно появляется только если файл раньше открывался и сохранялся в Excel. В противном случае будет `None`. Поэтому, когда данные нужны программе, часто проще посчитать самому: `ws["D2"] = ws["B2"].value * ws["C2"].value`.

## Стили

За оформление отвечают классы из `openpyxl.styles`: `Font` (шрифт), `PatternFill` (заливка), `Alignment` (выравнивание), `Border` и `Side` (рамки).

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

font = Font(bold=True, size=12, color="FFFFFF")          # белый жирный шрифт
fill = PatternFill(fill_type="solid", fgColor="4472C4")  # синяя заливка
al = Alignment(horizontal="center", vertical="center", wrap_text=True)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

cell = ws["A1"]
cell.font = font
cell.fill = fill
cell.alignment = al
cell.border = border
```

Числовой формат задаётся строкой: `cell.number_format = "#,##0.00"` — так числа покажутся с разделителями тысяч и двумя знаками после запятой.

## Организация листа

Часто нужны объединение ячеек, закрепление шапки и размеры колонок:

```python
ws.merge_cells("A1:C1")          # объединить три ячейки
ws.unmerge_cells("A1:C1")        # отменить объединение
ws.freeze_panes = "A2"           # закрепить строку 1 (область выше и левее A2)
ws.column_dimensions["A"].width = 30   # ширина колонки A
ws.row_dimensions[1].height = 24       # высота строки 1
```

## Полный пример

Соберём всё вместе: книга с шапкой, стилями, данными и формулой.

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Товары"

# стили шапки
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(fill_type="solid", fgColor="4472C4")
header_al = Alignment(horizontal="center", vertical="center")
thin = Side(style="thin", color="BFBFBF")
header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

headers = ["Название", "Цена", "Количество", "Стоимость"]
for col, name in enumerate(headers, start=1):
    c = ws.cell(row=1, column=col, value=name)
    c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_al, header_border

rows = [("Ноутбук", 79990, 3), ("Мышь", 1290, 15), ("Клавиатура", 3490, 8)]
for r, (name, price, qty) in enumerate(rows, start=2):
    ws["A"].cell(row=r, column=1, value=name)  # так нельзя — читай ниже!
```

Стоп! В последней строке ошибка: `ws["A"]` — это не колонка, а обращение к листу по имени. Правильно использовать `ws.cell(row=r, column=1, ...)`. Исправленная версия:

```python
for r, (name, price, qty) in enumerate(rows, start=2):
    ws.cell(row=r, column=1, value=name)
    ws.cell(row=r, column=2, value=price)
    ws.cell(row=r, column=3, value=qty)
    ws.cell(row=r, column=4, value=f"=B{r}*C{r}")

for col, width in zip("ABCD", [20, 10, 12, 14]):
    ws.column_dimensions[col].width = width

wb.save("shop.xlsx")
print("Сохранено: shop.xlsx")
```

А теперь прочитаем файл обратно:

```python
from openpyxl import load_workbook

wb = load_workbook("shop.xlsx")
ws = wb["Товары"]
for row in ws.iter_rows(min_row=1, max_row=5, values_only=True):
    print(row)
```

В колонке D ты увидишь строки формул: `('Ноутбук', 79990, 3, '=B2*C2')` — это ожидаемое поведение. Формулы живут в файле как текст, а считает их Excel.

<!--TASK-->
### Задача 1
Создай файл `budget.xlsx` с листом «Бюджет». Первая строка — шапка: «Категория», «План», «Факт», «Разница» — со стилями (жирный белый шрифт, синяя заливка `4472C4`, выравнивание по центру, рамки). Затем добавь четыре категории: Продукты (план 20000, факт 18500), Транспорт (5000, 6200), Связь (1500, 1500), Развлечения (8000, 7200). В колонке D для каждой строки запиши формулу `=B-C` (например, `=B2-C2`). Сохрани книгу, затем загрузи её заново и выведи на экран все строки через `iter_rows(values_only=True)`. Ожидаемый вывод: пять строк, и в колонке D видны тексты формул (а не числа).
### Задача 2
Напиши pytest-тест, который проверяет содержимое xlsx-артефакта. Создай модуль `inventory.py` с функцией `create_inventory(path)`, которая формирует книгу как в Задаче 1 (лист «Товары», шапка, три товара, формула в D) и сохраняет её по переданному пути, после чего возвращает путь. Затем создай файл `test_inventory.py`: тест вызывает `create_inventory(tmp_path / "inv.xlsx")`, загружает книгу обратно через `load_workbook` и проверяет: имя листа — «Товары», `ws["A1"].value == "Название"`, `ws["B2"].value == 79990`, а `ws["D2"].value` — строка, начинающаяся с `"="`. Запусти `python -m pytest test_inventory.py -q` и добейся зелёного результата.
### Задача 3
Напиши pytest-тест для стилей. Функция `style_header(ws)` в том же модуле `inventory.py` применяет к строке 1: жирный шрифт, синюю заливку `4472C4`, выравнивание по центру и тонкие рамки. Тест в `test_inventory.py`: создаёт книгу, вызывает `style_header`, затем проверяет `ws["A1"].font.bold is True`, `ws["A1"].fill.fill_type == "solid"`, что строка цвета `str(ws["A1"].fill.fgColor.rgb).endswith("4472C4")`, `ws["A1"].alignment.horizontal == "center"` и `ws["A1"].border.left.style == "thin"`. Помни: проверку фона лучше делать через `endswith`, потому что openpyxl хранит цвет в формате ARGB из 8 символов.
### Задача 4
Напиши pytest-тест для объединения ячеек и закрепления областей. Функция `make_report_sheet(wb)` создаёт в книге лист «Отчёт», объединяет ячейки `A1:C1`, пишет в `A1` заголовок «Отчёт о продажах» и закрепляет первую строку (`ws.freeze_panes = "A2"`). Тест: создаёт книгу, вызывает функцию, сохраняет по пути `tmp_path / "report.xlsx"`, загружает и проверяет: `str(list(ws.merged_cells.ranges)[0]) == "A1:C1"`, `ws.freeze_panes == "A2"` и `ws["A1"].value == "Отчёт о продажах"`.
### Задача 5
Напиши pytest-тест для числового формата и ширины колонок. Функция `format_money(ws)` в модуле `inventory.py`: для колонки B (строки 2–4) ставит `number_format = "#,##0.00"`, а ширину колонки B устанавливает равной 14. Тест: создаёт книгу с данными, вызывает `format_money`, сохраняет, загружает и проверяет `ws["B2"].number_format == "#,##0.00"` и `ws.column_dimensions["B"].width == 14`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Для записи ячеек используй `ws.cell(row=r, column=c, value=...)` в цикле по данным или прямое присваивание `ws["D2"] = "=B2-C2"`. После `wb.save("budget.xlsx")` открой файл заново `load_workbook("budget.xlsx")` и иди по строкам через `iter_rows(values_only=True)` — тогда ты увидишь, что openpyxl хранит формулу как строку.
### Подсказка 2
Функция должна принимать путь и возвращать его же — это удобно для тестов. В тесте используй встроенную фикстуру pytest `tmp_path`: она даёт временную папку, которая будет очищена автоматически. Проверка формулы: `assert isinstance(ws["D2"].value, str) and ws["D2"].value.startswith("=")`.
### Подсказка 3
Стили назначаются объекту ячейки: `cell.font = Font(bold=True)`, `cell.fill = PatternFill(fill_type="solid", fgColor="4472C4")`, `cell.alignment = Alignment(horizontal="center")`, `cell.border = Border(left=Side(style="thin"), right=Side(style="thin"), ...)`. В тесте сравнивай свойства выбранной ячейки, а не объекты целиком.
### Подсказка 4
`ws.merged_cells.ranges` — это коллекция объединённых диапазонов. Проверь её размер `len(...) == 1` и строковое представление первого элемента. `freeze_panes` присваивается строке: `ws.freeze_panes = "A2"` закрепляет всё, что выше и левее ячейки A2, то есть первую строку.
### Подсказка 5
`number_format` — обычная строка: `cell.number_format = "#,##0.00"`. Ширина колонки живёт в `ws.column_dimensions["B"].width`. Чтобы тест был правдивым, обязательно сохрани книгу и загрузи её снова — так ты проверишь реальный файл, а не объект в памяти.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Бюджет"

header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(fill_type="solid", fgColor="4472C4")
header_al = Alignment(horizontal="center", vertical="center")
thin = Side(style="thin", color="BFBFBF")
header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

for col, name in enumerate(["Категория", "План", "Факт", "Разница"], start=1):
    c = ws.cell(row=1, column=col, value=name)
    c.font, c.fill, c.alignment, c.border = header_font, header_fill, header_al, header_border

data = [("Продукты", 20000, 18500), ("Транспорт", 5000, 6200),
        ("Связь", 1500, 1500), ("Развлечения", 8000, 7200)]
for r, (cat, plan, fact) in enumerate(data, start=2):
    ws.cell(row=r, column=1, value=cat)
    ws.cell(row=r, column=2, value=plan)
    ws.cell(row=r, column=3, value=fact)
    ws.cell(row=r, column=4, value=f"=B{r}-C{r}")

wb.save("budget.xlsx")

wb2 = load_workbook("budget.xlsx")
ws2 = wb2["Бюджет"]
for row in ws2.iter_rows(min_row=1, max_row=5, values_only=True):
    print(row)
```

Вывод:

```
('Категория', 'План', 'Факт', 'Разница')
('Продукты', 20000, 18500, '=B2-C2')
('Транспорт', 5000, 6200, '=B3-C3')
('Связь', 1500, 1500, '=B4-C4')
('Развлечения', 8000, 7200, '=B5-C5')
```

Что здесь происходит? Мы построили книгу: создали лист, прописали стили шапки в цикле, заполнили данные и записали формулы как строки. При повторном открытии `data_only` не задан, поэтому openpyxl возвращает исходный текст формулы — это нормальное поведение и главный вывод урока: библиотека не считает формулы сама.
### Разбор 2
Модуль `inventory.py`:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def create_inventory(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Товары"

    font = Font(bold=True, color="FFFFFF")
    fill = PatternFill(fill_type="solid", fgColor="4472C4")
    al = Alignment(horizontal="center")
    thin = Side(style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col, name in enumerate(["Название", "Цена", "Количество", "Стоимость"], start=1):
        c = ws.cell(row=1, column=col, value=name)
        c.font, c.fill, c.alignment, c.border = font, fill, al, border

    rows = [("Ноутбук", 79990, 3), ("Мышь", 1290, 15), ("Клавиатура", 3490, 8)]
    for r, (name, price, qty) in enumerate(rows, start=2):
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=price)
        ws.cell(row=r, column=3, value=qty)
        ws.cell(row=r, column=4, value=f"=B{r}*C{r}")

    wb.save(path)
    return path
```

Тест `test_inventory.py`:

```python
from openpyxl import load_workbook
from inventory import create_inventory

def test_create_inventory_contents(tmp_path):
    path = create_inventory(tmp_path / "inv.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert ws.title == "Товары"
    assert ws["A1"].value == "Название"
    assert ws["B2"].value == 79990
    assert ws["D2"].value.startswith("=")
```

Что здесь происходит? Функция принимает путь и сохраняет книгу именно туда — тест может положить её во временную папку `tmp_path`, не засоряя рабочую директорию. Затем тест открывает файл заново: так проверяется реальный артефакт на диске. `startswith("=")` подтверждает, что в D2 лежит формула.
### Разбор 3
Функция и тест:

```python
def style_header(ws):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    font = Font(bold=True)
    fill = PatternFill(fill_type="solid", fgColor="4472C4")
    al = Alignment(horizontal="center", vertical="center")
    thin = Side(style="thin")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for col in range(1, ws.max_column + 1):
        c = ws.cell(row=1, column=col)
        c.font, c.fill, c.alignment, c.border = font, fill, al, border
    return ws
```

```python
from openpyxl import Workbook
from inventory import style_header

def test_style_header(tmp_path):
    wb = Workbook()
    ws = wb.active
    for col, name in enumerate(["A", "B", "C"], start=1):
        ws.cell(row=1, column=col, value=name)
    ws = style_header(ws)
    c = ws["A1"]
    assert c.font.bold is True
    assert c.fill.fill_type == "solid"
    assert str(c.fill.fgColor.rgb).endswith("4472C4")
    assert c.alignment.horizontal == "center"
    assert c.border.left.style == "thin"
```

Что здесь происходит? Стили применяются к каждой ячейке шапки. В тесте проверяются именно свойства, а не целые объекты: `c.fill.fgColor.rgb` возвращает цвет в формате ARGB (например, `004472C4`), поэтому сравниваем через `endswith`. Если бы мы сравнили целиком, тест был бы хрупким.
### Разбор 4
Функция и тест:

```python
def make_report_sheet(wb):
    ws = wb.create_sheet("Отчёт")
    ws.merge_cells("A1:C1")
    ws["A1"] = "Отчёт о продажах"
    ws.freeze_panes = "A2"
    return ws
```

```python
from openpyxl import Workbook, load_workbook
from inventory import make_report_sheet

def test_make_report_sheet(tmp_path):
    wb = Workbook()
    make_report_sheet(wb)
    path = tmp_path / "report.xlsx"
    wb.save(path)

    wb2 = load_workbook(path)
    ws = wb2["Отчёт"]
    assert len(ws.merged_cells.ranges) == 1
    assert str(list(ws.merged_cells.ranges)[0]) == "A1:C1"
    assert ws.freeze_panes == "A2"
    assert ws["A1"].value == "Отчёт о продажах"
```

Что здесь происходит? `merge_cells` объединяет диапазон, а `merged_cells.ranges` хранит список объединённых областей — после сохранения и загрузки он сохраняется. `freeze_panes` превращается в строку `"A2"`, что значит «закрепить всё выше и левее A2» (то есть шапку). Тест проверяет файл после round-trip, а значит, гарантирует, что настройки реально записались.
### Разбор 5
Функция и тест:

```python
def format_money(ws):
    for r in range(2, 5):
        ws.cell(row=r, column=2).number_format = "#,##0.00"
    ws.column_dimensions["B"].width = 14
    return ws
```

```python
from openpyxl import Workbook, load_workbook
from inventory import format_money, create_inventory

def test_format_money(tmp_path):
    path = create_inventory(tmp_path / "inv.xlsx")
    wb = load_workbook(path)
    ws = format_money(wb.active)
    wb.save(path)

    wb2 = load_workbook(path)
    ws2 = wb2.active
    assert ws2["B2"].number_format == "#,##0.00"
    assert ws2.column_dimensions["B"].width == 14
```

Что здесь происходит? Мы взяли реальный файл, применили к нему форматирование и сохранили повторно. `number_format` — строка, и сравнение с `"#,##0.00"` точно. Ширина колонки хранится в `column_dimensions`. Тест снова работает с файлом, а не с объектом в памяти — это главный принцип проверки офисных артефактов.
<!--/SOLUTION-->

<!--QUIZ-->
Какой объект представляет книгу Excel в openpyxl?
- Workbook
- Worksheet
- Cell
* Правильный ответ: Workbook
Создать книгу можно через Workbook(), а листы внутри неё — объекты Worksheet.

Как добавить новый лист в книгу?
- wb.add_sheet("Имя")
- wb.create_sheet("Имя")
- wb.new_sheet("Имя")
* Правильный ответ: wb.create_sheet("Имя")
Метод create_sheet добавляет лист в конец книги, а доступ к листу — через wb["Имя"].

Может ли openpyxl сам вычислять формулы?
- Да, всегда
- Нет, хранит их как строку
- Да, но только простые выражения
* Правильный ответ: Нет, хранит их как строку
openpyxl записывает формулу текстом; расчёт делает Excel при открытии файла.

Что вернёт load_workbook("f.xlsx", data_only=True) для ячейки с формулой, если файл не открывался в Excel?
- Саму формулу
- 0
- None
* Правильный ответ: None
Кэшированное значение формулы появляется только после сохранения файла в Excel. Если его нет — будет None.

Как задать жирный белый шрифт ячейке?
- cell.font = Font(bold=True, color="FFFFFF")
- cell.bold = True
- cell.style = "bold white"
* Правильный ответ: cell.font = Font(bold=True, color="FFFFFF")
Класс Font описывает шрифт: жирность, размер, цвет и т.д.

Как объединить ячейки A1:C1?
- ws.merge("A1:C1")
- ws.merge_cells("A1:C1")
- ws.combine("A1:C1")
* Правильный ответ: ws.merge_cells("A1:C1")
Метод merge_cells принимает диапазон строкой; проверить объединение можно через ws.merged_cells.ranges.

Что делает строка ws.freeze_panes = "A2"?
- Закрепляет колонку A
- Закрепляет всё, что выше и левее A2 (первую строку)
- Ничего, это просто текст
* Правильный ответ: Закрепляет всё, что выше и левее A2 (первую строку)
Область закрепления задаётся ячейкой: всё, что выше и левее неё, останется на экране при прокрутке.

Как сохранить книгу в файл?
- wb.write("file.xlsx")
- wb.save("file.xlsx")
- wb.export("file.xlsx")
* Правильный ответ: wb.save("file.xlsx")
Метод save записывает книгу на диск; путь передаётся строкой или Path.

Какая заливка задаётся сплошным цветом?
- PatternFill(fill_type="solid", fgColor="4472C4")
- Fill(color="4472C4")
- PatternFill(fgColor="4472C4")
* Правильный ответ: PatternFill(fill_type="solid", fgColor="4472C4")
Для сплошной заливки обязателен параметр fill_type="solid" и цвет fgColor.

Чем отличается ws["A1"] от ws.cell(row=1, column=1)?
- Это разные ячейки
- Это один и тот же способ доступа к A1
- ws.cell не существует
* Правильный ответ: Это один и тот же способ доступа к A1
Оба выражения возвращают объект Cell ячейки A1 — выбор стиля записи дело вкуса.
<!--/QUIZ-->
