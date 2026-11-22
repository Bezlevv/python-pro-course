---
title: Exam: Senior-Level Tools
summary: Test your knowledge of modern syntax, debugging, code quality, patterns, algorithms, and publishing packages.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What does the := (walrus) operator do?
- Assigns a value to a variable inside an expression and immediately returns it
- Compares two values
- Declares a global variable
- Is no different from a regular =
* Correct answer: Assigns a value to a variable inside an expression and immediately returns it
For example, while (line := input()) != "": reads a line and immediately checks it in the condition.

What does the case _ pattern mean in match/case?
- A compilation error
- A wildcard: it catches everything that didn't match the previous branches
- A comment
- Repeating the previous branch
* Correct answer: A wildcard: it catches everything that didn't match the previous branches
case _ is the final default branch, like else in if/elif/else.

What benefit does Enum offer compared to plain strings or numbers?
- It speeds up program execution
- It gives named constants: a typo in a name immediately raises AttributeError instead of a value error later
- It reduces the number of imports
- It automatically sorts values
* Correct answer: It gives named constants: a typo in a name immediately raises AttributeError instead of a value error later
Enum members are compared by identity, and reading documentation by names is better than magic numbers.

What does ruff do?
- Runs the program with a debugger
- Finds errors and style issues in code and can fix them automatically
- Compiles Python code to machine code
- Formats code in a single style
* Correct answer: Finds errors and style issues in code and can fix them automatically
Ruff is a fast linter: it finds unused imports, undefined names, and style violations.

What does black do?
- Runs tests
- Automatically formats code in a single style
- Checks types
- Optimizes program speed
* Correct answer: Automatically formats code in a single style
Black is an uncompromising formatter: it rewrites code in one style, removing formatting arguments.

What does mypy do?
- Checks that values match type annotations
- Measures function execution time
- Deploys code to a server
- Sorts imports
* Correct answer: Checks that values match type annotations
Mypy is static type checking: it catches, for example, a function that promises to return str but returns float.

When do pre-commit hooks fire?
- On every program run
- On every git commit
- On every file save
- On every dependency install
* Correct answer: On every git commit
Hooks run before the commit, and if a check fails, the commit is blocked.

What does the factory method design pattern do?
- Provides a common interface for creating objects, leaving the concrete class to subclasses
- Forbids creating objects
- Synchronizes access to shared data
- Caches function call results
* Correct answer: Provides a common interface for creating objects, leaving the concrete class to subclasses
The factory method is a creational pattern: code works with an interface, and the subclass decides which object to create.

What is the time complexity of binary search on a sorted array?
- O(n)
- O(log n)
- O(n²)
- O(1)
* Correct answer: O(log n)
Each step halves the search area, so the number of steps grows logarithmically with the array size.

In which file are a modern Python package's metadata described?
- setup.py
- pyproject.toml
- requirements.txt
- Pipfile
* Correct answer: pyproject.toml
It's the unified standard (PEP 621) for metadata, builds, and tool settings; the command python -m build creates sdist and wheel.
<!--/QUIZ-->
