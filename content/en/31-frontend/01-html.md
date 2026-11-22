---
title: HTML basics
summary: Elements, attributes, structure.
order: 1
duration: 40 min
difficulty: beginner
tags: html
---

HTML structures web pages.

## Skeleton

```html
<!DOCTYPE html>
<html>
<head>
  <title>Page</title>
</head>
<body>
  <h1>Hello</h1>
  <p>Text</p>
  <a href="https://example.com">Link</a>
</body>
</html>
```

## Common tags

h1–h6, p, a, img, ul/ol, div, span.

## Lesson summary

Tags + attributes form a page.

<!--TASK-->
### Task 1 — Skeleton
Write a full page.

### Task 2 — Heading
Add h1 and h2.

### Task 3 — Link
Add an anchor.

### Task 4 — Image
Add an img.

### Task 5 — Lists
Add ul and ol.

### Task 6 — Div
Group with div.

### Task 7 — Comment
Add an HTML comment.
<!--/TASK-->

<!--HINT-->
### Hint 1
DOCTYPE.

### Hint 2
h1.

### Hint 3
a.

### Hint 4
img.

### Hint 5
ul.

### Hint 6
div.

### Hint 7
<!-- -->.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```html
<!DOCTYPE html>
<html>
<head><title>Page</title></head>
<body></body>
</html>
```

### Solution 2
```html
<h1>Main title</h1>
<h2>Section</h2>
```

### Solution 3
```html
<a href="https://example.com">Example</a>
```

### Solution 4
```html
<img src="photo.jpg" alt="Photo">
```

### Solution 5
```html
<ul><li>One</li><li>Two</li></ul>
<ol><li>First</li><li>Second</li></ol>
```

### Solution 6
```html
<div class="card">
  <p>Card content</p>
</div>
```

### Solution 7
```html
<!-- это комментарий -->
```
<!--/SOLUTION-->

<!--QUIZ-->
What is HTML?
- Markup
- Scripting
- Styling
- None
* Correct answer: Markup
Structure.

What is a tag?
- Element
- Attribute
- Text
- None
* Correct answer: Element
<p>.

What is an attribute?
- Extra info
- Tag
- Text
- None
* Correct answer: Extra info
href.

What is href?
- Link target
- Image
- Style
- None
* Correct answer: Link target
URL.

What is src?
- Source
- Link
- Class
- None
* Correct answer: Source
Image.

What is alt?
- Alternative text
- Link
- Size
- None
* Correct answer: Alternative text
Accessibility.

What is h1?
- Main heading
- Paragraph
- Link
- None
* Correct answer: Main heading
Title.

What is p?
- Paragraph
- Heading
- List
- None
* Correct answer: Paragraph
Text.

What is ul?
- Unordered list
- Ordered
- Link
- None
* Correct answer: Unordered list
Bullets.

What is ol?
- Ordered list
- Unordered
- Table
- None
* Correct answer: Ordered list
Numbers.

What is div?
- Block container
- Text
- Link
- None
* Correct answer: Block container
Group.

What is a comment?
- Hidden note
- Visible
- Tag
- None
* Correct answer: Hidden note
<!-- -->.
<!--/QUIZ-->
