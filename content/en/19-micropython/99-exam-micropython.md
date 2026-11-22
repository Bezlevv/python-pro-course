---
title: Exam: MicroPython
summary: Test your MicroPython knowledge: machine.Pin, PWM, I2C, OLED, network.WLAN, socket, urequests, memory, and best practices.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What is MicroPython?
- A Python extension for building websites
- A compact implementation of Python for microcontrollers
- A version of Python for supercomputers
- A library for working with Excel
* Correct answer: A compact implementation of Python for microcontrollers
MicroPython runs directly on a microcontroller without an operating system and takes only a few hundred kilobytes.

Which module in MicroPython controls input/output pins?
- os
- machine
- sys
- math
* Correct answer: machine
The machine module has Pin, PWM, ADC, I2C, Timer, and other classes for working with hardware.

What does led.toggle() do?
- Turns the LED on forever
- Switches the state to the opposite
- Checks whether the LED is lit
- Turns off the board's power
* Correct answer: Switches the state to the opposite
If the LED is lit — toggle() turns it off; if off — turns it on.

What value will button.value() return when the button is pressed with a Pin.PULL_UP pull-up?
- 1
- 0
- 65535
- An error
* Correct answer: 0
Pressing shorts the pin to ground, and the level drops to 0 — so for PULL_UP the logic is "inverted".

What is the value range of pwm.duty_u16()?
- 0–1
- 0–255
- 0–65535
- -100–100
* Correct answer: 0–65535
duty_u16 takes a duty cycle from 0 (off) to 65535 (full power).

What PWM frequency does a servo need?
- 1000 Hz
- 50 Hz
- 1 Hz
- Any, from 1 to 50,000 Hz
* Correct answer: 50 Hz
Servos read the pulse width at 50 Hz (20 ms period).

What does oled.show() do after oled.text(...)?
- Nothing, the text appears immediately
- Sends the buffer to the screen — without this the picture won't appear
- Clears the screen
- Increases brightness
* Correct answer: Sends the buffer to the screen — without this the picture won't appear
Drawing goes into a buffer in the board's memory, and oled.show() transfers it to the screen controller.

How do you connect the board to Wi-Fi in client mode?
- network.WLAN(network.AP_IF)
- network.WLAN(network.STA_IF).active(True); wlan.connect(...)
- network.connect("Wi-Fi")
- socket.WLAN()
* Correct answer: network.WLAN(network.STA_IF).active(True); wlan.connect(...)
STA_IF is client mode: we enable the interface and connect to an access point.

What does s.accept() do on a server?
- Sends a response to the client
- Blocks execution and waits for a client to connect, then returns the connection and address
- Closes the connection
- Checks internet availability
* Correct answer: Blocks execution and waits for a client to connect, then returns the connection and address
accept() "falls asleep" until a client arrives and returns a tuple (conn, addr).

Why is it important to call r.close() after urequests.get()?
- To print the response on the screen
- To close the connection and not waste the board's memory
- To reboot the board
- To clear garbage
* Correct answer: To close the connection and not waste the board's memory
Every open connection takes memory and resources, of which the board has very few.

Why is string concatenation in a loop bad?
- Strings can't be added in MicroPython
- Each iteration creates a new string, discarding the old one — slow and costly
- This causes the timer to hang
- It is forbidden by the language standard
* Correct answer: Each iteration creates a new string, discarding the old one — slow and costly
It's better to collect the parts in a list and join them with "".join(...) in a single pass.

What is machine.Timer for?
- To reboot the board after a given period
- To call a function periodically without blocking the main loop
- To measure temperature
- To speed up code
* Correct answer: To call a function periodically without blocking the main loop
The timer calls the callback every given period regardless of what the main program is doing.
<!--/QUIZ-->
