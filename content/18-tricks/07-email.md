---
title: Email-рассылки: smtplib и шаблоны писем
summary: Отправка писем из Python: smtplib, структура письма EmailMessage, HTML и вложения, шаблоны и безопасное хранение данных.
order: 7
duration: 45 мин
difficulty: intermediate
tags: smtplib, email, рассылки, шаблоны
---

Письма — один из самых живых способов взаимодействия с пользователем: подтверждения, уведомления, отчёты. Python умеет отправлять их из коробки, без сторонних сервисов, а шаблоны позволяют строить красивые письма, не смешивая код и HTML.

## Строим письмо

Современный способ — класс `EmailMessage` из модуля `email.message`:

```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Привет из Python"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Это текст письма.\nВторая строка.")
```

Заголовки задаются как в словаре, а `set_content` кладёт тело письма. Посмотреть, как выглядит готовое письмо, можно так:

```python
print(msg.as_string())
```

Вы увидите заголовки, пустую строку и тело — это ровно то, что уйдёт по протоколу SMTP.

## HTML-версия письма

Простой текст — база, но рассылки живут на HTML. В одно письмо можно положить обе версии: получатели, чей клиент не поддерживает HTML, увидят текст.

```python
msg.set_content("Посмотри наше предложение!")
msg.add_alternative(
    "<h1>Привет!</h1><p>Посмотри наше предложение.</p>",
    subtype="html",
)
```

`add_alternative` добавляет альтернативную часть: письмо становится мультичастным, и клиент выберет самую «богатую» поддерживаемую версию.

## Вложения

Файлы добавляются через `add_attachment`:

```python
msg.add_attachment(
    open("report.pdf", "rb").read(),
    maintype="application",
    subtype="pdf",
    filename="report.pdf",
)
```

Для картинок `maintype` — `image`, для архива — `application`/`zip`. Главное — передать байты, тип и имя файла.

## Отправка через smtplib

Теперь самое главное — передать письмо серверу:

```python
import smtplib

with smtplib.SMTP_SSL("smtp.example.com", 465) as server:
    server.login("noreply@example.com", "пароль")
    server.send_message(msg)
```

`smtplib.SMTP_SSL` подключается по защищённому каналу и принимает хост и порт. `login` аутентифицирует, `send_message` отправляет готовое письмо. Порты: 465 — сразу SSL, 587 — STARTTLS после `server.starttls()`.

## Шаблоны писем

Смешивать HTML и код — плохо. Шаблон выносится в отдельную строку, а значения подставляются в него:

```python
from string import Template

template = Template(
    """<p>Привет, $name!</p>
    <p>Твой заказ №$order подтверждён.</p>"""
)

html = template.substitute(name="Аня", order=12345)
```

Для серьёзных рассылок удобнее Jinja2 с циклами и условиями, но встроенный `string.Template` покрывает простые случаи без зависимостей.

## Безопасность

Никогда не пиши пароль в коде. Храни его в переменных окружения:

```python
import os

password = os.environ["SMTP_PASSWORD"]
```

`os.environ` упадёт с понятной ошибкой, если переменной нет — и пароль не попадёт в репозиторий.

## Рассылка по списку

```python
recipients = ["a@example.com", "b@example.com"]

for email in recipients:
    msg = EmailMessage()
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    msg["Subject"] = "Акция"
    msg.set_content("Скидка 20%!")
    server.send_message(msg)
```

Для каждой цели собирается своё письмо — так проще персонализировать и не раскрывать список адресов получателям.

## Итог

- `EmailMessage` собирает письмо: заголовки, текст, HTML, вложения.
- `smtplib.SMTP_SSL` отправляет; данные для входа — из окружения.
- Шаблоны отделяют HTML от кода.
- Рассылка по списку — цикл с персональным письмом для каждого адреса.

<!--TASK-->
### Задача 1
Собери простое письмо через `EmailMessage`: тема «Тест», отправитель `noreply@example.com`, получатель `user@example.com`, текст «Привет! Это тестовое письмо.» Выведи `msg.as_string()` и убедись, что в выводе есть все заголовки и тело письма.

### Задача 2
Собери письмо с двумя версиями: текстовой «Посмотри наше предложение!» и HTML-версией с заголовком `<h1>Привет!</h1>` и абзацем. Выведи `msg.get_content_type()` и `msg.is_multipart()` — должно быть `multipart/alternative` и `True`. Затем выведи `msg.as_string()` и найди обе части.

### Задача 3
Напиши функцию `attach_report(msg, filename)`, которая читает файл в байтах и добавляет его вложение с `maintype="application"`, `subtype="pdf"` и именем файла. Создай тестовый файл `report.pdf` (просто с каким-нибудь содержимым), собери письмо и добавь вложение. Проверь, что `len(msg.iter_attachments()) == 1` и что имя вложения совпадает.

### Задача 4
Напиши функцию `send_email(msg, smtp_host, smtp_port, user, password)`, которая отправляет письмо через `smtplib.SMTP_SSL`. Используй `with`-блок. Затем перепиши её так, чтобы хост, порт, логин и пароль читались из `os.environ` с именами `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, а значения по умолчанию для хоста и порта были `smtp.example.com` и `465`.

### Задача 5
Напиши функцию `send_campaign(template_text, recipients, **values)`, которая для каждого адреса из списка строит письмо: тема «Акция», тело — результат подстановки `$name` и `$order` из `values` в шаблон. Вместо реальной отправки функция должна печатать `Отправлено на <email>`, а для проверки — возвращать список адресов. Убедись, что разные получатели получают одинаковый текст, но в письме подставляются значения.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Заголовки задаются через `msg["Subject"] = ...` и так далее; тело — `msg.set_content("...")`. `msg.as_string()` возвращает всё письмо строкой, и `print(msg.as_string())` покажет его целиком.

### Подсказка 2
`add_alternative(html, subtype="html")` добавляет HTML-часть, `set_content` — текстовую. `msg.is_multipart()` вернёт `True`, если частей больше одной; `msg.get_content_type()` покажет тип мультичастного письма.

### Подсказка 3
Чтение файла: `data = open(filename, "rb").read()`. Добавление: `msg.add_attachment(data, maintype="application", subtype="pdf", filename=filename)`. Перебор вложений: `list(msg.iter_attachments())` — список кортежей с содержимым и заголовками.

### Подсказка 4
`smtplib.SMTP_SSL(smtp_host, smtp_port)` внутри `with`; `server.login(user, password)` затем `server.send_message(msg)`. Для перехода на окружение: `os.environ.get("SMTP_HOST", "smtp.example.com")` и `int(os.environ.get("SMTP_PORT", "465"))` — не забудь `import os`.

### Подсказка 5
Используй `string.Template(template_text).substitute(**values)` для тела; `EmailMessage` с заголовками `From` и `To`; возвращай список `recipients`. Для проверки просто вызывай функцию с фейковыми значениями — отправка не нужна.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Тест"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Привет! Это тестовое письмо.")

print(msg.as_string())
```

`EmailMessage` собирает письмо в правильном формате. Заголовки `Subject`, `From`, `To` хранятся как поля сообщения, тело — через `set_content`. `as_string()` сериализует всё в одну строку: сначала заголовки, затем пустая строка и тело. Это ровно тот формат, который понимает любой SMTP-сервер.

### Разбор 2
```python
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Предложение"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Посмотри наше предложение!")
msg.add_alternative(
    "<h1>Привет!</h1><p>Посмотри наше предложение.</p>",
    subtype="html",
)

print(msg.is_multipart())       # True
print(msg.get_content_type())   # multipart/alternative
print(msg.as_string())
```

`set_content` создаёт первую часть — текст; `add_alternative` добавляет вторую — HTML. Письмо становится `multipart/alternative`: клиент сам выберет самую богатую поддерживаемую версию. `as_string()` покажет обе части с заголовками `Content-Type: text/plain` и `Content-Type: text/html`.

### Разбор 3
```python
from email.message import EmailMessage

def attach_report(msg, filename):
    with open(filename, "rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype="application", subtype="pdf", filename=filename)

with open("report.pdf", "wb") as f:
    f.write(b"%PDF-1.4 fake content")

msg = EmailMessage()
msg["Subject"] = "Отчёт"
msg["From"] = "noreply@example.com"
msg["To"] = "user@example.com"
msg.set_content("Во вложении отчёт.")
attach_report(msg, "report.pdf")

attachments = list(msg.iter_attachments())
print(len(attachments))                              # 1
print(attachments[0][1]["Content-Disposition"])      # содержит filename=report.pdf
```

Вложение — это часть письма с `Content-Type: application/pdf` и заголовком `Content-Disposition`. `add_attachment` принимает байты, главный и подчинённый типы и имя файла. `iter_attachments()` возвращает части-вложения, по которым можно проверить, что файл действительно добавлен.

### Разбор 4
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

`smtplib.SMTP_SSL` устанавливает защищённое соединение; `login` аутентифицирует, `send_message` отправляет готовое письмо. Вторая версия берёт настройки из окружения: значения по умолчанию для хоста и порта, обязательные переменные для учётных данных. Так пароль не попадёт в исходный код и репозиторий.

### Разбор 5
```python
from string import Template
from email.message import EmailMessage

def send_campaign(template_text, recipients, **values):
    template = Template(template_text)
    for email in recipients:
        msg = EmailMessage()
        msg["Subject"] = "Акция"
        msg["From"] = "noreply@example.com"
        msg["To"] = email
        msg.set_content(template.substitute(**values))
        print(f"Отправлено на {email}")
    return recipients

template = "Привет, $name! Твой заказ №$order подтверждён."
result = send_campaign(template, ["a@example.com", "b@example.com"], name="Аня", order=123)
print(result)
```

`string.Template` подставляет значения из словаря в шаблон: `$name` и `$order` заменяются на «Аня» и «123». В цикле для каждого адреса собирается персональное письмо — так получатели не видят чужие адреса, а текст можно персонализировать. Функция возвращает список адресов, что позволяет проверить результат и переиспользовать её.
<!--/SOLUTION-->

<!--QUIZ-->
Какой класс собирает письмо в Python?
- smtplib.SMTP
- email.message.EmailMessage
- string.Template
- socket.socket
* Правильный ответ: email.message.EmailMessage
EmailMessage хранит заголовки и тело письма и умеет сериализовать их в as_string().

Как задать тему письма?
- msg["Subject"] = "..."
- msg.subject = "..."
- set_content("...")
- add_alternative("...")
* Правильный ответ: msg["Subject"] = "..."
Заголовки письма присваиваются как ключи словаря: Subject, From, To.

Что делает msg.as_string()?
- Отправляет письмо
- Возвращает письмо строкой в формате SMTP
- Добавляет вложение
- Шифрует письмо
* Правильный ответ: Возвращает письмо строкой в формате SMTP
as_string() сериализует письмо: заголовки, пустая строка, тело — готовый формат для отправки.

Зачем нужна add_alternative(html, subtype="html")?
- Чтобы заменить текст на HTML
- Чтобы добавить HTML-версию письма рядом с текстовой
- Чтобы прикрепить файл
- Чтобы задать тему
* Правильный ответ: Чтобы добавить HTML-версию письма рядом с текстовой
Письмо становится мультичастным: клиент выберет поддерживаемую версию.

Какой класс отправляет письмо по SMTP?
- SMTP_SSL из smtplib
- EmailMessage
- Template
- os.environ
* Правильный ответ: SMTP_SSL из smtplib
smtplib.SMTP_SSL подключается по защищённому каналу и отправляет письмо через send_message.

Что отправляет server.send_message(msg)?
- Только тело письма
- Готовое письмо целиком
- Только заголовки
- Файл-вложение
* Правильный ответ: Готовое письмо целиком
send_message принимает объект EmailMessage и отправляет его со всеми заголовками и частями.

Почему пароль не стоит хранить в коде?
- Он не будет работать
- Он попадёт в репозиторий и компрометирует учётную запись
- Код станет медленнее
- Письма будут падать в спам
* Правильный ответ: Он попадёт в репозиторий и компрометирует учётную запись
Секреты хранят в переменных окружения — код остаётся безопасным при публикации.

Что делает string.Template(t).substitute(**values)?
- Парсит HTML
- Подставляет значения в шаблон вместо $имя
- Отправляет письмо
- Создаёт EmailMessage
* Правильный ответ: Подставляет значения в шаблон вместо $имя
substitute заменяет плейсхолдеры вида $name на переданные значения.

Как добавить PDF-вложение к письму?
- msg.add_attachment(data, maintype="application", subtype="pdf", filename="f.pdf")
- msg.set_content(open("f.pdf").read())
- msg.attach_pdf("f.pdf")
- msg["Attachment"] = "f.pdf"
* Правильный ответ: msg.add_attachment(data, maintype="application", subtype="pdf", filename="f.pdf")
add_attachment принимает байты, типы и имя файла и формирует часть с правильными заголовками.

Какой протокол использует smtplib?
- HTTP
- SMTP
- FTP
- SSH
* Правильный ответ: SMTP
Простой протокол передачи почты (SMTP) — стандарт для отправки электронных писем.
<!--/QUIZ-->
