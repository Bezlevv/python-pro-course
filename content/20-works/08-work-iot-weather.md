---
title: Самостоятельная работа: IoT-метеостанция на MicroPython
summary: Построение автономной метеостанции на MicroPython: датчик DHT22, чтение и обработка, лог на устройстве, отправка по WiFi на сервер и устойчивый цикл сбора данных.
order: 8
duration: 240 мин
difficulty: advanced
tags: micropython, dht22, wifi, urequests, iot, raspberry pi pico
---

# Самостоятельная работа: IoT-метеостанция на MicroPython

Привет! Это самостоятельная работа уровня advanced. За 240 минут ты построишь настоящую IoT-метеостанцию на микроконтроллере (Raspberry Pi Pico W или ESP32) и MicroPython: она будет измерять температуру и влажность, логировать данные на устройстве и отправлять их по WiFi на сервер. Это реальный инженерный проект — от железа до веб-приёмника.

## Постановка задачи

Агропарк «Весна» хочет контролировать микроклимат в теплице: температуру и влажность воздуха. Данные нужны в цифровом виде — с автоматической передачей на сервер, чтобы агроном мог следить за показаниями из офиса. Ты должен собрать прототип метеостанции.

Аппаратная часть:

- микроконтроллер Raspberry Pi Pico W или ESP32 (с WiFi);
- датчик температуры и влажности DHT22 (цифровой, 1-wire);
- опционально OLED-дисплей SSD1306 (128×64, I2C) или светодиод статуса.

Программная часть на MicroPython:

1. **Пин-аут и чтение**: DHT22 подключён к пину GP15 (Pico W) или GPIO15 (ESP32); данные читаются через библиотеку `dht`.
2. **Обработка**: фильтрация сбойных чтений, усреднение нескольких измерений, округление, проверка физических диапазонов.
3. **Локальный лог**: каждое измерение дописывается в файл `log.txt` на устройстве с меткой времени.
4. **Сеть**: подключение к WiFi, отправка JSON-запроса на сервер-приёмник по `urequests.post`.
5. **Автоматика**: бесконечный цикл измерений (раз в 30–60 секунд), устойчивость к сбоям сети и датчика, индикация состояния (OLED или LED).

Серверная часть (запускается на компьютере или VPS): простое FastAPI-приложение `weather_server.py` с эндпоинтом `POST /weather` (принимает JSON: `station_id`, `temperature`, `humidity`, `timestamp`) и `GET /weather` (возвращает все собранные измерения). Данные сохраняются в JSON-файл.

Требования к надёжности:

- сбой чтения DHT22 не должен ронять программу — цикл продолжается;
- потеря сети не должна ронять программу — следующие измерения продолжаются, отправка повторяется;
- программа должна стартовать автоматически при включении питания (файл `main.py` в корне файловой системы);
- весь код — в модулях `config.py`, `sensor.py`, `network_utils.py`, `main.py`.

## Что ты повторишь

MicroPython: `machine.Pin`, `dht.DHT22`, `network.WLAN`, `urequests`, `utime`, `gc`, файловый ввод-вывод, обработка исключений, фоновые задержки. FastAPI: `POST`/`GET`-эндпоинты, Pydantic-модель, CORS (при необходимости).

## План работы

Иди по этапам по порядку. Сначала — чтение датчика, потом логирование, потом сеть и автоматика. Каждый этап проверяется запуском на реальном устройстве.

<!--TASK-->
### Задача 1
Создай модуль `config.py`: в нём константы — пин датчика (`SENSOR_PIN = 15`), SSID и пароль WiFi (`WIFI_SSID`, `WIFI_PASSWORD`), адрес сервера (`SERVER_URL = "http://192.168.1.100:8000/weather"`), интервал измерений в секундах, `STATION_ID = "teplica-1"`. Затем создай `sensor.py` с функцией `read_sensor()`, которая создаёт объект `dht.DHT22(machine.Pin(SENSOR_PIN))`, вызывает `measure()`, возвращает кортеж `(temperature, humidity)` (температура с одним знаком после запятой, влажность — целая). Оберни вызов в `try/except` и в случае ошибки печатай предупреждение и возвращай `None`. В этом же модуле напиши `read_average(n=3)`, которая делает `n` измерений и возвращает среднее. Ожидаемый результат: запуск `python sensor.py` на устройстве (через `mpremote` или REPL) выводит температуру и влажность; при отсоединении датчика — аккуратное сообщение об ошибке вместо краха.

### Задача 2
Напиши функцию `validate_reading(temperature, humidity)` в `sensor.py`: температура вне диапазона (−40…+80 °C) или влажность вне (0…100 %) считаются некорректными; при некорректных данных возвращай `False`. Добавь функцию `format_record(temperature, humidity)`, которая возвращает строку лога вида `2026-11-01 14:30:05 | 23.4C | 55%`. Для времени используй `utime.localtime()`. Создай функцию `append_log(record)` в новом модуле `logger.py`: открывает файл `log.txt` в режиме дописывания (`a`), пишет строку и закрывает. Ожидаемый результат: после запуска в `log.txt` появляются строки с датой-временем, температурой и влажностью; валидация отклоняет нефизичные значения.

### Задача 3
Создай `network_utils.py` с функцией `connect_wifi()`: инициализация `network.WLAN(network.STA_IF)`, активация (`active(True)`), подключение `connect(ssid, password)` в цикле с ожиданием до 15 секунд (проверка `wlan.isconnected()`), вывод полученного IP через `wlan.ifconfig()[0]`. Если подключение не удалось — возвращай `False`, иначе `True`. Затем добавь функцию `send_reading(temperature, humidity)`, которая формирует JSON `{"station_id": STATION_ID, "temperature": temperature, "humidity": humidity, "timestamp": ...}` и отправляет `urequests.post(SERVER_URL, json=payload, timeout=5)`, закрывает ответ (`resp.close()`) и возвращает статус-код. Ожидаемый результат: при запущенном `weather_server.py` станция подключается к WiFi, отправляет данные, а сервер их принимает и сохраняет.

### Задача 4
Создай `weather_server.py` — приёмник на FastAPI: модель Pydantic `WeatherReading` (поля `station_id`, `temperature`, `humidity`, `timestamp`), эндпоинт `POST /weather` (валидация, сохранение в `measurements.json` как список словарей, возврат `{"status": "ok"}`, код 201), эндпоинт `GET /weather` (возврат всех измерений), у `GET /weather?limit=10` — последние 10. При старте сервер создаёт файл, если его нет. Ожидаемый результат: `uvicorn weather_server:app --reload` стартует, `POST` с валидным JSON возвращает 201, `GET /weather` показывает накопленные измерения.

### Задача 5
Создай `main.py` — главный цикл: инициализация WiFi (один раз), затем бесконечный цикл `while True`: измерение через `read_average(3)`, валидация, логирование в файл, при наличии сети — отправка на сервер, ожидание `INTERVAL` секунд. Все внешние операции (сеть, сервер, датчик) — в `try/except` с сообщением об ошибке, но без выхода из цикла. Добавь индикацию: если есть OLED (SSD1306) — вывод температуры и влажности на экран; если нет — короткие блики встроенного светодиода при успешной отправке (2 коротких) и при ошибке (3 длинных). Ожидаемый результат: станция работает часами без остановок, данные регулярно появляются в `measurements.json`, а логирование и повторные попытки отправки работают даже при перебоях сети.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
DHT22 — цифровой датчик, обмен происходит по одному проводу. Подключение: VCC → 3V3, GND → GND, DATA → GP15 (через подтягивающий резистор 4.7–10 кОм к 3V3). Импорт: `import dht`, `import machine`. Объект: `sensor = dht.DHT22(machine.Pin(15))`, дальше `sensor.measure()` и `sensor.temperature()` / `sensor.humidity()`. `measure()` может бросить `OSError` — лови и его. В MicroPython нет `float(input())` — просто конвертируй `sensor.temperature()` в float: значения уже float. `round(x, 1)` для температуры.

### Подсказка 2
`utime.localtime()` возвращает кортеж `(year, month, day, hour, minute, second, weekday, yearday)`. Форматируй через `"{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"`. С файлами в MicroPython всё как в обычном Python: `with open("log.txt", "a") as f: f.write(record + "\n")`. Валидация: `if not (-40 <= temperature <= 80 and 0 <= humidity <= 100): return False`.

### Подсказка 3
Порядок для WiFi: `wlan = network.WLAN(network.STA_IF)`, `wlan.active(True)`, затем `wlan.connect(ssid, password)`, и цикл `while not wlan.isconnected() and attempts < 15: utime.sleep(1)`. `urequests.post(url, json=payload, timeout=5)` — библиотека уже есть в стандартной прошивке; если нет — установи через `mpremote mip install urequests`. Обязательно `resp.close()`, иначе память утекает.

### Подсказка 4
Структура `measurements.json`: список словарей. При старте читай файл, если есть; при отсутствии — `[]`. `POST /weather`: `payload = WeatherReading.model_validate(...)`, `data.append(payload.model_dump())`, запись в файл. Для эндпоинта с `limit`: `data[-limit:]`. Для корректной работы Pydantic v2 используй `model_dump()` вместо `dict()`.

### Подсказка 5
Структура `main.py`: импорт всех модулей, `connect_wifi()`, затем `while True:`. Внутри: `reading = read_average(3)`, если `reading is not None` — валидация, `append_log(format_record(...))`, если `wlan.isconnected()` — `send_reading(...)`. Между итерациями `utime.sleep(INTERVAL)`. Обрабатывай исключения `Exception as e` (или конкретные `OSError`) — печатай `e` и продолжай. Для OLED: `from ssd1306 import SSD1306_I2C`, `i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))` (пины для Pico W), `oled = SSD1306_I2C(128, 64, i2c)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Файл `config.py`:

```python
SENSOR_PIN = 15
WIFI_SSID = "ВСТАВЬ_СВОЙ_SSID"
WIFI_PASSWORD = "ВСТАВЬ_ПАРОЛЬ"
SERVER_URL = "http://192.168.1.100:8000/weather"
STATION_ID = "teplica-1"
INTERVAL = 60  # секунд между измерениями
```

Файл `sensor.py`:

```python
import dht
import machine
import utime
from config import SENSOR_PIN

_sensor = dht.DHT22(machine.Pin(SENSOR_PIN))


def read_sensor():
    try:
        _sensor.measure()
        temperature = round(_sensor.temperature(), 1)
        humidity = int(_sensor.humidity())
        return temperature, humidity
    except OSError as e:
        print("Ошибка чтения DHT22:", e)
        return None


def read_average(n=3):
    values = []
    for _ in range(n):
        r = read_sensor()
        if r is not None:
            values.append(r)
        utime.sleep(1)
    if not values:
        return None
    temp = round(sum(v[0] for v in values) / len(values), 1)
    hum = int(sum(v[1] for v in values) / len(values))
    return temp, hum
```

DHT22 общается с контроллером по протоколу 1-wire: `measure()` отправляет стартовый сигнал и читает 40 бит данных, поэтому он может бросить `OSError` (например, если датчик отсоединён или сбой линии). Ключевая идея — обернуть опасное чтение: программа никогда не падает, а возвращает `None`, и вызывающий код решает, что делать. `read_average` делает несколько измерений и усредняет: это сглаживает случайные «дребезги» датчика. Обрати внимание на `utime` — его тоже нужно импортировать (`import utime`), если используешь `utime.sleep()` в `read_average`. Запуск проверки: `mpremote run sensor.py` (или вставь код в REPL).

### Разбор 2
Добавляем валидацию и лог в `sensor.py` и `logger.py`:

```python
def validate_reading(temperature, humidity):
    return -40 <= temperature <= 80 and 0 <= humidity <= 100


def format_record(temperature, humidity):
    now = utime.localtime()
    ts = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2], now[3], now[4], now[5])
    return f"{ts} | {temperature}C | {humidity}%"
```

Файл `logger.py`:

```python
def append_log(record):
    with open("log.txt", "a") as f:
        f.write(record + "\n")
```

`validate_reading` отсекает нефизичные значения: DHT22 умеет измерять только −40…+80 °C и 0…100 % влажности. Если датчик «свихнулся» (плохой контакт), его показания не попадут ни в лог, ни на сервер. `format_record` собирает читаемую строку: `utime.localtime()` возвращает кортеж из восьми чисел (год, месяц, день, час, минута, секунда, день недели, день года), и мы форматируем первые шесть. Файловый ввод-вывод в MicroPython почти идентичен обычному Python; режим `"a"` дописывает в конец файла. `with` автоматически закрывает файл — это важно на микроконтроллере, где файловая система работает с флеш-памяти и незакрытые файлы могут терять данные.

### Разбор 3
Файл `network_utils.py`:

```python
import network
import utime
import urequests
from config import WIFI_SSID, WIFI_PASSWORD, SERVER_URL, STATION_ID

wlan = network.WLAN(network.STA_IF)


def connect_wifi(timeout=15):
    wlan.active(True)
    if not wlan.isconnected():
        print("Подключение к WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        attempts = 0
        while not wlan.isconnected() and attempts < timeout:
            utime.sleep(1)
            attempts += 1
    if wlan.isconnected():
        print("IP-адрес:", wlan.ifconfig()[0])
        return True
    print("Не удалось подключиться к WiFi")
    return False


def send_reading(temperature, humidity):
    try:
        payload = {
            "station_id": STATION_ID,
            "temperature": temperature,
            "humidity": humidity,
            "timestamp": "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(
                *utime.localtime()[:6]),
        }
        resp = urequests.post(SERVER_URL, json=payload, timeout=5)
        status = resp.status_code
        resp.close()
        print("Отправлено, статус:", status)
        return status
    except Exception as e:
        print("Ошибка отправки:", e)
        return None
```

`network.WLAN(network.STA_IF)` — объект станции (клиента WiFi). `active(True)` включает радио. `connect` — асинхронный вызов: возвращается сразу, а реальное подключение занимает время, поэтому нужен цикл ожидания с проверкой `isconnected()` и таймаутом. `ifconfig()[0]` — IP-адрес. `urequests.post` по синтаксису похож на `requests`; `json=payload` сам сериализует словарь. `timeout=5` предохраняет от зависания. `resp.close()` обязателен: соединение сокета должно закрываться, иначе через много отправок закончится память. Формат метки времени `ISO 8601` с `T`-разделителем удобно парсить на сервере. Если прошивка не содержит `urequests` — установи: `mpremote mip install urequests`.

### Разбор 4
Файл `weather_server.py`:

```python
import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Weather Receiver")
FILE = Path("measurements.json")


class WeatherReading(BaseModel):
    station_id: str
    temperature: float
    humidity: int
    timestamp: str


def load_data():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    return []


def save_data(data):
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                    encoding="utf-8")


@app.post("/weather", status_code=201)
def add_reading(reading: WeatherReading):
    data = load_data()
    data.append(reading.model_dump())
    save_data(data)
    return {"status": "ok", "saved": reading.model_dump()}


@app.get("/weather")
def list_readings(limit: int | None = None):
    data = load_data()
    if limit is not None:
        return data[-limit:]
    return data
```

Сервер хранит измерения в JSON-файле — для прототипа этого достаточно (в бою здесь была бы база данных). Pydantic-модель `WeatherReading` автоматически валидирует входящий JSON: тип `float` для температуры, `int` для влажности, обязательные поля. Если станция пришлёт мусор — FastAPI вернёт 422. `model_dump()` превращает валидированную модель в словарь для сохранения. Эндпоинт `GET /weather?limit=10` отдаёт последние 10 измерений — удобно для проверки «вживую» в браузере. Запуск: `uvicorn weather_server:app --reload`. Для доступа с устройства из той же сети адрес — `http://<IP компьютера>:8000/weather`; не забудь разрешить порт 8000 в файрволе.

### Разбор 5
Файл `main.py`:

```python
import utime
import gc
import machine
from config import INTERVAL
from sensor import read_average, validate_reading, format_record
from logger import append_log
import network_utils

connected = network_utils.connect_wifi()

# опционально: OLED
try:
    from ssd1306 import SSD1306_I2C
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
    oled = SSD1306_I2C(128, 64, i2c)
except Exception:
    oled = None

led = machine.Pin("LED", machine.Pin.OUT) if hasattr(machine.Pin, "LED") \
    else None


def blink(n, long=False):
    if led is None:
        return
    for _ in range(n):
        led.on()
        utime.sleep(0.2 if not long else 0.8)
        led.off()
        utime.sleep(0.2)


while True:
    reading = read_average(3)
    if reading is not None:
        temperature, humidity = reading
        if validate_reading(temperature, humidity):
            record = format_record(temperature, humidity)
            print(record)
            append_log(record)
            if oled is not None:
                oled.fill(0)
                oled.text(f"T: {temperature}C", 0, 10)
                oled.text(f"H: {humidity}%", 0, 30)
                oled.show()
            if network_utils.wlan.isconnected():
                status = network_utils.send_reading(temperature, humidity)
                if status == 201:
                    blink(2)
                else:
                    blink(3, long=True)
            else:
                print("Сеть недоступна, пропускаю отправку")
                blink(1, long=True)
    gc.collect()
    utime.sleep(INTERVAL)
```

Главный цикл — сердце станции. Разделение обязанностей: `sensor` отвечает только за измерение, `logger` — за файл, `network_utils` — за сеть. Перед каждым будущим измерением `read_average` внутри делает три попытки с паузами, поэтому цикл не будет «молотить вхолостую». Валидация отклоняет мусор до логирования. Если сеть пропала — мы не падаем, а просто пропускаем отправку, и следующая итерация повторит попытку: это паттерн *graceful degradation*. `oled` и `led` опциональны и обёрнуты в `try/except` — без дисплея и светодиода программа работает. `gc.collect()` собирает мусор вручную: на микроконтроллере с ~260 КБ RAM это реально важно при долгой работе. С таким каркасом станция крутится дни и недели без перезагрузки.

Итог полного проекта: папка с `config.py`, `sensor.py`, `logger.py`, `network_utils.py`, `main.py` (для устройства) и `weather_server.py` (для компьютера) плюс файл `log.txt` и `measurements.json` с данными.
<!--/SOLUTION-->

## Критерии оценки

| Критерий | Что проверяется | Баллы |
|---|---|---|
| Чтение датчика | `DHT22` подключён, `read_sensor` возвращает корректные значения, обрабатывает `OSError` | 20 |
| Валидация и лог | `validate_reading`, `format_record`, `append_log`; строки в `log.txt` с датой и временем | 15 |
| Сеть | `connect_wifi` с таймаутом, `send_reading` с `resp.close()` | 20 |
| Сервер-приёмник | `POST /weather` сохраняет измерения, `GET /weather?limit=` работает | 15 |
| Главный цикл | устойчив к сбоям, работает 24+ часа, данные регулярно приходят на сервер | 20 |
| Структура кода | Модули разделены, константы в `config.py`, нет хардкода секретов в коде | 10 |

Итого 100 баллов. Оценка: 90+ — «отлично», 75–89 — «хорошо», 60–74 — «удовлетворительно», меньше 60 — работу стоит доработать.

## Что сдать

1. Код устройства: `config.py`, `sensor.py`, `logger.py`, `network_utils.py`, `main.py`.
2. Код сервера: `weather_server.py`.
3. Лог работы: фрагмент `log.txt` (хотя бы 10 строк) и фрагмент `measurements.json` — доказательство, что данные доходили до сервера.
4. Фото/скриншоты: собранная станция с подключённым DHT22, вывод отправки в терминале (mpremote), ответ `/docs` сервера и `GET /weather`.
5. Короткий README: схема подключения (пины), как прошить MicroPython, как установить `urequests`, как запустить сервер и устройство.

<!--QUIZ-->
Какой протокол использует датчик DHT22?
- UART
- 1-wire (один провод данных)
- I2C
- SPI
* Правильный ответ: 1-wire (один провод данных)
DHT22 передаёт данные по одному проводу данных с кастомной синхронизацией, поэтому `measure()` может бросить `OSError` при сбое линии.

Почему вызов `dht.DHT22(...).measure()` оборачивают в `try/except OSError`?
- Чтобы ускорить выполнение
- Чтобы сбой линии или отсутствие датчика не уронило программу
- Чтобы перезагрузить устройство
- Чтобы вывести экранную ошибку
* Правильный ответ: Чтобы сбой линии или отсутствие датчика не уронило программу
`measure()` читает данные через пины; при плохом контакте или неправильной схеме возникнет `OSError`, и программу нужно защитить.

Какую роль играет `read_average(3)`?
- Ограничивает число измерений в сутки
- Делает три измерения и усредняет их, сглаживая дребезг датчика
- Проверяет диапазоны значений
- Отправляет данные три раза
* Правильный ответ: Делает три измерения и усредняет их, сглаживая дребезг датчика
Одиночные измерения DHT22 могут «прыгать»; среднее из нескольких даёт стабильные значения.

Что возвращает `utime.localtime()`?
- Строку с датой
- Кортеж из восьми чисел: год, месяц, день, час, минута, секунда и другие поля
- Объект datetime
- Число секунд с начала эпохи
* Правильный ответ: Кортеж из восьми чисел: год, месяц, день, час, минута, секунда и другие поля
Индексы 0–5 — год, месяц, день, час, минута, секунда; далее день недели и день года.

Зачем нужен `resp.close()` после `urequests.post(...)`?
- Чтобы закрыть файл лога
- Чтобы освободить сокет и память — иначе утечки при длительной работе
- Чтобы отключить WiFi
- Чтобы завершить программу
* Правильный ответ: Чтобы освободить сокет и память — иначе утечки при длительной работе
Каждый не закрытый ответ держит сокет; на микроконтроллере это быстро исчерпает память.

Что произойдёт, если `wlan.connect(WIFI_SSID, WIFI_PASSWORD)` вызвать без цикла ожидания `isconnected()`?
- Программа сразу продолжит работу — подключение мгновенное
- Функция может вернуться до фактического подключения, и отправка данных провалится
- Произойдёт ошибка компиляции
- Соединение установится само
* Правильный ответ: Функция может вернуться до фактического подключения, и отправка данных провалится
`connect()` инициирует подключение асинхронно; ждать готовности нужно проверкой `isconnected()` в цикле.

Какой статус-код возвращает `POST /weather` при успешном сохранении?
- 200
- 201
- 404
- 422
* Правильный ответ: 201
201 Created — семантически верный код для создания ресурса; так же мы помечаем `status_code=201` в декораторе.

Как валидируется тело запроса на сервере `weather_server.py`?
- Вручную через if
- Автоматически моделью Pydantic: неверные типы дают 422
- Через декоратор CORS
- Никак
* Правильный ответ: Автоматически моделью Pydantic: неверные типы дают 422
FastAPI подставляет тело в `WeatherReading`; ошибки валидации превращаются в ответ 422.

Что делает `gc.collect()` в главном цикле?
- Перезагружает устройство
- Запускает сборщик мусора вручную — освобождает неиспользуемую память
- Чистит файл лога
- Отключает WiFi
* Правильный ответ: Запускает сборщик мусора вручную — освобождает неиспользуемую память
На микроконтроллере с малым объёмом RAM регулярный вызов помогает избегать фрагментации и OOM.
<!--/QUIZ-->
