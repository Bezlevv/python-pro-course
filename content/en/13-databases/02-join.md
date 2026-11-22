---
title: JOIN: inner and outer
summary: INNER JOIN, LEFT JOIN, keys.
order: 2
duration: 45 min
difficulty: advanced
tags: sql, join, relations
---

Joins combine data from several tables.

## Inner join

```sql
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

## Left join

```sql
SELECT c.name, o.id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;
```

## Keys

- Primary key: unique row ID;
- Foreign key: reference to another table.

## Lesson summary

JOIN links tables by keys; LEFT keeps left rows.

<!--TASK-->
### Task 1 — Inner
Join orders with customers.

### Task 2 — Left
Show all customers, even without orders.

### Task 3 — Alias
Use table aliases.

### Task 4 — ON
Explain the ON condition.

### Task 5 — Three tables
Join orders, customers, products.

### Task 6 — Count
Count orders per customer.

### Task 7 — Right idea
Explain RIGHT JOIN.
<!--/TASK-->

<!--HINT-->
### Hint 1
INNER JOIN.

### Hint 2
LEFT JOIN.

### Hint 3
o, c.

### Hint 4
Keys.

### Hint 5
Two joins.

### Hint 6
GROUP BY.

### Hint 7
Mirror.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```sql
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

### Solution 2
```sql
SELECT c.name, o.id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id;
```

### Solution 3
```sql
SELECT o.id, c.name
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.id;
```

### Solution 4
```sql
-- ON — условие связи: внешний ключ = первичный ключ
```

### Solution 5
```sql
SELECT o.id, c.name, p.title
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;
```

### Solution 6
```sql
SELECT c.name, COUNT(o.id) AS orders_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;
```

### Solution 7
```sql
-- RIGHT JOIN: как LEFT, но сохраняет правую таблицу
-- на практике чаще используют LEFT
```
<!--/SOLUTION-->

<!--QUIZ-->
What does JOIN do?
- Combines tables
- Deletes
- Sorts
- None
* Correct answer: Combines tables
By key.

What is INNER JOIN?
- Matching rows only
- All left
- All rows
- None
* Correct answer: Matching rows only
Intersection.

What is LEFT JOIN?
- Keeps all left
- Keeps right
- Only matches
- None
* Correct answer: Keeps all left
NULL fills.

What is a primary key?
- Unique row ID
- A reference
- A column
- None
* Correct answer: Unique row ID
id.

What is a foreign key?
- Reference to other
- Unique
- Empty
- None
* Correct answer: Reference to other
customer_id.

What is ON?
- Join condition
- A table
- A row
- None
* Correct answer: Join condition
Match.

What is an alias?
- Short name
- A key
- A join
- None
* Correct answer: Short name
o, c.

What is NULL in LEFT?
- No match
- Error
- Zero
- None
* Correct answer: No match
Missing.

What is GROUP BY?
- Groups rows
- Sorts
- Filters
- None
* Correct answer: Groups rows
Aggregation.

What is COUNT?
- Counts rows
- Sums
- Averages
- None
* Correct answer: Counts rows
Aggregate.

What is a many-to-one relation?
- Orders → customer
- Customer → many
- Both
- None
* Correct answer: Orders → customer
Fk.

What is a cartesian product?
- Without ON
- With ON
- Error
- None
* Correct answer: Without ON
All pairs.
<!--/QUIZ-->
