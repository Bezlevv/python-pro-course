---
title: HTTP-клиент requests
summary: Библиотека requests: GET и POST-запросы, параметры, заголовки, работа с JSON и обработка ошибок.
order: 2
duration: 35 мин
difficulty: intermediate
---

В прошлом уроке мы делали запросы встроенным модулем `urllib.request`. Он работает, но для серьёзной работы неудобен: многословный, с ним неудобно передавать параметры и JSON. Библиотека `requests` — стандарт де-факто для HTTP в Python. Ею пользуются миллионы разработчиков, и сейчас ты научишься ей пользоваться.

## Установка

Библиотека не входит в стандартную поставку Python — установи её командой:

```bash
pip install requests
```

Проверить установку можно так:

```python
import requests
print(requests.__version__)
```

## Первый GET-запрос

Всё начинается с функции `requests.get()`:

```python
import requests

r = requests.get("https://httpbin.org/get")
print(r.status_code)   # 200
print(r.text[:200])    # начало тела ответа
```

Ответ сохраняется в объекте Response. `r.status_code` — код статуса, `r.text` — тело ответа как текст.

## Параметры запроса

Чтобы добавить query-параметры, достаточно словаря в аргументе `params`:

```python
r = requests.get(
    "https://httpbin.org/get",
    params={"name": "Аня", "page": 2},
)
print(r.url)  # ...?name=Аня&page=2
```

`requests` сам собирает строку с `?` и `&`, а ещё корректно кодирует кириллицу.

## Ответ в формате JSON

Большинство современных API отдают JSON. Метод `.json()` сразу превращает ответ в Python-структуры:

```python
r = requests.get("https://api.github.com/users/python")
data = r.json()
print(data["public_repos"])  # число публичных репозиториев
```

GitHub API не требует ключа для простых запросов — отличная площадка для тренировки.

## POST и отправка данных

Для отправки данных используется `requests.post()`. Если передать `json=`, библиотека сама сделает JSON-сериализацию и выставит заголовок `Content-Type: application/json`:

```python
r = requests.post(
    "https://httpbin.org/post",
    json={"login": "anya", "age": 25},
)
print(r.json()["json"])  # {'login': 'anya', 'age': 25}
```

## Заголовки и тайм-ауты

Свои заголовки передаются через `headers=`. А `timeout` защищает программу от зависания, если сервер молчит:

```python
r = requests.get(
    "https://api.github.com/users/python",
    headers={"User-Agent": "my-app"},
    timeout=10,
)
```

## Обработка ошибок

Код статуса 4xx или 5xx не роняет программу автоматически — ответ просто считается неуспешным. Проверить результат помогает `raise_for_status()`:

```python
r = requests.get("https://httpbin.org/status/404")
print(r.status_code)      # 404
r.raise_for_status()      # бросит исключение
```

## Итог

`requests` закрывает почти все потребности HTTP-клиента: GET и POST, параметры, заголовки, JSON, тайм-ауты и контроль ошибок. Закрепим навык на реальном API.

<!--TASK-->
**Задача.** Напиши программу `todos.py`, которая:

1. Получает список задач с `https://jsonplaceholder.typicode.com/todos` (это бесплатный учебный API);
2. Выводит заголовки только выполненных задач (поле `completed` равно `True`);
3. В конце печатает строку вида `Выполнено: 100 из 200`.

Ожидаемый результат: сначала список заголовков — по одному на строку, затем итоговая строка с количеством. Для превращения ответа в Python-структуру используй метод `.json()` — он вернёт список словарей.
<!--/TASK-->

<!--HINT-->
Ответ API — это список словарей. Получи его методом `.json()`, затем отфильтруй элементы через генератор списка: `[t for t in todos if t["completed"]]`. Количество элементов считай функцией `len()`.
<!--/HINT-->

<!--SOLUTION-->
Решение:

```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = r.json()  # список словарей

completed = [todo for todo in todos if todo["completed"]]
for todo in completed:
    print(todo["title"])

print(f"Выполнено: {len(completed)} из {len(todos)}")
```

Разбор по шагам:

- `requests.get(...)` отправляет GET-запрос к учебному API и возвращает объект Response.
- `r.json()` разбирает JSON-ответ в список словарей — каждая задача содержит поля `title`, `completed`, `id`. Этот шаг обязателен: без него данные остались бы просто текстом.
- Генератор списка `[todo for todo in todos if todo["completed"]]` проходит по всем задачам и оставляет только те, где `completed` — истина (`True`). Заметь: мы читаем значение по ключу в каждом словаре.
- Цикл `for` печатает заголовки выполненных задач.
- Последняя строка использует f-строку: `len(completed)` — сколько задач выполнено, `len(todos)` — их общее число. Стойл `{}` внутри строки подставляет значения переменных.

Запуск: `python todos.py`.
<!--/SOLUTION-->
