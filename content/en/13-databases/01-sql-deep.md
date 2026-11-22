---
title: SQL Deep Dive: JOIN, aggregations, subqueries
summary: Join tables (INNER/LEFT JOIN), aggregate data (GROUP BY, HAVING) and build subqueries and CTEs with live examples using sqlite3.
order: 1
duration: 45 min
difficulty: advanced
tags: sql, join, group by, subqueries, cte, sqlite3
---

## Why a single SELECT is not enough

So far we have worked with a single table. But real databases consist of dozens of related tables: users, orders, products, payments. To get a meaningful answer, you have to join data together. In this lesson you will learn how to:

- join tables with different kinds of JOIN;
- aggregate rows with COUNT, SUM, AVG, MIN, MAX;
- group with GROUP BY and filter groups with HAVING;
- use subqueries and common table expressions (CTEs).

All the code works with the sqlite3 module — it is built into Python, and nothing needs to be installed.

## Our sample database

Imagine an online store. Let's create two tables: `users` and `orders`.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.executescript("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL
);
INSERT INTO users (id, name) VALUES
    (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
INSERT INTO orders (id, user_id, amount) VALUES
    (101, 1, 1500), (102, 1, 800),
    (103, 2, 3200), (104, 2, 900);
""")
print("Tables created")
```

Notice: Vera (id=3) has no orders. This will come in handy for the LEFT JOIN exercises.

## INNER JOIN: only the intersection

INNER JOIN keeps only the rows of the two tables that matched the join condition.

```python
cur.execute("""
SELECT users.name, orders.amount
FROM users
JOIN orders ON orders.user_id = users.id
ORDER BY users.name
""")
for name, amount in cur.fetchall():
    print(name, amount)
```

Output:

```
Anya 1500.0
Anya 800.0
Boris 3200.0
Boris 900.0
```

Vera is missing — she has no orders, so there is nothing for her to join on.

## LEFT JOIN: keep the whole left table

LEFT JOIN takes all rows of the left table (`users`) and fills in data from the right side wherever it exists. Where there is no match, NULL is inserted.

```python
cur.execute("""
SELECT users.name, COALESCE(SUM(orders.amount), 0) AS total
FROM users
LEFT JOIN orders ON orders.user_id = users.id
GROUP BY users.id
ORDER BY users.name
""")
for name, total in cur.fetchall():
    print(name, total)
```

Output:

```
Anya 2300.0
Boris 4100.0
Vera 0.0
```

With COALESCE we turn NULL into 0. Notice: aggregation made an appearance here too — more on that below.

## Aggregate functions and GROUP BY

Aggregate functions: COUNT — number of rows, SUM — sum, AVG — average, MIN/MAX — minimum/maximum. GROUP BY splits rows into groups by column value, and an aggregate function is applied to each group separately.

```python
cur.execute("""
SELECT users.name, COUNT(orders.id) AS cnt, SUM(orders.amount) AS total
FROM users
LEFT JOIN orders ON orders.user_id = users.id
GROUP BY users.id
""")
for name, cnt, total in cur.fetchall():
    print(name, cnt, total)
```

Output:

```
Anya 2 2300.0
Boris 2 4100.0
Vera 0 0.0
```

Important: any column in SELECT that is not an argument of an aggregate function must be listed in GROUP BY (or used inside another aggregate function).

## HAVING: filter by groups

WHERE filters rows before grouping. To filter the resulting groups, use HAVING.

```python
cur.execute("""
SELECT users.name, SUM(orders.amount) AS total
FROM users
JOIN orders ON orders.user_id = users.id
GROUP BY users.id
HAVING SUM(orders.amount) > 2000
""")
for name, total in cur.fetchall():
    print(name, total)
```

Output:

```
Anya 2300.0
Boris 4100.0
```

## Subqueries

A subquery is a query inside another query. It can appear in WHERE, FROM, SELECT or HAVING. A common pattern is IN with a subquery:

```python
cur.execute("""
SELECT name FROM users
WHERE id IN (
    SELECT user_id FROM orders
    WHERE amount >= 2000
)
""")
for (name,) in cur.fetchall():
    print(name)
```

Output:

```
Boris
```

A correlated subquery references the outer query. For example, let's find each user's largest order:

```python
cur.execute("""
SELECT users.name,
       (SELECT MAX(o.amount) FROM orders o
        WHERE o.user_id = users.id) AS best
FROM users
""")
for name, best in cur.fetchall():
    print(name, best)
```

Output:

```
Anya 1500.0
Boris 3200.0
Vera None
```

## CTE: WITH

A common table expression (CTE) makes a complex query readable: first you describe a "temporary table", then you use it in the main query.

```python
cur.execute("""
WITH totals AS (
    SELECT user_id, SUM(amount) AS total
    FROM orders
    GROUP BY user_id
)
SELECT users.name, totals.total
FROM users
JOIN totals ON totals.user_id = users.id
ORDER BY totals.total DESC
""")
for name, total in cur.fetchall():
    print(name, total)
```

Output:

```
Boris 4100.0
Anya 2300.0
```

## Query execution order

It helps to keep in mind the order in which the DBMS parses a query: it explains why WHERE does not see aggregates, and why aliases from SELECT are sometimes unavailable.

```mermaid
flowchart LR
    A["FROM and JOIN"] --> B["WHERE"]
    B --> C["GROUP BY"]
    C --> D["HAVING"]
    D --> E["Window functions"]
    E --> F["SELECT"]
    F --> G["ORDER BY"]
    G --> H["LIMIT"]
```

## Summary

Now you can join tables, aggregate data, group, filter groups and build subqueries. These skills are the foundation of any serious SQL — from reports to analytics. Let's lock them in with practice.

<!--TASK-->
### Task 1
Write a function `top_spenders()` that connects to an in-memory database, creates `users` and `orders` tables with exactly the same data as in the lesson (Anya — 1500 and 800, Boris — 3200 and 900, Vera — no orders), and returns a list of tuples `(name, total)` for users who have at least one order. Use SUM for the total, sort by total descending. Print the list. Expected output: `[('Boris', 4100.0), ('Anya', 2300.0)]`.

### Task 2
Write a function `left_join_report()` that uses the same schema and returns a list of tuples `(name, total)` for all users, including those with no orders — they should get 0 (use COALESCE). Sort by name alphabetically. Print the list. Expected output: `[('Anya', 2300.0), ('Boris', 4100.0), ('Vera', 0.0)]`.

### Task 3
Write a function `heavy_users(threshold)` that returns only the users whose total order amount is strictly greater than `threshold`. Use GROUP BY together with HAVING. For `threshold=2000` expected output: `[('Anya', 2300.0), ('Boris', 4100.0)]`. For `threshold=3000` expected output: `[('Boris', 4100.0)]`.

### Task 4
Write a function `who_ordered_over(min_amount)` that uses a subquery with IN to return the names of users who have at least one order with an amount of at least `min_amount`. Sort the result alphabetically. For `min_amount=2000` expected output: `['Boris']` (only Boris has an order for 3200). For `min_amount=800` expected output: `['Anya', 'Boris']`.

### Task 5
Write a function `best_order_each()` that, for every user with orders, computes the amount of their most expensive order. Do it with a correlated subquery (or a CTE with the ROW_NUMBER window function). Return a list of tuples `(name, best)` in name order. Expected output: `[('Anya', 1500.0), ('Boris', 3200.0)]`. Vera is absent from the list — she has no orders.

### Task 6
Write a function `revenue_share()` that works with the same `users`/`orders` schema as in the lesson and returns a list of tuples `(name, total, pct, place)`. `total` is the user's order total, `pct` is their share of total revenue in percent, rounded to one decimal place (`ROUND(..., 1)`), `place` is their rank by total. Compute the share with the window sum `SUM(SUM(orders.amount)) OVER ()` or a subquery `(SELECT SUM(amount) FROM orders)`, and the rank with `RANK() OVER (ORDER BY SUM(orders.amount) DESC)`. Do not include users without orders. Expected output: `[('Boris', 4100.0, 64.1, 1), ('Anya', 2300.0, 35.9, 2)]`.

### Task 7
Create three tables: `users(id, name)`, `orders(id, user_id)` and `order_items(order_id, product_id, qty, price)`. Fill them with data: Anya has orders 101 (two line items: 2 × 500 and 1 × 800) and 102 (1 × 500), Boris has order 103 (1 × 3200), Vera has no orders. Write a function `order_totals()` that joins the three tables in one query, counts the number of line items and the order total as `SUM(qty * price)`, keeps only orders more expensive than 1000 via `HAVING`, and sorts by total descending. Return a list of tuples `(order_id, name, items_count, total)`. Expected output: `[(103, 'Boris', 1, 3200.0), (101, 'Anya', 2, 1800.0)]` — order 102 for 500 does not make it into the result.

<!--/TASK-->

<!--HINT-->
### Hint 1
The function should create and fill the database itself: run the `CREATE TABLE` and `INSERT` statements from the lesson, then `conn.commit()`. Use `SUM(orders.amount)` for the total, `JOIN orders ON orders.user_id = users.id` for the join, and `GROUP BY users.id` for grouping. Sort descending with `ORDER BY total DESC`.

### Hint 2
The difference from Task 1 is the join type: use `LEFT JOIN`. Vera will appear in the result with a NULL total, so wrap SUM in `COALESCE(SUM(orders.amount), 0)`. Sort by name: `ORDER BY users.name`. Check that all non-aggregate columns in SELECT are listed in GROUP BY.

### Hint 3
First build the query with JOIN, GROUP BY and `SUM(orders.amount)`, then add `HAVING SUM(orders.amount) > ?` with the `threshold` parameter. Remember: WHERE won't work here, because it filters rows before grouping, and we need to filter groups.

### Hint 4
The subquery in parentheses should return `user_id` from the orders table where `amount >= ?`. The outer query: `SELECT name FROM users WHERE id IN (...) ORDER BY name`. Pass `min_amount` as a parameter via a tuple.

### Hint 5
Correlated variant: `SELECT users.name, (SELECT MAX(o.amount) FROM orders o WHERE o.user_id = users.id) AS best FROM users` — add a condition so users without orders are not shown (for example, `WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = users.id)`). CTE variant: `WITH ranked AS (SELECT user_id, amount, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn FROM orders) SELECT users.name, ranked.amount FROM users JOIN ranked ON ranked.user_id = users.id WHERE ranked.rn = 1 ORDER BY users.name`.

### Hint 6
A window function is computed after GROUP BY, so you can use an aggregate inside it: `RANK() OVER (ORDER BY SUM(orders.amount) DESC)`. For the share you need the grand total: `SUM(SUM(orders.amount)) OVER ()` — the outer SUM collects the group sums, and empty parentheses mean "over the whole result". Don't forget to multiply by `100.0` before dividing, otherwise SQLite will do integer division and return zeros.

### Hint 7
Join along the chain: `orders JOIN users ON users.id = orders.user_id JOIN order_items ON order_items.order_id = orders.id`. A line item total is `qty * price`, and the order total is `SUM(order_items.qty * order_items.price)`. Group by `orders.id`, and put the amount filter in `HAVING`, not `WHERE`: in WHERE the aggregate has not been computed yet. The number of line items is `COUNT(order_items.product_id)`.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import sqlite3

def top_spenders():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, SUM(orders.amount) AS total
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY total DESC
    """)
    return cur.fetchall()

print(top_spenders())
```

Result:

```
[('Boris', 4100.0), ('Anya', 2300.0)]
```

What's happening here? INNER JOIN joins the rows of users and orders on the match `orders.user_id = users.id`. Since Vera has no orders, her rows simply never appear in the join — this is what distinguishes INNER JOIN from LEFT JOIN. GROUP BY users.id collects each user's orders into one group, and SUM adds up their amounts. ORDER BY total DESC sorts the groups from the largest total to the smallest. Note: `total` is an alias for the expression, and you can use it in ORDER BY. The expected outcome: Boris leads with 4100, Anya follows.

### Solution 2
Solution:

```python
import sqlite3

def left_join_report():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, COALESCE(SUM(orders.amount), 0) AS total
    FROM users
    LEFT JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY users.name
    """)
    return cur.fetchall()

print(left_join_report())
```

Result:

```
[('Anya', 2300.0), ('Boris', 4100.0), ('Vera', 0.0)]
```

What's happening here? LEFT JOIN guarantees that every row of the left table users makes it into the result. Vera has no orders, so the values from orders become NULL: SUM(NULL) gives NULL, and that is exactly why COALESCE(..., 0) is needed — it replaces NULL with 0. This way the report shows all users, even those who never ordered anything. Sorting by name gives the order Anya → Boris → Vera. Remember the difference: INNER JOIN — only matches, LEFT JOIN — the whole left table plus matches on the right.

### Solution 3
Solution:

```python
import sqlite3

def heavy_users(threshold):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name, SUM(orders.amount) AS total
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    HAVING SUM(orders.amount) > ?
    """, (threshold,))
    return cur.fetchall()

print(heavy_users(2000))
print(heavy_users(3000))
```

Result:

```
[('Anya', 2300.0), ('Boris', 4100.0)]
[('Boris', 4100.0)]
```

What's happening here? The SQL execution order: first FROM/JOIN collect the rows, WHERE (if present) filters them, GROUP BY groups, then aggregate functions are applied, and only after that HAVING cuts off the groups that don't pass the condition. So `HAVING SUM(orders.amount) > ?` sees the already-computed group sums. At threshold 2000, Anya (2300) and Boris (4100) pass; at threshold 3000 — only Boris. A good practical touch: the threshold is passed as a parameter rather than hardcoded into the query string.

### Solution 4
Solution:

```python
import sqlite3

def who_ordered_over(min_amount):
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT name FROM users
    WHERE id IN (
        SELECT user_id FROM orders
        WHERE amount >= ?
    )
    ORDER BY name
    """, (min_amount,))
    return [row[0] for row in cur.fetchall()]

print(who_ordered_over(2000))
print(who_ordered_over(800))
```

Result:

```
['Boris']
['Anya', 'Boris']
```

What's happening here? The inner query returns the set of `user_id` values of orders whose amount is at least min_amount. The outer query takes the users whose id is in that set. At threshold 2000, the only qualifying order is Boris's 3200. At 800, orders 1500 (Anya), 3200 and 900 (Boris) qualify — but not Anya's 800, because the condition is `amount >= 800` — wait, 800 >= 800 is true, so the 800 order qualifies too, and Anya is in both lists. Note: the subquery runs once; IN does not become a loop — this is an ordinary independent subquery, not a correlated one.

### Solution 5
Solution via a correlated subquery:

```python
import sqlite3

def best_order_each():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name,
           (SELECT MAX(o.amount) FROM orders o
            WHERE o.user_id = users.id) AS best
    FROM users
    WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = users.id)
    ORDER BY users.name
    """)
    return cur.fetchall()

print(best_order_each())
```

Result:

```
[('Anya', 1500.0), ('Boris', 3200.0)]
```

What's happening here? The subquery in SELECT is correlated: for each users row it is recomputed and references the outer query's `users.id`. It picks the maximum order amount for exactly that user. The EXISTS condition filters out users without orders — otherwise Vera would appear in the result with NULL. The alternative via CTE and a window function: `WITH ranked AS (SELECT user_id, amount, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) AS rn FROM orders) SELECT users.name, ranked.amount FROM users JOIN ranked ON ranked.user_id = users.id WHERE ranked.rn = 1 ORDER BY users.name` — same result, but without re-running the subquery for every row.

### Solution 6
Solution:

```python
import sqlite3

def revenue_share():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id, amount) VALUES
        (101, 1, 1500), (102, 1, 800),
        (103, 2, 3200), (104, 2, 900);
    """)
    conn.commit()
    cur.execute("""
    SELECT users.name,
           SUM(orders.amount) AS total,
           ROUND(100.0 * SUM(orders.amount)
                 / SUM(SUM(orders.amount)) OVER (), 1) AS pct,
           RANK() OVER (ORDER BY SUM(orders.amount) DESC) AS place
    FROM users
    JOIN orders ON orders.user_id = users.id
    GROUP BY users.id
    ORDER BY total DESC
    """)
    return cur.fetchall()

print(revenue_share())
```

Result:

```
[('Boris', 4100.0, 64.1, 1), ('Anya', 2300.0, 35.9, 2)]
```

What's happening here? The query first groups orders by user and computes `SUM(orders.amount)` — this is plain aggregation. Then window functions kick in, working on top of the ready-made groups: `SUM(SUM(orders.amount)) OVER ()` takes the group sums 4100 and 2300 and adds them into the grand total 6400, without collapsing the rows themselves. `RANK() OVER (ORDER BY SUM(orders.amount) DESC)` numbers the groups by descending total, and with equal values both would get the same rank and the next number would be skipped. Multiplying by `100.0` is essential: with integer `100`, SQLite would do integer division and return zeros. `ROUND(..., 1)` leaves one decimal place, and the two shares add up to exactly 100%.

### Solution 7
Solution:

```python
import sqlite3

def order_totals():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL);
    CREATE TABLE order_items (
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        price REAL NOT NULL
    );
    INSERT INTO users (id, name) VALUES
        (1, 'Anya'), (2, 'Boris'), (3, 'Vera');
    INSERT INTO orders (id, user_id) VALUES
        (101, 1), (102, 1), (103, 2);
    INSERT INTO order_items (order_id, product_id, qty, price) VALUES
        (101, 10, 2, 500), (101, 20, 1, 800),
        (102, 10, 1, 500),
        (103, 30, 1, 3200);
    """)
    conn.commit()
    cur.execute("""
    SELECT orders.id, users.name,
           COUNT(order_items.product_id) AS items_count,
           SUM(order_items.qty * order_items.price) AS total
    FROM orders
    JOIN users ON users.id = orders.user_id
    JOIN order_items ON order_items.order_id = orders.id
    GROUP BY orders.id
    HAVING SUM(order_items.qty * order_items.price) > 1000
    ORDER BY total DESC
    """)
    return cur.fetchall()

print(order_totals())
```

Result:

```
[(103, 'Boris', 1, 3200.0), (101, 'Anya', 2, 1800.0)]
```

What's happening here? The query follows the chain of relationships: `orders` joins `users` by owner and `order_items` by order id. As a result, each line item becomes a separate row, but `GROUP BY orders.id` gathers them back into one order. The total is computed not from a ready-made column but from the expression `qty * price`: the two line items of order 101 give 1000 + 800 = 1800, order 102 is only 500 and is cut off by the `HAVING` condition. `COUNT` counts the number of line items, and for order 101 that's 2. Order 103 with a single 3200 line item tops the list. Note: `JOIN order_items` is an inner join, so an order without line items would not make it into the report; if you need those, you'd use `LEFT JOIN` and `COALESCE` for the total.

<!--/SOLUTION-->

<!--QUIZ-->
What will INNER JOIN return for a user who has no records in the right table?
- A row with NULL values on the right
- Nothing: this user will not appear in the result
- A join error
- A separate row with empty values
* Correct answer: Nothing: this user will not appear in the result
INNER JOIN keeps only matching pairs of rows; a user without orders is simply absent from the result.

How is LEFT JOIN different from INNER JOIN?
- LEFT JOIN works with only one table
- LEFT JOIN keeps all rows of the left table, inserting NULL where there are no matches
- INNER JOIN is always faster
- LEFT JOIN does not support GROUP BY
* Correct answer: LEFT JOIN keeps all rows of the left table, inserting NULL where there are no matches
LEFT JOIN includes all rows of the left table in the result, even if there are no matches on the right — NULL is inserted instead of data.

Why can't group sums be filtered with WHERE?
- WHERE cannot work with SUM
- WHERE runs before GROUP BY and does not see aggregate results
- WHERE runs after GROUP BY, but only for one group
- WHERE is forbidden in queries with JOIN
* Correct answer: WHERE runs before GROUP BY and does not see aggregate results
WHERE filters raw rows before grouping; aggregate results are available only in HAVING.

What will the subquery `(SELECT MAX(amount) FROM orders WHERE user_id = users.id)` inside SELECT return?
- The user's number of orders
- The maximum order amount for each row of the outer query
- A list of all amounts
- The user's first order
* Correct answer: The maximum order amount for each row of the outer query
This is a correlated subquery: it is computed for each row of the outer query and returns that user's maximum order amount.

What is a CTE (WITH)?
- A temporary named table inside a query that makes it readable
- A type of index
- A way to merge two databases
- A command to restart the server
* Correct answer: A temporary named table inside a query that makes it readable
A CTE is declared with WITH and then used like a regular table, simplifying complex queries.

Where does HAVING run relative to GROUP BY?
- Before GROUP BY
- After GROUP BY
- Instead of GROUP BY
- HAVING is not related to GROUP BY
* Correct answer: After GROUP BY
First the rows are grouped, then aggregate functions are computed, and only after that HAVING filters out groups.

Which aggregate function counts rows or non-NULL values?
- COUNT
- SUM
- AVG
* Correct answer: COUNT
COUNT(*) counts rows, COUNT(column) counts only non-NULL values.

What does COALESCE(x, 0) do?
- Returns x if it is not NULL, otherwise 0
- Adds x and 0
- Checks that x is greater than zero
* Correct answer: Returns x if it is not NULL, otherwise 0
COALESCE replaces NULL with the first non-NULL value from its argument list.

What does RANK() OVER (ORDER BY total DESC) do?
- Assigns rows a rank by descending total, without collapsing the result
- Physically sorts the table
- Sums the total values
- Removes duplicates
* Correct answer: Assigns rows a rank by descending total, without collapsing the result
A window function adds a column to rows rather than changing their count.

What does SUM(SUM(amount)) OVER () give in a query with GROUP BY?
- The grand total across all groups next to each row
- The sum within each group
- The average across groups
* Correct answer: The grand total across all groups next to each row
The inner SUM computes the group, the outer one with an empty OVER sums all groups.

What does COUNT(DISTINCT orders.id) count?
- The number of unique order ids; NULL is not counted
- The number of all rows, including duplicates
- The sum of order ids
* Correct answer: The number of unique order ids; NULL is not counted
DISTINCT removes repeats, and COUNT over a column ignores NULL.

What happens if the right side of a LEFT JOIN has several matches?
- The left row is repeated as many times as there are matches on the right
- Only the first match is returned
- The query fails with an error
* Correct answer: The left row is repeated as many times as there are matches on the right
That's why it's easy to double-count sums over such a result — you need aggregation or a separate subquery.
<!--/QUIZ-->
