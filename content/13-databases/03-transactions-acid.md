---
title: Транзакции и ACID
summary: Что такое транзакция и ACID, проблемы параллельности и уровни изоляции, savepoint-ы, блокировки и обработка «database is locked».
order: 3
duration: 45 мин
difficulty: advanced
tags: транзакции, acid, изоляция, блокировки, sqlite3
---

## Что такое транзакция

Транзакция — это группа операций с базой данных, которые выполняются как одно целое: либо все успешно (COMMIT), либо никакие (ROLLBACK). Классический пример — перевод денег между счетами:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    owner TEXT,
    balance REAL NOT NULL CHECK (balance >= 0)
);
INSERT INTO accounts VALUES (1, 'Аня', 5000), (2, 'Борис', 1000);
""")
conn.commit()

def transfer(from_id, to_id, amount):
    try:
        with conn:
            a = cur.execute(
                "SELECT balance FROM accounts WHERE id = ?", (from_id,)
            ).fetchone()[0]
            if a < amount:
                raise ValueError("Недостаточно средств")
            cur.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id),
            )
            cur.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id),
            )
            return True
    except ValueError:
        return False

print(transfer(1, 2, 700))
print(cur.execute("SELECT owner, balance FROM accounts ORDER BY id").fetchall())
```

Контекст `with conn:` сам открывает транзакцию и делает COMMIT при успехе или ROLLBACK при исключении. После перевода балансы: `[('Аня', 4300.0), ('Борис', 1700.0)]`.

Почему важна атомарность? Если бы первый UPDATE списал деньги, а второй UPDATE не выполнился из-за сбоя сети, деньги «испарились» бы. Транзакция гарантирует: либо оба изменения сохранятся, либо ни одного.

## ACID

- **Atomicity (Атомарность)** — все операции транзакции выполняются или все вместе, или никакие.
- **Consistency (Согласованность)** — после транзакции база остаётся в корректном состоянии: не нарушены ограничения CHECK, внешние ключи, триггеры.
- **Isolation (Изоляция)** — параллельные транзакции не видят промежуточных состояний друг друга.
- **Durability (Долговечность)** — закоммиченные данные переживают сбой питания или перезапуск базы.

## Проблемы параллельности

Когда две транзакции работают над одними данными, возникают классические проблемы:

- **Грязное чтение**: транзакция видит незакоммиченные изменения другой транзакции. Если та откатится, первая читала данные, которых никогда не существовало.
- **Неповторяемое чтение**: внутри одной транзакции одна и та же строка читается с разными значениями, потому что её изменила и закоммитила другая транзакция.
- **Фантомы**: повторный SELECT возвращает новые строки, добавленные другими транзакциями в промежутке.

Для борьбы с этим существуют уровни изоляции:

| Уровень | Грязное чтение | Неповторяемое чтение | Фантомы |
|---|---|---|---|
| READ UNCOMMITTED | возможно | возможно | возможно |
| READ COMMITTED | нет | возможно | возможно |
| REPEATABLE READ | нет | нет | возможно |
| SERIALIZABLE | нет | нет | нет |

Чем выше уровень, тем больше блокировок и тем ниже параллельность. SERIALIZABLE — самый безопасный, но и самый медленный.

## Транзакции в SQLite

SQLite по умолчанию использует DEFERRED-транзакции и сериализует записи через файловую блокировку: одновременно писать может только один процесс. Игнорировать это нельзя — два процесса при одновременной записи получат ошибку `database is locked`. Лечится `PRAGMA busy_timeout` и повторами:

```python
conn.execute("PRAGMA busy_timeout = 5000")  # ждать до 5 секунд
```

Чтобы явно управлять точками отката, есть savepoint-ы:

```python
conn.execute("SAVEPOINT sp1")
cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
conn.execute("ROLLBACK TO sp1")   # откатываем только изменения после savepoint
conn.execute("RELEASE sp1")
```

После этого изменение откачено, но сама транзакция продолжает жить, и её можно завершить COMMIT.

## Блокировки и дедлоки

**Пессимистическая блокировка** захватывает строки заранее (`SELECT ... FOR UPDATE` в PostgreSQL) — риск дедлоков, но гарантия стабильности. **Оптимистическая** не блокирует ничего, а при сохранении проверяет версию строки: если она изменилась — конфликт, запрос повторяется. Дедлок — это когда две транзакции ждут друг друга: A заблокировала строку 1 и ждёт строку 2, B — наоборот. Методы борьбы: единый порядок обращения к таблицам, короткие транзакции, тайм-ауты.

## Итог

Транзакции — основа надёжности данных. Три правила: держи транзакции короткими, не делай внутри них медленных внешних вызовов (сеть, файлы) и всегда обрабатывай исключения, чтобы ROLLBACK сработал.

<!--TASK-->
### Задача 1
Напиши функцию `transfer(from_id, to_id, amount)`, которая переводит деньги между счетами строго внутри транзакции и возвращает `True` при успехе или `False`, если средств недостаточно. Схема: `accounts(id, owner, balance)` с CHECK (balance >= 0); начальные данные: Аня — 5000, Борис — 1000. Убедись, что при неудачном переводе балансы не изменились. Выведи результаты трёх вызовов: `transfer(1, 2, 700)`, `transfer(1, 2, 9000)` и итоговые балансы. Ожидаемый вывод: `True`, `False`, `[('Аня', 4300.0), ('Борис', 1700.0)]`.

### Задача 2
Напиши функцию `atomic_batch(conn)`, которая создаёт таблицу `items(id INTEGER PRIMARY KEY, qty INTEGER CHECK (qty > 0))`, вставляет три валидные строки и коммитит их. Затем в одной транзакции пытается вставить ещё три строки, из которых одна нарушает CHECK (qty = 0). Функция должна вернуть кортеж `(count_before, count_after)` — число строк до и после неудачной попытки. Ожидаемый вывод: `(3, 3)` — вся пачка откатилась целиком.

### Задача 3
Напиши скрипт, который демонстрирует savepoint: внутри одной транзакции поставь `SAVEPOINT sp1`, уменьши баланс Ани на 100, затем сделай `ROLLBACK TO sp1`, затем увеличь баланс Бориса на 50 и закоммить. Выведи итоговые балансы. Ожидаемый вывод: `[('Аня', 5000.0), ('Борис', 1050.0)]` — откат затронул только первое изменение.

### Задача 4
Напиши скрипт с двумя соединениями к одной базе (используй URI `file:shareddb?mode=memory&cache=shared` с `uri=True`). Первое соединение открывает транзакцию `BEGIN IMMEDIATE` и делает UPDATE без COMMIT. Второе соединение с `PRAGMA busy_timeout = 0` пытается сделать свой UPDATE — поймай `sqlite3.OperationalError` и выведи текст ошибки. Затем закоммить первое соединение, установи `busy_timeout = 2000` на втором, повтори UPDATE — он должен пройти. Ожидаемый вывод: строка с `database is locked`, затем успешное выполнение.

### Задача 5
Напиши функцию `withdraw(conn, user_id, amount)`, которая списывает деньги со счёта внутри транзакции и возвращает `("ok", новый_баланс)` или `("error", None)`, если баланс стал бы отрицательным. Полагайся на CHECK-ограничение: лови `sqlite3.IntegrityError` и дай транзакции откатиться. Тест: `withdraw(conn, 1, 3000)` → `('ok', 2000.0)`; `withdraw(conn, 1, 9000)` → `('error', None)`; суммарный баланс всех счетов после всех операций должен оставаться 6000.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Используй `with conn:` — он сам коммитит при успехе и откатывает при исключении. Внутри сначала прочитай баланс `SELECT`, проверь `amount`, затем два `UPDATE`. Слишком большую сумму проверяй через `if a < amount: raise ValueError(...)`.

### Подсказка 2
Вставки через `cur.executemany("INSERT INTO items (qty) VALUES (?)", rows)` внутри `with conn:`. Число строк считай через `SELECT COUNT(*) FROM items` до и после блока. Ошибка IntegrityError должна произойти именно внутри блока, чтобы откат сработал автоматически.

### Подсказка 3
Порядок: `BEGIN` (или просто первый оператор), `SAVEPOINT sp1`, UPDATE Ани, `ROLLBACK TO sp1`, `RELEASE sp1`, UPDATE Бориса, `COMMIT`. Посмотри итоговые балансы: изменение Ани должно пропасть, изменение Бориса — остаться.

### Подсказка 4
Оба соединения должны использовать один и тот же URI, иначе это будут две разные базы и блокировки не будет. `BEGIN IMMEDIATE` захватывает блокировку на запись сразу. Для второго соединения выполни `conn2.execute("PRAGMA busy_timeout = 0")` перед первой попыткой и `conn2.execute("PRAGMA busy_timeout = 2000")` перед второй. Не забудь закрыть соединения в конце.

### Подсказка 5
Внутри `with conn:` выполняй `UPDATE accounts SET balance = balance - ? WHERE id = ?` и сразу читай новый баланс. Ошибку IntegrityError лови вокруг блока и возвращай `("error", None)`. Проверь итоговый баланс: сумма по всем счетам должна остаться 6000 — это и есть согласованность (Consistency).
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    owner TEXT,
    balance REAL NOT NULL CHECK (balance >= 0)
);
INSERT INTO accounts VALUES (1, 'Аня', 5000), (2, 'Борис', 1000);
""")
conn.commit()

def transfer(from_id, to_id, amount):
    try:
        with conn:
            a = cur.execute(
                "SELECT balance FROM accounts WHERE id = ?", (from_id,)
            ).fetchone()[0]
            if a < amount:
                raise ValueError("Недостаточно средств")
            cur.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, from_id),
            )
            cur.execute(
                "UPDATE accounts SET balance = balance + ? WHERE id = ?",
                (amount, to_id),
            )
            return True
    except ValueError:
        return False

print(transfer(1, 2, 700))
print(transfer(1, 2, 9000))
print(cur.execute("SELECT owner, balance FROM accounts ORDER BY id").fetchall())
```

Результат:

```
True
False
[('Аня', 4300.0), ('Борис', 1700.0)]
```

Что здесь происходит? `with conn:` — это менеджер контекста: он начинает транзакцию, а при выходе либо коммитит (если не было исключения), либо откатывает. Первый перевод уменьшает баланс Ани и увеличивает баланс Бориса — оба изменения сохраняются вместе. Второй перевод проверяет баланс, видит, что 5000 меньше 9000, бросает ValueError; контекст откатывает транзакцию, и ни одно из изменений не попадает в базу. Именно так выглядят атомарные денежные переводы в реальных системах.

### Разбор 2
Решение:

```python
import sqlite3

def atomic_batch(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        qty INTEGER CHECK (qty > 0)
    );
    """)
    cur.executemany("INSERT INTO items (qty) VALUES (?)", [(5,), (10,), (7,)])
    conn.commit()
    count_before = cur.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    try:
        with conn:
            cur.executemany(
                "INSERT INTO items (qty) VALUES (?)",
                [(3,), (0,), (12,)],   # (0,) нарушает CHECK
            )
    except sqlite3.IntegrityError:
        pass
    count_after = cur.execute("SELECT COUNT(*) FROM items").fetchone()[0]
    return (count_before, count_after)

conn = sqlite3.connect(":memory:")
print(atomic_batch(conn))
```

Результат:

```
(3, 3)
```

Что здесь происходит? Внутри `with conn:` выполняются три вставки. Третья строка со значением qty = 0 нарушает CHECK-ограничение, и SQLite бросает IntegrityError. Менеджер контекста видит исключение и откатывает всю транзакцию — включая две валидные строки, которые уже были вставлены. После отката в таблице по-прежнему три строки. Это и есть атомарность: частичный успех невозможен. Заметь: вне транзакции каждая вставка коммитилась бы отдельно, и две первые прошли бы «навсегда».

### Разбор 3
Решение:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    owner TEXT,
    balance REAL NOT NULL
);
INSERT INTO accounts VALUES (1, 'Аня', 5000), (2, 'Борис', 1000);
""")
conn.commit()

cur.execute("BEGIN")
cur.execute("SAVEPOINT sp1")
cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
cur.execute("ROLLBACK TO sp1")
cur.execute("RELEASE sp1")
cur.execute("UPDATE accounts SET balance = balance + 50 WHERE id = 2")
conn.commit()

print(cur.execute("SELECT owner, balance FROM accounts ORDER BY id").fetchall())
```

Результат:

```
[('Аня', 5000.0), ('Борис', 1050.0)]
```

Что здесь происходит? SAVEPOINT отмечает точку внутри транзакции. Все изменения после этой отметки можно откатить командой `ROLLBACK TO sp1`, не трогая более ранние изменения и не завершая транзакцию целиком. Здесь списание 100 у Ани откатывается, а начисление 50 Борису остаётся. Команда `RELEASE sp1` убирает savepoint — после неё откатиться к этой точке уже нельзя. Итог: баланс Ани без изменений, Борис получил 50. Savepoint-ы удобны в длинных операциях, где часть шагов можно безопасно отменить.

### Разбор 4
Решение:

```python
import sqlite3

URI = "file:shareddb?mode=memory&cache=shared"

conn1 = sqlite3.connect(URI, uri=True)
conn2 = sqlite3.connect(URI, uri=True)
c1, c2 = conn1.cursor(), conn2.cursor()
c1.executescript("""
CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance REAL);
INSERT INTO accounts VALUES (1, 'Аня', 5000), (2, 'Борис', 1000);
""")
conn1.commit()

c1.execute("BEGIN IMMEDIATE")
c1.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")

conn2.execute("PRAGMA busy_timeout = 0")
try:
    c2.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
except sqlite3.OperationalError as e:
    print("Первая попытка:", e)

conn1.commit()
conn2.execute("PRAGMA busy_timeout = 2000")
c2.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
conn2.commit()
print(c2.execute("SELECT owner, balance FROM accounts ORDER BY id").fetchall())
```

Результат:

```
Первая попытка: database is locked
[('Аня', 4900.0), ('Борис', 1100.0)]
```

Что здесь происходит? BEGIN IMMEDIATE сразу захватывает эксклюзивную блокировку на запись. Второе соединение с busy_timeout = 0 не ждёт ни секунды и получает `database is locked`. После COMMIT первого соединения блокировка освобождается; второе соединение с busy_timeout = 2000 ждёт до двух секунд и успешно выполняет свой UPDATE. Так в реальных сервисах решают конфликты писателей: ставят разумный тайм-аут и повторяют операцию, а не падают сразу.

### Разбор 5
Решение:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    owner TEXT,
    balance REAL NOT NULL CHECK (balance >= 0)
);
INSERT INTO accounts VALUES (1, 'Аня', 5000), (2, 'Борис', 1000);
""")
conn.commit()

def withdraw(conn, user_id, amount):
    cur = conn.cursor()
    try:
        with conn:
            cur.execute(
                "UPDATE accounts SET balance = balance - ? WHERE id = ?",
                (amount, user_id),
            )
            new_balance = cur.execute(
                "SELECT balance FROM accounts WHERE id = ?", (user_id,)
            ).fetchone()[0]
            return ("ok", new_balance)
    except sqlite3.IntegrityError:
        return ("error", None)

print(withdraw(conn, 1, 3000))
print(withdraw(conn, 1, 9000))
print(cur.execute("SELECT SUM(balance) FROM accounts").fetchone()[0])
```

Результат:

```
('ok', 2000.0)
('error', None)
6000.0
```

Что здесь происходит? Первый вывод списывает 3000: баланс становится 2000, транзакция коммитится. Второй вывод пытается списать 9000 с баланса 2000 — CHECK (balance >= 0) не даёт балансу стать отрицательным, SQLite бросает IntegrityError, контекст откатывает транзакцию, и мы возвращаем ("error", None). Суммарный баланс всех счетов остаётся 6000: база согласованна. Обрати внимание: мы положились на ограничение базы, а не только на проверку в Python — это надёжнее, потому что ограничение действует для любого кода, который пишет в таблицу.
<!--/SOLUTION-->

<!--QUIZ-->
Что гарантирует атомарность транзакции?
- Каждая операция выполняется независимо
- Либо все операции применяются, либо ни одна
- Данные переживают перезапуск базы
- Операции выполняются одновременно
* Правильный ответ: Либо все операции применяются, либо ни одна
Атомарность означает «всё или ничего»: частичный успех невозможен.

Какая проблема возникает, когда транзакция читает незакоммиченные изменения другой транзакции?
- Фантомы
- Грязное чтение
- Неповторяемое чтение
- Дедлок
* Правильный ответ: Грязное чтение
Если другая транзакция откатится, прочитанные данные окажутся несуществующими.

Какой уровень изоляции запрещает грязное чтение, но допускает неповторяемое?
- READ UNCOMMITTED
- READ COMMITTED
- SERIALIZABLE
- Никакой
* Правильный ответ: READ COMMITTED
READ COMMITTED видит только закоммиченные данные, но две одинаковые выборки внутри одной транзакции могут дать разные значения.

Что делает ROLLBACK TO sp1?
- Откатывает всю транзакцию
- Откатывает только изменения, сделанные после savepoint sp1
- Удаляет таблицу
- Закрывает соединение
* Правильный ответ: Откатывает только изменения, сделанные после savepoint sp1
Savepoint — точка отката внутри транзакции; ROLLBACK TO возвращает базу к этой точке, не завершая транзакцию.

Почему «database is locked» возникает при конкурентной записи в SQLite?
- Из-за ограничения размера базы
- Из-за эксклюзивной блокировки на запись — одновременно пишет только один процесс
- Из-за отсутствия индексов
- Из-за старой версии Python
* Правильный ответ: Из-за эксклюзивной блокировки на запись — одновременно пишет только один процесс
SQLite сериализует писателей; остальные ждут (busy_timeout) или получают ошибку.

Что означает Consistency (согласованность) в ACID?
- Данные после транзакции соответствуют всем ограничениям базы
- Данные зашифрованы
- Данные хранятся в одном файле
- Данные доступны только одному пользователю
* Правильный ответ: Данные после транзакции соответствуют всем ограничениям базы
CHECK, внешние ключи и триггеры не должны быть нарушены после COMMIT.
<!--/QUIZ-->
