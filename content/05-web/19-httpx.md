---
title: httpx: современный HTTP-клиент
summary: Современная библиотека httpx: синхронные и асинхронные запросы, клиент с повторным использованием соединений, таймауты, перенаправления и тестирование без сети.
order: 19
duration: 45 мин
difficulty: intermediate
tags: httpx, http, запросы, api, pytest
---

`requests` — отличная библиотека, но индустрия двинулась дальше. `httpx` — это современный HTTP-клиент, который умеет и синхронные, и асинхронные запросы, поддерживает HTTP/2 и предоставляет удобные средства для тестирования без реальной сети. Если тебе предстоит новый проект — это разумный выбор по умолчанию.

Установка: `pip install "httpx[http2]"`.

## Простой запрос

```python
import httpx

response = httpx.get("https://example.com")
print(response.status_code)   # 200
print(response.text[:50])     # начало HTML-страницы
print(response.headers["content-type"])
```

`response.text` — декодированный текст, `response.json()` — JSON как словарь, `response.content` — сырые байты. Обрати внимание: в отличие от `requests`, **по умолчанию httpx не следует перенаправлениям** и не имеет таймаута. Это осознанный выбор библиотеки: явное лучше неявного.

```python
response = httpx.get("https://httpbin.org/redirect/2", follow_redirects=True)
print(response.url)  # конечный URL после редиректов
```

## Параметры и заголовки

```python
response = httpx.get(
    "https://httpbin.org/get",
    params={"q": "python", "page": 2},
    headers={"User-Agent": "MyApp/1.0"},
    timeout=10.0,
)
print(response.json()["args"])  # {'q': 'python', 'page': '2'}
```

## Клиент: повторное использование соединений

Каждый вызов `httpx.get()` открывает новое соединение. В приложении, делающем много запросов, лучше использовать `Client` — он держит пул соединений, переиспользует их и позволяет задать общие настройки.

```python
with httpx.Client(base_url="https://httpbin.org", timeout=5.0) as client:
    r1 = client.get("/get")
    r2 = client.post("/post", json={"name": "Аня"})
    print(r2.json()["json"])
```

`client.post(..., json=...)` сам сериализует словарь в JSON и ставит заголовок `Content-Type`.

## Ошибки и таймауты

```python
try:
    response = httpx.get("https://httpbin.org/status/404")
    response.raise_for_status()  # поднимет ошибку при статусе >= 400
except httpx.HTTPStatusError as exc:
    print(f"Ошибка HTTP: {exc.response.status_code}")
```

`timeout` принимает число секунд или кортеж `(connect, read, write, pool)`. При превышении поднимается `httpx.TimeoutException`.

## Асинхронный режим

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            client.get("https://httpbin.org/get"),
            client.get("https://httpbin.org/uuid"),
        )
        for r in results:
            print(r.status_code)

asyncio.run(main())
```

`AsyncClient` использует те же методы, но с `await`. Это незаменимо, когда запросов много: они выполняются параллельно, а не по очереди.

## Тестирование без сети: MockTransport

Лучшее свойство httpx для разработчика — встроенный `MockTransport`. Он позволяет подменить сеть объектом, который отвечает на запросы, не выходя в интернет. На этом строятся быстрые и стабильные тесты.

```python
import httpx

def handler(request):
    return httpx.Response(200, json={"hello": "world"})

transport = httpx.MockTransport(handler)

with httpx.Client(transport=transport) as client:
    response = client.get("https://any-url.example")
    print(response.json())  # {'hello': 'world'}
```

Обработчик получает объект `request` и может смотреть на его `method`, `url`, `headers`, `content` — и отвечать по-разному в зависимости от них.

## Итог

- `httpx.get` — быстрый старт; `Client` — для серьёзной работы.
- Не забывай `timeout` и `follow_redirects` — у httpx свои значения по умолчанию.
- `AsyncClient` с `asyncio.gather` даёт параллельность.
- `MockTransport` делает тесты независимыми от сети.

<!--TASK-->
### Задача 1
Напиши функцию `fetch_title(url)`, которая запрашивает страницу через `httpx.get`, включает `follow_redirects=True` и таймаут 5 секунд, и возвращает кортеж `(status_code, content_type)` на основе `response.status_code` и `response.headers["content-type"]`. Проверь её на адресе `https://httpbin.org/get`. Выведи результат на экран.

### Задача 2
Используя `Client` с `base_url="https://httpbin.org"`, отправь POST-запрос на `/post` с `json={"title": "Python", "level": 3}`. Выведи значения `json` из ответа (то, что сервер получил) и `status_code`. Затем проверь обработку ошибок: выполни запрос на `/status/404` и перехвати `httpx.HTTPStatusError`, выведя код ошибки.

### Задача 3
Напиши асинхронную функцию `fetch_all(urls)`, которая через `AsyncClient` и `asyncio.gather` запрашивает все адреса списка параллельно и возвращает список кодов состояния. Проверь на трёх адресах `https://httpbin.org/status/200`, `/status/201`, `/status/204` и выведи результат. Запусти через `asyncio.run`.

### Задача 4
Напиши pytest-тест для функции `get_user(client, user_id)`:

```python
def get_user(client, user_id):
    response = client.get(f"/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

Используй `httpx.MockTransport`: обработчик должен возвращать `200` с `{"id": user_id, "name": "Аня"}` для `/users/1` и `404` для любого другого id. Проверь, что `get_user` возвращает словарь с именем для id=1, и что для id=2 поднимается `httpx.HTTPStatusError`.

### Задача 5
Напиши pytest-тест с параметризацией: `@pytest.mark.parametrize("status, expected", [(200, True), (301, True), (404, False)])`. Функция `is_ok(client, path)` возвращает `True`, если `response.status_code < 400`, иначе `False`. Используй `MockTransport`, который возвращает статус из пути запроса (например, `/status/404` → `404`). Тест должен проходить для всех трёх пар.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Импортируй `httpx`, вызови `httpx.get(url, follow_redirects=True, timeout=5.0)`. Заголовок читается через `response.headers["content-type"]` — он есть у любого ответа.

### Подсказка 2
`Client` открывается через `with`. Для POST: `client.post("/post", json={...})`. Ошибку лови через `except httpx.HTTPStatusError as exc:` и печатай `exc.response.status_code`.

### Подсказка 3
`async with httpx.AsyncClient() as client:` внутри функции, затем `await asyncio.gather(*[client.get(u) for u in urls])`. Коды — `[r.status_code for r in results]`. Запуск: `asyncio.run(fetch_all(urls))`.

### Подсказка 4
В обработчике смотри `request.url.path`: если он равен `/users/1` — верни `httpx.Response(200, json={...})`, иначе — `httpx.Response(404)`. Создай клиент: `httpx.Client(transport=httpx.MockTransport(handler))`. Для проверки ошибки используй `pytest.raises(httpx.HTTPStatusError)`.

### Подсказка 5
Обработчик читает `request.url.path`, извлекает число из `/status/<code>` и возвращает `httpx.Response(int(code))`. Параметризация подставит пары в сигнатуру теста; создавай клиент внутри теста для свежего транспорта.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
import httpx

def fetch_title(url):
    response = httpx.get(url, follow_redirects=True, timeout=5.0)
    return response.status_code, response.headers["content-type"]

print(fetch_title("https://httpbin.org/get"))
# (200, 'application/json')
```

`follow_redirects=True` включает прохождение перенаправлений, `timeout=5.0` задаёт таймаут. `response.status_code` и `response.headers["content-type"]` — обычные свойства ответа. Вернуть кортеж удобно: вызывающий код сам решит, что с ним делать.

### Разбор 2
```python
import httpx

with httpx.Client(base_url="https://httpbin.org", timeout=5.0) as client:
    r = client.post("/post", json={"title": "Python", "level": 3})
    print(r.status_code)          # 200
    print(r.json()["json"])       # {'title': 'Python', 'level': 3}

    try:
        bad = client.get("/status/404")
        bad.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Ошибка HTTP: {exc.response.status_code}")  # 404
```

`Client` переиспользует соединения и задаёт общие `timeout`. `json=` в POST сам сериализует словарь, а сервер эхо-возвращает его в поле `json`. `raise_for_status()` превращает любой статус 4xx/5xx в `httpx.HTTPStatusError`, которую можно перехватить и обработать.

### Разбор 3
```python
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[client.get(u) for u in urls])
        return [r.status_code for r in results]

print(asyncio.run(fetch_all([
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/201",
    "https://httpbin.org/status/204",
])))
# [200, 201, 204]
```

`AsyncClient` использует те же методы, что и синхронный `Client`, но с `await`. `asyncio.gather` запускает все запросы одновременно — суммарное время равно времени самого медленного, а не сумме. Это главный выигрыш асинхронного клиента.

### Разбор 4
```python
import httpx
import pytest

def get_user(client, user_id):
    response = client.get(f"/users/{user_id}")
    response.raise_for_status()
    return response.json()

def handler(request):
    if request.url.path == "/users/1":
        return httpx.Response(200, json={"id": 1, "name": "Аня"})
    return httpx.Response(404)

def test_get_user_ok():
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = get_user(client, 1)
    assert result["name"] == "Аня"

def test_get_user_missing():
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(httpx.HTTPStatusError):
            get_user(client, 2)
```

`MockTransport` заменяет сеть функцией-обработчиком. Первый тест проверяет успешный сценарий: обработчик возвращает `200` и JSON для `/users/1`. Второй тест ожидает ошибку: для `/users/2` возвращается `404`, `raise_for_status()` поднимает `httpx.HTTPStatusError`, и `pytest.raises` подтверждает это. Тесты не касаются сети и работают мгновенно.

### Разбор 5
```python
import httpx
import pytest

def is_ok(client, path):
    response = client.get(path)
    return response.status_code < 400

def handler(request):
    code = int(request.url.path.split("/")[-1])
    return httpx.Response(code)

@pytest.mark.parametrize("status, expected", [(200, True), (301, True), (404, False)])
def test_is_ok(status, expected):
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        assert is_ok(client, f"/status/{status}") is expected
```

Обработчик достаёт код статуса из последнего сегмента пути (например, `/status/404` → `404`) и возвращает ответ с этим статусом. Параметризация прогоняет один и тот же тест для трёх пар «статус → ожидание». Так один короткий тест покрывает и успех, и перенаправление, и ошибку — без единого реального запроса.
<!--/SOLUTION-->

<!--QUIZ-->
Что вернёт response.json(), если сервер ответил JSON-ом?
- Строку
- Словарь (или список) из декодированного JSON
- Байты
- HTML
* Правильный ответ: Словарь (или список) из декодированного JSON
response.json() декодирует тело ответа из JSON в типы Python.

Как в httpx включить следование перенаправлениям?
- follow_redirects=True
- redirects=True
- allow_redirects=True
- Оно включено по умолчанию
* Правильный ответ: follow_redirects=True
В отличие от requests, httpx по умолчанию не следует редиректам — параметр называется follow_redirects.

Для чего нужен объект Client?
- Только для POST-запросов
- Чтобы переиспользовать соединения и задавать общие настройки
- Чтобы шифровать запросы
- Чтобы отключить таймауты
* Правильный ответ: Чтобы переиспользовать соединения и задавать общие настройки
Client держит пул соединений и применяет base_url, timeout и другие настройки ко всем запросам.

Что делает response.raise_for_status()?
- Ничего
- Поднимает ошибку при статусе 4xx/5xx
- Возвращает статус
- Меняет статус на 200
* Правильный ответ: Поднимает ошибку при статусе 4xx/5xx
При статусе 400 или выше метод бросает httpx.HTTPStatusError.

Какой класс нужен для асинхронных запросов?
- httpx.AsyncClient
- httpx.Client
- httpx.Async
- asyncio.Client
* Правильный ответ: httpx.AsyncClient
AsyncClient работает с await и сочетается с asyncio.gather.

Что делает httpx.MockTransport?
- Шифрует трафик
- Подменяет сеть функцией-обработчиком для тестов
- Ускоряет запросы
- Кэширует ответы
* Правильный ответ: Подменяет сеть функцией-обработчиком для тестов
Обработчик получает request и возвращает Response — тесты идут без интернета.

Что вернёт httpx.get("https://httpbin.org/status/404") без raise_for_status()?
- Ошибку
- Response со статусом 404
- None
- Пустую строку
* Правильный ответ: Response со статусом 404
Сам по себе запрос не бросает ошибку: 404 — это обычный ответ, пока ты не вызовешь raise_for_status().

Как передать тело JSON в POST через httpx?
- json={"key": "value"}
- data='{"key": "value"}'
- body={"key": "value"}
- form={"key": "value"}
* Правильный ответ: json={"key": "value"}
Параметр json сам сериализует словарь и ставит Content-Type: application/json.

Что произойдёт при превышении таймаута?
- Вернётся пустой ответ
- Поднимется httpx.TimeoutException
- Запрос повторится
- Ничего
* Правильный ответ: Поднимется httpx.TimeoutException
Таймаут задаётся параметром timeout; при его превышении клиент бросает TimeoutException.

Чем AsyncClient отличается от Client?
- Только именами методов
- Методами с await: запросы можно запускать параллельно
- AsyncClient не умеет GET
- AsyncClient работает только в Jupyter
* Правильный ответ: Методами с await: запросы можно запускать параллельно
AsyncClient использует корутины: сочетание с asyncio.gather даёт параллельное выполнение запросов.
<!--/QUIZ-->
