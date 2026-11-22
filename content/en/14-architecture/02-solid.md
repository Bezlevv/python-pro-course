---
title: Clean Architecture and SOLID
summary: Principles that keep code flexible.
order: 2
duration: 50 min
difficulty: advanced
tags: solid, clean architecture
---

Solid principles guide maintainable design.

## SOLID

- S: single responsibility;
- O: open/closed;
- L: Liskov substitution;
- I: interface segregation;
- D: dependency inversion.

## In practice

```python
# D: зависеть от абстракций
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data): ...

class FileStorage(Storage):
    def save(self, data):
        with open("data.txt", "w") as f:
            f.write(data)

def run(storage: Storage, data):
    storage.save(data)
```

## Lesson summary

SOLID keeps modules small, open, and decoupled.

<!--TASK-->
### Task 1 — S
Split a class doing two jobs.

### Task 2 — O
Extend without editing (inheritance).

### Task 3 — L
Write a substitutable subclass.

### Task 4 — I
Split a broad interface.

### Task 5 — D
Inject dependency.

### Task 6 — Test
Swap storage in tests.

### Task 7 — When
When is SOLID overkill?
<!--/TASK-->

<!--HINT-->
### Hint 1
Two classes.

### Hint 2
Override.

### Hint 3
Contract.

### Hint 4
Small interfaces.

### Hint 5
Pass in.

### Hint 6
Fake.

### Hint 7
Small scripts.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
# Было: класс читает файл и печатает отчёт
# Стало: FileReader + ReportPrinter
```

### Solution 2
```python
class Report:
    def render(self):
        return "base"

class HtmlReport(Report):
    def render(self):
        return "<b>html</b>"
# новая функциональность — новый подкласс, без правки base
```

### Solution 3
```python
class Bird:
    def fly(self): return "fly"

class Sparrow(Bird):
    pass  # Sparrow можно использовать вместо Bird

def let_fly(bird: Bird):
    return bird.fly()
```

### Solution 4
```python
# Было: интерфейс с print() и scan()
# Стало: Printer и Scanner отдельно
```

### Solution 5
```python
class App:
    def __init__(self, storage: Storage):
        self.storage = storage
```

### Solution 6
```python
class FakeStorage(Storage):
    def __init__(self):
        self.data = None
    def save(self, data):
        self.data = data

app = App(FakeStorage())
```

### Solution 7
```python
# В маленьких скриптах SOLID избыточен;
# ценность растёт с размером проекта
```
<!--/SOLUTION-->

<!--QUIZ-->
What does S mean?
- Single responsibility
- Speed
- Size
- None
* Correct answer: Single responsibility
One job.

What does O mean?
- Open/closed
- Output
- Order
- None
* Correct answer: Open/closed
Extend.

What does L mean?
- Liskov substitution
- Loop
- Layer
- None
* Correct answer: Liskov substitution
Subclass.

What does I mean?
- Interface segregation
- Input
- Index
- None
* Correct answer: Interface segregation
Small.

What does D mean?
- Dependency inversion
- Data
- Delete
- None
* Correct answer: Dependency inversion
Abstract.

What is an ABC?
- Abstract base class
- A list
- An error
- None
* Correct answer: Abstract base class
abc.

What is abstractmethod?
- Declares interface
- Implements
- Deletes
- None
* Correct answer: Declares interface
Must.

What is dependency injection?
- Passing dependencies
- Creating inside
- Global
- None
* Correct answer: Passing dependencies
Constructor.

What is the benefit?
- Testability
- Speed
- Size
- None
* Correct answer: Testability
Fakes.

What is open/closed?
- Extend without edit
- Closed all
- Open all
- None
* Correct answer: Extend without edit
OCP.

What is a contract?
- Interface expectations
- A file
- A test
- None
* Correct answer: Interface expectations
LSP.

When skip SOLID?
- Small scripts
- Big apps
- Always
- None
* Correct answer: Small scripts
Overhead.
<!--/QUIZ-->
