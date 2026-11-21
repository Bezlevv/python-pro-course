---
title: Working with files
summary: Reading and writing text files, context managers, encodings, paths.
order: 12
duration: 35 min
difficulty: intermediate
tags: files, open, with, read, write
---

Files let programs store data between runs.

## Writing

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")
```

Modes: "w" (write, clears), "a" (append), "r" (read), "r+" (read/write).

## Reading

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()          # whole text
    lines = f.readlines()       # list of lines
```

Or iterate line by line:

```python
with open("data.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

## Context manager

`with` closes the file even on errors — always use it.

## Encodings

Use `encoding="utf-8"` for Russian text to avoid mojibake.

## Paths

`pathlib.Path` helps build paths reliably:

```python
from pathlib import Path
p = Path("data.txt")
print(p.exists(), p.read_text(encoding="utf-8"))
```

## Lesson summary

We learned to read/write files with `with`, choose modes, and use encoding correctly.

<!--TASK-->
### Task 1 — Write a file
Create "hello.txt" with two lines using open(..., "w"). Check the file exists.

### Task 2 — Append
Append a third line with mode "a"; then read the file and print the content.

### Task 3 — Read lines
Read "hello.txt" and print every line with its number (use enumerate).

### Task 4 — Count lines and words
Read a text file and print the number of lines and total words.

### Task 5 — Safe write with with
Rewrite the file using `with`; verify it closes automatically (no explicit close).

### Task 6 — Pathlib
Using Path, print exists(), name, suffix for "hello.txt".

### Task 7 — Write numbers
Write squares 1..10 into "squares.txt" (one per line), then read and print the sum of them.
<!--/TASK-->

<!--HINT-->
### Hint 1
open("hello.txt", "w") creates/clears the file.

### Hint 2
Mode "a" adds to the end.

### Hint 3
for i, line in enumerate(f): ...

### Hint 4
words = len(content.split()).

### Hint 5
with open(...) as f: block manages close.

### Hint 6
Path methods: exists(), name, suffix.

### Hint 7
Write in a loop; then read and sum.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.write("World\n")
```

### Solution 2
```python
with open("hello.txt", "a", encoding="utf-8") as f:
    f.write("Third line\n")

with open("hello.txt", encoding="utf-8") as f:
    print(f.read())
```

### Solution 3
```python
with open("hello.txt", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(i, line.strip())
```

### Solution 4
```python
with open("hello.txt", encoding="utf-8") as f:
    content = f.read()
print("Lines:", content.count("\n") + 1)
print("Words:", len(content.split()))
```

### Solution 5
```python
with open("hello.txt", "w", encoding="utf-8") as f:
    f.write("New content\n")
# файл закрыт автоматически после блока
```

### Solution 6
```python
from pathlib import Path
p = Path("hello.txt")
print(p.exists())    # True
print(p.name)        # hello.txt
print(p.suffix)      # .txt
```

### Solution 7
```python
with open("squares.txt", "w", encoding="utf-8") as f:
    for i in range(1, 11):
        f.write(f"{i*i}\n")

total = 0
with open("squares.txt", encoding="utf-8") as f:
    for line in f:
        total += int(line.strip())
print(total)   # 385
```
<!--/SOLUTION-->

<!--QUIZ-->
What does mode "w" do?
- Clears and writes
- Appends
- Reads
- Creates dir
* Correct answer: Clears and writes
Write mode.

What does mode "a" do?
- Appends to the end
- Clears
- Reads
- Rewrites
* Correct answer: Appends to the end
Append mode.

Why use with?
- File closes automatically
- It is faster
- Required for reading
- Nothing
* Correct answer: File closes automatically
Even on exceptions.

What does f.read() return?
- The whole text
- List of lines
- Bytes
- None
* Correct answer: The whole text
Single string.

What does f.readlines() return?
- List of lines
- Whole text
- Generator
- None
* Correct answer: List of lines
Each line as a string.

Which encoding for Russian text?
- utf-8
- ascii
- latin-1
- binary
* Correct answer: utf-8
Avoids mojibake.

What does Path("a.txt").exists() return?
- Boolean
- Name
- Size
- Content
* Correct answer: Boolean
True if exists.

What is p.suffix?
- ".txt"
- "a.txt"
- "a"
- None
* Correct answer: ".txt"
File extension.

How to write several lines?
- Loop with write
- write_all
- append lines
- print to file
* Correct answer: Loop with write
One call per line or with \n.

What happens if file is missing and mode "r"?
- FileNotFoundError
- Empty file
- Created
- None
* Correct answer: FileNotFoundError
Read requires the file.

How to read line by line?
- for line in f:
- f.read()
- f.readlines() all
- f.line()
* Correct answer: for line in f:
Iteration over the file object.

What does int(line.strip()) do in reading numbers?
- Converts the line to int
- Strips file
- Reads binary
- Errors
* Correct answer: Converts the line to int
Clean and convert.
<!--/QUIZ-->
