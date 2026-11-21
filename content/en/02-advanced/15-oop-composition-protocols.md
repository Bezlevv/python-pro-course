---
title: Composition and protocols instead of inheritance
summary: When inheritance hurts, composition, ABCs and structural typing with Protocol.
order: 15
duration: 50 min
difficulty: advanced
tags: composition, protocol, abc, typing
---

Deep inheritance hierarchies are brittle. Composition and protocols offer flexible alternatives.

## Why avoid deep inheritance

- is-a vs has-a;
- fragile base class problem;
- harder testing.

## ABC (abstract base classes)

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: int) -> str: ...

class CardPayment(Payment):
    def pay(self, amount: int) -> str:
        return f"Card: {amount}"
```

Cannot instantiate Payment.

## Protocol

```python
from typing import Protocol

class Payable(Protocol):
    def pay(self, amount: int) -> str: ...

class Wallet:
    def pay(self, amount: int) -> str:
        return f"Wallet: {amount}"

def charge(p: Payable, amount: int) -> str:
    return p.pay(amount)
```

Structural match — no inheritance needed.

## Composition

```python
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self, engine):
        self._engine = engine
    def start(self):
        return self._engine.start()
```

## Dependency injection

Pass dependencies in; test with fakes.

## Lesson summary

Use ABC for strict contracts, Protocol for shape, composition for flexibility.

<!--TASK-->
### Task 1 — ABC
Create Shape(ABC) with area(); implement Square and Circle.

### Task 2 — Protocol
Define Reader protocol; write process(r: Reader); use FileReader without inheritance.

### Task 3 — Composition
Build Duck with Flyable and Swimmable objects; delegate calls.

### Task 4 — Dependency injection
Write Report(writer) that writes to any writer.

### Task 5 — Validator protocol
Define Validator protocol and two implementations (Positive, Length).

### Task 6 — Repository with DI
Create UserService accepting a repo protocol; use MemoryRepository and DummyRepository.

### Task 7 — Notifier
Define Notifier protocol, two implementations, AlertService notifying all.
<!--/TASK-->

<!--HINT-->
### Hint 1
@abstractmethod def area(self): ...

### Hint 2
class Reader(Protocol): def read(self) -> str: ...

### Hint 3
self._flyer.fly() inside Duck.fly().

### Hint 4
__init__(self, writer); self._writer.write(...).

### Hint 5
validate returns bool.

### Hint 6
repo: Repository protocol in type hints.

### Hint 7
notify_all loops over notifiers.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self) -> float:
        return self.side ** 2

print(Square(4).area())   # 16
```

### Solution 2
```python
from typing import Protocol

class Reader(Protocol):
    def read(self) -> str: ...

def process(r: Reader) -> str:
    return r.read().upper()

class FileReader:
    def read(self) -> str:
        return "hello"

print(process(FileReader()))   # HELLO
```

### Solution 3
```python
class Flyable:
    def fly(self):
        return "flying"
class Swimmable:
    def swim(self):
        return "swimming"
class Duck:
    def __init__(self):
        self._flyer = Flyable()
        self._swimmer = Swimmable()
    def fly(self):
        return self._flyer.fly()
    def swim(self):
        return self._swimmer.swim()

d = Duck()
print(d.fly(), d.swim())
```

### Solution 4
```python
class Report:
    def __init__(self, writer):
        self._writer = writer
    def generate(self):
        self._writer.write("Annual report")
```

### Solution 5
```python
from typing import Protocol

class Validator(Protocol):
    def validate(self, value) -> bool: ...

class PositiveValidator:
    def validate(self, value) -> bool:
        return value > 0

class LengthValidator:
    def __init__(self, n=5):
        self.n = n
    def validate(self, value) -> bool:
        return len(value) >= self.n
```

### Solution 6
```python
class Repository(Protocol):
    def get_by_id(self, uid): ...

class MemoryRepository:
    def get_by_id(self, uid):
        return {1: "Anna"}.get(uid)
class DummyRepository:
    def get_by_id(self, uid):
        return "stub"

class UserService:
    def __init__(self, repo: Repository):
        self._repo = repo
    def get(self, uid):
        return self._repo.get_by_id(uid)
```

### Solution 7
```python
class Notifier(Protocol):
    def notify(self, message) -> None: ...

class EmailNotifier:
    def notify(self, message):
        print("Email:", message)
class SMSNotifier:
    def notify(self, message):
        print("SMS:", message)

class AlertService:
    def __init__(self, notifiers):
        self._notifiers = notifiers
    def notify_all(self, message):
        for n in self._notifiers:
            n.notify(message)

AlertService([EmailNotifier(), SMSNotifier()]).notify_all("Alert!")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is composition?
- Has-a relationship
- Is-a
- Inheritance
- Modules
* Correct answer: Has-a relationship
Objects inside objects.

What is ABC?
- Abstract base class
- Automatic class
- All classes
- Absolute
* Correct answer: Abstract base class
For contracts.

What does @abstractmethod do?
- Requires implementation in subclasses
- Removes method
- Adds default
- Nothing
* Correct answer: Requires implementation in subclasses
Abstraction.

What is Protocol?
- Structural type definition
- A class
- A module
- A decorator
* Correct answer: Structural type definition
Shape-based match.

What is structural typing?
- Matching by methods
- Matching by name
- By inheritance
- By module
* Correct answer: Matching by methods
Duck typing with type info.

What is dependency injection?
- Passing dependencies in
- Creating globally
- Importing only
- Deleting
* Correct answer: Passing dependencies in
Constructor/parameter.

Why mocking is easier with DI?
- Replace dependencies with fakes
- Faster
- Required
- No reason
* Correct answer: Replace dependencies with fakes
Isolation.

When to prefer Protocol over ABC?
- When only shape matters
- Always
- Never
- For methods
* Correct answer: When only shape matters
No inheritance burden.

What is the fragile base class problem?
- Parent change breaks children
- Children change parent
- No problem
- Memory leak
* Correct answer: Parent change breaks children
Deep hierarchies.

Can a class satisfy a Protocol without inheriting?
- Yes
- No
- Only same module
- Only named
* Correct answer: Yes
Structural match.

What is a "has-a" example?
- Car has Engine
- Car is Engine
- Car inherits Engine
- Car equals Engine
* Correct answer: Car has Engine
Composition.

What does DI improve?
- Testability
- Speed
- Memory only
- Syntax
* Correct answer: Testability
And flexibility.
<!--/QUIZ-->
