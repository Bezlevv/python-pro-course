---
title: Word: сложные отчёты и шаблоны
summary: Работа с шаблонами docx, плейсхолдеры, колонтитулы, разделы, динамические таблицы и слияние.
order: 5
duration: 50 мин
difficulty: advanced
tags: python-docx, word, шаблоны, отчёты, разделы
---

В этом уроке мы перейдём от отдельных блоков к настоящим производственным отчётам: шаблоны с плейсхолдерами, колонтитулы, разделы с разной ориентацией и динамические таблицы. Всё это — то, что нужно для генерации десятков однотипных документов.

## Шаблоны и плейсхолдеры

Вместо построения документа с нуля можно взять готовый `.docx` с фирменным оформлением и наполнить его данными. `Document("template.docx")` открывает любой существующий файл, а все `add_*` дописывают в конец. Чтобы вставлять данные в середину, используют «плейсхолдеры» — маркеры вида `{{name}}`, которые потом заменяются:

```python
from docx import Document

doc = Document("template.docx")
for p in doc.paragraphs:
    if "{{company}}" in p.text:
        p.text = "ООО «Ромашка»"
    if "{{date}}" in p.text:
        p.text = "1 ноября 2026"
doc.save("report.docx")
```

Присваивание `p.text` заменяет весь текст параграфа одним run — просто и надёжно. Если нужно сохранить форматирование части текста — работай с run-ами по отдельности.

## Колонтитулы

Колонтитулы живут в разделе: `section.header` и `section.footer`. По умолчанию там один пустой параграф:

```python
section = doc.sections[0]
header = section.header
header.paragraphs[0].text = "Отчёт | 2026"
footer = section.footer
footer.paragraphs[0].text = "Стр. "
```

Можно добавить и новые параграфы: `header.add_paragraph("...")`. Для разных первого/чётных/нечётных страниц существует `section.different_first_page_header_footer`.

## Разделы

Раздел — это «кусок» документа со своими настройками страницы. `doc.add_section(WD_SECTION.NEW_PAGE)` начинает новый раздел с новой страницы:

```python
from docx.enum.section import WD_SECTION, WD_ORIENT

sec = doc.add_section(WD_SECTION.NEW_PAGE)
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = sec.page_height, sec.page_width
```

При смене ориентации ширину и высоту нужно поменять местами — иначе страница просто «не повернётся». Так внутрь книжного отчёта вставляется альбомная страница для широкой таблицы.

## Динамические таблицы

Число строк часто известно только во время выполнения. `table.add_row()` добавляет строку в конец:

```python
data = [("Москва", 13_000_000), ("Питер", 5_600_000)]
table = doc.add_table(rows=1, cols=2)
table.style = "Table Grid"
table.cell(0, 0).text = "Город"
table.cell(0, 1).text = "Население"
for city, pop in data:
    row = table.add_row()
    row.cells[0].text = city
    row.cells[1].text = str(pop)
```

Объединение ячеек — метод `merge`:

```python
table.cell(0, 0).merge(table.cell(0, 1))   # объединить A1 и B1
```

После слияния `row.cells` отдаёт уникальные ячейки: в объединённой строке их станет меньше — это удобно проверять в тестах.

## Слияние документов

Чтобы склеить несколько отчётов, переносим содержимое источника в цель:

```python
def append_document(target, source_path):
    src = Document(source_path)
    for p in src.paragraphs:
        target.add_paragraph(p.text)
    for table in src.tables:
        new_table = target.add_table(rows=len(table.rows), cols=len(table.columns))
        for r, row in enumerate(table.rows):
            for c, cell in enumerate(row.cells):
                new_table.cell(r, c).text = cell.text
```

Это «конвейер»: несколько документов собираются в один итоговый.

## Проверка результата

После генерации обязательно открой результат тем же python-docx и сверь состав: `doc.paragraphs`, `doc.tables`, `doc.sections`. В шаблонных системах именно проверка артефакта — залог того, что ни один маркер не остался незаменённым.

<!--TASK-->
### Задача 1
Создай шаблон `template.docx` с текстом «Компания: {{company}}, дата: {{date}}, менеджер: {{manager}}». Затем напиши скрипт, который открывает шаблон, заменяет маркеры на реальные значения (например, «ООО Ромашка», «2026-11-01», «Иван Петров») и сохраняет новый файл `filled.docx`. После этого выведи на экран все параграфы `filled.docx`. Ожидаемый вывод: одна строка без маркеров с подставленными значениями.
### Задача 2
Напиши pytest-тест для замены плейсхолдеров. Функция `render_template(template_path, out_path, replacements)` принимает путь к шаблону, путь результата и словарь `{маркер: значение}`, заменяет все вхождения вида `{{ключ}}` в параграфах и сохраняет результат. Тест: создай шаблон с тремя маркерами, вызови функцию, загрузи результат и проверь, что текст параграфа содержит значения, а маркеры исчезли.
### Задача 3
Напиши pytest-тест для колонтитулов. Функция `add_header_footer(doc, header_text, footer_text)` записывает текст в первый параграф верхнего и нижнего колонтитулов первой секции. Тест: создаёт документ, вызывает функцию, сохраняет, загружает и проверяет `doc.sections[0].header.paragraphs[0].text` и аналогично для footer.
### Задача 4
Напиши pytest-тест для альбомного раздела. Функция `add_landscape_section(doc)` добавляет новый раздел с новой страницы, переводит его в альбомную ориентацию и меняет ширину/высоту местами. Тест: проверяет, что `len(doc.sections) == 2`, `doc.sections[1].orientation == WD_ORIENT.LANDSCAPE` и ширина второго раздела больше высоты.
### Задача 5
Напиши pytest-тест для динамической таблицы с объединением. Функция `build_report_table(doc, data)` создаёт таблицу: первая строка — объединённая шапка «Итоги по регионам» через `merge`, вторая строка — заголовки «Город, Население», дальше строки из `data`. Тест: проверяет `len(doc.tables) == 1`, число строк равно `2 + len(data)`, в объединённой строке `len(table.rows[0].cells) == 1`, а текст первой ячейки второй строки — «Город».
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Плейсхолдеры — просто текст, поэтому замена — это перебор `doc.paragraphs` и `str.replace`. Шаблон создай тем же python-docx: `doc.add_paragraph("Компания: {{company}}, дата: {{date}}, менеджер: {{manager}}")`. После замены сохрани результат в новый файл.
### Подсказка 2
Словарь `replacements` хранит `{"company": "ООО Ромашка", ...}`. В цикле по параграфам для каждой пары ключ/значение делай `p.text = p.text.replace("{{" + key + "}}", value)`. В тесте после загрузки проверь: `"{{" not in p.text` и `"ООО Ромашка" in p.text`.
### Подсказка 3
Колонтитулы: `doc.sections[0].header.paragraphs[0].text = header_text`. Не забудь сохранить и перезагрузить документ перед проверкой — текст колонтитула читается из файла. Для footer — `doc.sections[0].footer.paragraphs[0].text`.
### Подсказка 4
`doc.add_section(WD_SECTION.NEW_PAGE)` возвращает новый раздел. После присваивания `sec.orientation = WD_ORIENT.LANDSCAPE` поменяй местами `sec.page_width` и `sec.page_height`. В тесте сравнивай `sec.page_width > sec.page_height`. Импорт: `from docx.enum.section import WD_SECTION, WD_ORIENT`.
### Подсказка 5
Объединение: `table.cell(0, 0).merge(table.cell(0, 1))`. После этого в `table.rows[0].cells` останется одна ячейка. Строки добавляй через `table.add_row()` и заполняй `row.cells[0].text = ...`. Число строк: 1 (шапка) + 1 (заголовки) + len(data).
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from docx import Document

doc = Document()
doc.add_paragraph("Компания: {{company}}, дата: {{date}}, менеджер: {{manager}}")
doc.save("template.docx")

doc2 = Document("template.docx")
for p in doc2.paragraphs:
    p.text = (p.text.replace("{{company}}", "ООО Ромашка")
                   .replace("{{date}}", "2026-11-01")
                   .replace("{{manager}}", "Иван Петров"))
doc2.save("filled.docx")

doc3 = Document("filled.docx")
for p in doc3.paragraphs:
    print(p.text)
```

Вывод:

```
Компания: ООО Ромашка, дата: 2026-11-01, менеджер: Иван Петров
```

Что здесь происходит? Шаблон — обычный документ с маркерами. Замена идёт по тексту каждого параграфа: `str.replace` меняет вхождения, а присваивание `p.text` перезаписывает текст единым run. Такой подход позволяет держать оформление в шаблоне, а данные подставлять программно.
### Разбор 2
Функция:

```python
from docx import Document

def render_template(template_path, out_path, replacements):
    doc = Document(template_path)
    for p in doc.paragraphs:
        for key, value in replacements.items():
            p.text = p.text.replace("{{" + key + "}}", value)
    doc.save(out_path)
    return out_path
```

Тест:

```python
from docx import Document
from reports_word import render_template

def test_render_template(tmp_path):
    tpl = tmp_path / "template.docx"
    doc = Document()
    doc.add_paragraph("{{company}} / {{date}} / {{manager}}")
    doc.save(tpl)

    out = render_template(tpl, tmp_path / "out.docx",
                          {"company": "ООО Ромашка", "date": "2026",
                           "manager": "Иван Петров"})
    result = Document(out)
    text = result.paragraphs[0].text
    assert "ООО Ромашка" in text
    assert "2026" in text
    assert "Иван Петров" in text
    assert "{{" not in text
```

Что здесь происходит? Функция универсальна: принимает словарь замен, поэтому легко расширяется. Тест создаёт шаблон, прогоняет рендер и проверяет артефакт: значения подставлены, маркеров не осталось. Это ключевая проверка шаблонных систем — «не ушёл ни один плейсхолдер».
### Разбор 3
Функция:

```python
def add_header_footer(doc, header_text, footer_text):
    section = doc.sections[0]
    section.header.paragraphs[0].text = header_text
    section.footer.paragraphs[0].text = footer_text
    return doc
```

Тест:

```python
from docx import Document
from reports_word import add_header_footer

def test_add_header_footer(tmp_path):
    doc = Document()
    add_header_footer(doc, "Отчёт 2026", "Стр. ?")
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    section = doc2.sections[0]
    assert section.header.paragraphs[0].text == "Отчёт 2026"
    assert section.footer.paragraphs[0].text == "Стр. ?"
```

Что здесь происходит? Колонтитулы привязаны к разделу: `section.header` и `section.footer` — это объекты с параграфами. Первый параграф по умолчанию пустой — в него и пишем текст. Проверка после перезагрузки подтверждает, что колонтитулы сохранились в файле.
### Разбор 4
Функция:

```python
from docx.enum.section import WD_SECTION, WD_ORIENT

def add_landscape_section(doc):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = sec.page_height, sec.page_width
    return sec
```

Тест:

```python
def test_add_landscape_section(tmp_path):
    doc = Document()
    add_landscape_section(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    assert len(doc2.sections) == 2
    sec = doc2.sections[1]
    assert sec.orientation == WD_ORIENT.LANDSCAPE
    assert sec.page_width > sec.page_height
```

Что здесь происходит? Новый раздел начинается с новой страницы. После смены ориентации ширина и высота меняются местами — иначе `orientation` сам по себе ничего не даст. Тест проверяет и количество разделов, и ориентацию, и геометрию страницы.
### Разбор 5
Функция:

```python
def build_report_table(doc, data):
    table = doc.add_table(rows=2, cols=2)
    table.style = "Table Grid"
    table.cell(0, 0).merge(table.cell(0, 1))
    table.cell(0, 0).text = "Итоги по регионам"
    table.cell(1, 0).text = "Город"
    table.cell(1, 1).text = "Население"
    for city, pop in data:
        row = table.add_row()
        row.cells[0].text = city
        row.cells[1].text = str(pop)
    return table
```

Тест:

```python
def test_build_report_table(tmp_path):
    doc = Document()
    data = [("Москва", 13_000_000), ("Санкт-Петербург", 5_600_000)]
    build_report_table(doc, data)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    table = doc2.tables[0]
    assert len(doc2.tables) == 1
    assert len(table.rows) == 2 + len(data)
    assert len(table.rows[0].cells) == 1   # объединённая шапка
    assert table.cell(1, 0).text == "Город"
```

Что здесь происходит? `merge` объединяет две ячейки первой строки — поэтому `table.rows[0].cells` содержит одну ячейку. Строки добавляются динамически, и общее число строк равно 2 + len(data). Тест проверяет и структуру, и данные — ровно то, что нужно для проверки сложных таблиц.
<!--/SOLUTION-->

<!--QUIZ-->
Как открыть существующий документ как шаблон?
- Document("template.docx")
- Template("template.docx")
- OpenTemplate("template.docx")
* Правильный ответ: Document("template.docx")
Конструктор Document открывает любой .docx, и все add_* дописывают в конец.

Что такое плейсхолдер в шаблоне?
- Маркер вроде {{company}}, который заменяется данными
- Готовый стиль документа
- Таблица с данными
* Правильный ответ: Маркер вроде {{company}}, который заменяется данными
Плейсхолдеры — текст-метка; программа заменяет их реальными значениями.

Что произойдёт после присваивания p.text = "...".
?
- Текст параграфа заменится одним run
- Добавится новый параграф
- Ничего, p.text только для чтения
* Правильный ответ: Текст параграфа заменится одним run
Присваивание p.text перезаписывает содержимое параграфа единым run.

Где живут колонтитулы в python-docx?
- В разделе: section.header и section.footer
- В отдельном файле
- В каждом run-е
* Правильный ответ: В разделе: section.header и section.footer
Колонтитулы привязаны к секции документа.

Как добавить новый раздел с новой страницы?
- doc.add_section(WD_SECTION.NEW_PAGE)
- doc.new_page()
- doc.add_page_section()
* Правильный ответ: doc.add_section(WD_SECTION.NEW_PAGE)
add_section создаёт раздел; WD_SECTION.NEW_PAGE означает начало с новой страницы.

Что нужно сделать при переводе раздела в альбомную ориентацию?
- Поменять местами page_width и page_height
- Ничего, достаточно orientation
- Удалить раздел
* Правильный ответ: Поменять местами page_width и page_height
Иначе страница останется книжной по геометрии.

Как добавить строку в существующую таблицу?
- table.add_row()
- table.append_row()
- row = table.new_row()
* Правильный ответ: table.add_row()
add_row добавляет строку в конец таблицы и возвращает её.

Как объединить ячейки A1 и B1 таблицы?
- table.cell(0, 0).merge(table.cell(0, 1))
- table.merge("A1:B1")
- cell.join(0, 1)
* Правильный ответ: table.cell(0, 0).merge(table.cell(0, 1))
Метод merge вызывается на ячейке и принимает ячейку-партнёра.

Что вернёт table.rows[0].cells после объединения ячеек в первой строке?
- Список с одной ячейкой
- Список из двух ячеек
- Ошибку
* Правильный ответ: Список с одной ячейкой
row.cells отдаёт уникальные ячейки — объединённые не дублируются.

Как проверить, что в документе ровно одна таблица?
- len(doc.tables) == 1
- doc.table_count() == 1
- doc.tables == 1
* Правильный ответ: len(doc.tables) == 1
doc.tables — список всех таблиц документа.
<!--/QUIZ-->
