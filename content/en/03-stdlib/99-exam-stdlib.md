---
title: Exam: Standard Library and Tools
summary: Test your knowledge of the standard library and tools: collections, itertools, pathlib, logging, pytest, Git and argparse.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which class from collections is convenient for counting items?
- Counter
- ChainMap
- OrderedDict
- namedtuple
* Correct answer: Counter
Counter counts the frequency of items: Counter("abracadabra") will show how many times each letter appears.

What does itertools.product([1, 2], ["a", "b"]) return?
- 2 elements
- 4 elements
- 8 elements
- Error
* Correct answer: 4 elements
product creates a Cartesian product: pairs (1, "a"), (1, "b"), (2, "a"), (2, "b").

What is Path("docs/report.txt").suffix equal to?
- "report"
- ".txt"
- "docs"
- "txt"
* Correct answer: ".txt"
The suffix attribute returns the file extension together with the dot.

Which method writes a message to the log?
- print("...")
- logging.info("...")
- log("...")
- journal.write("...")
* Correct answer: logging.info("...")
logging.info() sends an INFO-level message to the configured log handler.

How does pytest find tests?
- By file names starting with pytest_
- By function names like test_*
- By the @test annotation
- Only if they're explicitly listed
* Correct answer: By function names like test_*
pytest automatically collects functions whose names start with test_.

What happens when assert 2 + 2 == 5 fails in a test?
- The test passes
- The test fails with an error
- The program stops
- Nothing
* Correct answer: The test fails with an error
A false assert statement raises an AssertionError, and the test is marked as failed.

Which sequence of commands commits changes in Git?
- git commit && git push
- git add . && git commit -m "сообщение"
- git push origin main
- git diff && git status
* Correct answer: git add . && git commit -m "сообщение"
First changes are added to the index with git add, then committed with git commit.

Which command shows the current state of the repository?
- git log
- git status
- git show
- git branch
* Correct answer: git status
git status shows modified files, new files and other uncommitted changes.

Which class from argparse parses command-line arguments?
- argparse.Parser
- argparse.ArgumentParser
- argparse.Args
- argparse.Parse
* Correct answer: argparse.ArgumentParser
ArgumentParser() creates a parser to which arguments are added via add_argument().

What happens when you access a missing key of defaultdict(list)?
- KeyError
- An empty list is created for that key
- None is returned
- The key is ignored
* Correct answer: An empty list is created for that key
defaultdict automatically creates a default value (here, an empty list) on the first access to a missing key.
<!--/QUIZ-->
