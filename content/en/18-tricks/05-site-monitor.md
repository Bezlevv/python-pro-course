---
title: Site Monitoring and Notifications
summary: We'll write a script that regularly checks site availability with requests and emails you via smtplib when there are problems.
order: 5
duration: 30 min
difficulty: intermediate
tags: requests, smtplib, monitoring, mail
---

Imagine: you administer a site, and you learn it went down from your users. Not worthy. The right approach is monitoring: a program checks the site every few minutes itself and writes to you if something's wrong. Let's examine two building blocks of this system: HTTP requests (`requests`) and email (`smtplib`).

## Checking Availability

The HTTP status tells whether everything is OK with the site. 200 — great, 404 — page not found, 500 — server error:

```python
import requests

r = requests.get("https://example.com")
print(r.status_code)                     # 200
print(r.elapsed.total_seconds())         # response time in seconds
```

Waiting for a response forever is a bad idea. So always specify `timeout`:

```python
try:
    r = requests.get("https://example.com", timeout=5)
    r.raise_for_status()   # raises an exception on 4xx/5xx codes
    print("Site is alive, time:", round(r.elapsed.total_seconds(), 2), "s")
except requests.exceptions.RequestException as e:
    print("Problems:", e)
```

`raise_for_status()` turns a bad status into an exception — and success/failure handling becomes uniform.

## Sending an Email

The standard `smtplib` module handles sending mail. All mail works the same way: connect to an SMTP server, switch to a secure connection (STARTTLS), log in, and send the message:

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "monitor@example.com"
    msg["To"] = "admin@example.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("monitor@example.com", "PASSWORD")
        server.send_message(msg)
```

You'll get the SMTP server, login, and password from your mail provider (for example, for Gmail: `smtp.gmail.com`, port 587). Never put a password directly into code — store it in an environment variable.

## The Monitoring Loop

Now join both parts: check + notify. An infinite loop with a pause:

```python
import time

while True:
    try:
        r = requests.get("https://example.com", timeout=5)
        r.raise_for_status()
        print(time.asctime(), "OK")
    except requests.exceptions.RequestException as e:
        send_alert("Site is down!", str(e))
        print("Site is down!")
    time.sleep(60)
```

The main idea is a loop with `time.sleep`, which is the essence of any monitoring. In the tasks we'll polish this scheme: add a list of sites and send email only on state changes.

<!--TASK-->
### Task 1
Check `https://example.com` with `requests.get` and print the status and response time in seconds. Use `r.status_code` and `r.elapsed.total_seconds()`. Expected result: lines like `Status: 200` and `Response time: 0.43 s`.

### Task 2
Make the check safe: add `timeout=5` and wrap the request in `try`/`except requests.exceptions.RequestException`. On error print `Site is unavailable: <description>`. Test on a definitely unavailable address, e.g. `https://nonexistent-domain-12345.ru`. Expected result: for a live site — the status; for a nonexistent one — a neat message without crashing.

### Task 3
Write a program that checks several sites: a list of URLs in a `urls` variable, a loop over it, and for each — status or error text. Expected result: for each site a line like `https://example.com: 200` or `https://broken.example: connection error`.

### Task 4
Write a function `send_alert(subject, body)` that sends an email via `smtplib`: `MIMEText`, Subject/From/To headers, `SMTP(host, 587)`, `starttls()`, `login()`, `send_message(msg)`. Take the password from the `MAIL_PASSWORD` environment variable (the `os` module). Call it with a test message. Expected result: the email arrives at the specified mailbox (or the program reports a connection error if the SMTP server isn't configured).

### Task 5
Assemble a full monitor: every 60 seconds check `https://example.com` with `requests.get(URL, timeout=5)`, print an `OK` or `FAIL` log, and send an email via `send_alert` only when transitioning from "working" to "down" (that is, don't repeat the email every minute while the site is down). Use `time.sleep(60)` and a boolean state variable. Expected result: a log line in the console every minute, and the email goes out only once at the start of the outage.
<!--/TASK-->

<!--HINT-->
### Hint 1
`r = requests.get("https://example.com")` — then print `r.status_code` and `round(r.elapsed.total_seconds(), 2)`. Don't forget `import requests`. If you have no internet at hand, substitute `https://httpbin.org/status/200`.

### Hint 2
Keep the network call only inside `try`, and in `except requests.exceptions.RequestException as e` print `f"Site is unavailable: {e}"`. Add `raise_for_status()` after `requests.get` so codes 404/500 also count as problems.

### Hint 3
`for url in urls:` — inside, the same `try`/`except`, but `print(url, "-", r.status_code)` on success and `print(url, "- error:", e)` on failure. Declare `urls` as a list before the loop.

### Hint 4
Skeleton: `msg = MIMEText(body, "plain", "utf-8")`; fill `msg["Subject"]`, `msg["From"]`, `msg["To"]`; then `with smtplib.SMTP("smtp.example.com", 587) as server:` → `server.starttls()` → `server.login("monitor@example.com", os.environ["MAIL_PASSWORD"])` → `server.send_message(msg)`. Import `os`, `smtplib`, `MIMEText`.

### Hint 5
Create `was_down = False` before the loop. On success set `was_down = False` and print `OK`. In `except`: if `not was_down` — call `send_alert(...)`, then set `was_down = True`. Put the pause at the end of the loop. This way the email goes out once, not every minute.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import requests

r = requests.get("https://example.com")
print("Status:", r.status_code)
print("Response time:", round(r.elapsed.total_seconds(), 2), "s")
```

Result (example):

```
Status: 200
Response time: 0.43 s
```

What's going on here? `requests.get` performs a GET request and returns a `Response` object. Its `status_code` attribute is the HTTP status, `elapsed` is the request duration (a `timedelta` object), and `total_seconds()` converts it to seconds. `round(..., 2)` rounds to two decimal places so the output doesn't have long tails. This pair of numbers is enough to understand that the site is alive and responds fast.

### Solution 2
Solution:

```python
import requests

url = "https://example.com"
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    print("Status:", r.status_code)
except requests.exceptions.RequestException as e:
    print("Site is unavailable:", e)
```

Result (example for an unavailable address):

```
Site is unavailable: HTTPConnectionPool(host='nonexistent-domain-12345.ru', port=80): Max retries exceeded with url: ...
```

What's going on here? `timeout=5` makes `requests` abandon the request if no response comes within 5 seconds — otherwise the script could hang for minutes. `raise_for_status()` throws an exception on 4xx/5xx statuses, so a 500 also lands in `except`. `requests.exceptions.RequestException` is the parent class of all the library's network errors: it catches timeouts, connection problems, and bad statuses alike. The program never crashes with a traceback.

### Solution 3
Solution:

```python
import requests

urls = [
    "https://example.com",
    "https://httpbin.org/status/200",
    "https://nonexistent-domain-12345.ru",
]

for url in urls:
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        print(url, "-", r.status_code)
    except requests.exceptions.RequestException as e:
        print(url, "- error:", e)
```

Result (example):

```
https://example.com - 200
https://httpbin.org/status/200 - 200
https://nonexistent-domain-12345.ru - error: ...
```

What's going on here? We moved the check into a loop: the same code runs for every address in the list. This is a classic technique: data goes in a list, logic is written once. Even if one site fails, `except` catches the error and the loop continues with the next address. Such a list is easy to extend: add a line — and the site is under watch.

### Solution 4
Solution:

```python
import os
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "monitor@example.com"
    msg["To"] = "admin@example.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("monitor@example.com", os.environ["MAIL_PASSWORD"])
        server.send_message(msg)

send_alert("Test", "This is a test email from monitoring.")
print("Email sent")
```

What's going on here? `MIMEText` builds a MIME-formatted message: body, `plain` type, UTF-8 encoding (important for non-Latin scripts). Headers are filled like a dict. `SMTP("smtp.example.com", 587)` opens a connection to the server, `starttls()` switches it to encryption — without it the login and message text would fly in plain text. `login()` takes the login and password from an environment variable: the secret never enters the code or the version control system. `send_message(msg)` sends the finished message. The `with` context manager closes the connection itself.

### Solution 5
Solution:

```python
import os
import time
import smtplib
import requests
from email.mime.text import MIMEText

def send_alert(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = "monitor@example.com"
    msg["To"] = "admin@example.com"
    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("monitor@example.com", os.environ["MAIL_PASSWORD"])
        server.send_message(msg)

URL = "https://example.com"
was_down = False

while True:
    try:
        r = requests.get(URL, timeout=5)
        r.raise_for_status()
        print(time.asctime(), "OK")
        was_down = False
    except requests.exceptions.RequestException as e:
        print(time.asctime(), "FAIL", e)
        if not was_down:
            send_alert("Site is down!", str(e))
        was_down = True
    time.sleep(60)
```

What's going on here? The `was_down` variable stores the site's previous state. While the site is alive (the `try` branch), it resets to `False`. As soon as a failure occurs, we check: if it was `False` before — this is the start of the outage, send the email and set `True`. The next minute the site is still down, but `was_down` is already `True`, so the email isn't duplicated. When the site recovers, `was_down` becomes `False` again, and the next outage is "first" once more. `time.asctime()` adds a timestamp to the log. This is what real, well-thought-out monitoring looks like.
<!--/SOLUTION-->

<!--QUIZ-->
What does HTTP status 200 mean?
- Page not found
- Request succeeded
- Server error
- Authorization required
* Correct answer: Request succeeded
200 — the site is available and responded correctly.

Why specify timeout in requests.get?
- To increase speed
- To avoid waiting for a response forever
- To add headers
- To change the method
* Correct answer: To avoid waiting for a response forever
timeout limits the waiting time: when exceeded, the request is interrupted by an exception.

What does raise_for_status() do?
- Returns the status code
- Raises an exception on 4xx/5xx statuses
- Changes the request method
- Retries the request
* Correct answer: Raises an exception on 4xx/5xx statuses
Thanks to it, a 404 or 500 also counts as an error and is handled in except.

Which standard module sends email?
- emails
- mailer
- smtplib
- sendmail
* Correct answer: smtplib
smtplib works with SMTP servers: connection, login, sending.

Why call starttls()?
- To speed up the connection
- To encrypt the connection
- To check mail
- To avoid spam
* Correct answer: To encrypt the connection
STARTTLS switches the connection to encryption — the login and message are invisible to outsiders.

What does time.sleep(60) do in monitoring?
- Speeds up the check
- Pauses 60 seconds between checks
- Prints the time
- Terminates the program
* Correct answer: Pauses 60 seconds between checks
The pause sets the check frequency: once a minute rather than nonstop.

Why does the monitoring loop need a was_down variable?
- So the email goes out only once — at the start of the outage
- To speed up site checking
- To set the pause length
- To log all sites at once
* Correct answer: So the email goes out only once — at the start of the outage
On a failure was_down becomes True, and subsequent checks don't duplicate the email while the site is down.

What happens if a site returns a 500?
- raise_for_status() raises an exception, and it's handled as a failure
- The program considers the site alive
- The request retries automatically
- The status is simply ignored
* Correct answer: raise_for_status() raises an exception, and it's handled as a failure
500 is a server error: raise_for_status() turns it into a RequestException, which is caught in except.
<!--/QUIZ-->
