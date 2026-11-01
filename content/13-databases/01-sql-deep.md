---
title: SQL глубоко: JOIN, агрегации, подзапросы
summary: Соединяем таблицы (INNER/LEFT JOIN), агрегируем данные (GROUP BY, HAVING) и строим подзапросы и CTE на живых примерах с sqlite3.
order: 1
duration: 45 мин
difficulty: advanced
tags: sql, join, group by, подзапросы, cte, sqlite3
---

## Почему одного SELECT мало

До сих пор мы работали с одной таблицей. Но настоящие базы состоят из десятков связанных таблиц: пользователи, заказы, товары, платежи. Чтобы получить осмысленный ответ, данные приходится соединять. В этом уроке ты научишься:

- соединять таблицы через JOIN разных видов;
- агрегировать строки с COUNT, SUM, AVG, MIN, MAX;
- группировать с GROUP BY и фильтровать группы через HAVING;
- использовать подзапросы и обобщённые табличные выражения (CTE).

Весь код работает с модулем sqlite3 — он встроен в Python, и для него ничего устанавливать не нужно.

## Наша учебная база

Представь интернет-магазин. Создадим две таблицы: `users` и `orders`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL
);
INSERT INTO users (id, name) VALUES
    (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
INSERT INTO orders (id, user_id, amount) VALUES
    (101, 1, 1500), (102, 1, 800),
    (103, 2, 3200), (104, 2, 900);
""")
print("Таблицы созданы")
```

Обрати внимание: у Веры (id=3) заказов нет. Это пригодится для упражнений с LEFT JOIN.

## INNER JOIN: только пересечение

INNER JOIN оставляет только те строки двух таблиц, которые совпали по условию соединения.

```python
cur.execute("""
SELECT users.name, orders.amount
FROM users
JOIN orders ON orders.user_id = users.id
ORDER BY users.name
""")
for name, amount in cur.fetchall():
    print(name, amount)
```

Вывод:

```
Аня 1500.0
Аня 800.0
Борис 3200.0
Борис 900.0
```

Вера пропала — у неё нет ни одного заказа, ей не с чем соединяться.

## LEFT JOIN: сохраняем левую таблицу целиком

LEFT JOIN берёт все строки левой таблицы (`users`), а справа подставляет данные там, где они есть. Где их нет — подставляется NULL.

```python
cur.execute("""
SELECT users.name, COALESCE(SUM(orders.amount), 0) AS total
FROM users
LEFT JOIN orders ON orders.user_id = users.id
GROUP BY users.id
ORDER BY users.name
""")
for name, total in cur.fetchall():
    print(name, total)
```

Вывод:

```
Аня 2300.0
Борис 4100.0
Вера 0.0
```

С COALESCE мы превращаем NULL в 0. Обрати внимание: здесь же появилась агрегация — про неё дальше.

## Агрегатные функции и GROUP BY

Агрегатные функции: COUNT — число строк, SUM — сумма, AVG — среднее, MIN/MAX — минимум/максимум. GROUP BY разбивает строки на группы по значению колонки, а агрегатная функция применяется к каждой группе отдельно.

```python
cur.execute("""
SELECT users.name, COUNT(orders.id) AS cnt, SUM(orders.amount) AS total
FROM users
LEFT JOIN orders ON orders.user_id = users.id
GROUP BY users.id
""")
for name, cnt, total in cur.fetchall():
    print(name, cnt, total)
```

Вывод:

```
Аня 2 2300.0
Борис 2 4100.0
Вера 0 0.0
```

Важно: любая колонка в SELECT, которая не является аргументом агрегатной функции, должна быть перечислена в GROUP BY (или использоваться в составе другой агрегатной функции).

## HAVING: фильтр по группам

WHERE фильтрует строки до группировки. Чтобы отфильтровать уже получившиеся группы, используют HAVING.

```python
cur.execute("""
SELECT users.name, SUM(orders.amount) AS total
FROM users
JOIN orders ON orders.user_id = users.id
GROUP BY users.id
HAVING SUM(orders.amount) > 2000
""")
for name, total in cur.fetchall():
    print(name, total)
```

Вывод:

```
Аня 2300.0
Борис 4100.0
```

## Подзапросы

Подзапрос — это запрос внутри другого запроса. Он может стоять в WHERE, FROM, SELECT или HAVING. Распространённый паттерн — IN с подзапросом:

```python
cur.execute("""
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE amount >= 2000
)
""")
for (name,) in cur.fetchall():
    print(name)
```

Вывод:

```
Борис
```

Коррелированный подзапрос ссылается на внешний запрос. Например, найдём для каждого пользователя его максимальный заказ:

```python
cur.execute("""
SELECT users.name,
       (SELECT MAX(o.amount) FROM orders o
        WHERE o.user_id = users.id) AS best
FROM users
""")
for name, best in cur.fetchall():
    print(name, best)
```

Вывод:

```
Аня 1500.0
Борис 3200.0
Вера None
```

## CTE: WITH

Обобщённое табличное выражение (CTE) делает сложный запрос читаемым: сначала описываешь «временную таблицу», а потом используешь её в основном запросе.

```python
cur.execute("""
WITH totals AS (
    SELECT user_id, SUM(amount) AS total
    FROM orders
    GROUP BY user_id
)
SELECT users.name, totals.total
FROM users
JOIN totals ON totals.user_id = users.id
ORDER BY totals.total DESC
""")
for name, total in cur.fetchall():
    print(name, total)
```

Вывод:

```
Борис 4100.0
Аня 2300.0
```

## Итог

Теперь ты умеешь соединять таблицы, агрегировать данные, группировать, фильтровать группы и строить подзапросы. Эти навыки — фундамент любого серьёзного SQL: от отчётов до аналитики. Закрепим практикой.

<!--TASK-->
### Задача 1
Напиши функцию `top_spenders()`, которая подключается к базе в памяти, создаёт таблицы `users` и `orders` ровно с теми же данными, что в уроке (Аня — 1500 и 800, Борис — 3200 и 900, Вера — без заказов), и возвращает список кортежей `(name, total)` для пользователей, у которых есть хотя бы один заказ. Сумма — через SUM, сортировка — по убыванию суммы. Выведи список на экран. Ожидаемый вывод: `[('Борис', 4100.0), ('Аня', 2300.0)]`.

### Задача 2
Напиши функцию `left_join_report()`, которая использует ту же схему и возвращает список кортежей `(name, total)` для всех пользователей, включая тех, у кого заказов нет — им нужно поставить 0 (используй COALESCE). Сортировка — по имени по алфавиту. Выведи список. Ожидаемый вывод: `[('Аня', 2300.0), ('Борис', 4100.0), ('Вера', 0.0)]`.

### Задача 3
Напиши функцию `heavy_users(threshold)`, которая возвращает только тех пользователей, чья суммарная сумма заказов строго больше `threshold`. Используй GROUP BY вместе с HAVING. Для `threshold=2000` ожидаемый вывод: `[('Аня', 2300.0), ('Борис', 4100.0)]`. Для `threshold=3000` ожидаемый вывод: `[('Борис', 4100.0)]`.

### Задача 4
Напиши функцию `who_ordered_over(min_amount)`, которая через подзапрос с IN возвращает имена пользователей, у которых есть хотя бы один заказ на сумму не меньше `min_amount`. Результат отсортируй по алфавиту. Для `min_amount=2000` ожидаемый вывод: `['Борис']` (только у Бориса есть заказ на 3200). Для `min_amount=800` ожидаемый вывод: `['Аня', 'Борис']`.

### Задача 5
Напиши функцию `best_order_each()`, которая для каждого пользователя с заказами вычисляет сумму его самого дорогого заказа. Сделай это с помощью коррелированного подзапроса (или CTE с оконной функцией ROW_NUMBER). Верни список кортежей `(name, best)` в порядке имён. Ожидаемый вывод: `[('Аня', 1500.0), ('Борис', 3200.0)]`. Вера в списке отсутствует — у неё нет заказов.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Функция должна сама создать базу и заполнить её: выполни `CREATE TABLE` и `INSERT` из урока, затем `conn.commit()`. Для суммы используй `SUM(orders.amount)`, для соединения — `JOIN orders ON orders.user_id = users.id`, группировку — `GROUP BY users.id`. Сортировку по убыванию сделай через `ORDER BY total DESC`.

### Подсказка 2
Отличие от задачи 1 — тип соединения: возьми `LEFT JOIN`. Вера попадёт в результат с NULL-суммой, поэтому оберни SUM в `COALESCE(SUM(orders.amount), 0)`. Сортировка по имени: `ORDER BY users.name`. Проверь, что в SELECT все неагрегатные колонки перечислены в GROUP BY.

### Подсказка 3
Сначала собери запрос с JOIN, GROUP BY и `SUM(orders.amount)`, а затем добавь `HAVING SUM(orders.amount) > ?` с параметром `threshold`. Помни: WHERE сюда не подойдёт, потому что он фильтрует строки до группировки, а нам нужно отфильтровать группы.

### Подсказка 4
Подзапрос в скобках должен возвращать `user_id` из таблицы orders, где `amount >= ?`. Внешний запрос: `SELECT name FROM users WHERE id IN (...) ORDER BY name`. Передай `min_amount` как параметр через кортеж.

### Подсказка 5
Коррелированный вариант: `SELECT users.name, (SELECT MAX(o.amount) FROM orders o WHERE o.user_id = users.id) AS best FROM users` — добавь условие, чтобы не выводить пользователей без заказов (например, `WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = users.id)`). В варианте с CTE: `WITH ranked AS (SELECT user_id, amount, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn FROM orders) SELECT users.name, ranked.amount FROM users JOIN ranked ON ranked.user_id = users.id WHERE ranked.rn = 1 ORDER BY users.name`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sqlite3

def top_spenders():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, SUM(orders.amount) AS total
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY total DESC
    """)
    return cur.fetchall()

print(top_spenders())
```

Результат:

```
[('Борис', 4100.0), ('Аня', 2300.0)]
```

Что здесь происходит? INNER JOIN соединяет строки users и orders по совпадению `orders.user_id = users.id`. Так как у Веры заказов нет, её строки в соединении просто не появляются — это и отличает INNER JOIN от LEFT JOIN. GROUP BY users.id собирает заказы каждого пользователя в одну группу, а SUM суммирует их суммы. ORDER BY total DESC сортирует группы от большей суммы к меньшей. Заметь: `total` — это псевдоним (alias) для выражения, его можно использовать в ORDER BY. Ожидаемый итог: Борис с 4100 впереди, Аня следом.

### Разбор 2
Решение:

```python
import sqlite3

def left_join_report():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, COALESCE(SUM(orders.amount), 0) AS total
    FROM users
    LEFT JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY users.name
    """)
    return cur.fetchall()

print(left_join_report())
```

Результат:

```
[('Аня', 2300.0), ('Борис', 4100.0), ('Вера', 0.0)]
```

Что здесь происходит? LEFT JOIN гарантирует, что все строки левой таблицы users попадут в результат. Для Веры нет ни одного заказа, поэтому значения из orders становятся NULL: SUM(NULL) даёт NULL, и именно для этого случая нужен COALESCE(..., 0) — он заменяет NULL на 0. Так отчёт показывает всех пользователей, даже тех, кто ничего не заказывал. Сортировка по имени даёт порядок Аня → Борис → Вера. Запомни различия: INNER JOIN — только совпадения, LEFT JOIN — вся левая таблица плюс совпадения справа.

### Разбор 3
Решение:

```python
import sqlite3

def heavy_users(threshold):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, SUM(orders.amount) AS total
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    HAVING SUM(orders.amount) > ?
    """, (threshold,))
    return cur.fetchall()

print(heavy_users(2000))
print(heavy_users(3000))
```

Результат:

```
[('Аня', 2300.0), ('Борис', 4100.0)]
[('Борис', 4100.0)]
```

Что здесь происходит? Порядок выполнения SQL: сначала FROM/JOIN собирают строки, WHERE (если есть) их фильтрует, GROUP BY группирует, затем применяются агрегатные функции, и только после этого HAVING отсеивает группы, не прошедшие условие. Поэтому `HAVING SUM(orders.amount) > ?` видит уже посчитанные суммы групп. При пороге 2000 проходят Аня (2300) и Борис (4100); при пороге 3000 — только Борис. Хороший практичный приём: порог передаётся параметром, а не вшивается в строку запроса.

### Разбор 4
Решение:

```python
import sqlite3

def who_ordered_over(min_amount):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT name FROM users
    WHERE id IN (
        SELECT user_id FROM orders
        WHERE amount >= ?
    )
    ORDER BY name
    """, (min_amount,))
    return [row[0] for row in cur.fetchall()]

print(who_ordered_over(2000))
print(who_ordered_over(800))
```

Результат:

```
['Борис']
['Аня', 'Борис']
```

Что здесь происходит? Внутренний запрос возвращает множество `user_id` тех заказов, чья сумма не меньше min_amount. Внешний запрос берёт пользователей, чей id попал в это множество. Для порога 2000 единственный подходящий заказ — 3200 у Бориса. Для 800 подходят заказы 1500 (Аня), 3200 и 900 (Борис) — но не 800 у Ани, потому что условие `amount >= 800` — стоп, 800 >= 800 истинно, значит заказ на 800 тоже подходит, и Аня есть в обоих списках. Обрати внимание: подзапрос выполняется один раз, IN не превращается в цикл — это не коррелированный подзапрос, а обычный, независимый.

### Разбор 5
Решение через коррелированный подзапрос:

```python
import sqlite3

def best_order_each():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Аня'), (2, 'Борис'), (3, 'Вера');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name,
           (SELECT MAX(o.amount) FROM orders o
            WHERE o.user_id = users.id) AS best
    FROM users
    WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = users.id)
    ORDER BY users.name
    """)
    return cur.fetchall()

print(best_order_each())
```

Результат:

```
[('Аня', 1500.0), ('Борис', 3200.0)]
```

Что здесь происходит? Подзапрос в SELECT — коррелированный: для каждой строки users он пересчитывается и ссылается на `users.id` внешнего запроса. Он выбирает максимум суммы заказов именно этого пользователя. Условие EXISTS отсеивает пользователей без заказов — иначе Вера попала бы в результат с NULL. Альтернатива через CTE и оконную функцию: `WITH ranked AS (SELECT user_id, amount, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn FROM orders) SELECT users.name, ranked.amount FROM users JOIN ranked ON ranked.user_id = users.id WHERE ranked.rn = 1 ORDER BY users.name` — тот же результат, но без повторного выполнения подзапроса для каждой строки.
<!--/SOLUTION-->

<!--QUIZ-->
Что вернёт INNER JOIN для пользователя, у которого нет ни одной записи в правой таблице?
- Строку с NULL-значениями справа
- Ничего: этот пользователь не попадёт в результат
- Ошибку соединения
- Отдельную строку с пустыми значениями
* Правильный ответ: Ничего: этот пользователь не попадёт в результат
INNER JOIN оставляет только совпавшие пары строк; пользователь без заказов просто отсутствует в результате.

Чем LEFT JOIN отличается от INNER JOIN?
- LEFT JOIN работает только с одной таблицей
- LEFT JOIN сохраняет все строки левой таблицы, подставляя NULL там, где нет совпадений
- INNER JOIN работает быстрее всегда
- LEFT JOIN не поддерживает GROUP BY
* Правильный ответ: LEFT JOIN сохраняет все строки левой таблицы, подставляя NULL там, где нет совпадений
LEFT JOIN включает в результат все строки левой таблицы, даже если справа нет совпадений — вместо данных подставляется NULL.

Почему сумму по группам нельзя отфильтровать через WHERE?
- WHERE не умеет работать с SUM
- WHERE выполняется до GROUP BY и не видит агрегатные результаты
- WHERE выполняется после GROUP BY, но только для одной группы
- WHERE запрещён в запросах с JOIN
* Правильный ответ: WHERE выполняется до GROUP BY и не видит агрегатные результаты
WHERE фильтрует сырые строки до группировки; результаты агрегатных функций доступны только в HAVING.

Что вернёт подзапрос `(SELECT MAX(amount) FROM orders WHERE user_id = users.id)` внутри SELECT?
- Число заказов пользователя
- Максимальную сумму заказа для каждой строки внешнего запроса
- Список всех сумм
- Первый заказ пользователя
* Правильный ответ: Максимальную сумму заказа для каждой строки внешнего запроса
Это коррелированный подзапрос: он вычисляется для каждой строки внешнего запроса и возвращает максимальную сумму заказа этого пользователя.

Что такое CTE (WITH)?
- Временная именованная таблица внутри запроса, делающая его читаемым
- Тип индекса
- Способ объединения двух баз
- Команда для перезапуска сервера
* Правильный ответ: Временная именованная таблица внутри запроса, делающая его читаемым
CTE объявляется через WITH и используется дальше как обычная таблица, упрощая сложные запросы.

Где выполняется HAVING относительно GROUP BY?
- До GROUP BY
- После GROUP BY
- Вместо GROUP BY
- HAVING не связан с GROUP BY
* Правильный ответ: После GROUP BY
Сначала строки группируются, затем вычисляются агрегатные функции, и только после этого HAVING отсеивает группы.

Какая агрегатная функция считает количество строк или ненулевых значений?
- COUNT
- SUM
- AVG
* Правильный ответ: COUNT
COUNT(*) считает строки, COUNT(колонка) — только ненулевые значения.

Что делает COALESCE(x, 0)?
- Возвращает x, если он не NULL, иначе 0
- Складывает x и 0
- Проверяет, что x больше нуля
* Правильный ответ: Возвращает x, если он не NULL, иначе 0
COALESCE заменяет NULL первым ненулевым значением из списка аргументов.
<!--/QUIZ-->
