---
title: Dask: parallel pandas
summary: DataFrames that scale out.
order: 2
duration: 45 min
difficulty: advanced
tags: dask
---

Dask extends pandas beyond one machine.

## Install and use

```python
import dask.dataframe as dd

df = dd.read_csv("big/*.csv")
print(df.head())
result = df.groupby("category")["value"].mean().compute()
```

## Lazy

Operations build a plan; compute() runs it.

## Lesson summary

Dask = pandas API + parallelism.

<!--TASK-->
### Task 1 — Read
Read many CSVs.

### Task 2 — Head
Show head.

### Task 3 — Group
Group and mean.

### Task 4 — Compute
Run compute().

### Task 5 — Lazy
Explain lazy evaluation.

### Task 6 — Partitions
Explain partitions.

### Task 7 — When
When use Dask?
<!--/TASK-->

<!--HINT-->
### Hint 1
dd.read_csv.

### Hint 2
head().

### Hint 3
groupby.

### Hint 4
compute().

### Hint 5
Deferred.

### Hint 6
Chunks.

### Hint 7
Big.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import dask.dataframe as dd
df = dd.read_csv("big/*.csv")
```

### Solution 2
```python
print(df.head())
```

### Solution 3
```python
result = df.groupby("category")["value"].mean()
```

### Solution 4
```python
print(result.compute())
```

### Solution 5
```text
Dask строит граф операций заранее;
выполняет их только при compute()
```

### Solution 6
```text
Данные делятся на партиции — куски,
которые обрабатываются параллельно
```

### Solution 7
```text
Когда данные не помещаются в память или
обработка слишком долгая для pandas
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Dask?
- Parallel computing
- Database
- Browser
- None
* Correct answer: Parallel computing
pandas-like.

What is dd?
- Dask DataFrame
- pandas
- Spark
- None
* Correct answer: Dask DataFrame
Alias.

What is lazy?
- Deferred
- Immediate
- Eager
- None
* Correct answer: Deferred
Plan.

What is compute?
- Runs plan
- Plans
- Reads
- None
* Correct answer: Runs plan
Result.

What is a partition?
- Chunk
- Full data
- Column
- None
* Correct answer: Chunk
Parallel.

What is read_csv?
- Loads files
- Writes
- Groups
- None
* Correct answer: Loads files
Multiple.

What is groupby?
- Groups
- Sorts
- Filters
- None
* Correct answer: Groups
Aggregate.

What is the graph?
- Operation plan
- Data
- Result
- None
* Correct answer: Operation plan
DAG.

What is parallelism?
- Simultaneous
- Sequential
- One
- None
* Correct answer: Simultaneous
Cores.

What is out-of-core?
- Disk-backed
- Memory-only
- Small
- None
* Correct answer: Disk-backed
Scale.

What is the benefit?
- Bigger data
- Faster always
- Required
- None
* Correct answer: Bigger data
pandas API.

What is a scheduler?
- Runs tasks
- Stores data
- Reads
- None
* Correct answer: Runs tasks
Threads.
<!--/QUIZ-->
