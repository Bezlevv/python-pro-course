---
title: Exam: Databases: Deep Dive
summary: Test your knowledge of SQL joins and aggregations, normalization, indexes, transactions and ACID, ORM, SQL injection and Redis.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Which JOIN will return a user without orders if they are on the left and orders are on the right?
- INNER JOIN
- LEFT JOIN
- CROSS JOIN
- None
* Correct answer: LEFT JOIN
LEFT JOIN keeps all rows of the left table, inserting NULL where there are no matches on the right.

How is HAVING different from WHERE?
- HAVING filters rows before grouping, WHERE — after
- HAVING filters groups after aggregation, WHERE — rows before it
- They are complete synonyms
- HAVING works only with JOIN
* Correct answer: HAVING filters groups after aggregation, WHERE — rows before it
WHERE doesn't see aggregate results; HAVING is needed for that.

Which violation does 3NF eliminate?
- Partial dependency on the composite key
- Transitive dependency of columns on each other
- Missing primary key
- Storing non-atomic values
* Correct answer: Transitive dependency of columns on each other
3NF requires 2NF and the absence of dependencies of the form "a column depends on another non-key column".

What does an index speed up in a database?
- Writing data
- Finding rows by a column without a full scan
- Creating tables
- Backups
* Correct answer: Finding rows by a column without a full scan
An index (usually a B-tree) shortens the path to the needed rows; writes slow down in the process.

Which ACID letter is responsible for a transaction either applying entirely or rolling back?
- A (Atomicity)
- C (Consistency)
- I (Isolation)
- D (Durability)
* Correct answer: A (Atomicity)
Atomicity: "all or nothing" — partial success is impossible.

Which isolation level completely eliminates dirty reads, non-repeatable reads and phantoms?
- READ UNCOMMITTED
- READ COMMITTED
- REPEATABLE READ
- SERIALIZABLE
* Correct answer: SERIALIZABLE
SERIALIZABLE is the strictest: transactions run as if they were one after another.

What does ROLLBACK TO sp1 do inside a transaction?
- Rolls back the whole transaction
- Rolls back the changes made after savepoint sp1
- Deletes all tables
- Ends the connection
* Correct answer: Rolls back the changes made after savepoint sp1
A savepoint is a rollback point; ROLLBACK TO returns the database to it without ending the transaction.

What is the cause of the N+1 problem in an ORM?
- The database duplicates data
- First N objects are loaded, then one more query runs for each to fetch related data
- Indexes are not used
- Queries run in parallel
* Correct answer: First N objects are loaded, then one more query runs for each to fetch related data
Lazy relationship loading produces 1 + N queries; it is solved with eager loading (selectinload, select_related).

Which defense against SQL injection is the main one?
- Removing extra spaces
- Parameterized queries (placeholders)
- Blacklisting SQL words
- Encrypting the database
* Correct answer: Parameterized queries (placeholders)
Values are sent separately from the query text and never become code.

What does the command SETEX key 300 value do in Redis?
- Reads the key's value
- Writes a value with a lifetime of 300 seconds
- Increases the value by 300
- Creates a list of 300 elements
* Correct answer: Writes a value with a lifetime of 300 seconds
SETEX is an atomic combination of SET and EXPIRE, the standard way to put data into a cache with a TTL.
<!--/QUIZ-->
