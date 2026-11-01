---
title: JavaScript для питониста: клиентская часть
summary: DOM, события, выборка элементов, изменение стилей, fetch к своему API, обработка форм без перезагрузки — и сравнение синтаксиса JS и Python.
order: 18
duration: 60 мин
difficulty: intermediate
tags: javascript, dom, fetch, фронтенд
---

До этого момента весь твой код жил на сервере: Flask, FastAPI или Django отвечали на запросы и возвращали HTML. Но одна половина веб-интерфейса всегда работает в браузере пользователя — и это JavaScript. На этом уроке ты научишься оживлять страницы: реагировать на клики, менять содержимое без перезагрузки и общаться с твоим же Python-API через `fetch`. Если ты уже знаешь Python, JavaScript покажется тебе знакомым — просто с другим синтаксисом.

## JavaScript и Python: сходства

Оба языка — интерпретируемые, с динамической типизацией и функциями как объектами первого класса. Вот как выглядят одни и те же идеи рядом.

**Переменные.** В Python — `x = 5`, в JS — `let x = 5`. Слово `let` означает изменяемую переменную, `const` — константу (переменную, которой нельзя присвоить новое значение):

```javascript
const name = "Аня";   // как name = "Аня" в Python, но переприсвоить нельзя
let count = 0;        // можно менять: count = count + 1
```

**Строки.** Шаблонные строки в JS — почти как f-строки в Python:

```javascript
const user = "Аня";
console.log(`Привет, ${user}!`);  // аналог f"Привет, {user}!"
```

**Коллекции.** Массив `[...]` похож на список, объект `{...}` — на словарь:

```javascript
const skills = ["Python", "JS"];     // как список
const profile = { name: "Аня", age: 25 };  // как словарь
```

Если в Python ты пишешь `profile["name"]`, то в JS — `profile.name`. **Циклы.** `for (const skill of skills)` — почти как `for skill in skills:` в Python.

## DOM — документ как дерево

Когда браузер открывает HTML-страницу, он строит модель документа (DOM, Document Object Model) — дерево, в котором каждый тег становится объектом. JavaScript может ходить по этому дереву: находить элементы, читать их и менять. Именно так страница «оживает».

**Выборка элементов.** Чтобы найти элемент, используй `document.querySelector` — он принимает CSS-селектор:

```javascript
const title = document.querySelector("h1");       // первый заголовок h1
const button = document.querySelector("#submit"); // элемент с id="submit"
const cards = document.querySelectorAll(".card"); // все элементы с классом card
```

`querySelectorAll` возвращает список элементов, по которому можно пройтись циклом. **Изменение текста и содержимого.** У каждого элемента есть свойства `textContent` (текст) и `innerHTML` (HTML внутри):

```javascript
document.querySelector("h1").textContent = "Привет, мир!";
```

**Изменение стилей.** Через свойство `style` или через классы:

```javascript
const body = document.body;
body.style.backgroundColor = "#1e1e2e";     // меняем фон напрямую
body.classList.toggle("dark-theme");        // добавляем/убираем CSS-класс
```

Второй способ предпочтительнее: стили остаются в CSS, а JS только переключает классы.

## События

Событие — это сигнал: клик, отправка формы, нажатие клавиши. Чтобы отреагировать, повесь обработчик через `addEventListener`:

```javascript
const button = document.querySelector("#greet");
button.addEventListener("click", () => {
  document.querySelector("#output").textContent = "Клик получен!";
});
```

Первая стрелка — это функция, которая выполнится при клике. Аналог в Python — передача функции как аргумента. Обрати внимание: имя события пишется без `on` — не `onclick`, а `"click"`.

## Обработка форм без перезагрузки

По умолчанию отправка формы перезагружает страницу. Чтобы этого избежать, перехвати событие `submit` и вызови `preventDefault()`:

```javascript
const form = document.querySelector("#comment-form");
form.addEventListener("submit", (event) => {
  event.preventDefault();  // отменяем перезагрузку страницы
  const data = new FormData(form);   // читаем поля формы
  const text = data.get("text");
  console.log(`Новый комментарий: ${text}`);
});
```

`FormData` — аналог словаря с значениями полей, где ключ — это атрибут `name` у `<input>`.

## fetch: общаемся с твоим API

`fetch` — встроенная функция браузера для HTTP-запросов. Это твой `requests` из Python, только в JS. Так выглядит GET-запрос к собственному Flask-эндпоинту:

```javascript
async function loadStats() {
  const response = await fetch("/api/stats");
  if (!response.ok) {
    throw new Error(`Ошибка HTTP: ${response.status}`);
  }
  const data = await response.json();  // JSON -> объект JS
  document.querySelector("#stats").textContent =
    `Статей: ${data.posts}, пользователей: ${data.users}`;
}
```

Слово `await` приостанавливает функцию, пока не придёт ответ — это аналог синхронного вызова в Python. `response.json()` парсит JSON, как `json.loads()` в Python. Для POST-запроса с данными:

```javascript
const response = await fetch("/api/comments", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Классный урок!" }),
});
```

`JSON.stringify` превращает объект в строку JSON — это обратная операция к `response.json()`.

## Итог

Теперь у тебя есть полный цикл: HTML описывает структуру, CSS — вид, JS — поведение, а Python-бэкенд — данные. В этой связке JS-код в браузере делает `fetch` к API Flask/FastAPI, получает JSON и обновляет DOM — без единой перезагрузки страницы. Закрепим всё задачами.

<!--TASK-->
### Задача 1
Создай HTML-страницу `hello_dom.html` с абзацем `<p id="greeting">Пока, мир!</p>` и кнопкой `<button id="change">Поменять текст</button>`. Подключи файл `script.js`. В нём напиши код: найди кнопку через `document.querySelector`, повесь на неё обработчик события `click`, а внутри обработчика поменяй текст абзаца на «Привет, мир!» через свойство `textContent`. Открой страницу в браузере, нажми кнопку и убедись, что текст абзаца меняется без перезагрузки страницы.

### Задача 2
Создай страницу `theme.html` с кнопкой `id="toggle"` и блоком `<div class="card">` с любым текстом. В файле `style.css` опиши класс `dark-theme` для `body`: тёмный фон (`background-color: #1e1e2e`) и светлый цвет текста. В `script.js` повесь на кнопку обработчик `click`, который переключает класс `dark-theme` на `document.body` через `classList.toggle`. Проверь в браузере: при каждом клике фон должен переключаться между светлым и тёмным, а сам текст в карточке должен оставаться читаемым.

### Задача 3
Создай страницу `form.html` с формой: поле `<input name="email" id="email">`, кнопка-«поле submit» и блок `<p id="message">` для вывода результата. В `script.js` повесь на форму обработчик `submit`, вызови `event.preventDefault()` (чтобы страница не перезагружалась), прочитай значение поля через `new FormData(form).get("email")` и проверь: если в строке нет символа `@`, выведи в `#message` текст «Некорректный email»; иначе — «Принято!». Проверь оба случая в браузере.

### Задача 4
Создай приложение «Статистика сайта». На бэкенде (Flask или FastAPI) сделай эндпоинт `GET /api/stats`, который возвращает JSON: `{"posts": 12, "users": 340, "comments": 1500}`. На фронтенде создай `stats.html` с кнопкой `id="load"` и блоком `<pre id="output">`. В `script.js` напиши асинхронную функцию `loadStats()`: она делает `fetch("/api/stats")`, проверяет `response.ok`, получает JSON через `response.json()` и выводит данные в `#output` в виде строки вида `Статей: 12, пользователей: 340, комментариев: 1500`. Повесь `loadStats` на клик по кнопке. Открой страницу, нажми кнопку и убедись, что данные приходят с сервера и отображаются.

### Задача 5
Собери мини-приложение «Комментарии». На бэкенде сделай два эндпоинта: `GET /api/comments` (возвращает список JSON-объектов с полями `author` и `text`) и `POST /api/comments` (принимает JSON `{"author": ..., "text": ...}`, добавляет комментарий и возвращает его обратно). На фронтенде: страница `comments.html` со списком `<ul id="list">`, формой (поля `name="author"` и `name="text"`) и блоком для ошибок. При загрузке страницы сделай `fetch` к `GET /api/comments` и выведи комментарии в список. При отправке формы — перехвати `submit`, сделай `POST` через `fetch` с заголовком `Content-Type: application/json` и телом `JSON.stringify({author, text})`, затем добавь ответ сервера в список через `createElement` и `appendChild` — без перезагрузки. Если сервер вернул ошибку, покажи её в блоке для ошибок. Проверь: комментарий появляется в списке сразу после отправки.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Используй `document.querySelector("#change")` для кнопки и `document.querySelector("#greeting")` для абзаца. Обработчик вешается так: `button.addEventListener("click", () => { ... })`. Внутри стрелочной функции присвой `greeting.textContent = "Привет, мир!"`. Подключай скрипт в конце `<body>` или через атрибут `defer`, чтобы элементы уже существовали к моменту выполнения JS.

### Подсказка 2
`classList.toggle("dark-theme")` сам добавляет класс, если его нет, и убирает, если он есть — не нужно писать проверки. Убедись, что в CSS класс записан как `.dark-theme { ... }`, а не как тег. Стили для `body` с этим классом перекроют базовые, если стоят позже в файле или имеют достаточную специфичность.

### Подсказка 3
Обработчик формы: `form.addEventListener("submit", (event) => { event.preventDefault(); ... })`. Для чтения поля используй `new FormData(form).get("email")`. Проверку на `@` сделай через `text.includes("@")`. Не забудь, что `email` — это атрибут `name` у `<input>`, а не `id`.

### Подсказка 4
Объяви функцию как `async function loadStats() { ... }` и внутри используй `await fetch(...)`. После `await fetch` проверь `if (!response.ok) throw new Error(...)`. `await response.json()` вернёт объект — обратись к его свойствам через `data.posts`, `data.users`, `data.comments`. Кнопка: `document.querySelector("#load").addEventListener("click", loadStats)`.

### Подсказка 5
Для POST укажи `method: "POST"`, `headers: { "Content-Type": "application/json" }` и `body: JSON.stringify({ author, text })`. Ответ сервера распарси через `await response.json()` — это будет объект добавленного комментария. Новый элемент списка создавай так: `const li = document.createElement("li"); li.textContent = `${c.author}: ${c.text}`; list.appendChild(li);`. Не забудь `event.preventDefault()` в обработчике формы.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение `script.js`:

```javascript
const button = document.querySelector("#change");
const greeting = document.querySelector("#greeting");

button.addEventListener("click", () => {
  greeting.textContent = "Привет, мир!";
});
```

Что здесь происходит? Сначала мы находим оба элемента в DOM с помощью `document.querySelector` — по атрибуту id, который записывается как `#change` и `#greeting`. Затем на кнопку вешается обработчик события через `addEventListener("click", ...)`. Второй аргумент — стрелочная функция, которая выполнится только тогда, когда пользователь кликнет по кнопке. Внутри неё мы присваиваем свойству `textContent` абзаца новую строку — браузер мгновенно перерисовывает текст на странице. Никакой перезагрузки не происходит: мы работаем с уже существующим элементом, а не создаём новые страницы. Эта схема — «найти элемент → повесить обработчик → изменить содержимое» — основа всей клиентской разработки.

### Разбор 2
Код `script.js`:

```javascript
const toggle = document.querySelector("#toggle");
toggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-theme");
});
```

CSS `style.css`:

```css
body.dark-theme {
  background-color: #1e1e2e;
  color: #e0e0e0;
}
```

Что здесь происходит? `classList.toggle("dark-theme")` проверяет, есть ли у `body` класс `dark-theme`. Если нет — добавляет, если есть — убирает. Это экономит целые `if/else`-конструкции: одно действие переключает состояние. Стили самого класса описаны в CSS, поэтому JS не смешивается с оформлением — это разделение ответственности, знакомое тебе по Python-проектам (логика отдельно, представление отдельно). Переключение классов — самый распространённый способ менять вид интерфейса: тёмные темы, активные пункты меню, подсветка карточек — всё делается именно так.

### Разбор 3
Код `script.js`:

```javascript
const form = document.querySelector("#signup");
const message = document.querySelector("#message");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const email = data.get("email");

  if (!email.includes("@")) {
    message.textContent = "Некорректный email";
  } else {
    message.textContent = "Принято!";
  }
});
```

Что здесь происходит? Без `event.preventDefault()` браузер отправил бы форму стандартным способом и перезагрузил страницу — наш JS вообще не успел бы показать результат. Вызвав `preventDefault()`, мы отменяем это поведение по умолчанию и берём управление на себя. `new FormData(form)` собирает все поля формы в объект, а `.get("email")` достаёт значение по атрибуту `name` поля. Проверка `email.includes("@")` — та же, что и в Python: `"@" in email`, только синтаксис другой. Так работает «одностраничная» валидация: пользователь видит ошибку мгновенно, не теряя заполненные данные.

### Разбор 4
Бэкенд на Flask (фрагмент):

```python
@app.get("/api/stats")
def stats():
    return {"posts": 12, "users": 340, "comments": 1500}
```

Фронтенд `script.js`:

```javascript
async function loadStats() {
  const response = await fetch("/api/stats");
  if (!response.ok) {
    throw new Error(`Ошибка HTTP: ${response.status}`);
  }
  const data = await response.json();
  document.querySelector("#output").textContent =
    `Статей: ${data.posts}, пользователей: ${data.users}, комментариев: ${data.comments}`;
}

document.querySelector("#load").addEventListener("click", loadStats);
```

Что здесь происходит? `fetch` возвращает Promise — объект, который «пообещает» результат позже. Ключевое слово `await` приостанавливает выполнение функции, пока браузер не получит ответ от сервера, — это аналог блокирующего вызова. `response.ok` — аналог `response.status_code == 200` в `requests`; если сервер вернул ошибку, мы её выбрасываем. `await response.json()` парсит тело ответа как JSON и превращает его в объект JS — так же, как `json.loads()` в Python. Дальше мы просто читаем свойства `data.posts` и т. д. и собираем строку через шаблонные строки. Так клиент и сервер общаются: Python отдаёт JSON, а JS его отображает.

### Разбор 5
Бэкенд на Flask (эскиз):

```python
comments = [{"author": "Аня", "text": "Первый комментарий"}]

@app.get("/api/comments")
def list_comments():
    return comments

@app.post("/api/comments")
def add_comment():
    data = request.get_json()
    comments.append(data)
    return data, 201
```

Фронтенд `script.js`:

```javascript
const list = document.querySelector("#list");
const form = document.querySelector("#comment-form");
const errorBox = document.querySelector("#error");

async function loadComments() {
  const response = await fetch("/api/comments");
  const items = await response.json();
  list.innerHTML = "";
  for (const c of items) {
    const li = document.createElement("li");
    li.textContent = `${c.author}: ${c.text}`;
    list.appendChild(li);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const payload = { author: data.get("author"), text: data.get("text") };
  try {
    const response = await fetch("/api/comments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error("Не удалось отправить");
    const created = await response.json();
    const li = document.createElement("li");
    li.textContent = `${created.author}: ${created.text}`;
    list.appendChild(li);
    form.reset();
  } catch (err) {
    errorBox.textContent = err.message;
  }
});

loadComments();
```

Что здесь происходит? При загрузке страницы вызывается `loadComments()`: она получает список комментариев и строит элементы `<li>` через `createElement` и `appendChild`. При отправке формы `preventDefault()` отменяет перезагрузку, `FormData` собирает поля, а `JSON.stringify` превращает объект в строку JSON для тела POST-запроса. Обрати внимание на обработку ошибок через `try/catch`: если сервер упал, сообщение появится в `#error`, а не «молча» сломает сценарий. Так выглядит полный цикл современного фронтенда: данные приходят и отправляются через `fetch`, а DOM обновляется точечно, без перезагрузки страницы.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает document.querySelector("p")?
- Возвращает первый элемент p на странице
- Возвращает все элементы p
- Создаёт новый элемент p
* Правильный ответ: Возвращает первый элемент p на странице
querySelector возвращает первый элемент, соответствующий CSS-селектору.

Какой метод добавляет или убирает класс у элемента?
- classList.toggle("имя")
- style.toggle("имя")
- addClass("имя")
* Правильный ответ: classList.toggle("имя")
classList.toggle сам добавляет класс, если его нет, и убирает, если есть.

Что делает event.preventDefault() в обработчике submit?
- Отменяет стандартное поведение формы (перезагрузку страницы)
- Отправляет форму на сервер
- Закрывает страницу
* Правильный ответ: Отменяет стандартное поведение формы (перезагрузку страницы)
preventDefault() блокирует действие браузера по умолчанию — например, перезагрузку при отправке формы.

Что вернёт await response.json()?
- Объект JavaScript, созданный из тела ответа в формате JSON
- Строку HTML
- Объект Response
* Правильный ответ: Объект JavaScript, созданный из тела ответа в формате JSON
response.json() парсит тело ответа и превращает JSON в объект или массив JS.

Как в JS объявляется константа?
- const x = 5
- let x = 5
- x = 5
* Правильный ответ: const x = 5
const объявляет переменную, которой нельзя присвоить новое значение.

Какая строка JS аналогична f"Привет, {user}!" из Python?
- `Привет, ${user}!`
- "Привет, {user}!"
- f"Привет, {user}!"
* Правильный ответ: `Привет, ${user}!`
Шаблонные строки в JS используются в обратных кавычках, а подстановка — через ${...}.

Что делает JSON.stringify({ text: "Привет" })?
- Превращает объект JS в строку JSON
- Превращает строку JSON в объект JS
- Отправляет объект на сервер
* Правильный ответ: Превращает объект JS в строку JSON
JSON.stringify — обратная операция к response.json(): объект становится строкой для тела запроса.

Какой метод находит все элементы с классом card?
- document.querySelectorAll(".card")
- document.querySelectorAll("#card")
- document.querySelector(".card")
* Правильный ответ: document.querySelectorAll(".card")
querySelectorAll возвращает список всех элементов по селектору, а точка перед card — это CSS-селектор класса.

Зачем нужен await перед fetch(...)?
- Чтобы дождаться ответа сервера, не блокируя выполнение остального кода
- Чтобы ускорить запрос
- Чтобы отправить несколько запросов сразу
* Правильный ответ: Чтобы дождаться ответа сервера, не блокируя выполнение остального кода
await приостанавливает асинхронную функцию до получения результата Promise.
<!--/QUIZ-->
