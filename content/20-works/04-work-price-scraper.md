---
title: Самостоятельная работа: скрейпер цен с уведомлениями
summary: Собери парсер цен с учебного магазина books.toscrape.com, сравнение с целевой ценой и уведомления: в консоль, в файл-лог и через e-mail (SMTP).
order: 4
duration: 180 мин
difficulty: advanced
tags: python, requests, BeautifulSoup, парсинг, цены, smtplib, уведомления, конфигурация
---

Это самая сложная самостоятельная работа модуля: настоящий маленький сервис мониторинга цен. Ты уже знаешь HTTP и парсинг из модуля 17; теперь ты соберёшь из этих знаний законченный инструмент, который умеет сам ходить на сайт, собирать цены, сравнивать их с целевой и уведомлять тебя о выгодных предложениях.

## Постановка задачи

Нужно написать программу `price_scraper.py`, которая периодически заходит на учебный сайт-магазин `https://books.toscrape.com/` (каталог книг с ценами), собирает цены, находит книги дешевле заданного порога и уведомляет тебя: выводит в консоль, пишет в файл-лог и (опционально) отправляет письмо на e-mail через SMTP. Программа запускается, работает в цикле с паузой и корректно завершается по `Ctrl+C`.

Чему ты научишься. Во-первых, уверенной работе с `requests`: сессии, заголовки, тайм-ауты, обработка ошибок сети. Во-вторых, парсингу HTML через `BeautifulSoup`: CSS-селекторы, извлечение атрибутов и текста. В-третьих, грамотной архитектуре: разделение на функции (получение страницы, парсинг, сравнение цен, уведомления), конфигурация в отдельном файле, вежливость по отношению к сайту (паузы между запросами).

## Требования к программе

- Сайт: `https://books.toscrape.com/` — первая страница каталога, на ней 20 книг с ценами в фунтах (`£51.77`).
- Конфигурация лежит в `config.json`: `threshold` (целевая цена), `interval` (секунды между проверками), `email_from`, `email_to`, `smtp_server`, `smtp_port`, `email_password` (можно пустые — тогда письма не отправляются).
- Запросы: `User-Agent`, `timeout`, переиспользование `requests.Session()`, проверка статуса через `raise_for_status()`.
- Парсинг: название книги — из атрибута `title` ссылки в `h3 > a`, цена — из `p.price_color`, нормализация в `float` (убрать `£`).
- Сравнение: книги с ценой ≤ `threshold` считаются выгодными и попадают в уведомление.
- Уведомления: консоль (отчёт с таблицей), файл `alerts.log` (каждая строка — запись с временем), e-mail через `smtplib` если конфигурация заполнена (иначе пропустить).
- Вежливость: пауза минимум 1 секунда между запросами, пауза `interval` между циклами проверки.
- Обработка ошибок сети: `requests.exceptions.RequestException` не должна ронять программу — после ошибки она ждёт следующий цикл.

## Как работать с заданием

Работай по этапам в одном файле `price_scraper.py`. После каждого этапа запускай программу и проверяй результат. Перед сдачей проверь: запуск с настоящим сайтом, запись в `alerts.log`, корректное завершение по `Ctrl+C`. Не забудь про `config.json` — программа должна работать и без почтовых настроек.

## Критерии оценки (10 баллов)

| Критерий | Баллы |
|---|---|
| HTTP-клиент: сессии, заголовки, тайм-ауты, raise_for_status | 2 |
| Парсинг каталога CSS-селекторами, корректная цена в float | 3 |
| Сравнение с порогом и табличный отчёт в консоль | 1 |
| Уведомления: лог-файл с временем, e-mail при наличии конфига | 2 |
| Цикл проверок с паузой, обработка ошибок сети, Ctrl+C | 2 |

Зачтено — от 7 баллов.

## Что сдать

- Файл `price_scraper.py` (полная рабочая версия после 5-го этапа).
- Файл `config.json` (с пустыми почтовыми полями, если нет SMTP).
- Файл `alerts.log` с несколькими записями из твоего теста.
- Пример вывода консоли (в `examples.txt` или комментарии).
- Комментарий в начале файла: как запустить, какие функции есть, что бы ты улучшил.
- Викторина по уроку на платформе (8 вопросов).

<!--TASK-->
### Задача 1

Напиши функцию `get_page(url, session)` с `requests.Session()`, заголовком `User-Agent` и `timeout=15`. После запроса вызови `response.raise_for_status()` и верни `response.text`. Оберни вызов в `try/except requests.exceptions.RequestException` — при ошибке печатай сообщение и возвращай `None`. Проверь на `https://books.toscrape.com/`: текст должен содержать `books` и `toscrape`. Ожидаемый результат — `len(page)` больше 10 000 символов.

### Задача 2

Напиши функцию `parse_books(html)`, которая принимает HTML и возвращает список словарей `{"title": str, "price": float}`. Используй `BeautifulSoup(html, "html.parser")` и селекторы: каждый товар — `article.product_pod`, название — `h3 > a` (атрибут `title`), цена — `p.price_color` (текст вида `£51.77`). Нормализуй цену: убери `£` и преврати в `float`. Проверь: на первой странице должно быть 20 книг, и все цены — положительные числа.

### Задача 3

Напиши функцию `is_bargain(book, threshold)`, которая возвращает `True`, если цена книги ≤ `threshold`. Затем собери список выгодных книг и выведи его таблицей: номер, название, цена. Выравнивание — f-строки с шириной. Проверь с `threshold=50`: в отчёт должны попасть только книги дешевле 50 фунтов. Ожидаемый вывод — строки вида `1. A Light in the Attic  £51.77` и т. д. для выгодных книг.

### Задача 4

Добавь уведомления. Функция `notify(bargains, config)` делает три вещи: печатает отчёт в консоль, дописывает в `alerts.log` построчно с временной меткой (`datetime.now().isoformat(timespec="seconds")`), а если в конфиге есть `smtp_server` — отправляет письмо через `smtplib.SMTP` (обязательно в `try/except`, чтобы сбой почты не ронял программу). Проверь: после запуска в `alerts.log` появляются записи с реальным временем.

### Задача 5

Собери всё в цикл мониторинга. Считай `config.json` (с дефолтами, если файла нет: `threshold=50`, `interval=60`). Цикл `while True`: получай страницу, парси, сравнивай, уведомляй, затем `time.sleep(interval)`. Обработай `KeyboardInterrupt` — при `Ctrl+C` выведи сообщение и завершись аккуратно. Между запросами внутри цикла держи паузу минимум 1 секунду. Проверь: запусти на `interval=10`, дождись 2–3 циклов, заверши через `Ctrl+C`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1

Сессию создавай один раз вне функции: `session = requests.Session()`, заголовок задай так: `session.headers.update({"User-Agent": "PriceScraper/1.0 (student@example.com)"})`. `raise_for_status()` бросит `HTTPError`, если сайт ответил ошибкой, — это отсекает «тихие» неудачи. Обёртка `try/except` с `return None` позволяет вызывающему коду просто проверить `if page is None`.

### Подсказка 2

Селектор товара: `soup.select("article.product_pod")`. Название: `item.select_one("h3 > a")["title"]`. Цена: `item.select_one("p.price_color").text` — например `"£51.77"`. Нормализация: `float(price_text.replace("£", ""))`. Если селектор что-то не нашёл, `select_one` вернёт `None` — проверь и пропусти такой товар.

### Подсказка 3

Простая фильтрация: `[b for b in books if b["price"] <= threshold]`. Для таблицы используй `enumerate(bargains, 1)` и f-строку: `f"{i:>3}. {title:<40} £{price:>6.2f}"`. Обрати внимание: сравнение `<=` включает цену, равную порогу, — это документировано в требованиях.

### Подсказка 4

Запись в лог: `with open("alerts.log", "a", encoding="utf-8") as f: f.write(f"{ts} | {title} | £{price:.2f}\n")` — режим `"a"` дописывает в конец. Для почты: `with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:` затем `server.sendmail(from_addr, to_addr, msg)`. Сообщение собери как `string` в простом формате — заголовки `Subject`, `From`, `To` и тело через пустую строку.

### Подсказка 5

Чтение конфига: `json.load(open("config.json", encoding="utf-8"))` с `try/except (FileNotFoundError, json.JSONDecodeError)` и дефолтами. Обработка `Ctrl+C`: оберни основной цикл в `try: ... except KeyboardInterrupt: print("Завершение работы.")`. Паузу между запросами вставь прямо в цикл: `time.sleep(1)` после обработки страницы — так ты не создашь лишнюю нагрузку на сайт.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```python
import requests

def get_page(url, session):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

session = requests.Session()
session.headers.update({"User-Agent": "PriceScraper/1.0 (student@example.com)"})
page = get_page("https://books.toscrape.com/", session)
print(len(page) if page else "Не удалось получить страницу")
```

Сессия сохраняет куки и заголовки между запросами — это ближе к поведению настоящего браузера. `timeout=15` страхует от зависания. `raise_for_status()` превращает ответы 4xx/5xx в исключение, поэтому молчаливые ошибки статуса не «проскочат». Общая обёртка `RequestException` ловит и сетевые сбои, и тайм-ауты, и HTTP-ошибки.

### Разбор 2

```python
from bs4 import BeautifulSoup

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for item in soup.select("article.product_pod"):
        title_tag = item.select_one("h3 > a")
        price_tag = item.select_one("p.price_color")
        if title_tag is None or price_tag is None:
            continue
        title = title_tag["title"]
        price = float(price_tag.text.replace("£", ""))
        books.append({"title": title, "price": price})
    return books
```

`BeautifulSoup` с встроенным парсером `html.parser` достаточен для учебных страниц. Селектор `article.product_pod` выбирает все карточки товаров, `h3 > a` — ссылку с названием, а атрибут `title` содержит полное название книги (в тексте ссылки оно может обрываться). `p.price_color` хранит строку `£51.77`; после `replace("£", "")` и `float(...)` получаем число. Проверка `is None` защищает от неожиданной вёрстки.

### Разбор 3

```python
def is_bargain(book, threshold):
    return book["price"] <= threshold

def print_report(bargains):
    print(f"\nНайдено выгодных книг: {len(bargains)}")
    for i, book in enumerate(bargains, 1):
        print(f"{i:>3}. {book['title']:<40} £{book['price']:>6.2f}")

bargains = [b for b in parse_books(page) if is_bargain(b, 50)]
print_report(bargains)
```

`is_bargain` — простая чистая функция: получила книгу и порог, вернула булево значение. Фильтрация списком — идиоматичный Python. `print_report` выводит выровненную таблицу: `:>3` прижимает номер вправо, `:<40` — название влево (с обрезкой слишком длинных), `:>6.2f` — цену с двумя знаками после запятой.

### Разбор 4

```python
from datetime import datetime
import smtplib

def log_alerts(bargains):
    ts = datetime.now().isoformat(timespec="seconds")
    with open("alerts.log", "a", encoding="utf-8") as f:
        for book in bargains:
            f.write(f"{ts} | {book['title']} | £{book['price']:.2f}\n")

def send_email(bargains, config):
    if not config.get("smtp_server"):
        return
    try:
        body = "\n".join(f"{b['title']} — £{b['price']:.2f}" for b in bargains)
        msg = f"Subject: Выгодные цены\nFrom: {config['email_from']}\nTo: {config['email_to']}\n\n{body}"
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            if config.get("email_password"):
                server.starttls()
                server.login(config["email_from"], config["email_password"])
            server.sendmail(config["email_from"], config["email_to"], msg)
    except Exception as e:
        print(f"Не удалось отправить письмо: {e}")

def notify(bargains, config):
    print_report(bargains)
    log_alerts(bargains)
    send_email(bargains, config)
```

Лог-файл открывается в режиме `"a"` — дописывание в конец, так история накапливается. ISO-время из `datetime.now().isoformat()` удобно сортировать и читать. Почта отправляется только если в конфиге есть `smtp_server`; при `starttls()` и логине — если задан пароль, иначе — анонимная отправка. Любая ошибка почты ловится и не роняет программу.

### Разбор 5

```python
import json
import time

def load_config(path="config.json"):
    defaults = {"threshold": 50, "interval": 60}
    try:
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
        defaults.update(config)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return defaults

def main():
    config = load_config()
    session = requests.Session()
    session.headers.update({"User-Agent": "PriceScraper/1.0 (student@example.com)"})
    print(f"Мониторинг цен: порог £{config['threshold']}, интервал {config['interval']} с. Ctrl+C — выход.")
    try:
        while True:
            page = get_page("https://books.toscrape.com/", session)
            if page is not None:
                books = parse_books(page)
                bargains = [b for b in books if is_bargain(b, config["threshold"])]
                if bargains:
                    notify(bargains, config)
                else:
                    print(f"{datetime.now().isoformat(timespec='seconds')}: выгодных цен нет")
            time.sleep(1)  # вежливость между запросами
            time.sleep(config["interval"])  # пауза между циклами
    except KeyboardInterrupt:
        print("\nЗавершение работы. Спасибо за использование!")

if __name__ == "__main__":
    main()
```

Конфиг читается с дефолтами — программа работает даже без файла. Бесконечный цикл живёт, пока не нажат `Ctrl+C`: `KeyboardInterrupt` перехватывается, и программа прощается аккуратно, не оставляя «полуживых» состояний. Две паузы соблюдают вежливость: секунда между запросами и `interval` между циклами проверки — так сервер не перегружается.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает response.raise_for_status()?
- Бросает исключение при HTTP-ошибке 4xx/5xx
- Возвращает текст ответа
- Проверяет кодировку
- Закрывает соединение
* Правильный ответ: Бросает исключение при HTTP-ошибке 4xx/5xx
Это защита от молчаливых неудач: статус 404 не пройдёт незамеченным.

Что вернёт float("51.77".replace("£", ""))?
- 51.77
- "51.77"
- 5177
- Ошибку
* Правильный ответ: 51.77
replace убирает символ фунта, а float превращает строку в число с плавающей точкой.

Какой селектор выбирает все карточки товаров на books.toscrape.com?
- article.product_pod
- div.book
- li.product
- .price_color
* Правильный ответ: article.product_pod
Именно такой класс у элемента article каждого товара на страницах каталога.

Что вернёт item.select_one("h3 > a")["title"]?
- Название книги из атрибута title
- Текст ссылки
- HTML ссылки
- Атрибут href
* Правильный ответ: Название книги из атрибута title
Атрибут title ссылки содержит полное название книги.

Зачем переиспользовать requests.Session()?
- Чтобы сохранять куки и заголовки между запросами
- Чтобы ускорить парсинг
- Чтобы обойти блокировку
- Это необязательно
* Правильный ответ: Чтобы сохранять куки и заголовки между запросами
Сессия — контейнер состояния: заголовки, куки и настройки применяются к каждому запросу.

Что означает логин в alerts.log в режиме "a"?
- Дописывание в конец файла
- Перезапись файла
- Создание нового файла
- Чтение файла
* Правильный ответ: Дописывание в конец файла
Режим "a" (append) сохраняет историю: каждая проверка добавляет новые строки.

Что произойдёт при нажатии Ctrl+C в цикле с try/except KeyboardInterrupt?
- Программа выполнит блок except и завершится аккуратно
- Программа игнорирует Ctrl+C
- Ошибка программы
- Перезапуск цикла
* Правильный ответ: Программа выполнит блок except и завершится аккуратно
Это стандартный способ вежливого завершения фоновых циклов.

Зачем ставить паузу между запросами к сайту?
- Чтобы не перегружать сервер (вежливость)
- Чтобы программа работала дольше
- Чтобы избежать ошибок парсинга
- Это не нужно
* Правильный ответ: Чтобы не перегружать сервер (вежливость)
Уважение к ресурсам сайта — часть этики парсинга; слишком частые запросы могут привести к блокировке.

Что возвращает soup.select("article.product_pod")?
- Список всех найденных элементов
- Первый найденный элемент
- Строку с HTML
- None
* Правильный ответ: Список всех найденных элементов
select() возвращает список всех совпадений; select_one() — только первое.

Как обработать отсутствие config.json при загрузке?
- try/except FileNotFoundError с дефолтами
- Не обрабатывать, программа упадёт
- Создать пустой файл
- Остановить программу
* Правильный ответ: try/except FileNotFoundError с дефолтами
Программа продолжает работать с настройками по умолчанию, даже если конфиг не создан.
<!--/QUIZ-->
