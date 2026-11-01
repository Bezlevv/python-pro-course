---
title: Мониторинг сайтов и уведомления
summary: Напишем скрипт, который регулярно проверяет доступность сайтов через requests и присылает письмо на почту через smtplib при проблемах.
order: 5
duration: 30 мин
difficulty: intermediate
tags: requests, smtplib, мониторинг, почта
---

Представь: ты администрируешь сайт, и о том, что он лёг, узнаёшь от пользователей. Недостойно. Правильный подход — мониторинг: программа сама проверяет сайт каждые несколько минут и пишет тебе, если что-то не так. Разберём два кирпича этой системы: HTTP-запросы (`requests`) и электронную почту (`smtplib`).

## Проверяем доступность

HTTP-статус отвечает, всё ли в порядке с сайтом. 200 — отлично, 404 — страница не найдена, 500 — ошибка на сервере:

```python
import requests

r = requests.get("https://example.com")
print(r.status_code)                     # 200
print(r.elapsed.total_seconds())         # время ответа в секундах
```

Плохая идея — ждать ответа бесконечно. Поэтому всегда указывай `timeout`:

```python
try:
    r = requests.get("https://example.com", timeout=5)
    r.raise_for_status()   # бросит исключение при коде 4xx/5xx
    print("Сайт жив, время:", round(r.elapsed.total_seconds(), 2), "с")
except requests.exceptions.RequestException as e:
    print("Проблемы:", e)
```

`raise_for_status()` превращает плохой статус в исключение — и код успеха и неудачи становится единообразным.

## Отправляем письмо

За отправку почты отвечает стандартный модуль `smtplib`. Любая почта работает одинаково: подключаемся к SMTP-серверу, переходим на защищённое соединение (STARTTLS), логинимся и отправляем письмо:

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
        server.login("monitor@example.com", "ПАРОЛЬ")
        server.send_message(msg)
```

SMTP-сервер, логин и пароль ты получишь у своей почтовой службы (например, для Gmail: `smtp.gmail.com`, порт 587). Никогда не вписывай пароль прямо в код — храни его в переменной окружения.

## Мониторинг-цикл

Теперь соединяем обе части: проверка + уведомление. Бесконечный цикл с паузой:

```python
import time

while True:
    try:
        r = requests.get("https://example.com", timeout=5)
        r.raise_for_status()
        print(time.asctime(), "OK")
    except requests.exceptions.RequestException as e:
        send_alert("Сайт недоступен!", str(e))
        print("Сайт недоступен!")
    time.sleep(60)
```

Главная идея — цикл с `time.sleep`, который и составляет суть любого мониторинга. В задачах мы доведём эту схему до ума: добавим список сайтов и будем слать письмо только при смене состояния.

<!--TASK-->
### Задача 1
Проверь сайт `https://example.com` через `requests.get` и выведи статус и время ответа в секундах. Используй `r.status_code` и `r.elapsed.total_seconds()`. Ожидаемый результат: строки вида `Статус: 200` и `Время ответа: 0.43 с`.

### Задача 2
Сделай проверку безопасной: добавь `timeout=5` и оберни запрос в `try`/`except requests.exceptions.RequestException`. При ошибке печатай `Сайт недоступен: <описание>`. Проверь на заведомо недоступном адресе, например `https://nonexistent-domain-12345.ru`. Ожидаемый результат: для живого сайта — статус, для несуществующего — аккуратное сообщение без падения программы.

### Задача 3
Напиши программу, которая проверяет несколько сайтов: список URL в переменной `urls`, цикл по нему, для каждого — статус или текст ошибки. Ожидаемый результат: для каждого сайта строка вида `https://example.com: 200` или `https://broken.example: ошибка соединения`.

### Задача 4
Напиши функцию `send_alert(subject, body)`, которая отправляет письмо через `smtplib`: `MIMEText`, заголовки Subject/From/To, `SMTP(host, 587)`, `starttls()`, `login()`, `send_message(msg)`. Пароль бери из переменной окружения `MAIL_PASSWORD` (модуль `os`). Вызови её с тестовым сообщением. Ожидаемый результат: письмо приходит на указанный ящик (или программа сообщает об ошибке подключения, если SMTP-сервер не настроен).

### Задача 5
Собери полный монитор: каждые 60 секунд проверяй `https://example.com` через `requests.get(URL, timeout=5)`, печатай лог `OK` или `FAIL`, а письмо через `send_alert` отправляй только при переходе из «работает» в «недоступен» (то есть не повторяй письмо каждую минуту, пока сайт лежит). Используй `time.sleep(60)` и булеву переменную состояния. Ожидаемый результат: в консоли лог раз в минуту, письмо уходит только один раз на начало сбоя.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`r = requests.get("https://example.com")` — дальше печатай `r.status_code` и `round(r.elapsed.total_seconds(), 2)`. Не забудь `import requests`. Если под рукой нет интернета, подставь `https://httpbin.org/status/200`.

### Подсказка 2
Держи обращение к сети только внутри `try`, а в `except requests.exceptions.RequestException as e` печатай `f"Сайт недоступен: {e}"`. `raise_for_status()` добавляй после `requests.get`, чтобы код 404/500 тоже считался проблемой.

### Подсказка 3
`for url in urls:` — внутри тот же `try`/`except`, но `print(url, "-", r.status_code)` в успехе и `print(url, "- ошибка:", e)` в ошибке. `urls` объяви списком до цикла.

### Подсказка 4
Скелет: `msg = MIMEText(body, "plain", "utf-8")`; заполни `msg["Subject"]`, `msg["From"]`, `msg["To"]`; затем `with smtplib.SMTP("smtp.example.com", 587) as server:` → `server.starttls()` → `server.login("monitor@example.com", os.environ["MAIL_PASSWORD"])` → `server.send_message(msg)`. Импортируй `os`, `smtplib`, `MIMEText`.

### Подсказка 5
Создай `was_down = False` до цикла. В успехе ставь `was_down = False` и печатай `OK`. В `except`: если `not was_down` — вызывай `send_alert(...)`, затем `was_down = True`. Паузу ставь в конце цикла. Так письмо уйдёт один раз, а не каждую минуту.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import requests

r = requests.get("https://example.com")
print("Статус:", r.status_code)
print("Время ответа:", round(r.elapsed.total_seconds(), 2), "с")
```

Результат (пример):

```
Статус: 200
Время ответа: 0.43 с
```

Что здесь происходит? `requests.get` выполняет GET-запрос и возвращает объект `Response`. Его атрибут `status_code` — HTTP-статус, `elapsed` — длительность запроса (объект `timedelta`), а `total_seconds()` переводит её в секунды. `round(..., 2)` округляет до двух знаков, чтобы вывод не содержал длинных хвостов. Такой пары чисел достаточно, чтобы понять, что сайт жив и отвечает быстро.

### Разбор 2
Решение:

```python
import requests

url = "https://example.com"
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    print("Статус:", r.status_code)
except requests.exceptions.RequestException as e:
    print("Сайт недоступен:", e)
```

Результат (пример для недоступного адреса):

```
Сайт недоступен: HTTPConnectionPool(host='nonexistent-domain-12345.ru', port=80): Max retries exceeded with url: ...
```

Что здесь происходит? `timeout=5` заставляет `requests` отказаться от запроса, если ответ не пришёл за 5 секунд, — иначе скрипт мог бы висеть минутами. `raise_for_status()` бросает исключение при статусе 4xx/5xx, поэтому код 500 тоже попадёт в `except`. `requests.exceptions.RequestException` — родительский класс всех сетевых ошибок библиотеки, он ловит и таймауты, и проблемы соединения, и плохие статусы. Программа никогда не упадёт с трейсбеком.

### Разбор 3
Решение:

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
        print(url, "- ошибка:", e)
```

Результат (пример):

```
https://example.com - 200
https://httpbin.org/status/200 - 200
https://nonexistent-domain-12345.ru - ошибка: ...
```

Что здесь происходит? Мы вынесли проверку в цикл: для каждого адреса из списка выполняется один и тот же код. Это классический приём: данные — в список, логика — один раз. Даже если один сайт упадёт, `except` перехватит ошибку, и цикл продолжит работу со следующим адресом. Такой список легко расширять: добавил строку — и сайт под наблюдением.

### Разбор 4
Решение:

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

send_alert("Тест", "Это тестовое письмо из мониторинга.")
print("Письмо отправлено")
```

Что здесь происходит? `MIMEText` строит письмо в формате MIME: тело, тип `plain`, кодировка UTF-8 (важно для кириллицы). Заголовки заполняются как у словаря. `SMTP("smtp.example.com", 587)` открывает соединение с сервером, `starttls()` переводит его на шифрование — без этого логин и текст письма летели бы открытым текстом. `login()` принимает логин и пароль из переменной окружения: так секрет не попадает в код и в систему контроля версий. `send_message(msg)` отправляет готовое письмо. Контекстный менеджер `with` сам закрывает соединение.

### Разбор 5
Решение:

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
            send_alert("Сайт недоступен!", str(e))
        was_down = True
    time.sleep(60)
```

Что здесь происходит? Переменная `was_down` хранит предыдущее состояние сайта. Пока сайт жив (ветка `try`), она сбрасывается в `False`. Как только происходит сбой, мы проверяем: если раньше был `False` — это начало сбоя, отправляем письмо и ставим `True`. На следующей минуте сайт всё ещё лежит, но `was_down` уже `True`, поэтому письмо не дублируется. Когда сайт оживёт, `was_down` снова станет `False`, и следующий сбой будет снова «первым». `time.asctime()` добавляет метку времени в лог. Так выглядит настоящий, продуманный мониторинг.
<!--/SOLUTION-->

<!--QUIZ-->
Что означает HTTP-статус 200?
- Страница не найдена
- Запрос успешен
- Ошибка на сервере
- Требуется авторизация
* Правильный ответ: Запрос успешен
200 — сайт доступен и ответил корректно.

Зачем в requests.get указывать timeout?
- Чтобы увеличить скорость
- Чтобы не ждать ответ вечно
- Чтобы добавить заголовки
- Чтобы сменить метод
* Правильный ответ: Чтобы не ждать ответ вечно
timeout ограничивает время ожидания: при превышении запрос прерывается исключением.

Что делает raise_for_status()?
- Возвращает статус-код
- Бросает исключение при статусе 4xx/5xx
- Меняет метод запроса
- Повторяет запрос
* Правильный ответ: Бросает исключение при статусе 4xx/5xx
Благодаря ей код 404 или 500 тоже считается ошибкой и обрабатывается в except.

Какой стандартный модуль отправляет электронную почту?
- emails
- mailer
- smtplib
- sendmail
* Правильный ответ: smtplib
smtplib работает с SMTP-серверами: подключение, логин, отправка.

Зачем вызывать starttls()?
- Чтобы ускорить соединение
- Чтобы зашифровать соединение
- Чтобы проверить почту
- Чтобы избежать спама
* Правильный ответ: Чтобы зашифровать соединение
STARTTLS переводит соединение на шифрование — логин и письмо не видны посторонним.

Что делает time.sleep(60) в мониторинге?
- Ускоряет проверку
- Ставит паузу 60 секунд между проверками
- Выводит время
- Завершает программу
* Правильный ответ: Ставит паузу 60 секунд между проверками
Пауза задаёт периодичность проверки: раз в минуту, а не безостановочно.
<!--/QUIZ-->
