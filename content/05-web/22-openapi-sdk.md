---
title: OpenAPI, генерация SDK и мок-серверы
summary: Описание API схемой OpenAPI, генерация клиентов, мок-серверы и контрактное тестирование.
order: 22
duration: 55 мин
difficulty: advanced
tags: openapi, swagger, генерация клиентов, моки
---

OpenAPI (бывший Swagger) — стандарт описания REST API. Схема становится единым источником правды: по ней создают документацию, клиентские SDK и мок-серверы.

## Что такое OpenAPI-схема

Файл (JSON/YAML) описывает пути, методы, параметры, тела запросов и ответы:

```yaml
openapi: 3.0.0
info:
  title: Книги
  version: 1.0.0
paths:
  /books:
    get:
      responses:
        '200':
          description: Список книг
```

## Автодокументация в FastAPI

FastAPI сам генерирует `/openapi.json` и Swagger UI на `/docs`. Схема — отражение кода.

## Генерация SDK

Инструменты: openapi-generator (Java/часто), а для Python — `openapi-generator-cli` или `datamodel-code-generator` (модели). Сгенерированный клиент можно использовать вместо ручного requests.

## Мок-серверы

Сервисы вроде `prism mock schema.yaml` или `openapi-mock` отдают примерные ответы по схеме. Это позволяет разрабатывать клиент раньше, чем бэкенд готов.

## Контрактное тестирование

Схема — контракт между поставщиком и потребителем. Сверка ответов со схемой выявляет несоответствия раньше, чем пользователи.

## Итог урока

OpenAPI — мост между командами: документация, SDK и моки автоматизируются, а интеграции становятся проверяемыми.

<!--TASK-->
### Задача 1 — Минимальная схема OpenAPI
Напиши OpenAPI 3.0-схему с одним путём `/ping`, методом GET и ответом 200. Сохрани в `schema.yaml` и проверь, что она валидна (например, `prism validate` или онлайн-проверка).

### Задача 2 — Схема для CRUD
Опиши путь `/books` (GET для списка, POST для создания) и `/books/{book_id}` (GET, PUT, DELETE). Укажи параметры, тела и коды ответов 200/201/404. Проверь схему.

### Задача 3 — FastAPI и openapi.json
Создай приложение FastAPI с маршрутом /items и моделью Pydantic. Открой `/openapi.json` и убедись, что схема содержит описание эндпоинта и компонент схемы.

### Задача 4 — Генерация моделей
Используй `datamodel-code-generator --input schema.yaml --output models.py` — сгенерируй pydantic-модели из схемы задач 2. Покажи сгенерированный файл.

### Задача 5 — Мок-сервер
Запусти мок на основе schema.yaml (например, `prism mock schema.yaml`). Проверь, что GET /books возвращает примерные данные без реального бэкенда.

### Задача 6 — Клиент на основе схемы
Сгенерируй Python-клиент (openapi-generator или самодельный через requests по схеме) и вызови метод получения книг у мок-сервера.

### Задача 7 — Контрактный тест
Напиши тест: отправь запрос к реальному бэкенду, получи ответ и провалидируй его против схемы (через openapi-spec-validator). Покажи результат для валидного и невалидного ответа.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Корректная схема: openapi: 3.0.0, info.title, paths.

### Подсказка 2
В параметрах для book_id укажи in: path, required: true.

### Подсказка 3
FastAPI сам отдаёт /openapi.json; Pydantic-модели попадают в components/schemas.

### Подсказка 4
pip install datamodel-code-generator; команда запустится из терминала.

### Подсказка 5
npm i -g @stoplight/prism-cli; затем prism mock schema.yaml.

### Подсказка 6
Можно использовать requests к http://127.0.0.1:4010/books.

### Подсказка 7
openapi-spec-validator умеет валидировать экземпляры по схеме.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```yaml
openapi: 3.0.0
info:
  title: Ping API
  version: 1.0.0
paths:
  /ping:
    get:
      responses:
        '200':
          description: ОК
```
Достаточно для минимальной схемы; валидность проверяется инструментами.

### Разбор 2
```yaml
paths:
  /books:
    get:
      responses:
        '200':
          description: Список
          content:
            application/json:
              schema:
                type: array
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Book'
      responses:
        '201':
          description: Создано
  /books/{book_id}:
    get:
      parameters:
        - name: book_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Книга
        '404':
          description: Не найдена
```
Схема описывает контракт CRUD полностью.

### Разбор 3
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items")
def list_items():
    return []
```
`/openapi.json` будет содержать компонент Item и эндпоинт /items.

### Разбор 4
```bash
pip install datamodel-code-generator
datamodel-code-generator --input schema.yaml --output models.py
```
В models.py появятся классы (например, Book) с полями из схемы — работает с Pydantic.

### Разбор 5
```bash
npm i -g @stoplight/prism-cli
prism mock schema.yaml
# Example: GET http://127.0.0.1:4010/books -> примерный массив
```
Мок отдаёт ответы на основе схемы без бэкенда.

### Разбор 6
```python
import requests
url = "http://127.0.0.1:4010/books"
r = requests.get(url, timeout=10)
print(r.status_code, r.json())
```
Клиент может быть и простым requests — главное, что адреса и тела известны из схемы.

### Разбор 7
```python
from openapi_spec_validator import validate_spec
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
import yaml

spec = yaml.safe_load(open("schema.yaml"))
validate_spec(spec)          # схема валидна

# Валидация ответа — через вызовы валидатора или вручную
```
Контракт проверяется автоматически; невалидный ответ вызовет ошибку.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое OpenAPI?
- Стандарт описания REST API
- Библиотека запросов
- Фреймворк
- База данных
* Правильный ответ: Стандарт описания REST API
Схема описывает контракт API.

Что FastAPI отдаёт автоматически?
- /openapi.json и /docs
- /swagger только
- /json
- Ничего
* Правильный ответ: /openapi.json и /docs
Схема генерится из кода.

Что делает мок-сервер?
- Отдаёт примерные ответы по схеме
- Хранит данные
- Шифрует
- Аутентифицирует
* Правильный ответ: Отдаёт примерные ответы по схеме
Разработка клиента не ждёт бэкенда.

Зачем нужен генератор SDK?
- Чтобы получить готовый клиент из схемы
- Чтобы написать схему
- Чтобы удалить API
- Чтобы ускорить БД
* Правильный ответ: Чтобы получить готовый клиент из схемы
SDK повторяет контракт.

Что такое контрактное тестирование?
- Проверка соответствия ответов схеме
- Тест скорости
- Тест UI
- Нагрузочный тест
* Правильный ответ: Проверка соответствия ответов схеме
Сверка контракта выявляет расхождения.

Какой инструмент генерирует модели из схемы?
- datamodel-code-generator
- black
- pytest
- gunicorn
* Правильный ответ: datamodel-code-generator
Создаёт pydantic-модели.

Как описать параметр пути?
- in: path, required: true
- in: query
- in: body
- in: header
* Правильный ответ: in: path, required: true
Параметры пути обязательны по определению.

Чем полезна единая схема?
- Единым источником правды
- Ускорением кода
- Защитой от хакеров
- Меньшим объёмом
* Правильный ответ: Единым источником правды
Документация, SDK и моки из одного места.

Как провалидировать ответ против схемы?
- Через openapi-spec-validator
- Через requests
- Через json.loads
- Через flask
* Правильный ответ: Через openapi-spec-validator
Инструмент проверяет экземпляры.

Почему моки полезны на раннем этапе?
- Клиент разрабатывается параллельно с бэкендом
- Они заменяют базу данных
- Они быстрее продакшена
- Они пишут код за вас
* Правильный ответ: Клиент разрабатывается параллельно с бэкендом
Контракт позволяет разделить работу команд.
<!--/QUIZ-->
