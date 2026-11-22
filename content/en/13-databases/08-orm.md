---
title: ORM: SQLAlchemy and Django ORM
summary: Models, queries, migrations.
order: 8
duration: 50 min
difficulty: advanced
tags: orm, sqlalchemy, django
---

ORM maps tables to Python classes.

## SQLAlchemy

```python
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine("sqlite:///app.db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add(User(name="Alice"))
    session.commit()
```

## Django ORM

```python
users = User.objects.filter(name__startswith="A")
user = User.objects.create(name="Bob")
```

## Lesson summary

ORM avoids writing raw SQL for routine work.

<!--TASK-->
### Task 1 — Engine
Create an engine.

### Task 2 — Model
Define a User model.

### Task 3 — Create
Create tables.

### Task 4 — Add
Add a user via session.

### Task 5 — Query
Query users.

### Task 6 — Django
Filter with Django ORM.

### Task 7 — Migrations
Explain why migrations.
<!--/TASK-->

<!--HINT-->
### Hint 1
create_engine.

### Hint 2
mapped_column.

### Hint 3
create_all.

### Hint 4
session.add.

### Hint 5
session.query.

### Hint 6
objects.filter.

### Hint 7
Schema changes.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///app.db")
```

### Solution 2
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
```

### Solution 3
```python
Base.metadata.create_all(engine)
```

### Solution 4
```python
with Session(engine) as session:
    session.add(User(name="Alice"))
    session.commit()
```

### Solution 5
```python
with Session(engine) as session:
    for user in session.query(User).all():
        print(user.id, user.name)
```

### Solution 6
```python
# Django
users = User.objects.filter(name__startswith="A")
# SQLAlchemy
users = session.query(User).filter(User.name.like("A%"))
```

### Solution 7
```python
# Миграции применяют изменения схемы к базе
# и хранят историю изменений
```
<!--/SOLUTION-->

<!--QUIZ-->
What is ORM?
- Object-relational mapping
- A database
- Raw SQL
- None
* Correct answer: Object-relational mapping
Classes.

What is a model?
- Table class
- A row
- A query
- None
* Correct answer: Table class
Definition.

What is a session?
- Work unit
- Engine
- Table
- None
* Correct answer: Work unit
Connection.

What is create_all?
- Creates tables
- Deletes
- Queries
- None
* Correct answer: Creates tables
DDL.

What is mapped_column?
- Column definition
- A table
- A query
- None
* Correct answer: Column definition
Type.

What is session.add?
- Stages an object
- Saves
- Deletes
- None
* Correct answer: Stages an object
Pending.

What is commit?
- Persists
- Cancels
- Reads
- None
* Correct answer: Persists
Flush.

What is query?
- Selects
- Inserts
- Creates
- None
* Correct answer: Selects
Retrieve.

What is a migration?
- Schema change
- Data copy
- Backup
- None
* Correct answer: Schema change
Versioned.

What is filter?
- Condition
- Sort
- Limit
- None
* Correct answer: Condition
WHERE.

What is __tablename__?
- Table name
- Class name
- Key
- None
* Correct answer: Table name
Meta.

Why ORM?
- Less SQL
- Faster always
- Required
- None
* Correct answer: Less SQL
Productivity.
<!--/QUIZ-->
