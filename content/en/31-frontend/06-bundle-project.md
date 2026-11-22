---
title: Workshop: building a complete website
summary: Putting it all together: semantic HTML, modern CSS, Jinja2 templates, and a Flask app in one project.
order: 6
duration: 90 min
difficulty: advanced
tags: project, html, css, jinja2, flask
---

The final lesson of the module. We will build a **full website**: with semantic markup, modern CSS built on variables and Flexbox/Grid, Jinja2 templates with inheritance and macros, Flask routes, and tests. It's a scaled-down but real web development stack — you'll meet this exact stack in any Python project.

## Project plan

We're making a mini-blog "My notes":

- two pages: a home page with a post list and a post page;
- a feedback form with validation;
- responsive layout: on wide screens — content + side panel, on narrow ones — a single column;
- tests for structure, styles, and behavior.

Folder structure:

```
blog/
├── app.py              # Flask app
├── templates/
│   ├── base.html       # skeleton with blocks
│   ├── index.html      # home page
│   ├── post.html       # post page
│   ├── contact.html    # feedback form
│   ├── macros.html     # macros (post card)
│   └── partials/
│       └── sidebar.html  # side panel
├── static/
│   └── style.css       # all styles
└── tests/
    ├── test_validation.py
    └── test_site.py
```

## Data

Posts can simply live in a list of dicts — a learning project doesn't need a database:

```python
POSTS = [
    {"id": 1, "title": "Why HTML matters",
     "date": "2026-10-15", "text": "..."},
    {"id": 2, "title": "Flexbox vs. Grid",
     "date": "2026-10-20", "text": "..."},
]

def get_post(post_id):
    return next((p for p in POSTS if p["id"] == post_id), None)
```

## Assembling a page

The home page uses the base template and the card macro:

```html
{% extends "base.html" %}
{% from "macros.html" import post_card %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>My notes</h1>
    <div class="cards">
        {% for post in posts %}
            {{ post_card(post) }}
        {% endfor %}
    </div>
{% endblock %}
```

Flask routes:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)

@app.route("/post/<int:post_id>")
def post(post_id):
    item = get_post(post_id)
    if item is None:
        return "Post not found", 404
    return render_template("post.html", post=item)
```

## Styles

In `static/style.css` — everything we've learned: variables in `:root`, cards on Grid (`repeat(auto-fit, minmax(...))`), a skeleton on `grid-template-areas`, transitions, media queries for mobile and dark theme.

## Styles: variables and layout

In `static/style.css` we'll bring everything we learned into one file. Start with design tokens — variables in `:root`: text and background colors, the brand accent, border radii, spacings. Next — base element styles: typography, links, buttons. Then components: cards (`.card`), navigation (`.nav`), the form (`.form` and fields), the panel (`.sidebar`). For the card layout on the home page use Grid: `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))` — the grid will adapt to the screen width by itself. For the page as a whole — a skeleton on `grid-template-areas`: the `header`, `nav`, `main`, `aside`, `footer` areas, and a media query rebuilds it into one column on mobile. Don't forget transitions on buttons and links, `:focus-visible` for keyboard navigation, and `prefers-reduced-motion` to respect users who disabled animations in the system. Such a file mirrors the whole module: semantics in HTML, styles in CSS, page assembly in Jinja2.

## Testing

We'll write two test files: a form validation test (logic + template) and an integration test of the whole site via jinja2 and BeautifulSoup. This approach is the standard in web development: page rendering is checked automatically, and any broken tag will be caught before deployment.

Let's go. The site is waiting!

<!--TASK-->
### Task 1
Create the project structure from the plan (folders `blog/`, `templates/`, `static/`, `tests/`, `templates/partials/`). Write `templates/base.html`:

- `<html lang="en">`, `<meta charset="UTF-8">`, `<meta name="viewport" ...>`;
- `<title>` inside the `{% block title %}` block;
- `<link rel="stylesheet" href="/static/style.css">`;
- `<header>` with `<nav>` and two links: "Home" (`/`) and "Contacts" (`/contact`);
- `<main>` with the `{% block content %}` block;
- `<footer>` with copyright;
- a `{% block sidebar %}` block in `<aside>`.

Expected result: the skeleton is ready, pages will inherit it.

### Task 2
Create `templates/macros.html` with a `post_card(post)` macro — a post card (`card` class): inside — `<article>`, `<h3>` with the title, `<time datetime="{{ post.date }}">`, `<p>` with truncated text (`{{ post.text|truncate(80) }}`), and a "Read" link to `/post/{{ post.id }}`. Then create `templates/index.html`: `extends base.html`, a `title` block — "Home", a `content` block — an `<h1>` heading and a loop over `posts` with `{{ post_card(post) }}`. Write a script `render_index.py` that renders `index.html` with a list of two posts and prints the result. Expected result: the HTML has two cards with titles and links.

### Task 3
Create `templates/post.html` (the post page): `extends base.html`, a `title` block — `{{ post.title }}`, a `content` block — `<article>` with `<h1>` (title), `<time>`, paragraphs of text. Create `templates/partials/sidebar.html` (a "Recent notes" block with a list of three links) and include it in `base.html` via `{% include "partials/sidebar.html" %}` inside the `sidebar` block. Then create `app.py` with `/` and `/post/<int:post_id>` routes (for an unknown id — "Post not found", status 404) and a `POSTS` list of three posts. Run `flask --app app run` and check: the home page shows cards, `/post/1` — the post, `/post/999` — 404.

### Task 4
Create `templates/contact.html` — a feedback form: "Name" field (`text`, `required`, `minlength="2"`), "Email" (`email`, `required`), "Message" (`textarea`, `required`, `minlength="10"`), a submit button. The form: `action="/contact"`, `method="post"`. In `app.py`, add a `/contact` route (GET — form, POST — validation) and a `validate_contact(data)` function (returns an error dict: name < 2 characters, email without `@`, message < 10 characters). On errors — render `contact.html` with `errors` and preserved `data`; on success — "Message sent!". Then write `tests/test_validation.py`:

- a parametrized test for `validate_contact` (empty data, short name, bad email, short message, valid data);
- a render test for `contact.html` with errors via jinja2 + `BeautifulSoup`: the HTML contains `<p class="error">` with the error text.

Expected result: all tests pass, the form works through the browser.

### Task 5
Write an integration test `tests/test_site.py` that renders all site pages via jinja2 and checks:

- `index.html`: has `<header>`, `<nav>`, `<main>`, `<footer>`; `<nav>` has two links; exactly three `<article class="card">`; each card has a `<time>` and a "Read" link;
- `post.html`: `<main>` contains an `<article>` with `<h1>`;
- `base.html`/all pages: the style is linked (`<link rel="stylesheet" href="/static/style.css">`), there is `<meta name="viewport" ...>`;
- the `contact.html` form: `method="post"`, `action="/contact"`, the "Name", "Email", "Message" fields have a `label` with `for` matching `id`, and `required`;
- `static/style.css`: has `:root` with at least three `--color-` variables, `display: grid` and `display: flex`, `@media`.

Expected result: all tests pass with one command `python -m pytest tests/`.
<!--/TASK-->

<!--HINT-->
### Hint 1
Blocks in `base.html`: `{% block title %}{% endblock %}`, `{% block content %}{% endblock %}`, `{% block sidebar %}{% endblock %}`. Navigation — `<nav><ul><li><a href="/">Home</a></li>...`. Remember: an empty `{% block %}` leaves a blank spot that descendants fill.

### Hint 2
The macro receives a post dict: `{% macro post_card(post) %}` and uses `post.title`, `post.date`, `post.text`, `post.id`. Import in `index.html`: `{% from "macros.html" import post_card %}`.

### Hint 3
In `post.html`, start with `{% extends "base.html" %}`. In `base.html`, inside `<aside>` place `{% include "partials/sidebar.html" %}`. For 404: `if item is None: return "Post not found", 404`.

### Hint 4
`validate_contact` returns the dict `{"name": "...", "email": "...", "message": "..."}` only for fields with errors. On success — `if not errors:` return "Message sent!". In the template: `{% for field, msg in errors.items() %}<p class="error">{{ field }}: {{ msg }}</p>{% endfor %}`.

### Hint 5
For tests define a fixture: `env = Environment(loader=FileSystemLoader("templates"), autoescape=True)`. To check "three cards": `len(soup.find_all("article", class_="card")) == 3`. For styles, read `static/style.css` and use `assert` with substrings.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My notes{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <nav aria-label="Main menu">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/contact">Contacts</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <aside>
        {% block sidebar %}{% endblock %}
    </aside>

    <footer>
        <p>© 2026, My notes</p>
    </footer>
</body>
</html>
```

What is happening here? This is the skeleton of the whole site: a header with navigation, a main area with a `content` block, a side panel with a `sidebar` block, and a footer. Child templates fill only the blocks, while the design and navigation are reused automatically. `meta viewport` and the style link live in one place — no need to repeat them on every page.

### Solution 2
`templates/macros.html`:

```html
{% macro post_card(post) %}
    <article class="card">
        <h3>{{ post.title }}</h3>
        <time datetime="{{ post.date }}">{{ post.date }}</time>
        <p>{{ post.text|truncate(80) }}</p>
        <a href="/post/{{ post.id }}">Read</a>
    </article>
{% endmacro %}
```

`templates/index.html`:

```html
{% extends "base.html" %}
{% from "macros.html" import post_card %}

{% block title %}Home{% endblock %}

{% block content %}
    <h1>My notes</h1>
    <div class="cards">
        {% for post in posts %}
            {{ post_card(post) }}
        {% endfor %}
    </div>
{% endblock %}
```

`render_index.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
posts = [
    {"id": 1, "title": "Why HTML matters",
     "date": "2026-10-15", "text": "Semantics is the foundation."},
    {"id": 2, "title": "Flexbox vs. Grid",
     "date": "2026-10-20", "text": "Choosing the right tool."},
]
print(env.get_template("index.html").render(posts=posts))
```

What is happening here? The macro encapsulates the card markup. `|truncate(80)` cuts long post text. In `index.html`, the loop goes over `posts` and calls the macro — two posts give two cards. Changing the card's design happens in one place — in the macro.

### Solution 3
`templates/post.html`:

```html
{% extends "base.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
    <article>
        <h1>{{ post.title }}</h1>
        <time datetime="{{ post.date }}">{{ post.date }}</time>
        <p>{{ post.text }}</p>
    </article>
{% endblock %}
```

`templates/partials/sidebar.html`:

```html
<h2>Recent notes</h2>
<ul>
    <li><a href="/post/1">Why HTML matters</a></li>
    <li><a href="/post/2">Flexbox vs. Grid</a></li>
    <li><a href="/post/3">Jinja2 macros</a></li>
</ul>
```

In `base.html`, inside `<aside>`: `{% include "partials/sidebar.html" %}`.

`app.py`:

```python
from flask import Flask, render_template

app = Flask(__name__)

POSTS = [
    {"id": 1, "title": "Why HTML matters",
     "date": "2026-10-15", "text": "Semantics is the foundation."},
    {"id": 2, "title": "Flexbox vs. Grid",
     "date": "2026-10-20", "text": "Choosing the right tool."},
    {"id": 3, "title": "Jinja2 macros",
     "date": "2026-10-25", "text": "Reusing markup."},
]

def get_post(post_id):
    return next((p for p in POSTS if p["id"] == post_id), None)

@app.route("/")
def index():
    return render_template("index.html", posts=POSTS)

@app.route("/post/<int:post_id>")
def post(post_id):
    item = get_post(post_id)
    if item is None:
        return "Post not found", 404
    return render_template("post.html", post=item)
```

What is happening here? `include` puts the side panel into all pages. The `/post/<int:post_id>` route takes a number from the URL; `get_post` looks up the post, and if it's missing — a 404 is returned. That's how the simplest "database" on a list of dicts works.

### Solution 4
`templates/contact.html` (fragment):

```html
{% extends "base.html" %}

{% block title %}Contacts{% endblock %}

{% block content %}
    <h1>Feedback</h1>
    {% for field, msg in errors.items() %}
        <p class="error">{{ field }}: {{ msg }}</p>
    {% endfor %}
    <form action="/contact" method="post">
        <label for="name">Name</label>
        <input id="name" name="name" type="text" required minlength="2"
               value="{{ data.get('name', '') }}">
        <label for="email">Email</label>
        <input id="email" name="email" type="email" required
               value="{{ data.get('email', '') }}">
        <label for="message">Message</label>
        <textarea id="message" name="message" required minlength="10">{{ data.get('message', '') }}</textarea>
        <button type="submit">Send</button>
    </form>
{% endblock %}
```

`app.py` is extended:

```python
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        errors = validate_contact(request.form)
        if not errors:
            return "Message sent!"
        return render_template("contact.html", errors=errors,
                               data=request.form)
    return render_template("contact.html", errors={}, data={})

def validate_contact(data):
    errors = {}
    if len(data.get("name", "").strip()) < 2:
        errors["name"] = "The name must be at least 2 characters long."
    if "@" not in data.get("email", ""):
        errors["email"] = "Please enter a valid email."
    if len(data.get("message", "").strip()) < 10:
        errors["message"] = "The message must be at least 10 characters long."
    return errors
```

`tests/test_validation.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

from app import validate_contact

@pytest.mark.parametrize("data, expected", [
    ({}, {"name", "email", "message"}),
    ({"name": "A", "email": "a@b.ru", "message": "x" * 10}, {"name"}),
    ({"name": "Anna", "email": "no", "message": "x" * 10}, {"email"}),
    ({"name": "Anna", "email": "a@b.ru", "message": "short"},
     {"message"}),
    ({"name": "Anna", "email": "a@b.ru", "message": "x" * 20}, set()),
])
def test_validate_contact(data, expected):
    assert set(validate_contact(data)) == expected


def test_contact_template_renders_errors():
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    html = env.get_template("contact.html").render(
        errors={"email": "Please enter a valid email."}, data={})
    soup = BeautifulSoup(html, "html.parser")
    error = soup.find("p", class_="error")
    assert error is not None
    assert "Please enter a valid email." in error.get_text()
```

What is happening here? Validation checks three fields and returns an error dict. The parametrized test covers five scenarios. The render test confirms the error appears in `<p class="error">`. The `data` values are put back into the fields — the user doesn't lose their input.

### Solution 5
`tests/test_site.py`:

```python
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def make_env():
    return Environment(loader=FileSystemLoader("templates"), autoescape=True)


def render(template_name, env=None, **context):
    env = env or make_env()
    return env.get_template(template_name).render(**context)


POSTS = [
    {"id": 1, "title": "A", "date": "2026-10-15", "text": "x" * 10},
    {"id": 2, "title": "B", "date": "2026-10-20", "text": "x" * 10},
    {"id": 3, "title": "C", "date": "2026-10-25", "text": "x" * 10},
]


def test_index_structure():
    soup = BeautifulSoup(render("index.html", posts=POSTS), "html.parser")
    assert soup.find("header") and soup.find("nav")
    assert soup.find("main") and soup.find("footer")
    assert len(soup.find("nav").find_all("a")) == 2
    cards = soup.find_all("article", class_="card")
    assert len(cards) == 3
    for card in cards:
        assert card.find("time") is not None
        link = card.find("a", string="Read")
        assert link is not None and link["href"].startswith("/post/")


def test_post_page():
    soup = BeautifulSoup(render("post.html", post=POSTS[0]), "html.parser")
    main = soup.find("main")
    assert main.find("article") is not None
    assert main.find("h1").get_text() == "A"


def test_head_meta_and_styles():
    soup = BeautifulSoup(render("index.html", posts=POSTS), "html.parser")
    assert soup.find("link", rel="stylesheet", href="/static/style.css")
    viewport = soup.find("meta", attrs={"name": "viewport"})
    assert viewport is not None


def test_contact_form():
    soup = BeautifulSoup(render("contact.html", errors={}, data={}),
                         "html.parser")
    form = soup.find("form")
    assert form["method"] == "post" and form["action"] == "/contact"
    for name in ("name", "email", "message"):
        field = soup.find(attrs={"name": name})
        assert field.get("required") is not None
        label = soup.find("label", attrs={"for": field["id"]})
        assert label is not None


def test_css_has_modern_features():
    with open("static/style.css", encoding="utf-8") as f:
        css = f.read()
    assert ":root" in css and "--color-" in css
    assert "display: grid" in css and "display: flex" in css
    assert "@media" in css
```

What is happening here? The integration test renders the real templates and checks everything at once: the skeleton is present, navigation has two links, there are exactly three cards and each leads to its page, the post renders with its title, styles are linked, the form is structured correctly, and the CSS uses modern features. Run: `python -m pytest tests/`. A green result means the site is assembled correctly — from markup to styles.
<!--/SOLUTION-->

<!--QUIZ-->
Which block in base.html does the post page fill?
- content
- footer
- title
- content and title
* Correct answer: content and title
The post defines both the tab title (title) and the content (content).

What does {% include "partials/sidebar.html" %} do?
- Inserts the panel into all pages that inherit base.html
- Creates a new file
- Overrides a block
* Correct answer: Inserts the panel into all pages that inherit base.html
include inserts a template fragment at the call site.

What does route /post/999 return if there is no post with id 999?
- "Post not found" with status 404
- An empty page
- The home page
* Correct answer: "Post not found" with status 404
The correct answer to a missing resource is 404.

What is the post_card macro for?
- To reuse the post card markup
- To store post data
- To include CSS
* Correct answer: To reuse the post card markup
The macro describes the card once and is called for each post.

What happens if you submit the form with an empty message?
- The server returns a validation error and shows the form again
- The data is saved
- The page refreshes
* Correct answer: The server returns a validation error and shows the form again
Server-side validation catches the empty message and shows an error.

Which file contains all the project styles?
- static/style.css
- templates/style.css
- style.html
* Correct answer: static/style.css
Static files (styles, scripts) live in the static folder.

What does the integration test check?
- That all pages render correctly: skeleton, cards, form, styles
- Only Python code
- Only CSS
* Correct answer: That all pages render correctly: skeleton, cards, form, styles
The integration test checks the assembled site as a whole.

Why use Jinja2 in the project instead of manual HTML?
- So pages are assembled from data and a common skeleton
- To speed up the browser
- To write less CSS
* Correct answer: So pages are assembled from data and a common skeleton
A template engine eliminates duplication and fills pages with data.

What happens if you remove block content from base.html?
- Child pages won't be able to insert their content
- Nothing changes
- The site stops loading
* Correct answer: Child pages won't be able to insert their content
Without the block, descendants can't fill the main area.

What are "static files"?
- CSS and JS served to the browser as-is
- Jinja2 templates
- Python modules
* Correct answer: CSS and JS served to the browser as-is
Static assets aren't processed by the server and are served directly.
<!--/QUIZ-->
