---
title: Patterns: Singleton, Factory, Observer
summary: Classic GoF patterns in Python.
order: 3
duration: 50 min
difficulty: advanced
tags: patterns, singleton, factory
---

Patterns are proven solutions to recurring problems.

## Singleton

```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Factory

```python
class Shape:
    def area(self): ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

def shape_factory(kind, **kw):
    if kind == "circle":
        return Circle(**kw)
    raise ValueError(kind)
```

## Observer

Events notify subscribers.

## Lesson summary

Use patterns where they reduce duplication.

<!--TASK-->
### Task 1 — Singleton
Implement Config singleton.

### Task 2 — Test
Check both instances are equal.

### Task 3 — Factory
Shape factory for circle/square.

### Task 4 — Observer
Simple event with subscribers.

### Task 5 — When singleton
When is it justified?

### Task 6 — Trade-off
Singleton downsides.

### Task 7 — Choose
Pattern for creating variants.
<!--/TASK-->

<!--HINT-->
### Hint 1
__new__.

### Hint 2
is.

### Hint 3
Factory.

### Hint 4
List of callbacks.

### Hint 5
Shared state.

### Hint 6
Global.

### Hint 7
Factory.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Solution 2
```python
a = Config(); b = Config()
print(a is b)   # True
```

### Solution 3
```python
class Square(Shape):
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2

def shape_factory(kind, **kw):
    if kind == "circle":
        return Circle(**kw)
    if kind == "square":
        return Square(**kw)
    raise ValueError(kind)
```

### Solution 4
```python
class Event:
    def __init__(self):
        self._subscribers = []
    def subscribe(self, fn):
        self._subscribers.append(fn)
    def emit(self, *args):
        for fn in self._subscribers:
            fn(*args)

event = Event()
event.subscribe(lambda x: print("got", x))
event.emit("hello")
```

### Solution 5
```python
# Один общий объект конфигурации/лога
# — но глобальное состояние усложняет тесты
```

### Solution 6
```python
# Глобальный доступ, скрытая связность,
# невозможно несколько экземпляров (для тестов)
```

### Solution 7
```python
# Создание вариантов объекта → Фабрика
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Singleton?
- One instance
- Many
- Zero
- None
* Correct answer: One instance
Shared.

What is __new__?
- Instance creation
- Init
- Delete
- None
* Correct answer: Instance creation
Before __init__.

What is a factory?
- Creates objects
- Destroys
- Sorts
- None
* Correct answer: Creates objects
Variant.

What is Observer?
- Notifies subscribers
- Creates
- Singleton
- None
* Correct answer: Notifies subscribers
Event.

What is emit?
- Fires event
- Subscribes
- Stops
- None
* Correct answer: Fires event
Call all.

What is subscribe?
- Adds listener
- Removes
- Fires
- None
* Correct answer: Adds listener
Register.

What is a pattern?
- Proven solution
- A bug
- A library
- None
* Correct answer: Proven solution
Reusable.

Is Singleton global state?
- Yes
- No
- Safe
- None
* Correct answer: Yes
Hidden.

When use Factory?
- Many variants
- One object
- Never
- None
* Correct answer: Many variants
Central.

What is area?
- Method
- Data
- Event
- None
* Correct answer: Method
Shape.

What is an instance?
- Created object
- Class
- Module
- None
* Correct answer: Created object
Object.

What is classmethod-like creation?
- Factory
- Singleton
- Observer
- None
* Correct answer: Factory
Interface.
<!--/QUIZ-->
