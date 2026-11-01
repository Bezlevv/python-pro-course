---
title: Excel: диаграммы и оформление отчётов
summary: Построение диаграмм через openpyxl.chart, настройка внешнего вида, подготовка листа к печати.
order: 3
duration: 45 мин
difficulty: intermediate
tags: openpyxl, диаграммы, chart, отчёты, печать
---

Диаграммы — лучшее, что делает отчёт наглядным. openpyxl умеет строить стандартные типы: столбчатые, линейные, круговые. Всё, что нужно, — описать данные ссылками на диапазоны листа, и библиотека сама упакует их в объект-диаграмму, которую Excel покажет при открытии файла.

## База: Reference и add_chart

Работа с диаграммами идёт через подмодуль `openpyxl.chart`. Сначала создаём объект диаграммы, затем описываем ссылку на данные (`Reference`) и размещаем диаграмму на листе:

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active
ws.append(["Месяц", "Продажи", "Прибыль"])
ws.append(["Январь", 120, 30])
ws.append(["Февраль", 150, 40])
ws.append(["Март", 90, 20])

chart = BarChart()
data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "E2")
wb.save("sales.xlsx")
```

Разбор: `Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)` — прямоугольник данных из двух колонок (Продажи и Прибыль) вместе с шапкой. `add_data(data, titles_from_data=True)` понимает, что первая строка — названия рядов. `set_categories(cats)` подставляет категории по оси X (месяцы). Итог: `ws.add_chart(chart, "E2")` прикрепляет диаграмму к листу, начиная с ячейки E2.

## Настройка диаграммы

Объект диаграммы имеет множество свойств:

```python
chart.title = "Продажи по месяцам"
chart.style = 10            # встроенная палитра (0–48)
chart.y_axis.title = "тыс. руб."
chart.x_axis.title = "Месяц"
chart.width = 20            # ширина в сантиметрах
chart.height = 10
chart.legend.position = "bottom"
```

Подписи значений включаются через `DataLabelList`:

```python
from openpyxl.chart.label import DataLabelList

chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True
```

Цвет ряда меняется через `graphicalProperties`:

```python
chart.series[0].graphicalProperties.solidFill = "4472C4"
```

## Круговая диаграмма

`PieChart` работает почти так же, но у него нет осей, а данные — один ряд:

```python
from openpyxl.chart import PieChart

pie = PieChart()
data = Reference(ws, min_col=2, min_row=1, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
pie.add_data(data, titles_from_data=True)
pie.set_categories(cats)
pie.title = "Структура продаж"
ws.add_chart(pie, "E18")
```

На одном листе может быть сколько угодно диаграмм — каждая прикрепляется своей координатой.

## Оформление и печать

Перед отправкой отчёта стоит настроить лист: скрыть сетку, задать область печати, ориентацию страницы:

```python
ws.sheet_view.showGridLines = False
ws.print_area = "A1:F15"
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.sheet_properties.tabColor = "4472C4"   # цвет вкладки
```

`print_area` ограничивает печать диапазоном; `fitToWidth`/`fitToHeight` вписывают лист в одну страницу при печати; `showGridLines = False` убирает серую сетку с экрана.

## Проверка диаграмм

Диаграммы хранятся в списке `ws._charts`. Хотя атрибут полуофициальный (с подчёркиванием), именно так их читают в тестах:

```python
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb.active
print(len(ws._charts))       # количество диаграмм
print(ws._charts[0].title)   # заголовок первой
```

Это позволяет писать pytest-тесты, которые проверяют, что отчёт действительно содержит диаграмму с нужным заголовком.

<!--TASK-->
### Задача 1
Создай файл `sales_chart.xlsx`: лист «Продажи» с шапкой «Месяц, Продажи, Прибыль» и шестью месяцами (Январь–Июнь) с произвольными числами. Добавь столбчатую диаграмму с заголовком «Продажи по месяцам», подписями значений, легендой снизу и синим цветом первого ряда. Сохрани файл, затем загрузи его заново и выведи на экран количество диаграмм на листе и заголовок первой из них. Ожидаемый вывод: `1` и `Продажи по месяцам`.
### Задача 2
Напиши pytest-тест, проверяющий наличие диаграммы в артефакте xlsx. Функция `make_sales_chart(path)` создаёт книгу с данными продаж (как в Задаче 1) и столбчатой диаграммой с заголовком «Продажи по месяцам», сохраняет её по пути и возвращает путь. Тест: вызывает функцию с `tmp_path / "sales.xlsx"`, загружает книгу, проверяет, что `len(ws._charts) == 1` и что `ws._charts[0].title == "Продажи по месяцам"`.
### Задача 3
Напиши pytest-тест для круговой диаграммы. Функция `make_pie_chart(path)` создаёт книгу с данными по категориям (название и значение) и круговой диаграммой с заголовком «Структура». Тест: после сохранения и загрузки проверь, что на листе ровно одна диаграмма, она является экземпляром `PieChart` (импортируй из `openpyxl.chart.pie_chart`), а её заголовок равен «Структура».
### Задача 4
Напиши pytest-тест для настроек печати. Функция `setup_print(ws)` настраивает лист: скрывает сетку (`showGridLines = False`), устанавливает область печати `A1:F15`, ориентацию `landscape` и цвет вкладки `4472C4`. Тест: создаёт книгу, вызывает функцию, сохраняет в `tmp_path`, загружает и проверяет: `ws.page_setup.orientation == "landscape"`, `ws.sheet_view.showGridLines is False`, `ws.sheet_properties.tabColor.rgb` заканчивается на `4472C4`, а `ws.print_area` содержит `A1:F15` (после загрузки может стать `$A$1:$F$15` — допусти обе формы).
### Задача 5
Напиши pytest-тест для полного отчёта. Функция `build_report(path)` создаёт лист «Отчёт» с данными, столбчатой диаграммой и настройками печати (всё из Задач 2 и 4). Тест загружает артефакт и проверяет сразу всё: есть одна диаграмма с заголовком, ориентация `landscape`, сетка скрыта, область печати установлена.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Данные удобно добавлять через `ws.append([...])` в цикле по списку месяцев. Ссылки на данные строй через `Reference(ws, min_col=2, max_col=3, min_row=1, max_row=7)` (шапка + 6 месяцев). Подписи значений: `chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True`. Цвет первого ряда: `chart.series[0].graphicalProperties.solidFill = "4472C4"`.
### Подсказка 2
Функция должна сохранять книгу по переданному пути и возвращать его. В тесте просто проверь `ws._charts`: это список объектов диаграмм. У диаграммы есть свойство `title` — сравнивай с ожидаемым заголовком. Не забудь импортировать `BarChart` и `Reference`.
### Подсказка 3
`PieChart` импортируется из `openpyxl.chart.pie_chart`. Проверка типа: `isinstance(chart, PieChart)`. Круговая диаграмма создаётся так же, как столбчатая, но без осей. `add_data` с `titles_from_data=True` и `set_categories` — обязательны.
### Подсказка 4
Цвет вкладки после загрузки: `ws.sheet_properties.tabColor.rgb` — сравнивай через `endswith("4472C4")`, чтобы не зависеть от формата ARGB. `print_area` при повторном открытии может стать `$A$1:$F$15` — используй `in ("A1:F15", "$A$1:$F$15")` или проверку `"A1:F15" in ws.print_area`.
### Подсказка 5
Собери `build_report` из уже готовых функций: `make_sales_chart` (без сохранения — верни книгу) и `setup_print`. Для этого разбей функции так, чтобы `make_sales_chart` возвращала `(wb, ws)`, а `setup_print` принимала `ws`. В тесте проверяй все настройки одним вызовом.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

wb = Workbook()
ws = wb.active
ws.title = "Продажи"
ws.append(["Месяц", "Продажи", "Прибыль"])
months = [("Январь", 120, 30), ("Февраль", 150, 40), ("Март", 90, 20),
          ("Апрель", 170, 45), ("Май", 200, 55), ("Июнь", 180, 50)]
for row in months:
    ws.append(row)

chart = BarChart()
data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=7)
cats = Reference(ws, min_col=1, min_row=2, max_row=7)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.title = "Продажи по месяцам"
chart.legend.position = "bottom"
chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True
chart.series[0].graphicalProperties.solidFill = "4472C4"
ws.add_chart(chart, "E2")

wb.save("sales_chart.xlsx")

wb2 = load_workbook("sales_chart.xlsx")
ws2 = wb2["Продажи"]
print(len(ws2._charts))
print(ws2._charts[0].title)
```

Вывод:

```
1
Продажи по месяцам
```

Что здесь происходит? Данные записаны через `append`. Диаграмма собирается из ссылок: `data` охватывает обе числовые колонки с шапкой, а `cats` — месяццы. Подписи значений, легенда и цвет ряда настраиваются свойствами диаграммы. После сохранения `ws._charts` содержит одну диаграмму с нужным заголовком — так мы убеждаемся, что диаграмма реально попала в файл.
### Разбор 2
Модуль (фрагмент):

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

def make_sales_chart(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Продажи"
    ws.append(["Месяц", "Продажи", "Прибыль"])
    for name, s, p in [("Январь", 120, 30), ("Февраль", 150, 40), ("Март", 90, 20)]:
        ws.append([name, s, p])

    chart = BarChart()
    data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = "Продажи по месяцам"
    chart.dataLabels = DataLabelList()
    chart.dataLabels.showVal = True
    ws.add_chart(chart, "E2")

    wb.save(path)
    return path
```

Тест:

```python
from openpyxl import load_workbook
from report_charts import make_sales_chart

def test_make_sales_chart(tmp_path):
    path = make_sales_chart(tmp_path / "sales.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert len(ws._charts) == 1
    assert ws._charts[0].title == "Продажи по месяцам"
```

Что здесь происходит? Функция инкапсулирует создание отчёта, а тест проверяет артефакт на диске. `ws._charts` — список диаграмм листа; в нём ровно одна, и её заголовок совпадает. Такой тест ловит регрессии: если кто-то удалит диаграмму или поменяет заголовок — тест упадёт.
### Разбор 3
Функция:

```python
from openpyxl.chart import PieChart, Reference

def make_pie_chart(path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Категория", "Доля"])
    ws.append(["Ноутбуки", 45])
    ws.append(["Мыши", 25])
    ws.append(["Клавиатуры", 30])

    pie = PieChart()
    data = Reference(ws, min_col=2, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(cats)
    pie.title = "Структура"
    ws.add_chart(pie, "D2")

    wb.save(path)
    return path
```

Тест:

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
    assert chart.title == "Структура"
```

Что здесь происходит? `PieChart` — отдельный класс (не наследник `BarChart`), поэтому проверка `isinstance` точна. У круговой диаграммы нет осей: хватает одного ряда данных и категорий. Заголовок сохраняется в файле и читается обратно.
### Разбор 4
Функция:

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

Тест:

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

Что здесь происходит? Настройки печати сохраняются в файл и читаются обратно. `print_area` при повторном открытии превращается в абсолютную ссылку `$A$1:$F$15`, поэтому проверяем через `in`. Цвет вкладки сравнивается через `endswith` — формат ARGB добавляет прозрачность в начало строки.
### Разбор 5
Сборка:

```python
def build_report(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Отчёт"
    ws.append(["Месяц", "Продажи"])
    for name, s in [("Январь", 120), ("Февраль", 150), ("Март", 90)]:
        ws.append([name, s])

    chart = BarChart()
    data = Reference(ws, min_col=2, min_row=1, max_row=4)
    cats = Reference(ws, min_col=1, min_row=2, max_row=4)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.title = "Продажи"
    ws.add_chart(chart, "D2")
    setup_print(ws)

    wb.save(path)
    return path
```

Тест:

```python
def test_build_report(tmp_path):
    path = build_report(tmp_path / "report.xlsx")
    wb = load_workbook(path)
    ws = wb.active
    assert len(ws._charts) == 1
    assert ws._charts[0].title == "Продажи"
    assert ws.page_setup.orientation == "landscape"
    assert ws.sheet_view.showGridLines is False
    assert "A1:F15" in ws.print_area
```

Что здесь происходит? `build_report` объединяет данные, диаграмму и печать в один отчёт. Интеграционный тест проверяет артефакт целиком: диаграмма на месте, страница альбомная, сетка скрыта, область печати задана. Это ровно то, что нужно автоматизировать при выпуске регулярных отчётов.
<!--/SOLUTION-->

<!--QUIZ-->
Из какого подмодуля импортируется BarChart?
- openpyxl.chart
- openpyxl.styles
- openpyxl.cell
* Правильный ответ: openpyxl.chart
Все диаграммы живут в openpyxl.chart: BarChart, LineChart, PieChart и другие.

Что описывает объект Reference?
- Ссылку на диапазон ячеек листа
- Стиль ячейки
- Формат числа
* Правильный ответ: Ссылку на диапазон ячеек листа
Reference(ws, min_col=..., min_row=..., max_col=..., max_row=...) задаёт прямоугольник данных для диаграммы.

Что делает add_data(data, titles_from_data=True)?
- Добавляет ряд данных, считая первую строку названиями рядов
- Добавляет категории
- Сохраняет книгу
* Правильный ответ: Добавляет ряд данных, считая первую строку названиями рядов
Флаг titles_from_data сообщает, что шапка — это подписи серий.

Зачем нужен set_categories(cats)?
- Чтобы задать подписи по оси X
- Чтобы задать цвет диаграммы
- Чтобы добавить подписи значений
* Правильный ответ: Чтобы задать подписи по оси X
Категории — это метки оси X (например, месяцы или категории).

Как прикрепить диаграмму к листу?
- ws.add_chart(chart, "E2")
- chart.attach(ws)
- ws.charts.append(chart)
* Правильный ответ: ws.add_chart(chart, "E2")
Метод add_chart размещает диаграмму на листе, начиная с указанной ячейки.

Как включить подписи значений на диаграмме?
- chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True
- chart.values = True
- chart.labels = True
* Правильный ответ: chart.dataLabels = DataLabelList(); chart.dataLabels.showVal = True
DataLabelList управляет подписями: showVal показывает сами значения.

Как поменять цвет ряда на диаграмме?
- chart.series[0].graphicalProperties.solidFill = "4472C4"
- chart.series[0].color = "4472C4"
- chart.fill = "4472C4"
* Правильный ответ: chart.series[0].graphicalProperties.solidFill = "4472C4"
Цвет заливки ряда задаётся через graphicalProperties.solidFill.

Как скрыть сетку листа?
- ws.sheet_view.showGridLines = False
- ws.hide_grid()
- ws.gridlines = False
* Правильный ответ: ws.sheet_view.showGridLines = False
Свойство showGridLines в sheet_view управляет отображением сетки.

Что делает ws.print_area = "A1:F15"?
- Ограничивает печать диапазоном A1:F15
- Печатает все листы
- Сохраняет только выделенное
* Правильный ответ: Ограничивает печать диапазоном A1:F15
print_area задаёт область листа, которая попадёт в печать.

Где хранятся диаграммы листа для проверки в тестах?
- В списке ws._charts
- В ws.diagrams
- Их нельзя прочитать обратно
* Правильный ответ: В списке ws._charts
Это полуофициальный, но рабочий атрибут; len(ws._charts) показывает число диаграмм.
<!--/QUIZ-->
