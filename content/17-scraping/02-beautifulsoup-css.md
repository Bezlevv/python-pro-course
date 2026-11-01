---
title: BeautifulSoup: CSS-селекторы
summary: Как разбирать HTML: BeautifulSoup, find/find_all, извлечение текста и атрибутов, CSS-селекторы через select.
order: 2
duration: 40 мин
difficulty: advanced
tags: beautifulsoup, html, css-селекторы, парсинг
---

Ты научился скачивать страницы. Теперь главный вопрос: как из кучи HTML-тегов достать нужные данные? Ответ — библиотека `BeautifulSoup` из пакета `beautifulsoup4`. Она превращает HTML в дерево объектов, по которому удобно ходить: искать элементы по тегам, классам, атрибутам — и всё это можно делать коротким и выразительным кодом.

## Установка и первый суп

Установи библиотеку вместе с парсером `lxml` (он быстрее встроенного):

```bash
pip install beautifulsoup4 lxml
```

Чтобы начать, создай объект `BeautifulSoup` из HTML-текста:

```python
from bs4 import BeautifulSoup

html = "<html><body><h1>Привет</h1><p class='text'>Мир</p></body></html>"
soup = BeautifulSoup(html, "lxml")
```

Второй аргумент — имя парсера: `"lxml"` или `"html.parser"`. HTML — это не текст с регулярками, а дерево тегов: внутри `html` лежит `body`, внутри него — `h1` и `p`. BeautifulSoup строит это дерево, и дальше мы по нему гуляем.

## find() и find_all(): поиск по тегам и атрибутам

`find_all()` возвращает **список** всех подходящих элементов, `find()` — первый из них (или `None`):

```python
soup.find("h1")                       # первый заголовок h1
soup.find_all("p")                    # все абзацы
soup.find_all("p", class_="text")     # абзацы с классом text
soup.find_all("a", href=True)         # ссылки с атрибутом href
```

Обрати внимание: для поиска по классу используется `class_` с подчёркиванием — потому что `class` в Python зарезервировано. Есть и короткая запись: `soup.find_all(class_="text")`. Если элементов нет — пустой список, это важно проверять, чтобы не упасть на `None`.

## CSS-селекторы: select() и select_one()

Мощь BeautifulSoup — в поддержке CSS-селекторов. `select()` возвращает все элементы, подходящие под селектор, а `select_one()` — первый:

```python
soup.select("p.text")          # абзацы с классом text
soup.select("div#content p")   # абзацы внутри div с id=content
soup.select_one("h1")          # первый h1
soup.select("a[href^='https']")  # ссылки, начинающиеся с https
```

Селекторы — тот же синтаксис, что и в CSS: `тег`, `.класс`, `#id`, `[атрибут]`, комбинаторы через пробел (потомок). Для большинства задач `select` и `select_one` — самый чистый способ. Помни: `select` всегда возвращает список, даже если элемент один.

## Извлекаем данные: текст и атрибуты

Нашли элемент — теперь вытащим из него текст и атрибуты:

```python
h1 = soup.select_one("h1")
print(h1.get_text())        # текст внутри элемента
print(h1.text)              # то же самое, короткая форма

a = soup.select_one("a")
print(a.get("href"))        # значение атрибута href
print(a["href"])            # то же, но упадёт, если атрибута нет
```

`get_text()` убирает теги и оставляет видимый текст. `get("href")` безопасно возвращает `None`, если атрибута нет, а `a["href"]` бросит `KeyError`. Для парсинга `get()` удобнее.

## Реальный пример: цитаты

Попробуем на учебном сайте цитат `https://quotes.toscrape.com/`. Там каждая цитата — в блоке `div.quote`, текст — в `span.text`, автор — в `small.author`, теги — в ссылках `a.tag`:

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

for quote in soup.select("div.quote")[:3]:
    text = quote.select_one("span.text").get_text()
    author = quote.select_one("small.author").get_text()
    print(author, "-", text)
```

Смотри, как читается код: «возьми все блоки `div.quote`, в каждом найди `span.text` и `small.author`, вытащи текст». Это и есть суть парсинга — описать, где лежат данные, и вытащить их.

## Навигация по дереву

Иногда удобно ходить от элемента к элементу: `.parent` — родитель, `.find_parent("div")` — ближайший родитель с тегом, `.next_sibling` — соседний элемент. Например, узнать блок всей цитаты по автору:

```python
small = soup.select_one("small.author")
quote_block = small.find_parent("div", class_="quote")
```

Но не увлекайся: цепочки `.parent.parent.parent` быстро ломаются при малейшем изменении разметки. CSS-селекторы обычно надёжнее.

## Итог

Рецепт любой выборки из HTML: скачай страницу → создай `BeautifulSoup` → выбери элементы через `select`/`find_all` → достань текст через `get_text()` и атрибуты через `get()`. Если элементов нет — список пуст, и это нормально. Теперь попрактикуемся на реальных сайтах.

<!--TASK-->
### Задача 1

Напиши программу `first_soup.py`. Скачай `https://quotes.toscrape.com/` с помощью `requests.get` (не забудь `timeout=10`) и создай `BeautifulSoup` с парсером `"lxml"`. Выведи: заголовок страницы через `soup.title.get_text()`, количество блоков цитат через `len(soup.select("div.quote"))` и количество уникальных авторов через `len(set(...))` — для последнего собери текст всех элементов `small.author`. В конце выведи первую цитату: её текст и автора.

### Задача 2

Собери всех авторов со страницы 1 сайта `https://quotes.toscrape.com/`. Напиши программу `authors.py`, которая с помощью `select("small.author")` собирает тексты авторов в множество, выводит общее число уникальных авторов и первых пять имён (отсортированных по алфавиту) через `sorted()`. Если на странице 10 цитат, а некоторые авторы повторяются — множество само уберёт дубликаты. Выведи строку вида `Уникальных авторов: N`, затем список имён по одному на строку.

### Задача 3

Найди на странице `https://quotes.toscrape.com/` ссылку «Next» — она лежит в блоке `li.next` внутри ссылки `a`. Используй `select_one("li.next a")`, выведи её атрибут `href` и полный абсолютный адрес: для этого просто склей `"https://quotes.toscrape.com"` + `href`. Также выведи текст ссылки (обычно `Next`). Если ссылки нет — выведи фразу `Следующей страницы нет`.

### Задача 4

Перейди на сайт книжного магазина `https://books.toscrape.com/`. Там каждая книга — в блоке `article.product_pod`, название — в `h3 a` (атрибут `title` или текст), цена — в `p.price_color`. Напиши программу `books.py`, которая выводит для первых пяти книг пары `Название — Цена` (например `A Light in the Attic — £51.77`), а затем показывает, сколько книг на странице стоят дешевле 20 фунтов: цену преврати в число через `float(цена[1:])` (убери символ `£`).

### Задача 5

У каждой цитаты на `https://quotes.toscrape.com/` есть теги — ссылки `a.tag` внутри блока `div.quote`. Напиши программу `tags.py`, которая собирает все теги всех цитат страницы в один список и с помощью `collections.Counter` считает частоту каждого тега. Выведи топ-3 самых частых тега в формате `тег: количество` по убыванию частоты. Подсказка: метод `most_common(3)` у `Counter` вернёт тройку лидеров.
<!--/TASK-->

<!--HINT-->
### Подсказка 1

`BeautifulSoup(html, "lxml")` принимает текст ответа из `r.text`. Заголовок: `soup.title.get_text()`. Блоки цитат: `soup.select("div.quote")`. Авторы: `soup.select("small.author")` — каждый элемент превращается в текст методом `get_text()`.

### Подсказка 2

Множество уберёт дубликаты автоматически: `authors = {a.get_text() for a in soup.select("small.author")}`. Длина — `len(authors)`. Сортировка — `sorted(authors)`. Срез первых пяти — `sorted(authors)[:5]`.

### Подсказка 3

Селектор `"li.next a"` ищет ссылку внутри блока с классом `next`. Атрибут — `link["href"]` или `link.get("href")`. Проверяй через `if link:` — если элемента нет, `select_one` вернёт `None`, и обращение к `["href"]` упадёт.

### Подсказка 4

Название книги: `book.select_one("h3 a")["title"]` или `book.select_one("h3 a").get_text()`. Цена: `book.select_one("p.price_color").get_text()` — строка вида `£51.77`. Для сравнения преврати её в float: `float(price[1:])` — срез с первого символа убирает `£`.

### Подсказка 5

Собери все теги всех цитат: двойной цикл или генератор `[tag.get_text() for quote in soup.select("div.quote") for tag in quote.select("a.tag")]`. `Counter` посчитает частоту. `most_common(3)` вернёт список кортежей `(тег, количество)` — пройдись по нему циклом и выведи.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

print("Заголовок:", soup.title.get_text())
print("Блоков цитат:", len(soup.select("div.quote")))

authors = {a.get_text() for a in soup.select("small.author")}
print("Уникальных авторов:", len(authors))

first = soup.select_one("div.quote")
print("Первая цитата:")
print(first.select_one("span.text").get_text())
print("-", first.select_one("small.author").get_text())
```

Разбор по шагам:

- `r.text` — HTML страницы. Из него создаётся `soup` — дерево элементов.
- `soup.title.get_text()` — текст внутри тега `<title>`. Это заголовок вкладки браузера.
- `soup.select("div.quote")` возвращает список всех блоков цитат — на этой странице их 10.
- Генератор множества `{a.get_text() for a in soup.select("small.author")}` собирает авторов и сразу убирает повторы: если один автор встречается трижды, в множестве он останется один раз.
- `soup.select_one("div.quote")` — первый блок цитаты. Внутри него `select_one("span.text")` ищет текст, `select_one("small.author")` — автора.
- Важный навык: сначала страница → `soup`, потом выборка. Всё остальное в парсере — вариации этого рецепта.

### Разбор 2

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

authors = {a.get_text() for a in soup.select("small.author")}
print("Уникальных авторов:", len(authors))

for name in sorted(authors)[:5]:
    print(name)
```

Разбор по шагам:

- `soup.select("small.author")` — все элементы с тегом `small` и классом `author`. На странице их столько же, сколько цитат, — по одному на цитату.
- `a.get_text()` достаёт имя автора. Множество `authors` автоматически удаляет дубликаты: Агата Кристи, встречающаяся дважды, попадёт в него один раз.
- `len(authors)` — количество уникальных авторов. На странице 1 их может быть меньше десяти, если кто-то повторяется.
- `sorted(authors)` сортирует имена в алфавитном порядке (для кириллицы и латиницы — по кодовым точкам), а `[:5]` берёт первые пять.
- Такой подход — «собери все значения, убери повторы» — встречается в парсинге постоянно: списки тегов, имён, категорий. Множество + `sorted` — стандартный инструмент.

### Разбор 3

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

next_link = soup.select_one("li.next a")
if next_link:
    href = next_link["href"]
    print("Текст ссылки:", next_link.get_text().strip())
    print("Относительный адрес:", href)
    print("Полный адрес:", "https://quotes.toscrape.com" + href)
else:
    print("Следующей страницы нет")
```

Разбор по шагам:

- Селектор `"li.next a"` означает: «ссылка `a` внутри элемента `li` с классом `next`». Это стандартная разметка пагинации на учебном сайте.
- `select_one` возвращает первый подходящий элемент или `None`. Проверка `if next_link:` обязательна: на последней странице блока `li.next` нет, и `next_link` будет `None`.
- `next_link["href"]` — значение атрибута: обычно `"/page/2/"` — относительный адрес. Полный URL получается склейкой с базой `https://quotes.toscrape.com`.
- `next_link.get_text().strip()` — видимый текст ссылки «Next». `strip()` убирает лишние пробелы и переводы строк.
- Именно так работает обход страниц: нашёл ссылку «Next» — переходи по ней, пока она есть. Вернёшься к этому в уроке про пагинацию.

### Разбор 4

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

books = soup.select("article.product_pod")
for book in books[:5]:
    title = book.select_one("h3 a")["title"]
    price = book.select_one("p.price_color").get_text()
    print(f"{title} — {price}")

cheap = 0
for book in books:
    price = book.select_one("p.price_color").get_text()
    if float(price[1:]) < 20:
        cheap += 1
print("Книг дешевле 20 фунтов:", cheap)
```

Разбор по шагам:

- `article.product_pod` — карточка книги на главной странице магазина.
- Название лежит в атрибуте `title` ссылки внутри `h3`: `book.select_one("h3 a")["title"]`. Можно было взять и текст ссылки, но `title` надёжнее — там полное название без сокращений.
- Цена — в `p.price_color`, например `£51.77`. Это строка, а для сравнения нужно число.
- `price[1:]` отрезает первый символ `£`, `float(...)` превращает `"51.77"` в `51.77`. Теперь можно сравнивать: `float(price[1:]) < 20`.
- Цикл по всем книгам считает те, что дешевле 20 фунтов. На главной странице таких обычно заметное количество — магазин специально выставляет дешёвые книги.
- Обрати внимание на `f"{title} — {price}"` — f-строку, которая подставляет значения прямо в текст.

### Разбор 5

```python
import requests
from collections import Counter
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

tags = [
    tag.get_text()
    for quote in soup.select("div.quote")
    for tag in quote.select("a.tag")
]

counter = Counter(tags)
for tag, count in counter.most_common(3):
    print(f"{tag}: {count}")
```

Разбор по шагам:

- Двойной генератор списка: внешний цикл идёт по блокам цитат (`soup.select("div.quote")`), внутренний — по ссылкам тегов внутри каждого блока (`quote.select("a.tag")`).
- `tag.get_text()` — текст тега, например `life`, `love`, `wisdom`. Итоговый список `tags` содержит все теги страницы, с повторами.
- `Counter(tags)` — словарь, который считает, сколько раз встретился каждый тег.
- `most_common(3)` возвращает список трёх самых частых пар `(тег, количество)` в порядке убывания: `[('life', 3), ('love', 2), ...]`.
- Цикл распаковывает пары и печатает `тег: количество`.
- Такой подсчёт частот — типичный шаг анализа собранных данных: кого/что чаще всего упоминают, какие категории популярны. `Counter` — стандартный модуль, никаких внешних библиотек не нужно.
<!--/SOLUTION-->

<!--QUIZ-->
Что возвращает soup.find_all("p")?
- Первый абзац p
- Список всех абзацев p
- Количество абзацев
- HTML-строку страницы
* Правильный ответ: Список всех абзацев p
find_all() всегда возвращает список элементов (возможно пустой).

Как правильно искать элементы по классу в find_all?
- find_all("p", class="text")
- find_all("p", class_="text")
- find_all("p", css="text")
- find_all("p.text")
* Правильный ответ: find_all("p", class_="text")
class — зарезервированное слово, поэтому используется class_ с подчёркиванием.

Что вернёт soup.select_one("h1"), если тега h1 на странице нет?
- Пустой список
- None
- Пустую строку
- Будет ошибка
* Правильный ответ: None
select_one() возвращает первый элемент или None, если ничего не найдено.

Как получить текст внутри элемента soup без вложенных тегов?
- element.html()
- element.get_text()
- element.text_value()
- element.inner_html()
* Правильный ответ: element.get_text()
get_text() (или .text) возвращает видимый текст элемента, отбрасывая теги.

Какой селектор выберет ссылки с классом tag внутри блока с классом quote?
- "a.tag quote"
- "div.quote a.tag"
- "quote > tag"
- "a.tag.quote"
* Правильный ответ: "div.quote a.tag"
Селектор «div.quote a.tag» — потомки: ссылки a.tag внутри div.quote.

В чём отличие select() от select_one()?
- select() по классу, select_one() по id
- select() возвращает список, select_one() — первый элемент или None
- select() работает только с тегами, select_one() — с атрибутами
- Никакой разницы нет
* Правильный ответ: select() возвращает список, select_one() — первый элемент или None
select() всегда даёт список всех совпадений, select_one() — только первое.

Что вернёт soup.find_all("a", href=True)?
- Все ссылки, у которых есть атрибут href
- Первую ссылку на странице
- Тексты всех ссылок
- Количество ссылок
* Правильный ответ: Все ссылки, у которых есть атрибут href
href=True — фильтр по наличию атрибута: в список попадают только те элементы a, у которых он есть.

Чем a.get("href") отличается от a["href"]?
- get("href") возвращает None, если атрибута нет, а a["href"] бросит KeyError
- Это полностью эквивалентные способы
- a["href"] безопаснее для парсинга
- get("href") работает только с текстом элемента
* Правильный ответ: get("href") возвращает None, если атрибута нет, а a["href"] бросит KeyError
В парсинге чаще используют get() — он не роняет программу при отсутствии атрибута.
<!--/QUIZ-->
