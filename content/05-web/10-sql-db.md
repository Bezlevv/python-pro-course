---
title: SQL и базы данных
summary: Основы реляционных баз данных, язык SQL и работа с SQLite из Python через модуль sqlite3.
order: 10
duration: 40 мин
difficulty: advanced
---

Сайты и приложения хранят данные в базах данных. В этом уроке мы освоим основы языка SQL на примере SQLite — самой популярной встроенной базы, которая уже есть в Python. Этот урок свяжет всё, что было раньше: любые фреймворки (Django, FastAPI) в итоге говорят с базой на SQL.

## Что такое реляционная база данных

Можно представить базу как набор Excel-таблиц. Каждая таблица — это сущность (книги, пользователи, заказы), строки — записи, столбцы — свойства. Столбец с уникальным номером каждой записи называют первичным ключом (PRIMARY KEY).

## SQLite и модуль sqlite3

SQLite хранит всю базу в одном файле. Модуль `sqlite3` входит в стандартную библиотеку Python — ничего устанавливать не нужно. Подключение:

```python
import sqlite3

conn = sqlite3.connect("books.db")   # создаст файл books.db
cursor = conn.cursor()
```

`connect` создаёт соединение с файлом, `cursor` — объект для выполнения запросов.

## Создание таблицы

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        year INTEGER
    )
""")
conn.commit()
```

Здесь `id` — первичный ключ, `title` — обязательная строка (NOT NULL), `year` — целое число.

## Добавление данных

INSERT — запрос на вставку:

```python
cursor.execute(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    ("Война и мир", "Лев Толстой", 1869),
)
conn.commit()
```

Обрати внимание на знаки вопроса: вместо того чтобы подставлять значения в строку напрямую, мы передаём их вторым аргументом. Это защита от SQL-инъекций — никогда не собирай запрос через f-строки!

## Чтение данных

SELECT позволяет выбирать данные:

```python
cursor.execute("SELECT title, year FROM books ORDER BY year DESC")
rows = cursor.fetchall()
for title, year in rows:
    print(title, year)
```

`fetchall()` возвращает список кортежей. Есть также `fetchone()` (первая строка) и `fetchmany(n)`.

Фильтрация:

```python
cursor.execute("SELECT * FROM books WHERE year > 1950 AND author LIKE '%Толстой%'")
```

## Изменение и удаление

```python
cursor.execute("UPDATE books SET year = 1869 WHERE title = 'Война и мир'")
cursor.execute("DELETE FROM books WHERE year < 1800")
conn.commit()
```

## Транзакции

Изменения не применяются, пока не вызван `commit()`. Если что-то пошло не так, `rollback()` откатит всё. Удобно пользоваться контекстным менеджером — он сам закоммитит изменения или откатит при ошибке:

```python
with sqlite3.connect("books.db") as conn:
    conn.execute(
        "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
        ("1984", "Дж. Оруэлл", 1949),
    )
```

## Полный пример

Соберём всё вместе — скрипт, который создаёт таблицу, наполняет её и выводит результат:

```python
import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)")
books = [("Война и мир", 1869), ("1984", 1949), ("Мастер и Маргарита", 1967)]
cur.executemany("INSERT INTO books (title, year) VALUES (?, ?)", books)
conn.commit()
cur.execute("SELECT title, year FROM books ORDER BY year")
for title, year in cur.fetchall():
    print(f"{year}: {title}")
conn.close()
```

Это программа, которую можно запустить как есть: `python books_db.py`.

## Итог урока

Мы узнали:

- что такое таблицы, строки и первичный ключ;
- как подключиться к SQLite из Python;
- как создавать таблицы, добавлять, читать, обновлять и удалять данные;
- почему важно использовать параметризованные запросы;
- как работают транзакции и commit.

Теперь закрепим всё практикой.

<!--TASK-->
### Задача 1
Напиши скрипт `library_db.py`, который: 1) создаёт таблицу `books` (id, title, author, year), 2) добавляет в неё не менее четырёх книг разных годов через `executemany`, 3) выбирает книги, изданные после 2000 года, отсортированные по году, и выводит их в формате `Год — Название`, 4) выводит средний год издания всех книг (SQL-функция `AVG`). Запусти скрипт и убедись, что на экране появились только книги новее 2000 года и среднее арифметическое годов. Опиши ожидаемый вывод.

### Задача 2
Создай скрипт `first_books.py`. В начале скрипта удаляй старую таблицу через `DROP TABLE IF EXISTS books` (чтобы повторные запуски давали одинаковый вывод), затем создавай её заново и наполняй четырьмя книгами разных годов через `executemany`. После этого выполни запрос `SELECT title, year FROM books ORDER BY year`: 1) выведи самую старую книгу через `fetchone()`, 2) выведи следующие две книги через `fetchmany(2)`. Формат вывода — `Год: Название`. Запусти скрипт два раза подряд и убедись, что вывод одинаковый. Опиши ожидаемый вывод.

### Задача 3
Создай скрипт `update_delete.py`. Создай таблицу `books` и наполни её пятью книгами: «Дюна» (1965), «1984» (1949), «Мастер и Маргарита» (1967), «Мёртвые души» (1842), «Щегол» (2013). Затем: 1) исправь год «1984» на 1950 через `UPDATE`, 2) удали все книги старше 1900 года через `DELETE`, 3) выведи оставшиеся книги в формате `Год — Название` и их количество через `SELECT COUNT(*)`. Запусти скрипт и опиши ожидаемый вывод: какие книги остались и сколько их.

### Задача 4
Создай скрипт `search_books.py`. Напиши функцию `search(pattern)`, которая принимает строку и возвращает список книг (title, year), где `title` содержит эту подстроку (оператор `LIKE` с параметром). Вызови её с `"война"` и с `"ма"`. Выведи результаты в формате `Год — Название`. В комментарии к коду объясни, почему вместо конкатенации строк используется параметр (`?`) и что случится, если собрать запрос через f-строку на основе ввода пользователя. Запусти скрипт и опиши ожидаемый вывод.

### Задача 5
Создай скрипт `transactions.py`. В начале удали файл базы `transactions.db`, если он существует, чтобы счётчик был предсказуем. Открой два независимых соединения с этой базой: `conn1` и `conn2`. Через `conn1` создай таблицу и вставь две книги (`INSERT`), но НЕ вызывай `commit()`. Через `conn2` посчитай количество книг (`SELECT COUNT(*)`) и выведи его. Затем вызови `conn1.commit()` и снова посчитай через `conn2`. Выведи оба числа с подписями «до commit» и «после commit». Запусти скрипт и опиши ожидаемый вывод — почему числа отличаются.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Используй `WHERE year > 2000` и `ORDER BY year`. Средний год считается так: `SELECT AVG(year) FROM books` — функция вернёт число с плавающей точкой, округли его через `round()`. Не забудь `conn.commit()` после добавления и `conn.close()` в конце.

### Подсказка 2
`DROP TABLE IF EXISTS books` удаляет таблицу только если она существует — так скрипт можно запускать многократно. После `execute()` курсор умеет `fetchone()` (первая строка) и `fetchmany(n)` (n строк). Держи `SELECT` с `ORDER BY year`, чтобы порядок строк был предсказуем.

### Подсказка 3
`UPDATE`: `UPDATE books SET year = ? WHERE title = ?` — не забудь передать значения параметрами. `DELETE`: `DELETE FROM books WHERE year < 1900`. После обоих изменений вызывай `conn.commit()`. Для количества используй `SELECT COUNT(*) FROM books` и `fetchone()[0]`.

### Подсказка 4
`LIKE` с параметром: `WHERE title LIKE ?`, а в аргументах передавай `f"%{pattern}%"` (или `"%" + pattern + "%"`). `%` — маска «любая последовательность символов». Без параметризации злоумышленник мог бы подставить `' OR '1'='1` и получить все записи — это SQL-инъекция.

### Подсказка 5
Изменения одного соединения не видны другим до `commit()`. Поэтому «до commit» в `conn2` должно быть 0, а «после commit» — 2. Закрывай оба соединения через `conn.close()`. Если хочешь увидеть откат — добавь `conn1.rollback()` и проверь, что вставка не сохранилась.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полный код `library_db.py`:

```python
import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        year INTEGER
    )
""")

books = [
    ("Дюна", "Фрэнк Герберт", 1965),
    ("Мастер и Маргарита", "Михаил Булгаков", 1967),
    ("Хроники Нарнии", "Клайв Льюис", 1950),
    ("Солярис", "Станислав Лем", 1961),
    ("Щегол", "Донна Тартт", 2013),
]
cur.executemany(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    books,
)
conn.commit()

print("Книги после 2000 года:")
cur.execute("SELECT year, title FROM books WHERE year > 2000 ORDER BY year")
for year, title in cur.fetchall():
    print(f"{year} — {title}")

cur.execute("SELECT AVG(year) FROM books")
avg_year = cur.fetchone()[0]
print(f"Средний год издания: {round(avg_year)}")

conn.close()
```

Запуск и ожидаемый вывод:

```bash
python library_db.py
```

```
Книги после 2000 года:
2013 — Щегол
Средний год издания: 1971
```

Разбор: `CREATE TABLE IF NOT EXISTS` создаёт таблицу только если её ещё нет. `executemany` за один вызов вставляет список кортежей. В `WHERE year > 2000` остаётся только книга 2013 года. `AVG(year)` возвращает среднее по всем строкам: (1965+1967+1950+1961+2013)/5 = 1971,2, округлённое до 1971. Параметризация `?` защищает данные от SQL-инъекций. Именно через такие запросы Django ORM «разговаривает» с базой внутри.

### Разбор 2
Полный код `first_books.py`:

```python
import sqlite3

conn = sqlite3.connect("first.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")
cur.execute("""
    CREATE TABLE books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year INTEGER
    )
""")

books = [("Дюна", 1965), ("1984", 1949), ("Мастер и Маргарита", 1967), ("Солярис", 1961)]
cur.executemany("INSERT INTO books (title, year) VALUES (?, ?)", books)
conn.commit()

cur.execute("SELECT title, year FROM books ORDER BY year")
first = cur.fetchone()
print(f"{first[1]}: {first[0]}")

next_two = cur.fetchmany(2)
for title, year in next_two:
    print(f"{year}: {title}")

conn.close()
```

Ожидаемый вывод:

```
1949: 1984
1961: Солярис
1965: Дюна
```

Разбор: `DROP TABLE IF EXISTS` гарантирует чистый старт: даже если скрипт запускался раньше, таблица пересоздаётся, и дубликатов не появится. `ORDER BY year` упорядочивает книги по возрастанию года. `fetchone()` берёт первую строку результирующего набора — самую старую книгу (1984). Важно: `fetchmany(2)` продолжает чтение с того места, где остановился `fetchone()`, — поэтому мы получаем следующие две книги (Солярис, Дюна). Курсор «помнит» позицию, пока не выполнен новый запрос или не закрыто соединение.

### Разбор 3
Полный код `update_delete.py`:

```python
import sqlite3

conn = sqlite3.connect("update.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")
cur.execute("CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER)")

books = [
    ("Дюна", 1965),
    ("1984", 1949),
    ("Мастер и Маргарита", 1967),
    ("Мёртвые души", 1842),
    ("Щегол", 2013),
]
cur.executemany("INSERT INTO books (title, year) VALUES (?, ?)", books)

cur.execute("UPDATE books SET year = ? WHERE title = ?", (1950, "1984"))
cur.execute("DELETE FROM books WHERE year < 1900")
conn.commit()

cur.execute("SELECT title, year FROM books ORDER BY year")
for title, year in cur.fetchall():
    print(f"{year} — {title}")

cur.execute("SELECT COUNT(*) FROM books")
print(f"Осталось книг: {cur.fetchone()[0]}")

conn.close()
```

Ожидаемый вывод:

```
1950 — 1984
1965 — Дюна
1967 — Мастер и Маргарита
2013 — Щегол
Осталось книг: 4
```

Разбор: `UPDATE` меняет год книги «1984» с 1949 на 1950 — условие `WHERE title = ?` уточняет, какую строку трогать, а параметры снова защищают от инъекций. Затем `DELETE FROM books WHERE year < 1900` удаляет только «Мёртвые души» (1842), так как остальные книги новее. Оба изменения фиксируются одним `commit()`. Финальный `SELECT` показывает, что в таблице осталось четыре книги, а `COUNT(*)` подтверждает число. Порядок операций важен: сначала `UPDATE`, потом `DELETE`, чтобы не потерять данные.

### Разбор 4
Полный код `search_books.py`:

```python
import sqlite3

conn = sqlite3.connect("search.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")
cur.execute("CREATE TABLE books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER)")
books = [("Война и мир", 1869), ("Мастер и Маргарита", 1967), ("Солярис", 1961), ("Маленькие женщины", 1868)]
cur.executemany("INSERT INTO books (title, year) VALUES (?, ?)", books)
conn.commit()

def search(pattern):
    # Используем параметр вместо конкатенации,
    # чтобы ввод пользователя не мог изменить сам SQL-запрос.
    cur.execute("SELECT title, year FROM books WHERE title LIKE ?", (f"%{pattern}%",))
    return cur.fetchall()

for pattern in ("война", "ма"):
    print(f"Поиск: {pattern}")
    for title, year in search(pattern):
        print(f"{year} — {title}")
    print()

conn.close()
```

Ожидаемый вывод:

```
Поиск: война
1869 — Война и мир

Поиск: ма
1967 — Мастер и Маргарита
1868 — Маленькие женщины
```

Разбор: функция `search` принимает подстроку и подставляет её в `LIKE`-шаблон: `%` вокруг паттерна означает «любая последовательность символов до и после». Параметр передаётся вторым аргументом `execute` — именно так SQLite получает значение отдельно от текста запроса. Если бы мы собрали запрос через f-строку (`f"... WHERE title LIKE '%{pattern}%'"`), пользовательский ввод с кавычками и `OR` мог бы изменить логику запроса — это классическая SQL-инъекция. Параметризация полностью исключает такую возможность, поэтому это обязательное правило для любого кода, работающего с базами.

### Разбор 5
Полный код `transactions.py`:

```python
import os
import sqlite3

if os.path.exists("transactions.db"):
    os.remove("transactions.db")

conn1 = sqlite3.connect("transactions.db")
conn2 = sqlite3.connect("transactions.db")

conn1.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)")
conn1.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("Дюна", 1965))
conn1.execute("INSERT INTO books (title, year) VALUES (?, ?)", ("1984", 1949))
# commit() НЕ вызываем

count_before = conn2.execute("SELECT COUNT(*) FROM books").fetchone()[0]
print(f"до commit: {count_before}")

conn1.commit()

count_after = conn2.execute("SELECT COUNT(*) FROM books").fetchone()[0]
print(f"после commit: {count_after}")

conn1.close()
conn2.close()
```

Ожидаемый вывод:

```
до commit: 0
после commit: 2
```

Разбор: у нас два независимых соединения с одним файлом базы. Вставки в `conn1` не подтверждены `commit()`, поэтому они ещё не «видны» другим соединениям: `conn2` в первом запросе видит 0 книг. После `conn1.commit()` изменения фиксируются, и `conn2` уже видит 2 строки. Так работает транзакционность: незакоммиченные изменения изолированы, а `rollback()` мог бы их отменить. Именно поэтому в веб-приложениях каждое изменение данных обязательно завершается `commit()` — иначе пользователь, подключённый другим соединением, не увидит новых записей.
<!--/SOLUTION-->

<!--QUIZ-->
Какой модуль Python предоставляет работу с SQLite?
- MySQLdb
- sqlite3
- pymongo
- psycopg2
* Правильный ответ: sqlite3
sqlite3 входит в стандартную библиотеку, поэтому ничего устанавливать не нужно.

Зачем в INSERT используются знаки вопроса (?)
- Это сокращение SQL
- Чтобы передать значения параметрами и защититься от SQL-инъекций
- Так запросы работают быстрее
- Чтобы запретить пустые значения
* Правильный ответ: Чтобы передать значения параметрами и защититься от SQL-инъекций
Значения передаются отдельно от текста запроса, поэтому злоумышленник не сможет изменить сам запрос.

Что делает conn.commit()?
- Закрывает соединение
- Сохраняет (фиксирует) все незафиксированные изменения
- Отменяет изменения
- Создаёт таблицу
* Правильный ответ: Сохраняет (фиксирует) все незафиксированные изменения
До commit() изменения живут только в рамках соединения; commit() применяет их к базе.

Какая команда SQL выбирает данные?
- SELECT
- INSERT
- UPDATE
- DELETE
* Правильный ответ: SELECT
INSERT добавляет строки, UPDATE меняет их, DELETE удаляет — а SELECT выбирает данные для чтения.

Что возвращает fetchall()?
- Первую строку результата
- Все строки результата в виде списка кортежей
- Число затронутых строк
- Объект курсора
* Правильный ответ: Все строки результата в виде списка кортежей
fetchall() возвращает список кортежей; fetchone() — одну строку, а fetchmany(n) — n строк.

Какой оператор SQL отбирает строки по условию?
- ORDER BY
- WHERE
- SELECT DISTINCT
- LIMIT
* Правильный ответ: WHERE
WHERE фильтрует строки до выборки: SELECT * FROM books WHERE year > 1950.

Что делает метод rollback()?
- Сохраняет изменения
- Отменяет все незафиксированные изменения транзакции
- Закрывает соединение
- Создаёт таблицу
* Правильный ответ: Отменяет все незафиксированные изменения транзакции
rollback() откатывает изменения, которые ещё не подтверждены commit(), возвращая базу к прежнему состоянию.

Для чего нужен первичный ключ (PRIMARY KEY)?
- Чтобы ускорить вывод
- Чтобы уникально идентифицировать каждую запись таблицы
- Чтобы хранить большие тексты
- Чтобы связать две таблицы автоматически
* Правильный ответ: Чтобы уникально идентифицировать каждую запись таблицы
Первичный ключ гарантирует уникальность строки и позволяет быстро находить её по id.
<!--/QUIZ-->
