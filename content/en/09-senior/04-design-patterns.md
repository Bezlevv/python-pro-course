---
title: Design patterns
summary: Factory, Singleton, Observer, Strategy and when to use them.
order: 4
duration: 45 min
difficulty: advanced
tags: patterns, factory, singleton, observer
---

Patterns are reusable architecture solutions.

## Factory

```python
class EmailNotifier:
    def send(self, msg):
        print(f"Email: {msg}")

class SmsNotifier:
    def send(self, msg):
        print(f"SMS: {msg}")

def create_notifier(kind):
    if kind == "email":
        return EmailNotifier()
    if kind == "sms":
        return SmsNotifier()
    raise ValueError(kind)
```

## Singleton

```python
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

## Observer

```python
class Event:
    def __init__(self):
        self._handlers = []
    def subscribe(self, fn):
        self._handlers.append(fn)
    def emit(self, *args):
        for fn in self._handlers:
            fn(*args)
```

## Strategy

Swap algorithms at runtime via objects.

## Lesson summary

Patterns give proven structures; choose the simplest fit.

<!--TASK-->
### Task 1 — Factory
Create a notifier factory and use both types.

### Task 2 — Singleton
Verify Config() is the same object.

### Task 3 — Observer
Subscribe two functions and emit.

### Task 4 — Strategy
Implement a sorter with two strategies.

### Task 5 — Builder idea
Describe a builder in comments.

### Task 6 — Adapter
Wrap an external logger into a standard interface.

### Task 7 — When not to use
Explain when patterns are unnecessary.
<!--/TASK-->

<!--HINT-->
### Hint 1
create_notifier.

### Hint 2
__new__.

### Hint 3
subscribe/emit.

### Hint 4
Classes with sort method.

### Hint 5
Step-by-step construction.

### Hint 6
Wrapper class.

### Hint 7
Small code, simple if.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
n1 = create_notifier("email")
n2 = create_notifier("sms")
n1.send("Hi")
n2.send("Hi")
```

### Solution 2
```python
c1 = Config()
c2 = Config()
print(c1 is c2)   # True
```

### Solution 3
```python
e = Event()
e.subscribe(lambda x: print("A", x))
e.subscribe(lambda x: print("B", x))
e.emit(1)
```

### Solution 4
```python
class BubbleSort:
    def sort(self, data):
        return sorted(data)   # упрощённо

class QuickSort:
    def sort(self, data):
        return sorted(data, reverse=False)

def apply(strategy, data):
    return strategy.sort(data)
```

### Solution 5
```python
# Builder: пошаговое создание сложного объекта
# (например, запрос с опциями)
```

### Solution 6
```python
class StandardLogger:
    def log(self, msg):
        print(msg)

class ExternalLogger:
    def write(self, text):
        print("EXT", text)

class Adapter(StandardLogger):
    def __init__(self, external):
        self.external = external
    def log(self, msg):
        self.external.write(msg)
```

### Solution 7
```python
# Для 20 строк кода паттерн — избыточность.
# Паттерны полезны при росте и повторяемости.
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a factory?
- Creates objects by type
- A singleton
- A strategy
- None
* Correct answer: Creates objects by type
Centralized.

What is Singleton?
- One instance
- Many
- Factory
- Observer
* Correct answer: One instance
Global state.

What is Observer?
- Notifies subscribers
- Creates
- Sorts
- None
* Correct answer: Notifies subscribers
Event.

What is Strategy?
- Swappable algorithm
- Singleton
- Factory
- None
* Correct answer: Swappable algorithm
At runtime.

What is an Adapter?
- Wraps interface
- Creates
- Sorts
- None
* Correct answer: Wraps interface
Compatibility.

When use factory?
- Many variants
- One class
- Always
- Never
* Correct answer: Many variants
Choice.

When use Singleton?
- Shared state
- Per-instance
- Always
- Never
* Correct answer: Shared state
Config.

What is a pattern?
- Proven solution
- A library
- A test
- None
* Correct answer: Proven solution
Architecture.

Are patterns mandatory?
- No
- Yes
- Always
- Only Python
* Correct answer: No
Context.

What is YAGNI?
- You aren't gonna need it
- Yes always
- A pattern
- None
* Correct answer: You aren't gonna need it
Simplicity.

What is KISS?
- Keep it simple
- A pattern
- A library
- None
* Correct answer: Keep it simple
Prefer.

What is overengineering?
- Unneeded complexity
- Good design
- Tests
- None
* Correct answer: Unneeded complexity
Avoid.
<!--/QUIZ-->
