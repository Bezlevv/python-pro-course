---
title: Финальный проект и публикация через PyInstaller
summary: Как собрать полноценное приложение из модулей, где хранить логику и данные, и как упаковать его в запускаемый .exe через PyInstaller.
order: 8
duration: 50 мин
difficulty: advanced
tags: PyQt6, PySide6, PyInstaller, проект, публикация, exe
---

Ты прошёл долгий путь: виджеты, сигналы, раскладки, диалоги, модели, стили и потоки. Теперь соберём всё это в настоящий проект — и упакуем в файл, который можно запустить на любом компьютере с Windows без установки Python.

## Структура проекта

Хороший проект не должен быть одним гигантским файлом. Стандартная структура приложения на PyQt6:

```
notes_app/
├── main.py            # точка входа: QApplication + главное окно
├── main_window.py     # класс главного окна
├── dialogs.py         # диалоги (если есть)
├── storage.py         # работа с данными (файлы, база)
└── requirements.txt   # зависимости
```

Разделяй логику (хранение данных, вычисления) и интерфейс. Так приложение проще тестировать и менять.

## Точка входа

`main.py` всегда минимален — он инициализирует приложение, показывает главное окно и запускает цикл событий:

```python
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Заметки")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Блок `if __name__ == "__main__":` позволяет импортировать модуль без запуска приложения — полезно для тестов.

## Главное окно как класс

Логику главного окна выноси в класс, наследующий `QMainWindow`. Всё построение — в `__init__` или в отдельном методе `_setup_ui()`:

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.resize(600, 400)
        self._setup_ui()
        self._connect_signals()
```

Это делает код читаемым: конструктор маленький, а каждый шаг — в своём методе.

## Хранение данных

Данные можно хранить в файле. Например, простейший «слой данных» для заметок:

```python
import json

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
```

Замечание: если файла нет, `load()` возвращает пустой список — так приложение запускается «на чистом листе».

## Сборка финального приложения

Соберём мини-приложение «Заметки»: `QListWidget` слева, поле ввода и кнопки «Добавить» и «Удалить» справа, всё сохранение — через `NoteStorage`.

```python
import sys, json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QListWidget, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QMessageBox)

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.storage = NoteStorage()
        self.setWindowTitle("Заметки")
        self.resize(500, 350)

        self.list_widget = QListWidget()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Новая заметка…")
        self.add_btn = QPushButton("Добавить")
        self.del_btn = QPushButton("Удалить")

        right = QVBoxLayout()
        right.addWidget(self.edit)
        right.addWidget(self.add_btn)
        right.addWidget(self.del_btn)
        right.addStretch()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.list_widget, 1)   # список растягивается
        layout.addLayout(right)
        self.setCentralWidget(central)

        self.add_btn.clicked.connect(self.add_note)
        self.del_btn.clicked.connect(self.delete_note)
        self.edit.returnPressed.connect(self.add_note)

        self.notes = self.storage.load()
        self.list_widget.addItems(self.notes)

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()
        self.storage.save(self.notes)

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(self, "Удаление", "Удалить заметку?")
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
            self.storage.save(self.notes)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Вот как связаны все изученные темы: раскладки (урок 3), диалоги (урок 4), сигналы (урок 2), класс `QMainWindow` (урок 4). Программа полностью рабочая — запусти и проверь.

## PyInstaller: упаковка в .exe

**PyInstaller** — инструмент, который собирает Python-скрипт и все библиотеки в один исполняемый файл. Установка:

```bash
pip install pyinstaller
```

Сборка:

```bash
pyinstaller --onefile --windowed --name NotesApp main.py
```

Что означает каждый флаг:

- `--onefile` — один файл `.exe` (всё внутри);
- `--windowed` — без консольного окна (для GUI-приложений);
- `--name NotesApp` — имя итогового файла;
- `--icon app.ico` — иконка приложения (опционально).

Результат появится в папке `dist/` — там лежит готовый `NotesApp.exe`. Его можно скопировать на другую машину и запустить: Python не нужен.

## Частые проблемы PyInstaller

1. **Отсутствие скрытых импортов.** Если приложение использует модули, которые PyInstaller не увидел статически, добавь:

   ```bash
   pyinstaller --hidden-import=модуль --onefile --windowed main.py
   ```

2. **Файлы ресурсов (иконки, шрифты, данные).** При `--onefile` ресурсы распаковываются во временную папку. Её путь доступен через `sys._MEIPASS`:

   ```python
   import sys, os
   def resource_path(relative):
       base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
       return os.path.join(base, relative)
   ```

   Используй `resource_path("notes.json")` для доступа к файлам рядом с программой.

3. **Запуск из dist, а не из проекта.** Тестируй собранный `.exe` именно из `dist/`, как будто это чужой компьютер.

## Итог урока

- Проект делится на модули: точка входа, главное окно, слой данных;
- хранение данных — через простые файлы (JSON) с обработкой отсутствия файла;
- PyInstaller: `pyinstaller --onefile --windowed --name App main.py`;
- для ресурсов в `--onefile` используй `sys._MEIPASS`;
- финальный `.exe` тестируется независимо от окружения разработки.

Теперь финальные задачи.

<!--TASK-->
### Задача 1
Создай структуру проекта `notes_app`: файлы `main.py`, `main_window.py`, `storage.py` и `requirements.txt` (в нём — строка `PyQt6`). В `storage.py` реализуй класс `NoteStorage` с методами `load()` и `save(notes)`, как в теории. Проверь, что `load()` корректно отрабатывает, когда файла ещё нет.

### Задача 2
Напиши класс `MainWindow(QMainWindow)` в файле `main_window.py`: слева — `QListWidget`, справа — `QLineEdit` и кнопки «Добавить» и «Удалить». Из `main.py` импортируй этот класс и покажи окно. Убедись, что программа запускается и показывает окно с заголовком «Заметки».

### Задача 3
Подключи логику: кнопка «Добавить» добавляет текст из поля в список (пустые строки игнорируются), поле очищается. Кнопка «Удалить» спрашивает подтверждение через `QMessageBox.question` и удаляет выбранную заметку. Проверь добавление нескольких заметок и удаление с подтверждением.

### Задача 4
Подключи сохранение: при добавлении и удалении вызывай `storage.save(self.notes)`, а при запуске — `storage.load()`. Закрой приложение, запусти снова и убедись, что заметки сохранились (файл `notes.json` появился рядом).

### Задача 5
Собери приложение через PyInstaller: `pyinstaller --onefile --windowed --name NotesApp main.py`. Запусти `dist/NotesApp.exe` (или эквивалент для своей ОС) и убедись, что окно появляется, заметки работают и файл `notes.json` создаётся рядом с исполняемым файлом. Если есть ошибки сборки — запиши их и попробуй добавить `--hidden-import` для проблемного модуля.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
В `storage.py` импортируй `json`. Метод `load()`: `try: open(...) except FileNotFoundError: return []`. Метод `save()`: `json.dump(notes, f, ensure_ascii=False, indent=2)`. В `requirements.txt` напиши `PyQt6`.

### Подсказка 2
В `main_window.py` импортируй `QMainWindow` и виджеты. В `__init__` задай `setWindowTitle`, `resize`, построй раскладку `QHBoxLayout` с `QListWidget` слева и `QVBoxLayout` справа, вызови `setCentralWidget`. В `main.py` создай `MainWindow()`, `show()`, `sys.exit(app.exec())`.

### Подсказка 3
Создай методы `add_note` и `delete_note`. В `add_note` используй `self.edit.text().strip()` — пустое значение игнорируется. В `delete_note` — `self.list_widget.currentRow()`, при `row < 0` выходи; подтверждение — `QMessageBox.question`; удаление элемента — `takeItem(row)`.

### Подсказка 4
Храни `self.notes` в `__init__`: `self.notes = self.storage.load()`, затем `self.list_widget.addItems(self.notes)`. В `add_note` и `delete_note` после изменения списка вызывай `self.storage.save(self.notes)`.

### Подсказка 5
Выполни сборку из корня проекта `notes_app`. Если после запуска `dist/NotesApp.exe` появляется ошибка про отсутствующий модуль — собери заново с `--hidden-import=имя_модуля`. Помни: запускать надо именно из `dist/`, а не из исходников.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
# storage.py
import json

class NoteStorage:
    def __init__(self, path="notes.json"):
        self.path = path

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, notes):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
```

```text
# requirements.txt
PyQt6
```

Что здесь происходит? `load()` читает JSON из файла; если файла нет (`FileNotFoundError`), возвращает пустой список — приложение стартует «с нуля». `save()` записывает список с сохранением кириллицы (`ensure_ascii=False`) и читаемым форматированием (`indent=2`). Указание `encoding="utf-8"` обязательно — без него на Windows возможны проблемы с русскими буквами. Такой класс — простой и надёжный слой данных: его можно протестировать отдельно от интерфейса.

### Разбор 2
Решение:

```python
# main_window.py
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QListWidget,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.resize(500, 350)

        self.list_widget = QListWidget()
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Новая заметка…")
        self.add_btn = QPushButton("Добавить")
        self.del_btn = QPushButton("Удалить")

        right = QVBoxLayout()
        right.addWidget(self.edit)
        right.addWidget(self.add_btn)
        right.addWidget(self.del_btn)
        right.addStretch()

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.list_widget, 1)
        layout.addLayout(right)
        self.setCentralWidget(central)
```

```python
# main.py
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Что здесь происходит? `main.py` — минимальная точка входа: `QApplication`, окно, `show()`, `exec()`. Всё построение интерфейса перенесено в `MainWindow.__init__`. `layout.addWidget(self.list_widget, 1)` — второй аргумент это «коэффициент растяжения»: список получит всё свободное место, а правая колонка останется компактной. Разделение на модули позволяет запускать и тестировать `MainWindow` независимо.

### Разбор 3
Решение:

```python
    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(
            self, "Удаление", "Удалить заметку?"
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
```

В `__init__` добавь `self.notes = []` и соединения: `self.add_btn.clicked.connect(self.add_note)`, `self.del_btn.clicked.connect(self.delete_note)`, `self.edit.returnPressed.connect(self.add_note)`.

Что здесь происходит? `add_note` берёт текст, убирает лишние пробелы (`strip()`) и игнорирует пустые строки. Добавление происходит в двух местах: в список `self.notes` и в `QListWidget`. `returnPressed` — сигнал поля, срабатывающий по Enter: ввод заметки не требует мыши. `delete_note` сначала проверяет `currentRow()`: если выделения нет, возвращает `-1`, и метод выходит. Подтверждение через `QMessageBox.question` — защита от случайного удаления. `takeItem(row)` убирает элемент из виджета списка.

### Разбор 4
Решение:

```python
    def __init__(self):
        ...
        self.storage = NoteStorage()
        self.notes = self.storage.load()
        self.list_widget.addItems(self.notes)
        ...

    def add_note(self):
        text = self.edit.text().strip()
        if not text:
            return
        self.notes.append(text)
        self.list_widget.addItem(text)
        self.edit.clear()
        self.storage.save(self.notes)

    def delete_note(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        answer = QMessageBox.question(self, "Удаление", "Удалить заметку?")
        if answer == QMessageBox.StandardButton.Yes:
            self.notes.pop(row)
            self.list_widget.takeItem(row)
            self.storage.save(self.notes)
```

Что здесь происходит? При запуске `storage.load()` читает сохранённые заметки и наполняет ими список. Каждое изменение (добавление или удаление) сразу записывается через `storage.save(self.notes)`. Если закрыть приложение и запустить снова — заметки на месте. Файл `notes.json` появится в рабочей папке после первого же изменения. Это простейшая, но рабочая схема персистентности: данные переживают перезапуск программы.

### Разбор 5
Решение:

```bash
cd notes_app
pip install pyinstaller
pyinstaller --onefile --windowed --name NotesApp main.py
```

После сборки:

```bash
./dist/NotesApp.exe    # Windows
./dist/NotesApp        # Linux/macOS
```

Что здесь происходит? PyInstaller анализирует импорты, собирает интерпретатор, библиотеки и скрипт в один файл в `dist/`. `--windowed` скрывает консоль. При первом запуске `NotesApp.exe` заметки пишутся в `notes.json` рядом с исполняемым файлом — а не в исходники. Если сборка падает с `ModuleNotFoundError`, добавь `--hidden-import=имя_модуля`. Советы: тестируй `.exe` из `dist/`, а не из исходников; иконка добавляется через `--icon app.ico`. Готовый файл можно скопировать на любой компьютер с Windows — Python там не нужен.
<!--/SOLUTION-->

<!--QUIZ-->
Для чего нужен файл main.py в проекте?
- Для хранения данных
- Это точка входа: QApplication, главное окно и exec()
- Для стилей
* Правильный ответ: Это точка входа: QApplication, главное окно и exec()
main.py запускает приложение и цикл событий.

Зачем блок if __name__ == "__main__"?
- Чтобы файл нельзя было импортировать
- Чтобы код запускался только при прямом запуске, а не при импорте
- Чтобы ускорить программу
* Правильный ответ: Чтобы код запускался только при прямом запуске, а не при импорте
Это позволяет импортировать модуль (например, в тестах) без побочных эффектов.

Какой флаг PyInstaller создаёт один файл?
- --onefile
- --single
- --bundle
* Правильный ответ: --onefile
--onefile упаковывает всё в один исполняемый файл.

Что делает флаг --windowed?
- Открывает окно при запуске
- Скрывает консольное окно
- Добавляет иконку
* Правильный ответ: Скрывает консольное окно
Для GUI-приложений консоль не нужна — её скрывают флагом --windowed.

Что такое sys._MEIPASS?
- Имя исполняемого файла
- Путь к временной папке с ресурсами в режиме --onefile
- Номер версии Python
* Правильный ответ: Путь к временной папке с ресурсами в режиме --onefile
В --onefile ресурсы распаковываются во временную папку; её путь лежит в sys._MEIPASS.

Как обработать отсутствие файла данных при загрузке?
- Выбросить ошибку
- Вернуть пустой список/значение по умолчанию
- Перезапустить приложение
* Правильный ответ: Вернуть пустой список/значение по умолчанию
Ловим FileNotFoundError и возвращаем пустой список — приложение стартует «с нуля».

Зачем отделять хранение данных от интерфейса?
- Так код короче
- Логику легче тестировать и менять независимо от UI
- Это требование PyInstaller
* Правильный ответ: Логику легче тестировать и менять независимо от UI
Слои данных и интерфейса — независимые модули: их можно разрабатывать и проверять отдельно.

Что делает takeItem(row) у QListWidget?
- Возвращает текст элемента
- Удаляет элемент с указанной позиции
- Добавляет элемент
* Правильный ответ: Удаляет элемент с указанной позиции
takeItem(row) убирает элемент из виджета списка.

Зачем нужен --hidden-import?
- Чтобы ускорить сборку
- Чтобы добавить модуль, который PyInstaller не нашёл статически
- Чтобы скрыть код
* Правильный ответ: Чтобы добавить модуль, который PyInstaller не нашёл статически
Иногда импорты динамические — PyInstaller их не видит, и модуль добавляют вручную.

Куда PyInstaller кладёт готовый файл?
- В папку build/
- В папку dist/
- В корень проекта
* Правильный ответ: В папку dist/
Готовый исполняемый файл появляется в dist/.
<!--/QUIZ-->
