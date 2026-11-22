---
title: Modern syntax: match/case, walrus, Enum
summary: Structural pattern matching, walrus operator, enums.
order: 1
duration: 40 min
difficulty: intermediate
tags: match, walrus, enum
---

Newer Python versions add expressive syntax.

## match/case

```python
def handle(command):
    match command:
        case "start":
            return "Starting"
        case "stop":
            return "Stopping"
        case ("move", x, y):
            return f"Move to {x}, {y}"
        case _:
            return "Unknown"
```

## Walrus

```python
while (line := input("> ")) != "quit":
    print(line.upper())
```

## Enum

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2

print(Color.RED.value)
```

## Lesson summary

match/case, := and Enum make code cleaner and safer.

<!--TASK-->
### Task 1 — match
Implement handle() with 3 cases.

### Task 2 — Tuple pattern
Match ("move", x, y).

### Task 3 — Wildcard
Add a default case.

### Task 4 — Walrus
Rewrite a read-until loop with :=.

### Task 5 — Enum
Define Color and print values.

### Task 6 — Compare enums
Check equality of two enum members.

### Task 7 — Type hints with Enum
Write a function accepting Color.
<!--/TASK-->

<!--HINT-->
### Hint 1
match command:.

### Hint 2
case ("move", x, y).

### Hint 3
case _:.

### Hint 4
while (line := input(...)).

### Hint 5
Enum class.

### Hint 6
== works.

### Hint 7
def f(c: Color).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def handle(command):
    match command:
        case "start":
            return "Starting"
        case "stop":
            return "Stopping"
        case _:
            return "Unknown"
```

### Solution 2
```python
case ("move", x, y):
    return f"Move to {x}, {y}"
```

### Solution 3
```python
case _:
    return "Unknown"
```

### Solution 4
```python
while (line := input("> ")) != "quit":
    print(line.upper())
```

### Solution 5
```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED.value, Color.GREEN.name)
```

### Solution 6
```python
print(Color.RED == Color.RED)      # True
print(Color.RED == Color.GREEN)    # False
```

### Solution 7
```python
def paint(c: Color) -> str:
    return f"paint {c.name.lower()}"

print(paint(Color.RED))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is match?
- Structural pattern matching
- A loop
- A regular expression
- None
* Correct answer: Structural pattern matching
Python 3.10+.

What is case?
- A pattern branch
- A variable
- A loop
- None
* Correct answer: A pattern branch
Match.

What is the wildcard?
- case _:
- case *:
- default:
- else:
* Correct answer: case _:
Anything.

What does := do?
- Assigns and returns
- Compares
- Deletes
- None
* Correct answer: Assigns and returns
Walrus.

What is Enum?
- Named constants
- A class? yes
- A dict
- None
* Correct answer: Named constants
Grouped.

What is .value?
- Stored value
- Name
- Type
- None
* Correct answer: Stored value
Int.

What is .name?
- Member name
- Value
- Type
- None
* Correct answer: Member name
String.

Can enums be compared?
- Yes, with ==
- No
- Only <
- None
* Correct answer: Yes, with ==
Identity.

Why Enum?
- Readable constants
- Faster
- Shorter
- None
* Correct answer: Readable constants
Safety.

What is a guard in match?
- if after pattern
- A loop
- A variable
- None
* Correct answer: if after pattern
case x if x > 0:.

Is := allowed in if?
- Yes
- No
- Only while
- None
* Correct answer: Yes
if (n := len(x)) > 5:.

What Python is match in?
- 3.10+
- 3.8
- 3.6
- 2.7
* Correct answer: 3.10+
Newer.
<!--/QUIZ-->
