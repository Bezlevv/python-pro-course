---
title: Independent Work: Personal Landing Site with Flask + Jinja2 + CSS
summary: Build a personal landing site: Flask + Jinja2 (inheritance, include, filters), CSS Flexbox/Grid with responsiveness, pytest tests of pages and templates.
order: 9
duration: 240 min
difficulty: intermediate
tags: flask, jinja2, html, css, tests
---

This is an independent work in which you will build a real web application — a personal landing site. All the studied topics come together here: Flask and routes, Jinja2 templates with inheritance, CSS layout with Flexbox and Grid, responsiveness, and pytest automated tests. The work is designed for several sittings: take your time, go through the stages in order, and run the program after each one.

## Problem statement

You need to create a personal landing site: a personal page telling about yourself, your skills, projects, and contacts. The site consists of several pages assembled from shared templates: a common header with navigation and a footer on every page, while the content changes. Data about skills and projects lives in Python code, and templates output it with loops and filters. The finished project is covered by pytest tests.

What you will learn: design an application skeleton, inherit templates, extract repeating fragments via include, write custom filters, style pages with variables, flex and grid with media queries, and verify the result with tests.

## Requirements

- An `app.py` application on Flask; routes `/` and `/about` (you may add your own); all pages render via `render_template`.
- A common skeleton `templates/base.html`: `<head>` with `meta charset`, `meta viewport`, a `title` block, and styles linked via `url_for("static", filename="style.css")`; in `<body>` — a `<header>` with `<nav>` (logo and links), `<main>` with a `content` block, and a `<footer>`.
- Child pages inherit `base.html` via `{% extends %}` and override only the `title` and `content` blocks. Common parts (header, footer) are not duplicated in pages.
- The main page contains sections: hero (name, role, photo), about (a couple of paragraphs about yourself), skills (a list of skills with levels), projects (a grid of project cards), contacts (links to Telegram/email and a stub form).
- Data (skills, projects) — lists of dictionaries in `app.py`; templates output them with `{% for %}` loops.
- At least one custom filter via `@app.template_filter` (for example, `level_label` or `truncate_words`) and the use of built-in ones: `length`, `default`, `upper`.
- Styles in `static/style.css`: CSS variables `:root`, reset `box-sizing: border-box`, flex navigation, grid project grid, media query `@media (max-width: 768px)`.
- Tests in `test_app.py` via `TestClient`: at least 8 assertions — statuses 200, key page texts, inheritance (common header/footer everywhere, different `<title>`), filter operation.
- Readable code with comments; the app runs with `python app.py` and opens at `http://127.0.0.1:5000/`.

## Assessment criteria (10 points)

| Criterion | Points |
|---|---|
| Flask skeleton + template inheritance (base.html, blocks, routes) | 2 |
| Main page sections and content (hero, about, skills, projects, contacts) | 2 |
| Styles: variables, flex navigation, grid grid, responsiveness | 2 |
| Dynamic data and a custom filter | 2 |
| pytest tests pass, code readable | 2 |

Passing grade — from 7 points.

## What to submit

- The file `app.py` (full working version after stage 5).
- Templates from `templates/`: `base.html`, `index.html`, `about.html`, fragments (for example, `contacts.html`).
- The file `static/style.css`.
- The file `test_app.py` — all tests green (`pytest test_app.py -v`).
- Screenshots of the desktop and mobile versions of the main page (or a short text description).
- A comment at the top of `app.py`: how to run, which files are responsible for what, what you would improve.
- The lesson quiz on the platform (8 questions).

<!--TASK-->
### Task 1

The application skeleton and template inheritance. Create `app.py`: a Flask app with routes `/` and `/about`, each returning `render_template` for `index.html` and `about.html`. Create `templates/base.html`: `<!DOCTYPE html>`, `<head>` with `meta charset`, `meta name="viewport"`, a `<title>{% block title %}...{% endblock %}</title>` block, and styles linked with `<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}\">`; in `<body>` — `<header>` with `<nav>` (logo «PythonПро» and links «Главная», «Обо мне»), `<main>` with a `{% block content %}{% endblock %}` block, footer `<footer>© 2026, PythonПро</footer>`. Create `templates/index.html` and `templates/about.html` with `{% extends "base.html" %}`: override `title` («Главная» and «Обо мне») and `content` (a greeting and a paragraph about yourself). Run `python app.py` and check both pages in the browser: the header, footer, and navigation must be on both, while the tab title differs.

### Task 2

Site sections. On the main `index.html`, inside the `content` block, add sections: `hero` — `<h1>` with your name, `<p>` with a role (for example, «Python-разработчик»), `<img>` with a photo; `about` — two or three paragraphs about yourself; `skills` — a bulleted `<ul>` list of four or five skills; `projects` — `<section class="projects">` with three `<article class="card">` (title and description); `contacts` — links to Telegram and email. Project descriptions can be written as text right in the template for now. In `about.html`, add a `content` block with two paragraphs and a list of hobbies. Refresh the pages in the browser and check that all sections display.

### Task 3

Styling: variables, flex, grid, responsiveness. Create `static/style.css`: `:root` with variables `--accent`, `--bg`, `--card-gap`; a universal reset `* { box-sizing: border-box; }`; styles for `body` (background `var(--bg)`, font), navigation (`display: flex`, `justify-content`, `gap`, `list-style: none`), sections, `.card` (border, padding, border-radius), and `.projects` (`display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: var(--card-gap);`). Add a media query `@media (max-width: 768px)`: navigation becomes `flex-direction: column`, `.projects` becomes `grid-template-columns: 1fr`. Link styles in `base.html` via `url_for`. Check: narrow the browser window — project columns should collapse into one, navigation into a column.

### Task 4

Dynamic data and filters. In `app.py`, define lists of dictionaries: `SKILLS = [{"name": "Python", "level": 5}, ...]` (4–5 skills) and `PROJECTS = [{"title": ..., "description": ..., "year": ...}, ...]` (3–4 projects). Pass them to `render_template` for `/`. In templates, output skills with a loop (e.g., `{{ skill.name }}`), projects as cards from dictionaries. Add a custom filter via `@app.template_filter("level_label")`: it turns a level number 1–5 into a word («новичок», «базовый», «средний», «уверенный», «эксперт»). Use it in the template: `{{ skill.level|level_label }}`. Also apply built-in filters: `{{ projects|length }}` (the number of projects), `{{ skill.name|upper }}` in at least one place, `{{ project.description|default("нет описания") }}`. Check the pages in the browser.

### Task 5

pytest tests of pages and templates. Create `test_app.py`: import `app` from `app.py`, `TestClient` from `flask.testing`, set up `client = TestClient(app)`. Write tests: `test_index_status` — `/` returns 200; `test_index_content` — the response text contains your name, the word «Проекты», and the number from the `length` filter (for example, «3 проекта» or similar); `test_about_status` — `/about` returns 200 and contains `<title>Обо мне</title>`; `test_inheritance` — both `/` and `/about` contain «PythonПро» (logo/footer) and the link `href="/about"`; `test_level_label_filter` — the `/` response contains the word «эксперт» (for a skill with level 5). Run `pytest test_app.py -v` and get all tests green.

<!--/TASK-->

<!--HINT-->
### Hint 1

Structure: `app.py` sits next to the `templates` and `static` folders. In `base.html`, all common parts — header, navigation, footer — sit outside blocks; the `title` and `content` blocks are the only things child templates override. The first line of `index.html` is `{% extends "base.html" %}`. Don't forget `app.run(debug=True)` under `if __name__ == "__main__":`.

### Hint 2

Each section is a `<section>` with a class for future styles: `class="hero"`, `class="about"`, `class="skills"`, `class="projects"`, `class="contacts"`. Inside sections use semantic tags: `h1`/`h2`, `p`, `ul`/`li`, `img`, `a`. The image can be linked from an external resource (for example, `https://picsum.photos/200`) — this doesn't violate the requirements.

### Hint 3

Variables are used via `var(--имя)`. For navigation, `display: flex; justify-content: center; gap: 24px; list-style: none;` on the `ul` (or its class) is enough. For the grid use `repeat(auto-fit, minmax(240px, 1fr))` — columns will wrap automatically without a hard-coded count. Write the media query at the end of the file.

### Hint 4

Filter: `@app.template_filter("level_label")` above `def level_label(level): ...`, which returns a word from the list `["новичок", "базовый", "средний", "уверенный", "эксперт"]` by index `level - 1` (with a bounds check). In the template: `{{ skill.level|level_label }}`. Note: `{{ projects|length }}` is a number wrapped in text: «У меня {{ projects|length }} проекта» — but for the numbers 1 and 5, carefully choose the word form or use a simpler sentence.

### Hint 5

`TestClient(app)` calls the application in memory without a server. `response.text` is the response body as a string; we search for substrings in it: `assert "PythonПро" in response.text`. To check different tab titles, search for `<title>Главная</title>` and `<title>Обо мне</title>` separately. Run `pytest test_app.py -v` from the project folder — tests should be discovered automatically.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
```

`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}PythonПро{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <nav>
            <a href="/" class="logo">PythonПро</a>
            <a href="/">Главная</a>
            <a href="/about">Обо мне</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>© 2026, PythonПро</footer>
</body>
</html>
```

`templates/index.html`:

```html
{% extends "base.html" %}

{% block title %}Главная{% endblock %}

{% block content %}
    <h1>Привет, я Аня!</h1>
    <p>Это мой сайт-визитка.</p>
{% endblock %}
```

`templates/about.html` — similarly, but `title` = «Обо мне» and different text in `content`. Breakdown. Flask automatically looks for templates in `templates` and static files in `static`; `url_for("static", filename="style.css")` generates the correct path. In `base.html`, the `title` and `content` blocks are "holes" in the skeleton that child templates fill. Navigation and footer sit outside blocks — so they are identical on all pages. Browser check: two pages with different tab titles but a shared header and footer. If the header disappeared, check that `{% extends %}` is the first line.

### Solution 2

A fragment of `index.html` (inside `content`):

```html
<section class="hero">
    <h1>Аня Иванова</h1>
    <p>Python-разработчик</p>
    <img src="https://picsum.photos/200" alt="Фото">
</section>

<section class="about">
    <h2>Обо мне</h2>
    <p>Изучаю Python и веб-разработку уже год. Делаю проекты на Flask.</p>
</section>

<section class="skills">
    <h2>Навыки</h2>
    <ul>
        <li>Python</li>
        <li>Flask</li>
        <li>HTML/CSS</li>
        <li>SQL</li>
    </ul>
</section>

<section class="projects">
    <h2>Проекты</h2>
    <article class="card"><h3>Визитка</h3><p>Этот сайт</p></article>
    <article class="card"><h3>Заметки</h3><p>Консольное приложение на Python</p></article>
    <article class="card"><h3>Бот</h3><p>Telegram-бот на Flask</p></article>
</section>

<section class="contacts">
    <h2>Контакты</h2>
    <a href="https://t.me/username">Telegram</a>
    <a href="mailto:me@example.com">Почта</a>
</section>
```

Breakdown. Each section is a `<section>` with a class: this gives a foothold for CSS at the next stage. Inside — only semantic tags: headings, paragraphs, lists, links. The skill list is `<ul>` with `<li>`; projects are `<article class="card">`, because a card is an independent self-contained block. Contact links: `https://t.me/username` for Telegram and `mailto:...` for email. There are no nested `##`-headings inside sections — only HTML; this matters for template cleanliness.

### Solution 3

`static/style.css` (key parts):

```css
:root {
    --accent: #2563eb;
    --bg: #f5f7fa;
    --card-gap: 16px;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: sans-serif;
    background: var(--bg);
}

nav {
    display: flex;
    justify-content: center;
    gap: 24px;
    padding: 16px;
    background: white;
}

nav a {
    color: var(--accent);
    text-decoration: none;
}

.card {
    border: 1px solid #ddd;
    padding: 16px;
    border-radius: 8px;
    background: white;
}

.projects {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: var(--card-gap);
}

@media (max-width: 768px) {
    nav { flex-direction: column; align-items: center; }
    .projects { grid-template-columns: 1fr; }
}
```

Breakdown. `:root` stores variables: accent color, background, spacing. `var(--bg)` substitutes the value — you can change the palette in one place. `* { box-sizing: border-box; }` keeps cards from "sprawling" due to padding. Navigation is flex: links in a centered row with `gap`. `.projects` is grid with `repeat(auto-fit, minmax(240px, 1fr))`: columns are created automatically as space allows (three on a wide screen, two on a medium one). The 768px media query turns navigation into a column and makes projects single-column. Checking in the browser with a narrowing window shows responsiveness.

### Solution 4

`app.py` (additions):

```python
SKILLS = [
    {"name": "Python", "level": 5},
    {"name": "Flask", "level": 4},
    {"name": "HTML/CSS", "level": 3},
    {"name": "SQL", "level": 2},
]

PROJECTS = [
    {"title": "Визитка", "description": "Этот сайт", "year": 2026},
    {"title": "Заметки", "description": "Консольный менеджер заметок", "year": 2025},
    {"title": "Трекер привычек", "description": "Приложение с напоминаниями", "year": 2025},
]

@app.template_filter("level_label")
def level_label(level):
    words = ["новичок", "базовый", "средний", "уверенный", "эксперт"]
    if 1 <= level <= len(words):
        return words[level - 1]
    return "неизвестно"

@app.route("/")
def index():
    return render_template("index.html", skills=SKILLS, projects=PROJECTS)
```

In the template:

```jinja
<ul>
    {% for skill in skills %}
        <li>{{ skill.name }} — {{ skill.level|level_label }}</li>
    {% endfor %}
</ul>
<p>Всего проектов: {{ projects|length }}</p>
```

Breakdown. Data is moved out of the template into Python — the template became a pure view, and data can be changed without touching HTML. The loop `{% for skill in skills %}` iterates dictionaries; field access is via a dot: `{{ skill.name }}`. The custom filter `level_label` takes a number and returns a word: `{{ skill.level|level_label }}`. The filter with a bounds check is safe for any value. The built-in `{{ projects|length }}` outputs the number of projects. If the list is empty, `{% for %}` just outputs nothing — rendering won't crash.

### Solution 5

`test_app.py`:

```python
from flask.testing import TestClient
from app import app, PROJECTS

client = TestClient(app)

def test_index_status():
    assert client.get("/").status_code == 200

def test_index_content():
    r = client.get("/")
    assert "Аня" in r.text
    assert "Проекты" in r.text
    assert f"{len(PROJECTS)}" in r.text

def test_about_status():
    r = client.get("/about")
    assert r.status_code == 200
    assert "<title>Обо мне</title>" in r.text

def test_inheritance():
    for path in ("/", "/about"):
        r = client.get(path)
        assert "PythonПро" in r.text
        assert 'href="/about"' in r.text

def test_level_label_filter():
    r = client.get("/")
    assert "эксперт" in r.text
```

Breakdown. `TestClient(app)` calls the application without starting a server — tests are fast and isolated. `test_index_status` and `test_about_status` check that pages respond with 200. `test_index_content` searches the HTML for the name, the section title, and the project count from data (comparing with `len(PROJECTS)` guards against desynchronization). `test_inheritance` is the essence of inheritance: the common «PythonПро» (logo and footer) and navigation are present on both pages. `test_level_label_filter` checks the custom filter: a skill with level 5 gives «эксперт» in the rendered HTML. Run `pytest test_app.py -v` — five green tests. If a test fails, read the pytest output: it shows on which line and which substring wasn't found.

<!--/SOLUTION-->

<!--QUIZ-->
Where does Flask look for templates by default?
- In the templates folder
- In the static folder
- In the project root
- In the pages folder
* Correct answer: In the templates folder
The templates folder sits next to app.py; file names are given in render_template without a path.

How to correctly link a CSS file in a template?
- <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
- <link rel="stylesheet" href="style.css">
- <style src="style.css">
- {% css "style.css" %}
* Correct answer: <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
url_for generates the static path regardless of the project structure.

What does {% block content %} do in the base template?
- Describes a place that child templates can fill
- Includes a file
- Declares a variable
- Imports a macro
* Correct answer: Describes a place that child templates can fill
A block is a "hole" in the skeleton; the child template overrides its content.

What must be the first line of a child template?
- {% extends "base.html" %}
- {% block %}
- {% include %}
- {% macro %}
* Correct answer: {% extends "base.html" %}
The extends directive declares inheritance and must come before all other content.

Why are custom filters needed?
- To transform data when outputting in a template
- To speed up Flask
- To replace loops
- To send forms
* Correct answer: To transform data when outputting in a template
For example, level_label turns a level number into a human-readable word: {{ skill.level|level_label }}.

What does TestClient do in tests?
- Calls the application in memory without a real server
- Opens a browser
- Sends emails
- Tests CSS
* Correct answer: Calls the application in memory without a real server
TestClient emulates HTTP requests, so tests don't require a running server.

How to check page content in a test?
- assert "текст" in response.text
- assert response.html == "текст"
- assert response.body.has("текст")
- print(response.text)
* Correct answer: assert "текст" in response.text
response.text is the response body as a string; the substring is searched with the in operator.

What does repeat(auto-fit, minmax(240px, 1fr)) do in grid?
- Automatically creates columns from 240px wide according to available space
- Always creates exactly 3 columns
- Makes the grid fixed
- Disables grid
* Correct answer: Automatically creates columns from 240px wide according to available space
Columns wrap depending on the window width — the layout is responsive without separate media rules for every width.

What happens to the navigation at max-width: 768px?
- Styles from the media query apply, e.g. flex-direction: column
- Nothing changes
- The navigation is removed
- The page becomes empty
* Correct answer: Styles from the media query apply, e.g. flex-direction: column
A media query overrides properties when the window width is ≤ 768px.

What does the inheritance test check?
- That common header and footer elements are on all pages
- That all pages are identical
- That CSS is linked
- That filters work
* Correct answer: That common header and footer elements are on all pages
The test searches the responses of several pages for the same substrings — logo, navigation links, footer text.
<!--/QUIZ-->
