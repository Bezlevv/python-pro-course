---
title: Web: sites, APIs, parsers
summary: Three paths on the web: sites with Django, Flask, FastAPI, talking to APIs, and collecting data with parsers. A live example of a request to a real public API.
order: 3
duration: 30 min
difficulty: beginner
tags: web, api, scraping, django, flask, fastapi, json
---

## The web is three superpowers

The internet is the biggest place where Python works. And there are three main directions:

1. **Building sites** — from a blog to a marketplace like Amazon.
2. **APIs** — the "language of communication" between programs: your code asks a service for data, the service answers.
3. **Parsers** — programs that collect data from web pages (prices, news, listings).

Today we'll open all three doors — and even write code that talks to a real server on the internet.

## Sites: Django, Flask, FastAPI

To make a site, you don't need to write a low-level server by hand. Python gives ready-made frameworks:

- **Django** — the "heavy artillery": everything included, admin panel, database, security. Instagram runs on Django (the largest project on this framework).
- **Flask** — light and minimalist: starts in five minutes, ideal for small services and learning projects.
- **FastAPI** — modern and fast: automatic documentation, excellent API support.

A minimal Flask site looks like this:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, world! This is my Flask site."

if __name__ == "__main__":
    app.run()
```

Install Flask (`pip install flask`), run it — and open `http://127.0.0.1:5000` in your browser. You just created a real website.

## APIs: programs talk to each other

An API (Application Programming Interface) is a set of rules by which programs exchange data. When you open a weather app, it asks the weather service's API for data. When you pay with a card, the payment service calls the bank's API.

Data is usually transferred in **JSON** format — a convenient text format that looks like Python dictionaries:

```json
{"userId": 1, "id": 1, "title": "Wash the dishes", "completed": false}
```

## Demo: a live request to a real API

Let's write a program that asks a real public API — JSONPlaceholder (a test service for learning). Python has a built-in module `urllib.request` that can reach the internet without installing anything:

```python
import json
import urllib.request

url = "https://jsonplaceholder.typicode.com/todos/1"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

print("Task:", data["title"])
print("Completed:", data["completed"])
```

What happens here? `urlopen(url)` opens a connection to the server and gets the response. `response.read()` reads the response body (text in JSON format), and `json.loads()` turns it into a Python dictionary. Then we access data by keys like a normal dictionary: `data["title"]`. If you have internet, you'll see the first task in the todo list. If there is no network, the program honestly reports an error — but the code is still a real API client.

## Parsers: collecting data from sites

A parser is a program that visits pages, extracts the needed data, and organizes it. Parsers are used for price monitoring, news collection, and analyzing listings.

Essentially a parser does the same as our API request: it gets a page, but instead of just printing JSON, it searches the text for the needed fragments. For complex pages people use the `BeautifulSoup` library — it can parse HTML and extract elements. It works roughly like this:

```python
# Simplified scheme: we got the page HTML
html = "<h1>Hello</h1><p>Price: 999 rub.</p>"

# This can be done via BeautifulSoup, but we'll just search the text
if "999 rub." in html:
    print("Found the price: 999 rub.")
```

## Parsing etiquette

Before writing a parser, remember three rules:

- **Read the site's rules.** Don't collect data the site forbids collecting.
- **Don't overload the server.** Pause between requests; don't "hammer" the site with thousands of requests per second.
- **Use the API if it exists.** If the site has a public API, it's always better and more legal than scraping.

## Lesson summary

Today we learned:

- that sites in Python are made with Django, Flask, and FastAPI;
- that an API is the language programs speak, and JSON is the main data format;
- how to write a real API request with `urllib.request`;
- what parsers are and why they're needed;
- how to collect data ethically and safely.

Now let's connect to the real internet.

<!--TASK-->
### Task 1
Write a program `post_fetcher.py` that requests post number 1 from JSONPlaceholder (address: `https://jsonplaceholder.typicode.com/posts/1`) and prints the post's title and body. Use `urllib.request` and `json.loads()` as in the lesson example. The JSON fields are `title` and `body`. Run the program — with internet you'll see the title and text of a real post.

### Task 2
Write a program `todo_stats.py` that gets the first 5 todos from JSONPlaceholder (`https://jsonplaceholder.typicode.com/todos/1` … `/todos/5`) and counts how many are completed (the `completed` field equals `True`). Print each todo with a `[x]` mark for completed and `[ ]` for not completed, and at the end print `Completed: N of 5`. Hint: you can request each number in a loop `for i in range(1, 6):`.

### Task 3
Write a program `user_posts.py` that gets the list of posts of user with id = 1 from JSONPlaceholder (address: `https://jsonplaceholder.typicode.com/posts?userId=1`) and prints their count and titles. Note: the response is not a dictionary but a list of dictionaries, so iterate over it with a loop. At the end print `Total posts: N`.

### Task 4
Write a program `json_explorer.py` that takes the following JSON string (an API response) and parses it without the internet: `{"name": "Python", "year": 1991, "creator": "Guido van Rossum", "popular": true}`. The program should print the language name, the creation year, and the word `popular` or `not very popular` depending on the `popular` field. Use `json.loads()` and key access.

### Task 5
Write a mini-API without a network: a function `my_api(request)` that takes a dictionary-"request" with an `action` key and returns a dictionary-"response". If `action == "hello"` — return `{"message": "Hello, world!"}`, if `action == "time"` — return `{"time": "now 12:00"}` (you can replace it with the current time via datetime), for anything else — `{"error": "Unknown action"}`. Call the function for all three actions and print the responses.
<!--/TASK-->

<!--HINT-->
### Hint 1
Add `import json` and `import urllib.request`. Run `with urllib.request.urlopen("https://jsonplaceholder.typicode.com/posts/1") as response:` and read `data = json.loads(response.read())`. The `title` and `body` fields are dictionary keys. Print them with `print(data["title"])` and `print(data["body"])`.

### Hint 2
Wrap the request in a loop: `for i in range(1, 6):` and build the URL inside with an f-string: `f"https://jsonplaceholder.typicode.com/todos/{i}"`. The `completed` field is boolean: `True` or `False`. Keep a counter of completed ones and add one when `data["completed"]` is truthy. For marks use `print("[x]", data["title"])` or `print("[ ]", data["title"])`.

### Hint 3
A request to `https://jsonplaceholder.typicode.com/posts?userId=1` returns a list. Read it: `posts = json.loads(response.read())`. Then `print("Total posts:", len(posts))` and a loop `for post in posts:` printing `post["title"]`. If the response unexpectedly turns out to be a dictionary, check the URL — the `?` sign may be missing.

### Hint 4
You can wrap the JSON string in triple quotes `"""..."""` or use single quotes inside double ones. `data = json.loads(text)` returns a dictionary. Field access: `data["name"]`, `data["year"]`, `data["popular"]`. For `popular` write an `if data["popular"]:` condition — it fires when the value is `True`.

### Hint 5
Define the function: `def my_api(request):`. Inside, check `request["action"]` with `if / elif / else`. For time you can use `from datetime import datetime` and `datetime.now().strftime("%H:%M")`. Call: `print(my_api({"action": "hello"}))` and so on. Note: the function must return a dictionary; you print it from outside.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import json
import urllib.request

url = "https://jsonplaceholder.typicode.com/posts/1"
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read())

print("Title:", data["title"])
print("Body:", data["body"])
```

Result (abbreviated):

```
Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
Body: quia et suscipit ...
```

What happens here? `urllib.request.urlopen(url)` opens a connection to the server. The `with` statement guarantees the connection closes even if an error occurs. `response.read()` returns the response bytes — in our case JSON text. `json.loads()` turns it into a Python dictionary. Then `data["title"]` and `data["body"]` are plain dictionary access. Congratulations: you wrote a full API client — the same kind of program apps use to show you news or weather.

### Solution 2
Solution:

```python
import json
import urllib.request

done = 0
for i in range(1, 6):
    url = f"https://jsonplaceholder.typicode.com/todos/{i}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read())
    mark = "[x]" if data["completed"] else "[ ]"
    print(mark, data["title"])
    if data["completed"]:
        done += 1

print("Completed:", done, "of 5")
```

Result:

```
[ ]  delectus aut autem
[x]  quis ut nam facilis et officia qui
[ ]  fugiat veniam minus
[ ]  et porro tempora
[x]  laboriosam mollitia et enim quasi adipisci quia provident illum
Completed: 2 of 5
```

What happens here? The f-string `f"...todos/{i}"` inserts the task number into the URL. The ternary operator `"[x]" if data["completed"] else "[ ]"` is a short condition: if `completed` is truthy we take `[x]`, otherwise `[ ]`. The `done` counter increases only for completed tasks. This way we automatically collected and processed data about five tasks — the same principle powers dashboards and reports that gather statistics from different sources.

### Solution 3
Solution:

```python
import json
import urllib.request

url = "https://jsonplaceholder.typicode.com/posts?userId=1"
with urllib.request.urlopen(url) as response:
    posts = json.loads(response.read())

print("Total posts:", len(posts))
for post in posts:
    print("-", post["title"])
```

Result (fragment):

```
Total posts: 10
- sunt aut facere repellat ...
- qui est esse
- ea molestias quasi exercitationem repellat qui ipsa sit aut
...
```

What happens here? The `?` sign in the URL starts query parameters: `userId=1` tells the server "return posts of user 1 only". The server returns not one object but a **list** of objects. `len(posts)` counts them, and the loop `for post in posts:` iterates each post and prints its title. Note: APIs often return lists, and working with them is a key skill for any web developer. Query parameters are how apps pass filtering conditions to servers.

### Solution 4
Solution:

```python
import json

text = '{"name": "Python", "year": 1991, "creator": "Guido van Rossum", "popular": true}'
data = json.loads(text)

print("Language:", data["name"])
print("Year:", data["year"])
if data["popular"]:
    print("Status: popular")
else:
    print("Status: not very popular")
```

Result:

```
Language: Python
Year: 1991
Status: popular
```

What happens here? In triple quotes the JSON text can be stored whole, including double quotes. `json.loads(text)` — "load from string" (s from string) — turns text into a dictionary. Note `true` in JSON: it automatically becomes boolean `True` in Python. The condition `if data["popular"]:` works directly with that value. So we learned to parse API responses even without the internet — a way to practice your skills on any data.

### Solution 5
Solution:

```python
from datetime import datetime

def my_api(request):
    if request["action"] == "hello":
        return {"message": "Hello, world!"}
    elif request["action"] == "time":
        now = datetime.now().strftime("%H:%M")
        return {"time": now}
    else:
        return {"error": "Unknown action"}

print(my_api({"action": "hello"}))
print(my_api({"action": "time"}))
print(my_api({"action": "magic"}))
```

Result:

```
{'message': 'Hello, world!'}
{'time': '14:35'}
{'error': 'Unknown action'}
```

What happens here? The `my_api` function is a model of a real API: it takes a request (dictionary) and returns a response (also a dictionary). Inside is routing: depending on `action` we choose what to answer. This is how hundreds of real services work: a request arrives — we parse it — we return a JSON answer. Eventually you'll replace `my_api` with Flask or FastAPI, and your function will become a real web service available at an internet address.
<!--/SOLUTION-->

<!--QUIZ-->
What is an API?
- Rules by which programs exchange data
- A page markup language
- A program for drawing interfaces
* Correct answer: Rules by which programs exchange data
An API is an interface through which one program requests data from another.

In what format is data usually transferred via APIs?
- JSON
- DOCX
- MP3
* Correct answer: JSON
JSON is a text data exchange format similar to Python dictionaries.

What does json.loads(text) do?
- Turns JSON text into Python objects (dictionary/list)
- Turns Python objects into JSON text
- Prints text nicely
* Correct answer: Turns JSON text into Python objects (dictionary/list)
json.loads() parses a JSON string and creates Python dictionaries and lists.

Which Python module makes HTTP requests without installing extra libraries?
- urllib.request
- turtle
- math
* Correct answer: urllib.request
urllib.request is part of the standard library and can access URLs.

What does urlopen(url) do?
- Opens a connection to the server and returns the response
- Creates a new browser tab
- Checks internet speed
* Correct answer: Opens a connection to the server and returns the response
urlopen() makes a request to the server and returns a response object.

Django, Flask, and FastAPI are...
- Frameworks for building web applications
- Code editors
- Databases
* Correct answer: Frameworks for building web applications
They are scaffolds that handle the server work so you only write the application logic.

What is a parser?
- A program that collects data from web pages
- A program that fixes the internet
- A programming language
* Correct answer: A program that collects data from web pages
A parser visits pages and extracts the needed data from them.

What is the `userId` parameter in the address /posts?userId=1 useful for?
- It filters the response: only that user's posts are returned
- It speeds up the internet
- It hides the page address
* Correct answer: It filters the response: only that user's posts are returned
Query parameters after the ? sign pass data selection conditions to the server.

What will an API return if you request a list of items?
- A list of dictionaries
- A single number
- An HTML string
* Correct answer: A list of dictionaries
Lists of objects arrive in JSON as arrays, which become Python lists.

How should you treat scraping other people's sites?
- Respect the site's rules, pause, and prefer the API
- You can download any data without limits
- Scraping is banned everywhere
* Correct answer: Respect the site's rules, pause, and prefer the API
Ethical scraping means following the site's rules and keeping the load manageable for the server.
<!--/QUIZ-->
