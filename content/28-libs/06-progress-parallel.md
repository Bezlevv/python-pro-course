---
title: tqdm и параллельная обработка с прогрессом
summary: Прогресс-бары tqdm и пулы concurrent.futures: параллелим IO-задачи, показываем прогресс и покрываем тестами.
order: 6
duration: 35 мин
difficulty: intermediate
tags: tqdm, concurrent.futures, параллельность, прогресс, pytest
---

Долгие скрипты без обратной связи заставляют гадать: «оно ещё работает или зависло?». `tqdm` решает эту проблему красивыми прогресс-барами, а `concurrent.futures` позволяет выполнять задачи параллельно. Вместе это даёт быстрые и наглядные утилиты.

## Установка

```bash
pip install tqdm
```

## tqdm: простой прогресс

```python
from tqdm import tqdm
from time import sleep

for i in tqdm(range(100), desc="Обработка", unit="шаг"):
    sleep(0.02)
```

В терминале появится полоса с процентами, скоростью и оставшимся временем. Параметр `desc` — подпись слева, `unit` — название единицы («шаг», «файл»). Контекстный менеджер тоже работает:

```python
with tqdm(total=100, desc="Загрузка") as pbar:
    for _ in range(100):
        sleep(0.01)
        pbar.update(1)
```

`update(1)` увеличивает счётчик вручную — удобно, когда итерации не равнозначны.

## Параллельность: ThreadPoolExecutor

`concurrent.futures` — стандартный модуль для пулов. `ThreadPoolExecutor` — для IO-задач (сеть, файлы): потоки упираются в ожидание ввода-вывода, а не в процессор.

```python
from concurrent.futures import ThreadPoolExecutor

def double(x):
    return x * 2

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(double, range(10)))
print(results)  # [0, 2, 4, ..., 18]
```

`pool.map(func, iterable)` применяет функцию к каждому элементу и возвращает результаты в том же порядке, что и входные данные. Для CPU-задач, которые реально грузят процессор, используют `ProcessPoolExecutor` — он обходит GIL за счёт отдельных процессов.

## Результаты по мере готовности: as_completed

`map` хорош, когда важен порядок. Если порядок не важен, а хочется обрабатывать результаты по мере появления, используют `submit` + `as_completed`:

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(double, x) for x in range(10)]
    for future in as_completed(futures):
        print(future.result())
```

## Соединяем: прогресс + параллельность

Самый частый паттерн утилит — параллельная работа с прогресс-баром:

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(double, x) for x in range(20)]
    for future in tqdm(as_completed(futures), total=20, desc="Считаю"):
        future.result()
```

`tqdm` оборачивает `as_completed`, а `total=20` сообщает общее число задач (иначе бар не знает длины). Так можно показывать, сколько задач уже завершилось.

## Тестирование параллельного кода

Параллельность не должна мешать тестам: функции, которые выполняют работу, должны оставаться чистыми и детерминированными. Мы оттестируем и `parallel_map`, и функцию хэширования файлов — без сети и без реальной задержки.

<!--TASK-->
### Задача 1
Напиши функцию `count_down(n)`, которая использует `tqdm(range(n), desc="Обработка", unit="шаг")` и внутри цикла делает `sleep(0.05)`. После цикла выведи `Готово!`. Проверь вручную: запусти `count_down(20)` — должна появиться полоса прогресса и сообщение. Ожидаемый результат: функция работает, показывает прогресс и печатает `Готово!`.

### Задача 2
Напиши функцию `parallel_map(func, items, max_workers=4)`, которая использует `ThreadPoolExecutor` и возвращает список результатов в порядке входных данных (через `list(pool.map(func, items))`). Проверь вручную: `parallel_map(lambda x: x * x, [1, 2, 3])` возвращает `[1, 4, 9]`. Ожидаемый результат: порядок и значения результатов совпадают с последовательным вызовом.

### Задача 3
Напиши функции `sha256_of_file(path)` и `hash_files(paths, max_workers=4)`. Первая читает файл байтами (`path.read_bytes()`) и возвращает `hashlib.sha256(...).hexdigest()`. Вторая создаёт `ThreadPoolExecutor`, отправляет все пути через `pool.submit(sha256_of_file, p)`, оборачивает `as_completed` в `tqdm` с `total=len(paths)` и `desc="Хэширую"`, и собирает словарь `{путь: хэш}`. Проверь вручную на паре файлов. Ожидаемый результат: словарь содержит хэш для каждого файла, совпадающий с прямым вычислением.

### Задача 4
Напиши pytest-тесты для `parallel_map`: (1) `parallel_map(lambda x: x * 2, [1, 2, 3, 4])` возвращает `[2, 4, 6, 8]`; (2) порядок результатов совпадает с порядком входов; (3) пустой список возвращает `[]`; (4) при исключении в функции (например, `lambda x: 1 // 0`) `pytest.raises(ZeroDivisionError)` срабатывает при обращении к результату. Запусти `python -m pytest test_parallel.py -v`. Ожидаемый результат: все 4 теста проходят.

### Задача 5
Напиши pytest-тесты для `hash_files`: в `tmp_path` создай три файла с известным содержимым (`b"abc"`, `b"def"`, `b"123"`). Проверь: (1) результат — словарь, где ключи — пути, а значения совпадают с `hashlib.sha256(содержимое).hexdigest()`; (2) `len(result) == 3`; (3) для несуществующего пути `pytest.raises(FileNotFoundError)` при вызове `hash_files([missing])`. Запусти тесты. Ожидаемый результат: все проверки проходят.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`for i in tqdm(range(n), desc="Обработка", unit="шаг"):` — внутри `sleep(0.05)`. `print("Готово!")` после цикла.

### Подсказка 2
Используй `with ThreadPoolExecutor(max_workers=max_workers) as pool:`; внутри `return list(pool.map(func, items))`. Импорт: `from concurrent.futures import ThreadPoolExecutor`.

### Подсказка 3
Хэш: `hashlib.sha256(path.read_bytes()).hexdigest()`. В `hash_files` создай `futures = [pool.submit(sha256_of_file, p) for p in paths]`, затем цикл `for future in tqdm(as_completed(futures), total=len(paths), desc="Хэширую")` с сборкой словаря. Импорты: `hashlib`, `as_completed`, `tqdm`, `ThreadPoolExecutor`.

### Подсказка 4
Исключение из `map` всплывает при итерации: `with pytest.raises(ZeroDivisionError): list(parallel_map(lambda x: 1 // 0, [1]))`. Проверку порядка делай на списке из 4-5 элементов с разными значениями.

### Подсказка 5
Создавай файлы: `Path(tmp_path / "a.txt").write_bytes(b"abc")`. Ожидаемый хэш: `hashlib.sha256(b"abc").hexdigest()`. Для отсутствующего пути не создавай файл и передай путь, которого нет.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полное решение:

```python
from time import sleep
from tqdm import tqdm

def count_down(n):
    for i in tqdm(range(n), desc="Обработка", unit="шаг"):
        sleep(0.05)
    print("Готово!")
```

Разбор. `tqdm(range(n), ...)` оборачивает итерируемый объект: на каждой итерации бар автоматически увеличивается. `desc` добавляет подпись слева, `unit` — название единицы после счётчика (например, `20.0 шаг/с`). `sleep(0.05)` имитирует полезную работу — в реальном коде здесь был бы запрос, вычисление или обработка файла. По завершении цикла печатается `Готово!`. Такой бар — дешёвый способ сделать любой долгий скрипт понятным.

### Разбор 2
Полное решение:

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_map(func, items, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(func, items))
```

Разбор. `ThreadPoolExecutor(max_workers=4)` создаёт пул из четырёх потоков. `pool.map(func, items)` выполняет `func` для каждого элемента параллельно, но возвращает результаты в порядке входных данных — это ключевое отличие от `as_completed`, где порядок произвольный. Контекстный менеджер `with` гарантирует, что потоки завершатся и ресурсы освободятся. Обёртка в `list(...)` материализует итератор — без неё исключения из воркеров всплыли бы только при переборе. Эта функция — универсальный инструмент для параллельного применения любой «чистой» функции.

### Разбор 3
Полное решение:

```python
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def sha256_of_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hash_files(paths, max_workers=4):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(sha256_of_file, p) for p in paths]
        for future in tqdm(as_completed(futures), total=len(paths),
                           desc="Хэширую"):
            path = paths[futures.index(future)]
            results[path] = future.result()
    return results
```

Разбор. `sha256_of_file` — чистая функция: читает файл целиком (`read_bytes`) и возвращает hex-хэш. `hash_files` отправляет пути в пул через `submit` — каждый вызов становится «будущим» объектом `Future`. `as_completed(futures)` отдаёт завершившиеся будущие объекты по мере готовности, а `tqdm(...)` вокруг него показывает прогресс; `total=len(paths)` задаёт длину бара, потому что `as_completed` сам по себе её не знает. Чтобы узнать путь завершившегося будущего, ищем его индекс в списке `futures`. Словарь результатов собирается по мере готовности — для большого числа файлов это заметно быстрее последовательного перебора.

### Разбор 4
Полное решение:

```python
import pytest
from parallel_utils import parallel_map

def test_parallel_map_values():
    assert parallel_map(lambda x: x * 2, [1, 2, 3, 4]) == [2, 4, 6, 8]

def test_parallel_map_preserves_order():
    items = list(range(10))
    assert parallel_map(lambda x: x + 100, items) == [x + 100 for x in items]

def test_parallel_map_empty():
    assert parallel_map(lambda x: x, []) == []

def test_parallel_map_raises():
    with pytest.raises(ZeroDivisionError):
        list(parallel_map(lambda x: 1 // 0, [1]))
```

Разбор. Первые два теста проверяют значения и порядок: `map` гарантирует соответствие индексов, и это поведение стоит закрепить тестом — при переходе на `as_completed` оно сломается. Третий тест — пустой вход. Четвёртый — поведение при исключении: ошибка из воркера всплывает при итерации по результатам, поэтому мы материализуем `list(...)` внутри `pytest.raises`. Тесты используют только чистые лямбды, без сети и задержек, поэтому они мгновенные и детерминированные.

### Разбор 5
Полное решение:

```python
import hashlib
import pytest
from pathlib import Path
from parallel_utils import hash_files

def test_hash_files_correct(tmp_path):
    data = {"a.txt": b"abc", "b.txt": b"def", "c.txt": b"123"}
    paths = []
    for name, content in data.items():
        p = tmp_path / name
        p.write_bytes(content)
        paths.append(p)

    result = hash_files(paths)

    assert len(result) == 3
    for p, content in zip(paths, data.values()):
        assert result[p] == hashlib.sha256(content).hexdigest()

def test_hash_files_missing_raises(tmp_path):
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        hash_files([missing])
```

Разбор. Первый тест создаёт три файла с известным содержимым и сравнивает результат `hash_files` с эталонным вычислением `hashlib.sha256(...)`. Словарь проверяется по ключам-путям: `result[p]` — хэш именно этого файла. Второй тест покрывает граничный случай: `read_bytes()` на несуществующем пути бросает `FileNotFoundError`, и исключение всплывает при обращении к `future.result()`, поэтому `pytest.raises` оборачивает вызов целиком. Такие тесты гарантируют, что параллельная логика не подменила содержимое и корректно обрабатывает ошибки.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает tqdm(range(100))?
- Показывает прогресс-бар по итерациям
- Ускоряет цикл
- Превращает range в список
- Печатает числа
* Правильный ответ: Показывает прогресс-бар по итерациям
Параметр оборачивает итерируемый объект и отображает прогресс.

Что означает параметр desc?
- Количество итераций
- Подпись слева от полосы
- Единицу измерения
- Скорость выполнения
* Правильный ответ: Подпись слева от полосы
desc задаёт текст, описывающий выполняемую работу.

Как вручную увеличить счётчик бара?
- pbar.update(1)
- pbar.inc()
- pbar.next(1)
- pbar += 1
* Правильный ответ: pbar.update(1)
update(n) увеличивает текущее значение на n.

Когда ThreadPoolExecutor ускоряет работу?
- На IO-задачах (сеть, файлы)
- На CPU-задачах в любом случае
- Только в одном потоке
- Никогда
* Правильный ответ: На IO-задачах (сеть, файлы)
Потоки ждут ввода-вывода, и параллельные ожидания сокращают общее время.

Какой пул использовать для тяжёлых вычислений?
- ProcessPoolExecutor
- ThreadPoolExecutor
- MultipoolExecutor
- Только цикл for
* Правильный ответ: ProcessPoolExecutor
Отдельные процессы обходят GIL и используют несколько ядер.

Что возвращает pool.map(func, items)?
- Список результатов в порядке входных данных
- Набор будущих объектов
- Итератор в произвольном порядке
- Ничего
* Правильный ответ: Список результатов в порядке входных данных
map сохраняет соответствие индексов.

Что делает as_completed(futures)?
- Возвращает выполнившиеся будущие объекты по мере готовности
- Выполняет все задачи
- Останавливает пул
- Сортирует результаты
* Правильный ответ: Возвращает выполнившиеся будущие объекты по мере готовности
as_completed отдаёт результаты сразу, как только они готовы.

Как показать прогресс для as_completed?
- tqdm(as_completed(futures), total=len(futures))
- tqdm(futures)
- Прогресс для него невозможен
- as_completed(tqdm(futures))
* Правильный ответ: tqdm(as_completed(futures), total=len(futures))
Бар нуждается в total, так как as_completed не знает длины.

Что произойдёт при исключении в воркере ThreadPoolExecutor?
- Ошибка всплывает при обращении к результату
- Исключение молча игнорируется
- Пул останавливается навсегда
- Программа завершается с кодом 0
* Правильный ответ: Ошибка всплывает при обращении к результату
future.result() или итерация по map пробрасывают исключение.

Что делает hash_files(paths) из урока?
- Хэширует файлы параллельно и возвращает словарь путей и хэшей
- Удаляет файлы
- Сортирует файлы по размеру
- Копирует файлы
* Правильный ответ: Хэширует файлы параллельно и возвращает словарь путей и хэшей
Каждый путь сопоставляется с SHA-256 хэшем содержимого.
<!--/QUIZ-->
