---
title: Projects: smart home
summary: Combine sensors, logic, and notifications.
order: 4
duration: 50 min
difficulty: advanced
tags: project, iot, smart home
---

Build a small smart-home device.

## Idea

Temperature monitor that prints and warns.

## Code

```python
from machine import Pin, ADC
import time
import network
import urequests

adc = ADC(Pin(34))

def read_temp():
    # упрощённо: превращаем сырое значение
    # в градусы по формуле датчика
    raw = adc.read()
    return raw / 4095 * 100

while True:
    t = read_temp()
    print("temp:", t)
    if t > 60:
        print("WARNING: too hot!")
        # тут можно отправить уведомление
    time.sleep(5)
```

## Lesson summary

Combine input, logic, and output.

<!--TASK-->
### Task 1 — Idea
Describe a device idea in 3 lines.

### Task 2 — Read
Read temperature.

### Task 3 — Logic
Add a threshold warning.

### Task 4 — Notify
Send an HTTP notification.

### Task 5 — LED
Blink an LED on warning.

### Task 6 — Log
Keep a history in a list.

### Task 7 — Save
Write data to a file.
<!--/TASK-->

<!--HINT-->
### Hint 1
Sensor.

### Hint 2
ADC.

### Hint 3
If.

### Hint 4
urequests.

### Hint 5
LED.

### Hint 6
Append.

### Hint 7
open().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Устройство: датчик температуры в комнате.
Каждые 5 секунд измеряет температуру.
При перегреве мигает LED и шлёт уведомление.
```

### Solution 2
```python
from machine import ADC
adc = ADC(Pin(34))
raw = adc.read()
```

### Solution 3
```python
if raw > 2000:
    print("hot!")
```

### Solution 4
```python
import urequests
if raw > 2000:
    try:
        r = urequests.post("https://example.com/notify",
                           json={"temp": raw})
        r.close()
    except OSError:
        pass
```

### Solution 5
```python
led = Pin(2, Pin.OUT)
if raw > 2000:
    for _ in range(5):
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.2)
```

### Solution 6
```python
history = []
history.append(raw)
if len(history) > 100:
    history.pop(0)
```

### Solution 7
```python
with open("log.txt", "a") as f:
    f.write(str(raw) + "\n")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an IoT device?
- Connected hardware
- Desktop app
- A website
- None
* Correct answer: Connected hardware
Internet.

What is a threshold?
- Limit
- Sensor
- Loop
- None
* Correct answer: Limit
If.

What is a notification?
- Alert
- Log
- LED
- None
* Correct answer: Alert
HTTP.

What is history?
- Past values
- Future
- One value
- None
* Correct answer: Past values
List.

What is a log file?
- Append-only record
- Overwrite
- Binary only
- None
* Correct answer: Append-only record
"a".

What is the main loop?
- Infinite cycle
- One run
- None
- Error
* Correct answer: Infinite cycle
while True.

What is a delay?
- Pause
- Speed
- Loop
- None
* Correct answer: Pause
sleep.

What is combining?
- Sensor + logic + output
- Sensor only
- Logic only
- None
* Correct answer: Sensor + logic + output
Project.

What is the output?
- Action
- Reading
- Input
- None
* Correct answer: Action
LED/HTTP.

What is an API call?
- HTTP request
- Sensor read
- Loop
- None
* Correct answer: HTTP request
Notify.

What is robustness?
- Handles errors
- Crashes
- Simple
- None
* Correct answer: Handles errors
try.

What is a prototype?
- Simple working version
- Final
- Design
- None
* Correct answer: Simple working version
First.
<!--/QUIZ-->
