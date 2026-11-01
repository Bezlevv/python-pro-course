---
title: Excel и Word: отчёты автоматически
summary: Автоматизируем офисные будни: создаём и форматируем таблицы Excel через openpyxl, а документы Word — через python-docx.
order: 4
duration: 35 мин
difficulty: intermediate
tags: openpyxl, python-docx, excel, word, отчёты
---

«Отчёт к понедельнику» — фраза, от которой вздрагивает любой офисный работник. А ведь именно такие задачи Python закрывает идеально: собрать данные, посчитать итоги, оформить таблицу. В этом уроке мы познакомимся с двумя библиотеками: `openpyxl` (Excel) и `python-docx` (Word).

## Установка

```bash
pip install openpyxl python-docx
```

## Создаём Excel-файл

Работа с `openpyxl` начинается с книги (`Workbook`) и листа (`Worksheet`):

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Продажи"
```

Добавлять данные можно по одной ячейке или целой строкой через `append()`:

```python
ws.append(["Товар", "Штук", "Цена"])      # шапка
ws.append(["Ноутбук", 12, 75000])
ws.append(["Мышка", 48, 1500])
ws.append(["Клавиатура", 20, 3500])
wb.save("sales.xlsx")
```

Форматирование — через стили: `Font` для шрифта, `PatternFill` для заливки:

```python
from openpyxl.styles import Font, PatternFill

bold = Font(bold=True)
fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
for cell in ws[1]:                 # первая строка — шапка
    cell.font = bold
    cell.fill = fill
```

Ширину колонки задаёт атрибут `column_dimensions`:

```python
ws.column_dimensions["A"].width = 15
```

## Читаем Excel

Чтение не сложнее создания:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
```

`iter_rows(values_only=True)` возвращает значения построчно — удобно для подсчёта сумм.

## Создаём Word-документ

`python-docx` строит документ из абзацев и таблиц. Начинаем с заголовка:

```python
from docx import Document

doc = Document()
doc.add_heading("Отчёт по продажам", level=1)
doc.add_paragraph("Составлен автоматически.")
doc.save("report.docx")
```

Таблицу добавляет метод `add_table`:

```python
table = doc.add_table(rows=1, cols=3)
hdr = table.rows[0].cells
hdr[0].text = "Товар"
hdr[1].text = "Штук"
hdr[2].text = "Цена"
```

Как видишь, принцип один и тот же: создать объект, наполнить данными, сохранить. Теперь соберём настоящий автоотчёт.

<!--TASK-->
### Задача 1
Создай Excel-файл `sales.xlsx` с тремя колонками: `Товар`, `Штук`, `Цена`. Лист назови `Продажи`, добавь шапку и три строки данных (придумай товары сам). Сохрани файл через `wb.save("sales.xlsx")`. Ожидаемый результат: файл появился рядом со скриптом и открывается в Excel или LibreOffice.

### Задача 2
Добавь форматирование к файлу из задачи 1: сделай шапку жирным шрифтом через `Font(bold=True)`, добавь жёлтую заливку через `PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")` и задай ширину колонки `A` равной 15. Ожидаемый результат: при открытии файла шапка выделена жёлтым и написана жирно.

### Задача 3
Прочитай `sales.xlsx` обратно через `load_workbook` и напечатай все строки данных без шапки (через `iter_rows(min_row=2, values_only=True)`), а затем сумму столбца «Штук». Ожидаемый результат: три строки данных в консоли и строка `Всего штук: <сумма>`.

### Задача 4
Создай Word-документ `report.docx`: заголовок `Отчёт по продажам` (уровень 1), абзац-введение и список из трёх пунктов (можно через три `add_paragraph` с дефисом в начале). Сохрани документ. Ожидаемый результат: открывающийся `report.docx` с заголовком, текстом и списком.

### Задача 5
Напиши программу-автоотчёт: прочитай `sales.xlsx`, для каждой строки посчитай выручку (`Штук × Цена`), построй в Word таблицу с колонками `Товар`, `Штук`, `Выручка` и итоговой строкой `ИТОГО` с общей суммой. Сохрани как `report.docx`. Ожидаемый результат: документ с таблицей и итогом, а в консоли — общая выручка.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`wb = Workbook(); ws = wb.active; ws.title = "Продажи"`. Строки добавляй через `ws.append([...])`: сначала шапку, потом данные. В конце `wb.save("sales.xlsx")` — без сохранения файла не будет.

### Подсказка 2
После `from openpyxl.styles import Font, PatternFill` создай `bold = Font(bold=True)` и `fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")`. Пройдись по шапке: `for cell in ws[1]: cell.font = bold; cell.fill = fill`. Ширина: `ws.column_dimensions["A"].width = 15`.

### Подсказка 3
`wb = load_workbook("sales.xlsx")`, `ws = wb.active`. Сумму копи, пока идёшь по `ws.iter_rows(min_row=2, values_only=True)`: в каждой строке элемент с индексом 1 — это «Штук». Печатай строки и итог после цикла.

### Подсказка 4
`doc = Document()`; `doc.add_heading("Отчёт по продажам", level=1)`; `doc.add_paragraph("Введение...")`; пункты списка — это просто абзацы: `doc.add_paragraph("- пункт 1")` и так далее; в конце `doc.save("report.docx")`.

### Подсказка 5
Собери алгоритм: читаешь Excel → создаёшь `Document()` → `add_heading` → `add_table(rows=1, cols=3)` → заполняешь шапку таблицы → для каждой строки Excel добавляешь строку таблицы через `table.add_row().cells` → итоговая строка. Выручку считай как `qty * price`, общую сумму накапливай в переменной.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Продажи"

ws.append(["Товар", "Штук", "Цена"])
ws.append(["Ноутбук", 12, 75000])
ws.append(["Мышка", 48, 1500])
ws.append(["Клавиатура", 20, 3500])

wb.save("sales.xlsx")
print("Файл sales.xlsx создан")
```

Что здесь происходит? `Workbook()` создаёт новую книгу с одним пустым листом, а `wb.active` возвращает этот лист. `ws.title` меняет его имя. `append()` добавляет строку целиком — значения распределяются по ячейкам слева направо. Наконец, `wb.save("sales.xlsx")` записывает книгу на диск. Обрати внимание: без `save()` файл не появится — это самая частая ошибка новичков.

### Разбор 2
Решение:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Продажи"

ws.append(["Товар", "Штук", "Цена"])
ws.append(["Ноутбук", 12, 75000])
ws.append(["Мышка", 48, 1500])
ws.append(["Клавиатура", 20, 3500])

bold = Font(bold=True)
fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

for cell in ws[1]:
    cell.font = bold
    cell.fill = fill

ws.column_dimensions["A"].width = 15

wb.save("sales.xlsx")
```

Что здесь происходит? Стили в openpyxl — это объекты, которые присваиваются ячейкам. `Font(bold=True)` делает текст жирным, `PatternFill` заливает ячейку цветом: `start_color` и `end_color` — цвета в формате RRGGBB (без решётки), а `fill_type="solid"` означает сплошную заливку. `ws[1]` обращается к первой строке (система координат XLSX начинается с единицы). Проход циклом по ячейкам шапки — самый простой способ применить стиль ко всей строке. `column_dimensions["A"].width = 15` задаёт ширину колонки A.

### Разбор 3
Решение:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active

total_qty = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    item, qty, price = row
    print(item, qty, price)
    total_qty += qty

print("Всего штук:", total_qty)
```

Результат (пример):

```
Ноутбук 12 75000
Мышка 48 1500
Клавиатура 20 3500
Всего штук: 80
```

Что здесь происходит? `load_workbook` открывает существующий файл. `iter_rows(min_row=2, values_only=True)` перебирает строки, начиная со второй (первая — шапка), и возвращает значения ячеек кортежами. Распаковка `item, qty, price = row` — чистый способ разобрать кортеж. В цикле мы сразу накапливаем сумму в `total_qty`. `values_only=True` — важный параметр: без него вы получили бы объекты ячеек, а не их значения.

### Разбор 4
Решение:

```python
from docx import Document

doc = Document()
doc.add_heading("Отчёт по продажам", level=1)
doc.add_paragraph("Этот отчёт составлен автоматически программой на Python.")
doc.add_paragraph("- Ноутбуки")
doc.add_paragraph("- Мышки")
doc.add_paragraph("- Клавиатуры")

doc.save("report.docx")
print("Документ report.docx создан")
```

Что здесь происходит? `Document()` создаёт пустой документ Word. `add_heading("...", level=1)` добавляет заголовок первого уровня — он получит стандартный стиль «Заголовок 1» с крупным шрифтом. `add_paragraph` добавляет обычные абзацы; пункты списка здесь оформлены просто дефисами в начале текста (для настоящего маркированного списка можно было бы использовать стиль `List Bullet`, но и такой вариант полностью открывается в Word). Всё сохраняется через `doc.save()`.

### Разбор 5
Решение:

```python
from openpyxl import load_workbook
from docx import Document

wb = load_workbook("sales.xlsx")
ws = wb.active

doc = Document()
doc.add_heading("Отчёт по продажам", level=1)

table = doc.add_table(rows=1, cols=3)
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text = "Товар", "Штук", "Выручка"

total = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    item, qty, price = row
    revenue = qty * price
    total += revenue
    cells = table.add_row().cells
    cells[0].text = item
    cells[1].text = str(qty)
    cells[2].text = f"{revenue:.0f} руб."

row = table.add_row().cells
row[0].text = "ИТОГО"
row[2].text = f"{total:.0f} руб."

doc.save("report.docx")
print("Готово! Общая выручка:", total)
```

Что здесь происходит? Это и есть настоящий автоотчёт. Мы читаем Excel, создаём Word-документ и таблицу из одной строки-шапки. Для каждой строки данных добавляем строку таблицы `table.add_row().cells`, заполняем ячейки текстом: выручку считаем как произведение количества на цену. Итоговая строка «ИТОГО» подводит сумму. Так один запуск скрипта заменяет час ручной работы в офисе — именно для этого и существует офисная автоматизация.
<!--/SOLUTION-->

<!--QUIZ-->
Как создать новый Excel-файл в openpyxl?
- openpyxl.file()
- Workbook() и wb.save("file.xlsx")
- xl.create()
- sheet.make()
* Правильный ответ: Workbook() и wb.save("file.xlsx")
Workbook создаёт книгу, а save записывает её на диск.

Что делает ws.append([...])?
- Добавляет строку значений в конец листа
- Удаляет строку
- Переименовывает лист
- Меняет цвет ячейки
* Правильный ответ: Добавляет строку значений в конец листа
append() принимает список или кортеж и записывает его следующей строкой.

Чем load_workbook отличается от Workbook?
- load_workbook читает существующий файл, а Workbook создаёт новый
- Это одно и то же
- load_workbook создаёт новую книгу
- Workbook читает файл
* Правильный ответ: load_workbook читает существующий файл, а Workbook создаёт новый
load_workbook("file.xlsx") открывает файл с диска, Workbook() начинает с чистого листа.

Как сделать текст ячейки жирным?
- cell.bold = True
- Присвоить ячейке Font(bold=True)
- cell.style = "bold"
- cell.font_size = 14
* Правильный ответ: Присвоить ячейке Font(bold=True)
Стили в openpyxl — объекты: создаёшь Font(bold=True) и присваиваешь cell.font.

Как добавить таблицу в Word-документ?
- doc.table.append(...)
- doc.add_table(rows=1, cols=3)
- doc.insert_table(...)
- table = doc.new_table(...)
* Правильный ответ: doc.add_table(rows=1, cols=3)
add_table создаёт таблицу с указанным числом строк и колонок.

Как добавить заголовок в python-docx?
- doc.add_title("...")
- doc.add_heading("...", level=1)
- doc.header("...")
- doc.add_text("...", style="heading")
* Правильный ответ: doc.add_heading("...", level=1)
add_heading добавляет заголовок с нужным уровнем, от 1 до 9.
<!--/QUIZ-->
