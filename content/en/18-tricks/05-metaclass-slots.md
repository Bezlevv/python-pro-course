---
title: Metaclasses and __slots__
summary: Class creation hooks, memory savings.
order: 5
duration: 45 min
difficulty: advanced
tags: metaclass, slots
---

Metaclasses customize class creation.

## __slots__

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
# меньше памяти, нет __dict__
```

## Metaclass

```python
class UpperMeta(type):
    def __new__(mcs, name, bases, namespace):
        upper = {k.upper(): v for k, v in namespace.items()}
        return super().__new__(mcs, name, bases, upper)

class Greeting(metaclass=UpperMeta):
    hello = "hi"

print(Greeting.HELLO)   # hi
```

## Lesson summary

Metaclasses are advanced; __slots__ saves memory.

<!--TASK-->
### Task 1 — Slots
Define Point with __slots__.

### Task 2 — Test
Set and read x, y.

### Task 3 — No dict
Show there's no __dict__.

### Task 4 — Meta
UpperMeta example.

### Task 5 — When slots
When use __slots__?

### Task 6 — When meta
When use metaclasses?

### Task 7 — Trade-off
Downside of __slots__.
<!--/TASK-->

<!--HINT-->
### Hint 1
__slots__.

### Hint 2
Attributes.

### Hint 3
hasattr.

### Hint 4
type subclass.

### Hint 5
Many objects.

### Hint 6
Frameworks.

### Hint 7
No dynamic.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Solution 2
```python
p = Point(1, 2)
print(p.x, p.y)   # 1 2
```

### Solution 3
```python
print(hasattr(p, "__dict__"))   # False
```

### Solution 4
```python
class UpperMeta(type):
    def __new__(mcs, name, bases, namespace):
        upper = {k.upper(): v for k, v in namespace.items()}
        return super().__new__(mcs, name, bases, upper)

class Greeting(metaclass=UpperMeta):
    hello = "hi"

print(Greeting.HELLO)   # hi
```

### Solution 5
```python
# Когда создаётся очень много объектов
# одного класса (например, в играх/данных)
```

### Solution 6
```python
# Редко: фреймворки, ORM, валидаторы,
# когда нужно менять поведение создания классов
```

### Solution 7
```python
# Нельзя добавлять новые атрибуты на лету,
# усложняется отладка
```
<!--/SOLUTION-->

<!--QUIZ-->
What is __slots__?
- Fixed attributes
- Dynamic
- Methods
- None
* Correct answer: Fixed attributes
Memory.

What does __slots__ save?
- Memory
- Time
- Code
- None
* Correct answer: Memory
No __dict__.

What is __dict__?
- Attribute storage
- Class
- Module
- None
* Correct answer: Attribute storage
Dict.

What is a metaclass?
- Class factory
- Instance
- Method
- None
* Correct answer: Class factory
type.

What is type?
- Root metaclass
- A class only
- A function
- None
* Correct answer: Root metaclass
Meta.

What is __new__?
- Creates class
- Inits
- Deletes
- None
* Correct answer: Creates class
Before.

What is namespace?
- Class attributes
- Methods only
- Module
- None
* Correct answer: Class attributes
Dict.

What is metaclass=?
- Selects metaclass
- Inherits
- Instantiates
- None
* Correct answer: Selects metaclass
Argument.

What is the benefit of slots?
- Less memory
- More memory
- Faster only
- None
* Correct answer: Less memory
Many objects.

What is the downside?
- No dynamic attrs
- Slower
- Required
- None
* Correct answer: No dynamic attrs
Fixed.

When metaclasses?
- Rarely
- Always
- Never
- None
* Correct answer: Rarely
Advanced.

What is inheritance?
- Class from class
- Meta
- Instance
- None
* Correct answer: Class from class
Base.
<!--/QUIZ-->
