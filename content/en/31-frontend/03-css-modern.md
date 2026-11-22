---
title: Modern CSS: variables, transitions, animations
summary: CSS variables, cascade and specificity, transition, keyframes animations, and media queries.
order: 3
duration: 45 min
difficulty: intermediate
tags: css, variables, animations, transition, media queries
---

CSS (Cascading Style Sheets) controls the page's appearance. In this lesson you'll move from "paint some text" to truly modern styling: variables that let you change the whole site theme with one line, smooth transitions, and animations.

## Selectors and specificity

Styles are applied via **selectors**: tags (`.h1`), classes (`.card`), ids (`#header`), attributes (`[type="email"]`), pseudo-classes (`:hover`, `:focus`, `:nth-child(2)`), and pseudo-elements (`::before`, `::after`).

Specificity decides which rule wins on conflict: id (strongest) > classes and attributes > tags. A useful rule: use classes, not ids, so styles are easier to reuse.

```css
.card { /* class — base level */
    background: #fff;
}
.card:hover { /* ":hover" — on hover */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

## CSS variables (custom properties)

Variables are declared inside `:root` (the root element's pseudo-class — `html`) and used via `var()`:

```css
:root {
    --color-primary: #3465e4;
    --color-text: #1f2430;
    --space: 8px;
}

.card {
    background: var(--color-primary);
    color: var(--color-text);
    padding: calc(var(--space) * 2);
}
```

Why bother? Declare a color once — and you change the whole site theme in one place: `--color-primary: #e4345c`. `calc()` computes values on the fly, e.g., `calc(100% - 40px)`.

## State pseudo-classes

- `:hover` — mouse over;
- `:focus` — element focused (keyboard);
- `:focus-visible` — focus visible to the user (modern standard);
- `:active` — moment of clicking;
- `:nth-child(n)` — ordinal position among siblings.

Important: there is no `:hover` state on phones, and `:focus` is the most important accessibility signal. Never remove focus outlines entirely (`outline: none` without a replacement) — that breaks keyboard navigation.

## Transitions

`transition` smoothly animates property changes between states. Shorthand: `transition: property duration timing-function delay`.

```css
.btn {
    background: var(--color-primary);
    transition: background 0.3s ease, transform 0.3s ease;
}
.btn:hover {
    background: #1e3f8f;
    transform: translateY(-2px);
}
```

Animate only properties the browser can animate cheaply: `transform`, `opacity`, colors, `box-shadow`. Don't animate `width` and `height` — it's jerky and slow.

## keyframes animations

If a transition is a reaction to an action, `@keyframes` is a scenario that runs on its own. You declare frames and attach them via `animation`:

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.hero-title {
    animation: fadeInUp 0.8s ease-out both;
}
```

`both` at the end means: before the start and after the end of the animation, the `from`/`to` frames apply (the element doesn't "jump").

## Media queries

`@media` applies styles when a condition is met — screen size, orientation, user settings:

```css
/* Base styles — for everyone */

@media (max-width: 600px) {
    .hero-title {
        font-size: 28px;
    }
    .sidebar { display: none; }
}

/* System dark theme */
@media (prefers-color-scheme: dark) {
    :root {
        --color-text: #e8eaf0;
    }
}

/* User asked for less motion */
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

Rule: **base styles first, then `@media`**. `prefers-reduced-motion` is mandatory courtesy: we disable animations for people with vestibular disorders.

## Order of work

1. Structure and variables — `:root`.
2. Base element styles.
3. Component styling with classes.
4. States (`:hover`, `:focus-visible`).
5. Transitions and animations.
6. Media queries at the end.

Now let's solidify: you'll build a page with variables, smooth buttons, animation, and responsiveness, then write tests that verify the styles themselves and their connection to HTML.

<!--TASK-->
### Task 1
Create a `css-project/` folder with `index.html` and `style.css` inside. In `style.css`, declare variables in `:root`: `--color-primary: #3465e4`, `--color-secondary: #2a9d8f`, `--color-background: #f5f7fa`, `--color-text: #1f2430`, `--radius: 12px`. Then style a simple page: a card (`.card` class) with a white background, `var(--radius)` rounding, and a border; a heading colored `var(--color-primary)`; a button (`.btn` class) with a `var(--color-primary)` background. Link `style.css` in `index.html` via `<link rel="stylesheet" href="style.css">`. Open in a browser — the colors must match the variables.

### Task 2
Add hover effects. Give the button:

- a smooth transition `transition: background 0.3s ease, transform 0.3s ease`;
- on `:hover` — a darker background (e.g., `#1e3f8f`) and a lift `transform: translateY(-2px)`;
- on `:focus-visible` — a visible ring `outline: 3px solid #ffb703; outline-offset: 2px;`.

Give the card a shadow on hover and a shadow transition. Check: on hover and when moving through the page with `Tab`, everything should change smoothly.

### Task 3
Create a banner at the top of the page (`.hero` class) with a heading (`.hero-title` class) and a subtitle. Add an entrance animation:

- `@keyframes fadeInUp` — from `opacity: 0; transform: translateY(20px)` to `opacity: 1; transform: translateY(0)`;
- the heading and subtitle get `animation: fadeInUp 0.8s ease-out both`, with the subtitle delayed by `animation-delay: 0.2s`.

Also add `@media (prefers-reduced-motion: reduce)` that almost completely disables animations and transitions.

### Task 4
Make the page responsive: add media queries:

- at `max-width: 600px`, reduce the heading font size to `26px` and hide the side column (`.sidebar` class; add it to the HTML with any text);
- at `prefers-color-scheme: dark`, override `--color-background` to `#16181d`, `--color-text` to `#e8eaf0`, `--color-primary` to `#6b9aff`.

Check in the browser: narrow the window to mobile size, turn on the system dark theme (if your browser supports it) — the page should react.

Then write a pytest test `test_responsive.py`: read `index.html`, render it via jinja2 (`env.from_string(html)`), parse with `BeautifulSoup`, and check that the page has an element with the `sidebar` class. After that, read `style.css` and check that it contains `@media (max-width: 600px)`, a `display: none` rule for `.sidebar`, and a `prefers-color-scheme: dark` block overriding the `--color-background` and `--color-text` variables. Expected result: all test checks pass.

### Task 5
Write pytest tests `test_css.py`:

- a `style.css` test: read the file as text and check for `:root`, at least three `--color-` variables, `var(` usage in rules, `transition` on `.btn`, `@keyframes fadeInUp`, and `@media`;
- a render test: render the `index.html` template via jinja2 (plain text without variables — you can read the file) and check with `BeautifulSoup` that the page has `<link rel="stylesheet" href="style.css">` and elements with the `card`, `btn`, and `hero-title` classes;
- a connection test: collect all classes from the CSS file (via the regular expression `\.([a-z-]+)\s*\{`) and verify that every class from the HTML (`card`, `btn`, `hero`, `hero-title`, `sidebar`) is present in the CSS.

Expected result: all three tests pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
Variables are declared as `--name: value;` inside `:root { ... }`, and used as `var(--name)`. In `index.html`, be sure to link the styles in `<head>`: `<link rel="stylesheet" href="style.css">`. Don't forget `<meta name="viewport" ...>`.

### Hint 2
`transition` is a shorthand: `transition: background 0.3s ease, transform 0.3s ease` combines property, duration, timing function, and delay. To avoid losing `:focus` when using a mouse, set `:focus-visible` separately from `:hover`. Shadow: `box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15)`.

### Hint 3
Key frames: `@keyframes fadeInUp { from { ... } to { ... } }`. Attach with `animation: fadeInUp 0.8s ease-out both`. For the second element add `animation-delay: 0.2s` — and be sure to include `animation-fill-mode: both` (otherwise the element is visible before the start).

### Hint 4
Write media queries after the main rules. Syntax: `@media (max-width: 600px) { ... }`. For the dark theme: `@media (prefers-color-scheme: dark) { :root { --color-background: #16181d; } }`. For the test: `env.from_string(html).render()` returns the same string — that's rendering through jinja2; then work with BeautifulSoup. Check `display: none` for `.sidebar` by CSS: find the `@media (max-width: 600px)` block and make sure `.sidebar { display: none; }` is inside.

### Hint 5
Reading the file: `with open("style.css", encoding="utf-8") as f: css = f.read()`. Presence check: `assert ":root" in css`. Classes from CSS: `re.findall(r"\.([a-z-]+)\s*\{", css)`. For jinja2 rendering: `env = Environment(autoescape=True); template = env.from_string(html_text)` — or just parse `index.html` directly with BeautifulSoup.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
`style.css`:

```css
:root {
    --color-primary: #3465e4;
    --color-secondary: #2a9d8f;
    --color-background: #f5f7fa;
    --color-text: #1f2430;
    --radius: 12px;
}

body {
    background: var(--color-background);
    color: var(--color-text);
    font-family: Arial, sans-serif;
}

.card {
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: var(--radius);
    padding: 24px;
}

h1, h2 { color: var(--color-primary); }

.btn {
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    padding: 12px 24px;
    cursor: pointer;
}
```

In `index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS project</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="card">
        <h1>Hello, CSS!</h1>
        <p>This is a card with variables.</p>
        <button class="btn">Click</button>
    </div>
</body>
</html>
```

What is happening here? All colors and the radius are declared in `:root` as variables, and elements use `var(...)`. Now, to change the whole palette, you only need to edit values in one place — `:root`. This approach is called "design tokens".

### Solution 2
Extending `style.css`:

```css
.btn {
    background: var(--color-primary);
    color: #fff;
    border: none;
    border-radius: var(--radius);
    padding: 12px 24px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
}
.btn:hover {
    background: #1e3f8f;
    transform: translateY(-2px);
}
.btn:focus-visible {
    outline: 3px solid #ffb703;
    outline-offset: 2px;
}
.card {
    background: #fff;
    border-radius: var(--radius);
    padding: 24px;
    transition: box-shadow 0.3s ease;
}
.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

What is happening here? `transition` describes what will change smoothly and for how long: the background and the shift over 0.3s. On `:hover`, the end values change and the browser animates the transition. `:focus-visible` fires only when focus really needs to be shown (e.g., keyboard navigation) — that's an accessibility requirement. The card's shadow also transitions smoothly because it has `transition: box-shadow` declared.

### Solution 3
Adding the banner and the animation:

```css
.hero {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: #fff;
    padding: 48px;
    border-radius: var(--radius);
}

.hero-title {
    font-size: 36px;
    margin: 0;
    animation: fadeInUp 0.8s ease-out both;
}
.hero-subtitle {
    animation: fadeInUp 0.8s ease-out 0.2s both;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        animation-delay: 0s !important;
        transition-duration: 0.01ms !important;
    }
}
```

What is happening here? `@keyframes fadeInUp` describes two frames: the start (transparent, shifted down) and the finish (visible, in place). `animation: fadeInUp 0.8s ease-out both` attaches the scenario; `both` (that is `animation-fill-mode: both`) applies the starting frame before the start and the final one after the end — the element doesn't blink. The subtitle has a `0.2s` delay, so it appears right after the heading. The `prefers-reduced-motion` media query shortens animations to milliseconds for users who disabled them in the system.

### Solution 4
Adding responsiveness:

```css
@media (max-width: 600px) {
    .hero-title { font-size: 26px; }
    .sidebar { display: none; }
}

@media (prefers-color-scheme: dark) {
    :root {
        --color-background: #16181d;
        --color-text: #e8eaf0;
        --color-primary: #6b9aff;
    }
}
```

`test_responsive.py`:

```python
import re
from bs4 import BeautifulSoup
from jinja2 import Environment


def render_index():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return Environment().from_string(html).render()


def test_has_sidebar_element():
    soup = BeautifulSoup(render_index(), "html.parser")
    assert soup.find(class_="sidebar") is not None


def test_media_queries_present():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    assert "@media (max-width: 600px)" in css
    assert "@media (prefers-color-scheme: dark)" in css
    assert "--color-background" in css and "--color-text" in css


def test_sidebar_hidden_on_mobile():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"@media \(max-width: 600px\)\s*\{([^}]*)\}", css)
    assert m is not None
    assert "display: none" in m.group(1)
    assert ".sidebar" in m.group(1)
```

What is happening here? The first test confirms that the `sidebar` class really exists in the HTML — so the media query has something to hide. The second checks for both media queries and the dark-theme variables. The third cuts out the body of the mobile media query with a regular expression and makes sure `.sidebar` is indeed hidden inside it via `display: none`. That verifies the CSS's "behavior", not just its existence.

Now let's break down the rest of the responsive task. On screens up to 600px, the heading shrinks and the side column hides — typical mobile behavior. And `prefers-color-scheme: dark` overrides variables when the system dark theme is on: the background turns dark, the text light, and the brand color lightens for contrast. The beauty of variables is that overriding them in `:root` automatically recolors every element that uses `var()`.

### Solution 5
`test_css.py`:

```python
import re
from bs4 import BeautifulSoup


def read_css():
    with open("style.css", encoding="utf-8") as f:
        return f.read()


def test_css_has_variables_and_keywords():
    css = read_css()
    assert ":root" in css
    assert len(re.findall(r"--color-[a-z-]+:", css)) >= 3
    assert "var(" in css
    assert "transition:" in css
    assert "@keyframes fadeInUp" in css
    assert "@media" in css


def test_html_links_css_and_has_classes():
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    link = soup.find("link", rel="stylesheet")
    assert link is not None and link.get("href") == "style.css"
    for cls in ("card", "btn", "hero", "hero-title", "sidebar"):
        assert soup.find(class_=cls) is not None, f"Missing class {cls}"


def test_html_classes_defined_in_css():
    css = read_css()
    css_classes = set(re.findall(r"\.([a-z-]+)\s*\{", css))
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for element in soup.find_all(class_=True):
        for cls in element.get("class"):
            assert cls in css_classes, f"Class {cls} is not defined in CSS"
```

What is happening here? The first test reads CSS as text and looks for key constructs: `:root`, at least three variables, `var()`, `transition`, `@keyframes`, and `@media`. The second test checks that the page links the correct `style.css` and contains the required classes. The third (and most interesting) collects all class names from the CSS with a regular expression and verifies that every class used in the HTML is indeed defined in the styles. If a class is missing from the CSS, the test fails.
<!--/SOLUTION-->

<!--QUIZ-->
Where are CSS variables declared so all elements can access them?
- In the body selector
- In :root
- Separately in every class
* Correct answer: In :root
:root is the root element's pseudo-class; variables declared there are visible to all elements.

How do you use a CSS variable?
- var(--name)
- get(--name)
- use(--name)
* Correct answer: var(--name)
A variable's value is substituted via var(--name).

What does transition do?
- Changes the element's color instantly
- Smoothly animates property changes between states
- Creates new styles
* Correct answer: Smoothly animates property changes between states
transition sets a smooth change when properties switch.

What is @keyframes?
- A way to set a font
- An animation scenario: a set of frames with intermediate states
- A selector type
* Correct answer: An animation scenario: a set of frames with intermediate states
@keyframes describes how an element changes over time.

Which pseudo-class fires on keyboard focus?
- :hover
- :focus-visible
- :active
* Correct answer: :focus-visible
:focus-visible shows focus only when it matters (usually the keyboard).

What does @media (max-width: 600px) do?
- Applies styles on screens no wider than 600px
- Increases the font to 600px
- Hides all elements
* Correct answer: Applies styles on screens no wider than 600px
This is a media query — the inner styles act only on narrow screens.

What is prefers-reduced-motion for?
- To speed up animations
- To disable or shorten animations for users who ask for it
- To enable animations on old browsers
* Correct answer: To disable or shorten animations for users who ask for it
It's respect for users with vestibular disorders.

Which properties are safe and cheap to animate?
- width and height
- transform and opacity
- font-size and padding
* Correct answer: transform and opacity
transform and opacity are animated on the GPU and don't cause page reflow.

What does calc(100% - 40px) do?
- Computes a value on the fly
- Rounds a number
- Declares a variable
* Correct answer: Computes a value on the fly
calc() lets you combine units and compute sizes.

What does fill-mode: both mean in an animation?
- The animation plays twice
- The from/to frames apply before the start and after the end — the element doesn't "jump"
- The element disappears after the animation
* Correct answer: The from/to frames apply before the start and after the end — the element doesn't "jump"
both applies the starting frame before the start and the final frame after completion.
<!--/QUIZ-->
