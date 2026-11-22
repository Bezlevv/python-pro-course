---
title: Exam: Layout and templates
summary: Final check for the module "Layout and Templates: HTML, CSS, Jinja".
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, html, css, jinja2
---

<!--QUIZ-->
Which tag should appear exactly once on a page and contain the main content?
- main
- header
- section
* Correct answer: main
main is the page's main content; there must be exactly one such tag.

What does the aria-label attribute do?
- Gives the element an accessible name that the screen reader announces
- Adds a tooltip on hover
- Changes the element's color
* Correct answer: Gives the element an accessible name that the screen reader announces
aria-label names an element for assistive technologies when there is no visible text.

Which input attribute makes the browser check the email format?
- type="email"
- pattern="email"
- format="email"
* Correct answer: type="email"
type="email" makes the browser check that the value looks like an email.

Why is server-side validation needed if client-side exists?
- Client-side checks can be bypassed, so the server must re-check the data
- To speed up the browser
- It isn't needed
* Correct answer: Client-side checks can be bypassed, so the server must re-check the data
Browser checks are bypassed with a direct request, so server-side validation is mandatory.

How do you declare and use a CSS variable?
- :root { --color: #000; } and background: var(--color);
- $color: #000; and background: $color;
- define color #000; and use color
* Correct answer: :root { --color: #000; } and background: var(--color);
Variables are declared with --name and used via var(--name).

What does transition do?
- Smoothly animates property changes between states
- Changes the color instantly
- Creates a new page
* Correct answer: Smoothly animates property changes between states
transition sets a smooth change when a property value switches.

What does grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)) do?
- Creates a responsive grid: as many columns as fit
- Creates exactly three columns
- Forbids column wrapping
* Correct answer: Creates a responsive grid: as many columns as fit
auto-fit counts columns by width; minmax sets the minimum size of each.

Which Jinja2 operator handles template inheritance?
- {% extends %}
- {% include %}
- {% macro %}
* Correct answer: {% extends %}
{% extends "base.html" %} attaches the parent template, and it must be the first line.

What does the filter {{ value|default("none") }} do?
- Returns "none" if value is not set (or empty)
- Uppercases the text
- Deletes the value
* Correct answer: Returns "none" if value is not set (or empty)
default substitutes a default value when the variable is absent.

What does autoescape=True do in Jinja2?
- Enables output escaping: HTML tags become safe text
- Disables type checks
- Speeds up rendering
* Correct answer: Enables output escaping: HTML tags become safe text
autoescape neutralizes XSS by turning special characters into entities.
<!--/QUIZ-->
