---
title: CSS: styles and selectors
summary: Selectors, properties, box model.
order: 2
duration: 45 min
difficulty: beginner
tags: css
---

CSS styles HTML elements.

## Rules

```css
p {
    color: #333;
    font-size: 16px;
}

.card {
    background: #f5f5f5;
    padding: 12px;
    border-radius: 8px;
}

#title {
    color: blue;
}
```

## Selectors

- p — tag;
- .card — class;
- #title — id.

## Box model

margin → border → padding → content.

## Lesson summary

Selectors + properties style pages.

<!--TASK-->
### Task 1 — Tag
Style all p.

### Task 2 — Class
Style .card.

### Task 3 — Id
Style #title.

### Task 4 — Color
Set text and background.

### Task 5 — Font
Font size and family.

### Task 6 — Box
Padding and margin.

### Task 7 — Border
Rounded border.
<!--/TASK-->

<!--HINT-->
### Hint 1
p {}.

### Hint 2
.card {}.

### Hint 3
#title {}.

### Hint 4
color.

### Hint 5
font-size.

### Hint 6
padding.

### Hint 7
border-radius.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```css
p {
    color: #333;
}
```

### Solution 2
```css
.card {
    background: #f5f5f5;
}
```

### Solution 3
```css
#title {
    color: blue;
}
```

### Solution 4
```css
p { color: #333; background: white; }
```

### Solution 5
```css
p { font-size: 16px; font-family: Arial, sans-serif; }
```

### Solution 6
```css
.card { padding: 16px; margin: 8px; }
```

### Solution 7
```css
.card { border: 1px solid #ccc; border-radius: 8px; }
```
<!--/SOLUTION-->

<!--QUIZ-->
What is CSS?
- Styling
- Markup
- Logic
- None
* Correct answer: Styling
Look.

What is a selector?
- Target
- Property
- Value
- None
* Correct answer: Target
p, .card.

What is a class?
- .name
- #name
- tag
- None
* Correct answer: .name
Reusable.

What is an id?
- #name
- .name
- tag
- None
* Correct answer: #name
Unique.

What is color?
- Text color
- Background
- Border
- None
* Correct answer: Text color
Foreground.

What is font-size?
- Text size
- Color
- Spacing
- None
* Correct answer: Text size
px.

What is padding?
- Inside space
- Outside
- Border
- None
* Correct answer: Inside space
Content.

What is margin?
- Outside space
- Inside
- Border
- None
* Correct answer: Outside space
Between.

What is border?
- Edge line
- Background
- Font
- None
* Correct answer: Edge line
Width.

What is border-radius?
- Rounding
- Thickness
- Color
- None
* Correct answer: Rounding
Corners.

What is the box model?
- margin/border/padding/content
- Colors
- Fonts
- None
* Correct answer: margin/border/padding/content
Layout.

What is a declaration?
- Property: value
- Selector
- Tag
- None
* Correct answer: Property: value
Rule.
<!--/QUIZ-->
