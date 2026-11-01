---
title: Упаковка и публикация на PyPI
summary: Превращаем свой код в пакет: pyproject.toml, сборка wheel, загрузка на PyPI через twine.
order: 6
duration: 50 мин
difficulty: advanced
tags: упаковка, PyPI, pyproject, twine, публикация
---

Ты написал полезный модуль — отлично. Но чтобы им могли пользоваться другие (и ты сам в других проектах), код нужно **упаковать** в стандартный формат, а затем **опубликовать** в репозиторий. В мире Python таким репозиторием служит PyPI (Python Package Index) — тот самый, откуда берутся `pip install ...`. В этом уроке пройдём весь путь: от папки с кодом до пакета на TestPyPI.

## Структура проекта

Современный стандарт — «src-раскладка», когда код лежит в подпапке `src/`:

```
hello_pack/
├── src/
│   └── hello_pack/
│       ├── __init__.py
│       └── core.py
├── README.md
└── pyproject.toml
```

Сам код:

```python
# src/hello_pack/core.py
def greet(name: str = "мир") -> str:
    return f"Привет, {name}!"
```

## pyproject.toml

Это — «паспорт» пакета. Современный Python описывает всё в одном файле `pyproject.toml` (стандарт PEP 621):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-pack"
version = "0.1.0"
description = "Пакет, который здоровается."
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Твоё имя"}]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = []

[project.urls]
Homepage = "https://example.com/hello-pack"

[tool.setuptools.packages.find]
where = ["src"]
```

Обрати внимание: секция `[build-system]` сообщает, чем собирать пакет (здесь — setuptools), `[project]` описывает метаданные, а `[tool.setuptools.packages.find]` указывает, где искать код — в `src/`. Поле `license` в новых версиях setuptools лучше задавать через `license = {file = "LICENSE"}` или `{text = "MIT"}` — главное, чтобы файл лицензии существовал, если ты указываешь `file`.

## Сборка и локальная установка

Сначала установим инструменты сборки и загрузки:

```bash
python -m pip install --upgrade build twine
```

Сборка создаёт два артефакта в папке `dist/` — исходники (`sdist`) и готовый колесо (`wheel`):

```bash
python -m build
```

После сборки в `dist/` появятся `hello_pack-0.1.0.tar.gz` и `hello_pack-0.1.0-py3-none-any.whl`. Wheel — это готовый к установке архив: именно его pip ставит быстрее всего.

Чтобы проверять код «вживую», установи пакет в режиме редактирования:

```bash
python -m pip install -e .
```

Теперь `import hello_pack` работает из любого места, причём при изменении кода ничего переустанавливать не нужно.

## Публикация на PyPI

Для публикации нужен аккаунт на [pypi.org](https://pypi.org/) и **API-токен** (создаётся в настройках аккаунта). Токен — это секрет: не клади его в код и не коммить в git.

Публикация:

```bash
python -m twine upload dist/*
```

Twine запросит имя пользователя и пароль — в качестве имени укажи `__token__`, а в качестве пароля — сам токен. Чтобы не ошибиться на реальном PyPI, сначала тренируются на **TestPyPI** — песочнице с теми же правилами:

```bash
python -m twine upload --repository testpypi dist/*
```

После успешной загрузки пакет можно ставить оттуда:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ hello-pack
```

Важно про версии: PyPI не позволяет перезаписать опубликованную версию. Исправление требует **новой версии** — отсюда практика семантического версионирования (semver): `MAJOR.MINOR.PATCH` — мажорная версия меняется при несовместимых изменениях, минорная — при новых возможностях, патч — при исправлениях ошибок.

## Итог урока

Путь таков: структура с `src/`, манифест `pyproject.toml`, сборка через `python -m build`, локальная `-e .` установка, затем `twine upload` — сначала на TestPyPI, потом на PyPI. Теперь собери свой первый пакет.

<!--TASK-->
### Задача 1
Создай пакет `hello_pack` по структуре из урока:

1. Папки `src/hello_pack/` с `__init__.py` (пустым или с импортом `greet`) и `core.py` с функцией `greet(name="мир")`.
2. `README.md` с кратким описанием.
3. `pyproject.toml` с полями: `name = "hello-pack"`, `version = "0.1.0"`, `requires-python = ">=3.10"`, `license = {text = "MIT"}`, классификаторами и `[tool.setuptools.packages.find] where = ["src"]`.
4. Собери пакет: `python -m build`. Убедись, что в `dist/` два файла.
5. Установи локально: `python -m pip install -e .` и проверь:

```python
from hello_pack import greet
print(greet("Аня"))   # Привет, Аня!
```

6. (Необязательно, требует аккаунта и токена) Загрузи на TestPyPI через `python -m twine upload --repository testpypi dist/*` и установи оттуда в чистую среду.

Ожидаемый результат: папка `dist/` с `hello_pack-0.1.0.tar.gz` и `hello_pack-0.1.0-py3-none-any.whl`, а функция `greet` импортируется и работает.

### Задача 2
Добавь пакету `hello_pack` консольную команду. Создай файл `src/hello_pack/cli.py`:

```python
import argparse
from .core import greet


def main() -> None:
    parser = argparse.ArgumentParser(description="Поздороваться")
    parser.add_argument("--name", default="мир", help="Кого приветствовать")
    args = parser.parse_args()
    print(greet(args.name))
```

Затем дополни `pyproject.toml` секцией:

```toml
[project.scripts]
hello-cli = "hello_pack.cli:main"
```

Пересобери пакет (`python -m build`), переустанови `python -m pip install -e .` и запусти `hello-cli --name Аня`. Ожидаемый вывод:

```
Привет, Аня!
```

Если команда не находится — проверь, что `pip install -e .` прошёл успешно и что путь в `[project.scripts]` указан верно.

### Задача 3
Подними версию пакета до `0.2.0` и добавь в корень файл `CHANGELOG.md`:

```markdown
# Журнал изменений

## 0.2.0
- Добавлена консольная команда hello-cli.
- Обновлён README.

## 0.1.0
- Первый выпуск: функция greet.
```

Обнови `README.md` (добавь раздел «Установка» с `pip install -e .` и пример использования). Пересобери пакет и проверь, что в `dist/` появились файлы с новой версией: `hello_pack-0.2.0.tar.gz` и `hello_pack-0.2.0-py3-none-any.whl`. Объясни в комментарии, почему PyPI не разрешает перезаписать уже опубликованную версию `0.1.0` и для чего нужно семантическое версионирование.

### Задача 4
Расширь `pyproject.toml` секцией dev-зависимостей:

```toml
[project.optional-dependencies]
dev = ["ruff", "mypy", "pytest"]
```

Переустанови пакет с этой секцией: `python -m pip install -e ".[dev]"`. Затем проверь, что `ruff`, `mypy` и `pytest` доступны: выполни `python -m ruff --version`, `python -m mypy --version`, `python -m pytest --version`. Если какая-то команда не находит модуль — проверь, что установка прошла с нужной секцией. Запиши вывод всех трёх версий в ответ. В комментарии объясни, зачем dev-зависимости отделяют от основных.

### Задача 5
Проверь архив перед публикацией. Выполни `python -m twine check dist/*` — команда валидирует метаданные и читаемость архива. Ожидаемый вывод:

```
Checking dist/hello_pack-0.2.0-py3-none-any.whl: Passed
Checking dist/hello_pack-0.2.0.tar.gz: Passed
```

Затем (необязательно, если есть аккаунт на TestPyPI) загрузи пакет: `python -m twine upload --repository testpypi dist/*` с логином `__token__` и API-токеном. После загрузки установи пакет в чистую среду из тестового индекса:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ hello-pack
```

Проверь, что `from hello_pack import greet` работает и что `pip show hello-pack` показывает установленную версию. Если публиковать некуда — просто опиши шаги и ожидаемые выводы команд.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Если команды `python -m build` нет — сначала выполни `python -m pip install --upgrade build twine`. Убедись, что файл называется именно `pyproject.toml` и лежит в корне проекта. Для `__init__.py` достаточно `from .core import greet`. Если установка `-e .` не находит пакет — проверь `where = ["src"]` в `[tool.setuptools.packages.find]`.

### Подсказка 2
Секция `[project.scripts]` описывает соответствие «имя команды → функция». Имя `hello-cli` станет исполняемым файлом в окружении, а путь `hello_pack.cli:main` означает: модуль `hello_pack.cli`, функция `main`. После изменения pyproject обязательно перезапусти `pip install -e .`, иначе команда не появится.

### Подсказка 3
Версия хранится только в `pyproject.toml`, в поле `version`. После её изменения пересобери проект (`python -m build`) — старые артефакты в `dist/` останутся, поэтому ориентируйся на имена новых файлов. PyPI не даёт удалить или перезаписать выпущенную версию: исправление выпускается как новая версия с увеличенным номером.

### Подсказка 4
Секция `[project.optional-dependencies]` группирует зависимости по назначению. Ключ `dev` — произвольное имя; установка `pip install -e ".[dev]"` ставит и пакет, и всё из группы. Если передать `.[dev]` без кавычек, некоторые оболочки интерпретируют скобки — поэтому всегда ставь кавычки.

### Подсказка 5
Twine check не требует интернета — он читает локальные файлы из `dist/`. Проблемы он находит такие: отсутствующие метаданные, неверные ссылки на лицензию, ошибки чтения архива. Для загрузки подготовь переменные окружения `TWINE_USERNAME=__token__` и `TWINE_PASSWORD=<токен>` — это надёжнее, чем вводить их вручную.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Одно из возможных решений.

Полный `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "hello-pack"
version = "0.1.0"
description = "Пакет, который здоровается."
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Твоё имя"}]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
]
dependencies = []

[project.urls]
Homepage = "https://example.com/hello-pack"

[tool.setuptools.packages.find]
where = ["src"]
```

Код:

```python
# src/hello_pack/core.py
def greet(name: str = "мир") -> str:
    return f"Привет, {name}!"
```

```python
# src/hello_pack/__init__.py
from .core import greet
```

Шаги выполнения:

```bash
python -m pip install --upgrade build twine
python -m build
python -m pip install -e .
python -c "from hello_pack import greet; print(greet('Аня'))"
```

Команда `python -m build` последовательно собирает sdist (архив с исходниками, `hello_pack-0.1.0.tar.gz`) и wheel (`hello_pack-0.1.0-py3-none-any.whl`). Почему wheel называется `py3-none-any`? `py3` — код работает на любом Python 3, `none` — не привязан к конкретной платформе (например, Windows/Linux), `any` — универсален. Это «чистый Python», поэтому пакет можно ставить где угодно.

Установка `-e .` (editable) ставит пакет «ссылкой»: изменения в `src/` сразу видны при импорте, переустановка не нужна. Это идеально для разработки.

Загрузка на TestPyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

Twine спросит логин и пароль: логин — `__token__`, пароль — API-токен. Если всё прошло успешно, пакет появится на `test.pypi.org`. Перед публикацией на настоящий PyPI стоит проверить имя: оно должно быть уникальным — `hello-pack` наверняка занят, придумай своё. И помни: опубликованную версию нельзя перезаписать — только выпустить новую, увеличив `version`.

### Разбор 2
Решение. Файл `src/hello_pack/cli.py` — как в условии. В `pyproject.toml` добавлена секция:

```toml
[project.scripts]
hello-cli = "hello_pack.cli:main"
```

После `python -m pip install -e .` setuptools создаёт исполняемый скрипт `hello-cli` (в venv — в папке `Scripts/` или `bin/`, в системе — рядом с интерпретатором). При вызове `hello-cli --name Аня` запускается функция `main`: `argparse` разбирает аргументы, `--name` подставляет имя, и печатается `Привет, Аня!`. Если не указать `--name` — используется значение по умолчанию `мир`. Это стандартный способ добавить CLI: никаких внешних библиотек, только `argparse` из стандартной библиотеки и одна секция в pyproject.

### Разбор 3
Решение: в `pyproject.toml` поле `version = "0.2.0"`; добавлен `CHANGELOG.md`; `README.md` дополнен разделом установки. Далее:

```bash
python -m build
ls dist/
```

В `dist/` появятся `hello_pack-0.2.0.tar.gz` и `hello_pack-0.2.0-py3-none-any.whl`. Старые файлы 0.1.0 останутся лежать рядом — это нормально, twine загрузит то, что ты передашь. Почему нельзя перезаписать версию? PyPI хранит каждую версию как неизменяемый артефакт: пользователи могли уже установить 0.1.0, и если бы она вдруг изменилась, проверка целостности и воспроизводимость сборок нарушились бы. Поэтому исправления выпускаются как новые версии. Семантическое версионирование (semver) помогает общаться без слов: MAJOR меняется при несовместимых изменениях, MINOR — при новых возможностях, PATCH — при исправлениях ошибок. 0.2.0 — минорное обновление с новой функциональностью (CLI).

### Разбор 4
Решение: секция в `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["ruff", "mypy", "pytest"]
```

Установка `python -m pip install -e ".[dev]"` ставит пакет в editable-режиме плюс инструменты из группы `dev`. Проверка версий:

```bash
python -m ruff --version    # ruff 0.x.x
python -m mypy --version    # mypy 1.x.x
python -m pytest --version  # pytest 8.x.x
```

Dev-зависимости не попадают в основные `dependencies = []`, потому что они нужны только разработчикам: линтеры, форматеры, тесты. Конечный пользователь, который ставит `hello-pack` с PyPI, получает лишь то, что нужно для работы пакета, — это ускоряет установку и снижает риск конфликтов версий. Группы можно называть как угодно: `dev`, `test`, `docs`, `lint` — главное, чтобы имена отражали назначение.

### Разбор 5
Решение:

```bash
python -m twine check dist/*
```

Вывод:

```
Checking dist/hello_pack-0.2.0-py3-none-any.whl: Passed
Checking dist/hello_pack-0.2.0.tar.gz: Passed
```

Twine проверил, что оба артефакта содержат корректные метаданные и читаются. Если бы, например, в `pyproject.toml` стояла ссылка на несуществующий файл лицензии, check сообщил бы об ошибке. Затем загрузка:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=<твой-токен>
python -m twine upload --repository testpypi dist/*
```

Twine выведет `Uploading hello_pack-0.2.0-py3-none-any.whl`, затем URL на `test.pypi.org` и `Server response (200): OK`. Установка из тестового индекса в свежем venv:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ hello-pack
python -c "from hello_pack import greet; print(greet('Мир'))"
```

`pip show hello-pack` покажет Version: 0.2.0. Полный цикл «собрал → проверил → опубликовал → установил» замкнут.
<!--/SOLUTION-->

<!--QUIZ-->
В каком файле описываются метаданные пакета в современном Python?

- setup.py
- pyproject.toml
- requirements.txt
* Правильный ответ: pyproject.toml
Это единый стандарт (PEP 621) для метаданных, сборки и настроек инструментов.

Что создаёт команда `python -m build`?

- Только wheel-файл
- Оба артефакта: sdist (исходники) и wheel
- Устанавливает пакет в систему
* Правильный ответ: Оба артефакта: sdist (исходники) и wheel
`sdist` — архив исходников, `wheel` — готовый к установке бинарный архив.

Какой инструмент загружает пакет на PyPI?

- pip
- twine
- mypy
* Правильный ответ: twine
Twine — официальный инструмент загрузки: `python -m twine upload dist/*`.

Что означает установка `pip install -e .`?

- Установка пакета в режиме редактирования: изменения в коде сразу видны
- Полная переустановка Python
- Установка только зависимостей
* Правильный ответ: Установка пакета в режиме редактирования: изменения в коде сразу видны
Editable-установка связывает пакет с исходными файлами, и их не нужно переустанавливать после правок.

Зачем нужен TestPyPI?

- Чтобы проверить публикацию и установку, не засоряя настоящий PyPI
- Чтобы ускорить загрузку пакетов
- Это частный репозиторий внутри компании
* Правильный ответ: Чтобы проверить публикацию и установку, не засоряя настоящий PyPI
TestPyPI — песочница: то же поведение, что и у PyPI, но без риска испортить реальный пакет.
<!--/QUIZ-->
