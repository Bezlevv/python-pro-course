---
title: Healthchecks, readiness и алерты
summary: Liveness против readiness, реализация /healthz и /readyz с проверкой зависимостей, и правила алертов на PromQL.
order: 5
duration: 30 мин
difficulty: advanced
tags: healthcheck, liveness, readiness, алерты, promql, fastapi, slo
---

Приложение можно запустить — но это не значит, что оно готово принимать трафик. Оркестраторы (Kubernetes) и балансировщики постоянно проверяют здоровье приложений, и качество этих проверок напрямую определяет, насколько быстро система восстановится после сбоя. В этом уроке разберём два главных вида проверок — **liveness** и **readiness** — и то, как превращать метрики в алерты.

## Liveness: жив ли процесс

**Liveness** отвечает на вопрос «процесс жив и не завис?». Если проверка проваливается, оркестратор **перезапускает** контейнер (restart). Типичная реализация — минимальный эндпоинт, который просто отвечает `200`, если приложение может обрабатывать запросы вообще:

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/healthz")
def liveness():
    return JSONResponse({"status": "ok"})
```

Важно: в liveness **нельзя** включать проверки внешних зависимостей. Если база данных на 30 секунд станет недоступной, а liveness начнёт возвращать 503 — оркестратор перезапустит приложение, и проблема не решится, а усугубится. Liveness должен быть «тупым»: процесс отвечает — значит, жив.

## Readiness: готов ли принимать трафик

**Readiness** отвечает на вопрос «может ли приложение прямо сейчас выполнять работу?». Она проверяет **зависимости**: доступна ли база данных, кэш, очередь, внешние API. Если readiness возвращает ошибку — оркестратор **отзывает** трафик у поды (но не перезапускает её). Проверка выглядит так:

```python
async def check_db() -> bool:
    try:
        async with db.pool.acquire() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False

@app.get("/readyz")
async def readiness():
    if not await check_db():
        return JSONResponse({"status": "unavailable", "component": "db"}, status_code=503)
    return JSONResponse({"status": "ok"})
```

`503` означает: «не готов, не шлите трафик». Когда зависимость вернётся, эндпоинт снова начнёт отвечать `200` — и оркестратор вернёт поду в ротацию.

## Опасные паттерны

1. **Чекать БД на каждый запрос** — readiness опрашивается каждые несколько секунд каждым экземпляром. Если каждая проверка открывает соединение к БД, это лишняя нагрузка. Решение — кеширование результата на 5–10 секунд.
2. **Таймауты без границ** — если база зависла, `SELECT 1` может висеть минуты, и проверка не ответит вовремя. Всегда задавай таймаут (например, 1–2 секунды).
3. **Чекать всё сразу** — readiness должна возвращать `503`, если **хоть одна** критическая зависимость недоступна, но каждая проверка должна быть быстрой и независимой.

## Дизайн интерфейса проверок

Чтобы тестировать readiness без реальной базы, вынеси проверку за интерфейс:

```python
from abc import ABC, abstractmethod

class HealthChecker(ABC):
    @abstractmethod
    def check(self) -> bool:
        """Возвращает True, если зависимость доступна."""
        raise NotImplementedError

class DummyChecker(HealthChecker):
    def __init__(self, healthy: bool = True):
        self._healthy = healthy
    def check(self) -> bool:
        return self._healthy
```

В проде передаётся реальный чекер БД, в тестах — `DummyChecker(healthy=False)`. Это классический паттерн для изоляции внешних систем.

## Алерты: от метрик к решению

Метрики бесполезны, если никто не реагирует. Алерты — это правила (rules) на языке **PromQL**, которые Prometheus вычисляет периодически, и если условие выполняется дольше `for` — отправляется уведомление в Alertmanager. Пример правила:

```yaml
groups:
  - name: orders.rules
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_errors_total[5m]))
            / sum(rate(http_requests_total[5m])) > 0.05
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Ошибки выше 5% за 5 минут"
          description: "Доля ошибок {{ $value | humanizePercentage }}"
```

- `expr` — PromQL-выражение. `rate(...[5m])` считает скорость роста счётчика за 5 минут; отношение ошибок к запросам — доля ошибок.
- `for: 10m` — фальшивая тревога не сработает: условие должно держаться 10 минут подряд.
- `severity` и аннотации — для маршрутизации в Alertmanager (кому слать, с какой важностью).

## SLO и burn rate

Современный подход — строить алерты на **SLO** (Service Level Objective): например, «99.9% запросов должны завершаться успешно за месяц». Гореть должен не сам факт нарушения, а **burn rate** — скорость «сгорания» бюджета ошибок. Если за 30 дней допустимо 0.1% ошибок, то 1% ошибок за час — это burn rate 10×, и нужно алертить немедленно. Простое правило: алертить, когда доля ошибок за 5 минут превышает целевой уровень в несколько раз.

## Лучшие практики

- Разделяй liveness и readiness в отдельные эндпоинты с разными именами (`/healthz`, `/readyz`).
- Не перезапускай поду при отказе зависимости — отзывай трафик через readiness.
- Кешируй результаты проверок и всегда ставь таймауты.
- Алерты должны содержать `for`, чтобы избегать ложных срабатываний.
- Проверяй алерты на тестовых данных перед заливкой в прод.

<!--TASK-->
### Задача 1
Создай файл `health_app.py` с FastAPI-приложением и двумя эндпоинтами: `GET /healthz` (liveness, всегда отвечает `{"status": "ok"}` с кодом 200) и `GET /readyz` (readiness, возвращает `{"status": "ok"}` или `{"status": "unavailable", "component": "db"}` с кодом 503). Для readiness используй интерфейс `HealthChecker` с методом `check()` и класс `DummyChecker` из теории. Подключи `DummyChecker()` в качестве зависимости через `Depends`. Убедись, что оба эндпоинта работают.

### Задача 2
Добавь в `health_app.py` кеширование результата readiness: результаты проверки не должны запрашиваться чаще, чем раз в 5 секунд. Реализуй класс `CachedHealthChecker` (обёртку над `HealthChecker`), который запоминает последний результат и время проверки, а если прошло меньше 5 секунд — возвращает сохранённый результат без вызова внутреннего чекера. Подключи его вместо `DummyChecker`.

### Задача 3
Напиши pytest-тесты в `test_health.py`. Тест 1: `TestClient` с `DummyChecker(healthy=True)` — `GET /healthz` возвращает 200 и `{"status": "ok"}`, `GET /readyz` возвращает 200. Тест 2: `DummyChecker(healthy=False)` — `GET /readyz` возвращает 503 и `{"status": "unavailable", "component": "db"}`. Тест 3: `CachedHealthChecker` — создай счётчик вызовов (например, обёртку, которая увеличивает счётчик при каждом `check()`), сделай 10 запросов к `/readyz` и проверь, что внутренний чекер вызывался не более 2 раз (первый + ещё один после сброса кеша). Запусти `pytest test_health.py -v`.

### Задача 4
Добавь в `test_health.py` тест с таймаутом: обёртка `SlowChecker`, которая спит 0.2 секунды и возвращает `True`. Создай `CachedHealthChecker(SlowChecker(), ttl=1.0)` (параметр `ttl` — время жизни кеша в секундах). Тест: сделай запрос к `/readyz` и измерь время — оно должно быть меньше 0.2 секунды при повторном запросе (кеш сработал), а первый запрос — медленнее. Проверь, что обе проверки завершились успешно (200).

### Задача 5
Создай файл `alerts.yml` с двумя правилами алертов: `HighErrorRate` (доля ошибок `http_errors_total / http_requests_total` за 5 минут больше 0.05, `for: 10m`, severity critical) и `ServiceDown` (метрика `up{job="orders"}` равна 0 в течение 2 минут, severity critical). Затем напиши в комментарии (внутри YAML) объяснение: почему `for` защищает от ложных срабатываний и почему для `ServiceDown` хватает короткого `for`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Зависимость через `Depends`: `from fastapi import Depends`; функция `get_checker() -> HealthChecker: return DummyChecker()`; в эндпоинте `checker: HealthChecker = Depends(get_checker)`. Для 503 используй `JSONResponse(..., status_code=503)`.

### Подсказка 2
В `CachedHealthChecker` храни `_last_time: float = 0.0` и `_last_ok: bool = True`. В `check()` сравнивай `time.monotonic() - self._last_time > self.ttl`. Помни: `ttl` можно сделать параметром конструктора, чтобы в тестах использовать маленькие значения.

### Подсказка 3
`TestClient` создаётся через `from fastapi.testclient import TestClient`; в тесте можно пересоздать `app` с нужным чекером (или создать функцию `make_app(checker)`). Счётчик вызовов: класс с атрибутом `calls = 0` и `check()`, который увеличивает его и вызывает `self._inner.check()`.

### Подсказка 4
Используй `time.perf_counter()` вокруг запросов. С `ttl=1.0` первый запрос вызовет `SlowChecker` (спит), а второй — попадёт в кеш и вернётся мгновенно. В `CachedHealthChecker` не забудь обновлять `_last_time` **только** когда реально вызывался внутренний чекер (иначе кеш не «сработает»).

### Подсказка 5
Правило YAML: `groups:` → `rules:` → `alert:`, `expr:`, `for:`, `labels:`, `annotations:`. Для `ServiceDown` используй `expr: up{job="orders"} == 0`. В комментарии: короткий `for` для аптайма оправдан, потому что «сервис недоступен» — это уже факт, а не флуктуация.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение (`health_app.py`):

```python
from abc import ABC, abstractmethod
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

class HealthChecker(ABC):
    @abstractmethod
    def check(self) -> bool:
        raise NotImplementedError

class DummyChecker(HealthChecker):
    def __init__(self, healthy: bool = True):
        self._healthy = healthy
    def check(self) -> bool:
        return self._healthy

app = FastAPI()

def get_checker() -> HealthChecker:
    return DummyChecker()

@app.get("/healthz")
def liveness():
    return JSONResponse({"status": "ok"})

@app.get("/readyz")
def readiness(checker: HealthChecker = Depends(get_checker)):
    if not checker.check():
        return JSONResponse({"status": "unavailable", "component": "db"}, status_code=503)
    return JSONResponse({"status": "ok"})
```

Что здесь происходит? `HealthChecker` — интерфейс: любые реализации можно подставлять в readiness. `Depends(get_checker)` — механизм внедрения зависимостей FastAPI: вместо того чтобы жёстко создавать чекер внутри эндпоинта, мы получаем его из фабрики. Теперь тесты подставят `DummyChecker(healthy=False)` и проверят 503.

### Разбор 2
Решение:

```python
import time

class CachedHealthChecker(HealthChecker):
    def __init__(self, inner: HealthChecker, ttl: float = 5.0):
        self._inner = inner
        self.ttl = ttl
        self._last_time = 0.0
        self._last_ok = True

    def check(self) -> bool:
        now = time.monotonic()
        if now - self._last_time >= self.ttl:
            self._last_ok = self._inner.check()
            self._last_time = now
        return self._last_ok

def get_checker() -> HealthChecker:
    return CachedHealthChecker(DummyChecker())
```

Что здесь происходит? `time.monotonic()` — монотонные часы, не зависящие от перевода системного времени. Первый вызов всегда проходит дальше; последующие в течение `ttl` секунд возвращают закешированный результат. Все время жизни кеша — 5 секунд, поэтому оркестратор, опрашивающий readiness каждые 3 секунды, будет дёргать базу лишь раз в 5 секунд.

### Разбор 3
Решение:

```python
from fastapi.testclient import TestClient
from health_app import CachedHealthChecker, DummyChecker, HealthChecker, app

class CountingChecker(HealthChecker):
    def __init__(self, inner: HealthChecker):
        self._inner = inner
        self.calls = 0
    def check(self) -> bool:
        self.calls += 1
        return self._inner.check()

def test_liveness_and_ready_ok():
    client = TestClient(app)
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/readyz").status_code == 200

def test_ready_unavailable():
    app.dependency_overrides[get_checker] = lambda: DummyChecker(healthy=False)
    client = TestClient(app)
    resp = client.get("/readyz")
    assert resp.status_code == 503
    assert resp.json()["status"] == "unavailable"

def test_cached_checker_limits_calls():
    counting = CountingChecker(DummyChecker())
    cached = CachedHealthChecker(counting, ttl=5.0)
    app.dependency_overrides[get_checker] = lambda: cached
    client = TestClient(app)
    for _ in range(10):
        client.get("/readyz")
    assert counting.calls <= 2
```

Что здесь происходит? `dependency_overrides` — официальный механизм FastAPI для подмены зависимостей в тестах: мы заменяем `get_checker` на функцию, возвращающую наш чекер. `CountingChecker` считает реальные вызовы внутреннего чекера. После 10 запросов кеш с `ttl=5.0` позволил вызвать внутренний чекер лишь один-два раза — это и есть защита от лишней нагрузки на БД.

### Разбор 4
Решение:

```python
import time

class SlowChecker(HealthChecker):
    def check(self) -> bool:
        time.sleep(0.2)
        return True

def test_cached_checker_ttl():
    cached = CachedHealthChecker(SlowChecker(), ttl=1.0)
    app.dependency_overrides[get_checker] = lambda: cached
    client = TestClient(app)

    t0 = time.perf_counter()
    assert client.get("/readyz").status_code == 200
    first = time.perf_counter() - t0

    t0 = time.perf_counter()
    assert client.get("/readyz").status_code == 200
    second = time.perf_counter() - t0

    assert first >= 0.2
    assert second < 0.2
```

Что здесь происходит? Первый запрос проходит через медленный чекер (≈0.2 c), второй — забирает результат из кеша и отвечает почти мгновенно. Так мы подтверждаем и саму логику кеша, и то, что он не «протекает» между запросами. В реальном проде таймаут проверки БД должен быть жёстким (1–2 с) — иначе readiness сама станет тормозом.

### Разбор 5
Решение (`alerts.yml`):

```yaml
groups:
  - name: orders.rules
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_errors_total[5m]))
            / sum(rate(http_requests_total[5m])) > 0.05
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Ошибки выше 5% за 5 минут"
          description: "Доля ошибок {{ $value | humanizePercentage }}"

      - alert: ServiceDown
        expr: up{job="orders"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Сервис orders недоступен"
          description: "Метрика up для job=orders равна 0 уже 2 минуты"
```

Что здесь происходит? `for` — это «подтверждающий» интервал: тревога сработает только если выражение истинно непрерывно в течение указанного времени. Для доли ошибок 10 минут отсекают кратковременные всплески (один неудачный тест, перезапуск поды). Для `ServiceDown` хватает 2 минут: `up == 0` — уже факт остановки, а не флуктуация; тянуть с реакцией на полную недоступность сервиса нельзя.
<!--/SOLUTION-->

<!--QUIZ-->
Что отвечает на вопрос «жив ли процесс и не завис ли он?»
- Readiness
- Liveness
- Startup probe
* Правильный ответ: Liveness
Liveness — проверка жизнеспособности процесса; при провале — рестарт.

Что произойдёт, если readiness вернёт 503?
- Контейнер будет перезапущен
- Трафик будет отозван у поды, но контейнер продолжит работать
- Приложение будет остановлено
* Правильный ответ: Трафик будет отозван у поды, но контейнер продолжит работать
Readiness не вызывает рестарт — она лишь убирает поду из ротации.

Почему в liveness нельзя включать проверку базы данных?
- База данных слишком медленная
- При отказе БД оркестратор начнёт перезапускать приложение в цикле
- Liveness не умеет ходить в сеть
* Правильный ответ: При отказе БД оркестратор начнёт перезапускать приложение в цикле
Liveness должен быть минимальным: зависимость недоступна ≠ процесс мёртв.

Что делает CachedHealthChecker?
- Проверяет кеш приложения
- Кеширует результат проверки на ttl секунд, чтобы не дёргать зависимость
- Отправляет метрики в кеш
* Правильный ответ: Кеширует результат проверки на ttl секунд, чтобы не дёргать зависимость
Результат check() переиспользуется, пока не истечёт ttl.

Как в pytest подменить зависимость FastAPI?
- Через параметр
- Через app.dependency_overrides
- Через мок импорта
* Правильный ответ: Через app.dependency_overrides
dependency_overrides заменяет функцию-зависимость на тестовую.

Какой статус-код у readiness при недоступной зависимости?
- 500
- 503
- 404
* Правильный ответ: 503
503 — «Service Unavailable», готовность не достигнута.

Что считает rate(http_errors_total[5m])?
- Общее число ошибок
- Скорость роста счётчика ошибок за 5 минут
- Среднее время ошибки
* Правильный ответ: Скорость роста счётчика ошибок за 5 минут
rate делит прирост на интервал и даёт скорость в единицах в секунду.

Зачем нужен for: 10m в правиле алерта?
- Чтобы алерт работал быстрее
- Чтобы тревога сработала только после 10 минут непрерывного нарушения
- Чтобы отключить алерт
* Правильный ответ: Чтобы тревога сработала только после 10 минут непрерывного нарушения
for отсекает ложные срабатывания от кратковременных всплесков.

Что такое SLO?
- Целевой уровень качества сервиса (например, 99.9% успешных запросов)
- Список сервисов
- Протокол мониторинга
* Правильный ответ: Целевой уровень качества сервиса (например, 99.9% успешных запросов)
SLO — цель, от которой считаются burn rate и алерты.

Почему метка job="orders" в выражении up{job="orders"} важна?
- Это необязательное украшение
- Она выделяет метрики конкретного сервиса среди всех собираемых
- Она отключает алерт
* Правильный ответ: Она выделяет метрики конкретного сервиса среди всех собираемых
Без job алерт сработал бы по любому экземпляру.
<!--/QUIZ-->
