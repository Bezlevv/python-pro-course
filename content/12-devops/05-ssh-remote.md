---
title: Удалённое управление: SSH и paramiko
summary: Как выполнять команды на удалённых серверах по SSH из Python и копировать файлы через SFTP с помощью библиотеки paramiko.
order: 5
duration: 40 мин
difficulty: advanced
tags: SSH, paramiko, SFTP, серверы, удалённое управление
---

## Зачем Python умеет ходить по SSH

Разработчики и DevOps-инженеры постоянно работают с удалёнными серверами: обновить код, перезапустить сервис, посмотреть логи, собрать статистику. Вручную это делается через терминал и SSH. Но когда серверов десятки, а команды повторяются, SSH-сессии автоматизируют из Python.

Библиотека **paramiko** — это реализация протокола SSH на чистом Python. Она позволяет подключаться к серверам, выполнять команды и работать с файлами через SFTP. Устанавливается как `pip install paramiko`.

## Подключение и простая команда

Минимальный пример: подключиться и выполнить `uname -a` (информация о системе):

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password="secret")

stdin, stdout, stderr = client.exec_command("uname -a")
print(stdout.read().decode())
client.close()
```

Разберём по шагам. `SSHClient()` создаёт клиент. `set_missing_host_key_policy(paramiko.AutoAddPolicy())` автоматически добавляет неизвестные ключи хостов — удобно для скриптов, но в проде лучше сверять ключи с `RejectPolicy` (по умолчанию) и заранее прописывать известные. `connect` открывает соединение. `exec_command` выполняет команду и возвращает три потока: stdin, stdout, stderr. `stdout.read()` читает весь вывод, а `.decode()` превращает байты в строку. В конце обязательно `close()`.

## Чтение ошибок

Команда может завершиться с ошибкой. Полезно проверять код возврата:

```python
stdin, stdout, stderr = client.exec_command("ls /nonexistent")
exit_status = stdout.channel.recv_exit_status()
print("Код возврата:", exit_status)
print("Ошибка:", stderr.read().decode())
```

`stdout.channel.recv_exit_status()` ждёт завершения команды и возвращает её код возврата. Так мы отличаем успех (0) от ошибки.

## Работа с файлами: SFTP

SFTP — это подпротокол SSH для передачи файлов. Через paramiko он получается из того же соединения:

```python
sftp = client.open_sftp()
sftp.get("/var/log/app.log", "app_local.log")   # скачать
sftp.put("config.yaml", "/srv/app/config.yaml")  # загрузить
sftp.close()
```

`get` скачивает файл с сервера, `put` — загружает на сервер. Объект `sftp` также умеет `listdir`, `stat`, `mkdir`, `remove` — почти всё, что умеет обычный файловый менеджер.

## Обработка ошибок подключения

Сеть ненадёжна: сервер может быть недоступен, пароль — неверным. Обязательно оборачивай подключение в `try/except`:

```python
try:
    client.connect(host, port=22, username=user, password=pwd, timeout=10)
except paramiko.AuthenticationException:
    print("Не удалось аутентифицироваться")
except paramiko.SSHException as e:
    print("Ошибка SSH:", e)
except TimeoutError:
    print("Таймаут подключения")
```

`AuthenticationException` — неверный логин или пароль, `SSHException` — прочие проблемы протокола, `TimeoutError` — сервер не отвечает. Хороший скрипт всегда сообщает, что именно пошло не так.

## Безопасность

Пароли в коде — плохая практика: их увидят все, у кого есть доступ к репозиторию. Лучше используй SSH-ключи (параметр `key_filename`), переменные окружения или менеджеры секретов. В примерах ниже для простоты мы используем пароль из переменной, но в проде — ключи.

## Путь одной команды

Любая автоматизация по SSH раскладывается на один и тот же набор шагов — от соединения до закрытия канала.

```mermaid
flowchart LR
    A["Скрипт"] --> B["SSHClient.connect"]
    B --> C["exec_command"]
    C --> D["stdout и код возврата"]
    D --> E["open_sftp"]
    E --> F["get или put"]
    F --> G["close"]
```

## Итог

Мы научились подключаться по SSH, выполнять команды, читать их вывод и ошибки, а также передавать файлы через SFTP. Это фундамент для скриптов деплоя и администрирования. Теперь задачи.

<!--TASK-->
### Задача 1
Напиши скрипт `ssh_uptime.py`, который подключается к серверу (следующие адрес `192.168.1.50`, пользователь `deploy`, пароль `secret`) и выполняет команду `uptime`. Выведи вывод команды на экран. Используй `SSHClient`, `AutoAddPolicy` и `exec_command`. Не забудь закрыть соединение через `client.close()` в самом конце.

### Задача 2
Создай скрипт `ssh_status.py`, который выполняет на сервере команду `service nginx status` и выводит и вывод, и код возврата (через `stdout.channel.recv_exit_status()`). Если код возврата не равен нулю, выведи дополнительно сообщение `Сервис не работает!`. Проверь поведение на заведомо отсутствующем сервисе (например, `service ghost-service status`), чтобы увидеть ненулевой код.

### Задача 3
Напиши скрипт `sftp_download.py`, который скачивает с сервера файл `/var/log/app.log` в локальный файл `app.log` через `sftp.get()`. Перед скачиванием выведи размер удалённого файла через `sftp.stat("/var/log/app.log").st_size`. Оберни подключение в `try/except`, перехватывая `paramiko.AuthenticationException`, `paramiko.SSHException` и `TimeoutError`.

### Задача 4
Создай скрипт `sftp_upload.py`, который загружает локальный файл `backup.tar.gz` на сервер в путь `/srv/backups/backup.tar.gz` через `sftp.put()`. Перед загрузкой создай удалённую папку `/srv/backups`, если её нет: проверь через `try: sftp.stat(...)` и создай через `sftp.mkdir(...)`, перехватив `FileNotFoundError`.

### Задача 5
Напиши скрипт `multi_host.py`, который выполняет команду `hostname` на трёх серверах из списка `[("192.168.1.50", "deploy", "secret"), ("192.168.1.51", "deploy", "secret"), ("192.168.1.52", "deploy", "secret")]` и выводит для каждого: адрес и результат команды. Если подключение к какому-то серверу не удалось — выведи `Не удалось подключиться к <адрес>`, но продолжи работу с остальными. Используй цикл и `try/except` вокруг подключения.

### Задача 6
Напиши функцию `disk_usage(client, threshold=80)`, которая выполняет на сервере команду `df -h /`, читает stdout и разбирает вывод. Найди процент использования регулярным выражением `(\d+)%`, верни кортеж `(percent, status)`, где `status` — `"ALERT"`, если процент больше или равен порогу, иначе `"OK"`. Если вывод пуст или процент не найден — верни `(None, "UNKNOWN")`. Проверь функцию на клиенте-заглушке: класс с методом `exec_command`, возвращающим подготовленный вывод через `io.BytesIO`. Так тест не зависит от живого сервера. Ожидаемый вывод для строки `78% /` при пороге 80: `(78, 'OK')`, а при пороге 75 — `(78, 'ALERT')`.

### Задача 7
Напиши скрипт `sync_conf.py`, который копирует все файлы `*.conf` из локального каталога `conf/` в `/etc/app/conf/` на сервере. Для каждого файла сравни размер с удалённым (`sftp.stat(remote).st_size`): если размеры совпадают — пропусти файл, иначе загрузи через `sftp.put`. Если удалённый каталог отсутствует (при `stat` летит `FileNotFoundError`) — создай его через `sftp.mkdir`. В конце выведи `Загружено: N, пропущено: M`. Прогони скрипт дважды: первый раз должны загрузиться все три файла, второй — ни одного. Ожидаемый вывод: `Загружено: 3, пропущено: 0`, затем `Загружено: 0, пропущено: 3`.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай клиент: `client = paramiko.SSHClient()`, затем `client.set_missing_host_key_policy(paramiko.AutoAddPolicy())`. Подключение: `client.connect("192.168.1.50", username="deploy", password="secret")`. Вывод: `print(stdout.read().decode())`.

### Подсказка 2
После `exec_command` жди завершения: `exit_status = stdout.channel.recv_exit_status()`. Затем сравни `if exit_status != 0:`. Не забудь прочитать stderr — там обычно причина ошибки.

### Подсказка 3
SFTP-сессия: `sftp = client.open_sftp()`. Размер файла: `sftp.stat(path).st_size`. Скачивание: `sftp.get(remote, local)`. Закрывай и `sftp`, и `client`. `TimeoutError` — встроенное исключение, его не нужно импортировать.

### Подсказка 4
Проверяй существование папки: `try: sftp.stat("/srv/backups") except FileNotFoundError: sftp.mkdir("/srv/backups")`. Затем `sftp.put("backup.tar.gz", "/srv/backups/backup.tar.gz")`.

### Подсказка 5
В цикле `for host, user, pwd in hosts:` оборачивай `connect` в `try/except Exception as e:` — внутри `except` печатай сообщение и продолжай через `continue`. Успешное выполнение — печать результата. После каждого сервера закрывай клиент.

### Подсказка 6
Заглушка должна повторять только тот кусок API, который использует функция: `def exec_command(self, cmd): return None, io.BytesIO(self.output.encode()), io.BytesIO(b"")`. В самой функции читай `stdout.read().decode()`, ищи `re.search(r"(\d+)%", output)` и проверяй `if not m`. Порог сравнивай нестрого: `percent >= threshold`, иначе ровно 80% при пороге 80 останется без тревоги, а это уже повод смотреть на диск.

### Подсказка 7
Разделяй две проверки: `sftp.stat(REMOTE_DIR)` для каталога и `sftp.stat(remote)` для каждого файла — во втором случае `FileNotFoundError` означает «файла ещё нет», а не ошибку. Размер локального файла — `local.stat().st_size`. Счётчики увеличивай в ветках `continue` и после `put`. Не забудь закрыть `sftp`, а потом `client`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password="secret")

stdin, stdout, stderr = client.exec_command("uptime")
print(stdout.read().decode())

client.close()
```

Вывод (пример):

```
 10:45:02 up 42 days,  3:20,  1 user,  load average: 0.08, 0.12, 0.15
```

Что здесь происходит? `SSHClient` — это менеджер соединения. `set_missing_host_key_policy(AutoAddPolicy())` говорит: если хост неизвестен, добавь его ключ автоматически — это избавляет от необходимости прописывать каждый сервер вручную (в проде лучше `RejectPolicy` с явным списком известных ключей). `exec_command` не ждёт завершения команды сам по себе — он лишь запускает её в канале, поэтому мы читаем `stdout.read()`, который блокирует выполнение, пока команда не закончится. `.decode()` превращает байты в строку. `close()` закрывает соединение — это важно, иначе в скрипте возникнут «висящие» соединения.

### Разбор 2
Решение:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password="secret")

stdin, stdout, stderr = client.exec_command("service nginx status")
exit_status = stdout.channel.recv_exit_status()

print("Вывод:", stdout.read().decode())
print("Код возврата:", exit_status)
if exit_status != 0:
    print("Ошибка:", stderr.read().decode())
    print("Сервис не работает!")

client.close()
```

Что здесь происходит? Команда `service ... status` возвращает 0, если сервис запущен, и ненулевой код иначе. `recv_exit_status()` блокирует выполнение до завершения команды и возвращает её код возврата — это аналог `$?` в bash. Дальше мы проверяем код и, если он не ноль, печатаем stderr и сообщение. Важно: stdout и stderr нужно читать после `recv_exit_status`, либо до него — оба варианта работают, но изменение порядка может повлиять на то, сколько данных буферизовано. Для коротких команд вывод читается целиком.

### Разбор 3
Решение:

```python
import paramiko

REMOTE = "/var/log/app.log"
LOCAL = "app.log"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect("192.168.1.50", username="deploy", password="secret", timeout=10)
    sftp = client.open_sftp()
    size = sftp.stat(REMOTE).st_size
    print(f"Размер удалённого файла: {size} байт")
    sftp.get(REMOTE, LOCAL)
    print(f"Скачано в {LOCAL}")
    sftp.close()
except paramiko.AuthenticationException:
    print("Не удалось аутентифицироваться")
except paramiko.SSHException as e:
    print("Ошибка SSH:", e)
except TimeoutError:
    print("Таймаут подключения")
finally:
    client.close()
```

Что здесь происходит? `timeout=10` ограничивает ожидание подключения 10 секундами. `sftp.stat(REMOTE).st_size` даёт размер файла на сервере без скачивания. `sftp.get` выполняет передачу. Блок `except` перехватывает три характерные ошибки: неверные учётные данные, любые ошибки протокола и таймаут. `finally` гарантирует, что соединение закроется даже при ошибке. Такой шаблон — стандарт для скриптов, работающих с сетью: сеть ненадёжна, и программа не должна падать с невнятным трейсбеком.

### Разбор 4
Решение:

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.1.50", username="deploy", password="secret")

sftp = client.open_sftp()
try:
    sftp.stat("/srv/backups")
except FileNotFoundError:
    sftp.mkdir("/srv/backups")
    print("Создана папка /srv/backups")

sftp.put("backup.tar.gz", "/srv/backups/backup.tar.gz")
print("Файл загружен")
sftp.close()
client.close()
```

Что здесь происходит? `sftp.stat` проверяет существование удалённой папки: если её нет, paramiko бросает `FileNotFoundError` (то же исключение, что и в Python при работе с локальными файлами — это удобно). Мы перехватываем его и создаём папку через `sftp.mkdir`. Затем `sftp.put` загружает локальный файл на сервер. Обрати внимание на порядок закрытия: сначала `sftp`, потом `client`. В проде вместо жёстко заданного пароля лучше передавать `key_filename="/home/deploy/.ssh/id_ed25519"` — тогда не придётся хранить пароль в коде.

### Разбор 5
Решение:

```python
import paramiko

hosts = [
    ("192.168.1.50", "deploy", "secret"),
    ("192.168.1.51", "deploy", "secret"),
    ("192.168.1.52", "deploy", "secret"),
]

for host, user, pwd in hosts:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=pwd, timeout=5)
        stdin, stdout, stderr = client.exec_command("hostname")
        print(f"{host}: {stdout.read().decode().strip()}")
    except Exception as e:
        print(f"Не удалось подключиться к {host}: {e}")
    finally:
        client.close()
```

Вывод (пример):

```
192.168.1.50: web-01
192.168.1.51: web-02
192.168.1.52: db-01
```

Что здесь происходит? Список `hosts` — это кортежи «адрес, логин, пароль». Цикл идёт по всем серверам: для каждого создаём отдельного клиента (важно — соединения нельзя переиспользовать между разными хостами). `try/except Exception` ловит любую ошибку подключения (недоступный хост, неверный пароль) и печатает адрес с причиной, не останавливая весь скрипт. `finally` закрывает клиента в любом случае. Такой скрипт — основа «обхода» флота серверов: можно добавить сюда любую команду и получить отчёт по всем машинам.

### Разбор 6
Решение:

```python
import io
import re

def disk_usage(client, threshold=80):
    stdin, stdout, stderr = client.exec_command("df -h /")
    output = stdout.read().decode()
    m = re.search(r"(\d+)%", output)
    if not m:
        return (None, "UNKNOWN")
    percent = int(m.group(1))
    status = "ALERT" if percent >= threshold else "OK"
    return (percent, status)

class FakeClient:
    """Заглушка: отдаёт заранее подготовленный вывод команды."""
    def __init__(self, output):
        self.output = output

    def exec_command(self, cmd):
        return None, io.BytesIO(self.output.encode()), io.BytesIO(b"")

df_output = (
    "Filesystem      Size  Used Avail Use% Mounted on\n"
    "/dev/sda1        50G   39G  8.6G  78% /\n"
)
client = FakeClient(df_output)
print(disk_usage(client, 80))
print(disk_usage(client, 75))
```

Вывод:

```
(78, 'OK')
(78, 'ALERT')
```

Что здесь происходит? `exec_command` возвращает три потока, но нам нужен только stdout; читаем его целиком и декодируем из байтов в строку. Регулярное выражение `(\d+)%` ищет число перед знаком процента и захватывает его в группу — `int(m.group(1))` даёт готовое значение. Из `df -h` процент приходит округлённым, поэтому не стоит ждать точности до десятой: для пороговой тревоги этого достаточно. Если команда вернула неожиданный формат (другая локаль, другая файловая система), `re.search` вернёт `None`, и функция честно скажет `UNKNOWN`, а не упадёт с `AttributeError`. Класс `FakeClient` — важная часть решения: он повторяет только `exec_command`, поэтому тест не требует ни сети, ни сервера, ни библиотеки paramiko в момент проверки логики.

### Разбор 7
Решение:

```python
from pathlib import Path
import paramiko

REMOTE_DIR = "/etc/app/conf"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    "192.168.1.50",
    username="deploy",
    key_filename=str(Path.home() / ".ssh" / "id_ed25519"),
    timeout=10,
)
sftp = client.open_sftp()

try:
    sftp.stat(REMOTE_DIR)
except FileNotFoundError:
    sftp.mkdir(REMOTE_DIR)

uploaded = 0
skipped = 0

for local in Path("conf").glob("*.conf"):
    remote = f"{REMOTE_DIR}/{local.name}"
    try:
        remote_size = sftp.stat(remote).st_size
    except FileNotFoundError:
        remote_size = None
    if remote_size == local.stat().st_size:
        skipped += 1
        continue
    sftp.put(str(local), remote)
    uploaded += 1

print(f"Загружено: {uploaded}, пропущено: {skipped}")
sftp.close()
client.close()
```

Вывод при двух прогонах:

```
Загружено: 3, пропущено: 0
Загружено: 0, пропущено: 3
```

Что здесь происходит? Скрипт идёт по локальным файлам `*.conf` и для каждого строит удалённый путь. Проверка размера — дешёвый способ понять, менялся ли файл: если размеры совпали, содержимое почти наверняка то же, и трафик не тратится. `FileNotFoundError` во внутреннем `try` означает «файла на сервере ещё нет», поэтому `remote_size` становится `None`, условие не срабатывает и файл загружается. Отдельная проверка каталога нужна один раз: `mkdir` без неё упадёт, если папка уже существует. Счётчики разделяют два исхода, и по отчёту сразу видно, был ли это первый прогон или повторный. Аутентификация идёт по ключу через `key_filename` — в отличие от пароля в коде, ключ не попадает в репозиторий. Закрываем сначала `sftp`, потом `client`: сессия живёт внутри соединения.

<!--/SOLUTION-->

<!--QUIZ-->
Какой метод paramiko выполняет команду на сервере?
- exec_command
- run_command
- execute
* Правильный ответ: exec_command
exec_command запускает команду в SSH-канале и возвращает stdin, stdout, stderr.

Что делает set_missing_host_key_policy(AutoAddPolicy())?
- Добавляет неизвестные ключи хостов автоматически
- Отключает проверку ключей
- Запрещает подключение к новым хостам
* Правильный ответ: Добавляет неизвестные ключи хостов автоматически
AutoAddPolicy доверяет новым хостам без подтверждения.

Как узнать код возврата команды в paramiko?
- stdout.channel.recv_exit_status()
- stderr.read()
- client.returncode
* Правильный ответ: stdout.channel.recv_exit_status()
recv_exit_status() ждёт завершения и возвращает код возврата.

Какой метод SFTP скачивает файл с сервера?
- sftp.get()
- sftp.put()
- sftp.download()
* Правильный ответ: sftp.get()
get(remote, local) скачивает файл с сервера на локальную машину.

Какую ошибку бросит paramiko при неверном пароле?
- paramiko.AuthenticationException
- paramiko.SSHException
- TimeoutError
* Правильный ответ: paramiko.AuthenticationException
AuthenticationException сигнализирует о проблемах аутентификации.

Что возвращает exec_command?
- Три потока: stdin, stdout, stderr
- Одну строку с выводом
- Код возврата
* Правильный ответ: Три потока: stdin, stdout, stderr
Распаковка: stdin, stdout, stderr = client.exec_command("cmd").

Какой метод SFTP загружает файл на сервер?
- sftp.put()
- sftp.get()
- sftp.send()
* Правильный ответ: sftp.put()
put(local, remote) загружает локальный файл на сервер; get — скачивает.

Какое исключение бросит paramiko при недоступном сервере (таймаут)?
- TimeoutError
- paramiko.AuthenticationException
- FileNotFoundError
* Правильный ответ: TimeoutError
Если сервер не отвечает за отведённое время, возникает TimeoutError.

Что вернёт stdout.read(), если команда ничего не напечатала?
- b""
- None
- Пустую строку str
* Правильный ответ: b""
read() возвращает байты, поэтому пустой вывод — это b"", а не None.

Зачем указывать timeout в client.connect()?
- Чтобы подключение не висело бесконечно на мёртвом сервере
- Чтобы команда выполнялась дольше
- Чтобы отключить проверку ключей хоста
* Правильный ответ: Чтобы подключение не висело бесконечно на мёртвом сервере
Без таймаута скрипт может ждать недоступный хост очень долго.

Что делает sftp.listdir(path)?
- Возвращает список имён файлов в каталоге
- Скачивает каталог целиком
- Удаляет каталог
* Правильный ответ: Возвращает список имён файлов в каталоге
Это аналог os.listdir, но для удалённой файловой системы.

Что предпочтительнее пароля в коде для автоматизации по SSH?
- SSH-ключ через key_filename
- Логин root с простым паролем
- Отключение проверки ключа хоста
* Правильный ответ: SSH-ключ через key_filename
Ключ не хранится в репозитории и не попадает в историю коммитов.
<!--/QUIZ-->
