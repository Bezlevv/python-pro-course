---
title: HTMX and Alpine.js
summary: Server-driven UI with HTMX and lightweight reactivity with Alpine.
order: 15
duration: 45 min
difficulty: intermediate
tags: htmx, alpine, frontend
---

HTMX adds AJAX via HTML attributes; Alpine adds small interactivity.

## HTMX

```html
<button hx-get="/more" hx-target="#list" hx-swap="innerHTML">
  Load more
</button>
<div id="list">...</div>
```

Attributes: hx-get, hx-post, hx-target, hx-swap.

## Alpine

```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <p x-show="open">Hidden now shown</p>
</div>
```

## In Flask/FastAPI

An endpoint returns HTML fragments that HTMX swaps.

## Lesson summary

HTMX: minimal JS, server returns fragments; Alpine: small state.

<!--TASK-->
### Task 1 — hx-get
Create a button that loads /more into #list.

### Task 2 — hx-target
Target a div by id.

### Task 3 — hx-swap
Swap with innerHTML.

### Task 4 — hx-post
Post a form without reload.

### Task 5 — Alpine state
Use x-data with a counter.

### Task 6 — Alpine show
Toggle visibility with x-show.

### Task 7 — Fragment endpoint
Write a route returning an HTML fragment.
<!--/TASK-->

<!--HINT-->
### Hint 1
hx-get="/more".

### Hint 2
hx-target="#list".

### Hint 3
hx-swap="innerHTML".

### Hint 4
hx-post="/save".

### Hint 5
x-data="{ count: 0 }".

### Hint 6
x-show.

### Hint 7
Return HTML string.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```html
<button hx-get="/more" hx-target="#list">Load</button>
<div id="list"></div>
```

### Solution 2
```html
<button hx-get="/more" hx-target="#list" hx-swap="innerHTML">Load</button>
```

### Solution 3
```html
<div id="list" hx-swap="innerHTML"></div>
```

### Solution 4
```html
<form hx-post="/save" hx-target="#result">
  <input name="q">
  <button>Save</button>
</form>
<div id="result"></div>
```

### Solution 5
```html
<div x-data="{ count: 0 }">
  <button @click="count++">+</button>
  <span x-text="count"></span>
</div>
```

### Solution 6
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <p x-show="open">Now visible</p>
</div>
```

### Solution 7
```python
@app.get("/more")
def more():
    return "<p>More items</p>"
```
<!--/SOLUTION-->

<!--QUIZ-->
What does hx-get do?
- Fetches via AJAX
- Submits form
- Hides
- Styles
* Correct answer: Fetches via AJAX
GET.

What is hx-target?
- Where to place result
- URL
- Method
- Data
* Correct answer: Where to place result
Selector.

What is hx-swap?
- How to swap content
- What to send
- When
- Where
* Correct answer: How to swap content
innerHTML etc.

What is hx-post?
- AJAX POST
- GET
- Delete
- Put
* Correct answer: AJAX POST
Submit.

What does HTMX minimize?
- JavaScript
- HTML
- Python
- CSS
* Correct answer: JavaScript
Attributes.

What is Alpine.js?
- Lightweight JS framework
- Server
- ORM
- Template
* Correct answer: Lightweight JS framework
Interactivity.

What is x-data?
- Component state
- URL
- Method
- Event
* Correct answer: Component state
{}.

What does @click do?
- Click listener
- Style
- Fetch
- Loop
* Correct answer: Click listener
Event.

What does x-show do?
- Toggles visibility
- Fetches
- Posts
- Counts
* Correct answer: Toggles visibility
Based on state.

What does x-text do?
- Sets text content
- Sets HTML
- Hides
- Styles
* Correct answer: Sets text content
Binding.

What does a fragment endpoint return?
- HTML snippet
- Full page
- JSON
- File
* Correct answer: HTML snippet
Swapped.

Which attribute replaces a full page reload?
- hx-swap
- hx-post
- x-show
- @click
* Correct answer: hx-swap
Partial update.
<!--/QUIZ-->
