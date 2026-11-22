---
title: Email Campaigns: smtplib and Message Templates
summary: Sending emails from Python: smtplib, EmailMessage structure, HTML and attachments, templates, and safe credential storage.
order: 7
duration: 45 min
difficulty: intermediate
tags: smtplib, email, campaigns, templates
---

Email is one of the most lively ways to interact with a user: confirmations, notifications, reports. Python can send it out of the box, without third-party services, and templates let you build beautiful emails without mixing code and HTML.

## Building a Message

The modern way is the `EmailMessage` class from the `email.message` module:

```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Hello from Python"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("This is the message text.\nSecond line.")
```

Headers are set like dict entries, and `set_content` puts the body. You can look at the finished message like this:

```python
print(msg.as_string())
```

You'll see headers, an empty line, and the body — that's exactly what goes out over SMTP.

## The HTML Version

Plain text is the base, but campaigns live on HTML. You can put both versions in one message: recipients whose clients don't support HTML will see text.

```python
msg.set_content("Check out our offer!")
msg.add_alternative(
    "<h1>Hi!</h1><p>Check out our offer.</p>",
    subtype="html",
)
```

`add_alternative` adds an alternative part: the message becomes multipart, and the client picks the richest supported version.

## Attachments

Files are added with `add_attachment`:

```python
msg.add_attachment(
    open("report.pdf", "rb").read(),
    maintype="application",
    subtype="pdf",
    filename="report.pdf",
)
```

For images `maintype` is `image`, for archives — `application`/`zip`. The key is to pass bytes, a type, and the file name.

## Sending via smtplib

Now the most important part — handing the message to the server:

```python
import smtplib

with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
    server.login("noreply@example.com", "password")
    server.send_message(msg)
```

`smtplib.SMTP_SSL` connects over a secure channel and takes a host and port. `login` authenticates, `send_message` sends the ready message. Ports: 465 — SSL right away, 587 — STARTTLS after `server.starttls()`.

## Message Templates

Mixing HTML and code is bad. The template goes into a separate string, and values are substituted into it:

```python
from string import Template

template = Template(
    """<p>Hi, $name!</p>
    <p>Your order #$order is confirmed.</p>"""
)

html = template.substitute(name="Anna", order=12345)
```

For serious campaigns, Jinja2 with loops and conditions is more convenient, but the built-in `string.Template` covers simple cases with zero dependencies.

## Security

Never write a password in code. Store it in environment variables:

```python
import os

password = os.environ["SMTP_PASSWORD"]
```

`os.environ` fails with a clear error if the variable is missing — and the password never reaches the repository.

## Sending to a List

```python
recipients = ["a@example.com", "b@example.com"]

for email in recipients:
    msg = EmailMessage()
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    msg["Subject"] = "Promotion"
    msg.set_content("20% discount!")
    server.send_message(msg)
```

A separate message is assembled for each recipient — that makes personalization easier and keeps the recipient list hidden from others.

## Summary

- `EmailMessage` assembles the message: headers, text, HTML, attachments.
- `smtplib.SMTP_SSL` sends; credentials come from the environment.
- Templates separate HTML from code.
- A list campaign is a loop with a personal message for each address.

<!--TASK-->
### Task 1
Assemble a simple message with `EmailMessage`: subject "Test", sender `noreply@example.com`, recipient `user@example.com`, text "Hi! This is a test message." Print `msg.as_string()` and make sure all headers and the body are in the output.

### Task 2
Assemble a message with two versions: the text one "Check out our offer!" and an HTML version with an `<h1>Hi!</h1>` heading and a paragraph. Print `msg.get_content_type()` and `msg.is_multipart()` — they should be `multipart/alternative` and `True`. Then print `msg.as_string()` and find both parts.

### Task 3
Write a function `attach_report(msg, filename)` that reads the file as bytes and adds it as an attachment with `maintype="application"`, `subtype="pdf"`, and the file name. Create a test file `report.pdf` (with any content), assemble a message, and add the attachment. Check that `len(msg.iter_attachments()) == 1` and that the attachment name matches.

### Task 4
Write a function `send_email(msg, smtp_host, smtp_port, user, password)` that sends a message via `smtplib.SMTP_SSL`. Use a `with` block. Then rewrite it so host, port, login, and password come from `os.environ` with names `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, with default host and port values `smtp.example.com` and `465`.

### Task 5
Write a function `send_campaign(template_text, recipients, **values)` that for each address in the list builds a message: subject "Promotion", body — the result of substituting `$name` and `$order` from `values` into the template. Instead of actually sending, the function should print `Sent to <email>` and, for verification, return the list of addresses. Make sure different recipients get the same text, but with values substituted in.
<!--/TASK-->

<!--HINT-->
### Hint 1
Headers are set via `msg["Subject"] = ...` and so on; body — `msg.set_content("...")`. `msg.as_string()` returns the whole message as a string, and `print(msg.as_string())` shows it in full.

### Hint 2
`add_alternative(html, subtype="html")` adds the HTML part, `set_content` — the text one. `msg.is_multipart()` returns `True` when there's more than one part; `msg.get_content_type()` shows the multipart message type.

### Hint 3
Reading the file: `data = open(filename, "rb").read()`. Adding: `msg.add_attachment(data, maintype="application", subtype="pdf", filename=filename)`. Iterating attachments: `list(msg.iter_attachments())` — a list of tuples with content and headers.

### Hint 4
`smtplib.SMTP_SSL(smtp_host, smtp_port)` inside `with`; `server.login(user, password)` then `server.send_message(msg)`. For moving to the environment: `os.environ.get("SMTP_HOST", "smtp.example.com")` and `int(os.environ.get("SMTP_PORT", "465"))` — don't forget `import os`.

### Hint 5
Use `string.Template(template_text).substitute(**values)` for the body; `EmailMessage` with `From` and `To` headers; return the `recipients` list. To verify, just call the function with fake values — no sending needed.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Test"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Hi! This is a test message.")

print(msg.as_string())
```

`EmailMessage` assembles the message in the correct format. The `Subject`, `From`, `To` headers are stored as message fields, the body via `set_content`. `as_string()` serializes everything into one string: headers first, then an empty line and the body. This is exactly the format any SMTP server understands.

### Solution 2
```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Offer"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Check out our offer!")
msg.add_alternative(
    "<h1>Hi!</h1><p>Check out our offer.</p>",
    subtype="html",
)

print(msg.is_multipart())       # True
print(msg.get_content_type())   # multipart/alternative
print(msg.as_string())
```

`set_content` creates the first part — text; `add_alternative` adds the second — HTML. The message becomes `multipart/alternative`: the client picks the richest supported version itself. `as_string()` will show both parts with `Content-Type: text/plain` and `Content-Type: text/html` headers.

### Solution 3
```python
from email.message import EmailMessage

def attach_report(msg, filename):
    with open(filename, "rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype="application", subtype="pdf", filename=filename)

with open("report.pdf", "wb") as f:
    f.write(b"%PDF-1.4 fake content")

msg = EmailMessage()
msg["Subject"] = "Report"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("The report is attached.")
attach_report(msg, "report.pdf")

attachments = list(msg.iter_attachments())
print(len(attachments))                              # 1
print(attachments[0][1]["Content-Disposition"])      # contains filename=report.pdf
```

An attachment is a message part with `Content-Type: application/pdf` and a `Content-Disposition` header. `add_attachment` takes bytes, the main and subtype, and the file name. `iter_attachments()` returns the attachment parts, so you can check that the file was really added.

### Solution 4
```python
import smtplib
import os

def send_email(msg, smtp_host, smtp_port, user, password):
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(user, password)
        server.send_message(msg)

def send_email_env(msg):
    host = os.environ.get("SMTP_HOST", "smtp.example.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]
    send_email(msg, host, port, user, password)
```

`smtplib.SMTP_SSL` establishes a secure connection; `login` authenticates, `send_message` sends the ready message. The second version takes settings from the environment: defaults for host and port, required variables for credentials. This way the password never enters the source code or repository.

### Solution 5
```python
from string import Template
from email.message import EmailMessage

def send_campaign(template_text, recipients, **values):
    template = Template(template_text)
    for email in recipients:
        msg = EmailMessage()
        msg["Subject"] = "Promotion"
        msg["From"] = "noreply@example.com"
        msg["To"] = email
        msg.set_content(template.substitute(**values))
        print(f"Sent to {email}")
    return recipients

template = "Hi, $name! Your order #$order is confirmed."
result = send_campaign(template, ["a@example.com", "b@example.com"], name="Anna", order=123)
print(result)
```

`string.Template` substitutes values from the dict into the template: `$name` and `$order` are replaced with "Anna" and "123". In the loop, a personal message is assembled for each address — so recipients don't see each other's addresses, and the text can be personalized. The function returns the list of addresses, letting you verify the result and reuse it.
<!--/SOLUTION-->

<!--QUIZ-->
Which class assembles an email in Python?
- smtplib.SMTP
- email.message.EmailMessage
- string.Template
- socket.socket
* Correct answer: email.message.EmailMessage
EmailMessage stores the headers and body and can serialize them in as_string().

How do you set the message subject?
- msg["Subject"] = "..."
- msg.subject = "..."
- set_content("...")
- add_alternative("...")
* Correct answer: msg["Subject"] = "..."
Message headers are assigned like dictionary keys: Subject, From, To.

What does msg.as_string() do?
- Sends the message
- Returns the message as a string in SMTP format
- Adds an attachment
- Encrypts the message
* Correct answer: Returns the message as a string in SMTP format
as_string() serializes the message: headers, empty line, body — a ready-to-send format.

Why do you need add_alternative(html, subtype="html")?
- To replace text with HTML
- To add an HTML version of the message alongside the text one
- To attach a file
- To set the subject
* Correct answer: To add an HTML version of the message alongside the text one
The message becomes multipart: the client picks the supported version.

Which class sends an email over SMTP?
- SMTP_SSL from smtplib
- EmailMessage
- Template
- os.environ
* Correct answer: SMTP_SSL from smtplib
smtplib.SMTP_SSL connects over a secure channel and sends the message via send_message.

What does server.send_message(msg) send?
- Only the message body
- The whole message
- Only the headers
- An attachment file
* Correct answer: The whole message
send_message accepts an EmailMessage object and sends it with all headers and parts.

Why shouldn't a password be stored in code?
- It won't work
- It lands in the repository and compromises the account
- The code becomes slower
- Emails go to spam
* Correct answer: It lands in the repository and compromises the account
Secrets are kept in environment variables — the code stays safe when published.

What does string.Template(t).substitute(**values) do?
- Parses HTML
- Substitutes values into the template instead of $name
- Sends an email
- Creates an EmailMessage
* Correct answer: Substitutes values into the template instead of $name
substitute replaces placeholders like $name with the passed values.

How do you add a PDF attachment to a message?
- msg.add_attachment(data, maintype="application", subtype="pdf", filename="f.pdf")
- msg.set_content(open("f.pdf").read())
- msg.attach_pdf("f.pdf")
- msg["Attachment"] = "f.pdf"
* Correct answer: msg.add_attachment(data, maintype="application", subtype="pdf", filename="f.pdf")
add_attachment takes bytes, types, and the file name, forming a part with correct headers.

Which protocol does smtplib use?
- HTTP
- SMTP
- FTP
- SSH
* Correct answer: SMTP
Simple Mail Transfer Protocol (SMTP) is the standard for sending email.
<!--/QUIZ-->
