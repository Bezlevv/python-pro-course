---
title: Мониторинг и скрипты для CI
summary: Как собирать метрики, проверять здоровье сервисов и встраивать Python-скрипты в пайплайны непрерывной интеграции (CI).
order: 6
duration: 40 мин
difficulty: advanced
tags: мониторинг, CI, subprocess, отчёты, healthcheck
---

## Что такое мониторинг

Мониторинг — это наблюдение за состоянием системы: жив ли сервер, сколько места осталось на диске, не упал ли сервис, как быстро отвечает API. Без мониторинга команда узнаёт о проблемах от пользователей — а это худший способ.

Python отлично подходит для написания скриптов мониторинга: они запускаются по расписанию (из прошлого урока) или входят в состав CI-пайплайна, а результат можно отправлять в лог, файл или мессенджер.

## Скрипт-проверка: сбор данных

Типичный скрипт мониторинга собирает данные из нескольких источников. Для системных показателей часто используются внешние команды через `subprocess`:

```python
import subprocess

result = subprocess.run(
    ["df", "-h", "/"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout)
```

`df -h /` показывает занятость диска. `check=True` заставляет `subprocess` бросить `CalledProcessError`, если команда завершилась с ошибкой. Так скрипт не «молчит» о проблемах, а явно падает.

## Проверка здоровья сервиса

Часто нужно проверить, отвечает ли веб-сервис. Простейший способ — послать HTTP-запрос к health-эндпоинту. Стандартная библиотека `urllib` отлично справляется:

```python
import urllib.request

try:
    with urllib.request.urlopen("http://localhost:8000/health", timeout=5) as resp:
        print("Статус:", resp.status)
        print("Ответ:", resp.read().decode())
except urllib.error.URLError as e:
    print("Сервис недоступен:", e)
```

`urlopen` открывает URL, `resp.status` — код ответа, а таймаут не даёт скрипту зависнуть навсегда. Для этого примера достаточно `urllib` — он есть в стандартной библиотеке.

## Сбор отчёта

Данные мониторинга удобно собирать в словарь и сериализовать, например, в JSON — такой отчёт легко читать и отправлять дальше:

```python
import json

report = {
    "host": "web-01",
    "disk_free_gb": 42.5,
    "service": "up",
    "healthy": True,
}
print(json.dumps(report, indent=2, ensure_ascii=False))
```

## Скрипты для CI

Continuous Integration (CI) — это практика, при которой каждый коммит автоматически прогоняется через проверки: тесты, линтеры, сборку. CI-системы (GitHub Actions, GitLab CI, Jenkins) запускают команды в свежих окружениях, и Python-скрипты в этих пайплайнах решают сотни задач: прогоняют тесты, проверяют форматирование, собирают отчёты.

Главное правило для скриптов в CI: **корректный код возврата**. Если скрипт завершился с кодом 0 — пайплайн считается успешным, с ненулевым — падает. Поэтому в конце скрипта важно явно завершаться с `sys.exit(0)` или `sys.exit(1)` в зависимости от результата проверок.

## Простой CI-скрипт

Представь, что тебе нужно проверить, что в проекте нет файлов больше 1 МБ, а затем запустить тесты:

```python
import subprocess
import sys
from pathlib import Path

big_files = [p for p in Path(".").rglob("*")
             if p.is_file() and p.stat().st_size > 1_000_000]
if big_files:
    print("Найдены большие файлы:", [p.name for p in big_files])
    sys.exit(1)

result = subprocess.run(["python", "-m", "pytest", "-q"], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
    sys.exit(result.returncode)
```

Это ровно то, что происходит в настоящих CI: скрипт проверяет условия и либо проходит дальше (код 0), либо падает с сообщением.

## Итог

Мы научились собирать данные о системе через `subprocess`, проверять здоровье сервисов через `urllib`, оформлять отчёты в JSON и строить скрипты, которые корректно сигнализируют о результате через код возврата. Это всё, что нужно для простого мониторинга и встраивания в CI. Закрепляем задачами.

<!--TASK-->
### Задача 1
Напиши скрипт `df_check.py`, который выполняет команду `df -h /` через `subprocess.run` с `capture_output=True`, `text=True` и `check=True`, а затем печатает вывод. Добавь обработку `subprocess.CalledProcessError`: если команда не удалась, выведи `Ошибка при получении данных о диске` и завершись с кодом 1.

### Задача 2
Создай скрипт `healthcheck.py`, который проверяет доступность `http://localhost:8000/health` через `urllib.request.urlopen` с таймаутом 5 секунд. Если сервис ответил — выведи `OK, код 200` (или реальный код) и завершись с кодом 0. Если сервис недоступен (перехвати `urllib.error.URLError`) — выведи `Сервис недоступен` и завершись с кодом 1.

### Задача 3
Напиши скрипт `report_json.py`, который собирает отчёт о состоянии системы в словарь: имя хоста (через `subprocess` и команду `hostname`), текущее время (модуль `datetime`), количество файлов в текущем каталоге (через `pathlib`) и сохраняет отчёт в файл `report.json` через `json.dump` с `indent=2`. Затем прочитай файл обратно и выведи его содержимое.

### Задача 4
Создай скрипт `check_large.py`, который обходит текущий каталог через `Path(".").rglob("*")` и находит все файлы размером больше 1 МБ (1_000_000 байт). Если такие есть — выведи их имена по одному на строку и завершись с кодом 1. Если нет — выведи `Всё в порядке` и завершись с кодом 0. Это классический CI-скрипт-страж.

### Задача 5
Напиши скрипт `ci_summary.py`, который «запускает» три проверки (обычные функции, возвращающие True/False: `check_tests()`, `check_lint()`, `check_build()`), собирает результаты в список, печатает сводку вида `check_tests: PASS` / `check_lint: FAIL` и в конце завершается с кодом 0, если все прошли, и с кодом 1, если хоть одна провалилась. Смоделируй одну провалившуюся проверку и убедись, что код возврата равен 1.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Вызывай `subprocess.run(["df", "-h", "/"], capture_output=True, text=True, check=True)` внутри `try`. Перехватывай `subprocess.CalledProcessError as e:`. При ошибке — `print(...)` и `sys.exit(1)`. Не забудь `import sys`.

### Подсказка 2
Открывай URL через `with urllib.request.urlopen(url, timeout=5) as resp:` — внутри блока `try`. Код ответа — `resp.status`. В `except urllib.error.URLError:` печатай сообщение и выходи с `sys.exit(1)`.

### Подсказка 3
Хост получи так: `subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()`. Время: `datetime.datetime.now().isoformat()`. Файлы: `sum(1 for p in Path(".").rglob("*") if p.is_file())`. Запись — `json.dump(report, f, indent=2, ensure_ascii=False)`.

### Подсказка 4
Используй list comprehension: `big = [p for p in Path(".").rglob("*") if p.is_file() and p.stat().st_size > 1_000_000]`. Если `big` непустой — циклом печатай `p.name`, затем `sys.exit(1)`. Иначе — `sys.exit(0)`.

### Подсказка 5
Определи список проверок: `checks = [("check_tests", check_tests), ...]`. В цикле вызывай функцию, сравнивай с True, печатай PASS/FAIL и накапливай `all_ok = all_ok and ok`. В конце: `sys.exit(0 if all_ok else 1)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import subprocess
import sys

try:
    result = subprocess.run(
        ["df", "-h", "/"],
        capture_output=True,
        text=True,
        check=True,
    )
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Ошибка при получении данных о диске")
    print(e.stderr)
    sys.exit(1)
```

Что здесь происходит? `df -h /` выводит информацию о диске, на котором смонтирован корень. `check=True` превращает ошибку команды в исключение `CalledProcessError` — так мы не пропустим сбой. В блоке `except` печатаем человекочитаемое сообщение и stderr команды, а затем завершаемся с кодом 1. Это важный паттерн: скрипт мониторинга должен не просто «упасть», а объяснить, что случилось. В успешном случае мы печатаем вывод `df` — там видны размер, занятость и процент использования диска.

### Разбор 2
Решение:

```python
import sys
import urllib.request
import urllib.error

url = "http://localhost:8000/health"

try:
    with urllib.request.urlopen(url, timeout=5) as resp:
        print(f"OK, код {resp.status}")
    sys.exit(0)
except urllib.error.URLError:
    print("Сервис недоступен")
    sys.exit(1)
```

Что здесь происходит? `urlopen` посылает GET-запрос и открывает соединение. Контекстный менеджер `with` гарантирует закрытие соединения. `timeout=5` — критично: без него скрипт может висеть долго, ожидая ответа от мёртвого сервера. Если сервис работает, печатаем код ответа (200 — норма) и выходим с 0. Если `urlopen` бросил `URLError` (сервер не отвечает, DNS не резолвится, соединение отклонено) — сообщаем и выходим с 1. Такой healthcheck можно вешать в cron каждые пару минут: код возврата сам подскажет, всё ли в порядке.

### Разбор 3
Решение:

```python
import datetime
import json
import subprocess
from pathlib import Path

host = subprocess.run(["hostname"], capture_output=True, text=True).stdout.strip()

report = {
    "host": host,
    "time": datetime.datetime.now().isoformat(),
    "files_count": sum(1 for p in Path(".").rglob("*") if p.is_file()),
}

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

with open("report.json", encoding="utf-8") as f:
    print(f.read())
```

Вывод (пример):

```json
{
  "host": "web-01",
  "time": "2026-11-01T14:25:00.123456",
  "files_count": 142
}
```

Что здесь происходит? Сбор данных разбит на независимые части: хост берём из `hostname`, время — из `datetime`, а количество файлов считаем генератором: `sum(1 for p in ... if p.is_file())` обходит дерево каталога и считает только файлы. `isoformat()` даёт время в стандартном ISO-формате, удобном для хранения. Затем отчёт сериализуется в JSON и записывается, а сразу после — читается обратно и выводится. Такой отчёт можно хранить по одному на проверку и сравнивать изменения.

### Разбор 4
Решение:

```python
import sys
from pathlib import Path

big = [
    p for p in Path(".").rglob("*")
    if p.is_file() and p.stat().st_size > 1_000_000
]

if big:
    for p in big:
        print(p.name)
    sys.exit(1)
else:
    print("Всё в порядке")
    sys.exit(0)
```

Что здесь происходит? `rglob("*")` рекурсивно обходит весь каталог, включая подпапки. В list comprehension мы сразу фильтруем: только файлы (`is_file()`) размером больше мегабайта. Если список `big` непустой — печатаем имена нарушителей и завершаемся с кодом 1. Если пустой — «Всё в порядке» и код 0. Это классический «страж» в CI: если в репозиторий закоммитили бинарник на 500 МБ, пайплайн упадёт с понятным списком файлов, и разработчик быстро поймёт причину.

### Разбор 5
Решение:

```python
import sys

def check_tests():
    return True

def check_lint():
    return False   # смоделированная провальная проверка

def check_build():
    return True

checks = [
    ("check_tests", check_tests),
    ("check_lint", check_lint),
    ("check_build", check_build),
]

all_ok = True
for name, fn in checks:
    ok = fn()
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    all_ok = all_ok and ok

sys.exit(0 if all_ok else 1)
```

Вывод:

```
check_tests: PASS
check_lint: FAIL
check_build: PASS
```

Что здесь происходит? Список `checks` хранит пары «имя, функция». Цикл вызывает каждую проверку, печатает результат и накапливает общий флаг `all_ok`. Выражение `sys.exit(0 if all_ok else 1)` — тернарный оператор: код 0 при полном успехе, 1 иначе. В реальном CI вместо заглушек были бы настоящие проверки: `pytest`, `flake8`, сборка. А этот каркас — универсален: добавил пару в список — и новая проверка уже в отчёте и влияет на результат сборки.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает параметр check=True в subprocess.run?
- Бросает CalledProcessError при ненулевом коде возврата
- Проверяет наличие команды
- Ждёт завершения команды
* Правильный ответ: Бросает CalledProcessError при ненулевом коде возврата
Без check=True ошибка команды осталась бы незамеченной.

Какой модуль стандартной библиотеки делает HTTP-запросы?
- urllib.request
- requests
- urllib.parse
* Правильный ответ: urllib.request
urllib.request.urlopen — простой способ получить URL из стандартной библиотеки.

Какой код возврата означает успех в CI?
- 0
- 1
- 2
* Правильный ответ: 0
CI считает пайплайн успешным, если команда вернула 0.

Что делает sys.exit(1)?
- Завершает программу с кодом возврата 1
- Печатает ошибку
- Пропускает остаток кода
* Правильный ответ: Завершает программу с кодом возврата 1
sys.exit(code) завершает процесс с указанным кодом.

Что из этого — пример CI-проверки?
- Прогон тестов pytest
- Установка шрифтов
- Настройка браузера
* Правильный ответ: Прогон тестов pytest
CI автоматически прогоняет тесты, линтеры и сборку при каждом коммите.

Какой метод pathlib обходит каталог рекурсивно?
- rglob("*")
- glob("*")
- iterdir()
* Правильный ответ: rglob("*")
rglob находит файлы во всех вложенных папках, glob — только в текущей.
<!--/QUIZ-->
