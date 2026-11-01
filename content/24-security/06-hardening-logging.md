---
title: Укрепление и логирование безопасности
summary: Список укрепления production-приложения: привилегии, лимиты, безопасные настройки — и правильное логирование без секретов, с ротацией и аудитом.
order: 6
duration: 45 мин
difficulty: advanced
tags: укрепление, логирование, аудит, ротация, фильтры, django
---

Последний барьер — сделать так, чтобы атаку было **дорого провести** и **невозможно скрыть**. Первое — укрепление (hardening), второе — логирование и мониторинг.

## Укрепление: проверочный список

Hardening — набор рутинных действий, которые резко повышают цену взлома.

1. **Наименьшие привилегии.** Сервис работает от пользователя без прав администратора; база данных — отдельный пользователь с правами только на свою схему. Файлы с секретами — права `0600` (только владелец).
2. **Минимизация зависимостей.** Меньше библиотек — меньше поверхность атаки. Обновляй и проводи аудит (урок 2).
3. **Лимиты.** Ограничивай размер ввода, количество запросов, длину сессии. Rate limiting ломает перебор паролей и DoS.
4. **Безопасные настройки Django.** Это часто включают по умолчанию:

```python
# settings.py
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
X_FRAME_OPTIONS = "DENY"
```

5. **Изоляция.** Docker без root, отдельный пользователь в контейнере, лимиты ресурсов. Сегментация сети не даёт SSRF/взлому одного сервиса утащить всё сразу.
6. **Секреты** — из окружения (урок 2).

## Логирование: что и как

Даже идеально укреплённая система может быть атакована — важно это **заметить**. OWASP A09: сбои логирования и мониторинга позволяют атаке остаться незамеченной. Правильные логи:

- **Никогда не пиши секреты.** Пароли, токены, cookies — маскируй или не логируй вовсе.
- **Структурированность.** Формат с временем, уровнем, регистром, request id.
- **Ротация** — файлы логов не должны расти бесконечно.
- **Аудит чувствительных действий** — вход, выход, смена пароля, удаление данных — в отдельный поток.

Пример настроенного логгера с ротацией и фильтром секретов:

```python
import logging
from logging.handlers import RotatingFileHandler

REDACTED = {"суперсекрет"}

class RedactFilter(logging.Filter):
    def filter(self, record):
        for secret in REDACTED:
            if secret in record.getMessage():
                record.msg = record.msg.replace(secret, "***")
        return True

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)
handler.addFilter(RedactFilter())
logger.addHandler(handler)

logger.info("Пользователь залогинился: токен суперсекрет")
```

`RotatingFileHandler` обрезает файл при достижении `maxBytes`, храня `backupCount` резервных копий — логи не съедают диск.

Ошибки нужно логировать с трейсбеком (`logger.exception`), но не `секреты в исключениях. Чувствительные действия — отдельный `audit logger` с колонками `время | пользователь | действие | результат`.

## Мониторинг

Логи бесполезны, если их никто не читает. Сбирай метрики (количество ошибок 4xx/5xx, время ответа), настраивай алерты на подозрительные паттерны: N неудачных логинов подряд, доступ к несуществующим URL, запросы с необычными IP. Централизация логов (ELK/Loki) позволяет искать по всем сервисам сразу.

## Итог урока

Укрепление снижает вероятность успешной атаки, логирование — увеличивает вероятность её обнаружения. Вместе они замыкают контур защиты: атака дорогая и заметная. Теперь закрепим практикой.

<!--TASK-->
### Задача 1
Настрой логгер `app_logger` уровня `INFO`, который пишет в файл `app.log` через `RotatingFileHandler` с `maxBytes=1_000_000` и `backupCount=5`, и форматтером `"%(asctime)s %(levelname)s %(message)s"`. Передай его в `logging.basicConfig(handlers=[handler])`. Затем запиши `logger.info("Приложение запущено")` и прочитай первые строки файла через `open("app.log", encoding="utf-8")` — выведи первые три строки. Убедись, что в выводе есть время, уровень `INFO` и сообщение.

### Задача 2
Создай класс `RedactFilter(logging.Filter)`, который в методе `filter(record)` заменяет все вхождения секретов из множества `SECRETS` в `record.msg` на `"***"` и возвращает `True`. Примени фильтр к логгеру и запиши `logger.info("Токен: секрет123")` с `SECRETS = {"секрет123"}` в файл. Затем прочитай файл и выведи строку — в ней должно быть `***`, а не `секрет123`.

### Задача 3
Создай `logging.LoggerAdapter` с именем `auth_logger`, который автоматически добавляет поле `user` во все сообщения. Для этого определи подкласс, который в `process(msg, kwargs)` добавляет `kwargs["extra"]["user"]` (значение из self.extra). Используй `LoggerAdapter(logger, {"user": "alice"})`, запиши `info("Попытка входа")`, и при чтении файла выведи строку — в ней должен встречаться `alice`. Если сложно с адаптером — можно использовать `logger.info("...", extra={"user": "alice"})`.

### Задача 4
Напиши функцию `ensure_private(path)`, которая проверяет и при необходимости исправляет права файла: если путь — файл, права должны быть `0o600`, если каталог — `0o700`. Используй `os.stat(path).st_mode & 0o777` для чтения текущих прав и `os.chmod(path, 0o600)` для исправления. Создай временный файл через `tempfile.NamedTemporaryFile(delete=False)`, вызови `ensure_private`, и выведи итоговые права в формате `oct(режим)`.

### Задача 5
Напиши функцию `log_audit(action, user, ok)`, которая пишет в отдельный файл `audit.log` строку формата `время | действие | пользователь | ok`. Используй `logging.getLogger("audit")` с `FileHandler("audit.log", encoding="utf-8")` и форматтером `"%(asctime)s | %(action)s | %(user)s | %(ok)s"`. Запиши три события: `("login", "alice", True)`, `("login", "bob", False)`, `("delete", "alice", True)`, затем прочитай файл и выведи его строки. Убедись, что каждая строка содержит четыре поля.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`logging.basicConfig(handlers=[handler])` с `level=logging.INFO`. `RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)`. Читай файл через `open("app.log", encoding="utf-8").readlines()[:3]`.
### Подсказка 2
`record.msg` — строка сообщения, `record.getMessage()` — с подстановкой аргументов. Заменяй через `str.replace`. Верни `True`. Не забудь `handler.addFilter(RedactFilter())`.
### Подсказка 3
Подкласс `logging.LoggerAdapter`: переопредели `process(self, msg, kwargs)`, там `kwargs["extra"] = dict(kwargs.get("extra", {}), user=self.extra["user"])` и верни `(msg, kwargs)`. Или проще: передавать `extra={"user": "alice"}` в каждый вызов.
### Подсказка 4
`os.stat(path).st_mode & 0o777` — текущий режим. Для каталога используй `os.path.isdir(path)`. `tempfile.NamedTemporaryFile(delete=False)` создаёт временный файл, путь — в `.name`.
### Подсказка 5
`logging.getLogger("audit")` — отдельный логгер со своим хендлером. В `Formatter` можно передать поля через `extra` в вызове: `logger.info("", extra={"action": action, "user": user, "ok": ok})`. Форматтер: `"%(asctime)s | %(action)s | %(user)s | %(ok)s"`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logging.basicConfig(handlers=[handler], level=logging.INFO)
logger = logging.getLogger("app")

logger.info("Приложение запущено")

for line in open("app.log", encoding="utf-8").readlines()[:3]:
    print(line, end="")
```

Результат (пример):

```
2026-11-01 12:00:00,123 INFO Приложение запущено
```

Что здесь происходит? `RotatingFileHandler` при достижении `maxBytes` (1 МБ) переименовывает старый файл в `app.log.1`, `app.log.2` и так далее, оставляя не более `backupCount=5` копий. Форматтер добавляет время, уровень и сообщение. `basicConfig(handlers=[handler])` применяет хендлер к корневому логгеру, `getLogger("app")` его наследует. Ротация обязательна на проде: без неё лог-файл растёт бесконечно и занимает весь диск — а это уже отказ в обслуживании.

### Разбор 2
Решение:

```python
import logging
from logging.handlers import RotatingFileHandler

SECRETS = {"секрет123"}

class RedactFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        for secret in SECRETS:
            msg = msg.replace(secret, "***")
        record.msg = msg
        return True

handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)
handler.addFilter(RedactFilter())
logging.basicConfig(handlers=[handler], level=logging.INFO)
logger = logging.getLogger("app")

logger.info("Токен: секрет123")

for line in open("app.log", encoding="utf-8").readlines()[:3]:
    print(line, end="")
```

Результат (пример):

```
2026-11-01 12:01:00,123 INFO Токен: ***
```

Что здесь происходит? `logging.Filter` с методом `filter(record)` возвращает `True`, если запись нужно сохранить, и может изменить сам `record`. Мы берём сообщение через `record.getMessage()` (он подставляет аргументы в формат-строку), заменяем найденные секреты на `***` и записываем обратно в `record.msg`. Хендлер с фильтром добавляется через `addFilter`. Так секрет не попадает в файл лога — даже если программист забыл его замаскировать вручную. Это обязательная практика: логи читают не только свои, а лог-файлы любят попадать в тикеты и на форумы.

### Разбор 3
Решение:

```python
import logging
from logging.handlers import RotatingFileHandler

class UserAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        kwargs["extra"] = dict(kwargs.get("extra", {}), user=self.extra["user"])
        return msg, kwargs

handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=5)
handler.setFormatter(logging.Formatter("%(asctime)s %(user)s %(message)s"))
logging.basicConfig(handlers=[handler], level=logging.INFO)
logger = UserAdapter(logging.getLogger("auth"), {"user": "alice"})

logger.info("Попытка входа")

for line in open("app.log", encoding="utf-8").readlines()[:3]:
    print(line, end="")
```

Результат (пример):

```
2026-11-01 12:02:00,123 alice Попытка входа
```

Что здесь происходит? `LoggerAdapter` оборачивает логгер и позволяет добавлять контекст во все сообщения. Метод `process` вызывается для каждого сообщения; мы вкладываем `user` из `self.extra` в `kwargs["extra"]`, а форматтер подставляет его в строку через `%(user)s`. Так все действия конкретного пользователя связываются в единую цепочку логов. В реальных системах вместо имени пользователя часто используют `request_id` — сквозной идентификатор запроса, по которому можно собрать все логи одной операции во всех сервисах.

### Разбор 4
Решение:

```python
import os
import tempfile

def ensure_private(path):
    mode = os.stat(path).st_mode & 0o777
    if os.path.isdir(path):
        if mode != 0o700:
            os.chmod(path, 0o700)
    else:
        if mode != 0o600:
            os.chmod(path, 0o600)
    return os.stat(path).st_mode & 0o777

with tempfile.NamedTemporaryFile(delete=False) as tmp:
    path = tmp.name

print(oct(ensure_private(path)))
os.unlink(path)
```

Результат (пример):

```
0o600
```

Что здесь происходит? `os.stat(path).st_mode & 0o777` извлекает биты прав из полного режима. Для файла ожидаем `0o600` (чтение/запись только владельцу), для каталога — `0o700` (ещё и вход). Если права не те — `os.chmod` исправляет их. Такая функция нужна, когда приложение при старте создаёт файлы с секретами или конфигурацией: умолчальные права могут дать чтение другим пользователям системы. На Windows chmod работает ограниченно, но на Linux-проде это стандартная мера. После проверки временный файл удаляется через `os.unlink`.

### Разбор 5
Решение:

```python
import logging

audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler("audit.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s | %(action)s | %(user)s | %(ok)s"))
audit_logger.addHandler(handler)

def log_audit(action, user, ok):
    audit_logger.info("", extra={"action": action, "user": user, "ok": ok})

log_audit("login", "alice", True)
log_audit("login", "bob", False)
log_audit("delete", "alice", True)

for line in open("audit.log", encoding="utf-8").readlines():
    print(line, end="")
```

Результат (пример):

```
2026-11-01 12:03:00,123 | login | alice | True
2026-11-01 12:03:01,456 | login | bob | False
2026-11-01 12:03:02,789 | delete | alice | True
```

Что здесь происходит? Отдельный логгер `audit` пишет в собственный файл `audit.log` — так события безопасности не смешиваются с потоком обычных сообщений. Поля `action`, `user`, `ok` передаются через `extra`, а форматтер расставляет их в строку. Важно: аудит-лог должен быть **append-only** — его нельзя позволить чистить приложению, а доступ на запись лучше ограничить. Благодаря такому логу расследование инцидента превращается в простой запрос: «кто и когда менял/удалял/входил и было ли это успешно». Этого требует и OWASP A09: без логов атаку невозможно заметить.
<!--/SOLUTION-->

<!--QUIZ-->
Что означает «наименьшие привилегии»?
- Каждый сервис имеет ровно столько прав, сколько нужно
- Всем дать root-доступ
- Запретить всё
* Правильный ответ: Каждый сервис имеет ровно столько прав, сколько нужно
Лишние права увеличивают ущерб от взлома.

Какие права должны быть у файла с секретом на Linux?
- 0600
- 0666
- 0777
* Правильный ответ: 0600
Чтение и запись только для владельца.

Что делает RotatingFileHandler?
- Обрезает лог-файл при достижении размера и хранит резервные копии
- Шифрует логи
- Удаляет старые логи
* Правильный ответ: Обрезает лог-файл при достижении размера и хранит резервные копии
maxBytes и backupCount ограничивают суммарный объём логов.

Зачем нужен фильтр для маскировки секретов в логах?
- Чтобы секреты не попадали в файлы логов
- Чтобы логи были короче
- Чтобы ускорить запись
* Правильный ответ: Чтобы секреты не попадали в файлы логов
Логи часто копируют в тикеты и на форумы — секреты там недопустимы.

Что делает LoggerAdapter?
- Добавляет контекст (например, пользователя) во все сообщения логгера
- Создаёт новый файл лога
- Шифрует сообщения
* Правильный ответ: Добавляет контекст (например, пользователя) во все сообщения логгера
process() расширяет kwargs["extra"] и форматтер подставляет значения.

Что такое audit-лог?
- Отдельный лог чувствительных действий: вход, удаление, смена прав
- Копия всех логов приложения
- Лог только ошибок
* Правильный ответ: Отдельный лог чувствительных действий: вход, удаление, смена прав
Он помогает расследовать инциденты.

Какой параметр Django отключает режим отладки в проде?
- DEBUG = False
- DEBUG = True
- ALLOWED_HOSTS = []
* Правильный ответ: DEBUG = False
Отладка раскрывает стектрейсы и внутренности приложения.

Что такое HSTS (HTTP Strict Transport Security)?
- Запрет на переход по незашифрованному HTTP
- Запрет на редиректы
- Способ кэширования
* Правильный ответ: Запрет на переход по незашифрованному HTTP
SECURE_HSTS_SECONDS заставляет браузеры ходить только по HTTPS.

Зачем нужны лимиты и rate limiting?
- Чтобы замедлить перебор паролей и смягчить DoS
- Чтобы ускорить сервер
- Чтобы скрыть ошибки
* Правильный ответ: Чтобы замедлить перебор паролей и смягчить DoS
Ограничение частоты запросов — стандартная защита.

Какой класс OWASP описывает отсутствие логирования атак?
- A09 — Сбои логирования и мониторинга
- A01 — Контроль доступа
- A06 — Устаревшие компоненты
* Правильный ответ: A09 — Сбои логирования и мониторинга
Без логов и мониторинга атаку нельзя обнаружить.
<!--/QUIZ-->
