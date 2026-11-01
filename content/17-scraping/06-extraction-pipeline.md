---
title: Конвейер сбора: HTML → данные → CSV/БД
summary: Полный конвейер: загрузка, парсинг, извлечение, очистка, дедупликация и сохранение в CSV и SQLite.
order: 6
duration: 45 мин
difficulty: advanced
tags: csv, sqlite3, конвейер, очистка данных, хранение, дедупликация
---

Ты умеешь скачивать страницы, разбирать HTML и обходить пагинацию. Пора собрать всё в единый **конвейер** — программу, которая превращает «сырой» HTML в аккуратные данные на диске: в CSV-файл или базу данных. Именно так устроены настоящие сборщики данных.

## Стадии конвейера

Любой конвейер сбора состоит из этапов:

1. **Fetch** — скачать страницу (`requests`).
2. **Parse** — разобрать HTML в дерево (`BeautifulSoup`).
3. **Extract** — вытащить нужные поля (текст, авторы, цены).
4. **Clean** — почистить: убрать пробелы, пустые значения, превратить строки в числа.
5. **Store** — сохранить в CSV или базу данных.

Разделение на стадии — это и есть модульность: можно менять источник данных, не трогая сохранение, и наоборот.

## Сохранение в CSV

Модуль `csv` — стандартный. Запись списка словарей:

```python
import csv

rows = [
    {"author": "Аня", "book": "Python для начинающих"},
    {"author": "Борис", "book": "SQL без слёз"},
]

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "book"])
    writer.writeheader()
    writer.writerows(rows)
```

Обязательно `newline=""` — иначе в файле появятся лишние пустые строки. `encoding="utf-8"` — чтобы кириллица читалась правильно. `DictWriter` сам пишет заголовки и строки из словарей.

Чтение обратно:

```python
with open("books.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["author"], "-", row["book"])
```

## Сохранение в SQLite

SQLite — база данных в одном файле, встроенная прямо в Python (модуль `sqlite3`). Для парсинга это удобнее CSV: есть типы, поиск по запросам и защита от дубликатов:

```python
import sqlite3

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

cur.execute(
    "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
    ("Текст цитаты", "Автор", "life, love"),
)
conn.commit()
conn.close()
```

`?` — плейсхолдеры: никогда не подставляй значения в SQL-строку через f-строки — это опасно. `conn.commit()` сохраняет изменения, `conn.close()` закрывает файл.

## Очистка данных

Извлечённые значения редко бывают идеальными. Типичные операции:

```python
price_text = "£51.77"
price = float(price_text[1:])   # '51.77' -> 51.77

name = "  Аня  "
name = name.strip()              # убираем пробелы по краям

if not name:
    continue                     # пропускаем пустые значения
```

Правило: **очищай до сохранения** — в файл/базу должны попадать уже готовые данные.

## Дедупликация

Если запустить один и тот же конвейер дважды, данные продублируются. Решение — в базе: `UNIQUE(text, author)` + `INSERT OR IGNORE` (пропустить, если такая строка уже есть). В CSV такой защиты нет — поэтому уникальность приходится обеспечивать в коде, например через множество уже встреченных id.

## Полный конвейер

Соберём цитаты в SQLite:

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for q in soup.select("div.quote"):
        text = q.select_one("span.text").get_text().strip()
        author = q.select_one("small.author").get_text().strip()
        tags = ", ".join(t.get_text() for t in q.select("a.tag"))
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (text, author, tags),
        )

conn.commit()
cur.execute("SELECT COUNT(*) FROM quotes")
print("Всего цитат:", cur.fetchone()[0])
conn.close()
```

Здесь в одном цикле соединены все стадии: запрос → разбор → извлечение → очистка (`strip`) → сохранение с дедупликацией.

## Итог

Конвейер = fetch → parse → extract → clean → store. CSV — просто, SQLite — надёжно. `csv.DictWriter` и `sqlite3` с плейсхолдерами `?` — фундамент хранения. Очистка и дедупликация — то, что отличает «просто собрал» от «собрал качественно». Финальный проект модуля!

<!--TASK-->
### Задача 1

Напиши программу `csv_basics.py`, которая создаёт список из трёх словарей: `{"city": "Москва", "population": 13000000}`, `{"city": "Санкт-Петербург", "population": 5600000}`, `{"city": "Новосибирск", "population": 1600000}`. Запиши его в файл `cities.csv` через `csv.DictWriter` (с `newline=""` и `encoding="utf-8"`), затем прочитай обратно через `csv.DictReader` и выведи все строки в формате `Город: <city>, Население: <population>`. Проверь, что файл создан, через `Path("cities.csv").exists()`.

### Задача 2

Напиши программу `quotes_csv.py`, которая скачивает страницу 1 сайта `https://quotes.toscrape.com/`, извлекает все цитаты (`div.quote`): текст (`span.text`), автора (`small.author`) и теги (`a.tag`, через запятую). Очисти текст и автора через `strip()`. Сохрани всё в файл `quotes.csv` с колонками `text, author, tags` через `csv.DictWriter`. В конце выведи количество записанных строк.

### Задача 3

Создай базу данных `quotes.db` с таблицей `quotes` (колонки: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `text TEXT NOT NULL`, `author TEXT NOT NULL`, `tags TEXT`, и ограничение `UNIQUE(text, author)`). Напиши программу `quotes_db.py`, которая собирает цитаты с первых трёх страниц `https://quotes.toscrape.com/` и вставляет их через `INSERT OR IGNORE`. После вставки выведи общее число строк в таблице (`SELECT COUNT(*)`) и количество уникальных авторов (`SELECT COUNT(DISTINCT author)`).

### Задача 4

Напиши функцию `pipeline(max_pages=3)`, которая выполняет полный конвейер: сбор цитат со страниц (как в задаче 3), очистку через `strip()`, пропуск пустых текстов (если текст пустой — `continue`) и вставку в SQLite. Функция должна возвращать количество вставленных строк (`cur.rowcount` суммировать по вставкам). Вызови её с `max_pages=3`, выведи результат и убедись, что повторный вызов добавляет 0 новых строк (всё уже есть в базе).

### Задача 5

Объедини CSV и SQLite: собери цитаты со страницы 1 в `quotes.csv` (как в задаче 2), затем прочитай этот CSV через `csv.DictReader` и загрузи содержимое в таблицу `quotes` базы данных `quotes.db` через `INSERT OR IGNORE`. Используй только реальные данные из CSV — никакого дублирования кода сбора. В конце выведи количество строк в базе. Убедись, что повторная загрузка того же CSV не увеличивает число строк.
<!--/TASK-->

<!--HINT-->
### Подсказка 1

`csv.DictWriter(f, fieldnames=["city", "population"])` — порядок колонок задаёт `fieldnames`. Не забудь `writer.writeheader()` перед `writer.writerows(rows)`. Чтение: `csv.DictReader(f)` — строки превращаются в словари по заголовкам.

### Подсказка 2

Теги собирай так: `", ".join(t.get_text() for t in q.select("a.tag"))`. Для записи собери список словарей `{"text": ..., "author": ..., "tags": ...}` и передай в `writer.writerows(rows)`. Количество строк — `len(rows)`.

### Подсказка 3

Обязательно `conn.commit()` после всех вставок и `conn.close()` в конце. Для подсчёта: `cur.execute("SELECT COUNT(*) FROM quotes")` и `cur.fetchone()[0]`. `COUNT(DISTINCT author)` считает уникальных авторов.

### Подсказка 4

`cur.rowcount` после `execute("INSERT OR IGNORE ...")` — сколько строк реально вставлено (0, если строка уже была). Суммируй его по всем цитатам. Повторный вызов покажет 0 — это и есть проверка дедупликации.

### Подсказка 5

Читай CSV: `with open("quotes.csv", encoding="utf-8") as f: rows = list(csv.DictReader(f))`. Затем цикл с `INSERT OR IGNORE` по `rows`. В базе `UNIQUE(text, author)` не даст дубликатам появиться — повторная загрузка не изменит `COUNT(*)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```python
import csv
from pathlib import Path

rows = [
    {"city": "Москва", "population": 13000000},
    {"city": "Санкт-Петербург", "population": 5600000},
    {"city": "Новосибирск", "population": 1600000},
]

with open("cities.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["city", "population"])
    writer.writeheader()
    writer.writerows(rows)

print("Файл создан:", Path("cities.csv").exists())

with open("cities.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"Город: {row['city']}, Население: {row['population']}")
```

Разбор по шагам:

- `open("cities.csv", "w", newline="", encoding="utf-8")` — три важных момента: `"w"` — запись (файл пересоздастся), `newline=""` — без лишних пустых строк (иначе CSV-запись вставит `\r\n` между строками), `encoding="utf-8"` — чтобы кириллица сохранилась корректно.
- `csv.DictWriter` получает `fieldnames` — порядок колонок. `writeheader()` записывает первую строку-заголовок `city,population`.
- `writer.writerows(rows)` записывает все словари: ключи словарей должны совпадать с `fieldnames`.
- `Path("cities.csv").exists()` проверяет создание файла.
- `csv.DictReader(f)` читает файл: первая строка становится заголовками, каждая следующая — словарём. Обращение `row['city']` и `row['population']` — по именам колонок.
- Так работает обмен данными: любой скрипт или таблица Excel откроют `cities.csv`.

### Разбор 2

```python
import csv
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

rows = []
for q in soup.select("div.quote"):
    text = q.select_one("span.text").get_text().strip()
    author = q.select_one("small.author").get_text().strip()
    tags = ", ".join(t.get_text() for t in q.select("a.tag"))
    rows.append({"text": text, "author": author, "tags": tags})

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(rows)

print("Записано цитат:", len(rows))
```

Разбор по шагам:

- `soup.select("div.quote")` — все блоки цитат страницы.
- Для каждой цитаты: текст из `span.text`, автор из `small.author`, теги — список текстов `a.tag`, соединённых запятой через `", ".join(...)`.
- `strip()` убирает лишние пробелы и переводы строк по краям — это стадия очистки. Без неё в CSV попали бы «грязные» строки.
- Список `rows` — чистые словари. `csv.DictWriter` записывает их с заголовками `text,author,tags`.
- `len(rows)` — количество записанных цитат (на странице 1 их 10).
- Модульность: если завтра сайт сменит разметку — поменяется только блок извлечения, а запись в CSV останется.

### Разбор 3

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for q in soup.select("div.quote"):
        text = q.select_one("span.text").get_text().strip()
        author = q.select_one("small.author").get_text().strip()
        tags = ", ".join(t.get_text() for t in q.select("a.tag"))
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (text, author, tags),
        )

conn.commit()

cur.execute("SELECT COUNT(*) FROM quotes")
print("Всего цитат:", cur.fetchone()[0])
cur.execute("SELECT COUNT(DISTINCT author) FROM quotes")
print("Уникальных авторов:", cur.fetchone()[0])
conn.close()
```

Разбор по шагам:

- `sqlite3.connect("quotes.db")` создаёт (или открывает) файл базы данных.
- `CREATE TABLE IF NOT EXISTS` — таблица создастся один раз; при повторном запуске она уже есть. `AUTOINCREMENT` сам назначает `id`.
- `UNIQUE(text, author)` — ограничение: комбинация текст+автор не может повторяться. Это защита от дубликатов на уровне базы.
- `INSERT OR IGNORE` — вставить строку, но если такая уже есть — молча пропустить. Вместе с `UNIQUE` это идеальная дедупликация.
- Плейсхолдеры `?` — значения передаются отдельным кортежем. Никогда не вставляй данные в SQL через f-строки — это опасно.
- `conn.commit()` фиксирует изменения (без него они не сохранятся), `conn.close()` закрывает файл.
- `SELECT COUNT(*)` — число строк, `SELECT COUNT(DISTINCT author)` — уникальные авторы. На трёх страницах будет ~30 цитат и несколько десятков авторов с повторами.

### Разбор 4

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

def pipeline(max_pages=3):
    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT,
            UNIQUE(text, author)
        )
    """)

    inserted = 0
    for page in range(1, max_pages + 1):
        r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        for q in soup.select("div.quote"):
            text = q.select_one("span.text").get_text().strip()
            author = q.select_one("small.author").get_text().strip()
            if not text or not author:
                continue  # пропускаем пустые значения
            tags = ", ".join(t.get_text() for t in q.select("a.tag"))
            cur.execute(
                "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
                (text, author, tags),
            )
            inserted += cur.rowcount

    conn.commit()
    conn.close()
    return inserted

first = pipeline(max_pages=3)
print("Первая вставка:", first, "строк")
second = pipeline(max_pages=3)
print("Повторная вставка:", second, "строк")
```

Разбор по шагам:

- Функция оборачивает весь конвейер: подключение, создание таблицы, сбор, очистку, вставку. Возвращает число реально вставленных строк.
- `if not text or not author: continue` — стадия очистки: пустые значения пропускаются, чтобы не засорять базу.
- `cur.rowcount` после `execute(...)` — количество строк, затронутых операцией. Для `INSERT OR IGNORE` это 1, если строка вставлена, и 0, если она уже была.
- `inserted += cur.rowcount` суммирует реальные вставки.
- Первый вызов вернёт ~30 (все цитаты новые). Второй вызов вернёт 0 — те же цитаты уже есть, и `INSERT OR IGNORE` ничего не добавит. Это наглядная проверка дедупликации.
- Повторный запуск безопасен: таблица уже существует (`IF NOT EXISTS`), данные не дублируются.

### Разбор 5

```python
import csv
import sqlite3
import requests
from bs4 import BeautifulSoup

# Шаг 1: собираем в CSV
r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

rows = []
for q in soup.select("div.quote"):
    text = q.select_one("span.text").get_text().strip()
    author = q.select_one("small.author").get_text().strip()
    tags = ", ".join(t.get_text() for t in q.select("a.tag"))
    rows.append({"text": text, "author": author, "tags": tags})

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(rows)

# Шаг 2: загружаем CSV в SQLite
conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

with open("quotes.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (row["text"], row["author"], row["tags"]),
        )

conn.commit()
cur.execute("SELECT COUNT(*) FROM quotes")
print("Строк в базе:", cur.fetchone()[0])
conn.close()
```

Разбор по шагам:

- Шаг 1 полностью повторяет задачу 2: сбор с сайта и запись в CSV. Файл `quotes.csv` — «промежуточное хранилище».
- Шаг 2 читает CSV через `csv.DictReader` — он сам превращает строки в словари по заголовкам `text,author,tags`.
- Каждая строка CSV вставляется `INSERT OR IGNORE` с плейсхолдерами. `UNIQUE(text, author)` в таблице не даёт появляться дубликатам.
- Повторная загрузка того же CSV не увеличит `COUNT(*)` — все строки уже есть, и `IGNORE` их пропустит.
- Это переход от одноразового скрипта к настоящему конвейеру: источник (сайт) → файл (CSV) → база (SQLite). Каждая стадия отделена, данные на каждом этапе проверяемы — CSV можно открыть и посмотреть глазами, базу — запросить SQL-ом.
- Такой «пиплайн» легко расширять: добавить пагинацию, фильтры, другой формат хранения — не ломая остальные части.
<!--/SOLUTION-->

<!--QUIZ-->
Для чего нужен параметр newline="" при записи CSV?
- Чтобы файл был меньше
- Чтобы не появлялись лишние пустые строки
- Чтобы включить кодировку UTF-8
- Чтобы записать заголовки
* Правильный ответ: Чтобы не появлялись лишние пустые строки
Без newline="" запись CSV вставляет лишние переносы строк.

Что делает INSERT OR IGNORE в SQLite?
- Вставляет строку всегда, даже если есть дубликат
- Пропускает вставку, если строка с такими же уникальными значениями уже есть
- Удаляет старую строку перед вставкой
- Вызывает ошибку при дубликате
* Правильный ответ: Пропускает вставку, если строка с такими же уникальными значениями уже есть
Вместе с UNIQUE это даёт дедупликацию на уровне базы.

Зачем использовать плейсхолдеры ? в SQL-запросах?
- Чтобы ускорить запрос
- Чтобы безопасно подставлять значения, не конструируя SQL-строку вручную
- Чтобы запрос стал короче
- Это требование синтаксиса CREATE TABLE
* Правильный ответ: Чтобы безопасно подставлять значения, не конструируя SQL-строку вручную
Плейсхолдеры защищают от ошибок и опасных значений, а значения передаются отдельным кортежем.

Что делает cur.rowcount после INSERT OR IGNORE?
- Возвращает общее количество строк в таблице
- Возвращает число строк, затронутых операцией (1 или 0)
- Возвращает последний вставленный id
- Возвращает имя таблицы
* Правильный ответ: Возвращает число строк, затронутых операцией (1 или 0)
Для INSERT OR IGNORE это 1, если строка вставлена, и 0, если она уже была.

Какая стадия конвейера убирает лишние пробелы и пустые значения?
- Fetch
- Parse
- Clean
- Store
* Правильный ответ: Clean
Очистка (strip, пропуск пустых) происходит до сохранения.

Почему UNIQUE(text, author) защищает от дубликатов даже при повторном запуске программы?
- Потому что SQLite сам удаляет повторы
- Потому что база не даст вставить строку с уже существующей комбинацией (а INSERT OR IGNORE её пропустит)
- Потому что тексты всегда уникальны
- Это не работает, нужно вручную проверять
* Правильный ответ: Потому что база не даст вставить строку с уже существующей комбинацией (а INSERT OR IGNORE её пропустит)
Ограничение UNIQUE на уровне таблицы гарантирует уникальность независимо от кода.
<!--/QUIZ-->
