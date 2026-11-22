---
title: QSS: Styling and Dark Theme
summary: Interface styling: the QSS language, selectors, pseudo-classes, plus QPalette and programmatic dark themes.
order: 6
duration: 40 min
difficulty: advanced
tags: PyQt6, PySide6, QSS, styles, setStyleSheet, QPalette, dark theme
---

Qt widgets look like standard operating system elements by default. But for your own application you often want a unique style: your own colors, rounded buttons, neat fields. In Qt this is done in two ways: via **QSS** (Qt Style Sheets) — a language very similar to CSS — and via **QPalette** — programmatic color palette configuration.

## What is QSS

QSS is style strings. They can be assigned to a specific widget via `setStyleSheet` or to the whole application:

```python
app.setStyleSheet("QPushButton { background-color: lightblue; }")
```

A rule consists of a **selector** (which widgets) and **declarations** (which properties). As in CSS, widgets inherit styles from parents, but a direct rule beats an inherited one.

The simplest example — a rounded colored button:

```python
button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        font-size: 14px;
    }
""")
```

## Selectors

A selector picks which widgets a rule applies to:

```css
QPushButton { ... }               /* all buttons */
QLineEdit { ... }                 /* all input fields */
QWidget#mainPanel { ... }         /* widget with objectName="mainPanel" */
#okButton { ... }                 /* any widget with objectName="okButton" */
QLineEdit[class="search"] { ... } /* by dynamic property */
```

Selection by `objectName` is the main tool for styling specific elements: give the widget a name via `setObjectName`, then address it with `#name`.

```python
label.setObjectName("title")
app.setStyleSheet("#title { font-size: 24px; color: navy; }")
```

## Properties

The most common properties:

- colors: `background-color`, `color`, `border-color`;
- borders: `border`, `border-radius`, `border-width`;
- text: `font-size`, `font-family`, `font-weight`, `font-style`;
- spacing: `padding`, `margin`;
- alignment: `qproperty-alignment: 'AlignCenter';`.

Any property can be applied to any widget, but they behave differently: for example, `border-radius` looks nice on buttons and fields, but doesn't change `QListView`'s look.

## Pseudo-classes

Pseudo-classes describe widget **states**:

```css
QPushButton:hover { background-color: #45a049; }   /* mouse hover */
QPushButton:pressed { background-color: #3d8b40; } /* pressed */
QPushButton:disabled { background-color: gray; }   /* disabled */
QCheckBox:checked { color: green; }                /* checked */
QLineEdit:focus { border: 2px solid blue; }        /* focused */
```

A pseudo-class comes right after the selector with a colon and combines with other selectors:

```css
#sendButton:hover { background-color: orange; }
```

## Styling the whole application

To style everything at once, pass a QSS string to `app.setStyleSheet`. That's how entire themes are made. A dark theme is a classic:

```python
app.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #f0f0f0;
        font-size: 13px;
    }
    QPushButton {
        background-color: #3c3f41;
        border: 1px solid #555;
        border-radius: 6px;
        padding: 6px 14px;
    }
    QPushButton:hover { background-color: #4a4d4f; }
    QPushButton:pressed { background-color: #2f3133; }
    QLineEdit {
        background-color: #1e1e1e;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 4px 8px;
    }
    QLineEdit:focus { border-color: #4a90d9; }
""")
```

How does this work? `QWidget { background-color: #2b2b2b; }` paints the background of all widgets. But many widgets have their own palettes (for example, input fields), so specific elements need individual rules.

## Changing themes on the fly

The theme can be switched right while the application runs — just call `setStyleSheet` with a new string. A toggle that changes the theme is often used:

```python
def toggle_theme(checked):
    if checked:
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet("")
```

## QPalette — color palette

The second mechanism is `QPalette`. It stores colors for roles: window background, text background, selection accent color, and so on.

```python
from PyQt6.QtGui import QPalette, QColor

palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(43, 43, 43))
palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 144, 217))
app.setPalette(palette)
```

Main roles: `Window` (window background), `WindowText` (text on background), `Base` (background of input fields and lists), `Text` (text in fields), `Highlight` (selected text background), `HighlightedText` (selection text), `Button` (button background).

`QPalette` is the "native" way: it instantly repaints all widgets, including those not covered by QSS. Meanwhile `QSS` gives more control over details: borders, rounding, pseudo-classes. The best approach is combining both: QPalette for base colors, QSS for fine-tuning.

## Lesson summary

- QSS is a CSS-like style language: `setStyleSheet` on a widget or application;
- selectors: by class, by `objectName` (`#name`), by properties;
- pseudo-classes: `:hover`, `:pressed`, `:disabled`, `:checked`, `:focus`;
- `QPalette` sets colors by roles and repaints everything at once;
- themes can be switched on the fly by changing the QSS string.

Now practice.

<!--TASK-->
### Task 1
Create a window with three buttons and give them a common style via `app.setStyleSheet`: green background (`#4CAF50`), white text, `border-radius: 8px` rounding, `padding: 10px 20px` insets, font size 14px. Verify the style applies to all three buttons at once.

### Task 2
Create a window with three buttons, each with its own `objectName` (`submit`, `cancel`, `danger`). Via `app.setStyleSheet` style them differently using the `#submit`, `#cancel`, `#danger` selectors: green, gray, and red respectively.

### Task 3
Add pseudo-classes to the button from task 2: for `#submit` — `:hover` (lighter), `:pressed` (darker); for `#danger` — `:hover` with a red tint; and `#cancel:disabled` — gray background and gray text. Verify the states change on hover, press, and disabling the button.

### Task 4
Create an application with a theme toggle: a `QCheckBox` "Dark theme". When the checkbox is checked — apply dark QSS (background `#2b2b2b`, light text, dark input fields); when unchecked — return the standard theme (`setStyleSheet("")`). Use the `toggled` signal for switching.

### Task 5
Use `QPalette` to configure the palette: window background light gray (`#f0f0f0`), text dark (`#1a1a1a`), field background white (`#ffffff`), accent color blue (`#4a90d9`). Create a window with a label and an input field and verify the colors apply to all widgets without a single QSS rule.
<!--/TASK-->

<!--HINT-->
### Hint 1
Put the QSS string into a variable and pass it to `app.setStyleSheet(...)`. The `QPushButton` selector applies to all buttons in the application. Don't forget to wrap the string in triple quotes so QSS can be written over multiple lines.

### Hint 2
Give each button a `setObjectName(...)`. In QSS write `#submit { ... }`, `#cancel { ... }`, `#danger { ... }`. The background is set with `background-color`, the text with `color`.

### Hint 3
Pseudo-classes are appended to the selector with a colon: `#submit:hover { ... }`, `#submit:pressed { ... }`. For the disabled state — `#cancel:disabled { ... }`. Test disabling via `cancel_btn.setEnabled(False)`.

### Hint 4
Connect `check_box.toggled.connect(toggle_theme)`. Inside the slot check `checked`: if `True` — `app.setStyleSheet(DARK_THEME)`, otherwise — `app.setStyleSheet("")`. Keep the dark theme string in a global variable.

### Hint 5
Create a `QPalette()`, assign roles via `palette.setColor(QPalette.ColorRole.Window, QColor(...))` and pass it to `app.setPalette(palette)`. Roles: `Window`, `WindowText`, `Base`, `Text`, `Highlight`, `HighlightedText`.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication(sys.argv)

app.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 14px;
    }
""")

window = QWidget()
window.setWindowTitle("Style for all buttons")
window.resize(300, 220)

layout = QVBoxLayout(window)
for text in ["Save", "Send", "OK"]:
    layout.addWidget(QPushButton(text))

window.show()
sys.exit(app.exec())
```

What's happening here? `app.setStyleSheet(...)` sets the style for the whole application, so the rule `QPushButton { ... }` applies to all three buttons. `background-color` is the background color, `color` — the text color, `border-radius: 8px` rounds the corners, `padding: 10px 20px` creates insets (10px top/bottom, 20px left/right), `font-size` sets the font size. Note the triple quotes: it's convenient to write QSS multiline.

### Walkthrough 2
Solution:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication(sys.argv)

app.setStyleSheet("""
    #submit { background-color: #4CAF50; color: white; }
    #cancel { background-color: #9e9e9e; color: white; }
    #danger { background-color: #f44336; color: white; }
""")

window = QWidget()
window.setWindowTitle("Selectors by name")
window.resize(300, 200)

layout = QVBoxLayout(window)
submit = QPushButton("Save")
cancel = QPushButton("Cancel")
danger = QPushButton("Delete")
submit.setObjectName("submit")
cancel.setObjectName("cancel")
danger.setObjectName("danger")
layout.addWidget(submit)
layout.addWidget(cancel)
layout.addWidget(danger)

window.show()
sys.exit(app.exec())
```

What's happening here? The `#submit` selector addresses the widget whose `objectName` equals `"submit"`. `setObjectName` is a regular method; if no name is set, the `#`-selector won't work. The `#` prefix distinguishes name selectors from class selectors. This way identical widgets can be styled differently without creating separate classes. The buttons now have green, gray, and red backgrounds.

### Walkthrough 3
Solution:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication(sys.argv)

app.setStyleSheet("""
    #submit {
        background-color: #4CAF50; color: white; padding: 8px 16px;
    }
    #submit:hover { background-color: #66bb6a; }
    #submit:pressed { background-color: #388e3c; }
    #danger { background-color: #f44336; color: white; }
    #danger:hover { background-color: #e57373; }
    #cancel {
        background-color: #9e9e9e; color: white; padding: 8px 16px;
    }
    #cancel:disabled { background-color: #ddd; color: #999; }
""")

window = QWidget()
window.setWindowTitle("Pseudo-classes")
window.resize(300, 220)

layout = QVBoxLayout(window)
submit = QPushButton("Save")
cancel = QPushButton("Cancel")
danger = QPushButton("Delete")
submit.setObjectName("submit")
cancel.setObjectName("cancel")
danger.setObjectName("danger")
layout.addWidget(submit)
layout.addWidget(cancel)
layout.addWidget(danger)

cancel.setEnabled(False)   # show the :disabled state

window.show()
sys.exit(app.exec())
```

What's happening here? Rules with pseudo-classes have higher priority than plain ones, so on mouse hover (`:hover`) the `#submit` background becomes lighter, and on press (`:pressed`) — darker. The "Cancel" button is disabled with `setEnabled(False)`, and the `#cancel:disabled` rule paints it gray (`#ddd`) with gray text (`#999`). Thus widget states are reflected visually.

### Walkthrough 4
Solution:

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QLineEdit, QVBoxLayout

DARK_THEME = """
    QWidget {
        background-color: #2b2b2b;
        color: #f0f0f0;
        font-size: 13px;
    }
    QPushButton {
        background-color: #3c3f41;
        border: 1px solid #555;
        border-radius: 6px;
        padding: 6px 14px;
    }
    QPushButton:hover { background-color: #4a4d4f; }
    QLineEdit {
        background-color: #1e1e1e;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 4px 8px;
    }
    QLineEdit:focus { border-color: #4a90d9; }
"""

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Theme switching")
window.resize(300, 180)

def toggle_theme(checked):
    if checked:
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet("")

layout = QVBoxLayout(window)
toggle = QCheckBox("Dark theme")
toggle.toggled.connect(toggle_theme)
layout.addWidget(toggle)
layout.addWidget(QLineEdit())
layout.addWidget(QPushButton("Button"))

window.show()
sys.exit(app.exec())
```

What's happening here? When the checkbox is checked, `toggled` emits `True`, and `setStyleSheet(DARK_THEME)` repaints the whole application: the window background becomes dark, text light, fields and buttons graphite-colored, and the field gets a blue border on focus (`QLineEdit:focus { border-color: #4a90d9; }`). When the checkbox is unchecked, `app.setStyleSheet("")` returns the default style. Thus themes switch without restarting the application.

### Walkthrough 5
Solution:

```python
import sys
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout

app = QApplication(sys.argv)

palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
palette.setColor(QPalette.ColorRole.WindowText, QColor("#1a1a1a"))
palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
palette.setColor(QPalette.ColorRole.Text, QColor("#1a1a1a"))
palette.setColor(QPalette.ColorRole.Highlight, QColor("#4a90d9"))
palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
app.setPalette(palette)

window = QWidget()
window.setWindowTitle("Palette")
window.resize(300, 150)

layout = QVBoxLayout(window)
layout.addWidget(QLabel("Text"))
layout.addWidget(QLineEdit())

window.show()
sys.exit(app.exec())
```

What's happening here? `QPalette` stores colors by roles. `Window` — the window background, `WindowText` — text over it, `Base` — the background of input fields and lists, `Text` — text inside them, `Highlight` — the selection color, `HighlightedText` — the selection text color. After `app.setPalette(palette)` all widgets repaint automatically: the window background is light gray, fields are white, selection is blue. Not a single QSS rule was needed. This is the cleanest way to change an application's "base" color scheme.
<!--/SOLUTION-->

<!--QUIZ-->
Which method applies QSS to the whole application?
- app.setStylesheet(...)
- app.setStyleSheet(...)
- app.style(...)
* Correct answer: app.setStyleSheet(...)
setStyleSheet takes a string with QSS rules and applies it to the application.

How in QSS to address a widget with objectName="okButton"?
- QPushButton.okButton
- #okButton
- .okButton
* Correct answer: #okButton
The selector with a hash # selects a widget by objectName.

What does the pseudo-class :hover do?
- Applies the style on mouse hover
- Applies the style always
- Removes the style
* Correct answer: Applies the style on mouse hover
:hover activates when the cursor is over the widget.

Which property is responsible for rounding corners?
- corner-radius
- border-radius
- round
* Correct answer: border-radius
border-radius sets the corner rounding radius in pixels.

What does the Window role define in QPalette?
- The text color
- The window background color
- The border color
* Correct answer: The window background color
The Window role is the base background color of the window and parent widgets.

How to apply a style only to buttons inside a widget with objectName="panel"?
- #panel QPushButton { ... }
- QPushButton #panel { ... }
- #panel:QPushButton { ... }
* Correct answer: #panel QPushButton { ... }
A space in the selector means "any descendant": buttons inside the panel.

Which widget's state does :checked describe?
- QLineEdit
- QCheckBox
- QLabel
* Correct answer: QCheckBox
:checked fires for checked checkboxes (and similar toggles).

What does app.setStyleSheet("") do?
- Raises an error
- Resets the styles, returning the default look
- Closes the application
* Correct answer: Resets the styles, returning the default look
An empty string cancels all custom QSS rules.

Which QPalette role is responsible for the background of input fields?
- Base
- Window
- Button
* Correct answer: Base
The Base role is the background of text fields, lists, and other "white" areas.

Can a dark theme be enabled while the application runs?
- No, only at startup
- Yes, by calling setStyleSheet with a new theme at any moment
- Only by restarting the OS
* Correct answer: Yes, by calling setStyleSheet with a new theme at any moment
Styles apply instantly; this is often done on a toggle's signal.
<!--/QUIZ-->
