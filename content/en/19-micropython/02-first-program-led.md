---
title: First program: blinking an LED
summary: We assemble the first circuit, learn to control pins via machine.Pin, and write the classic program — blinking an LED.
order: 2
duration: 25 min
difficulty: intermediate
tags: micropython, gpio, led, machine.pin, time.sleep
---

The classic "first program" for a microcontroller is blinking an LED. It is the hardware equivalent of `print("Hello, world!")`: you confirm that the board works, that you assembled the circuit correctly, and that you learned to control pins. Along the way you will master two of the most important tools: `machine.Pin` and `time.sleep`.

## What you need to assemble

Take an LED and a 220–330 ohm resistor. Connect them in series: the anode leg (the long one, through the resistor) goes to pin 2 of the board, and the cathode leg (the short one) goes to ground (GND). The resistor is mandatory: it limits the current and protects both the LED and the board's pin from burning out. Many boards also have a built-in LED: on the Raspberry Pi Pico it is pin 25 (GP25), on many ESP32 boards — pin 2. In that case nothing needs soldering — you can write code right away and watch the built-in LED.

## Pins: output and input

Any microcontroller pin can be configured as an output (OUT) — to apply voltage to it, or as an input (IN) — to read the signal level from outside. For this, a `Pin` object is created:

```python
from machine import Pin

led = Pin(2, Pin.OUT)  # pin 2 works as an output
```

Now the `led` object can be controlled:

```python
led.value(1)   # high level (3.3 V) — the LED is on
led.value(0)   # low level (0 V) — the LED is off
```

There are also short forms — `led.on()` and `led.off()`, as well as `led.toggle()`, which switches the state to the opposite:

```python
led.toggle()  # if it was on — it turns off, and vice versa
```

## First blinking

Let's put it all together. To make the LED blink, you need to alternate turning it on and off with pauses:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)
    time.sleep(0.5)   # on for half a second
    led.value(0)
    time.sleep(0.5)   # off for half a second
```

The `while True:` loop runs forever, so the LED will blink as long as the board is powered. To stop the program — press Ctrl+C in Thonny (or Reset on the board).

And if you need to blink exactly N times — use `range`:

```python
for _ in range(5):
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

The blink rate is set by the pauses: the smaller `time.sleep(0.5)` is, the faster.

## What happens inside

`led.value(1)` is not an abstraction: the microcontroller puts 3.3 V on the pin, current flows through the resistor, and the LED lights up. `led.value(0)` — the voltage drops to zero, the current disappears, and the LED turns off. You are literally controlling electricity with a few lines of Python. In a few lessons you will understand that more complex things — PWM, sensors, and even Wi-Fi — are based on the same principle.
<!--TASK-->
### Task 1
Write a program that blinks an LED exactly 5 times: on for 1 second, off for 1 second. Use a `for` loop and the `value()` method. After the fifth blink, the LED should stay off and the program should end.

### Task 2
Rewrite the solution to the first task using the `on()`, `off()`, and `toggle()` methods instead of `value()`. Make two variants: (a) with `on()`/`off()`, (b) with `toggle()` — 10 blinks. Make sure both variants work identically.

### Task 3
Write a program that sends an SOS signal in Morse code: three short blinks (0.3 s each), a 0.3 s pause, three long blinks (1 s each), a 0.3 s pause, and three short blinks again. Between repetitions of the whole signal — a 2-second pause. The loop is infinite.

### Task 4
Assemble a "traffic light" from two LEDs: red on pin 2, green on pin 4. The program should alternately: light the red for 2 seconds, then turn it off and light the green for 2 seconds, and so on forever. Add a 0.5-second delay between switches so you can see the "traffic light" switching.

### Task 5
Write an "accelerating LED" program: the LED blinks 10 times, and each next blink is 20% faster than the previous one. Start with a 1-second pause: 1.0, 0.8, 0.64, ... (multiply the pause by 0.8). After 10 blinks, print the message `Done, speed: 0.13 s` (with your actual pause value).
<!--/TASK-->

<!--HINT-->
### Hint 1
The `for i in range(5):` loop repeats its body 5 times. Inside: `led.value(1)`, `time.sleep(1)`, `led.value(0)`, `time.sleep(1)`. Nothing needs to be added after the loop — without `while True` the program ends by itself.

### Hint 2
`led.on()` and `led.off()` are synonyms for `value(1)` and `value(0)`. For variant (b), replace both pairs with a single `led.toggle()` call followed by a `time.sleep(0.5)` pause — the method switches the state itself.

### Hint 3
Create a `blink(duration)` function that turns the LED on, waits `duration`, turns it off, and waits 0.3 s. Then a long signal is `blink(1)`, a short one is `blink(0.3)`. Make long pauses between repetitions with `time.sleep(2)`.

### Hint 4
Create two Pin objects: `red = Pin(2, Pin.OUT)` and `green = Pin(4, Pin.OUT)`. In an infinite loop: `red.on()`, `time.sleep(2)`, `red.off()`, `time.sleep(0.5)`, then the same for `green`.

### Hint 5
Store the pause in a variable: `delay = 1.0`. Inside the loop do `delay = delay * 0.8` (or `delay *= 0.8`). At the end print the current value: `print("Done, speed:", round(delay, 2), "s")`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Program:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

for _ in range(5):
    led.value(1)
    time.sleep(1)
    led.value(0)
    time.sleep(1)
```

What's happening here? `for _ in range(5)` repeats the loop body exactly 5 times. In each iteration the LED turns on (`value(1)`), waits a second, turns off (`value(0)`), and waits a second again. After the fifth repeat the loop ends, the program reaches the end of the file and stops — the LED stays off. The `_` variable is the conventional Python name for an "unused" loop variable: we don't need the value itself, only the number of repetitions.

### Solution 2
Variant (a):

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

for _ in range(5):
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
```

Variant (b):

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

for _ in range(10):
    led.toggle()
    time.sleep(0.5)
```

What's happening here? `on()`/`off()` are just more readable synonyms for `value(1)`/`value(0)`. And `toggle()` flips the state to the opposite: if the LED was on — it turns off, if off — it turns on. So in variant (b) one call per iteration is enough: each call switches the state, and the 0.5 s pause creates the blinking. Note: both variants produce the same blink "pattern", but differ in style and amount of code.

### Solution 3
Program:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

def blink(duration):
    led.on()
    time.sleep(duration)
    led.off()
    time.sleep(0.3)

while True:
    for _ in range(3):      # three short
        blink(0.3)
    time.sleep(0.3)
    for _ in range(3):      # three long
        blink(1)
    time.sleep(0.3)
    for _ in range(3):      # three short
        blink(0.3)
    time.sleep(2)           # pause between signals
```

What's happening here? The `blink(duration)` function factors out the repeated "turn on — wait — turn off — wait" sequence. A short signal is `blink(0.3)`, a long one is `blink(1)`. The triples are repeated with `for` loops. Grouping code into functions makes the program readable and lets you change durations in one place. The 2-second pause at the end of the outer loop separates one SOS signal from the next.

### Solution 4
Program:

```python
from machine import Pin
import time

red = Pin(2, Pin.OUT)
green = Pin(4, Pin.OUT)

while True:
    red.on()
    time.sleep(2)
    red.off()
    time.sleep(0.5)

    green.on()
    time.sleep(2)
    green.off()
    time.sleep(0.5)
```

What's happening here? We have two independent `Pin` objects, each controlling its own LED. First the red one burns for 2 seconds, turns off, and after a short 0.5 s pause the green one lights up. The pause between switches is needed so the boundary of states is visible — without it the switch would look "blended". The `while True` loop repeats this sequence forever — this is the classic "traffic light" structure: states alternate by timing.

### Solution 5
Program:

```python
from machine import Pin
import time

led = Pin(2, Pin.OUT)

delay = 1.0
for _ in range(10):
    led.on()
    time.sleep(delay)
    led.off()
    time.sleep(delay)
    delay *= 0.8

print("Done, speed:", round(delay, 2), "s")
```

What's happening here? The `delay` variable stores the current pause. Each blink uses it, and then the line `delay *= 0.8` reduces the pause by 20%: 1.0 → 0.8 → 0.64 → 0.512 and so on. After 10 iterations `delay` is approximately 0.13 — that's what `print()` prints with rounding via `round(delay, 2)`. This is how we see a variable "living" inside a loop and how simple arithmetic turns into controlling the speed of a physical process.
<!--/SOLUTION-->

<!--QUIZ-->
What does led.value(1) do?
- Reads the value from the pin
- Applies a high level to the pin — the LED lights up
- Switches the pin to input mode
- Turns off the board's power
* Correct answer: Applies a high level to the pin — the LED lights up
value(1) sets a high voltage level on the pin, current flows through the resistor, and the LED is on.

Why does an LED circuit need a resistor?
- To make the LED shine brighter
- To limit the current and protect the LED and the pin
- To slow down the blinking
- For decoration
* Correct answer: To limit the current and protect the LED and the pin
Without a resistor the current will be too high, and the LED (or pin) may burn out.

What does the toggle() method do?
- Applies a high level forever
- Switches the state to the opposite
- Resets the pin to zero state
- Reboots the board
* Correct answer: Switches the state to the opposite
If the LED is on — toggle() turns it off; if off — turns it on.

How many times will the body of the for _ in range(3) loop execute?
- 2
- 3
- 4
- Infinitely
* Correct answer: 3
range(3) gives values 0, 1, 2 — the loop body executes exactly 3 times.

What does time.sleep(0.5) do?
- Stops the program for half a second
- Doubles execution speed
- Puts the board into sleep mode forever
- Nothing, it's a comment
* Correct answer: Stops the program for half a second
time.sleep(0.5) pauses execution for 0.5 seconds (time is in seconds).

How do you stop an infinite while True loop in Thonny?
- Close Thonny
- Press Ctrl+C
- Turn off the monitor
- No way
* Correct answer: Press Ctrl+C
Ctrl+C interrupts program execution in Thonny (the Reset button also works on the board).

Which method turns the LED off?
- led.value(1)
- led.value(0)
- led.toggle()
- led.on()
* Correct answer: led.value(0)
value(0) applies a low level (0 V) to the pin — no current flows, and the LED turns off.

What will happen if you remove the resistor from the LED circuit?
- The LED will shine brighter and safely
- The current will become too high, and the LED or pin may burn out
- Nothing will change
- The blinking will become faster
* Correct answer: The current will become too high, and the LED or pin may burn out
The resistor limits the current; without it the LED may burn out and the pin may fail.
<!--/QUIZ-->
