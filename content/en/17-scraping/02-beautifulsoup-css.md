---
title: BeautifulSoup: CSS selectors
summary: How to parse HTML: BeautifulSoup, find/find_all, extracting text and attributes, CSS selectors via select.
order: 2
duration: 40 min
difficulty: advanced
tags: beautifulsoup, html, css selectors, scraping
---

You've learned how to download pages. Now the main question: how do you pull the data you need out of a pile of HTML tags? The answer — the `BeautifulSoup` library from the `beautifulsoup4` package. It turns HTML into a tree of objects that's easy to walk: search for elements by tags, classes, attributes — and all of it with short, expressive code.

## Installation and your first soup

Install the library together with the `lxml` parser (it's faster than the built-in one):

```bash
pip install beautifulsoup4 lxml
```

To get started, create a `BeautifulSoup` object from HTML text:

```python
from bs4 import BeautifulSoup

html = "<html><body><h1>Hello</h1><p class='text'>World</p></body></html>"
soup = BeautifulSoup(html, "lxml")
```

The second argument is the parser name: `"lxml"` or `"html.parser"`. HTML is not text to be handled with regex — it's a tree of tags: inside `html` lies `body`, inside it — `h1` and `p`. BeautifulSoup builds this tree, and then we walk it.

## find() and find_all(): searching by tags and attributes

`find_all()` returns a **list** of all matching elements, `find()` — the first one (or `None`):

```python
soup.find("h1")                       # first h1 heading
soup.find_all("p")                    # all paragraphs
soup.find_all("p", class_="text")     # paragraphs with the class text
soup.find_all("a", href=True)         # links with the href attribute
```

Note: to search by class you use `class_` with an underscore — because `class` is reserved in Python. There's also a shorter form: `soup.find_all(class_="text")`. If there are no elements — an empty list; it's important to check this so you don't crash on `None`.

## CSS selectors: select() and select_one()

BeautifulSoup's power is its support for CSS selectors. `select()` returns all elements matching a selector, and `select_one()` — the first:

```python
soup.select("p.text")          # paragraphs with the class text
soup.select("div#content p")   # paragraphs inside a div with id=content
soup.select_one("h1")          # first h1
soup.select("a[href^='https']")  # links starting with https
```

Selectors use the same syntax as CSS: `tag`, `.class`, `#id`, `[attribute]`, combinators with a space (descendant). For most tasks, `select` and `select_one` are the cleanest way. Remember: `select` always returns a list, even if there's just one element.

## Extracting data: text and attributes

Found an element — now pull the text and attributes out of it:

```python
h1 = soup.select_one("h1")
print(h1.get_text())        # text inside the element
print(h1.text)              # same thing, short form

a = soup.select_one("a")
print(a.get("href"))        # value of the href attribute
print(a["href"])            # same, but will fail if the attribute is missing
```

`get_text()` strips tags and leaves the visible text. `get("href")` safely returns `None` if the attribute is missing, while `a["href"]` raises `KeyError`. For scraping, `get()` is more convenient.

## A real example: quotes

Let's try the training quotes site `https://quotes.toscrape.com/`. There, each quote is in a `div.quote` block, the text — in `span.text`, the author — in `small.author`, the tags — in `a.tag` links:

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

for quote in soup.select("div.quote")[:3]:
    text = quote.select_one("span.text").get_text()
    author = quote.select_one("small.author").get_text()
    print(author, "-", text)
```

See how readable the code is: "take all `div.quote` blocks, find `span.text` and `small.author` in each, pull out the text". That's the essence of scraping — describing where the data lives and extracting it.

## Navigating the tree

Sometimes it's convenient to move from element to element: `.parent` — the parent, `.find_parent("div")` — the nearest parent with that tag, `.next_sibling` — the adjacent element. For example, to find the whole quote block by author:

```python
small = soup.select_one("small.author")
quote_block = small.find_parent("div", class_="quote")
```

But don't overdo it: chains like `.parent.parent.parent` break quickly at the slightest change in markup. CSS selectors are usually more reliable.

## Summary

The recipe for any extraction from HTML: download the page → create a `BeautifulSoup` → select elements via `select`/`find_all` → get text with `get_text()` and attributes with `get()`. If there are no elements — the list is empty, and that's normal. Now let's practice on real sites.

<!--TASK-->
### Task 1

Write a program `first_soup.py`. Download `https://quotes.toscrape.com/` using `requests.get` (don't forget `timeout=10`) and create a `BeautifulSoup` with the `"lxml"` parser. Print: the page title via `soup.title.get_text()`, the number of quote blocks via `len(soup.select("div.quote"))`, and the number of unique authors via `len(set(...))` — for the latter, collect the text of all `small.author` elements. At the end, print the first quote: its text and author.

### Task 2

Collect all authors from page 1 of `https://quotes.toscrape.com/`. Write a program `authors.py` that uses `select("small.author")` to collect author texts into a set, prints the total number of unique authors and the first five names (sorted alphabetically) via `sorted()`. If the page has 10 quotes and some authors repeat — the set will remove duplicates by itself. Print a line like `Unique authors: N`, then the list of names, one per line.

### Task 3

On the page `https://quotes.toscrape.com/` find the "Next" link — it sits in a `li.next` block inside an `a` link. Use `select_one("li.next a")`, print its `href` attribute and the full absolute address: just concatenate `"https://quotes.toscrape.com"` + `href`. Also print the link's text (usually `Next`). If there's no link — print the phrase `There is no next page`.

### Task 4

Go to the bookstore site `https://books.toscrape.com/`. There, each book is in an `article.product_pod` block, the title — in `h3 a` (the `title` attribute or the text), the price — in `p.price_color`. Write a program `books.py` that prints pairs `Title — Price` for the first five books (e.g. `A Light in the Attic — £51.77`), and then shows how many books on the page cost less than £20: turn the price into a number via `float(price[1:])` (remove the `£` symbol).

### Task 5

Each quote on `https://quotes.toscrape.com/` has tags — `a.tag` links inside the `div.quote` block. Write a program `tags.py` that collects all tags of all quotes on the page into a single list and uses `collections.Counter` to count the frequency of each tag. Print the top 3 most frequent tags in the format `tag: count` in descending order of frequency. Hint: the `most_common(3)` method of `Counter` returns the top three.
<!--/TASK-->

<!--HINT-->
### Hint 1

`BeautifulSoup(html, "lxml")` takes the response text from `r.text`. Title: `soup.title.get_text()`. Quote blocks: `soup.select("div.quote")`. Authors: `soup.select("small.author")` — each element is turned into text with `get_text()`.

### Hint 2

A set removes duplicates automatically: `authors = {a.get_text() for a in soup.select("small.author")}`. Length — `len(authors)`. Sorting — `sorted(authors)`. Slice of the first five — `sorted(authors)[:5]`.

### Hint 3

The selector `"li.next a"` looks for a link inside a block with the class `next`. The attribute is `link["href"]` or `link.get("href")`. Check with `if link:` — if there's no element, `select_one` returns `None`, and accessing `["href"]` will crash.

### Hint 4

Book title: `book.select_one("h3 a")["title"]` or `book.select_one("h3 a").get_text()`. Price: `book.select_one("p.price_color").get_text()` — a string like `£51.77`. To compare, turn it into a float: `float(price[1:])` — the slice from the first character removes `£`.

### Hint 5

Collect all tags of all quotes: a double loop or a generator `[tag.get_text() for quote in soup.select("div.quote") for tag in quote.select("a.tag")]`. `Counter` counts frequencies. `most_common(3)` returns a list of tuples `(tag, count)` — loop over it and print.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

print("Title:", soup.title.get_text())
print("Quote blocks:", len(soup.select("div.quote")))

authors = {a.get_text() for a in soup.select("small.author")}
print("Unique authors:", len(authors))

first = soup.select_one("div.quote")
print("First quote:")
print(first.select_one("span.text").get_text())
print("-", first.select_one("small.author").get_text())
```

Step-by-step breakdown:

- `r.text` — the page's HTML. From it, `soup` is created — a tree of elements.
- `soup.title.get_text()` — the text inside the `<title>` tag. That's the browser tab title.
- `soup.select("div.quote")` returns a list of all quote blocks — there are 10 of them on this page.
- The set generator `{a.get_text() for a in soup.select("small.author")}` collects authors and immediately removes repeats: if one author appears three times, they remain in the set once.
- `soup.select_one("div.quote")` — the first quote block. Inside it, `select_one("span.text")` finds the text, `select_one("small.author")` — the author.
- An important skill: first page → `soup`, then selection. Everything else in a scraper is a variation of this recipe.

### Solution 2

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

authors = {a.get_text() for a in soup.select("small.author")}
print("Unique authors:", len(authors))

for name in sorted(authors)[:5]:
    print(name)
```

Step-by-step breakdown:

- `soup.select("small.author")` — all elements with the tag `small` and class `author`. There are as many of them on the page as there are quotes — one per quote.
- `a.get_text()` extracts the author's name. The `authors` set automatically removes duplicates: Agatha Christie, appearing twice, ends up in it once.
- `len(authors)` — the number of unique authors. On page 1 there may be fewer than ten if someone repeats.
- `sorted(authors)` sorts the names alphabetically, and `[:5]` takes the first five.
- This approach — "collect all values, remove repeats" — appears constantly in scraping: lists of tags, names, categories. Set + `sorted` is the standard tool.

### Solution 3

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

next_link = soup.select_one("li.next a")
if next_link:
    href = next_link["href"]
    print("Link text:", next_link.get_text().strip())
    print("Relative address:", href)
    print("Full address:", "https://quotes.toscrape.com" + href)
else:
    print("There is no next page")
```

Step-by-step breakdown:

- The selector `"li.next a"` means: "an `a` link inside an `li` element with the class `next`". That's the standard pagination markup on the training site.
- `select_one` returns the first matching element or `None`. The `if next_link:` check is a must: on the last page there's no `li.next` block, and `next_link` will be `None`.
- `next_link["href"]` — the attribute value: usually `"/page/2/"` — a relative address. The full URL is built by concatenating with the base `https://quotes.toscrape.com`.
- `next_link.get_text().strip()` — the visible "Next" link text. `strip()` removes extra whitespace and newlines.
- This is exactly how page traversal works: found the "Next" link — follow it while it exists. You'll come back to this in the lesson on pagination.

### Solution 4

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

books = soup.select("article.product_pod")
for book in books[:5]:
    title = book.select_one("h3 a")["title"]
    price = book.select_one("p.price_color").get_text()
    print(f"{title} — {price}")

cheap = 0
for book in books:
    price = book.select_one("p.price_color").get_text()
    if float(price[1:]) < 20:
        cheap += 1
print("Books cheaper than £20:", cheap)
```

Step-by-step breakdown:

- `article.product_pod` — a book card on the store's main page.
- The title sits in the `title` attribute of the link inside `h3`: `book.select_one("h3 a")["title"]`. You could also take the link's text, but `title` is more reliable — it holds the full name without abbreviations.
- The price is in `p.price_color`, e.g. `£51.77`. It's a string, and comparison needs a number.
- `price[1:]` cuts off the first `£` character, `float(...)` turns `"51.77"` into `51.77`. Now you can compare: `float(price[1:]) < 20`.
- The loop over all books counts those cheaper than £20. On the main page there are usually quite a few — the store deliberately features cheap books.
- Note the `f"{title} — {price}"` — an f-string that inserts values right into the text.

### Solution 5

```python
import requests
from collections import Counter
from bs4 import BeautifulSoup

r = requests.get("https://quotes.toscrape.com/", timeout=10)
soup = BeautifulSoup(r.text, "lxml")

tags = [
    tag.get_text()
    for quote in soup.select("div.quote")
    for tag in quote.select("a.tag")
]

counter = Counter(tags)
for tag, count in counter.most_common(3):
    print(f"{tag}: {count}")
```

Step-by-step breakdown:

- A double list generator: the outer loop goes over quote blocks (`soup.select("div.quote")`), the inner one over the tag links inside each block (`quote.select("a.tag")`).
- `tag.get_text()` — the tag text, e.g. `life`, `love`, `wisdom`. The resulting `tags` list contains all tags of the page, with repeats.
- `Counter(tags)` — a dictionary that counts how many times each tag occurs.
- `most_common(3)` returns a list of the three most frequent `(tag, count)` pairs in descending order: `[('life', 3), ('love', 2), ...]`.
- The loop unpacks the pairs and prints `tag: count`.
- Counting frequencies like this is a typical step in analyzing collected data: who/what is mentioned most often, which categories are popular. `Counter` is a standard module — no external libraries needed.
<!--/SOLUTION-->

<!--QUIZ-->
What does soup.find_all("p") return?
- The first paragraph p
- A list of all paragraphs p
- The number of paragraphs
- The page's HTML string
* Correct answer: A list of all paragraphs p
find_all() always returns a list of elements (possibly empty).

How do you correctly search for elements by class in find_all?
- find_all("p", class="text")
- find_all("p", class_="text")
- find_all("p", css="text")
- find_all("p.text")
* Correct answer: find_all("p", class_="text")
class is a reserved word, so class_ with an underscore is used.

What will soup.select_one("h1") return if there is no h1 tag on the page?
- An empty list
- None
- An empty string
- An error will be raised
* Correct answer: None
select_one() returns the first element or None if nothing is found.

How do you get the text inside a soup element without nested tags?
- element.html()
- element.get_text()
- element.text_value()
- element.inner_html()
* Correct answer: element.get_text()
get_text() (or .text) returns the visible text of the element, discarding tags.

Which selector will pick links with the class tag inside a block with the class quote?
- "a.tag quote"
- "div.quote a.tag"
- "quote > tag"
- "a.tag.quote"
* Correct answer: "div.quote a.tag"
The selector "div.quote a.tag" means descendants: a.tag links inside div.quote.

What is the difference between select() and select_one()?
- select() by class, select_one() by id
- select() returns a list, select_one() returns the first element or None
- select() works only with tags, select_one() with attributes
- There is no difference
* Correct answer: select() returns a list, select_one() returns the first element or None
select() always gives a list of all matches, select_one() — only the first one.

What will soup.find_all("a", href=True) return?
- All links that have the href attribute
- The first link on the page
- The texts of all links
- The number of links
* Correct answer: All links that have the href attribute
href=True is a filter on attribute presence: only those a elements that have it get into the list.

How is a.get("href") different from a["href"]?
- get("href") returns None if the attribute is missing, while a["href"] raises KeyError
- These are completely equivalent ways
- a["href"] is safer for scraping
- get("href") works only with element text
* Correct answer: get("href") returns None if the attribute is missing, while a["href"] raises KeyError
In scraping, get() is used more often — it doesn't crash the program when an attribute is missing.
<!--/QUIZ-->
