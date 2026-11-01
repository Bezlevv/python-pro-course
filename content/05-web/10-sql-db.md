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
**Задача.** Напиши скрипт `library_db.py`, который: 1) создаёт таблицу `books` (id, title, author, year), 2) добавляет в неё не менее четырёх книг разных годов через `executemany`, 3) выбирает книги, изданные после 2000 года, отсортированные по году, и выводит их в формате `Год — Название`, 4) выводит средний год издания всех книг (SQL-функция `AVG`). Запусти скрипт и убедись, что на экране появились только книги новее 2000 года и среднее арифметическое годов. Опиши ожидаемый вывод.
<!--/TASK-->

<!--HINT-->
Используй `WHERE year > 2000` и `ORDER BY year`. Средний год считается так: `SELECT AVG(year) FROM books` — функция вернёт число с плавающей точкой, округли его через `round()`. Не забудь `conn.commit()` после добавления и `conn.close()` в конце.
<!--/HINT-->

<!--SOLUTION-->
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
<!--/SOLUTION-->
