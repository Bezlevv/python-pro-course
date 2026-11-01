---
title: Магические методы и property
summary: Как сделать свои классы «нативными»: __str__, __repr__, __len__, __eq__, операторы и property.
order: 3
duration: 45 мин
difficulty: advanced
---

У встроенных объектов Python есть удобное поведение: строку можно складывать, у списка спрашивать длину через `len()`, объекты сравнивать. А можно ли научить этому свои классы? Да — с помощью **магических методов**. Это методы с двойными подчёркиваниями, которые Python вызывает автоматически в определённых ситуациях.

## __str__ и __repr__: строковые представления

Сейчас `print()` от нашего объекта скажет `__main__.Point object at 0x...` — не очень полезно. Исправим это:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
print(p)          # Point(1, 2) — сработал __str__
print(str(p))     # тоже Point(1, 2)
```

`__str__` вызывается `print()` и `str()`, чтобы получить человекочитаемое описание. Есть ещё `__repr__` — формальное представление, которое показывает IDE и `repr()`:

```python
class Point:
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
```

Хорошая практика: `__repr__` делаем однозначным (по нему можно восстановить объект), а `__str__` — красивым для глаз.

## __len__ и __getitem__: поведение «коллекции»

Если класс хранит набор элементов, можно разрешить `len()` и обращение по индексу:

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

cart = ShoppingCart()
cart.add("хлеб")
cart.add("молоко")
print(len(cart))      # 2 — сработал __len__
print(cart[0])        # хлеб — сработал __getitem__
```

Бонус: раз есть `__getitem__`, объект становится итерируемым — по нему можно пройтись циклом `for`.

## Магические методы сравнения и арифметики

Python позволяет перегружать операторы. Например, `==` использует `__eq__`, а `+` — `__add__`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = p1 + p2
print(p1 == p2)   # True — теперь сравнение осмысленное
print(p3)         # Point(2, 4)
```

Теперь точки можно складывать, как числа! Всего таких методов много: `__sub__`, `__mul__`, `__lt__`, `__hash__` и другие.

## property: контроль доступа к атрибутам

Иногда хочется управлять тем, как читается и записывается атрибут. Классический пример — температура: хранить её лучше в Цельсиях, а давать доступ и в Фаренгейтах. Декоратор `@property` превращает метод в атрибут:

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.celsius)     # 25 — читается как атрибут
print(t.fahrenheit)  # 77.0 — вычисляется на лету
```

Мы назвали атрибут `_celsius` с подчёркиванием — так мы показываем, что это «внутренняя» переменная, и обращаться к ней напрямую не стоит. А `@property`-метод `celsius` отдаёт её наружу. Если нужно разрешить изменение с проверкой, добавляют сеттер:

```python
class Temperature:
    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
        self._celsius = value

t = Temperature(25)
t.celsius = 30      # ок
# t.celsius = -300  # ValueError!
```

## Итог

Магические методы встраивают твой класс в синтаксис Python: печать, длина, индексация, сравнение, арифметика. А `property` даёт чистый интерфейс доступа к данным с проверками. Это главные инструменты для создания «полноценных» типов.

<!--TASK-->
**Задача.** Создай класс `Money`, который хранит сумму в рублях. Реализуй:

- `__init__(self, amount)` — хранит сумму,
- `__str__` — возвращает строку вида `123 руб.`,
- `__eq__` — сравнивает суммы двух объектов `Money`,
- `__add__` — возвращает новый объект `Money` с суммой двух,
- свойство `rubles` с сеттером, который не даёт установить отрицательную сумму (бросай `ValueError`).

Проверь: сложи `Money(100)` и `Money(50)`, сравни `Money(150)` с результатом, попробуй установить отрицательную сумму и поймай ошибку.
<!--/TASK-->

<!--HINT-->
В `__add__` верни новый `Money(self.amount + other.amount)`. Для свойства используй `@property` и `@rubles.setter` — в сеттере проверь `value < 0`. Чтобы увидеть `ValueError`, запусти код в блоке `try/except` или не перехватывай её вовсе.
<!--/HINT-->

<!--SOLUTION-->
Одно из возможных решений:

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"{self.amount} руб."

    def __eq__(self, other):
        return self.amount == other.amount

    def __add__(self, other):
        return Money(self.amount + other.amount)

    @property
    def rubles(self):
        return self.amount

    @rubles.setter
    def rubles(self, value):
        if value < 0:
            raise ValueError("Сумма не может быть отрицательной")
        self.amount = value

a = Money(100)
b = Money(50)
total = a + b
print(total)               # 150 руб.
print(total == Money(150)) # True
total.rubles = 200
print(total)               # 200 руб.

try:
    total.rubles = -5
except ValueError as e:
    print(e)               # Сумма не может быть отрицательной
```

Результат:

```
150 руб.
True
200 руб.
Сумма не может быть отрицательной
```

Что здесь происходит? `__str__` делает так, что `print(total)` показывает привычное `150 руб.`. `__eq__` сравнивает внутренние суммы, поэтому `total == Money(150)` даёт `True`. `__add__` создаёт новый объект, не изменяя исходные — это хороший стиль: арифметические операции возвращают новые объекты.

Свойство `rubles` прячет атрибут `amount` за интерфейсом: чтение идёт через геттер, а запись — через сеттер с проверкой. Когда мы пробуем установить `-5`, сеттер бросает `ValueError`, который мы ловим в `try/except` и печатаем сообщение. Так объект не может оказаться в неверном состоянии.
<!--/SOLUTION-->
