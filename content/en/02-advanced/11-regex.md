---
title: Regular expressions (re)
summary: Patterns, search/match/findall, groups, substitution and flags.
order: 11
duration: 45 min
difficulty: intermediate
tags: regex, re, patterns, groups, sub
---

Regular expressions describe text patterns. The `re` module applies them.

## Basics

```python
import re

text = "Contact: a@test.ru"
m = re.search(r"[\w.]+@[\w.]+\.[a-z]+", text)
print(m.group())   # a@test.ru
```

## Common functions

- re.search — first match anywhere;
- re.match — match at the start;
- re.findall — all matches as list;
- re.sub — replace;
- re.finditer — iterator of matches.

## Groups

```python
m = re.search(r"(\d{4})-(\d{2})", "2026-11")
print(m.group(1), m.group(2))
```

## Character classes

- \d — digit; \w — word char; \s — space;
- . — any char except newline;
- [a-z] — range; [^...] — negation.

## Quantifiers

- * — 0 or more; + — 1 or more; ? — 0 or 1;
- {n} — exactly n; {n,m} — from n to m.

## Flags

re.IGNORECASE, re.MULTILINE, re.DOTALL.

## Lesson summary

Regex is powerful for validation, parsing and search. Learn patterns step by step.

<!--TASK-->
### Task 1 — Find digits
Use re.findall(r"\d+", "Order 42: 3 items, 12 rub") → ["42","3","12"].

### Task 2 — Email search
Write a function find_email(text) using re.search to find the first email.

### Task 3 — Groups
Extract day, month, year from "25-01-2026" using three groups.

### Task 4 — Replace
Replace all digits in "a1b22c333" with "#" using re.sub.

### Task 5 — Validation
Write is_phone(s) that returns True for patterns like "+7 123 456-78-90".

### Task 6 — finditer
Use finditer to print positions (start, end) of words "python" in a text.

### Task 7 — Flags
Use re.IGNORECASE to find "PYTHON" in "I love Python" and return True.
<!--/TASK-->

<!--HINT-->
### Hint 1
r"\d+" matches digit sequences.

### Hint 2
Search for r"[\w.]+@[\w.]+\.[a-z]+".

### Hint 3
Parentheses create groups; m.group(1) etc.

### Hint 4
re.sub(r"\d+", "#", text).

### Hint 5
Pattern r"\+7 \d{3} \d{3}-\d{2}-\d{2}".

### Hint 6
for m in re.finditer(...): print(m.start(), m.end()).

### Hint 7
re.search(r"python", text, flags=re.IGNORECASE).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import re
print(re.findall(r"\d+", "Order 42: 3 items, 12 rub"))   # ['42','3','12']
```

### Solution 2
```python
def find_email(text):
    m = re.search(r"[\w.]+@[\w.]+\.[a-z]+", text)
    return m.group() if m else None

print(find_email("Contact: a@test.ru"))
```

### Solution 3
```python
m = re.search(r"(\d{2})-(\d{2})-(\d{4})", "25-01-2026")
print(m.group(1), m.group(2), m.group(3))   # 25 01 2026
```

### Solution 4
```python
print(re.sub(r"\d+", "#", "a1b22c333"))   # a#b#c#
```

### Solution 5
```python
def is_phone(s):
    return bool(re.fullmatch(r"\+7 \d{3} \d{3}-\d{2}-\d{2}", s))

print(is_phone("+7 123 456-78-90"))   # True
print(is_phone("12345"))              # False
```

### Solution 6
```python
text = "I love python, Python is fun"
for m in re.finditer(r"python", text, flags=re.IGNORECASE):
    print(m.start(), m.end())
```

### Solution 7
```python
print(bool(re.search(r"python", "I love Python", flags=re.IGNORECASE)))   # True
```
<!--/SOLUTION-->

<!--QUIZ-->
What does re.search do?
- Finds the first match anywhere
- Matches only at start
- Returns all
- Replaces
* Correct answer: Finds the first match anywhere
Returns Match or None.

What does re.findall return?
- List of all matches
- First match
- Generator
- None
* Correct answer: List of all matches
Strings by default.

What does \d match?
- A digit
- A word
- A space
- A letter
* Correct answer: A digit
0-9.

What does + mean?
- One or more
- Zero or more
- Zero or one
- Exactly one
* Correct answer: One or more
Quantifier.

What does * mean?
- Zero or more
- One or more
- Optional
- Exactly
* Correct answer: Zero or more
Quantifier.

What is a group?
- Parenthesized part of a pattern
- A list
- A flag
- A char
* Correct answer: Parenthesized part of a pattern
Captured.

How to get the first group?
- m.group(1)
- m[0]
- m.groups(1)
- m.group()
* Correct answer: m.group(1)
Indexed capture.

What does re.sub do?
- Replaces matches
- Searches
- Splits
- Compiles
* Correct answer: Replaces matches
With a replacement string/function.

What does re.IGNORECASE do?
- Ignores case
- Matches digits
- Line anchors
- Dotall
* Correct answer: Ignores case
Flags argument.

What does re.fullmatch do?
- Requires the whole string to match
- Matches anywhere
- Returns list
- Compiles
* Correct answer: Requires the whole string to match
Useful for validation.

What does \w match?
- Word character (letters, digits, _)
- Only letters
- Only digits
- Space
* Correct answer: Word character
Letters, digits, underscore.

What does re.finditer return?
- Iterator of Match objects
- List
- String
- None
* Correct answer: Iterator of Match objects
Useful for positions.
<!--/QUIZ-->
