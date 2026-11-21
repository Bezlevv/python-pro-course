---
title: Elasticsearch: индексирование, поиск и агрегации
summary: Полнотекстовый поиск, маппинги, поисковые запросы, фильтры и агрегации на Python.
order: 7
duration: 55 мин
difficulty: advanced
tags: elasticsearch, opensearch, поиск, агрегации
---

Elasticsearch — распределённый поисковый движок на базе Lucene. Он используется для полнотекстового поиска, логов и аналитики. В уроке работаем через официальный клиент `elasticsearch-py`.

## Основные понятия

- Индекс — аналог «таблицы»/«базы» для документов.
- Документ — JSON-объект с полями.
- Маппинг — схема типов полей (text, keyword, integer...).

## Клиент и создание индекса

```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
es.indices.create(index="books", ignore=400)
```

## Запись документов

```python
es.index(index="books", id=1, document={"title": "Python для начинающих", "year": 2020})
```

## Поиск

```python
resp = es.search(index="books", query={"match": {"title": "Python"}})
```

## Агрегации

```python
resp = es.search(index="books", aggs={"by_year": {"terms": {"field": "year"}}})
```

## Итог урока

Elasticsearch даёт молниеносный полнотекстовый поиск и группировки; клиент на Python повторяет REST API один в один.

```mermaid
flowchart LR
    A["Индекс"] --> B["Документы"]
    B --> C["match поиск"]
    C --> D["Агрегации"]
    D --> E["Аналитика"]
```


## Практическое применение

Elasticsearch используют для поиска по каталогам, аналитики логов и мониторинга. Агрегации позволяют строить дашборды без выгрузки сырых данных. Умение строить индексы и запросы — востребованная компетенция для бэкенд- и дата-инженеров. Клиент на Python делает интеграцию с остальной экосистемой простой.


Помимо поиска, Elasticsearch часто используют для мониторинга логов: агенты пишут события в индекс, а дашборды собирают агрегации в реальном времени. При проектировании индекса важно заранее решить, какие поля будут keyword (точные фильтры), а какие text (поиск). Обновление маппинга после создания индекса ограничено, поэтому схему продумывают до записи данных.


Дополнительно стоит освоить `multi_match` — поиск по нескольким полям с весами, и `fuzzy`-поиск, который прощает опечатки. Пагинация результатов делается через `from`/`size`, а сортировка — через `sort`. Для безопасной интеграции с пользовательским вводом нельзя собирать запросы строковой интерполяцией — используйте query DSL-структуры: это уберегает от ошибок и неожиданных интерпретаций.


<!--TASK-->
### Задача 1 — Подключение и проверка
Подключись к Elasticsearch и проверь доступность через es.ping() или GET /. Если инстанса нет — опиши запуск через Docker (elasticsearch:8.x).

### Задача 2 — Создание индекса
Создай индекс books с маппингом: title text, year integer, in_stock boolean. Покажи ответ API.

### Задача 3 — Добавление документов
Добавь 3 документа (разные названия книг). Проверь, что id 1 возвращается через es.get.

### Задача 4 — Match-поиск
Найди книги, где в title встречается «Python», через match. Выведи хиты: score и source.

### Задача 5 — Фразовый поиск
Найди точную фразу «для начинающих» через match_phrase. Объясни разницу с match.

### Задача 6 — Фильтры и диапазон
Найди книги с year >= 2019 через bool filter range. Выведи количество найденных.

### Задача 7 — Агрегация по годам
Сгруппируй книги по годам через aggs terms. Выведи бакеты с количеством.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.14.3.

### Подсказка 2
es.indices.create(index="books", mappings={...}).

### Подсказка 3
es.index(index="books", id=N, document={...}).

### Подсказка 4
query={"match": {"title": "Python"}}.

### Подсказка 5
query={"match_phrase": {"title": "для начинающих"}}.

### Подсказка 6
query={"bool": {"filter": [{"range": {"year": {"gte": 2019}}}]}}.

### Подсказка 7
aggs={"by_year": {"terms": {"field": "year"}}}.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
```python
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
print(es.ping())
```
Если True — сервер доступен.

### Разбор 2
```python
mappings = {
    "properties": {
        "title": {"type": "text"},
        "year": {"type": "integer"},
        "in_stock": {"type": "boolean"},
    }
}
print(es.indices.create(index="books", mappings=mappings))
```
Маппинг задаёт типы полей.

### Разбор 3
```python
books = [
    {"title": "Python для начинающих", "year": 2020, "in_stock": True},
    {"title": "Глубокое обучение", "year": 2021, "in_stock": False},
    {"title": "Python в науке", "year": 2019, "in_stock": True},
]
for i, b in enumerate(books, start=1):
    es.index(index="books", id=i, document=b)

print(es.get(index="books", id=1)["_source"])
```
Документы добавлены.

### Разбор 4
```python
resp = es.search(index="books", query={"match": {"title": "Python"}})
for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```
Match работает по анализированным полям.

### Разбор 5
```python
resp = es.search(index="books", query={"match_phrase": {"title": "для начинающих"}})
print([h["_source"]["title"] for h in resp["hits"]["hits"]])
```
match_phrase хранит последовательность слов.

### Разбор 6
```python
resp = es.search(index="books", query={
    "bool": {"filter": [{"range": {"year": {"gte": 2019}}}]}
})
print(resp["hits"]["total"]["value"])
```
Фильтры не влияют на релевантность.

### Разбор 7
```python
resp = es.search(index="books", aggs={"by_year": {"terms": {"field": "year"}}})
for bucket in resp["aggregations"]["by_year"]["buckets"]:
    print(bucket["key"], bucket["doc_count"])
```
Агрегации группируют документы.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое индекс в Elasticsearch?
- Коллекция документов с маппингом
- Таблица БД
- Строка
- Кластер
* Правильный ответ: Коллекция документов с маппингом
Аналог базы/таблицы.

Какой тип поля для полнотекстового поиска?
- text
- keyword
- integer
- boolean
* Правильный ответ: text
text анализируется, keyword — точное совпадение.

Что делает match?
- Анализирует запрос и ищет по полю
- Точное совпадение
- Фразу
- Рейтинг
* Правильный ответ: Анализирует запрос и ищет по полю
Словарный поиск.

Чем match_phrase отличается от match?
- Требует точной последовательности слов
- Быстрее
- Ищет только по id
- Работает с числами
* Правильный ответ: Требует точной последовательности слов
Это фразовый поиск.

Что такое фильтр в bool query?
- Условие без влияния на score
- Полный поиск
- Сортировка
- Пагинация
* Правильный ответ: Условие без влияния на score
Фильтры кэшируются.

Что делает aggregations?
- Группирует и считает по полям
- Сортирует
- Удаляет документы
- Меняет маппинг
* Правильный ответ: Группирует и считает по полям
Аналитика по запросу.

Как добавить документ?
- es.index(index=..., id=..., document=...)
- es.create_index
- es.put
- es.append
* Правильный ответ: es.index(index=..., id=..., document=...)
Метод index пишет/обновляет.

Что вернёт es.get(index, id)?
- Словарь с _source
- Список
- Число
- Строку
* Правильный ответ: Словарь с _source
Документ в JSON.

Какой параметр задаёт «больше или равно»?
- gte
- lte
- gt
- eq
* Правильный ответ: gte
greater than or equal.

Что такое score?
- Мера релевантности документа
- Размер файла
- Время
- Номер версии
* Правильный ответ: Мера релевантности документа
Чем больше, тем точнее совпадение.
Что такое маппинг?
- Схема типов полей индекса
- Список документов
- Журнал
- Кластер
* Правильный ответ: Схема типов полей индекса
Определяет, как анализируются поля.

Какая версия клиента работает с ES 8?
- elasticsearch-py 8.x
- 5.x
- 1.x
- Любая
* Правильный ответ: elasticsearch-py 8.x
Совместимость версий.


<!--/QUIZ-->
