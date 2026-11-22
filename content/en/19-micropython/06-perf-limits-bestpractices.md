---
title: Limits, memory, and best practices
summary: Learning to live in a world of hundreds of kilobytes of RAM: watching memory, saving resources, using timers and interrupts.
order: 6
duration: 35 min
difficulty: advanced
tags: micropython, memory, gc, timers, irq, optimization
---

MicroPython runs the same Python as your computer, but on hardware with very modest resources. You need to treat them like expensive fuel: wisely. This lesson is about writing programs that don't "eat up" the board and don't freeze.

## How much memory we have

An ESP32 usually has 320 KB of RAM, a Raspberry Pi Pico — 264 KB. That's thousands of times less than a laptop. Check for yourself:

```python
import gc
import micropython

gc.collect()                 # collect garbage
print("Free:", gc.mem_free(), "bytes")
print("Used:", gc.mem_alloc(), "bytes")
micropython.mem_info()       # detailed report
```

`gc` is the garbage collector: it finds objects that are no longer needed and frees memory. `gc.collect()` runs collection manually. `micropython.mem_info()` prints a summary. If free memory is low — the program will start crashing with `MemoryError`.

## Why you shouldn't create objects in loops

The most common cause of leaks is creating new objects in a loop. Take a look:

```python
bad = ""
for i in range(1000):
    bad = bad + str(i)   # a NEW string is created every time!
```

Each iteration creates a new copy of the string and leaves the old one to the garbage. This is both slow and memory-hungry. The right way is to collect the parts in a list and join once:

```python
good = "".join(str(i) for i in range(1000))
```

Rule: **don't create objects in a loop if you can collect them later**. This applies to strings, lists, dictionaries, and buffers.

## bytearray instead of a list

For storing bytes (sensor data, packets, images) use `bytearray` — it takes exactly 1 byte per element, unlike a list of integers:

```python
buf = bytearray(100)     # 100 bytes
lst = [0] * 100          # a list — an order of magnitude bigger
import sys
print(sys.getsizeof(buf), sys.getsizeof(lst))
```

`sys.getsizeof()` shows the object's size. On MicroPython the difference is easily 4–10 times — for large buffers this is critical.

## Timers instead of waiting

A `while True:` loop with `time.sleep()` is simple, but while the program sleeps, it can't do anything else. For periodic actions, a hardware timer is better: it calls the function itself, without the main loop's involvement.

```python
import machine
import time

def tick(timer):
    print("Tick!")

timer = machine.Timer(period=500, mode=machine.Timer.PERIODIC, callback=tick)

while True:
    time.sleep(1)   # the main program is busy with its own business
```

The timer calls `tick()` every 500 ms, while the main loop does its own thing. Important: you can't do long operations inside the callback (sleep, heavy computations) — that blocks everything else.

## Pin interrupts

The same applies to buttons: instead of polling in a loop, you can attach an **interrupt** (IRQ) handler that fires by itself when the level changes:

```python
from machine import Pin
count = 0

def on_press(pin):
    global count
    count += 1
    print("Pressed:", count)

button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

while True:
    pass
```

`IRQ_FALLING` — triggers on a falling edge (press). The handler must be short: no `sleep`, minimum work — otherwise you can miss events or catch a failure.

## Resilience: exceptions and watchdogs

In real devices everything breaks: a sensor goes silent, the network disappears, the sensor hangs. Therefore: wrap dangerous operations in `try/except` (like with DHT22), and if the device must run for days, add a watchdog timer `machine.WDT` that reboots the board if the program hangs:

```python
wdt = machine.WDT(timeout=5000)   # 5 seconds
while True:
    # device work...
    wdt.feed()   # confirm: I'm alive
```

## Summary: best practices checklist

1. Don't create objects in loops — collect them later.
2. Store byte data in `bytearray`, not in lists.
3. Watch memory: `gc.mem_free()` before long operations.
4. Periodic actions — via `Timer`, not via `sleep`.
5. Buttons and sensors — via `irq`, not via polling in a loop.
6. All external operations (network, sensors) — in `try/except`.
7. A watchdog timer for long-running work.
8. Don't use `float` if integers are enough — they take more memory.

With these tools, the board will survive both 24 hours of continuous work and complex projects. Move on to the tasks — they will cement each tool.
<!--TASK-->
### Task 1
Write a program that measures memory: first `gc.collect()` and `gc.mem_free()` — record value A. Then create a list `[0] * 10000` and call `gc.mem_free()` again — record value B. Print `Before: A`, `After: B`, `Difference: A - B`. Explain why the difference is smaller than you might expect (a list stores references, not the numbers themselves).

### Task 2
Compare sizes: create `bytearray(1000)` and `[0] * 1000`, print their sizes via `sys.getsizeof()`. Write in your answer how many times larger the list is (you can compute it programmatically: `sys.getsizeof(lst) // sys.getsizeof(buf)`).

### Task 3
Write a program with a timer: `machine.Timer` with a 500 ms period calls a callback that prints `Tick: N` (N is a counter). In the main `while True:` loop print `Main loop` every second via `time.sleep(1)`. Make sure the messages interleave instead of waiting for each other.

### Task 4
Rewrite the program that builds a string from 1000 elements: first the "naive" variant via concatenation (adding in a loop), then via `join`. Measure the time of each version via `time.ticks_ms()` (record the difference) and print both results.

### Task 5
Build a "reliable button": on pin 14 — a button with `irq` (trigger on falling edge, `Pin.IRQ_FALLING`), in the handler — only increment a counter (no print!). The main loop prints the counter every 2 seconds and calls `gc.collect()`. Run for 20 seconds, press the button 10 times, and check: the counter almost always shows 10 (no bounce, no losses).
<!--/TASK-->

<!--HINT-->
### Hint 1
Record `mem_free` in a variable before and after creating the list: `a = gc.mem_free()`, then `lst = [0] * 10000`, then `b = gc.mem_free()`. `print("Difference:", a - b)`. Remember: a list of 10,000 zeros is 10,000 references to a single `0` object.

### Hint 2
`import sys` — then `buf = bytearray(1000)`, `lst = [0] * 1000`, `print(sys.getsizeof(buf))`, `print(sys.getsizeof(lst))`. For comparison: `print("Times:", sys.getsizeof(lst) // sys.getsizeof(buf))`.

### Hint 3
Callback: `def tick(timer): global n; n += 1; print("Tick:", n)`. Timer: `timer = machine.Timer(period=500, mode=machine.Timer.PERIODIC, callback=tick)`. In the main loop — `print("Main loop")`, `time.sleep(1)`.

### Hint 4
Measurement: `start = time.ticks_ms()` before the loop, `time.ticks_diff(time.ticks_ms(), start)` after. Naive variant: `s = ""; for i in range(1000): s += str(i)`. Via join: `s = "".join(str(i) for i in range(1000))`.

### Hint 5
Counter: `count = 0` (global). In the handler: `global count; count += 1`. Main loop: `while True: print("Counter:", count); gc.collect(); time.sleep(2)`. Initialize `irq` after creating the button.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Program:

```python
import gc

gc.collect()
a = gc.mem_free()
lst = [0] * 10000
b = gc.mem_free()
print("Before:", a)
print("After:", b)
print("Difference:", a - b)
```

What's happening here? `gc.mem_free()` — how many bytes are free now. After creating a list of 10,000 zeros, free memory decreased — but not by 10,000 bytes, less, because the list stores **references** to objects, not copies of numbers: all `0`s are the same object, and the list is an array of 10,000 references of a few bytes each. The difference roughly equals the size of the reference array. This is an important understanding: a list is a "shelf with labels", and the data itself lies separately.

### Solution 2
Program:

```python
import sys
buf = bytearray(1000)
lst = [0] * 1000
print("bytearray:", sys.getsizeof(buf))
print("list:", sys.getsizeof(lst))
print("Times:", sys.getsizeof(lst) // sys.getsizeof(buf))
```

What's happening here? `bytearray(1000)` allocates exactly 1000 bytes — one per element. The list `[0] * 1000` contains 1000 references of 4 bytes each plus overhead — usually 4–10 times more. So for storing byte data (sensor readings, images, network packets) always use `bytearray` — it's a memory saving the board will appreciate.

### Solution 3
Program:

```python
import machine
import time

n = 0

def tick(timer):
    global n
    n += 1
    print("Tick:", n)

timer = machine.Timer(period=500, mode=machine.Timer.PERIODIC, callback=tick)

while True:
    print("Main loop")
    time.sleep(1)
```

What's happening here? The timer is a hardware "alarm clock" that calls `tick()` every 500 ms regardless of what the main loop is doing. So messages interleave on the screen: `Tick` and `Main loop` go "in parallel". If we used only `sleep`, the program could do only one action at a time. Note: `tick()` must be short — it runs "in the shadow" of the main code.

### Solution 4
Program:

```python
import time

# Naive variant
start = time.ticks_ms()
s = ""
for i in range(1000):
    s += str(i)
naive = time.ticks_diff(time.ticks_ms(), start)

# Via join
start = time.ticks_ms()
s = "".join(str(i) for i in range(1000))
joined = time.ticks_diff(time.ticks_ms(), start)

print("Concatenation:", naive, "ms")
print("join:", joined, "ms")
```

What's happening here? `s += str(i)` creates a new string on every iteration: the old one goes to garbage, the new one is one character longer. This is quadratic complexity: 1000 iterations mean millions of copying operations. `join` goes through the list of parts once and joins them in a single pass. The difference is tens and hundreds of times — and it grows with size. On a real board, where every millisecond counts, this is noticeable immediately.

### Solution 5
Program:

```python
from machine import Pin
import gc
import time

count = 0

def on_press(pin):
    global count
    count += 1

button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

while True:
    print("Counter:", count)
    gc.collect()
    time.sleep(2)
```

What's happening here? The interrupt fires at the moment the level falls — exactly at the moment of pressing, without polling in a loop. The handler only does `count += 1` — short and fast, so events aren't missed. Printing and garbage collection are moved to the main loop so they don't slow down the handler. Debouncing isn't needed here: `IRQ_FALLING` fires once per edge, and if bounce produces extra edges, they're cut at the hardware level or a tiny delay is added in the handler.
<!--/SOLUTION-->

<!--QUIZ-->
Which module is responsible for garbage collection in MicroPython?
- os
- gc
- sys
- machine
* Correct answer: gc
gc.collect() forces garbage collection; gc.mem_free() shows free memory.

Why is string concatenation in a loop a bad practice?
- Because strings can't be added
- Each iteration creates a new string, discarding the old one — slow and memory-intensive
- Because it's forbidden in MicroPython
- Because strings aren't supported in MicroPython
* Correct answer: Each iteration creates a new string, discarding the old one — slow and memory-intensive
Adding in a loop has quadratic complexity; the right way is to collect the parts and join them with "".join(...).

What is more efficient for storing 1000 bytes of data?
- A list [0] * 1000
- bytearray(1000)
- A dictionary
- A tuple
* Correct answer: bytearray(1000)
bytearray stores exactly 1 byte per element; a list stores references and takes many times more.

What is machine.Timer for?
- To reboot the board
- To call a function periodically without blocking the main loop
- To measure voltage
- To speed up code
* Correct answer: To call a function periodically without blocking the main loop
The timer calls the callback every given period regardless of the main program.

What does button.irq(trigger=Pin.IRQ_FALLING, handler=on_press) mean?
- The button is polled every 10 ms
- The on_press handler will be called when the level on the pin falls
- The button will turn off
- The program will stop
* Correct answer: The on_press handler will be called when the level on the pin falls
IRQ is an interrupt: the handler fires by itself, without polling in a loop; IRQ_FALLING — on a falling edge (press).

What should the body of an interrupt (IRQ) handler be like?
- Verbose, with print and sleep
- Short, without long operations and sleeps
- Contain an infinite loop
- Contain a Wi-Fi connection
* Correct answer: Short, without long operations and sleeps
Long operations in the handler block the board and can lead to missed events and failures.

What does machine.WDT(timeout=5000) do?
- Will reboot the board if wdt.feed() isn't called within 5 seconds
- Will reduce power consumption
- Will increase the clock frequency
- Will block the USB port
* Correct answer: Will reboot the board if wdt.feed() isn't called within 5 seconds
A watchdog timer reboots the board on a hang: the program must regularly call feed() to confirm it's alive.

What does gc.mem_free() return?
- The amount of used memory
- The amount of free memory
- The number of objects in memory
- The number of bytes in the firmware
* Correct answer: The amount of free memory
mem_free() shows free bytes; the opposite function — gc.mem_alloc() — shows used ones.
<!--/QUIZ-->
