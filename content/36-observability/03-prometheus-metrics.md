---
title: Prometheus: метрики приложений
summary: Счётчики, gauge, гистограммы; экспонирование метрик через /metrics и инструментация FastAPI библиотекой prometheus_client.
order: 3
duration: 35 мин
difficulty: advanced
tags: prometheus, метрики, prometheus_client, counter, gauge, histogram, fastapi
---

Логи описывают отдельные события, трейсы — цепочки вызовов, а **метрики** дают ответ на вопрос «что происходит с системой прямо сейчас»: сколько запросов в секунду, какая задержка, сколько памяти занято. Метрики — это числа с метками времени, и они лежат в основе алертов и дашбордов. Самый популярный инструмент сбора — **Prometheus**, а для Python существует стандартная библиотека **prometheus_client**.

## Как работает Prometheus

Prometheus — это сервер, который периодически «вытягивает» метрики из приложений: приложение публикует их на endpoint'е `/metrics`, а Prometheus опрашивает его каждые N секунд (обычно 15). Формат ответа — простой текстовый протокол **exposition format**:

```
# HELP http_requests_total Total HTTP requests.
# TYPE http_requests_total counter
http_requests_total{method="GET",status="200"} 42.0
```

Каждая строка — это имя метрики, набор меток (labels) в фигурных скобках и числовое значение. Комментарии `# HELP` и `# TYPE` описывают метрику и её тип.

## Типы метрик

1. **Counter** — только возрастающий счётчик: количество запросов, ошибок, байт. Значение только увеличивается (сброс — при перезапуске процесса).
2. **Gauge** — может и расти, и падать: текущее число активных соединений, температура, размер очереди.
3. **Histogram** — распределение значений (например, времени ответа): Prometheus считает суммы и количество значений в заданных бакетах, поэтому можно вычислять перцентили (p50, p95, p99).
4. **Summary** — похожа на гистограмму, но перцентили считаются на стороне приложения; используется реже.

## Первая метрика

Установим библиотеку:

```bash
pip install prometheus-client
```

```python
from prometheus_client import Counter, Gauge, Histogram, generate_latest

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "status"],
)

HTTP_REQUESTS.labels(method="GET", status="200").inc()
```

`с` — имя метрики (по конвенции Prometheus имена имеют суффикс `_total` у счётчиков, `_seconds` у времени, `_bytes` у размеров), второй аргумент — HELP-описание. `.labels(method=..., status=...)` возвращает «семейство» счётчика с заданными метками; `.inc()` увеличивает на 1, `.inc(5)` — на 5.

Текущее число входящих запросов:

```python
INFLIGHT = Gauge("http_inflight_requests", "Requests currently being processed")
INFLIGHT.inc()   # запрос начался
try:
    ...
finally:
    INFLIGHT.dec()  # запрос закончился
```

`Gauge` поддерживает `inc()`, `dec()`, `set(value)`, `set_to_current_time()`.

## Гистограмма времени ответа

```python
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

@contextmanager
def track_duration():
    start = time.perf_counter()
    try:
        yield
    finally:
        REQUEST_DURATION.observe(time.perf_counter() - start)
```

`buckets` — границы интервалов. По умолчанию `Histogram` использует стандартные бакеты (от 0.005 до 10), но под конкретный сервис их часто задают вручную.

## Эндпоинт /metrics

Чтобы Prometheus мог забрать метрики, в приложении должен быть endpoint `/metrics`, возвращающий `generate_latest()`:

```python
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

`generate_latest()` возвращает байты в exposition format для всех метрик, зарегистрированных в глобальном реестре (`REGISTRY`). `CONTENT_TYPE_LATEST` — правильный `Content-Type: text/plain; version=0.0.4; charset=utf-8`. Для быстрой проверки можно запустить `start_http_server(8000)` — Prometheus-клиент сам поднимет HTTP-сервер с `/metrics`.

**Важно про multiprocess**: если приложение запущено в несколько процессов (например, gunicorn с несколькими воркерами), каждый процесс имеет свой набор метрик, и нужен специальный режим `prometheus_multiproc_dir` с `CollectorRegistry` и `MultiProcessCollector` — об этом обязательно читай документацию перед деплоем.

## Middleware для FastAPI

Соберём всё вместе — замер времени и счётчик запросов:

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        HTTP_REQUESTS.labels(method=request.method, status="500").inc()
        raise
    REQUEST_DURATION.observe(time.perf_counter() - start)
    HTTP_REQUESTS.labels(method=request.method, status=str(response.status_code)).inc()
    return response
```

`Request.method` — метод запроса, `response.status_code` — код ответа. Так мы получаем метрики `http_requests_total{method="GET",status="200"}` и `http_request_duration_seconds`.

## Лучшие практики

- **Следи за кардинальностью меток.** Метки должны иметь ограниченное число значений: `method`, `status` — можно, а вот `user_id` или конкретный `path` с id (например, `/orders/12345`) — нельзя: количество серий метрик взорвётся. Для маршрутов используй шаблон пути `/orders/{order_id}`.
- Именуй метрики по стандарту: суффиксы `_total`, `_seconds`, `_bytes`, единицы измерения.
- Не добавляй HELP-тексты с лишней информацией — они попадают в каждый скрейп.
- Гистограммы хранят и суммы (`_sum`), и количества (`_count`) — сумма делится на количество, и получается среднее. Перцентили вычисляются запросом к Prometheus.

<!--TASK-->
### Задача 1
Создай файл `metrics_app.py` с FastAPI-приложением: эндпоинт `/metrics`, возвращающий `generate_latest()` с `CONTENT_TYPE_LATEST`, и эндпоинт `/hello`, возвращающий `{"message": "hello"}`. Добавь счётчик `http_requests_total` с метками `method` и `status`. В middleware обновляй счётчик после каждого запроса. Запусти приложение (`uvicorn metrics_app:app`), сделай несколько запросов на `/hello` через `curl` и проверь, что в `/metrics` появилась строка `http_requests_total{method="GET",status="200"}` с числом, равным количеству запросов.

### Задача 2
Добавь в `metrics_app.py` gauge `http_inflight_requests` — текущее число обрабатываемых запросов. В middleware перед `call_next` вызови `INFLIGHT.inc()`, а в `finally` — `INFLIGHT.dec()`. Затем добавь гистограмму `http_request_duration_seconds` с бакетами `(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)` и в middleware измеряй время обработки и вызывай `observe()`. Проверь, что в `/metrics` появились строки `http_request_duration_seconds_bucket`, `http_request_duration_seconds_sum` и `http_request_duration_seconds_count`, а также `http_inflight_requests`.

### Задача 3
Напиши pytest-тесты в файле `test_metrics.py`. Создай **отдельный** `CollectorRegistry` (`from prometheus_client import CollectorRegistry, Counter, generate_latest`), зарегистрируй в нём счётчик с метками, увеличь его на 5 с меткой `method="GET"`, затем вызови `generate_latest(registry)` и проверь, что в тексте есть строка `test_requests_total{method="GET"} 5.0`. Во втором тесте проверь, что гистограмма после `observe(0.3)` содержит строки `_count` и `_sum`. Убедись, что тесты не конфликтуют с глобальным реестром (используй свой `CollectorRegistry` в каждом тесте).

### Задача 4
Добавь в `test_metrics.py` интеграционный тест приложения из задачи 2. Создай `TestClient(app)`, сделай два запроса к `/hello`, затем получи `/metrics` и проверь: (1) ответ имеет статус 200; (2) в тексте есть строка `http_requests_total{method="GET",status="200"} 2.0`; (3) есть строки `http_request_duration_seconds_count` и `http_request_duration_seconds_sum`. Подсказка: в тесте приложение уже использует глобальный реестр — это ок, но учти, что параллельно запущенные тесты могут «видеть» метрики друг друга; поэтому используй уникальные имена или запускай тесты последовательно.

### Задача 5
Реализуй middleware, который логирует «необычные» ответы: если `response.status_code >= 400`, увеличь счётчик `http_errors_total` с меткой `status`. Покажи, как в `/metrics` будет выглядеть строка для 404. Затем напиши краткий комментарий в коде о том, почему метку `path` с конкретным id ставить нельзя, а метку `path` с шаблоном — можно.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Счётчик: `HTTP_REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "status"])`. В middleware после `response = await call_next(request)` вызови `HTTP_REQUESTS.labels(method=request.method, status=str(response.status_code)).inc()`. Не забудь вернуть `response`.

### Подсказка 2
Gauge: `INFLIGHT = Gauge("http_inflight_requests", "Requests currently being processed")`. В middleware: `INFLIGHT.inc()` до `call_next`, и `INFLIGHT.dec()` в `finally`. Гистограмма: `REQUEST_DURATION = Histogram("http_request_duration_seconds", "...", buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0))`; в `finally` — `REQUEST_DURATION.observe(time.perf_counter() - start)`.

### Подсказка 3
Реестр: `registry = CollectorRegistry()`, затем `c = Counter("test_requests_total", "...", ["method"], registry=registry)`, `c.labels(method="GET").inc(5)` и `text = generate_latest(registry).decode()`. Проверка: `assert "test_requests_total{method=\"GET\"} 5.0" in text`. Для гистограммы: `h = Histogram("test_duration_seconds", "...", registry=registry)`, `h.observe(0.3)`, затем проверь `"test_duration_seconds_count 1.0" in text` и `"test_duration_seconds_sum" in text`.

### Подсказка 4
В интеграционном тесте надо сделать запросы *до* чтения `/metrics`, иначе счётчик будет 0. Если в тексте `http_requests_total` нет — проверь, что middleware применяется (напиши `print()` в middleware на время отладки помни, что `TestClient` поддерживает middleware). Обрати внимание на порядок: счётчик увеличивается после `call_next`, поэтому первый запрос к `/metrics` сам увеличит счётчик.

### Подсказка 5
Счётчик ошибок: `HTTP_ERRORS = Counter("http_errors_total", "Total error responses", ["status"])`. В middleware: `if response.status_code >= 400: HTTP_ERRORS.labels(status=str(response.status_code)).inc()`. Для проверки 404 сделай запрос к несуществующему пути `/nope`. Комментарий: имя метрики должно иметь ограниченное число значений — `/orders/12345` создаёт новую серию на каждый id.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение (`metrics_app.py`):

```python
import time
from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = FastAPI()

HTTP_REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "status"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)
    HTTP_REQUESTS.labels(method=request.method, status=str(response.status_code)).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

Что здесь происходит? `Counter` с метками `method` и `status` — это «семейство» счётчиков: каждая комбинация меток даёт отдельную серию. В middleware после обработки запроса мы увеличиваем нужную серию. Prometheus по адресу `/metrics` увидит:

```
http_requests_total{method="GET",status="200"} 3.0
```

`generate_latest()` собирает все метрики из глобального `REGISTRY` и сериализует их в exposition format.

### Разбор 2
Решение:

```python
INFLIGHT = Gauge("http_inflight_requests", "Requests currently being processed")
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    INFLIGHT.inc()
    start = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        REQUEST_DURATION.observe(time.perf_counter() - start)
        INFLIGHT.dec()
    HTTP_REQUESTS.labels(method=request.method, status=str(response.status_code)).inc()
    return response
```

Что здесь происходит? `INFLIGHT` — это gauge: он увеличивается, когда запрос начался, и уменьшается при завершении. `finally` гарантирует, что даже при исключении gauge не «зависнет» в увеличенном состоянии. Гистограмма с помощью `observe` заносит измерение в бакеты. В `/metrics` мы увидим блоки `http_inflight_requests` (одно число), `http_request_duration_seconds_bucket{le="0.05"}`, `..._bucket{le="0.1"}`, ..., `..._bucket{le="+Inf"}`, плюс `_sum` и `_count`.

### Разбор 3
Решение:

```python
import pytest
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest

def test_counter_with_labels():
    registry = CollectorRegistry()
    c = Counter("test_requests_total", "Total test requests", ["method"], registry=registry)
    c.labels(method="GET").inc(5)
    text = generate_latest(registry).decode()
    assert 'test_requests_total{method="GET"} 5.0' in text

def test_histogram_count_sum():
    registry = CollectorRegistry()
    h = Histogram("test_duration_seconds", "Test duration", registry=registry)
    h.observe(0.3)
    text = generate_latest(registry).decode()
    assert "test_duration_seconds_count 1.0" in text
    assert "test_duration_seconds_sum" in text
```

Что здесь происходит? Глобальный `REGISTRY` содержит метрики всех тестов и может конфликтовать. `CollectorRegistry()` создаёт изолированный реестр — внутри теста мы работаем только с ним, и `generate_latest(registry)` сериализует именно его. Обрати внимание на формат: значение 5.0 выводится как `5.0` (Prometheus всегда печатает девятичную точку). Гистограмма `_sum` после `observe(0.3)` равна 0.3, и это проверяется наличием строки.

### Разбор 4
Решение:

```python
from fastapi.testclient import TestClient
from metrics_app import app

def test_metrics_endpoint_after_requests():
    client = TestClient(app)
    client.get("/hello")
    client.get("/hello")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    text = resp.text
    assert 'http_requests_total{method="GET",status="200"} 2.0' in text
    assert "http_request_duration_seconds_count" in text
    assert "http_request_duration_seconds_sum" in text
```

Что здесь происходит? `TestClient` полностью повторяет жизненный цикл запроса, включая middleware. Два запроса к `/hello` увеличивают `http_requests_total` до 2.0, а третий запрос — сам к `/metrics` — читает состояние. Важная деталь: middleware увеличивает счётчик после `call_next`, поэтому запрос к `/metrics` тоже попадает в счётчики — но он уже выполнен к моменту чтения `resp.text`, так что его собственный вклад не «съедается». Если в тексте нет строки с `2.0` — проверь, что приложение действительно использует тот же глобальный реестр, что и `generate_latest()`.

### Разбор 5
Решение:

```python
HTTP_ERRORS = Counter("http_errors_total", "Total error responses", ["status"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    INFLIGHT.inc()
    start = time.perf_counter()
    try:
        response = await call_next(request)
    finally:
        REQUEST_DURATION.observe(time.perf_counter() - start)
        INFLIGHT.dec()
    if response.status_code >= 400:
        HTTP_ERRORS.labels(status=str(response.status_code)).inc()
    HTTP_REQUESTS.labels(method=request.method, status=str(response.status_code)).inc()
    return response
```

В `/metrics` появится строка `http_errors_total{status="404"} 1.0` после запроса к несуществующему пути. Что здесь происходит? Мы отделяем ошибки в отдельную метрику, чтобы было удобно строить алерты на долю 5xx. Комментарий про кардинальность: если написать `labels(method=..., path=request.url.path)`, то запрос к `/orders/12345` и к `/orders/67890` создадут **разные серии** метрик — уже через день их наберутся тысячи, и Prometheus начнёт тормозить и тратить память. Поэтому в метки кладут только ограниченные значения: метод, статус, шаблон пути (`/orders/{order_id}`).
<!--/SOLUTION-->

<!--QUIZ-->
Какой тип метрики подходит для счётчика запросов?
- Gauge
- Counter
- Histogram
* Правильный ответ: Counter
Counter — только возрастающий счётчик; запросы — классический пример.

Какой тип метрики может и увеличиваться, и уменьшаться?
- Counter
- Gauge
- Summary
* Правильный ответ: Gauge
Gauge отражает текущее значение: соединения, очередь, температура.

Что делает Histogram.observe(0.3)?
- Увеличивает счётчик на 0.3
- Заносит измерение 0.3 в бакеты распределения
- Устанавливает значение гистограммы в 0.3
* Правильный ответ: Заносит измерение 0.3 в бакеты распределения
observe добавляет наблюдение в распределение; Prometheus затем считает перцентили.

Какой endpoint обычно отдаёт метрики в Prometheus?
- /health
- /metrics
- /status
* Правильный ответ: /metrics
Prometheus опрашивает /metrics в формате exposition.

Какая функция формирует текст метрик?
- format_metrics()
- generate_latest()
- render_metrics()
* Правильный ответ: generate_latest()
generate_latest() возвращает байты в exposition format из реестра.

Что вернёт generate_latest(registry) с собственным CollectorRegistry?
- Метрики только этого реестра
- Все метрики процесса
- Ошибку
* Правильный ответ: Метрики только этого реестра
Передача registry позволяет изолировать метрики в тестах.

Почему нельзя использовать user_id как метку?
- Слишком длинное имя
- Количество уникальных значений неограниченно — кардинальность взорвётся
- Prometheus не поддерживает строковые метки
* Правильный ответ: Количество уникальных значений неограниченно — кардинальность взорвётся
Каждая комбинация меток — отдельная серия; тысячи пользователей создадут тысячи серий.

Что делает INFLIGHT.dec() в finally?
- Сбрасывает gauge в ноль
- Уменьшает текущее значение gauge, даже если была ошибка
- Устанавливает gauge в 1
* Правильный ответ: Уменьшает текущее значение gauge, даже если была ошибка
finally гарантирует уменьшение при любом исходе — иначе gauge «зависнет».

Какой Content-Type должен быть у /metrics?
- application/json
- text/plain; version=0.0.4; charset=utf-8
- text/html
* Правильный ответ: text/plain; version=0.0.4; charset=utf-8
Это значение лежит в константе CONTENT_TYPE_LATEST.

Что обозначает строка http_requests_total{method="GET",status="200"} 42.0?
- 42 запроса с меткой GET и статусом 200
- 42 гистограммы
- 42 ошибки
* Правильный ответ: 42 запроса с меткой GET и статусом 200
Серия метрик с метками method=GET, status=200 насчитала 42.0.
<!--/QUIZ-->
