---
title: Sensors and GPIO
summary: Read inputs, common sensors.
order: 2
duration: 45 min
difficulty: intermediate
tags: sensors, gpio
---

Sensors convert physical quantities to signals.

## Digital input

```python
from machine import Pin
button = Pin(0, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("pressed")
```

## Analog

```python
from machine import ADC
adc = ADC(Pin(34))
value = adc.read()   # 0–4095
```

## Common sensors

Temperature, distance (ultrasonic), light, motion.

## Lesson summary

Digital reads 0/1; ADC reads analog voltages.

<!--TASK-->
### Task 1 — Button
Read a button with pull-up.

### Task 2 — Debounce
Add a small delay.

### Task 3 — ADC
Read and print analog.

### Task 4 — Map
Scale 0–4095 to 0–100.

### Task 5 — Temperature idea
Which sensor reads temperature?

### Task 6 — Ultrasonic idea
Which reads distance?

### Task 7 — Safety
Why pull-up resistors?
<!--/TASK-->

<!--HINT-->
### Hint 1
value().

### Hint 2
sleep.

### Hint 3
ADC.

### Hint 4
Scale.

### Hint 5
DHT.

### Hint 6
HC-SR04.

### Hint 7
Stable.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from machine import Pin
button = Pin(0, Pin.IN, Pin.PULL_UP)
while True:
    if button.value() == 0:
        print("pressed")
```

### Solution 2
```python
import time
while True:
    if button.value() == 0:
        print("pressed")
        time.sleep_ms(50)   # debounce
```

### Solution 3
```python
from machine import ADC
adc = ADC(Pin(34))
print(adc.read())
```

### Solution 4
```python
raw = adc.read()
percent = raw * 100 // 4095
```

### Solution 5
```python
# DHT11/DHT22 (температура и влажность),
# DS18B20 (температура)
```

### Solution 6
```python
# HC-SR04 — ультразвуковой дальномер
```

### Solution 7
```python
# Подтяжка определяет стабильный уровень
# на неподключённом входе
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a sensor?
- Physical input
- Output
- CPU
- None
* Correct answer: Physical input
Measure.

What is GPIO?
- Pins
- Memory
- Power
- None
* Correct answer: Pins
I/O.

What is digital?
- 0/1
- Range
- Voltage
- None
* Correct answer: 0/1
Pulse.

What is analog?
- Continuous range
- 0/1
- Text
- None
* Correct answer: Continuous range
ADC.

What is PULL_UP?
- Stable high default
- Low
- None
- Both
* Correct answer: Stable high default
Mode.

What is debounce?
- Filter noise
- Amplify
- Delay only
- None
* Correct answer: Filter noise
Stable.

What is DHT11?
- Temp/humidity
- Distance
- Motion
- None
* Correct answer: Temp/humidity
Sensor.

What is HC-SR04?
- Ultrasonic distance
- Temp
- Light
- None
* Correct answer: Ultrasonic distance
Sensor.

What is ADC?
- Analog-to-digital
- Digital output
- PWM
- None
* Correct answer: Analog-to-digital
Converter.

What is raw value?
- Unscaled
- Percent
- Voltage
- None
* Correct answer: Unscaled
0–4095.

What is scaling?
- Mapping range
- Raising
- Converting
- None
* Correct answer: Mapping range
Percent.

What is a pull-down?
- Stable low default
- High
- None
- Same
* Correct answer: Stable low default
Mode.
<!--/QUIZ-->
