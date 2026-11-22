---
title: GPIO: buttons and sensors
summary: We read digital inputs — buttons with pull-up and debouncing, as well as analog signals via ADC and the DHT22 temperature sensor.
order: 3
duration: 30 min
difficulty: intermediate
tags: micropython, gpio, buttons, adc, dht22, pull-up, debounce
---

In the last lesson we learned to control outputs — apply voltage to an LED. Now we'll learn to read inputs: find out whether a button is pressed, what voltage is on a pin, what the room temperature is. This turns the board from a "blinker" into a device that reacts to the world around it.

## Digital input: a button

A button is the simplest sensor. When pressed, it closes the circuit; when released, it opens it. Connect a button between pin 14 and GND:

```python
from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_UP)
```

Pay attention to `Pin.PULL_UP` — this is the **internal pull-up to power**. Without it, when the button is not pressed, the pin "hangs in the air" and reads a random value. The pull-up fixes the level: not pressed → high level on the pin (1), pressed → the pin is shorted to ground → low level (0):

```python
print(button.value())  # 1 — not pressed, 0 — pressed
```

Notice the inverted logic: pressing gives `0`. This is normal for a pull-up.

## Contact bounce

Real buttons "bounce" when pressed: the contact opens and closes several times for a few milliseconds, and one "click" can produce dozens of activations. Check it yourself:

```python
count = 0
while count < 10:
    if button.value() == 0:
        count += 1
        print("Pressed:", count)
        while button.value() == 0:
            pass  # wait until released
```

While pressed, `print` runs once, but when released the contact may "bounce" several times. Debouncing is done with a pause — after detecting a press, wait 20–50 ms, then read again:

```python
if button.value() == 0:
    time.sleep_ms(30)          # wait for the bounce to settle
    if button.value() == 0:    # check again
        print("Definitely pressed!")
```

This technique is called **debouncing**. It is mandatory in any real program with buttons.

## Analog signal: ADC

A button gives only two states. But how do you measure, for example, the voltage from a potentiometer or the light level? For this you need an **ADC** (analog-to-digital converter) — it converts voltage (0–3.3 V) into a number. In MicroPython this is done like this:

```python
from machine import Pin, ADC

adc = ADC(Pin(34))        # pin 34 (ESP32) supports ADC
value = adc.read_u16()    # a number from 0 to 65535
print(value)
```

The higher the voltage, the larger the number: 0 V → 0, 3.3 V → 65535. A regular "digital" pin cannot do this — the ADC has a special input stage. On the Raspberry Pi Pico, the ADC pins are 26–28.

## Digital sensor DHT22

Many sensors communicate with the board via a digital protocol — for example, DHT22 measures temperature and humidity:

```python
from machine import Pin
from dht import DHT22
import time

dht = DHT22(Pin(4))

while True:
    dht.measure()                        # request a measurement
    print("Temperature:", dht.temperature(), "C")
    print("Humidity:", dht.humidity(), "%")
    time.sleep(2)
```

The sensor needs time to measure, so you can't insert long pauses between `measure()` and reading, and polling itself should be done no more than once every 2 seconds. Sometimes DHT22 "doesn't respond" — then an `OSError` appears, and such a failure must be handled carefully via `try/except`:

```python
try:
    dht.measure()
    print(dht.temperature())
except OSError:
    print("Read error, trying again")
```

Now you have a full set: read digital inputs, measure voltage, and talk to smart sensors. Move on to the tasks.
<!--TASK-->
### Task 1
Connect a button to pin 14 (pull-up). Write a program that in an infinite loop prints `Pressed!` while the button is held and `Released` when it is released. Hint: the state changes less often than once every 0.2 seconds, so the pause in the loop should be smaller.

### Task 2
Write a press counter program: on each button press add 1 to a counter and print it, but only after every fifth press — `Counter: 5`, `Counter: 10`, and so on. Use the `%` operator. While the button is held, the counter should not grow.

### Task 3
Implement debouncing: count button presses checking the state twice — immediately and after 30 milliseconds (`time.sleep_ms(30)`). Compare the result with a similar program without debouncing: how many extra "presses" will the second version count over 10 real clicks?

### Task 4
Connect a potentiometer to an ADC pin (on ESP32 — pin 34). Write a program that every 0.5 seconds prints the raw value `adc.read_u16()` and its "percent": `value * 100 // 65535` (integer division). Turn the potentiometer knob and make sure the percent changes from 0 to 100.

### Task 5
Connect a DHT22 sensor to pin 4. Write a program that every 2 seconds prints temperature and humidity, and on a read error (`OSError`) prints `Read error` and continues working. At the end of each loop print a separate `---` line. Run it and leave it working for 20 seconds — check that the program doesn't crash.
<!--/TASK-->

<!--HINT-->
### Hint 1
Create `button = Pin(14, Pin.IN, Pin.PULL_UP)`. In a `while True:` loop read `button.value()`: if it's `0` — print `Pressed!`, otherwise — `Released`. A `time.sleep(0.1)` pause is enough.

### Hint 2
Create a variable `count = 0`. When `button.value() == 0` and the button was "just" not pressed — increment `count`. So one hold doesn't produce many activations, wait for release: `while button.value() == 0: time.sleep_ms(50)`. Then check: `if count % 5 == 0: print("Counter:", count)`.

### Hint 3
Inside the press condition add a second check: after the first `if button.value() == 0:` do `time.sleep_ms(30)`, then again `if button.value() == 0:`. Only then count the press. Without the pause, the "bouncing" contact will cause false activations.

### Hint 4
`adc.read_u16()` returns a number from 0 to 65535. Compute percent as `value * 100 // 65535` — `//` gives the integer part of division. In the loop: `print(value, "->", percent, "%")` and `time.sleep(0.5)`. Don't forget to import `ADC` from `machine`.

### Hint 5
Wrap `dht.measure()` and the reads in `try/except OSError:`. Inside `try` print `dht.temperature()` and `dht.humidity()`. In `except` — print `Read error`. After the block — `print("---")` and `time.sleep(2)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Program:

```python
from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Pressed!")
    else:
        print("Released")
    time.sleep(0.1)
```

What's happening here? `Pin(14, Pin.IN, Pin.PULL_UP)` configures pin 14 as an input with an internal pull-up to power: when the button is not pressed, the pin reads `1`; when pressed, it shorts to ground and gives `0`. The loop polls the button 10 times per second (0.1 s pause) and prints the state. If you set a pause longer than a second, you can "miss" a short press, so polling is done more often than a possible press.

### Solution 2
Program:

```python
from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)
count = 0
pressed = False

while True:
    if button.value() == 0 and not pressed:
        pressed = True
        count += 1
        if count % 5 == 0:
            print("Counter:", count)
    if button.value() == 1:
        pressed = False
    time.sleep_ms(50)
```

What's happening here? The `pressed` flag remembers that the button has already been "counted" and prevents the counter from growing while the button is held. When the button is released (`value() == 1`), the flag resets, and the next press will be counted. `count % 5 == 0` — the remainder of division by 5 is zero exactly for 5, 10, 15... This is the classic way to "trigger every fifth time".

### Solution 3
Program with debouncing:

```python
from machine import Pin
import time

button = Pin(14, Pin.IN, Pin.PULL_UP)
count = 0

while True:
    if button.value() == 0:
        time.sleep_ms(30)                 # wait for the contact to settle
        if button.value() == 0:           # second check
            count += 1
            print("Pressed:", count)
            while button.value() == 0:
                time.sleep_ms(10)         # wait until released
            time.sleep_ms(50)
```

What's happening here? The first check "catches" a possible press, and the second confirms it after 30 ms: if the bounce is still "shaking", by the time of the second check the contact could have opened, and the false activation is filtered out. In the version without the pause, one click can give 10–30 activations because the electrical contact opens and closes at hundreds of hertz. Debouncing is mandatory in all "real-world" programs with buttons.

### Solution 4
Program:

```python
from machine import Pin, ADC
import time

adc = ADC(Pin(34))

while True:
    value = adc.read_u16()
    percent = value * 100 // 65535
    print(value, "->", percent, "%")
    time.sleep(0.5)
```

What's happening here? `adc.read_u16()` returns a number from 0 to 65535 proportional to the voltage on the pin: 0 V → 0, 3.3 V → 65535. `value * 100 // 65535` converts this to percent — integer division `//` discards the fractional part. When you turn the potentiometer knob, the voltage changes, and the percent smoothly goes from ~0 to ~100. The same technique is used for reading photoresistors, joysticks, and analog sensors.

### Solution 5
Program:

```python
from machine import Pin
from dht import DHT22
import time

dht = DHT22(Pin(4))

while True:
    try:
        dht.measure()
        print("Temperature:", dht.temperature(), "C")
        print("Humidity:", dht.humidity(), "%")
    except OSError:
        print("Read error")
    print("---")
    time.sleep(2)
```

What's happening here? `dht.measure()` sends a request to the sensor and waits for a response. If the sensor didn't manage to respond (unstable power, too-short cable, signal noise), MicroPython throws `OSError` — and without `try/except` the program would crash. We catch the error, print `Read error`, and continue the loop. The `---` separator makes the output readable, and the 2-second pause satisfies DHT22's requirement not to poll it more often than once every 2 seconds.
<!--/SOLUTION-->

<!--QUIZ-->
Why is Pin.PULL_UP used when connecting a button?
- To increase read speed
- So that without pressing, the pin reads a definite level rather than a random value
- To protect the pin from a short circuit
- So the button doesn't bounce
* Correct answer: So that without pressing, the pin reads a definite level rather than a random value
The pull-up fixes the level on the pin: not pressed → 1, pressed (short to ground) → 0.

What value will button.value() return when the button is pressed with a pull-up?
- 1
- 0
- 65535
- true
* Correct answer: 0
Pressing shorts the pin to ground, and the level drops to 0 — the logic is "inverted".

What is contact bounce?
- The program triggering too fast
- Brief repeated opening/closing of the contact when pressed
- The sound a button makes
- A compilation error
* Correct answer: Brief repeated opening/closing of the contact when pressed
The mechanical contact "bounces" for a few ms, causing false activations; it is cured with a debouncing pause.

What does adc.read_u16() return?
- 1 or 0
- A number from 0 to 65535 proportional to voltage
- Voltage in volts
- A string with the pin name
* Correct answer: A number from 0 to 65535 proportional to voltage
The ADC converts 0–3.3 V voltage into a number 0–65535.

Which DHT22 method requests a new measurement?
- dht.read()
- dht.measure()
- dht.update()
- dht.sample()
* Correct answer: dht.measure()
dht.measure() starts a measurement, after which dht.temperature() and dht.humidity() return the results.

What happens without try/except if the DHT22 doesn't respond?
- The program will wait forever
- An OSError will appear, and the program will crash with an error
- The sensor will reboot
- Nothing, 0 will be returned
* Correct answer: An OSError will appear, and the program will crash with an error
A failed exchange with the sensor throws OSError; handling it with try/except makes the program robust.

Which pin on ESP32 can be used for analog reading (ADC)?
- Pin 2
- Pin 34
- Any pin
- Pin GND
* Correct answer: Pin 34
The ADC exists only on special pins: on ESP32 these are usually pins 32–39, including 34.

What does the fragment while button.value() == 0: pass do?
- Runs forever while the button is pressed — waits for release
- Turns the button on
- Skips the next line
- Reboots the board
* Correct answer: Runs forever while the button is pressed — waits for release
The loop spins while the value is 0 and exits only after the button is released — so one press isn't counted several times.
<!--/QUIZ-->
