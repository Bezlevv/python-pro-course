---
title: CLI utilities: argparse
summary: Parsing command-line arguments, flags, defaults and subcommands.
order: 6
duration: 40 min
difficulty: intermediate
tags: argparse, cli, flags
---

Command-line tools read arguments. argparse is the standard way.

## Basic parser

```python
import argparse

parser = argparse.ArgumentParser(description="My tool")
parser.add_argument("--name", default="world")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
print(f"Hello, {args.name}")
```

## Positional arguments

```python
parser.add_argument("file")
# python tool.py data.txt
```

## Types

```python
parser.add_argument("--count", type=int, default=1)
```

## Choices

```python
parser.add_argument("--mode", choices=["fast", "safe"], default="safe")
```

## Subcommands

```python
sub = parser.add_subparsers(dest="command")
hello = sub.add_parser("hello")
hello.add_argument("--name", default="world")
```

## Lesson summary

argparse handles flags, defaults, types, choices and subcommands.

<!--TASK-->
### Task 1 — Hello flag
Create a script with --name (default "world") printing "Hello, ...".

### Task 2 — Verbose flag
Add --verbose (store_true); print extra info when present.

### Task 3 — Count with type
Add --count int with default 1; repeat hello count times.

### Task 4 — Choices
Add --mode with choices ["fast","safe"]; use it.

### Task 5 — Positional
Add a positional file argument; print its name.

### Task 6 — Help
Run commands with -h and show the help output.

### Task 7 — Subcommands
Implement hello and add subcommands (calc with op and numbers).
<!--/TASK-->

<!--HINT-->
### Hint 1
parser.add_argument("--name", default="world").

### Hint 2
action="store_true".

### Hint 3
type=int, default=1; loop range(args.count).

### Hint 4
choices=["fast", "safe"].

### Hint 5
parser.add_argument("file").

### Hint 6
python tool.py -h.

### Hint 7
add_subparsers(dest="command").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--name", default="world")
args = parser.parse_args()
print(f"Hello, {args.name}")
```

### Solution 2
```python
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()
if args.verbose:
    print("verbose mode")
```

### Solution 3
```python
parser.add_argument("--count", type=int, default=1)
args = parser.parse_args()
for _ in range(args.count):
    print("Hi")
```

### Solution 4
```python
parser.add_argument("--mode", choices=["fast", "safe"], default="safe")
args = parser.parse_args()
print(args.mode)
```

### Solution 5
```python
parser.add_argument("file")
args = parser.parse_args()
print(args.file)
```

### Solution 6
```bash
python tool.py -h
```

### Solution 7
```python
sub = parser.add_subparsers(dest="command")
calc = sub.add_parser("calc")
calc.add_argument("op", choices=["add", "sub"])
calc.add_argument("a", type=int)
calc.add_argument("b", type=int)
args = parser.parse_args()
if args.command == "calc":
    print(args.a + args.b if args.op == "add" else args.a - args.b)
```
<!--/SOLUTION-->

<!--QUIZ-->
Which module parses CLI args?
- argparse
- sys.argv by hand
- json
- logging
* Correct answer: argparse
Standard tool.

What does add_argument do?
- Declares a parameter
- Parses
- Runs
- Imports
* Correct answer: Declares a parameter
Configuration.

What is default?
- Value when argument absent
- Required
- Choice
- Type
* Correct answer: Value when argument absent
Fallback.

What does store_true do?
- Flag becomes True if present
- Stores string
- Counts
- Asks
* Correct answer: Flag becomes True if present
Boolean flags.

What is type=int for?
- Converts to int
- Validates letters
- Default
- Help
* Correct answer: Converts to int
Parsed type.

What are choices?
- Allowed values
- Required values
- Defaults
- Types
* Correct answer: Allowed values
Error otherwise.

What is a positional argument?
- Argument without flag
- --name
- -h
- choices
* Correct answer: Argument without flag
Order-based.

What does parse_args return?
- Namespace with args
- Dict
- List
- None
* Correct answer: Namespace with args
args.name etc.

What does -h do?
- Shows help
- Runs
- Deletes
- Errors
* Correct answer: Shows help
Auto-generated.

What are subcommands?
- Separate sets of args
- Flags
- Types
- Choices
* Correct answer: Separate sets of args
Like git add/commit.

What is dest?
- Attribute name for arg
- Default
- Type
- Help
* Correct answer: Attribute name for arg
args.dest.

Can you run argparse without args?
- Yes, if defaults exist
- No
- Only with -h
- Error always
* Correct answer: Yes, if defaults exist
Optional flags.
<!--/QUIZ-->
