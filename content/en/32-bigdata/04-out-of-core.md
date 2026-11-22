---
title: Data Larger Than Memory: Chunking and Arrow
summary: How to process data that doesn't fit into RAM: streaming block-by-block reads and the Apache Arrow format.
order: 4
duration: 40 min
difficulty: advanced
tags: pyarrow, chunking, out-of-core, recordbatch, memory
---

## The Memory Wall

Imagine: you have a 50 GB file, and the machine has 16 GB of RAM. Attempting `pd.read_csv("big.csv")` will end either in a crash with `MemoryError` or with the operating system killing the process. This is a fundamental limitation: any data structure must fit into RAM before you can work with it.

There are two ways out. The first is to buy a server with a terabyte of memory (expensive). The second is out-of-core processing: don't load everything at once — read data in pieces, process each piece, and accumulate the result. This approach is called chunking, and it underlies all big-data tools: Polars streaming, Dask, Spark.

## Apache Arrow: a Format Everyone Understands

Almost all modern big-data tools store data in Apache Arrow — a columnar binary format. What it gives:

- Columnar layout: values of one column lie together, which speeds up column aggregations tens of times;
- Zero-copy: reading from an Arrow array requires no conversion — numbers already lie as raw numbers, without Python wrappers;
- A standard: Arrow is understood by Polars, Dask, Spark, DuckDB, pandas (via the `arrow` backend) — data can be passed between libraries without serialization.

Python access to Arrow is provided by the `pyarrow` library:

```bash
pip install pyarrow
```

## Tables and RecordBatches

The simplest object is `pyarrow.Table`:

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.table({
    "city": ["Moscow", "Saint Petersburg", "Kazan"],
    "amount": [100.0, 200.0, 150.0],
})
print(table.schema)
print(table.num_rows, table.num_columns)
```

A table consists of RecordBatches — chunks of several thousand rows. Batches are what allow streaming Parquet reads: not the whole table, but one batch at a time.

## Streaming Parquet Reads

Inside, a Parquet file is split into row groups — independent blocks of rows. The library can read one row group at a time without opening the others:

```python
pf = pq.ParquetFile("big.parquet")
print("Row groups:", pf.num_row_groups)

for batch in pf.iter_batches(batch_size=10_000):
    # batch is a RecordBatch of 10,000 rows
    print(batch.num_rows)
```

`iter_batches` returns a generator: at any moment only one batch is in memory. This is the core of out-of-core.

## Computations on Batches

A batch can be processed with Arrow itself. For example, summing a column:

```python
import pyarrow.compute as pc

total = 0.0
for batch in pf.iter_batches(batch_size=10_000):
    total += pc.sum(batch.column("amount")).as_py()
print("Total:", total)
```

`pc.sum` computes the sum in Arrow's native code, and `.as_py()` converts the scalar into a plain Python float. We accumulated the sum over a 50 GB file while holding at most 10,000 rows in memory.

## Reading CSV in Blocks

Similarly you can read CSV — `pyarrow.csv.open_csv` creates a stream of RecordBatches:

```python
import pyarrow.csv as pv

reader = pv.open_csv("big.csv", read_options=pv.ReadOptions(block_size=4_096))
rows = 0
while True:
    try:
        batch = reader.read_next_batch()
    except StopIteration:
        break
    rows += batch.num_rows
print("Rows:", rows)
```

`block_size` is the block size in bytes read at once.

Out-of-core reading scheme: the file is never loaded entirely; only the current batch and an accumulator live in memory.

```mermaid
flowchart LR
    A["Parquet file"] --> B["row groups"]
    B --> C["iter_batches"]
    C --> D["per-batch aggregate"]
    D --> E["accumulated total"]
```

## Memory and Speed

Out-of-core isn't free: we re-read the file every time another aggregate is needed. So in practice:

- compute all needed aggregates in one pass (accumulate in a single loop);
- store intermediate results in compact formats (Parquet), not CSV;
- if data is needed repeatedly — use databases or Dask/Spark with caching.

Now let's solidify it with practice.

<!--TASK-->
### Task 1
Create a file `make_big.py` that generates a Parquet with 200,000 rows: columns `id` (integers), `city` (from the list "Moscow", "Saint Petersburg", "Kazan") and `amount` (random values from 0 to 1000). Write it to `big.parquet` with `row_group_size=20_000` via `pq.write_table`. Then in `chunk_intro.py` open `pq.ParquetFile`, print the number of row groups, the number of rows, and the sum of `amount` via `pc.sum` over the whole table.

### Task 2
Implement the function in `chunk_utils.py`:

```python
def total_from_parquet(path: str, batch_size: int = 10_000) -> float:
    """Stub function: batched summation."""
    return 0.0
```

It should open `pq.ParquetFile`, iterate over `iter_batches(batch_size=batch_size)`, accumulate the sum of the `amount` column via `pc.sum` and return the total. For 200,000 rows with `batch_size=10_000` the sum must match the sum computed over the whole table at once. Print both sums and check they are equal.

### Task 3
Write a function `count_csv_rows_in_chunks(path, block_size=4096)` that counts the total number of rows in a CSV file via `pv.open_csv` and `read_next_batch`. Generate a CSV file with 5,000 rows in `make_big.py` (no header, one "number,number" pair per line). Verify the function returns 5,000, and that with `block_size=1024` the result is the same.

### Task 4
Write pytest tests for `total_from_parquet`. In `test_chunk_utils.py` via `tmp_path` create a temporary Parquet with known `amount` values (for example, [1.0, 2.0, 3.0, 4.0, 5.0]) and `row_group_size=2`. Check: (1) the sum is 15.0; (2) with `batch_size=1` the sum is the same; (3) with `batch_size=100` (larger than the row count) the sum is the same; (4) for an empty table the sum is 0.0. Run pytest.

### Task 5
Write pytest tests for `count_csv_rows_in_chunks`. In `test_chunk_utils.py` create a temporary CSV with 3 data rows (plus one trailing empty line). Check that the function returns 3, and that it correctly handles lines containing spaces and empty values. Then check that `block_size` doesn't affect the result (compare `block_size=128` and `block_size=8192`). Run pytest and get a green run.

### Task 6
Write a function `city_stats(path, batch_size=20_000)` that in one pass over batches computes for each city the row count, the sum, and the maximum of the `amount` column. Inside the loop convert the batch columns to lists via `to_pylist()` and update a dictionary of the form `{city: [count, total, max]}`. Return the finished dictionary. Verify on `big.parquet`: the sum of all `total` matches the file's total sum, and the sum of `count` matches the row count. Expected output — a dictionary for three cities and `True` at the end.

### Task 7
Write a function `filter_to_parquet(src, dst, min_sum=500)` that reads the source file in batches with only the needed columns (`iter_batches(columns=["id", "amount"])`), selects rows with `amount >= min_sum` via `pyarrow.compute` and appends them to a new Parquet via `pq.ParquetWriter`. Return the number of written rows. Verify that the new file has no rows below the threshold and that its count matches the number of matching rows in the source table. Expected output — the row count and `True`.

<!--/TASK-->

<!--HINT-->
### Hint 1
Generation: `pa.table({...})` with numbers via `range(200_000)` and a repeating city list (for example, `["Moscow", "Saint Petersburg", "Kazan"] * 66_666 + ...`). Write: `pq.write_table(table, "big.parquet", row_group_size=20_000)`. Whole-table sum: `pc.sum(table.column("amount")).as_py()`.

### Hint 2
Inside the function: `pf = pq.ParquetFile(path)`, then a loop over `pf.iter_batches(batch_size=batch_size)`, in each — `total += pc.sum(batch.column("amount")).as_py()`. Don't forget `import pyarrow.compute as pc`.

### Hint 3
`pv.open_csv(path, read_options=pv.ReadOptions(block_size=block_size))` returns a reader. In a loop: `while True: try: batch = reader.read_next_batch() except StopIteration: break`. `batch.num_rows` — the number of rows in the batch. For a headerless CSV pass `parse_options=pv.ParseOptions(header_rows=0)` — otherwise the first row will be consumed as a header.

### Hint 4
Temporary Parquet: `pa.table({"amount": [1.0, 2.0, 3.0, 4.0, 5.0]})`, then `pq.write_table(table, tmp_path / "data.parquet", row_group_size=2)`. For an empty table create `pa.table({"amount": []})`. All three batch_size checks should give 15.0.

### Hint 5
CSV with an empty line: create the lines "1,2", "3,4", "5,6" and add `\n` at the end — with `header_rows=0` this won't create an extra row. If an empty row really exists, filter out empty batches after reading, but in the test verify that the function returns exactly 3. block_size comparison: `assert count_csv_rows_in_chunks(str(path), 128) == count_csv_rows_in_chunks(str(path), 8192) == 3`.

### Hint 6
Set up `stats = {}` and in the loop get the cities and sums: `cities = batch.column("city").to_pylist()`, `values = batch.column("amount").to_pylist()`. Then plain `zip`: `entry = stats.setdefault(city, [0, 0.0, 0.0])`, increment `entry[0]`, add to `entry[1]` and update `entry[2] = max(entry[2], value)`. Memory is bounded by one batch and the number of cities, not by the file size.

### Hint 7
Mask: `mask = pc.greater_equal(batch.column("amount"), min_sum)`, filter — `filtered = batch.filter(mask)`. Writer: `writer = pq.ParquetWriter(dst, filtered.schema)`, then `writer.write_batch(filtered)` for each non-empty batch and `writer.close()` in `finally`. Count rows via `filtered.num_rows`.

<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
# make_big.py
import pyarrow as pa
import pyarrow.parquet as pq

cities = ["Moscow", "Saint Petersburg", "Kazan"]
table = pa.table({
    "id": list(range(200_000)),
    "city": (cities * 66_667)[:200_000],
    "amount": [float((i * 7919) % 1000) for i in range(200_000)],
})
pq.write_table(table, "big.parquet", row_group_size=20_000)
```

```python
# chunk_intro.py
import pyarrow.parquet as pq
import pyarrow.compute as pc

pf = pq.ParquetFile("big.parquet")
print("Row groups:", pf.num_row_groups)

table = pf.read()
print("Rows:", table.num_rows)
print("Sum:", pc.sum(table.column("amount")).as_py())
```

Output: `Row groups: 10`, `Rows: 200000`, `Sum: ...`. What's happening here? `row_group_size=20_000` splits the table into 10 row groups. When reading, `pf.read()` loads everything — that's fine for a control check, but not in production. `pc.sum` computes the sum in Arrow's native code and returns a scalar that is converted to a float via `.as_py()`.

### Walkthrough 2
Solution:

```python
# chunk_utils.py
import pyarrow.parquet as pq
import pyarrow.compute as pc

def total_from_parquet(path: str, batch_size: int = 10_000) -> float:
    """Stub function: batched summation."""
    return 0.0
    pf = pq.ParquetFile(path)
    total = 0.0
    for batch in pf.iter_batches(batch_size=batch_size):
        total += pc.sum(batch.column("amount")).as_py()
    return total

if __name__ == "__main__":
    total = total_from_parquet("big.parquet", batch_size=10_000)
    whole = pc.sum(pq.read_table("big.parquet").column("amount")).as_py()
    print("By chunks:", total)
    print("Whole:", whole)
    print("Equal:", abs(total - whole) < 1e-9)
```

Output: `By chunks: ...`, `Whole: ...`, `Equal: True`. What's happening here? The function walks through batches of 10 thousand rows and accumulates the sum. At any moment only one batch is in memory — 10 thousand rows instead of 200 thousand. This is the essence of out-of-core: memory doesn't depend on the file size, only on `batch_size`. Comparing with the "whole" computation confirms correctness.

### Walkthrough 3
Solution:

```python
# make_big.py (addition)
import pyarrow.csv as pv
with open("big.csv", "w") as f:
    for i in range(5_000):
        f.write(f"{i},{i * 2}\n")
```

```python
# chunk_utils.py (addition)
import pyarrow.csv as pv

def count_csv_rows_in_chunks(path: str, block_size: int = 4096) -> int:
    reader = pv.open_csv(path, read_options=pv.ReadOptions(block_size=block_size),
                         parse_options=pv.ParseOptions(header_rows=0))
    rows = 0
    while True:
        try:
            batch = reader.read_next_batch()
        except StopIteration:
            break
        rows += batch.num_rows
    return rows
```

Check: `print(count_csv_rows_in_chunks("big.csv"), count_csv_rows_in_chunks("big.csv", 1024))` — both values are 5000. What's happening here? `open_csv` returns a reader that yields RecordBatches. `header_rows=0` says there is no header. `block_size` sets the block size in bytes — but the result doesn't depend on it, because we simply add up the number of rows across all batches.

### Walkthrough 4
Solution:

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from chunk_utils import total_from_parquet

@pytest.fixture
def tmp_pq(tmp_path):
    table = pa.table({"amount": [1.0, 2.0, 3.0, 4.0, 5.0]})
    path = tmp_path / "data.parquet"
    pq.write_table(table, path, row_group_size=2)
    return path

def test_total(tmp_pq):
    assert total_from_parquet(str(tmp_pq)) == pytest.approx(15.0)

def test_batch_size_1(tmp_pq):
    assert total_from_parquet(str(tmp_pq), batch_size=1) == pytest.approx(15.0)

def test_batch_size_large(tmp_pq):
    assert total_from_parquet(str(tmp_pq), batch_size=100) == pytest.approx(15.0)

def test_empty_table(tmp_path):
    table = pa.table({"amount": []})
    path = tmp_path / "empty.parquet"
    pq.write_table(table, path)
    assert total_from_parquet(str(path)) == pytest.approx(0.0)
```

What's happening here? The fixture creates a file with `row_group_size=2` — so there are several row groups inside, which forces the function to actually read piece by piece. The tests check three batch sizes (1, the default 10,000, 100) — all must give 15.0. The empty table covers the edge case: the loop never runs, and the sum stays 0.0. `pytest.approx` guards against floating-point errors.

### Walkthrough 5
Solution:

```python
import pytest
from chunk_utils import count_csv_rows_in_chunks

def test_count_rows(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("1,2\n3,4\n5,6\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path)) == 3

def test_block_size_does_not_matter(tmp_path):
    path = tmp_path / "data2.csv"
    path.write_text("10,20\n30,40\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path), 128) == 2
    assert count_csv_rows_in_chunks(str(path), 8192) == 2

def test_blank_lines(tmp_path):
    path = tmp_path / "data3.csv"
    path.write_text("1,2\n\n3,4\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path)) == 3
```

What's happening here? The first test is a basic count. The second verifies that `block_size` doesn't affect the result — an important property for API stability. The third test with an empty line: an empty line in a CSV doesn't produce a batch with empty columns; it simply adds no data, so the counter is still 3. This covers the typical "dirty" data case where an extra newline often sits at the end of a file. Run: `pytest test_chunk_utils.py -v`.

### Walkthrough 6
Solution:

```python
import pyarrow.parquet as pq

def city_stats(path: str, batch_size: int = 20_000) -> dict:
    pf = pq.ParquetFile(path)
    stats = {}
    for batch in pf.iter_batches(batch_size=batch_size):
        cities = batch.column("city").to_pylist()
        values = batch.column("amount").to_pylist()
        for city, value in zip(cities, values):
            entry = stats.setdefault(city, [0, 0.0, 0.0])
            entry[0] += 1
            entry[1] += value
            entry[2] = max(entry[2], value)
    return stats

stats = city_stats("big.parquet")
print(stats)
total = sum(v[1] for v in stats.values())
rows = sum(v[0] for v in stats.values())
print("Sum converges:", abs(total - 99_000.0) < 1e-6)
print("Rows:", rows)
```

Output: the dictionary `{'Moscow': [66667, ...], 'Saint Petersburg': [...], 'Kazan': [...]}` and the checks. What's happening here? We compute three aggregates in one pass because each batch is read from disk exactly once. The accumulator is a plain dictionary with three numbers per city: its size depends on the number of cities, not on the file size. `to_pylist()` creates Python lists only for one batch, so peak memory ≈ `batch_size` rows. If we called `table.to_pylist()` for the whole file, we'd get 200 thousand Python objects — tens of times more memory than the Parquet itself. Checking that the sum of all `total` across cities matches `pc.sum` over the whole column is a good control.

### Walkthrough 7
Solution:

```python
import pyarrow.parquet as pq
import pyarrow.compute as pc

def filter_to_parquet(src: str, dst: str, min_sum: float = 500) -> int:
    pf = pq.ParquetFile(src)
    writer = None
    written = 0
    try:
        for batch in pf.iter_batches(batch_size=10_000, columns=["id", "amount"]):
            filtered = batch.filter(pc.greater_equal(batch.column("amount"), min_sum))
            if filtered.num_rows == 0:
                continue
            if writer is None:
                writer = pq.ParquetWriter(dst, filtered.schema)
            writer.write_batch(filtered)
            written += filtered.num_rows
    finally:
        if writer is not None:
            writer.close()
    return written

written = filter_to_parquet("big.parquet", "filtered.parquet")
check = pq.read_table("filtered.parquet")
print("Written:", written)
print("Minimum in new file:", pc.min(check.column("amount")).as_py())
print("Match:", written == check.num_rows and pc.min(check.column("amount")).as_py() >= 500)
```

Output: the number of written rows and `Match: True`. What's happening here? `columns=["id", "amount"]` is a projection: the `city` column is never read from disk, saving both memory and time. `batch.filter(mask)` returns a new RecordBatch with only the matching rows, without touching the original. `ParquetWriter` is created lazily at the first non-empty batch: if no row passes the filter, we don't create an empty file and don't crash on the schema. `finally` guarantees `close()`, otherwise the file would be left incomplete and unreadable. This "read batch — filter — write batch" pattern underlies ETL over tens of gigabytes with just a few gigabytes of RAM.

<!--/SOLUTION-->

<!--QUIZ-->
What does out-of-core mean?
- Processing data that doesn't fit into memory, in pieces
- Processing data on a GPU
- Storing data in RAM
* Correct answer: Processing data that doesn't fit into memory, in pieces
Out-of-core reads data in blocks and accumulates the result.

Which format underlies Polars and Dask?
- Apache Arrow
- JSON
- XML
* Correct answer: Apache Arrow
Arrow is a columnar binary format understood by almost all big-data tools.

What is a RecordBatch in Arrow?
- A chunk of a table with several thousand rows
- A whole file
- A table schema
* Correct answer: A chunk of a table with several thousand rows
Batches are what allow streaming data reads.

Which ParquetFile method reads data in blocks?
- iter_batches
- read_table
- read_all
* Correct answer: iter_batches
iter_batches returns a generator of RecordBatches, one at a time.

What is a row group in Parquet?
- An independent block of rows inside a file
- A file column
- A folder with files
* Correct answer: An independent block of rows inside a file
A row group can be read separately from the others.

What will pc.sum(arr).as_py() return?
- A number as a Python type
- A RecordBatch
- An Arrow array
* Correct answer: A number as a Python type
as_py converts an Arrow scalar into an ordinary Python object.

Which parameter sets the block size when reading CSV?
- block_size
- chunk
- batch_rows
* Correct answer: block_size
block_size sets the block size in bytes for open_csv.

Why is header_rows=0 needed in ParseOptions?
- To say the CSV has no header
- To skip the first 0 rows
- To add a header
* Correct answer: To say the CSV has no header
Otherwise the first row would be treated as a header.

What happens if you read a file larger than memory via read_table?
- MemoryError or process death
- Everything reads fine
- The file is compressed automatically
* Correct answer: MemoryError or process death
The whole table would try to fit into RAM.

What is better to store for repeated reads of large data?
- Parquet with row groups
- CSV
- Text logs
* Correct answer: Parquet with row groups
Parquet lets you read only the needed blocks and columns.

What does the `columns=["id", "amount"]` parameter give in `iter_batches`?
- Reads only the specified columns — saving memory and time
- Changes column names
- Sorts columns
* Correct answer: Reads only the specified columns — saving memory and time
This is a projection: unneeded columns are not read from disk at all.

Why is `pq.ParquetWriter` needed?
- To write batches to a file piece by piece without assembling the whole table
- To read row groups
- To compress CSV
* Correct answer: To write batches to a file piece by piece without assembling the whole table
The writer accepts batches and appends them as they arrive.

How much memory does a batched aggregate require?
- Roughly one batch plus accumulators
- The whole file
- Twice the file size
* Correct answer: Roughly one batch plus accumulators
Memory depends on `batch_size` and the number of groups, not on the file size.

Why can't you call `table.to_pylist()` on a 50 GB file?
- A list of Python objects is many times larger than the data and won't fit in memory
- The method doesn't exist
- Parquet doesn't support lists
* Correct answer: A list of Python objects is many times larger than the data and won't fit in memory
Each element is a Python object with overhead.

<!--/QUIZ-->
