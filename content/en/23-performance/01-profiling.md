---
title: Profiling: cProfile, line_profiler
summary: Find bottlenecks first.
order: 1
duration: 45 min
difficulty: advanced
tags: profiling, cprofile
---

Profile before optimizing.

## cProfile

```bash
python -m cProfile -s cumtime script.py
```

## In code

```python
import cProfile
cProfile.run("my_function()", sort="cumtime")
```

## line_profiler

```bash
pip install line_profiler
kernprof -l -v script.py
```

## Lesson summary

Measure, find hot spots, then optimize.

<!--TASK-->
### Task 1 — cProfile
Profile a script via CLI.

### Task 2 — Sort
Sort by cumulative time.

### Task 3 — In code
Profile a function.

### Task 4 — line_profiler
Install and run.

### Task 5 — Analyze
Find the slowest function.

### Task 6 — Optimize
Improve it.

### Task 7 — Verify
Re-profile and compare.
<!--/TASK-->

<!--HINT-->
### Hint 1
-m cProfile.

### Hint 2
-s cumtime.

### Hint 3
run().

### Hint 4
kernprof.

### Hint 5
Cumtime.

### Hint 6
Fix.

### Hint 7
Compare.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
python -m cProfile -s cumtime script.py
```

### Solution 2
```bash
python -m cProfile -s cumtime script.py > prof.txt
```

### Solution 3
```python
import cProfile
cProfile.run("my_function()", sort="cumtime")
```

### Solution 4
```bash
pip install line_profiler
kernprof -l -v script.py
# в коде: @profile над функцией
```

### Solution 5
```text
Читать столбец cumtime: где суммарное время
наибольшее — там узкое место
```

### Solution 6
```text
Например: заменить повторный вызов sorted()
в цикле на один вызов до цикла
```

### Solution 7
```text
Запустить профиль ещё раз и сравнить
время до/после
```
<!--/SOLUTION-->

<!--QUIZ-->
What is profiling?
- Measuring time
- Testing
- Debugging
- None
* Correct answer: Measuring time
Hot spots.

What is cProfile?
- Built-in profiler
- Line profiler
- Debugger
- None
* Correct answer: Built-in profiler
Module.

What is cumtime?
- Cumulative time
- Per call
- Total
- None
* Correct answer: Cumulative time
Including calls.

What is ncalls?
- Call count
- Time
- Memory
- None
* Correct answer: Call count
Calls.

What is tottime?
- Own time
- With calls
- Total
- None
* Correct answer: Own time
Exclusive.

What is kernprof?
- Line profiler
- cProfile
- pytest
- None
* Correct answer: Line profiler
Tool.

What is @profile?
- Marks function
- Decorates test
- Skips
- None
* Correct answer: Marks function
Line.

What is a bottleneck?
- Slowest part
- Fastest
- Bug
- None
* Correct answer: Slowest part
Limit.

What is sort?
- Ordering
- Timing
- Memory
- None
* Correct answer: Ordering
cumtime.

What is a hot spot?
- Heavy code
- Light
- New
- None
* Correct answer: Heavy code
Optimize.

Why profile first?
- Evidence
- Guess
- Speed
- None
* Correct answer: Evidence
No guessing.

What is the result?
- Numbers
- Code
- Tests
- None
* Correct answer: Numbers
Compare.
<!--/QUIZ-->
