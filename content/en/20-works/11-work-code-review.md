---
title: Independent Work: Code Review of Someone Else's Code
summary: Conduct a professional code review of someone else's program: find bugs, style and security issues, write a stage-by-stage report, and propose fixes.
order: 11
duration: 120 min
difficulty: intermediate
tags: code review, report, code quality, debugging
---

This lesson has no regular material presentation — this is an independent work assignment. You can already read someone else's code, run programs, and use exceptions. Now you'll try yourself as a reviewer: you'll get a "foreign" program, find its weak spots, and produce a professional report. This is a skill from real work: every pull request goes through review, and the ability to point out problems politely and precisely is valued no less than the ability to fix them.

## Problem statement

You are given the code of the program "Bank Account" in the file `account.py`. It can open an account, deposit money, withdraw it, and print a statement. The program runs, but defects are hidden in it: bugs, sloppy style, reliability and security issues. Your task is to conduct a full code review: find and reproduce the problems, classify them, write a report, and propose fixes.

```python
# account.py
import datetime

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance = self.balance + amount
        self.transactions.append((datetime.datetime.now(), "deposit", amount))

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance = self.balance - amount
            self.transactions.append((datetime.datetime.now(), "withdraw", amount))
        else:
            print("Недостаточно средств")

    def show(self):
        print("Владелец:", self.owner)
        print("Баланс:", self.balance)
        for t in self.transactions:
            print(t)

acc = BankAccount("Аня", 100)
acc.deposit(50)
acc.withdraw(30)
acc.show()
```

What's wrong with this code? Run it, experiment, try to "break" it. You will find at least: depositing a negative amount, withdrawing a negative amount, withdrawing the entire amount, lost money with fractional amounts (due to float), unhandled exceptions, PEP 8 style violations, and a lack of data protection.

## Requirements

- The report is written in the file `review.md` in Markdown.
- Each note is a separate entry: item number, severity (`критично` / `важно` / `незначительно`), the line or function where the problem is, a description, reproduction (what to do to see it), and a fix recommendation.
- All problems must be **reproduced**: you must run the program and make sure the bug actually manifests.
- At the end of the report — a verdict and a proposed corrected code (in `account_fixed.py`).
- You must not change the original `account.py`: it is needed for comparison.

## How to work on the assignment

Complete the stages in order. Each stage produces a finished part of the report that can be checked. Don't move to the next stage until the previous one is ready: review is a systematic process, not a list of random guesses.

## Assessment criteria (10 points)

| Criterion | Points |
|---|---|
| At least 8 problems found and reproduced | 3 |
| Each note contains severity, line, description, and reproduction | 3 |
| The report is structured, readable, and has a verdict | 2 |
| A corrected working code is proposed | 2 |

Passing grade — from 7 points.

## What to submit

- The file `review.md` — the full report on all five stages.
- The file `account_fixed.py` — the corrected version of the program.
- The lesson quiz on the platform (8 questions).

<!--TASK-->
### Task 1
Run `account.py` several times. Do a "survey": what the program does, what functions it has, what data it stores. Write an "Overview" section in `review.md`: the program's purpose, 3–5 lines on how it's organized, and observations about the code (structure, function length, readability). Then run simple scenarios: deposit 50, withdraw 30, print the statement. Make sure the basic logic works.

### Task 2
Find input bugs. Try depositing `-50`, withdrawing `-30`, withdrawing `0`, withdrawing more than the balance, withdrawing exactly the whole amount. For each case, record: what you did, what the program printed, and what would be correct. Separately check withdrawing the whole amount — after it, the account should have `0` left, but check whether the condition `self.balance >= amount` really allows it. Put the found problems into the report with severity and recommendations.

### Task 3
Check money accuracy. Deposit `0.1` ten times, then print the balance. Then withdraw `0.3`. Compare the result with the expected `1.0` and `0.7`. Write down why the errors occur (remember floating-point representation) and what needs to be done so money is counted exactly: which library fits and how to rewrite the methods. Add this note to the report with severity `важно` or `критично`.

### Task 4
Check reliability and security. Call `acc.deposit("сто")` — what happens? Did the account state break after the error? Check whether the balance can be changed directly via `acc.balance = 1000000` and whether the history can be forged via `acc.transactions`. Then look at the code with style eyes: check line lengths, spaces around operators (PEP 8), the use of `print` instead of logging, and the lack of documentation. Record all observations in the report.

### Task 5
Assemble the final report: number all notes, set priorities, write a verdict («код требует доработки» etc.). Then rewrite the program in `account_fixed.py`: add amount validation, exact money via `decimal.Decimal`, attribute protection, error handling, and clear messages. Verify that the corrected version correctly handles all cases from tasks 2–4.

<!--/TASK-->

<!--HINT-->
### Hint 1
The overview shouldn't be long: purpose, key methods, data types. Run the program with `python account.py` from the folder with the file. Note the statement output format.

### Hint 2
Negative amounts must not change the balance. For "withdraw the whole amount", check the condition: `if self.balance >= amount` is true on equality — so withdrawing the whole amount is **allowed**; make sure the balance becomes 0 afterwards, and decide whether it's a bug or a feature. For withdrawing more — the message «Недостаточно средств».

### Hint 3
Check: `0.1 + 0.1 + ... + 0.1` gives `0.9999999999999999`, not `1.0`. Money is counted via `decimal.Decimal` with strings: `Decimal("0.1")`. Recall the lessons on `Decimal` and `quantize`.

### Hint 4
`acc.deposit("сто")` — an error when adding a string and a number; at that moment the transaction has already been added to the list — the state is partially broken. Direct access: `acc.balance`, `acc.transactions` are public, so the data is unprotected; this is a security issue. Logging: `print` is not suitable for serious code — `logging` is better.

### Hint 5
Verdict: list the main problems (money accuracy, validation, unprotected data) and decide whether the code is ready for production. Corrected code: use `Decimal` for `balance`, check `amount > 0` in both methods, hide data via `_owner`, `_balance`, `_transactions` and add getters, wrap errors in exceptions.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
An example "Overview" section for `review.md`:

```markdown
# Code review: account.py

## Обзор
Программа «Банковский счёт» моделирует простой счёт:
- BankAccount хранит владельца, баланс и список транзакций.
- deposit() добавляет сумму к балансу и пишет транзакцию.
- withdraw() снимает сумму при достаточном балансе.
- show() печатает владельца, баланс и выписку.

Наблюдения: код короткий и читаемый, но методы зависят от
глобального состояния, типы не аннотированы, вывод — через print.
```

Basic scenarios work: `acc.deposit(50)` gives a balance of 150, `acc.withdraw(30)` — 120. At this stage the main thing is to record the "as is" state so you can later compare with expectations.

### Solution 2
The checks give the following results:

| Input | What happens | Rating |
|---|---|---|
| `deposit(-50)` | Balance decreases by 50 | Critical |
| `withdraw(-30)` | Balance grows by 30 | Critical |
| `withdraw(0)` | Nothing, but a transaction is written | Minor |
| `withdraw(1000)` | Message «Недостаточно средств» | OK |
| `withdraw(100)` at balance 100 | Balance 0, withdrawal allowed | Debatable |

Notes: `deposit` and `withdraw` don't check the amount's sign, so negative amounts "work" in reverse. The condition `self.balance >= amount` allows withdrawing the whole amount — this is acceptable behavior, but it's worth noting: `withdraw(0)` writes a useless transaction; it should be forbidden.

### Solution 3

```python
acc = BankAccount("Аня", 0)
for _ in range(10):
    acc.deposit(0.1)
print(acc.balance)  # 0.9999999999999999
acc.withdraw(0.3)
print(acc.balance)  # 0.6999999999999999
```

Cause: floating-point numbers are stored in binary, and `0.1` is not exactly representable. Money needs `decimal.Decimal`:

```python
from decimal import Decimal

# в методах:
self.balance = Decimal(str(amount))  # или Decimal("0.1")
```

Recommendation: store the balance as `Decimal`, accept all amounts as `Decimal` or strings, and format output via `quantize`.

### Solution 4

```python
acc = BankAccount("Аня", 100)
acc.deposit("сто")  # TypeError: unsupported operand type(s) for +
```

The error occurs when adding an `int` and a string; meanwhile the transaction is already added — the state is partially broken. Direct access:

```python
acc.balance = 1000000      # работает
acc.transactions.append("фейк")  # работает
```

Notes:
- **No type validation** — the methods should check that the amount is a number.
- **Unprotected attributes** — `balance` and `transactions` are public; private names (`_balance`, `_transactions`) and getters are needed.
- **Style**: long lines, no spaces around `=` in `__init__` (for example, `self.owner = owner` is fine, but `balance=0` in the signature — PEP 8 recommends `balance=0` without spaces, which is acceptable), output via `print` instead of `logging`.

### Solution 5
Example verdict:

```markdown
Вердикт: код требует доработки перед использованием.
Главные проблемы: неточные деньги (float), отсутствие валидации
отрицательных сумм, незащищённые атрибуты, print вместо логирования.
Рекомендации: перевести на Decimal, добавить проверки, скрыть
данные, логировать через logging.
```

Corrected code in `account_fixed.py`:

```python
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO)

class BankAccount:
    def __init__(self, owner, balance="0"):
        self._owner = owner
        self._balance = Decimal(str(balance))
        self._transactions = []

    def deposit(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._balance += amount
        self._transactions.append(("deposit", amount))
        logging.info("Депозит: %s", amount)

    def withdraw(self, amount):
        amount = Decimal(str(amount))
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount
        self._transactions.append(("withdraw", amount))

    @property
    def balance(self):
        return self._balance

    def show(self):
        print("Владелец:", self._owner)
        print("Баланс:", self._balance)
        for t in self._transactions:
            print(t)
```

Now `deposit(-50)` raises `ValueError`, and so does `withdraw(-30)`; the balance is stored as `Decimal`, and private attributes are protected from direct modification; access to the balance is via the `balance` property.

<!--/SOLUTION-->

<!--QUIZ-->
What is code review?
- Automatic syntax checking
- Reading code by a colleague to find problems and improve quality
- Running tests
- Writing documentation
* Correct answer: Reading code by a colleague to find problems and improve quality
Code review is a systematic analysis of code by another person, not just a syntax check.

Why can't money be stored in float?
- Because floating-point numbers are not exact when representing decimal fractions
- Because float is too slow
- Because float can't add
- It can be stored, there are no errors
* Correct answer: Because floating-point numbers are not exact when representing decimal fractions
0.1 is not exactly representable in binary, so rounding errors accumulate.

What happens with acc.deposit(-50)?
- The balance increases by 50
- The balance decreases by 50
- An error
- Nothing
* Correct answer: The balance decreases by 50
The method doesn't check the sign: a negative amount simply gets added to the balance.

What needs to be done to protect attributes from direct modification?
- Rename them to _balance and add a getter
- Add __slots__
- Make the class final
- Nothing, it's impossible
* Correct answer: Rename them to _balance and add a getter
Private names with an underscore are a convention, and a property gives controlled access.

What should replace print for logging in serious code?
- Nothing, print is universal
- The logging module
- The input function
- Comments
* Correct answer: The logging module
logging has levels, filters, and file output — print only suits simple scripts.

What will withdraw(0) return?
- The message «Недостаточно средств»
- Nothing, but an empty transaction gets added
- An error
- The balance becomes zero
* Correct answer: Nothing, but an empty transaction gets added
The condition `balance >= 0` is true, so a zero transaction gets written — garbage in the history.

Which data type fits money?
- int
- float
- decimal.Decimal
- str
* Correct answer: decimal.Decimal
Decimal performs exact decimal arithmetic; amounts are better passed as strings.

What is a note's severity in the report?
- The order of viewing the file
- The degree of the problem's impact on the code's behavior
- Code beauty
- Writing time
* Correct answer: The degree of the problem's impact on the code's behavior
Severity (critical/important/minor) helps prioritize fixes.

What must each report entry contain?
- Only the problem's name
- Severity, line, description, reproduction, and a recommendation
- Only the corrected code
- Nothing, just a file list
* Correct answer: Severity, line, description, reproduction, and a recommendation
A full entry lets the author understand the problem and fix it quickly.

Why is it important to reproduce a bug before recording it?
- To make sure the problem is real and understand the conditions under which it appears
- To spend more time
- To make the program faster
- It's optional
* Correct answer: To make sure the problem is real and understand the conditions under which it appears
Reproduction distinguishes a confirmed bug from a guess.
<!--/QUIZ-->
