---
title: Дескрипторы, __slots__, метаклассы и MRO
summary: Внутреннее устройство классов: дескрипторы атрибутов, экономия памяти через __slots__, создание классов через метаклассы и порядок разрешения методов MRO.
order: 14
duration: 60 мин
difficulty: advanced
tags: descriptors, slots, metaclass, mro
---

Ты уже умеешь писать классы, наследование и магические методы. Этот урок открывает «под капот» самого механизма классов: как атрибуты вообще работают, почему `property` — это частный случай более общего механизма, как сэкономить память и как Python решает, какой метод вызвать при сложном наследовании. Это не абстрактная теория: понимание этих механизмов напрямую влияет на производительность и читаемость твоего кода.

## Дескрипторы

Дескриптор — это класс, который определяет хотя бы один из методов `__get__`, `__set__` или `__delete__`. Если такой объект положен в класс как атрибут, Python при обращении к нему через экземпляр вызывает не сам атрибут, а его методы.

```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Значение должно быть положительным")
        instance.__dict__[self._name] = value

class Product:
    price = PositiveNumber()

p = Product()
p.price = 150  # Ok
print(p.price)   # 150
# p.price = -5  # ValueError
```

Как это работает: `price` — экземпляр `PositiveNumber`, лежащий в классе. Когда ты пишешь `p.price = 150`, Python видит, что у атрибута есть `__set__`, и вызывает его. Такой дескриптор называется **data-дескриптором** — он есть и `__get__`, и `__set__`. У `property` и `staticmethod` — тоже data-дескрипторы.

Если у объекта есть только `__get__`, это **non-data-дескриптор**. Его приоритет ниже, чем у обычного атрибута экземпляра:

```python
class cached_property:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        instance.__dict__[self.func.__name__] = value
        return value

class Report:
    def __init__(self, data):
        self.data = data

    @cached_property
    def total(self):
        print("Считаю...")
        return sum(self.data)

r = Report([1, 2, 3])
print(r.total)  # Считаю... 6
print(r.total)  # 6 — из __dict__ экземпляра, не пересчитывается
```

Первый вызов считает значение и прячет его в `__dict__` экземпляра; второй вызов находит обычный атрибут экземпляра раньше, чем non-data-дескриптор. Так работает кэширование без лишних зависимостей.

## __slots__ и память

По умолчанию каждый экземпляр носит `__dict__` — словарь атрибутов. Это удобно, но дорого: словарь весит заметно больше, чем сам объект. Если известно, какие атрибуты будут у объекта, можно объявить `__slots__`:

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

Теперь у экземпляра нет `__dict__`, атрибуты хранятся в компактных слотах, и `p.z = 1` вызовет `AttributeError`. Памяти расходуется в разы меньше — это критично для миллионов объектов. Два нюанса: `__slots__` не наследуются автоматически (в наследнике нужно объявить свои), а если нужны слабые ссылки, добавь `'__weakref__'` в слоты.

## Метаклассы

Класс в Python — тоже объект, и создаёт его `type`. Метакласс — это класс класса. Ты можешь подменить `type` и перехватить момент создания класса через `__new__`:

```python
class RegistryMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "Base":
            mcs.registry[name] = cls
        return cls

class Base(metaclass=RegistryMeta):
    pass

class Cat(Base):
    pass

print(RegistryMeta.registry)  # {'Cat': <class '__main__.Cat'>}
```

Такое используют для автоматической регистрации моделей, плагинов и обработчиков. `__new__` метакласса получает имя класса, кортеж баз и пространство имён (тот самый словарь, который в обычном классе создаёт `type`).

## MRO: порядок разрешения методов

Когда один класс наследует от нескольких, Python должен решить, чей метод вызвать и в каком порядке. Порядок называется MRO (Method Resolution Order) и вычисляется по алгоритму C3:

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print([c.__name__ for c in D.mro()])
# ['D', 'B', 'C', 'A', 'object']
```

Каждый класс появляется в MRO ровно один раз, и любой родитель стоит после своих потомков. `super()` ходит не к «родителю», а по MRO дальше — поэтому с `super()` можно строить кооперативные цепочки вызовов.

```python
class LoggerMixin:
    def save(self):
        print("Логируем сохранение")
        return super().save()

class Store:
    def save(self):
        print("Сохраняем в БД")

class Report(LoggerMixin, Store):
    pass

Report().save()
# Логируем сохранение
# Сохраняем в БД
```

`super()` в `LoggerMixin` находит следующий класс после `LoggerMixin` в MRO — это `Store`, и вызывает его `save`. Порядок `LoggerMixin, Store` даёт «обёртку» вокруг базового поведения.

## Итог

- Дескрипторы перехватывают доступ к атрибутам; data-дескрипторы сильнее атрибутов экземпляра, non-data — слабее.
- `__slots__` экономит память, отключая `__dict__`.
- Метаклассы перехватывают создание классов.
- MRO определяет порядок вызовов; `super()` — инструмент кооперативного наследования.

<!--TASK-->
### Задача 1
Напиши data-дескриптор `StringField`, который хранит строку и не даёт записать в атрибут не-строку. Используй `__set_name__`, чтобы узнать имя атрибута, и храни значение в `__dict__` экземпляра. Проверь на классе `User` с полями `name` и `city`: присвой корректные значения и выведи их, затем попробуй записать `123` и убедись, что поднимается `TypeError` с понятным сообщением.

### Задача 2
Создай класс `Note` с `__slots__ = ("title", "body")` и конструктором. Покажи, что: 1) атрибуты работают как обычно; 2) добавить новый атрибут нельзя — получится `AttributeError`; 3) у экземпляра нет `__dict__` (проверь через `hasattr`). Затем создай наследника `DatedNote` с дополнительным слотом `date` и убедись, что у него тоже нет `__dict__`.

### Задача 3
Реализуй non-data-дескриптор `once`, который вычисляет значение функции при первом обращении и кэширует его в `__dict__` экземпляра. Проверь на классе с дорогой операцией (например, вычисление простого числа): первый вызов печатает «Считаю...», второй — сразу отдаёт результат. Убедись, что после кэширования в `__dict__` появился атрибут.

### Задача 4
Напиши метакласс `DefaultMeta`, который в `__new__` добавляет в класс метод `describe`, возвращающий строку вида `Класс <имя> создан`. Создай с его помощью два класса (например, `Cat` и `Dog`) и вызови `describe()` у экземпляров. Проверь, что у обоих классов есть этот метод, и что он работает независимо.

### Задача 5
Дана иерархия: `A` с методом `hello`, `B(A)` с `hello` через `super()`, `C(A)` с `hello` через `super()`, `D(B, C)`. Выведи `D.mro()` и предскажи, в каком порядке напечатаются сообщения при вызове `D().hello()`. Затем реализуй код и сверь предсказание с реальным выводом. В комментарии объясни, почему порядок именно такой.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Дескриптор: нужен `__set_name__` для запоминания имени, `__get__` для чтения из `instance.__dict__` и `__set__` с проверкой `isinstance(value, str)`. Не забудь про `instance is None` в `__get__`.

### Подсказка 2
В классе с `__slots__` после `__init__` проверь `hasattr(p, "__dict__")` — должно быть `False`. Наследник должен сам объявить свои слоты: иначе у него появится `__dict__`.

### Подсказка 3
Дескриптор хранит функцию в `__init__`; в `__get__` проверяй `if name in instance.__dict__: return instance.__dict__[name]`. Имя для `__dict__` возьми из `self.func.__name__`.

### Подсказка 4
В `__new__` метакласса namespace — это словарь атрибутов. Добавь туда функцию: `namespace["describe"] = lambda self: f"Класс {type(self).__name__} создан"` и передай namespace в `super().__new__`.

### Подсказка 5
Разложи вызов: `D().hello()` → сначала `B.hello`, внутри `super()` → следующий в MRO после `B` — `C`, затем `C.hello` вызывает `super()` → `A`. Выведется три строки в порядке B → C → A.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
class StringField:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self._name} должен быть строкой")
        instance.__dict__[self._name] = value

class User:
    name = StringField()
    city = StringField()

    def __init__(self, name, city):
        self.name = name
        self.city = city

u = User("Аня", "Москва")
print(u.name, u.city)  # Аня Москва
# u.name = 123  # TypeError: name должен быть строкой
```

`__set_name__` вызывается Python'ом при создании класса, когда дескриптор связывается с именем атрибута. В `__set__` мы проверяем тип и пишем значение в `__dict__` экземпляра, а `__get__` читает оттуда. Ветка `instance is None` нужна для обращения через класс: `User.name` вернёт сам дескриптор, а не значение.

### Разбор 2
```python
class Note:
    __slots__ = ("title", "body")

    def __init__(self, title, body):
        self.title = title
        self.body = body

class DatedNote(Note):
    __slots__ = ("date",)

n = Note("Заголовок", "Текст")
print(n.title, n.body)
print(hasattr(n, "__dict__"))   # False
# n.extra = 1                   # AttributeError

dn = DatedNote("Сегодня", "Дела")
dn.date = "2026-11-01"
print(dn.date, hasattr(dn, "__dict__"))  # 2026-11-01 False
```

`__slots__` заменяет `__dict__` компактными слотами. Поэтому `hasattr(n, "__dict__")` даёт `False`, а присваивание нового атрибута бросает `AttributeError`. Наследник обязан объявить свои слоты: если бы `DatedNote` их не имел, у него появился бы обычный `__dict__`, и экономия бы пропала.

### Разбор 3
```python
class once:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        name = self.func.__name__
        if name not in instance.__dict__:
            print("Считаю...")
            instance.__dict__[name] = self.func(instance)
        return instance.__dict__[name]

class Prime:
    def __init__(self, n):
        self.n = n

    @once
    def get_prime(self):
        return max(p for p in range(2, self.n) if all(p % d for d in range(2, p)))

p = Prime(1000)
print(p.get_prime)   # Считаю... 997
print(p.get_prime)   # 997 — без пересчёта
```

`once` — non-data-дескриптор: у него только `__get__`. При первом обращении `__get__` вычисляет результат и кладёт его в `__dict__` экземпляра. При втором обращении Python сначала ищет атрибут в `__dict__` экземпляра, находит его и **не доходит** до дескриптора — поэтому «Считаю...» печатается один раз.

### Разбор 4
```python
class DefaultMeta(type):
    def __new__(mcs, name, bases, namespace):
        def describe(self):
            return f"Класс {type(self).__name__} создан"
        namespace["describe"] = describe
        return super().__new__(mcs, name, bases, namespace)

class Cat(metaclass=DefaultMeta):
    pass

class Dog(metaclass=DefaultMeta):
    pass

print(Cat().describe())  # Класс Cat создан
print(Dog().describe())  # Класс Dog создан
```

Метакласс перехватывает создание класса: `__new__` получает имя, кортеж баз и словарь атрибутов. Мы добавляем в словарь метод `describe` — и он попадает в каждый класс, созданный этим метаклассом. Это общий принцип: метакласс — это фабрика классов, которая может добавлять методы, атрибуты и проверки.

### Разбор 5
```python
class A:
    def hello(self):
        print("A")

class B(A):
    def hello(self):
        print("B")
        super().hello()

class C(A):
    def hello(self):
        print("C")
        super().hello()

class D(B, C):
    pass

print([c.__name__ for c in D.mro()])
# ['D', 'B', 'C', 'A', 'object']

D().hello()
# B
# C
# A
```

MRO для ромба строится по алгоритму C3: каждый класс появляется один раз, родители — после потомков. Вызов `D().hello()` идёт по MRO: сначала `B`, затем `super()` в `B` находит следующий класс после `B` — это `C`, а уже `super()` внутри `C` приводит к `A`. Так `super()` позволяет каждому классу «дополнить» поведение следующего, не зная о нём ничего.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает дескриптор, у которого определён только __get__?
- Это data-дескриптор
- Это non-data-дескриптор
- Это метакласс
- Такого не бывает
* Правильный ответ: Это non-data-дескриптор
Дескриптор с одним лишь __get__ называется non-data: обычный атрибут экземпляра имеет над ним приоритет.

Что произойдёт при записи p.price = -5, если price — дескриптор PositiveNumber из урока?
- Значение запишется
- Поднимется ValueError
- Поднимется TypeError
- Значение проигнорируется
* Правильный ответ: Поднимется ValueError
__set__ дескриптора проверяет значение и бросает ValueError для неположительных чисел.

Какой метод вызывается, когда дескриптор связывается с именем атрибута в классе?
- __set_name__
- __get__
- __init__
- __slots__
* Правильный ответ: __set_name__
Python вызывает __set_name__ при создании класса, передавая владельца и имя атрибута.

Что делает __slots__?
- Добавляет объекту __dict__
- Заменяет __dict__ компактными слотами
- Ускоряет наследование
- Запрещает наследование
* Правильный ответ: Заменяет __dict__ компактными слотами
Вместо словаря атрибутов экземпляр хранит значения в фиксированных слотах — это экономит память.

Можно ли добавить новый атрибут экземпляру класса с __slots__?
- Да, всегда
- Нет, будет AttributeError
- Да, но только строки
- Можно, если атрибут числовой
* Правильный ответ: Нет, будет AttributeError
Без __dict__ некуда положить новый атрибут, поэтому Python бросает AttributeError.

Что создаёт класс в Python по умолчанию?
- object
- type
- class
- metaclass
* Правильный ответ: type
Класс — это объект, создаваемый type; метакласс — это класс, который создаёт классы.

В каком методе метакласса перехватывается момент создания класса?
- __init__
- __new__
- __call__
- __create__
* Правильный ответ: __new__
__new__ метакласса получает имя, базы и namespace и возвращает новый класс.

Какой порядок будет у D.mro() для D(B, C), где B(A) и C(A)?
- D, B, C, A, object
- D, A, B, C, object
- D, B, A, C, object
- D, C, B, A, object
* Правильный ответ: D, B, C, A, object
Алгоритм C3 даёт D → B → C → A → object: родители идут после потомков, а порядок баз сохраняется.

Что вернёт super() внутри метода класса B в иерархии D(B, C)?
- Класс A
- Следующий класс в MRO после B
- Класс D
- Сам класс B
* Правильный ответ: Следующий класс в MRO после B
super() движется по MRO: после B идёт C, поэтому вызовется метод C.

Зачем нужен non-data-дескриптор с кэшированием?
- Чтобы ускорить вызовы функций
- Чтобы вычислять значение один раз и хранить его в __dict__ экземпляра
- Чтобы запретить изменение атрибута
- Чтобы создать метакласс
* Правильный ответ: Чтобы вычислять значение один раз и хранить его в __dict__ экземпляра
Первый вызов считает и прячет результат в __dict__, дальше обычный атрибут имеет приоритет над non-data-дескриптором.
<!--/QUIZ-->
