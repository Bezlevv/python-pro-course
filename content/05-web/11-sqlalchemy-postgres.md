---
title: SQLAlchemy и PostgreSQL
summary: ORM, движок Engine, сессии, модели, связи между таблицами и работа с PostgreSQL через SQLAlchemy 2.0.
order: 11
duration: 45 мин
difficulty: advanced
tags: sqlalchemy, postgresql, orm, базы данных, модели
---

В прошлом уроке мы писали SQL вручную через модуль `sqlite3`. Это работает, но в большом проекте хочется работать с базой как с обычными объектами Python: не собирать строки SQL, а просто создавать классы и вызывать методы. Именно это даёт **ORM** (Object-Relational Mapping) — прослойка между Python и базой. Самый популярный ORM в мире Python — **SQLAlchemy**. В этом уроке мы изучим его на примере PostgreSQL — промышленной базы данных, которую используют почти все серьёзные веб-приложения.

## Что такое SQLAlchemy

SQLAlchemy состоит из двух уровней:

- **Core** — низкоуровневая работа с SQL: движок, соединения, текст запросов. Это как `sqlite3`, но для любой базы.
- **ORM** — высокоуровневая работа: ты описываешь модели (классы Python), а SQLAlchemy сам превращает их в таблицы и запросы.

Работать мы будем с ORM, но понимать Core полезно — именно там живёт движок и сессии.

## Установка и подключение к PostgreSQL

Установим SQLAlchemy и драйвер для PostgreSQL — `psycopg2`:

```bash
pip install sqlalchemy psycopg2-binary
```

Теперь создадим движок — объект, который умеет подключаться к базе. Строка подключения описывает базу, пользователя и пароль:

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://user:password@localhost:5432/mydb",
    echo=True,  # показывать SQL-запросы в консоли
)
```

Если у тебя нет PostgreSQL под рукой, для экспериментов подойдёт та же схема, но с SQLite — SQLAlchemy умеет и в неё, и код менять почти не придётся:

```python
engine = create_engine("sqlite:///local.db", echo=True)
```

Движок сам не создаёт таблицы — он только управляет соединениями. Таблицы создаются через модели.

## Модели: таблицы как классы

В SQLAlchemy 2.0 модель — это класс, унаследованный от `DeclarativeBase`. Каждый атрибут класса — столбец таблицы:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
```

Обрати внимание на аннотации `Mapped[...]` — именно по ним SQLAlchemy понимает тип столбца. `mapped_column` позволяет добавить детали: длину строк, первичный ключ и так далее.

Чтобы создать таблицу в базе, достаточно вызвать:

```python
Base.metadata.create_all(engine)
```

Эта команда создаст все таблицы, описанные в моделях, если их ещё нет.

## Сессии и CRUD

Сессия — это «рабочее пространство»: ты добавляешь объекты, меняешь их, а потом одним разом фиксируешь всё в базе. Сессии создаются фабрикой `sessionmaker`:

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

Добавление записи — создай объект модели и добавь его в сессию:

```python
book = Book(title="Война и мир", author="Лев Толстой", year=1869)
session.add(book)
session.commit()  # только теперь данные реально попали в базу
```

Пока не вызван `commit()`, изменения «живут» только в сессии. Если что-то пошло не так, можно откатить всё через `session.rollback()`.

Чтение данных делается через `select()`:

```python
from sqlalchemy import select

books = session.scalars(select(Book)).all()
for book in books:
    print(book.title, book.year)
```

Фильтрация — метод `where`:

```python
old_books = session.scalars(
    select(Book).where(Book.year < 1900)
).all()
```

Обновление — просто измени атрибут и зафиксируй:

```python
book = session.scalars(select(Book).where(Book.title == "Война и мир")).one()
book.year = 1868
session.commit()
```

Удаление:

```python
session.delete(book)
session.commit()
```

## Связи между таблицами

В реальном приложении таблицы связаны: у пользователя есть посты, у заказа — товары. В SQLAlchemy связь описывается через `ForeignKey` и `relationship`:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

Теперь можно пройти по связи в обе стороны:

```python
user = User(name="Аня")
session.add(user)
session.flush()  # получить id без commit

post = Post(title="Мой первый пост", user_id=user.id)
session.add(post)
session.commit()

# Аня и её посты
print(user.posts[0].title)
```

## Почему ORM, а не чистый SQL

ORM защищает от SQL-инъекций (значения всегда экранируются), упрощает перенос между базами (SQLite → PostgreSQL — смена одной строки подключения) и делает код читаемым. Но за удобство приходится платить: сложные запросы на ORM бывают медленнее ручного SQL. Поэтому в больших проектах используют комбинацию: ORM для типовых операций, а «сырой» SQL — для тяжёлой аналитики.

## Как устроен путь запроса

Прежде чем перейти к практике, соберём в одну картину всё, что делает SQLAlchemy: от класса-модели до строки в PostgreSQL.

```mermaid
flowchart LR
    A["Модели: Mapped"] --> B["Session: add / select"]
    B --> C["commit()"]
    C --> D["Engine"]
    D --> E["PostgreSQL"]
    F["Base.metadata.create_all"] --> D
```

`create_all` проходит по метаданным моделей и создаёт таблицы; дальше все операции идут через сессию, а сессия — через движок, который держит пул соединений с конкретной базой.

## Итог урока

Мы узнали: как устроен SQLAlchemy (Core и ORM), как создать движок и подключиться к PostgreSQL, как описывать модели через `Mapped`/`mapped_column`, как работать с сессиями, выполнять CRUD и задавать связи между таблицами. Это фундамент для любого современного веб-приложения на Python.

<!--TASK-->
### Задача 1
Напиши скрипт `library.py`, который:

1. Создаёт движок SQLite (`sqlite:///library.db`) — так проще проверить, а код одинаково заработает и с PostgreSQL.
2. Описывает две модели: `Author` (id, name) и `Book` (id, title, year, author_id — внешний ключ на `authors.id`), связанные через `relationship`.
3. Создаёт таблицы через `Base.metadata.create_all(engine)`.
4. Добавляет двух авторов и по книге каждому: Толстой — «Война и мир» (1869), Пушкин — «Евгений Онегин» (1833).
5. Выводит на экран имена всех авторов и их книги, например: `Лев Толстой: Война и мир (1869)`.

Запусти скрипт и убедись, что в выводе обе книги и оба автора.

### Задача 2
Создай скрипт `crud.py`. Опиши модель `Book` (id, title, year, rating — число с плавающей точкой) и создай таблицы через `Base.metadata.create_all(engine)` с движком `sqlite:///crud.db`. Добавь через `session.add_all` три книги: «Цветы для Элджернона» (1966, рейтинг 4.9), «Солярис» (1961, 4.5), «Дюна» (1965, 4.8). Затем: 1) найди «Солярис» и поменяй ему рейтинг на 4.7, 2) удали «Дюна», 3) выведи оставшиеся книги в формате `Название (год): рейтинг`, отсортировав по году. Запусти скрипт и опиши ожидаемый вывод.

### Задача 3
Создай скрипт `filter_books.py`. Используй модель `Book` из задачи 2 (та же база `crud.db`). Выбери все книги, изданные после 1960 года, отсортированные по году по убыванию: `select(Book).where(Book.year > 1960).order_by(Book.year.desc())`. Выведи список и количество книг (через `len(...)`). Дополнительно выведи самую раннюю книгу из отобранных через `.first()`. Запусти скрипт и опиши ожидаемый вывод.

### Задача 4
Создай скрипт `find_author.py` с моделями `Author` (id, name) и `Book` (id, title, year, author_id + внешний ключ). Добавь двух авторов и по одной книге каждому. Напиши функцию `book_year(title)`, которая возвращает год книги по названию, а если такой книги нет — возвращает None. Вызови её с существующим названием (например, «Война и мир») и с несуществующим, выведи результат: год либо строку `Не найдено`. Запусти скрипт и опиши ожидаемый вывод.

### Задача 5
Доработай скрипт из задачи 4 (сохрани его как `relations.py`): добавь третьего автора и две его книги. Затем: 1) найди автора по имени через `select(Author).where(Author.name == ...)` и через `author.books` выведи все его книги в формате `Название (год)`; 2) найди одну конкретную книгу и выведи её автора через `book.author.name`; 3) выведи суммарное количество книг у каждого автора через `len(author.books)`. Запусти скрипт и опиши ожидаемый вывод.
### Задача 6
Создай скрипт `report.py` с базой `sqlite:///report.db`. Опиши модели `Author` (id, name) и `Book` (id, title, year, author_id с внешним ключом) — как в задаче 1. Добавь авторов: Лев Толстой, Эрих Мария Ремарк, Александр Пушкин и Николая Гоголя (у Гоголя книг не будет). Книги: Толстой — «Война и мир» (1869), «Анна Каренина» (1877), «Воскресение» (1899); Ремарк — «Три товарища» (1936), «На Западном фронте без перемен» (1929); Пушкин — «Евгений Онегин» (1833). Затем одним запросом с `select(Author.name, func.count(Book.id))`, `join` и `group_by` выведи, сколько книг у каждого автора: сначала строку `Авторов с книгами: N`, потом по строке `Имя: количество` в порядке убывания числа книг (при равенстве — по алфавиту), в конце `Всего книг: M`. Запусти скрипт и опиши ожидаемый вывод. Обрати внимание, попал ли Гоголь в отчёт и почему.

### Задача 7
Создай скрипт `unique_email.py` с базой `sqlite:///subscribers.db`. Опиши модель `Subscriber` (id, `email: Mapped[str] = mapped_column(unique=True)`). Напиши функцию `subscribe(session, email) -> bool`: она добавляет подписчика и делает `commit()`; если база отвергла вставку из-за дубликата (`IntegrityError`), функция делает `rollback()` и возвращает `False`, иначе `True`. Вызови функцию для адресов `anya@example.com`, `borya@example.com` и снова `anya@example.com`, печатая `Добавлен: <email>` или `Дубликат отклонён: <email>`. В конце посчитай подписчиков через `select(func.count(Subscriber.id))` и выведи `В базе: N подписчика`. Запусти скрипт: третий вызов не должен ломать программу и не должен добавлять вторую запись.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Вспомни шаги: создай `Base` (DeclarativeBase), опиши модели, добавь `ForeignKey("authors.id")` в модель книги и `relationship` с `back_populates` в обе стороны. После `session.add(...)` не забывай `session.commit()`. Чтобы пройти по связи, используй `author.books` — список книг автора. Для вывода — цикл `for` по всем авторам.

### Подсказка 2
Выборка одной записи: `session.scalars(select(Book).where(Book.title == "...")).one()`. После изменения атрибута достаточно `session.commit()`. Для удаления используй `session.delete(book)`. Сортировка: `select(Book).order_by(Book.year)`.

### Подсказка 3
`where(Book.year > 1960)` — фильтр, `.order_by(Book.year.desc())` — убывающая сортировка. `session.scalars(...).all()` вернёт список моделей, `len()` посчитает их количество. `.first()` вернёт первый элемент выборки или None, если выборка пуста.

### Подсказка 4
`session.scalars(select(Book).where(Book.title == title)).first()` вернёт объект книги или None. В функции верни `book.year if book else None`. В основном коде проверяй: `if year is None: print("Не найдено")`.

### Подсказка 5
`relationship` с `back_populates` позволяет ходить по связи в обе стороны: `author.books` — список книг автора, `book.author` — объект автора. Не забудь `session.add_all` и `session.commit()` до чтения. Порядок книг в `author.books` не гарантирован — при желании отсортируй список в коде.
### Подсказка 6
Агрегаты живут в `sqlalchemy.func`: `from sqlalchemy import func`. Запрос: `select(Author.name, func.count(Book.id)).join(Book, Book.author_id == Author.id).group_by(Author.id).order_by(func.count(Book.id).desc(), Author.name)`. `session.execute(stmt)` вернёт строки-кортежи `(name, count)`, которые удобно распаковать в цикле `for name, total in session.execute(stmt)`. `join` — внутреннее соединение: авторы без книг в выборку не попадают, поэтому Гоголя в отчёте не будет. Сумму книг по всем авторам считай отдельным запросом `select(func.count(Book.id))`.

### Подсказка 7
`unique=True` в `mapped_column` создаёт в таблице ограничение уникальности: база физически не даст вставить второй такой же email. Нарушение проявляется на `commit()` как `sqlalchemy.exc.IntegrityError` — импортируй его явно. После ошибки обязателен `session.rollback()`: без него сессия останется в нерабочем состоянии, и следующий `add`/`commit` упадёт с `PendingRollbackError`. Счётчик: `session.scalar(select(func.count(Subscriber.id)))`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Одно из возможных решений:

```python
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import select

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

engine = create_engine("sqlite:///library.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

tolstoy = Author(name="Лев Толстой")
pushkin = Author(name="Александр Пушкин")
session.add_all([tolstoy, pushkin])
session.flush()

session.add_all([
    Book(title="Война и мир", year=1869, author_id=tolstoy.id),
    Book(title="Евгений Онегин", year=1833, author_id=pushkin.id),
])
session.commit()

authors = session.scalars(select(Author)).all()
for author in authors:
    for book in author.books:
        print(f"{author.name}: {book.title} ({book.year})")
```

Результат:

```
Лев Толстой: Война и мир (1869)
Александр Пушкин: Евгений Онегин (1833)
```

Разбор шагов. `Base` — общий предок всех моделей; через него `metadata.create_all` узнаёт, какие таблицы создавать. В моделях `Mapped[t]` задаёт тип столбца, `ForeignKey("authors.id")` — ссылку на родительскую таблицу, а `relationship` — объектную связь: `author.books` вернёт список книг, `book.author` — автора. `session.add_all` добавляет сразу несколько объектов; `flush()` записывает их в базу и выдаёт id, не фиксируя окончательно. После `commit()` данные гарантированно сохранены, и можно читать их через `select(Author)` — вывод показывает, что связи работают в обе стороны.

### Разбор 2
Полный код `crud.py`:

```python
from sqlalchemy import create_engine, select, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    rating: Mapped[float] = mapped_column(Float)

engine = create_engine("sqlite:///crud.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    Book(title="Цветы для Элджернона", year=1966, rating=4.9),
    Book(title="Солярис", year=1961, rating=4.5),
    Book(title="Дюна", year=1965, rating=4.8),
])
session.commit()

book = session.scalars(select(Book).where(Book.title == "Солярис")).one()
book.rating = 4.7

dune = session.scalars(select(Book).where(Book.title == "Дюна")).one()
session.delete(dune)

session.commit()

books = session.scalars(select(Book).order_by(Book.year)).all()
for b in books:
    print(f"{b.title} ({b.year}): {b.rating}")
```

Ожидаемый вывод:

```
Солярис (1961): 4.7
Цветы для Элджернона (1966): 4.9
```

Разбор: `add_all` добавляет три объекта в сессию, `commit()` фиксирует их. Поиск книги выполняется через `select(Book).where(Book.title == "...")` — `one()` требует ровно одну строку и бросает ошибку, если совпадений несколько. Изменение сводится к присваиванию атрибута `book.rating = 4.7` — SQLAlchemy отслеживает изменения и сгенерирует `UPDATE` при `commit()`. Удаление через `session.delete(dune)` тоже реально произойдёт только после `commit()`. Финальный запрос с `order_by(Book.year)` выводит оставшиеся книги по возрастанию года — «Дюна» пропала, рейтинг «Солярис» обновлён.

### Разбор 3
Полный код `filter_books.py`:

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    rating: Mapped[float] = mapped_column()

engine = create_engine("sqlite:///crud.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

stmt = select(Book).where(Book.year > 1960).order_by(Book.year.desc())
books = session.scalars(stmt).all()

print("Книги после 1960 года:")
for b in books:
    print(f"{b.year} — {b.title}")
print(f"Всего: {len(books)}")

first = session.scalars(select(Book).where(Book.year > 1960).order_by(Book.year)).first()
if first is not None:
    print(f"Самая ранняя: {first.title} ({first.year})")
```

Ожидаемый вывод (при данных из задачи 2):

```
Книги после 1960 года:
1966 — Цветы для Элджернона
1961 — Солярис
Всего: 2
Самая ранняя: Солярис (1961)
```

Разбор: `where(Book.year > 1960)` превращается SQLAlchemy в SQL-условие `WHERE year > 1960`, а `order_by(Book.year.desc())` — в `ORDER BY year DESC`. `session.scalars(...).all()` возвращает список объектов модели, поэтому `len(books)` даёт количество. Второй запрос использует `.first()` с возрастающей сортировкой — он вернёт первую (самую раннюю) книгу из отобранных или None, если выборка пуста; проверка `if first is not None` защищает от ошибки при пустой базе.

### Разбор 4
Полный код `find_author.py`:

```python
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

engine = create_engine("sqlite:///find.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

tolstoy = Author(name="Лев Толстой")
pushkin = Author(name="Александр Пушкин")
session.add_all([tolstoy, pushkin])
session.flush()
session.add_all([
    Book(title="Война и мир", year=1869, author_id=tolstoy.id),
    Book(title="Евгений Онегин", year=1833, author_id=pushkin.id),
])
session.commit()

def book_year(title: str):
    book = session.scalars(select(Book).where(Book.title == title)).first()
    return book.year if book else None

for title in ("Война и мир", "Капитанская дочка"):
    year = book_year(title)
    if year is None:
        print(f"{title}: Не найдено")
    else:
        print(f"{title}: {year}")
```

Ожидаемый вывод:

```
Война и мир: 1869
Капитанская дочка: Не найдено
```

Разбор: `.first()` вместо `.one()` — ключевой приём: он возвращает первый подходящий объект или None, если ничего не найдено, и никогда не бросает исключение. Функция `book_year` использует тернарный оператор `book.year if book else None` — так несуществующая книга превращается в None. В основном цикле мы проверяем результат и печатаем либо год, либо «Не найдено». Такой паттерн поиска «найдено или нет» — база для логики веб-приложений: например, проверка существования пользователя перед входом.

### Разбор 5
Полный код `relations.py`:

```python
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

engine = create_engine("sqlite:///relations.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

tolstoy = Author(name="Лев Толстой")
pushkin = Author(name="Александр Пушкин")
remarque = Author(name="Эрих Мария Ремарк")
session.add_all([tolstoy, pushkin, remarque])
session.flush()

session.add_all([
    Book(title="Война и мир", year=1869, author_id=tolstoy.id),
    Book(title="Евгений Онегин", year=1833, author_id=pushkin.id),
    Book(title="На Западном фронте без перемен", year=1929, author_id=remarque.id),
    Book(title="Три товарища", year=1936, author_id=remarque.id),
])
session.commit()

authors = session.scalars(select(Author)).all()
for author in authors:
    print(f"{author.name}: книг — {len(author.books)}")
    for book in author.books:
        print(f"  {book.title} ({book.year})")

some_book = session.scalars(select(Book).where(Book.title == "Три товарища")).one()
print(f"Автор книги «Три товарища»: {some_book.author.name}")
```

Ожидаемый вывод:

```
Лев Толстой: книг — 1
  Война и мир (1869)
Александр Пушкин: книг — 1
  Евгений Онегин (1833)
Эрих Мария Ремарк: книг — 2
  На Западном фронте без перемен (1929)
  Три товарища (1936)
Автор книги «Три товарища»: Эрих Мария Ремарк
```

Разбор: третий автор добавлен с двумя книгами — это наглядный пример отношения «один ко многим»: один автор, много книг. `author.books` возвращает список связанных книг, поэтому `len(author.books)` показывает их количество. Обратный ход — `book.author` — возвращает объект автора книги. Обе стороны связи работают благодаря `relationship(back_populates=...)`: SQLAlchemy и синхронизирует, и грузит связанные объекты при обращении. Именно так в реальных приложениях строятся связи «пользователь — его посты», «автор — его статьи» и так далее.
### Разбор 6
Полный код `report.py`:

```python
from sqlalchemy import create_engine, ForeignKey, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

engine = create_engine("sqlite:///report.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

tolstoy = Author(name="Лев Толстой")
remarque = Author(name="Эрих Мария Ремарк")
pushkin = Author(name="Александр Пушкин")
gogol = Author(name="Николай Гоголь")
session.add_all([tolstoy, remarque, pushkin, gogol])
session.flush()

session.add_all([
    Book(title="Война и мир", year=1869, author_id=tolstoy.id),
    Book(title="Анна Каренина", year=1877, author_id=tolstoy.id),
    Book(title="Воскресение", year=1899, author_id=tolstoy.id),
    Book(title="Три товарища", year=1936, author_id=remarque.id),
    Book(title="На Западном фронте без перемен", year=1929, author_id=remarque.id),
    Book(title="Евгений Онегин", year=1833, author_id=pushkin.id),
])
session.commit()

stmt = (
    select(Author.name, func.count(Book.id))
    .join(Book, Book.author_id == Author.id)
    .group_by(Author.id)
    .order_by(func.count(Book.id).desc(), Author.name)
)
rows = session.execute(stmt).all()

print(f"Авторов с книгами: {len(rows)}")
for name, total in rows:
    print(f"{name}: {total}")

print(f"Всего книг: {session.scalar(select(func.count(Book.id)))}")
```

Ожидаемый вывод:

```
Авторов с книгами: 3
Лев Толстой: 3
Эрих Мария Ремарк: 2
Александр Пушкин: 1
Всего книг: 6
```

Разбор: `select(Author.name, func.count(Book.id))` — это уже не выборка целых объектов, а выборка двух колонок, поэтому `session.execute(...)` возвращает строки-кортежи, а не модели; распаковка `for name, total in rows` работает именно благодаря этому. `join(Book, Book.author_id == Author.id)` превращается в SQL `JOIN books ON books.author_id = authors.id`, а `group_by(Author.id)` — в `GROUP BY authors.id`: база сама считает количество строк в каждой группе. Сортировка по `func.count(Book.id).desc()` ставит наверх самого плодовитого автора, второй ключ `Author.name` делает порядок предсказуемым при равном числе книг. Гоголь в отчёте отсутствует: `join` — внутреннее соединение, и автор без книг теряется. Если нужны и «нулевые» авторы, берут `outerjoin` и `func.coalesce(func.count(Book.id), 0)`. Агрегатные запросы вроде этого — типовой способ строить отчёты и счётчики для дашбордов, не выгружая все строки в Python.

### Разбор 7
Полный код `unique_email.py`:

```python
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase):
    pass

class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)

engine = create_engine("sqlite:///subscribers.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def subscribe(session, email: str) -> bool:
    session.add(Subscriber(email=email))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return False
    return True

for email in ("anya@example.com", "borya@example.com", "anya@example.com"):
    if subscribe(session, email):
        print(f"Добавлен: {email}")
    else:
        print(f"Дубликат отклонён: {email}")

total = session.scalar(select(func.count(Subscriber.id)))
print(f"В базе: {total} подписчика")
```

Ожидаемый вывод:

```
Добавлен: anya@example.com
Добавлен: borya@example.com
Дубликат отклонён: anya@example.com
В базе: 2 подписчика
```

Разбор: `unique=True` — это не проверка в Python, а ограничение самой таблицы: SQLite (и PostgreSQL) создаёт уникальный индекс по столбцу `email` и физически не пропустит вторую такую строку. `session.add(...)` лишь кладёт объект в сессию, а реальный `INSERT` уходит в базу на `commit()` — именно там и возникает `IntegrityError`. Перехватив исключение, мы обязаны вызвать `session.rollback()`: после неудачной фиксации сессия остаётся в состоянии «транзакция сломана», и любой следующий запрос упадёт с `PendingRollbackError`. `rollback()` откатывает неудавшуюся вставку и возвращает сессию в рабочее состояние, поэтому третий вызов спокойно обрабатывается, а счётчик показывает 2. Такой приём «попробовать вставить — обработать конфликт» надёжнее предварительной проверки `select`: между проверкой и вставкой другой процесс может успеть добавить ту же запись, и только ограничение базы даёт настоящую гарантию.
<!--/SOLUTION-->

<!--QUIZ-->
Что из перечисленного делает SQLAlchemy ORM?
- Только ускоряет сервер
- Позволяет работать с таблицами базы данных как с обычными классами Python
- Заменяет собой PostgreSQL
- Автоматически создаёт веб-интерфейс
* Правильный ответ: Позволяет работать с таблицами базы данных как с обычными классами Python
ORM превращает строки таблиц в объекты Python: класс модели — таблица, экземпляр — строка, атрибут — столбец.

Зачем нужен вызов session.commit()?
- Чтобы соединиться с базой данных
- Чтобы сохранить все изменения сессии в базе данных
- Чтобы создать таблицы
- Чтобы закрыть соединение
* Правильный ответ: Чтобы сохранить все изменения сессии в базе данных
До commit() изменения живут только в памяти сессии; commit() фиксирует их в базе, а rollback() отменяет.

Чем SQLAlchemy Core отличается от ORM?
- Core — это низкоуровневый API для работы с SQL, ORM — высокоуровневый поверх него
- Core работает только с PostgreSQL, ORM — только с SQLite
- Это два разных языка программирования
- Ничем не отличаются
* Правильный ответ: Core — это низкоуровневый API для работы с SQL, ORM — высокоуровневый поверх него
Core даёт прямой контроль над запросами и соединениями, а ORM надстраивает модели и объектные связи.

Что произойдёт, если поменять строку подключения с sqlite:///local.db на postgresql+psycopg2://...?
- Придётся переписать все модели
- Ничего: модели и код останутся теми же, изменится только движок
- ORM перестанет работать
- База удалится
* Правильный ответ: Ничего: модели и код останутся теми же, изменится только движок
Одно из главных преимуществ ORM — смена базы почти не требует правки кода: меняется лишь строка подключения.

Как задать связь «один ко многим» между таблицами users и posts?
- Добавить столбец id в обе таблицы
- Добавить в posts столбец user_id с ForeignKey("users.id") и relationship в обеих моделях
- Написать UNION SELECT
- Связать через поле title
* Правильный ответ: Добавить в posts столбец user_id с ForeignKey("users.id") и relationship в обеих моделях
Внешний ключ хранит id родительской записи, а relationship даёт удобный доступ к связанным объектам (author.posts, post.author).

Как создать все таблицы, описанные в моделях?
- session.commit()
- Base.metadata.create_all(engine)
- engine.create_tables()
- models.migrate()
* Правильный ответ: Base.metadata.create_all(engine)
Эта команда создаёт отсутствующие таблицы для всех моделей, унаследованных от Base.

Что вернёт session.scalars(select(Book)).all()?
- SQL-строку
- Список объектов Book
- Словарь записей
- Число записей
* Правильный ответ: Список объектов Book
scalars() возвращает скалярные значения — объекты моделей; .all() собирает их в список.

Зачем нужен session.flush()?
- Чтобы закрыть сессию
- Чтобы отправить изменения в базу и получить id, не фиксируя их окончательно
- Чтобы откатить изменения
- Чтобы удалить таблицу
* Правильный ответ: Чтобы отправить изменения в базу и получить id, не фиксируя их окончательно
flush() выполняет INSERT в базе, после чего объект получает id — но commit() ещё не происходил, и изменения можно откатить.
Как посчитать количество книг у каждого автора одним запросом?
- Загрузить всех авторов и вызвать len(author.books) в цикле
- Использовать func.count(Book.id) вместе с join и group_by
- Вызвать session.commit() несколько раз
- Отсортировать книги по году
* Правильный ответ: Использовать func.count(Book.id) вместе с join и group_by
Агрегат func.count в паре с group_by заставляет базу посчитать строки в каждой группе — без выгрузки всех объектов в Python.

Что нужно сделать сразу после исключения IntegrityError при commit()?
- Ничего, сессия восстановится сама
- Вызвать session.rollback(), иначе сессия останется в нерабочем состоянии
- Закрыть движок engine.dispose()
- Повторить тот же commit() без изменений
* Правильный ответ: Вызвать session.rollback(), иначе сессия останется в нерабочем состоянии
После неудачной фиксации транзакция сломана: без rollback() следующая операция упадёт с PendingRollbackError.

Что вернёт session.get(Book, 42), если книги с id 42 нет?
- Исключение NoResultFound
- None
- Пустой список
- Новый объект Book
* Правильный ответ: None
session.get() ищет по первичному ключу и возвращает None при отсутствии записи — удобно для проверок вида «есть или нет».

Зачем в mapped_column указывают unique=True?
- Чтобы база сама не допускала повторяющихся значений в этом столбце
- Чтобы ускорить создание таблиц
- Чтобы столбец стал первичным ключом
- Чтобы значение шифровалось
* Правильный ответ: Чтобы база сама не допускала повторяющихся значений в этом столбце
Это ограничение на уровне схемы: создаётся уникальный индекс, и повторная вставка отклоняется с IntegrityError.
<!--/QUIZ-->
