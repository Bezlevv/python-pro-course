---
title: Exam: Popular Libraries
summary: Test your knowledge of Pillow, requests, rich, typer, openpyxl/python-docx and tqdm/concurrent.futures.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What does img.thumbnail((100, 100)) return?
- A new Image object
- None — the image is modified in place
- Tuple (100, 100)
- An error
* Correct answer: None — the image is modified in place
thumbnail() modifies the object and returns None; proportions are preserved.

Why convert RGBA to RGB before saving as JPEG?
- JPEG doesn't support an alpha channel
- It speeds up saving
- Without it the file won't open
- This is only required for WebP
* Correct answer: JPEG doesn't support an alpha channel
JPEG doesn't store transparency, so the extra channel is removed.

What does HTTPAdapter(max_retries=Retry(...)) do in requests?
- Enables automatic retries and a connection pool
- Speeds up DNS queries
- Encrypts traffic
- Switches the protocol to HTTP/2
* Correct answer: Enables automatic retries and a connection pool
HTTPAdapter is responsible for the connection pool and applies the retry policy.

What does r.raise_for_status() do?
- Returns the status code
- Raises HTTPError on 4xx/5xx
- Ignores errors
- Sets a timeout
* Correct answer: Raises HTTPError on 4xx/5xx
raise_for_status() turns HTTP errors into exceptions.

Why does rich disable ANSI codes when outputting to StringIO?
- Because colors are only supported in terminals
- To speed up output
- It's a random bug
- For Windows XP compatibility
* Correct answer: Because colors are only supported in terminals
Rich writes clean text without control codes to non-terminals.

How to build a table in rich?
- Create a Table, add columns and rows, pass it to console.print()
- Call console.table_data()
- Use the Grid class
- Write Markdown
* Correct answer: Create a Table, add columns and rows, pass it to console.print()
Table collects data, console.print renders it.

How to declare a command in typer?
- @app.command() over a function
- app.add_command()
- typer.run_command()
- class Command(app)
* Correct answer: @app.command() over a function
The decorator registers the function as a CLI command.

How are typer commands tested?
- CliRunner from typer.testing
- requests
- unittest.mock.patch
- Only by launching a separate process
* Correct answer: CliRunner from typer.testing
runner.invoke(app, args) runs the command in-process and returns a Result.

How to write a formula into an openpyxl cell?
- ws["B8"] = "=SUM(B2:B7)"
- ws["B8"] = SUM(B2:B7)
- ws.formula(B8, "SUM")
- Impossible
* Correct answer: ws["B8"] = "=SUM(B2:B7)"
The formula is stored as a string; Excel computes the value.

When does ThreadPoolExecutor speed up execution?
- On IO tasks (network, files)
- Only on simple computations
- Never
- Always, even on CPU tasks
* Correct answer: On IO tasks (network, files)
Threads are efficient when a task waits for I/O.
<!--/QUIZ-->
