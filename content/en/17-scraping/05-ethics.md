---
title: Ethics and legality of scraping
summary: robots.txt, ToS, rate limits, privacy.
order: 5
duration: 40 min
difficulty: intermediate
tags: ethics, robots, scraping
---

Scrape responsibly and legally.

## robots.txt

```text
User-agent: *
Disallow: /private/
```

Check the site's robots.txt first.

## Rules

- Respect robots.txt and rate limits;
- Read Terms of Service;
- Identify yourself with a User-Agent;
- Do not store personal data.

## Lesson summary

Legal scraping is respectful and limited.

<!--TASK-->
### Task 1 — robots
Explain what robots.txt does.

### Task 2 — Check
Look up robots.txt for a site (in comments).

### Task 3 — Rate
Why delay between requests?

### Task 4 — ToS
Why read Terms of Service?

### Task 5 — UA
Set an honest User-Agent.

### Task 6 — Data
What data should not be stored?

### Task 7 — Ethical
List three ethical rules.
<!--/TASK-->

<!--HINT-->
### Hint 1
Rules.

### Hint 2
robots.txt.

### Hint 3
Don't overload.

### Hint 4
Permission.

### Hint 5
Identify.

### Hint 6
Personal.

### Hint 7
Respect.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```text
robots.txt — правила для поисковых роботов:
какие пути можно и нельзя сканировать
```

### Solution 2
```python
# import requests
# r = requests.get("https://example.com/robots.txt")
# print(r.text)
```

### Solution 3
```python
# Между запросами нужна пауза,
# чтобы не перегружать сервер
```

### Solution 4
```python
# Условия использования сайта определяют
# разрешён ли парсинг и как
```

### Solution 5
```python
headers = {"User-Agent": "MyScraper/1.0 (contact@example.com)"}
```

### Solution 6
```python
# Персональные данные, пароли, закрытые
# и защищённые авторским правом материалы
```

### Solution 7
```text
— Соблюдать robots.txt и лимиты
— Не собирать личные данные
— Указывать контакты и цель
```
<!--/SOLUTION-->

<!--QUIZ-->
What is robots.txt?
- Crawling rules
- A login
- An API
- None
* Correct answer: Crawling rules
Policy.

What is Disallow?
- Forbidden path
- Allowed
- Required
- None
* Correct answer: Forbidden path
Rule.

What is a rate limit?
- Requests per time
- A file
- A header
- None
* Correct answer: Requests per time
Delay.

Why delay?
- Be polite
- Faster
- Required
- None
* Correct answer: Be polite
Load.

What is ToS?
- Terms of Service
- Text only
- A login
- None
* Correct answer: Terms of Service
Legal.

What is a User-Agent?
- Client identity
- A password
- A cookie
- None
* Correct answer: Client identity
Header.

What is personal data?
- Private info
- Public text
- HTML
- None
* Correct answer: Private info
Protect.

What is consent?
- Permission
- Ignoring
- Required only
- None
* Correct answer: Permission
Ethics.

What is overloading?
- Too many requests
- Few
- Normal
- None
* Correct answer: Too many requests
Harm.

What is caching?
- Storing results
- Re-scraping
- Ignoring
- None
* Correct answer: Storing results
Politeness.

What is legality?
- Law compliance
- Speed
- Style
- None
* Correct answer: Law compliance
Must.

What is the best practice?
- Check rules + limit + identify
- Scrape all
- Ignore
- None
* Correct answer: Check rules + limit + identify
Ethical.
<!--/QUIZ-->
