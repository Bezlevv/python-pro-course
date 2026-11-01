---
title: Продвинутый ORM: N+1, select_related, bulk
summary: SQLAlchemy и Django ORM: модель и сессия, проблема N+1, жадная загрузка (selectinload, select_related) и массовые операции bulk.
order: 4
duration: 45 мин
difficulty: advanced
tags: orm, sqlalchemy, django, n+1, bulk
---

## Что такое ORM

ORM (Object-Relational Mapping) — это мост между таблицами базы данных и объектами Python. Ты работаешь с классами и методами, а не с SQL-строками, а ORM сам превращает вызовы в запросы. Самые популярные варианты в Python — SQLAlchemy (гибкий, используется в FastAPI и многих приложениях) и встроенный Django ORM. Перед запуском примеров установи библиотеку: `pip install sqlalchemy`.

## SQLAlchemy: модель и сессия

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, Session, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
```

Сессия — рабочая область, где живут объекты, и фабрика запросов:

```python
with Session(engine) as session:
    a = Author(name="Аня")
    session.add(a)
    session.flush()          # назначаем id без коммита
    session.add_all([
        Book(title="Книга 1", price=500, author=a),
        Book(title="Книга 2", price=700, author=a),
    ])
    session.commit()
```

Объекты попадают в базу только после flush/commit. Пока не закоммичено, изменения видны лишь внутри сессии.

## Проблема N+1

Это главная ловушка ORM. Она возникает, когда мы сначала загружаем N родителей, а потом в цикле для каждого обращаемся к его детям — каждый такой доступ превращается в отдельный SQL-запрос.

```python
with Session(engine) as session:
    authors = session.query(Author).all()      # 1 запрос
    for auth in authors:
        _ = auth.books                        # ещё 1 запрос на каждого автора
```

Итог: 1 + N запросов. Для 200 авторов — 201 обращение к базе вместо двух. На локальной базе это незаметно, но в продакшене с сетью каждая задержка суммируется.

## Жадная загрузка: selectinload / joinedload

Решение — загрузить связи сразу, одним-двумя запросами:

```python
from sqlalchemy.orm import selectinload

with Session(engine) as session:
    authors = session.query(Author).options(
        selectinload(Author.books)
    ).all()
```

`selectinload` делает второй запрос, который получает книги всех авторов разом (условие IN). `joinedload` использует JOIN и делает один запрос, но умножает строки — при пагинации это опасно. Правило: для коллекций обычно берут selectinload, для скалярных связей (ForeignKey) — joinedload.

## Django ORM: select_related и prefetch_related

В Django эквиваленты:

- `select_related()` — для ForeignKey и OneToOne (через JOIN, один запрос);
- `prefetch_related()` — для ManyToMany и обратных связей (отдельным запросом с IN).

```python
users = User.objects.select_related("profile").prefetch_related("orders")
```

Плюс полезные приёмы: `iterator()` для потокового чтения больших выборок и `only()`/`defer()` для загрузки не всех колонок.

## Массовые операции: bulk

Добавление тысяч объектов по одному — боль: каждый add + flush = отдельный запрос. Экономный вариант:

```python
from sqlalchemy.orm import bulk_insert_mappings

rows = [{"title": f"Книга {i}", "price": 100.0, "author_id": 1}
        for i in range(5000)]
with Session(engine) as session:
    session.bulk_insert_mappings(Book, rows)
    session.commit()
```

`bulk_insert_mappings` упаковывает тысячи строк в несколько INSERT. В Django соответствие — `Model.objects.bulk_create([...])`, а для обновления — `bulk_update`. Важно: bulk-операции обходят жизненный цикл ORM — не вызывают события (сигналы в Django), не синхронизируют объекты, уже находящиеся в памяти. Используй их там, где главное скорость, а не бизнес-логика.

## Когда ORM мешает

ORM хорош для 95% задач, но сложные отчёты, оконные функции и массовая трансформация данных часто проще и быстрее на сыром SQL. Компромисс — `session.execute(text("..."))` c параметрами, который возвращает Row-объекты.

## Итог

Главные правила продвинутого использования ORM: следи за количеством запросов (N+1), загружай связи жадно там, где они нужны, и применяй bulk для пачек данных. Замеряй число запросов до и после оптимизаций.

<!--TASK-->
### Задача 1
Напиши скрипт с моделями `Author` и `Book` (как в уроке, с колонкой price). Заполни базу: 5 авторов, у каждого по 3 книги. Подключи счётчик SQL-запросов через событие `event.listen(engine, "before_cursor_execute", counter)`. Затем в одной сессии выполни `session.query(Author).all()` и в цикле прочитай `len(author.books)` для каждого. Верни кортеж `(n_authors, n_queries)`. Ожидаемый вывод: `(5, 6)` — один запрос на авторов плюс пять запросов на книги.

### Задача 2
Модифицируй скрипт из задачи 1: загрузи авторов с `selectinload(Author.books)` и снова посчитай запросы. Верни `(n_authors, n_queries)`. Ожидаемый вывод: `(5, 2)` — один запрос на авторов и один массовый запрос на книги всех авторов.

### Задача 3
Напиши функцию `bulk_fill(session, n)`, которая вставляет `n` книг через `bulk_insert_mappings` (author_id = 1, цена 100.0). Верни кортеж `(n, count_in_db)`, где count_in_db — число строк в таблице books после вставки. Для `n=2000` ожидаемый вывод: `(2000, 2000)`.

### Задача 4
Напиши функцию `bulk_update_prices(session)`, которая повышает цену всех книг автора 1 на 10% через `bulk_update_mappings`. Верни кортеж `(updated, total_price)`, где updated — число обновлённых строк, total_price — сумма цен всех книг после обновления. Заполни базу: автор 1 с книгами по 100, 200, 300 (итог после обновления — 660.0). Ожидаемый вывод: `(3, 660.0)`.

### Задача 5
Напиши функцию `authors_with_book_counts(session)`, которая одним запросом (без N+1) возвращает список кортежей `(name, book_count)` для всех авторов, отсортированный по имени. Используй `session.query(Author, func.count(Book.id)).outerjoin(Book).group_by(Author.id).order_by(Author.name)`. Ожидаемый вывод: `[('Аня', 3), ('Борис', 3), ('Вера', 3), ('Глеб', 3), ('Дима', 3)]` — при база из 5 авторов по 3 книги.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Счётчик: `count = {"n": 0}`; `event.listen(engine, "before_cursor_execute", lambda conn, cur, stmt, params, context, executemany: count.__setitem__("n", count["n"] + 1))`. Создай авторов циклом: `for i in range(5): a = Author(name=["Аня","Борис","Вера","Глеб","Дима"][i]); session.add(a); session.flush(); session.add_all([Book(...)] for j in range(3))`. Важно: чтение `author.books` в цикле должно идти уже после завершения запроса на авторов.

### Подсказка 2
Добавь `.options(selectinload(Author.books))` к запросу авторов. Количество запросов должно упасть до двух: сами авторы + книги всех авторов одним запросом с IN. Проверь, что в сессии не осталось «ленивых» обращений.

### Подсказка 3
Используй `session.bulk_insert_mappings(Book, rows)` — rows — список словарей `{"title": ..., "price": 100.0, "author_id": 1}`. После commit посчитай `session.query(func.count(Book.id)).scalar()`. Обрати внимание: bulk_insert_mappings не возвращает id вставленных строк.

### Подсказка 4
Сначала прочитай список `(id, цена)` книг автора 1. Затем сформируй список словарей `{"id": row_id, "price": price * 1.1}` и передай в `session.bulk_update_mappings(Book, rows)`. Сумму посчитай запросом `SELECT SUM(price) FROM books`. Помни: после bulk_update_mappings сессия не знает о новых ценах — читай из базы заново.

### Подсказка 5
`session.query(Author, func.count(Book.id)).outerjoin(Book, Book.author_id == Author.id).group_by(Author.id).order_by(Author.name)` вернёт пары (Author, count). Преврати их в кортежи `(name, count)`. outerjoin нужен, чтобы авторы без книг тоже попали в результат с нулём.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, event
from sqlalchemy.orm import declarative_base, Session, relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

count = {"n": 0}
event.listen(engine, "before_cursor_execute",
            lambda conn, cur, stmt, params, context, executemany:
            count.__setitem__("n", count["n"] + 1))

names = ["Аня", "Борис", "Вера", "Глеб", "Дима"]
with Session(engine) as session:
    for i in range(5):
        a = Author(name=names[i])
        session.add(a)
        session.flush()
        session.add_all([
            Book(title=f"Книга {j}", price=100.0 * (j + 1), author=a)
            for j in range(3)
        ])
    session.commit()

    authors = session.query(Author).all()
    for auth in authors:
        _ = len(auth.books)
    print((len(authors), count["n"]))
```

Результат:

```
(5, 6)
```

Что здесь происходит? Запрос `session.query(Author).all()` — это одно обращение к базе. Но `author.books` — ленивая (lazy) связь: при первом обращении ORM выполняет отдельный запрос для каждого автора. Пять авторов — пять дополнительных запросов. Итог 1 + 5 = 6. Событие before_cursor_execute считает все реально выполненные SQL-операторы, включая служебные. Обрати внимание на flush: без него у авторов не было бы id, и вставка книг ссылалась бы на несуществующих авторов.

### Разбор 2
Решение:

```python
from sqlalchemy.orm import selectinload

# ... модели, engine, счётчик и заполнение базы как в задаче 1 ...

with Session(engine) as session:
    authors = session.query(Author).options(
        selectinload(Author.books)
    ).all()
    for auth in authors:
        _ = len(auth.books)
    print((len(authors), count["n"]))
```

Результат:

```
(5, 2)
```

Что здесь происходит? `selectinload` меняет стратегию загрузки связи books с ленивой на жадную: ORM сначала грузит авторов, а затем одним запросом с `WHERE author_id IN (...)` достаёт книги всех пяти авторов разом. `len(auth.books)` больше не порождает запросы — книги уже лежат в объектах. Итог: 2 запроса вместо 6. Для коллекций selectinload предпочтительнее joinedload: он не умножает строки авторов и не ломает пагинацию. В Django тот же эффект даёт prefetch_related, а для ForeignKey — select_related.

### Разбор 3
Решение:

```python
from sqlalchemy.orm import bulk_insert_mappings
from sqlalchemy import func

# ... модели, engine и заполнение базы (хотя бы один автор) ...

def bulk_fill(session, n):
    rows = [
        {"title": f"Книга {i}", "price": 100.0, "author_id": 1}
        for i in range(n)
    ]
    session.bulk_insert_mappings(Book, rows)
    session.commit()
    count_in_db = session.query(func.count(Book.id)).scalar()
    return (n, count_in_db)

with Session(engine) as session:
    print(bulk_fill(session, 2000))
```

Результат:

```
(2000, 2000)
```

Что здесь происходит? `bulk_insert_mappings` принимает список словарей и упаковывает их в несколько INSERT — по умолчанию кусками по 1000 строк. Это радикально быстрее, чем 2000 циклов с add и flush: каждый цикл — это отдельный сетевой кругосвет и отдельная компиляция запроса. Число строк в базе после вставки совпадает с запрошенным: 2000. Ограничение: bulk не возвращает сгенерированные id и не обновляет объекты в сессии, поэтому count_in_db мы читаем свежим запросом.

### Разбор 4
Решение:

```python
from sqlalchemy.orm import bulk_update_mappings
from sqlalchemy import func

# ... модели, engine, заполнение базы: автор 1 с книгами 100, 200, 300 ...

def bulk_update_prices(session):
    rows = session.query(Book.id, Book.price).filter(
        Book.author_id == 1
    ).all()
    updates = [
        {"id": row_id, "price": price * 1.1}
        for row_id, price in rows
    ]
    session.bulk_update_mappings(Book, updates)
    session.commit()
    total = session.query(func.sum(Book.price)).scalar()
    return (len(updates), total)

with Session(engine) as session:
    print(bulk_update_prices(session))
```

Результат:

```
(3, 660.0)
```

Что здесь происходит? Сначала читаем текущие id и цены книг автора 1: 100, 200, 300. Формируем список словарей с новыми ценами: 110, 220, 330. `bulk_update_mappings` выполняет UPDATE по каждому id — снова пачкой, а не по одному. Сумма цен после обновления — 660.0. Важная деталь: bulk_update_mappings не синхронизирует объекты в памяти, поэтому после неё мы читаем сумму прямо из базы, а не из локальных объектов. Это самый быстрый способ обновить большое число строк с вычисленными значениями.

### Разбор 5
Решение:

```python
from sqlalchemy import func

# ... модели, engine, заполнение базы: 5 авторов по 3 книги ...

def authors_with_book_counts(session):
    result = (
        session.query(Author.name, func.count(Book.id))
        .outerjoin(Book, Book.author_id == Author.id)
        .group_by(Author.id)
        .order_by(Author.name)
        .all()
    )
    return [(name, cnt) for name, cnt in result]

with Session(engine) as session:
    print(authors_with_book_counts(session))
```

Результат:

```
[('Аня', 3), ('Борис', 3), ('Вера', 3), ('Глеб', 3), ('Дима', 3)]
```

Что здесь происходит? Один запрос делает JOIN таблиц авторов и книг, группирует по автору и считает количество книг в каждой группе — без N+1 и без загрузки лишних объектов. `outerjoin` гарантирует, что автор без книг попадёт в результат со счётчиком 0. Условие соединения передаётся как аргумент outerjoin, потому что у обеих таблиц нет естественного FK-совпадения по имени колонки. Такой паттерн — стандарт для «лёгких» отчётов: считаем агрегаты в базе, а не в Python.
<!--/SOLUTION-->

<!--QUIZ-->
В чём суть проблемы N+1 в ORM?
- База отвечает N+1 раз на один запрос из-за репликации
- Сначала грузится N родителей, затем для каждого выполняется ещё по одному запросу
- Запросы выполняются по очереди, а не параллельно
- Индексы замедляют выборку
* Правильный ответ: Сначала грузится N родителей, затем для каждого выполняется ещё по одному запросу
Каждое обращение к ленивой связи порождает отдельный запрос: итог 1 + N обращений.

Чем selectinload отличается от joinedload?
- selectinload делает второй запрос с IN, joinedload использует JOIN (умножая строки)
- selectinload работает только в Django
- joinedload не поддерживает коллекции
- Разницы нет
* Правильный ответ: selectinload делает второй запрос с IN, joinedload использует JOIN (умножая строки)
Для коллекций чаще берут selectinload — он не ломает пагинацию, в отличие от умножения строк JOIN-ом.

Что в Django ORM соответствует selectinload для ManyToMany?
- select_related
- prefetch_related
- only()
- filter()
* Правильный ответ: prefetch_related
prefetch_related грузит связь отдельным запросом с IN; select_related работает через JOIN для ForeignKey/OneToOne.

Почему bulk_insert_mappings быстрее цикла с add()?
- Потому что пропускает проверки базы
- Потому что упаковывает много строк в один INSERT, сокращая число запросов
- Потому что не пишет в базу
- Потому что использует отдельное соединение
* Правильный ответ: Потому что упаковывает много строк в один INSERT, сокращая число запросов
Главные издержки — сетевые кругосветы и компиляция запросов; bulk их сокращает.

Какое ограничение есть у bulk-операций?
- Они работают только с PostgreSQL
- Они обходят жизненный цикл ORM: события и синхронизацию объектов
- Они не поддерживают INSERT
- Они всегда медленнее обычных
* Правильный ответ: Они обходят жизненный цикл ORM: события и синхронизацию объектов
Например, в Django bulk_create не вызывает сигналы, а new-объекты не появляются в сессии.

Что вернёт session.query(Author, func.count(Book.id)).outerjoin(Book).group_by(Author.id)?
- Пары (автор, число его книг), включая авторов без книг
- Только авторов с книгами
- Список всех книг
- Ошибку, потому что outerjoin не работает с агрегатами
* Правильный ответ: Пары (автор, число его книг), включая авторов без книг
outerjoin оставляет авторов без книг со счётчиком 0, GROUP BY группирует по автору.

Что такое сессия в SQLAlchemy?
- Рабочая область, где живут объекты, и фабрика запросов
- Таблица в базе данных
- Соединение с сервером базы
* Правильный ответ: Рабочая область, где живут объекты, и фабрика запросов
Объекты добавляются в сессию и попадают в базу только после flush/commit.

Для каких связей обычно используют joinedload?
- Для скалярных связей (ForeignKey, OneToOne)
- Для коллекций ManyToMany
- Только для наследования
* Правильный ответ: Для скалярных связей (ForeignKey, OneToOne)
JOIN умножает строки, поэтому для коллекций безопаснее selectinload.
<!--/QUIZ-->
