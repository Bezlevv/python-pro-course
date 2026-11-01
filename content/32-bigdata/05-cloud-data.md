---
title: Облачные хранилища и Parquet
summary: Parquet как стандарт для аналитических данных, работа с S3 через boto3 и s3fs, партиционирование и pushdown-фильтры.
order: 5
duration: 40 мин
difficulty: advanced
tags: parquet, s3, boto3, s3fs, pyarrow, облако
---

## Почему Parquet — стандарт

В предыдущем уроке ты увидел, как читать Parquet блоками. Parquet — это колоночный формат файла, и именно он стал де-факто стандартом для аналитических данных. Почему:

- **Колоночность**: колонки хранятся отдельно, поэтому можно читать только нужные колонки;
- **Сжатие**: колонки сжимаются (snappy, zstd, gzip), часто в 5–10 раз;
- **Статистики**: в заголовках каждого row group лежат минимумы/максимумы колонок, что позволяет пропускать целые блоки;
- **Схема**: тип колонок хранится в файле, данные самодокументируемы.

## Parquet на практике

Запись и чтение через pyarrow:

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.table({
    "дата": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "город": ["Москва", "Питер", "Москва"],
    "сумма": [100.0, 200.0, 150.0],
})

pq.write_table(table, "sales.parquet", compression="zstd", row_group_size=1000)

t = pq.read_table("sales.parquet")
print(t.schema)
```

Атрибуты файла:

```python
pf = pq.ParquetFile("sales.parquet")
print(pf.metadata.num_rows)
print(pf.metadata.row_group(0).column(2).statistics)  # статистики колонки
```

## Облачные хранилища

Парадигма больших данных: файлы живут не на диске сервера, а в объектном хранилище — Amazon S3, Yandex Object Storage, Google Cloud Storage, MinIO. Ключевая идея: S3 — это просто «папка» с объектами, к которой обращаются по пути вида `s3://bucket/key`.

Клиентов два: низкоуровневый `boto3` (SDK от AWS) и файловый `s3fs` (работает как локальная файловая система).

```bash
pip install boto3 s3fs
```

## boto3: низкий уровень

```python
import boto3

s3 = boto3.client("s3")  # креды из переменных окружения

# Список бакетов
print([b["Name"] for b in s3.list_buckets()["Buckets"]])

# Список объектов
resp = s3.list_objects_v2(Bucket="my-bucket", Prefix="sales/")
for obj in resp.get("Contents", []):
    print(obj["Key"], obj["Size"])

# Загрузка и скачивание
s3.upload_file("local.parquet", "my-bucket", "sales/local.parquet")
s3.download_file("my-bucket", "sales/local.parquet", "downloaded.parquet")
```

Креды берутся из переменных окружения `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (или через профиль). В коде их не хранят никогда.

## s3fs: работаем как с диском

`s3fs` реализует интерфейс файловой системы:

```python
import s3fs

fs = s3fs.S3FileSystem()
print(fs.ls("my-bucket/sales/"))

with fs.open("my-bucket/sales/data.parquet", "rb") as f:
    table = pq.read_table(f)  # читаем прямо из S3
```

Как только у нас есть файловый объект, любой код, который умеет читать из файла, работает с облаком без изменений.

## Прямое чтение из S3 в библиотеках

Polars умеет читать S3 напрямую (нужен `s3fs`):

```python
import polars as pl
q = pl.scan_parquet("s3://my-bucket/sales/*.parquet")
print(q.collect())
```

Dask — через `storage_options`:

```python
import dask.dataframe as dd
ddf = dd.read_parquet("s3://my-bucket/sales/", storage_options={"anon": False})
```

## Партиционирование

Большие аналитические наборы партиционируют — раскладывают по подпапкам по значению колонки:

```
sales/
├── город=Москва/part.parquet
└── город=Питер/part.parquet
```

Запись hive-партиций:

```python
import pyarrow.dataset as ds

ds.write_dataset(table, "sales", format="parquet", partitioning=["город"])
```

Чтение с фильтром на партицию:

```python
dataset = ds.dataset("sales", format="parquet", partitioning="hive")
filtered = dataset.to_table(filter=ds.field("город") == "Москва")
```

Фильтр продавливается в путь — читаются только нужные папки, это экономит сетевой трафик и время. Теперь практика.

<!--TASK-->
### Задача 1
Создай файл `parquet_intro.py`. Сгенерируй таблицу `pa.table` с колонками `город` (три города), `месяц` (6 месяцев) и `выручка` (случайные числа). Запиши её в `sales.parquet` с `compression="zstd"` и `row_group_size=100`. Затем открой `pq.ParquetFile`, выведи: схему, число строк, число row groups и статистики колонки `выручка` первого row group. Объясни в комментарии, что означают `min` и `max` в статистиках.

### Задача 2
Напиши функцию `split_s3_path(path)` в файле `s3_utils.py`, которая принимает путь вида `s3://bucket/key/part.parquet` и возвращает кортеж `(bucket, key)`. Добавь проверку: если путь не начинается с `s3://`, функция должна бросить `ValueError`. Проверь работу на трёх путях, включая ключ без слэша и путь с вложенными папками.

### Задача 3
Адаптируй код из первого урока: в `s3_utils.py` напиши функцию `describe_s3_parquet(path, s3_client)`, которая принимает готовый клиент boto3 и путь `s3://bucket/key`. Функция должна скачать файл во временную папку через `s3_client.download_file`, открыть `pq.ParquetFile` и вернуть словарь `{"rows": ..., "columns": ..., "row_groups": ...}`. Не вызывай её с реальными кредами — просто подготовь код, который будет работать после подстановки клиента.

### Задача 4
Напиши pytest-тесты для `split_s3_path` и для записи/чтения Parquet. В `test_s3_utils.py` через `tmp_path` создай таблицу, запиши её в Parquet, прочитай обратно и проверь, что схема и данные совпали. Для `split_s3_path` проверь: корректный путь, путь без ключа, путь с вложенными папками и поднятие `ValueError` для неправильного пути. Запусти pytest.

### Задача 5
Напиши pytest-тесты для партиционированного датасета. Через `tmp_path` создай таблицу с колонками `город` и `выручка`, запиши её через `ds.write_dataset(..., partitioning=["город"])`, затем открой через `ds.dataset(partitioning="hive")`. Проверь: (1) в папке появились подпапки `город=...`; (2) `dataset.to_table(filter=ds.field("город") == "Москва")` возвращает только строки Москвы; (3) общее число строк равно числу строк исходной таблицы. Запусти pytest.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Случайные числа: `[float((i * 7919) % 1000) for i in range(N)]`. Статистики: `pf.metadata.row_group(0).column(2).statistics` — атрибуты `min`, `max` доступны у объекта статистик. Имя колонки: `pf.schema.column(2).name`.

### Подсказка 2
Путь `s3://a/b/c`: нужно убрать префикс `s3://`, затем разделить по первому `/` на бакет и ключ: `bucket, _, key = rest.partition("/")`. Если `/` нет — ключ пустой строки.

### Подсказка 3
`tempfile.NamedTemporaryFile(delete=False)` или `tmp_path`-подобный локальный путь. `s3_client.download_file(bucket, key, local_path)` — метод boto3. Потом `pq.ParquetFile(local_path)`. Не забудь удалить временный файл после использования.

### Подсказка 4
Для сверки схемы сравни `t.schema == original.schema` и `t.to_pydict() == table.to_pydict()`. Для `split_s3_path`: `assert split_s3_path("s3://b/k.parquet") == ("b", "k.parquet")`, для ошибки используй `pytest.raises(ValueError)`.

### Подсказка 5
После `ds.write_dataset` список подпапок: `sorted(p.name for p in (tmp_path / "sales").iterdir())` — должны быть `город=Москва` и `город=Питер`. Фильтр: `ds.field("город") == "Москва"`. Для полного числа строк: `len(dataset.to_table())`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import pyarrow as pa
import pyarrow.parquet as pq

cities = ["Москва", "Питер", "Казань"]
table = pa.table({
    "город": [cities[i % 3] for i in range(600)],
    "месяц": [f"2024-{m:02d}" for m in [(i % 6) + 1 for i in range(600)]],
    "выручка": [float((i * 7919) % 1000) for i in range(600)],
})
pq.write_table(table, "sales.parquet", compression="zstd", row_group_size=100)

pf = pq.ParquetFile("sales.parquet")
print("Схема:", pf.schema)
print("Строк:", pf.metadata.num_rows)
print("Row groups:", pf.num_row_groups)

stats = pf.metadata.row_group(0).column(2).statistics
print("Статистики выручки (row group 0): min =", stats.min, ", max =", stats.max)
```

Вывод: схема с тремя колонками, 600 строк, 6 row groups и статистики первого row group. Что здесь происходит? `pq.write_table` сжимает колонки алгоритмом zstd и разбивает на row groups по 100 строк. Статистики в заголовке каждого row group позволяют читателю не открывать блок, если условие фильтра не может быть выполнено (например, `filter(pl.col("выручка") > 5000)` — если `max < 5000`, блок пропускается).

### Разбор 2
Решение:

```python
def split_s3_path(path: str) -> tuple:
    if not path.startswith("s3://"):
        raise ValueError(f"Не S3-путь: {path}")
    rest = path[len("s3://"):]
    bucket, sep, key = rest.partition("/")
    if not sep:
        key = ""
    return bucket, key
```

Проверка:

```python
print(split_s3_path("s3://my-bucket/sales/part.parquet"))  # ('my-bucket', 'sales/part.parquet')
print(split_s3_path("s3://my-bucket"))                      # ('my-bucket', '')
print(split_s3_path("https://example.com"))                 # ValueError
```

Что здесь происходит? `partition("/")` делит строку на три части: до первого слэша, сам слэш и всё после. Если слэша нет — ключ пустой, значит, путь указывает на весь бакет. Проверка префикса защищает от мусорных входов. Такая функция полезна, когда ты получаешь путь от пользователя и должен разложить его на параметры для boto3 (бакет и ключ раздельно).

### Разбор 3
Решение:

```python
import tempfile
import os
import pyarrow.parquet as pq
from s3_utils import split_s3_path

def describe_s3_parquet(path: str, s3_client) -> dict:
    bucket, key = split_s3_path(path)
    if not key:
        raise ValueError("Ключ не указан")

    fd, local = tempfile.mkstemp(suffix=".parquet")
    os.close(fd)
    try:
        s3_client.download_file(bucket, key, local)
        pf = pq.ParquetFile(local)
        return {
            "rows": pf.metadata.num_rows,
            "columns": [pf.schema.column(i).name for i in range(pf.schema.num_columns)],
            "row_groups": pf.num_row_groups,
        }
    finally:
        os.unlink(local)
```

Что здесь происходит? Функция полностью готова к работе с реальным клиентом, но ничего не вызывает сама — клиент передаётся снаружи (dependency injection). Это позволяет тестировать логику с моком и не тратить сетевые запросы. Скачанный файл лежит во временной папке и удаляется даже при ошибке благодаря `finally`. Такой дизайн — стандарт для кода, работающего с облаком.

### Разбор 4
Решение:

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from s3_utils import split_s3_path

def _make_table():
    return pa.table({"город": ["Москва", "Питер"], "выручка": [100.0, 200.0]})

def test_parquet_roundtrip(tmp_path):
    path = tmp_path / "data.parquet"
    pq.write_table(_make_table(), path)
    loaded = pq.read_table(path)
    assert loaded.schema == _make_table().schema
    assert loaded.to_pydict() == _make_table().to_pydict()

def test_split_s3_path_basic():
    assert split_s3_path("s3://b/k.parquet") == ("b", "k.parquet")

def test_split_s3_path_no_key():
    assert split_s3_path("s3://bucket") == ("bucket", "")

def test_split_s3_path_nested():
    assert split_s3_path("s3://b/a/b/c.parquet") == ("b", "a/b/c.parquet")

def test_split_s3_path_invalid():
    with pytest.raises(ValueError):
        split_s3_path("https://example.com/file")
```

Что здесь происходит? Roundtrip-тест проверяет, что схема и данные переживают запись и чтение — это фундамент надёжности. Тесты `split_s3_path` покрывают основные случаи и ошибку. Ни один тест не обращается к сети: всё работает локально и быстро.

### Разбор 5
Решение:

```python
import pyarrow as pa
import pyarrow.dataset as ds
import pytest

def test_partitioned_dataset(tmp_path):
    table = pa.table({
        "город": ["Москва", "Питер", "Москва", "Питер"],
        "выручка": [100.0, 200.0, 300.0, 400.0],
    })
    ds.write_dataset(table, tmp_path / "sales", format="parquet", partitioning=["город"])

    dirs = sorted(p.name for p in (tmp_path / "sales").iterdir())
    assert dirs == ["город=Москва", "город=Питер"]

    dataset = ds.dataset(tmp_path / "sales", format="parquet", partitioning="hive")
    moscow = dataset.to_table(filter=ds.field("город") == "Москва")
    assert moscow.num_rows == 2
    assert set(moscow.column("город").to_pylist()) == {"Москва"}

    assert dataset.to_table().num_rows == 4
```

Что здесь происходит? `partitioning=["город"]` создаёт подпапки вида `город=Москва/`. При чтении с `partitioning="hive"` библиотека понимает эту разметку и добавляет колонку `город` из пути. Фильтр `ds.field("город") == "Москва"` продавливается на уровень файловой системы: читаются только файлы в папке `город=Москва`. Это ключевая оптимизация для облачных хранилищ — меньше данных качается по сети.
<!--/SOLUTION-->

<!--QUIZ-->
Какое преимущество даёт колоночный формат Parquet?
- Можно читать только нужные колонки
- Можно менять данные прямо в файле
- Он занимает больше места
* Правильный ответ: Можно читать только нужные колонки
Колоночность позволяет выбирать колонки и пропускать остальные.

Что хранится в статистиках row group?
- Минимумы и максимумы колонок
- Содержимое всех строк
- Хеши объектов
* Правильный ответ: Минимумы и максимумы колонок
Статистики позволяют пропускать блоки при фильтрации.

Какой параметр задаёт алгоритм сжатия в pq.write_table?
- compression
- codec
- zip
* Правильный ответ: compression
compression="zstd" или "snappy" задаёт кодек.

Что возвращает s3fs.S3FileSystem().ls("bucket/path")?
- Список объектов/папок по пути
- Содержимое файлов
- Схему Parquet
* Правильный ответ: Список объектов/папок по пути
ls работает как в локальной файловой системе.

Какой метод boto3 скачивает объект?
- s3_client.download_file(bucket, key, local)
- s3_client.get_object(bucket)
- s3_client.read(bucket, key)
* Правильный ответ: s3_client.download_file(bucket, key, local)
download_file принимает бакет, ключ и локальный путь.

Откуда boto3 берёт креды?
- Из переменных окружения AWS_ACCESS_KEY_ID и AWS_SECRET_ACCESS_KEY
- Из кода программы
- Из файла данных
* Правильный ответ: Из переменных окружения AWS_ACCESS_KEY_ID и AWS_SECRET_ACCESS_KEY
Креды никогда не должны попадать в код и в репозиторий.

Что такое hive-партиционирование?
- Разложение данных по подпапкам вида колонка=значение
- Сжатие файлов
- Разбиение на row groups
* Правильный ответ: Разложение данных по подпапкам вида колонка=значение
Имена папок содержат колонку и значение, что позволяет фильтровать по пути.

Что делает фильтр ds.field("город") == "Москва" при чтении датасета?
- Продавливается в пути и читает только нужные папки
- Считывает все данные и фильтрует в памяти
- Ничего, это синтаксис
* Правильный ответ: Продавливается в пути и читает только нужные папки
Это экономит сетевой трафик и время.

Как Polars читает Parquet из S3?
- pl.scan_parquet("s3://bucket/key")
- pl.read_bytes("s3://...")
- pl.read_remote("...")
* Правильный ответ: pl.scan_parquet("s3://bucket/key")
Нужен установленный s3fs для поддержки fsspec.

Что будет, если вызвать split_s3_path с путём не s3://?
- ValueError
- None
- Пустой кортеж
* Правильный ответ: ValueError
Функция проверяет префикс и бросает исключение.
<!--/QUIZ-->
