---
title: PostgreSQL: setup and psycopg
summary: Install, create db, psycopg connect.
order: 7
duration: 50 min
difficulty: advanced
tags: postgres, psycopg
---

PostgreSQL is a powerful server database.

## Create database

```bash
createdb mydb
psql mydb
```

## Python: psycopg

```python
import psycopg

with psycopg.connect("dbname=mydb user=postgres password=secret") as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS items (id serial PRIMARY KEY, name text)")
        cur.execute("INSERT INTO items (name) VALUES (%s)", ("book",))
```

## Placeholders

psycopg uses %s.

## Lesson summary

Postgres for production; psycopg is the driver.

<!--TASK-->
### Task 1 — Crate db
Create a database.

### Task 2 — Connect
Connect with psycopg.

### Task 3 — Table
Create a table with serial id.

### Task 4 — Insert
Insert with %s.

### Task 5 — Query
Select rows.

### Task 6 — Error
Handle connection error.

### Task 7 — Compare
SQLite vs Postgres.
<!--/TASK-->

<!--HINT-->
### Hint 1
createdb.

### Hint 2
psycopg.connect.

### Hint 3
serial.

### Hint 4
%s.

### Hint 5
fetchall.

### Hint 6
try/except.

### Hint 7
Server vs file.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```bash
createdb mydb
psql mydb
```

### Solution 2
```python
import psycopg
conn = psycopg.connect("dbname=mydb user=postgres password=secret")
```

### Solution 3
```python
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id serial PRIMARY KEY,
            name text NOT NULL
        )
    """)
```

### Solution 4
```python
with conn.cursor() as cur:
    cur.execute("INSERT INTO items (name) VALUES (%s)", ("book",))
conn.commit()
```

### Solution 5
```python
with conn.cursor() as cur:
    cur.execute("SELECT * FROM items")
    for row in cur.fetchall():
        print(row)
```

### Solution 6
```python
try:
    conn = psycopg.connect("dbname=mydb user=postgres password=secret")
except psycopg.OperationalError as e:
    print("connection failed:", e)
```

### Solution 7
```python
# SQLite: файл, без сервера, для малого объёма
# PostgreSQL: сервер, конкурентность, для продакшена
```
<!--/SOLUTION-->

<!--QUIZ-->
What is PostgreSQL?
- Server DB
- File DB
- Python module
- None
* Correct answer: Server DB
Production.

What is createdb?
- Creates database
- Deletes
- Connects
- None
* Correct answer: Creates database
CLI.

What is psycopg?
- PostgreSQL driver
- A database
- SQLite
- None
* Correct answer: PostgreSQL driver
Python.

What is %s?
- Placeholder
- String
- Error
- None
* Correct answer: Placeholder
psycopg.

What is serial?
- Auto-increment
- A type only
- A key only
- None
* Correct answer: Auto-increment
Integer.

What is conn.cursor()?
- Execute queries
- Connect
- Close
- None
* Correct answer: Execute queries
Cursor.

What is commit?
- Saves
- Reads
- Opens
- None
* Correct answer: Saves
Transaction.

What is OperationalError?
- Connection failure
- Logic error
- Warning
- None
* Correct answer: Connection failure
Exception.

What is dbname?
- Database name
- Host
- User
- None
* Correct answer: Database name
Conn.

What is psql?
- CLI client
- Server
- Driver
- None
* Correct answer: CLI client
Shell.

When use Postgres?
- Production
- Prototypes
- Never
- None
* Correct answer: Production
Scale.

What is a connection string?
- dbname/user/password
- SQL
- Table
- None
* Correct answer: dbname/user/password
Params.
<!--/QUIZ-->
