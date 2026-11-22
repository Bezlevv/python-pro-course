---
title: SQLite from Python: sqlite3
summary: Connect, execute, parameters, fetch.
order: 6
duration: 45 min
difficulty: intermediate
tags: sqlite, sqlite3
---

SQLite is a file database built into Python.

## Connect

```python
import sqlite3
conn = sqlite3.connect("app.db")
cur = conn.cursor()
```

## Execute

```python
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
conn.commit()
```

## Fetch

```python
cur.execute("SELECT * FROM users")
print(cur.fetchall())
```

## Parameter safety

Always use ? placeholders.

## Lesson summary

sqlite3 gives a full database without a server.

<!--TASK-->
### Task 1 — Connect
Open app.db.

### Task 2 — Table
Create a table.

### Task 3 — Insert
Insert a row with a placeholder.

### Task 4 — Fetch
Select all rows.

### Task 5 — Update
Update a value.

### Task 6 — Delete
Delete a row.

### Task 7 — Context
Use with conn:.
<!--/TASK-->

<!--HINT-->
### Hint 1
sqlite3.connect.

### Hint 2
CREATE TABLE.

### Hint 3
(?,).

### Hint 4
fetchall.

### Hint 5
UPDATE.

### Hint 6
DELETE.

### Hint 7
with conn.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import sqlite3
conn = sqlite3.connect("app.db")
```

### Solution 2
```python
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")
```

### Solution 3
```python
cur.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
conn.commit()
```

### Solution 4
```python
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)
```

### Solution 5
```python
cur.execute("UPDATE users SET name = ? WHERE id = ?", ("Alicia", 1))
conn.commit()
```

### Solution 6
```python
cur.execute("DELETE FROM users WHERE id = ?", (1,))
conn.commit()
```

### Solution 7
```python
with sqlite3.connect("app.db") as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
# with фиксирует транзакцию при успехе
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQLite?
- File database
- Server DB
- A Python lib only
- None
* Correct answer: File database
Embedded.

What is sqlite3?
- Built-in module
- A server
- A package
- None
* Correct answer: Built-in module
Standard.

What does connect do?
- Opens database
- Queries
- Closes
- None
* Correct answer: Opens database
File.

What is a cursor?
- Executes queries
- Opens file
- Closes
- None
* Correct answer: Executes queries
Object.

What is execute?
- Runs one statement
- Opens
- Connects
- None
* Correct answer: Runs one statement
SQL.

What are placeholders?
- ? params
- Direct text
- Errors
- None
* Correct answer: ? params
Safe.

Why placeholders?
- Prevents injection
- Faster
- Required
- None
* Correct answer: Prevents injection
Security.

What is commit?
- Saves changes
- Reads
- Opens
- None
* Correct answer: Saves changes
Persist.

What is fetchall?
- All rows
- One row
- None
- Query
* Correct answer: All rows
List.

What is INTEGER PRIMARY KEY?
- Auto id
- Text
- Float
- None
* Correct answer: Auto id
Rowid.

What is the with block?
- Auto-commits
- Errors
- Slower
- None
* Correct answer: Auto-commits
Context.

What is a row?
- Tuple
- Dict
- String
- None
* Correct answer: Tuple
Values.
<!--/QUIZ-->
