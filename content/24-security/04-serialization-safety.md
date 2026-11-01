---
title: Безопасная сериализация и pickle
summary: Почему pickle опасен для недоверенных данных, как злоумышленник строит эксплойт и как защититься: allowlist классов, безопасные форматы и подписанные полезные нагрузки.
order: 4
duration: 45 мин
difficulty: advanced
tags: pickle, сериализация, json, hmac, yaml, всп
---

**Сериализация** — превращение объекта в байты (например, для сохранения или передачи по сети), **десериализация** — обратный процесс. Проблема в том, что многие форматы позволяют закодировать не только данные, но и код, который выполнится при загрузке. Разберём, чем опасен `pickle` и как правильно передавать данные.

## Почему pickle опасен

`pickle` — встроенный формат Python. Удобство обманчиво: `pickle.dumps(obj)` превращает любой объект в байты, `pickle.loads(data)` — обратно. Но при распаковке pickle может выполнить произвольный код: для этого используется метод `__reduce__`, который возвращает кортеж «вызываемый объект + аргументы». Посмотри:

```python
import pickle
import subprocess

class Harmless:
    def __reduce__(self):
        return (subprocess.run, (["echo", "ПОПАЛИСЬ!"],))

payload = pickle.dumps(Harmless())
print(payload[:30])  # видно, что это pickle-байты
```

Если сервер вызовет `pickle.loads(payload)` на таких данных от клиента, выполнится `subprocess.run(["echo", "ПОПАЛИСЬ!"])` — а вместо `echo` злоумышленник подставит `rm -rf` или чтение секретов. **Правило: никогда не десериализуй pickle из недоверенного источника.** Не используй pickle для данных, которые пересекают границу доверия: от клиента, из внешнего сервиса, из файла, который может кто-то менять.

## Какие форматы использовать

- **JSON** — безопасен по своей природе (только данные, никакого кода), идеален для обмена между сервисами. Нюанс: `json.loads` не выполняет код, но не проверяет типы — следи сам.
- **YAML** — используй только `yaml.safe_load`, а не `yaml.load`, который умеет создавать произвольные объекты (в старых версиях PyYAML это давало RCE).
- **msgpack, protobuf, avro** — безопасные бинарные форматы для данных.
- Если нужно передать именно Python-объекты — только через подписанные структуры данных (JSON + HMAC-подпись).

## Подписанные полезные нагрузки

Чтобы данные не могли подменить по дороге, их подписывают MAC-алгоритмом. Пример — подпись JSON токеном на `hmac`:

```python
import base64
import hashlib
import hmac
import json

KEY = "очень-секретный-ключ".encode()

def sign(payload: dict) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(KEY, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"

def verify(token: str) -> dict:
    body, _, sig = token.rpartition(".")
    expected = hmac.new(KEY, body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Подпись не совпала")
    return json.loads(base64.urlsafe_b64decode(body.encode()))
```

`sig` вычисляется из тела и секретного ключа; подменить тело без ключа невозможно — подпись не сойдётся. Проверка идёт **до** разбора JSON, чтобы не разбирать поддельные данные.

## Десериализация с allowlist

Если без `pickle` никак (например, свой кэш внутри доверенного периметра), ограничь, какие классы можно создавать. Для этого переопределяют `find_class` в `pickle.Unpickler`:

```python
import pickle

ALLOWED = {(collections, "OrderedDict")}  # пример: только стандартные типы

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) not in ALLOWED:
            raise pickle.UnpicklingError(f"Класс {module}.{name} запрещён")
        return super().find_class(module, name)
```

Остальное — только через безопасные форматы и подписи.

## Итог урока

pickle — мощный, но опасный инструмент: он выполняет код при загрузке. JSON/YAML(safe) — данные без кода. Если данные должны быть целостными — подписывай их HMAC и проверяй подпись до разбора. Если pickle неизбежен — allowlist классов. Теперь закрепим на практике.

<!--TASK-->
### Задача 1
Напиши функции `sign(payload)` и `verify(token)` для подписанной JSON-полезной нагрузки. `sign` принимает словарь и возвращает строку `тело.подпись`, где тело — `base64.urlsafe_b64encode` от `json.dumps(payload)`, а подпись — `hmac.new(KEY, body, hashlib.sha256).hexdigest()`. `verify` разбивает токен через `rpartition(".")`, сверяет подпись через `hmac.compare_digest` и возвращает разобранный JSON, а при несовпадении бросает `ValueError("Подпись не совпала")`. Проверь: подпиши `{"user": "admin"}`, вызови `verify(token)` (должен вернуть исходный словарь), затем испорть последний символ токена и убедись, что `verify` бросает `ValueError` (поймай и выведи сообщение).

### Задача 2
Создай класс `Evil`, у которого метод `__reduce__` возвращает `(print, ("ВНИМАНИЕ: код выполнился",))`. Сериализуй его через `pickle.dumps(Evil())` и сохрани результат в переменную `payload`. НЕ вызывай `pickle.loads(payload)` — вместо этого просто выведи первые 40 символов payload и строку `Payload создан, НЕ распаковывать!`. Так ты увидишь, как выглядит «подарок» злоумышленника, не активируя его.

### Задача 3
Напиши функцию `validate_payload(data)`, которая проверяет входящий JSON (уже разобранный) на соответствие схеме и возвращает очищенный словарь. Допустимы только ключи `name` (строка), `age` (int) и `role` (строка из списка `{"user", "admin"}`). Если ключ неизвестен или тип неверный — игнорируй поле. Если `role` не из списка — игнорируй его. Верни словарь только с допустимыми полями. Проверь на `{"name": "Alice", "age": 30, "role": "user", "extra": "вредный ключ"}` — должен вернуться только `{"name": "Alice", "age": 30, "role": "user"}`. Выведи результат.

### Задача 4
Реализуй `SafeUnpickler(pickle.Unpickler)` с переопределённым `find_class`, который разрешает создавать только классы `collections.OrderedDict` и `datetime.datetime`, а для всего остального бросает `pickle.UnpicklingError` с сообщением `Класс {module}.{name} запрещён`. Проверь: `pickle.dumps(collections.OrderedDict(a=1))` должен распаковаться успешно, а `pickle.dumps(print)` — бросить исключение (поймай и выведи сообщение). Создавать экземпляры классов не нужно — достаточно упаковать/распаковать.

### Задача 5
Напиши функцию `safe_extract(zip_path, dest_dir)`, которая извлекает ZIP-архив без уязвимости «zip slip» (путь-захода за пределы папки назначения). Для каждого имени файла в `zipfile.ZipFile(zip_path).namelist()` строй целевой путь через `Path(dest_dir) / name`, затем проверяй `target.resolve().is_relative_to(Path(dest_dir).resolve())` — если нет, пропускай файл и печатай `Пропущен опасный путь: <name>`, иначе создавай родительскую папку и извлекай файл. Затем создай в памяти безопасный архив с одним файлом через `io.BytesIO` + `zipfile.ZipFile(mode="w")` и проверь, что он корректно извлекается в временную папку. Выведи список извлечённых файлов.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`rpartition(".")` возвращает кортеж `(до, разделитель, после)` — бери `[0]` и `[2]`. `base64.urlsafe_b64decode` для разбора тела. Ключ задай как глобальную константу: `KEY = "секретный-ключ".encode()`. Не забудь `hmac.compare_digest`.
### Подсказка 2
Метод `__reduce__` возвращает кортеж `(функция, аргументы)`. `pickle.dumps` сериализует; `pickle.loads` выполнит при распаковке — поэтому мы его не вызываем, а только показываем `payload[:40]`.
### Подсказка 3
Создай пустой словарь-результат и добавляй поля только после проверок. Для `role` сверяйся с множеством `{"user", "admin"}`. `isinstance(value, int)` отличает числа от строк; `isinstance(value, str)` — строки.
### Подсказка 4
`find_class(self, module, name)` вызывается при создании объекта; сверяй `(module, name)` с allowlist-множеством. Для `datetime.datetime` модуль называется `datetime`, имя — `datetime`. Используй `pickle.Unpickler(io.BytesIO(data))` и `.load()` для распаковки.
### Подсказка 5
`Path(dest_dir).resolve()` нормализует путь. `is_relative_to` проверяет, что целевой путь внутри папки. Для записи в архив: `zf.writestr("hello.txt", "hi")`; читается байтовый поток через `io.BytesIO(buf.getvalue())`. Не забудь `import zipfile, io, tempfile, pathlib`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import base64
import hashlib
import hmac
import json

KEY = "секретный-ключ".encode()

def sign(payload):
    body = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(KEY, body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"

def verify(token):
    body, _, sig = token.rpartition(".")
    expected = hmac.new(KEY, body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Подпись не совпала")
    return json.loads(base64.urlsafe_b64decode(body.encode()))

token = sign({"user": "admin"})
print(verify(token))
try:
    verify(token[:-1] + ("A" if token[-1] != "A" else "B"))
except ValueError as e:
    print(e)
```

Результат:

```
{'user': 'admin'}
Подпись не совпала
```

Что здесь происходит? `sign` кодирует JSON в base64 (URL-safe), считает HMAC-SHA256 от тела и склеивает через точку. `verify` разбивает токен, заново считает ожидаемую подпись и сравнивает через `compare_digest` — за постоянное время. Если хоть один символ тела или подписи изменился, подпись не совпадёт, и мы бросаем `ValueError` **до** `json.loads` — то есть не разбираем поддельные данные. Это важный порядок: сначала целостность, потом разбор.

### Разбор 2
Решение:

```python
import pickle

class Evil:
    def __reduce__(self):
        return (print, ("ВНИМАНИЕ: код выполнился",))

payload = pickle.dumps(Evil())
print(payload[:40])
print("Payload создан, НЕ распаковывать!")
```

Результат (примерно):

```
b'\x80\x05\x95\x81\x00\x00\x00\x00\x00\x00\x00\x8c\x08builtins\x94\x8c\x05print\x94\x93\x94\x8c\x14ВНИМАНИЕ: код выполнился'
Payload создан, НЕ распаковывать!
```

Что здесь происходит? В байтах видно `builtins` и `print` — pickle записал не просто данные, а команду «вызови print с этой строкой». Если бы сервер вызвал `pickle.loads(payload)`, в консоль напечаталось бы `ВНИМАНИЕ: код выполнился`. Злоумышленник с `__reduce__` может подставить вместо `print` что угодно: `eval`, `os.system`, `subprocess.run`. Это и есть суть эксплуатации pickle: десериализация = выполнение кода. Запомни главное правило: `pickle.loads` можно вызывать только для данных, которые ты сам создал и которые никто не мог подменить.

### Разбор 3
Решение:

```python
def validate_payload(data):
    result = {}
    if isinstance(data.get("name"), str):
        result["name"] = data["name"]
    if isinstance(data.get("age"), int):
        result["age"] = data["age"]
    if data.get("role") in {"user", "admin"}:
        result["role"] = data["role"]
    return result

raw = {"name": "Alice", "age": 30, "role": "user", "extra": "вредный ключ"}
print(validate_payload(raw))
```

Результат:

```
{'name': 'Alice', 'age': 30, 'role': 'user'}
```

Что здесь происходит? Функция строит новый словарь, копируя только поля, прошедшие проверки. `"extra": "вредный ключ"` отбрасывается — его нет в схеме. Типы контролируются через `isinstance`: `"age": 30` — int, а строка `"30"` не прошла бы. `role` сравнивается с белым списком. Это «allowlist-подход» к данным: мы начинаем с пустого результата и добавляем только то, что разрешили, а не пропускаем всё, что не запретили. Такой валидатор — первый слой защиты перед тем, как данные попадут в бизнес-логику.

### Разбор 4
Решение:

```python
import io
import pickle
import collections
import datetime

ALLOWED = {
    ("collections", "OrderedDict"),
    ("datetime", "datetime"),
}

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) not in ALLOWED:
            raise pickle.UnpicklingError(f"Класс {module}.{name} запрещён")
        return super().find_class(module, name)

def loads(data):
    return SafeUnpickler(io.BytesIO(data)).load()

print(loads(pickle.dumps(collections.OrderedDict(a=1))))
try:
    loads(pickle.dumps(print))
except pickle.UnpicklingError as e:
    print(e)
```

Результат:

```
OrderedDict([('a', 1)])
Класс builtins.print запрещён
```

Что здесь происходит? Стандартный `Unpickler` при встрече с объектом вызывает `find_class(module, name)` — именно здесь можно запретить опасные классы. Наш класс пропускает только `OrderedDict` и `datetime`, а `builtins.print` вызывает ошибку. Обрати внимание: `pickle.dumps(print)` — не вызов функции, а упаковка ссылки на неё; она удалась, а вот распаковка остановлена. Такой allowlist — защита «последней надежды», когда обойтись без pickle нельзя. Но помни: даже с allowlist лучше не принимать pickle извне, потому что ошибка в списке разрешённых классов = RCE.

### Разбор 5
Решение:

```python
import io
import tempfile
import zipfile
from pathlib import Path

def safe_extract(zip_path, dest_dir):
    dest = Path(dest_dir).resolve()
    extracted = []
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            target = (dest / name).resolve()
            if not target.is_relative_to(dest):
                print(f"Пропущен опасный путь: {name}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(name) as src, open(target, "wb") as out:
                out.write(src.read())
            extracted.append(name)
    return extracted

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as zf:
    zf.writestr("hello.txt", "hi")
buf.seek(0)

with tempfile.TemporaryDirectory() as tmp:
    print(safe_extract(buf, tmp))
```

Результат:

```
['hello.txt']
```

Что здесь происходит? Атака «zip slip» — когда в архиве есть имя файла вида `../secret.txt`, и наивный `zf.extract` записывает его вне папки назначения. Мы строим целевой путь, нормализуем его через `resolve()`, и проверяем `is_relative_to(dest)`. Если путь выходит за пределы — файл пропускается с предупреждением. Для безопасного файла создаётся родительская папка и данные копируются вручную. Это тот же принцип, что и в SSRF: любое «внешнее» имя не должно увести нас за границу доверия.
<!--/SOLUTION-->

<!--QUIZ-->
Почему pickle опасен для недоверенных данных?
- Он может выполнить произвольный код при распаковке
- Он медленно работает
- Он шифрует данные
* Правильный ответ: Он может выполнить произвольный код при распаковке
Метод __reduce__ позволяет закодировать вызов любой функции.

Что возвращает метод __reduce__?
- Кортеж (вызываемый объект, аргументы)
- Строку с JSON
- Список атрибутов
* Правильный ответ: Кортеж (вызываемый объект, аргументы)
При распаковке pickle вызовет этот объект с этими аргументами.

Какой формат безопасен для обмена данными по сети?
- JSON
- pickle
- Нативный бинарный дамп Python
* Правильный ответ: JSON
JSON содержит только данные; никакого кода при разборе не выполняется.

Что делает yaml.safe_load?
- Разбирает YAML, не создавая произвольные объекты
- Выполняет код на Python
- Шифрует YAML
* Правильный ответ: Разбирает YAML, не создавая произвольные объекты
yaml.load в старых версиях мог создавать объекты и приводить к RCE.

Что такое HMAC?
- Код аутентификации сообщения на основе секретного ключа
- Способ сжатия данных
- Тип базы данных
* Правильный ответ: Код аутентификации сообщения на основе секретного ключа
HMAC позволяет проверить, что данные не изменялись и созданы владельцем ключа.

В каком порядке нужно проверять подписанные данные?
- Сначала подпись, потом разбор
- Сначала разбор, потом подпись
- Порядок не важен
* Правильный ответ: Сначала подпись, потом разбор
Не разбирай данные, чья целостность не подтверждена.

Что делает find_class в Unpickler?
- Решает, какие классы можно создавать при распаковке
- Сжимает pickle
- Ускоряет распаковку
* Правильный ответ: Решает, какие классы можно создавать при распаковке
Переопределив find_class, можно ввести allowlist классов.

Что такое «zip slip»?
- Атака, при которой файл из архива записывается вне папки назначения
- Переполнение буфера
- Подбор пароля к архиву
* Правильный ответ: Атака, при которой файл из архива записывается вне папки назначения
Имена вроде ../secret.txt уводят запись за пределы.

Как проверить, что целевой путь внутри папки?
- target.resolve().is_relative_to(dest)
- len(target) > 100
- target.exists()
* Правильный ответ: target.resolve().is_relative_to(dest)
resolve() нормализует путь, is_relative_to проверяет принадлежность.

Какой принцип описывает стратегию «начинаем с пустого результата и добавляем только разрешённое»?
- Allowlist (белый список)
- Blacklist (чёрный список)
- Дефолт
* Правильный ответ: Allowlist (белый список)
Разрешено явно — остальное отвергается.
<!--/QUIZ-->
