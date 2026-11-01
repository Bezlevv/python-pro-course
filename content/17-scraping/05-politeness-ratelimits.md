---
title: Этика парсинга: лимиты и троттлинг
summary: Вежливый парсинг: robots.txt, условия использования, идентификация, троттлинг и экспоненциальная пауза при ошибках.
order: 5
duration: 35 мин
difficulty: intermediate
tags: этика, robots.txt, троттлинг, rate limit, вежливый парсинг
---

Парсинг — это не «грабёж» данных, а взаимодействие с сервером. Хороший парсер думает не только о том, как быстрее всё забрать, но и о том, как не навредить. Слишком частые запросы перегружают сервер, ломают сайты для людей и приводят к блокировке твоего IP. В этом уроке — правила вежливого сбора данных и инструменты, которые их соблюдают.

## Сначала спроси разрешения: robots.txt

Почти у каждого сайта есть файл `robots.txt` — он лежит в корне домена и описывает, что можно сканировать, а что нельзя:

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://quotes.toscrape.com/robots.txt")
rp.read()

print(rp.can_fetch("*", "https://quotes.toscrape.com/page/1/"))
print(rp.can_fetch("*", "https://quotes.toscrape.com/login"))
```

`can_fetch("*", url)` отвечает на вопрос: «можно ли моему агенту (`*` — любой) загрузить этот URL?». Модуль `urllib.robotparser` — стандартный, ничего устанавливать не нужно. Проверяй `robots.txt` перед обходом сайта — особенно если это не учебный полигон.

## Условия использования и личные данные

`robots.txt` — технический сигнал, но юридически важно и то, что написано в условиях использования сайта. Обычно запрещено собирать личные данные (имена, адреса, телефоны) и перепродавать их. Парсинг «для себя» и «для исследований» сам по себе не плох, но если данные касаются людей — подумай, есть ли у тебя право их собирать и хранить. Если сайт явно запрещает парсинг в условиях — уважай это. Для экспериментов используй учебные сайты вроде `quotes.toscrape.com` и `books.toscrape.com`: они созданы специально для тренировки.

## Представься: свой User-Agent

Серверы смотрят на `User-Agent`, чтобы понять, кто к ним пришёл. Честный парсер указывает, кто он такой, и оставляет контакт:

```python
HEADERS = {
    "User-Agent": "StudyScraper/1.0 (contact: student@example.com)",
}
```

Если что-то пойдёт не так (например, твой скрипт зациклится), владелец сайта сможет с тобой связаться. Анонимность здесь — не цель: вежливая идентификация снижает вероятность блокировки.

## Троттлинг: паузы между запросами

Даже если сайт разрешает парсинг, отправлять десятки запросов в секунду не стоит. Добавь паузу между запросами — **троттлинг**:

```python
import time
import requests

for page in range(1, 4):
    r = requests.get(f"https://quotes.toscrape.com/page/{page}/", timeout=10)
    print(page, r.status_code)
    time.sleep(2)  # минимум 2 секунды между запросами
```

Пауза в 1–3 секунды — разумный минимум для небольшого обхода. Для серьёзных проектов добавляют случайный «джиттер» — небольшую случайную вариацию паузы, чтобы трафик не выглядел идеально ритмичным: `time.sleep(1 + random.random())`.

## Лимиты и коды ошибок: 429

Если ты слишком быстр, сервер ответит кодом **429 Too Many Requests** — «слишком много запросов». Это официальный сигнал: притормози. Некоторые серверы даже говорят, сколько ждать, через заголовок `Retry-After`:

```python
import time

delay = 1
for attempt in range(5):
    r = requests.get("https://httpbin.org/status/429", timeout=10)
    if r.status_code == 429:
        wait = float(r.headers.get("Retry-After", delay))
        print(f"429: ждём {wait} с")
        time.sleep(wait)
        delay *= 2
    else:
        r.raise_for_status()
        print("Успех:", r.status_code)
        break
```

Это **экспоненциальная пауза**: с каждой неудачей ждём вдвое дольше (1 с, 2 с, 4 с...). Такой алгоритм даёт серверу время оправиться и не превращает парсер в «долбёжку».

## Другие вежливые приёмы

- **Кэшируй** уже загруженные страницы — не скачивай то же самое дважды.
- **Ограничивай параллельность**: не запускай 50 потоков по одному сайту.
- **Работай в непиковые часы**, если сайт маленький.
- **Останавливайся за пределами рабочего времени**, если сайт явно об этом говорит.

## Итог

Вежливый парсер: проверяет `robots.txt`, читает условия использования, представляется своим `User-Agent`, делает паузы между запросами и корректно реагирует на `429` экспоненциальной паузой. Это не только этично, но и практично: вежливых гостей блокируют реже, а данные собираются надёжнее. Собираем вежливого клиента!

<!--TASK-->
### Задача 1

Напиши программу `check_robots.py`, которая проверяет разрешения для двух учебных сайтов: `https://quotes.toscrape.com/` и `https://books.toscrape.com/`. Для каждого используй `urllib.robotparser.RobotFileParser()`, задай URL `robots.txt` через `set_url`, загрузи через `read()` и выведи результаты `can_fetch("*", ...)` для главной страницы и для адреса `/admin` (если он попадёт под запрет — увидишь `False`). Формат вывода: `Сайт: главная -> True/False, /admin -> True/False`.

### Задача 2

Напиши класс `PoliteFetcher` с конструктором `__init__(self, delay=2.0)`. Внутри храни `self.delay` и словарь `self.headers` со стандартным `User-Agent`: `"StudyScraper/1.0 (contact: student@example.com)"`. Метод `get(self, url)` делает `requests.get(url, headers=self.headers, timeout=10)`, между последовательными запросами делает паузу `self.delay` секунд. Протестируй: собери первые 3 страницы `https://quotes.toscrape.com/page/{n}/` и для каждой выведи номер, код статуса и сколько секунд прошло с предыдущего запроса (`time.time()`).

### Задача 3

Напиши функцию `fetch_with_backoff(url, max_attempts=5)`, которая делает GET-запрос с тайм-аутом 10 секунд. Если статус `429` — читает заголовок `Retry-After` (если его нет, использует текущую задержку) и ждёт это число секунд, затем удваивает задержку и пробует снова. Если статус другой — вызывает `raise_for_status()` и возвращает ответ. Протестируй на `https://httpbin.org/status/429` с `max_attempts=2`: программа должна вывести два предупреждения и упасть с `RuntimeError` после исчерпания попыток.

### Задача 4

Собери содержимое первых двух страниц `https://books.toscrape.com/` вежливым способом: класс `PoliteFetcher` из задачи 2 с `delay=1`. Для каждой страницы выведи номер и количество карточек книг (`article.product_pod`), посчитанное через BeautifulSoup. Убедись, что между запросами есть пауза не меньше 1 секунды. Выведи общее количество книг за два запроса.

### Задача 5

Собери всё вместе: напиши класс `PoliteScraper`, который объединяет проверку `robots.txt` (кэширует результат в словаре `self.robots`), стандартные заголовки и троттлинг с задержкой. Метод `fetch(self, url)` сначала проверяет `robots.txt` сайта через `can_fetch("*", url)`; если нельзя — печатает `Запрещено robots.txt: <url>` и возвращает `None`. Если можно — делает запрос с паузой. Протестируй на `https://quotes.toscrape.com/page/1/` (должен вернуть ответ) и на `https://quotes.toscrape.com/login` (результат может быть любым — выведи, что вернул метод).
<!--/TASK-->

<!--HINT-->
### Подсказка 1

`RobotFileParser` — стандартный модуль `urllib.robotparser`. Порядок: создать, `set_url` (URL файла robots.txt), `read()`, затем `can_fetch("*", url)`. Учебные сайты обычно разрешают почти всё, но `/admin` часто закрыт. Выводи результаты через f-строки.

### Подсказка 2

В классе сохраняй `self.last_request_time` — момент последнего запроса. Перед новым запросом вычисли `elapsed = time.time() - self.last_request_time` и, если `elapsed < self.delay`, спи `self.delay - elapsed` секунд. После запроса обновляй `self.last_request_time = time.time()`. Это точный троттлинг, а не просто «спать после каждого запроса».

### Подсказка 3

Задержку храни в переменной `delay`, начиная с 1. При `429`: `wait = float(r.headers.get("Retry-After", delay))`, затем `time.sleep(wait)` и `delay *= 2`. После `max_attempts` попыток — `raise RuntimeError("Rate limit не отпустил")`. Учитывай: `httpbin.org/status/429` всегда отвечает 429.

### Подсказка 4

Парсинг страниц книжного магазина: `BeautifulSoup(r.text, "lxml")` и `soup.select("article.product_pod")`. Используй класс из задачи 2 — но поскольку ты пишешь отдельный файл, скопируй класс в него. Измеряй паузу через `time.time()` до и после `get()`.

### Подсказка 5

Разбей URL через `urllib.parse.urlparse(url)` — домен: `parsed.netloc`. В `self.robots` храни словарь `{домен: RobotFileParser}`. Если домена нет — создай парсер, `set_url(f"https://{домен}/robots.txt")`, `read()` и сохрани. Затем `self.robots[домен].can_fetch("*", url)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```python
import urllib.robotparser

for site in ("https://quotes.toscrape.com", "https://books.toscrape.com"):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(site + "/robots.txt")
    rp.read()

    main = rp.can_fetch("*", site + "/")
    admin = rp.can_fetch("*", site + "/admin")
    print(f"{site}: главная -> {main}, /admin -> {admin}")
```

Разбор по шагам:

- `RobotFileParser` — стандартный класс из `urllib.robotparser`. Он умеет скачивать `robots.txt` и отвечать на вопросы о разрешениях.
- `set_url(site + "/robots.txt")` указывает адрес файла; `read()` загружает и разбирает его.
- `can_fetch("*", url)` возвращает `True`/`False`: можно ли агенту `*` (любому) загрузить `url`.
- Учебные сайты обычно разрешают сканировать страницы, но закрывают служебные пути вроде `/admin` — там ты увидишь `False`.
- Обрати внимание: `robots.txt` проверяется для каждого домена, перед обходом. Это первая строка «вежливого парсера» — узнай правила, прежде чем идти в гости.

### Разбор 2

```python
import time
import requests

class PoliteFetcher:
    def __init__(self, delay=2.0):
        self.delay = delay
        self.headers = {
            "User-Agent": "StudyScraper/1.0 (contact: student@example.com)",
        }
        self.last_request_time = 0.0

    def get(self, url):
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

fetcher = PoliteFetcher(delay=2.0)
prev = None
for page in range(1, 4):
    r = fetcher.get(f"https://quotes.toscrape.com/page/{page}/")
    now = time.time()
    gap = now - prev if prev else 0.0
    prev = now
    print(f"Страница {page}: статус {r.status_code}, прошло {gap:.1f} с")
```

Разбор по шагам:

- Класс оборачивает вежливое поведение: заголовки, троттлинг, единую точку всех запросов.
- `self.last_request_time` хранит момент прошлого запроса. Перед новым сравниваем `elapsed` с `self.delay`: не прошло ли достаточно времени. Если нет — спим ровно столько, сколько не хватает. Это точнее, чем «спать после каждого запроса», — интервал между запросами не накапливает ошибку.
- `self.headers` — честная идентификация: `User-Agent` с контактом. Это позволяет владельцу сайта связаться с тобой при проблемах.
- В тесте `gap` показывает фактическую паузу между запросами — она не меньше 2 секунд. Если бы запрос занял много времени, `gap` учёл бы это.
- Такой класс — фундамент любого серьёзного парсера: в одном месте живут правила приличия.

### Разбор 3

```python
import time
import requests

def fetch_with_backoff(url, max_attempts=5):
    delay = 1.0
    for attempt in range(max_attempts):
        r = requests.get(url, timeout=10)
        if r.status_code == 429:
            wait = float(r.headers.get("Retry-After", delay))
            print(f"Попытка {attempt + 1}: 429, ждём {wait} с")
            time.sleep(wait)
            delay *= 2
            continue
        r.raise_for_status()
        return r
    raise RuntimeError("Rate limit не отпустил")

try:
    fetch_with_backoff("https://httpbin.org/status/429", max_attempts=2)
except RuntimeError as e:
    print("Итог:", e)
```

Разбор по шагам:

- `delay = 1.0` — начальная пауза. На каждой неудаче она удваивается: 1 с, 2 с, 4 с, 8 с...
- При `429` сначала пробуем взять `Retry-After` — заголовок, в котором сервер сам сообщает, сколько ждать. Если его нет — используем текущую `delay`.
- `time.sleep(wait)` — реальное ожидание. `delay *= 2` готовит следующую, более длинную паузу.
- `continue` переходит к следующей попытке. Если статус не 429 — `raise_for_status()` проверит остальные ошибки, а успех вернёт `r`.
- После `max_attempts` неудач — `RuntimeError`: парсер не будет долбить вечно, а честно сообщит, что не справился с лимитом.
- Тест на `httpbin.org/status/429` всегда отвечает 429, поэтому программа дважды выведет предупреждение и упадёт с `RuntimeError` — ровно как задумано.

### Разбор 4

```python
import time
import requests
from bs4 import BeautifulSoup

class PoliteFetcher:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.headers = {"User-Agent": "StudyScraper/1.0 (contact: student@example.com)"}
        self.last_request_time = 0.0

    def get(self, url):
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

fetcher = PoliteFetcher(delay=1.0)
total = 0

for page in range(1, 3):
    t0 = time.time()
    r = fetcher.get(f"https://books.toscrape.com/catalogue/page-{page}.html")
    soup = BeautifulSoup(r.text, "lxml")
    books = soup.select("article.product_pod")
    total += len(books)
    print(f"Страница {page}: книг {len(books)}, запрос занял {time.time() - t0:.1f} с")

print("Всего книг:", total)
```

Разбор по шагам:

- Обрати внимание на адреса: у книжного магазина пагинация не `page/1/`, а `catalogue/page-1.html` — каждый сайт делает по-своему. Парсер должен уметь заметить такое.
- `fetch` через `PoliteFetcher` гарантирует паузу минимум 1 секунду между запросами.
- `BeautifulSoup(r.text, "lxml")` + `select("article.product_pod")` считают карточки книг на странице (их 20).
- Замер `time.time() - t0` показывает, сколько занял весь цикл «запрос + пауза». Даже на быстрой сети между запросами будет интервал не меньше заданного.
- Суммируя книги по страницам, получаем общее количество. Это учебный пример: сбор с пагинацией и уважением к серверу.

### Разбор 5

```python
import time
import requests
from urllib.parse import urlparse
import urllib.robotparser

class PoliteScraper:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.headers = {"User-Agent": "StudyScraper/1.0 (contact: student@example.com)"}
        self.last_request_time = 0.0
        self.robots = {}

    def _check_robots(self, url):
        domain = urlparse(url).netloc
        if domain not in self.robots:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            rp.read()
            self.robots[domain] = rp
        return self.robots[domain].can_fetch("*", url)

    def fetch(self, url):
        if not self._check_robots(url):
            print(f"Запрещено robots.txt: {url}")
            return None
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
        r = requests.get(url, headers=self.headers, timeout=10)
        self.last_request_time = time.time()
        return r

scraper = PoliteScraper(delay=1.0)

r = scraper.fetch("https://quotes.toscrape.com/page/1/")
print("Главная:", r.status_code if r else None)

r = scraper.fetch("https://quotes.toscrape.com/login")
print("/login:", r.status_code if r else None)
```

Разбор по шагам:

- `_check_robots(url)` определяет домен через `urlparse(url).netloc` и проверяет кэш `self.robots`: если этот домен ещё не проверялся — создаёт и сохраняет `RobotFileParser`. Повторная проверка не перекачивает файл.
- Если `robots.txt` запрещает URL — метод печатает предупреждение и возвращает `None`. Парсер не нарушает правила даже случайно.
- Троттлинг — тот же, что в `PoliteFetcher`: пауза до минимального интервала между запросами.
- Честный `User-Agent` с контактом задан один раз в `self.headers`.
- Тест: `/page/1/` обычно разрешён и вернёт ответ, `/login` — служебная страница, её статус может быть любым: главное, что программа честно сообщит результат проверки.
- Такой класс — готовый «скелет» вежливого парсера: правила, лимиты и идентификация собраны в одном месте.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое robots.txt?
- Файл со статистикой посещений сайта
- Файл с правилами, какие части сайта можно сканировать
- Зашифрованный файл с паролями
- Служебный файл для настройки сервера
* Правильный ответ: Файл с правилами, какие части сайта можно сканировать
robots.txt лежит в корне сайта и описывает, что разрешено/запрещено для сканеров.

Как в Python проверить разрешение из robots.txt?
- requests.get("robots.txt")
- urllib.robotparser.RobotFileParser().can_fetch()
- bs4.BeautifulSoup
- os.stat("robots.txt")
* Правильный ответ: urllib.robotparser.RobotFileParser().can_fetch()
RobotFileParser загружает файл, can_fetch("*", url) отвечает, можно ли его скачивать.

Что означает HTTP-код 429?
- Страница не найдена
- Слишком много запросов (rate limit)
- Требуется авторизация
- Внутренняя ошибка сервера
* Правильный ответ: Слишком много запросов (rate limit)
429 Too Many Requests — сервер просит притормозить; часто указывается заголовок Retry-After.

Что такое троттлинг?
- Ускорение запросов за счёт параллельности
- Ограничение частоты запросов паузами
- Сжатие передаваемых данных
- Шифрование запросов
* Правильный ответ: Ограничение частоты запросов паузами
Троттлинг вставляет задержки между запросами, чтобы не перегружать сервер.

Зачем в экспоненциальной паузе удваивать задержку?
- Чтобы быстрее закончить обход
- Чтобы дать серверу время оправиться и не «долбить» его
- Чтобы обойти блокировку по IP
- Чтобы сэкономить трафик
* Правильный ответ: Чтобы дать серверу время оправиться и не «долбить» его
С каждой неудачей ждём вдвое дольше — нагрузка на сервер падает, шанс успеха растёт.

Зачем указывать свой контакт в User-Agent?
- Без него запросы не отправляются
- Чтобы владелец сайта мог связаться при проблемах
- Чтобы ускорить ответ сервера
- Чтобы скрыть свой IP
* Правильный ответ: Чтобы владелец сайта мог связаться при проблемах
Честная идентификация снижает риск блокировки и позволяет решить проблемы вежливо.

Что означает HTTP-код 403 при парсинге?
- Доступ запрещён — повторять запрос бессмысленно
- Страница не найдена
- Сервер временно перегружен
- Требуется перенаправление
* Правильный ответ: Доступ запрещён — повторять запрос бессмысленно
403 — постоянный отказ, ретраи здесь не помогут. В отличие от 5xx, повторяют только временные ошибки.

Зачем к паузе между запросами добавляют случайный «джиттер»?
- Чтобы трафик не выглядел идеально ритмичным
- Чтобы ускорить сбор данных
- Чтобы обойти запреты robots.txt
- Это требование модуля smtplib
* Правильный ответ: Чтобы трафик не выглядел идеально ритмичным
Выражение time.sleep(1 + random.random()) делает интервалы неравномерными — нагрузка выглядит естественнее.
<!--/QUIZ-->
