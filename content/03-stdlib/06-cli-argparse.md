---
title: CLI-утилиты: argparse
summary: Создаём профессиональные программы командной строки: аргументы, флаги, значения по умолчанию и подкоманды.
order: 6
duration: 40 мин
difficulty: advanced
---

Многие программы запускаются из терминала и принимают аргументы: `python script.py data.txt --verbose`. Разбор этих аргументов — целая наука: нужно поддерживать и позиционные значения, и флаги, и значения по умолчанию, и понятные сообщения об ошибках. Всё это умеет модуль `argparse` из стандартной библиотеки.

## Простейший парсер

`ArgumentParser` описывает, какие аргументы принимает программа, а `parse_args()` разбирает команду из `sys.argv`:

```python
import argparse

parser = argparse.ArgumentParser(description="Считает сумму чисел")
parser.add_argument("numbers", type=float, nargs="+", help="числа для сложения")
parser.add_argument("--verbose", action="store_true", help="подробный вывод")
args = parser.parse_args()

total = sum(args.numbers)
if args.verbose:
    print(f"Сумма чисел {args.numbers} равна {total}")
else:
    print(total)
```

Запуск:

```bash
python sum_cli.py 1 2.5 3
python sum_cli.py 1 2.5 3 --verbose
```

Что здесь произошло? `numbers` — позиционный аргумент: он обязателен и берётся из позиции в команде. `nargs="+"` означает «одно или несколько значений». `--verbose` — флаг: `action="store_true"` делает его булевым, `True`, если флаг передан, иначе `False`.

## Типы и значения по умолчанию

`argparse` сам преобразует строки в нужные типы и проверяет их:

```python
parser.add_argument("-n", "--top", type=int, default=10, help="сколько слов показать")
parser.add_argument("--format", choices=["text", "csv"], default="text", help="формат вывода")
```

Если `type=int` не сможет преобразовать значение, парсер сам напечатает ошибку и завершит программу с кодом 2. `choices` ограничивает допустимые значения, `default` задаёт значение по умолчанию, если флаг не передан.

## Подкоманды

Сложные утилиты (как `git commit`, `pip install`) имеют подкоманды. Их делают через `add_subparsers`:

```python
subparsers = parser.add_subparsers(dest="command", required=True)

add_parser = subparsers.add_parser("add", help="сложить числа")
add_parser.add_argument("numbers", nargs="+", type=float)

mul_parser = subparsers.add_parser("mul", help="умножить числа")
mul_parser.add_argument("numbers", nargs="+", type=float)
```

Теперь `python calc.py add 1 2 3` и `python calc.py mul 2 4` — две разные подкоманды с собственными аргументами.

## Помощь и ошибки

Парсер автоматически генерирует справку: `python script.py --help` покажет описание всех аргументов. Для собственных ошибок есть `parser.error("сообщение")` — он печатает сообщение, подсказку использования и завершает программу.

## Итог урока

Мы разобрали argparse: позиционные аргументы, флаги, типы, `default`, `choices`, подкоманды и автоматическую справку. Теперь соберём настоящую CLI-утилиту.

<!--TASK-->
**Задача.** Создай CLI-утилиту `words.py` для анализа текстового файла:

1. Позиционный аргумент `path` — путь к текстовому файлу;
2. Флаг `-n` / `--top` (по умолчанию 10) — сколько самых частых слов показать;
3. Флаг `--no-stopwords` — убрать из подсчёта служебные слова (предлоги и союзы: «и», «в», «на», «с», «по», «для», «что», «это», «как», «не»);
4. Если файла не существует — программа печатает понятное сообщение об ошибке и завершается с ненулевым кодом;
5. Вывод: каждая строка вида `слово: количество`, отсортировано по убыванию частоты.

Создай тестовый файл `text.txt` с 20–30 словами и проверь утилиту с разными флагами.

Ожидаемый результат: `python words.py text.txt` печатает топ-10 слов; `python words.py text.txt -n 3 --no-stopwords` — топ-3 без служебных слов.
<!--/TASK-->

<!--HINT-->
Объяви `parser.add_argument("path")`, `parser.add_argument("-n", "--top", type=int, default=10)`, `parser.add_argument("--no-stopwords", action="store_true")`. Проверяй существование файла через `Path(args.path).exists()` и прерывай парсер через `parser.error(...)`. Считай частоту через `Counter` из `collections` и выводи через `most_common(args.top)`.
<!--/HINT-->

<!--SOLUTION-->
Одно из возможных решений:

```python
import argparse
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "и", "в", "на", "с", "по", "для", "что", "это",
    "как", "не", "а", "но", "или", "из", "к", "у", "о", "от",
}

parser = argparse.ArgumentParser(description="Топ самых частых слов в файле")
parser.add_argument("path", help="путь к текстовому файлу")
parser.add_argument("-n", "--top", type=int, default=10,
                    help="сколько слов показать (по умолчанию 10)")
parser.add_argument("--no-stopwords", action="store_true",
                    help="убрать служебные слова")
args = parser.parse_args()

file_path = Path(args.path)
if not file_path.exists():
    parser.error(f"Файл не найден: {args.path}")

text = file_path.read_text(encoding="utf-8")
words = re.findall(r"[а-яёa-z]+", text.lower())

if args.no_stopwords:
    words = [w for w in words if w not in STOPWORDS]

for word, count in Counter(words).most_common(args.top):
    print(f"{word}: {count}")
```

Примеры запуска:

```bash
$ python words.py text.txt
и: 4
в: 3
питон: 3
код: 2
...

$ python words.py text.txt -n 3 --no-stopwords
питон: 3
код: 2
язык: 2

$ python words.py no_such_file.txt
usage: words.py [-h] [-n TOP] [--no-stopwords] path
words.py: error: Файл не найден: no_such_file.txt
```

Разбор шагов. Сначала `ArgumentParser` описывает интерфейс: обязательный путь, опциональный `-n/--top` с типом `int` и значением по умолчанию 10, и флаг `--no-stopwords` с `action="store_true"`. `parse_args()` собирает всё в объект `args`, и дальше мы обращаемся к нему как к обычным атрибутам. Существование файла проверяется до чтения: `parser.error` печатает подсказку использования и завершает программу с ненулевым кодом (2) — это стандартное поведение CLI-утилит. Слова извлекаются регулярным выражением, приводятся к нижнему регистру, а при `--no-stopwords` отфильтровываются через множество стоп-слов. Наконец, `Counter(words).most_common(args.top)` сразу даёт отсортированный топ — цикл печатает пары «слово: количество». Обрати внимание, как `-h/--help` тоже работает бесплатно: argparse сам генерирует справку.
<!--/SOLUTION-->
