---
title: Exam: Big Data and Distributed Computing
summary: Final assessment for the "Big Data and Distributed Computing" module: Polars, Dask, Ray, out-of-core, Parquet/S3, streaming.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, polars, dask, ray, pyarrow, parquet, s3, streaming
---

<!--QUIZ-->
Which Polars method runs the execution of a lazy plan?
- collect()
- run()
- execute()
* Correct answer: collect()
scan_* build a LazyFrame, and collect() executes the plan.

What does with_columns do in Polars?
- Adds new columns via expressions
- Removes columns
- Renames columns
* Correct answer: Adds new columns via expressions
with_columns returns a new DataFrame with the added columns.

What is a partition in Dask?
- A small pandas DataFrame, part of a large dataset
- A separate file with settings
- A Python module
* Correct answer: A small pandas DataFrame, part of a large dataset
Dask cuts data into partitions and processes them in parallel.

What will ddf.groupby("city")["sum"].sum() return without compute()?
- A lazy Dask object
- A number
- A pandas Series
* Correct answer: A lazy Dask object
All Dask operations are lazy until compute() is called.

What does @ray.remote do to a function?
- Turns it into a remote task
- Speeds up its execution
- Adds logging
* Correct answer: Turns it into a remote task
The call returns an ObjectRef; the value is obtained via ray.get().

What is an actor in Ray?
- A remote object with state and methods
- A stateless function
- A thread pool
* Correct answer: A remote object with state and methods
An actor holds state and serializes method calls.

What is out-of-core processing?
- Reading and processing data in pieces without fitting it all into memory
- Processing on GPU
- Data compression
* Correct answer: Reading and processing data in pieces without fitting it all into memory
Data is read in blocks, and the result is accumulated.

Which ParquetFile method reads data in batches?
- iter_batches
- read_table
- read_all
* Correct answer: iter_batches
iter_batches returns a generator of RecordBatches.

What allows filtering partitioned data without reading all files?
- Pushdown filters over paths and statistics
- File compression
- In-memory indexes
* Correct answer: Pushdown filters over paths and statistics
The filter condition is pushed down into paths and row groups.

What is a topic in Kafka?
- A named stream of messages
- A broker server
- A message format
* Correct answer: A named stream of messages
A topic is a message queue read by consumers.
<!--/QUIZ-->
