---
title: PySpark basics
summary: SparkSession, RDD, DataFrames.
order: 3
duration: 50 min
difficulty: advanced
tags: pyspark
---

PySpark brings Spark to Python.

## Session

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("demo").getOrCreate()
```

## DataFrame

```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.show(5)
df.printSchema()
```

## Operations

```python
from pyspark.sql.functions import avg

result = df.groupBy("category").agg(avg("value"))
result.show()
```

## Data summary

SparkSession → DataFrame → operations.

<!--TASK-->
### Task 1 — Session
Create SparkSession.

### Task 2 — Read
Read CSV.

### Task 3 — Show
Show rows.

### Task 4 — Schema
Print schema.

### Task 5 — Group
Group and average.

### Task 6 — Filter
Filter rows.

### Task 7 — Write
Write results as Parquet.
<!--/TASK-->

<!--HINT-->
### Hint 1
SparkSession.

### Hint 2
read.csv.

### Hint 3
show().

### Hint 4
printSchema().

### Hint 5
groupBy.

### Hint 6
filter.

### Hint 7
write.parquet.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("demo").getOrCreate()
```

### Solution 2
```python
df = spark.read.csv("data.csv", header=True, inferSchema=True)
```

### Solution 3
```python
df.show(5)
```

### Solution 4
```python
df.printSchema()
```

### Solution 5
```python
from pyspark.sql.functions import avg
df.groupBy("category").agg(avg("value")).show()
```

### Solution 6
```python
df.filter(df["value"] > 100).show()
```

### Solution 7
```python
df.write.parquet("out/")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Spark?
- Cluster engine
- Database
- Browser
- None
* Correct answer: Cluster engine
Distributed.

What is PySpark?
- Python API
- A library
- Database
- None
* Correct answer: Python API
Spark.

What is SparkSession?
- Entry point
- Data
- Job
- None
* Correct answer: Entry point
Builder.

What is a DataFrame?
- Distributed table
- Local
- RDD only
- None
* Correct answer: Distributed table
Columns.

What is show?
- Prints rows
- Saves
- Reads
- None
* Correct answer: Prints rows
Preview.

What is schema?
- Types
- Data
- Size
- None
* Correct answer: Types
printSchema.

What is groupBy?
- Groups
- Filters
- Sorts
- None
* Correct answer: Groups
agg.

What is agg?
- Aggregates
- Reads
- Writes
- None
* Correct answer: Aggregates
avg.

What is filter?
- Condition
- Group
- Sort
- None
* Correct answer: Condition
Where.

What is parquet?
- Columnar format
- CSV
- JSON
- None
* Correct answer: Columnar format
Fast.

What is a cluster?
- Machines
- One server
- File
- None
* Correct answer: Machines
Distributed.

What is lazy?
- Deferred
- Immediate
- Eager
- None
* Correct answer: Deferred
Actions.
<!--/QUIZ-->
