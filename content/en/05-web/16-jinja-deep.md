---
title: Jinja2 in depth: inheritance, macros, filters
summary: extends/block, include, macros, custom filters, whitespace control, autoescape.
order: 16
duration: 50 min
difficulty: advanced
tags: jinja2, flask, templates, macros
---

Beyond basics, Jinja2 supports inheritance, macros and custom filters.

## Inheritance

`base.html`:
```html
<html><body>
{% block content %}{% endblock %}
</body></html>
```
child:
```html
{% extends "base.html" %}
{% block content %}<h1>Hi</h1>{% endblock %}
```

## Include

```html
{% include "header.html" %}
```

## Macros

```html
{% macro input(name) %}
  <input name="{{ name }}">
{% endmacro %}
{{ input("email") }}
```

## Custom filter

```python
from flask import Flask
app = Flask(__name__)

@app.template_filter("upper")
def upper_filter(s):
    return s.upper()
```

## Autoescape

Django/Flask autoescape by default: `{{ value }}` escapes HTML.

## Whitespace control

`{%- ... -%}` trims whitespace.

## Lesson summary

Inheritance, include, macros and filters make templates maintainable.

<!--TASK-->
### Task 1 — Base and child
Create base.html with a block; extend it in child.

### Task 2 — Include
Include a partial header.

### Task 3 — Macro
Define a macro for inputs and use it twice.

### Task 4 — Custom filter
Register a "shout" filter and use it.

### Task 5 — Loop in template
Render a list with a for loop.

### Task 6 — Filters chain
Use |upper|length in a template.

### Task 7 — Autoescape
Show the difference between {{ value }} and |safe.
<!--/TASK-->

<!--HINT-->
### Hint 1
{% block content %}.

### Hint 2
{% include %}.

### Hint 3
{% macro name(...) %}.

### Hint 4
@app.template_filter("shout").

### Hint 5
{% for x in xs %}.

### Hint 6
{{ s|upper|length }}.

### Hint 7
|safe disables escaping.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
base.html:
```html
<html><body>
{% block content %}{% endblock %}
</body></html>
```
child:
```html
{% extends "base.html" %}
{% block content %}<h1>Hi</h1>{% endblock %}
```

### Solution 2
```html
{% include "header.html" %}
```

### Solution 3
```html
{% macro input(name) %}
  <input name="{{ name }}">
{% endmacro %}
{{ input("email") }}
{{ input("name") }}
```

### Solution 4
```python
@app.template_filter("shout")
def shout(s):
    return s.upper() + "!"
```
```html
{{ "hi"|shout }}   <!-- HI! -->
```

### Solution 5
```html
{% for item in items %}
  <p>{{ item }}</p>
{% endfor %}
```

### Solution 6
```html
{{ "python"|upper|length }}   <!-- 6 -->
```

### Solution 7
```html
{{ value }}   <!-- экранирует <script> -->
{{ value|safe }}  <!-- опасно -->
```
<!--/SOLUTION-->

<!--QUIZ-->
What does {% extends %} do?
- Inherits a base template
- Includes
- Imports
- Loops
* Correct answer: Inherits a base template
Base layout.

What is {% block %}?
- A fillable slot
- A loop
- A macro
- A filter
* Correct answer: A fillable slot
Overridden.

What does {% include %} do?
- Inserts a template
- Extends
- Defines
- Loops
* Correct answer: Inserts a template
Partial.

What is a macro?
- Reusable snippet
- A filter
- A block
- A loop
* Correct answer: Reusable snippet
Callable.

How to call a macro?
- {{ macro_name(args) }}
- {% macro %}
- {{ block }}
- {% call %}
* Correct answer: {{ macro_name(args) }}
Output.

What is a custom filter?
- A Python function in templates
- A block
- A macro
- A loop
* Correct answer: A Python function in templates
Registered.

How to register a filter?
- @app.template_filter("name")
- @filter
- add_filter()
- jinja.filter
* Correct answer: @app.template_filter("name")
Decorator.

What is autoescape?
- HTML escaping by default
- Disabled
- Forced
- None
* Correct answer: HTML escaping by default
Safety.

What does |safe do?
- Marks as safe HTML
- Escapes
- Deletes
- Sorts
* Correct answer: Marks as safe HTML
No escaping.

What is {%- -%}?
- Whitespace trim
- Loop
- Comment
- Filter
* Correct answer: Whitespace trim
Clean output.

Why use macros?
- DRY
- Faster
- Required
- Styling
* Correct answer: DRY
Reuse.

Can filters chain?
- Yes
- No
- Once
- Two max
* Correct answer: Yes
|a|b.
<!--/QUIZ-->
