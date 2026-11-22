---
title: Configs: YAML, JSON, TOML
summary: Reading/writing configuration formats.
order: 2
duration: 40 min
difficulty: intermediate
tags: yaml, json, toml
---

Configs keep settings outside code.

## JSON

```python
import json
data = {"debug": True, "port": 8000}
json.dump(data, open("config.json", "w"), indent=2)
loaded = json.load(open("config.json"))
```

## YAML

```python
import yaml
data = {"app": {"port": 8000}}
yaml.dump(data, open("config.yaml", "w"))
loaded = yaml.safe_load(open("config.yaml"))
```

## TOML

```python
import tomllib
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
```

## Lesson summary

Three standard config formats; pick by ecosystem.

<!--TASK-->
### Task 1 — JSON write
Write config to JSON with indent.

### Task 2 — JSON read
Read it back.

### Task 3 — YAML
Write and read YAML.

### Task 4 — TOML
Read a TOML file.

### Task 5 — Compare
List differences in comments.

### Task 6 — Nested
Store nested config.

### Task 7 — Env override
Merge env var with config.
<!--/TASK-->

<!--HINT-->
### Hint 1
json.dump.

### Hint 2
json.load.

### Hint 3
yaml.safe_load.

### Hint 4
tomllib.

### Hint 5
Comments.

### Hint 6
Dict.

### Hint 7
os.environ.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import json
config = {"app": {"port": 8000, "debug": True}}
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
```

### Solution 2
```python
with open("config.json", encoding="utf-8") as f:
    data = json.load(f)
print(data["app"]["port"])
```

### Solution 3
```python
import yaml
with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f)
with open("config.yaml", encoding="utf-8") as f:
    data = yaml.safe_load(f)
```

### Solution 4
```python
import tomllib
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
print(data.get("project", {}))
```

### Solution 5
```python
# JSON: универсален, без комментариев
# YAML: читаемый, комментарии
# TOML: строгий, для метаданных
```

### Solution 6
```python
config = {"db": {"host": "localhost", "port": 5432}}
```

### Solution 7
```python
import os
port = int(os.environ.get("PORT", config["app"]["port"]))
```
<!--/SOLUTION-->

<!--QUIZ-->
What is json.dump?
- Writes JSON
- Reads
- Parses
- None
* Correct answer: Writes JSON
To file.

What is json.load?
- Reads JSON
- Writes
- Converts
- None
* Correct answer: Reads JSON
From file.

What is yaml.safe_load?
- Safe parse
- Dump
- Execute
- None
* Correct answer: Safe parse
Security.

What is tomllib?
- TOML parser
- Writer
- YAML
- None
* Correct answer: TOML parser
Standard.

Why indent=2?
- Readable
- Smaller
- Faster
- None
* Correct answer: Readable
Pretty.

What is a nested config?
- Dict in dict
- Flat
- List
- None
* Correct answer: Dict in dict
Sections.

What is os.environ.get?
- Reads env var
- Sets
- Deletes
- None
* Correct answer: Reads env var
Override.

Why configs outside code?
- Change without code
- Speed
- Style
- None
* Correct answer: Change without code
Deploy.

Which format supports comments?
- YAML
- JSON
- Both
- None
* Correct answer: YAML
Readable.

Which is strict?
- TOML
- JSON
- YAML
- None
* Correct answer: TOML
Typed.

What is safe_load?
- Parses without objects
- Executes
- Dumps
- None
* Correct answer: Parses without objects
Secure.

What is a default in get?
- Fallback
- Error
- None
- Delete
* Correct answer: Fallback
Safe.
<!--/QUIZ-->
