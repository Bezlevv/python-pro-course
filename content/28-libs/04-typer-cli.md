---
title: typer: современные CLI с тестами
summary: Создание командной строки на typer: аргументы, опции, типы и help — и тестирование через CliRunner с pytest.
order: 4
duration: 40 мин
difficulty: intermediate
tags: typer, cli, командная строка, pytest
---

`typer` — библиотека для создания интерфейсов командной строки (CLI). Она построена на `click`, но объявляет команды через аннотации типов Python: меньше кода, автозаполнение, `--help` из коробки. В этом уроке мы напишем утилиту с несколькими командами и покроем её тестами.

## Установка и первая команда

```bash
pip install typer
```

Минимальное приложение:

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    """Поздороваться с пользователем."""
    typer.echo(f"Привет, {name}!")

if __name__ == "__main__":
    app()
```

Запуск:

```bash
python cli.py hello Аня
# Привет, Аня!
```

Декоратор `@app.command()` превращает функцию в команду. Аргумент `name: str` становится позиционным аргументом CLI: если его не передать, typer сам выведет понятную ошибку. Docstring функции автоматически становится текстом помощи в `--help`.

## Аргументы и опции

Позиционные аргументы — `name: str`. Опции объявляются `typer.Option(...)` с дефолтом:

```python
@app.command()
def hello(name: str, greeting: str = typer.Option("Привет", help="Слово приветствия")):
    typer.echo(f"{greeting}, {name}!")
```

Теперь `python cli.py hello Аня --greeting Здравствуйте` выведет `Здравствуйте, Аня!`. Булевы флаги — это `bool` с `typer.Option(False, "--verbose")` или просто `verbose: bool = False` (появится флаг `--verbose/--no-verbose`).

Множественные значения — через `List[int]`:

```python
from typing import List

@app.command()
def total(numbers: List[int]):
    typer.echo(sum(numbers))
```

Вызов: `python cli.py total 1 2 3` → `6`.

## Ошибки и коды возврата

Чтобы завершить команду с ошибкой, используют `typer.Exit(code=1)`:

```python
from pathlib import Path

@app.command()
def file_info(path: Path):
    if not path.exists():
        typer.echo(f"Файл не найден: {path}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"{path.name}: {path.stat().st_size} байт")
```

`err=True` отправляет сообщение в stderr, а `Exit(code=1)` задаёт код возврата процесса — скрипты и CI смогут его поймать.

## Тестирование: CliRunner

Тестировать CLI можно через `typer.testing.CliRunner`. Он вызывает команды внутри процесса теста, без запуска отдельного процесса:

```python
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_hello():
    result = runner.invoke(app, ["hello", "Аня"])
    assert result.exit_code == 0
    assert "Привет, Аня!" in result.stdout
```

`runner.invoke(app, args)` возвращает `Result` с `exit_code` и `stdout`. Внутри `runner.isolated_filesystem()` можно создавать временные файлы — это идеально для команд, работающих с файлами.

## Почему typer, а не argparse

У `argparse` больше шаблонного кода, типы приходится указывать вручную, help тоже. Typer берёт всё на себя: типы из аннотаций, генерация `--help`, подсказки при ошибках. Для маленьких и средних утилит это заметно быстрее и чище. Поехали практиковаться.

<!--TASK-->
### Задача 1
Создай файл `cli.py` с приложением `app = typer.Typer()`. Добавь команду `hello`: позиционный аргумент `name: str` и опцию `greeting: str = typer.Option("Привет", help="Слово приветствия")`. Команда печатает `f"{greeting}, {name}!"` через `typer.echo`. Проверь: `python cli.py hello Аня` печатает `Привет, Аня!`, а `python cli.py hello Аня --greeting Здравствуйте` — `Здравствуйте, Аня!`. Ожидаемый результат: обе команды работают, `--help` показывает описание опции.

### Задача 2
Добавь в `cli.py` команду `total`, которая принимает `numbers: List[int]` и печатает их сумму. Проверь: `python cli.py total 1 2 3` выводит `6`, а `python cli.py total` — `0`. Ожидаемый результат: сумма печатается корректно, в том числе для пустого списка.

### Задача 3
Добавь в `cli.py` команду `file-info` с аргументом `path: Path`. Если файл не существует — выведи `Файл не найден: {path}` в stderr (`err=True`) и подними `typer.Exit(code=1)`. Если существует — выведи `{path.name}: {size} байт`. Проверь на реальном файле и на несуществующем: во втором случае команда должна завершиться с кодом 1. Ожидаемый результат: для существующего файла код возврата 0 и вывод размера, для отсутствующего — код 1 и сообщение в stderr.

### Задача 4
Напиши pytest-тесты для команд `hello` и `total` через `CliRunner`: (1) `runner.invoke(app, ["hello", "Аня"])` — `exit_code == 0` и `"Привет, Аня!" in result.stdout`; (2) с опцией `--greeting` — другой текст; (3) `total` для `["1", "2", "3"]` — `exit_code == 0`, вывод `6`; (4) `total` без чисел — вывод `0`. Запусти `python -m pytest test_cli.py -v`. Ожидаемый результат: все 4 теста проходят.

### Задача 5
Напиши pytest-тесты для `file-info`: (1) внутри `runner.isolated_filesystem()` создай файл `data.txt` с текстом, затем `runner.invoke(app, ["file-info", "data.txt"])` — `exit_code == 0` и в `result.stdout` есть `data.txt` и размер файла; (2) для `runner.invoke(app, ["file-info", "missing.txt"])` — `exit_code == 1` и `"не найден" in result.stderr`. Запусти тесты. Ожидаемый результат: все проверки проходят.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Тип опции: `greeting: str = typer.Option("Привет", help="Слово приветствия")`. Имя опции typer выведет из имени переменной: `--greeting`. Не забудь `if __name__ == "__main__": app()` для запуска из файла.

### Подсказка 2
Импортируй `from typing import List`. Сигнатура: `def total(numbers: List[int])`. Сумма — `sum(numbers)`. Typer преобразует строки из командной строки в int автоматически.

### Подсказка 3
Используй `from pathlib import Path`. Проверка: `if not path.exists():`. Для stderr: `typer.echo(..., err=True)`. Завершение: `raise typer.Exit(code=1)`. Размер: `path.stat().st_size`.

### Подсказка 4
Один `runner` на модуль: `runner = CliRunner()`. Каждый тест — отдельная функция с `result = runner.invoke(app, [...])`. Проверяй `result.exit_code` и `result.stdout`. Импортируй `app` из `cli.py`.

### Подсказка 5
Используй `with runner.isolated_filesystem():` — внутри текущая директория временная. Создавай файл: `Path("data.txt").write_text("привет", encoding="utf-8")`. Для проверки размера сравни `"data.txt" in result.stdout` и не сравнивай точное число: оно зависит от текста. stderr: `result.stderr`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полное решение (файл `cli.py`):

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str, greeting: str = typer.Option("Привет", help="Слово приветствия")):
    """Поздороваться с пользователем."""
    typer.echo(f"{greeting}, {name}!")

if __name__ == "__main__":
    app()
```

Разбор. Typer читает аннотации типов: `name: str` становится обязательным позиционным аргументом, `greeting: str = typer.Option(...)` — опцией с дефолтом `Привет`. Имя опции `--greeting` генерируется из имени переменной. `typer.echo` — аналог `print`, но с правильной обработкой юникода и кодировок. Запуск `python cli.py hello Аня` выводит `Привет, Аня!`; передача `--greeting Здравствуйте` меняет слово. Флаг `--help` сгенерирован автоматически: typer задействует docstring функции как описание. Обрати внимание: ничего вручную парсить не нужно — весь синтаксический разбор делает библиотека.

### Разбор 2
Полное решение (добавляем в `cli.py`):

```python
from typing import List

@app.command()
def total(numbers: List[int]):
    """Сумма переданных чисел."""
    typer.echo(sum(numbers))
```

Разбор. Аннотация `List[int]` означает, что команда принимает произвольное число чисел. Typer преобразует каждую строку CLI в `int` (а если это невозможно — выведет понятную ошибку с подсказкой). Если чисел не передано, `numbers` — пустой список, и `sum([])` возвращает `0`, поэтому `python cli.py total` корректно выводит `0`. Такой вариант изящнее, чем вручную парсить `sys.argv` и конвертировать типы с проверками.

### Разбор 3
Полное решение (добавляем в `cli.py`):

```python
from pathlib import Path

@app.command()
def file_info(path: Path):
    """Показать размер файла."""
    if not path.exists():
        typer.echo(f"Файл не найден: {path}", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"{path.name}: {path.stat().st_size} байт")
```

Разбор. `path: Path` заставляет typer преобразовать строку CLI в объект `pathlib.Path`. Если файл отсутствует — сообщение об ошибке уходит в stderr (`err=True`), а `typer.Exit(code=1)` завершает процесс с кодом 1: так оболочка и CI поймут, что команда провалилась. В успешном случае печатается имя файла и размер из `stat().st_size`. Это минимальный, но «правильный» CLI: с понятными ошибками и кодами возврата.

### Разбор 4
Полное решение (файл `test_cli.py`):

```python
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_hello_default_greeting():
    result = runner.invoke(app, ["hello", "Аня"])
    assert result.exit_code == 0
    assert "Привет, Аня!" in result.stdout

def test_hello_custom_greeting():
    result = runner.invoke(app, ["hello", "Аня", "--greeting", "Здравствуйте"])
    assert result.exit_code == 0
    assert "Здравствуйте, Аня!" in result.stdout

def test_total_three_numbers():
    result = runner.invoke(app, ["total", "1", "2", "3"])
    assert result.exit_code == 0
    assert "6" in result.stdout

def test_total_empty():
    result = runner.invoke(app, ["total"])
    assert result.exit_code == 0
    assert "0" in result.stdout
```

Разбор. `CliRunner` запускает приложение in-process: без поднятия процесса, быстро и безопасно. `runner.invoke(app, ["hello", "Аня"])` — ровно то же, что `python cli.py hello Аня`. Результат проверяется по `exit_code` (0 — успех) и содержанию `stdout`. Тесты покрывают и дефолтное приветствие, и опцию, и сумму, и граничный случай пустого списка. Это «золотая» привычка: каждая команда и каждая ветка — в тестах.

### Разбор 5
Полное решение (добавляем в `test_cli.py`):

```python
from pathlib import Path

def test_file_info_existing_file():
    with runner.isolated_filesystem():
        Path("data.txt").write_text("Привет, мир!", encoding="utf-8")
        result = runner.invoke(app, ["file-info", "data.txt"])
        assert result.exit_code == 0
        assert "data.txt" in result.stdout
        assert "байт" in result.stdout

def test_file_info_missing_file():
    result = runner.invoke(app, ["file-info", "missing.txt"])
    assert result.exit_code == 1
    assert "не найден" in result.stderr
```

Разбор. `runner.isolated_filesystem()` создаёт временную рабочую директорию на время блока — файлы, созданные внутри, существуют только там и удаляются после теста. Первый тест пишет `data.txt` и проверяет успешный сценарий: код 0, имя файла и слово «байт» в выводе (точный размер не сравниваем — он зависит от кодировки, поэтому проверяем форму вывода). Второй тест — «счастливый путь» отсутствия файла: код 1 и сообщение в `stderr`. Именно так тестируются утилиты командной строки: через реальный вызов, с временными файлами и без ручного запуска терминала.
<!--/SOLUTION-->

<!--QUIZ-->
Что используется для создания команды в typer?
- @app.command() над функцией
- typer.cmd()
- @command
- class Command
* Правильный ответ: @app.command() над функцией
Декоратор регистрирует функцию как команду CLI.

Как объявить позиционный аргумент?
- name: str
- name = typer.Argument()
- @arg("name")
- typer.positional("name")
* Правильный ответ: name: str
Аннотация типа делает параметр позиционным аргументом.

Как объявить опцию с дефолтом?
- greeting: str = typer.Option("Привет")
- greeting = "Привет"
- @option(greeting)
- typer.flag(greeting)
* Правильный ответ: greeting: str = typer.Option("Привет")
typer.Option создаёт опцию --greeting с заданным значением по умолчанию.

Что делает typer.echo()?
- Выводит текст (аналог print) с правильной кодировкой
- Возвращает текст
- Читает ввод пользователя
- Подсвечивает текст
* Правильный ответ: Выводит текст (аналог print) с правильной кодировкой
typer.echo печатает в stdout, корректно обрабатывая юникод.

Как завершить команду с кодом ошибки?
- raise typer.Exit(code=1)
- return 1
- sys.exit(1) в любом месте
- typer.error()
* Правильный ответ: raise typer.Exit(code=1)
Exit немедленно останавливает выполнение и задаёт код возврата.

Как тестировать команды typer?
- Через CliRunner из typer.testing
- Только запуском процесса
- Через unittest.mock
- Тестировать CLI нельзя
* Правильный ответ: Через CliRunner из typer.testing
CliRunner.invoke(app, args) запускает команду in-process.

Что содержит result.exit_code при успехе?
- 0
- 1
- Текст вывода
- None
* Правильный ответ: 0
Код 0 означает успешное завершение.

Что делает runner.isolated_filesystem()?
- Создаёт временную папку на время блока
- Изолирует сеть
- Останавливает другие команды
- Сохраняет вывод в файл
* Правильный ответ: Создаёт временную папку на время блока
Файлы внутри блока существуют только во временной директории.

Как принять несколько чисел в команде?
- numbers: List[int]
- numbers: int[]
- numbers: str
- Невозможно
* Правильный ответ: numbers: List[int]
Typer принимает произвольное число значений и преобразует их в int.

Зачем typer нужен docstring функции?
- Он выводится в --help
- Он ускоряет выполнение
- Он не нужен
- Он заменяет код
* Правильный ответ: Он выводится в --help
Docstring становится описанием команды в справке.
<!--/QUIZ-->
