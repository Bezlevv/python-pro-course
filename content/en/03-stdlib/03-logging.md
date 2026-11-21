---
title: Logging (logging)
summary: Levels, formatters, handlers, file logging and configuration.
order: 3
duration: 35 min
difficulty: intermediate
tags: logging, levels, handlers
---

Logging is better than print for diagnostics: levels, destinations, formats.

## Basic usage

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.debug("debug")     # not shown
logging.info("info")
logging.warning("warn")
logging.error("error")
```

## Levels

DEBUG < INFO < WARNING < ERROR < CRITICAL.

## Configuring

```python
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)
```

## Handlers

```python
logger = logging.getLogger("my")
handler = logging.StreamHandler()
logger.addHandler(handler)
```

## Lesson summary

Logging gives level-based, configurable diagnostics.

<!--TASK-->
### Task 1 — Basic levels
Set level=logging.DEBUG and log all five levels; observe output.

### Task 2 — File logging
Configure basicConfig with filename and write messages; read the file.

### Task 3 — Format
Use format with asctime, levelname, message; run and see output.

### Task 4 — Logger by name
Create logger = logging.getLogger("app"); log info.

### Task 5 — Only warning+
Set level=WARNING; verify info is not shown.

### Task 6 — Handler
Add StreamHandler to a logger and log.

### Task 7 — Exception logging
Log an exception with logger.exception inside except.
<!--/TASK-->

<!--HINT-->
### Hint 1
logging.debug/info/warning/error/critical.

### Hint 2
filename="app.log".

### Hint 3
format="%(asctime)s %(levelname)s %(message)s".

### Hint 4
logging.getLogger("app").

### Hint 5
level=logging.WARNING.

### Hint 6
handler = logging.StreamHandler(); logger.addHandler(handler).

### Hint 7
logger.exception("msg") inside except.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("d")
logging.info("i")
logging.warning("w")
logging.error("e")
logging.critical("c")
```

### Solution 2
```python
logging.basicConfig(filename="app.log", level=logging.INFO, encoding="utf-8")
logging.info("saved")
print(open("app.log", encoding="utf-8").read())
```

### Solution 3
```python
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logging.info("hello")
```

### Solution 4
```python
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.info("from app logger")
```

### Solution 5
```python
logging.basicConfig(level=logging.WARNING)
logging.info("hidden")     # not shown
logging.warning("shown")
```

### Solution 6
```python
logger = logging.getLogger("h")
h = logging.StreamHandler()
logger.addHandler(h)
logger.setLevel(logging.INFO)
logger.info("via handler")
```

### Solution 7
```python
logger = logging.getLogger("ex")
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("failed")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is the default level?
- WARNING
- DEBUG
- INFO
- ERROR
* Correct answer: WARNING
Messages below are hidden.

Which level is the lowest?
- DEBUG
- INFO
- WARNING
- ERROR
* Correct answer: DEBUG
Most verbose.

What does basicConfig do?
- Configures root logger
- Creates files
- Imports
- Deletes
* Correct answer: Configures root logger
Level, format, handlers.

What is a Formatter?
- Defines log line layout
- A place
- A level
- A file
* Correct answer: Defines log line layout
%(message)s etc.

What is %(asctime)s?
- Timestamp placeholder
- Level
- Message
- Name
* Correct answer: Timestamp placeholder
Current time.

What does a Handler do?
- Sends records somewhere
- Filters
- Formats
- Counts
* Correct answer: Sends records somewhere
Console/file.

Why logging over print?
- Levels and destinations
- Faster
- Import
- Simpler only
* Correct answer: Levels and destinations
Control output.

What does logger.exception do?
- Logs with traceback
- Relies
- Raises
- Stops
* Correct answer: Logs with traceback
Inside except.

What is the root logger?
- Default logger
- A child
- A handler
- A level
* Correct answer: Default logger
Used unless getLogger.

What does getLogger("app") do?
- Returns a named logger
- Creates file
- Sets format
- Imports
* Correct answer: Returns a named logger
Namespacing.

Can logging write to a file?
- Yes, via filename
- No
- Only console
- Only sys
* Correct answer: Yes, via filename
basicConfig(filename=...).

What is CRITICAL?
- Highest level
- Lowest
- Middle
- Not a level
* Correct answer: Highest level
Most severe.
<!--/QUIZ-->
