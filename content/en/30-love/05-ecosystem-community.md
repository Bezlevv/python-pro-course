---
title: Ecosystem and Community
summary: PyPI, pip, and hundreds of thousands of libraries: how the world of Python works and why helping each other is the norm here.
order: 5
duration: 25 min
difficulty: beginner
tags: pip, PyPI, libraries, community, open source
---

Python is strong not only by itself but also by everything built around it: libraries, tools, and people. Today we'll peek into this world and learn to navigate it.

## PyPI: the gold mine

The main warehouse of Python packages is called PyPI (Python Package Index) — it's the site `pypi.org`, where hundreds of thousands of libraries live. If you need a function, there's a 99% chance someone has already written a library for it. Drawing charts, parsing websites, making games, working with spreadsheets, Telegram bots, neural networks — ready-made solutions exist for all of it.

## pip: the magic courier

Libraries are installed with the `pip` command right from the terminal:

```bash
pip install requests
```

This command downloads the package from PyPI and installs it into your environment. Then you can simply import it:

```python
import requests
```

There are many packages, so it's customary to keep their list in a `requirements.txt` file — then anyone can reproduce your environment with the single command `pip install -r requirements.txt`.

## Well-known libraries

Here are a few names you'll keep running into:

- `requests` — HTTP requests to websites;
- `beautifulsoup4` — parsing HTML pages;
- `numpy` — math and arrays;
- `pandas` — tables and data analysis;
- `matplotlib` — charts and visualization;
- `django` and `flask` — websites;
- `pygame` — games;
- `pillow` — working with images;
- `pytest` — testing.

What matters: **free and open**. Almost all libraries are open source: the source code is open, and you can read, study, and improve it. It's the best textbook imaginable.

## Environments and cleanliness

Different projects require different library versions. To keep them from interfering, virtual environments are used:

```bash
python -m venv .venv
```

On Windows, activate it with `.venv\Scripts\activate`; on macOS/Linux: `source .venv/bin/activate`. After that, `pip` installs packages into an isolated environment.

## Community: people who love Python

People stand behind the language. PyCon conferences are held annually in dozens of countries, including PyCon Russia. The PEP (Python Enhancement Proposal) project is documents proposing language improvements: anyone can propose their idea. And the Python Software Foundation (PSF) is a non-profit organization that governs the language's development.

Even a beginner can help the community: answer a question on a forum, translate documentation, report a bug in a library, write a post about what you learned. That's how everything grows: people share, and the language gets better. The Zen of Python says: "Now is better than never" — so start participating today.

Now practice — all of it on the standard library, nothing to install.

<!--TASK-->
### Task 1
Create a dictionary `library_guide` where the key is the library name and the value is a short description of what it's for. Include at least five libraries from the lesson (for example, `requests`, `pandas`, `matplotlib`, `django`, `pygame`). Then print the dictionary contents as a table: on each line — the name and description separated by `—`. Use a loop over `items()`. Expected result: five lines like `requests — HTTP requests to websites`.

### Task 2
Write a function `recommend(task)` that returns the name of a suitable library based on a task description. Use a dictionary with task keys: `"website"` → `"django"`, `"chart"` → `"matplotlib"`, `"table"` → `"pandas"`, `"game"` → `"pygame"`, `"requests"` → `"requests"`. If the task is not in the dictionary — return the string `I don't know, search on PyPI!`. Test the function with five keys and one absent word. Expected output: five names and a warning for the unknown task.

### Task 3
Write a program that checks which libraries are already installed in the system. Create a list of names: `["requests", "pandas", "flask", "pygame"]`. For each name, try to import the module (`importlib.import_module`) and print `requests — installed` or `requests — not installed`. Use `try/except ImportError`. Expected result: four lines with the real status for your computer.

### Task 4
Create a function `print_requirements(packages)` that takes a list of libraries and prints line by line the contents of a future `requirements.txt` file — each library on its own line without quotes or brackets. Before the list, print the heading `My requirements.txt:`. Use `str.join` for neat output. Test it on the list `["requests", "pandas", "matplotlib"]`. Expected output: the heading and three lines with names.

### Task 5
Write a "Community advice" program that helps choose what to do today. Create a list of five ideas: `"read pandas documentation"`, `"write a post about what you learned"`, `"answer a beginner's question"`, `"study the source code of a favorite library"`, `"take part in PyCon"`. Pick a random idea with `random.choice` and print the phrase `Today I: <idea>!`. Expected result: one random line with the phrase.

<!--/TASK-->

<!--HINT-->
### Hint 1
A dictionary is created like this: `library_guide = {"requests": "HTTP requests to websites"}`. The loop `for name, description in library_guide.items():` unpacks the pairs. For output use `print(f"{name} — {description}")`.

### Hint 2
A function with `if task in guide:` and `return guide[task]`, and at the end — `return "I don't know, search on PyPI!"`. Or use `guide.get(task, "I don't know, search on PyPI!")` — that's shorter and safer.

### Hint 3
`import importlib`, then `importlib.import_module(name)`. If the module exists, the import succeeds; if not, `ImportError` is raised. Handle it with `except ImportError:`.

### Hint 4
`"\n".join(packages)` joins the elements with newlines. Before that, print the heading. Don't add quotes — just the library names.

### Hint 5
`import random`, then `idea = random.choice(ideas)`. Store the list of ideas in a variable, then plug the chosen idea into the string. Run the program several times — you'll get a different piece of advice each time.

<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
library_guide = {
    "requests": "HTTP requests to websites",
    "pandas": "tables and data analysis",
    "matplotlib": "charts and visualization",
    "django": "websites",
    "pygame": "games",
}

for name, description in library_guide.items():
    print(f"{name} — {description}")
```

Result:

```
requests — HTTP requests to websites
pandas — tables and data analysis
matplotlib — charts and visualization
django — websites
pygame — games
```

What's happening here? We store data in a dictionary where the key is the library name and the value is the description. The loop `for name, description in library_guide.items()` unpacks each pair. The f-string assembles the output line. This approach is convenient: to add a library, just write one more line in the dictionary — the loop will print it on its own. Data is separated from output logic, which is good style.

### Walkthrough 2
Solution:

```python
guide = {
    "website": "django",
    "chart": "matplotlib",
    "table": "pandas",
    "game": "pygame",
    "requests": "requests",
}

def recommend(task):
    return guide.get(task, "I don't know, search on PyPI!")

for task in ["website", "chart", "table", "game", "requests", "bot"]:
    print(task, "→", recommend(task))
```

Result:

```
website → django
chart → matplotlib
table → pandas
game → pygame
requests → requests
bot → I don't know, search on PyPI!
```

What's happening here? The `dict.get(task, default)` method is a safe way to fetch a value: if the key is missing, the default value is returned. This way the `recommend` function does everything in one line: no `if` or explicit `return` for a missing key. That's idiomatic Python: short, clear, and without branching. Testing on five known tasks and one unknown word shows both paths.

### Walkthrough 3
Solution:

```python
import importlib

packages = ["requests", "pandas", "flask", "pygame"]

for name in packages:
    try:
        importlib.import_module(name)
        print(f"{name} — installed")
    except ImportError:
        print(f"{name} — not installed")
```

Result (example):

```
requests — installed
pandas — installed
flask — not installed
pygame — not installed
```

What's happening here? `importlib.import_module(name)` tries to import a module by name — the same as `import requests`, but with a name from a variable. If the module is installed, the import succeeds and "installed" is printed. If not, `ImportError` is raised, which we catch and print "not installed." This technique is useful when you need to check dozens of packages without knowing in advance which are present. The result on your computer may differ — that's normal.

### Walkthrough 4
Solution:

```python
def print_requirements(packages):
    print("My requirements.txt:")
    print("\n".join(packages))

print_requirements(["requests", "pandas", "matplotlib"])
```

Result:

```
My requirements.txt:
requests
pandas
matplotlib
```

What's happening here? `"\n".join(packages)` joins the list elements with a newline character — resulting in multi-line text. That's what a real `requirements.txt` file looks like: one package name per line. This file is an industry standard: you can attach it to a project, and anyone can reproduce the environment with `pip install -r requirements.txt`. We don't print quotes, so the output exactly matches the real file format.

### Walkthrough 5
Solution:

```python
import random

ideas = [
    "read pandas documentation",
    "write a post about what you learned",
    "answer a beginner's question",
    "study the source code of a favorite library",
    "take part in PyCon",
]

idea = random.choice(ideas)
print(f"Today I: {idea}!")
```

Result (one of the variants):

```
Today I: study the source code of a favorite library!
```

What's happening here? `random.choice(ideas)` picks one random element from the list. Each run offers a different idea — a little "community oracle." The f-string plugs the chosen idea into the phrase. Although the result is random, the program always prints exactly one line. Such a random generator is a simple way to add life and surprise to any program.

<!--/SOLUTION-->

<!--QUIZ-->
What is PyPI?
- A warehouse of Python packages with hundreds of thousands of libraries
- A programming language
- A terminal
* Correct answer: A warehouse of Python packages with hundreds of thousands of libraries
PyPI is the Python Package Index: the main repository of libraries.

Which command installs a library?
- pip install library_name
- python run library_name
- install library_name
* Correct answer: pip install library_name
pip downloads the package from PyPI and installs it into the environment.

What is the file listing project dependencies called?
- requirements.txt
- dependencies.py
- packages.json
* Correct answer: requirements.txt
The command pip install -r requirements.txt reproduces the project environment.

Which library is needed for charts?
- matplotlib
- requests
- pygame
* Correct answer: matplotlib
matplotlib creates charts and diagrams.

Which library is needed for tables and data analysis?
- pandas
- flask
- pillow
* Correct answer: pandas
pandas works with tables in data analysis.

What is open source?
- The source code is open: you can read and improve it
- A closed program
- A program that cannot be downloaded
* Correct answer: The source code is open: you can read and improve it
Open code is available for study and improvement by the community.

Why are virtual environments needed?
- To isolate the dependencies of different projects
- To speed up the internet
- To hide code
* Correct answer: To isolate the dependencies of different projects
Environments keep library versions of different projects from conflicting.

How do you check inside a program whether a library is installed?
- Try to import it and catch ImportError
- Read the documentation
- Restart the computer
* Correct answer: Try to import it and catch ImportError
A missing module manifests as ImportError on import.

What does the abbreviation PSF stand for?
- Python Software Foundation — the organization governing Python's development
- Personal Software Format
- Python Simple File
* Correct answer: Python Software Foundation — the organization governing Python's development
PSF is a non-profit organization that supports the language.

What is PyCon?
- The Python community conference
- A library for games
- A pip command
* Correct answer: The Python community conference
PyCon is an annual conference where Python developers meet.
<!--/QUIZ-->
