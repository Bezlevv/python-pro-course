---
title: SQL basics: SELECT, WHERE, ORDER BY
summary: Querying, filtering, sorting data.
order: 1
duration: 45 min
difficulty: intermediate
tags: sql, select, where
---

SQL extracts and shapes data.

## SELECT

```sql
SELECT name, price FROM products;
```

## WHERE

```sql
SELECT * FROM products WHERE price > 100;
```

## ORDER BY

```sql
SELECT * FROM products ORDER BY price DESC;
```

## Limit

```sql
SELECT * FROM products LIMIT 10;
```

## Lesson summary

SELECT + WHERE + ORDER BY cover most queries.

<!--TASK-->
### Task 1 — Select
Select two columns.

### Task 2 — Where
Filter price > 50.

### Task 3 — Order
Sort by name ascending.

### Task 4 — Limit
Take 5 rows.

### Task 5 — Combine
Filter + sort + limit in one query.

### Task 6 — Operators
Use BETWEEN and IN.

### Task 7 — Alias
Use AS alias.
<!--/TASK-->

<!--HINT-->
### Hint 1
SELECT name, price.

### Hint 2
WHERE price > 50.

### Hint 3
ORDER BY name.

### Hint 4
LIMIT 5.

### Hint 5
All together.

### Hint 6
BETWEEN, IN.

### Hint 7
AS p.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```sql
SELECT name, price FROM products;
```

### Solution 2
```sql
SELECT * FROM products WHERE price > 50;
```

### Solution 3
```sql
SELECT * FROM products ORDER BY name ASC;
```

### Solution 4
```sql
SELECT * FROM products LIMIT 5;
```

### Solution 5
```sql
SELECT * FROM products
WHERE price > 50
ORDER BY price DESC
LIMIT 5;
```

### Solution 6
```sql
SELECT * FROM products WHERE price BETWEEN 10 AND 100;
SELECT * FROM products WHERE category IN ('books', 'games');
```

### Solution 7
```sql
SELECT price * 0.9 AS discounted FROM products;
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQL?
- Query language
- A Python module
- A database
- None
* Correct answer: Query language
Standard.

What does SELECT do?
- Fetches columns
- Deletes
- Inserts
- None
* Correct answer: Fetches columns
Read.

What does WHERE do?
- Filters rows
- Sorts
- Groups
- None
* Correct answer: Filters rows
Condition.

What does ORDER BY do?
- Sorts
- Filters
- Limits
- None
* Correct answer: Sorts
ASC/DESC.

What does LIMIT do?
- Caps rows
- Sorts
- Joins
- None
* Correct answer: Caps rows
Pagination.

What is *?
- All columns
- All rows
- Table
- None
* Correct answer: All columns
Select.

What is BETWEEN?
- Inclusive range
- Equal
- Like
- None
* Correct answer: Inclusive range
Numbers.

What is IN?
- Set membership
- Range
- Sort
- None
* Correct answer: Set membership
List.

What is AS?
- Alias
- Sort
- Filter
- None
* Correct answer: Alias
Column name.

What is DESC?
- Descending
- Ascending
- Delete
- None
* Correct answer: Descending
Newest first.

What is ASC?
- Ascending
- Descending
- Add
- None
* Correct answer: Ascending
A→Z.

What is a row?
- One record
- A column
- A table
- None
* Correct answer: One record
Tuple.
<!--/QUIZ-->
