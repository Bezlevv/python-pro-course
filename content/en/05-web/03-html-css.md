---
title: Basics of HTML and CSS
summary: HTML tags, attributes, CSS selectors, box model basics.
order: 3
duration: 40 min
difficulty: beginner
tags: html, css
---

HTML gives structure; CSS gives style.

## HTML skeleton

```html
<!DOCTYPE html>
<html>
<head><title>Page</title></head>
<body>
  <h1>Hello</h1>
  <p>Text</p>
</body>
</html>
```

## Common tags

h1-h6, p, a, img, ul/li, div, span, form.

## Attributes

```html
<a href="https://example.com">link</a>
<img src="pic.png" alt="pic">
```

## CSS

```css
h1 { color: blue; }
.container { max-width: 800px; }
#main { padding: 10px; }
```

Selectors: element, .class, #id.

## Box model

margin, border, padding, content.

## Lesson summary

HTML markup + CSS styling; selectors and box model are core.

<!--TASK-->
### Task 1 — Page
Create a minimal HTML page with title and h1.

### Task 2 — Tags
Add p, a, img, ul with 2 items.

### Task 3 — Attributes
Set href, src, alt attributes.

### Task 4 — CSS color
Style h1 red via a <style> tag.

### Task 5 — Class selector
Add .highlight class and style it.

### Task 6 — ID selector
Add #main id and set width.

### Task 7 — Box model
Set margin, padding, border on a div.
<!--/TASK-->

<!--HINT-->
### Hint 1
<!DOCTYPE html> skeleton.

### Hint 2
Semantic tags.

### Hint 3
href, src, alt.

### Hint 4
<style>h1{color:red}</style>.

### Hint 5
.class selector.

### Hint 6
#id selector.

### Hint 7
margin/padding/border.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```html
<!DOCTYPE html>
<html>
<head><title>My Page</title></head>
<body><h1>Hello</h1></body>
</html>
```

### Solution 2
```html
<p>Paragraph</p>
<a href="https://example.com">Link</a>
<img src="pic.png" alt="pic">
<ul><li>One</li><li>Two</li></ul>
```

### Solution 3
```html
<a href="https://example.com">site</a>
<img src="logo.png" alt="Logo">
```

### Solution 4
```html
<style>h1 { color: red; }</style>
<h1>Red title</h1>
```

### Solution 5
```html
<style>.highlight { background: yellow; }</style>
<p class="highlight">Text</p>
```

### Solution 6
```html
<style>#main { width: 600px; }</style>
<div id="main">...</div>
```

### Solution 7
```html
<style>div.box { margin: 10px; padding: 20px; border: 1px solid black; }</style>
<div class="box">Content</div>
```
<!--/SOLUTION-->

<!--QUIZ-->
What does HTML define?
- Structure
- Style
- Logic
- Data
* Correct answer: Structure
Markup.

What does CSS define?
- Style
- Structure
- Scripts
- Forms
* Correct answer: Style
Presentation.

Which tag is a heading?
- h1
- p
- a
- img
* Correct answer: h1
Heading.

Which tag is a link?
- a
- p
- div
- ul
* Correct answer: a
Anchor.

What is an attribute?
- name="value"
- A tag
- Text
- CSS
* Correct answer: name="value"
Config.

What is a class selector?
- .name
- #name
- name
- tag
* Correct answer: .name
Dot.

What is an id selector?
- #name
- .name
- tag
- none
* Correct answer: #name
Hash.

What is the box model?
- margin, border, padding, content
- Colors
- Fonts
- Tags
* Correct answer: margin, border, padding, content
Layout.

What is padding?
- Inner space
- Outer space
- Border
- Content
* Correct answer: Inner space
Around content.

What is margin?
- Outer space
- Inner
- Border
- Size
* Correct answer: Outer space
Outside border.

How to include CSS?
- <style> or external link
- In Python
- In HTML attributes only
- Nowhere
* Correct answer: <style> or external link
Standard.

What is div?
- A block container
- A link
- An image
- A heading
* Correct answer: A block container
Layout block.
<!--/QUIZ-->
