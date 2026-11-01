---
title: CSS глубоко: Flexbox, Grid, адаптивность
summary: Селекторы и специфичность, модель бокса, Flexbox и Grid, медиазапросы, CSS-переменные и типовые ошибки вёрстки.
order: 17
duration: 50 мин
difficulty: intermediate
tags: html, css, flexbox, grid, адаптивность
---

В уроке про основы HTML и CSS мы научились красить элементы и подключать стили. Теперь разберёмся, как устроена «тяжёлая артиллерия» CSS: почему одни правила побеждают другие, как правильно считать размеры блоков, как раскладывать элементы в ряд и в сетку и что делать, чтобы страница не разваливалась на телефоне.

## Селекторы и специфичность

CSS-правило состоит из селектора и блока свойств. Но когда несколько правил целятся в один элемент, браузер применяет правило с большей **специфичностью** — «весом» селектора. Вес считают так: inline-стиль (атрибут `style`) — 1000; `id` — 100; классы, атрибуты и псевдоклассы — 10; теги и псевдоэлементы — 1.

```css
.card h2 { color: blue; }   /* вес 0-1-1 */
h2 { color: red; }          /* вес 0-0-1 */
```

Синее правило весомее, поэтому `h2` внутри `.card` станет синим. `!important` перебивает всё — но это костыль, который ломает каскад: к нему прибегают лишь в крайних случаях, а в обычном коде лучше уточнить селектор.

## Модель бокса (box model)

Каждый элемент — прямоугольник из четырёх слоёв: содержимое (`content`), внутренний отступ (`padding`), рамка (`border`) и внешний отступ (`margin`). По умолчанию `width` относится только к содержимому: если задать `width: 300px` и `padding: 20px`, реальный блок станет 340px. Половина проблем вёрстки — отсюда. Лечится `box-sizing: border-box`:

```css
*, *::before, *::after {
    box-sizing: border-box;
}
```

Теперь `width` включает `padding` и `border`, и блок не расползается. Ещё нюанс: вертикальные `margin` соседних блоков схлопываются — берётся больший, а не сумма.

## Flexbox

Flexbox раскладывает элементы вдоль одной оси (одномерно). `display: flex` у контейнера делает его детей «флекс-элементами». Основные свойства:

- `flex-direction: row` (по умолчанию) или `column` — направление главной оси;
- `justify-content` — распределение вдоль главной оси: `center`, `space-between`, `space-around`;
- `align-items` — выравнивание поперёк: `center`, `stretch`, `flex-start`;
- `gap` — расстояние между элементами (не нужно больше танцевать с margin);
- `flex-wrap: wrap` — разрешить перенос на новую строку.

```css
.nav__list {
    display: flex;
    gap: 24px;
    justify-content: center;
    align-items: center;
    list-style: none;
}
```

Карточки в ряд — тот же рецепт: контейнер `flex` + `flex-wrap` на случай нехватки места.

## Grid

Grid — двумерная сетка: строки и колонки сразу.

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}
```

`repeat(3, 1fr)` — три равные колонки, `1fr` означает «одна доля свободного места». Элемент может занимать несколько колонок: `grid-column: span 2`. Основное правило выбора: grid — для общего каркаса и сеток, flex — для рядов элементов.

## Адаптивность и медиазапросы

Медиазапросы меняют стили в зависимости от ширины окна:

```css
@media (max-width: 768px) {
    .gallery { grid-template-columns: 1fr; }
}
```

Стили внутри применятся, когда ширина окна меньше или равна 768px. Перед этим обязательно добавь в `<head>` мету:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Без неё телефон покажет «уменьшенную» страницу с крошечным текстом. Классический план: на десктопе три колонки, на планшете две, на телефоне одна.

## Переменные

Повторяющиеся цвета и значения выносят в переменные:

```css
:root {
    --accent: #2563eb;
    --gap: 16px;
}
```

Использование: `background: var(--accent);` и `gap: var(--gap);`. Поменял значение в одном месте — обновилось везде. Переменные можно переопределять внутри медиазапросов, например для мобильной темы.

## Типовые ошибки

1. Забыли `box-sizing: border-box` — элементы шире, чем задумано, появляется горизонтальная прокрутка.
2. Жёсткие ширины в `px` вместо `1fr`, процентов или `auto` — страница не адаптируется.
3. Путают `justify-content` (главная ось) с `align-items` (поперечная).
4. Забывают `flex-wrap: wrap` — в узком окне элементы сжимаются до нуля.
5. Нет `meta viewport` — на телефоне мелкий текст.
6. `!important` и «войны специфичности» вместо более конкретных селекторов.
7. `margin` вместо `gap` — отступы между элементами «плывут» при переносах.

## Итог

Мы разобрались со специфичностью и моделью бокса, научились раскладывать элементы через flex и grid, делать сетки адаптивными через медиазапросы и убирать повторения через переменные. Каждая задача ниже — это маленький макет, у которого ты сам проверишь структуру с помощью Python-скрипта.

<!--TASK-->
### Задача 1

Создай карточку профиля с правильной моделью бокса. Файл `card.html`: полноценный HTML-документ с `<div class="card">`, внутри — `<img>`, `<h2>` и `<p>`. Файл `style.css`: универсальное правило `* { box-sizing: border-box; }` и правила для `.card`: `width: 320px`, `padding: 20px`, `border: 1px solid #ddd`, `border-radius: 12px`, `margin: 20px auto`. Напиши и запусти проверочный скрипт `check_card.py`: через `BeautifulSoup` проверь наличие `.card` и элементов `img`, `h2`, `p` внутри него; строковыми проверками по `style.css` проверь, что в нём есть `box-sizing: border-box` и все пять перечисленных правил. Выведи «Все проверки пройдены ✅» или список проблем.

### Задача 2

Собери горизонтальную навигацию на Flexbox. Файл `nav.html`: `<nav class="nav">` с `<ul class="nav__list">`, внутри — четыре `<li>` со ссылками `<a href="#">`. Файл `style.css`: для `.nav__list` — `display: flex`, `justify-content: center`, `align-items: center`, `gap: 20px`, `list-style: none`; для `.nav a` — `text-decoration: none` и цвет `#2563eb`. Напиши `check_nav.py`: `BeautifulSoup` проверяет, что `ul.nav__list` существует и содержит ровно четыре ссылки; строковые проверки подтверждают наличие `display: flex`, `justify-content`, `align-items`, `gap`, `list-style: none` в правиле для `.nav__list`. Запусти и убедись, что все проверки пройдены.

### Задача 3

Сделай галерею на Grid. Файл `gallery.html`: `<section class="gallery">` с шестью `<article class="card">`, в каждом `<h3>` и `<p>`. Файл `style.css`: для `.gallery` — `display: grid`, `grid-template-columns: repeat(3, 1fr)`, `gap: 16px`; для `.card` — `padding: 16px`, `border: 1px solid #eee`, `border-radius: 8px`. Проверочный скрипт `check_gallery.py`: `BeautifulSoup` считает карточки (должно быть 6), а строковые проверки убеждаются, что в CSS есть `display: grid`, паттерн `repeat(3, 1fr)` (используй `import re` и `re.search(r"repeat\(\s*3\s*,\s*1fr\s*\)", css)`) и `gap`. Запусти скрипт.

### Задача 4

Добавь переменные и адаптивность. В `gallery.html` добавь в `<head>` `<meta name="viewport" content="width=device-width, initial-scale=1">`. В `style.css` добавь блок `:root` с переменными `--accent: #2563eb` и `--card-gap: 16px`, замени `gap: 16px` на `gap: var(--card-gap)`, а цвет ссылок замени на `var(--accent)`. Затем добавь медиазапрос `@media (max-width: 768px)`, внутри которого `.gallery` получает `grid-template-columns: 1fr`. Обнови `check_gallery.py` (или создай `check_responsive.py`): проверь `meta[name="viewport"]` через `BeautifulSoup`, наличие `:root` и `var(--card-gap)` в CSS, а также наличие `@media` и `grid-template-columns: 1fr` внутри медиазапроса.

### Задача 5

Собери мини-макет страницы: шапка, сетка и подвал. Файл `page.html`: `<header>` с `<nav>` (flex-навигация из задачи 2), `<main>` c `<section class="grid">` из четырёх `<article class="card">`, `<footer>` с текстом. Файл `style.css`: переменные `:root`, сброс `box-sizing`, flex-навигация, `.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: var(--card-gap); }` и медиазапрос `@media (max-width: 768px)`, где `.grid` становится `1fr`, а навигация — `flex-direction: column`. Напиши `check_page.py`: `BeautifulSoup` проверяет наличие `header`, `main`, `footer`, `nav`, `.grid` и четырёх `.card`; строковые проверки — наличие `display: flex`, `display: grid`, `:root`, `var(--card-gap)`, `@media` и `flex-direction: column`. Запусти скрипт и добейся «Все проверки пройдены ✅».

<!--/TASK-->

<!--HINT-->
### Подсказка 1

Класс в HTML — атрибут `class="card"`, в CSS ему соответствует `.card` с точкой. `BeautifulSoup(html, "html.parser")`, выборка `soup.select_one(".card")`. Не забудь про `pip install beautifulsoup4`, если библиотеки нет. Правило `*` для box-sizing можно проверить простым `"box-sizing" in css and "border-box" in css`.

### Подсказка 2

`ul.nav__list` — это выборка «ul с классом nav__list»: `soup.select("ul.nav__list a")` вернёт все ссылки внутри. Их должно быть ровно четыре: `len(...) == 4`. В CSS проверяй именно подстроки: `"display: flex" in css`, `"justify-content" in css` — точность записи: после двоеточия нужен пробел.

### Подсказка 3

Подсчёт карточек: `cards = soup.select("section.gallery .card")`, затем `len(cards) == 6`. Для `repeat(3, 1fr)` используй регулярное выражение — пробелы вокруг числа допускаются: `r"repeat\(\s*3\s*,\s*1fr\s*\)"`. Если `re.search` вернул `None` — правила нет.

### Подсказка 4

`meta[name="viewport"]` ищется так: `soup.find("meta", attrs={"name": "viewport"})` — вернёт `None`, если тега нет. Внутри медиазапросов переменные переопределяются так же, как в `:root`. Для проверки «1fr внутри @media» проще всего искать обе подстроки: `"@media" in css and "grid-template-columns: 1fr" in css`.

### Подсказка 5

Собирай проверки в список кортежей `(условие, сообщение_об_ошибке)` и в конце выводи либо список проблем, либо «Все проверки пройдены ✅». Не забывай: `flex-direction: column` должен встретиться внутри медиазапросa, но для простоты можно проверять лишь наличие подстроки в файле.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1

`card.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <title>Карточка</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="card">
        <img src="https://picsum.photos/200" alt="Фото">
        <h2>Аня Иванова</h2>
        <p>Изучаю Python и веб-разработку.</p>
    </div>
</body>
</html>
```

`style.css`:

```css
* {
    box-sizing: border-box;
}

.card {
    width: 320px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 12px;
    margin: 20px auto;
}
```

`check_card.py`:

```python
from bs4 import BeautifulSoup

html = open("card.html", encoding="utf-8").read()
css = open("style.css", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

errors = []
card = soup.select_one(".card")
if card is None:
    errors.append("не найден элемент .card")
else:
    for tag in ("img", "h2", "p"):
        if card.select_one(tag) is None:
            errors.append(f"в .card нет <{tag}>")

if "box-sizing" not in css or "border-box" not in css:
    errors.append("нет box-sizing: border-box")
for rule in ["width: 320px", "padding: 20px", "border: 1px solid #ddd",
             "border-radius: 12px", "margin: 20px auto"]:
    if rule not in css:
        errors.append(f"нет правила {rule}")

if errors:
    print("Проблемы:")
    for e in errors:
        print(" -", e)
else:
    print("Все проверки пройдены ✅")
```

Разбор. `* { box-sizing: border-box; }` — универсальный селектор: он применяется к каждому элементу. Без него `width: 320px` означала бы ширину только содержимого, и с `padding: 20px` карточка выросла бы до 360px — блок перестал бы помещаться в 320px. `margin: 20px auto` центрирует блок по горизонтали («auto» делит свободное место поровну слева и справа). Проверочный скрипт открывает оба файла: `BeautifulSoup` проверяет структуру HTML, а строковые проверки — наличие ключевых правил в CSS. Так автоматизируется то, что обычно проверяют глазами.

### Разбор 2

`nav.html` (фрагмент):

```html
<nav class="nav">
    <ul class="nav__list">
        <li><a href="#">Главная</a></li>
        <li><a href="#">Обо мне</a></li>
        <li><a href="#">Навыки</a></li>
        <li><a href="#">Контакты</a></li>
    </ul>
</nav>
```

`style.css`:

```css
.nav__list {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    list-style: none;
}

.nav a {
    text-decoration: none;
    color: #2563eb;
}
```

`check_nav.py`:

```python
from bs4 import BeautifulSoup

html = open("nav.html", encoding="utf-8").read()
css = open("style.css", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

errors = []
links = soup.select("ul.nav__list a")
if len(links) != 4:
    errors.append(f"в nav__list ссылок {len(links)}, а нужно 4")

for rule in ["display: flex", "justify-content", "align-items",
             "gap", "list-style: none"]:
    if rule not in css:
        errors.append(f"в CSS нет {rule}")

if errors:
    print("Проблемы:")
    for e in errors:
        print(" -", e)
else:
    print("Все проверки пройдены ✅")
```

Разбор. `display: flex` превращает `ul` во флекс-контейнер, а `li` — во флекс-элементы, которые встают в один ряд. `justify-content: center` центрирует ряд по главной оси (горизонтали), `align-items: center` выравнивает элементы поперёк. `gap: 20px` задаёт расстояние между пунктами — раньше для этого приходилось добавлять `margin` каждому `li`, что давало лишние отступы по краям. `list-style: none` убирает маркеры списка. CSS-строка `ul.nav__list a` в проверке выбирает все ссылки внутри списка: их ровно четыре, как и требуется.

### Разбор 3

`gallery.html` (фрагмент):

```html
<section class="gallery">
    <article class="card">
        <h3>Проект 1</h3>
        <p>Описание первого проекта.</p>
    </article>
    <!-- ещё пять карточек -->
</section>
```

`style.css`:

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.card {
    padding: 16px;
    border: 1px solid #eee;
    border-radius: 8px;
}
```

`check_gallery.py`:

```python
import re
from bs4 import BeautifulSoup

html = open("gallery.html", encoding="utf-8").read()
css = open("style.css", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

errors = []
cards = soup.select("section.gallery .card")
if len(cards) != 6:
    errors.append(f"карточек {len(cards)}, а нужно 6")

for rule in ["display: grid", "gap"]:
    if rule not in css:
        errors.append(f"в CSS нет {rule}")
if not re.search(r"repeat\(\s*3\s*,\s*1fr\s*\)", css):
    errors.append("нет grid-template-columns: repeat(3, 1fr)")

if errors:
    print("Проблемы:")
    for e in errors:
        print(" -", e)
else:
    print("Все проверки пройдены ✅")
```

Разбор. `display: grid` включает сеточный режим. `grid-template-columns: repeat(3, 1fr)` делит контейнер на три равные колонки: `1fr` — это одна доля свободного места, поэтому колонки одинаковые, а при изменении ширины окна они растягиваются вместе с ним. `gap: 16px` даёт одинаковые промежутки и между колонками, и между строками. Карточки автоматически раскладываются: первые три — в первую строку, следующие три — во вторую. В проверке `re.search` с паттерном `repeat(3, 1fr)` находит правило, даже если в CSS стоят лишние пробелы, — строгая подстрока `repeat(3, 1fr)` могла бы не совпасть.

### Разбор 4

`gallery.html` — в `<head>`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

`style.css`:

```css
:root {
    --accent: #2563eb;
    --card-gap: 16px;
}

.gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--card-gap);
}

.card {
    padding: 16px;
    border: 1px solid #eee;
    border-radius: 8px;
}

@media (max-width: 768px) {
    .gallery {
        grid-template-columns: 1fr;
    }
}
```

`check_responsive.py`:

```python
from bs4 import BeautifulSoup

html = open("gallery.html", encoding="utf-8").read()
css = open("style.css", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

errors = []
if soup.find("meta", attrs={"name": "viewport"}) is None:
    errors.append("нет <meta name=viewport>")
for rule in [":root", "var(--card-gap)", "@media",
             "grid-template-columns: 1fr"]:
    if rule not in css:
        errors.append(f"в CSS нет {rule}")

if errors:
    print("Проблемы:")
    for e in errors:
        print(" -", e)
else:
    print("Все проверки пройдены ✅")
```

Разбор. `:root` — это корневой элемент (`<html>`), в нём объявляют глобальные переменные. `var(--card-gap)` подставляет значение переменной, поэтому если захочешь изменить расстояние между карточками, правишь одну строку в `:root`. Медиазапрос `@media (max-width: 768px)` срабатывает, когда окно уже 768px или уже: галерея становится одноколоночной. `meta viewport` — обязательный спутник адаптивности: без него браузер телефона считает, что страница шире экрана, и ужимает её целиком, а с ним использует реальную ширину устройства. Проверка `soup.find("meta", attrs={"name": "viewport"})` находит тег по атрибуту.

### Разбор 5

`page.html` (скелет):

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Макет</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav class="nav">
            <ul class="nav__list">
                <li><a href="#">Главная</a></li>
                <li><a href="#">Обо мне</a></li>
                <li><a href="#">Контакты</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <section class="grid">
            <article class="card"><h3>Карточка 1</h3><p>Текст</p></article>
            <article class="card"><h3>Карточка 2</h3><p>Текст</p></article>
            <article class="card"><h3>Карточка 3</h3><p>Текст</p></article>
            <article class="card"><h3>Карточка 4</h3><p>Текст</p></article>
        </section>
    </main>
    <footer>© 2026, PythonПро</footer>
</body>
</html>
```

`style.css` (ключевые части):

```css
:root {
    --accent: #2563eb;
    --card-gap: 16px;
}

* { box-sizing: border-box; }

.nav__list {
    display: flex;
    gap: 20px;
    justify-content: center;
    list-style: none;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--card-gap);
}

@media (max-width: 768px) {
    .grid { grid-template-columns: 1fr; }
    .nav__list { flex-direction: column; align-items: center; }
}
```

`check_page.py`:

```python
from bs4 import BeautifulSoup

html = open("page.html", encoding="utf-8").read()
css = open("style.css", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")

errors = []
for selector, what in [("header", "<header>"), ("main", "<main>"),
                       ("footer", "<footer>"), ("nav", "<nav>"),
                       ("section.grid", "section.grid")]:
    if soup.select_one(selector) is None:
        errors.append(f"нет {what}")
if len(soup.select("section.grid .card")) != 4:
    errors.append("в .grid должно быть 4 карточки")

for rule in ["display: flex", "display: grid", ":root",
             "var(--card-gap)", "@media", "flex-direction: column"]:
    if rule not in css:
        errors.append(f"в CSS нет {rule}")

if errors:
    print("Проблемы:")
    for e in errors:
        print(" -", e)
else:
    print("Все проверки пройдены ✅")
```

Разбор. Страница собирается из трёх смысловых зон — `header`, `main`, `footer` — это семантические теги, которые помогают и браузеру, и проверочному скрипту. Навигация на `flex` держит ссылки в одну линию по центру. Сетка `.grid` на `grid` раскладывает четыре карточки в две колонки. Медиазапрос на 768px переключает сетку в одну колонку и разворачивает навигацию вертикально (`flex-direction: column`) — на узком экране это читается лучше. Проверочный скрипт совмещает структурные проверки (что есть header/main/footer/nav/grid и ровно четыре карточки) и строковые (ключевые CSS-правила). Такой скрипт — прообраз настоящих автотестов вёрстки.

<!--/SOLUTION-->

<!--QUIZ-->
Что означает 1fr в grid-template-columns?
- Одну долю свободного места
- Один пиксель
- 100% ширины
- Один элемент
* Правильный ответ: Одну долю свободного места
fr — доля (fraction): три колонки 1fr займут всё место поровну.

Какой селектор весомее в специфичности?
- #header
- .card
- h2
- * 
* Правильный ответ: #header
id даёт 100 очков, класс — 10, тег — 1. id побеждает (если не вмешивается !important).

Что делает box-sizing: border-box?
- Включает padding и border в width элемента
- Убирает border
- Добавляет margin
- Округляет углы
* Правильный ответ: Включает padding и border в width элемента
Блок не «расползается»: заданная ширина становится полной шириной элемента.

За что отвечает justify-content во flex-контейнере?
- За распределение вдоль главной оси
- За вертикальное выравнивание
- За расстояние до родителя
- За перенос строк
* Правильный ответ: За распределение вдоль главной оси
justify-content работает вдоль flex-direction; align-items — поперёк оси.

Какой инструмент двумерный: flex или grid?
- Grid
- Flex
- Оба одинаково
- Ни один
* Правильный ответ: Grid
Grid управляет колонками и строками сразу; flex раскладывает вдоль одной оси.

Как объявить переменную цвета accent?
- :root { --accent: #2563eb; }
- $accent: #2563eb;
- @accent: #2563eb;
- --accent: #2563eb; (вне любого блока)
* Правильный ответ: :root { --accent: #2563eb; }
Переменные CSS объявляются с двумя дефисами, чаще всего в :root, и используются через var(--accent).

Зачем нужен <meta name="viewport">?
- Для корректного масштабирования на мобильных
- Для подключения CSS
- Для SEO
- Для шрифтов
* Правильный ответ: Для корректного масштабирования на мобильных
Без него телефон показывает уменьшенную страницу целиком, а не адаптированную вёрстку.

Почему !important считают вредным приёмом?
- Он ломает каскад и порождает войны специфичности
- Он не работает
- Он замедляет сайт
- Он доступен только в Grid
* Правильный ответ: Он ломает каскад и порождает войны специфичности
!important перебивает любые правила, из-за чего стили становится невозможно предсказать.

Как задать расстояние 16px между элементами flex-контейнера?
- gap: 16px
- margin: 16px
- padding: 16px
- space-between: 16px
* Правильный ответ: gap: 16px
gap задаёт промежутки между всеми элементами без лишних отступов по краям.

Что делает flex-wrap: wrap?
- Разрешает элементам переноситься на новую строку
- Запрещает переносы
- Центрирует элементы
- Делает элементы одинаковой ширины
* Правильный ответ: Разрешает элементам переноситься на новую строку
Без wrap элементы сжимаются, чтобы уместиться в одну строку; с wrap — переносятся.
<!--/QUIZ-->
