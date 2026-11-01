---
title: Проект: API-сервис на FastAPI
summary: Разрабатываем REST API для коллекции книг: модель данных, валидация, CRUD-операции, автодокументация.
order: 3
duration: 90 мин
difficulty: advanced
---

Привет! В этом проекте мы окунёмся в мир бэкенда: напишем настоящий API-сервис на FastAPI. API — это интерфейс, через который программы общаются друг с другом. Наш сервис будет управлять коллекцией книг: добавлять, искать, изменять и удалять записи.

## О проекте

Мы создадим REST API, где каждый ресурс — книга — адресуется через URL:

- `GET /books` — список всех книг;
- `POST /books` — добавить книгу;
- `GET /books/{id}` — одна книга по id;
- `PUT /books/{id}` — обновить книгу;
- `DELETE /books/{id}` — удалить книгу.

Клиент (браузер, скрипт или другая программа) шлёт HTTP-запросы и получает JSON-ответы. FastAPI сам валидирует данные, строит схему и генерирует документацию.

## План сборки

1. Установить FastAPI и uvicorn.
2. Описать модель книги через Pydantic.
3. Создать хранилище данных.
4. Реализовать маршруты CRUD.
5. Добавить поиск и валидацию.
6. Запустить сервер и проверить документацию.

## Шаг 1. Установка

```bash
pip install fastapi uvicorn
```

FastAPI — сам фреймворк, а uvicorn — сервер, который запускает приложение.

## Шаг 2. Модель Pydantic

Pydantic описывает структуру данных. Создадим модель книги:

```python
from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=1455, le=2026)
    isbn: str
```

`BaseModel` — базовая модель Pydantic. Аннотации типов (`str`, `int`) задают обязательные поля, а `Field(ge=1455, le=2026)` добавляет ограничения: год должен лежать между 1455 (первая печатная книга) и текущим годом. Если данные не пройдут проверку, FastAPI сам вернёт клиенту ошибку 422.

## Шаг 3. Хранилище

Для простоты храним книги в памяти — в списке словарей. В реальном проекте здесь была бы база данных:

```python
books_db = []
next_id = 1
```

## Шаг 4. Маршруты CRUD

Начнём с получения списка и добавления:

```python
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Book Service")


@app.get("/books")
def list_books():
    return books_db


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    global next_id
    new_book = book.model_dump()
    new_book["id"] = next_id
    next_id += 1
    books_db.append(new_book)
    return new_book
```

FastAPI сам понимает, что параметр `book: Book` надо взять из тела запроса, проверить и превратить в объект `Book`. `model_dump()` — метод Pydantic, который возвращает обычный словарь. `status_code=201` — правильный код ответа для создания ресурса.

Дальше — получение одной книги, обновление и удаление:

```python
def find_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    old = find_book(book_id)
    old.update(book.model_dump())
    return old


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    book = find_book(book_id)
    books_db.remove(book)
```

`find_book` — вспомогательная функция: либо возвращает книгу, либо бросает `HTTPException` с кодом 404. `HTTPException` — стандартный способ сообщить об ошибке в FastAPI.

## Шаг 5. Поиск и валидация

Добавим параметр запроса для поиска по названию:

```python
@app.get("/books")
def list_books(search: str | None = None):
    if search is None:
        return books_db
    found = [b for b in books_db if search.lower() in b["title"].lower()]
    return found
```

`str | None = None` — необязательный query-параметр. Теперь запрос `GET /books?search=python` вернёт только подходящие книги.

## Шаг 6. Запуск

```bash
uvicorn main:app --reload
```

Сервер поднимется на http://127.0.0.1:8000, а документация будет доступна по адресу http://127.0.0.1:8000/docs — это одна из главных фишек FastAPI. Там можно вручную отправлять запросы и смотреть ответы.

## Итог урока

Мы узнали:

- что такое REST API и какие бывают методы;
- как описывать данные моделями Pydantic;
- как создавать маршруты и обрабатывать ошибки;
- как работают query-параметры и автодокументация.

<!--TASK-->
**Задача.** Собери сервис целиком, затем расширь его двумя функциями:

1. Защитись от дублей: при добавлении книги проверь, нет ли уже книги с таким же `isbn`; если есть — верни ошибку 409 (Conflict) через `HTTPException(status_code=409, ...)`.
2. Добавь эндпоинт `GET /books/{book_id}/stats`, который возвращает JSON вида `{"title": ..., "words_in_title": 12}` — количество слов в названии книги.

Ожидаемый результат: повторный `POST` с тем же ISBN возвращает `{"detail": "Книга с таким ISBN уже существует"}` и код 409; `GET /books/1/stats` возвращает статистику.
<!--/TASK-->

<!--HINT-->
Список существующих ISBN легко получить генератором `[b["isbn"] for b in books_db]` или проверкой через `any(...)`. Статистику считай просто: `len(book["title"].split())`. Проверить оба эндпоинта удобно в Swagger UI по адресу `/docs` — там же видны коды ответов.
<!--/HINT-->

<!--SOLUTION-->
Полное решение (`main.py`):

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Book Service")

books_db = []
next_id = 1


class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=1455, le=2026)
    isbn: str


def find_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.get("/books")
def list_books(search: str | None = None):
    if search is None:
        return books_db
    return [b for b in books_db if search.lower() in b["title"].lower()]


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: Book):
    global next_id
    if any(b["isbn"] == book.isbn for b in books_db):
        raise HTTPException(status_code=409, detail="Книга с таким ISBN уже существует")
    new_book = book.model_dump()
    new_book["id"] = next_id
    next_id += 1
    books_db.append(new_book)
    return new_book


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.get("/books/{book_id}/stats")
def book_stats(book_id: int):
    book = find_book(book_id)
    return {"title": book["title"], "words_in_title": len(book["title"].split())}


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    old = find_book(book_id)
    old.update(book.model_dump())
    return old


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    book = find_book(book_id)
    books_db.remove(book)
```

Разбор:

- Проверка дублей: `any(b["isbn"] == book.isbn for b in books_db)` — смотрим, существует ли книга с таким ISBN. Если да — бросаем 409, клиент увидит понятное сообщение.
- `/stats`: используем уже готовую `find_book` — это пример переиспользования кода. `book["title"].split()` делит название на слова.
- Обрати внимание: `/books/{book_id}/stats` не конфликтует с `/books/{book_id}` — у путей разное число сегментов, и FastAPI различает их автоматически.
- Запуск: `uvicorn main:app --reload`. В `/docs` можно потрогать каждый эндпоинт: отправить запрос и увидеть ответ.
<!--/SOLUTION-->
