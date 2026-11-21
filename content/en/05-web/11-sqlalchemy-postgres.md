---
title: SQLAlchemy and PostgreSQL
summary: Engine, sessions, ORM models, querying and connections to PostgreSQL.
order: 11
duration: 50 min
difficulty: advanced
tags: sqlalchemy, postgres, orm
---

SQLAlchemy is a flexible SQL toolkit and ORM; PostgreSQL is a production database.

## Engine

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///db.sqlite3")
```

## Declarative model

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
```

## Session

```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
```

## CRUD

```python
session.add(Product(name="Pen", price=10))
session.commit()

products = session.query(Product).filter(Product.price < 20).all()
```

## PostgreSQL

```python
engine = create_engine("postgresql+psycopg://user:pass@localhost/db")
```

## Lesson summary

SQLAlchemy: declarative models, sessions, queries; switch engines easily.

<!--TASK-->
### Task 1 — Engine
Create a SQLite engine and connect.

### Task 2 — Model
Define a declarative Product model.

### Task 3 — Create tables
Use Base.metadata.create_all(engine).

### Task 4 — Add
Add a product and commit.

### Task 5 — Query
List products with price < 20.

### Task 6 — Update
Change a product's price and commit.

### Task 7 — PostgreSQL string
Show the connection URL for PostgreSQL.
<!--/TASK-->

<!--HINT-->
### Hint 1
create_engine("sqlite:///db.sqlite3").

### Hint 2
Base + Mapped columns.

### Hint 3
Base.metadata.create_all(engine).

### Hint 4
session.add(product); session.commit().

### Hint 5
session.query(Product).filter(...).

### Hint 6
Set attribute and commit.

### Hint 7
postgresql+psycopg://user:pass@host/db.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///db.sqlite3")
```

### Solution 2
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
```

### Solution 3
```python
Base.metadata.create_all(engine)
```

### Solution 4
```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
session.add(Product(name="Pen", price=10))
session.commit()
```

### Solution 5
```python
products = session.query(Product).filter(Product.price < 20).all()
```

### Solution 6
```python
p = session.query(Product).filter_by(name="Pen").first()
p.price = 12
session.commit()
```

### Solution 7
```python
engine = create_engine("postgresql+psycopg://user:pass@localhost/db")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SQLAlchemy?
- SQL toolkit/ORM
- Database
- Framework
- Template
* Correct answer: SQL toolkit/ORM
Python.

What is an engine?
- Connection core
- Table
- Model
- Query
* Correct answer: Connection core
Dialect.

What is a declarative model?
- Class mapping to a table
- A query
- A session
- A view
* Correct answer: Class mapping to a table
Base.

What is Mapped[str]?
- Column type annotation
- A string
- A query
- A table
* Correct answer: Column type annotation
Typed.

What is a session?
- Unit of work
- Table
- Model
- Engine
* Correct answer: Unit of work
Add/query.

What does session.add do?
- Stages an object
- Saves immediately
- Deletes
- Queries
* Correct answer: Stages an object
Needs commit.

What does commit do?
- Flushes to DB
- Reads
- Rolls back
- Closes
* Correct answer: Flushes to DB
Persist.

How to query?
- session.query(Model).filter(...)
- SELECT
- model.find
- all()
* Correct answer: session.query(Model).filter(...)
ORM.

What is filter_by?
- Simple equality filter
- Raw SQL
- Ordering
- Limit
* Correct answer: Simple equality filter
Shorthand.

What is the PostgreSQL URL scheme?
- postgresql+psycopg://
- sqlite://
- mysql://
- orm://
* Correct answer: postgresql+psycopg://
Driver.

What does create_all do?
- Creates tables
- Drops
- Reads
- Migrates
* Correct answer: Creates tables
From models.

Is SQLAlchemy cross-DB?
- Yes
- No
- SQLite only
- Postgres only
* Correct answer: Yes
Dialects.
<!--/QUIZ-->
