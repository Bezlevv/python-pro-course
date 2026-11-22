---
title: Useful libraries overview
summary: Popular tools for common tasks.
order: 1
duration: 40 min
difficulty: intermediate
tags: libraries
---

The ecosystem has a library for almost everything.

## Categories

- Data: pandas, polars, NumPy;
- Web: requests, aiohttp, FastAPI;
- CLI: typer, click, rich;
- Utils: more-itertools, python-dateutil.

## Install

```bash
pip install pandas rich typer
```

## Example: rich

```python
from rich import print
print("[bold green]Hello[/bold green]")
```

## Lesson summary

Pick the right library per task.

<!--TASK-->
### Task 1 — Data
Name two data libraries.

### Task 2 — Web
Name two web libraries.

### Task 3 — CLI
Name a CLI library.

### Task 4 — Rich
Print colored text.

### Task 5 — Choice
Which for CSV analysis?

### Task 6 — Docs
Where to check docs?

### Task 7 — Compare
pandas vs polars.
<!--/TASK-->

<!--HINT-->
### Hint 1
pandas.

### Hint 2
requests.

### Hint 3
typer.

### Hint 4
rich.

### Hint 5
pandas.

### Hint 6
PyPI.

### Hint 7
Speed.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
pandas, polars, NumPy
```

### Solution 2
```text
requests, aiohttp, FastAPI, httpx
```

### Solution 3
```text
typer, click, argparse, rich
```

### Solution 4
```python
from rich import print
print("[bold green]Done[/bold green]")
```

### Solution 5
```text
pandas — для CSV и таблиц; polars — если нужна скорость
```

### Solution 6
```text
PyPI (pypi.org), официальные доки, GitHub
```

### Solution 7
```text
pandas: широкие возможности, зрелый
polars: быстрее, меньше памяти, похожий API
```
<!--/SOLUTION-->

<!--QUIZ-->
What is pandas?
- Data library
- Web
- CLI
- None
* Correct answer: Data library
Tables.

What is polars?
- Fast data library
- Slow
- Web
- None
* Correct answer: Fast data library
Rust.

What is requests?
- HTTP client
- Data
- CLI
- None
* Correct answer: HTTP client
GET.

What is aiohttp?
- Async HTTP
- Sync
- Data
- None
* Correct answer: Async HTTP
asyncio.

What is typer?
- CLI builder
- GUI
- Web
- None
* Correct answer: CLI builder
Commands.

What is rich?
- Pretty output
- Data
- HTTP
- None
* Correct answer: Pretty output
Colors.

What is PyPI?
- Package index
- A database
- A browser
- None
* Correct answer: Package index
pip.

What is pip?
- Installer
- Compiler
- Linter
- None
* Correct answer: Installer
Packages.

What is a dependency?
- Library
- Code
- Test
- None
* Correct answer: Library
Used.

What is a DataFrame?
- Table object
- List
- String
- None
* Correct answer: Table object
pandas.

What is a CLI?
- Command line
- GUI
- Web
- None
* Correct answer: Command line
Terminal.

What is the ecosystem?
- Libraries
- One tool
- A language only
- None
* Correct answer: Libraries
Variety.
<!--/QUIZ-->
