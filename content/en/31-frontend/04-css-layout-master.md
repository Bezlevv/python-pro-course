---
title: Layout mastery: Flexbox and Grid
summary: The two main mechanisms of modern layout — Flexbox for single-axis rows and Grid for grids — plus responsive strategies.
order: 4
duration: 50 min
difficulty: advanced
tags: css, flexbox, grid, responsiveness, layout
---

Time for real layout. In the past, layout developers suffered with `float` and tables; today there are two powerful mechanisms: **Flexbox** — for distributing items along a single axis, and **CSS Grid** — for two-dimensional grids. Master them and you'll lay out almost any interface.

## Flexbox: axis and distribution

Flexbox works with "flexible" items in a container. The container (`display: flex`) has a main axis (horizontal by default) and a cross axis.

```css
.nav {
    display: flex;
    justify-content: space-between; /* distribution along the main axis */
    align-items: center;            /* alignment along the cross axis */
    gap: 16px;                       /* spacing between items */
}
```

Key properties:

- `flex-direction` — `row` (default), `column`, `row-reverse`, `column-reverse`;
- `justify-content` — distribution along the main axis: `flex-start`, `center`, `space-between`, `space-around`, `space-evenly`;
- `align-items` — alignment along the cross axis: `stretch`, `center`, `flex-start`, `flex-end`;
- `flex-wrap: wrap` — wrapping items onto new lines;
- `gap` — the gutter between items (replaces margins);
- `flex-grow`, `flex-shrink`, `flex-basis` — how items grow, shrink, and their base size.

The classic trick is centering a single item: give the container `display: flex; justify-content: center; align-items: center;`. It doesn't get simpler.

```css
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.card {
    flex: 1 1 240px;  /* grows, shrinks, base 240px */
}
```

## Grid: a two-axis grid

Grid divides the container into columns and rows. Its main power is `grid-template-columns`, where you can repeat columns and use `fr` units (fractions of free space):

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}
```

Let's decode: `repeat(auto-fit, ...)` — as many columns as fit; `minmax(220px, 1fr)` — each column is at least 220px, then grows equally. That's a ready-made responsive grid without a single media query.

Explicit grids are defined by listing columns:

```css
.layout {
    display: grid;
    grid-template-columns: 200px 1fr 240px; /* sides + content */
    grid-template-areas:
        "header header header"
        "nav main sidebar"
        "footer footer footer";
    gap: 16px;
}
```

Items are placed by named areas: `grid-area: header` (often `grid-area: nav;` etc.). This is handy for a whole-page skeleton.

## Flex or Grid?

A simple criterion:

- **Order along a single axis** (menu, row of cards, centering) — Flexbox.
- **A grid in both directions or a page skeleton** (gallery, multi-column layout) — Grid.
- Want cards of equal width that wrap — often both work, but Grid with `auto-fit` is more elegant.

Both mechanisms combine easily: Grid lays out the page's sections, and Flexbox works inside sections.

## Layout choice algorithm

When facing a new task, ask yourself three questions in this order:

1. **Is this a single axis?** Menu, button row, icons in a line, vertical list — take Flexbox. It was made for line layout.
2. **Is this a two-dimensional grid?** Cards in several rows, price list, calendar, page skeleton with columns — take Grid. It controls columns and rows at once.
3. **Is this a component inside a grid?** For example, a card in a gallery whose text and button sit in one row. Then Grid outside, Flexbox inside the card.

This order saves you from the common mistake of trying to do everything with one mechanism. The golden standard of modern layout: Grid for the page's "skeleton", Flexbox for the "muscles" — the inner filling of components. And don't forget: `gap` works in both, and `auto-fit` with `minmax` makes a grid responsive without a single media query.

## Responsive strategies

- **Grid with `auto-fit`/`minmax`** — the grid adapts to the width by itself.
- **Flex with `flex-wrap: wrap` and `flex-basis`** — items wrap.
- **Media queries** — when you need to rebuild the whole skeleton: e.g., turn a three-column layout into one column:

```css
@media (max-width: 800px) {
    .layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "nav"
            "main"
            "sidebar"
            "footer";
    }
}
```

## Common mistakes

- Forgot `gap` and set margins on every other element — use `gap`.
- Mixing up `justify-content` (main axis) and `align-items` (cross axis).
- Hardcoding pixel widths instead of `minmax`/`fr` — responsiveness breaks.
- Not setting `flex-wrap: wrap`, so items overflow the screen.

Now let's put all this into practical tasks — from navigation to a full page skeleton with tests.

<!--TASK-->
### Task 1
Create `layout-project/index.html` and `style.css`. Build horizontal navigation with Flexbox:

- `<nav class="nav">` contains a logo ("Logo" text) and `<ul class="nav-links">` with four links;
- the `.nav` container — `display: flex; justify-content: space-between; align-items: center;`;
- the `.nav-links` list — `display: flex; gap: 24px;` with no markers (`list-style: none`).

Expected result: logo on the left, links on the right, all vertically centered.

### Task 2
Create a `.center` class — a block that centers its content both horizontally and vertically (e.g., a section with "Hello, world!" text at full window height: `min-height: 100vh`). Then build a row of cards: a `.card-row` container with `display: flex; flex-wrap: wrap; gap: 20px;` and three `.card` cards with `flex: 1 1 240px;`. Expected result: on a wide screen three cards in a row; when narrowed, they wrap and take as much width as fits.

### Task 3
Build a responsive gallery on Grid: a `.gallery` container with `display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;` and eight cards (`.card` class, any content). Expected result: as the window width changes, the column count changes automatically, without a single media query.

### Task 4
Build a page skeleton on Grid with named areas. Elements: `<header class="site-header">`, `<nav class="sidebar">`, `<main class="content">`, `<aside class="aside">`, `<footer class="site-footer">`. Give the `.layout` container:

- `display: grid`;
- `grid-template-columns: 200px 1fr 240px`;
- `grid-template-areas` with the areas `header header header`, `sidebar content aside`, `footer footer footer`;
- each element a `grid-area` with its name.

Then add a media query: at `max-width: 800px`, rebuild the grid into one column (`grid-template-columns: 1fr`) and stack the areas vertically. Check in the browser: narrow the window — the skeleton should rebuild.

Additionally, write a pytest test `test_grid_layout.py`: render `index.html` via jinja2 (`Environment().from_string(html).render()`) and check with `BeautifulSoup` that all five skeleton elements exist (`.layout`, `.site-header`, `.sidebar`, `.content`, `.aside`, `.site-footer`); then read `style.css` and check that the `.layout` class has `grid-template-areas`, and inside the `@media (max-width: 800px)` block there is `grid-template-columns: 1fr`. Expected result: all checks pass.

### Task 5
Write pytest tests `test_layout.py`:

- an HTML test: read `index.html` with `BeautifulSoup` and check that all five skeleton elements exist (`.layout`, `.site-header`, `.sidebar`, `.content`, `.aside`, `.site-footer`);
- a CSS test: read `style.css` and check that it contains `display: flex` and `display: grid`, `justify-content`, `align-items`, `gap`, `grid-template-columns`, `grid-template-areas`, `@media`;
- a layout test: make sure the `.layout` class uses `grid-template-areas` and `.nav` uses `justify-content: space-between`;
- a responsiveness test: check that `grid-template-columns: 1fr` appears inside `@media (max-width: 800px)`.

Expected result: all tests pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
Nested flex: the outer `.nav` lays out the logo and the list, and the list `.nav-links` itself is also `display: flex` with links. Don't forget `list-style: none` and `padding: 0` for the list.

### Hint 2
Centering: `.center { display: flex; justify-content: center; align-items: center; min-height: 100vh; }`. For cards: `.card-row { display: flex; flex-wrap: wrap; gap: 20px; }`, and `.card { flex: 1 1 240px; }` — that is `flex-grow: 1; flex-shrink: 1; flex-basis: 240px`.

### Hint 3
The magic is in one line: `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));`. `auto-fit` creates as many columns as fit, and `minmax(220px, 1fr)` guarantees a minimum of 220px and equal growth. Add `gap: 16px`.

### Hint 4
Areas are defined row by row: `grid-template-areas: "header header header" "sidebar content aside" "footer footer footer";`. Each element gets its own `grid-area: header;` (and so on). Area names must match the elements' `grid-area`. In the media query, override both `grid-template-columns` and `grid-template-areas`. For the test: cut out the `@media (max-width: 800px)` block with the regular expression `re.search(r"@media \(max-width: 800px\)\s*\{", css)` and check `grid-template-columns: 1fr` in the remaining part.

### Hint 5
To check the `layout` class, find its block in the CSS with a regular expression: `re.search(r"\.layout\s*\{([^}]*)\}", css)`. The result is in group 1. Check `"grid-template-areas" in layout_block`. For the media query: `re.search(r"@media \(max-width: 800px\)\s*\{([^}]*)\}", css)`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
HTML:

```html
<nav class="nav">
    <span class="logo">Logo</span>
    <ul class="nav-links">
        <li><a href="#">Home</a></li>
        <li><a href="#">Blog</a></li>
        <li><a href="#">Projects</a></li>
        <li><a href="#">Contacts</a></li>
    </ul>
</nav>
```

CSS:

```css
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
}
.nav-links {
    display: flex;
    gap: 24px;
    list-style: none;
    margin: 0;
    padding: 0;
}
```

What is happening here? `.nav` becomes a flex container: `justify-content: space-between` pushes the logo and the list to opposite edges, `align-items: center` aligns them vertically. Inside the list there is its own flex: links go in a row with a `gap: 24px` gutter. `list-style: none` removes the list markers. This is a classic site header.

### Solution 2
HTML:

```html
<section class="center">
    <p>Hello, world!</p>
</section>

<div class="card-row">
    <div class="card">Card 1</div>
    <div class="card">Card 2</div>
    <div class="card">Card 3</div>
</div>
```

CSS:

```css
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: #f0f4f8;
}
.card-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 24px;
}
.card {
    flex: 1 1 240px;
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
```

What is happening here? The `.center` section takes at least the window height and centers its content on both axes. In `.card-row`, `flex-wrap: wrap` allows wrapping, and `gap: 20px` sets the gutters. Each card has `flex: 1 1 240px`: a base of 240px, but it grows when there is free space (`grow: 1`) and shrinks when space is tight (`shrink: 1`), never overflowing the screen.

### Solution 3
HTML:

```html
<div class="gallery">
    <div class="card">1</div>
    <div class="card">2</div>
    <!-- ... 8 cards in total -->
</div>
```

CSS:

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    padding: 24px;
}
.card {
    background: #fff;
    border: 1px solid #e0e4ec;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
}
```

What is happening here? Grid counts how many columns of at least 220px fit into the container and creates exactly that many. When the window narrows, there are fewer columns; when it widens, more — and all of them grow equally thanks to `1fr`. No media query is needed. This is the ideal recipe for galleries, catalogs, and tiles.

### Solution 4
HTML:

```html
<div class="layout">
    <header class="site-header">Header</header>
    <nav class="sidebar">Menu</nav>
    <main class="content">Content</main>
    <aside class="aside">Side panel</aside>
    <footer class="site-footer">Footer</footer>
</div>
```

CSS:

```css
.layout {
    display: grid;
    grid-template-columns: 200px 1fr 240px;
    grid-template-areas:
        "header header header"
        "sidebar content aside"
        "footer footer footer";
    gap: 16px;
    min-height: 100vh;
}
.site-header { grid-area: header; }
.sidebar    { grid-area: sidebar; }
.content     { grid-area: content; }
.aside      { grid-area: aside; }
.site-footer { grid-area: footer; }

@media (max-width: 800px) {
    .layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "sidebar"
            "content"
            "aside"
            "footer";
    }
}
```

`test_grid_layout.py`:

```python
import re
from bs4 import BeautifulSoup
from jinja2 import Environment


def render_index():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return Environment().from_string(html).render()


def test_layout_elements_exist():
    soup = BeautifulSoup(render_index(), "html.parser")
    for cls in ("layout", "site-header", "sidebar", "content", "aside", "site-footer"):
        assert soup.find(class_=cls) is not None, f"Missing class {cls}"


def test_layout_uses_grid_areas():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"\.layout\s*\{([^}]*)\}", css)
    assert m is not None
    assert "grid-template-areas" in m.group(1)


def test_media_switches_to_one_column():
    with open("style.css", encoding="utf-8") as f:
        css = f.read()
    m = re.search(r"@media \(max-width: 800px\)\s*\{", css)
    assert m is not None
    rest = css[m.end():]
    assert "grid-template-columns: 1fr" in rest
```

What is happening here? The first test renders the HTML through jinja2 and checks that all five skeleton elements are in place. The second cuts out the `.layout` rule body and verifies that the skeleton is built on `grid-template-areas`. The third finds the media query and checks that `grid-template-columns: 1fr` appears after it — meaning the mobile version switches to one column. Now the skeleton itself: `grid-template-areas` describes it row by row: three columns (`200px` — menu, `1fr` — content, `240px` — panel) and three rows. Each element gets its area name via `grid-area`. On narrow screens, the media query overrides both the columns (`1fr`) and the areas — everything stacks into one column. One CSS file holds two layouts.

### Solution 5
`test_layout.py`:

```python
import re
from bs4 import BeautifulSoup


def read_css():
    with open("style.css", encoding="utf-8") as f:
        return f.read()


def css_block(selector):
    css = read_css()
    m = re.search(r"\.%s\s*\{([^}]*)\}" % selector, css)
    return m.group(1) if m else ""


def test_html_has_layout_elements():
    with open("index.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for cls in ("layout", "site-header", "sidebar", "content", "aside", "site-footer"):
        assert soup.find(class_=cls) is not None, f"Missing class {cls}"


def test_css_has_key_properties():
    css = read_css()
    for prop in ("display: flex", "display: grid", "justify-content",
                 "align-items", "gap", "grid-template-columns",
                 "grid-template-areas", "@media"):
        assert prop in css, f"Missing '{prop}'"


def test_nav_uses_space_between():
    assert "justify-content: space-between" in css_block("nav")


def test_layout_uses_grid_areas():
    assert "grid-template-areas" in css_block("layout")


def test_media_switches_to_one_column():
    css = read_css()
    m = re.search(r"@media \(max-width: 800px\)\s*\{", css)
    assert m is not None
    media_block = css[m.end():]
    assert "grid-template-columns: 1fr" in media_block
```

What is happening here? `css_block()` cuts out the rule body by selector — so we check properties for a specific class, not just their presence in the file. `test_nav_uses_space_between` confirms the navigation uses the right distribution; `test_layout_uses_grid_areas` confirms the skeleton is built on areas. The last test finds the media query, cuts off everything after its opening brace, and checks that the columns switch to one.
<!--/SOLUTION-->

<!--QUIZ-->
Which property makes an element a flex container?
- display: flex
- position: flex
- flex: container
* Correct answer: display: flex
display: flex enables Flexbox layout on a container.

What does justify-content: space-between do?
- Centers items vertically
- Pushes items to the edges, leaving equal space between them
- Makes items equal width
* Correct answer: Pushes items to the edges, leaving equal space between them
space-between places the first and last items at the edges and the rest between them.

What does gap set?
- Space between neighboring items
- Margin from the page edge
- Item transparency
* Correct answer: Space between neighboring items
gap is the distance between items inside a flex/grid container.

What does flex: 1 1 240px mean?
- grow: 1, shrink: 1, basis: 240px
- Only sets a base of 240px
- Forbids stretching
* Correct answer: grow: 1, shrink: 1, basis: 240px
The shorthand sets three properties: growth, shrinking, and base size.

What does grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)) do?
- Creates a responsive grid: as many columns as fit
- Creates exactly three columns
- Forbids column wrapping
* Correct answer: Creates a responsive grid: as many columns as fit
auto-fit counts columns by the container width; minmax sets their minimum size.

What does the 1fr unit mean in a grid?
- One fraction of the free space
- One pixel
- 1% of the width
* Correct answer: One fraction of the free space
The fr unit distributes free space proportionally to fractions.

What are grid-template-areas for?
- To name grid areas and place items in them
- To set area colors
- To declare variables
* Correct answer: To name grid areas and place items in them
Areas are defined by rows, and items get names via grid-area.

What should you choose for a one-line menu of links?
- Flexbox
- Grid with areas
- float
* Correct answer: Flexbox
For a single axis — Flexbox; Grid is better for two-dimensional grids.

What happens with flex-wrap: wrap?
- Items wrap to a new line when they don't fit
- Items shrink to 0
- Items are hidden
* Correct answer: Items wrap to a new line when they don't fit
wrap allows wrapping instead of squeezing into one line.

How do you center a block on both axes?
- display: flex; justify-content: center; align-items: center;
- text-align: center; margin: auto;
- display: block; width: 50%;
* Correct answer: display: flex; justify-content: center; align-items: center;
Both properties center along the main and cross axes.
<!--/QUIZ-->
