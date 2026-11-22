---
title: Semantic HTML5 and Accessibility
summary: Semantic HTML5 tags, a proper document skeleton, and accessibility fundamentals: ARIA, alt texts, keyboard navigation.
order: 1
duration: 40 min
difficulty: intermediate
tags: html, semantics, accessibility, aria, seo
---

In this lesson you will learn to write HTML so that browsers, search engines, and screen readers (programs that read content aloud for blind users) understand your page equally well. This is called **semantic markup**, and it is the first step toward professional frontend development.

## Why semantics matter

A browser does not "read" a page the way a person does. It parses the DOM tree, and the tags you choose affect a great deal:

- **SEO.** Search engines rank pages better when headings, lists, and main content are marked up correctly.
- **Accessibility (a11y).** A screen reader announces `header`, `nav`, and `article` in a special way: the user can jump between sections.
- **Maintainability.** Semantic code is easier to maintain, and writing tests for it is simpler — we will cover that in the tasks.

## Document skeleton

Every page starts with a skeleton. Note the `lang` attribute — it is required for accessibility, because the screen reader uses it to choose pronunciation:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My blog</title>
</head>
<body>
    <!-- content -->
</body>
</html>
```

`<meta name="viewport">` is needed for correct rendering on phones, and `charset="UTF-8"` for non-ASCII text.

## Key semantic tags

The golden rule: **choose a tag by meaning, not by appearance**.

- `<header>` — page or section header: logo, title, menu.
- `<nav>` — the main site navigation (if there is one menu, it usually lives inside `header` too).
- `<main>` — the main content of the page. It must be **unique** on the page.
- `<section>` — a logical section with its own heading (`<h2>` or lower).
- `<article>` — a self-contained, complete block: a blog post, a comment, a product card.
- `<aside>` — a side panel: supplementary information, links, ads.
- `<footer>` — the page footer: copyright, contacts, links.
- `<figure>` and `<figcaption>` — an illustration and its caption.
- `<time datetime="...">` — a date in a machine-readable format.
- `<address>` — contact information.
- `<details>` / `<summary>` — a collapsible block.
- `<mark>` — highlighted text fragment.

Here is a minimal example of a semantic site skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
</head>
<body>
    <header>
        <nav aria-label="Main menu">
            <ul>
                <li><a href="#about">About me</a></li>
                <li><a href="#works">Works</a></li>
                <li><a href="#contacts">Contacts</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section id="about">
            <h1>Anna</h1>
            <p>I am a web developer.</p>
        </section>

        <section id="works">
            <h2>My works</h2>
            <article>
                <h3>Online store</h3>
                <p>A project preview...</p>
            </article>
        </section>
    </main>

    <aside>
        <h2>Skills</h2>
        <ul>
            <li>HTML/CSS</li>
            <li>Python</li>
        </ul>
    </aside>

    <footer>
        <address>Moscow, Primer St., 1</address>
    </footer>
</body>
</html>
```

Note: there is exactly one `<h1>` in the document, and it is inside `<main>`. Headings form a hierarchy: `h1` → `h2` → `h3`.

## Accessibility: getting started

Accessibility is about making sure everyone can use the site: for example, blind people through a screen reader, or people who control the computer with the keyboard only. The basic minimum:

- **`alt` on images.** It is read by the screen reader instead of the picture. Decorative images get `alt=""` (empty — the screen reader will simply skip them).
- **`<label>` on form fields.** The label text must be linked to the field via `for` and `id`.
- **A logical focus order.** Keyboard navigation follows the order of elements in the DOM, so the semantic structure matters beyond mere appearance.
- **A "Skip to content" link (skip-link).** The first link on the page points to `<main>` and is visible only on focus.

## ARIA

ARIA (Accessible Rich Internet Applications) is a set of attributes that extend semantics when standard tags are not enough. The most common ones:

- `role` — the role of an element, e.g. `role="navigation"`, `role="alert"`.
- `aria-label` — an accessible name for an element when there is no visible text (e.g., for an icon button).
- `aria-hidden="true"` — hides an element from the screen reader (e.g., a decorative icon).
- `aria-live="polite"` — a region where dynamic messages appear, so the screen reader announces them.

Important: **don't duplicate what a tag already provides**. If you use `<nav>`, you don't need to add `role="navigation"` — the role is built in. ARIA is only needed where tag semantics fall short:

```html
<header>
    <nav>
        <ul>
            <li><a href="#home" aria-current="page">Home</a></li>
            <li><a href="#blog">Blog</a></li>
        </ul>
    </nav>
</header>

<button aria-label="Open menu">☰</button>

<img src="decor.svg" alt="">
<p aria-live="polite" role="status">Item added to cart</p>
```

## Checking your page

Two simple ways to check accessibility and validity:

- [W3C Validator](https://validator.w3.org/) — checks HTML syntax.
- The **axe DevTools** extension or Lighthouse in Chrome DevTools — automated accessibility checks.

A good habit: before submitting your work, tab through the page with the `Tab` key — all content must be reachable without a mouse.

Now let's put everything into practice. You will turn "div soup" markup into semantic markup and write tests that automatically check the structure and accessibility.

<!--TASK-->
### Task 1
In front of you is a typical "div-soup" layout — parts of it carry no semantic meaning:

```html
<div class="header">
    <div class="menu">
        <span><a href="#about">About me</a></span>
        <span><a href="#works">Works</a></span>
    </div>
</div>
<div class="content">
    <div class="title"><h1>Anna</h1></div>
    <div class="text"><p>I am a web developer.</p></div>
    <div class="block">
        <div class="block-title"><h2>Project 1</h2></div>
        <div class="block-text"><p>Project description.</p></div>
    </div>
</div>
<div class="footer">
    <div>© 2026, Anna</div>
</div>
```

Rewrite this fragment as semantic HTML: use `header`, `nav`, `main`, `section`, `article`, `footer`. Wrap the menu in a `<ul>` with links. Make sure `<h1>` is unique and sits inside `<main>`. Save the result to `semantic.html`. Expected result: valid HTML without `<div>`s that carry no meaning (they are allowed only where no semantic tag exists).

### Task 2
Write a pytest test in `test_semantics.py` that automatically verifies your `semantic.html` page from task 1. Cover the following requirements:

- the page has exactly one `<main>`, one `<header>`, and one `<footer>`;
- inside `<nav>` there are exactly two `<a>` links;
- the page has exactly one `<h1>`, and it is inside `<main>`;
- the entire page text (ignoring tags) contains the substring “Anna”.

Use `BeautifulSoup` from the `bs4` package (install it if missing: `pip install beautifulsoup4`). Read the file, parse it with the `html.parser` parser, and write assertions with `assert`. Run the test with `python -m pytest test_semantics.py` from the folder containing the file. Expected result: all tests pass green.

### Task 3
Take your `semantic.html` and improve its accessibility. Add:

1. the `lang="en"` attribute on `<html>`;
2. a `<label for="search">` label and an `<input id="search" type="search" placeholder="Search">` field in the header;
3. `aria-label="Main menu"` on `<nav>`;
4. a skip-link anchor: `<a class="skip-link" href="#main">Skip to content</a>` as the first link in `<body>`, and give `<main>` `id="main"`;
5. a decorative element — e.g., a ✨ icon in the footer — with `aria-hidden="true"`.

Save the result and check the page in a browser: the “Skip to content” link must appear when you press `Tab`.

### Task 4
Write a second pytest test, `test_accessibility.py`, for the page from task 3. It should check:

- `<html>` has a `lang` attribute;
- the `skip-link` link exists and is the first element inside `<body>`;
- `<nav>` has an `aria-label` attribute;
- the search `<input>` has a linked `<label>` (the label's `for` matches the field's `id`);
- an element with `aria-hidden="true"` exists.

Use `BeautifulSoup` again. Expected result: all five checks pass.

### Task 5
Build a news section in a separate `news.html` file — a mini-page on the topic “Python 3.13 has been released”. Use the required elements:

- `<article>` — the news wrapper;
- `<h1>` — the headline;
- `<time datetime="2026-10-15">October 15, 2026</time>` — the date;
- `<figure>` with `<img>` (any image via a link) and `<figcaption>` — the caption;
- `<address>` — the author of the news;
- `<details>` with `<summary>Details</summary>` — a collapsible block with text inside;
- `<mark>` — an important highlighted word in the text.

Expected result: valid semantic HTML in which each of the listed tags occurs exactly once.
<!--/TASK-->

<!--HINT-->
### Hint 1
Replace each meaningful `div` with a semantic tag one-to-one: `div.header` → `<header>`, `div.menu` → `<nav>`, `div.content` → `<main>`, `div.block` → `<article>`, `div.footer` → `<footer>`. Wrap the links in `<ul><li>`. Don't forget: one `h1`, and it lives in `main`.

### Hint 2
Import the libraries: `from bs4 import BeautifulSoup` and `import pytest`. Read the file like this: `with open("semantic.html", encoding="utf-8") as f: soup = BeautifulSoup(f.read(), "html.parser")`. Count elements with `len(soup.find_all("main"))`. Get the page text with `soup.get_text()`.

### Hint 3
A skip-link is a plain link, but its CSS rules usually hide it until focus: `.skip-link { position: absolute; left: -9999px; } .skip-link:focus { left: 0; }`. If you are not writing CSS yet, just place the link first in `<body>` and give `main` `id="main"`.

### Hint 4
The label–field link is checked like this: `label = soup.find("label"); field_id = label["for"]; field = soup.find(id=field_id)`. Make sure `field` is not `None`. Check `aria-hidden` with `elem.get("aria-hidden") == "true"`.

### Hint 5
Start with the `<html lang="en">` skeleton; inside it goes `<article>`. Order inside `article`: `h1`, `time`, `figure` (with `img` and `figcaption`), paragraphs, `address`, `details`. Write `datetime` on `time` in YYYY-MM-DD format.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
The semantic version of the fragment:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>About me</title>
</head>
<body>
    <header>
        <nav aria-label="Main menu">
            <ul>
                <li><a href="#about">About me</a></li>
                <li><a href="#works">Works</a></li>
            </ul>
        </nav>
    </header>

    <main id="main">
        <section id="about">
            <h1>Anna</h1>
            <p>I am a web developer.</p>
        </section>

        <section id="works">
            <h2>Project 1</h2>
            <article>
                <h3>Project title</h3>
                <p>Project description.</p>
            </article>
        </section>
    </main>

    <footer>
        <p>© 2026, Anna</p>
    </footer>
</body>
</html>
```

What is happening here? Every `div` with a "speaking" class was replaced by a semantic tag: `header` — the top, `nav` — the menu, `main` — the main content, `section` — a section, `article` — a complete block, `footer` — the bottom. Menu links are wrapped in a `<ul>` list, because a menu is a navigation list. Note: `h1` appears exactly once and sits inside `main` — this is a requirement of both SEO and accessibility. The `lang="en"` attribute tells the browser and the screen reader the page's language.

### Solution 2
`test_semantics.py`:

```python
import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def soup():
    with open("semantic.html", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def test_one_main_header_footer(soup):
    assert len(soup.find_all("main")) == 1
    assert len(soup.find_all("header")) == 1
    assert len(soup.find_all("footer")) == 1


def test_nav_has_two_links(soup):
    nav = soup.find("nav")
    assert nav is not None
    assert len(nav.find_all("a")) == 2


def test_single_h1_inside_main(soup):
    main = soup.find("main")
    h1s_in_main = main.find_all("h1")
    assert len(h1s_in_main) == 1
    assert len(soup.find_all("h1")) == 1


def test_page_mentions_name(soup):
    assert "Anna" in soup.get_text()
```

What is happening here? Via `BeautifulSoup` we parse HTML into a tree. `find_all("main")` returns the list of all `<main>` elements — there must be exactly one of each. For navigation, we first find `<nav>` itself, then count the links inside it. `test_single_h1_inside_main` checks two facts at once: `h1` exists inside `main` and is the only one on the whole page. `soup.get_text()` returns all the visible text without tags, so the name check works even if "Anna" appears in different parts of the markup. Run with `python -m pytest test_semantics.py`.

### Solution 3
Here is the fragment with improved accessibility:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>About me</title>
    <style>
        .skip-link { position: absolute; left: -9999px; }
        .skip-link:focus { left: 10px; top: 10px; background: #fff; }
    </style>
</head>
<body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header>
        <nav aria-label="Main menu">...</nav>
        <form role="search">
            <label for="search">Search the site</label>
            <input id="search" type="search" placeholder="Search">
        </form>
    </header>
    <main id="main">...</main>
    <footer>
        <p>✨ <span aria-hidden="true">✨</span> © 2026, Anna</p>
    </footer>
</body>
</html>
```

What is happening here? The skip-link comes first in `<body>`, so it gets the first keyboard focus. CSS hides it (`left: -9999px`), but brings it back on focus. `aria-label` on `nav` gives the menu a name the screen reader will announce. The search label is linked to the field via `for`/`id`. The decorative star icon got `aria-hidden="true"` so the screen reader skips it — it carries no meaning.

### Solution 4
`test_accessibility.py`:

```python
from bs4 import BeautifulSoup


def load_html():
    with open("semantic.html", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def test_html_has_lang():
    soup = load_html()
    assert soup.html.get("lang") == "en"


def test_skip_link_is_first():
    soup = load_html()
    body_children = list(soup.body.children)
    first_tag = next(el for el in body_children if getattr(el, "name", None))
    assert first_tag.get("class") == ["skip-link"]


def test_nav_has_aria_label():
    soup = load_html()
    assert soup.find("nav").get("aria-label") == "Main menu"


def test_label_connected_to_input():
    soup = load_html()
    label = soup.find("label", attrs={"for": "search"})
    field = soup.find(id="search")
    assert label is not None and field is not None


def test_aria_hidden_exists():
    soup = load_html()
    assert soup.find(attrs={"aria-hidden": "true"}) is not None
```

What is happening here? In `test_skip_link_is_first` we iterate over the direct children of `<body>` and take the first element (text nodes have no `name` attribute). This is more honest than just searching for a link: we verify its position. The label test ensures both `<label for="search">` and `<input id="search">` exist — meaning the connection is intact. `soup.find(attrs={"aria-hidden": "true"})` finds any element with that attribute. All five tests should pass after completing task 3.

### Solution 5
`news.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>News: Python 3.13</title>
</head>
<body>
    <article>
        <h1>Python 3.13 has been released</h1>
        <p><time datetime="2026-10-15">October 15, 2026</time></p>
        <figure>
            <img src="https://www.python.org/static/img/python-logo.png"
                 alt="Python logo">
            <figcaption>The official Python logo</figcaption>
        </figure>
        <p>The release introduces a <mark>JIT compiler</mark> that speeds up
           code execution.</p>
        <details>
            <summary>Details</summary>
            <p>Some programs are now up to 30% faster. Updating is
               recommended for all users.</p>
        </details>
        <address>Author: the python.org team</address>
    </article>
</body>
</html>
```

What is happening here? `<article>` wraps the whole self-contained news item: you can lift it out of the page without losing meaning. `<time>` holds both a human-readable date and a machine-readable one in `datetime` (YYYY-MM-DD format). `<figure>` ties the image to its `<figcaption>` caption: the screen reader reads the caption, and `alt` contains the image description. `<details>/<summary>` creates a collapsible block without a single line of JavaScript. `<address>` holds the contact information. `<mark>` highlights the important word. Such a block is read equally well by humans and automated parsers.
<!--/SOLUTION-->

<!--QUIZ-->
Which tag marks the main content of a page?
- main
- header
- body
* Correct answer: main
The main tag must appear once on the page and contain the page's unique content.

How many h1 tags are recommended per page?
- One
- As many as you want
- No more than three
* Correct answer: One
One h1 per page is a requirement of semantics and SEO.

What does the attribute aria-hidden="true" do?
- Makes the element invisible in the browser
- Hides the element from the screen reader
- Disables the element
* Correct answer: Hides the element from the screen reader
aria-hidden removes the element from the accessibility tree — the screen reader will not announce it.

Inside which tag does the main menu link list logically belong?
- div
- nav
- section
* Correct answer: nav
The nav tag is meant for navigation blocks, and a link list is a ul inside nav.

What should go into alt for a decorative image that carries no meaning?
- An empty string alt=""
- A description of the image
- Nothing at all
* Correct answer: An empty string alt=""
An empty alt tells the screen reader to skip the image — it carries no information.

Which attribute is required on the html tag for accessibility?
- lang
- dir
- class
* Correct answer: lang
lang specifies the page's language; the screen reader uses it for pronunciation.

What is the figure tag for?
- Large font size
- Grouping an illustration with its caption
- Creating a table
* Correct answer: Grouping an illustration with its caption
figure combines media content with figcaption — its caption.

What is a skip-link?
- A link to the end of the page
- The first link on the page, pointing to the main content
- A link to the site header
* Correct answer: The first link on the page, pointing to the main content
A skip-link lets users jump straight to main, bypassing navigation.

Which tag fits a blog post best?
- section
- article
- aside
* Correct answer: article
article is a self-contained, complete block, e.g., a blog post.

What does the aria-label attribute do?
- Changes the element's color
- Gives the element an accessible name that the screen reader announces
- Adds a tooltip on hover
* Correct answer: Gives the element an accessible name that the screen reader announces
aria-label names an element when there is no visible text.
<!--/QUIZ-->
