---
title: Exam: Web Scraping and Data Collection
summary: Test your scraping knowledge: HTTP sessions, BeautifulSoup, Selenium/Playwright, pagination, ethics, and collection pipelines.
order: 99
duration: 30 min
difficulty: advanced
tags: exam
exam: true
---

<!--QUIZ-->
Why should a scraper use requests.Session() instead of single requests.get() calls?
- To make requests fly faster
- To keep cookies and other settings between requests
- To bypass blocks automatically
- To avoid specifying timeouts
* Correct answer: To keep cookies and other settings between requests
A session is a container: cookies, headers, and adapters live in it between requests, like in a single "visit".

Why might a scraper fail to get data without the User-Agent header?
- Without it, the server doesn't know who is requesting the page and may serve different content or block the request
- Because without it the request can't be sent
- Because it speeds up the network
- It doesn't affect the result at all
* Correct answer: Without it, the server doesn't know who is requesting the page and may serve different content or block the request
User-Agent identifies the client; an empty or suspicious header is a reason to serve a "trimmed" version or reject the request.

How do you select all elements with the class quote in BeautifulSoup?
- soup.find_all("div", class="quote")
- soup.select("div.quote")
- soup.select_one("div.quote")
- soup.find("div.quote")
* Correct answer: soup.select("div.quote")
select() with a CSS selector returns a list of all matches; .class corresponds to class="quote".

What will soup.find_all("a") return if the page has no links at all?
- None
- An empty list
- An empty string
- An exception
* Correct answer: An empty list
find_all() always returns a list — possibly empty. That's convenient: you can iterate safely.

Why doesn't requests see the content of dynamic pages?
- Because such pages are forbidden to download
- Because requests doesn't execute JavaScript, and the content is created in the browser
- Because requests works only with JSON
- It sees all content without exceptions
* Correct answer: Because requests doesn't execute JavaScript, and the content is created in the browser
Such pages need a real browser: Selenium or Playwright.

What does page.wait_for_selector("div.quote") do in Playwright?
- Slows down page loading
- Waits for the div.quote element to appear, at most for the specified time
- Searches for text inside div.quote
- Takes a screenshot of the page
* Correct answer: Waits for the div.quote element to appear, at most for the specified time
This is an explicit wait: it's more economical than time.sleep() and doesn't "sleep blindly".

Which sign shows that pagination by page numbers has ended?
- The page returned code 200
- The page returned an empty data list
- The page parameter became greater than 50
- The Content-Type header changed
* Correct answer: The page returned an empty data list
An empty batch is a signal of the end; the loop finishes. An artificial page limit is also useful.

What is robots.txt and why check it?
- A file with the site's advertising
- A file with rules about which parts of a site can be crawled
- A file with administrator passwords
- A log of server requests
* Correct answer: A file with rules about which parts of a site can be crawled
Checking via urllib.robotparser.RobotFileParser().can_fetch("*", url) is the first step of a polite scraper.

What does the HTTP code 429 mean and how should you react?
- The page was not found, move on
- Too many requests: you need to wait (Retry-After) and use exponential backoff
- Authorization is required
- A client-side error, retry immediately
* Correct answer: Too many requests: you need to wait (Retry-After) and use exponential backoff
429 is a signal to slow down. The pause grows with each attempt so as not to overload the server.

How do you keep duplicates out of the database in SQLite when the program is run again?
- Use csv.DictWriter
- Set UNIQUE(text, author) and insert via INSERT OR IGNORE
- Check count before each insertion
- Use only SELECT, without INSERT
* Correct answer: Set UNIQUE(text, author) and insert via INSERT OR IGNORE
A uniqueness constraint at the table level + IGNORE skips already-existing rows.
<!--/QUIZ-->
