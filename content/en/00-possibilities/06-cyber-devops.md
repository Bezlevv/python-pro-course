---
title: DevOps, networks, security, robotics
summary: Infrastructure and deployment automation, network programming, data protection, and Python in robotics and IoT.
order: 6
duration: 30 min
difficulty: beginner
tags: devops, networking, security, robotics, iot, hashlib
---

## Python manages not only code but computers too

When a program goes live, it needs "infrastructure": servers, databases, automatic checks, backups. A DevOps engineer takes care of all this. And yes, Python is the main language of this profession. But that's not all: network tools, data protection utilities, and even robot programs are written in Python. Let's walk through these four worlds.

## DevOps: infrastructure automation

DevOps (Development + Operations) is a culture where development and operations work together and everything routine is automated. What a DevOps engineer does in Python:

- writes scripts for deploying services (deployment);
- automates code checks and test runs;
- collects metrics: server load, errors, response times;
- works with clouds (AWS, Yandex Cloud) — Python is everywhere.

Here is a typical "infrastructure" script — it writes logs to a file so you can later understand what was happening:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.info("Service started")
logging.warning("Low memory")
logging.error("Failed to connect to the database")
```

The `logging` module keeps an event journal. It's the standard in any industrial system: nothing gets "lost", everything is recorded with time and importance level.

## Networks: programs talk over wires

Any network is an exchange of messages. Python provides a low-level tool — the `socket` module, through which programs establish connections:

```python
import socket

# Get the site's IP address by its name
ip = socket.gethostbyname("google.com")
print("IP address of google.com:", ip)
```

`socket.gethostbyname()` turns a domain name into an IP address — a step toward understanding how the internet works. All of Python's network libraries are built on `socket`, from `urllib.request` to Telegram bots. Python is also great at "listening to a port" and becoming a server that accepts connections.

## Security: data protection

Security is not only movie hacks but everyday things: passwords, encryption, data integrity checks. Python helps both defenders and (legally) researchers.

The main tool is **hashing**. A hash is a "fingerprint" of data: the same text always produces the same short string, and different texts almost always produce different ones:

```python
import hashlib

password=[redacted]
hash_value = hashlib.sha256(password.encode()).hexdigest()
print("Password hash:", hash_value)
```

Why does this matter? Real passwords are not stored in the database — their hashes are. If the database is stolen, the attacker won't learn the original passwords, because restoring text from a hash is practically impossible. `hashlib.sha256` is a cryptographic algorithm, `encode()` turns the string into bytes, `hexdigest()` into a readable string.

## Robotics and IoT

The Internet of Things (IoT) is when smart devices talk to each other: bulbs, sensors, thermostats, cameras. Python is here too:

- **Raspberry Pi** — a mini-computer the size of a bank card that runs Python: smart home, weather stations, wheeled robots.
- **MicroPython** — a version of Python for microcontrollers (boards like ESP32, Arduino). Same syntax, just on small hardware.
- **Robotics** — from educational robots to industrial manipulators: Python controls motors, reads sensors, processes camera images.

An example for Raspberry Pi — blinking an LED:

```python
# Simplified scheme (for real — on Raspberry Pi via GPIO)
import time

for i in range(5):
    print("LED on" if i % 2 == 0 else "LED off")
    time.sleep(0.5)
```

The main takeaway: **Python works everywhere — from a server cluster to a small board costing a few dollars.**

## Lesson summary

Today we learned:

- that DevOps engineers automate infrastructure in Python;
- how to log events with the `logging` module;
- how programs communicate over the network via `socket`;
- why passwords are stored as hashes and how to compute them with `hashlib`;
- that Python lives in robotics and IoT: Raspberry Pi, MicroPython, Arduino.

Now let's try on the engineer's role.

<!--TASK-->
### Task 1
Write a program `password_hash.py` that takes the string `"my-secret-password"`, computes its SHA-256 hash, and prints it along with the hash string's length. Use `hashlib.sha256(text.encode()).hexdigest()`. Then also print the hash of `"my-secret-passwor"` (one character shorter). Compare the two strings visually: they must be completely different — that is the property of a hash.

### Task 2
Write a program `password_checker.py` that stores a reference password hash (take it from the result of Task 1) and asks the user to enter a password via `input()`. The program computes the hash of the entered string and compares it with the reference. If they match — print `Access granted`, otherwise — `Access denied`. Test both cases: a correct and an incorrect password.

### Task 3
Write a program `domain_ip.py` that takes a domain name (e.g., `"python.org"`), resolves its IP address via `socket.gethostbyname()`, and prints `Domain: python.org -> IP: 151.101.0.223`. Wrap the call in `try/except` and on error print `Could not resolve address`. Test on two or three domains, e.g., `python.org` and `github.com`.

### Task 4
Write a program `logger_demo.py` that configures logging to a file `app.log` (with the INFO level and the lesson's format), then writes five events: an info about startup, three warnings (`logging.warning`), and one error (`logging.error`). After writing, open `app.log`, read it, and print its contents. Make sure the log contains time, level, and text of each event.

### Task 5
Write a program `monitor.py` — a "state monitor" that 3 times with a 2-second pause writes the current time and free memory level to the log (you can use a random number from 0 to 100 with `random.randint(0, 100)` to simulate the percentage). Use `logging` and `time.sleep(2)`. At the end read and print the log file contents. This is a mini-model of real monitoring agents.
<!--/TASK-->

<!--HINT-->
### Hint 1
Add `import hashlib`. Compute the hash: `h = hashlib.sha256("my-secret-password".encode()).hexdigest()`. The hash string length is `len(h)` (for SHA-256 it is always 64 characters). Write the second string with one letter removed at the end.

### Hint 2
Store the reference hash as a string: `expected = "full_hash_from_task_1"`. Then `user_input = input("Enter password: ")` and `actual = hashlib.sha256(user_input.encode()).hexdigest()`. The comparison is `if actual == expected:`. Don't print the password itself — that's bad practice.

### Hint 3
Add `import socket`. Wrap the call: `try: ip = socket.gethostbyname(domain) except socket.gaierror: print("Could not resolve address")`. Catch the specific `socket.gaierror` exception — it is raised when the domain is not found. Print the line with an f-string.

### Hint 4
Configure `logging.basicConfig(level=logging.INFO, filename="app.log", encoding="utf-8", format="%(asctime)s %(levelname)s %(message)s")`. Then call `logging.info(...)`, `logging.warning(...)` three times, and `logging.error(...)`. After that read the file: `print(Path("app.log").read_text(encoding="utf-8"))` or with a regular `open()`.

### Hint 5
In a loop `for i in range(3):` write `logging.info(f"Check {i+1}: free {random.randint(0, 100)}%")` and then `time.sleep(2)`. Don't forget `import random`, `import time`, `import logging`, and the `basicConfig` setup. At the end print the log file contents.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import hashlib

h1 = hashlib.sha256("my-secret-password".encode()).hexdigest()
h2 = hashlib.sha256("my-secret-passwor".encode()).hexdigest()

print("Hash of the correct password:", h1)
print("Hash length:", len(h1))
print("Hash of the password with a typo:", h2)
```

Result (abbreviated):

```
Hash of the correct password: 3f70b9c2...  (64 characters)
Hash length: 64
Hash of the password with a typo: 8a1c5d70...  (completely different!)
```

What happens here? `"my-secret-password".encode()` turns the string into a byte sequence — hash functions work with bytes. `hashlib.sha256(...)` creates a hash object, `.hexdigest()` — a string of 64 hexadecimal characters. The key observation: changing one character completely changes the hash. Because of this property hashes are used for integrity checks: if a file changes by even a byte, its hash becomes different, and that's immediately visible.

### Solution 2
Solution:

```python
import hashlib

expected = "3f70b9c2..."  # insert your hash from Task 1 here
user_input = input("Enter password: ")
actual = hashlib.sha256(user_input.encode()).hexdigest()

if actual == expected:
    print("Access granted")
else:
    print("Access denied")
```

Result with the correct password:

```
Enter password: my-secret-password
Access granted
```

What happens here? We don't store the password but its hash. On input, we compute the hash of the entered string and compare it with the reference. If the strings match, their hashes match, so the password is correct. This is how real authentication works: the database stores hashes, and even a database leak doesn't reveal passwords. Note: if you enter a password with a typo, the hash will differ and access will be denied — that's the hash's avalanche effect in action.

### Solution 3
Solution:

```python
import socket

def resolve(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"Domain: {domain} -> IP: {ip}")
    except socket.gaierror:
        print("Could not resolve address:", domain)

resolve("python.org")
resolve("github.com")
resolve("no-such-domain.xyz")
```

Result (approximately):

```
Domain: python.org -> IP: 151.101.0.223
Domain: github.com -> IP: 140.82.112.4
Could not resolve address: no-such-domain.xyz
```

What happens here? `socket.gethostbyname(domain)` queries the Domain Name System (DNS) and gets the IP address. `try/except` with `socket.gaierror` catches the case when the domain doesn't exist (gaierror — "getaddrinfo error"). This is our first direct conversation with the internet's network infrastructure. Such lookups happen thousands of times per second when you simply open a site in a browser.

### Solution 4
Solution:

```python
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.info("Service started")
logging.warning("Low memory")
logging.warning("Disk 90% full")
logging.warning("Slow database connection")
logging.error("Failed to connect to the database")

print(Path("app.log").read_text(encoding="utf-8"))
```

Result (approximately):

```
2026-11-01 12:00:00,123 INFO Service started
2026-11-01 12:00:00,124 WARNING Low memory
...
```

What happens here? `basicConfig` configures logging once: INFO level (all events of this level and above are written), the file `app.log`, and a format with time and level. Each event is then appended to the file with a timestamp. `Path("app.log").read_text()` reads the log back. In industrial systems such logs are the main way to understand what happened to a service: when it crashed, what preceded it, where to look for the cause.

### Solution 5
Solution:

```python
import logging
import random
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    filename="monitor.log",
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)

for i in range(3):
    memory = random.randint(0, 100)
    logging.info(f"Check {i + 1}: free {memory}%")
    time.sleep(2)

print(Path("monitor.log").read_text(encoding="utf-8"))
```

Result (approximately):

```
2026-11-01 12:05:00,112 INFO Check 1: free 67%
2026-11-01 12:05:02,119 INFO Check 2: free 42%
2026-11-01 12:05:04,125 INFO Check 3: free 88%
```

What happens here? The loop runs three times, each event is written to the log, and `time.sleep(2)` creates a pause between checks — like a real monitoring agent that polls the system every few seconds. The f-string inserts the check number and the free memory percentage. This is a mini-model of real monitoring systems like Zabbix or Prometheus: they collect metrics and write them to journals the same way, just at a larger scale.
<!--/SOLUTION-->

<!--QUIZ-->
What is DevOps?
- A culture and practices that unite development and operations
- A programming language
- A program for drawing
* Correct answer: A culture and practices that unite development and operations
DevOps automates deployment, testing, and monitoring of services.

What is the logging module for?
- Keeping an event journal of the program
- Drawing charts
- Working with the network
* Correct answer: Keeping an event journal of the program
logging records events with time and importance level to the console or a file.

What does socket.gethostbyname("python.org") do?
- Returns the domain's IP address
- Opens the site in a browser
- Checks internet speed
* Correct answer: Returns the domain's IP address
The function finds the host address via DNS by its domain name.

What is a hash?
- A "fingerprint" of data: a short string, unique for different data
- An encrypted password that can be decrypted
- A random number
* Correct answer: A "fingerprint" of data: a short string, unique for different data
A hash is irreversible: the original text cannot be restored from it.

What does hashlib.sha256(text.encode()).hexdigest() do?
- Computes the SHA-256 hash and returns it as a string
- Encrypts text and allows decrypting it
- Compresses text
* Correct answer: Computes the SHA-256 hash and returns it as a string
hexdigest() returns a 64-character hexadecimal string — the hash.

Why are passwords stored as hashes?
- If the database leaks, attackers won't learn the original passwords
- Because hashes take less space
- It speeds up login
* Correct answer: If the database leaks, attackers won't learn the original passwords
Hashing protects users even when the database leaks.

What happens to a hash if one character in the text changes?
- The hash changes completely
- The hash doesn't change
- The hash becomes shorter
* Correct answer: The hash changes completely
Avalanche effect: the smallest change in input gives a completely different hash.

Which devices does MicroPython run on?
- Microcontrollers and small boards like ESP32
- Only supercomputers
- Only phones
* Correct answer: Microcontrollers and small boards like ESP32
MicroPython is a version of Python for hardware with limited resources.

Which mini-computer is often used for a smart home in Python?
- Raspberry Pi
- A mechanical calculator
- A game console
* Correct answer: Raspberry Pi
Raspberry Pi runs Python scripts to control sensors and devices.

What does time.sleep(2) do?
- A 2-second pause between program actions
- Speeds the program up 2 times
- Increases font size 2 times
* Correct answer: A 2-second pause between program actions
time.sleep() suspends the program for the given number of seconds.
<!--/QUIZ-->
