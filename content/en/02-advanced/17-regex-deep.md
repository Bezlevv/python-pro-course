---
title: Regular expressions: advanced level
summary: Named groups, lookarounds, flags, substitution with functions, recursion and performance.
order: 17
duration: 55 min
difficulty: advanced
tags: regex, named groups, lookahead, verbose
---

Beyond basics, regex offers powerful instruments for precise text processing.

## Named groups

```python
import re
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2026-11")
print(m.group("year"), m.group("month"))
```

## Lookarounds

- (?=...) ahead; (?!...) not ahead;
- (?<=...) behind; (?<!...) not behind.

```python
re.findall(r"\d+(?= руб)", "100 руб, 50 долл")   # ['100']
```

## Flags

re.IGNORECASE, re.MULTILINE, re.DOTALL, re.VERBOSE.

## Substitution with functions

```python
re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "10 и 20")
```

## Compilation

```python
pattern = re.compile(r"\b\w{4}\b")
```

## Performance

Compile once; avoid catastrophic backtracking (nested quantifiers).

## Lesson summary

Advanced regex: named groups, lookarounds, flags, callable sub, compilation.

<!--TASK-->
### Task 1 — Named groups
Extract name and age from "Ivan 25" with named groups.

### Task 2 — Lookahead
Find numbers followed by "руб" in a mixed string.

### Task 3 — Lookbehind
Find numbers after "%" using lookbehind.

### Task 4 — MULTILINE
Find lines starting with "TODO" in multiline text.

### Task 5 — VERBOSE
Write a verbose date pattern with comments.

### Task 6 — Sub with function
Double all numbers in a string using re.sub with a function.

### Task 7 — Compile + finditer
Compile an email pattern and print start/end of each match.
<!--/TASK-->

<!--HINT-->
### Hint 1
(?P<name>\w+) (?P<age>\d+).

### Hint 2
\d+(?= руб).

### Hint 3
(?<=%)\d+.

### Hint 4
r"^TODO.*" with re.MULTILINE.

### Hint 5
re.X lets whitespace and comments.

### Hint 6
lambda m: str(int(m.group()) * 2).

### Hint 7
pattern.finditer(text).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
m = re.search(r"(?P<name>\w+) (?P<age>\d+)", "Ivan 25")
print(m.group("name"), m.group("age"))
```

### Solution 2
```python
print(re.findall(r"\d+(?= руб)", "100 руб, 50 долл"))   # ['100']
```

### Solution 3
```python
print(re.findall(r"(?<=%)\d+", "20%, 30%"))   # ['20', '30']
```

### Solution 4
```python
text = "TODO: fix\nwork done\nTODO: test"
print(re.findall(r"^TODO.*", text, flags=re.MULTILINE))
```

### Solution 5
```python
pattern = re.compile(r"""
    (?P<day>\d{2})   # day
    [-/]
    (?P<month>\d{2})
    [-/]
    (?P<year>\d{4})
""", re.VERBOSE)
print(pattern.search("25-01-2026").groupdict())
```

### Solution 6
```python
print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "10 и 20"))   # 20 и 40
```

### Solution 7
```python
pattern = re.compile(r"\b[\w.]+@[\w.]+\.[a-z]+\b")
for m in pattern.finditer("Mail: a@test.ru, b@example.org"):
    print(m.group(), m.start(), m.end())
```
<!--/SOLUTION-->

<!--QUIZ-->
How to name a group?
- (?P<name>...)
- (?<name>...)
- (name:...)
- (?P=name)
* Correct answer: (?P<name>...)
Access via group("name").

What is lookahead?
- Checks what follows without including it
- Captures
- Escapes
- Flags
* Correct answer: Checks what follows without including it
(?=...).

What is lookbehind?
- Checks what precedes
- What follows
- Captures
- Substitutes
* Correct answer: Checks what precedes
(?<=...).

What does re.MULTILINE do?
- ^/$ match line boundaries
- Ignores case
- Dot matches newlines
- Allows comments
* Correct answer: ^/$ match line boundaries
Per-line anchors.

What does re.VERBOSE do?
- Allows whitespace/comments in pattern
- Speeds up
- Removes groups
- Adds unicode
* Correct answer: Allows whitespace/comments in pattern
Readable patterns.

What does re.DOTALL do?
- . matches newlines too
- . matches only letters
- Disables flags
- Nothing
* Correct answer: . matches newlines too
Inclusive dot.

Can re.sub take a function?
- Yes
- No
- Only strings
- Only compiled
* Correct answer: Yes
Receives Match.

Why compile patterns?
- Reuse and speed
- Required
- Only for big texts
- Always error
* Correct answer: Reuse and speed
pattern = re.compile(...).

What is catastrophic backtracking?
- Exponential slowdown from nested quantifiers
- Fast failure
- A bug in re
- Memory leak
* Correct answer: Exponential slowdown from nested quantifiers
Example: (a+)+.

What does finditer return?
- Iterator of matches
- List
- String
- None
* Correct answer: Iterator of matches
For loops and positions.

What is \b?
- Word boundary
- Digit
- Space
- Newline
* Correct answer: Word boundary
Anchors.

How to get groups dict?
- m.groupdict()
- m.groups()
- m.group()
- m.items()
* Correct answer: m.groupdict()
Named groups as dict.
<!--/QUIZ-->
