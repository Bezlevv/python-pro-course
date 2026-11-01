---
title: PyQt/PySide: продвинутый GUI
summary: Переходим на промышленные фреймворки PyQt6/PySide6: сигналы, слоты, раскладки, QTimer и стили.
order: 4
duration: 40 мин
difficulty: advanced
tags: PyQt6, PySide6, GUI, сигналы, слоты, QTimer
---

Tkinter отлично подходит для простых приложений, но у профессиональных инструментов есть серьёзные преимущества: богатая библиотека виджетов, поддержка стилей и таблиц, работа с мультимедиа и графикой, высокая производительность. Два главных игрока в мире Python — это **PyQt** (от компании Riverbank) и **PySide** (официальная версия от Qt для Python). Их API почти идентичны, поэтому, научившись одному, ты легко перейдёшь на другой. В этом уроке мы используем PyQt6.

## Установка и каркас приложения

```bash
pip install PyQt6
```

Минимальное приложение на PyQt6:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Моё окно")
window.resize(400, 300)

label = QLabel("Привет, PyQt!", window)
window.setCentralWidget(label)

window.show()
sys.exit(app.exec())
```

Разберём по строкам. `QApplication` — это приложение целиком; он управляет циклом событий, настройками и глобальным состоянием. `QMainWindow` — главное окно с готовой структурой: меню, панель инструментов, статус-бар. `QLabel` — надпись; чтобы она стала центром окна, передаём её в `setCentralWidget`. И финал: `window.show()` делает окно видимым, а `app.exec()` запускает цикл событий. `sys.exit` передаёт код завершения приложения системе.

## Сигналы и слоты

Сердце Qt — механизм **сигналов и слотов**. Сигнал — это событие (например, нажатие кнопки), а слот — метод, который на него реагирует. Связываются они через `connect`:

```python
from PyQt6.QtWidgets import QPushButton, QLabel

def on_click():
    label.setText("Кнопка нажата!")

button = QPushButton("Нажми")
button.clicked.connect(on_click)
```

Обрати внимание: в `connect` передаётся функция без скобок — ровно так же, как `command` в tkinter. Разница в том, что сигналы Qt гораздо богаче: у кнопки есть `clicked(bool)`, у поля ввода — `textChanged(str)`, у ползунка — `valueChanged(int)`. Данные, которые несёт сигнал, передаются в слот как аргументы:

```python
from PyQt6.QtWidgets import QLineEdit

def on_text(text):
    print("Введено:", text)

line_edit = QLineEdit()
line_edit.textChanged.connect(on_text)
```

Слоты можно создавать через обычные функции или методы класса. А если нужно передать дополнительные аргументы — используют `lambda`.

## Раскладки: QVBoxLayout и QHBoxLayout

В PyQt виджеты раскладывают не координатами, а **layout-ами** — менеджерами компоновки. `QVBoxLayout` ставит элементы вертикально, `QHBoxLayout` — горизонтально:

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

central = QWidget()
layout = QVBoxLayout(central)
layout.addWidget(QPushButton("Первая"))
layout.addWidget(QPushButton("Вторая"))
window.setCentralWidget(central)
```

Layout автоматически перестраивает элементы при изменении размера окна — ничего не «разъезжается» и не перекрывается. Это огромное преимущество перед ручной расстановкой.

## QTimer: анимации и таймеры

`QTimer` умеет вызывать функцию через равные промежутки времени. Это основа любых анимаций и секундомеров:

```python
from PyQt6.QtCore import QTimer

seconds = 0

def tick():
    global seconds
    seconds += 1
    label.setText(f"Прошло: {seconds} с")

timer = QTimer()
timer.timeout.connect(tick)
timer.start(1000)  # каждые 1000 мс = 1 секунда
```

`timer.start(1000)` запускает таймер; каждую секунду `QTimer` излучает сигнал `timeout`, который вызывает `tick`. Чтобы остановить — `timer.stop()`. Таймер не блокирует интерфейс: пока идёт отсчёт, окно продолжает откликаться на мышь.

## Списки: QListWidget

Для списков есть готовый виджет `QListWidget`:

```python
from PyQt6.QtWidgets import QListWidget

list_widget = QListWidget()
list_widget.addItem("Первый пункт")
list_widget.addItem("Второй пункт")
```

Это удобная база для todo-приложений, журналов, меню.

## Итог урока

Мы узнали, как:

- устанавливать PyQt6 и собирать приложение из `QApplication`, `QMainWindow`, `setCentralWidget`;
- связывать события (сигналы) с обработчиками (слотами) через `connect`;
- раскладывать виджеты через `QVBoxLayout`/`QHBoxLayout`;
- запускать периодические действия через `QTimer`;
- работать со списками через `QListWidget`.

Это фундамент для серьёзных десктоп-приложений. Практикуемся.

<!--TASK-->
### Задача 1
Создай приложение PyQt6: окно 500×350 с заголовком «Мой первый PyQt». В центре — надпись `QLabel` с текстом «Привет, PyQt!» и размером шрифта 20 (используй `setFont` с `QFont` из `PyQt6.QtGui`). Окно должно открываться и закрываться без ошибок.

### Задача 2
Добавь к задаче 1 кнопку `QPushButton` «Нажми меня» и поле ввода `QLineEdit`. При нажатии кнопки текст из поля должен копироваться в надпись: если поле пустое — надпись становится «Поле пустое», иначе — «Ты ввёл: <текст>». Используй сигнал `clicked` и метод `text()` у поля.

### Задача 3
Переделай приложение на раскладки: создай центральный виджет `QWidget`, в него — `QVBoxLayout`. Размести в нём поле ввода, кнопку и надпись результата. Добавь вторую кнопку «Очистить», которая очищает поле и надпись. Проверь, что при растягивании окна элементы не разъезжаются.

### Задача 4
Создай секундомер на `QTimer`: надпись в центре показывает прошедшие секунды, кнопка «Старт» запускает таймер на 1000 мс, «Стоп» — останавливает, «Сброс» — обнуляет счётчик и надпись. При старте заново секунды продолжают отсчёт (не сбрасываются).

### Задача 5
Собери todo-приложение: `QListWidget` для задач, поле ввода и кнопка «Добавить». По нажатию текст из поля добавляется в список как новый пункт, поле очищается. Кнопка «Удалить выбранное» удаляет выбранный элемент (`currentRow()` + `takeItem(...)`). Если поле пустое — покажи `QMessageBox.warning`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Импортируй `from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel` и `from PyQt6.QtGui import QFont`. Создай `app = QApplication(sys.argv)`, `window = QMainWindow()`, затем `label = QLabel("Привет, PyQt!", window)`, `label.setFont(QFont("Arial", 20))` и `window.setCentralWidget(label)`. В конце `window.show(); sys.exit(app.exec())`.

### Подсказка 2
Создай `line_edit = QLineEdit()` и `button = QPushButton("Нажми меня")`. В обработчике `def on_click():` получай `text = line_edit.text()`; если `text == ""` — `label.setText("Поле пустое")`, иначе — `label.setText(f"Ты ввёл: {text}")`. Свяжи: `button.clicked.connect(on_click)`.

### Подсказка 3
Создай `central = QWidget()` и `layout = QVBoxLayout(central)`, затем `layout.addWidget(line_edit)`, `layout.addWidget(button)`, `layout.addWidget(label)`, `layout.addWidget(clear_button)` и `window.setCentralWidget(central)`. Кнопка «Очистить»: `line_edit.clear()` и `label.setText("")`.

### Подсказка 4
Заведи `seconds = 0` и `label` с текстом «0 с». `timer = QTimer()`; `timer.timeout.connect(tick)`; в `tick()` — `global seconds; seconds += 1; label.setText(f"{seconds} с")`. Старт: `timer.start(1000)`, стоп: `timer.stop()`, сброс: `timer.stop(); seconds = 0; label.setText("0 с")`.

### Подсказка 5
Для добавления: `if text.strip() == "": QMessageBox.warning(window, "Внимание", "Введите задачу")` иначе `list_widget.addItem(text); line_edit.clear()`. Для удаления: `row = list_widget.currentRow(); if row >= 0: list_widget.takeItem(row)`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QFont

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Мой первый PyQt")
window.resize(500, 350)

label = QLabel("Привет, PyQt!", window)
label.setFont(QFont("Arial", 20))
window.setCentralWidget(label)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QApplication(sys.argv)` инициализирует приложение — без него не работает ни один виджет. `QMainWindow` создаёт главное окно. `QLabel` — надпись; `QFont("Arial", 20)` задаёт шрифт и размер. Так как окно управляет всей областью через `setCentralWidget`, надпись растянется по центру. `window.show()` делает окно видимым, `app.exec()` запускает цикл событий и возвращает код завершения, который `sys.exit` передаёт операционной системе. Обрати внимание: вся программа ждёт, пока пользователь закроет окно, — это нормальное поведение GUI-приложений.

### Разбор 2
Решение:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Копирование текста")
window.resize(400, 200)

label = QLabel("Пока пусто", window)
line_edit = QLineEdit(window)
button = QPushButton("Нажми меня", window)

def on_click():
    text = line_edit.text()
    if text == "":
        label.setText("Поле пустое")
    else:
        label.setText(f"Ты ввёл: {text}")

button.clicked.connect(on_click)

window.setCentralWidget(label)
window.show()
sys.exit(app.exec())
```

Что здесь происходит? Обработчик `on_click` срабатывает при каждом сигнале `clicked`. Метод `text()` возвращает текущее содержимое поля ввода. Мы ветвимся: пустое поле — один текст, непустое — другой. `label.setText(...)` меняет содержимое надписи. Заметь: `connect` принимает ссылку на функцию без скобок — вызываться она будет самой Qt при клике. Порядок: `setCentralWidget` принимает только один виджет, поэтому надпись «съела» всё место; в следующей задаче мы исправим это раскладками.

### Разбор 3
Решение:

```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Раскладки")
window.resize(400, 250)

central = QWidget()
layout = QVBoxLayout(central)

label = QLabel("Результат появится здесь")
line_edit = QLineEdit()
button = QPushButton("Показать текст")
clear_button = QPushButton("Очистить")

def on_click():
    text = line_edit.text()
    label.setText("Поле пустое" if text == "" else f"Ты ввёл: {text}")

def on_clear():
    line_edit.clear()
    label.setText("Результат появится здесь")

button.clicked.connect(on_click)
clear_button.clicked.connect(on_clear)

layout.addWidget(line_edit)
layout.addWidget(button)
layout.addWidget(clear_button)
layout.addWidget(label)
window.setCentralWidget(central)
window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QVBoxLayout(central)` привязывает раскладку к центральному виджету. `addWidget` добавляет элементы сверху вниз. Теперь все виджеты живут вместе в одном контейнере — при растягивании окна они распределяют место пропорционально и не перекрываются. Мы также добавили кнопку «Очистить» со своим слотом `on_clear`. Тернарный оператор в `on_click` — компактная замена `if/else`. Такая структура — центральный виджет + layout — каноническая для всех приложений PyQt.

### Разбор 4
Решение:

```python
import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QVBoxLayout)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Секундомер")
window.resize(300, 200)

central = QWidget()
layout = QVBoxLayout(central)
seconds = 0
label = QLabel("0 с")
start_button = QPushButton("Старт")
stop_button = QPushButton("Стоп")
reset_button = QPushButton("Сброс")

def tick():
    global seconds
    seconds += 1
    label.setText(f"{seconds} с")

timer = QTimer()
timer.timeout.connect(tick)

start_button.clicked.connect(lambda: timer.start(1000))
stop_button.clicked.connect(timer.stop)
reset_button.clicked.connect(lambda: (timer.stop(), globals().update(seconds=0), label.setText("0 с")))

for w in (label, start_button, stop_button, reset_button):
    layout.addWidget(w)

window.setCentralWidget(central)
window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QTimer` работает в главном потоке: когда приходит `timeout`, Qt вызывает `tick`. `timer.start(1000)` запускает периодический вызов каждые 1000 мс. Кнопка «Стоп» получает слотом сам метод `timer.stop` — обрати внимание, без скобок и без lambda: сигнал просто вызывает метод. «Сброс» — сложнее: нужно остановить таймер, обнулить `seconds` и обновить надпись, поэтому мы используем lambda с кортежем действий. `globals().update(seconds=0)` — трюк для смены глобальной переменной из lambda; в реальном проекте лучше хранить состояние в атрибутах класса приложения, но для скрипта это допустимо.

### Разбор 5
Решение:

```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QPushButton, QListWidget, QVBoxLayout,
                             QMessageBox)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Мои задачи")
window.resize(350, 350)

central = QWidget()
layout = QVBoxLayout(central)
list_widget = QListWidget()
line_edit = QLineEdit()
add_button = QPushButton("Добавить")
remove_button = QPushButton("Удалить выбранное")

def add_task():
    text = line_edit.text().strip()
    if text == "":
        QMessageBox.warning(window, "Внимание", "Введите задачу")
        return
    list_widget.addItem(text)
    line_edit.clear()

def remove_task():
    row = list_widget.currentRow()
    if row < 0:
        QMessageBox.information(window, "Подсказка", "Сначала выберите задачу")
        return
    list_widget.takeItem(row)

add_button.clicked.connect(add_task)
remove_button.clicked.connect(remove_task)

layout.addWidget(list_widget)
layout.addWidget(line_edit)
layout.addWidget(add_button)
layout.addWidget(remove_button)

window.setCentralWidget(central)
window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QListWidget` хранит пункты списка. `addItem` добавляет новый, `takeItem(row)` удаляет по индексу. `currentRow()` возвращает индекс выбранного элемента или `-1`, если ничего не выбрано, — мы обрабатываем этот случай отдельно. `QMessageBox.warning` и `information` — модальные диалоги, блокирующие окно до ответа пользователя. Обрати внимание на `.strip()`: пустая строка из пробелов тоже считается пустой. Это полноценное рабочее приложение — добавь кнопки «Выполнено», «Сохранить в файл» — и получится настоящий планировщик.
<!--/SOLUTION-->

<!--QUIZ-->
Какой класс нужен для запуска цикла событий PyQt6?
- QMainWindow
- QApplication
- QWidget
* Правильный ответ: QApplication
QApplication — это приложение; его метод exec() запускает цикл событий.

Как связывается сигнал кнопки с функцией?
- button.clicked.connect(my_func) — без скобок
- button.clicked = my_func()
- button.on_click(my_func)
* Правильный ответ: button.clicked.connect(my_func) — без скобок
connect принимает ссылку на функцию; Qt вызывает её при срабатывании сигнала.

Что делает setCentralWidget?
- Задаёт заголовок окна
- Размещает главный виджет в окне
- Меняет размер окна
* Правильный ответ: Размещает главный виджет в окне
setCentralWidget назначает виджет «центром» QMainWindow.

Как называется менеджер компоновки для вертикального размещения элементов?
- QHBoxLayout
- QVBoxLayout
- QGridLayout
* Правильный ответ: QVBoxLayout
QVBoxLayout располагает элементы вертикально, сверху вниз.

Какой сигнал таймера срабатывает через равные промежутки?
- timeout
- tick
- fire
* Правильный ответ: timeout
QTimer излучает timeout через заданный интервал; его связывают со слотом через connect.

Что означает миллисекундный аргумент timer.start(1000)?
- Таймер сработает через 1000 секунд
- Интервал между срабатываниями — 1000 мс
- Таймер остановится через 1000 мс
* Правильный ответ: Интервал между срабатываниями — 1000 мс
start(1000) — периодический вызов раз в секунду.

Какой метод возвращает индекс выбранного элемента QListWidget?
- selectedRow()
- currentRow()
- index()
* Правильный ответ: currentRow()
currentRow() возвращает индекс выбранного пункта или -1, если выбора нет.

Чем PySide6 отличается от PyQt6?
- Это разные языки программирования
- Практически одинаковые API, разные компании-владельцы
- PySide6 не поддерживает Qt
* Правильный ответ: Практически одинаковые API, разные компании-владельцы
PyQt6 (Riverbank) и PySide6 (Qt for Python) почти идентичны по API — код переносится с минимальными правками.
<!--/QUIZ-->
