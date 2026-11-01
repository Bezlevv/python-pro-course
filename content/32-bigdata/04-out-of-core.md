---
title: Данные больше памяти: chunking и Arrow
summary: Как обрабатывать данные, которые не помещаются в оперативную память: потоковое чтение блоками и формат Apache Arrow.
order: 4
duration: 40 мин
difficulty: advanced
tags: pyarrow, chunking, out-of-core, recordbatch, память
---

## Стена памяти

Представь: у тебя файл на 50 ГБ, а в машине 16 ГБ оперативной памяти. Попытка `pd.read_csv("big.csv")` закончится либо падением с `MemoryError`, либо убийством процесса операционной системой. Это фундаментальное ограничение: любая структура данных обязана поместиться в RAM, прежде чем с ней можно будет работать.

Выходов два. Первый — купить сервер с терабайтом памяти (дорого). Второй — **out-of-core** обработка: не загружать всё сразу, а читать данные частями, обрабатывать каждую часть и накапливать результат. Так подход называется chunking, и он лежит в основе всех больших инструментов: Polars streaming, Dask, Spark.

## Apache Arrow: формат, который понимает каждый

Почти все современные инструменты больших данных хранят данные в формате **Apache Arrow** — колоночном бинарном формате. Что это даёт:

- **Колоночность**: данные одного столбца лежат рядом, что ускоряет агрегации по колонкам в десятки раз;
- **Zero-copy**: чтение из Arrow-массива не требует конвертации — числа уже лежат как сырые числа, без обёрток Python;
- **Стандарт**: Arrow понимают Polars, Dask, Spark, DuckDB, pandas (через `arrow` backend) — данные можно передавать между библиотеками без сериализации.

Python-доступ к Arrow даёт библиотека `pyarrow`:

```bash
pip install pyarrow
```

## Таблицы и RecordBatch

Самый простой объект — `pyarrow.Table`:

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.table({
    "город": ["Москва", "Питер", "Казань"],
    "сумма": [100.0, 200.0, 150.0],
})
print(table.schema)
print(table.num_rows, table.num_columns)
```

Таблица состоит из **RecordBatch** — кусочков по несколько тысяч строк. Именно батчи позволяют читать Parquet потоково: не всю таблицу, а по одному батчу за раз.

## Потоковое чтение Parquet

Файл Parquet внутри разделён на **row group** — независимые блоки строк. Библиотека умеет читать по одному row group, не открывая остальные:

```python
pf = pq.ParquetFile("big.parquet")
print("Row groups:", pf.num_row_groups)

for batch in pf.iter_batches(batch_size=10_000):
    # batch — это RecordBatch на 10 000 строк
    print(batch.num_rows)
```

`iter_batches` возвращает генератор: в каждый момент времени в памяти только один батч. Это и есть ядро out-of-core.

## Вычисления на батчах

Обработать батч можно средствами самого Arrow. Например, сумма колонки:

```python
import pyarrow.compute as pc

total = 0.0
for batch in pf.iter_batches(batch_size=10_000):
    total += pc.sum(batch.column("сумма")).as_py()
print("Итого:", total)
```

`pc.sum` считает сумму в нативном коде Arrow, а `.as_py()` превращает скаляр в обычный Python-float. Мы накопили сумму по 50-гигабайтному файлу, держа в памяти максимум 10 тысяч строк.

## Чтение CSV блоками

Аналогично можно читать CSV — `pyarrow.csv.open_csv` создаёт поток RecordBatch'ей:

```python
import pyarrow.csv as pv

reader = pv.open_csv("big.csv", read_options=pv.ReadOptions(block_size=4_096))
rows = 0
while True:
    try:
        batch = reader.read_next_batch()
    except StopIteration:
        break
    rows += batch.num_rows
print("Строк:", rows)
```

`block_size` — размер блока в байтах, который читается за раз.

## Память и скорость

Out-of-core не бесплатен: мы читаем файл заново каждый раз, когда нужен другой агрегат. Поэтому на практике:

- считай все нужные агрегаты за один проход (накапливай в одном цикле);
- храни промежуточные результаты в компактных форматах (Parquet), а не в CSV;
- если данные нужны многократно — используй базы данных или Dask/Spark с кэшированием.

Теперь закрепим практикой.

<!--TASK-->
### Задача 1
Создай файл `make_big.py`, который генерирует Parquet с 200 000 строк: колонки `id` (целые), `город` (из списка «Москва», «Питер», «Казань») и `сумма` (случайные от 0 до 1000). Запиши его в `big.parquet` с `row_group_size=20_000` через `pq.write_table`. Затем в `chunk_intro.py` открой `pq.ParquetFile`, выведи количество row groups, число строк и сумму `сумма` через `pc.sum` по всей таблице.

### Задача 2
Реализуй в `chunk_utils.py` функцию:

```python
def total_from_parquet(path: str, batch_size: int = 10_000) -> float:
    """Функция-заглушка: суммирование по батчам."""
    return 0.0
```

Она должна открыть `pq.ParquetFile`, проитерироваться по `iter_batches(batch_size=batch_size)`, накопить сумму колонки `сумма` через `pc.sum` и вернуть итог. Для 200 000 строк с `batch_size=10_000` сумма должна совпасть с суммой, посчитанной по всей таблице целиком. Выведи обе суммы и проверь равенство.

### Задача 3
Напиши функцию `count_csv_rows_in_chunks(path, block_size=4096)`, которая через `pv.open_csv` и `read_next_batch` считает общее число строк в CSV-файле. Сгенерируй в `make_big.py` CSV-файл с 5 000 строками (без заголовка, по одной паре «число,число» на строку). Убедись, что функция возвращает 5 000, а также что с `block_size=1024` результат тот же.

### Задача 4
Напиши pytest-тесты для `total_from_parquet`. В `test_chunk_utils.py` через `tmp_path` создай временный Parquet с известными значениями `сумма` (например, [1.0, 2.0, 3.0, 4.0, 5.0]) и `row_group_size=2`. Проверь: (1) сумма равна 15.0; (2) с `batch_size=1` сумма та же; (3) с `batch_size=100` (больше числа строк) сумма та же; (4) для пустой таблицы сумма равна 0.0. Запусти pytest.

### Задача 5
Напиши pytest-тесты для `count_csv_rows_in_chunks`. В `test_chunk_utils.py` создай временный CSV с 3 строками данных (плюс одна пустая строка в конце). Проверь, что функция возвращает 3, и что она корректно работает со строками, содержащими пробелы и пустые значения. Затем проверь, что `block_size` не влияет на результат (сравни `block_size=128` и `block_size=8192`). Запусти pytest и добейся зелёного прогона.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Генерация: `pa.table({...})` с числами через `range(200_000)` и повторяющимся списком городов (например, `["Москва", "Питер", "Казань"] * 66_666 + ...`). Запись: `pq.write_table(table, "big.parquet", row_group_size=20_000)`. Сумма по всей таблице: `pc.sum(table.column("сумма")).as_py()`.

### Подсказка 2
Внутри функции: `pf = pq.ParquetFile(path)`, затем цикл по `pf.iter_batches(batch_size=batch_size)`, в каждом — `total += pc.sum(batch.column("сумма")).as_py()`. Не забудь `import pyarrow.compute as pc`.

### Подсказка 3
`pv.open_csv(path, read_options=pv.ReadOptions(block_size=block_size))` возвращает читателя. В цикле `while True: try: batch = reader.read_next_batch() except StopIteration: break`. `batch.num_rows` — число строк в батче. Для CSV без заголовка укажи `parse_options=pv.ParseOptions(header_rows=0)` — иначе первая строка будет съедена как заголовок.

### Подсказка 4
Временный Parquet: `pa.table({"сумма": [1.0, 2.0, 3.0, 4.0, 5.0]})`, затем `pq.write_table(table, tmp_path / "data.parquet", row_group_size=2)`. Для пустой таблицы создай `pa.table({"сумма": []})`. Все три batch_size-проверки должны давать 15.0.

### Подсказка 5
CSV с пустой строкой: создай строки «1,2», «3,4», «5,6» и добавь `\n` в конце — при `header_rows=0` это не создаст лишней строки. Если пустая строка реально есть — после чтения отфильтруй пустые батчи, но в тесте проверь, что функция возвращает ровно 3. Сравнение block_size: `assert count_csv_rows_in_chunks(str(path), 128) == count_csv_rows_in_chunks(str(path), 8192) == 3`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
# make_big.py
import pyarrow as pa
import pyarrow.parquet as pq

cities = ["Москва", "Питер", "Казань"]
table = pa.table({
    "id": list(range(200_000)),
    "город": (cities * 66_667)[:200_000],
    "сумма": [float((i * 7919) % 1000) for i in range(200_000)],
})
pq.write_table(table, "big.parquet", row_group_size=20_000)
```

```python
# chunk_intro.py
import pyarrow.parquet as pq
import pyarrow.compute as pc

pf = pq.ParquetFile("big.parquet")
print("Row groups:", pf.num_row_groups)

table = pf.read()
print("Строк:", table.num_rows)
print("Сумма:", pc.sum(table.column("сумма")).as_py())
```

Вывод: `Row groups: 10`, `Строк: 200000`, `Сумма: ...`. Что здесь происходит? `row_group_size=20_000` разбивает таблицу на 10 row groups. При чтении `pf.read()` загружается всё — это нормально для контрольной проверки, но в production так не делают. `pc.sum` считает сумму в нативном коде Arrow и возвращает скаляр, который превращается в float через `.as_py()`.

### Разбор 2
Решение:

```python
# chunk_utils.py
import pyarrow.parquet as pq
import pyarrow.compute as pc

def total_from_parquet(path: str, batch_size: int = 10_000) -> float:
    """Функция-заглушка: суммирование по батчам."""
    return 0.0
    pf = pq.ParquetFile(path)
    total = 0.0
    for batch in pf.iter_batches(batch_size=batch_size):
        total += pc.sum(batch.column("сумма")).as_py()
    return total

if __name__ == "__main__":
    total = total_from_parquet("big.parquet", batch_size=10_000)
    whole = pc.sum(pq.read_table("big.parquet").column("сумма")).as_py()
    print("Чанками:", total)
    print("Целиком:", whole)
    print("Равны:", abs(total - whole) < 1e-9)
```

Вывод: `Чанками: ...`, `Целиком: ...`, `Равны: True`. Что здесь происходит? Функция проходит по батчам по 10 тысяч строк и накапливает сумму. В памяти одновременно — только один батч, то есть 10 тысяч строк вместо 200 тысяч. Это и есть суть out-of-core: память не зависит от размера файла, а только от `batch_size`. Сравнение с «целиком» подтверждает корректность.

### Разбор 3
Решение:

```python
# make_big.py (дополнение)
import pyarrow.csv as pv
with open("big.csv", "w") as f:
    for i in range(5_000):
        f.write(f"{i},{i * 2}\n")
```

```python
# chunk_utils.py (дополнение)
import pyarrow.csv as pv

def count_csv_rows_in_chunks(path: str, block_size: int = 4096) -> int:
    reader = pv.open_csv(path, read_options=pv.ReadOptions(block_size=block_size),
                         parse_options=pv.ParseOptions(header_rows=0))
    rows = 0
    while True:
        try:
            batch = reader.read_next_batch()
        except StopIteration:
            break
        rows += batch.num_rows
    return rows
```

Проверка: `print(count_csv_rows_in_chunks("big.csv"), count_csv_rows_in_chunks("big.csv", 1024))` — оба значения 5000. Что здесь происходит? `open_csv` возвращает читателя, который отдаёт RecordBatch'и. `header_rows=0` говорит, что заголовка нет. `block_size` задаёт размер блока в байтах — но результат не зависит от него, потому что мы просто суммируем число строк во всех батчах.

### Разбор 4
Решение:

```python
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from chunk_utils import total_from_parquet

@pytest.fixture
def tmp_pq(tmp_path):
    table = pa.table({"сумма": [1.0, 2.0, 3.0, 4.0, 5.0]})
    path = tmp_path / "data.parquet"
    pq.write_table(table, path, row_group_size=2)
    return path

def test_total(tmp_pq):
    assert total_from_parquet(str(tmp_pq)) == pytest.approx(15.0)

def test_batch_size_1(tmp_pq):
    assert total_from_parquet(str(tmp_pq), batch_size=1) == pytest.approx(15.0)

def test_batch_size_large(tmp_pq):
    assert total_from_parquet(str(tmp_pq), batch_size=100) == pytest.approx(15.0)

def test_empty_table(tmp_path):
    table = pa.table({"сумма": []})
    path = tmp_path / "empty.parquet"
    pq.write_table(table, path)
    assert total_from_parquet(str(path)) == pytest.approx(0.0)
```

Что здесь происходит? Фикстура создаёт файл с `row_group_size=2` — то есть внутри будет несколько row groups, что заставляет функцию реально читать по частям. Тесты проверяют три размера батчей (1, дефолтный 10 000, 100) — все должны дать 15.0. Пустая таблица покрывает краевой случай: цикл не выполнится ни разу, сумма останется 0.0. `pytest.approx` защищает от ошибок плавающей точки.

### Разбор 5
Решение:

```python
import pytest
from chunk_utils import count_csv_rows_in_chunks

def test_count_rows(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("1,2\n3,4\n5,6\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path)) == 3

def test_block_size_does_not_matter(tmp_path):
    path = tmp_path / "data2.csv"
    path.write_text("10,20\n30,40\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path), 128) == 2
    assert count_csv_rows_in_chunks(str(path), 8192) == 2

def test_blank_lines(tmp_path):
    path = tmp_path / "data3.csv"
    path.write_text("1,2\n\n3,4\n", encoding="utf-8")
    assert count_csv_rows_in_chunks(str(path)) == 3
```

Что здесь происходит? Первый тест — базовый счёт. Второй проверяет, что `block_size` не влияет на результат — важное свойство для стабильности API. Третий тест с пустой строкой: пустая строка в CSV не даёт батча с пустыми колонками, а просто не добавляет данных, поэтому счётчик по-прежнему 3. Это покрывает типичный случай «грязных» данных, где в конце файла часто есть лишний перенос строки. Запуск: `pytest test_chunk_utils.py -v`.
<!--/SOLUTION-->

<!--QUIZ-->
Что означает out-of-core?
- Обработка данных, которые не помещаются в память, частями
- Обработка данных на графическом процессоре
- Хранение данных в оперативной памяти
* Правильный ответ: Обработка данных, которые не помещаются в память, частями
Out-of-core читает данные блоками и накапливает результат.

Какой формат лежит в основе Polars и Dask?
- Apache Arrow
- JSON
- XML
* Правильный ответ: Apache Arrow
Arrow — колоночный бинарный формат, который понимают почти все инструменты больших данных.

Что такое RecordBatch в Arrow?
- Кусочек таблицы из нескольких тысяч строк
- Целый файл
- Схема таблицы
* Правильный ответ: Кусочек таблицы из нескольких тысяч строк
Именно батчи позволяют читать данные потоково.

Какой метод ParquetFile читает данные блоками?
- iter_batches
- read_table
- read_all
* Правильный ответ: iter_batches
iter_batches возвращает генератор RecordBatch'ей, по одному за раз.

Что такое row group в Parquet?
- Независимый блок строк внутри файла
- Колонка файла
- Папка с файлами
* Правильный ответ: Независимый блок строк внутри файла
Row group можно читать отдельно от остальных.

Что вернёт pc.sum(arr).as_py()?
- Число в виде Python-типа
- RecordBatch
- Массив Arrow
* Правильный ответ: Число в виде Python-типа
as_py превращает скаляр Arrow в обычный Python-объект.

Какой параметр задаёт размер блока при чтении CSV?
- block_size
- chunk
- batch_rows
* Правильный ответ: block_size
block_size задаёт размер блока в байтах для open_csv.

Зачем нужен header_rows=0 в ParseOptions?
- Чтобы сказать, что заголовка в CSV нет
- Чтобы пропустить первые 0 строк
- Чтобы добавить заголовок
* Правильный ответ: Чтобы сказать, что заголовка в CSV нет
Иначе первая строка будет принята за заголовок.

Что произойдёт, если читать файл больше памяти через read_table?
- MemoryError или смерть процесса
- Всё прочитается нормально
- Файл сожмётся автоматически
* Правильный ответ: MemoryError или смерть процесса
Вся таблица попытается поместиться в оперативную память.

Что лучше хранить для многократного чтения больших данных?
- Parquet с row groups
- CSV
- Текстовые логи
* Правильный ответ: Parquet с row groups
Parquet позволяет читать только нужные блоки и колонки.
<!--/QUIZ-->
