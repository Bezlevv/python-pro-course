---
title: Excel: чтение и анализ данных
summary: Загрузка книг, чтение ячеек и диапазонов, агрегация данных и запись результатов обратно в Excel.
order: 2
duration: 45 мин
difficulty: intermediate
tags: openpyxl, excel, анализ данных, load_workbook, чтение
---

Чтение данных — вторая половина работы с Excel. Чаще всего книги открывают не для редактирования, а чтобы вытащить данные и проанализировать их. В этом уроке мы научимся загружать файлы, аккуратно обходить диапазоны и собирать из сырых ячеек осмысленные итоги.

## Загрузка книги

Для чтения используется `load_workbook`. Функция возвращает `Workbook`, из которого берём нужный лист:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb["Sales"]
print(ws["A1"].value)   # первая ячейка
```

Важный нюанс: если в файле есть формулы и ты хочешь получить их вычисленные значения, используй флаг `data_only=True`:

```python
wb = load_workbook("sales.xlsx", data_only=True)
```

Но помни из прошлого урока: если файл никогда не открывался в Excel, кэшированных значений нет, и формульные ячейки вернут `None`. В таком случае расчёты надо делать самому.

## Режим только для чтения

Большие файлы (десятки тысяч строк) лучше открывать в режиме `read_only=True`. В этом режиме листы читаются потоково, без загрузки всей книги в память:

```python
wb = load_workbook("big.xlsx", read_only=True)
```

Минусы: в этом режиме нельзя изменять ячейки, а часть настроек (например, стили) недоступна. Зато скорость и память — на высоте.

## Границы и обход

Количество заполненных строк и колонок сообщают `ws.max_row` и `ws.max_column`. Обходить таблицу удобно циклом `iter_rows`:

```python
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
    print(row)
```

`values_only=True` сразу превращает строку в кортеж значений. Получить все данные листа одним списком можно так:

```python
data = list(ws.iter_rows(values_only=True))
```

## Работа с заголовками

Первая строка почти всегда — названия полей. Надёжный код сначала строит словарь «название → индекс колонки», а потом обращается к данным по имени, а не по магическим номерам:

```python
header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
# теперь header["Сумма"] даёт номер колонки
```

Так анализ не сломается, если поменяется порядок колонок. `ws[1]` — это первая строка листа, итерируется по ячейкам.

## Агрегация

Суммы, средние, максимумы — обычные циклы. Разберём пример: посчитаем выручку по категориям и найдём самый продаваемый товар.

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx", data_only=True)
ws = wb["Sales"]

header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
by_category = {}
total = 0.0
count = 0

for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is None:          # пропускаем пустые строки
        continue
    category = row[header["Категория"] - 1]
    amount = row[header["Сумма"] - 1]
    by_category[category] = by_category.get(category, 0.0) + amount
    total += amount
    count += 1

print("Строк с данными:", count)
print("Общая выручка:", round(total, 2))
for cat, s in sorted(by_category.items()):
    print(f"{cat}: {s:.2f}")
```

Обрати внимание: `row` — кортеж, поэтому индексы считаем с нуля, а `header` даёт номер колонки с единицы, отсюда `- 1`.

Тип данных важен: числа приходят как `int`/`float`, даты — как `datetime`, текст — как `str`. Если в данных встречаются пропуски, они превращаются в `None` — проверяй перед арифметикой.

## Запись результатов обратно

Анализ обычно заканчивается отчётом. Результаты можно записать в новый лист той же книги или в отдельный файл:

```python
from openpyxl import Workbook

out = Workbook()
ws_out = out.active
ws_out.title = "Итоги"
ws_out.append(["Категория", "Сумма"])
for cat, s in sorted(by_category.items()):
    ws_out.append([cat, s])
out.save("summary.xlsx")
```

`ws.append(...)` добавляет строку в конец — это самый короткий способ заполнить лист данными.

<!--TASK-->
### Задача 1
Напиши скрипт `read_shop.py`, который загружает файл `shop.xlsx` (создай его сам: лист «Товары», шапка «Название, Цена, Количество, Стоимость» и три товара с ценами и количествами). Программа должна вывести на экран все строки листа и посчитать общую стоимость склада. Важно: колонка D в файле содержит формулы, поэтому не полагайся на `data_only` — считай стоимость сам: цена × количество. Ожидаемый вывод: строки таблицы и строка вида `Итого стоимость склада: 123.45` (число зависит от твоих данных).
### Задача 2
Напиши pytest-тест для функции чтения. Функция `load_rows(path)` в модуле `sales_utils.py` возвращает список кортежей всех строк листа без шапки (это значит, что первая строка пропускается). Тест в `test_sales_utils.py`: сначала создаёт книгу с данными (лист с заголовками и тремя строками значений), сохраняет её в `tmp_path`, затем вызывает `load_rows` и сравнивает результат с ожидаемым списком кортежей. Запусти `python -m pytest test_sales_utils.py -q`.
### Задача 3
Напиши pytest-тест с параметризацией. Функция `top_product(path)` возвращает название товара с максимальной стоимостью (стоимость = цена × количество, считай сам). С помощью `@pytest.mark.parametrize` проверь её на двух разных наборах данных: в первом максимум у «Ноутбука», во втором — у «Монитора». Для этого в тесте создавай разные книги и передавай пути в параметризованный тест.
### Задача 4
Напиши pytest-тест для агрегации по категориям. Функция `summarize_by_category(path)` возвращает словарь `{категория: сумма}`, где сумма считается как цена × количество по всем строкам. Тест: создай книгу с тремя категориями и несколькими товарами, сохрани в `tmp_path`, вызови функцию и проверь, что словарь содержит ожидаемые суммы. Затем добавь проверку пустой книги: если данных нет, функция возвращает пустой словарь.
### Задача 5
Напиши скрипт `make_summary.py`, который читает `sales.xlsx` и создаёт новый файл `summary.xlsx` с листом «Итоги». В нём должны быть строки: «Общая выручка», «Средняя стоимость заказа», «Максимальная стоимость», «Количество позиций» — каждая со своим значением. Затем напиши pytest-тест, который проверяет содержимое артефакта `summary.xlsx`: загружает его и убеждается, что ячейка с «Общая выручка» содержит правильное число (посчитай его заранее в тесте из тех же данных).
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай файл через `Workbook()` + `ws.append(...)`, как в конце теории. Для чтения используй `ws.iter_rows(values_only=True)`; шапку пропусти (например, `next(...)` или срез списка). Стоимость позиции — `цена * количество`, суммируй в цикле.
### Подсказка 2
Тест строит входной файл прямо в теле теста: `Workbook()`, `ws.append(["Название", "Цена"])`, затем строки данных, `wb.save(tmp_path / "data.xlsx")`. Функция `load_rows` читает `ws.iter_rows(min_row=2, values_only=True)` и возвращает `list(...)`. Сравнение — обычным `assert result == expected`.
### Подсказка 3
Параметризация: `@pytest.mark.parametrize("rows, expected", [...])`, где `rows` — список кортежей для книги, а `expected` — ожидаемое имя товара. Внутри теста создай книгу из `rows`, сохрани во временную папку и вызови `top_product`. Не забудь, что тест должен создать файл для каждого набора.
### Подсказка 4
В функции используй `dict.get(key, 0.0)` или `collections.defaultdict(float)` для накопления сумм. Для теста с пустой книгой просто не добавляй строки данных в лист — только шапку. Тогда `summarize_by_category` должна вернуть `{}`.
### Подсказка 5
Фиксируй ожидаемые значения в тесте, пересчитывая их из тех же данных, которые записываешь в `sales.xlsx`. Например, передай данные в хелпер, который создаёт файл, и посчитай итоги в тесте тем же способом. После создания `summary.xlsx` загрузи его и сравни значения ячеек.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from openpyxl import Workbook, load_workbook

# создаём входной файл, если его нет
wb = Workbook()
ws = wb.active
ws.title = "Товары"
ws.append(["Название", "Цена", "Количество", "Стоимость"])
ws.append(["Ноутбук", 79990, 3])
ws.append(["Мышь", 1290, 15])
ws.append(["Клавиатура", 3490, 8])
wb.save("shop.xlsx")

wb2 = load_workbook("shop.xlsx")
ws2 = wb2["Товары"]
total = 0.0
for row in ws2.iter_rows(values_only=True):
    print(row)
    if row[0] == "Название":
        continue
    total += row[1] * row[2]
print(f"Итого стоимость склада: {total:.2f}")
```

Вывод:

```
('Название', 'Цена', 'Количество', 'Стоимость')
('Ноутбук', 79990, 3, None)
('Мышь', 1290, 15, None)
('Клавиатура', 3490, 8, None)
Итого стоимость склада: 286810.00
```

Что здесь происходит? Мы не полагаемся на колонку D с формулами (она вернула бы `None` без `data_only`), а считаем стоимость сами: `row[1] * row[2]`. Шапка пропускается сравнением с её первым значением. Такой подход работает всегда, независимо от того, открывался ли файл в Excel.
### Разбор 2
Модуль `sales_utils.py`:

```python
from openpyxl import load_workbook

def load_rows(path):
    wb = load_workbook(path)
    ws = wb.active
    return list(ws.iter_rows(min_row=2, values_only=True))
```

Тест:

```python
from openpyxl import Workbook
from sales_utils import load_rows

def test_load_rows(tmp_path):
    path = tmp_path / "data.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Товар", "Цена"])
    ws.append(["Ноутбук", 79990])
    ws.append(["Мышь", 1290])
    wb.save(path)

    assert load_rows(path) == [("Ноутбук", 79990), ("Мышь", 1290)]
```

Что здесь происходит? `load_rows` пропускает первую строку (`min_row=2`) и возвращает список кортежей. Тест сам создаёт входной файл во временной папке — это чистый юнит-тест: он не зависит от посторонних файлов на диске, а `tmp_path` гарантирует очистку.
### Разбор 3
Функция:

```python
def top_product(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.active
    best_name, best_total = None, -1.0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        total = row[1] * row[2]
        if total > best_total:
            best_name, best_total = row[0], total
    return best_name
```

Тест:

```python
import pytest
from openpyxl import Workbook
from sales_utils import top_product

def make_book(path, rows):
    wb = Workbook()
    ws = wb.active
    ws.append(["Товар", "Цена", "Количество"])
    for r in rows:
        ws.append(r)
    wb.save(path)

@pytest.mark.parametrize("rows, expected", [
    ([("Ноутбук", 79990, 3), ("Мышь", 1290, 15)], "Ноутбук"),
    ([("Клавиатура", 3490, 8), ("Монитор", 25000, 2)], "Монитор"),
])
def test_top_product(tmp_path, rows, expected):
    path = tmp_path / "data.xlsx"
    make_book(path, rows)
    assert top_product(path) == expected
```

Что здесь происходит? `@pytest.mark.parametrize` запускает один тест с разными наборами данных. Хелпер `make_book` строит книгу из списка кортежей. Сравниваем только имя товара — результат функции. Так мы проверяем логику на двух разных «входных мирах» без дублирования кода теста.
### Разбор 4
Функция:

```python
from collections import defaultdict

def summarize_by_category(path):
    wb = load_workbook(path, data_only=True)
    ws = wb.active
    header = {cell.value: idx for idx, cell in enumerate(ws[1], start=1)}
    sums = defaultdict(float)
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        cat = row[header["Категория"] - 1]
        sums[cat] += row[header["Цена"] - 1] * row[header["Количество"] - 1]
    return dict(sums)
```

Тест:

```python
def test_summarize_by_category(tmp_path):
    path = tmp_path / "sales.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Категория", "Цена", "Количество"])
    ws.append(["Электроника", 1000, 2])
    ws.append(["Электроника", 500, 4])
    ws.append(["Канцтовары", 200, 10])
    wb.save(path)

    assert summarize_by_category(path) == {"Электроника": 4000.0, "Канцтовары": 2000.0}

def test_summarize_empty(tmp_path):
    path = tmp_path / "empty.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Категория", "Цена", "Количество"])
    wb.save(path)
    assert summarize_by_category(path) == {}
```

Что здесь происходит? Словарь `defaultdict(float)` удобно копит суммы: несуществующий ключ автоматически получает `0.0`. Индексы берутся из шапки, поэтому порядок колонок не важен. Пустая книга (только шапка) даёт пустой словарь — второй тест фиксирует этот крайний случай.
### Разбор 5
Скрипт `make_summary.py`:

```python
from openpyxl import Workbook, load_workbook

def make_summary(source_path, out_path):
    wb = load_workbook(source_path, data_only=True)
    ws = wb.active
    totals, count, max_total = 0.0, 0, 0.0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        t = row[1] * row[2]
        totals += t
        max_total = max(max_total, t)
        count += 1

    out = Workbook()
    out_ws = out.active
    out_ws.title = "Итоги"
    out_ws.append(["Показатель", "Значение"])
    out_ws.append(["Общая выручка", round(totals, 2)])
    out_ws.append(["Средняя стоимость заказа", round(totals / count, 2)])
    out_ws.append(["Максимальная стоимость", round(max_total, 2)])
    out_ws.append(["Количество позиций", count])
    out.save(out_path)
    return out_path
```

Тест:

```python
def test_make_summary(tmp_path):
    src = tmp_path / "sales.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["Товар", "Цена", "Количество"])
    ws.append(["Ноутбук", 79990, 3])
    ws.append(["Мышь", 1290, 15])
    wb.save(src)

    out = make_summary(src, tmp_path / "summary.xlsx")
    wb2 = load_workbook(out)
    ws2 = wb2["Итоги"]
    rows = {r[0]: r[1] for r in ws2.iter_rows(min_row=2, values_only=True)}
    assert rows["Общая выручка"] == 79990 * 3 + 1290 * 15
    assert rows["Количество позиций"] == 2
```

Что здесь происходит? `make_summary` читает исходник, считает итоги и пишет новый файл. Тест независимо пересчитывает ожидаемую выручку из тех же данных и сравнивает с содержимым артефакта — то есть проверяет реальный файл, а не внутреннюю логику функции.
<!--/SOLUTION-->

<!--QUIZ-->
Как загрузить книгу с диска?
- Workbook("file.xlsx")
- load_workbook("file.xlsx")
- open("file.xlsx")
* Правильный ответ: load_workbook("file.xlsx")
load_workbook читает файл и возвращает объект Workbook.

Что делает флаг read_only=True в load_workbook?
- Ускоряет чтение и экономит память, но запрещает изменения
- Разрешает изменять ячейки
- Включает подсветку формул
* Правильный ответ: Ускоряет чтение и экономит память, но запрещает изменения
В режиме read_only листы читаются потоково, но писать в книгу нельзя.

Что возвращает ws.max_row?
- Номер последней строки с данными
- Количество колонок
- Список всех строк
* Правильный ответ: Номер последней строки с данными
ws.max_row — число заполненных строк (последняя строка с данными).

Что делает параметр values_only=True в iter_rows?
- Возвращает кортежи значений вместо объектов Cell
- Возвращает только непустые ячейки
- Возвращает заголовки колонок
* Правильный ответ: Возвращает кортежи значений вместо объектов Cell
Так данные сразу готовы к использованию: кортежи значений, а не объекты ячеек.

Почему при data_only=True формульные ячейки могут быть None?
- В файле нет формул
- Файл не пересчитывался и не сохранялся в Excel
- openpyxl не умеет читать формулы
* Правильный ответ: Файл не пересчитывался и не сохранялся в Excel
Кэшированные значения формул появляются только после открытия и сохранения файла в Excel.

Как найти номер колонки по названию в шапке?
- Прочитать первую строку и построить словарь имя → индекс
- Использовать ws.column("Название")
- Это невозможно
* Правильный ответ: Прочитать первую строку и построить словарь имя → индекс
Словарь вида {cell.value: idx for idx, cell in enumerate(ws[1], start=1)} делает код устойчивым к перестановке колонок.

Как пропустить пустые строки при анализе?
- Проверять, что первое значение строки не None
- Вызывать skip()
- Пустые строки не встречаются
* Правильный ответ: Проверять, что первое значение строки не None
Пустые ячейки превращаются в None, поэтому условие if row[0] is None: continue надёжно отсекает пустые строки.

Какой тип у даты, считанной из ячейки Excel?
- str
- datetime.datetime
- float
* Правильный ответ: datetime.datetime
Excel хранит даты как числа с форматом; openpyxl конвертирует их в datetime.

Как добавить строку в конец листа?
- ws.append([...])
- ws.add_row([...])
- ws.insert([...])
* Правильный ответ: ws.append([...])
Метод append дописывает строку значений в конец листа — удобно при построении отчётов.

Что вернёт list(ws.iter_rows(values_only=True))?
- Список кортежей всех строк листа
- Список объектов Cell
- Число строк
* Правильный ответ: Список кортежей всех строк листа
iter_rows с values_only=True генерирует кортежи значений, а list(...) собирает их в список.
<!--/QUIZ-->
