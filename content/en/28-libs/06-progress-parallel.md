---
title: tqdm and parallel processing with progress
summary: tqdm progress bars and concurrent.futures pools: parallelize IO tasks, show progress and cover with tests.
order: 6
duration: 35 min
difficulty: intermediate
tags: tqdm, concurrent.futures, parallelism, progress, pytest
---

Long scripts without feedback make you guess: "is it still working or hung?". `tqdm` solves this with beautiful progress bars, and `concurrent.futures` lets you run tasks in parallel. Together they give fast, visible utilities.

## Installation

```bash
pip install tqdm
```

## tqdm: simple progress

```python
from tqdm import tqdm
from time import sleep

for i in tqdm(range(100), desc="Processing", unit="step"):
    sleep(0.02)
```

A bar with percentages, speed and remaining time appears in the terminal. The `desc` parameter is a label on the left, `unit` — the unit name ("step", "file"). The context manager also works:

```python
with tqdm(total=100, desc="Downloading") as pbar:
    for _ in range(100):
        sleep(0.01)
        pbar.update(1)
```

`update(1)` increments the counter manually — handy when iterations aren't equal.

## Parallelism: ThreadPoolExecutor

`concurrent.futures` is the standard module for pools. `ThreadPoolExecutor` is for IO tasks (network, files): threads spend time waiting for I/O, not burning CPU.

```python
from concurrent.futures import ThreadPoolExecutor

def double(x):
    return x * 2

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(double, range(10)))
print(results)  # [0, 2, 4, ..., 18]
```

`pool.map(func, iterable)` applies the function to each element and returns results in the same order as the input. For CPU-bound tasks that really load the processor, use `ProcessPoolExecutor` — it bypasses the GIL using separate processes.

## Results as they arrive: as_completed

`map` is good when order matters. If order doesn't matter and you want to process results as they appear, use `submit` + `as_completed`:

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(double, x) for x in range(10)]
    for future in as_completed(futures):
        print(future.result())
```

## Combining: progress + parallelism

The most common utility pattern is parallel work with a progress bar:

```python
with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(double, x) for x in range(20)]
    for future in tqdm(as_completed(futures), total=20, desc="Counting"):
        future.result()
```

`tqdm` wraps `as_completed`, and `total=20` tells the total number of tasks (otherwise the bar doesn't know the length). This way you can show how many tasks have completed.

## Testing parallel code

Parallelism shouldn't interfere with tests: functions that do the work should stay pure and deterministic. We'll test both `parallel_map` and a file hashing function — without network and without real delays.

<!--TASK-->
### Task 1
Write a function `count_down(n)` that uses `tqdm(range(n), desc="Processing", unit="step")` and does `sleep(0.05)` inside the loop. After the loop print `Done!`. Check manually: run `count_down(20)` — a progress bar and the message should appear. Expected result: the function works, shows progress and prints `Done!`.

### Task 2
Write a function `parallel_map(func, items, max_workers=4)` that uses `ThreadPoolExecutor` and returns a list of results in input order (via `list(pool.map(func, items))`). Check manually: `parallel_map(lambda x: x * x, [1, 2, 3])` returns `[1, 4, 9]`. Expected result: the order and values of results match a sequential call.

### Task 3
Write functions `sha256_of_file(path)` and `hash_files(paths, max_workers=4)`. The first reads the file as bytes (`path.read_bytes()`) and returns `hashlib.sha256(...).hexdigest()`. The second creates a `ThreadPoolExecutor`, submits all paths via `pool.submit(sha256_of_file, p)`, wraps `as_completed` in `tqdm` with `total=len(paths)` and `desc="Hashing"`, and collects a dict `{path: hash}`. Check manually on a couple of files. Expected result: the dict contains a hash for each file matching direct computation.

### Task 4
Write pytest tests for `parallel_map`: (1) `parallel_map(lambda x: x * 2, [1, 2, 3, 4])` returns `[2, 4, 6, 8]`; (2) result order matches input order; (3) an empty list returns `[]`; (4) on an exception in the function (e.g., `lambda x: 1 // 0`) `pytest.raises(ZeroDivisionError)` fires when accessing the result. Run `python -m pytest test_parallel.py -v`. Expected result: all 4 tests pass.

### Task 5
Write pytest tests for `hash_files`: in `tmp_path` create three files with known content (`b"abc"`, `b"def"`, `b"123"`). Check: (1) the result is a dict where keys are paths and values match `hashlib.sha256(content).hexdigest()`; (2) `len(result) == 3`; (3) for a nonexistent path `pytest.raises(FileNotFoundError)` when calling `hash_files([missing])`. Run the tests. Expected result: all checks pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
`for i in tqdm(range(n), desc="Processing", unit="step"):` — inside `sleep(0.05)`. `print("Done!")` after the loop.

### Hint 2
Use `with ThreadPoolExecutor(max_workers=max_workers) as pool:`; inside `return list(pool.map(func, items))`. Import: `from concurrent.futures import ThreadPoolExecutor`.

### Hint 3
Hash: `hashlib.sha256(path.read_bytes()).hexdigest()`. In `hash_files` create `futures = [pool.submit(sha256_of_file, p) for p in paths]`, then the loop `for future in tqdm(as_completed(futures), total=len(paths), desc="Hashing")` collecting the dict. Imports: `hashlib`, `as_completed`, `tqdm`, `ThreadPoolExecutor`.

### Hint 4
An exception from `map` surfaces during iteration: `with pytest.raises(ZeroDivisionError): list(parallel_map(lambda x: 1 // 0, [1]))`. Check order on a list of 4–5 elements with different values.

### Hint 5
Create files: `Path(tmp_path / "a.txt").write_bytes(b"abc")`. Expected hash: `hashlib.sha256(b"abc").hexdigest()`. For the missing path don't create a file and pass a path that doesn't exist.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Full solution:

```python
from time import sleep
from tqdm import tqdm

def count_down(n):
    for i in tqdm(range(n), desc="Processing", unit="step"):
        sleep(0.05)
    print("Done!")
```

Walkthrough. `tqdm(range(n), ...)` wraps an iterable: on each iteration the bar advances automatically. `desc` adds a label on the left, `unit` — a unit name after the counter (e.g., `20.0 step/s`). `sleep(0.05)` imitates useful work — in real code there'd be a request, computation or file processing. After the loop, `Done!` is printed. Such a bar is a cheap way to make any long script comprehensible.

### Walkthrough 2
Full solution:

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_map(func, items, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        return list(pool.map(func, items))
```

Walkthrough. `ThreadPoolExecutor(max_workers=4)` creates a pool of four threads. `pool.map(func, items)` runs `func` for each element in parallel but returns results in input order — this is the key difference from `as_completed`, where order is arbitrary. The `with` context manager guarantees threads finish and resources are released. The `list(...)` wrapper materializes the iterator — without it, worker exceptions would surface only during iteration. This function is a universal tool for applying any "pure" function in parallel.

### Walkthrough 3
Full solution:

```python
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def sha256_of_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hash_files(paths, max_workers=4):
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(sha256_of_file, p) for p in paths]
        for future in tqdm(as_completed(futures), total=len(paths),
                           desc="Hashing"):
            path = paths[futures.index(future)]
            results[path] = future.result()
    return results
```

Walkthrough. `sha256_of_file` is a pure function: it reads the whole file (`read_bytes`) and returns a hex hash. `hash_files` submits paths to the pool via `submit` — each call becomes a `Future` object. `as_completed(futures)` yields finished futures as they're ready, and `tqdm(...)` around it shows progress; `total=len(paths)` sets the bar length because `as_completed` doesn't know it itself. To find the path of a finished future we look up its index in the `futures` list. The results dict is collected as they arrive — for a large number of files this is noticeably faster than sequential iteration.

### Walkthrough 4
Full solution:

```python
import pytest
from parallel_utils import parallel_map

def test_parallel_map_values():
    assert parallel_map(lambda x: x * 2, [1, 2, 3, 4]) == [2, 4, 6, 8]

def test_parallel_map_preserves_order():
    items = list(range(10))
    assert parallel_map(lambda x: x + 100, items) == [x + 100 for x in items]

def test_parallel_map_empty():
    assert parallel_map(lambda x: x, []) == []

def test_parallel_map_raises():
    with pytest.raises(ZeroDivisionError):
        list(parallel_map(lambda x: 1 // 0, [1]))
```

Walkthrough. The first two tests verify values and order: `map` guarantees index correspondence, and this behavior is worth pinning with a test — switching to `as_completed` would break it. The third test covers empty input. The fourth — behavior on exception: a worker error surfaces during iteration over results, so we materialize `list(...)` inside `pytest.raises`. The tests use only pure lambdas, without network or delays, so they're instant and deterministic.

### Walkthrough 5
Full solution:

```python
import hashlib
import pytest
from pathlib import Path
from parallel_utils import hash_files

def test_hash_files_correct(tmp_path):
    data = {"a.txt": b"abc", "b.txt": b"def", "c.txt": b"123"}
    paths = []
    for name, content in data.items():
        p = tmp_path / name
        p.write_bytes(content)
        paths.append(p)

    result = hash_files(paths)

    assert len(result) == 3
    for p, content in zip(paths, data.values()):
        assert result[p] == hashlib.sha256(content).hexdigest()

def test_hash_files_missing_raises(tmp_path):
    missing = tmp_path / "nope.txt"
    with pytest.raises(FileNotFoundError):
        hash_files([missing])
```

Walkthrough. The first test creates three files with known content and compares `hash_files` output with the reference `hashlib.sha256(...)` computation. The dict is checked by path keys: `result[p]` is the hash of exactly that file. The second test covers the edge case: `read_bytes()` on a nonexistent path throws `FileNotFoundError`, and the exception surfaces when accessing `future.result()`, so `pytest.raises` wraps the whole call. Such tests guarantee parallel logic didn't swap content and handles errors correctly.
<!--/SOLUTION-->

<!--QUIZ-->
What does tqdm(range(100)) do?
- Shows a progress bar over iterations
- Speeds up the loop
- Turns range into a list
- Prints numbers
* Correct answer: Shows a progress bar over iterations
The parameter wraps an iterable and displays progress.

What does the desc parameter mean?
- The number of iterations
- A label to the left of the bar
- A unit of measure
- Execution speed
* Correct answer: A label to the left of the bar
desc sets the text describing the work being done.

How to manually increment the bar counter?
- pbar.update(1)
- pbar.inc()
- pbar.next(1)
- pbar += 1
* Correct answer: pbar.update(1)
update(n) increases the current value by n.

When does ThreadPoolExecutor speed up work?
- On IO tasks (network, files)
- On CPU tasks under all circumstances
- Only in a single thread
- Never
* Correct answer: On IO tasks (network, files)
Threads wait for I/O, and parallel waits reduce total time.

Which pool to use for heavy computations?
- ProcessPoolExecutor
- ThreadPoolExecutor
- MultipoolExecutor
- Only a for loop
* Correct answer: ProcessPoolExecutor
Separate processes bypass the GIL and use multiple cores.

What does pool.map(func, items) return?
- A list of results in input order
- A set of future objects
- An iterator in arbitrary order
- Nothing
* Correct answer: A list of results in input order
map preserves index correspondence.

What does as_completed(futures) do?
- Returns finished futures as they become ready
- Executes all tasks
- Stops the pool
- Sorts results
* Correct answer: Returns finished futures as they become ready
as_completed yields results as soon as they're ready.

How to show progress for as_completed?
- tqdm(as_completed(futures), total=len(futures))
- tqdm(futures)
- Progress is impossible for it
- as_completed(tqdm(futures))
* Correct answer: tqdm(as_completed(futures), total=len(futures))
The bar needs total because as_completed doesn't know the length.

What happens on an exception in a ThreadPoolExecutor worker?
- The error surfaces when accessing the result
- The exception is silently ignored
- The pool stops forever
- The program exits with code 0
* Correct answer: The error surfaces when accessing the result
future.result() or iterating over map re-raises the exception.

What does hash_files(paths) from the lesson do?
- Hashes files in parallel and returns a dict of paths and hashes
- Deletes files
- Sorts files by size
- Copies files
* Correct answer: Hashes files in parallel and returns a dict of paths and hashes
Each path is mapped to the SHA-256 hash of its content.
<!--/QUIZ-->
