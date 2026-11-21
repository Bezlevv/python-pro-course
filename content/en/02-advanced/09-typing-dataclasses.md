---
title: Type annotations and dataclasses
summary: Annotations, typing hints, dataclasses, field and frozen models.
order: 9
duration: 40 min
difficulty: intermediate
tags: typing, annotations, dataclass, field
---

Type annotations document and, with tools like mypy, verify your code.

## Annotations

```python
def greet(name: str, age: int = 0) -> str:
    return f"{name}, {age}"
```

`-> str` is the return type.

## Built-in generic types

```python
from typing import List, Dict, Optional

def total(values: List[int]) -> int:
    return sum(values)

def find(d: Dict[str, int], key: str) -> Optional[int]:
    return d.get(key)
```

## dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int = 0
    tags: list = field(default_factory=list)
```

`@dataclass` generates __init__, __repr__, __eq__ automatically.

## field(default_factory)

Use it for mutable defaults (lists, dicts).

## frozen=True

```python
@dataclass(frozen=True)
class Point:
    x: int
    y: int
```

Immutable instances.

## Lesson summary

Annotations improve readability and tooling; dataclasses reduce boilerplate.

<!--TASK-->
### Task 1 — Annotated function
Write add(a: int, b: int) -> int; call it.

### Task 2 — Optional
Write find_key(d: dict, key: str) -> Optional[int] using dict.get.

### Task 3 — List[int]
Write total(values: list[int]) -> int using sum.

### Task 4 — Basic dataclass
Create @dataclass Product with name and price; create and print instance.

### Task 5 — default_factory
Create @dataclass Cart with items: list = field(default_factory=list); add to two carts separately.

### Task 6 — frozen
Create @dataclass(frozen=True) Point; try to mutate and catch exception.

### Task 7 — Nested types
Annotate a function returning dict[str, list[int]] and show usage.
<!--/TASK-->

<!--HINT-->
### Hint 1
Use -> int for return.

### Hint 2
from typing import Optional.

### Hint 3
list[int] is valid in Python 3.9+.

### Hint 4
@dataclass above class.

### Hint 5
field(default_factory=list).

### Hint 6
FrozenInstanceError on set.

### Hint 7
dict[str, list[int]] type hint.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))   # 5
```

### Solution 2
```python
from typing import Optional

def find_key(d: dict, key: str) -> Optional[int]:
    return d.get(key)

print(find_key({"a": 1}, "a"))   # 1
print(find_key({"a": 1}, "b"))   # None
```

### Solution 3
```python
def total(values: list[int]) -> int:
    return sum(values)

print(total([1, 2, 3]))   # 6
```

### Solution 4
```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

p = Product("Laptop", 999.99)
print(p)   # Product(name='Laptop', price=999.99)
```

### Solution 5
```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list = field(default_factory=list)

c1 = Cart()
c2 = Cart()
c1.items.append("book")
print(c1.items, c2.items)   # ['book'] []
```

### Solution 6
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
try:
    p.x = 5
except Exception as e:
    print(type(e).__name__)   # FrozenInstanceError
```

### Solution 7
```python
def stats(nums: list[int]) -> dict[str, list[int]]:
    return {"evens": [x for x in nums if x % 2 == 0],
            "odds": [x for x in nums if x % 2]}

print(stats([1, 2, 3, 4]))
```
<!--/SOLUTION-->

<!--QUIZ-->
What does -> int mean?
- Return type annotation
- Argument type
- Nothing
- Error
* Correct answer: Return type annotation
Documents the function.

What is Optional[int]?
- int or None
- int
- None
- list
* Correct answer: int or None
Shorthand.

What is list[int]?
- List of ints
- An int
- A tuple
- A set
* Correct answer: List of ints
Generic annotation.

What do dataclasses reduce?
- Boilerplate (__init__, __repr__, __eq__)
- Memory
- Speed
- Imports
* Correct answer: Boilerplate
Generated automatically.

Why use field(default_factory=list)?
- Fresh list per instance
- Shared list
- None
- Tuple
* Correct answer: Fresh list per instance
Avoids shared mutable default.

What is frozen=True?
- Immutable dataclass
- Faster
- Bigger
- Required
* Correct answer: Immutable dataclass
No mutation after creation.

What exception on mutation of frozen?
- FrozenInstanceError
- TypeError
- ValueError
- KeyError
* Correct answer: FrozenInstanceError
Dataclasses raises.

What does @dataclass generate?
- __init__, __repr__, __eq__
- Only __init__
- Methods only
- Nothing
* Correct answer: __init__, __repr__, __eq__
Standard.

Is `age: int = 0` valid?
- Yes, default value
- No
- Only str
- Requires field
* Correct answer: Yes, default value
Allowed.

What is dict[str, list[int]]?
- Dict of str to list of ints
- Dict of lists
- List of dicts
- Tuple
* Correct answer: Dict of str to list of ints
Nested annotation.

Are annotations enforced at runtime?
- No, they are hints
- Yes, always
- Only on classes
- Only in functions
* Correct answer: No, they are hints
Tools like mypy check them.

Which tool checks annotations?
- mypy
- pytest
- black
- pytest only
* Correct answer: mypy
Static type checker.
<!--/QUIZ-->
