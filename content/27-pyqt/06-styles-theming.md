---
title: QSS: стилизация и тёмная тема
summary: Стилизация интерфейса: язык QSS, селекторы, псевдоклассы, а также QPalette и программные тёмные темы.
order: 6
duration: 40 мин
difficulty: advanced
tags: PyQt6, PySide6, QSS, стили, setStyleSheet, QPalette, тёмная тема
---

Виджеты Qt по умолчанию выглядят как стандартные элементы операционной системы. Но для собственного приложения часто хочется уникального стиля: своих цветов, скруглённых кнопок, аккуратных полей. В Qt это делается двумя способами: через **QSS** (Qt Style Sheets) — язык, очень похожий на CSS, и через **QPalette** — программную настройку палитры цветов.

## Что такое QSS

QSS — это строки стилей. Их можно назначить конкретному виджету через `setStyleSheet` или всему приложению:

```python
app.setStyleSheet("QPushButton { background-color: lightblue; }")
```

Правило состоит из **селектора** (какие виджеты) и **объявлений** (какие свойства). Как и в CSS, виджеты наследуют стили от родителей, но прямое правило важнее унаследованного.

Простейший пример — скруглённая цветная кнопка:

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

## Селекторы

Селектор выбирает, к каким виджетам применить правило:

```css
QPushButton { ... }               /* все кнопки */
QLineEdit { ... }                 /* все поля ввода */
QWidget#mainPanel { ... }         /* виджет с objectName="mainPanel" */
#okButton { ... }                 /* любой виджет с objectName="okButton" */
QLineEdit[class="search"] { ... } /* по динамическому свойству */
```

Селектор по `objectName` — главный инструмент стилизации конкретных элементов: дай виджету имя через `setObjectName`, и обращайся к нему через `#имя`.

```python
label.setObjectName("title")
app.setStyleSheet("#title { font-size: 24px; color: navy; }")
```

## Свойства

Самые ходовые свойства:

- цвета: `background-color`, `color`, `border-color`;
- рамки: `border`, `border-radius`, `border-width`;
- текст: `font-size`, `font-family`, `font-weight`, `font-style`;
- отступы: `padding`, `margin`;
- выравнивание: `qproperty-alignment: 'AlignCenter';`.

Любое свойство можно применить к любому виджету, но работают они по-разному: например, `border-radius` красиво смотрится на кнопках и полях, но не меняет внешний вид `QListView`.

## Псевдоклассы

Псевдоклассы описывают **состояния** виджета:

```css
QPushButton:hover { background-color: #45a049; }   /* наведение мыши */
QPushButton:pressed { background-color: #3d8b40; } /* нажата */
QPushButton:disabled { background-color: gray; }   /* выключена */
QCheckBox:checked { color: green; }                /* отмечена */
QLineEdit:focus { border: 2px solid blue; }        /* в фокусе */
```

Псевдокласс идёт сразу после селектора через двоеточие и комбинируется с другими селекторами:

```css
#sendButton:hover { background-color: orange; }
```

## Стилизация всего приложения

Чтобы стилизовать всё сразу, передай строку QSS в `app.setStyleSheet`. Так делаются целые темы. Тёмная тема — классика:

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

Как это работает? `QWidget { background-color: #2b2b2b; }` красит фон всех виджетов. Но у многих виджетов есть собственные палитры (например, у полей ввода), поэтому для конкретных элементов нужно указывать их индивидуальные правила.

## Изменение темы на лету

Тему можно переключать прямо во время работы приложения — достаточно вызвать `setStyleSheet` с новой строкой. Часто используют переключатель, который меняет тему:

```python
def toggle_theme(checked):
    if checked:
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet("")
```

## QPalette — палитра цветов

Второй механизм — `QPalette`. Он хранит цвета для ролей: фон окна, фон текста, акцентный цвет выделения и так далее.

```python
from PyQt6.QtGui import QPalette, QColor

palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor(43, 43, 43))
palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 144, 217))
app.setPalette(palette)
```

Основные роли: `Window` (фон окна), `WindowText` (текст на фоне), `Base` (фон полей ввода и списков), `Text` (текст в полях), `Highlight` (фон выделенного текста), `HighlightedText` (текст выделения), `Button` (фон кнопок).

`QPalette` — «нативный» способ: он мгновенно перекрашивает все виджеты, включая те, что не покрыты QSS. А вот `QSS` даёт больше контроля над деталями: рамки, скругления, псевдоклассы. Лучший подход — комбинировать оба: QPalette для базовых цветов, QSS для тонкой настройки.

## Итог урока

- QSS — CSS-подобный язык стилей: `setStyleSheet` на виджете или приложении;
- селекторы: по классу, по `objectName` (`#имя`), по свойствам;
- псевдоклассы: `:hover`, `:pressed`, `:disabled`, `:checked`, `:focus`;
- `QPalette` задаёт цвета по ролям и перекрашивает всё сразу;
- темы можно переключать на лету, меняя строку QSS.

Теперь практика.

<!--TASK-->
### Задача 1
Создай окно с тремя кнопками и задай им общий стиль через `app.setStyleSheet`: зелёный фон (`#4CAF50`), белый текст, скругление `border-radius: 8px`, отступы `padding: 10px 20px`, размер шрифта 14px. Проверь, что стиль применился ко всем трём кнопкам одновременно.

### Задача 2
Создай окно с тремя кнопками, у каждой из которых свой `objectName` (`submit`, `cancel`, `danger`). Через `app.setStyleSheet` стилизуй их по-разному с помощью селекторов `#submit`, `#cancel`, `#danger`: зелёную, серую и красную соответственно.

### Задача 3
Добавь к кнопке из задачи 2 псевдоклассы: для `#submit` — `:hover` (светлее), `:pressed` (темнее), для `#danger` — `:hover` с красным оттенком, а `#cancel:disabled` — серый фон и серый текст. Проверь, что состояния меняются при наведении, нажатии и отключении кнопки.

### Задача 4
Создай приложение с переключателем темы: `QCheckBox` «Тёмная тема». Когда флажок отмечен — применяй тёмную QSS (фон `#2b2b2b`, светлый текст, тёмные поля ввода); когда снят — возвращай стандартную тему (`setStyleSheet("")`). Используй сигнал `toggled` для переключения.

### Задача 5
Используй `QPalette` для настройки палитры: фон окна светло-серый (`#f0f0f0`), текст тёмный (`#1a1a1a`), фон полей белый (`#ffffff`), акцентный цвет — синий (`#4a90d9`). Создай окно с ярлыком и полем ввода и убедись, что цвета применились ко всем виджетам без единого правила QSS.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Собери строку QSS в переменную и передай её в `app.setStyleSheet(...)`. Селектор `QPushButton` применится ко всем кнопкам приложения. Не забудь перенести строку в тройные кавычки, чтобы QSS можно было писать в несколько строк.

### Подсказка 2
Каждой кнопке задай `setObjectName(...)`. В QSS пиши `#submit { ... }`, `#cancel { ... }`, `#danger { ... }`. Фон задаётся `background-color`, текст — `color`.

### Подсказка 3
Псевдоклассы добавляются к селектору через двоеточие: `#submit:hover { ... }`, `#submit:pressed { ... }`. Для отключённого состояния — `#cancel:disabled { ... }`. Проверь отключение через `cancel_btn.setEnabled(False)`.

### Подсказка 4
Подключи `check_box.toggled.connect(toggle_theme)`. Внутри слота проверяй `checked`: если `True` — `app.setStyleSheet(DARK_THEME)`, иначе — `app.setStyleSheet("")`. Держи строку тёмной темы в глобальной переменной.

### Подсказка 5
Создай `QPalette()`, назначь роли через `palette.setColor(QPalette.ColorRole.Window, QColor(...))` и передай в `app.setPalette(palette)`. Роли: `Window`, `WindowText`, `Base`, `Text`, `Highlight`, `HighlightedText`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

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
window.setWindowTitle("Стиль для всех кнопок")
window.resize(300, 220)

layout = QVBoxLayout(window)
for text in ["Сохранить", "Отправить", "OK"]:
    layout.addWidget(QPushButton(text))

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `app.setStyleSheet(...)` задаёт стиль всему приложению, поэтому правило `QPushButton { ... }` применяется ко всем трём кнопкам. `background-color` — цвет фона, `color` — цвет текста, `border-radius: 8px` скругляет углы, `padding: 10px 20px` создаёт отступы (10px сверху/снизу, 20px слева/справа), `font-size` задаёт размер шрифта. Обрати внимание на тройные кавычки: QSS удобно писать многострочно.

### Разбор 2
Решение:

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
window.setWindowTitle("Селекторы по имени")
window.resize(300, 200)

layout = QVBoxLayout(window)
submit = QPushButton("Сохранить")
cancel = QPushButton("Отмена")
danger = QPushButton("Удалить")
submit.setObjectName("submit")
cancel.setObjectName("cancel")
danger.setObjectName("danger")
layout.addWidget(submit)
layout.addWidget(cancel)
layout.addWidget(danger)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Селектор `#submit` обращается к виджету с `objectName` равным `"submit"`. `setObjectName` — обычный метод; если имя не задано, `#`-селектор не сработает. Префикс `#` отличает селекторы по имени от селекторов по классу. Так можно стилизовать одинаковые виджеты по-разному, не создавая отдельные классы. Кнопки теперь имеют зелёный, серый и красный фон.

### Разбор 3
Решение:

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
window.setWindowTitle("Псевдоклассы")
window.resize(300, 220)

layout = QVBoxLayout(window)
submit = QPushButton("Сохранить")
cancel = QPushButton("Отмена")
danger = QPushButton("Удалить")
submit.setObjectName("submit")
cancel.setObjectName("cancel")
danger.setObjectName("danger")
layout.addWidget(submit)
layout.addWidget(cancel)
layout.addWidget(danger)

cancel.setEnabled(False)   # покажем состояние :disabled

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Правила с псевдоклассами имеют более высокий приоритет, чем обычные, поэтому при наведении мыши (`:hover`) фон `#submit` становится светлее, при нажатии (`:pressed`) — темнее. Кнопка «Отмена» отключена `setEnabled(False)`, и правило `#cancel:disabled` красит её в серый (`#ddd`) с серым текстом (`#999`). Так состояния виджетов отражаются визуально.

### Разбор 4
Решение:

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
window.setWindowTitle("Переключение темы")
window.resize(300, 180)

def toggle_theme(checked):
    if checked:
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet("")

layout = QVBoxLayout(window)
toggle = QCheckBox("Тёмная тема")
toggle.toggled.connect(toggle_theme)
layout.addWidget(toggle)
layout.addWidget(QLineEdit())
layout.addWidget(QPushButton("Кнопка"))

window.show()
sys.exit(app.exec())
```

Что здесь происходит? При отмеченном флажке `toggled` испускает `True`, и `setStyleSheet(DARK_THEME)` перекрашивает всё приложение: фон окна становится тёмным, текст светлым, поля и кнопки — графитовыми, а поле при фокусе получает синюю рамку (`QLineEdit:focus { border-color: #4a90d9; }`). При снятии флажка `app.setStyleSheet("")` возвращает стиль по умолчанию. Так темы переключаются без перезапуска приложения.

### Разбор 5
Решение:

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
window.setWindowTitle("Палитра")
window.resize(300, 150)

layout = QVBoxLayout(window)
layout.addWidget(QLabel("Текст"))
layout.addWidget(QLineEdit())

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QPalette` хранит цвета по ролям. `Window` — фон окна, `WindowText` — текст поверх него, `Base` — фон полей ввода и списков, `Text` — текст в них, `Highlight` — цвет выделения, `HighlightedText` — цвет текста выделения. После `app.setPalette(palette)` все виджеты перекрашиваются автоматически: фон окна светло-серый, поля белые, выделение синее. Ни одного правила QSS не понадобилось. Это самый чистый способ поменять «базовую» цветовую схему приложения.
<!--/SOLUTION-->

<!--QUIZ-->
Какой метод применяет QSS ко всему приложению?
- app.setStylesheet(...)
- app.setStyleSheet(...)
- app.style(...)
* Правильный ответ: app.setStyleSheet(...)
setStyleSheet принимает строку с правилами QSS и применяет её к приложению.

Как в QSS обратиться к виджету с objectName="okButton"?
- QPushButton.okButton
- #okButton
- .okButton
* Правильный ответ: #okButton
Селектор с решёткой # выбирает виджет по objectName.

Что делает псевдокласс :hover?
- Применяет стиль при наведении мыши
- Применяет стиль всегда
- Убирает стиль
* Правильный ответ: Применяет стиль при наведении мыши
:hover активируется, когда курсор над виджетом.

Какое свойство отвечает за скругление углов?
- corner-radius
- border-radius
- round
* Правильный ответ: border-radius
border-radius задаёт радиус скругления углов в пикселях.

Что определяет роля Window в QPalette?
- Цвет текста
- Цвет фона окна
- Цвет рамки
* Правильный ответ: Цвет фона окна
Роля Window — базовый цвет фона окна и родительских виджетов.

Как применить стиль только к кнопкам внутри виджета с objectName="panel"?
- #panel QPushButton { ... }
- QPushButton #panel { ... }
- #panel:QPushButton { ... }
* Правильный ответ: #panel QPushButton { ... }
Пробел в селекторе — «любой потомок»: кнопки внутри панели.

Состояние какого виджета описывает :checked?
- QLineEdit
- QCheckBox
- QLabel
* Правильный ответ: QCheckBox
:checked срабатывает для отмеченных флажков (и подобных переключателей).

Что делает по.setStyleSheet("")?
- Вызывает ошибку
- Сбрасывает стили, возвращая вид по умолчанию
- Закрывает приложение
* Правильный ответ: Сбрасывает стили, возвращая вид по умолчанию
Пустая строка отменяет все пользовательские QSS-правила.

Какая роль QPalette отвечает за фон полей ввода?
- Base
- Window
- Button
* Правильный ответ: Base
Роля Base — фон текстовых полей, списков и других «белых» областей.

Можно ли включить тёмную тему во время работы приложения?
- Нет, только при запуске
- Да, вызвав setStyleSheet с новой темой в любой момент
- Только перезапуском ОС
* Правильный ответ: Да, вызвав setStyleSheet с новой темой в любой момент
Стили применяются мгновенно; часто это делается по сигналу переключателя.
<!--/QUIZ-->
