---
title: Кэширование и идемпотентность
summary: Стратегии кэширования (cache-aside, TTL, write-through), защита от прострела и лавины, идемпотентные операции и ключи идемпотентности.
order: 6
duration: 45 мин
difficulty: advanced
tags: кэш, идемпотентность, ttl, cache-aside, прострел, retry
---

Кэширование и идемпотентность — две техники, которые делают системы быстрыми и надёжными под нагрузкой. Первая ускоряет чтение, вторая защищает от двойных платежей и повторных запросов.

## Кэширование: паттерн cache-aside

Самый распространённый паттерн — **cache-aside** (ленивое кэширование): сначала смотрим в кэш; если есть (hit) — возвращаем; если нет (miss) — читаем из базы, кладём в кэш и возвращаем. В Python легко показать с словарём как «кэшем»:

```python
import time

class Cache:
    def __init__(self, ttl=5.0):
        self.store = {}
        self.ttl = ttl

    def get(self, key):
        item = self.store.get(key)
        if item is None:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            del self.store[key]
            return None
        return value

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)
```

TTL (time-to-live) гарантирует, что данные устареют даже без явной инвалидации.

Схема cache-aside для базы:

```python
def get_user(user_id, cache, db):
    key = f"user:{user_id}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    row = db.get(user_id)          # тяжёлый запрос
    if row is not None:
        cache.set(key, row)
    return row
```

## Write-through и write-back

Кроме cache-aside есть стратегии записи. **Write-through**: при записи в базу сразу пишем и в кэш — кэш всегда свежий, но запись дороже. **Write-back**: пишем только в кэш, а в базу сбрасываем асинхронно — быстро, но есть риск потерять данные при падении. Для большинства случаев cache-aside + TTL достаточно.

## Прострел и лавина

- **Кэш-прострел (cache stampede)**: ключ истёк, и десятки запросов одновременно проваливаются в базу. Лечится «single flight» — только один поток идёт в базу, остальные ждут его результат.
- **Лавина (cache avalanche)**: массовое протухание ключей одновременно — все запросы бьют в базу. Лечится джиттером TTL (случайное небольшое отклонение) и предварительным прогревом.

Single flight на одном процессе — это просто блокировка:

```python
import threading

lock = threading.Lock()
inflight = {}

def get_or_load(key, load):
    with lock:
        if key in inflight:
            return inflight[key]
        inflight[key] = load()
    return inflight[key]
```

(В многопроцессных системах используются распределённые блокировки, например, на Redis.)

## Идемпотентность

Идемпотентная операция — та, которую можно выполнить несколько раз, и результат будет как от одного выполнения. В HTTP это `GET`, `PUT`, `DELETE`. А вот `POST` (создание) идемпотентным не является: двойной клик по кнопке «Оплатить» создаст два платежа.

Решение — **ключ идемпотентности**: клиент отправляет уникальный `Idempotency-Key` в заголовке; сервер запоминает ключ и результат первой обработки и для повторного запроса с тем же ключом возвращает сохранённый результат:

```python
class IdempotentHandler:
    def __init__(self):
        self.results = {}

    def handle(self, key, operation):
        if key in self.results:
            return self.results[key], "повтор"
        result = operation()
        self.results[key] = result
        return result, "первично"
```

Дубликаты можно распознавать и по бизнес-признаку (например, `order_id` в теле запроса), но ключ — самый общий механизм. Главное правило: ключ должен быть уникальным для логической операции, и ответы должны храниться достаточно долго, чтобы покрыть окно повторных запросов.

<!--TASK-->
### Задача 1
Реализуй cache-aside с TTL. Напиши класс `Cache` (как в теории) и функцию `get_user(user_id, cache, db)`, где `db` — словарь «базы данных» с пользователями. Первый запрос должен идти в базу (печать `База: user 1`), второй — из кэша (печать `Кэш: user 1`). Для проверки вставь в `db` пользователя `{1: {"name": "Аня"}}`. Ожидаемый вывод: сначала строка `База: user 1`, затем `Кэш: user 1`.

### Задача 2
Реализуй защиту от кэш-прострела (single flight). Напиши функцию `single_flight(key, load, lock, inflight)`, где `inflight` — словарь «в полёте», `lock` — `threading.Lock()`. Функция должна: если `key` уже в `inflight` — вернуть его результат; иначе выполнить `load()` (печатает `Загрузка...`), сохранить результат и вернуть. Вызови её дважды с одним ключом — «Загрузка...» должна напечататься ровно один раз. Ожидаемый вывод: `Загрузка...` и `42` дважды (строки: `Загрузка...`, `Результат: 42`, `Результат: 42`).

### Задача 3
Сделай write-through кэш. Класс `WriteThroughCache` принимает `cache` и `db`; метод `set(key, value)` пишет и в базу, и в кэш; метод `get(key)` читает из кэша. Проверь: `set("user:1", {"name": "Аня"})`, затем `get("user:1")`, а затем напрямую проверь, что значение есть в `db`. Ожидаемый вывод: `Из кэша: {'name': 'Аня'}` и `В базе: {'name': 'Аня'}`.

### Задача 4
Реализуй идемпотентный обработчик оплаты. Класс `PaymentHandler` с ключом в ключе `IdempotentHandler` (как в теории): метод `charge(key, amount)` возвращает кортеж `(result, tag)`, где `tag` — `"первично"` или `"повтор"`. Оба вызова с одним ключом должны вернуть одинаковый результат (например, `{"status": "ok", "amount": 100}`), но тег у второго — `"повтор"`. Ожидаемый вывод: `первично`, `повтор`.

### Задача 5
Реализуй кэш с джиттером TTL для защиты от лавины. Класс `JitterCache` — наследник `Cache` из задачи 1, но в `set` добавляет к TTL случайное число от 0 до `jitter` (0.5). Напиши проверку: создай кэш с `ttl=1.0`, `jitter=0.5`, положи ключ и выведи `store[key]` — значение должно храниться с `expires_at`, бóльшим `time.time()`, а разница между `expires_at` и `time.time()` должна быть между 1.0 и 1.5. Ожидаемый вывод: `True` (проверка диапазона).
<!--/TASK-->

<!--HINT-->
### Подсказка 1
В `get_user` печатай `База: user {user_id}` перед обращением к `db` и `Кэш: user {user_id}` при попадании. В `db` храни данные, а в `cache` — уже после первого чтения. Не забудь `import time` для TTL.

### Подсказка 2
`single_flight` должна работать так: `with lock: if key in inflight: return inflight[key]`; иначе `result = load(); with lock: inflight[key] = result; return result`. Лямбда `load` печатает `Загрузка...` и возвращает 42. Второй вызов должен вернуть 42, не загружая снова.

### Подсказка 3
Метод `set` сразу пишет в `cache.store[key]` (можно без TTL) и в `db[key]`. Метод `get` возвращает `self.cache.get(key)`. Для проверки базы напечатай `db` напрямую.

### Подсказка 4
В `charge` проверяй `if key in self.results: return self.results[key], "повтор"`; иначе выполни оплату (просто верни словарь), сохрани в `self.results[key]` и верни `(result, "первично")`.

### Подсказка 5
В `set` переопредели: `expires_at = time.time() + self.ttl + random.uniform(0, self.jitter)`. Проверка: `now = time.time()`; вычисли `expires_at` из `cache.store["k"]`; печатай `1.0 <= expires_at - now <= 1.5`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import time

class Cache:
    def __init__(self, ttl=5.0):
        self.store = {}
        self.ttl = ttl

    def get(self, key):
        item = self.store.get(key)
        if item is None:
            return None
        value, expires_at = item
        if time.time() > expires_at:
            del self.store[key]
            return None
        return value

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)

def get_user(user_id, cache, db):
    key = f"user:{user_id}"
    cached = cache.get(key)
    if cached is not None:
        print(f"Кэш: {key}")
        return cached
    print(f"База: {key}")
    row = db.get(user_id)
    if row is not None:
        cache.set(key, row)
    return row

db = {1: {"name": "Аня"}}
cache = Cache()
get_user(1, cache, db)
get_user(1, cache, db)
```

Вывод:

```
База: user 1
Кэш: user 1
```

Что здесь происходит? Первый вызов промахивается мимо кэша, читает базу и кладёт результат в кэш. Второй попадает в кэш. Так база получает только один тяжёлый запрос вместо двух — суть cache-aside.

### Разбор 2
Решение:

```python
import threading

lock = threading.Lock()
inflight = {}

def single_flight(key, load, lock, inflight):
    with lock:
        if key in inflight:
            return inflight[key]
    result = load()
    with lock:
        inflight[key] = result
    return result

def load():
    print("Загрузка...")
    return 42

r1 = single_flight("user:1", load, lock, inflight)
r2 = single_flight("user:1", load, lock, inflight)
print(f"Результат: {r1}")
print(f"Результат: {r2}")
```

Вывод:

```
Загрузка...
Результат: 42
Результат: 42
```

Что здесь происходит? Первый вызов выполняет `load()` один раз, второй находит ключ в `inflight` и сразу возвращает сохранённый результат. Даже если 50 запросов придут одновременно после протухания кэша, базу ударит только один — это защита от прострела.

### Разбор 3
Решение:

```python
class WriteThroughCache:
    def __init__(self, cache, db):
        self.cache = cache
        self.db = db

    def set(self, key, value):
        self.cache.store[key] = (value, float("inf"))
        self.db[key] = value

    def get(self, key):
        return self.cache.get(key)

db = {}
cache = Cache()
wt = WriteThroughCache(cache, db)
wt.set("user:1", {"name": "Аня"})
print(f"Из кэша: {wt.get('user:1')}")
print(f"В базе: {db['user:1']}")
```

Вывод:

```
Из кэша: {'name': 'Аня'}
В базе: {'name': 'Аня'}
```

Что здесь происходит? Write-through пишет в оба места сразу: кэш всегда свежий после записи, и база не расходится с кэшем. Цена — каждая запись стоит как запись в базу плюс запись в кэш.

### Разбор 4
Решение:

```python
class PaymentHandler:
    def __init__(self):
        self.results = {}

    def charge(self, key, amount):
        if key in self.results:
            return self.results[key], "повтор"
        result = {"status": "ok", "amount": amount}
        self.results[key] = result
        return result, "первично"

handler = PaymentHandler()
print(handler.charge("pay-42", 100)[1])
print(handler.charge("pay-42", 100)[1])
```

Вывод:

```
первично
повтор
```

Что здесь происходит? Первый вызов выполняет оплату и запоминает результат за ключом `pay-42`. Второй с тем же ключом не списывает деньги повторно, а возвращает тот же результат с тегом `повтор`. Это защищает от двойной оплаты при сетевых повторах или двойном клике.

### Разбор 5
Решение:

```python
import time
import random

class JitterCache(Cache):
    def __init__(self, ttl=5.0, jitter=0.5):
        super().__init__(ttl)
        self.jitter = jitter

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl + random.uniform(0, self.jitter))

cache = JitterCache(ttl=1.0, jitter=0.5)
cache.set("k", "v")
expires_at = cache.store["k"][1]
now = time.time()
print(1.0 <= expires_at - now <= 1.5)
```

Вывод: `True`. Что здесь происходит? Каждый ключ получает свой чуть-чуть разный срок жизни: ключи истекают не одновременно, а «размазаны» по интервалу. Это снижает вероятность лавины, когда все ключи протухают разом и база получает удар от всех запросов сразу.
<!--/SOLUTION-->

<!--QUIZ-->
Что происходит при «промахе» (miss) в cache-aside?
- Возвращается ошибка
- Данные читаются из базы и кладутся в кэш
- Кэш очищается
- Запрос игнорируется
* Правильный ответ: Данные читаются из базы и кладутся в кэш
После чтения из базы результат сохраняется в кэш с TTL.

Зачем нужен TTL?
- Чтобы ключи автоматически устаревали
- Чтобы ускорить запись
- Чтобы запретить чтение
- Чтобы искать ключи
* Правильный ответ: Чтобы ключи автоматически устаревали
TTL гарантирует, что устаревшие данные не будут жить вечно.

Что такое кэш-прострел?
- Все ключи протухают одновременно
- Много запросов одновременно проваливаются в базу после истечения ключа
- Медленная сеть
- Ошибка в коде
* Правильный ответ: Много запросов одновременно проваливаются в базу после истечения ключа
Против этого помогает single flight — только один поток загружает данные.

Какой метод HTTP идемпотентный?
- POST
- GET
- PATCH (в общем случае нет)
- Никакой
* Правильный ответ: GET
GET, PUT и DELETE безопасно повторять; POST — нет.

Что делает ключ идемпотентности?
- Позволяет серверу распознать повторный запрос и вернуть сохранённый результат
- Шифрует запрос
- Ускоряет базу
- Меняет метод HTTP
* Правильный ответ: Позволяет серверу распознать повторный запрос и вернуть сохранённый результат
Повторная оплата с тем же ключом не списывает деньги дважды.

Как защититься от лавины?
- Добавить джиттер к TTL и прогревать ключи
- Убрать кэш совсем
- Увеличить базу в 10 раз
- Отключить TTL
* Правильный ответ: Добавить джиттер к TTL и прогревать ключи
Ключи протухают вразнобой, и нагрузка на базу распределяется.
<!--/QUIZ-->
