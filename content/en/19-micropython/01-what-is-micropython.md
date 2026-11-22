---
title: What is MicroPython
summary: Getting to know MicroPython: how it differs from classic Python, which boards it brings to life, and how to run your first program in the very first lesson.
order: 1
duration: 25 min
difficulty: intermediate
tags: micropython, microcontrollers, esp32, raspberry pi pico, repl, thonny
---

Microcontrollers surround us everywhere: they are inside washing machines, smart light bulbs, fitness bracelets, and even your refrigerator. They are tiny computers with a processor and memory, but without a monitor, keyboard, or operating system. You can program them in low-level languages like C, but that is slow and difficult. Or you can use MicroPython — a simpler version of Python created specifically for such devices.

## What is MicroPython

MicroPython is an implementation of the Python language that runs directly on a microcontroller. It was created by engineer Damien George in 2014. The core of the language remains the same: loops, functions, lists, dictionaries, classes — everything you know from the course works here too. But there are important differences as well.

First, the MicroPython interpreter takes up only a few hundred kilobytes of flash memory and can work with 20–500 KB of RAM. For comparison: regular CPython would need tens of megabytes for the same task. Second, MicroPython does not rely on an operating system: it manages the hardware itself. Third, it uses a different set of modules: instead of the bloated standard library, compact modules `machine`, `network`, `ujson`, `urequests`, `time`.

Code in MicroPython is written the same way as regular Python, so almost everything you already know will come in handy.

## REPL — a live dialogue with the board

REPL is an interactive mode where commands execute immediately. If you connect the board to your computer via USB and open a terminal (for example, in the Thonny program), a `>>>` prompt appears:

```python
>>> print("Hello, MicroPython!")
Hello, MicroPython!
>>> 2 ** 10
1024
>>> 17 * 3
51
```

Each line executes instantly — the board responds right away. This is the best way to experiment.

## How to identify your board

You can ask MicroPython what it is running on:

```python
import os
print(os.uname())
```

In response you will get something like:

```
(sysname='esp32', nodename='esp32', release='1.24.0', version='v1.24.0 on 2024-09-02', machine='ESP32 module with ESP32')
```

Built-in variables are also useful:

```python
import sys
print(sys.platform)
print(sys.version)
```

## The machine module — the key to hardware

All operations with pins, timers, PWM, and other devices live in the `machine` module. Take a look at what it contains:

```python
import machine
print(dir(machine))
```

You will see `Pin`, `PWM`, `ADC`, `I2C`, `Timer`, `WDT` and much more. These are the "control levers" of the board. For example, here is how to turn on an LED connected to pin 2:

```python
from machine import Pin
led = Pin(2, Pin.OUT)  # pin 2 — as output
led.value(1)            # set high level — LED is on
```

No magic: we are simply controlling a physical output of the microcontroller. The following lessons will be entirely devoted to this.

## How to install MicroPython

To get this environment, you need to "flash" the board: write a firmware file (`.bin`) into its memory. The easiest way is through the Thonny program, which can flash the board, edit code, and show the REPL. You choose your board (ESP32, Raspberry Pi Pico, and others), download the official firmware from micropython.org, and run the installation. After that, the board is ready to execute.

## What's next

In this module we will learn to bring hardware to life: blink LEDs, read buttons and sensors, control servos and displays, and connect the board to the internet. All of it — with real examples and tasks. Let's begin!

<!--TASK-->
### Task 1
Connect the board to your computer and open the REPL. Print the greeting `Hello, MicroPython!`, then compute `17 * 3` and `2 ** 10`. Write down in your answer exactly what the board printed and how fast each line executed (usually — fractions of a second).

### Task 2
Create a new `hello.py` file in Thonny with the following content: first `print("Hello, MicroPython!")`, then `import sys` and `print(sys.version)`. Run the script. What do you see on the screen? How does running a file differ from executing the same command in the REPL?

### Task 3
Write a program that prints information about your board: `import os`, then `print(os.uname())`. Run it and write down the `sysname` string from the result. If you have several boards — compare their outputs.

### Task 4
Run `import machine` and `print(dir(machine))`. Pick three names from this list that, in your opinion, are related to controlling pins or reading signals, and explain in your own words what they might be used for. Look for hints in the names or documentation.

### Task 5
Write a program that does the following: prints `Starting work`, waits two seconds (`import time` + `time.sleep(2)`), then prints `Done`. Run it and check that there is indeed a noticeable pause between the lines. Change the wait time to 5 seconds and run again.
<!--/TASK-->

<!--HINT-->
### Hint 1
In the REPL just type expressions and press Enter. Numbers can be entered as is, without print(): `>>> 17 * 3` also works, but it is better to get used to `print()` — the output is clearer and identical on any board.

### Hint 2
A file in Thonny is a regular text file with a `.py` extension. Commands run from top to bottom. Be careful: REPL output appears right after each line, while file output is printed all at once after launching.

### Hint 3
`os.uname()` returns an object similar to a dictionary with fields `sysname`, `nodename`, `release`, `version`, `machine`. Print it entirely with `print()` — and just find the `sysname=...` line in the text.

### Hint 4
Look in the list for short, meaningful names: `Pin`, `PWM`, `ADC`, `I2C`, `Timer`, `DAC`. `Pin` is almost certainly input/output. Think about what `ADC` could mean (hint: the letter A stands for analog).

### Hint 5
A sequence of commands is just lines one after another. A pause is made with `time.sleep(2)` — the function takes seconds. Don't forget to run `import time` first. MicroPython also has `time.sleep_ms(2000)` — for milliseconds.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
In the REPL we print:

```python
>>> print("Hello, MicroPython!")
```

Result: `Hello, MicroPython!`. Then:

```python
>>> 17 * 3
51
>>> 2 ** 10
1024
```

What's happening here? The REPL executes each entered line right after pressing Enter. Expressions like `17 * 3` are evaluated, and the result is printed automatically. Execution takes fractions of a second — the microcontroller runs at 80–240 MHz and handles simple computations very quickly. Note: the `>>>` prompt returns after every command — this means the board is ready for the next input.

### Solution 2
The `hello.py` file:

```python
print("Hello, MicroPython!")
import sys
print(sys.version)
```

After running with the Run button in Thonny you will see:

```
Hello, MicroPython!
3.4.0
```

What's happening here? The script runs as a single "launch": lines go from top to bottom, and all output is printed together. In the REPL, each line runs separately and the result is visible immediately — so the REPL is convenient for experimenting, while files are for writing real programs. `sys.version` shows the MicroPython version (for example, `3.4.0` is the Python 3.4 core with additions). This is a quick way to make sure the firmware is installed correctly.

### Solution 3
Program:

```python
import os
print(os.uname())
```

Typical output for ESP32:

```
(sysname='esp32', nodename='esp32', release='1.24.0', version='v1.24.0 on 2024-09-02', machine='ESP32 module with ESP32')
```

And for Raspberry Pi Pico:

```
(sysname='rp2', nodename='rp2', release='1.24.0', version='v1.24.0 on 2024-09-02', machine='Raspberry Pi Pico with RP2040')
```

What's happening here? `os.uname()` returns an object with fields: `sysname` — platform name, `release` — firmware version, `machine` — hardware description. This is useful when you need to write a program that behaves differently on different boards. For example, you can compare `sysname` with `"esp32"` and choose different pin numbers.

### Solution 4
`dir(machine)` will return a list like:

```
['ADC', 'DAC', 'I2C', 'Pin', 'PWM', 'RTC', 'SoftI2C', 'SoftSPI', 'SPI', 'Timer', 'UART', 'WDT', ...]
```

Three meaningful names and their purpose:

- `Pin` — digital pin control: turn an output on/off, read the level at an input. This is the basis of all hardware work.
- `ADC` — analog-to-digital converter: converts voltage (for example, from a potentiometer) into a number from 0 to 65535.
- `I2C` — a bus for communicating with external chips: displays, sensors, memory.

What's happening here? `dir()` shows all names available in the module. By reading the names, you can guess their capabilities: capital letters indicate classes. This is a universal technique — you can explore any module this way, even without documentation.

### Solution 5
Program:

```python
import time
print("Starting work")
time.sleep(2)
print("Done")
```

Result: first `Starting work` is printed, then the board "freezes" for two seconds, and only then `Done` appears. With `time.sleep(5)` the pause becomes even more noticeable. What's happening here? `time.sleep(2)` stops the program for 2 seconds (time is in seconds). This is the basic function for all time delays: pauses between LED blinks, waiting for a sensor response, button debouncing. MicroPython also has `time.sleep_ms()` — for milliseconds, it is more convenient when you need precision.
<!--/SOLUTION-->

<!--QUIZ-->
What is MicroPython?
- An extension for web frameworks
- An implementation of Python for microcontrollers
- A new programming language similar to C
- A library for data analysis
* Correct answer: An implementation of Python for microcontrollers
MicroPython is a compact implementation of Python that runs directly on a microcontroller without an operating system.

Why does MicroPython fit into a device with 256 KB of RAM?
- Because it is written in assembly
- Because the interpreter is compact and manages the hardware itself
- Because it doesn't store variables
- Because it only works with integers
* Correct answer: Because the interpreter is compact and manages the hardware itself
MicroPython doesn't require an OS: its interpreter takes a few hundred kilobytes and works directly with the hardware.

Which module in MicroPython is responsible for controlling input/output pins?
- os
- sys
- machine
- math
* Correct answer: machine
The machine module contains Pin, PWM, ADC, I2C, Timer, and other classes for working with hardware.

What will print(2 ** 10) output?
- 12
- 20
- 1024
- 10240
* Correct answer: 1024
The ** operator raises to a power: 2 to the tenth power equals 1024.

What is the interactive mode called that executes commands one by one right after input?
- Compiler
- REPL
- Driver
- Sandbox
* Correct answer: REPL
REPL shows the >>> prompt and executes every entered command instantly — convenient for experiments.

How do you find out the platform name MicroPython is running on?
- print(os.uname())
- print(sys.path)
- print(gc.mem_free())
- print(machine.reset())
* Correct answer: print(os.uname())
os.uname() returns an object with sysname, release, version, and machine fields — i.e., info about the board and firmware.

What is the time module used for in MicroPython?
- To control input/output pins
- For pauses and working with time
- To connect to Wi-Fi
- To work with the screen
* Correct answer: For pauses and working with time
The time.sleep() and time.sleep_ms() functions make pauses, and time.ticks_ms() measures intervals — all about time.

What needs to be written into the board's memory to install MicroPython?
- A file with a .py extension
- Firmware — a file with a .bin extension
- A README text file
- C sources
* Correct answer: Firmware — a file with a .bin extension
Firmware (.bin) contains the MicroPython interpreter; it is loaded via Thonny or esptool.
<!--/QUIZ-->
