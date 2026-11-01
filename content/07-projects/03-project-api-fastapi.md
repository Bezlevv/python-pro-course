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
### Задача 1
Установи fastapi и uvicorn через pip. Создай файл main.py: опиши модель Book на базе Pydantic (поля title, author, year с ограничениями через Field(ge=1455, le=2026), isbn) и приложение FastAPI с эндпоинтом GET /books, который пока возвращает пустой список. Запусти сервер командой uvicorn main:app --reload и открой документацию по адресу http://127.0.0.1:8000/docs. Ожидаемый результат: сервер стартует, а GET /books возвращает [] в Swagger UI.

### Задача 2
Реализуй добавление книги: эндпоинт POST /books со status_code=status.HTTP_201_CREATED. Храни книги в списке словарей books_db, а id присваивай через переменную next_id (не забудь про global). Возвращай созданную книгу с полем id. Ожидаемый результат: POST с валидным JSON создаёт запись, возвращает её с id и кодом 201, а GET /books показывает этот список.

### Задача 3
Реализуй три эндпоинта: GET /books/{book_id} — вернуть книгу по id, PUT /books/{book_id} — обновить поля книги через old.update(book.model_dump()), DELETE /books/{book_id} — удалить книгу из списка. Напиши вспомогательную функцию find_book(book_id), которая либо возвращает книгу, либо поднимает HTTPException(status_code=404, detail="Книга не найдена"). Ожидаемый результат: обращение к несуществующему id даёт 404, а PUT и DELETE работают корректно.

### Задача 4
Добавь параметр поиска в GET /books: измени сигнатуру на list_books(search: str | None = None), и если search задан — возвращай только книги, в названии которых встречается искомая подстрока без учёта регистра (используй lower()). Ожидаемый результат: запрос GET /books?search=python возвращает только подходящие книги, а без параметра — все.

### Задача 5
Добавь две функции: при POST проверяй, нет ли уже книги с таким же isbn (используй any(...)); если есть — подними HTTPException(status_code=409, detail="Книга с таким ISBN уже существует"). Добавь эндпоинт GET /books/{book_id}/stats, возвращающий {"title": ..., "words_in_title": N}, где N — количество слов в названии. Ожидаемый результат: повторный POST с тем же ISBN даёт код 409, а /books/1/stats возвращает статистику.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Установка выполняется командой pip install fastapi uvicorn. Запуск uvicorn main:app --reload означает: файл main.py, объект app внутри него, флаг --reload перезапускает сервер при изменении кода. Модель Pydantic — это класс, наследующий BaseModel, с аннотациями типов полей.

### Подсказка 2
Метод model_dump() возвращает обычный словарь с данными модели. Добавь в него ключ id и положи словарь в books_db. Чтобы менять next_id внутри функции, объяви global next_id в начале. Код 201 задаётся аргументом status_code декоратора.

### Подсказка 3
find_book(book_id) перебирает books_db и сравнивает book["id"] с book_id; если ничего не найдено — raise HTTPException(status_code=404, detail="Книга не найдена"). Для PUT используй old.update(book.model_dump()), для DELETE — books_db.remove(book). HTTPException импортируется из fastapi.

### Подсказка 4
Параметр с дефолтным значением None автоматически становится необязательным query-параметром. Проверяй поиск так: search.lower() in b["title"].lower() — это делает сравнение без учёта регистра. Не забудь обработать случай search is None.

### Подсказка 5
Для проверки дублей используй генератор: any(b["isbn"] == book.isbn for b in books_db). Количество слов в названии считай через len(book["title"].split()). Путь /books/{book_id}/stats не конфликтует с /books/{book_id}: у них разное число сегментов.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Начальная версия `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Book Service")


class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=1455, le=2026)
    isbn: str


@app.get("/books")
def list_books():
    return []
```

FastAPI — это фреймворк, а uvicorn — ASGI-сервер, который исполняет приложение. Команда uvicorn main:app --reload говорит: возьми из файла main.py объект app и запусти его; флаг --reload перезапускает сервер при каждом сохранении файла — удобно при разработке. Модель Book наследует BaseModel: Pydantic использует аннотации типов, чтобы знать, какие поля обязательны и какого они типа. Поле year дополнительно ограничено через Field(ge=1455, le=2026): год книги не может быть раньше 1455 (первая печатная книга) и позже 2026. Если клиент пришлёт год вне диапазона, FastAPI сам вернёт ответ с кодом 422 и описанием ошибки. Эндпоинт GET /books объявлен декоратором @app.get; сейчас он возвращает пустой список — это заглушка, которую мы наполним дальше. Документация откроется по /docs, там же удобно тестировать запросы.

### Разбор 2
Добавляем создание книги:

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Book Service")

books_db = []
next_id = 1


class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=1455, le=2026)
    isbn: str


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

Когда клиент отправляет POST на /books с JSON в теле, FastAPI видит аннотацию book: Book, валидирует входящие данные по модели и передаёт в функцию готовый объект Book. Если данные некорректны (например, нет title или год вне диапазона), FastAPI сам вернёт 422 — писать проверки вручную не нужно. Метод model_dump() превращает модель в обычный словарь; мы добавляем в него ключ id и кладём в books_db. Переменная next_id — глобальная, поэтому внутри функции нужна строка global next_id, иначе Python посчитает её локальной и бросит ошибку. Код ответа 201 (Created) задаётся через status_code в декораторе — это семантически верный ответ для успешного создания ресурса. Теперь добавленная книга видна и в GET /books.

### Разбор 3
Добавляем получение, обновление и удаление:

```python
from fastapi import FastAPI, HTTPException, status

...

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

Вспомогательная функция find_book централизует поиск: она перебирает список, а если книга с таким id не найдена, поднимает HTTPException с кодом 404 и текстом «Книга не найдена». FastAPI перехватывает это исключение и превращает его в JSON-ответ с соответствующим HTTP-статусом. GET /books/{book_id} просто возвращает результат find_book. PUT обновляет: find_book находит старый словарь, а old.update(book.model_dump()) заменяет его поля новыми значениями из тела запроса — при этом id не меняется, ведь его нет в модели. DELETE находит книгу и убирает её из списка через remove; код 204 означает «Успешно, без содержимого» — это стандарт для удаления.

### Разбор 4
Добавляем поиск:

```python
@app.get("/books")
def list_books(search: str | None = None):
    if search is None:
        return books_db
    return [b for b in books_db if search.lower() in b["title"].lower()]
```

Параметр функции с дефолтным значением None автоматически становится необязательным query-параметром: клиент может обратиться к /books без параметров или с ?search=python. Когда search не задан, функция возвращает весь список. Если параметр есть, мы строим новый список через генератор списка: для каждой книги b проверяется, входит ли искомая подстрока в название. Метод lower() применяется и к запросу, и к названию, поэтому поиск не зависит от регистра: «PYTHON», «Python» и «python» дадут одинаковый результат. Такой поиск — подстрочный, то есть вернёт и книги, в названии которых подстрока встречается не с начала слова. Проверь в /docs: GET /books?search=python вернёт только подходящие книги.

### Разбор 5
Полное решение `main.py`:

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

Проверка дублей: any(b["isbn"] == book.isbn for b in books_db) проходит по всем книгам и возвращает True, если хотя бы одна имеет такой же ISBN. Если да — поднимаем HTTPException с кодом 409 (Conflict) и понятным сообщением; это правильный семантический код для конфликта с существующим ресурсом. Эндпоинт /books/{book_id}/stats переиспользует find_book и считает количество слов: book["title"].split() делит название по пробелам, а len() даёт число элементов. Обрати внимание: путь с двумя сегментами не конфликтует с /books/{book_id} — FastAPI различает маршруты по числу сегментов. Запуск: uvicorn main:app --reload; в /docs удобно проверить каждый эндпоинт и увидеть коды ответов.
<!--/SOLUTION-->

<!--QUIZ-->
Какой пакет запускает FastAPI-приложение как сервер?
- Flask
- uvicorn
- sqlite3
- requests
* Правильный ответ: uvicorn
FastAPI — фреймворк, а uvicorn — ASGI-сервер, который исполняет приложение: uvicorn main:app --reload.

Что описывает класс, унаследованный от BaseModel в Pydantic?
- Схему базы данных
- Модель данных с типами полей и валидацией
- Конфигурацию сервера
- HTTP-заголовки
* Правильный ответ: Модель данных с типами полей и валидацией
Pydantic использует аннотации типов: поля становятся обязательными, а данные проверяются при создании объекта.

Какой код ответа возвращается при успешном создании ресурса?
- 200
- 201
- 404
- 500
* Правильный ответ: 201
201 Created означает, что ресурс успешно создан; для остальных успешных операций используется 200.

Что произойдёт, если передать год 1800 при ограничении Field(ge=1455, le=2026)?
- Книга создастся без проверки
- FastAPI вернёт ошибку 422 с описанием
- Сервер завершится с ошибкой
- Год автоматически исправится на 2026
* Правильный ответ: FastAPI вернёт ошибку 422 с описанием
Валидация Pydantic не пропустит значение вне диапазона, и FastAPI превратит это в ответ 422 Validation Error.

Что делает HTTPException(status_code=404, detail="...")?
- Логирует ошибку в консоль
- Останавливает обработку и возвращает клиенту JSON с кодом 404
- Перезапускает приложение
- Игнорирует запрос
* Правильный ответ: Останавливает обработку и возвращает клиенту JSON с кодом 404
FastAPI перехватывает HTTPException и превращает его в ответ с указанным статусом и текстом detail.

Что возвращает метод model_dump() модели Pydantic?
- Тензор данных
- Обычный словарь с данными модели
- Строку JSON
- Список имён полей
* Правильный ответ: Обычный словарь с данными модели
model_dump() превращает объект модели в стандартный словарь Python, который удобно хранить и изменять.

Какой метод HTTP используется для полного обновления книги?
- GET
- PUT
- DELETE
- POST
* Правильный ответ: PUT
PUT заменяет ресурс целиком новыми данными; в нашем проекте он обновляет поля книги.

Что такое query-параметр в FastAPI?
- Необязательный параметр в строке запроса, например ?search=python
- Параметр в теле запроса
- Первая часть URL
- Заголовок ответа
* Правильный ответ: Необязательный параметр в строке запроса, например ?search=python
Параметры функции с дефолтным значением автоматически становятся query-параметрами.
<!--/QUIZ-->
