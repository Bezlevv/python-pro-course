---
title: Асинхронная производительность и пулы
summary: Как asyncio ускоряет I/O-bound-код, почему нельзя блокировать цикл событий и как использовать пулы потоков и процессов через run_in_executor и to_thread.
order: 5
duration: 30 мин
difficulty: advanced
tags: asyncio, пулы, ThreadPoolExecutor, ProcessPoolExecutor, Semaphore
---

Асинхронное программирование в Python строится вокруг **цикла событий** (event loop): одна «нить» безостановочно обрабатывает задачи, а когда задача ждёт ввода-вывода, цикл переключается на другую. Это даёт огромный выигрыш на I/O-bound-задачах: сетевых запросах, работе с базами данных, чтении файлов. Ловушка — блокирующие операции внутри корутин: они останавливают весь цикл. В этом уроке разберёмся, как измерять производительность asyncio, как «заворачивать» блокирующий код в пулы и как ограничивать степень конкурентности.

## Модель asyncio

Корутина объявляется `async def` и исполняется до первого `await`. В момент `await` управление возвращается циклу событий, который запускает другую готовую задачу. Так «параллельность» достигается кооперативно, без потоков и без GIL.

Самый простой способ запустить несколько корутин вместе — `asyncio.gather`:

```python
import asyncio
import time

async def fetch(i):
    await asyncio.sleep(0.2)   # имитация сетевого запроса
    return i * 2

async def main():
    t0 = time.perf_counter()
    results = await asyncio.gather(*(fetch(i) for i in range(5)))
    t1 = time.perf_counter()
    print(results)
    print(f"время: {t1 - t0:.2f} сек")  # ~0.2 сек, а не 1.0

asyncio.run(main())
```

Пять корутин суммарно «спят» 1 секунду, но выполнение занимает ~0.2 секунды: цикл ждёт все пять запросов одновременно. Это и есть суть asyncio — конкурентное ожидание, а не истинная параллельность вычислений.

## Блокирующий код убивает цикл событий

Если внутри корутины вызвать синхронную блокирующую операцию (например, `time.sleep(1)` или тяжёлое вычисление), цикл событий **замирает** целиком — никакие другие корутины не смогут работать, пока она не завершится:

```python
import asyncio
import time

async def bad():
    time.sleep(1)      # блокирует весь цикл событий!

async def good():
    await asyncio.sleep(1)  # отдаёт управление циклу

async def main():
    t0 = time.perf_counter()
    await asyncio.gather(bad(), bad())
    t1 = time.perf_counter()
    print(f"с time.sleep: {t1 - t0:.2f} сек")  # ~2 сек

    t0 = time.perf_counter()
    await asyncio.gather(good(), good())
    t1 = time.perf_counter()
    print(f"с asyncio.sleep: {t1 - t0:.2f} сек")  # ~1 сек

asyncio.run(main())
```

Правило: в корутинах нельзя использовать блокирующие вызовы. Но реальный код часто содержит синхронные библиотеки — для них есть `asyncio.to_thread` и пулы.

## asyncio.to_thread: блокирующий код — в пул потоков

`asyncio.to_thread(func, *args)` выполняет `func` в отдельном потоке из встроенного пула и возвращает awaitable. Цикл событий остаётся свободным:

```python
import asyncio
import time

def blocking_work(x):
    time.sleep(0.5)
    return x * 10

async def main():
    t0 = time.perf_counter()
    results = await asyncio.gather(
        asyncio.to_thread(blocking_work, 1),
        asyncio.to_thread(blocking_work, 2),
    )
    t1 = time.perf_counter()
    print(results)
    print(f"время: {t1 - t0:.2f} сек")  # ~0.5 сек

asyncio.run(main())
```

Пул потоков — это `concurrent.futures.ThreadPoolExecutor` внутри. Помни: потоки в классическом CPython ограничены GIL, поэтому для CPU-bound-вычислений `to_thread` не даст ускорения — нужны процессы.

## run_in_executor: пул процессов для вычислений

Для настоящей параллельности вычислений есть `loop.run_in_executor(pool, func, *args)` с `ProcessPoolExecutor`. Каждый процесс — отдельный интерпретатор, поэтому тяжёлые расчёты разойдутся по ядрам:

```python
import asyncio
import concurrent.futures

def cpu_heavy(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

async def main():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        results = await asyncio.gather(
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
        )
    print(results)

asyncio.run(main())
```

`ProcessPoolExecutor` как контекстный менеджер корректно закрывает процессы. Важно: аргументы и результаты функций между процессами сериализуются (pickle), поэтому они должны быть простыми.

## Ограничение конкурентности: Semaphore

`gather` запускает всё сразу. Если задач много, а внешний сервис не выдержит натиска, конкурентность нужно ограничить. Классический инструмент — `asyncio.Semaphore`:

```python
import asyncio

semaphore = asyncio.Semaphore(3)

async def limited_task(i):
    async with semaphore:
        await asyncio.sleep(0.1)
        return i

async def main():
    results = await asyncio.gather(*(limited_task(i) for i in range(10)))
    print(results)

asyncio.run(main())
```

Одновременно выполняются не больше 3 корутин; остальные ждут освобождения слота. Это и есть «троттлинг» — важный приём для продакшена.

## Итог урока

asyncio ускоряет I/O-bound-код за счёт конкурентного ожидания. Блокирующие вызовы внутри корутин нужно выносить: `asyncio.to_thread` — для I/O-библиотек, `loop.run_in_executor` с `ProcessPoolExecutor` — для CPU-bound. Конкурентность ограничивается через `asyncio.Semaphore`. Попрактикуемся.

<!--TASK-->
### Задача 1
Напиши корутину `fetch(i)`, которая `await asyncio.sleep(0.2)` и возвращает `i * 2`. В `main()` выполни 5 таких корутин **последовательно** (в цикле по одной через `await fetch(i)`) и замерь время `time.perf_counter()`. Затем — **конкурентно** через `asyncio.gather` и снова замерь. Выведи результаты и оба времени. В комментарии объясни разницу (ожидай ~1.0 сек против ~0.2 сек).

### Задача 2
Создай корутину `task(name, delay)`, которая печатает `start: name`, затем `await asyncio.sleep(delay)` и печатает `end: name`. В `main()` запусти через `asyncio.gather` две такие задачи с `delay=0.3` и `delay=0.3`. Выведи пары «start/end» в порядке их появления. В комментарии объясни, почему обе `end`-строки появятся почти одновременно, хотя задачи выполняются в одном потоке.

### Задача 3
Напиши функцию `blocking_work(x)`, которая делает `time.sleep(0.5)` и возвращает `x * 10`. В `main()` запусти через `asyncio.gather` 4 вызова `asyncio.to_thread(blocking_work, i)` для `i` от 1 до 4, замерь время. Выведи результаты и время. В комментарии объясни, почему суммарное время ~0.5 сек, а не 2 сек, и что было бы при прямом вызове `blocking_work` в корутине.

### Задача 4
Напиши функцию `cpu_heavy(n)` — сумму квадратов от 0 до `n-1` через `concurrent.futures.ProcessPoolExecutor` и `loop.run_in_executor` в корутине: запусти 3 задачи по `n=3_000_000`, дождись через `asyncio.gather`, выведи результаты. Замерь время всего запуска через `time.perf_counter()` вокруг `asyncio.run(main())`. В комментарии объясни, почему для CPU-bound нужен именно пул процессов, а не потоков.

### Задача 5
Создай `semaphore = asyncio.Semaphore(2)` и корутину `limited_task(i)`, которая внутри `async with semaphore:` печатает `Старт: i`, ждёт `await asyncio.sleep(0.2)` и печатает `Финиш: i`. В `main()` запусти через `asyncio.gather` 6 таких задач. Выведи всю последовательность сообщений. В комментарии объясни, почему в любой момент времени «Старт» печатают максимум две задачи.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Последовательно: `for i in range(5): await fetch(i)`. Конкурентно: `await asyncio.gather(*(fetch(i) for i in range(5)))`. Замеряй вокруг каждого блока: `t0 = time.perf_counter()` … `t1 = time.perf_counter()`.

### Подсказка 2
Печать внутри корутины: `print(f"start: {name}")`. `gather` запускает задачи, и они переключаются в момент `await asyncio.sleep`. Порядок start-строк — по порядку запуска, end-строки появятся вместе после общего ожидания.

### Подсказка 3
`to_thread` возвращает awaitable: `await asyncio.to_thread(blocking_work, 1)`. В gather передавай выражения: `asyncio.to_thread(blocking_work, i)`. Прямой вызов `blocking_work` в корутине заблокировал бы цикл на 0.5 сек на каждую задачу.

### Подсказка 4
`with concurrent.futures.ProcessPoolExecutor() as pool:` — внутри `loop.run_in_executor(pool, cpu_heavy, 3_000_000)`. Не забудь `asyncio.get_running_loop()`. Результаты — список из трёх одинаковых чисел. Если процессы не успевают стартовать, добавь прогрев: два «холостых» вызова не нужны, достаточно спокойно дождаться gather.

### Подсказка 5
`async with semaphore:` сам захватывает и освобождает слот. Печать до `await`. С 6 задачами и семафором 2 в любой момент «Старт» печатают только 2 задачи: остальные ждут внутри `async with`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import asyncio
import time

async def fetch(i):
    await asyncio.sleep(0.2)
    return i * 2

async def main():
    t0 = time.perf_counter()
    seq = []
    for i in range(5):
        seq.append(await fetch(i))
    t1 = time.perf_counter()
    print("последовательно:", seq)
    print(f"время: {t1 - t0:.2f} сек")

    t0 = time.perf_counter()
    conc = await asyncio.gather(*(fetch(i) for i in range(5)))
    t1 = time.perf_counter()
    print("конкурентно:", conc)
    print(f"время: {t1 - t0:.2f} сек")

asyncio.run(main())
```

Результат:

```
последовательно: [0, 2, 4, 6, 8]
время: 1.00 сек
конкурентно: [0, 2, 4, 6, 8]
время: 0.20 сек
```

Что здесь происходит? В последовательном варианте каждая корутина ждёт свой `sleep(0.2)` одна за другой: 5 × 0.2 = 1.0 сек. В `gather` все 5 корутин стартуют сразу: каждая доходит до `await asyncio.sleep`, отдаёт управление циклу, и все пять ожиданий идут параллельно — суммарно 0.2 сек. Это и есть конкурентное ожидание: выигрыш не в вычислениях, а в том, что время ожидания перекрывается. `gather` возвращает результаты в порядке аргументов.

### Разбор 2
Решение:

```python
import asyncio

async def task(name, delay):
    print(f"start: {name}")
    await asyncio.sleep(delay)
    print(f"end: {name}")

async def main():
    await asyncio.gather(
        task("A", 0.3),
        task("B", 0.3),
    )

asyncio.run(main())
```

Результат:

```
start: A
start: B
end: A
end: B
```

Что здесь происходит? Задачи стартуют по очереди: «A» печатает start, доходит до `await` и возвращает управление; «B» печатает start и тоже засыпает. Через 0.3 сек цикл событий будит обе, и end-строки печатаются почти подряд (порядок может слегка различаться). Это наглядно показывает кооперативную модель: один поток, много «спящих» корутин, и никто никого не блокирует.

### Разбор 3
Решение:

```python
import asyncio
import time

def blocking_work(x):
    time.sleep(0.5)
    return x * 10

async def main():
    t0 = time.perf_counter()
    results = await asyncio.gather(
        asyncio.to_thread(blocking_work, 1),
        asyncio.to_thread(blocking_work, 2),
        asyncio.to_thread(blocking_work, 3),
        asyncio.to_thread(blocking_work, 4),
    )
    t1 = time.perf_counter()
    print(results)
    print(f"время: {t1 - t0:.2f} сек")

asyncio.run(main())
```

Результат:

```
[10, 20, 30, 40]
время: 0.50 сек
```

Что здесь происходит? `asyncio.to_thread` кладёт `blocking_work` в пул потоков. Четыре потока спят одновременно по 0.5 сек — суммарно 0.5 сек. Если бы мы вызвали `blocking_work(1)` прямо в корутине, цикл событий замер бы на 0.5 сек, затем на вторую задачу — ещё 0.5, и так далее: вышло бы 2 сек. Важно: `time.sleep` внутри потока не мешает циклу событий, потому что поток — вне цикла. `to_thread` — правильный способ интеграции синхронных I/O-библиотек в asyncio.

### Разбор 4
Решение:

```python
import asyncio
import concurrent.futures
import time

def cpu_heavy(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

async def main():
    loop = asyncio.get_running_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        results = await asyncio.gather(
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
            loop.run_in_executor(pool, cpu_heavy, 3_000_000),
        )
    print(results)

t0 = time.perf_counter()
asyncio.run(main())
t1 = time.perf_counter()
print(f"общее время: {t1 - t0:.2f} сек")
```

Результат:

```
[2999998500000500000, 2999998500000500000, 2999998500000500000]
общее время: 1.10 сек
```

Что здесь происходит? Три вызова `cpu_heavy` — это вычисления, упирающиеся в процессор. Пул потоков здесь не помог бы: GIL разрешает исполнять байт-код только одному потоку. `ProcessPoolExecutor` создаёт отдельные процессы — у каждого свой интерпретатор и свой GIL, поэтому три задачи реально разошлись по ядрам. Время ~1.1 сек — это примерно время одной задачи (одна задача ~1 сек) плюс накладные расходы на старт процессов и передачу данных. Если бы это было последовательно, заняло бы ~3 сек. Помни: аргументы и результаты сериализуются через pickle, поэтому они должны быть простыми объектами.

### Разбор 5
Решение:

```python
import asyncio

semaphore = asyncio.Semaphore(2)

async def limited_task(i):
    async with semaphore:
        print(f"Старт: {i}")
        await asyncio.sleep(0.2)
        print(f"Финиш: {i}")

async def main():
    await asyncio.gather(*(limited_task(i) for i in range(6)))

asyncio.run(main())
```

Результат (порядок финишей может варьироваться):

```
Старт: 0
Старт: 1
Финиш: 0
Финиш: 1
Старт: 2
Старт: 3
Финиш: 2
Финиш: 3
Старт: 4
Старт: 5
Финиш: 4
Финиш: 5
```

Что здесь происходит? `asyncio.Semaphore(2)` разрешает одновременно не больше двух владельцев. Первые две задачи проходят сквозь `async with semaphore` и печатают «Старт». Остальные четыре ждут у входа. Когда задача 0 заканчивает сон и выходит из `async with`, слот освобождается — и следующая задача заходит. Поэтому паттерн повторяется: всегда активны ровно две задачи. Это ограничение конкурентности (троттлинг) — незаменимо при работе с внешними API с лимитами запросов.
<!--/SOLUTION-->

<!--QUIZ-->
В чём суть asyncio?
- В использовании множества потоков
- В кооперативной конкурентности: один цикл событий переключается между ожидающими корутинами
- В параллельном исполнении байт-кода
- В компиляции в C
* Правильный ответ: В кооперативной конкурентности: один цикл событий переключается между ожидающими корутинами
Во время await корутина отдаёт управление циклу, и цикл исполняет другую готовую задачу.

Что произойдёт, если в корутине вызвать time.sleep(1)?
- Ничего страшного
- Цикл событий заблокируется целиком на 1 секунду
- Sleep преобразуется в await автоматически
- Задача уйдёт в отдельный поток
* Правильный ответ: Цикл событий заблокируется целиком на 1 секунду
Блокирующий вызов останавливает цикл: никакие другие корутины не исполнятся.

Что делает asyncio.to_thread?
- Компилирует функцию в C
- Выполняет функцию в потоке из пула, не блокируя цикл событий
- Запускает новый процесс
- Отменяет задачу
* Правильный ответ: Выполняет функцию в потоке из пула, не блокируя цикл событий
to_thread — удобная обёртка над пулом потоков для синхронных I/O-функций.

Почему для CPU-bound-вычислений в asyncio нужен ProcessPoolExecutor?
- Потому что потоки упираются в GIL: байт-код исполняет один поток
- Потому что процессы быстрее создаются
- Потому что потоки не существуют
- Потому что gather не работает с потоками
* Правильный ответ: Потому что потоки упираются в GIL: байт-код исполняет один поток
Каждый процесс — отдельный интерпретатор, поэтому вычисления разбегаются по ядрам.

Как ограничить число одновременно выполняющихся корутин?
- asyncio.Semaphore(N)
- asyncio.Queue
- threading.Lock
- time.sleep
* Правильный ответ: asyncio.Semaphore(N)
Семафор разрешает только N одновременных владельцев; остальные ждут.

Что возвращает asyncio.gather?
- Корутины
- Список результатов в порядке переданных awaitables
- Число задач
- Логи
* Правильный ответ: Список результатов в порядке переданных awaitables
Порядок соответствует порядку аргументов, а не времени завершения.

Какая операция — блокирующая для цикла событий?
- await asyncio.sleep(1)
- time.sleep(1)
- await asyncio.gather(...)
- await asyncio.to_thread(func)
* Правильный ответ: time.sleep(1)
time.sleep синхронна: она не отдаёт управление циклу событий.

Что происходит с аргументами и результатами функций в ProcessPoolExecutor?
- Они передаются напрямую через память
- Они сериализуются (pickle) при передаче между процессами
- Они игнорируются
- Они хранятся в БД
* Правильный ответ: Они сериализуются (pickle) при передаче между процессами
У процессов раздельная память, поэтому данные упаковываются и распаковываются.

Почему 5 корутин с await asyncio.sleep(0.2) выполняются ~0.2 сек?
- Потому что sleep параллелит вычисления
- Потому что ожидания перекрываются: цикл ждёт все пять одновременно
- Потому что sleep быстрее на малых числах
- Потому что gather ускоряет код вдвое
* Правильный ответ: Потому что ожидания перекрываются: цикл ждёт все пять одновременно
Суммарное время определяется самым долгим ожиданием, а не суммой.

Что лучше для синхронной I/O-функции внутри корутины?
- Вызвать её напрямую
- async viacio.to_thread(blocking_work, x)
- time.sleep
- Использовать глобальную переменную
* Правильный ответ: asyncio.to_thread(blocking_work, x)
Прямой вызов заблокировал бы цикл событий; to_thread уводит работу в пул потоков.
<!--/QUIZ-->
