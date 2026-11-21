---
title: SQL and databases
summary: SQLite, CREATE/SELECT/INSERT/UPDATE/DELETE, WHERE, joins basics.
order: 10
duration: 45 min
difficulty: intermediate
tags: sql, sqlite, queries
---

SQL talks to databases; SQLite is built into Python.

## Connect

```python
import sqlite3
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
```

## CREATE

```sql
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price REAL
);
```

## CRUD

```sql
INSERT INTO products (name, price) VALUES ('Pen', 10);
SELECT * FROM products WHERE price < 20;
UPDATE products SET price = 12 WHERE name = 'Pen';
DELETE FROM products WHERE name = 'Pen';
```

## Commit

```python
con.commit()
con.close()
```

## Lesson summary

SQLite + SQL: create, read, update, delete; commit changes.

<!--TASK-->
### Task 1 — Connect
Open an in-memory database and create a table.

### Task 2 — Insert
Insert three rows.

### Task 3 — Select
Select all rows and print.

### Task 4 — Where
Select rows with price < 20.

### Task 5 — Update
Update a price and print the change.

### Task 6 — Delete
Delete one row and count remaining.

### Task 7 — Commit
Persist to a file DB and reopen.
<!--/TASK-->

<!--HINT-->
### Hint 1
sqlite3.connect(":memory:").

### Hint 2
cur.execute("INSERT ...", (name, price)).

### Hint 3
cur.execute("SELECT *").fetchall().

### Hint 4
WHERE price < ?.

### Hint 5
UPDATE ... SET price = ? WHERE name = ?.

### Hint 6
DELETE ... WHERE name = ?.

### Hint 7
connect("file.db"); commit.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import sqlite3
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("""CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)""")
```

### Solution 2
```python
rows = [("Pen", 10), ("Book", 50), ("Note", 5)]
cur.executemany("INSERT INTO products (name, price) VALUES (?, ?)", rows)
```

### Solution 3
```python
print(cur.execute("SELECT * FROM products").fetchall())
```

### Solution 4
```python
print(cur.execute("SELECT * FROM products WHERE price < ?", (20,)).fetchall())
```

### Solution 5
```python
cur.execute("UPDATE products SET price = ? WHERE name = ?", (12, "Pen"))
con.commit()
```

### Solution 6
```python
cur.execute("DELETE FROM products WHERE name = ?", ("Note",))
print(cur.execute("SELECT COUNT(*) FROM products").fetchone()[0])
```

### Solution 7
```python
con = sqlite3.connect("db.sqlite3")
# ... операции ...
con.commit()
con.close()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQLite?
- Embedded database
- Server DB
- ORM
- CSV
* Correct answer: Embedded database
File-based.

How to connect?
- sqlite3.connect("db")
- sql.connect
- open()
- db()
* Correct answer: sqlite3.connect("db")
Standard.

What does CREATE TABLE do?
- Creates a table
- Deletes
- Reads
- Updates
* Correct answer: Creates a table
Schema.

What does SELECT do?
- Reads data
- Inserts
- Deletes
- Creates
* Correct answer: Reads data
Query.

What does WHERE do?
- Filters rows
- Sorts
- Groups
- Joins
* Correct answer: Filters rows
Condition.

What does INSERT do?
- Adds a row
- Reads
- Deletes
- Updates
* Correct answer: Adds a row
Create.

What does UPDATE do?
- Modifies rows
- Adds
- Reads
- Drops
* Correct answer: Modifies rows
Change.

What does DELETE do?
- Removes rows
- Drops table
- Selects
- Inserts
* Correct answer: Removes rows
Remove.

What is a parameterized query?
- ? placeholders
- f-string
- + concatenation
- raw
* Correct answer: ? placeholders
Safe.

What does commit do?
- Saves changes
- Reads
- Closes
- Rolls back
* Correct answer: Saves changes
Persist.

What does fetchall do?
- Returns all rows
- One row
- None
- Cursor
* Correct answer: Returns all rows
List.

What is PRIMARY KEY?
- Unique row id
- Name
- Price
- Foreign
* Correct answer: Unique row id
Identity.
<!--/QUIZ-->
