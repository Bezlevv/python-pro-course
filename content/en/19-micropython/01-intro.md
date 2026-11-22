---
title: MicroPython on microcontrollers
summary: What MicroPython is, boards, blink.
order: 1
duration: 40 min
difficulty: intermediate
tags: micropython, embedded
---

MicroPython runs Python on small boards.

## What

A lean Python 3 implementation for microcontrollers.

## Boards

ESP32, Raspberry Pi Pico, micro:bit.

## Blink

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)
while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```

## Lesson summary

MicroPython brings Python to hardware.

<!--TASK-->
### Task 1 — Import
Import Pin.

### Task 2 — Setup
Set pin as output.

### Task 3 — Loop
Blink with sleep.

### Task 4 — Read
Read a digital input.

### Task 5 — ADC
Read an analog value.

### Task 6 — Board
Name two boards.

### Task 7 — Compare
Differences from desktop Python.
<!--/TASK-->

<!--HINT-->
### Hint 1
machine.

### Hint 2
Pin.OUT.

### Hint 3
time.sleep.

### Hint 4
Pin.IN.

### Hint 5
ADC.

### Hint 6
ESP32.

### Hint 7
Modules.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from machine import Pin
```

### Solution 2
```python
led = Pin(2, Pin.OUT)
```

### Solution 3
```python
import time
while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
```

### Solution 4
```python
button = Pin(0, Pin.IN, Pin.PULL_UP)
print(button.value())   # 0 или 1
```

### Solution 5
```python
from machine import ADC
adc = ADC(Pin(34))
print(adc.read())   # 0–4095
```

### Solution 6
```python
# ESP32, Raspberry Pi Pico, micro:bit,
# STM32, nRF52
```

### Solution 7
```python
# Минимум памяти, свои модули (machine),
# нет больших стандартных библиотек
```
<!--/SOLUTION-->

<!--QUIZ-->
What is MicroPython?
- For microcontrollers
- Desktop Python
- A browser
- None
* Correct answer: For microcontrollers
Lean.

What is ESP32?
- Board
- A library
- A protocol
- None
* Correct answer: Board
Wi-Fi.

What is Pin?
- GPIO control
- A connector
- A module
- None
* Correct answer: GPIO control
machine.

What is Pin.OUT?
- Output mode
- Input
- Analog
- None
* Correct answer: Output mode
Write.

What is value(1)?
- High
- Low
- Read
- None
* Correct answer: High
On.

What is sleep?
- Pause
- Loop
- Pin
- None
* Correct answer: Pause
Seconds.

What is ADC?
- Analog read
- Digital
- Output
- None
* Correct answer: Analog read
Voltage.

What is PULL_UP?
- Resistor mode
- LED
- Loop
- None
* Correct answer: Resistor mode
Input.

What is GPIO?
- General purpose I/O
- A file
- A library
- None
* Correct answer: General purpose I/O
Pins.

What is a micro:bit?
- Board
- A chip only
- A laptop
- None
* Correct answer: Board
Educational.

What is the pin number?
- GPIO index
- Voltage
- Time
- None
* Correct answer: GPIO index
2/0/34.

What is embedded?
- Inside hardware
- Desktop
- Cloud
- None
* Correct answer: Inside hardware
IoT.
<!--/QUIZ-->
