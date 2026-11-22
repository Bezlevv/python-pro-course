---
title: Big Data basics
summary: What it is, the 3 V's, tools.
order: 1
duration: 40 min
difficulty: intermediate
tags: bigdata
---

Big Data exceeds one machine's comfort.

## 3 V's

- Volume: huge size;
- Velocity: fast generation;
- Variety: many formats.

## Tools

Hadoop, Spark, Kafka, data warehouses.

## Python

PySpark, Dask for out-of-core processing.

## Lesson summary

Big Data = scale in size, speed, variety.

<!--TASK-->
### Task 1 — Volume
Give an example.

### Task 2 — Velocity
Give an example.

### Task 3 — Variety
Give an example.

### Task 4 — Tools
Name three tools.

### Task 5 — PySpark
Why use PySpark?

### Task 6 — Batch vs stream
Difference.

### Task 7 — When
When is "big" really needed?
<!--/TASK-->

<!--HINT-->
### Hint 1
TB.

### Hint 2
Real-time.

### Hint 3
Formats.

### Hint 4
Spark.

### Hint 5
Distributed.

### Hint 6
Time.

### Hint 7
Scale.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
Терабайты логов или транзакций
```

### Solution 2
```text
Миллионы событий в секунду: клики, датчики
```

### Solution 3
```text
CSV, JSON, изображения, видео, аудио
```

### Solution 4
```text
Apache Spark, Hadoop, Kafka, Redshift, ClickHouse
```

### Solution 5
```text
PySpark запускает Spark-обработку из Python —
данные обрабатываются на кластере
```

### Solution 6
```text
Batch: обрабатывает накопленное по расписанию
Stream: обрабатывает по мере поступления
```

### Solution 7
```text
Когда данные не помещаются в память одной машины
или обычные инструменты слишком медленные
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Big Data?
- Huge datasets
- Small
- One file
- None
* Correct answer: Huge datasets
Scale.

What is volume?
- Size
- Speed
- Variety
- None
* Correct answer: Size
TB.

What is velocity?
- Speed
- Size
- Variety
- None
* Correct answer: Speed
Real-time.

What is variety?
- Formats
- Size
- Speed
- None
* Correct answer: Formats
Types.

What is Spark?
- Processing engine
- Database
- Browser
- None
* Correct answer: Processing engine
Distributed.

What is Kafka?
- Event streaming
- Storage
- Query
- None
* Correct answer: Event streaming
Queue.

What is PySpark?
- Python API
- Library only
- Database
- None
* Correct answer: Python API
Spark.

What is batch?
- Scheduled chunks
- Continuous
- Instant
- None
* Correct answer: Scheduled chunks
Nightly.

What is stream?
- Continuous data
- Static
- Batch
- None
* Correct answer: Continuous data
Real-time.

What is distributed?
- Many machines
- One
- Small
- None
* Correct answer: Many machines
Cluster.

What is a cluster?
- Machine group
- One server
- A file
- None
* Correct answer: Machine group
Spark.

What is out-of-core?
- Beyond memory
- In memory
- Small
- None
* Correct answer: Beyond memory
Disk.
<!--/QUIZ-->
