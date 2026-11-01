---
title: Динамические страницы: Selenium и Playwright
summary: Когда HTML приходит «пустым»: Selenium WebDriver и Playwright для страниц, которые рендерятся JavaScript-ом.
order: 3
duration: 45 мин
difficulty: advanced
tags: selenium, playwright, браузер, javascript, динамические страницы
---

Бывает так: `requests` скачал страницу, а в ней нет ни одного товара, ни одной цитаты — только пустой каркас. Это значит, что контент создаёт JavaScript уже в браузере: сервер отдаёт оболочку, а данные подгружаются скриптами. `requests` не запускает JS, поэтому видит пустоту. Для таких страниц нужен настоящий браузер, которым управляет программа. Два главных инструмента — **Selenium** и **Playwright**.

## Когда нужен браузер

Признаки динамической страницы: данные появляются после прокрутки (бесконечная лента), контент грузится кнопкой «Показать ещё», страница перестраивается под действия пользователя. Спроси себя: «а увижу ли я эти данные, если выключить JavaScript?». Если нет — нужен браузер.

## Selenium: классика жанра

Selenium управляет настоящим браузером через WebDriver. Установка:

```bash
pip install selenium
```

Драйвер Chrome (ChromeDriver) Selenium умеет скачивать сам, но проще использовать **Selenium Manager**, входящий в состав библиотеки, — он сам подберёт драйвер под твою версию браузера. Базовый скрипт:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless=new")  # без окна
driver = webdriver.Chrome(options=options)
driver.get("https://quotes.toscrape.com/")

quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
print(len(quotes))

driver.quit()  # всегда закрывай браузер
```

`find_elements(By.CSS_SELECTOR, "div.quote")` — поиск элементов по CSS-селектору, как в BeautifulSoup. `find_element` (без `s`) вернёт первый или бросит исключение, если его нет.

## Ожидания: не спи, а жди

Раньше программисты вставляли `time.sleep(5)` и надеялись, что страница успеет загрузиться. Это плохо: либо ждёшь слишком долго, либо слишком мало. Правильный способ — **явные ожидания**: жди, пока условие не выполнится, максимум N секунд:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
quote = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote")))
```

Здесь Selenium ждёт появления элемента до 10 секунд и не тратит ни миллисекунды лишней.

## Playwright: современная альтернатива

Playwright — более молодой инструмент от тех же людей, что сделали Puppeteer. Его фишки: автоматические ожидания (не нужно вручную дожидаться элементов), простой синхронный API и один код для Chrome, Firefox и Safari.

```bash
pip install playwright
playwright install chromium
```

Команда `playwright install chromium` скачивает сам браузер. Первый скрипт:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")

    page.wait_for_selector("div.quote")  # ждём цитаты
    quotes = page.locator("div.quote")
    print(quotes.count())

    browser.close()
```

`page.locator("div.quote")` — «локейтор»: описание элементов, а не их список. Он не выполняет поиск сразу, а делает это в момент обращения. Методы: `.count()` — сколько элементов, `.first` — первый, `.inner_text()` — текст, `.all_inner_texts()` — тексты всех.

## Клики, скриншоты и формы

Playwright умеет всё то, что делает пользователь в браузере:

```python
page.locator("input#search").fill("python")
page.locator("button").click()
page.wait_for_selector("div.result")
page.screenshot(path="result.png")
```

`fill()` вводит текст в поле, `click()` кликает, `wait_for_selector()` ждёт результат. Скриншоты помогают отладить парсер: сохранил картинку — увидел, что реально открылось в браузере.

## Что выбрать

Для коротких задач и быстрого старта — Playwright: меньше кода, авто-ожидания, один инструмент для трёх браузеров. Selenium полезен, когда нужен зрелый инструмент с огромным сообществом или специфические сценарии (например, управление уже открытым браузером). Главное — не забудь закрыть браузер: в Playwright за это отвечает `with`-блок, в Selenium — `driver.quit()`.

## Итог

Динамические страницы — не приговор: запускаем браузер, ждём появления элементов, собираем данные. Playwright и Selenium дают один и тот же набор суперспособностей — клики, заполнение форм, ожидания, скриншоты. Упражняемся!

<!--TASK-->
### Задача 1

Напиши первый скрипт на Playwright `first_playwright.py`. С помощью `sync_playwright()` открой `https://quotes.toscrape.com/` в Chromium (headless). После `page.goto()` дождись появления блоков цитат через `page.wait_for_selector("div.quote")`, затем выведи заголовок страницы через `page.title()` и количество цитат через `page.locator("div.quote").count()`. Не забудь закрыть браузер. Ожидаемый вывод: заголовок `Quotes to Scrape` и число `10`.

### Задача 2

На странице `https://quotes.toscrape.com/` найди цитату, в тексте которой есть фраза `The world is a book`. Через `page.locator("div.quote", has_text="The world is a book")` выбери блок цитаты, затем внутри него с помощью `locator("small.author").inner_text()` достань автора. Выведи автора и полный текст цитаты через `locator("span.text").inner_text()`. Ожидаемый вывод: автор `Albert Einstein` и текст цитаты.

### Задача 3

Напиши программу `next_pages.py`, которая проходит по трём страницам сайта цитат с помощью кнопки «Next». Старт — `https://quotes.toscrape.com/page/1/`. После загрузки каждой страницы собери авторов через `page.locator("small.author").all_inner_texts()` и добавь их в множество. Затем найди кнопку через `page.locator("li.next a")`, кликни `click()` и дождись следующей страницы через `page.wait_for_selector("div.quote")`. В конце выведи количество уникальных авторов за три страницы.

### Задача 4

Открой `https://books.toscrape.com/` в Playwright, дождись карточек книг (`article.product_pod`). Сделай скриншот главной страницы в файл `books.png` через `page.screenshot(path="books.png")`. Затем проверь через `pathlib.Path("books.png").exists()`, что файл создан, и выведи его размер в байтах через `.stat().st_size`. Не забудь закрыть браузер.

### Задача 5

Поработай с динамической формой. Открой `https://demo.playwright.dev/todomvc/` — это демо-приложение списка дел на JavaScript. Найди поле ввода через `page.locator("input.new-todo")`, введи текст `Купить молоко` через `fill()`, нажми `Enter` через `press("Enter")`. Дождись появления элемента списка через `page.wait_for_selector("ul.todo-list li")` и выведи количество задач через `page.locator("ul.todo-list li").count()`. Ожидаемый вывод: `1`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1

Оборачивай работу в `with sync_playwright() as p:`. Браузер: `browser = p.chromium.launch(headless=True)`, страница: `page = browser.new_page()`. `page.wait_for_selector("div.quote")` подождёт, пока цитаты загрузятся. `page.title()` — заголовок вкладки.

### Подсказка 2

`page.locator("div.quote", has_text="The world is a book")` ищет блок цитаты, в тексте которого есть эта фраза. Автор: `quote.locator("small.author").inner_text()`. Текст: `quote.locator("span.text").inner_text()`. `inner_text()` возвращает видимый текст элемента.

### Подсказка 3

Собери авторов страницы в множество: `authors.update(page.locator("small.author").all_inner_texts())`. Пагинация: ищи ссылку `page.locator("li.next a")`, проверяй её существование через `.count() > 0`, кликай `.click()` и жди загрузки: `page.wait_for_selector("div.quote")`. Цикл `for` на 3 итерации с `break`, если ссылки нет.

### Подсказка 4

`page.screenshot(path="books.png")` сохраняет скриншот. `from pathlib import Path` — `Path("books.png").exists()` вернёт `True`, если файл создан, а `Path("books.png").stat().st_size` — размер в байтах. Делай скриншот после `wait_for_selector`, чтобы страница успела отрисоваться.

### Подсказка 5

Ввод в поле: `page.locator("input.new-todo").fill("Купить молоко")`. Нажатие Enter: `.press("Enter")`. После этого JS-приложение добавит элемент списка. `page.wait_for_selector("ul.todo-list li")` дождётся его, затем `page.locator("ul.todo-list li").count()` покажет количество задач.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/")
    page.wait_for_selector("div.quote")

    print("Заголовок:", page.title())
    print("Цитат:", page.locator("div.quote").count())

    browser.close()
```

Разбор по шагам:

- `with sync_playwright() as p:` — контекстный менеджер: он запускает Playwright и гарантированно освобождает ресурсы, даже если в коде будет исключение.
- `p.chromium.launch(headless=True)` запускает браузер без окна. `headless=True` — режим «невидимки», стандарт для парсеров.
- `page.goto(...)` открывает адрес. `page.wait_for_selector("div.quote")` — ключевой момент: ждёт, пока на странице появятся блоки цитат. Без этого мы могли бы посчитать элементы до того, как JS их отрисует.
- `page.title()` возвращает заголовок вкладки — `Quotes to Scrape`.
- `page.locator("div.quote").count()` — количество блоков цитат. Локейтор не «ищет» сразу, а считает элементы в момент вызова.
- `browser.close()` закрывает браузер. Если забыть — процесс браузера останется висеть в памяти. Для надёжности можно использовать `with browser:` в реальных проектах.

### Разбор 2

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")
    page.wait_for_selector("div.quote")

    quote = page.locator("div.quote", has_text="The world is a book")
    author = quote.locator("small.author").inner_text()
    text = quote.locator("span.text").inner_text()

    print("Автор:", author)
    print("Текст:", text)
    browser.close()
```

Разбор по шагам:

- `page.locator("div.quote", has_text="The world is a book")` — локейтор с фильтром по тексту: будут выбраны только те блоки цитат, внутри которых есть эта фраза. Это удобная альтернатива перебору всех цитат и проверке условий в Python.
- `quote.locator("small.author")` — поиск уже внутри конкретного блока. Локейторы можно вкладывать: внешний сужает область, внутренний ищет внутри неё.
- `inner_text()` возвращает видимый текст элемента: для автора — `Albert Einstein`, для цитаты — весь текст в `span.text`.
- Вывод подтверждает, что фильтр сработал: цитата Эйнштейна «The world is a book and those who do not travel read only one page» — первая на странице, и автор именно Albert Einstein.
- Такой стиль — «найди родительский блок по тексту, потом достань данные из него» — универсален для динамических интерфейсов: списки, карточки, таблицы.

### Разбор 3

```python
from playwright.sync_api import sync_playwright

authors = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 4):
        page.goto(f"https://quotes.toscrape.com/page/{page_num}/")
        page.wait_for_selector("div.quote")
        authors.update(page.locator("small.author").all_inner_texts())

        next_link = page.locator("li.next a")
        if next_link.count() == 0:
            break

    browser.close()

print("Уникальных авторов за 3 страницы:", len(authors))
```

Разбор по шагам:

- Цикл `for page_num in range(1, 4)` проходит страницы 1, 2 и 3. Адрес формируется f-строкой — так выглядят URL пагинации на многих сайтах.
- `page.wait_for_selector("div.quote")` после каждого `goto` — гарантия, что цитаты успели загрузиться.
- `page.locator("small.author").all_inner_texts()` возвращает список текстов всех авторов на странице. `authors.update(...)` добавляет их в множество — дубликаты исчезают автоматически.
- `page.locator("li.next a").count()` — количество ссылок «Next»: 1, если есть следующая страница, 0 — если нет. Проверка защищает цикл от выхода за последнюю страницу.
- В итоге в множестве — уникальные авторы трёх страниц. Такая пагинация с обходом по «Next» — универсальный приём, он работает и в Playwright, и в Selenium, и в BeautifulSoup.

### Разбор 4

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    page.wait_for_selector("article.product_pod")

    page.screenshot(path="books.png")
    browser.close()

screenshot = Path("books.png")
print("Файл существует:", screenshot.exists())
print("Размер:", screenshot.stat().st_size, "байт")
```

Разбор по шагам:

- `page.wait_for_selector("article.product_pod")` ждёт, пока отрисуются карточки книг, — только тогда скриншот будет содержать весь магазин.
- `page.screenshot(path="books.png")` сохраняет картинку текущего состояния страницы. Формат определяется расширением файла.
- `Path("books.png")` из `pathlib` — объект пути. `screenshot.exists()` проверяет, что файл реально создан; `screenshot.stat().st_size` — размер в байтах. Типичный размер такого скриншота — десятки-сотни килобайт.
- Закрытие браузера происходит до проверки файла — скриншот уже записан на диск, это безопасно.
- Скриншоты — главный инструмент отладки браузерного парсера: видишь, что реально открылось, а не то, что ты ожидал.

### Разбор 5

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://demo.playwright.dev/todomvc/")

    input_box = page.locator("input.new-todo")
    input_box.fill("Купить молоко")
    input_box.press("Enter")

    page.wait_for_selector("ul.todo-list li")
    print("Задач в списке:", page.locator("ul.todo-list li").count())
    browser.close()
```

Разбор по шагам:

- TodoMVC — классическое демо одностраничного приложения: вся логика на JavaScript, данные не приходят с сервера в HTML. Именно такой случай требует браузера.
- `page.locator("input.new-todo")` — поле ввода новой задачи. `fill("Купить молоко")` вводит текст, `press("Enter")` эмулирует нажатие Enter — приложение реагирует и добавляет задачу в список.
- `page.wait_for_selector("ul.todo-list li")` ждёт появления первого элемента списка: после Enter проходит немного времени, и без ожидания мы могли бы увидеть `0`.
- `page.locator("ul.todo-list li").count()` считает задачи. Мы добавили одну — вывод `1`.
- Это прототип настоящего парсинга динамических интерфейсов: поле ввода → действие → ожидание результата → сбор данных. Так же автоматизируются поиск на сайтах, фильтры, корзины и бесконечные ленты.
<!--/SOLUTION-->

<!--QUIZ-->
Почему requests не видит контент динамических страниц?
- Потому что requests не поддерживает HTTPS
- Потому что requests не выполняет JavaScript
- Потому что такие страницы отдают только бинарные данные
- Он видит всё, вопрос неверный
* Правильный ответ: Потому что requests не выполняет JavaScript
Контент создаётся скриптами уже в браузере, а requests получает лишь «пустую» оболочку.

Что такое headless-режим браузера?
- Браузер работает без графического окна
- Браузер работает только с локальными файлами
- Браузер отключает JavaScript
- Браузер работает без сети
* Правильный ответ: Браузер работает без графического окна
Headless-режим запускает настоящий браузер, но без окна — идеально для парсеров.

Зачем нужны явные ожидания (wait_for_selector, WebDriverWait)?
- Чтобы ускорить загрузку страницы
- Чтобы дождаться появления элемента, а не спать «вслепую»
- Чтобы заменить браузер на requests
- Чтобы отключить тайм-ауты
* Правильный ответ: Чтобы дождаться появления элемента, а не спать «вслепую»
Ожидания проверяют условие (например, элемент появился) и не тратят лишнее время.

Что возвращает page.locator("div.quote").count()?
- Первый элемент div.quote
- Количество элементов div.quote
- Текст первого div.quote
- HTML всей страницы
* Правильный ответ: Количество элементов div.quote
count() считает элементы, подходящие под локейтор.

Как впwright ввести текст в поле и нажать Enter?
- field.write() + field.enter()
- locator.fill() + locator.press("Enter")
- locator.set_text() + locator.click()
- locator.type() + locator.submit()
* Правильный ответ: locator.fill() + locator.press("Enter")
fill() вводит текст, press("Enter") эмулирует нажатие клавиши.

Что будет, если не закрыть браузер в Playwright/Selenium?
- Ничего страшного, он закроется сам
- Процесс браузера останется висеть в памяти
- Скрипт упадёт с ошибкой на каждой строке
- Данные перестанут сохраняться
* Правильный ответ: Процесс браузера останется висеть в памяти
Браузер нужно закрывать: browser.close() или driver.quit(). В Playwright это удобно делать через with-блок.
<!--/QUIZ-->
