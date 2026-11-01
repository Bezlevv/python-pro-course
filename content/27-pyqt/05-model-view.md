---
title: Модель-представление и делегаты
summary: Архитектура Model/View: QListView и QTableView, QStandardItemModel, роли элементов, выделение и собственные делегаты через QStyledItemDelegate.
order: 5
duration: 45 мин
difficulty: advanced
tags: PyQt6, PySide6, QListView, QTableView, QStandardItemModel, QStyledItemDelegate, делегаты, модель-представление
---

`QListWidget` и `QTableWidget` удобны, но хранят данные внутри себя. В реальных приложениях данные часто живут отдельно — в базе, в API, в большом списке объектов. Для этого в Qt есть архитектура **Модель-представление** (Model/View): **модель** хранит данные, а **представление** показывает их и даёт пользователю редактировать. Одно представление может показывать одну модель, а одна модель — несколько представлений одновременно.

## Как это устроено

Три участника:

1. **Модель** (`QStandardItemModel` и подобные) — данные и правила доступа к ним;
2. **Представление** (`QListView`, `QTableView`, `QTreeView`) — как данные выглядят на экране;
3. **Делегат** (`QStyledItemDelegate`) — как рисуются и редактируются отдельные ячейки.

Код связывает модель с представлением:

```python
view.setModel(model)
```

## QStandardItemModel — универсальная модель

`QStandardItemModel` — модель общего назначения, которая хранит элементы `QStandardItem`:

```python
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QListView

model = QStandardItemModel()
for name in ["Аня", "Петя", "Оля"]:
    item = QStandardItem(name)
    model.appendRow(item)

view = QListView()
view.setModel(model)
```

Каждый элемент — объект `QStandardItem`. У него есть текст, иконка, флажки разрешений и **роли**.

## Роли

Данные в элементе хранятся по «ролям» — именованным слотям для разных целей. Основные:

- `Qt.ItemDataRole.DisplayRole` — текст, который показывается;
- `Qt.ItemDataRole.EditRole` — текст для редактирования;
- `Qt.ItemDataRole.ToolTipRole` — всплывающая подсказка;
- `Qt.ItemDataRole.CheckStateRole` — состояние флажка;
- `Qt.ItemDataRole.ForegroundRole` — цвет текста;
- `Qt.ItemDataRole.FontRole` — шрифт.

```python
item = QStandardItem("Важно")
item.setToolTip("Этот элемент важен")
item.setForeground(QBrush(QColor("red")))
item.setCheckable(True)          # включить флажок
```

Читать значения можно через `item.data(role)` или через короткие методы `item.text()`, `item.isCheckable()`.

## QTableView и QStandardItemModel

Для таблицы модель строится через `setItem(row, col, item)`:

```python
from PyQt6.QtWidgets import QTableView, QHeaderView

model = QStandardItemModel(0, 3)   # 0 строк, 3 столбца
model.setHorizontalHeaderLabels(["Имя", "Оценка", "Статус"])

model.appendRow([
    QStandardItem("Аня"),
    QStandardItem("5"),
    QStandardItem("Отлично"),
])
model.appendRow([
    QStandardItem("Петя"),
    QStandardItem("4"),
    QStandardItem("Хорошо"),
])

table = QTableView()
table.setModel(model)
table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
```

`appendRow` принимает список элементов — по одному на столбец. Заголовки задаются через `setHorizontalHeaderLabels`.

## Выделение и текущий элемент

Представление само управляет выделением. Текущий элемент доступен через `selectionModel` и `currentIndex`:

```python
def on_current_changed(current, previous):
    if current.isValid():
        print("Выбрано:", current.data())

table.selectionModel().currentChanged.connect(on_current_changed)
```

`QModelIndex` — «адрес» ячейки. `isValid()` говорит, есть ли за индексом реальный элемент; `data()` читает DisplayRole. Для таблиц у индекса есть `row()` и `column()`.

## Сортировка и прокси-модели

Модель можно сортировать, а между моделью и представлением можно вставить **прокси-модель**, которая фильтрует или сортирует, не трогая исходные данные:

```python
from PyQt6.QtCore import QSortFilterProxyModel, Qt

proxy = QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
proxy.setFilterFixedString("А")

view.setModel(proxy)
```

`QSortFilterProxyModel` — базовый фильтр: `setFilterFixedString` оставляет строки, содержащие подстроку. Представление теперь работает с прокси, а исходная модель неизменна.

## Делегаты: как рисуются ячейки

За отрисовку и редактирование ячейки отвечает делегат. По умолчанию используется `QStyledItemDelegate`, но его можно переопределить. Собственный делегат — класс, наследующий `QStyledItemDelegate`, в котором переопределяют методы:

- `paint()` — как рисовать ячейку;
- `sizeHint()` — какой размер нужен ячейке;
- `createEditor()` — какой виджет использовать для редактирования.

Классический пример — столбец с прогресс-барами:

```python
from PyQt6.QtWidgets import QStyledItemDelegate, QStyle, QApplication
from PyQt6.QtCore import Qt

class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        progress = int(index.data()) or 0
        # рисуем стандартную рамку ячейки
        super().paint(painter, option, index)
        # а поверх — шкалу прогресса
        opt = QStyleOptionProgressBar()
        opt.rect = option.rect.adjusted(4, 4, -4, -4)
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        QApplication.style().drawControl(
            QStyle.ControlElement.CE_ProgressBar, opt, painter
        )

table.setItemDelegateForColumn(2, ProgressDelegate(table))
```

`setItemDelegateForColumn(col, delegate)` назначает делегат конкретному столбцу. Обрати внимание: `index.data()` возвращает значение из модели, а `option.rect` — прямоугольник ячейки. Собственные делегаты — мощный инструмент: в них можно рисовать диаграммы, фото, цветные индикаторы.

## Итог урока

- Модель хранит данные, представление их показывает; связь — `view.setModel(model)`;
- `QStandardItemModel` — универсальная модель; данные лежат по ролям (`DisplayRole` и другие);
- `QListView` и `QTableView` — представления; выделение читается через `selectionModel`;
- `QSortFilterProxyModel` фильтрует и сортирует без изменения модели;
- делегаты (`QStyledItemDelegate`) переопределяют отрисовку и редактирование ячеек.

Теперь задачи.

<!--TASK-->
### Задача 1
Создай `QListView` с моделью `QStandardItemModel`, заполненной пятью языками программирования (Python, Java, C++, JavaScript, Go). При смене выделения печатай в консоль текст выбранного элемента. Убедись, что при первом запуске ничего не печатается, пока ты не кликнешь по элементу.

### Задача 2
Создай `QTableView` с моделью 5 строк и 3 столбцов: Имя, Город, Возраст. Заполни любыми данными. Заголовки столбцов — «Имя», «Город», «Возраст». Сделай так, чтобы при клике на ячейку в консоль печаталось `Строка 2, столбец 1: Москва` (с фактическими номерами и текстом).

### Задача 3
Добавь к таблице из задачи 2 возможность сортировки: сделай заголовки столбцов кликабельными (сортировка по клику). Используй `setSortingEnabled(True)` у представления — при этом сама модель должна сортироваться. Проверь, что клик по заголовку «Возраст» упорядочивает строки по возрасту.

### Задача 4
Помести `QSortFilterProxyModel` между моделью и представлением. Добавь в окно поле ввода `QLineEdit`; при вводе текста модель должна фильтровать строки, у которых имя содержит введённую подстроку (без учёта регистра). Например, при вводе «ан» останутся только строки с «Аня», «Анна» и т.п.

### Задача 5
Создай таблицу с числами 0–100 в третьем столбце и собственным делегатом `ProgressDelegate`, который рисует в этом столбце прогресс-бары (как в примере из теории). Остальные столбцы должны выглядеть стандартно. Убедись, что полосы прогресса видны и растягиваются вместе с окном.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай модель `QStandardItemModel()`, для каждого языка — `QStandardItem(lang)` и `model.appendRow(item)`. Затем `view.setModel(model)`. Выделение: `view.selectionModel().currentChanged.connect(handler)`, где handler принимает `(current, previous)` и печатает `current.data()` при `current.isValid()`.

### Подсказка 2
Создай модель `QStandardItemModel(0, 3)` и задай заголовки через `setHorizontalHeaderLabels(["Имя", "Город", "Возраст"])`. Добавляй строки через `model.appendRow([QStandardItem(...), ...])`. Текущую ячейку читай через `table.selectionModel().currentChanged.connect(handler)`; внутри — `current.row()`, `current.column()`, `current.data()`.

### Подсказка 3
У представления вызови `table.setSortingEnabled(True)`. Клик по заголовку включит сортировку. Важно: при заполнении модели **после** включения сортировки строки могут перескакивать — заполняй модель до `setSortingEnabled(True)`, либо сортируй вручную через `model.sort(...)`.

### Подсказка 4
Создай `proxy = QSortFilterProxyModel()`, затем `proxy.setSourceModel(model)` и `view.setModel(proxy)`. В слоте `edit.textChanged.connect(handler)` вызывай `proxy.setFilterFixedString(text)`. Если текст пуст — фильтр отключается сам (пустая строка не исключает ничего).

### Подсказка 5
Определи класс `ProgressDelegate(QStyledItemDelegate)` с методом `paint`, как в теории: `super().paint(...)`, затем `QStyleOptionProgressBar`, `opt.progress = int(index.data())`, и `QApplication.style().drawControl(QStyle.ControlElement.CE_ProgressBar, opt, painter)`. Подключи: `table.setItemDelegateForColumn(2, ProgressDelegate(table))`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QListView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Языки")
window.resize(300, 250)

model = QStandardItemModel()
for lang in ["Python", "Java", "C++", "JavaScript", "Go"]:
    model.appendRow(QStandardItem(lang))

view = QListView()
view.setModel(model)

def on_current_changed(current, previous):
    if current.isValid():
        print("Выбрано:", current.data())

view.selectionModel().currentChanged.connect(on_current_changed)

layout = QVBoxLayout(window)
layout.addWidget(view)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Модель живёт отдельно от представления: мы наполняем её элементами, не трогая `QListView`. `view.setModel(model)` связывает их. Сигнал `currentChanged` испускается, когда текущий элемент меняется, и передаёт два объекта `QModelIndex` — новый и старый. `current.isValid()` проверяет, что индекс указывает на существующую ячейку, а `current.data()` возвращает текст (DisplayRole). Ничего не печатается при запуске, потому что текущий элемент ещё не выбран — сигнал сработает только после клика.

### Разбор 2
Решение:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Таблица")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Имя", "Город", "Возраст"])

rows = [
    ("Аня", "Москва", "25"),
    ("Петя", "Казань", "30"),
    ("Оля", "Сочи", "22"),
    ("Игорь", "Псков", "35"),
    ("Марина", "Екатеринбург", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

table = QTableView()
table.setModel(model)

def on_current_changed(current, previous):
    if current.isValid():
        print(f"Строка {current.row()}, столбец {current.column()}: "
              f"{current.data()}")

table.selectionModel().currentChanged.connect(on_current_changed)

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Клик по ячейке «Москва» напечатает:

```
Строка 0, столбец 1: Москва
```

Что здесь происходит? `QStandardItemModel(0, 3)` создаёт модель с 0 строк и 3 столбцами. Каждый `appendRow` добавляет строку из трёх `QStandardItem`. `setHorizontalHeaderLabels` задаёт заголовки. Позиция ячейки — `current.row()` и `current.column()`: индексы начинаются с нуля, поэтому строка «Аня» имеет номер 0.

### Разбор 3
Решение:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QWidget, QTableView, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Сортировка")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Имя", "Город", "Возраст"])

rows = [
    ("Аня", "Москва", "25"),
    ("Петя", "Казань", "30"),
    ("Оля", "Сочи", "22"),
    ("Игорь", "Псков", "35"),
    ("Марина", "Екатеринбург", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

table = QTableView()
table.setModel(model)
table.setSortingEnabled(True)   # клик по заголовку сортирует

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `setSortingEnabled(True)` даёт представлению право сортировать модель при клике по заголовку столбца. Qt строит невидимую «сортировочную» память и переставляет строки модели. Отметим важный нюанс: элементы хранятся как строки, поэтому сортировка по «Возраст» будет **лексикографической** — «22», «25», «28», «30», «35» совпадают с числовой, но трёхзначные числа встали бы неверно. Для честной числовой сортировки нужно хранить числа через `item.setData(value, Qt.ItemDataRole.EditRole)` или использовать `QSortFilterProxyModel.setSortRole`.

### Разбор 4
Решение:

```python
import sys
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QWidget, QTableView,
                             QLineEdit, QVBoxLayout)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Фильтр")
window.resize(400, 300)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Имя", "Город", "Возраст"])

rows = [
    ("Аня", "Москва", "25"),
    ("Петя", "Казань", "30"),
    ("Оля", "Сочи", "22"),
    ("Анна", "Псков", "35"),
    ("Марина", "Екатеринбург", "28"),
]
for name, city, age in rows:
    model.appendRow([QStandardItem(name),
                     QStandardItem(city),
                     QStandardItem(age)])

proxy = QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

table = QTableView()
table.setModel(proxy)

edit = QLineEdit()
edit.setPlaceholderText("Фильтр по имени…")

def apply_filter(text):
    proxy.setFilterFixedString(text)

edit.textChanged.connect(apply_filter)

layout = QVBoxLayout(window)
layout.addWidget(edit)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Вводим «ан» — остаются «Аня» и «Анна». Что здесь происходит? Прокси-модель встаёт между моделью и представлением: `table.setModel(proxy)`, а `proxy` оборачивает исходную `model`. `setFilterFixedString` включает фильтр по точному совпадению подстроки в DisplayRole — по умолчанию проверяется первый столбец. `setFilterCaseSensitivity(CaseInsensitive)` делает поиск независимым от регистра. Пустая строка фильтра не исключает ничего, так что очистка поля возвращает все строки. Прокси не трогает исходную модель — важное свойство архитектуры.

### Разбор 5
Решение:

```python
import sys
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (QApplication, QWidget, QTableView,
                             QVBoxLayout, QStyledItemDelegate,
                             QStyleOptionProgressBar, QStyle, QApplication as QtApp)

class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        progress = int(index.data() or 0)
        if not 0 <= progress <= 100:
            return
        opt = QStyleOptionProgressBar()
        opt.rect = option.rect.adjusted(4, 4, -4, -4)
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = f"{progress}%"
        opt.textVisible = True
        QtApp.style().drawControl(
            QStyle.ControlElement.CE_ProgressBar, opt, painter
        )

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Делегат прогресса")
window.resize(400, 250)

model = QStandardItemModel(0, 3)
model.setHorizontalHeaderLabels(["Задача", "Владелец", "Прогресс"])

tasks = [
    ("Парсинг", "Аня", 80),
    ("UI", "Петя", 45),
    ("Тесты", "Оля", 100),
    ("Документация", "Игорь", 15),
]
for task, owner, progress in tasks:
    model.appendRow([QStandardItem(task),
                     QStandardItem(owner),
                     QStandardItem(str(progress))])

table = QTableView()
table.setModel(model)
table.setItemDelegateForColumn(2, ProgressDelegate(table))

layout = QVBoxLayout(window)
layout.addWidget(table)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `ProgressDelegate.paint` вызывается для каждой видимой ячейки третьего столбца. Сначала `super().paint(...)` рисует стандартный фон и рамку, затем на `option.rect` (прямоугольник ячейки) с отступами в 4 пикселя накладывается стилизованная полоса прогресса: `QStyleOptionProgressBar` описывает желаемое состояние, а `drawControl(CE_ProgressBar, opt, painter)` отрисовывает его средствами текущей стилевой темы. Значение читается из модели через `index.data()`. Для остальных столбцов делегат не назначен, поэтому они отображаются по умолчанию.
<!--/SOLUTION-->

<!--QUIZ-->
Что хранит модель в архитектуре Модель-представление?
- Только внешний вид
- Данные и правила доступа к ним
- Позицию окна
* Правильный ответ: Данные и правила доступа к ним
Модель отвечает за данные, представление — за их отображение.

Как связать модель с представлением?
- view.addWidget(model)
- view.setModel(model)
- model.setView(view)
* Правильный ответ: view.setModel(model)
Представление получает модель через setModel.

Какой класс — универсальная модель из стандартных элементов?
- QTableWidget
- QStandardItemModel
- QModelIndex
* Правильный ответ: QStandardItemModel
QStandardItemModel хранит элементы QStandardItem и умеет отдавать их представлениям.

Что возвращает index.data() (индекс элемента)?
- Строку-адрес
- Значение роли DisplayRole
- Объект виджета
* Правильный ответ: Значение роли DisplayRole
data() без аргумента читает роли DisplayRole — текст, показанный в ячейке.

Что означает item.setCheckable(True)?
- Элемент нельзя удалить
- У элемента появится флажок
- Элемент станет невидимым
* Правильный ответ: У элемента появится флажок
Флажок хранится в роли CheckStateRole и управляется пользователем.

Как узнать номер строки текущей ячейки?
- index.row()
- index.line()
- index.number()
* Правильный ответ: index.row()
QModelIndex.row() возвращает номер строки, column() — столбца.

Зачем нужен QSortFilterProxyModel?
- Для ускорения отрисовки
- Для фильтрации и сортировки без изменения исходной модели
- Для объединения нескольких окон
* Правильный ответ: Для фильтрации и сортировки без изменения исходной модели
Прокси превращается между моделью и представлением и модифицирует «вид» данных.

Что делает table.setSortingEnabled(True)?
- Включает сортировку кликом по заголовку столбца
- Запрещает менять порядок строк
- Сортирует сразу при запуске
* Правильный ответ: Включает сортировку кликом по заголовку столбца
Клик по заголовку сортирует строки по этому столбцу.

Какие методы переопределяет собственный делегат?
- paint, sizeHint, createEditor
- draw, resize, move
- update, insert, delete
* Правильный ответ: paint, sizeHint, createEditor
paint рисует ячейку, sizeHint задаёт размер, createEditor создаёт редактор.

Как назначить делегат только третьему столбцу?
- table.setDelegate(delegate)
- table.setItemDelegateForColumn(2, delegate)
- table.setColumnDelegate(3, delegate)
* Правильный ответ: table.setItemDelegateForColumn(2, delegate)
setItemDelegateForColumn(индекс_столбца, делегат) применяет делегат к одному столбцу.
<!--/QUIZ-->
