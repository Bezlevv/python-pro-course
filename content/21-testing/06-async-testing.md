---
title: Тестирование асинхронного кода
summary: Пишем тесты для async-функций: pytest-asyncio, AsyncMock, асинхронные фикстуры, таймауты и проверка параллельных операций.
order: 6
duration: 45 мин
difficulty: advanced
tags: pytest-asyncio, асинхронность, AsyncMock, таймауты
---

Код на `async`/`await` нельзя тестировать как обычный: тестовая функция тоже должна быть асинхронной, а событийный цикл нужно подготовить заранее. В этом уроке разберём, как это делать с помощью `pytest-asyncio` и `AsyncMock`.

## pytest-asyncio: асинхронные тесты

Установка:

```bash
pip install pytest-asyncio
```

После этого можно писать тесты, которые объявляются как `async def` и помечаются `@pytest.mark.asyncio`:

```python
import asyncio
import pytest

async def slow_add(a, b):
    await asyncio.sleep(0.01)
    return a + b

@pytest.mark.asyncio
async def test_slow_add():
    assert await slow_add(1, 2) == 3
```

pytest-asyncio сам создаёт событийный цикл, запускает в нём корутину-тест и убирает цикл после. Параметр `loop_scope` в маркере позволяет управлять временем жизни цикла: `@pytest.mark.asyncio(loop_scope="session")` переиспользует один цикл на все тесты сессии (удобно для медленных фикстур).

## async-функции без маркера

Если тест синхронный, но нужно вызвать одну async-функцию, используй `asyncio.run()`:

```python
def test_slow_add_sync():
    assert asyncio.run(slow_add(1, 2)) == 3
```

`asyncio.run()` создаёт новый цикл, выполняет корутину и закрывает цикл. Это простой приём для точечных проверок.

## AsyncMock

Для асинхронных зависимостей (например, `client.get` из HTTP-клиента) обычный `MagicMock` не подходит: `await mock.get(url)` упадёт, потому что `MagicMock` возвращает не корутину. Решение — `AsyncMock` из `unittest.mock`:

```python
from unittest.mock import AsyncMock

async def fetch_data(client, url):
    return await client.get(url)

def test_fetch_data():
    client = AsyncMock()
    client.get.return_value = "ok"
    assert asyncio.run(fetch_data(client, "/data")) == "ok"
```

`AsyncMock` возвращает awaitable, поэтому `await client.get(url)` работает. Можно даже задавать `side_effect` с исключениями — например, чтобы протестировать обработку сбоя сети.

## Асинхронные фикстуры

Фикстуры тоже могут быть асинхронными — `async def` с `@pytest.fixture`, и pytest-asyncio корректно их запустит:

```python
@pytest.fixture
async def client():
    c = make_client()
    yield c
    await c.close()
```

Тест-корутина получает такую фикстуру как обычный параметр.

## Таймауты

Асинхронный код часто работает с сетью, и важно проверять поведение при зависаниях. Контекстный менеджер `asyncio.timeout` (Python 3.11+) ограничивает время выполнения и бросает `asyncio.TimeoutError`:

```python
async def hang():
    await asyncio.sleep(10)

@pytest.mark.asyncio
async def test_hang_timeout():
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.01):
            await hang()
```

Если код не уложился в таймаут — тест это фиксирует. Это основа проверки «не зависает ли наш код».

## Параллельность: asyncio.gather

`asyncio.gather` выполняет корутины параллельно. Свойство для проверки: результат собирается в том же порядке, что и переданные корутины:

```python
async def collect(ids):
    return await asyncio.gather(*(fetch(i) for i in ids))
```

Тест проверяет, что порядок результатов совпадает с порядком `ids` — это контракт `gather`.

## Итог

Для асинхронных тестов нужен `pytest-asyncio` с маркером `@pytest.mark.asyncio`, для подмены асинхронных зависимостей — `AsyncMock`, а для проверки таймаутов — `asyncio.timeout`.

Теперь закрепим всё практикой.

<!--TASK-->
### Задача 1
Напиши async-функцию `greet_async(name)`, которая делает `await asyncio.sleep(0.01)` и возвращает `f"Привет, {name}!"`. Создай тест `test_greet_async` с `@pytest.mark.asyncio`, который проверяет, что `await greet_async("Аня") == "Привет, Аня!"`. Установи `pytest-asyncio`, запусти pytest — должно быть `1 passed`.

### Задача 2
Напиши синхронный тест `test_greet_sync`, который вызывает `greet_async` через `asyncio.run()`, без маркера `@pytest.mark.asyncio`. Проверь тот же результат. Запусти — должно быть `2 passed` (два теста из задач 1 и 2).

### Задача 3
Напиши async-функцию `fetch_data(client, url)`, которая возвращает `await client.get(url)`. Создай тест с `AsyncMock`: назначь `client.get.return_value = "ok"`, вызови `fetch_data` через `asyncio.run` и проверь, что результат равен `"ok"`, а `client.get.assert_called_once_with("/data")`. Запусти — `3 passed` (все три теста).

### Задача 4
Напиши async-функцию `fetch_with_timeout(client, url, timeout)`, которая оборачивает вызов `await client.get(url)` в `async with asyncio.timeout(timeout)`. Создай тест: `AsyncMock` с `client.get.side_effect = asyncio.TimeoutError()`, и проверь через `pytest.raises(asyncio.TimeoutError)`, что вызов `fetch_with_timeout(client, "/data", 1)` бросает таймаут. Запусти — `4 passed`.

### Задача 5
Напиши async-функцию `fetch_all(ids)`, которая собирает результаты через `asyncio.gather(*(fetch(i) for i in ids))`, где `fetch(i)` — это `async` функция, возвращающая `f"data-{i}"`. Напиши тест: передай `[1, 2, 3]` и проверь, что результат равен `["data-1", "data-2", "data-3"]` — порядок сохраняется. Запусти — `5 passed`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Не забудь `pip install pytest-asyncio`. Тест объявляется `async def test_greet_async():` с декоратором `@pytest.mark.asyncio`. Внутри — `assert await greet_async("Аня") == "Привет, Аня!"`. Событийный цикл создаст pytest-asyncio автоматически.

### Подсказка 2
Синхронный тест — обычная `def` без декоратора. Внутри вызови `asyncio.run(greet_async("Аня"))`. Обрати внимание: `asyncio.run` создаёт новый цикл и закрывает его после выполнения.

### Подсказка 3
`from unittest.mock import AsyncMock`. Создай `client = AsyncMock()`, назначь `client.get.return_value = "ok"`. Вызов `fetch_data` — через `asyncio.run(fetch_data(client, "/data"))`, так как тест синхронный. После вызова проверь `client.get.assert_called_once_with("/data")`.

### Подсказка 4
`asyncio.timeout(timeout)` — контекстный менеджер: `async with asyncio.timeout(timeout):`. Он бросает `asyncio.TimeoutError`, если внутренний код не успел. Для проверки используй `with pytest.raises(asyncio.TimeoutError):` вокруг вызова через `asyncio.run`.

### Подсказка 5
`fetch` — вспомогательная async-функция: `async def fetch(i): return f"data-{i}"`. `asyncio.gather(*(fetch(i) for i in ids))` принимает корутины через распаковку `*`. В тесте сравни `asyncio.run(fetch_all([1, 2, 3]))` с `["data-1", "data-2", "data-3"]`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import asyncio
import pytest

async def greet_async(name):
    await asyncio.sleep(0.01)
    return f"Привет, {name}!"

@pytest.mark.asyncio
async def test_greet_async():
    assert await greet_async("Аня") == "Привет, Аня!"
```

Запуск: `python -m pytest`. Результат: `1 passed`.

Что здесь происходит? Маркер `@pytest.mark.asyncio` сообщает pytest-asyncio, что тест — корутину и её нужно выполнить в событийном цикле. pytest-asyncio создаёт цикл, запускает в нём тест и после завершения убирает его. Функция `greet_async` имитирует реальную асинхронную работу через `asyncio.sleep(0.01)` — настоящий ввод-вывод (сеть, диск) ведёт себя похоже: код ждёт, не блокируя основной поток. Тест корректно `await`-ит вызов и сравнивает результат.

### Разбор 2
Решение:

```python
import asyncio
import pytest

async def greet_async(name):
    await asyncio.sleep(0.01)
    return f"Привет, {name}!"

@pytest.mark.asyncio
async def test_greet_async():
    assert await greet_async("Аня") == "Привет, Аня!"

def test_greet_sync():
    assert asyncio.run(greet_async("Аня")) == "Привет, Аня!"
```

Запуск: `python -m pytest`. Результат: `2 passed`.

Что здесь происходит? Синхронный тест `test_greet_sync` не требует маркера: `asyncio.run()` создаёт новый событийный цикл, выполняет корутину `greet_async("Аня")` и закрывает цикл. Это удобно, когда async-функцию нужно проверить точечно из обычного теста. Обрати внимание на разницу: `pytest.mark.asyncio` работает с уже созданным pytest-asyncio циклом, а `asyncio.run` сам управляет жизнью цикла. В одном файле можно смешивать оба подхода — как здесь.

### Разбор 3
Решение:

```python
import asyncio
from unittest.mock import AsyncMock

async def fetch_data(client, url):
    return await client.get(url)

def test_fetch_data():
    client = AsyncMock()
    client.get.return_value = "ok"
    result = asyncio.run(fetch_data(client, "/data"))
    assert result == "ok"
    client.get.assert_called_once_with("/data")
```

Запуск: `python -m pytest`. Результат: `3 passed`.

Что здесь происходит? `AsyncMock` — это асинхронный аналог `MagicMock`: его методы возвращают awaitable, поэтому `await client.get(url)` работает. Обычный `MagicMock` здесь не подошёл бы: `await` на результате `MagicMock` упал бы с ошибкой «object is not awaitable». `client.get.return_value = "ok"` настраивает результат вызова, а `assert_called_once_with("/data")` проверяет, что метод вызван ровно один раз с правильным URL. Так мы изолируем тест от настоящего сетевого клиента.

### Разбор 4
Решение:

```python
import asyncio
import pytest
from unittest.mock import AsyncMock

async def fetch_with_timeout(client, url, timeout):
    async with asyncio.timeout(timeout):
        return await client.get(url)

def test_fetch_timeout():
    client = AsyncMock()
    client.get.side_effect = asyncio.TimeoutError()
    with pytest.raises(asyncio.TimeoutError):
        asyncio.run(fetch_with_timeout(client, "/data", 1))
```

Запуск: `python -m pytest`. Результат: `4 passed`.

Что здесь происходит? `asyncio.timeout(timeout)` — контекстный менеджер: если внутренний код не завершился за отведённое время, он бросает `asyncio.TimeoutError`. В тесте мы имитируем зависание сети: `client.get.side_effect = asyncio.TimeoutError()` заставляет каждый вызов бросать таймаут. Обёртка `pytest.raises(asyncio.TimeoutError)` проверяет, что `fetch_with_timeout` пробрасывает исключение наружу — значит, вызывающий код сможет его обработать. Это классическая проверка устойчивости к зависаниям.

### Разбор 5
Решение:

```python
import asyncio
import pytest

async def fetch(i):
    return f"data-{i}"

async def fetch_all(ids):
    return await asyncio.gather(*(fetch(i) for i in ids))

@pytest.mark.asyncio
async def test_fetch_all():
    result = await fetch_all([1, 2, 3])
    assert result == ["data-1", "data-2", "data-3"]
```

Запуск: `python -m pytest`. Результат: `5 passed`.

Что здесь происходит? `asyncio.gather` принимает корутины и запускает их параллельно. Распаковка `*(fetch(i) for i in ids)` превращает генератор в отдельные аргументы. Важное свойство `gather`: результаты собираются в том же порядке, в котором были переданы корутины, — независимо от того, какая завершилась первой. Тест проверяет именно этот контракт: список `["data-1", "data-2", "data-3"]` соответствует порядку `ids`. Если бы ты написал свою версию параллельной обработки, такое свойство поймало бы ошибку с порядком.
<!--/SOLUTION-->

<!--QUIZ-->
Какой маркер нужен для асинхронного теста в pytest-asyncio?
- @pytest.mark.asyncio
- @pytest.mark.async
- @pytest.mark.coro
* Правильный ответ: @pytest.mark.asyncio
Маркер указывает pytest-asyncio, что тест — это корутину, которую нужно выполнить в событийном цикле.

Как вызвать async-функцию из синхронного теста?
- Через asyncio.run()
- Через await без подготовки
- Через asyncio.sleep()
* Правильный ответ: Через asyncio.run()
asyncio.run() создаёт цикл, выполняет корутину и закрывает цикл.

Почему для асинхронных зависимостей нужен AsyncMock, а не MagicMock?
- MagicMock не существует в Python
- Результат MagicMock не является awaitable, и await упадёт
- AsyncMock быстрее
* Правильный ответ: Результат MagicMock не является awaitable, и await упадёт
AsyncMock возвращает awaitable, поэтому await client.get(url) работает.

Что бросает asyncio.timeout при превышении времени?
- TimeoutError из asyncio
- RuntimeError
- KeyboardInterrupt
* Правильный ответ: TimeoutError из asyncio
Контекстный менеджер asyncio.timeout отменяет выполнение и бросает asyncio.TimeoutError.

В каком порядке asyncio.gather возвращает результаты?
- В порядке завершения корутин
- В порядке передачи корутин
- В случайном порядке
* Правильный ответ: В порядке передачи корутин
gather собирает результаты в том же порядке, в котором переданны корутины.

Что произойдёт с обычным тестом (def), содержащим await?
- Он выполнится корректно
- Произойдёт синтаксическая ошибка, потому что await допустим только внутри async-функции
- Ошибка не возникнет, но await проигнорируется
* Правильный ответ: Произойдёт синтаксическая ошибка
await можно использовать только внутри функций, объявленных с async.

Что делает pytest-asyncio под капотом?
- Создаёт событийный цикл, выполняет тест-корутину и убирает цикл
- Конвертирует async в sync
- Ускоряет тесты
* Правильный ответ: Создаёт событийный цикл, выполняет тест-корутину и убирает цикл
Маркер @pytest.mark.asyncio управляет жизнью цикла вокруг теста.

Как проверить, что async-функция бросает исключение?
- Обернуть вызов в with pytest.raises(...)
- Добавить try/except внутри теста
- Проверить код возврата
* Правильный ответ: Обернуть вызов в with pytest.raises(...)
pytest.raises перехватывает исключение и считает тест успешным, только если оно возникло.
<!--/QUIZ-->
