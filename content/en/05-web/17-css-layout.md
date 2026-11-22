---
title: CSS in depth: Flexbox, Grid, responsive
summary: Layout with Flexbox and Grid, media queries, variables.
order: 17
duration: 50 min
difficulty: intermediate
tags: css, flexbox, grid, responsive
---

Modern layouts use Flexbox and Grid; responsive design adapts screens.

## Flexbox

```css
.container {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
}
```

## Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
```

## Media queries

```css
@media (max-width: 600px) {
  .grid { grid-template-columns: 1fr; }
}
```

## Variables

```css
:root {
  --main-color: #7c5cff;
}
.button { background: var(--main-color); }
```

## Lesson summary

Flexbox for one-dimensional layout, Grid for two, media queries for responsiveness.

<!--TASK-->
### Task 1 — Flex
Center three boxes with flex.

### Task 2 — Gap
Use gap for spacing.

### Task 3 — Grid
Create a 3-column grid.

### Task 4 — Responsive
Change to 1 column under 600px.

### Task 5 — Variables
Define a color variable and use it.

### Task 6 — Align
Align items with align-items.

### Task 7 — Auto-fit
Use minmax with auto-fit for adaptive columns.
<!--/TASK-->

<!--HINT-->
### Hint 1
display: flex; justify-content: center.

### Hint 2
gap: 12px.

### Hint 3
grid-template-columns: repeat(3, 1fr).

### Hint 4
@media.

### Hint 5
:root vars.

### Hint 6
align-items: center.

### Hint 7
repeat(auto-fit, minmax(150px, 1fr)).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```css
.container {
  display: flex;
  justify-content: center;
  gap: 12px;
}
```

### Solution 2
```css
.container { gap: 12px; }
```

### Solution 3
```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
```

### Solution 4
```css
@media (max-width: 600px) {
  .grid { grid-template-columns: 1fr; }
}
```

### Solution 5
```css
:root { --main: #7c5cff; }
.button { background: var(--main); }
```

### Solution 6
```css
.container {
  display: flex;
  align-items: center;
}
```

### Solution 7
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
```
<!--/SOLUTION-->

<!--QUIZ-->
What does display:flex do?
- Flex layout
- Grid
- None
- Block
* Correct answer: Flex layout
Row/column.

What is justify-content?
- Main axis alignment
- Cross axis
- Gap
- Order
* Correct answer: Main axis alignment
Position.

What is align-items?
- Cross axis alignment
- Main axis
- Gap
- Size
* Correct answer: Cross axis alignment
Vertical.

What does gap do?
- Space between items
- Padding
- Margin
- Border
* Correct answer: Space between items
Spacing.

What is display:grid?
- Grid layout
- Flex
- Block
- Inline
* Correct answer: Grid layout
Two-dimensional.

What are grid-template-columns?
- Column tracks
- Rows
- Gap
- Align
* Correct answer: Column tracks
Sizes.

What is repeat(3, 1fr)?
- 3 equal columns
- 1 column
- 3 rows
- None
* Correct answer: 3 equal columns
Fraction units.

What is a media query?
- Responsive breakpoint
- A style
- A layout
- A color
* Correct answer: Responsive breakpoint
@media.

What are CSS variables?
- Custom properties
- Constants
- Classes
- IDs
* Correct answer: Custom properties
--name.

What does minmax do?
- Min/max track size
- Fixed
- Auto
- None
* Correct answer: Min/max track size
Adaptive.

What does auto-fit do?
- Fits as many columns
- One
- Fixed three
- Zero
* Correct answer: Fits as many columns
Responsive grid.

What does 1fr mean?
- One fraction
- One pixel
- One row
- Flex
* Correct answer: One fraction
Unit.
<!--/QUIZ-->
