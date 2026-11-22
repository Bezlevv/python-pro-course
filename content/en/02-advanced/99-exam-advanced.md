---
title: Exam: Advanced Python
summary: Test your knowledge of advanced Python: OOP, decorators, generators, context managers, typing, async, regular expressions and venv.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which method is called automatically when an object of a class is created?
- __init__
- __new__
- __main__
- __start__
* Correct answer: __init__
The __init__ method is the constructor; it initializes a new object.

Why is super().__init__() called in a subclass?
- To redefine the class
- To call a parent class method
- To create a new object
- To terminate the program
* Correct answer: To call a parent class method
super() accesses methods of the base class, preserving the parent's initialization.

What does a decorator do to a function?
- Deletes the function
- Speeds up code execution
- Wraps the function, extending its behavior
- Changes the function's name
* Correct answer: Wraps the function, extending its behavior
A decorator is a function that takes a function and returns a new version with additional behavior.

How is a generator different from a regular function?
- It returns a list immediately
- It uses yield and computes values lazily
- It cannot take arguments
- It always returns None
* Correct answer: It uses yield and computes values lazily
A generator yields values one at a time via yield and doesn't store them all in memory at once.

Which methods does a context manager implement?
- __open__ / __close__
- __enter__ / __exit__
- __start__ / __stop__
- __begin__ / __end__
* Correct answer: __enter__ / __exit__
A with block calls __enter__ on entry and __exit__ on exit, even if an error occurred.

What is lambda?
- A data type
- An anonymous function
- A module
- A decorator
* Correct answer: An anonymous function
lambda x: x * 2 creates a small nameless function in a single expression.

Which decorator simplifies creating data storage classes?
- @classmethod
- @dataclass
- @property
- @staticmethod
* Correct answer: @dataclass
@dataclass automatically generates __init__, __repr__ and comparison for the class fields.

How do you declare an async function?
- async def fetch_data(): ...
- await def fetch_data(): ...
- async function fetch_data(): ...
- def fetch_data() async: ...
* Correct answer: async def fetch_data(): ...
Async functions are declared with async def, and results are awaited with await.

What does re.findall(r"\d+", "цена: 100 руб.") return?
- ["100"]
- ["цена", "100"]
- [100]
- ["цена:"]
* Correct answer: ["100"]
re.findall returns a list of all matches of the pattern; \d+ finds sequences of digits.

How do you create an isolated environment for a project?
- pip freeze
- python -m venv env
- python install env
- pip install venv
* Correct answer: python -m venv env
The command python -m venv creates a virtual environment with its own packages.
<!--/QUIZ-->
