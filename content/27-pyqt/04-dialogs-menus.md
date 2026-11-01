---
title: Диалоги, меню и тулбары
summary: Главное окно QMainWindow: меню, действия QAction, тулбары, статусбар, а также стандартные диалоги QMessageBox, QFileDialog и QInputDialog.
order: 4
duration: 40 мин
difficulty: intermediate
tags: PyQt6, PySide6, QMainWindow, QAction, QMenu, QToolBar, QStatusBar, QMessageBox, QFileDialog, QInputDialog
---

Пока мы показывали только одиночные `QWidget`. Но настоящие приложения имеют структуру: меню сверху, панель инструментов, статусную строку снизу и «рабочую область» по центру. Всё это даёт класс `QMainWindow`. А ещё нам понадобятся стандартные диалоги — окна для выбора файлов, ввода текста и подтверждения действий.

## QMainWindow — главное окно приложения

`QMainWindow` — готовый каркас настольного приложения. Он делится на зоны:

- **меню** — строка сверху (`menuBar()`);
- **тулбары** — панели с кнопками (`addToolBar`);
- **центральный виджет** — главная область (`setCentralWidget`);
- **статусбар** — строка внизу (`statusBar()`).

```python
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QToolBar, QStatusBar)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Главное окно")
window.resize(600, 400)

window.setCentralWidget(QLabel("Рабочая область"))

window.statusBar().showMessage("Готово")   # статусбар

toolbar = QToolBar("Основная")
window.addToolBar(toolbar)

window.show()
sys.exit(app.exec())
```

`setCentralWidget` — обязательный шаг: именно он определяет, что занимает основную площадь окна.

## QAction — действия

`QAction` описывает одно действие: «Открыть», «Сохранить», «Выход». Одно действие можно разместить сразу в нескольких местах — в меню, на тулбаре и в контекстном меню — и оно будет работать везде одинаково:

```python
from PyQt6.QtGui import QAction

open_action = QAction("Открыть", window)
open_action.setShortcut("Ctrl+O")          # горячие клавиши
open_action.setStatusTip("Открыть файл")    # подсказка в статусбаре
open_action.triggered.connect(open_file)    # сигнал выполнения

window.menuBar().addMenu("Файл").addAction(open_action)
toolbar.addAction(open_action)
```

Сигнал `triggered` испускается при активации действия — кликом по меню, по тулбару или горячей клавишей. `setCheckable(True)` превращает действие в переключатель, а `setIcon` добавляет иконку (нужен файл изображения).

## Меню

Меню строятся из `QMenu`. Метод `menuBar().addMenu("Файл")` возвращает меню, в которое добавляются действия, разделители и подменю:

```python
menu = window.menuBar().addMenu("Файл")
menu.addAction(open_action)
menu.addSeparator()                 # горизонтальная линия
menu.addAction(exit_action)

edit_menu = window.menuBar().addMenu("Правка")
submenu = edit_menu.addMenu("Вставка")   # подменю
submenu.addAction(QAction("Из буфера", window))
```

## QToolBar — тулбар

Тулбар — ряд кнопок под меню. Кнопки можно перетаскивать, а панель — прятать:

```python
toolbar = QToolBar("Основная", window)
toolbar.addAction(open_action)
toolbar.addSeparator()
toolbar.addAction(exit_action)
window.addToolBar(toolbar)
```

## QStatusBar — статусбар

Строка состояния внизу окна. `showMessage` выводит временное сообщение, а постоянные виджеты добавляются через `addWidget`:

```python
window.statusBar().showMessage("Файл сохранён", 3000)  # на 3 секунды
window.statusBar().addPermanentWidget(QLabel("v1.0"))
```

## QMessageBox — информационные окна

`QMessageBox` показывает стандартные окна сообщений. Это статические методы, которые возвращают ответ пользователя:

```python
from PyQt6.QtWidgets import QMessageBox

QMessageBox.information(window, "Заголовок", "Текст сообщения")
QMessageBox.warning(window, "Предупреждение", "Файл не найден")
QMessageBox.critical(window, "Ошибка", "Не удалось сохранить")
QMessageBox.about(window, "О программе", "Моё приложение v1.0")
```

Кнопка «Да/Нет»:

```python
answer = QMessageBox.question(
    window, "Подтверждение", "Удалить файл?",
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)
if answer == QMessageBox.StandardButton.Yes:
    print("Удаляем")
```

`question` возвращает нажатую кнопку; набор кнопок задаётся через битовую операцию `|`.

## QFileDialog — выбор файлов

```python
from PyQt6.QtWidgets import QFileDialog

# открыть файл (возвращает путь и фильтр)
file_path, _ = QFileDialog.getOpenFileName(
    window, "Выберите файл", "",
    "Текстовые файлы (*.txt);;Все файлы (*)"
)
if file_path:
    print("Открыт:", file_path)

# сохранить файл
save_path, _ = QFileDialog.getSaveFileName(window, "Сохранить как", "untitled.txt")
```

`getOpenFileName` возвращает кортеж из пути и выбранного фильтра, поэтому путь распаковывается в `file_path, _`.

## QInputDialog — ввод данных

`QInputDialog` запрашивает одну строку или число:

```python
from PyQt6.QtWidgets import QInputDialog

name, ok = QInputDialog.getText(window, "Имя", "Как тебя зовут?")
if ok and name:
    print("Привет,", name)

age, ok = QInputDialog.getInt(window, "Возраст", "Сколько тебе лет?", 18, 0, 120)
if ok:
    print("Возраст:", age)

city, ok = QInputDialog.getItem(
    window, "Город", "Выбери город", ["Москва", "Казань", "Сочи"], 0, False
)
```

Каждый метод возвращает кортеж `(значение, ok)`, где `ok` — было ли подтверждено (`True`) или отменено (`False`).

## Собираем всё вместе

Маленький редактор с меню и диалогами:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QFileDialog, QMessageBox)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Редактор")
window.resize(600, 400)

label = QLabel("Файл не открыт")
window.setCentralWidget(label)

def open_file():
    path, _ = QFileDialog.getOpenFileName(window, "Открыть", "", "*.txt")
    if path:
        label.setText(f"Открыт: {path}")
        window.statusBar().showMessage(f"Открыт {path}")

def about():
    QMessageBox.about(window, "О программе", "Пример редактора на PyQt6")

open_action = QAction("Открыть", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

about_action = QAction("О программе", window)
about_action.triggered.connect(about)

exit_action = QAction("Выход", window)
exit_action.setShortcut("Ctrl+Q")
exit_action.triggered.connect(app.quit)

file_menu = window.menuBar().addMenu("Файл")
file_menu.addAction(open_action)
file_menu.addSeparator()
file_menu.addAction(exit_action)

help_menu = window.menuBar().addMenu("Справка")
help_menu.addAction(about_action)

window.show()
sys.exit(app.exec())
```

## Итог урока

- `QMainWindow` — каркас: меню, тулбар, центральный виджет, статусбар;
- `QAction` — действие, которое живёт сразу в меню и тулбаре;
- `QMessageBox` — информация, предупреждения, вопросы;
- `QFileDialog` — выбор файлов; `QInputDialog` — ввод текста/чисел;
- любой диалог возвращает ответ или отмену — проверяй через `ok` и `answer`.

Теперь практика.

<!--TASK-->
### Задача 1
Создай `QMainWindow` с меню «Файл», содержащим три действия: «Новый», «Открыть…» и разделитель с действием «Выход» (горячая клавиша `Ctrl+Q`). При выборе «Новый» печатай в консоль `Новый файл создан`, при «Выход» — завершай приложение через `app.quit()`.

### Задача 2
Добавь к окну подтверждение выхода: при выборе «Выход» сначала показывай `QMessageBox.question` «Точно выйти?» с кнопками Да/Нет. Выходи из приложения только если пользователь нажал «Да». Проверь обе ветки.

### Задача 3
Создай главное окно с центральным ярлыком и действием «Открыть…» (меню «Файл», горячая клавиша `Ctrl+O`). При выборе показывай `QFileDialog.getOpenFileName` с фильтром только для `.txt`, а выбранный путь выводи в ярлык: `Файл: <путь>`. Если пользователь отменил выбор — печатай в консоль `Отменено`.

### Задача 4
Добавь к окну диалог `QInputDialog.getText`: действие «Переименовать» в меню «Правка» запрашивает новый заголовок окна. Если пользователь ввёл текст и нажал OK — установи его заголовком через `setWindowTitle`. Если отменил — ничего не меняй.

### Задача 5
Собери полное окно: меню «Файл» (Открыть, Выход), тулбар с тем же действием «Открыть» и статусбар, который показывает сообщение `Готово` при запуске, а при открытии файла — путь к нему. Проверь, что действие «Открыть» работает и из меню, и с тулбара, и по `Ctrl+O`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай `QAction("Новый", window)` и `QAction("Выход", window)`. Для выхода подключи `exit_action.triggered.connect(app.quit)`. Меню получи так: `menu = window.menuBar().addMenu("Файл")`, затем `menu.addAction(...)`. Разделитель — `menu.addSeparator()`. Горячая клавиша — `setShortcut("Ctrl+Q")`.

### Подсказка 2
В слоте выхода вызови `QMessageBox.question(window, "Подтверждение", "Точно выйти?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)`. Сравни результат с `QMessageBox.StandardButton.Yes`. Если совпало — только тогда `app.quit()`.

### Подсказка 3
Используй `QFileDialog.getOpenFileName(window, "Открыть", "", "Текстовые файлы (*.txt)")`. Результат распакуй в `(path, _)`. Если `path` непустой — `label.setText(f"Файл: {path}")`, иначе `print("Отменено")`.

### Подсказка 4
Вызови `QInputDialog.getText(window, "Переименовать", "Новый заголовок:")` и распакуй в `(text, ok)`. Если `ok` — `window.setWindowTitle(text)`. Помни: действие добавляется в меню «Правка»: `window.menuBar().addMenu("Правка").addAction(action)`.

### Подсказка 5
Создай одно действие `open_action` и добавь его и в меню (`menu.addAction(open_action)`), и на тулбар (`toolbar.addAction(open_action)`). Статусбар: `window.statusBar().showMessage("Готово")` при запуске, а в слоте открытия — `window.statusBar().showMessage(f"Открыт {path}")`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Меню")
window.resize(400, 300)
window.setCentralWidget(QLabel("Рабочая область"))

def new_file():
    print("Новый файл создан")

new_action = QAction("Новый", window)
new_action.triggered.connect(new_file)

exit_action = QAction("Выход", window)
exit_action.setShortcut("Ctrl+Q")
exit_action.triggered.connect(app.quit)

menu = window.menuBar().addMenu("Файл")
menu.addAction(new_action)
menu.addSeparator()
menu.addAction(exit_action)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `menuBar().addMenu("Файл")` создаёт меню и возвращает его. `addAction` кладёт в него действия, `addSeparator` — разделительную линию. `QAction` связывает «смысл действия» и его отображение: одно действие можно добавить и в меню, и в тулбар. Сигнал `triggered` срабатывает при выборе пункта меню. `app.quit()` завершает цикл событий, и `exec()` возвращает управление. Попробуй также нажать `Ctrl+Q` — горячая клавиша сработает без обращения к меню.

### Разбор 2
Решение:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QMessageBox)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Подтверждение выхода")
window.resize(400, 300)
window.setCentralWidget(QLabel("Рабочая область"))

def confirm_exit():
    answer = QMessageBox.question(
        window, "Подтверждение", "Точно выйти?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if answer == QMessageBox.StandardButton.Yes:
        app.quit()
    else:
        print("Выход отменён")

exit_action = QAction("Выход", window)
exit_action.triggered.connect(confirm_exit)

window.menuBar().addMenu("Файл").addAction(exit_action)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `QMessageBox.question` открывает модальное окно — программа «замирает», пока пользователь не нажмёт кнопку. Набор кнопок складывается из флагов через `|`. Метод возвращает нажатую кнопку; если это `Yes` — вызываем `app.quit()`, иначе просто печатаем «Выход отменён». Такой паттерн защищает от случайного закрытия приложения с несохранёнными данными.

### Разбор 3
Решение:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Открытие файла")
window.resize(500, 300)

label = QLabel("Файл не открыт")
window.setCentralWidget(label)

def open_file():
    path, _ = QFileDialog.getOpenFileName(
        window, "Открыть", "", "Текстовые файлы (*.txt)"
    )
    if path:
        label.setText(f"Файл: {path}")
    else:
        print("Отменено")

open_action = QAction("Открыть…", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

window.menuBar().addMenu("Файл").addAction(open_action)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `getOpenFileName` возвращает кортеж `(путь, фильтр)`. Мы распаковываем его в `path, _` — подчёркивание значит «это значение нам не нужно». Если пользователь закрыл диалог без выбора, `path` — пустая строка, поэтому печатаем «Отменено». Если файл выбран — путь появляется в ярлыке. Обрати внимание на фильтр `"Текстовые файлы (*.txt)"`: в диалоге будут видны только `.txt`-файлы, хотя ввести имя вручную всё равно можно.

### Разбор 4
Решение:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QInputDialog

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Исходный заголовок")
window.resize(400, 300)
window.setCentralWidget(QLabel("Рабочая область"))

def rename():
    text, ok = QInputDialog.getText(window, "Переименовать", "Новый заголовок:")
    if ok and text:
        window.setWindowTitle(text)

rename_action = QAction("Переименовать", window)
rename_action.triggered.connect(rename)

window.menuBar().addMenu("Правка").addAction(rename_action)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `getText` возвращает кортеж `(текст, ok)`. Если пользователь нажал OK, `ok` равен `True`, а `text` содержит введённую строку. Мы проверяем и `ok`, и непустой `text` — если пользователь нажал OK с пустым полем, заголовок не меняется. `setWindowTitle(text)` мгновенно обновляет заголовок окна. Обрати внимание: если бы мы просто вызвали `setWindowTitle(text)` без проверки `ok`, при отмене диалог вернул бы пустую строку и стёр заголовок.

### Разбор 5
Решение:

```python
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QToolBar, QFileDialog)

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Тулбар и статусбар")
window.resize(500, 300)

label = QLabel("Файл не открыт")
window.setCentralWidget(label)

window.statusBar().showMessage("Готово")

def open_file():
    path, _ = QFileDialog.getOpenFileName(window, "Открыть", "", "*.txt")
    if path:
        label.setText(f"Файл: {path}")
        window.statusBar().showMessage(f"Открыт {path}")

open_action = QAction("Открыть", window)
open_action.setShortcut("Ctrl+O")
open_action.triggered.connect(open_file)

menu = window.menuBar().addMenu("Файл")
menu.addAction(open_action)

toolbar = QToolBar("Основная")
window.addToolBar(toolbar)
toolbar.addAction(open_action)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Одно и то же действие `open_action` добавлено и в меню, и на тулбар — поэтому клик по любому из них (и `Ctrl+O`) запускает один и тот же слот `open_file`. `QToolBar` создаётся и прикрепляется через `addToolBar`; его можно открепить и перетащить. Статусбар показывает «Готово», а после открытия файла — его путь. Обрати внимание, что действие на тулбаре отображается как кнопка с текстом, а в меню — как пункт: вид зависит от места размещения.
<!--/SOLUTION-->

<!--QUIZ-->
Какой класс даёт готовый каркас с меню и статусбаром?
- QWidget
- QMainWindow
- QDialog
* Правильный ответ: QMainWindow
QMainWindow содержит menuBar(), addToolBar, setCentralWidget и statusBar().

Как задать центральный виджет главного окна?
- setCentralWidget(widget)
- addWidget(widget)
- setWidget(widget)
* Правильный ответ: setCentralWidget(widget)
Центральный виджет занимает основную область между тулбарами и статусбаром.

Что описывает класс QAction?
- Окно приложения
- Одно действие, которое можно разместить в меню и тулбаре
- Кнопку-переключатель
* Правильный ответ: Одно действие, которое можно разместить в меню и тулбаре
QAction — единое «действие», которое работает в любом месте интерфейса.

Какой сигнал испускает QAction при активации?
- clicked
- triggered
- activated
* Правильный ответ: triggered
triggered срабатывает при выборе действия из меню, тулбара или по горячей клавише.

Как добавить разделитель в меню?
- menu.addLine()
- menu.addSeparator()
- menu.insertSeparator()
* Правильный ответ: menu.addSeparator()
addSeparator добавляет горизонтальную линию между пунктами меню.

Что возвращает QMessageBox.question?
- Ничего
- Нажатую кнопку
- True всегда
* Правильный ответ: Нажатую кнопку
question возвращает кнопку, которую нажал пользователь, например StandardButton.Yes.

Какой метод показывает диалог выбора файла?
- QFileDialog.open()
- QFileDialog.getOpenFileName()
- QFileDialog.chooseFile()
* Правильный ответ: QFileDialog.getOpenFileName()
getOpenFileName показывает системный диалог и возвращает путь к выбранному файлу.

Что возвращает QInputDialog.getText?
- Только строку
- Кортеж (текст, ok), где ok — подтвердил ли пользователь
- Список строк
* Правильный ответ: Кортеж (текст, ok), где ok — подтвердил ли пользователь
Кортеж из значения и флага успеха позволяет отличить ввод от отмены.

Для чего нужен метод setShortcut("Ctrl+O")?
- Для задания текста действия
- Для назначения горячей клавиши
- Для скрытия действия
* Правильный ответ: Для назначения горячей клавиши
По горячей клавише действие срабатывает без открытия меню.

Что делает statusBar().showMessage("Готово", 3000)?
- Показывает сообщение в статусбаре на 3 секунды
- Навсегда закрепляет текст
- Добавляет панель
* Правильный ответ: Показывает сообщение в статусбаре на 3 секунды
Второй аргумент — таймаут отображения в миллисекундах.
<!--/QUIZ-->
