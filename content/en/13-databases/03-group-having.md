---
title: Grouping and aggregation
summary: GROUP BY, HAVING, aggregates.
order: 3
duration: 45 min
difficulty: advanced
tags: sql, group by, having
---

Aggregates summarize many rows into few.

## Aggregates

```sql
SELECT COUNT(*), AVG(price), MAX(price), MIN(price)
FROM products;
```

## GROUP BY

```sql
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category;
```

## HAVING

```sql
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50;
```

## Lesson summary

GROUP BY collapses rows; HAVING filters groups.

<!--TASK-->
### Task 1 — Count
Count all products.

### Task 2 — Group
Count per category.

### Task 3 — Average
Average price per category.

### Task 4 — Having
Show categories with avg > 50.

### Task 5 — Sum
Total stock per category.

### Task 6 — Min/max
Find cheapest and dearest.

### Task 7 — Where vs having
Explain the difference.
<!--/TASK-->

<!--HINT-->
### Hint 1
COUNT(*).

### Hint 2
GROUP BY category.

### Hint 3
AVG(price).

### Hint 4
HAVING.

### Hint 5
SUM(stock).

### Hint 6
MIN/MAX.

### Hint 7
Rows vs groups.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```sql
SELECT COUNT(*) FROM products;
```

### Solution 2
```sql
SELECT category, COUNT(*) AS cnt
FROM products
GROUP BY category;
```

### Solution 3
```sql
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category;
```

### Solution 4
```sql
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category
HAVING AVG(price) > 50;
```

### Solution 5
```sql
SELECT category, SUM(stock) AS total
FROM products
GROUP BY category;
```

### Solution 6
```sql
SELECT MIN(price), MAX(price) FROM products;
```

### Solution 7
```sql
-- WHERE: фильтрует строки ДО группировки
-- HAVING: фильтрует группы ПОСЛЕ
```
<!--/SOLUTION-->

<!--QUIZ-->
What is COUNT?
- Counts rows
- Sums
- Averages
- None
* Correct answer: Counts rows
Aggregate.

What is AVG?
- Average
- Count
- Max
- None
* Correct answer: Average
Mean.

What is SUM?
- Total
- Count
- Sort
- None
* Correct answer: Total
Addition.

What is MAX?
- Largest
- Smallest
- Average
- None
* Correct answer: Largest
Max value.

What is MIN?
- Smallest
- Largest
- Count
- None
* Correct answer: Smallest
Min value.

What is GROUP BY?
- Groups rows
- Sorts
- Filters
- None
* Correct answer: Groups rows
Category.

What is HAVING?
- Filters groups
- Filters rows
- Sorts
- None
* Correct answer: Filters groups
After.

What is WHERE?
- Filters rows
- Filters groups
- Groups
- None
* Correct answer: Filters rows
Before.

Can we use WHERE with COUNT?
- No
- Yes
- Always
- None
* Correct answer: No
HAVING.

What is an aggregate?
- Summary value
- A row
- A column
- None
* Correct answer: Summary value
Function.

What does GROUP BY produce?
- One row per group
- All rows
- One row
- None
* Correct answer: One row per group
Collapse.

What is cnt?
- Alias for count
- A column
- A table
- None
* Correct answer: Alias for count
AS.
<!--/QUIZ-->
