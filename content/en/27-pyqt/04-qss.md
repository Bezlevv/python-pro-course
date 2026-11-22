---
title: Styling with QSS
summary: Style sheets, selectors, properties.
order: 4
duration: 40 min
difficulty: intermediate
tags: pyqt, qss
---

QSS styles Qt widgets like CSS.

## Set style

```python
app.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
""")
```

## Selectors

- QPushButton — by type;
- #id — object name;
- QLabel#title — combined.

## Lesson summary

QSS: selectors + properties.

<!--TASK-->
### Task 1 — Button
Style a button.

### Task 2 — Hover
Add hover state.

### Task 3 — Object name
Style by objectName.

### Task 4 — Window
Set background.

### Task 5 — Font
QSS font size.

### Task 6 — Border
Rounded corners.

### Task 7 — Theme
Dark theme snippet.
<!--/TASK-->

<!--HINT-->
### Hint 1
QPushButton.

### Hint 2
:hover.

### Hint 3
#btn.

### Hint 4
QWidget.

### Hint 5
font-size.

### Hint 6
border-radius.

### Hint 7
Background.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
app.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
    }
""")
```

### Solution 2
```python
QPushButton:hover { background-color: #45a049; }
```

### Solution 3
```python
button.setObjectName("saveBtn")
# QSS: #saveBtn { font-weight: bold; }
```

### Solution 4
```python
QWidget { background-color: #f0f0f0; }
```

### Solution 5
```python
QLabel { font-size: 16px; }
```

### Solution 6
```python
QPushButton { border-radius: 8px; }
```

### Solution 7
```python
app.setStyleSheet("""
    QWidget { background-color: #2b2b2b; color: #eee; }
    QPushButton { background-color: #3c3f41; }
    QPushButton:hover { background-color: #4f5254; }
""")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is QSS?
- Style language
- Database
- Widget
- None
* Correct answer: Style language
CSS-like.

What is a selector?
- What to style
- Value
- Property
- None
* Correct answer: What to style
QPushButton.

What is :hover?
- Hover state
- Click
- Focus
- None
* Correct answer: Hover state
Mouse.

What is a property?
- Visual attribute
- Selector
- Widget
- None
* Correct answer: Visual attribute
Color.

What is background-color?
- Fill
- Text
- Border
- None
* Correct answer: Fill
Property.

What is color?
- Text color
- Fill
- Border
- None
* Correct answer: Text color
Foreground.

What is border-radius?
- Rounded
- Thickness
- Size
- None
* Correct answer: Rounded
Corners.

What is padding?
- Inner space
- Outer
- Border
- None
* Correct answer: Inner space
Gap.

What is font-size?
- Text size
- Color
- Weight
- None
* Correct answer: Text size
px.

What is objectName?
- Id
- Type
- Layout
- None
* Correct answer: Id
#name.

What is setStyleSheet?
- Applies styles
- Creates widget
- Saves
- None
* Correct answer: Applies styles
Global.

What is a theme?
- Consistent look
- One widget
- Layout
- None
* Correct answer: Consistent look
Dark.
<!--/QUIZ-->
