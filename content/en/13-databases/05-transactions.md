---
title: Transactions and ACID
summary: Begin/commit/rollback, isolation.
order: 5
duration: 40 min
difficulty: advanced
tags: sql, transactions, acid
---

Transactions group operations that must all succeed.

## Basic

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

## Rollback

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
ROLLBACK;
```

## ACID

- Atomicity — all or nothing;
- Consistency — valid state;
- Isolation — concurrent safety;
- Durability — survives crash.

## Lesson summary

Transactions protect data consistency.

<!--TASK-->
### Task 1 — Transfer
Write a two-step transfer.

### Task 2 — Commit
Commit it.

### Task 3 — Rollback
Roll back a wrong update.

### Task 4 — Atomicity
Explain all-or-nothing.

### Task 5 — Isolation
Explain concurrent transactions.

### Task 6 — Python
Use a transaction with sqlite3.

### Task 7 — Savepoint
Use SAVEPOINT.
<!--/TASK-->

<!--HINT-->
### Hint 1
BEGIN.

### Hint 2
COMMIT.

### Hint 3
ROLLBACK.

### Hint 4
All or none.

### Hint 5
Parallel.

### Hint 6
conn.commit().

### Hint 7
SAVEPOINT.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### Solution 2
```sql
COMMIT;
```

### Solution 3
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
ROLLBACK;
```

### Solution 4
```sql
-- Все операции выполняются как одна:
-- либо все, либо ни одна
```

### Solution 5
```sql
-- Параллельные транзакции не должны
-- видеть чужие незавершённые данные
```

### Solution 6
```python
import sqlite3
conn = sqlite3.connect("bank.db")
cur = conn.cursor()
try:
    cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    conn.commit()
except Exception:
    conn.rollback()
    raise
```

### Solution 7
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT sp;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
ROLLBACK TO sp;
COMMIT;
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a transaction?
- A group of ops
- One op
- A table
- None
* Correct answer: A group of ops
Atomic.

What is COMMIT?
- Saves changes
- Cancels
- Pauses
- None
* Correct answer: Saves changes
Permanent.

What is ROLLBACK?
- Undoes changes
- Saves
- Starts
- None
* Correct answer: Undoes changes
Cancel.

What is atomicity?
- All or nothing
- Partial
- Fast
- None
* Correct answer: All or nothing
Either.

What is consistency?
- Valid state
- Fast
- Random
- None
* Correct answer: Valid state
Rules.

What is isolation?
- Concurrent safety
- Secrecy
- Speed
- None
* Correct answer: Concurrent safety
Transactions.

What is durability?
- Survives crash
- Temporary
- Fast
- None
* Correct answer: Survives crash
Disk.

What is a savepoint?
- Partial rollback point
- A commit
- A start
- None
* Correct answer: Partial rollback point
Nested.

What is conn.commit()?
- Saves in Python
- Reads
- Closes
- None
* Correct answer: Saves in Python
SQLite.

What is conn.rollback()?
- Undoes in Python
- Saves
- Opens
- None
* Correct answer: Undoes in Python
Except.

Why transactions in banking?
- No lost money
- Speed
- Style
- None
* Correct answer: No lost money
Safety.

What is a deadlock?
- Two wait on each other
- An error
- A rollback
- None
* Correct answer: Two wait on each other
Concurrency.
<!--/QUIZ-->
