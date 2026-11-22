---
title: Debugging and profiling
summary: pdb, breakpoint(), cProfile, reading stack traces.
order: 2
duration: 45 min
difficulty: intermediate
tags: pdb, debugging, cProfile
---

Debuggers pause code; profilers show where time goes.

## breakpoint()

```python
def compute(x):
    y = x * 2
    breakpoint()   # pdb starts here
    return y + 1
```

pdb commands: n (next), s (step into), p name (print), c (continue), q (quit).

## cProfile

```bash
python -m cProfile -s cumulative script.py
```

Shows time per function.

## Profiling snippet

```python
import cProfile

def work():
    return sum(i * i for i in range(1_000_000))

cProfile.run("work()")
```

## Lesson summary

breakpoint() opens pdb; cProfile finds hot spots.

<!--TASK-->
### Task 1 — breakpoint
Insert breakpoint() and list pdb commands.

### Task 2 — p name
Explain what p x does.

### Task 3 — cProfile run
Profile a function with cProfile.run.

### Task 4 — CLI
Run python -m cProfile -s cumulative.

### Task 5 — Compare
Profile two functions and compare.

### Task 6 — Traceback
Read a traceback and point to the error line.

### Task 7 — Line profiling idea
Mention line_profiler.
<!--/TASK-->

<!--HINT-->
### Hint 1
breakpoint().

### Hint 2
p x prints x.

### Hint 3
cProfile.run("fn()").

### Hint 4
Command line.

### Hint 5
Two runs.

### Hint 6
Last line.

### Hint 7
line_profiler.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
def compute(x):
    y = x * 2
    breakpoint()
    return y + 1
# pdb: n, s, p y, c, q
```

### Solution 2
```python
# p y — печатает текущее значение переменной y
```

### Solution 3
```python
import cProfile

def work():
    return sum(i * i for i in range(1_000_000))

cProfile.run("work()")
```

### Solution 4
```bash
python -m cProfile -s cumulative script.py
```

### Solution 5
```python
import cProfile

def fast():
    return sum(range(1_000_000))

def slow():
    total = 0
    for i in range(1_000_000):
        total += i
    return total

cProfile.run("fast()")
cProfile.run("slow()")
```

### Solution 6
```python
# Traceback: последняя строка — место ошибки
# Читай тип (TypeError, ValueError) и сообщение
```

### Solution 7
```python
# line_profiler показывает время по строкам:
# pip install line_profiler
```
<!--/SOLUTION-->

<!--QUIZ-->
What does breakpoint() do?
- Starts pdb
- Ends program
- Prints
- None
* Correct answer: Starts pdb
Debugger.

What is n in pdb?
- Next line
- Now
- Name
- None
* Correct answer: Next line
Step over.

What is s?
- Step into
- Stop
- Skip
- None
* Correct answer: Step into
Function.

What is p?
- Print variable
- Pause
- Path
- None
* Correct answer: Print variable
value.

What is c?
- Continue
- Close
- Clear
- None
* Correct answer: Continue
Run to end.

What is q?
- Quit
- Query
- Quick
- None
* Correct answer: Quit
Exit.

What is cProfile?
- Profiler
- Debugger
- Linter
- None
* Correct answer: Profiler
Timing.

What is -s cumulative?
- Sort by total time
- Sort size
- Skip
- None
* Correct answer: Sort by total time
Order.

What is tottime?
- Own time
- Cumulative
- Total
- None
* Correct answer: Own time
Excluding calls.

What is cumtime?
- Inclusive time
- Own
- Start
- None
* Correct answer: Inclusive time
With calls.

What are hot spots?
- Slow functions
- Errors
- Lines
- None
* Correct answer: Slow functions
Optimize.

What is line_profiler?
- Per-line profiling
- A debugger
- A linter
- None
* Correct answer: Per-line profiling
Details.
<!--/QUIZ-->
