---
title: PWM, servos, and displays
summary: Smooth brightness control and servo control via PWM, as well as displaying text and graphics on an OLED display over the I2C bus.
order: 4
duration: 30 min
difficulty: intermediate
tags: micropython, pwm, servo, i2c, oled, ssd1306
---

We know how to turn an LED on and off, but often we need to do more: smoothly change brightness, rotate a servo to an exact angle, or show data on a small screen. All of this is the next step in mastering hardware, and today we'll take it.

## PWM: pulse width modulation

If you just apply 0 or 3.3 V to an LED, it blinks. But if you switch the voltage thousands of times per second, the eye doesn't notice the switching: the LED just seems dimmer or brighter. That's exactly what **PWM** (pulse width modulation) does — it generates a square wave with a variable "duty cycle": the fraction of time the signal is on.

```python
from machine import Pin, PWM

pwm = PWM(Pin(2), freq=1000)   # frequency 1000 Hz
pwm.duty_u16(32768)             # duty cycle: 0..65535
```

`duty_u16` is the "duty cycle" in the range 0–65535: 0 — off, 65535 — full brightness, 32768 — about half. Changing it smoothly changes brightness:

```python
import time
for duty in range(0, 65536, 1000):
    pwm.duty_u16(duty)
    time.sleep_ms(3)
```

## Servo

A servo is a motor with feedback that can rotate its shaft to a given angle (usually 0–180°). It is controlled by PWM at 50 Hz, and the angle is set by the pulse width: 0.5 ms — 0°, 1.5 ms — 90°, 2.5 ms — 180°.

```python
from machine import Pin, PWM

servo = PWM(Pin(13), freq=50)   # servos like 50 Hz

def set_angle(angle):
    # 0° => 0.5 ms, 180° => 2.5 ms with a 20 ms period
    duty = int(1638 + (8191 - 1638) * angle / 180)
    servo.duty_u16(duty)

set_angle(90)   # turn to 90°
```

The numbers 1638 and 8191 are `duty_u16` values corresponding to 0.5 ms and 2.5 ms out of a 20 ms period. Connect the servo: brown wire — GND, red — 5V (or 3.3V for small servos), orange — signal pin.

## OLED display over I2C

Small OLED screens (0.96", 128×64) communicate over the **I2C** bus — via two wires: SCL (clock) and SDA (data). On ESP32 the standard I2C pins are 22 (SCL) and 21 (SDA); on the Raspberry Pi Pico — 1 and 0.

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)   # 128x64 pixel screen

oled.fill(0)              # clear the screen (fill with black)
oled.text("Hello!", 0, 0)
oled.text("MicroPython", 0, 16)
oled.show()               # send the buffer to the screen
```

Everything you draw goes into the board's memory (a buffer), and is actually shown only after `oled.show()`. Text lines on the screen are 8 pixels tall, so it's convenient to place them every 8–10 pixels vertically. You can also draw shapes: `oled.fill_rect(x, y, w, h, 1)` — a filled rectangle, `oled.hline(x, y, w, 1)` — a line.

## Putting it together

Now it's easy to combine knowledge: for example, show the LED's current brightness on the screen while the potentiometer knob changes it. This is almost a real device with an interface. In the tasks we'll make several such projects — from LED "breathing" to a thermometer on screen.
<!--TASK-->
### Task 1
Write an LED "breathing" program: brightness smoothly rises from 0 to 65535 and smoothly falls back. Each step — `pwm.duty_u16(duty)` and `time.sleep_ms(2)`. The loop is infinite. The LED should "breathe", not blink.

### Task 2
Connect a servo to pin 13. Write a program that slowly rotates it from 0° to 180° and back. At each 5° step make a 200 ms pause. Use the `set_angle(angle)` function from the theory.

### Task 3
Connect a passive buzzer to pin 12. Write a program that plays a simple melody: the notes "E, G, A, G, E, E, E" — a sequence of (frequency Hz, duration ms): (330, 300), (392, 300), (440, 300), (392, 300), (330, 300), (330, 150), (330, 150). For each note create a PWM with its frequency, wait for the duration, then turn it off (`deinit()`).

### Task 4
Connect an OLED display over I2C. Write a program that shows three lines on the screen: `Temperature: 24 C`, `Humidity: 45 %`, `Date: 01.11`. The lines should update every second with the same values (you can change only the digits of the time). After each draw — `oled.show()`.

### Task 5
Put it all together: a potentiometer on ADC pin 34 and an OLED over I2C. Every 0.2 seconds the program reads `adc.read_u16()`, converts it to percent, and displays it: the number of filled bar segments (rectangles) under the label `Level: N %`. The bar — 20 rectangles, each 5 pixels wide.
<!--/TASK-->

<!--HINT-->
### Hint 1
One loop for rising: `for duty in range(0, 65536, 300)`. Then a loop for falling: `for duty in range(65536, -1, -300)` (negative step). Inside — `pwm.duty_u16(duty)` and `time.sleep_ms(2)`.

### Hint 2
`for angle in range(0, 181, 5)` — rising, then `for angle in range(180, -1, -5)` — falling. Inside: `set_angle(angle)`, `time.sleep_ms(200)`. Don't forget `freq=50` when creating the PWM.

### Hint 3
Store the melody as a list of tuples: `melody = [(330, 300), (392, 300), ...]`. Inside the loop over `freq, dur` create `PWM(Pin(12), freq=freq)`, wait `time.sleep_ms(dur)`, then `pwm.deinit()`. After a note — a small 50 ms pause.

### Hint 4
Before each draw: `oled.fill(0)`. Then `oled.text("Temperature: 24 C", 0, 0)`, and so on. At the end — `oled.show()`. In a `while True:` loop add `time.sleep(1)`. For seconds you can use `time.localtime()` — but start with fixed text.

### Hint 5
Compute percent: `percent = adc.read_u16() * 100 // 65535`. The number of filled rectangles: `filled = percent * 20 // 100`. Draw them with a loop: `for i in range(filled): oled.fill_rect(0 + i * 6, 20, 5, 8, 1)`. Don't forget `oled.show()`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Program:

```python
from machine import Pin, PWM
import time

pwm = PWM(Pin(2), freq=1000)

while True:
    for duty in range(0, 65536, 300):
        pwm.duty_u16(duty)
        time.sleep_ms(2)
    for duty in range(65536, -1, -300):
        pwm.duty_u16(duty)
        time.sleep_ms(2)
```

What's happening here? The first loop raises `duty_u16` from 0 to 65535, the second lowers it back. A step of 300 and a 2 ms pause give hundreds of intermediate values — the eye doesn't see jumps, and the LED smoothly lights up and fades. This is the classic "breathing" effect. Instead of `duty_u16`, newer firmware also has `duty_ns` — but `duty_u16` is universal on ESP32 and Raspberry Pi Pico.

### Solution 2
Program:

```python
from machine import Pin, PWM
import time

servo = PWM(Pin(13), freq=50)

def set_angle(angle):
    duty = int(1638 + (8191 - 1638) * angle / 180)
    servo.duty_u16(duty)

while True:
    for angle in range(0, 181, 5):
        set_angle(angle)
        time.sleep_ms(200)
    for angle in range(180, -1, -5):
        set_angle(angle)
        time.sleep_ms(200)
```

What's happening here? The servo is controlled by 50 Hz pulses: angle 0° corresponds to a 0.5 ms pulse width, 180° — 2.5 ms. With a 20 ms period that's `duty_u16` 1638 and 8191. The formula interpolates the angle into this range: the larger the angle, the wider the pulse, the farther the shaft rotates. A 5° step and a 200 ms pause make the movement smooth — the servo "rides" to each position instead of jerking.

### Solution 3
Program:

```python
from machine import Pin, PWM
import time

melody = [(330, 300), (392, 300), (440, 300),
          (392, 300), (330, 300), (330, 150), (330, 150)]

while True:
    for freq, dur in melody:
        pwm = PWM(Pin(12), freq=freq)
        time.sleep_ms(dur)
        pwm.deinit()
        time.sleep_ms(50)
```

What's happening here? A passive buzzer can't produce sound by itself — it needs a signal of the right frequency, which PWM generates. Each note is a PWM with a frequency equal to the note's frequency (330 Hz — "E"). `deinit()` frees the pin and stops the signal — otherwise the note would sound forever. The 50 ms pause between notes makes the melody intelligible. This technique won't work with an active buzzer — it just needs a power level.

### Solution 4
Program:

```python
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

while True:
    oled.fill(0)
    oled.text("Temperature: 24 C", 0, 0)
    oled.text("Humidity: 45 %", 0, 16)
    oled.text("Date: 01.11", 0, 32)
    oled.show()
    time.sleep(1)
```

What's happening here? `oled.fill(0)` clears the buffer — without it old characters would remain on the screen. `oled.text()` draws text into the buffer, but it's shown only after `oled.show()`, which sends the whole buffer over I2C to the screen controller. The 16-pixel spacing between lines is convenient: the font is 8 pixels tall, plus a gap. During `time.sleep(1)` the screen keeps the image — OLEDs don't need constant refreshing.

### Solution 5
Program:

```python
from machine import Pin, ADC, I2C
from ssd1306 import SSD1306_I2C
import time

adc = ADC(Pin(34))
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

while True:
    percent = adc.read_u16() * 100 // 65535
    oled.fill(0)
    oled.text("Level: " + str(percent) + " %", 0, 0)
    filled = percent * 20 // 100
    for i in range(filled):
        oled.fill_rect(0 + i * 6, 20, 5, 8, 1)
    oled.show()
    time.sleep(0.2)
```

What's happening here? We combined three modules: the ADC reads the voltage from the potentiometer, `percent` converts it to percent, and the OLED draws both text and a bar indicator. `fill_rect(x, y, w, h, 1)` fills a 5×8 pixel rectangle, and 20 such rectangles side by side form a scale. The number of filled squares is proportional to the percent. This is how real instruments are made: sensor → logic → screen.
<!--/SOLUTION-->

<!--QUIZ-->
What controls the LED brightness when using PWM?
- The signal frequency
- The duty_u16 value — the fraction of time the signal is on
- The pin number
- The value of voltage()
* Correct answer: The duty_u16 value — the fraction of time the signal is on
The larger duty_u16 (0–65535) is, the longer the signal is on per period, the brighter the light.

What PWM frequency is needed to control a servo?
- 1000 Hz
- 50 Hz
- 5 Hz
- 400000 Hz
* Correct answer: 50 Hz
Servos read the pulse width at 50 Hz (20 ms period) — this is the standard.

What does oled.show() do?
- Switches the screen to sleep mode
- Sends the buffer to the screen — only then does the picture appear
- Clears the screen
- Increases brightness
* Correct answer: Sends the buffer to the screen — only then does the picture appear
Drawing goes into a buffer in the board's memory; oled.show() transfers it to the screen controller.

Over which bus is a 0.96" OLED display usually connected?
- UART
- I2C
- SPI
- WLAN
* Correct answer: I2C
The display uses the I2C bus with two wires — SCL and SDA.

What will pwm.duty_u16(0) return?
- Full brightness
- The signal is off (0% duty cycle)
- An error
- 50% duty cycle
* Correct answer: The signal is off (0% duty cycle)
duty_u16(0) means the signal is never on — the LED doesn't light, the servo is at its extreme position.

What does pwm.deinit() do?
- Reboots the board
- Frees the pin and stops signal generation
- Sets the duty cycle to 50%
- Turns PWM back on
* Correct answer: Frees the pin and stops signal generation
deinit() turns off PWM and allows the pin to be reused (for example, for another buzzer note).

How do you convert brightness percent into a duty_u16 value?
- percent * 655 // 100
- percent * 65535 // 100
- percent // 65535 * 100
- 65535 - percent
* Correct answer: percent * 65535 // 100
The duty_u16 range is 0–65535, so 100% corresponds to 65535: percent is multiplied by 65535 and divided by 100.

What does a 50 Hz PWM frequency mean?
- The signal repeats 50 times per second
- 50 pulses per minute
- The signal duty cycle is 50%
- The servo will rotate 50°
* Correct answer: The signal repeats 50 times per second
50 Hz is a 20 ms period; standard servos read pulse width at exactly this frequency.
<!--/QUIZ-->
