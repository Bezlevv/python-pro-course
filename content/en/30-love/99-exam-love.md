---
title: Exam: The Soul of Python
summary: Test yourself on the whole module: from idioms and the Zen to the ecosystem and projects for the soul.
order: 99
duration: 30 min
difficulty: advanced
exam: true
---

<!--QUIZ-->
Which slice will return the string "python" in reverse order?
- "python"[::-1]
- "python"[::1]
- "python"[-1:]
* Correct answer: "python"[::-1]
A negative step of -1 traverses the sequence from the end.

What does the line a, b = b, a do?
- Swaps the values of a and b without a third variable
- Copies a into b
- Assigns the value of b to a, while b stays unchanged
* Correct answer: Swaps the values of a and b without a third variable
The right side builds a tuple that is unpacked into the variables on the left.

What will zip([1, 2], ["a", "b"]) wrapped in list() return?
- [(1, "a"), (2, "b")]
- [1, 2, "a", "b"]
- [(1, 2), ("a", "b")]
* Correct answer: [(1, "a"), (2, "b")]
zip pairs elements with the same indexes into tuples.

What does the keyword yield do in a function?
- Turns the function into a generator
- Returns the function
- Finishes the program
* Correct answer: Turns the function into a generator
yield temporarily pauses execution and hands out a value.

How many times can you iterate over a generator?
- Once, after which it is exhausted
- An infinite number of times
- Twice
* Correct answer: Once, after which it is exhausted
A generator is lazy and doesn't repeat values after a full pass.

What does @functools.cache do?
- Caches the results of function calls
- Speeds up the internet
- Remembers the function name
* Correct answer: Caches the results of function calls
cache saves the result for each argument and reuses it.

Which block catches the error when dividing by zero?
- except ZeroDivisionError
- except TypeError
- except ValueError
* Correct answer: except ZeroDivisionError
ZeroDivisionError occurs precisely when dividing by zero.

What does itertools.cycle(["a", "b"]) do?
- Infinitely repeats the elements
- Returns a list
- Sorts the list
* Correct answer: Infinitely repeats the elements
cycle loops the sequence: a, b, a, b, ...

Why is field(default_factory=list) needed in a dataclass?
- So each object gets a separate list
- So the list is shared
- So the field is required
* Correct answer: So each object gets a separate list
default_factory creates a new list for each instance.

What is PyPI?
- A warehouse of Python packages
- A programming language
- An installation command
* Correct answer: A warehouse of Python packages
PyPI is the library repository from which pip installs packages.
<!--/QUIZ-->
