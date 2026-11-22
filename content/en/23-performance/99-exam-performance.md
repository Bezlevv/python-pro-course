---
title: Exam: Python Performance
summary: Test your knowledge of profiling, optimization, Cython/Numba, free-threading, async performance, and scaling.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which tool is suitable for finding function-level bottlenecks?
- timeit
- cProfile
- asyncio
- queue
* Correct answer: cProfile
cProfile shows the time and call count of every function, including nested ones.

What does the cumtime column in cProfile output show?
- Time inside the function itself, excluding nested calls
- Total time including nested calls
- The number of function calls
- The function's memory size
* Correct answer: Total time including nested calls
cumtime = tottime + child-call time; sort_stats("cumulative") sorts by it.

What does tracemalloc do?
- Measures function speed
- Tracks memory allocations and shows where they happen
- Compiles code to C
- Manages threads
* Correct answer: Tracks memory allocations and shows where they happen
tracemalloc snapshots help find leaks and large per-line allocations.

Why is checking item in set faster than item in list?
- set stores elements in a hash table: lookup is O(1) on average; a list scans elements — O(n)
- set weighs less
- list is forbidden for large data
- There's no difference
* Correct answer: set stores elements in a hash table: lookup is O(1) on average; a list scans elements — O(n)
A hash table gives constant-time lookup; a list requires a linear pass.

What does @njit from Numba do?
- Runs the function in a separate process
- Compiles the function to machine code on the first call (JIT)
- Rewrites the function in Cython
- Adds caching
* Correct answer: Compiles the function to machine code on the first call (JIT)
The first call is the "warmup" (compilation), then the code runs as machine code.

What is Cython?
- A profiling library
- A superset language of Python, compiled into a C extension
- An alternative interpreter
- A package manager
* Correct answer: A superset language of Python, compiled into a C extension
.pyx files are built via cythonize into importable modules.

What does free-threading (PEP 703) do?
- Removes the GIL: threads can run on multiple cores simultaneously
- Always speeds up single-threaded code
- Forbids threads
- Replaces processors
* Correct answer: Removes the GIL: threads can run on multiple cores simultaneously
A GIL-free build, at the price of overhead and demands on C extensions.

Why can counter += 1 in several threads give a wrong result?
- The operation isn't atomic: reads and writes can interleave across threads
- Numbers don't add in threads
- Threads don't see variables
- The result is always larger than expected
* Correct answer: The operation isn't atomic: reads and writes can interleave across threads
A data race: two threads can read the same value and write the same result; protection — threading.Lock.

What happens if you call time.sleep(1) inside a coroutine?
- The event loop is fully blocked for 1 second
- The task moves to a separate thread
- Nothing
- Sleep automatically becomes await
* Correct answer: The event loop is fully blocked for 1 second
Blocking calls are forbidden in coroutines; for them there are asyncio.to_thread and run_in_executor.

What does the p95 percentile show?
- The time within which 95% of requests finished
- Average response time
- Maximum time
- Requests per second
* Correct answer: The time within which 95% of requests finished
p95 is the standard latency goal: the "tail" of slow requests becomes visible.
<!--/QUIZ-->
