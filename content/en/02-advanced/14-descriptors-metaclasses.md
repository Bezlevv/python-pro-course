---
title: Descriptors, __slots__, metaclasses, MRO
summary: Advanced attribute control, memory optimization and class creation internals.
order: 14
duration: 60 min
difficulty: advanced
tags: descriptors, slots, metaclass, mro
---

These advanced topics control how attributes and classes behave.

## Descriptors

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, owner=None):
        return getattr(obj, self.name, 0)
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("positive only")
        setattr(obj, self.name, value)
```

## __slots__

`__slots__` declares fixed attributes and saves memory:

```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

No __dict__ per instance.

## Metaclasses

A metaclass creates classes:

```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        namespace["created"] = True
        return super().__new__(mcs, name, bases, namespace)

class A(metaclass=Meta):
    pass

print(A.created)   # True
```

## MRO

Method resolution order determines which method is used:

```python
class A: pass
class B(A): pass
print(B.__mro__)
```

## Lesson summary

Descriptors control attributes; __slots__ saves memory; metaclasses customize class creation; MRO resolves methods.

<!--TASK-->
### Task 1 — Descriptor
Implement Positive descriptor and test with negative value raising ValueError.

### Task 2 — __slots__
Create class Point with __slots__ ("x","y"); verify it has no __dict__.

### Task 3 — Metaclass logging
Create a metaclass that prints the class name on creation.

### Task 4 — Metaclass adding attribute
Create a metaclass that adds a class attribute code = 42.

### Task 5 — MRO print
Print __mro__ for class C(A, B) where A, B defined.

### Task 6 — super() in multiple inheritance
Use super() in methods to call the next class in MRO; verify output order.

### Task 7 — __slots__ with properties
Combine __slots__ and a property getter/setter.
<!--/TASK-->

<!--HINT-->
### Hint 1
__set__ raises ValueError for negative.

### Hint 2
__slots__ = ("x", "y").

### Hint 3
class Meta(type): __new__ prints name.

### Hint 4
namespace["code"] = 42.

### Hint 5
C.__mro__ shows order.

### Hint 6
super().method() goes to next in MRO.

### Hint 7
@property with __slots__ backing name.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, owner=None):
        return getattr(obj, self.name, 0)
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("positive only")
        setattr(obj, self.name, value)

class Account:
    balance = Positive()

a = Account()
a.balance = 100
print(a.balance)
try:
    a.balance = -1
except ValueError as e:
    print(e)
```

### Solution 2
```python
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(hasattr(p, "__dict__"))   # False
```

### Solution 3
```python
class LoggingMeta(type):
    def __new__(mcs, name, bases, namespace):
        print("Creating class", name)
        return super().__new__(mcs, name, bases, namespace)

class A(metaclass=LoggingMeta):
    pass
```

### Solution 4
```python
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        namespace["code"] = 42
        return super().__new__(mcs, name, bases, namespace)

class A(metaclass=Meta):
    pass

print(A.code)   # 42
```

### Solution 5
```python
class A: pass
class B: pass
class C(A, B): pass
print(C.__mro__)
```

### Solution 6
```python
class A:
    def hello(self):
        return "A"
class B(A):
    def hello(self):
        return super().hello() + "B"
print(B().hello())   # AB
```

### Solution 7
```python
class Temp:
    __slots__ = ("_celsius",)
    def __init__(self, c):
        self._celsius = c
    @property
    def celsius(self):
        return self._celsius
    @celsius.setter
    def celsius(self, v):
        self._celsius = v
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a descriptor?
- Object controlling attribute access
- A method
- A class only
- A dunder only
* Correct answer: Object controlling attribute access
Implements __get__/__set__.

What does __set_name__ do?
- Informs the descriptor of the attribute name
- Sets the value
- Deletes
- Returns
* Correct answer: Informs the descriptor of the attribute name
At class creation.

What are __slots__?
- Fixed attribute list to save memory
- Optional features
- Built-in methods
- Types
* Correct answer: Fixed attribute list to save memory
No __dict__.

What disappears with __slots__?
- __dict__
- __init__
- __repr__
- __eq__
* Correct answer: __dict__
Per-instance dict.

What is a metaclass?
- A class that creates classes
- An instance
- A descriptor
- A module
* Correct answer: A class that creates classes
type is the default.

What does __new__ in metaclass do?
- Creates the class
- Creates instances
- Deletes
- Returns namespace
* Correct answer: Creates the class
At class definition.

What is MRO?
- Method resolution order
- Method revision order
- Module order
- Memory
* Correct answer: Method resolution order
Order of lookup.

How to see MRO?
- cls.__mro__
- cls.mro() both
- mro(cls)
- type(cls)
* Correct answer: cls.__mro__
Tuple of classes.

What does super() use?
- MRO
- __init__
- Descriptors
- Slots
* Correct answer: MRO
Finds next class.

Can __slots__ and property coexist?
- Yes
- No
- Only in Python 3.12
- Never
* Correct answer: Yes
Use underscore backing.

What is type?
- Metaclass
- Class
- Function
- Instance
* Correct answer: Metaclass
Default metaclass.

What happens if you set an unlisted attribute with __slots__?
- AttributeError
- It works
- Warning
- Deleted
* Correct answer: AttributeError
Limited attributes.
<!--/QUIZ-->
