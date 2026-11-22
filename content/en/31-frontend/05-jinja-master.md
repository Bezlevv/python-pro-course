---
title: Jinja2 mastery: inheritance, macros, filters
summary: The Jinja2 template engine: variables, filters, inheritance via extends/block, include, macros, and autoescape.
order: 5
duration: 50 min
difficulty: advanced
tags: jinja2, templates, flask, macros, filters
---

You've already written HTML by hand. But in real web applications, pages are assembled from data: a product list, a user profile, a news feed. For that you need a **template engine** — a tool that fills an HTML skeleton with data. The most popular one in the Python world is **Jinja2**.

## The first template

The `jinja2` library is a Python package. Minimal example:

```python
from jinja2 import Template

template = Template("Hello, {{ name }}!")
print(template.render(name="Anna"))  # Hello, Anna!
```

Jinja2 syntax:

- `{{ expression }}` — output a value;
- `{% statement %}` — logic: conditions, loops, inheritance;
- `{# comment #}` — a comment, not included in the output.

Inside `{{ }}` you can use almost any Python expression: arithmetic, method calls, list and dict access. `{{ user.name }}` and `{{ user["name"] }}` are equivalent.

## Conditions and loops

```python
template = Template("""
{% for item in items %}
    {{ loop.index }}. {{ item }}
{% endfor %}
{% if items|length == 0 %}
    The list is empty.
{% endif %}
""")
print(template.render(items=["Python", "Jinja2"]))
```

The `loop` variable is available inside loops: `loop.index` (from 1), `loop.index0` (from 0), `loop.first`, `loop.last`.

## Filters

Filters are applied with `|` and transform values. Main ones:

- `{{ name|upper }}` — uppercase; also `lower`, `capitalize`, `title`;
- `{{ items|join(", ") }}` — joins a list;
- `{{ items|length }}` — length;
- `{{ value|default("no value") }}` — default value (for `False` use `default("...", boolean=True)`);
- `{{ price|round(2) }}` — rounding;
- `{{ text|truncate(50) }}` — truncates text;
- `{{ text|e }}` / `{{ text|safe }}` — escaping and "raw" output.

```python
from jinja2 import Template

t = Template("Total: {{ total|round(2) }} ₽")
print(t.render(total=1234.5678))  # Total: 1234.57 ₽
```

## autoescape: security by default

By default, in `jinja2.Template` **autoescape is disabled** — output is not escaped. That means if user-provided HTML lands in a template, it will "come alive". In Flask, autoescape is enabled for `.html` templates, but if you create templates by hand — enable it yourself:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
t = env.from_string("{{ user_input }}")
print(t.render(user_input="<script>alert(1)</script>"))
# &lt;script&gt;alert(1)&lt;/script&gt;
```

Rule: **never mark user input as `|safe`**. `|safe` is only for trusted HTML (e.g., markup you wrote).

## Inheritance: extends and block

Inheritance is Jinja2's flagship feature. You build a base template `base.html` with blocks, and child pages fill them:

```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Site{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Header{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}© 2026{% endblock %}</footer>
</body>
</html>
```

```html
<!-- page.html -->
{% extends "base.html" %}

{% block title %}About me{% endblock %}

{% block content %}
    <h1>About me</h1>
    <p>Hi! My name is Anna.</p>
{% endblock %}
```

If a child template doesn't override a block, the parent's content remains. And `{{ super() }}` inserts the parent content inside the overridden block. A child template **must** start with `{% extends %}`.

## include and macros

`{% include "partials/footer.html" %}` inserts another template's content — convenient for reusable pieces (cards, buttons). Even more powerful are **macros**: functions inside templates:

```html
{% macro card(title, text) %}
    <article class="card">
        <h3>{{ title }}</h3>
        <p>{{ text }}</p>
    </article>
{% endmacro %}
```

Usage:

```html
{{ card("Project 1", "Description of the first project") }}
{{ card("Project 2", "Description of the second project") }}
```

Macros can be stored in a separate file and imported via `{% import "macros.html" as ui %}` or `{% from "macros.html" import card %}`. Macros can have default values: `{% macro card(title, text="") %}`.

## Environment and FileSystemLoader

In a real project, templates live in a folder. `Environment` with `FileSystemLoader` loads them:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
template = env.get_template("page.html")
print(template.render(user="Anna"))
```

That's exactly what Flask does: it creates a Jinja2 environment for the `templates/` folder with autoescape enabled.

## Whitespace and output control

Service tags can be "tightened" against text: `{%-` and `-%}` strip surrounding whitespace and newlines. Handy when you need to output items in one line without extra spaces.

Now let's put it all together: you'll build inheritance, write macros, master escaping, and cover everything with tests.

<!--TASK-->
### Task 1
Write a script `basics.py` that creates an `Environment(autoescape=True)` and renders a string template:

```
Hello, {{ name|capitalize }}! Today is {{ day }}.
You have {{ tasks|length }} tasks: {{ tasks|join(", ") }}.
```

Pass `name="anya"`, `day="Saturday"`, `tasks=["Python", "CSS", "Jinja2"]`. Print the result. Expected result:

```
Hello, Anya! Today is Saturday.
You have 3 tasks: Python, CSS, Jinja2.
```

### Task 2
Create a `templates/` folder with two templates: `base.html` and `about.html`. In `base.html` — a page skeleton with `title` and `content` blocks. In `about.html` — `{% extends "base.html" %}`, override `title` to "About me" and `content` to a paragraph about yourself. Then write a script `render_about.py` that renders `about.html` via `Environment(loader=FileSystemLoader("templates"), autoescape=True)` and prints the result. Additionally, write a pytest test `test_extends.py`: check with `BeautifulSoup` that the rendered HTML contains `<title>About me</title>`, the `content` block's content, and the skeleton from `base.html` (`<main>`, `<footer>`). Expected result: the page is assembled from two templates.

### Task 3
Create `templates/macros.html` with a `card(title, text)` macro (a card: `<article class="card">` with `<h3>` and `<p>`). Then create a `gallery.html` template that imports the macro via `{% from "macros.html" import card %}` and, in a `{% for post in posts %}` loop, outputs `{{ card(post.title, post.text) }}`. Write a script that renders `gallery.html` with a list of three posts and prints the HTML. Expected result: the output has three cards, each with a title and text.

### Task 4
Create two scripts that demonstrate the difference in escaping. The first — `unsafe.py`: the template `{{ user_input }}` with `Environment(autoescape=False)` renders `<img src=x onerror=alert(1)>` — print the result. The second — `safe.py`: the same template, but with `Environment(autoescape=True)`; print the result. Then modify `safe.py`: add the `|safe` filter to the output and print again. Expected result: in the first case — a raw HTML tag; in the second — an escaped sequence (`&lt;img ...&gt;`); in the third — the raw tag again. In a comment in the code, explain why the `|safe` variant is dangerous for user input.

### Task 5
Write a test file `test_jinja.py` (use pytest) that checks:

- **Macro**: render a template with the `card` macro for a list of two posts and check with `BeautifulSoup` that the HTML has exactly two `<article class="card">`, each with an `<h3>` containing the title;
- **Inheritance**: render `about.html` and check that `title` is "About me" and `<main>` contains an `<h1>`;
- **Autoescape**: render `{{ value }}` with `Environment(autoescape=True)` and the value `<script>alert(1)</script>`, check that the HTML has no `<script>` tag (no `<script>` substring) but has `&lt;script&gt;`;
- **Filters**: render `{{ text|truncate(10) }}` with a long text and check that the result is shorter than the original and ends with `...`.

Expected result: all tests pass; run with `python -m pytest test_jinja.py`.
<!--/TASK-->

<!--HINT-->
### Hint 1
`Environment(autoescape=True)` creates the environment. A string template — via `Environment.from_string("...")` or simply `Template("...")` from `jinja2`. Filters are written with `|`: `{{ name|capitalize }}`.

### Hint 2
Base template with blocks: `{% block title %}...{% endblock %}`. The child starts with `{% extends "base.html" %}`. Loader: `Environment(loader=FileSystemLoader("templates"), autoescape=True)`; `env.get_template("about.html").render()`.

### Hint 3
A macro is declared `{% macro card(title, text) %}...{% endmacro %}`. Import: `{% from "macros.html" import card %}`. In the `{% for post in posts %}` loop call `{{ card(post.title, post.text) }}`. Pass `posts=[{"title": ..., "text": ...}, ...]` to `render()`.

### Hint 4
By default `Environment(autoescape=False)`. Enabling: `Environment(autoescape=True)`. Check the output with your eyes: a raw tag versus `&lt;...&gt;`. `|safe` disables escaping for a specific value.

### Hint 5
For tests, reuse `Environment(loader=FileSystemLoader("templates"), autoescape=True)`. A nice trick is a fixture: `@pytest.fixture` returns the environment. To check cards: `soup.find_all("article", class_="card")`. For autoescaping: `assert "<script>" not in html`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
`basics.py`:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
template = env.from_string(
    "Hello, {{ name|capitalize }}! Today is {{ day }}.\n"
    "You have {{ tasks|length }} tasks: {{ tasks|join(', ') }}."
)
result = template.render(
    name="anya", day="Saturday", tasks=["Python", "CSS", "Jinja2"],
)
print(result)
```

Output:

```
Hello, Anya! Today is Saturday.
You have 3 tasks: Python, CSS, Jinja2.
```

What is happening here? `env.from_string()` turns a string into a template. `{{ name|capitalize }}` capitalizes the first letter; `{{ tasks|length }}` counts the list items; `{{ tasks|join(', ') }}` joins the list with a comma and a space. `Environment(autoescape=True)` is on from the start — get used to the safe mode.

### Solution 2
`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Site{% endblock %}</title>
</head>
<body>
    <header>{% block header %}Header{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}© 2026{% endblock %}</footer>
</body>
</html>
```

`templates/about.html`:

```html
{% extends "base.html" %}

{% block title %}About me{% endblock %}

{% block content %}
    <h1>About me</h1>
    <p>Hi! My name is Anna.</p>
{% endblock %}
```

`render_about.py`:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
print(env.get_template("about.html").render())
```

`test_extends.py`:

```python
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def render_about():
    env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
    return env.get_template("about.html").render()


def test_title_and_content_blocks():
    html = render_about()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.title.get_text() == "About me"
    main = soup.find("main")
    assert main.find("h1").get_text() == "About me"
    assert main.find("p") is not None


def test_base_frame_present():
    html = render_about()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("footer") is not None
    assert soup.find("header") is not None
```

What is happening here? `about.html` inherits the `base.html` skeleton: the `title` and `content` blocks are overridden, while `header` and `footer` remain parent ones. The tests confirm that the assembled page contains both the overridden blocks and the base skeleton. That's how inheritance works: no duplicated work, each page defines only what is its own.

### Solution 3
`templates/macros.html`:

```html
{% macro card(title, text) %}
    <article class="card">
        <h3>{{ title }}</h3>
        <p>{{ text }}</p>
    </article>
{% endmacro %}
```

`templates/gallery.html`:

```html
{% from "macros.html" import card %}
<div class="gallery">
    {% for post in posts %}
        {{ card(post.title, post.text) }}
    {% endfor %}
</div>
```

Script:

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
posts = [
    {"title": "Python 3.13", "text": "New release"},
    {"title": "Jinja2", "text": "Template engine"},
    {"title": "Grid", "text": "Responsive grid"},
]
print(env.get_template("gallery.html").render(posts=posts))
```

What is happening here? The `card` macro is a "function" inside the template: declared once, called as many times as needed. `{% from "macros.html" import card %}` pulls it in from a separate file — macros can be reused across all pages. The `{% for post in posts %}` loop goes over the post list and calls the macro for each. The result is clean, repeatable markup without copy-paste.

### Solution 4
`unsafe.py`:

```python
from jinja2 import Environment

env = Environment()  # autoescape is disabled by default
print(env.from_string("{{ user_input }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
```

Output: the raw tag `<img src=x onerror=alert(1)>` — the browser will execute it.

`safe.py`:

```python
from jinja2 import Environment

env = Environment(autoescape=True)
print(env.from_string("{{ user_input }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
# &lt;img src=x onerror=alert(1)&gt;

print(env.from_string("{{ user_input|safe }}").render(
    user_input="<img src=x onerror=alert(1)>",
))
# <img src=x onerror=alert(1)>
```

What is happening here? With `autoescape=True`, special characters turn into safe entities: `<` → `&lt;`, `>` → `&gt;` — and the browser shows them as text. The `|safe` filter disables escaping and returns raw HTML. If you apply it to user input, an attacker can inject their script (XSS). Takeaway: `|safe` is only for trusted HTML.

### Solution 5
`test_jinja.py`:

```python
import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader("templates"), autoescape=True)


def test_macro_renders_cards(env):
    template = env.get_template("gallery.html")
    html = template.render(posts=[
        {"title": "A", "text": "1"},
        {"title": "B", "text": "2"},
    ])
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("article", class_="card")
    assert len(cards) == 2
    assert cards[0].find("h3").get_text() == "A"
    assert cards[1].find("p").get_text() == "2"


def test_inheritance(env):
    html = env.get_template("about.html").render()
    soup = BeautifulSoup(html, "html.parser")
    assert soup.title.get_text() == "About me"
    assert soup.find("main").find("h1") is not None


def test_autoescape_prevents_xss(env):
    html = env.from_string("{{ value }}").render(
        value="<script>alert(1)</script>")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_truncate_filter(env):
    html = env.from_string("{{ text|truncate(10) }}").render(
        text="A very long sentence of text")
    result = html.strip()
    assert len(result) < len("A very long sentence of text")
    assert result.endswith("...")
```

What is happening here? The `env` fixture creates an environment with a loader and autoescape — tests don't duplicate code. The macro check counts cards and looks inside each one. The autoescape test guarantees the main thing: a foreign script will not get into the page. The `truncate` test verifies that a long text is cut off and ends with an ellipsis. All four tests run with `python -m pytest test_jinja.py`.
<!--/SOLUTION-->

<!--QUIZ-->
What do double curly braces {{ }} mean in Jinja2?
- Output the value of an expression
- A comment
- A logic operator
* Correct answer: Output the value of an expression
{{ expression }} outputs the result into HTML.

What is the template inheritance operator called?
- {% extend %}
- {% extends %}
- {% include %}
* Correct answer: {% extends %}
{% extends "base.html" %} inherits from a base template, and it must be the first line.

What does the {% block content %} block do?
- Defines a place a child template can fill
- Comments out code
- Includes a file
* Correct answer: Defines a place a child template can fill
Blocks are "holes" in the base template that descendants override.

Which filter capitalizes the first letter?
- upper
- capitalize
- title (per word)
- Choose all that apply
* Correct answer: capitalize
capitalize makes the first letter of the string uppercase; title does it for every word.

What does {{ super() }} do?
- Inserts the parent block's content
- Calls a function
- Removes a block
* Correct answer: Inserts the parent block's content
super() lets you extend the parent block without losing its content.

What is a macro in Jinja2?
- A function inside a template — a reusable markup fragment
- A built-in filter
- A data type
* Correct answer: A function inside a template — a reusable markup fragment
Macros are declared with {% macro %} and called like functions.

What does the |join(", ") filter do?
- Joins list items with a comma and a space
- Adds items to a list
- Sorts a list
* Correct answer: Joins list items with a comma and a space
join turns a list into a string with the given separator.

What does autoescape=True do?
- Enables output escaping — HTML tags in data become safe text
- Disables type checks
- Speeds up rendering
* Correct answer: Enables output escaping — HTML tags in data become safe text
autoescape turns special characters into entities, neutralizing XSS.

When can you use the |safe filter?
- Only for trusted HTML, never for user input
- For any input
- Never
* Correct answer: Only for trusted HTML, never for user input
|safe disables escaping — on user input it's a vulnerability.

What does {% include %} do?
- Inserts another template's content at the current place
- Inherits a template
- Imports macros
* Correct answer: Inserts another template's content at the current place
include plugs a ready fragment (e.g., a footer) into a template.
<!--/QUIZ-->
