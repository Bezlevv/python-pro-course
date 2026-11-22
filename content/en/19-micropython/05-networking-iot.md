---
title: Wi-Fi, HTTP, and a web server on the board
summary: We connect the board to Wi-Fi, make HTTP requests via urequests, and turn the microcontroller into a real web server.
order: 5
duration: 35 min
difficulty: advanced
tags: micropython, wi-fi, http, socket, urequests, iot, esp32
---

The most valuable capability of MicroPython is turning a cheap board into a "smart" device that lives on the internet: it sends sensor data to a server and is controlled from a browser. This lesson is the heart of IoT development.

## Wi-Fi: the network module

The board (ESP32, Raspberry Pi Pico W) connects to Wi-Fi like a regular laptop. The `network` module and the `WLAN` class are responsible for this. First we create an interface in client mode (STA_IF), enable it, and connect:

```python
import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("MyNetwork", "password")

while not wlan.isconnected():
    time.sleep(1)
    print("Connecting...")

print("IP address:", wlan.ifconfig()[0])
```

`wlan.isconnected()` returns `True` when the board has received an IP address from the router. `ifconfig()` returns a tuple: (IP, mask, gateway, DNS). If the board can't connect — check the network name and password; ESP32 supports only 2.4 GHz networks.

## HTTP client: urequests

HTTP is the protocol browsers use to talk to websites. From MicroPython you can make HTTP requests with the compact `urequests` module (the analog of `requests` on a computer):

```python
import urequests

r = urequests.get("http://example.com")
print("Status:", r.status_code)   # 200 — success
print("Text:", r.text[:100])
r.close()
```

`urequests.get()` is a GET request: download a page. The response is an object with `status_code` (response code, 200 = OK), `text` (response body), and `json()` (if the server responded with JSON). Don't forget `r.close()` — the board has little memory, and open connections eat it. There are also `urequests.post()`, `put()`, `delete()`.

## Web server on the board: socket

The board can also become a server itself: listen on a port and respond to browser requests. The `socket` module is used for this — low-level network work.

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))   # listen on port 80 on all interfaces
s.listen(1)

while True:
    conn, addr = s.accept()       # wait for a client
    request = conn.recv(1024)     # read the request
    print("Request from", addr)
    conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    conn.send("<h1>Hello from the board!</h1>")
    conn.close()
```

What's happening here? `bind()` attaches "listening" to port 80, `listen(1)` enables the queue, `accept()` waits until a browser connects and returns the connection `conn` and the client's address. `recv(1024)` reads the request. Then we send two packets: the response headers and the page body. The end of the headers is an empty line `\r\n\r\n`. After `conn.close()` the loop waits for the next client again.

Open `http://IP-of-board` in a browser — you'll see your page. Controlling a device from a web page works the same way: the browser sends a request, and the server on the board reads it and, for example, turns on an LED.

## Security and care

Working with the network adds many surprises: a wrong password, an unstable network, a foreign request. Therefore wrap network operations in `try/except` and set timeouts. In real IoT devices, data is encrypted with HTTPS and control access is protected by a password — but for first experiments a local network is enough.
<!--TASK-->
### Task 1
Connect the board to your home Wi-Fi network. Write a program that connects, waits for the connection, and prints `Connected! IP: 192.168.1.23` (with your real address). If the connection fails within 15 seconds — print `Connection error` and end the program.

### Task 2
Using `urequests`, send a GET request to `http://example.com`. Print the status code and the first 100 characters of the response text. Then send a request to a non-existent address (for example, `http://192.0.2.1/nope`) and make sure the program doesn't crash — handle the error with `try/except`.

### Task 3
Write a web server that responds with a page titled `<h1>My IoT board</h1>` and text `Working!` below it. Check in a browser: open `http://IP-of-board` and make sure the page renders.

### Task 4
Add button state reading to the server: the page should show `Button: PRESSED` or `Button: NOT PRESSED` depending on the real state of the button on pin 14. Each browser request should read the pin anew. Refresh the page several times while pressing and releasing the button.

### Task 5
Build a "smart light": a server on port 80, an LED on pin 2. When you visit `http://IP-of-board/?led=on` the LED turns on; at `http://IP-of-board/?led=off` it turns off. The page shows the current state (`LED: ON` / `LED: OFF`) and two links "Turn on" and "Turn off".
<!--/TASK-->

<!--HINT-->
### Hint 1
Use `while not wlan.isconnected():` with an attempt counter (for example, `for i in range(15):`). After the loop check `wlan.isconnected()` again — if `False`, print the error and call `sys.exit()`.

### Hint 2
Wrap `urequests.get(...)` in `try: ... except OSError as e: print("Error:", e)`. After a successful response be sure to `r.close()`. `r.text[:100]` — the first 100 characters of the string.

### Hint 3
The server code from the theory: `s = socket.socket(...)`, `bind`, `listen`, an `accept` → `recv` → `send` → `close` loop. Pass the HTML whole in one `conn.send(html)` — first define `html` as a string with `\r\n\r\n` after the headers.

### Hint 4
Create `button = Pin(14, Pin.IN, Pin.PULL_UP)` next to the server. When handling the request, build the HTML depending on `button.value()`: if `0` — `PRESSED`, otherwise — `NOT PRESSED`. Insert the string via an f-string or concatenation.

### Hint 5
In the server loop read the request: `request = conn.recv(1024).decode()`. Check: `if "led=on" in request: led.on()`, `elif "led=off" in request: led.off()`. Insert the current state and links into the HTML page: `<a href="/?led=on">Turn on</a>`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Program:

```python
import network
import time
import sys

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("MyNetwork", "password")

for _ in range(15):
    if wlan.isconnected():
        break
    time.sleep(1)
    print("Connecting...")

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print("Connected! IP:", ip)
else:
    print("Connection error")
    sys.exit()
```

What's happening here? The `for` loop gives 15 attempts of one second each but exits early if the connection is established. After the loop, a second `isconnected()` check determines the outcome: the IP is taken from `ifconfig()[0]`. This is an important technique — don't hang an infinite wait: if the network is unavailable, the program should honestly say so and exit rather than freeze forever.

### Solution 2
Program:

```python
import urequests

try:
    r = urequests.get("http://example.com")
    print("Status:", r.status_code)
    print("Text:", r.text[:100])
    r.close()
except OSError as e:
    print("Error:", e)

try:
    r = urequests.get("http://192.0.2.1/nope")
    print("Status:", r.status_code)
    r.close()
except OSError as e:
    print("Error:", e)
```

What's happening here? The first request succeeds: `status_code` = 200, `text[:100]` — the first 100 characters of HTML. The second address (192.0.2.1 — a network reserved for testing) is unavailable: `urequests` will throw `OSError`, which we catch and print instead of letting the program crash. `r.close()` frees the socket — on a board with hundreds of KB of memory, every "lost" connection is a leak.

### Solution 3
Program:

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(1)

html = ("HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "\r\n"
        "<h1>My IoT board</h1>"
        "<p>Working!</p>")

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    print("Request from", addr)
    conn.send(html)
    conn.close()
```

What's happening here? The `html` string is assembled from response headers and body. `\r\n` is a line break in HTTP; the empty line separates headers from the body. `SO_REUSEADDR` lets you restart the server immediately after Ctrl+C without waiting for the OS to free the port. `accept()` blocks the program until a client arrives — the server "sleeps" waiting.

### Solution 4
Program:

```python
import socket
from machine import Pin

button = Pin(14, Pin.IN, Pin.PULL_UP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(1)

while True:
    conn, addr = s.accept()
    conn.recv(1024)
    state = "PRESSED" if button.value() == 0 else "NOT PRESSED"
    html = ("HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>Button status</h1>"
            "<p>Button: " + state + "</p>")
    conn.send(html)
    conn.close()
```

What's happening here? The button is read at the moment of each request — so the page always shows the current state. The ternary operator `a if condition else b` picks the string. Now we have a real "smart device": the browser is the remote control, the board is the instrument, and everything goes through HTTP.

### Solution 5
Program:

```python
import socket
from machine import Pin

led = Pin(2, Pin.OUT)
led.off()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(1)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    if "led=on" in request:
        led.on()
    elif "led=off" in request:
        led.off()
    state = "ON" if led.value() else "OFF"
    html = ("HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>Smart light</h1>"
            "<p>LED: " + state + "</p>"
            "<a href='/?led=on'>Turn on</a> "
            "<a href='/?led=off'>Turn off</a>")
    conn.send(html)
    conn.close()
```

What's happening here? The browser sends a request like `GET /?led=on HTTP/1.1` — and we simply look for the substring `led=on` in the request text. The HTML links point to the same addresses, so control works directly from the displayed page. This is a minimal but fully working IoT pattern: the device listens to HTTP, reacts to commands, and reports its state.
<!--/SOLUTION-->

<!--QUIZ-->
Which WLAN mode is used to connect to a router (client)?
- WLAN(AP_IF)
- WLAN(STA_IF)
- WLAN(ETH_IF)
- WLAN(GSM_IF)
* Correct answer: WLAN(STA_IF)
STA_IF is client mode (station): the board connects to an existing network.

What does wlan.ifconfig() return?
- The network name
- A tuple (IP, mask, gateway, DNS)
- Signal strength
- The router's MAC address
* Correct answer: A tuple (IP, mask, gateway, DNS)
ifconfig() gives network settings; the first element of the tuple is the board's IP address.

Which HTTP response code means success?
- 404
- 200
- 500
- 301
* Correct answer: 200
200 OK — the request was handled successfully; 404 — not found, 500 — server error.

Why call r.close() after urequests.get()?
- To close the connection and not waste memory
- To clear the screen
- To save the response to a file
- To reboot the board
* Correct answer: To close the connection and not waste memory
Every open connection takes memory and network resources; the board has few of them.

What do s.bind(), s.listen(), s.accept() do in a server?
- Connect to the internet
- Bind a port, enable the queue, and wait for a client
- Send a response to the client
- Encrypt the connection
* Correct answer: Bind a port, enable the queue, and wait for a client
bind() assigns a port, listen(1) enables the queue, accept() blocks execution until a client connects.

How do you find the substring "led=on" in a request in MicroPython?
- Search with the find method on the request object
- Via `if "led=on" in request:`
- Call regex.match()
- Split by the "=" character
* Correct answer: Via `if "led=on" in request:`
The in operator checks whether a substring occurs — the simplest way to parse a command from a URL.

Which WLAN mode is needed for the board to distribute Wi-Fi itself (access point)?
- STA_IF
- AP_IF
- ETH_IF
- GSM_IF
* Correct answer: AP_IF
AP_IF is access point mode: the board creates its own network that other devices connect to.

Why does ESP32 often not see a 5 GHz network?
- Because it only supports 2.4 GHz
- Because the router hides the network
- Due to lack of memory
- This is a feature of any Wi-Fi
* Correct answer: Because it only supports 2.4 GHz
Most ESP32 boards work only in the 2.4 GHz band — choose such a network when connecting.
<!--/QUIZ-->
