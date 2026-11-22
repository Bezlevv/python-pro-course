---
title: Exam: Testing in Depth
summary: Test your knowledge of testing: pytest, fixtures, parametrization, mocking, TDD, coverage, property-based, and async tests.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
What does the scope="module" parameter of a pytest fixture do?
- Creates the fixture anew for every test
- Creates the fixture once for the whole file
- Forbids using the fixture
* Correct answer: Creates the fixture once for the whole file
With scope="module" the fixture is created once and reused by all tests in the file.

What will a MagicMock call return if you set mock.get.side_effect = [1, 2]?
- Always 1
- 1 on the first call and 2 on the second
- A random number
* Correct answer: 1 on the first call and 2 on the second
side_effect with a list hands out values one per call.

Which string should you patch if module app wrote import requests and calls requests.get?
- app.requests.get
- requests.get
- app.get
* Correct answer: app.requests.get
You patch the place of use — the name requests.get in module app's namespace.

What is the order of TDD phases?
- Implementation → tests → refactoring
- Test (red) → implementation (green) → refactoring
- Refactoring → test → implementation
* Correct answer: Test (red) → implementation (green) → refactoring
First a failing test, then a minimal implementation, then code improvement.

What does the --cov-fail-under=80 flag do?
- Ends the run with an error if coverage is below 80%
- Limits coverage to 80 lines
- Shows only the first 80% of the report
* Correct answer: Ends the run with an error if coverage is below 80%
This is a quality threshold: below 80% coverage, pytest exits with an error.

How do you exclude an entry point from the coverage count?
- Put # pragma: no cover at the end of the lines
- Rename the file
- Run pytest with the --no-main flag
* Correct answer: Put # pragma: no cover at the end of the lines
The comment excludes the line from coverage evaluation.

What does assume(b != 0) do in a property test?
- Raises an exception when b == 0
- Discards examples with zero b
- Rounds b
* Correct answer: Discards examples with zero b
assume filters inputs for which the property is undefined.

What happens if a property is violated?
- Hypothesis finds a counterexample and shrinks it to the minimum
- The test is skipped
- Hypothesis stops generating data
* Correct answer: Hypothesis finds a counterexample and shrinks it to the minimum
Automatic shrinking (shrinking) is a key hypothesis feature.

Which marker is needed for a coroutine test?
- @pytest.mark.asyncio
- @pytest.mark.async
- @pytest.mark.await
* Correct answer: @pytest.mark.asyncio
The marker tells pytest-asyncio to run the test in an event loop.

Why is AsyncMock needed for async dependencies?
- Because MagicMock doesn't return an awaitable, and await will fail
- Because AsyncMock is faster
- Because MagicMock cannot be imported
* Correct answer: Because MagicMock doesn't return an awaitable, and await will fail
AsyncMock returns an awaitable, so await client.get(url) works.
<!--/QUIZ-->
