---
title: Нормализация и индексы
summary: Приводим схему базы к нормальным формам (1НФ–3НФ) и ускоряем запросы индексами: CREATE INDEX, уникальные и составные индексы, EXPLAIN QUERY PLAN.
order: 2
duration: 45 мин
difficulty: advanced
tags: нормализация, нф, индексы, explain, производительность
---

## Зачем нормализация

Нормализация — это процесс организации таблиц для уменьшения избыточности и аномалий. Представь таблицу заказов, где имя клиента хранится прямо в строке заказа:

| order_id | client_name | client_phone | product |
|---|---|---|---|
| 1 | Аня | +7-111 | Клавиатура |
| 2 | Аня | +7-111 | Мышь |

Если Аня сменит телефон — придётся обновлять несколько строк: это аномалия обновления. Если она отменит все заказы, мы потеряем информацию о клиенте: аномалия удаления. Если нужно добавить клиента без заказов — придётся вставлять строку с пустым заказом: аномалия вставки. Нормализация распределяет данные по таблицам так, чтобы каждая сущность хранилась в одном месте и менялась один раз.

## Первая нормальная форма (1НФ)

Таблица в 1НФ, если значения во всех ячейках атомарные (нельзя хранить список через запятую) и у таблицы есть первичный ключ. Вот нарушение:

```sql
CREATE TABLE bad_orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    items TEXT  -- 'клавиатура,мышь' — не атомарно!
);
```

## Вторая нормальная форма (2НФ)

2НФ требует 1НФ и отсутствия частичных зависимостей: каждая непервичная колонка должна зависеть от всего составного ключа целиком, а не от его части.

```sql
CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

Здесь price зависит от пары (order_id, product_id) — от обеих частей ключа. Если бы мы добавили `user_name`, который зависит только от `order_id`, это нарушило бы 2НФ: имя клиента дублировалось бы в каждой строке с одним заказом.

## Третья нормальная форма (3НФ)

3НФ требует 2НФ и отсутствия транзитивных зависимостей: непервичные колонки не должны зависеть друг от друга через третью. Например, город зависит от почтового индекса, а индекс — от адреса:

```sql
-- Плохо: country зависит от city, а city — от address
CREATE TABLE customers_bad (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city TEXT,
    country TEXT
);

-- Хорошо: city и country вынесены в справочник
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    country TEXT
);
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city_id INTEGER REFERENCES cities(id)
);
```

Если страна сменит название, в схеме «плохо» пришлось бы обновлять каждую запись клиента; в схеме «хорошо» — одну строку справочника.

## Нормализация — не догма

После 3НФ существуют BCNF, 4НФ, 5НФ, но на практике стремление к 3НФ — золотая середина. Иногда схему сознательно денормализуют: добавляют избыточную колонку, чтобы ускорить частые чтения (например, заранее посчитанную сумму заказов в профиле пользователя). Главное — делать это осознанно, с комментарием в коде и пониманием, какую аномалию ты вносишь.

## Индексы

Индекс — это структура (обычно B-дерево), которая позволяет находить строки по колонке без полного сканирования таблицы. Без индекса СУБД просматривает все строки: в таблице из 100 000 строк — 100 000 сравнений. С индексом — десятки шагов.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT,
    price REAL
);
""")
cur.executemany(
    "INSERT INTO products (id, sku, price) VALUES (?, ?, ?)",
    [(i, f"SKU-{i}", i * 10) for i in range(200_000)],
)
conn.commit()

cur.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE sku = 'SKU-199999'")
print("До индекса:", cur.fetchall())

cur.execute("CREATE INDEX idx_products_sku ON products(sku)")
cur.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE sku = 'SKU-199999'")
print("После индекса:", cur.fetchall())
```

До индекса план — `SCAN products` (полное сканирование), после — `SEARCH products USING INDEX` (поиск по индексу).

## Виды индексов

- Уникальный: `CREATE UNIQUE INDEX ...` — не даёт вставить дубликат.
- Составной: `CREATE INDEX idx ON orders(user_id, status)` — полезен для запросов с WHERE по обеим колонкам.
- Покрывающий: если в индексе есть все нужные колонки, СУБД не читает саму таблицу.
- Цена: каждый индекс замедляет INSERT/UPDATE/DELETE (нужно обновлять дерево), поэтому индексы создают под реальные запросы, а не «на всякий случай».

## Когда индекс не поможет

- В маленьких таблицах быстрее полное сканирование.
- Когда селективность низкая: например, колонка с двумя значениями из миллиона строк — индекс вернёт почти всю таблицу.
- При `LIKE '%...'` — литеральный поиск с ведущим `%` не использует обычный B-tree индекс.

## Итог

Нормализация делает схему честной и устойчивой к изменениям, а индексы — быстрой. Оба инструмента применяют осознанно: формальная нормализация ради галочки и бесконечные индексы одинаково вредны. Проверяй свои индексы через EXPLAIN QUERY PLAN.

<!--TASK-->
### Задача 1
Дана таблица с нарушением 2НФ:

```python
cur.executescript("""
CREATE TABLE order_items_bad (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
INSERT INTO order_items_bad VALUES
    (1, 10, 'Клавиатура', 1500),
    (1, 20, 'Мышь', 800),
    (2, 10, 'Клавиатура', 1500),
    (3, 30, 'Монитор', 12000);
""")
```

`product_name` зависит только от `product_id` — это частичная зависимость. Напиши функцию `split_to_2nf(conn)`, которая создаёт таблицы `products(product_id, product_name)` и `order_items(order_id, product_id, price)`, переносит данные и возвращает кортеж `(n_products, n_items)`. Ожидаемый вывод: `(3, 4)` (три товара, четыре позиции заказов).

### Задача 2
Дана таблица с транзитивной зависимостью:

```python
cur.executescript("""
CREATE TABLE employees_bad (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    department_name TEXT NOT NULL,
    department_floor INTEGER NOT NULL
);
INSERT INTO employees_bad VALUES
    (1, 'Аня', 10, 'Разработка', 3),
    (2, 'Борис', 10, 'Разработка', 3),
    (3, 'Вера', 20, 'Маркетинг', 5),
    (4, 'Глеб', 20, 'Маркетинг', 5);
""")
```

`department_name` и `department_floor` зависят от `department_id`, а не от `id`. Напиши функцию `to_3nf(conn)`, которая создаёт `departments(department_id, name, floor)` и `employees(id, name, department_id)`, переносит данные и возвращает `(n_depts, n_emps)`. Ожидаемый вывод: `(2, 4)`.

### Задача 3
Напиши функцию `index_plan(conn)`, которая в базе с таблицей `orders(user_id, amount)` (заполни её 1000 случайных строк сама) делает следующее: сначала выполняет `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42` и запоминает план, затем создаёт индекс `CREATE INDEX idx_orders_user ON orders(user_id)` и снова выполняет тот же EXPLAIN. Верни кортеж `(plan_before, plan_after)`. В `plan_before` должна встречаться подстрока `SCAN`, в `plan_after` — `USING INDEX`. Выведи оба плана.

### Задача 4
Напиши функцию `enforce_unique(conn)`, которая создаёт таблицу `users(id, email)`, заполняет её двумя строками, добавляет `CREATE UNIQUE INDEX idx_users_email ON users(email)` и затем пытается вставить третью строку с уже существующим email. Поймай `sqlite3.IntegrityError` и верни строку `"blocked"` — или верни `"inserted"`, если дубликат прошёл. Ожидаемый вывод: `blocked`.

### Задача 5
Напиши функцию `composite_plan(conn)`, которая создаёт таблицу `orders(id, user_id, status, amount)`, заполняет её 500 строками (статусы `'new'` и `'done'`), затем создаёт составной индекс `CREATE INDEX idx_orders_user_status ON orders(user_id, status)`. После этого выполни `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 7 AND status = 'new'` и верни строку плана. Проверь, что в ней есть `USING INDEX`. Выведи план.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай таблицы через `CREATE TABLE products AS SELECT DISTINCT product_id, product_name FROM order_items_bad` или вручную со вставкой DISTINCT-значений. Для order_items просто выбери order_id, product_id, price из исходной таблицы. Посчитай строки через `SELECT COUNT(*)` по каждой новой таблице.

### Подсказка 2
Сначала создай `departments` с DISTINCT-значениями `department_id, department_name, department_floor` из employees_bad. Затем создай `employees` с `id, name, department_id` из employees_bad и добавь внешний ключ на departments. Верни `(COUNT(departments), COUNT(employees))`.

### Подсказка 3
EXPLAIN QUERY PLAN возвращает строки вида `(0, 0, 0, 'SCAN orders')` — план находится в четвёртом элементе кортежа. Собери все строки в список и преврати в строки через `" ".join(...)`. До создания индекса увидишь SCAN, после — SEARCH ... USING INDEX.

### Подсказка 4
Оберни вставку дубликата в `try/except sqlite3.IntegrityError`. Помни: уникальный индекс проверяется при INSERT, поэтому нарушение условия вызовет исключение. Не забудь `conn.commit()` после начальных вставок. Дубликат — это вторая вставка с тем же email.

### Подсказка 5
Составной индекс работает, когда колонки в WHERE идут в том же порядке, что в индексе (сначала user_id, потом status). Сгенерируй строки циклом: `user_id = i % 50`, `status = 'new' if i % 2 == 0 else 'done'`, `amount = i * 10`. В EXPLAIN ищи `SEARCH orders USING INDEX idx_orders_user_status`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sqlite3

def split_to_2nf(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE order_items_bad (
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        PRIMARY KEY (order_id, product_id)
    );
    INSERT INTO order_items_bad VALUES
        (1, 10, 'Клавиатура', 1500),
        (1, 20, 'Мышь', 800),
        (2, 10, 'Клавиатура', 1500),
        (3, 30, 'Монитор', 12000);
    CREATE TABLE products AS
        SELECT DISTINCT product_id, product_name FROM order_items_bad;
    CREATE TABLE order_items AS
        SELECT order_id, product_id, price FROM order_items_bad;
    """)
    conn.commit()
    n_products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    n_items = cur.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
    return (n_products, n_items)

conn = sqlite3.connect(":memory:")
print(split_to_2nf(conn))
```

Результат:

```
(3, 4)
```

Что здесь происходит? Исходная таблица хранит название товара в каждой строке заказа: если «Клавиатура» переименуется, придётся обновлять две строки. Мы выносим товары в отдельную таблицу `products` — DISTINCT убирает дубликаты имён. Таблица `order_items` остаётся с парным ключом и ценой, которая действительно зависит от пары (order_id, product_id). Количество товаров — 3, позиций заказов — 4. Теперь название товара живёт в одном месте.

### Разбор 2
Решение:

```python
import sqlite3

def to_3nf(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE employees_bad (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        department_name TEXT NOT NULL,
        department_floor INTEGER NOT NULL
    );
    INSERT INTO employees_bad VALUES
        (1, 'Аня', 10, 'Разработка', 3),
        (2, 'Борис', 10, 'Разработка', 3),
        (3, 'Вера', 20, 'Маркетинг', 5),
        (4, 'Глеб', 20, 'Маркетинг', 5);
    CREATE TABLE departments AS
        SELECT DISTINCT department_id, department_name AS name, department_floor AS floor
        FROM employees_bad;
    CREATE TABLE employees AS
        SELECT id, name, department_id FROM employees_bad;
    """)
    conn.commit()
    n_depts = cur.execute("SELECT COUNT(*) FROM departments").fetchone()[0]
    n_emps = cur.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    return (n_depts, n_emps)

conn = sqlite3.connect(":memory:")
print(to_3nf(conn))
```

Результат:

```
(2, 4)
```

Что здесь происходит? В employees_bad название отдела и этаж повторяются для каждого сотрудника и зависят от department_id — это транзитивная зависимость (сотрудник → отдел → его характеристики). Мы переносим отделы в справочник departments: DISTINCT убирает дубликаты, поэтому получается 2 отдела, а не 4. В employees остаются только данные, зависящие напрямую от id сотрудника. Теперь переезд отдела на другой этаж — это обновление одной строки справочника, а не четырёх.

### Разбор 3
Решение:

```python
import sqlite3

def index_plan(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE orders (user_id INTEGER, amount REAL);
    """)
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?)",
        [(i % 100, i * 3.5) for i in range(1000)],
    )
    conn.commit()
    plan_before = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42"
    ).fetchall()
    cur.execute("CREATE INDEX idx_orders_user ON orders(user_id)")
    plan_after = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42"
    ).fetchall()
    fmt = lambda rows: " | ".join(row[3] for row in rows)
    return (fmt(plan_before), fmt(plan_after))

conn = sqlite3.connect(":memory:")
before, after = index_plan(conn)
print("До:", before)
print("После:", after)
```

Результат (примерно):

```
До: SCAN orders
После: SEARCH orders USING INDEX idx_orders_user (user_id=?)
```

Что здесь происходит? До индекса планировщик вынужден прочитать все 1000 строк — план SCAN orders. После создания индекса план меняется на SEARCH ... USING INDEX: СУБД спускается по B-дереву и находит нужные строки за O(log n) шагов. Для 1000 строк разница незаметна, но на миллионах она превращается в порядки. Запомни сам приём: прежде чем спорить о скорости, смотри EXPLAIN QUERY PLAN — план расскажет, используется ли индекс вообще.

### Разбор 4
Решение:

```python
import sqlite3

def enforce_unique(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT);
    INSERT INTO users VALUES (1, 'anya@example.com'), (2, 'boris@example.com');
    CREATE UNIQUE INDEX idx_users_email ON users(email);
    """)
    conn.commit()
    try:
        cur.execute("INSERT INTO users VALUES (3, 'anya@example.com')")
        conn.commit()
        return "inserted"
    except sqlite3.IntegrityError:
        return "blocked"

conn = sqlite3.connect(":memory:")
print(enforce_unique(conn))
```

Результат:

```
blocked
```

Что здесь происходит? Уникальный индекс гарантирует уникальность значений на уровне СУБД, а не в коде приложения. При попытке вставить второй раз email `anya@example.com` SQLite отклоняет вставку и бросает IntegrityError. Мы ловим его и возвращаем "blocked". Обрати внимание: проверка происходит даже если в другой части приложения кто-то «забыл» проверить дубликат. Именно поэтому уникальные индексы — стандартный способ защитить email, артикулы и другие естественные ключи.

### Разбор 5
Решение:

```python
import sqlite3

def composite_plan(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT,
        amount REAL
    );
    """)
    rows = [
        (i, i % 50, "new" if i % 2 == 0 else "done", i * 10.0)
        for i in range(500)
    ]
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", rows)
    conn.commit()
    cur.execute("CREATE INDEX idx_orders_user_status ON orders(user_id, status)")
    plan = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 7 AND status = 'new'"
    ).fetchall()
    return " | ".join(row[3] for row in plan)

conn = sqlite3.connect(":memory:")
print(composite_plan(conn))
```

Результат (примерно):

```
SEARCH orders USING INDEX idx_orders_user_status (user_id=? AND status=?)
```

Что здесь происходит? Составной индекс `(user_id, status)` обслуживает запросы, которые фильтруют по обеим колонкам. Порядок колонок важен: индекс (user_id, status) поможет и для `WHERE user_id = 7`, и для `WHERE user_id = 7 AND status = 'new'`, но не для `WHERE status = 'new'` — левая колонка индекса должна участвовать в условии. Если бы мы создали индекс (status, user_id), ситуация была бы обратной. План SEARCH подтверждает: база идёт по индексу, а не сканирует таблицу.
<!--/SOLUTION-->

<!--QUIZ-->
Какая аномалия возникает, если клиент меняет телефон, хранящийся в каждой строке его заказа?
- Аномалия удаления
- Аномалия обновления
- Аномалия вставки
- Никакой, это нормально
* Правильный ответ: Аномалия обновления
Одно изменение приходится повторять в нескольких строках, и легко забыть обновить одну из них.

Что требуется для 2НФ?
- Только наличие первичного ключа
- 1НФ и отсутствие частичных зависимостей от составного ключа
- Отсутствие транзитивных зависимостей
- Уникальность всех колонок
* Правильный ответ: 1НФ и отсутствие частичных зависимостей от составного ключа
2НФ добавляет к 1НФ требование: непервичные колонки зависят от всего ключа целиком, а не от его части.

Что такое транзитивная зависимость (нарушение 3НФ)?
- Колонка зависит от другой непервичной колонки, а та — от ключа
- Две колонки полностью совпадают
- Колонка зависит от составного ключа
- Зависимость от другой таблицы
* Правильный ответ: Колонка зависит от другой непервичной колонки, а та — от ключа
Например, пол зависит от города, а город — от адреса; это признак плохой схемы.

Что такое индекс в БД?
- Копия всей таблицы
- Структура для быстрого поиска строк по колонке
- Список ограничений таблицы
- Журнал изменений
* Правильный ответ: Структура для быстрого поиска строк по колонке
Индекс (обычно B-дерево) позволяет находить строки без полного сканирования таблицы.

Какая плата за каждый индекс?
- Хранение данных занимает меньше места
- Замедление INSERT/UPDATE/DELETE
- Ускорение записи
- Индексы бесплатны
* Правильный ответ: Замедление INSERT/UPDATE/DELETE
При каждой записи нужно обновлять и дерево индекса, поэтому индексы создают под реальные запросы.

Что покажет EXPLAIN QUERY PLAN после создания подходящего индекса?
- SCAN таблицы
- SEARCH таблицы USING INDEX
- Ошибку синтаксиса
- Пустой результат
* Правильный ответ: SEARCH таблицы USING INDEX
План показывает, каким способом база достаёт данные: по индексу (SEARCH ... USING INDEX) или полным сканированием (SCAN).

Зачем нужен UNIQUE INDEX?
- Чтобы ускорить выборку
- Чтобы гарантировать уникальность значений на уровне СУБД
- Чтобы запретить NULL
- Чтобы ускорить запись
* Правильный ответ: Чтобы гарантировать уникальность значений на уровне СУБД
Уникальный индекс не даёт вставить дубликат, даже если код приложения забыл проверить.

Какие требования у первой нормальной формы (1НФ)?
- Атомарные значения в ячейках и наличие первичного ключа
- Отсутствие частичных зависимостей
- Отсутствие транзитивных зависимостей
* Правильный ответ: Атомарные значения в ячейках и наличие первичного ключа
Хранение списка через запятую в одной ячейке нарушает 1НФ.
<!--/QUIZ-->
