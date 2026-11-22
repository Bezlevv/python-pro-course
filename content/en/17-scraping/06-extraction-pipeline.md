---
title: Collection pipeline: HTML → data → CSV/DB
summary: A full pipeline: fetching, parsing, extraction, cleaning, deduplication, and saving to CSV and SQLite.
order: 6
duration: 45 min
difficulty: advanced
tags: csv, sqlite3, pipeline, data cleaning, storage, deduplication
---

You know how to download pages, parse HTML, and walk pagination. It's time to assemble everything into a single **pipeline** — a program that turns "raw" HTML into neat data on disk: into a CSV file or a database. That's exactly how real data collectors are built.

## Pipeline stages

Any collection pipeline consists of stages:

1. **Fetch** — download the page (`requests`).
2. **Parse** — turn the HTML into a tree (`BeautifulSoup`).
3. **Extract** — pull out the needed fields (text, authors, prices).
4. **Clean** — tidy up: remove whitespace, empty values, turn strings into numbers.
5. **Store** — save to CSV or a database.

Dividing into stages is modularity: you can change the data source without touching the saving, and vice versa.

## Saving to CSV

The `csv` module is standard. Writing a list of dictionaries:

```python
import csv

rows = [
    {"author": "Anna", "book": "Python for Beginners"},
    {"author": "Boris", "book": "SQL Without Tears"},
]

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "book"])
    writer.writeheader()
    writer.writerows(rows)
```

`newline=""` is a must — otherwise extra blank lines appear in the file. `encoding="utf-8"` — so Cyrillic reads correctly. `DictWriter` writes headers and rows from dictionaries itself.

Reading back:

```python
with open("books.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["author"], "-", row["book"])
```

## Saving to SQLite

SQLite is a database in a single file, built right into Python (the `sqlite3` module). For scraping it's more convenient than CSV: there are types, query-based search, and protection against duplicates:

```python
import sqlite3

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

cur.execute(
    "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
    ("Quote text", "Author", "life, love"),
)
conn.commit()
conn.close()
```

`?` — placeholders: never insert values into an SQL string via f-strings — that's dangerous. `conn.commit()` saves changes, `conn.close()` closes the file.

## Cleaning data

Extracted values are rarely perfect. Typical operations:

```python
price_text = "£51.77"
price = float(price_text[1:])   # '51.77' -> 51.77

name = "  Anna  "
name = name.strip()              # remove edge whitespace

# if not name:
#     continue  # inside a loop, skips empty values
```

The rule: **clean before saving** — finished data should go into the file/database.

## Deduplication

If you run the same pipeline twice, the data gets duplicated. The solution — in the database: `UNIQUE(text, author)` + `INSERT OR IGNORE` (skip if such a row already exists). CSV has no such protection — so uniqueness must be ensured in code, for example via a set of already-seen ids.

## The full pipeline

Let's collect quotes into SQLite:

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for q in soup.select("div.quote"):
        text = q.select_one("span.text").get_text().strip()
        author = q.select_one("small.author").get_text().strip()
        tags = ", ".join(t.get_text() for t in q.select("a.tag"))
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (text, author, tags),
        )

conn.commit()
cur.execute("SELECT COUNT(*) FROM quotes")
print("Total quotes:", cur.fetchone()[0])
conn.close()
```

Here all stages are joined in one loop: request → parse → extract → clean (`strip`) → save with deduplication.

## Summary

Pipeline = fetch → parse → extract → clean → store. CSV is simple, SQLite is reliable. `csv.DictWriter` and `sqlite3` with `?` placeholders — the foundation of storage. Cleaning and deduplication are what separates "just collected" from "collected well". The module's final project!

<!--TASK-->
### Task 1

Write a program `csv_basics.py` that creates a list of three dictionaries: `{"city": "Moscow", "population": 13000000}`, `{"city": "Saint Petersburg", "population": 5600000}`, `{"city": "Novosibirsk", "population": 1600000}`. Write it to the file `cities.csv` via `csv.DictWriter` (with `newline=""` and `encoding="utf-8"`), then read it back via `csv.DictReader` and print all rows in the format `City: <city>, Population: <population>`. Check the file was created via `Path("cities.csv").exists()`.

### Task 2

Write a program `quotes_csv.py` that downloads page 1 of `https://quotes.toscrape.com/`, extracts all quotes (`div.quote`): text (`span.text`), author (`small.author`), and tags (`a.tag`, comma-separated). Clean the text and author with `strip()`. Save everything to the file `quotes.csv` with the columns `text, author, tags` via `csv.DictWriter`. At the end, print the number of rows written.

### Task 3

Create a database `quotes.db` with a table `quotes` (columns: `id INTEGER PRIMARY KEY AUTOINCREMENT`, `text TEXT NOT NULL`, `author TEXT NOT NULL`, `tags TEXT`, and the constraint `UNIQUE(text, author)`). Write a program `quotes_db.py` that collects quotes from the first three pages of `https://quotes.toscrape.com/` and inserts them via `INSERT OR IGNORE`. After insertion, print the total number of rows in the table (`SELECT COUNT(*)`) and the number of unique authors (`SELECT COUNT(DISTINCT author)`).

### Task 4

Write a function `pipeline(max_pages=3)` that runs the full pipeline: collecting quotes from pages (as in task 3), cleaning with `strip()`, skipping empty texts (if the text is empty — `continue`), and inserting into SQLite. The function should return the number of inserted rows (sum `cur.rowcount` over inserts). Call it with `max_pages=3`, print the result, and make sure a second call adds 0 new rows (everything is already in the database).

### Task 5

Combine CSV and SQLite: collect quotes from page 1 into `quotes.csv` (as in task 2), then read this CSV via `csv.DictReader` and load its contents into the `quotes` table of the `quotes.db` database via `INSERT OR IGNORE`. Use only real data from the CSV — no duplication of the collection code. At the end, print the number of rows in the database. Make sure reloading the same CSV doesn't increase the row count.
<!--/TASK-->

<!--HINT-->
### Hint 1

`csv.DictWriter(f, fieldnames=["city", "population"])` — the column order is set by `fieldnames`. Don't forget `writer.writeheader()` before `writer.writerows(rows)`. Reading: `csv.DictReader(f)` — rows become dictionaries by the headers.

### Hint 2

Collect tags like this: `", ".join(t.get_text() for t in q.select("a.tag"))`. For writing, collect a list of dictionaries `{"text": ..., "author": ..., "tags": ...}` and pass it to `writer.writerows(rows)`. The row count is `len(rows)`.

### Hint 3

Be sure to call `conn.commit()` after all inserts and `conn.close()` at the end. For counting: `cur.execute("SELECT COUNT(*) FROM quotes")` and `cur.fetchone()[0]`. `COUNT(DISTINCT author)` counts unique authors.

### Hint 4

`cur.rowcount` after `execute("INSERT OR IGNORE ...")` — how many rows were actually inserted (0 if the row already existed). Sum it over all quotes. A second call will show 0 — that's the deduplication check.

### Hint 5

Read the CSV: `with open("quotes.csv", encoding="utf-8") as f: rows = list(csv.DictReader(f))`. Then a loop with `INSERT OR IGNORE` over `rows`. In the database, `UNIQUE(text, author)` won't let duplicates appear — reloading won't change `COUNT(*)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
import csv
from pathlib import Path

rows = [
    {"city": "Moscow", "population": 13000000},
    {"city": "Saint Petersburg", "population": 5600000},
    {"city": "Novosibirsk", "population": 1600000},
]

with open("cities.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["city", "population"])
    writer.writeheader()
    writer.writerows(rows)

print("File created:", Path("cities.csv").exists())

with open("cities.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"City: {row['city']}, Population: {row['population']}")
```

Step-by-step breakdown:

- `open("cities.csv", "w", newline="", encoding="utf-8")` — three important points: `"w"` — writing (the file will be recreated), `newline=""` — no extra blank lines (otherwise CSV writing inserts `\r\n` between rows), `encoding="utf-8"` — so Cyrillic is preserved correctly.
- `csv.DictWriter` receives `fieldnames` — the column order. `writeheader()` writes the first header row `city,population`.
- `writer.writerows(rows)` writes all dictionaries: the dictionary keys must match `fieldnames`.
- `Path("cities.csv").exists()` checks the file was created.
- `csv.DictReader(f)` reads the file: the first row becomes the headers, each next one — a dictionary. Accessing `row['city']` and `row['population']` is by column name.
- That's how data exchange works: any script or Excel sheet will open `cities.csv`.

### Solution 2

```python
import csv
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

rows = []
for q in soup.select("div.quote"):
    text = q.select_one("span.text").get_text().strip()
    author = q.select_one("small.author").get_text().strip()
    tags = ", ".join(t.get_text() for t in q.select("a.tag"))
    rows.append({"text": text, "author": author, "tags": tags})

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(rows)

print("Quotes written:", len(rows))
```

Step-by-step breakdown:

- `soup.select("div.quote")` — all quote blocks on the page.
- For each quote: text from `span.text`, author from `small.author`, tags — a list of `a.tag` texts joined with a comma via `", ".join(...)`.
- `strip()` removes extra whitespace and newlines at the edges — that's the cleaning stage. Without it, "dirty" strings would get into the CSV.
- The `rows` list — clean dictionaries. `csv.DictWriter` writes them with the headers `text,author,tags`.
- `len(rows)` — the number of quotes written (page 1 has 10 of them).
- Modularity: if the site changes its markup tomorrow, only the extraction block changes; the CSV writing stays.

### Solution 3

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    soup = BeautifulSoup(r.text, "lxml")
    for q in soup.select("div.quote"):
        text = q.select_one("span.text").get_text().strip()
        author = q.select_one("small.author").get_text().strip()
        tags = ", ".join(t.get_text() for t in q.select("a.tag"))
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (text, author, tags),
        )

conn.commit()

cur.execute("SELECT COUNT(*) FROM quotes")
print("Total quotes:", cur.fetchone()[0])
cur.execute("SELECT COUNT(DISTINCT author) FROM quotes")
print("Unique authors:", cur.fetchone()[0])
conn.close()
```

Step-by-step breakdown:

- `sqlite3.connect("quotes.db")` creates (or opens) the database file.
- `CREATE TABLE IF NOT EXISTS` — the table is created once; on a repeated run it already exists. `AUTOINCREMENT` assigns `id` itself.
- `UNIQUE(text, author)` — a constraint: the text+author combination cannot repeat. That's protection against duplicates at the database level.
- `INSERT OR IGNORE` — insert a row, but if one already exists — silently skip. Together with `UNIQUE` this is ideal deduplication.
- `?` placeholders — values are passed as a separate tuple. Never insert data into SQL via f-strings — that's dangerous.
- `conn.commit()` fixes the changes (without it they won't be saved), `conn.close()` closes the file.
- `SELECT COUNT(*)` — the number of rows, `SELECT COUNT(DISTINCT author)` — unique authors. Across three pages there will be ~30 quotes and several dozen authors with repeats.

### Solution 4

```python
import sqlite3
import requests
from bs4 import BeautifulSoup

def pipeline(max_pages=3):
    conn = sqlite3.connect("quotes.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            tags TEXT,
            UNIQUE(text, author)
        )
    """)

    inserted = 0
    for page in range(1, max_pages + 1):
        r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        for q in soup.select("div.quote"):
            text = q.select_one("span.text").get_text().strip()
            author = q.select_one("small.author").get_text().strip()
            if not text or not author:
                continue  # skip empty values
            tags = ", ".join(t.get_text() for t in q.select("a.tag"))
            cur.execute(
                "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
                (text, author, tags),
            )
            inserted += cur.rowcount

    conn.commit()
    conn.close()
    return inserted

first = pipeline(max_pages=3)
print("First insertion:", first, "rows")
second = pipeline(max_pages=3)
print("Second insertion:", second, "rows")
```

Step-by-step breakdown:

- The function wraps the whole pipeline: connection, table creation, collection, cleaning, insertion. It returns the number of rows actually inserted.
- `if not text or not author: continue` — the cleaning stage: empty values are skipped so they don't litter the database.
- `cur.rowcount` after `execute(...)` — the number of rows affected by the operation. For `INSERT OR IGNORE` that's 1 if the row was inserted and 0 if it already existed.
- `inserted += cur.rowcount` sums the real insertions.
- The first call returns ~30 (all quotes are new). The second call returns 0 — the same quotes already exist, and `INSERT OR IGNORE` adds nothing. That's a visible deduplication check.
- A repeated run is safe: the table already exists (`IF NOT EXISTS`), data isn't duplicated.

### Solution 5

```python
import csv
import sqlite3
import requests
from bs4 import BeautifulSoup

# Step 1: collect into CSV
r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

rows = []
for q in soup.select("div.quote"):
    text = q.select_one("span.text").get_text().strip()
    author = q.select_one("small.author").get_text().strip()
    tags = ", ".join(t.get_text() for t in q.select("a.tag"))
    rows.append({"text": text, "author": author, "tags": tags})

with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(rows)

# Step 2: load the CSV into SQLite
conn = sqlite3.connect("quotes.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        tags TEXT,
        UNIQUE(text, author)
    )
""")

with open("quotes.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cur.execute(
            "INSERT OR IGNORE INTO quotes (text, author, tags) VALUES (?, ?, ?)",
            (row["text"], row["author"], row["tags"]),
        )

conn.commit()
cur.execute("SELECT COUNT(*) FROM quotes")
print("Rows in database:", cur.fetchone()[0])
conn.close()
```

Step-by-step breakdown:

- Step 1 fully repeats task 2: collection from the site and writing to CSV. The `quotes.csv` file is an "intermediate storage".
- Step 2 reads the CSV via `csv.DictReader` — it turns rows into dictionaries by the headers `text,author,tags` itself.
- Each CSV row is inserted with `INSERT OR IGNORE` and placeholders. The `UNIQUE(text, author)` constraint in the table prevents duplicates from appearing.
- Reloading the same CSV won't increase `COUNT(*)` — all rows already exist, and `IGNORE` skips them.
- This is the transition from a one-off script to a real pipeline: source (site) → file (CSV) → database (SQLite). Each stage is separated, and the data is verifiable at every step — the CSV can be opened and looked at with your own eyes, the database can be queried with SQL.
- Such a pipeline is easy to extend: add pagination, filters, another storage format — without breaking the other parts.
<!--/SOLUTION-->

<!--QUIZ-->
Why is the parameter newline="" needed when writing CSV?
- To make the file smaller
- So extra blank lines don't appear
- To enable UTF-8 encoding
- To write headers
* Correct answer: So extra blank lines don't appear
Without newline="", CSV writing inserts extra line breaks.

What does INSERT OR IGNORE do in SQLite?
- Always inserts a row, even if there's a duplicate
- Skips the insertion if a row with the same unique values already exists
- Deletes the old row before inserting
- Raises an error on a duplicate
* Correct answer: Skips the insertion if a row with the same unique values already exists
Together with UNIQUE this gives deduplication at the database level.

Why use ? placeholders in SQL queries?
- To speed up the query
- To safely insert values without constructing an SQL string by hand
- To make the query shorter
- It's a requirement of CREATE TABLE syntax
* Correct answer: To safely insert values without constructing an SQL string by hand
Placeholders protect against errors and dangerous values; values are passed as a separate tuple.

What does cur.rowcount return after INSERT OR IGNORE?
- The total number of rows in the table
- The number of rows affected by the operation (1 or 0)
- The last inserted id
- The table name
* Correct answer: The number of rows affected by the operation (1 or 0)
For INSERT OR IGNORE it's 1 if the row was inserted and 0 if it already existed.

Which pipeline stage removes extra whitespace and empty values?
- Fetch
- Parse
- Clean
- Store
* Correct answer: Clean
Cleaning (strip, skipping empty values) happens before saving.

Why does UNIQUE(text, author) protect against duplicates even when the program is run again?
- Because SQLite removes repeats itself
- Because the database won't allow inserting a row with an already-existing combination (and INSERT OR IGNORE skips it)
- Because texts are always unique
- It doesn't work, you must check manually
* Correct answer: Because the database won't allow inserting a row with an already-existing combination (and INSERT OR IGNORE skips it)
The UNIQUE constraint at the table level guarantees uniqueness regardless of code.

Which csv.DictWriter method writes the header row with column names?
- writeheader()
- header()
- title()
- write_head()
* Correct answer: writeheader()
writeheader() takes the column names from fieldnames and writes them as the file's first row.

What happens if you forget to call conn.commit() after INSERT in SQLite?
- The changes won't be saved to the database file
- Nothing, the data will save itself
- The database will be deleted
- An error will appear on every request
* Correct answer: The changes won't be saved to the database file
commit() commits the transaction; without it the changes are rolled back when the connection closes.
<!--/QUIZ-->
