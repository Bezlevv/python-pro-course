---
title: Independent Work: IoT Weather Station on MicroPython
summary: Build an autonomous weather station on MicroPython: DHT22 sensor, reading and processing, on-device logging, sending over WiFi to a server, and a resilient data collection loop.
order: 8
duration: 240 min
difficulty: advanced
tags: micropython, dht22, wifi, urequests, iot, raspberry pi pico
---

# Independent Work: IoT Weather Station on MicroPython

Hi! This is an advanced-level independent work. In 240 minutes you will build a real IoT weather station on a microcontroller (Raspberry Pi Pico W or ESP32) with MicroPython: it will measure temperature and humidity, log data on the device, and send it over WiFi to a server. This is a real engineering project — from hardware to a web receiver.

## Problem statement

The agropark «Весна» wants to control the microclimate in a greenhouse: air temperature and humidity. The data must be digital — with automatic transmission to a server, so the agronomist can monitor readings from the office. You need to assemble a weather station prototype.

Hardware part:

- a microcontroller Raspberry Pi Pico W or ESP32 (with WiFi);
- a DHT22 temperature and humidity sensor (digital, 1-wire);
- optionally an OLED display SSD1306 (128×64, I2C) or a status LED.

Software part in MicroPython:

1. **Pinout and reading**: DHT22 is connected to pin GP15 (Pico W) or GPIO15 (ESP32); data is read via the `dht` library.
2. **Processing**: filtering failed readings, averaging several measurements, rounding, checking physical ranges.
3. **Local log**: each measurement is appended to the `log.txt` file on the device with a timestamp.
4. **Network**: connect to WiFi and send a JSON request to the receiver server via `urequests.post`.
5. **Automation**: an infinite measurement loop (every 30–60 seconds), resilience to network and sensor failures, status indication (OLED or LED).

Server part (runs on a computer or VPS): a simple FastAPI application `weather_server.py` with the endpoint `POST /weather` (accepts JSON: `station_id`, `temperature`, `humidity`, `timestamp`) and `GET /weather` (returns all collected measurements). Data is saved to a JSON file.

Reliability requirements:

- a DHT22 read failure must not crash the program — the loop continues;
- a network loss must not crash the program — subsequent measurements continue, sending is retried;
- the program must start automatically on power-up (the `main.py` file in the root of the filesystem);
- all code — in the modules `config.py`, `sensor.py`, `network_utils.py`, `main.py`.

## What you will review

MicroPython: `machine.Pin`, `dht.DHT22`, `network.WLAN`, `urequests`, `utime`, `gc`, file input-output, exception handling, background delays. FastAPI: `POST`/`GET` endpoints, a Pydantic model, CORS (if needed).

## Work plan

Go through the stages in order. First — sensor reading, then logging, then network and automation. Each stage is verified by running on a real device.

<!--TASK-->
### Task 1
Create the module `config.py`: constants in it — the sensor pin (`SENSOR_PIN = 15`), WiFi SSID and password (`WIFI_SSID`, `WIFI_PASSWORD`), the server address (`SERVER_URL = "http://192.168.1.100:8000/weather"`), the measurement interval in seconds, `STATION_ID = "teplica-1"`. Then create `sensor.py` with the function `read_sensor()` that creates a `dht.DHT22(machine.Pin(SENSOR_PIN))` object, calls `measure()`, and returns a tuple `(temperature, humidity)` (temperature with one decimal place, humidity as an integer). Wrap the call in `try/except` and on error print a warning and return `None`. In the same module write `read_average(n=3)` that takes `n` measurements and returns the average. Expected result: running `python sensor.py` on the device (via `mpremote` or REPL) prints temperature and humidity; when the sensor is disconnected — a neat error message instead of a crash.

### Task 2
Write the function `validate_reading(temperature, humidity)` in `sensor.py`: temperature outside (−40…+80 °C) or humidity outside (0…100 %) counts as invalid; on invalid data return `False`. Add the function `format_record(temperature, humidity)` that returns a log line like `2026-11-01 14:30:05 | 23.4C | 55%`. For time use `utime.localtime()`. Create the function `append_log(record)` in a new module `logger.py`: it opens the `log.txt` file in append mode (`a`), writes the line, and closes. Expected result: after running, `log.txt` contains lines with date-time, temperature, and humidity; validation rejects non-physical values.

### Task 3
Create `network_utils.py` with the function `connect_wifi()`: initialize `network.WLAN(network.STA_IF)`, activate (`active(True)`), connect `connect(ssid, password)` in a loop waiting up to 15 seconds (checking `wlan.isconnected()`), print the obtained IP via `wlan.ifconfig()[0]`. If the connection fails — return `False`, otherwise `True`. Then add the function `send_reading(temperature, humidity)` that builds JSON `{"station_id": STATION_ID, "temperature": temperature, "humidity": humidity, "timestamp": ...}` and sends `urequests.post(SERVER_URL, json=payload, timeout=5)`, closes the response (`resp.close()`), and returns the status code. Expected result: with `weather_server.py` running, the station connects to WiFi, sends data, and the server receives and saves it.

### Task 4
Create `weather_server.py` — a FastAPI receiver: a Pydantic model `WeatherReading` (fields `station_id`, `temperature`, `humidity`, `timestamp`), the endpoint `POST /weather` (validation, saving to `measurements.json` as a list of dictionaries, returning `{"status": "ok"}`, code 201), the endpoint `GET /weather` (returns all measurements), and `GET /weather?limit=10` — the last 10. On startup the server creates the file if it doesn't exist. Expected result: `uvicorn weather_server:app --reload` starts, `POST` with valid JSON returns 201, `GET /weather` shows accumulated measurements.

### Task 5
Create `main.py` — the main loop: initialize WiFi (once), then an infinite loop `while True`: measure via `read_average(3)`, validate, log to a file, and if the network is up — send to the server, wait `INTERVAL` seconds. All external operations (network, server, sensor) — in `try/except` with an error message, but without exiting the loop. Add indication: if there is an OLED (SSD1306) — show temperature and humidity on screen; if not — short blinks of the built-in LED on successful send (2 short) and on error (3 long). Expected result: the station works for hours without stopping, data regularly appears in `measurements.json`, and logging and send retries work even with network interruptions.

<!--/TASK-->

<!--HINT-->
### Hint 1
DHT22 is a digital sensor; communication happens over one wire. Wiring: VCC → 3V3, GND → GND, DATA → GP15 (through a 4.7–10 kΩ pull-up resistor to 3V3). Import: `import dht`, `import machine`. Object: `sensor = dht.DHT22(machine.Pin(15))`, then `sensor.measure()` and `sensor.temperature()` / `sensor.humidity()`. `measure()` may raise `OSError` — catch that too. MicroPython has no `float(input())` — just convert `sensor.temperature()` to float: the values are already floats. `round(x, 1)` for temperature.

### Hint 2
`utime.localtime()` returns a tuple `(year, month, day, hour, minute, second, weekday, yearday)`. Format with `"{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}"`. Files in MicroPython work like in regular Python: `with open("log.txt", "a") as f: f.write(record + "\n")`. Validation: `if not (-40 <= temperature <= 80 and 0 <= humidity <= 100): return False`.

### Hint 3
WiFi order: `wlan = network.WLAN(network.STA_IF)`, `wlan.active(True)`, then `wlan.connect(ssid, password)`, and a loop `while not wlan.isconnected() and attempts < 15: utime.sleep(1)`. `urequests.post(url, json=payload, timeout=5)` — the library is already in the standard firmware; if not, install it via `mpremote mip install urequests`. Definitely `resp.close()`, otherwise memory leaks.

### Hint 4
`measurements.json` structure: a list of dictionaries. On startup read the file if it exists; if absent — `[]`. `POST /weather`: `payload = WeatherReading.model_validate(...)`, `data.append(payload.model_dump())`, write to the file. For the endpoint with `limit`: `data[-limit:]`. For correct Pydantic v2 behavior use `model_dump()` instead of `dict()`.

### Hint 5
`main.py` structure: import all modules, `connect_wifi()`, then `while True:`. Inside: `reading = read_average(3)`; if `reading is not None` — validate, `append_log(format_record(...))`, and if `wlan.isconnected()` — `send_reading(...)`. Between iterations `utime.sleep(INTERVAL)`. Handle exceptions `Exception as e` (or specific `OSError`) — print `e` and continue. For OLED: `from ssd1306 import SSD1306_I2C`, `i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))` (pins for Pico W), `oled = SSD1306_I2C(128, 64, i2c)`.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
File `config.py`:

```python
SENSOR_PIN = 15
WIFI_SSID = "INSERT_YOUR_SSID"
WIFI_PASSWORD=[redacted]
SERVER_URL = "http://192.168.1.100:8000/weather"
STATION_ID = "teplica-1"
INTERVAL = 60  # секунд между измерениями
```

File `sensor.py`:

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

DHT22 talks to the controller over the 1-wire protocol: `measure()` sends a start signal and reads 40 bits of data, so it can raise `OSError` (for example, if the sensor is disconnected or the line is faulty). The key idea is to wrap the dangerous read: the program never crashes but returns `None`, and the calling code decides what to do. `read_average` takes several measurements and averages them: this smooths out random sensor "jitter". Note `utime` — import it too (`import utime`) if you use `utime.sleep()` in `read_average`. Check run: `mpremote run sensor.py` (or paste the code into REPL).

### Solution 2
We add validation and the log to `sensor.py` and `logger.py`:

```python
def validate_reading(temperature, humidity):
    return -40 <= temperature <= 80 and 0 <= humidity <= 100


def format_record(temperature, humidity):
    now = utime.localtime()
    ts = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2], now[3], now[4], now[5])
    return f"{ts} | {temperature}C | {humidity}%"
```

File `logger.py`:

```python
def append_log(record):
    with open("log.txt", "a") as f:
        f.write(record + "\n")
```

`validate_reading` rejects non-physical values: DHT22 can only measure −40…+80 °C and 0…100 % humidity. If the sensor "goes mad" (bad contact), its readings get into neither the log nor the server. `format_record` builds a readable line: `utime.localtime()` returns a tuple of eight numbers (year, month, day, hour, minute, second, weekday, day of year), and we format the first six. File I/O in MicroPython is nearly identical to regular Python; mode `"a"` appends to the end of the file. `with` closes the file automatically — this matters on a microcontroller where the filesystem works with flash memory and unclosed files can lose data.

### Solution 3
File `network_utils.py`:

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

`network.WLAN(network.STA_IF)` is the station object (a WiFi client). `active(True)` turns the radio on. `connect` is an asynchronous call: it returns immediately, while the actual connection takes time, so a waiting loop with an `isconnected()` check and timeout is needed. `ifconfig()[0]` is the IP address. `urequests.post` is syntactically similar to `requests`; `json=payload` serializes the dictionary itself. `timeout=5` guards against hanging. `resp.close()` is mandatory: the socket connection must be closed, otherwise after many sends the memory runs out. The ISO 8601 timestamp format with the `T` separator is convenient to parse on the server. If the firmware lacks `urequests`, install it: `mpremote mip install urequests`.

### Solution 4
File `weather_server.py`:

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

The server stores measurements in a JSON file — enough for a prototype (in production there would be a database here). The Pydantic model `WeatherReading` automatically validates incoming JSON: type `float` for temperature, `int` for humidity, required fields. If the station sends garbage, FastAPI returns 422. `model_dump()` turns the validated model into a dictionary for saving. The endpoint `GET /weather?limit=10` returns the last 10 measurements — handy for "live" checks in a browser. Run: `uvicorn weather_server:app --reload`. For device access from the same network, the address is `http://<IP компьютера>:8000/weather`; don't forget to allow port 8000 in the firewall.

### Solution 5
File `main.py`:

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

The main loop is the station's heart. Separation of responsibilities: `sensor` only measures, `logger` only handles the file, `network_utils` only handles the network. Before each upcoming measurement, `read_average` internally makes three attempts with pauses, so the loop won't "thrash" idle. Validation rejects garbage before logging. If the network is down, we don't crash — we just skip the send, and the next iteration retries: this is the *graceful degradation* pattern. `oled` and `led` are optional and wrapped in `try/except` — without a display and LED the program works. `gc.collect()` collects garbage manually: on a microcontroller with ~260 KB RAM this genuinely matters during long runs. With such a skeleton the station runs for days and weeks without a reboot.

The whole project's result: a folder with `config.py`, `sensor.py`, `logger.py`, `network_utils.py`, `main.py` (for the device) and `weather_server.py` (for the computer), plus `log.txt` and `measurements.json` with data.

<!--/SOLUTION-->

## Assessment criteria

| Criterion | What is checked | Points |
|---|---|---|
| Sensor reading | `DHT22` connected, `read_sensor` returns correct values, handles `OSError` | 20 |
| Validation and log | `validate_reading`, `format_record`, `append_log`; `log.txt` lines with date and time | 15 |
| Network | `connect_wifi` with timeout, `send_reading` with `resp.close()` | 20 |
| Receiver server | `POST /weather` saves measurements, `GET /weather?limit=` works | 15 |
| Main loop | resilient to failures, runs 24+ hours, data regularly reaches the server | 20 |
| Code structure | Modules separated, constants in `config.py`, no hardcoded secrets in code | 10 |

Total 100 points. Grade: 90+ — "excellent", 75–89 — "good", 60–74 — "satisfactory", below 60 — the work should be refined.

## What to submit

1. Device code: `config.py`, `sensor.py`, `logger.py`, `network_utils.py`, `main.py`.
2. Server code: `weather_server.py`.
3. Work log: a fragment of `log.txt` (at least 10 lines) and a fragment of `measurements.json` — proof that data reached the server.
4. Photos/screenshots: the assembled station with DHT22 connected, send output in the terminal (mpremote), the server's `/docs` response, and `GET /weather`.
5. A short README: wiring diagram (pins), how to flash MicroPython, how to install `urequests`, how to run the server and the device.

<!--QUIZ-->
Which protocol does the DHT22 sensor use?
- UART
- 1-wire (one data wire)
- I2C
- SPI
* Correct answer: 1-wire (one data wire)
DHT22 transmits data over one data wire with custom synchronization, so `measure()` may raise `OSError` on a line fault.

Why is the `dht.DHT22(...).measure()` call wrapped in `try/except OSError`?
- To speed up execution
- So a line fault or a missing sensor doesn't crash the program
- To reboot the device
- To show a screen error
* Correct answer: So a line fault or a missing sensor doesn't crash the program
`measure()` reads data through pins; with bad contact or a wrong circuit an `OSError` occurs, and the program must be protected.

What role does `read_average(3)` play?
- Limits the number of daily measurements
- Takes three measurements and averages them, smoothing sensor jitter
- Checks value ranges
- Sends data three times
* Correct answer: Takes three measurements and averages them, smoothing sensor jitter
Single DHT22 readings can "jump"; the average of several gives stable values.

What does `utime.localtime()` return?
- A date string
- A tuple of eight numbers: year, month, day, hour, minute, second, and other fields
- A datetime object
- Seconds since the epoch
* Correct answer: A tuple of eight numbers: year, month, day, hour, minute, second, and other fields
Indices 0–5 are year, month, day, hour, minute, second; then weekday and day of year.

Why is `resp.close()` needed after `urequests.post(...)`?
- To close the log file
- To free the socket and memory — otherwise leaks during long operation
- To turn off WiFi
- To end the program
* Correct answer: To free the socket and memory — otherwise leaks during long operation
Every unclosed response holds a socket; on a microcontroller this quickly exhausts memory.

What happens if `wlan.connect(WIFI_SSID, WIFI_PASSWORD)` is called without a wait loop for `isconnected()`?
- The program immediately continues — the connection is instant
- The function may return before the actual connection, and sending data will fail
- A compilation error occurs
- The connection establishes itself
* Correct answer: The function may return before the actual connection, and sending data will fail
`connect()` initiates the connection asynchronously; readiness must be awaited by checking `isconnected()` in a loop.

What status code does `POST /weather` return on successful saving?
- 200
- 201
- 404
- 422
* Correct answer: 201
201 Created is the semantically correct code for creating a resource; that's how we mark `status_code=201` in the decorator.

How is the request body validated on the `weather_server.py` server?
- Manually with if
- Automatically by a Pydantic model: wrong types give 422
- Via a CORS decorator
- Not at all
* Correct answer: Automatically by a Pydantic model: wrong types give 422
FastAPI inserts the body into `WeatherReading`; validation errors turn into a 422 response.

What does `gc.collect()` do in the main loop?
- Reboots the device
- Runs the garbage collector manually — frees unused memory
- Cleans the log file
- Turns off WiFi
* Correct answer: Runs the garbage collector manually — frees unused memory
On a microcontroller with little RAM, regular calls help avoid fragmentation and OOM.
<!--/QUIZ-->
