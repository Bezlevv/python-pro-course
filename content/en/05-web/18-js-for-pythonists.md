---
title: JavaScript for Pythonists
summary: DOM, events, fetch, JSON, comparing JS vs Python syntax.
order: 18
duration: 60 min
difficulty: intermediate
tags: javascript, dom, fetch
---

JavaScript runs in the browser; knowing Python helps learn its syntax.

## Variables and strings

```javascript
let name = "Anna";
const age = 21;
console.log(`Hello, ${name}`);
```

## DOM

```javascript
const btn = document.getElementById("btn");
btn.addEventListener("click", () => {
  document.getElementById("out").textContent = "Clicked";
});
```

## fetch

```javascript
fetch("/api/data")
  .then(r => r.json())
  .then(data => console.log(data));
```

## JSON

```javascript
const obj = { name: "Anna" };
const s = JSON.stringify(obj);
const back = JSON.parse(s);
```

## Lesson summary

JS: DOM events, fetch API, JSON; Python helps with syntax mapping.

<!--TASK-->
### Task 1 — Variables
Create let/const and log a template string.

### Task 2 — DOM select
Select an element by id.

### Task 3 — Event
Add a click listener that updates text.

### Task 4 — fetch GET
Fetch /api/data and log the JSON.

### Task 5 — fetch POST
Send a POST with JSON body.

### Task 6 — JSON
Stringify and parse an object.

### Task 7 — Loop
Loop over an array with for..of.
<!--/TASK-->

<!--HINT-->
### Hint 1
let/const; `...`.

### Hint 2
document.getElementById.

### Hint 3
addEventListener("click", ...).

### Hint 4
fetch(url).then(r => r.json()).

### Hint 5
fetch with method: "POST", headers, body.

### Hint 6
JSON.stringify/parse.

### Hint 7
for (const x of arr).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```javascript
let name = "Anna";
const age = 21;
console.log(`Hello, ${name}, ${age}`);
```

### Solution 2
```javascript
const el = document.getElementById("app");
```

### Solution 3
```javascript
const btn = document.getElementById("btn");
btn.addEventListener("click", () => {
  document.getElementById("out").textContent = "Clicked";
});
```

### Solution 4
```javascript
fetch("/api/data")
  .then(r => r.json())
  .then(data => console.log(data));
```

### Solution 5
```javascript
fetch("/api/save", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Anna" })
});
```

### Solution 6
```javascript
const s = JSON.stringify({ a: 1 });
const back = JSON.parse(s);
```

### Solution 7
```javascript
for (const x of [1, 2, 3]) {
  console.log(x);
}
```
<!--/SOLUTION-->

<!--QUIZ-->
What is const?
- Constant binding
- Variable
- Function
- Type
* Correct answer: Constant binding
Cannot reassign.

What is let?
- Block-scoped variable
- Constant
- Global
- Type
* Correct answer: Block-scoped variable
Mutable.

What is the DOM?
- Document Object Model
- A database
- A server
- A style
* Correct answer: Document Object Model
Page tree.

How to select by id?
- document.getElementById("id")
- $("id")
- queryOnly
- getClass
* Correct answer: document.getElementById("id")
Method.

What does addEventListener do?
- Attaches an event
- Fires
- Removes
- Logs
* Correct answer: Attaches an event
Listener.

What is fetch?
- Browser API for HTTP
- A library
- A tag
- A style
* Correct answer: Browser API for HTTP
Promises.

What does .json() return?
- Promise resolving parsed JSON
- String
- Error
- None
* Correct answer: Promise resolving parsed JSON
Chain.

How to send JSON?
- headers + JSON.stringify(body)
- body string only
- query
- form
* Correct answer: headers + JSON.stringify(body)
POST.

What is JSON.stringify?
- Object to string
- String to object
- Clone
- Sort
* Correct answer: Object to string
Serialize.

What is JSON.parse?
- String to object
- Object to string
- Format
- None
* Correct answer: String to object
Parse.

What is a template literal?
- `...${var}...`
- "..." only
- '...'
- <...>
* Correct answer: `...${var}...`
Interpolation.

What is console.log?
- Output
- Return
- Alert
- Fetch
* Correct answer: Output
Debug.
<!--/QUIZ-->
