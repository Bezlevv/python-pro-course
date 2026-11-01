---
title: Логирование (logging)
summary: Профессиональная запись событий программы: уровни, форматы, обработчики и логирование ошибок.
order: 3
duration: 30 мин
difficulty: intermediate
---

Когда программа маленькая, для отладки хватает `print()`. Но в реальном проекте нужно знать не только «что произошло», но и когда, насколько это серьёзно, и куда записать событие. Для этого в Python есть модуль `logging` — встроенная система журналирования.

## Уровни логирования

Каждое сообщение имеет уровень важности. По возрастанию: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. По умолчанию выводятся сообщения от `WARNING` и выше — то есть `DEBUG` и `INFO` по умолчанию скрыты:

```python
import logging

logging.debug("Отладка")          # не выведется (уровень ниже WARNING)
logging.info("Программа запущена") # не выведется
logging.warning("Мало места на диске")
logging.error("Ошибка чтения файла")
```

Результат:

```
WARNING:root:Мало места на диске
ERROR:root:Ошибка чтения файла
```

## Настройка basicConfig

Функция `basicConfig` задаёт уровень, формат и место вывода. В формате используются плейсхолдеры: `%(asctime)s` — время, `%(levelname)s` — уровень, `%(message)s` — сам текст:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logging.info("Старт программы")
logging.warning("Внимание: мало места")
```

Теперь `INFO`-сообщения видны, и у каждой строки есть временная метка.

## Логгеры и обработчики

Глобальная настройка удобна в маленьких скриптах, но в больших проектах используют именованные логгеры — по одному на модуль:

```python
import logging

logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("app.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(handler)

logger.info("Это уйдёт и в файл app.log")
```

Обработчик (`handler`) решает, куда писать: в консоль (`StreamHandler`), в файл (`FileHandler`) или куда-то ещё. Можно добавить несколько обработчиков — например, в файл и на консоль одновременно.

## Логирование ошибок

В блоке `except` используй `logger.exception(...)` — он запишет сообщение с уровнем `ERROR` и добавит полный след исключения (traceback):

```python
logger = logging.getLogger("my_app")

try:
    1 / 0
except ZeroDivisionError:
    logger.exception("Деление на ноль")
```

Ещё один нюанс: не подставляй значения в текст через f-строки, если в этом нет необходимости. Лучше передавать их аргументами: `logger.info("Пользователь %s зашёл", user)` — форматирование произойдёт только если сообщение действительно будет выведено, а это быстрее.

## Итог урока

Мы узнали, чем `logging` лучше `print` (уровни, времена, направления вывода), как настраивать `basicConfig`, как делать именованные логгеры с обработчиками и как логировать исключения. Теперь применим это в настоящей программе.

<!--TASK-->
**Задача.** Напиши программу `log_calc.py` — простой калькулятор с логированием:

1. Программа в цикле просит ввести выражение вида `число операция число` (например, `10 + 5`), считает и печатает результат;
2. Каждое успешно выполненное действие логируется на уровне `INFO` с сообщением вида `Вычисление: 10 + 5 = 15`;
3. Если ввод непонятный (не три части, неизвестная операция) — логируется `WARNING`;
4. Если происходит ошибка вычисления (например, деление на ноль) — логируется `ERROR` со следом исключения;
5. Логи пишутся и в консоль, и в файл `calc.log` с временем, уровнем и сообщением.

Ожидаемый результат: во время сессии в консоли видны строки логов, а в файле `calc.log` лежит история сессии с временными метками. Выход из цикла — по слову `выход`.
<!--/TASK-->

<!--HINT-->
Создай логгер `logging.getLogger("calc")` с уровнем `INFO`, добавь ему два обработчика: `StreamHandler` (консоль) и `FileHandler("calc.log", encoding="utf-8")`, обоим задай один и тот же `Formatter`. Разбирай ввод через `line.split()` и `float()`. В `except` используй `logger.exception(...)` для ошибок вычисления.
<!--/HINT-->

<!--SOLUTION-->
Одно из возможных решений:

```python
import logging

logger = logging.getLogger("calc")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

console = logging.StreamHandler()
console.setFormatter(formatter)

file_handler = logging.FileHandler("calc.log", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file_handler)

logger.info("Калькулятор запущен")

while True:
    line = input("Введи выражение (например, 10 + 5) или 'выход': ").strip()
    if line.lower() == "выход":
        logger.info("Работа завершена")
        break

    parts = line.split()
    if len(parts) != 3:
        logger.warning(f"Непонятный ввод: {line!r}")
        continue

    try:
        a, op, b = float(parts[0]), parts[1], float(parts[2])
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = a / b
        else:
            logger.warning(f"Неизвестная операция: {op}")
            continue
        logger.info(f"Вычисление: {a:g} {op} {b:g} = {result:g}")
        print(f"Результат: {result:g}")
    except ZeroDivisionError:
        logger.exception("Деление на ноль")
    except ValueError:
        logger.warning("Не удалось разобрать числа")
```

Пример сессии:

```
Введи выражение (например, 10 + 5) или 'выход': 10 + 5
2024-01-15 12:00:01,123 | INFO | Калькулятор запущен
2024-01-15 12:00:05,456 | INFO | Вычисление: 10 + 5 = 15
Результат: 15
Введи выражение (например, 10 + 5) или 'выход': 5 / 0
2024-01-15 12:00:12,789 | ERROR | Деление на ноль
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
Введи выражение (например, 10 + 5) или 'выход': выход
2024-01-15 12:00:20,000 | INFO | Работа завершена
```

Разбор шагов. Логгер `calc` получает уровень `INFO` — значит, сообщения `INFO` и выше будут записываться. Ему добавлены два обработчика с одинаковым форматом: один пишет в консоль, другой — в файл `calc.log`, поэтому история сессии сохраняется. Ввод разбивается на три части; если частей не три — это `WARNING` (не настолько серьёзно, чтобы прерывать программу). Сами вычисления обёрнуты в `try/except`: `ZeroDivisionError` логируется через `logger.exception`, который добавляет к сообщению полный трейсбек, а `ValueError` от `float()` — через `logger.warning`. Так по файлу лога можно восстановить весь ход сессии — это главное преимущество перед `print`.
<!--/SOLUTION-->
