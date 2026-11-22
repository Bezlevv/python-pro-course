---
title: Exam: Concurrency
summary: Test your knowledge of threads, the GIL, multiprocessing, pools, queues, and asyncio.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What is the GIL?
- A library for creating threads
- A global lock of the CPython interpreter: at any moment only one thread executes bytecode
- An import caching mechanism
- A multithreading debugging mode
* Correct answer: A global lock of the CPython interpreter: at any moment only one thread executes bytecode
The GIL protects the interpreter's internal structures, but because of it true thread parallelism is impossible.

Why don't threads speed up CPU-bound tasks?
- Threads are banned on most platforms
- Because of the GIL only one thread runs at a time, so total time barely changes
- Threads only speed up I/O
- Threads have no access to the CPU
* Correct answer: Because of the GIL only one thread runs at a time, so total time barely changes
Threads just switch quickly, and switching overhead even adds time.

Which tool should you choose to really use several CPU cores?
- threading.Thread
- multiprocessing.Process
- asyncio.create_task
- queue.Queue
* Correct answer: multiprocessing.Process
Each process is a separate interpreter with its own GIL, so processes run on different cores in parallel.

Why can't processes just use shared global variables?
- Variables don't exist in processes
- Each process has its own memory, and changes in one process aren't visible to others
- Global variables are only available in the main process
- Processes only see copies of global variables
* Correct answer: Each process has its own memory, and changes in one process aren't visible to others
Special tools are needed for exchanging data: Value, Array, or Queue.

Why is the if __name__ == "__main__": construct needed in scripts with multiprocessing?
- To start the program faster
- So that when the interpreter restarts (spawn on Windows), the process-creation code doesn't run again in each child process
- It's a syntactic requirement of all Python programs
- To avoid stack overflow
* Correct answer: So that when the interpreter restarts (spawn on Windows), the process-creation code doesn't run again in each child process
Without this protection a child process would create new processes recursively.

What does the t.join() method do?
- Starts thread t
- Stops thread t forever
- Blocks the calling thread until thread t finishes
- Removes thread t from memory
* Correct answer: Blocks the calling thread until thread t finishes
join() lets you wait for a thread to finish, for example before printing the final result.

Why is ThreadPoolExecutor needed?
- To limit the number of concurrently running threads and reuse them for many tasks
- To create processes instead of threads
- To disable the GIL
- To turn sequential code into asynchronous code
* Correct answer: To limit the number of concurrently running threads and reuse them for many tasks
Pools (executor.submit and executor.map) handle thread creation and management: tasks are queued and run by free workers.

How do you protect a shared variable from a data race?
- Declare it as global
- Wrap the change in with lock: using a threading.Lock object
- Use print() for output
- Increase the number of threads
* Correct answer: Wrap the change in with lock: using a threading.Lock object
A mutex makes the critical section mutually exclusive, and the context manager guarantees the lock is released even on an exception.

How is a coroutine declared in asyncio?
- def coro(): ...
- async def coro(): ... with await inside
- with coro(): ...
- await def coro(): ...
* Correct answer: async def coro(): ... with await inside
A coroutine is declared with async def, and await is used at waiting points, where it yields control to the event loop.

What does asyncio.gather do?
- Runs coroutines sequentially
- Runs several coroutines in parallel and returns results in the order they were passed
- Limits coroutine execution time
- Stops the event loop
* Correct answer: Runs several coroutines in parallel and returns results in the order they were passed
If order doesn't matter, use asyncio.as_completed, which yields results as they become ready.

What happens when the timeout set by asyncio.wait_for is exceeded?
- The task keeps running in the background
- An asyncio.TimeoutError exception is raised, and the task is cancelled
- The program hangs forever
- The result becomes None
* Correct answer: An asyncio.TimeoutError exception is raised, and the task is cancelled
A timeout stops you from waiting on a slow service forever: the wait is interrupted, and the task receives a cancellation request.
<!--/QUIZ-->
