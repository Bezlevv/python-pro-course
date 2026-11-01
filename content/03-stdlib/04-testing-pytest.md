---
title: Тестирование: pytest
summary: Пишем автоматические тесты: assert, параметризация, обработка исключений и фикстуры в pytest.
order: 4
duration: 35 мин
difficulty: intermediate
---

Ты наверняка знаком с ситуацией: дописал функцию, всё работает — а через неделю после правки что-то сломалось. Автоматические тесты решают эту проблему: они запускаются за секунды и сразу говорят, какая функция ведёт себя не так. В Python стандарт де-факто — фреймворк `pytest`. Его нужно установить: `pip install pytest`.

## Как устроен тест

Тест — это обычная функция, имя которой начинается с `test_`. Внутри — проверки через `assert`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

Если `assert` вернёт `False`, pytest сообщит, какой тест упал и с какими значениями. Запуск — из терминала:

```bash
python -m pytest
```

pytest сам найдёт все файлы вида `test_*.py` и функции `test_*` в текущей папке.

## Полезные флаги

```bash
python -m pytest -v                    # подробный вывод по каждому тесту
python -m pytest test_discount.py       # только конкретный файл
python -m pytest -k "discount"          # тесты, в имени которых есть слово
python -m pytest --maxfail=1            # остановиться после первой ошибки
```

## Параметризация

Если нужно проверить функцию на многих наборах данных, не пиши десять почти одинаковых функций — используй `@pytest.mark.parametrize`:

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

pytest выполнит этот тест трижды — по одному разу на каждый набор аргументов.

## Проверка исключений

Если функция должна бросать исключение, ожидай его через `pytest.raises`:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("деление на ноль")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

Тест пройдёт, только если внутри блока `with` действительно возникнет `ValueError`.

## Фикстуры

Фикстура (fixture) — это подготовка данных, которой пользуются несколько тестов. Она помечается `@pytest.fixture` и передаётся тесту как аргумент:

```python
@pytest.fixture
def numbers():
    return [3, 1, 2]

def test_sorted(numbers):
    assert sorted(numbers) == [1, 2, 3]
```

Фикстуры можно складывать в общий файл `conftest.py`, чтобы ими пользовались все тесты проекта.

## Итог урока

Мы узнали, как писать тесты на pytest: функции `test_*`, проверки `assert`, параметризация, `pytest.raises` для исключений и фикстуры для подготовки данных. Теперь напишем тесты для настоящей функции.

<!--TASK-->
**Задача.** Напиши функцию `calc_discount(price, discount)`, которая возвращает цену со скидкой по формуле `price * (1 - discount / 100)`. Правила: если `price` отрицательная — `ValueError`; если `discount` не в диапазоне от 0 до 100 — `ValueError`.

Создай файл `test_discount.py` с тестами:

1. Параметризованный тест для обычных случаев: `(200, 10, 180.0)`, `(100, 0, 100.0)`, `(50, 100, 0.0)`, `(80, 25, 60.0)`;
2. Тест: скидка 150 вызывает `ValueError`;
3. Тест: отрицательная цена вызывает `ValueError`.

Запусти `python -m pytest test_discount.py -v` и добейся, чтобы все тесты прошли.

Ожидаемый результат: pytest сообщает о 6 пройденных тестах (4 параметризованных + 2 на ошибки) без единой ошибки.
<!--/TASK-->

<!--HINT-->
Для параметризации используй `@pytest.mark.parametrize("price,discount,expected", [...])`. Для проверки ошибок — `with pytest.raises(ValueError): calc_discount(...)`. Обрати внимание на тип результата: деление в Python возвращает `float`, поэтому сравнивай со значениями вроде `180.0`.
<!--/HINT-->

<!--SOLUTION-->
Функция в файле `discount.py`:

```python
def calc_discount(price, discount):
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    if not 0 <= discount <= 100:
        raise ValueError("Скидка должна быть от 0 до 100")
    return price * (1 - discount / 100)
```

Тесты в файле `test_discount.py`:

```python
import pytest
from discount import calc_discount

@pytest.mark.parametrize("price,discount,expected", [
    (200, 10, 180.0),
    (100, 0, 100.0),
    (50, 100, 0.0),
    (80, 25, 60.0),
])
def test_calc_discount(price, discount, expected):
    assert calc_discount(price, discount) == expected

def test_discount_too_large():
    with pytest.raises(ValueError):
        calc_discount(100, 150)

def test_negative_price():
    with pytest.raises(ValueError):
        calc_discount(-50, 10)
```

Запуск и результат:

```bash
python -m pytest test_discount.py -v
```

```
============================= test session starts ==============================
collected 6 items

test_discount.py::test_calc_discount[200-10-180.0] PASSED              [ 16%]
test_discount.py::test_calc_discount[100-0-100.0] PASSED               [ 33%]
test_discount.py::test_calc_discount[50-100-0.0] PASSED                [ 50%]
test_discount.py::test_calc_discount[80-25-60.0] PASSED                [ 66%]
test_discount.py::test_calc_discount_too_large PASSED                  [ 83%]
test_discount.py::test_calc_discount_negative_price PASSED             [100%]

============================== 6 passed in 0.03s ===============================
```

Разбор шагов. Функция `calc_discount` сначала валидирует входные данные: отрицательная цена и скидка вне диапазона [0, 100] бросают `ValueError`. В тестах сначала идёт параметризованная проверка: один тест превращается в четыре, каждый прогоняется со своим набором значений — это заметно сокращает дублирование кода. Затем два отдельных теста проверяют исключения: `pytest.raises(ValueError)` «ловит» ожидаемую ошибку, и если её нет — тест падает. Обрати внимание на число `180.0` с точкой: деление в Python всегда даёт `float`, поэтому сравнение с целым `180` тоже прошло бы, но для ясности тесты используют явные дробные значения. Когда все 6 тестов зелёные, можно спокойно рефакторить функцию — pytest сразу заметит любую регрессию.
<!--/SOLUTION-->
