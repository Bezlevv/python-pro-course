---
title: Cloud Storage and Parquet
summary: Parquet as the standard for analytical data, working with S3 via boto3 and s3fs, partitioning, and pushdown filters.
order: 5
duration: 40 min
difficulty: advanced
tags: parquet, s3, boto3, s3fs, pyarrow, cloud
---

## Why Parquet Is the Standard

In the previous lesson you saw how to read Parquet in blocks. Parquet is a columnar file format, and it has become the de facto standard for analytical data. Why:

- Columnar layout: columns are stored separately, so you can read only the needed columns;
- Compression: columns are compressed (snappy, zstd, gzip), often 5–10×;
- Statistics: each row group's header holds column minimums/maximums, which lets you skip whole blocks;
- Schema: column types are stored in the file; data is self-documenting.

## Parquet in Practice

Writing and reading via pyarrow:

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.table({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "city": ["Moscow", "Saint Petersburg", "Moscow"],
    "amount": [100.0, 200.0, 150.0],
})

pq.write_table(table, "sales.parquet", compression="zstd", row_group_size=1000)

t = pq.read_table("sales.parquet")
print(t.schema)
```

File attributes:

```python
pf = pq.ParquetFile("sales.parquet")
print(pf.metadata.num_rows)
print(pf.metadata.row_group(0).column(2).statistics)  # column statistics
```

## Cloud Storage

The big-data paradigm: files live not on a server disk but in object storage — Amazon S3, Yandex Object Storage, Google Cloud Storage, MinIO. The key idea: S3 is just a "folder" with objects addressed by paths like `s3://bucket/key`.

There are two clients: low-level `boto3` (the AWS SDK) and file-like `s3fs` (works like a local file system).

```bash
pip install boto3 s3fs
```

## boto3: Low Level

```python
import boto3

s3 = boto3.client("s3")  # credentials from environment variables

# List buckets
print([b["Name"] for b in s3.list_buckets()["Buckets"]])

# List objects
resp = s3.list_objects_v2(Bucket="my-bucket", Prefix="sales/")
for obj in resp.get("Contents", []):
    print(obj["Key"], obj["Size"])

# Upload and download
s3.upload_file("local.parquet", "my-bucket", "sales/local.parquet")
s3.download_file("my-bucket", "sales/local.parquet", "downloaded.parquet")
```

Credentials come from the environment variables `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (or from a profile). They are never stored in code.

## s3fs: Work as with a Disk

`s3fs` implements a file system interface:

```python
import s3fs

fs = s3fs.S3FileSystem()
print(fs.ls("my-bucket/sales/"))

with fs.open("my-bucket/sales/data.parquet", "rb") as f:
    table = pq.read_table(f)  # read directly from S3
```

Once we have a file-like object, any code that can read from a file works with the cloud without changes.

## Direct S3 Reads in Libraries

Polars can read S3 directly (s3fs is required):

```python
import polars as pl
q = pl.scan_parquet("s3://my-bucket/sales/*.parquet")
print(q.collect())
```

Dask — via `storage_options`:

```python
import dask.dataframe as dd
ddf = dd.read_parquet("s3://my-bucket/sales/", storage_options={"anon": False})
```

## Partitioning

Large analytical datasets are partitioned — laid out into subfolders by column value:

```
sales/
├── city=Moscow/part.parquet
└── city=Saint Petersburg/part.parquet
```

Writing hive partitions:

```python
import pyarrow.dataset as ds

ds.write_dataset(table, "sales", format="parquet", partitioning=["city"])
```

Reading with a partition filter:

```python
dataset = ds.dataset("sales", format="parquet", partitioning="hive")
filtered = dataset.to_table(filter=ds.field("city") == "Moscow")
```

The filter is pushed down into paths — only the needed folders are read, saving network traffic and time. Now practice.

<!--TASK-->
### Task 1
Create a file `parquet_intro.py`. Generate a `pa.table` with columns `city` (three cities), `month` (6 months) and `revenue` (random numbers). Write it to `sales.parquet` with `compression="zstd"` and `row_group_size=100`. Then open `pq.ParquetFile` and print: the schema, the row count, the number of row groups, and the statistics of the `revenue` column of the first row group. Explain in a comment what `min` and `max` in the statistics mean.

### Task 2
Write a function `split_s3_path(path)` in `s3_utils.py` that takes a path of the form `s3://bucket/key/part.parquet` and returns a tuple `(bucket, key)`. Add a check: if the path doesn't start with `s3://`, the function must raise `ValueError`. Test it on three paths, including a key without a slash and a path with nested folders.

### Task 3
Adapt the code from the first lesson: in `s3_utils.py` write a function `describe_s3_parquet(path, s3_client)` that takes a ready boto3 client and a path `s3://bucket/key`. The function should download the file to a temporary folder via `s3_client.download_file`, open `pq.ParquetFile` and return a dictionary `{"rows": ..., "columns": ..., "row_groups": ...}`. Don't call it with real credentials — just prepare code that will work after substituting the client.

### Task 4
Write pytest tests for `split_s3_path` and for writing/reading Parquet. In `test_s3_utils.py` via `tmp_path` create a table, write it to Parquet, read it back and check that the schema and data match. For `split_s3_path` check: a valid path, a path without a key, a path with nested folders, and `ValueError` being raised for an invalid path. Run pytest.

### Task 5
Write pytest tests for the partitioned dataset. Via `tmp_path` create a table with `city` and `revenue` columns, write it via `ds.write_dataset(..., partitioning=["city"])`, then open it via `ds.dataset(partitioning="hive")`. Check: (1) subfolders `city=...` appeared in the folder; (2) `dataset.to_table(filter=ds.field("city") == "Moscow")` returns only Moscow rows; (3) the total number of rows equals the number of rows in the original table. Run pytest.
<!--/TASK-->

<!--HINT-->
### Hint 1
Random numbers: `[float((i * 7919) % 1000) for i in range(N)]`. Statistics: `pf.metadata.row_group(0).column(2).statistics` — the `min` and `max` attributes are available on the statistics object. Column name: `pf.schema.column(2).name`.

### Hint 2
Path `s3://a/b/c`: strip the `s3://` prefix, then split at the first `/` into bucket and key: `bucket, _, key = rest.partition("/")`. If there is no `/` — the key is an empty string.

### Hint 3
`tempfile.NamedTemporaryFile(delete=False)` or a `tmp_path`-like local path. `s3_client.download_file(bucket, key, local_path)` — a boto3 method. Then `pq.ParquetFile(local_path)`. Don't forget to delete the temporary file after use.

### Hint 4
To compare schemas use `t.schema == original.schema` and `t.to_pydict() == table.to_pydict()`. For `split_s3_path`: `assert split_s3_path("s3://b/k.parquet") == ("b", "k.parquet")`, for the error use `pytest.raises(ValueError)`.

### Hint 5
After `ds.write_dataset` list the subfolders: `sorted(p.name for p in (tmp_path / "sales").iterdir())` — there should be `city=Moscow` and `city=Saint Petersburg`. Filter: `ds.field("city") == "Moscow"`. For the total row count: `len(dataset.to_table())`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import pyarrow as pa
import pyarrow.parquet as pq

cities = ["Moscow", "Saint Petersburg", "Kazan"]
table = pa.table({
    "city": [cities[i % 3] for i in range(600)],
    "month": [f"2024-{m:02d}" for m in [(i % 6) + 1 for i in range(600)]],
    "revenue": [float((i * 7919) % 1000) for i in range(600)],
})
pq.write_table(table, "sales.parquet", compression="zstd", row_group_size=100)

pf = pq.ParquetFile("sales.parquet")
print("Schema:", pf.schema)
print("Rows:", pf.metadata.num_rows)
print("Row groups:", pf.num_row_groups)

stats = pf.metadata.row_group(0).column(2).statistics
print("Revenue statistics (row group 0): min =", stats.min, ", max =", stats.max)
```

Output: a schema with three columns, 600 rows, 6 row groups, and the statistics of the first row group. What's happening here? `pq.write_table` compresses the columns with the zstd algorithm and splits them into row groups of 100 rows. The statistics in each row group's header let the reader skip a block if the filter condition cannot be satisfied (for example, `filter(pl.col("revenue") > 5000)` — if `max < 5000`, the block is skipped).

### Walkthrough 2
Solution:

```python
def split_s3_path(path: str) -> tuple:
    if not path.startswith("s3://"):
        raise ValueError(f"Not an S3 path: {path}")
    rest = path[len("s3://"):]
    bucket, sep, key = rest.partition("/")
    if not sep:
        key = ""
    return bucket, key
```

Check:

```python
print(split_s3_path("s3://my-bucket/sales/part.parquet"))  # ('my-bucket', 'sales/part.parquet')
print(split_s3_path("s3://my-bucket"))                      # ('my-bucket', '')
print(split_s3_path("https://example.com"))                 # ValueError
```

What's happening here? `partition("/")` splits the string into three parts: everything before the first slash, the slash itself, and everything after. If there is no slash — the key is empty, meaning the path points at the whole bucket. The prefix check guards against garbage input. Such a function is useful when you receive a path from a user and need to break it into parameters for boto3 (bucket and key separately).

### Walkthrough 3
Solution:

```python
import tempfile
import os
import pyarrow.parquet as pq
from s3_utils import split_s3_path

def describe_s3_parquet(path: str, s3_client) -> dict:
    bucket, key = split_s3_path(path)
    if not key:
        raise ValueError("Key not specified")

    fd, local = tempfile.mkstemp(suffix=".parquet")
    os.close(fd)
    try:
        s3_client.download_file(bucket, key, local)
        pf = pq.ParquetFile(local)
        return {
            "rows": pf.metadata.num_rows,
            "columns": [pf.schema.column(i).name for i in range(pf.schema.num_columns)],
            "row_groups": pf.num_row_groups,
        }
    finally:
        os.unlink(local)
```

What's happening here? The function is fully ready to work with a real client, but it calls nothing itself — the client is passed from outside (dependency injection). This lets you test the logic with a mock without spending network requests. The downloaded file lives in a temporary folder and is deleted even on error thanks to `finally`. Such a design is the standard for cloud code.

### Walkthrough 4
Solution:

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from s3_utils import split_s3_path

def _make_table():
    return pa.table({"city": ["Moscow", "Saint Petersburg"], "revenue": [100.0, 200.0]})

def test_parquet_roundtrip(tmp_path):
    path = tmp_path / "data.parquet"
    pq.write_table(_make_table(), path)
    loaded = pq.read_table(path)
    assert loaded.schema == _make_table().schema
    assert loaded.to_pydict() == _make_table().to_pydict()

def test_split_s3_path_basic():
    assert split_s3_path("s3://b/k.parquet") == ("b", "k.parquet")

def test_split_s3_path_no_key():
    assert split_s3_path("s3://bucket") == ("bucket", "")

def test_split_s3_path_nested():
    assert split_s3_path("s3://b/a/b/c.parquet") == ("b", "a/b/c.parquet")

def test_split_s3_path_invalid():
    with pytest.raises(ValueError):
        split_s3_path("https://example.com/file")
```

What's happening here? The roundtrip test verifies that the schema and data survive writing and reading — this is the foundation of reliability. The `split_s3_path` tests cover the main cases and the error. No test touches the network: everything works locally and fast.

### Walkthrough 5
Solution:

```python
import pyarrow as pa
import pyarrow.dataset as ds
import pytest

def test_partitioned_dataset(tmp_path):
    table = pa.table({
        "city": ["Moscow", "Saint Petersburg", "Moscow", "Saint Petersburg"],
        "revenue": [100.0, 200.0, 300.0, 400.0],
    })
    ds.write_dataset(table, tmp_path / "sales", format="parquet", partitioning=["city"])

    dirs = sorted(p.name for p in (tmp_path / "sales").iterdir())
    assert dirs == ["city=Moscow", "city=Saint Petersburg"]

    dataset = ds.dataset(tmp_path / "sales", format="parquet", partitioning="hive")
    moscow = dataset.to_table(filter=ds.field("city") == "Moscow")
    assert moscow.num_rows == 2
    assert set(moscow.column("city").to_pylist()) == {"Moscow"}

    assert dataset.to_table().num_rows == 4
```

What's happening here? `partitioning=["city"]` creates subfolders like `city=Moscow/`. When reading with `partitioning="hive"`, the library understands this layout and adds the `city` column from the path. The filter `ds.field("city") == "Moscow"` is pushed down to the file system level: only the files in the `city=Moscow` folder are read. This is a key optimization for cloud storage — less data is downloaded over the network.
<!--/SOLUTION-->

<!--QUIZ-->
What advantage does the columnar Parquet format give?
- You can read only the needed columns
- You can modify data directly in the file
- It takes more space
* Correct answer: You can read only the needed columns
Columnar layout lets you select columns and skip the rest.

What is stored in row group statistics?
- Column minimums and maximums
- The contents of all rows
- Object hashes
* Correct answer: Column minimums and maximums
Statistics allow skipping blocks during filtering.

Which parameter sets the compression algorithm in pq.write_table?
- compression
- codec
- zip
* Correct answer: compression
compression="zstd" or "snappy" sets the codec.

What does s3fs.S3FileSystem().ls("bucket/path") return?
- A list of objects/folders at the path
- The contents of files
- A Parquet schema
* Correct answer: A list of objects/folders at the path
ls works like in a local file system.

Which boto3 method downloads an object?
- s3_client.download_file(bucket, key, local)
- s3_client.get_object(bucket)
- s3_client.read(bucket, key)
* Correct answer: s3_client.download_file(bucket, key, local)
download_file takes a bucket, a key, and a local path.

Where does boto3 get credentials?
- From the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
- From the program code
- From a data file
* Correct answer: From the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
Credentials must never end up in code or in a repository.

What is hive partitioning?
- Laying data out into subfolders of the form column=value
- Compressing files
- Splitting into row groups
* Correct answer: Laying data out into subfolders of the form column=value
Folder names contain the column and value, which allows filtering by path.

What does the filter ds.field("city") == "Moscow" do when reading a dataset?
- Is pushed down into paths and reads only the needed folders
- Reads all data and filters in memory
- Nothing, it's just syntax
* Correct answer: Is pushed down into paths and reads only the needed folders
This saves network traffic and time.

How does Polars read Parquet from S3?
- pl.scan_parquet("s3://bucket/key")
- pl.read_bytes("s3://...")
- pl.read_remote("...")
* Correct answer: pl.scan_parquet("s3://bucket/key")
s3fs must be installed for fsspec support.

What happens if split_s3_path is called with a non-s3:// path?
- ValueError
- None
- An empty tuple
* Correct answer: ValueError
The function checks the prefix and raises an exception.
<!--/QUIZ-->
