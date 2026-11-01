---
title: HTMX и Alpine.js: фронтенд без боли
summary: Динамические страницы без React: HTMX для обновления HTML-фрагментов и Alpine.js для интерактивности.
order: 15
duration: 35 мин
difficulty: intermediate
tags: htmx, alpinejs, фронтенд, flask, fastapi
---

До сих пор мы делали серверную часть, а страницы отдавали целиком: каждый клик — обновление всей страницы. Но современные сайты ведут себя иначе: лайки ставятся без перезагрузки, фильтры работают мгновенно. Обычно для этого берут React или Vue — но это целая экосистема: сборщики, npm, тысячи зависимостей. Есть путь проще: **HTMX** и **Alpine.js** — две маленькие библиотеки, которые добавляют динамику на обычные HTML-страницы без единого шага сборки.

## HTMX: сервер возвращает фрагменты

Идея HTMX: не возвращать JSON и не перерисовывать страницу на клиенте, а пусть **сервер возвращает готовый HTML-фрагмент**, а HTMX просто подставляет его в нужное место. Это как AJAX, но без написания JavaScript.

Подключить HTMX — одна строка:

```html
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

Всё управление — через HTML-атрибуты:

- `hx-get` / `hx-post` — куда отправить запрос;
- `hx-trigger` — по какому событию (по умолчанию — клик для GET);
- `hx-target` — куда вставить ответ;
- `hx-swap` — как вставить (`innerHTML` по умолчанию).

Простой пример — кнопка, которая подгружает текст с сервера:

```html
<button hx-get="/random-quote" hx-target="#quote" hx-swap="innerHTML">
  Показать цитату
</button>
<div id="quote">Здесь будет цитата</div>
```

Сервер (Flask или FastAPI) возвращает не JSON, а кусок HTML:

```python
# Flask
@app.get("/random-quote")
def random_quote():
    return "<p>Всякая всячина — лучший друг программиста.</p>"
```

При клике HTMX сам сделает `GET /random-quote` и заменит содержимое `#quote`. Ни строчки JavaScript — только атрибуты.

## Формы и события

Через `hx-post` и `hx-trigger="change"` можно отправлять формы без перезагрузки:

```html
<form hx-post="/subscribe" hx-target="#result">
  <input type="email" name="email" required>
  <button type="submit">Подписаться</button>
</form>
<div id="result"></div>
```

Сервер отдаст `<p>Готово! Проверь почту.</p>` — и HTMX вставит его в `#result`. Атрибут `hx-trigger` позволяет ловить и другие события: `keyup`, `submit`, `load` и их комбинации.

## Alpine.js: интерактивность на странице

HTMX отлично ходит на сервер, но локальные штуки — открыть меню, посчитать клики, показать/скрыть блок — проще сделать на клиенте. Вот тут и нужен Alpine.js — крошечный фреймворк с «реактивностью», похожий на Vue, но без сборки.

Подключение — так же одна строка:

```html
<script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
```

Счётчик кликов:

```html
<div x-data="{ count: 0 }">
  <button @click="count++">Клик! {{ count }}</button>
</div>
```

Разбор:

- `x-data` — объявляет «состояние» компонента (объект с данными);
- `@click` — сокращение для `x-on:click`, обработчик события;
- `{{ count }}` — вывод значения в текст.

Показать/скрыть блок:

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <p x-show="open">Теперь меня видно!</p>
</div>
```

`x-show` скрывает элемент, пока выражение ложно. Есть также `x-if`, `x-for` (циклы), `x-model` (двусторонняя связь с полем ввода).

## HTMX + Alpine: вместе

Они отлично сочетаются: HTMX обновляет серверные данные, Alpine — локальную логику. Например, список задач с лайками: HTMX отправляет POST на сервер, получает новый HTML-фрагмент, а Alpine управляет открытием формы добавления.

## Где это уместно

HTMX + Alpine идеальны для: админок, внутренних инструментов, лендингов, простых блогов и MVP. Если проект вырастет в полноценное SPA (одностраничное приложение) со сложным состоянием — тогда стоит смотреть в сторону React/Vue, но для большинства задач «лёгкий» стек намного быстрее в разработке.

## Итог урока

Мы узнали: HTMX делает AJAX-запросы прямо из HTML-атрибутов и подставляет серверные HTML-фрагменты, а Alpine.js добавляет реактивность на странице без сборки. Вместе они закрывают 90% задач «оживления» страниц без тяжёлых фреймворков.

<!--TASK-->
### Задача 1
Создай страницу `index.html` + простое Flask-приложение `htmx_app.py`:

1. На странице — кнопка «Показать время» с `hx-get="/time"` и `hx-target="#clock"`, а под ней `<div id="clock">`.
2. Flask-роут `/time` возвращает HTML-фрагмент с текущим временем: `<p>Сейчас: 12:34:56</p>`.
3. Добавь на ту же страницу Alpine.js: поле ввода с `x-model="name"` и приветствие `Привет, <имя>!` (если имя пустое — просто `Привет!`).

Запусти Flask, открой страницу, нажми кнопку — время должно появиться без перезагрузки; введи имя — приветствие должно обновляться сразу.

### Задача 2
Создай Flask-приложение `subscribe_app.py` и страницу `subscribe.html`. На странице — форма с `<form hx-post="/subscribe" hx-target="#result">`, полем `input type="email" name="email"` и кнопкой. В Flask: `GET /` отдаёт страницу; `POST /subscribe` читает `request.form["email"]`, проверяет, что в адресе есть символ `@`, и возвращает фрагмент: при успехе — `<p class="ok">Готово! Проверь почту.</p>`, при ошибке — `<p class="error">Неверный адрес</p>`. Запусти приложение, введи валидный и невалидный email. Опиши ожидаемое поведение страницы.

### Задача 3
Создай приложение `todo_app.py`: глобальный список `tasks` в памяти (например, список строк). Страница `todo.html`: заголовок, форма с `<form hx-post="/tasks" hx-target="#task-list">`, поле ввода названия и `<ul id="task-list">`, в котором сервер рендерит все задачи. Роут `POST /tasks` добавляет новую задачу из формы и возвращает обновлённый `<ul>` целиком (фрагмент с `<li>` для каждой задачи). Проверь: добавь три задачи подряд — список должен расти без перезагрузки страницы. Опиши ожидаемое поведение.

### Задача 4
Создай статическую страницу `alpine_demo.html` с Alpine.js. Реализуй: 1) счётчик кликов: `<div x-data="{ count: 0 }">` с кнопкой `@click="count++"` и выводом `{{ count }}`; 2) переключатель видимости: кнопка `@click="open = !open"` и `<p x-show="open">`; 3) список книг из массива через `template x-for` с выводом названия и года, и поле поиска с `x-model="query"`, фильтрующее список (используй метод `filteredBooks()`). Опиши ожидаемое поведение каждой части.

### Задача 5
Создай Flask-приложение `shop_app.py`: словарь товаров `{1: {"name": "Кружка", "likes": 0}, ...}` (минимум три товара) и страницу `shop.html`. Для каждого товара — карточка: название, счётчик лайков `<span id="likes-1">♥ 0</span>` и кнопка `<button hx-post="/like/1" hx-target="#likes-1">Лайк</button>`. Роут `POST /like/<int:item_id>` увеличивает счётчик и возвращает фрагмент `<span>♥ N</span>`. На странице также добавь Alpine-поиск: поле `x-model="query"` и список карточек, отфильтрованный по названию (данные товаров передай из Flask в `x-data` через `tojson`). Проверь: ставь лайки (число меняется без перезагрузки), набирай текст в поиске. Опиши ожидаемое поведение.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Для времени в Flask: `from datetime import datetime` и `datetime.now().strftime("%H:%M:%S")`. Фрагмент — обычная строка с тегами: `f"<p>Сейчас: {now}</p>"`. Для Alpine: `x-data="{ name: '' }"`, в тексте — `x-text="name ? 'Привет, ' + name + '!' : 'Привет!'"` (или выражение прямо в `{{ }}`).

### Подсказка 2
HTMX-атрибуты: `hx-post` — метод и путь, `hx-target="#result"` — куда вставить ответ; по умолчанию `hx-swap` — `innerHTML`. В Flask проверка: `if "@" not in email: return '<p class="error">...</p>'`. Не забудь CDN-скрипт HTMX в head страницы.

### Подсказка 3
Храни задачи в глобальном списке Python: `tasks.append(request.form["title"])`. Фрагмент собери f-строкой: `"".join(f"<li>{t}</li>" for t in tasks)`. `hx-target="#task-list"` — target — сам `<ul>`, и HTMX заменит его внутреннее содержимое.

### Подсказка 4
В `x-data` объяви `{ count: 0, open: false, query: "", books: [...], filteredBooks() { return this.books.filter(b => b.title.includes(this.query)) } }`. В `template x-for` используй `:key` и помни: выражение внутри `x-for` ссылается на переменную цикла. `x-show` лишь скрывает элемент (display: none).

### Подсказка 5
Данные для Alpine передай из Flask: `x-data='{ query: "", items: {{ items | tojson }} }'` — `tojson` сериализует Python-список в JSON. В JS-выражениях фильтруй `this.items`. Для HTMX важно: `hx-target` ссылается на id конкретного `<span>` — спаны должны иметь уникальные id.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Приложение `htmx_app.py`:

```python
from datetime import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
  <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body>
  <button hx-get="/time" hx-target="#clock">Показать время</button>
  <div id="clock"></div>

  <div x-data="{ name: '' }">
    <input type="text" x-model="name" placeholder="Твоё имя">
    <p x-text="name ? 'Привет, ' + name + '!' : 'Привет!'"></p>
  </div>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.get("/time")
def current_time():
    now = datetime.now().strftime("%H:%M:%S")
    return f"<p>Сейчас: {now}</p>"
```

Запуск: `flask --app htmx_app run`. Кнопка подгрузит `#clock` без перезагрузки; при вводе имени приветствие меняется мгновенно.

Разбор. Страница — обычная строка с подключёнными CDN-скриптами, никакой сборки. HTMX-часть: `hx-get="/time"` — запрос GET; `hx-target="#clock"` — куда вставлять ответ; по умолчанию `hx-swap="innerHTML"` заменяет содержимое блока, поэтому время появляется внутри `#clock`. Важно: `/time` отдаёт именно HTML-фрагмент, а не JSON — HTMX со вставит как есть. Alpine-часть: `x-data` заводит состояние `name`; `x-model="name"` связывает поле ввода с состоянием; `x-text` вычисляет текст приветствия при каждом изменении — так используется тернарный оператор для пустого имени. Ни одного рукописного `<script>` с логикой — только декларативные атрибуты.

### Разбор 2
Приложение `subscribe_app.py`:

```python
from flask import Flask, render_template_string, request

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
</head>
<body>
  <h1>Подписка</h1>
  <form hx-post="/subscribe" hx-target="#result">
    <input type="email" name="email" placeholder="email@example.com" required>
    <button type="submit">Подписаться</button>
  </form>
  <div id="result"></div>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.post("/subscribe")
def subscribe():
    email = request.form["email"]
    if "@" not in email:
        return '<p class="error">Неверный адрес</p>'
    return '<p class="ok">Готово! Проверь почту.</p>'
```

Разбор: форма использует `hx-post="/subscribe"` — при отправке HTMX перехватит submit-событие и пошлёт POST-запрос, не перезагружая страницу. `hx-target="#result"` говорит, куда вставить ответ, — в `<div id="result">`. Сервер читает `request.form["email"]`, проверяет наличие `@` и возвращает маленький HTML-фрагмент: `<p>` с классом `ok` или `error`. HTMX заменяет содержимое `#result` этим фрагментом. Проверка: при валидном адресе появляется зелёное «Готово!», при невалидном — сообщение об ошибке, и ни разу страница не перезагружается.

### Разбор 3
Приложение `todo_app.py`:

```python
from flask import Flask, render_template_string, request

app = Flask(__name__)
tasks: list[str] = []

PAGE = """
<!doctype html>
<html>
<head>
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
</head>
<body>
  <h1>Список задач</h1>
  <form hx-post="/tasks" hx-target="#task-list">
    <input type="text" name="title" placeholder="Новая задача" required>
    <button type="submit">Добавить</button>
  </form>
  <ul id="task-list">
    {% for t in tasks %}<li>{{ t }}</li>{% endfor %}
  </ul>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE, tasks=tasks)

@app.post("/tasks")
def add_task():
    tasks.append(request.form["title"])
    return "".join(f"<li>{t}</li>" for t in tasks)
```

Разбор: изначально `<ul id="task-list">` заполняется на сервере циклом Jinja по списку `tasks`. При submit форма уходит POST-запросом на `/tasks`; роут добавляет новую задачу в глобальный список и строит весь `<ul>` заново из текущих задач: `"".join(f"<li>{t}</li>" for t in tasks)` — это и есть HTML-фрагмент, который HTMX вернёт в `#task-list`. Так как `hx-target` указывает на сам `<ul>`, а swap по умолчанию `innerHTML`, содержимое списка заменится полностью — новая задача появится в конце. Каждая добавленная задача отображается без перезагрузки страницы, а при обновлении страницы список сохранится, потому что `tasks` живёт в памяти процесса.

### Разбор 4
Файл `alpine_demo.html`:

```html
<!doctype html>
<html>
<head>
  <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body>
  <div x-data="{ count: 0, open: false, query: '', books: [
      { title: 'Война и мир', year: 1869 },
      { title: '1984', year: 1949 },
      { title: 'Мастер и Маргарита', year: 1967 }
    ],
    filteredBooks() {
      return this.books.filter(b => b.title.includes(this.query));
    }
  }">
    <h2>Счётчик</h2>
    <button @click="count++">Клик! {{ count }}</button>

    <h2>Видимость</h2>
    <button @click="open = !open">Toggle</button>
    <p x-show="open">Теперь меня видно!</p>

    <h2>Книги</h2>
    <input type="text" x-model="query" placeholder="Фильтр по названию">
    <ul>
      <template x-for="book in filteredBooks()" :key="book.title">
        <li>
          <span x-text="book.title"></span>
          (<span x-text="book.year"></span>)
        </li>
      </template>
    </ul>
  </div>
</body>
</html>
```

Разбор: `x-data` объявляет реактивный объект состояния: числа, булевы значения, строку `query`, массив книг и метод `filteredBooks()`. Кнопка счётчика через `@click="count++"` увеличивает `count`, а `{{ count }}` мгновенно перерисовывается. `x-show="open"` управляет видимостью через CSS (`display: none`), поэтому блок скрывается и появляется без пересоздания DOM. Фильтр: поле `x-model="query"` синхронизируется с состоянием, а `template x-for` проходит по результату `filteredBooks()` — при каждом вводе методы пересчитываются, и список мгновенно сужается. Так Alpine закрывает всю локальную интерактивность без единого запроса к серверу.

### Разбор 5
Приложение `shop_app.py`:

```python
from flask import Flask, render_template_string

app = Flask(__name__)

products = {
    1: {"name": "Кружка", "likes": 0},
    2: {"name": "Футболка", "likes": 0},
    3: {"name": "Стикеры", "likes": 0},
}

PAGE = """
<!doctype html>
<html>
<head>
  <script src="https://unpkg.com/htmx.org@1.9.12"></script>
  <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body>
  <h1>Магазин</h1>
  <div x-data='{ query: "", items: {{ items | tojson }} }'>
    <input type="text" x-model="query" placeholder="Поиск товаров">
    <template x-for="item in items.filter(i => i.name.includes(query))" :key="item.id">
      <div class="card">
        <p><span x-text="item.name"></span></p>
        <span :id="'likes-' + item.id" x-text="'♥ ' + item.likes"></span>
        <button :hx-post="'/like/' + item.id" :hx-target="'#likes-' + item.id">Лайк</button>
      </div>
    </template>
  </div>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE, items=list(products.values()))

@app.post("/like/<int:item_id>")
def like(item_id: int):
    products[item_id]["likes"] += 1
    likes = products[item_id]["likes"]
    return f"<span>♥ {likes}</span>"
```

Разбор: товары передаются из Flask в Alpine через `{{ items | tojson }}` — фильтр Jinja сериализует Python-список в JSON, поэтому `x-data` получает данные, а `x-for` рендерит карточки. Поле поиска с `x-model="query"` фильтрует массив прямо в выражении `items.filter(i => i.name.includes(query))` — список мгновенно сужается при вводе. HTMX-часть: на кнопке атрибуты `hx-post` и `hx-target` задаются динамически через Alpine-биндинг (`:hx-post="'/like/' + item.id"`), и HTMX читает их в момент клика. Сервер увеличивает счётчик и возвращает свежий `<span>` с числом лайков, который подставляется в нужный `<span>`. Так HTMX и Alpine дополняют друг друга: первая обновляет серверные данные, вторая — локальную логику.
<!--/SOLUTION-->

<!--QUIZ-->
Какой атрибут HTMX указывает, куда вставить ответ сервера?
- hx-get
- hx-target
- hx-trigger
- hx-swap
* Правильный ответ: hx-target
hx-target задаёт CSS-селектор элемента, в который HTMX вставит полученный HTML.

Что возвращает сервер для HTMX — JSON или HTML?
- Только JSON
- HTML-фрагмент, который HTMX подставляет в страницу
- Бинарные файлы
- Ничего
* Правильный ответ: HTML-фрагмент, который HTMX подставляет в страницу
Философия HTMX: сервер рендерит разметку, а HTMX лишь меняет её место на странице.

Как в Alpine.js объявить состояние компонента?
- С помощью x-data="{ ... }"
- С помощью hx-get
- С помощью @click
- С помощью x-show
* Правильный ответ: С помощью x-data="{ ... }"
x-data создаёт реактивный объект состояния, к которому обращаются выражения внутри компонента.

Что делает x-model в Alpine.js?
- Скрывает элемент
- Связывает поле ввода с состоянием (двусторонняя связь)
- Отправляет запрос на сервер
- Перезагружает страницу
* Правильный ответ: Связывает поле ввода с состоянием (двусторонняя связь)
При вводе текста состояние обновляется, а все места, где оно выводится (например, через x-text), тут же перерисовываются.

Где уместно применять связку HTMX + Alpine.js?
- В тяжёлых одностраничных приложениях с большим состоянием
- В админках, лендингах, простых сервисах, где не нужна сборка
- Только в мобильных приложениях
- Только на сервере
* Правильный ответ: В админках, лендингах, простых сервисах, где не нужна сборка
Это лёгкий стек без build-шага: быстро внедряется и подходит для большинства типовых задач, а для сложных SPA лучше взять React/Vue.
<!--/QUIZ-->
