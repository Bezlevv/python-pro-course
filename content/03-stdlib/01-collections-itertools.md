---
title: collections, itertools, functools
summary: Расширенные контейнеры, ленивые генераторы комбинаторики и удобные декораторы функций — инструменты для чистого и быстрого кода.
order: 1
duration: 30 мин
difficulty: intermediate
---

Когда код начинает расти, одних встроенных типов часто не хватает. Стандартная библиотека Python включает сотни модулей, и среди них есть три настоящих «ударных»: `collections`, `itertools` и `functools`. Их называют китами функционального стиля — они позволяют писать меньше кода, который при этом работает быстрее и читается лучше.

## collections: умные контейнеры

Модуль `collections` предоставляет расширенные варианты встроенных коллекций.

**Counter** — счётчик для подсчёта любых элементов:

```python
from collections import Counter

words = ["питон", "код", "питон", "данные", "код", "питон"]
counter = Counter(words)
print(counter)                    # Counter({'питон': 3, 'код': 2, 'данные': 1})
print(counter.most_common(2))     # [('питон', 3), ('код', 2)]
```

**defaultdict** — словарь, который сам создаёт значение для отсутствующего ключа:

```python
from collections import defaultdict

groups = defaultdict(list)
for num in [1, 2, 3, 4, 5, 6]:
    groups[num % 2].append(num)
print(dict(groups))   # {1: [1, 3, 5], 0: [2, 4, 6]}
```

**deque** — двухсторонняя очередь; вставка и удаление с обоих концов выполняются быстро:

```python
from collections import deque

queue = deque([1, 2, 3])
queue.append(4)      # добавить справа
queue.appendleft(0)  # добавить слева
print(queue.pop())       # 4
print(queue.popleft())   # 0
```

**namedtuple** — кортеж с именованными полями:

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 5)
print(p.x, p.y)   # 3 5
```

## itertools: комбинаторика и ленивые последовательности

Модуль `itertools` — это фабрики итераторов. Они не хранят данные в памяти целиком, а выдают элементы по одному, поэтому идеально работают с длинными последовательностями.

`count`, `cycle` и `repeat` создают бесконечные или повторяющиеся последовательности. Вместе с `islice` их легко обрезать:

```python
from itertools import count, cycle, islice

print(list(islice(count(10), 4)))   # [10, 11, 12, 13]
print(list(islice(cycle("ab"), 5))) # ['a', 'b', 'a', 'b', 'a']
```

`chain` склеивает несколько итераторов в один, `product` даёт декартово произведение, а `permutations` и `combinations` — все перестановки и сочетания:

```python
from itertools import chain, product, permutations

print(list(chain([1, 2], [3, 4])))        # [1, 2, 3, 4]
print(list(product("AB", [1, 2])))        # [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
print(list(permutations("ABC", 2)))       # все упорядоченные пары
```

`groupby` группирует соседние равные элементы — перед вызовом данные обычно сортируют:

```python
from itertools import groupby

data = sorted([3, 1, 3, 2, 1, 3])
for key, group in groupby(data):
    print(key, len(list(group)))   # 1 2 / 2 1 / 3 3
```

## functools: функциональные помощники

`lru_cache` кэширует результаты функции: если её вызвать повторно с теми же аргументами, тело не выполнится заново, а вернётся сохранённый результат:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(35))          # 9227465
print(fib.cache_info()) # CacheInfo(hits=..., misses=..., ...)
```

`partial` фиксирует часть аргументов функции, а `reduce` сворачивает последовательность в одно значение:

```python
from functools import partial, reduce

power = partial(pow, 2)              # 2 в степени n
print(power(10))                     # 1024
print(reduce(lambda a, b: a + b, range(1, 6)))  # 15
```

## Итог урока

Мы познакомились с тремя модулями, без которых не обходится почти ни один серьёзный проект: `collections` (Counter, defaultdict, deque, namedtuple), `itertools` (chain, product, groupby и другие ленивые генераторы) и `functools` (lru_cache, partial, reduce). Теперь применим их вместе в одной задаче.

<!--TASK-->
**Задача.** Напиши программу `text_stats.py`, которая:

1. Хранит в переменной `text` большой текст (минимум 30 слов — подойдёт любой абзац из книги или новости);
2. Разбивает его на слова: приводит к нижнему регистру и убирает знаки препинания;
3. Подсчитывает частоту слов с помощью `Counter`;
4. Выводит пять самых частых слов в формате `слово — N раз`;
5. Оборачивает функцию разбора текста в `lru_cache`, вызывает её дважды с одним и тем же текстом и печатает `cache_info()` этого декоратора.

Ожидаемый результат: на экране пять строк вида `и — 4 раза`, а затем строка `CacheInfo(...)` с `hits=1` и `misses=1` — первый вызов выполнил работу, второй взял результат из кэша.
<!--/TASK-->

<!--HINT-->
Для очистки текста используй модуль `re`: `re.findall(r"[а-яё]+", text.lower())` вернёт список слов без знаков препинания. Добавь декоратор `@lru_cache(maxsize=128)` над функцией, которая превращает текст в `Counter`. Состояние кэша смотри через `stats.cache_info()` у самой функции.
<!--/HINT-->

<!--SOLUTION-->
Одно из возможных решений:

```python
import re
from collections import Counter
from functools import lru_cache

text = (
    "Питон — язык программирования, который читается почти как английский текст. "
    "Питон прост, мощен и очень востребован. Изучайте Питон каждый день, "
    "и тогда Питон станет вашим главным инструментом."
)

@lru_cache(maxsize=128)
def count_words(text):
    words = re.findall(r"[а-яё]+", text.lower())
    return Counter(words)

stats_first = count_words(text)
stats_second = count_words(text)  # тот же текст — попадание в кэш

for word, freq in stats_first.most_common(5):
    print(f"{word} — {freq} раз")

print(count_words.cache_info())
```

Результат:

```
питон — 4 раз
и — 2 раз
язык — 1 раз
программирования — 1 раз
который — 1 раз
CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)
```

Разбор шагов. Регулярное выражение `[а-яё]+` вырезает только последовательности букв, поэтому знаки препинания и кавычки пропадают автоматически; `lower()` приводит всё к нижнему регистру, чтобы «Питон» и «питон» считались одним словом. Функция `count_words` обёрнута в `@lru_cache`: при первом вызове тело выполняется, результат кладётся в кэш, а при втором вызове с тем же текстом Python возвращает сохранённый `Counter`, не выполняя функцию повторно — об этом говорят `hits=1` (одно попадание) и `misses=1` (один промах). Наконец, `most_common(5)` возвращает пять пар «слово — частота», которые мы печатаем в цикле. Кэширование тяжёлых вычислений особенно полезно при обработке больших объёмов данных — например, когда один и тот же файл анализируется несколько раз.
<!--/SOLUTION-->
