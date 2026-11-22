---
title: Dynamic pages: Selenium and Playwright
summary: When HTML arrives "empty": Selenium WebDriver and Playwright for pages that are rendered by JavaScript.
order: 3
duration: 45 min
difficulty: advanced
tags: selenium, playwright, browser, javascript, dynamic pages
---

Sometimes it happens: `requests` downloaded the page, and there's not a single product or quote in it — only an empty shell. That means the content is created by JavaScript in the browser: the server sends the wrapper, and the data is loaded by scripts. `requests` doesn't run JS, so it sees emptiness. For such pages you need a real browser controlled by a program. The two main tools are **Selenium** and **Playwright**.

## When you need a browser

Signs of a dynamic page: data appears after scrolling (an infinite feed), content loads via a "Show more" button, the page rearranges itself in response to user actions. Ask yourself: "would I see this data if JavaScript were turned off?" If not — you need a browser.

## Selenium: the classic

Selenium drives a real browser through WebDriver. Installation:

```bash
pip install selenium
```

Selenium can download the Chrome driver (ChromeDriver) itself, but it's easier to use **Selenium Manager**, which ships with the library — it will pick a driver matching your browser version by itself. A basic script:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless=new")  # without a window
driver = webdriver.Chrome(options=options)
driver.get("https://quotes.toscrape.com/")

quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")
print(len(quotes))

driver.quit()  # always close the browser
```

`find_elements(By.CSS_SELECTOR, "div.quote")` — finding elements by a CSS selector, like in BeautifulSoup. `find_element` (without `s`) returns the first one or raises an exception if there is none.

## Waiting: don't sleep, wait

Programmers used to insert `time.sleep(5)` and hope the page would finish loading. That's bad: either you wait too long or too little. The right way — **explicit waits**: wait until a condition is met, at most N seconds:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
quote = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote")))
```

Here Selenium waits up to 10 seconds for the element to appear and doesn't waste a single extra millisecond.

## Playwright: a modern alternative

Playwright is a younger tool from the same people who made Puppeteer. Its features: automatic waits (no need to wait for elements manually), a simple synchronous API, and one codebase for Chrome, Firefox, and Safari.

```bash
pip install playwright
playwright install chromium
```

The command `playwright install chromium` downloads the browser itself. First script:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")

    page.wait_for_selector("div.quote")  # wait for quotes
    quotes = page.locator("div.quote")
    print(quotes.count())

    browser.close()
```

`page.locator("div.quote")` — a "locator": a description of elements, not their list. It doesn't search right away, but at the moment of use. Methods: `.count()` — how many elements, `.first` — the first one, `.inner_text()` — text, `.all_inner_texts()` — texts of all.

## Clicks, screenshots, and forms

Playwright can do everything a user does in a browser:

```python
page.locator("input#search").fill("python")
page.locator("button").click()
page.wait_for_selector("div.result")
page.screenshot(path="result.png")
```

`fill()` enters text into a field, `click()` clicks, `wait_for_selector()` waits for the result. Screenshots help debug a scraper: save a picture and see what actually opened in the browser.

## What to choose

For short tasks and a quick start — Playwright: less code, auto-waits, one tool for three browsers. Selenium is useful when you need a mature tool with a huge community or specific scenarios (for example, controlling an already-open browser). The main thing — don't forget to close the browser: in Playwright a `with` block handles it, in Selenium — `driver.quit()`.

## Summary

Dynamic pages are not a death sentence: launch a browser, wait for elements to appear, collect data. Playwright and Selenium provide the same set of superpowers — clicks, form filling, waits, screenshots. Let's practice!

<!--TASK-->
### Task 1

Write your first Playwright script `first_playwright.py`. Using `sync_playwright()`, open `https://quotes.toscrape.com/` in Chromium (headless). After `page.goto()`, wait for the quote blocks to appear via `page.wait_for_selector("div.quote")`, then print the page title via `page.title()` and the number of quotes via `page.locator("div.quote").count()`. Don't forget to close the browser. Expected output: the title `Quotes to Scrape` and the number `10`.

### Task 2

On the page `https://quotes.toscrape.com/` find the quote whose text contains the phrase `The world is a book`. Using `page.locator("div.quote", has_text="The world is a book")` select the quote block, then inside it get the author with `locator("small.author").inner_text()`. Print the author and the full quote text via `locator("span.text").inner_text()`. Expected output: author `Albert Einstein` and the quote text.

### Task 3

Write a program `next_pages.py` that walks through three pages of the quotes site using the "Next" button. Start — `https://quotes.toscrape.com/page/1/`. After each page loads, collect authors via `page.locator("small.author").all_inner_texts()` and add them to a set. Then find the button via `page.locator("li.next a")`, click with `click()` and wait for the next page via `page.wait_for_selector("div.quote")`. At the end, print the number of unique authors across three pages.

### Task 4

Open `https://books.toscrape.com/` in Playwright, wait for the book cards (`article.product_pod`). Take a screenshot of the main page to the file `books.png` via `page.screenshot(path="books.png")`. Then check with `pathlib.Path("books.png").exists()` that the file was created, and print its size in bytes via `.stat().st_size`. Don't forget to close the browser.

### Task 5

Work with a dynamic form. Open `https://demo.playwright.dev/todomvc/` — a JavaScript demo app for a to-do list. Find the input field via `page.locator("input.new-todo")`, enter the text `Buy milk` via `fill()`, press `Enter` via `press("Enter")`. Wait for the list item to appear via `page.wait_for_selector("ul.todo-list li")` and print the number of tasks via `page.locator("ul.todo-list li").count()`. Expected output: `1`.
<!--/TASK-->

<!--HINT-->
### Hint 1

Wrap the work in `with sync_playwright() as p:`. Browser: `browser = p.chromium.launch(headless=True)`, page: `page = browser.new_page()`. `page.wait_for_selector("div.quote")` will wait until the quotes load. `page.title()` — the tab title.

### Hint 2

`page.locator("div.quote", has_text="The world is a book")` searches for the quote block whose text contains that phrase. Author: `quote.locator("small.author").inner_text()`. Text: `quote.locator("span.text").inner_text()`. `inner_text()` returns the visible text of the element.

### Hint 3

Collect the page's authors into a set: `authors.update(page.locator("small.author").all_inner_texts())`. Pagination: find the link `page.locator("li.next a")`, check it exists via `.count() > 0`, click `.click()` and wait for loading: `page.wait_for_selector("div.quote")`. A `for` loop of 3 iterations with `break` if there's no link.

### Hint 4

`page.screenshot(path="books.png")` saves a screenshot. `from pathlib import Path` — `Path("books.png").exists()` returns `True` if the file was created, and `Path("books.png").stat().st_size` — the size in bytes. Take the screenshot after `wait_for_selector` so the page has time to render.

### Hint 5

Entering text into a field: `page.locator("input.new-todo").fill("Buy milk")`. Pressing Enter: `.press("Enter")`. After that the JS app adds a list item. `page.wait_for_selector("ul.todo-list li")` waits for it, then `page.locator("ul.todo-list li").count()` shows the number of tasks.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/")
    page.wait_for_selector("div.quote")

    print("Title:", page.title())
    print("Quotes:", page.locator("div.quote").count())

    browser.close()
```

Step-by-step breakdown:

- `with sync_playwright() as p:` — a context manager: it starts Playwright and guarantees resources are released, even if an exception occurs in the code.
- `p.chromium.launch(headless=True)` launches the browser without a window. `headless=True` — the "invisible" mode, the standard for scrapers.
- `page.goto(...)` opens the address. `page.wait_for_selector("div.quote")` — the key moment: waits until the quote blocks appear on the page. Without it we could count elements before JS renders them.
- `page.title()` returns the tab title — `Quotes to Scrape`.
- `page.locator("div.quote").count()` — the number of quote blocks. A locator doesn't "search" right away; it counts elements at the moment of the call.
- `browser.close()` closes the browser. If you forget — the browser process stays hanging in memory. For reliability, you can use `with browser:` in real projects.

### Solution 2

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com/")
    page.wait_for_selector("div.quote")

    quote = page.locator("div.quote", has_text="The world is a book")
    author = quote.locator("small.author").inner_text()
    text = quote.locator("span.text").inner_text()

    print("Author:", author)
    print("Text:", text)
    browser.close()
```

Step-by-step breakdown:

- `page.locator("div.quote", has_text="The world is a book")` — a locator with a text filter: only those quote blocks whose contents contain that phrase will be selected. It's a convenient alternative to iterating over all quotes and checking conditions in Python.
- `quote.locator("small.author")` — searching inside a specific block. Locators can be nested: the outer one narrows the area, the inner one searches within it.
- `inner_text()` returns the visible text of the element: for the author — `Albert Einstein`, for a quote — the whole text in `span.text`.
- The output confirms the filter worked: Einstein's quote "The world is a book and those who do not travel read only one page" is the first on the page, and the author is indeed Albert Einstein.
- This style — "find the parent block by text, then extract data from it" — is universal for dynamic interfaces: lists, cards, tables.

### Solution 3

```python
from playwright.sync_api import sync_playwright

authors = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for page_num in range(1, 4):
        page.goto(f"https://quotes.toscrape.com/page/{page_num}/")
        page.wait_for_selector("div.quote")
        authors.update(page.locator("small.author").all_inner_texts())

        next_link = page.locator("li.next a")
        if next_link.count() == 0:
            break

    browser.close()

print("Unique authors over 3 pages:", len(authors))
```

Step-by-step breakdown:

- The loop `for page_num in range(1, 4)` goes through pages 1, 2, and 3. The address is built with an f-string — that's what pagination URLs look like on many sites.
- `page.wait_for_selector("div.quote")` after each `goto` — a guarantee that the quotes have loaded.
- `page.locator("small.author").all_inner_texts()` returns a list of texts of all authors on the page. `authors.update(...)` adds them to the set — duplicates vanish automatically.
- `page.locator("li.next a").count()` — the number of "Next" links: 1 if there's a next page, 0 if not. The check protects the loop from going past the last page.
- In the end the set holds the unique authors of three pages. Such "Next"-based pagination is a universal technique — it works in Playwright, Selenium, and BeautifulSoup alike.

### Solution 4

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    page.wait_for_selector("article.product_pod")

    page.screenshot(path="books.png")
    browser.close()

screenshot = Path("books.png")
print("File exists:", screenshot.exists())
print("Size:", screenshot.stat().st_size, "bytes")
```

Step-by-step breakdown:

- `page.wait_for_selector("article.product_pod")` waits until the book cards are rendered — only then will the screenshot contain the whole store.
- `page.screenshot(path="books.png")` saves a picture of the current page state. The format is determined by the file extension.
- `Path("books.png")` from `pathlib` — a path object. `screenshot.exists()` checks the file was actually created; `screenshot.stat().st_size` — the size in bytes. A typical size for such a screenshot is tens-to-hundreds of kilobytes.
- The browser is closed before the file check — the screenshot is already written to disk, so it's safe.
- Screenshots are the main debugging tool for a browser-based scraper: you see what actually opened, not what you expected.

### Solution 5

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://demo.playwright.dev/todomvc/")

    input_box = page.locator("input.new-todo")
    input_box.fill("Buy milk")
    input_box.press("Enter")

    page.wait_for_selector("ul.todo-list li")
    print("Tasks in the list:", page.locator("ul.todo-list li").count())
    browser.close()
```

Step-by-step breakdown:

- TodoMVC is a classic demo of a single-page app: all logic in JavaScript, data doesn't come from the server in HTML. This is exactly the case that requires a browser.
- `page.locator("input.new-todo")` — the field for entering a new task. `fill("Buy milk")` enters text, `press("Enter")` emulates pressing Enter — the app reacts and adds the task to the list.
- `page.wait_for_selector("ul.todo-list li")` waits for the first list item to appear: after Enter some time passes, and without waiting we could see `0`.
- `page.locator("ul.todo-list li").count()` counts tasks. We added one — the output is `1`.
- This is a prototype of real scraping of dynamic interfaces: input field → action → waiting for the result → collecting data. Site search, filters, carts, and infinite feeds are automated the same way.
<!--/SOLUTION-->

<!--QUIZ-->
Why doesn't requests see the content of dynamic pages?
- Because requests doesn't support HTTPS
- Because requests doesn't execute JavaScript
- Because such pages serve only binary data
- It sees everything, the question is wrong
* Correct answer: Because requests doesn't execute JavaScript
The content is created by scripts in the browser, while requests gets only an "empty" shell.

What is the headless mode of a browser?
- The browser runs without a graphical window
- The browser works only with local files
- The browser disables JavaScript
- The browser runs without a network
* Correct answer: The browser runs without a graphical window
Headless mode runs a real browser, but without a window — ideal for scrapers.

Why are explicit waits needed (wait_for_selector, WebDriverWait)?
- To speed up page loading
- To wait for an element to appear instead of sleeping "blindly"
- To replace the browser with requests
- To disable timeouts
* Correct answer: To wait for an element to appear instead of sleeping "blindly"
Waits check a condition (for example, an element appeared) and don't waste extra time.

What does page.locator("div.quote").count() return?
- The first div.quote element
- The number of div.quote elements
- The text of the first div.quote
- The HTML of the whole page
* Correct answer: The number of div.quote elements
count() counts the elements matching the locator.

How do you enter text into a field and press Enter in Playwright?
- field.write() + field.enter()
- locator.fill() + locator.press("Enter")
- locator.set_text() + locator.click()
- locator.type() + locator.submit()
* Correct answer: locator.fill() + locator.press("Enter")
fill() enters text, press("Enter") emulates pressing a key.

What happens if you don't close the browser in Playwright/Selenium?
- Nothing terrible, it will close itself
- The browser process will stay hanging in memory
- The script will crash with an error on every line
- Data will stop being saved
* Correct answer: The browser process will stay hanging in memory
The browser must be closed: browser.close() or driver.quit(). In Playwright a with-block is convenient for this.

What does page.screenshot(path="books.png") do?
- Saves an image of the current page state to the file books.png
- Downloads a picture found on the page
- Prints a screenshot to the console
- Closes the page
* Correct answer: Saves an image of the current page state to the file books.png
Screenshots show what was actually rendered in the browser — the main debugging tool.

Which Playwright method enters text into an input field?
- locator.fill("text")
- locator.write("text")
- locator.type_keys("text")
- locator.input("text")
* Correct answer: locator.fill("text")
fill() sets the field's value, and press("Enter") emulates pressing a key.
<!--/QUIZ-->
