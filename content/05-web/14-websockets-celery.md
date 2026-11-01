---
title: WebSockets и фоновые задачи
summary: WebSockets для мгновенной связи с клиентом, Celery и RQ для фоновых задач.
order: 14
duration: 45 мин
difficulty: advanced
tags: websockets, celery, rq, redis, async, fastapi
---

Обычный HTTP работает так: клиент просит — сервер отвечает. Но есть задачи, где этого мало. Чат: сообщение должно прийти собеседнику сразу, без его перезагрузки страницы. Уведомления, онлайн-статусы, совместное редактирование — всё это требует постоянного канала связи. А ещё есть задачи, которые не должны тормозить ответ пользователю: отправка писем, генерация отчётов, обработка видео. Обе проблемы решаются на этом уроке.

## WebSockets: постоянный канал

WebSocket — это протокол поверх TCP, который держит соединение открытым: сервер и клиент могут в любой момент отправить сообщение друг другу. Одно соединение вместо сотен HTTP-запросов.

В FastAPI WebSocket описывается через `@app.websocket`:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # принимаем соединение
    while True:
        message = await websocket.receive_text()  # ждём сообщение
        await websocket.send_text(f"Привет, ты написал: {message}")
```

Клиент на стороне браузера — это обычный JavaScript:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");
ws.onopen = () => ws.send("Привет с клиента!");
ws.onmessage = (event) => console.log(event.data);
```

В `ws:`, `await websocket.receive_text()` — ждёт текстовое сообщение с клиента, `await websocket.send_text(...)` — отправляет обратно. Всё асинхронно: пока ждём сообщение, сервер не блокируется и может обслуживать других клиентов.

## Многопользовательский чат

Чтобы сообщение доходило до всех, сервер держит список подключённых сокетов:

```python
connections: list[WebSocket] = []

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for conn in connections:
                await conn.send_text(message)
    finally:
        connections.remove(websocket)
```

Каждое новое подключение попадает в список; когда приходит сообщение, оно рассылается всем. `try/finally` гарантирует, что при разрыве соединения сокет уберётся из списка (иначе отправим сообщение в закрытый сокет и получим ошибку).

## Фоновые задачи: зачем это нужно

Представь: пользователь нажал «Скачать отчёт». Если считать отчёт прямо в обработчике запроса, пользователь будет ждать 10 секунд, а если сервер при этом ещё и не успеет вовремя ответить — получит таймаут. Правильный подход — вернуть ответ сразу, а тяжёлую работу отдать **фоновому исполнителю**.

Два самых популярных инструмента: **Celery** и **RQ**. Оба используют очередь на базе Redis: приложение кладёт задачу в очередь, а отдельный воркер-процесс достаёт и выполняет её.

## RQ: простая очередь

RQ (Redis Queue) — минималистичный вариант для небольших проектов. Сначала нужно установить Redis и библиотеки:

```bash
pip install rq redis
```

Опишем функцию — задачу. Важно: она должна быть импортируемой (не внутри другой функции):

```python
# tasks.py
def send_email(to: str, text: str):
    # медленная реальная отправка
    print(f"Письмо для {to}: {text}")
```

Кладём задачу в очередь и запускаем воркер:

```python
from redis import Redis
from rq import Queue

redis_conn = Redis()
queue = Queue(connection=redis_conn)
job = queue.enqueue("tasks.send_email", "anya@example.com", "Привет!")
print(job.id)
```

В терминале (отдельный процесс) запускаем воркер:

```bash
rq worker
```

Воркер достанет задачу из очереди и выполнит `send_email`.

## Celery: промышленный стандарт

Celery мощнее: планировщик расписаний, ретраи при сбоях, несколько очередей. Базовая конфигурация:

```python
# celery_app.py
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")
app.conf.task_serializer = "json"
```

Задача:

```python
@app.task
def send_email(to: str, text: str):
    print(f"Письмо для {to}: {text}")
```

Запуск:

```python
from celery_app import send_email
result = send_email.delay("anya@example.com", "Привет!")
print(result.id)
```

Воркер — в терминале:

```bash
celery -A celery_app worker --loglevel=info
```

`.delay()` кладёт задачу в очередь и немедленно возвращает управление — ответ пользователю не ждёт выполнения.

## Как это сочетается с FastAPI

В FastAPI всё просто: эндпоинт кладёт задачу в очередь и сразу возвращает `202 Accepted` (или просто успех):

```python
@app.post("/emails")
def send_email_route(to: str):
    send_email.delay(to, "Привет!")
    return {"status": "queued", "to": to}
```

Клиент не видит задержки, а письмо уйдёт, как только воркер до него доберётся.

## Итог урока

Мы разобрались, чем WebSockets отличаются от HTTP (постоянный двусторонний канал), как написать чат на FastAPI, и зачем фоновая очередь: RQ — просто, Celery — мощно. Оба инструмента отделяют быстрый ответ от тяжёлой работы.

<!--TASK-->
### Задача 1
Напиши FastAPI-приложение `chat_app.py` с двумя частями:

1. WebSocket-эндпоинт `/echo` — принимает текстовое сообщение и возвращает его с префиксом `Эхо: ` (например, на `привет` ответит `Эхо: привет`).
2. Эндпоинт `POST /jobs` — принимает JSON `{"name": "..."}` и «выполняет» медленную фоновую задачу: через `time.sleep(2)` выводит в консоль `Задача <name> выполнена`. Для имитации очереди просто верни `{"status": "queued"}` сразу, а задачу запусти через `threading.Thread` (или, если Redis установлен, через RQ).

Открой `/docs`, отправь сообщение через WebSocket-клиент (например, в браузере) и убедись, что получаешь `Эхо: ...`.

### Задача 2
Создай файл `chat.py` с FastAPI-приложением: эндпоинт `WS /chat` принимает соединение (`accept()`), добавляет сокет в глобальный список `connections`, затем в цикле читает сообщение `receive_text()` и рассылает его всем сокетам из списка через `send_text()`. При разрыве соединения (`finally`) убирай сокет из списка. Проверь в двух вкладках браузера (или двух WebSocket-клиентах): открой `ws://localhost:8000/chat` в обеих, отправь сообщение из первой — оно должно появиться в обеих. Опиши ожидаемое поведение. Зачем нужен `try/finally`?

### Задача 3
Создай файл `heartbeat.py`: эндпоинт `WS /ws/heartbeat` принимает соединение, затем в бесконечном цикле отправляет текстовое сообщение `"ping"` через `websocket.send_text("ping")` и ждёт `await asyncio.sleep(2)`. Открой страницу в браузере с `new WebSocket("ws://localhost:8000/ws/heartbeat")` и обработчиком `onmessage`, который выводит полученные сообщения в консоль. Наблюдай: сколько сообщений появляется в минуту? Что произойдёт с циклом, если соединение закроется? Опиши ожидаемое поведение.

### Задача 4
Создай файл `tasks.py` с функцией `send_email(to, text)`, которая печатает `Письмо для <to>: <text>`. Затем создай `enqueue.py`: подключись к Redis (`Redis()`), создай `Queue(connection=...)`, положи в очередь задачу `queue.enqueue("tasks.send_email", "anya@example.com", "Привет!")` и выведи `job.id`. В отдельном терминале запусти `rq worker`. Запусти `enqueue.py` и опиши, что появится в консоли воркер. Если Redis не установлен — опиши, какой шаг не выполнился, и как это исправить.

### Задача 5
Создай `celery_app.py`: экземпляр `Celery("tasks", broker="redis://localhost:6379/0")` и задачу `@app.task` `send_email`. Затем создай `main.py` с FastAPI и эндпоинтом `POST /emails`, который принимает JSON `{"to": ...}`, вызывает `send_email.delay(to, "Привет!")` и возвращает `{"status": "queued"}`. Запусти воркер `celery -A celery_app worker --loglevel=info`, затем отправь запрос через `/docs`. Опиши: что возвращает эндпоинт немедленно и что появляется в консоли воркер через некоторое время.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Для WebSocket не забудь `await websocket.accept()` до цикла. Для эха хватит одного `receive_text()` и одного `send_text()`. Для фоновой задачи: `def heavy_task(name): time.sleep(2); print(...)` и запуск `threading.Thread(target=heavy_task, args=(name,), daemon=True).start()` — верни ответ сразу, до завершения паузы.

### Подсказка 2
Не отправляй сообщение отправителю отдельно: он и так получит его через цикл рассылки. `try/finally` гарантирует удаление сокета из списка даже при ошибке — иначе следующее сообщение будет пытаться отправиться в закрытый сокет, и поднимется исключение. Для проверки в браузере используй `new WebSocket(...)` и обработчики `onopen/onmessage`.

### Подсказка 3
Цикл — `while True:`; `asyncio.sleep(2)` — асинхронная пауза, которая не блокирует сервер: другие соединения продолжают работать. Если соединение закроется, `send_text` поднимет исключение — оберни цикл в `try/except WebSocketDisconnect`, чтобы не ронять приложение. В минуту примерно 30 сообщений (60 / 2).

### Подсказка 4
Функция должна быть импортируемой — поэтому она живёт в отдельном модуле `tasks.py`, а не внутри `enqueue.py`. Воркер (`rq worker`) запускается из той же директории, чтобы нашёл `tasks`. Ожидаемый вывод в консоли воркер: `Письмо для anya@example.com: Привет!`.

### Подсказка 5
`.delay()` кладёт задачу в брокер и сразу возвращает управление — `main.py` не ждёт выполнения. Воркер в отдельном терминале: `celery -A celery_app worker --loglevel=info`. Важно, чтобы `celery_app` и `main` были в одной директории, а Redis запущен.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Одно из возможных решений:

```python
import time
import threading
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

app = FastAPI()

@app.websocket("/echo")
async def echo(websocket: WebSocket):
    await websocket.accept()
    message = await websocket.receive_text()
    await websocket.send_text(f"Эхо: {message}")

def heavy_task(name: str):
    time.sleep(2)
    print(f"Задача {name} выполнена")

class JobIn(BaseModel):
    name: str

@app.post("/jobs")
def create_job(job: JobIn):
    threading.Thread(target=heavy_task, args=(job.name,), daemon=True).start()
    return {"status": "queued", "name": job.name}
```

Проверка WebSocket (например, в консоли браузера):

```javascript
const ws = new WebSocket("ws://localhost:8000/echo");
ws.onopen = () => ws.send("привет");
ws.onmessage = (event) => console.log(event.data); // "Эхо: привет"
```

Разбор. В `/echo` сначала `accept()` — без этого клиент не получит подтверждение соединения. Затем читаем сообщение и сразу отправляем ответ: `send_text` вызовется ровно один раз, потому что у нас нет цикла. Для `/jobs` мы используем `threading.Thread` с `daemon=True`: задача уходит в отдельный поток, а эндпоинт тут же возвращает `{"status": "queued"}` — клиент не ждёт две секунды. В реальном проекте `heavy_task` заменится на `queue.enqueue(...)` (RQ) или `.delay(...)` (Celery), но принцип тот же: ответ возвращается мгновенно, а работа выполняется в фоне.

### Разбор 2
Полный код `chat.py`:

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()
connections: list[WebSocket] = []

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for conn in connections:
                await conn.send_text(message)
    finally:
        connections.remove(websocket)
```

Клиент для проверки в двух вкладках браузера:

```javascript
const ws = new WebSocket("ws://localhost:8000/chat");
ws.onopen = () => ws.send("Привет всем!");
ws.onmessage = (e) => console.log("Получено:", e.data);
```

Разбор: при каждом подключении сокет добавляется в список `connections`. Когда любой клиент отправляет сообщение, мы проходим по всему списку и шлём это сообщение каждому — поэтому отправитель тоже получает свою копию (дополнительная отправка ему не нужна). `try/finally` критичен: если соединение оборвётся (клиент закрыл вкладку), `receive_text()` бросит исключение, но `finally` выполнится и уберёт сокет из списка. Без этого сломавшийся сокет остался бы в списке, и следующие рассылки пытались бы писать в закрытый сокет, поднимая ошибку на стороне сервера.

### Разбор 3
Полный код `heartbeat.py`:

```python
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/heartbeat")
async def heartbeat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text("ping")
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print("Клиент отключился")
```

Проверка в браузере:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/heartbeat");
ws.onmessage = (e) => console.log(e.data); // "ping" каждые 2 секунды
```

Разбор: цикл `while True` отправляет `ping` и ждёт 2 секунды. `asyncio.sleep(2)` — асинхронная пауза: пока она идёт, цикл событий сервера свободен и обслуживает другие соединения — например, второй клиент получит свой `ping` независимо. В минуту выйдет примерно 30 сообщений (60 / 2). Когда вкладка закрывается, сервер получает `WebSocketDisconnect` — мы ловим его и корректно завершаем обработчик: без `try/except` исключение ушло бы наверх и могло бы уронить приложение. Такие heartbeat-циклы используются для проверки «живости» соединения, онлайн-статусов и пульса задач.

### Разбор 4
Файл `tasks.py`:

```python
def send_email(to: str, text: str):
    print(f"Письмо для {to}: {text}")
```

Файл `enqueue.py`:

```python
from redis import Redis
from rq import Queue

redis_conn = Redis()
queue = Queue(connection=redis_conn)

job = queue.enqueue("tasks.send_email", "anya@example.com", "Привет!")
print("ID задачи:", job.id)
```

Запуск:

```bash
pip install rq redis
rq worker
python enqueue.py
```

Ожидаемый вывод в консоли воркер:

```
Письмо для anya@example.com: Привет!
```

Разбор: `send_email` вынесена в отдельный модуль, потому что воркер импортирует задачу по строковому пути `"tasks.send_email"` — функции, определённые внутри других функций или внутри `enqueue.py`, так импортировать нельзя. `queue.enqueue(...)` кладёт вызов в очередь Redis и немедленно возвращает объект `job` с id. Воркер `rq worker` — это отдельный процесс: он слушает очередь, забирает задачу и выполняет её, печатая строку. Если Redis не установлен, `Redis()` бросит ошибку соединения — исправляется установкой и запуском Redis (`redis-server`). Одно из преимуществ RQ — простота: минимум конфигурации для маленьких проектов.

### Разбор 5
Файл `celery_app.py`:

```python
from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")
app.conf.task_serializer = "json"

@app.task
def send_email(to: str, text: str):
    print(f"Письмо для {to}: {text}")
```

Файл `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from celery_app import send_email

app = FastAPI()

class EmailIn(BaseModel):
    to: str

@app.post("/emails")
def create_email(data: EmailIn):
    send_email.delay(data.to, "Привет!")
    return {"status": "queued", "to": data.to}
```

Запуск:

```bash
celery -A celery_app worker --loglevel=info
uvicorn main:app
```

Разбор: эндпоинт `POST /emails` вызывает `send_email.delay(...)` — Celery кладёт задачу в брокер (Redis) и сразу возвращает управление, поэтому ответ `{"status": "queued"}` приходит мгновенно, без паузы. Воркер `celery -A celery_app worker` — отдельный процесс, который забирает задачу из очереди и выполняет её: в его консоли примерно через секунду появится `Письмо для anya@example.com: Привет!`. Такой паттерн отделяет быстрый HTTP-ответ от тяжёлой работы: пользователь видит «поставлено в очередь», а реальная отправка происходит в фоне. Celery в отличие от RQ умеет расписания, повторы при сбоях и несколько очередей.
<!--/SOLUTION-->

<!--QUIZ-->
Чем WebSocket отличается от HTTP?
- WebSocket работает только для статических файлов
- WebSocket держит постоянное двустороннее соединение, позволяя серверу самому отправлять сообщения
- WebSocket медленнее HTTP
- Это одно и то же
* Правильный ответ: WebSocket держит постоянное двустороннее соединение, позволяя серверу самому отправлять сообщения
HTTP — «запрос-ответ»: сервер отвечает только на запросы. WebSocket открывает канал, по которому обе стороны шлют сообщения в любой момент.

Какой вызов обязателен перед тем, как общаться с клиентом по WebSocket?
- websocket.send_text("ok")
- websocket.accept()
- websocket.close()
- websocket.receive_bytes()
* Правильный ответ: websocket.accept()
Без accept() сервер не завершит рукопожатие, и клиент не сможет обмениваться сообщениями.

Зачем фоновые задачи (Celery/RQ) нужны в веб-приложении?
- Чтобы ускорить базу данных
- Чтобы тяжёлая работа не блокировала ответ пользователю
- Чтобы заменить собой WebSocket
- Чтобы шифровать пароли
* Правильный ответ: Чтобы тяжёлая работа не блокировала ответ пользователю
Приложение кладёт задачу в очередь и сразу отвечает; отдельный воркер выполняет её позже, не заставляя клиента ждать.

Что делает воркер (worker) в Celery/RQ?
- Отвечает на HTTP-запросы
- Забирает задачи из очереди и выполняет их в отдельном процессе
- Хранит пароли
- Рендерит HTML-шаблоны
* Правильный ответ: Забирает задачи из очереди и выполняет их в отдельном процессе
Воркер — это отдельный процесс (rq worker / celery worker), который слушает очередь и выполняет поступающие задачи.

Как положить задачу в очередь Celery?
- Вызвать функцию напрямую
- Вызвать send_email.delay(...)
- Отправить POST-запрос на /tasks
- Запустить python manage.py migrate
* Правильный ответ: Вызвать send_email.delay(...)
Метод .delay() кладёт задачу в брокер и сразу возвращает управление — выполнение происходит асинхронно.
<!--/QUIZ-->
