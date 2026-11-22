---
title: Normalization and indexes
summary: Bring a database schema to normal forms (1NF–3NF) and speed up queries with indexes: CREATE INDEX, unique and composite indexes, EXPLAIN QUERY PLAN.
order: 2
duration: 45 min
difficulty: advanced
tags: normalization, nf, indexes, explain, performance
---

## Why normalize

Normalization is the process of organizing tables to reduce redundancy and anomalies. Imagine an orders table where the customer name is stored directly in each order row:

| order_id | client_name | client_phone | product |
|---|---|---|---|
| 1 | Anya | +7-111 | Keyboard |
| 2 | Anya | +7-111 | Mouse |

If Anya changes her phone number, you'd have to update several rows: that's an update anomaly. If she cancels all her orders, you lose the customer information: that's a deletion anomaly. If you need to add a customer without orders, you'd have to insert a row with an empty order: that's an insertion anomaly. Normalization distributes data across tables so that each entity is stored in one place and changed once.

## First normal form (1NF)

A table is in 1NF if all cell values are atomic (you can't store a comma-separated list) and the table has a primary key. Here is a violation:

```sql
CREATE TABLE bad_orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    items TEXT  -- 'keyboard,mouse' — not atomic!
);
```

## Second normal form (2NF)

2NF requires 1NF and the absence of partial dependencies: every non-key column must depend on the whole composite key, not on a part of it.

```sql
CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

Here price depends on the pair (order_id, product_id) — on both parts of the key. If we added `user_name`, which depends only on `order_id`, that would violate 2NF: the customer name would be duplicated in every row of the same order.

## Third normal form (3NF)

3NF requires 2NF and the absence of transitive dependencies: non-key columns must not depend on each other through a third one. For example, a city depends on a postal code, and the code depends on the address:

```sql
-- Bad: country depends on city, and city depends on address
CREATE TABLE customers_bad (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city TEXT,
    country TEXT
);

-- Good: city and country are moved into a lookup table
CREATE TABLE cities (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    country TEXT
);
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    address TEXT,
    city_id INTEGER REFERENCES cities(id)
);
```

If a country changes its name, in the "bad" schema you'd have to update every customer record; in the "good" schema — one row of the lookup table.

## Normalization is not dogma

After 3NF there are BCNF, 4NF, 5NF, but in practice aiming for 3NF is the sweet spot. Sometimes a schema is deliberately denormalized: an extra column is added to speed up frequent reads (for example, a precomputed order total in a user profile). The key is to do it deliberately, with a comment in the code and a clear understanding of which anomaly you are introducing.

## Indexes

An index is a structure (usually a B-tree) that lets you find rows by a column without scanning the whole table. Without an index the DBMS looks through every row: in a table of 100,000 rows — 100,000 comparisons. With an index — dozens of steps.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT,
    price REAL
);
""")
cur.executemany(
    "INSERT INTO products (id, sku, price) VALUES (?, ?, ?)",
    [(i, f"SKU-{i}", i * 10) for i in range(200_000)],
)
conn.commit()

cur.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE sku = 'SKU-199999'")
print("Before index:", cur.fetchall())

cur.execute("CREATE INDEX idx_products_sku ON products(sku)")
cur.execute("EXPLAIN QUERY PLAN SELECT * FROM products WHERE sku = 'SKU-199999'")
print("After index:", cur.fetchall())
```

Before the index the plan is `SCAN products` (full scan), after — `SEARCH products USING INDEX` (index lookup).

## Types of indexes

- Unique: `CREATE UNIQUE INDEX ...` — prevents inserting a duplicate.
- Composite: `CREATE INDEX idx ON orders(user_id, status)` — useful for queries with WHERE on both columns.
- Covering: if the index contains all the needed columns, the DBMS does not read the table itself.
- Cost: every index slows down INSERT/UPDATE/DELETE (the tree must be updated), so indexes are created for real queries, not "just in case".

## When an index doesn't help

- In small tables a full scan is faster.
- When selectivity is low: for example, a column with two values out of a million rows — the index would return almost the whole table.
- With `LIKE '%...'` — a literal search with a leading `%` does not use a regular B-tree index.

```mermaid
flowchart LR
    A["Table"] --> B["Normalization: 1NF→3NF"]
    B --> C["Indexes"]
    C --> D["EXPLAIN QUERY PLAN"]
```

## Summary

Normalization makes a schema honest and resilient to change, and indexes make it fast. Both tools should be applied deliberately: formal normalization for the sake of a checkbox and endless indexes are equally harmful. Verify your indexes with EXPLAIN QUERY PLAN.

<!--TASK-->
### Task 1
Given a table with a 2NF violation:

```python
cur.executescript("""
CREATE TABLE order_items_bad (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
INSERT INTO order_items_bad VALUES
    (1, 10, 'Keyboard', 1500),
    (1, 20, 'Mouse', 800),
    (2, 10, 'Keyboard', 1500),
    (3, 30, 'Monitor', 12000);
""")
```

`product_name` depends only on `product_id` — that's a partial dependency. Write a function `split_to_2nf(conn)` that creates `products(product_id, product_name)` and `order_items(order_id, product_id, price)` tables, moves the data over, and returns the tuple `(n_products, n_items)`. Expected output: `(3, 4)` (three products, four order line items).

### Task 2
Given a table with a transitive dependency:

```python
cur.executescript("""
CREATE TABLE employees_bad (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    department_name TEXT NOT NULL,
    department_floor INTEGER NOT NULL
);
INSERT INTO employees_bad VALUES
    (1, 'Anya', 10, 'Development', 3),
    (2, 'Boris', 10, 'Development', 3),
    (3, 'Vera', 20, 'Marketing', 5),
    (4, 'Gleb', 20, 'Marketing', 5);
""")
```

`department_name` and `department_floor` depend on `department_id`, not on `id`. Write a function `to_3nf(conn)` that creates `departments(department_id, name, floor)` and `employees(id, name, department_id)`, moves the data over, and returns `(n_depts, n_emps)`. Expected output: `(2, 4)`.

### Task 3
Write a function `index_plan(conn)` that, in a database with an `orders(user_id, amount)` table (fill it with 1000 random rows yourself), does the following: first runs `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42` and remembers the plan, then creates the index `CREATE INDEX idx_orders_user ON orders(user_id)` and runs the same EXPLAIN again. Return the tuple `(plan_before, plan_after)`. `plan_before` should contain the substring `SCAN`, `plan_after` — `USING INDEX`. Print both plans.

### Task 4
Write a function `enforce_unique(conn)` that creates a `users(id, email)` table, fills it with two rows, adds `CREATE UNIQUE INDEX idx_users_email ON users(email)`, and then tries to insert a third row with an existing email. Catch `sqlite3.IntegrityError` and return the string `"blocked"` — or return `"inserted"` if the duplicate went through. Expected output: `blocked`.

### Task 5
Write a function `composite_plan(conn)` that creates an `orders(id, user_id, status, amount)` table, fills it with 500 rows (statuses `'new'` and `'done'`), then creates a composite index `CREATE INDEX idx_orders_user_status ON orders(user_id, status)`. After that run `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 7 AND status = 'new'` and return the plan string. Check that it contains `USING INDEX`. Print the plan.
### Task 6 — Composite index and EXPLAIN
Create an orders table (id, user_id, status, created_at) and fill it with 1000 rows. Add a composite index `(user_id, status)` and show `EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id=? AND status=?` with and without the index (DROP INDEX). Expected result: a plan with "SEARCH ... USING INDEX" versus "SCAN".
### Task 7 — Denormalization for reads
Explain with an example: for frequently showing "customer name + number of orders", you can add an orders_count field to users and update it on every order. Implement a SQLite trigger `AFTER INSERT ON orders` that increments orders_count. Verify that the value grows after an insert.

<!--/TASK-->

<!--HINT-->
### Hint 1
Create the tables via `CREATE TABLE products AS SELECT DISTINCT product_id, product_name FROM order_items_bad` or manually with DISTINCT values inserted. For order_items, just select order_id, product_id, price from the source table. Count rows with `SELECT COUNT(*)` on each new table.

### Hint 2
First create `departments` with DISTINCT values of `department_id, department_name, department_floor` from employees_bad. Then create `employees` with `id, name, department_id` from employees_bad and add a foreign key to departments. Return `(COUNT(departments), COUNT(employees))`.

### Hint 3
EXPLAIN QUERY PLAN returns rows like `(0, 0, 0, 'SCAN orders')` — the plan is in the fourth element of the tuple. Collect all rows into a list and join them into strings with `" ".join(...)`. Before creating the index you'll see SCAN, after — SEARCH ... USING INDEX.

### Hint 4
Wrap the duplicate insert in `try/except sqlite3.IntegrityError`. Remember: the unique index is checked at INSERT, so violating the constraint raises an exception. Don't forget `conn.commit()` after the initial inserts. The duplicate is the second insert with the same email.

### Hint 5
A composite index works when the columns in WHERE come in the same order as in the index (first user_id, then status). Generate the rows with a loop: `user_id = i % 50`, `status = 'new' if i % 2 == 0 else 'done'`, `amount = i * 10`. In EXPLAIN look for `SEARCH orders USING INDEX idx_orders_user_status`.
### Hint 6
Index: `CREATE INDEX idx_orders_user_status ON orders(user_id, status)`. EXPLAIN will show whether the index is used.
### Hint 7
Trigger: `CREATE TRIGGER inc_orders AFTER INSERT ON orders BEGIN UPDATE users SET orders_count = orders_count + 1 WHERE id = NEW.user_id; END;`

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import sqlite3

def split_to_2nf(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE order_items_bad (
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        PRIMARY KEY (order_id, product_id)
    );
    INSERT INTO order_items_bad VALUES
        (1, 10, 'Keyboard', 1500),
        (1, 20, 'Mouse', 800),
        (2, 10, 'Keyboard', 1500),
        (3, 30, 'Monitor', 12000);
    CREATE TABLE products AS
        SELECT DISTINCT product_id, product_name FROM order_items_bad;
    CREATE TABLE order_items AS
        SELECT order_id, product_id, price FROM order_items_bad;
    """)
    conn.commit()
    n_products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    n_items = cur.execute("SELECT COUNT(*) FROM order_items").fetchone()[0]
    return (n_products, n_items)

conn = sqlite3.connect(":memory:")
print(split_to_2nf(conn))
```

Result:

```
(3, 4)
```

What's happening here? The source table stores the product name in every order row: if "Keyboard" is renamed, you'd have to update two rows. We move products into a separate `products` table — DISTINCT removes duplicate names. The `order_items` table keeps the pair key and the price, which genuinely depends on the pair (order_id, product_id). There are 3 products and 4 order line items. Now the product name lives in one place.

### Solution 2
Solution:

```python
import sqlite3

def to_3nf(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE employees_bad (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department_id INTEGER NOT NULL,
        department_name TEXT NOT NULL,
        department_floor INTEGER NOT NULL
    );
    INSERT INTO employees_bad VALUES
        (1, 'Anya', 10, 'Development', 3),
        (2, 'Boris', 10, 'Development', 3),
        (3, 'Vera', 20, 'Marketing', 5),
        (4, 'Gleb', 20, 'Marketing', 5);
    CREATE TABLE departments AS
        SELECT DISTINCT department_id, department_name AS name, department_floor AS floor
        FROM employees_bad;
    CREATE TABLE employees AS
        SELECT id, name, department_id FROM employees_bad;
    """)
    conn.commit()
    n_depts = cur.execute("SELECT COUNT(*) FROM departments").fetchone()[0]
    n_emps = cur.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    return (n_depts, n_emps)

conn = sqlite3.connect(":memory:")
print(to_3nf(conn))
```

Result:

```
(2, 4)
```

What's happening here? In employees_bad the department name and floor are repeated for every employee and depend on department_id — that's a transitive dependency (employee → department → its attributes). We move departments into a lookup table: DISTINCT removes duplicates, so we get 2 departments instead of 4. In employees only the data that directly depends on the employee id remains. Now moving a department to another floor is an update of one lookup row, not four.

### Solution 3
Solution:

```python
import sqlite3

def index_plan(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE orders (user_id INTEGER, amount REAL);
    """)
    cur.executemany(
        "INSERT INTO orders VALUES (?, ?)",
        [(i % 100, i * 3.5) for i in range(1000)],
    )
    conn.commit()
    plan_before = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42"
    ).fetchall()
    cur.execute("CREATE INDEX idx_orders_user ON orders(user_id)")
    plan_after = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 42"
    ).fetchall()
    fmt = lambda rows: " | ".join(row[3] for row in rows)
    return (fmt(plan_before), fmt(plan_after))

conn = sqlite3.connect(":memory:")
before, after = index_plan(conn)
print("Before:", before)
print("After:", after)
```

Result (approximately):

```
Before: SCAN orders
After: SEARCH orders USING INDEX idx_orders_user (user_id=)
```

What's happening here? Without an index the planner has to read all 1000 rows — the plan is SCAN orders. After creating the index the plan changes to SEARCH ... USING INDEX: the DBMS walks down the B-tree and finds the needed rows in O(log n) steps. For 1000 rows the difference is imperceptible, but on millions it becomes orders of magnitude. Remember the technique itself: before arguing about speed, look at EXPLAIN QUERY PLAN — the plan will tell you whether the index is used at all.

### Solution 4
Solution:

```python
import sqlite3

def enforce_unique(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT);
    INSERT INTO users VALUES (1, 'anya@example.com'), (2, 'boris@example.com');
    CREATE UNIQUE INDEX idx_users_email ON users(email);
    """)
    conn.commit()
    try:
        cur.execute("INSERT INTO users VALUES (3, 'anya@example.com')")
        conn.commit()
        return "inserted"
    except sqlite3.IntegrityError:
        return "blocked"

conn = sqlite3.connect(":memory:")
print(enforce_unique(conn))
```

Result:

```
blocked
```

What's happening here? A unique index guarantees uniqueness at the DBMS level, not in application code. When an attempt is made to insert the email `anya@example.com` a second time, SQLite rejects the insert and raises IntegrityError. We catch it and return "blocked". Note: the check happens even if some other part of the application "forgot" to check for a duplicate. That's why unique indexes are the standard way to protect emails, SKUs and other natural keys.

### Solution 5
Solution:

```python
import sqlite3

def composite_plan(conn):
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT,
        amount REAL
    );
    """)
    rows = [
        (i, i % 50, "new" if i % 2 == 0 else "done", i * 10.0)
        for i in range(500)
    ]
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", rows)
    conn.commit()
    cur.execute("CREATE INDEX idx_orders_user_status ON orders(user_id, status)")
    plan = cur.execute(
        "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 7 AND status = 'new'"
    ).fetchall()
    return " | ".join(row[3] for row in plan)

conn = sqlite3.connect(":memory:")
print(composite_plan(conn))
```

Result (approximately):

```
SEARCH orders USING INDEX idx_orders_user_status (user_id=? AND status=)
```

What's happening here? The composite index `(user_id, status)` serves queries that filter on both columns. Column order matters: an index on (user_id, status) helps both `WHERE user_id = 7` and `WHERE user_id = 7 AND status = 'new'`, but not `WHERE status = 'new'` — the leftmost index column must participate in the condition. If we had created the index on (status, user_id), the situation would be reversed. The SEARCH plan confirms: the database walks the index instead of scanning the table.
### Solution 6
```sql
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1 AND status = 'new';
-- SEARCH orders USING INDEX idx_orders_user_status
DROP INDEX idx_orders_user_status;
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 1 AND status = 'new';
-- SCAN orders
```
A composite index speeds up filters on both columns; without it — a full scan.
### Solution 7
```sql
CREATE TRIGGER inc_orders AFTER INSERT ON orders
BEGIN
    UPDATE users SET orders_count = orders_count + 1
    WHERE id = NEW.user_id;
END;
```
After an INSERT of an order the counter updates automatically. Denormalization is a deliberate trade-off for read speed.

<!--/SOLUTION-->

<!--QUIZ-->
Which anomaly occurs when a customer changes the phone number stored in every row of their orders?
- Deletion anomaly
- Update anomaly
- Insertion anomaly
- None, it's fine
* Correct answer: Update anomaly
One change must be repeated across several rows, and it's easy to forget to update one of them.

What is required for 2NF?
- Only having a primary key
- 1NF and no partial dependencies on the composite key
- No transitive dependencies
- All columns unique
* Correct answer: 1NF and no partial dependencies on the composite key
2NF adds to 1NF the requirement: non-key columns depend on the whole key, not on a part of it.

What is a transitive dependency (a 3NF violation)?
- A column depends on another non-key column, which depends on the key
- Two columns are completely identical
- A column depends on the composite key
- A dependency on another table
* Correct answer: A column depends on another non-key column, which depends on the key
For example, a country depends on a city, and a city depends on an address; that's a sign of a bad schema.

What is an index in a database?
- A copy of the whole table
- A structure for quickly finding rows by a column
- A list of table constraints
- A change log
* Correct answer: A structure for quickly finding rows by a column
An index (usually a B-tree) lets you find rows without scanning the whole table.

What is the cost of each index?
- Data takes less storage space
- INSERT/UPDATE/DELETE slow down
- Writes speed up
- Indexes are free
* Correct answer: INSERT/UPDATE/DELETE slow down
Every write must also update the index tree, so indexes are created for real queries.

What will EXPLAIN QUERY PLAN show after creating a suitable index?
- SCAN of the table
- SEARCH of the table USING INDEX
- A syntax error
- An empty result
* Correct answer: SEARCH of the table USING INDEX
The plan shows how the database retrieves data: via an index (SEARCH ... USING INDEX) or a full scan (SCAN).

Why is a UNIQUE INDEX needed?
- To speed up retrieval
- To guarantee uniqueness of values at the DBMS level
- To forbid NULL
- To speed up writes
* Correct answer: To guarantee uniqueness of values at the DBMS level
A unique index prevents inserting a duplicate even if the application code forgot to check.

What are the requirements of the first normal form (1NF)?
- Atomic values in cells and a primary key
- No partial dependencies
- No transitive dependencies
* Correct answer: Atomic values in cells and a primary key
Storing a comma-separated list in one cell violates 1NF.
What is a composite index?
- An index on several columns
- An index on one column
- A unique index
- A primary key
* Correct answer: An index on several columns
The order of columns matters for queries.

What will EXPLAIN QUERY PLAN show?
- How the DBMS intends to execute the query
- Data
- Errors
- Indexes
* Correct answer: How the DBMS intends to execute the query
SEARCH ... USING INDEX means the index is used.

What is a trigger?
- Code that runs automatically on an event (INSERT/UPDATE/DELETE)
- A view
- A stored function
- An index
* Correct answer: Code that runs automatically on an event
A trigger performs actions after/before a change.

When is denormalization useful?
- When aggregates are read often and writes are rare
- Always
- Never
- Only in tests
* Correct answer: When aggregates are read often and writes are rare
We sacrifice write consistency for read speed.

# 
<!--/QUIZ-->
