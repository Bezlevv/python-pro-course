---
title: Exam: Python for DevOps
summary: Final knowledge check on automation, configs, log parsing, schedulers, SSH, and monitoring.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, devops, final
---

<!--QUIZ-->
Which standard-library module parses command-line arguments?
- argparse
- getopt
- click
* Correct answer: argparse
argparse is part of the standard library and lets you describe arguments flexibly.

What will subprocess.run(["echo", "hi"], capture_output=True, text=True).stdout return?
- "hi\n"
- "hi"
- b"hi\n"
* Correct answer: "hi\n"
text=True returns a string, and capture_output=True captures the output; the newline is preserved.

Which config format does tomllib read?
- TOML
- JSON
- YAML
* Correct answer: TOML
tomllib appeared in Python 3.11 for reading TOML files.

Why is it better to use yaml.safe_load instead of yaml.load?
- Because safe_load does not create arbitrary objects when parsing
- Because safe_load is faster
- Because load is deprecated and removed
* Correct answer: Because safe_load does not create arbitrary objects when parsing
safe_load protects against executing dangerous objects from untrusted files.

What will re.findall(r"\d+", "2026 year, 3 tasks") return?
- ['2026', '3']
- '20263'
- ['2026', '0', '3']
* Correct answer: ['2026', '3']
findall returns a list of all matches of the pattern.

How to get a command's exit code in paramiko?
- stdout.channel.recv_exit_status()
- client.returncode
- stderr.read()
* Correct answer: stdout.channel.recv_exit_status()
recv_exit_status() waits for completion and returns the command's exit code.

What does the entry 0 3 * * * mean in crontab?
- Runs at 03:00 every day
- Runs every 3 minutes
- Runs at 00:03 every hour
* Correct answer: Runs at 03:00 every day
Fields: minute 0, hour 3, day of month *, month *, day of week *.

How do schedule and cron differ?
- schedule lives inside a Python process, cron is a system scheduler
- schedule works only on Windows, cron only on Linux
- They are the same thing
* Correct answer: schedule lives inside a Python process, cron is a system scheduler
cron survives system reboots; schedule disappears together with the process.

What does schedule.run_pending() do?
- Runs tasks whose time has come
- Stops all tasks
- Sleeps for one second
* Correct answer: Runs tasks whose time has come
run_pending() must be called in a loop for tasks to execute.

Which exit code should a CI script return when a check fails?
- 1
- 0
- 2
* Correct answer: 1
A non-zero code means failure: CI stops the pipeline and flags the build red.

What does Path("data").rglob("*.log") do?
- Recursively finds .log files in all subfolders of data
- Finds .log files only in the data folder itself
- Creates .log files
* Correct answer: Recursively finds .log files in all subfolders of data
rglob walks the entire directory tree; glob only the current level.

How to read a JSON file in Python?
- json.load(f)
- json.dump(f)
- json.read(f)
* Correct answer: json.load(f)
json.load reads JSON from a file object and returns a dict.
<!--/QUIZ-->
