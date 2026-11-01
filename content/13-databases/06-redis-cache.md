---
title: Кэширование с Redis
summary: Redis как кэш: строки и TTL, паттерн cache-aside, pipeline, инвалидация, защита от кэш-прострела и мягкая деградация.
order: 6
duration: 45 мин
difficulty: advanced
tags: redis, кэш, cache-aside, ttl, pipeline
---

## Что такое Redis

Redis — быстрый сервер структур данных в оперативной памяти. Чаще всего он используется как кэш перед базой данных: горячие данные живут в RAM и отдаются за микросекунды, а тяжёлая база защищается от лишней нагрузки. Ключевые структуры Redis — строки, списки, множества, хеши и отсортированные множества. Установи клиент и подключимся:

```bash
pip install redis
```

```python
import redis

r = redis.Redis(host="localhost", port=6379, db=0)
r.set("greeting", "Привет!")
print(r.get("greeting"))   # b'Привет!'
r.delete("greeting")
```

Redis хранит байты, поэтому `get` возвращает `bytes` — `b'Привет!'`. Если удобнее строки, передай `decode_responses=True` при создании клиента. Для локальных экспериментов без сервера можно использовать `fakeredis` — это библиотека с тем же API (установка: `pip install fakeredis`, клиент: `fakeredis.FakeRedis()`).

## Основные команды

- `SET key value` / `GET key` — записать/прочитать строку.
- `SETEX key seconds value` — записать строку с временем жизни (TTL).
- `EXPIRE key seconds` — задать TTL уже существующему ключу.
- `TTL key` — сколько секунд осталось жить: -1 — без срока, -2 — ключа нет.
- `INCR key` / `DECR key` — атомарный инкремент/декремент.
- `DEL key` — удалить ключ.

```python
r.setex("profile:42", 60, "{...}")   # живёт 60 секунд
print(r.ttl("profile:42"))            # примерно 60
```

## Паттерн cache-aside (ленивое кэширование)

Самый распространённый паттерн кэширования. Схема:

1. Читаем ключ из Redis.
2. Ключ есть — возвращаем значение (hit).
3. Ключа нет (miss) — читаем из базы данных, кладём в Redis с TTL, возвращаем.

```python
def get_user(user_id):
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached is not None:
        return cached.decode()
    row = cur.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
    value = row[0] if row else None
    if value is not None:
        r.setex(key, 300, value)   # кэш на 5 минут
    return value
```

## TTL и инвалидация

Кэш всегда рискует устареть. Есть два рычага:

- **TTL** — данные автоматически исчезают через N секунд, и следующий запрос считает их заново.
- **Активная инвалидация** — при обновлении записи в базе удаляем ключ (DEL или EXPIRE), чтобы следующий запрос перечитал свежие данные.

Правило: TTL — базовая защита от устаревания, а инвалидация на запись — для данных, которые меняются часто и должны быть свежими немедленно.

## Кэш-прострел (cache stampede)

Если ключ истёк, а к нему одновременно обратились 1000 запросов — все они пойдут в базу данных. Защита: «один пишет, остальные ждут» через блокировку с `SETNX` (set if not exists), либо обновление ключа фоном до истечения. Отдельная проблема — «кэш-пробивание»: запросы по ключам, которых нет в базе, не кэшируются, и каждый такой запрос бьёт в базу. Решение — кэшировать и отрицательный результат на короткий срок.

## Pipeline

Каждая команда — отдельный сетевой кругосвет; на 1000 командах это дорого. Pipeline упаковывает команды в один сетевой обмен:

```python
pipe = r.pipeline()
for i in range(1000):
    pipe.incr(f"counter:{i}")
pipe.execute()
```

## Что если Redis упал?

Код не должен падать вместе с Redis. Оберни вызовы в try/except и при недоступности кэша просто читай базу — это называется мягкой деградацией (graceful degradation). Для тестов без сервера используй `fakeredis` — тот же API, те же тесты.

## Итог

Redis — мощный инструмент, но кэш всегда компромисс: он ускоряет чтение ценой риска устаревших данных и усложнения кода. Кэшируй только тяжёлые и часто читаемые данные, всегда ставь TTL и проектируй деградацию.

<!--TASK-->
### Задача 1
Напиши функцию `string_roundtrip(r)`, которая принимает redis-клиента (реальный `redis.Redis` или `fakeredis.FakeRedis()`) и выполняет: `SET` ключа `"city"` со значением `"Москва"`, затем `GET`, `TTL`, `EXPIRE` на 100 секунд, снова `TTL`, и `DEL`. Верни кортеж: `(city_value, ttl_before, ttl_after, exists_after_delete)`, где ttl_before — TTL сразу после SET (ожидается -1), ttl_after — после EXPIRE (1–100), exists_after_delete — результат GET после DEL (None). Выведи кортеж.

### Задача 2
Напиши декоратор `cached(ttl)`, который оборачивает произвольную функцию и кэширует её результат в Redis: ключ — `"cache:" + имя_функции + ":" + str(аргумент)`. Если значения нет — вызов вычисляет, сохраняет через `setex` и возвращает; если есть — возвращает из кэша без вычисления. Функция `slow(x)` пусть считает `x * x` и печатает `"compute"` при каждом реальном вычислении. Верни кортеж `(a, b, compute_count)`, где a, b — результаты двух вызовов `slow(5)`, а compute_count — сколько раз печаталось "compute". Ожидаемый вывод: `(25, 25, 1)`.

### Задача 3
Напиши функцию `pipeline_incr(r)`, которая через pipeline инкрементирует 500 ключей `counter:0` ... `counter:499` (начальные значения 0) и возвращает кортеж `(n_commands, total_sum)`, где n_commands — число команд в pipeline, total_sum — сумма всех получившихся значений. Ожидаемый вывод: `(500, 500)`.

### Задача 4
Напиши функцию `get_user_cached(r, cur, user_id)`, реализующую паттерн cache-aside: сначала Redis (ключ `user:<id>`), при промахе — sqlite3-таблица `users(id, name)` (в памяти), затем `setex` на 300 секунд. Верни кортеж `(value, from_cache)`, где from_cache — True, если значение пришло из Redis. Тест: первый вызов для user_id=1 → `('Аня', False)`, второй → `('Аня', True)`.

### Задача 5
Напиши функцию `invalidate_on_update(r, cur, user_id, new_name)`, которая обновляет имя пользователя в базе и удаляет его ключ из кэша (инвалидация). После этого вызови `get_user_cached` снова и верни кортеж `(fresh_value, from_cache)`. Сначала заполни кэш вызовом `get_user_cached(r, cur, 1)` (вернёт "Аня"), затем обнови имя на "Анна". Ожидаемый вывод: `('Анна', False)` — значение свежее, потому что старый кэш удалён.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`r.set("city", "Москва")` вернёт True. `r.get` возвращает bytes, поэтому сравнивай с `b"Москва"` или декодируй: `value.decode()`. `r.ttl("city")` после SET даёт -1, после EXPIRE — число секунд от 1 до 100. `r.delete("city")` вернёт 1 (удалён один ключ), а GET после этого — None.

### Подсказка 2
Внутри декоратора: `key = f"cache:{func.__name__}:{arg}"`; попробуй `r.get(key)` — если не None, верни `float(value)` (или decode). Если None — вычисли `result = func(arg)`, сохрани `r.setex(key, ttl, str(result))` и верни. Счётчик "compute" — обычная глобальная переменная; инкрементируй её внутри slow() перед печатью.

### Подсказка 3
`pipe = r.pipeline()`; цикл `for i in range(500): pipe.incr(f"counter:{i}")`; `pipe.execute()` возвращает список результатов (все будут 1). Сумма результатов = 500, число команд = 500. Можешь проверить `len(results) == 500`.

### Подсказка 4
Сначала `cached = r.get(f"user:{user_id}")`. Если есть — `return (cached.decode(), True)`. Если нет — запрос `SELECT name FROM users WHERE id = ?` через cur, затем `r.setex(f"user:{user_id}", 300, name)` и `(name, False)`. Создай таблицу users с одной строкой (1, 'Аня').

### Подсказка 5
После `UPDATE users SET name = ? WHERE id = ?` в базе сделай `r.delete(f"user:{user_id}")`. Потом вызови `get_user_cached` — она увидит промах, прочитает новое имя из базы и снова закэширует его.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import fakeredis

def string_roundtrip(r):
    r.set("city", "Москва")
    city_value = r.get("city").decode()
    ttl_before = r.ttl("city")
    r.expire("city", 100)
    ttl_after = r.ttl("city")
    r.delete("city")
    exists_after_delete = r.get("city")
    return (city_value, ttl_before, ttl_after, exists_after_delete)

r = fakeredis.FakeRedis()
print(string_roundtrip(r))
```

Результат (примерно):

```
('Москва', -1, 100, None)
```

Что здесь происходит? `SET` создаёт ключ без срока жизни, поэтому TTL сразу после записи равен -1. `EXPIRE` назначает время жизни — 100 секунд, и теперь TTL возвращает число от 1 до 100 (точное значение зависит от момента проверки). После `DEL` ключ исчезает, и `GET` возвращает None. Обрати внимание: `get` возвращает bytes, поэтому мы декодируем значение в строку. Для теста использован fakeredis — тот же API, что у настоящего клиента, но без сервера.

### Разбор 2
Решение:

```python
import fakeredis

r = fakeredis.FakeRedis()
compute_count = {"n": 0}

def cached(ttl):
    def decorator(func):
        def wrapper(arg):
            key = f"cache:{func.__name__}:{arg}"
            value = r.get(key)
            if value is not None:
                return float(value)
            result = func(arg)
            r.setex(key, ttl, str(result))
            return result
        return wrapper
    return decorator

@cached(ttl=60)
def slow(x):
    compute_count["n"] += 1
    print("compute")
    return x * x

a = slow(5)
b = slow(5)
print((a, b, compute_count["n"]))
```

Результат:

```
compute
(25, 25, 1)
```

Что здесь происходит? Первый вызов `slow(5)` не находит кэш, вычисляет 25, сохраняет значение в Redis на 60 секунд и печатает "compute". Второй вызов с тем же аргументом находит ключ `cache:slow:5` и возвращает закэшированное значение, не выполняя тело функции. Поэтому "compute" печатается один раз. Именно так устроены декораторы кэширования в боевых сервисах: сложные вычисления выполняются один раз, а повторные запросы обслуживаются из Redis за микросекунды.

### Разбор 3
Решение:

```python
import fakeredis

def pipeline_incr(r):
    pipe = r.pipeline()
    for i in range(500):
        pipe.incr(f"counter:{i}")
    results = pipe.execute()
    return (len(results), sum(results))

r = fakeredis.FakeRedis()
print(pipeline_incr(r))
```

Результат:

```
(500, 500)
```

Что здесь происходит? Каждая команда `INCR` по отдельности — это сетевой обмен с сервером; 500 команд без pipeline — 500 кругосветов. Pipeline собирает все команды в один буфер и отправляет их одним пакетом, а `execute()` возвращает список результатов в том же порядке. Здесь результатом каждого INCR будет 1 (начальное значение 0, инкремент даёт 1), поэтому сумма — 500. В реальных системах pipeline сокращает задержку в десятки раз, когда нужно выполнить много простых команд.

### Разбор 4
Решение:

```python
import sqlite3
import fakeredis

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO users VALUES (1, 'Аня');
""")
conn.commit()

r = fakeredis.FakeRedis()

def get_user_cached(r, cur, user_id):
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached is not None:
        return (cached.decode(), True)
    row = cur.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    name = row[0]
    r.setex(key, 300, name)
    return (name, False)

print(get_user_cached(r, cur, 1))
print(get_user_cached(r, cur, 1))
```

Результат:

```
('Аня', False)
('Аня', True)
```

Что здесь происходит? Это классический cache-aside. Первый вызов — промах: значения в Redis нет, поэтому читаем базу, сохраняем имя в Redis на 300 секунд и возвращаем с флагом False. Второй вызов — попадание: ключ уже есть в кэше, мы возвращаем его без обращения к базе с флагом True. Так горячие записи постепенно «разогревают» кэш, а база получает только реальные промахи.

### Разбор 5
Решение:

```python
import sqlite3
import fakeredis

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO users VALUES (1, 'Аня');
""")
conn.commit()

r = fakeredis.FakeRedis()

def get_user_cached(r, cur, user_id):
    key = f"user:{user_id}"
    cached = r.get(key)
    if cached is not None:
        return (cached.decode(), True)
    row = cur.execute(
        "SELECT name FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    name = row[0]
    r.setex(key, 300, name)
    return (name, False)

def invalidate_on_update(r, cur, user_id, new_name):
    cur.execute("UPDATE users SET name = ? WHERE id = ?",
                (new_name, user_id))
    conn.commit()
    r.delete(f"user:{user_id}")

print(get_user_cached(r, cur, 1))      # кэшируем "Аня"
invalidate_on_update(r, cur, 1, "Анна")
print(get_user_cached(r, cur, 1))      # свежее имя из базы
```

Результат:

```
('Аня', False)
('Анна', False)
```

Что здесь происходит? Сначала мы заполняем кэш именем "Аня". Затем обновляем запись в базе на "Анна" и удаляем ключ из Redis — это инвалидация кэша. Следующий вызов `get_user_cached` видит промах, читает свежее имя из базы, снова кэширует его и возвращает "Анна" с флагом False. Если бы мы не удалили ключ, следующий запрос вернул бы устаревшее "Аня" из кэша. Так связка TTL + инвалидация на запись поддерживает баланс между скоростью и свежестью данных.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает команда SETEX key 60 value?
- Записывает значение и задаёт ему время жизни 60 секунд
- Записывает значение навсегда
- Удаляет ключ через 60 секунд
- Увеличивает значение на 60
* Правильный ответ: Записывает значение и задаёт ему время жизни 60 секунд
SETEX — SET + EXPIRE одной командой.

Что вернёт TTL для ключа без срока жизни?
- 0
- -1
- 60
- Ошибку
* Правильный ответ: -1
-1 означает «бессрочный», -2 — «ключа не существует».

Какой первый шаг в паттерне cache-aside?
- Записать данные в базу
- Прочитать ключ из Redis; при промахе — читать базу
- Перезапустить Redis
- Удалить все ключи
* Правильный ответ: Прочитать ключ из Redis; при промахе — читать базу
При промахе данные берутся из базы и кладутся в кэш с TTL.

Что такое кэш-прострел (cache stampede)?
- Когда много запросов одновременно попадают на истёкший ключ и все идут в базу
- Когда Redis переполняется
- Когда кэш хранит слишком много ключей
- Когда база падает из-за нехватки памяти
* Правильный ответ: Когда много запросов одновременно попадают на истёкший ключ и все идут в базу
Защита: блокировка через SETNX или фоновое обновление ключа.

Зачем нужен pipeline?
- Чтобы шифровать данные
- Чтобы отправить много команд одним сетевым обменом
- Чтобы очистить кэш
- Чтобы автоматически задавать TTL
* Правильный ответ: Чтобы отправить много команд одним сетевым обменом
Pipeline сокращает число сетевых кругосветов и сильно ускоряет пакетные операции.

Что делать, если Redis недоступен?
- Уронить приложение
- Читать базу напрямую — мягкая деградация
- Перезапустить Redis автоматически
- Игнорировать ошибки и вернуть пустоту
* Правильный ответ: Читать базу напрямую — мягкая деградация
Вызовы к Redis оборачиваются в try/except, и при сбое данные читаются из базы.
<!--/QUIZ-->
