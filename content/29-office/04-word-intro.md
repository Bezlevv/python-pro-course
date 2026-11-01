---
title: python-docx: документы, стили, таблицы
summary: Создание документов Word: параграфы, стили, таблицы, изображения, разделы и сохранение.
order: 4
duration: 45 мин
difficulty: intermediate
tags: python-docx, word, документы, стили, таблицы
---

python-docx — библиотека для создания и изменения документов Word (`.docx`) без самого Word. Документ `.docx` — это XML внутри zip-архива, и python-docx аккуратно работает с этой структурой. Установка:

```bash
pip install python-docx
```

## Базовые объекты

Документ строится иерархически: `Document` → `section` (раздел) → `paragraph` (параграф) → `run` (фрагмент текста с единым форматированием), а также `table` (таблица) → `row` → `cell` → параграфы.

```python
from docx import Document

doc = Document()               # новый пустой документ
p = doc.add_paragraph("Привет!")  # параграф
doc.save("hello.docx")
```

Пустой `Document()` уже содержит один пустой параграф. Любой текст слова — это последовательность `run`-ов. Именно на `run`-ах висят свойства форматирования: жирность, курсив, размер, цвет.

```python
p = doc.add_paragraph()
run = p.add_run("Важное сообщение")
run.bold = True
run.italic = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

## Заголовки и стили

Заголовки добавляются через `add_heading`, стили — через присваивание `paragraph.style`:

```python
doc.add_heading("Отчёт", level=1)          # заголовок 1 уровня
doc.add_heading("Подраздел", level=2)

p = doc.add_paragraph("Обычный текст")
p.style = doc.styles["Heading 2"]          # применить готовый стиль
```

Встроенные стили: `"Title"`, `"Heading 1"`, `"Heading 2"`, `"Normal"`, `"Quote"`, `"Intense Quote"` и другие. `doc.styles` — коллекция стилей документа.

## Выравнивание параграфа

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

p = doc.add_paragraph("По центру")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

## Таблицы

```python
table = doc.add_table(rows=2, cols=3)
table.cell(0, 0).text = "Ячейка A1"
table.cell(0, 1).text = "Ячейка B1"
table.add_row()                 # добавить строку
table.style = "Light Grid Accent 1"
```

Ячейка — это мини-документ со своими параграфами. `table.style` принимает имя встроенного стиля таблицы Word.

## Изображения

`add_picture` вставляет картинку в новый параграф. Ширину и высоту можно задать в дюймах (`Inches`) или сантиметрах (`Cm`):

```python
from docx.shared import Inches, Pt, Cm, RGBColor

doc.add_picture("logo.png", width=Inches(2))
```

Если нужна картинка внутри конкретного параграфа — добавь её через run:

```python
p = doc.add_paragraph()
p.add_run().add_picture("logo.png", height=Cm(3))
```

Для примера сгенерируем изображение библиотекой Pillow (она ставится как `pip install pillow`):

```python
from PIL import Image

img = Image.new("RGB", (200, 100), "steelblue")
img.save("logo.png")
```

## Разделы и страница

У документа есть разделы (`doc.sections`) — области с собственными настройками страницы. По умолчанию раздел один:

```python
section = doc.sections[0]
print(section.page_width, section.page_height)
```

`doc.add_page_break()` вставляет разрыв страницы в текущий поток текста.

## Чтение документа

Готовый документ открывается тем же классом:

```python
doc2 = Document("hello.docx")
for p in doc2.paragraphs:
    print(p.text)
print("Таблиц:", len(doc2.tables))
```

`doc.paragraphs` — все параграфы, `doc.tables` — все таблицы. Это основа для тестов: сгенерировал документ — открой его и проверь содержимое.

## Полный пример

Соберём мини-отчёт: заголовок, абзац, таблица и картинка.

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

Image.new("RGB", (200, 100), "steelblue").save("logo.png")

doc = Document()
doc.add_heading("Отчёт о продажах", level=1)

p = doc.add_paragraph("Итоги за квартал.")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

table = doc.add_table(rows=2, cols=2)
table.style = "Light Grid Accent 1"
table.cell(0, 0).text = "Показатель"
table.cell(0, 1).text = "Значение"
table.cell(1, 0).text = "Выручка"
table.cell(1, 1).text = "1 200 000"

doc.add_picture("logo.png", width=Inches(1.5))
doc.save("report.docx")
print("Готово: report.docx")
```

<!--TASK-->
### Задача 1
Создай файл `resume.docx`: заголовок уровня 1 «Резюме», параграф с именем и должностью (например, «Иван Петров — Python-разработчик»), список из трёх навыков (параграфы с маркерами или обычные абзацы) и таблицу 2×2 «Язык → Уровень» (Python → Продвинутый, SQL → Средний). Сохрани документ, затем загрузи его заново и выведи на экран все параграфы и количество строк таблицы. Ожидаемый вывод: тексты параграфов и число строк.
### Задача 2
Напиши pytest-тест для содержимого docx-артефакта. Функция `create_document(path)` создаёт документ с тремя параграфами, причём средний — жирный (run с `bold=True`), сохраняет по пути и возвращает путь. Тест: загружает документ через `Document(path)` и проверяет, что `len(doc.paragraphs) == 3`, второй параграф содержит текст, а его первый run имеет `bold is True`.
### Задача 3
Напиши pytest-тест для таблицы. Функция `add_skills_table(doc)` добавляет в документ таблицу 3×2 со стилем `"Light Grid Accent 1"`, заполняет её заголовками и двумя строками данных. Тест: создаёт документ, вызывает функцию, сохраняет в `tmp_path`, загружает и проверяет: `len(doc.tables) == 1`, `len(table.rows) == 3`, `len(table.columns) == 2` и `table.cell(0, 0).text == "Язык"`.
### Задача 4
Напиши pytest-тест для вставки изображения. Функция `add_logo(doc, image_path)` вставляет картинку шириной 2 дюйма. Тест: создай изображение через Pillow (например, красный прямоугольник 100×50) в `tmp_path`, вызови функцию, сохрани документ, загрузи его и проверь: `len(doc.inline_shapes) == 1` и `doc.inline_shapes[0].width` больше нуля.
### Задача 5
Напиши pytest-тест для форматирования run-ов. Функция `style_summary(doc)` добавляет параграф с run: жирным, курсивным, размером 14 pt и красным цветом (`RGBColor(0xFF, 0, 0)`). Тест: сохраняет документ, загружает, находит последний параграф, берёт его первый run и проверяет все четыре свойства.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Параграфы добавляются через `doc.add_paragraph(...)`, заголовок — `doc.add_heading("Резюме", level=1)`. Таблица: `doc.add_table(rows=3, cols=2)` и заполнение через `table.cell(r, c).text`. После сохранения открой документ заново: `doc2 = Document("resume.docx")`, затем `for p in doc2.paragraphs: print(p.text)` и `print(len(doc2.tables[0].rows))`.
### Подсказка 2
Жирность задаётся на run: `run.bold = True`. Чтобы проверить именно его, создай параграф явно: `p = doc.add_paragraph(); run = p.add_run("текст"); run.bold = True`. В тесте: `p = doc.paragraphs[1]; assert p.runs[0].bold is True`.
### Подсказка 3
После загрузки документа доступ к таблице: `table = doc.tables[0]`. Число строк — `len(table.rows)`, колонок — `len(table.columns)`. Текст ячейки — `table.cell(0, 0).text`. Не забудь назначить стиль `table.style = "Light Grid Accent 1"` до заполнения.
### Подсказка 4
`doc.inline_shapes` — список встроенных изображений документа; у каждого есть `width` (в EMU, число). Проверка `shape.width > 0` гарантирует, что картинка вставлена с ненулевым размером. Width задавай так: `doc.add_picture(image_path, width=Inches(2))`.
### Подсказка 5
Свойства run: `bold`, `italic`, `font.size` (объект Pt — сравнивай `run.font.size.pt == 14`), `font.color.rgb` (сравнивай с `RGBColor(0xFF, 0, 0)`). Импорты: `from docx.shared import Pt, RGBColor`. Если параграф содержит один run — бери `p.runs[0]`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from docx import Document

doc = Document()
doc.add_heading("Резюме", level=1)
doc.add_paragraph("Иван Петров — Python-разработчик")
for skill in ["Python", "SQL", "Git"]:
    doc.add_paragraph(f"- {skill}")

table = doc.add_table(rows=3, cols=2)
table.cell(0, 0).text = "Язык"
table.cell(0, 1).text = "Уровень"
table.cell(1, 0).text = "Python"
table.cell(1, 1).text = "Продвинутый"
table.cell(2, 0).text = "SQL"
table.cell(2, 1).text = "Средний"

doc.save("resume.docx")

doc2 = Document("resume.docx")
for p in doc2.paragraphs:
    print(p.text)
table2 = doc2.tables[0]
print("Строк в таблице:", len(table2.rows))
```

Вывод содержит тексты параграфов и строку `Строк в таблице: 3`. Что здесь происходит? Мы собрали документ из стандартных блоков: заголовок, абзацы, таблица. При повторном открытии `doc.paragraphs` отдаёт все параграфы (включая заголовок), а `doc.tables[0]` — первую таблицу. Число строк `len(table2.rows)` подтверждает, что таблица записалась целиком.
### Разбор 2
Функция:

```python
from docx import Document

def create_document(path):
    doc = Document()
    doc.add_paragraph("Первый параграф")
    p = doc.add_paragraph()
    run = p.add_run("Второй, жирный")
    run.bold = True
    doc.add_paragraph("Третий параграф")
    doc.save(path)
    return path
```

Тест:

```python
from docx import Document
from word_docs import create_document

def test_create_document(tmp_path):
    path = create_document(tmp_path / "doc.docx")
    doc = Document(path)
    assert len(doc.paragraphs) == 3
    p = doc.paragraphs[1]
    assert p.text == "Второй, жирный"
    assert p.runs[0].bold is True
```

Что здесь происходит? Функция строит документ и возвращает путь — тест открывает артефакт с диска. Параграфы считаются по `doc.paragraphs`, а форматирование проверяется на конкретном run. Если бы жирность была не на run, а где-то ещё, тест бы это поймал.
### Разбор 3
Функция:

```python
def add_skills_table(doc):
    table = doc.add_table(rows=3, cols=2)
    table.style = "Light Grid Accent 1"
    table.cell(0, 0).text = "Язык"
    table.cell(0, 1).text = "Уровень"
    table.cell(1, 0).text = "Python"
    table.cell(1, 1).text = "Продвинутый"
    table.cell(2, 0).text = "SQL"
    table.cell(2, 1).text = "Средний"
    return table
```

Тест:

```python
from docx import Document
from word_docs import add_skills_table

def test_add_skills_table(tmp_path):
    doc = Document()
    add_skills_table(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    table = doc2.tables[0]
    assert len(doc2.tables) == 1
    assert len(table.rows) == 3
    assert len(table.columns) == 2
    assert table.cell(0, 0).text == "Язык"
```

Что здесь происходит? Тест проверяет реальный файл после round-trip: одна таблица, 3 строки, 2 колонки, содержимое первой ячейки. `table.cell(0, 0).text` — чтение текста ячейки; это надёжный способ проверки данных документа.
### Разбор 4
Функция и тест:

```python
from docx.shared import Inches

def add_logo(doc, image_path):
    doc.add_picture(image_path, width=Inches(2))
    return doc
```

```python
from docx import Document
from PIL import Image
from word_docs import add_logo

def test_add_logo(tmp_path):
    img_path = tmp_path / "logo.png"
    Image.new("RGB", (100, 50), "red").save(img_path)

    doc = Document()
    add_logo(doc, img_path)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    assert len(doc2.inline_shapes) == 1
    assert doc2.inline_shapes[0].width > 0
```

Что здесь происходит? Изображение создаётся Pillow прямо во временной папке — тест не зависит от внешних файлов. `inline_shapes` содержит встроенные изображения; ширина хранится в условных единицах EMU, поэтому проверяем «больше нуля». Так мы убеждаемся, что картинка реально попала в документ.
### Разбор 5
Функция:

```python
from docx.shared import Pt, RGBColor

def style_summary(doc):
    p = doc.add_paragraph()
    run = p.add_run("Итоги")
    run.bold = True
    run.italic = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0xFF, 0, 0)
    return p
```

Тест:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from word_docs import style_summary

def test_style_summary(tmp_path):
    doc = Document()
    style_summary(doc)
    path = tmp_path / "doc.docx"
    doc.save(path)

    doc2 = Document(path)
    run = doc2.paragraphs[-1].runs[0]
    assert run.bold is True
    assert run.italic is True
    assert run.font.size.pt == 14
    assert run.font.color.rgb == RGBColor(0xFF, 0, 0)
```

Что здесь происходит? Все четыре свойства заданы на одном run. После загрузки мы берём последний параграф документа и его первый run. Сравнение `run.font.size.pt == 14` проверяет размер в пунктах, а `run.font.color.rgb` — цвет. Это ровно те проверки, что нужны для контроля оформления отчётов.
<!--/SOLUTION-->

<!--QUIZ-->
Как создать новый документ Word в python-docx?
- Document()
- Word()
- Docx()
* Правильный ответ: Document()
Класс Document открывает новый документ или существующий файл.

Из чего состоит параграф в python-docx?
- Из run-ов (фрагментов текста)
- Из ячеек
- Из разделов
* Правильный ответ: Из run-ов (фрагментов текста)
Каждый run — кусок текста со своими свойствами (жирность, цвет, размер).

Как сделать текст жирным?
- run.bold = True
- paragraph.bold = True
- Text.bold = True
* Правильный ответ: run.bold = True
Жирность — свойство run, а не параграфа целиком.

Как добавить заголовок уровня 2?
- doc.add_heading("Текст", level=2)
- doc.add_title("Текст", 2)
- doc.add_paragraph("Текст", style="H2")
* Правильный ответ: doc.add_heading("Текст", level=2)
add_heading создаёт параграф со стилем соответствующего уровня.

Как добавить таблицу 3×4?
- doc.add_table(rows=3, cols=4)
- doc.create_table(3, 4)
- doc.add_table(3, 4)
* Правильный ответ: doc.add_table(rows=3, cols=4)
Метод add_table принимает количество строк и колонок именованными аргументами.

Как записать текст в ячейку таблицы?
- table.cell(0, 0).text = "Привет"
- table[0][0] = "Привет"
- cell.write("Привет")
* Правильный ответ: table.cell(0, 0).text = "Привет"
table.cell(r, c) возвращает ячейку, у которой есть свойство text.

Что делает doc.add_picture("logo.png", width=Inches(2))?
- Вставляет изображение в новый параграф с шириной 2 дюйма
- Вставляет изображение на замену тексту
- Сохраняет картинку отдельным файлом
* Правильный ответ: Вставляет изображение в новый параграф с шириной 2 дюйма
add_picture добавляет картинку как встроенное изображение; размер задаётся в Inches или Cm.

Как открыть существующий документ?
- Document("file.docx")
- open("file.docx")
- Load("file.docx")
* Правильный ответ: Document("file.docx")
Передай путь в конструктор Document — и получишь документ для чтения и правки.

Где взять список всех параграфов документа?
- doc.paragraphs
- doc.runs
- doc.text
* Правильный ответ: doc.paragraphs
Свойство paragraphs возвращает все параграфы документа в порядке следования.

Что такое раздел (section) в python-docx?
- Область с собственными настройками страницы
- Отдельный абзац
- Таблица
* Правильный ответ: Область с собственными настройками страницы
У документа как минимум один раздел; у каждого свои поля, ориентация и размер страницы.
<!--/QUIZ-->
