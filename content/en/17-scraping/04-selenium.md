---
title: Selenium: browser automation
summary: WebDriver, find elements, actions.
order: 4
duration: 50 min
difficulty: advanced
tags: selenium, browser
---

Selenium drives a real browser.

## Setup

```python
from selenium import webdriver
driver = webdriver.Chrome()
```

## Open and find

```python
driver.get("https://example.com")
element = driver.find_element("tag name", "h1")
print(element.text)
```

## Interact

```python
search = driver.find_element("name", "q")
search.send_keys("python")
search.submit()
```

## Cleanup

```python
driver.quit()
```

## Lesson summary

Selenium automates clicks, forms, and checks.

<!--TASK-->
### Task 1 — Start
Open Chrome via WebDriver.

### Task 2 — Navigate
Go to a page.

### Task 3 — Find
Get the h1 text.

### Task 4 — Type
Fill a search field.

### Task 5 — Click
Click a button.

### Task 6 — Wait
Wait for an element.

### Task 7 — Quit
Close the driver.
<!--/TASK-->

<!--HINT-->
### Hint 1
webdriver.Chrome().

### Hint 2
get().

### Hint 3
find_element.

### Hint 4
send_keys.

### Hint 5
click().

### Hint 6
WebDriverWait.

### Hint 7
quit().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from selenium import webdriver
driver = webdriver.Chrome()
```

### Solution 2
```python
driver.get("https://example.com")
```

### Solution 3
```python
h1 = driver.find_element("tag name", "h1")
print(h1.text)
```

### Solution 4
```python
search = driver.find_element("name", "q")
search.send_keys("python")
search.submit()
```

### Solution 5
```python
button = driver.find_element("css selector", "button.submit")
button.click()
```

### Solution 6
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(("css selector", ".result"))
)
```

### Solution 7
```python
driver.quit()
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Selenium?
- Browser automation
- HTML parser
- HTTP client
- None
* Correct answer: Browser automation
Real browser.

What is WebDriver?
- Browser control API
- A browser
- A driver file
- None
* Correct answer: Browser control API
Interface.

What is driver.get?
- Opens URL
- Finds
- Clicks
- None
* Correct answer: Opens URL
Navigate.

What is find_element?
- Locates one
- All
- Clicks
- None
* Correct answer: Locates one
By.

What is send_keys?
- Types text
- Clicks
- Reads
- None
* Correct answer: Types text
Input.

What is click?
- Presses element
- Types
- Waits
- None
* Correct answer: Presses element
Action.

What is a locator?
- How to find
- A call
- A text
- None
* Correct answer: How to find
css/name.

What is WebDriverWait?
- Waits for condition
- Sleeps
- Clicks
- None
* Correct answer: Waits for condition
Sync.

What is EC?
- Expected conditions
- Error
- Element
- None
* Correct answer: Expected conditions
Presence.

What is driver.quit?
- Closes browser
- Refreshes
- Waits
- None
* Correct answer: Closes browser
Cleanup.

What is a dynamic page?
- JS-rendered
- Static
- Empty
- None
* Correct answer: JS-rendered
Selenium.

Why use headers?
- Not needed
- Always
- Faster
- None
* Correct answer: Not needed
Real browser.
<!--/QUIZ-->
