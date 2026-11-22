---
title: Indexes and query performance
summary: CREATE INDEX, EXPLAIN, covering indexes.
order: 4
duration: 40 min
difficulty: advanced
tags: sql, index, explain
---

Indexes speed up lookups.

## Create index

```sql
CREATE INDEX idx_products_price ON products(price);
```

## EXPLAIN

```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE price > 100;
```

## Trade-off

Indexes speed reads but slow writes.

## Lesson summary

Index hot columns; check plans with EXPLAIN.

<!--TASK-->
### Task 1 — Index
Create an index on price.

### Task 2 — Explain
Explain a query plan.

### Task 3 — Composite
Index (category, price).

### Task 4 — Trade-off
Describe read/write cost.

### Task 5 — When not
When not to index?

### Task 6 — Unique
Create a unique index.

### Task 7 — Check
List existing indexes.
<!--/TASK-->

<!--HINT-->
### Hint 1
CREATE INDEX.

### Hint 2
EXPLAIN.

### Hint 3
Composite.

### Hint 4
Writes.

### Hint 5
Small tables.

### Hint 6
UNIQUE.

### Hint 7
PRAGMA / pg_indexes.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```sql
CREATE INDEX idx_products_price ON products(price);
```

### Solution 2
```sql
EXPLAIN ANALYZE SELECT * FROM products WHERE price > 100;
```

### Solution 3
```sql
CREATE INDEX idx_products_cat_price ON products(category, price);
```

### Solution 4
```sql
-- Чтение ускоряется, вставка/обновление замедляются
-- (индекс надо поддерживать)
```

### Solution 5
```sql
-- На маленьких таблицах или при редких запросах
-- индекс не оправдан
```

### Solution 6
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

### Solution 7
```sql
-- PostgreSQL: SELECT * FROM pg_indexes WHERE tablename = 'products';
-- SQLite: PRAGMA index_list('products');
```
<!--/SOLUTION-->

<!--QUIZ-->
What is an index?
- Lookup accelerator
- A table
- A query
- None
* Correct answer: Lookup accelerator
B-tree.

What does CREATE INDEX do?
- Adds index
- Drops
- Sorts
- None
* Correct answer: Adds index
Fast.

What is EXPLAIN?
- Shows plan
- Runs
- Deletes
- None
* Correct answer: Shows plan
Analyze.

What is a composite index?
- Multiple columns
- One column
- A table
- None
* Correct answer: Multiple columns
(category, price).

What is the trade-off?
- Reads vs writes
- Speed only
- Space only
- None
* Correct answer: Reads vs writes
Balance.

Do indexes slow writes?
- Yes
- No
- Never
- None
* Correct answer: Yes
Maintenance.

What is a unique index?
- Enforces uniqueness
- Allows dupes
- Faster
- None
* Correct answer: Enforces uniqueness
Constraint.

When skip an index?
- Small table
- Huge reads
- Always
- None
* Correct answer: Small table
Not worth.

What is the primary key index?
- Automatic
- Manual
- Optional
- None
* Correct answer: Automatic
Created.

What is a bitmap/seq scan?
- Full table read
- Index read
- Error
- None
* Correct answer: Full table read
Slow.

What is the benefit?
- Fast lookups
- Small size
- Required
- None
* Correct answer: Fast lookups
Search.

What is pg_indexes?
- Index metadata
- Data
- Queries
- None
* Correct answer: Index metadata
Postgres.
<!--/QUIZ-->
