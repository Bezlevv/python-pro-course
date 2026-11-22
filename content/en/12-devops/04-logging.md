---
title: Monitoring and logging
summary: logging module, levels, structured logs.
order: 4
duration: 40 min
difficulty: intermediate
tags: logging, monitoring
---

Logging records what the app did.

## Basic logging

```python
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logging.info("started")
logging.error("something failed")
```

## Structured logs

```python
logging.info("user action", extra={"user": "alice"})
```

## Levels

DEBUG, INFO, WARNING, ERROR, CRITICAL.

## Lesson summary

Use logging, not print, for production observability.

<!--TASK-->
### Task 1 — Configure
Set level INFO with a format.

### Task 2 — Log
Use info/warning/error.

### Task 3 — Logger
Create a module logger.

### Task 4 — File
Write logs to a file.

### Task 5 — Structured
Add extra fields.

### Task 6 — Filter
Set DEBUG level and explain.

### Task 7 — Compare
print vs logging.
<!--/TASK-->

<!--HINT-->
### Hint 1
basicConfig.

### Hint 2
logging.info.

### Hint 3
getLogger(__name__).

### Hint 4
filename=.

### Hint 5
extra.

### Hint 6
Lowest level.

### Hint 7
Levels.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
```

### Solution 2
```python
logging.info("app started")
logging.warning("low disk")
logging.error("db connection failed")
```

### Solution 3
```python
logger = logging.getLogger(__name__)
logger.info("module loaded")
```

### Solution 4
```python
logging.basicConfig(filename="app.log", level=logging.INFO)
```

### Solution 5
```python
logging.info("login", extra={"user": "alice"})
```

### Solution 6
```python
# DEBUG: подробные диагностические сообщения,
# в продакшене обычно INFO и выше
```

### Solution 7
```python
# print: в stdout, нет уровней
# logging: уровни, файлы, форматы
```
<!--/SOLUTION-->

<!--QUIZ-->
What is logging?
- Event records
- Print
- Errors only
- None
* Correct answer: Event records
Module.

What is a level?
- Severity
- Text
- Format
- None
* Correct answer: Severity
DEBUG…CRITICAL.

What is INFO?
- Normal events
- Errors
- Debug
- None
* Correct answer: Normal events
Standard.

What is ERROR?
- Failures
- Info
- Debug
- None
* Correct answer: Failures
Logged.

What is basicConfig?
- One-time setup
- A logger
- A handler
- None
* Correct answer: One-time setup
Global.

What is getLogger?
- Module logger
- Print
- File
- None
* Correct answer: Module logger
Named.

What is a handler?
- Output destination
- Level
- Format
- None
* Correct answer: Output destination
Console/file.

What is a formatter?
- Output layout
- Destination
- Filter
- None
* Correct answer: Output layout
Template.

Why not print?
- No levels
- Faster
- Required
- None
* Correct answer: No levels
Production.

What is WARNING?
- Potential issue
- Fatal
- Debug
- None
* Correct answer: Potential issue
Attention.

What is DEBUG?
- Detailed diagnostics
- Errors
- Info
- None
* Correct answer: Detailed diagnostics
Verbose.

What is structured logging?
- Key-value fields
- Free text
- JSON always
- None
* Correct answer: Key-value fields
Searchable.
<!--/QUIZ-->
