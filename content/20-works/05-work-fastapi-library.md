---
title: Самостоятельная работа: API-сервис библиотеки на FastAPI
summary: Полный цикл разработки бэкенда библиотеки: модели Pydantic, CRUD для книг и читателей, выдача/возврат, поиск, статистика и тесты.
order: 5
duration: 180 мин
difficulty: advanced
tags: fastapi, pydantic, rest api, crud, uvicorn, тестирование
---

# Самостоятельная работа: API-сервис библиотеки на FastAPI

Привет! Это самостоятельная работа уровня advanced. За 180 минут ты пройдёшь путь реального бэкенд-разработчика: спроектируешь модель данных, реализуешь REST API, добавишь валидацию, поиск, статистику и тесты. Всё, что ты здесь сделаешь, — готовая основа для сервиса, который можно отдать заказчику.

## Постановка задачи

Городская библиотека «Питон» просит автоматизировать учёт выдачи книг. Сейчас всё ведётся в бумажном журнале, и библиотекарь тратит часы на поиск нужной записи. Тебе нужно спроектировать и реализовать REST API-сервис, которым будут пользоваться библиотекарь и читатели.

Сервис должен управлять тремя сущностями:

- **книга (Book)**: `id`, `title`, `author`, `year`, `genre`, `isbn`, `copies` — количество экземпляров в фонде;
- **читатель (Reader)**: `id`, `name`, `email`, `birth_year`, `registered_at`;
- **выдача (Borrow)**: `id`, `book_id`, `reader_id`, `borrow_date`, `return_date` (значение `None`, если книга ещё не возвращена).

Функциональные требования:

1. **Полный CRUD** для книг и читателей: создание, чтение списком и по id, обновление, удаление.
2. **Выдача книги**: эндпоинт `POST /borrows` принимает `book_id` и `reader_id`, уменьшает число доступных экземпляров и фиксирует дату выдачи. Если свободных экземпляров нет — сервис должен отказать.
3. **Возврат книги**: эндпоинт `POST /borrows/{id}/return` помечает выдачу возвращённой и возвращает экземпляр в фонд.
4. **Поиск и фильтрация**: поиск по названию и автору, фильтр по жанру, доступности, сортировка, пагинация.
5. **Статистика**: сколько всего книг, сколько доступно сейчас, сколько выдач активно, сколько читателей, топ самых популярных книг.
6. **Понятные ошибки** с правильными HTTP-кодами: 404 (нет ресурса), 409 (конфликт, например дубль ISBN или выдача недоступной книги), 422 (невалидные данные).
7. **Тесты** ключевых сценариев.

Требования к реализации:

- все модели данных — на базе Pydantic, ограничения задаются через `Field` и констрейнты;
- данные хранятся в памяти (списки словарей), структура позволяет генерировать `id` последовательно;
- даты передаются строками ISO 8601 (`ГГГГ-ММ-ДД`), сегодняшний день берётся из `datetime.date.today()`;
- каждый эндпоинт возвращает JSON и корректный статус-код;
- приложение запускается командой `uvicorn main:app --reload`, документация доступна по адресу `/docs`.

## Что ты повторишь

FastAPI и Pydantic, декораторы маршрутов, query-параметры, обработку ошибок через `HTTPException`, паттерн «хранилище отдельно от маршрутов», автоматическую документацию Swagger UI, тесты через `TestClient`.

## План работы

Работа разбита на 5 этапов. Проходи их по порядку: каждый следующий опирается на предыдущий. Не переходи к новому этапу, пока не проверены, что предыдущие сценарии работают в `/docs`.

<!--TASK-->
### Задача 1
Создай структуру проекта: папку `library` с файлами `models.py`, `storage.py`, `main.py`. В `models.py` опиши Pydantic-модели `Book`, `Reader` и `Borrow` с аннотациями и ограничениями: `title` и `author` — непустые строки; `year` — между 1455 и текущим годом (используй `Field(ge=1455, le=<текущий год>)`); `isbn` — строка; `copies` — целое не меньше 1; `email` — валидный адрес через `EmailStr`; `birth_year` — не раньше 1900; `borrow_date` и `return_date` — `date | None`. В `storage.py` заведи пустые списки для книг, читателей, выдач и счётчики id. В `main.py` создай приложение FastAPI с эндпоинтами `GET /books` и `GET /readers`, которые возвращают пустые списки. Ожидаемый результат: `uvicorn main:app --reload` стартует без ошибок, страница `/docs` открывается, а `GET /books` и `GET /readers` возвращают `[]`.

### Задача 2
Реализуй полный CRUD для книг: `POST /books` — создание с проверкой уникальности `isbn` (повторный ISBN даёт код 409), `GET /books/{book_id}` — получение по id (нет книги — 404), `PUT /books/{book_id}` — обновление полей, `DELETE /books/{book_id}` — удаление с кодом 204. Вынеси работу с данными в функции модуля `storage.py`, например `get_books()`, `add_book(data)`, `book_by_id(book_id)`, `update_book(book_id, data)`, `delete_book(book_id)` — маршруты должны оставаться тонкими. Ожидаемый результат: все четыре операции работают через `/docs`, повторный `POST` с тем же ISBN даёт 409, обращение к несуществующему id даёт 404, `DELETE` возвращает 204.

### Задача 3
Добавь выдачу и возврат книг. Эндпоинт `POST /borrows` принимает тело вида `{"book_id": 1, "reader_id": 1}`: проверь, что книга и читатель существуют (иначе 404), что есть свободные экземпляры — `copies > 0` (иначе 409 «Нет доступных экземпляров»), затем уменьши `copies` на 1 и создай запись с `borrow_date` = сегодняшней датой и `return_date = None`. Эндпоинт `POST /borrows/{borrow_id}/return` находит выдачу, и если она ещё не закрыта, ставит `return_date` = сегодня и увеличивает `copies` на 1. Добавь также `GET /borrows` с необязательным параметром `?active=true`, который оставляет только незакрытые выдачи. Ожидаемый результат: выдача уменьшает количество доступных экземпляров; при нуле свободных копий выдача даёт 409; возврат восстанавливает `copies`.

### Задача 4
Расширь `GET /books` параметрами поиска, фильтрации, сортировки и пагинации: `search` — подстрока в `title` или `author` без учёта регистра; `genre` — точное совпадение жанра; `available=true` — только книги с `copies > 0`; `sort` — значения `year`, `-year` (по убыванию), `title`; `limit` и `offset` — пагинация. Все параметры необязательные. Ожидаемый результат: комбинации параметров работают, например `GET /books?search=python&available=true&sort=-year&limit=5` возвращает до пяти книг, отфильтрованных по поиску и доступности, отсортированных по году по убыванию.

### Задача 5
Добавь эндпоинт `GET /stats`, возвращающий `{"total_books": ..., "available_books": ..., "active_borrows": ..., "total_readers": ..., "top_books": [{"title": ..., "borrow_count": ...}]}` — топ-5 книг по числу выдач. Запрети удаление книги, у которой есть активные выдачи (код 409). Напиши тесты в файле `test_app.py` через `TestClient`: минимум 4 сценария (создание книги; дубль ISBN — 409; выдача книги и затем возврат; статистика). Ожидаемый результат: `pytest test_app.py` проходит полностью, статистика корректно отражает состояние «библиотеки».
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Pydantic импортируется так: `from pydantic import BaseModel, Field, EmailStr`. `EmailStr` требует пакет `email-validator` (`pip install email-validator`). Для дат используй `from datetime import date` и аннотацию `date | None`. Текущий год можно получить через `date.today().year` и подставить в `Field(le=...)`. Класс `Book` наследует `BaseModel`, поля с `Field` получают ограничения: `Field(min_length=1, max_length=200)` для строк, `Field(ge=1455, le=date.today().year)` для года. Список `books_db` и счётчик `next_book_id` заведи в `storage.py` на уровне модуля.

### Подсказка 2
В `storage.py` пиши функции, которые работают с глобальными списками: внутри функций, где ты присваиваешь счётчику новое значение, объяви `global next_book_id`. Проверка дублей ISBN: `any(b["isbn"] == data["isbn"] for b in books_db)` — если `True`, подними `HTTPException(status_code=409, detail="Книга с таким ISBN уже существует")`. Для 404 заведи вспомогательную функцию `book_by_id`, которая либо возвращает словарь, либо поднимает `HTTPException(status_code=404, detail="Книга не найдена")`. `PUT` обновляет через `old.update(data)`, `DELETE` — через `books_db.remove(book)` со статусом 204.

### Подсказка 3
Создавая выдачу, сначала найди книгу и читателя через их функции-«поисковики» — если кого-то нет, сразу 404. Потом проверь `book["copies"] > 0`. Если нет — 409. Далее уменьши `copies`: `book["copies"] -= 1`. Запись о выдаче формируй как `{"id": ..., "book_id": ..., "reader_id": ..., "borrow_date": str(date.today()), "return_date": None}`. Для возврата найди запись по id, проверь `borrow["return_date"] is None`, иначе верни 409 (повторный возврат). Затем проставь дату и увеличи `copies` у книги через `book_by_id(borrow["book_id"])`.

### Подсказка 4
Все параметры — со значениями по умолчанию: `search: str | None = None`, `sort: str = "year"` и так далее — FastAPI сам сделает их query-параметрами. Фильтрацию строй цепочкой: сначала поиск, потом жанр, потом доступность. Для сортировки используй `sorted(result, key=lambda b: b["title"], reverse=(sort.startswith("-")))` и срезай ключ: `sort.lstrip("-")`. Пагинация — простой срез списка: `result[offset:offset + limit]`. Не забудь про дефолты `limit=10, offset=0`.

### Подсказка 5
Для топа книг посчитай частоту `book_id` в `borrows_db` с `return_date` или без — не важно, сверять можно все выдачи: `Counter(b["book_id"] for b in borrows_db)` из `collections`. Проверку запрета удаления делай в `delete_book`: если `any(b["book_id"] == book_id and b["return_date"] is None for b in borrows_db)` — 409. Тесты: `from fastapi.testclient import TestClient`, затем `client = TestClient(app)` — объект `client` работает как `requests`: `client.post("/books", json={...})`, `client.get("/books")`. Проверяй `response.status_code` и `response.json()`. `TestClient` запускает приложение в памяти, поднимать uvicorn для тестов не нужно.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Начнём с моделей. Файл `library/models.py`:

```python
from datetime import date
from pydantic import BaseModel, Field, EmailStr


class Book(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1455, le=date.today().year)
    genre: str = Field(min_length=1, max_length=50)
    isbn: str = Field(min_length=10, max_length=17)
    copies: int = Field(ge=1)


class Reader(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    birth_year: int = Field(ge=1900, le=date.today().year)


class Borrow(BaseModel):
    book_id: int
    reader_id: int
    borrow_date: date | None = None
    return_date: date | None = None
```

`BaseModel` включает валидацию: аннотации типов задают типы полей, а `Field` добавляет ограничения — `min_length`/`max_length` для строк, `ge` (больше или равно) и `le` для чисел. `EmailStr` проверяет, что строка — корректный адрес электронной почты, но требует пакет `email-validator` (`pip install email-validator`). Строка `le=date.today().year` вычисляет текущий год при определении класса — ограничение всегда актуально. Для даты выдачи мы используем `date | None`, потому что при создании записи `return_date` ещё неизвестна.

Теперь хранилище — файл `library/storage.py`:

```python
books_db = []
readers_db = []
borrows_db = []
next_book_id = 1
next_reader_id = 1
next_borrow_id = 1
```

И минимальное приложение — `library/main.py`:

```python
from fastapi import FastAPI
from storage import books_db, readers_db

app = FastAPI(title="Library API", description="Сервис библиотеки «Питон»")


@app.get("/books")
def list_books():
    return books_db


@app.get("/readers")
def list_readers():
    return readers_db
```

Разделение на модули — ключевая архитектурная идея: `models.py` отвечает за контракт данных, `storage.py` — за хранение, `main.py` — за HTTP-слой. Такой код легко развивать: заменить списки на базу данных можно, не трогая маршруты. Запуск: `uvicorn main:app --reload` из папки `library`. Если uvicorn не найдет модуль, запусти из папки проекта: `uvicorn library.main:app --reload`. Открой http://127.0.0.1:8000/docs — там автоматически собрана интерактивная документация обоих эндпоинтов.

### Разбор 2
Наполняем хранилище функциями. `library/storage.py`:

```python
from fastapi import HTTPException

books_db = []
readers_db = []
borrows_db = []
next_book_id = 1
next_reader_id = 1
next_borrow_id = 1


def list_books():
    return books_db


def book_by_id(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


def add_book(data: dict):
    global next_book_id
    if any(b["isbn"] == data["isbn"] for b in books_db):
        raise HTTPException(status_code=409, detail="Книга с таким ISBN уже существует")
    book = {"id": next_book_id, **data}
    next_book_id += 1
    books_db.append(book)
    return book


def update_book(book_id: int, data: dict):
    book = book_by_id(book_id)
    book.update(data)
    return book


def delete_book(book_id: int):
    book = book_by_id(book_id)
    books_db.remove(book)
```

Маршруты в `library/main.py`:

```python
from fastapi import FastAPI, status
from models import Book
import storage

app = FastAPI(title="Library API")


@app.get("/books")
def list_books():
    return storage.list_books()


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    return storage.add_book(book.model_dump())


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return storage.book_by_id(book_id)


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    return storage.update_book(book_id, book.model_dump())


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    storage.delete_book(book_id)
```

Ключевые моменты: `book.model_dump()` превращает объект Pydantic в словарь — именно его мы храним. `add_book` проверяет уникальность ISBN через `any(...)` и бросает `HTTPException` с кодом 409, если дубль найден. Функция `book_by_id` централизует «не найдено»: любой маршрут получает 404 автоматически. Обрати внимание на `global next_book_id`: без него Python посчитал бы переменную локальной и упал. Код 204 для DELETE — стандарт «успешно, без содержимого».

### Разбор 3
Добавляем выдачу и возврат. В `storage.py`:

```python
from datetime import date


def borrow_book(book_id: int, reader_id: int):
    global next_borrow_id
    book = book_by_id(book_id)
    if not any(r["id"] == reader_id for r in readers_db):
        raise HTTPException(status_code=404, detail="Читатель не найден")
    if book["copies"] <= 0:
        raise HTTPException(status_code=409, detail="Нет доступных экземпляров")
    book["copies"] -= 1
    record = {
        "id": next_borrow_id,
        "book_id": book_id,
        "reader_id": reader_id,
        "borrow_date": str(date.today()),
        "return_date": None,
    }
    next_borrow_id += 1
    borrows_db.append(record)
    return record


def return_book(borrow_id: int):
    for borrow in borrows_db:
        if borrow["id"] == borrow_id:
            if borrow["return_date"] is not None:
                raise HTTPException(status_code=409, detail="Книга уже возвращена")
            borrow["return_date"] = str(date.today())
            book_by_id(borrow["book_id"])["copies"] += 1
            return borrow
    raise HTTPException(status_code=404, detail="Выдача не найдена")
```

Маршруты:

```python
from models import Book, Borrow


@app.post("/borrows", status_code=status.HTTP_201_CREATED)
def create_borrow(payload: Borrow):
    return storage.borrow_book(payload.book_id, payload.reader_id)


@app.post("/borrows/{borrow_id}/return")
def return_borrow(borrow_id: int):
    return storage.return_book(borrow_id)


@app.get("/borrows")
def list_borrows(active: bool | None = None):
    if active is None:
        return storage.borrows_db
    return [b for b in storage.borrows_db if (b["return_date"] is None) == active]
```

Логика: `borrow_book` сначала находит книгу и проверяет читателя (404, если кого-то нет), затем смотрит на `copies` — если ноль, 409. Только после всех проверок мы меняем состояние: уменьшаем счётчик и создаём запись. Это важный принцип: сначала все валидации, потом мутации — иначе легко получить «съеденную» копию при ошибке. `return_book` ищет запись, а если `return_date` уже проставлен, отвечает 409 — двойной возврат невозможен. Параметр `?active=true` фильтрует по `return_date is None`; выражение `(b["return_date"] is None) == active` лаконично покрывает оба случая.

### Разбор 4
Расширяем `GET /books`:

```python
@app.get("/books")
def list_books(search: str | None = None, genre: str | None = None,
               available: bool | None = None, sort: str = "year",
               limit: int = 10, offset: int = 0):
    result = storage.books_db
    if search:
        search = search.lower()
        result = [b for b in result
                  if search in b["title"].lower() or search in b["author"].lower()]
    if genre:
        result = [b for b in result if b["genre"].lower() == genre.lower()]
    if available is not None:
        result = [b for b in result if (b["copies"] > 0) == available]
    key = sort.lstrip("-")
    result = sorted(result, key=lambda b: b[key], reverse=sort.startswith("-"))
    return result[offset:offset + limit]
```

Все параметры имеют значения по умолчанию, поэтому FastAPI трактует их как необязательные query-параметры. Фильтрация — цепочка генераторов списков: каждая ступень сужает результат. Поиск сравнивает приведённые к нижнему регистру подстроки, поэтому регистр не важен. Сортировка: `sort.lstrip("-")` даёт имя поля, `reverse=sort.startswith("-")` переворачивает порядок для значений с минусом (например `-year`). Пагинация — срез списка `[offset:offset + limit]`. Проверь в `/docs`: комбинации параметров, например `?search=python&available=true&sort=-year&limit=5`, работают независимо.

### Разбор 5
Финальный штрих — статистика и тесты. В `storage.py`:

```python
from collections import Counter


def get_stats():
    total_books = len(books_db)
    available_books = sum(1 for b in books_db if b["copies"] > 0)
    active_borrows = sum(1 for b in borrows_db if b["return_date"] is None)
    counts = Counter(b["book_id"] for b in borrows_db)
    top = []
    for book_id, count in counts.most_common(5):
        book = book_by_id(book_id)
        top.append({"title": book["title"], "borrow_count": count})
    return {
        "total_books": total_books,
        "available_books": available_books,
        "active_borrows": active_borrows,
        "total_readers": len(readers_db),
        "top_books": top,
    }
```

И запрет удаления книги с активными выдачами — дополни проверку в `delete_book`:

```python
def delete_book(book_id: int):
    book = book_by_id(book_id)
    if any(b["book_id"] == book_id and b["return_date"] is None for b in borrows_db):
        raise HTTPException(status_code=409, detail="Нельзя удалить книгу с активными выдачами")
    books_db.remove(book)
```

Тесты `test_app.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_book():
    r = client.post("/books", json={
        "title": "Чистый код", "author": "Р. Мартин", "year": 2008,
        "genre": "Программирование", "isbn": "978-5-93286-146-9", "copies": 2,
    })
    assert r.status_code == 201
    assert r.json()["id"] == 1


def test_duplicate_isbn():
    payload = {
        "title": "Другая книга", "author": "Автор", "year": 2020,
        "genre": "Фантастика", "isbn": "978-5-93286-146-9", "copies": 1,
    }
    assert client.post("/books", json=payload).status_code == 409


def test_borrow_and_return():
    client.post("/books", json={
        "title": "Гарри Поттер", "author": "Дж. Роулинг", "year": 1997,
        "genre": "Фэнтези", "isbn": "978-5-389-00040-4", "copies": 1,
    })
    client.post("/readers", json={"name": "Иван", "email": "ivan@mail.ru", "birth_year": 1990})
    r = client.post("/borrows", json={"book_id": 1, "reader_id": 1})
    assert r.status_code == 201
    assert client.post("/borrows", json={"book_id": 1, "reader_id": 1}).status_code == 409
    borrow_id = r.json()["id"]
    assert client.post(f"/borrows/{borrow_id}/return").status_code == 200
    assert client.post(f"/borrows/{borrow_id}/return").status_code == 409


def test_stats():
    stats = client.get("/stats").json()
    assert stats["total_books"] == 2
    assert stats["active_borrows"] == 0
```

`TestClient` из `fastapi.testclient` запускает приложение в памяти — сервер поднимать не нужно. Внимание: тесты используют общее глобальное хранилище, поэтому они должны идти в порядке, который не ломается (мы создаём книги в первых тестах и опираемся на них в `test_stats`). Запуск: `pytest test_app.py` из папки `library`. `Counter` из `collections` удобно считает частоты; `most_common(5)` сразу даёт топ-5. Статистика считается на лету — это нормально для in-memory хранилища. Проверь запрет удаления: `DELETE /books/1` при активной выдаче вернёт 409.
<!--/SOLUTION-->

## Критерии оценки

| Критерий | Что проверяется | Баллы |
|---|---|---|
| Модели и валидация | Корректные Pydantic-модели, ограничения `Field`, `EmailStr`, даты | 15 |
| Архитектура | Разделение на `models.py` / `storage.py` / `main.py`, тонкие маршруты | 15 |
| CRUD книг | Все 5 операций, коды 201/204/404/409 | 15 |
| Выдача и возврат | Уменьшение/восстановление `copies`, защита от повторной выдачи и возврата | 15 |
| Поиск, фильтрация, сортировка, пагинация | Все параметры работают совместно | 15 |
| Статистика и запрет удаления | Корректные цифры, топ-5, 409 при активных выдачах | 10 |
| Тесты | Минимум 4 сценария, `pytest` проходит | 10 |
| Документация и запуск | `/docs` открывается, uvicorn стартует без ошибок | 5 |

Итого 100 баллов. Оценка: 90+ — «отлично», 75–89 — «хорошо», 60–74 — «удовлетворительно», меньше 60 — работу стоит доработать и сдать повторно.

## Что сдать

1. Файлы проекта: `library/models.py`, `library/storage.py`, `library/main.py`, `library/test_app.py`.
2. Краткий README (10–20 строк): как установить зависимости, как запустить сервер, как запустить тесты, список эндпоинтов с примерами.
3. Скриншоты подтверждения работы: страница `/docs`, успешный `pytest`, один-два примера ответов API (можно через curl: `curl http://127.0.0.1:8000/books`).
4. Собери всё в один архив или храни в репозитории — папку `library` целиком.

<!--QUIZ-->
Что делает аннотация `year: int = Field(ge=1455, le=2026)` в Pydantic?
- Устанавливает значение по умолчанию 1455
- Ограничивает поле числами от 1455 до 2026 включительно
- Делает поле необязательным
- Запрещает менять поле после создания
* Правильный ответ: Ограничивает поле числами от 1455 до 2026 включительно
`ge` и `le` задают допустимый диапазон: значение меньше 1455 или больше 2026 вызовет ошибку валидации 422.

Какой код ответа вернёт FastAPI при попытке создать книгу с уже существующим ISBN, если в коде поднят `HTTPException(status_code=409, ...)`?
- 404
- 409
- 422
- 500
* Правильный ответ: 409
409 Conflict — семантически верный код для конфликта с существующим ресурсом, например дубля уникального поля.

Для чего нужен `model_dump()` у объекта Pydantic?
- Для сохранения модели в базу данных
- Для превращения объекта модели в обычный словарь
- Для проверки, существует ли объект
- Для генерации JSON-схемы
* Правильный ответ: Для превращения объекта модели в обычный словарь
`model_dump()` возвращает стандартный словарь Python — именно его удобно хранить в списке или передавать дальше.

Что произойдёт, если функция `book_by_id` не найдёт книгу и поднимет `HTTPException(status_code=404, ...)`?
- Сервер упадёт с ошибкой
- FastAPI вернёт клиенту JSON с кодом 404 и текстом detail
- Запрос будет молча проигнорирован
- Откроется страница ошибки приложения
* Правильный ответ: FastAPI вернёт клиенту JSON с кодом 404 и текстом detail
FastAPI перехватывает `HTTPException` и превращает её в HTTP-ответ с указанным статусом.

Почему внутри функции `add_book` нужна строка `global next_book_id`?
- Без неё Python бросит ошибку при обращении к переменной
- Иначе Python посчитает переменную локальной и создаст новую, а счётчик не увеличится
- `global` нужен для объявления типа переменной
- Без неё список books_db не будет виден
* Правильный ответ: Иначе Python посчитает переменную локальной и создаст новую, а счётчик не увеличится
Присваивание внутри функции делает переменную локальной; `global` говорит Python работать с глобальной версией.

Что вернёт `GET /books/999`, если книги с id 999 нет?
- Пустой список []
- Ошибку 404 с текстом «Книга не найдена»
- Ошибку 422
- None
* Правильный ответ: Ошибку 404 с текстом «Книга не найдена»
`book_by_id` поднимает `HTTPException` со статусом 404 — это стандартный способ сообщить о несуществующем ресурсе.

Как правильно задать необязательный query-параметр поиска в FastAPI?
- `def list_books(search: str = "all")`
- `def list_books(search: str | None = None)`
- `def list_books(search)` 
- `def list_books(search: str = None)`
* Правильный ответ: `def list_books(search: str | None = None)`
Параметр с дефолтным значением `None` и аннотацией `str | None` становится необязательным query-параметром.

Что означает код 204 в ответе на `DELETE /books/{book_id}`?
- Ошибка — книга не найдена
- Успешное удаление без содержимого в теле ответа
- Ресурс создан
- Перенаправление
* Правильный ответ: Успешное удаление без содержимого в теле ответа
204 No Content — стандартный код для успешного удаления: тело ответа пустое.

Что делает `TestClient(app)` из `fastapi.testclient`?
- Запускает uvicorn на порту 8000
- Создаёт HTTP-клиент для тестирования приложения в памяти
- Проверяет валидность OpenAPI-схемы
- Перезапускает сервер после каждого запроса
* Правильный ответ: Создаёт HTTP-клиент для тестирования приложения в памяти
`TestClient` вызывает приложение напрямую, без реального сервера — поэтому тесты быстрые и не требуют портов.
<!--/QUIZ-->
