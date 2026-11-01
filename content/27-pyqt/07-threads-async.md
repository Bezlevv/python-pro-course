---
title: Потоки в GUI: QThread и QThreadPool
summary: Почему интерфейс замирает при долгих операциях, и как это исправить с помощью QThread, паттерна worker + moveToThread и QThreadPool с QRunnable.
order: 7
duration: 45 мин
difficulty: advanced
tags: PyQt6, PySide6, QThread, QThreadPool, QRunnable, потоки, async
---

Скоро ты заметишь: как только в программе появляется долгая операция — скачивание файла, обработка большого списка, обращение к базе данных — окно «замирает» и перестаёт реагировать на клики. Это фундаментальная проблема GUI, и сегодня мы разберёмся, почему так происходит и как это чинить.

## Почему замирает интерфейс

Вспомни урок 1: цикл событий `app.exec()` ждёт события и рассылает их обработчикам. Пока обработчик работает, цикл не крутится. Если обработчик «завис» на 10 секунд — все эти 10 секунд клики и клавиши ждут своей очереди, и окно выглядит замёрзшим.

```python
# ❌ Так делать нельзя: слот блокирует цикл событий
def hard_work():
    time.sleep(5)          # 5 секунд «мёртвой» паузы
    label.setText("Готово")

button.clicked.connect(hard_work)
```

Обычные программы выполняются в одном потоке. **Поток** (thread) — отдельная «линия» выполнения. Чтобы цикл событий не блокировался, долгую работу нужно выносить в отдельный поток, а результат возвращать в главный через сигналы.

## QThread — базовый поток

`QThread` — класс Qt для потоков. Самый простой способ — унаследовать `QThread` и переопределить метод `run()`:

```python
from PyQt6.QtCore import QThread, pyqtSignal
import time

class Worker(QThread):
    progress = pyqtSignal(int)        # сигнал прогресса
    finished_ok = pyqtSignal(str)     # сигнал результата

    def run(self):
        for i in range(101):
            time.sleep(0.05)
            self.progress.emit(i)
        self.finished_ok.emit("Работа завершена")
```

Запуск — через `start()`; остановить поток можно методом `quit()` или флагом `requestInterruption()`:

```python
worker = Worker()
worker.progress.connect(progress_bar.setValue)
worker.finished_ok.connect(label.setText)
worker.start()
```

⚠️ ВАЖНО: методы `run()` работают **не** в главном потоке, поэтому им нельзя напрямую трогать виджеты. Взаимодействие — только через сигналы! Qt сам безопасно доставит сигнал в главный поток, если слот находится в нём.

## Паттерн worker + moveToThread

Классический способ — класс-работник на базе `QObject`, а поток создаётся отдельно:

```python
from PyQt6.QtCore import QObject, QThread, pyqtSignal
import time

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def work(self):
        for i in range(101):
            time.sleep(0.03)
            self.progress.emit(i)
        self.finished.emit()

thread = QThread()
worker = Worker()
worker.moveToThread(thread)          # переселяем worker в поток
thread.started.connect(worker.work)  # при старте потока — запускаем работу
worker.progress.connect(progress_bar.setValue)
worker.finished.connect(thread.quit) # по завершении — останавливаем поток
worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)
thread.start()
```

Разбор важных моментов:

- `moveToThread(thread)` «переселяет» объект в другой поток;
- сигнал `thread.started` срабатывает при старте потока и запускает `work()`;
- `worker.finished` — сигнал, который вернёт управление главному потоку (слот `thread.quit` выполнится там);
- `deleteLater` безопасно удаляет объекты после завершения.

## QThreadPool и QRunnable

Для «коротких» задач в Qt есть пул потоков — `QThreadPool`. Задача — это объект класса `QRunnable`:

```python
from PyQt6.QtCore import QThreadPool, QRunnable, pyqtSignal, QObject

class TaskSignals(QObject):
    done = pyqtSignal(str)

class Task(QRunnable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.signals = TaskSignals()

    def run(self):
        # долгая работа
        for i in range(50):
            time.sleep(0.02)
        self.signals.done.emit(f"Задача {self.name} завершена")

pool = QThreadPool.globalInstance()   # общий пул
task = Task("A")
task.signals.done.connect(label.setText)
pool.start(task)
```

`QThreadPool` сам управляет потоками: задачи выстраиваются в очередь и выполняются по мере освобождения потоков. `globalInstance()` — разделяемый на всё приложение пул. `QRunnable` не может иметь сигналов напрямую — поэтому сигналы выносятся в отдельный класс `QObject` (например, `TaskSignals`).

## Проверка: поток ли это?

Иногда важно знать, какой поток исполняет код (например, чтобы не трогать виджеты из потока):

```python
from PyQt6.QtCore import QThread

print(QThread.currentThread() is QThread.currentThread())  # True
```

В главном потоке `QThread.currentThread()` — объект «главного» потока. Внутри `run()` — объект рабочего потока.

## Итог урока

- Долгие операции в главном потоке «замораживают» GUI;
- `QThread` + переопределение `run()` — простейший поток;
- паттерн `worker` + `moveToThread` — разделение логики и жизненного цикла;
- `QThreadPool` + `QRunnable` — пул для параллельных коротких задач;
- связь с интерфейсом — только через сигналы, напрямую виджеты из потока не трогают.

Теперь практика.

<!--TASK-->
### Задача 1
Создай окно с кнопкой «Запустить» и ярлыком. По нажатию — `time.sleep(3)` в слоте, затем ярлык покажет «Готово». Запусти программу, нажми кнопку и попробуй в эти 3 секунды подвигать окно. Опиши в комментарии кода, что произошло и почему (это демонстрация проблемы).

### Задача 2
Перепиши программу из задачи 1 так, чтобы пауза выполнялась в `QThread`: создай класс `SleepThread(QThread)` с методом `run()`, который делает `time.sleep(3)` и испускает сигнал `done = pyqtSignal()`. Подключи сигнал к слоту, который ставит «Готово». Проверь, что окно остаётся «живым» во время паузы.

### Задача 3
Создай поток, который считает от 0 до 100 с шагом 1 (задержка 0.05 с) и через сигнал `progress = pyqtSignal(int)` обновляет прогресс-бар `QProgressBar`. По завершении — сигнал `finished`, который выводит «Готово!» в ярлык. Убедись, что шкала прогресса заполняется плавно, а окно не замирает.

### Задача 4
Реализуй паттерн worker + moveToThread: класс `Worker(QObject)` с методом `work()`, который делает 100 итераций по `time.sleep(0.02)` и испускает `progress`. Создай поток через `QThread`, пересели worker через `moveToThread`, запусти и подключи `finished` к остановке потока `thread.quit()`. Проверь, что после завершения потока программа корректно завершается без ошибок.

### Задача 5
Используй `QThreadPool` и `QRunnable`: создай 5 задач, каждая из которых «работает» 1 секунду (цикл из `time.sleep(0.02)`) и испускает сигнал `done` с текстом `Задача N завершена`. Подключи сигналы всех задач к общему ярлыку, который показывает последний полученный текст. Запусти все 5 задач через `pool.start(task)` и убедись, что они выполняются параллельно (суммарное время — заметно меньше 5 секунд).
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай слот `def start_work(): time.sleep(3); label.setText("Готово")` и подключи его к `button.clicked`. Попробуй во время паузы перетащить окно — оно «не слушается». Это происходит потому, что слот блокирует цикл событий.

### Подсказка 2
Создай класс `SleepThread(QThread)` с `done = pyqtSignal()` и `run()`, внутри которого `time.sleep(3)` и `self.done.emit()`. Подключи `thread.done.connect(lambda: label.setText("Готово"))` и запусти `thread.start()`. Теперь окно можно двигать.

### Подсказка 3
В `run()` делай `for i in range(101): time.sleep(0.05); self.progress.emit(i)`. Прогресс-бар — `QProgressBar`, создай его в главном окне и подключи `thread.progress.connect(bar.setValue)`. У `QProgressBar` есть метод `setValue`, который принимает число.

### Подсказка 4
Создай `thread = QThread()` и `worker = Worker()`, затем `worker.moveToThread(thread)`. Запуск: `thread.started.connect(worker.work)`. Завершение: `worker.finished.connect(thread.quit)` и `worker.finished.connect(worker.deleteLater)`, а также `thread.finished.connect(thread.deleteLater)`. Не забудь `thread.start()`.

### Подсказка 5
Создай класс `TaskSignals(QObject)` с `done = pyqtSignal(str)` и `Task(QRunnable)`, у которого `self.signals = TaskSignals()`. В `run()` — цикл и `self.signals.done.emit(...)`. Получи `pool = QThreadPool.globalInstance()` и запусти все 5 задач. Соедини `task.signals.done` с общим слотом, который обновляет ярлык.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import sys, time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Зависание")
window.resize(300, 150)

label = QLabel("Ожидание…")
button = QPushButton("Запустить")
layout = QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button)

def start_work():
    # ❌ Блокируем цикл событий на 3 секунды
    time.sleep(3)
    label.setText("Готово")

button.clicked.connect(start_work)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Когда ты нажимаешь кнопку, слот `start_work` выполняется в главном потоке. `time.sleep(3)` останавливает выполнение на 3 секунды — а вместе с ним и цикл событий. Окно перестаёт реагировать: его нельзя подвигать, кнопки не отвечают. Это классический «фриз» (зависание). Обрати внимание: никакой ошибки нет — просто приложение временно мертво. Именно эту проблему решают потоки.

### Разбор 2
Решение:

```python
import sys, time
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class SleepThread(QThread):
    done = pyqtSignal()

    def run(self):
        time.sleep(3)
        self.done.emit()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Поток")
window.resize(300, 150)

label = QLabel("Ожидание…")
button = QPushButton("Запустить")
layout = QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button)

thread = SleepThread()
thread.done.connect(lambda: label.setText("Готово"))

def start():
    label.setText("Ожидание…")
    thread.start()

button.clicked.connect(start)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `run()` выполняется в отдельном потоке, поэтому `time.sleep(3)` не трогает цикл событий — окно остаётся активным и его можно двигать. Когда пауза заканчивается, поток испускает сигнал `done`, и Qt безопасно доставляет его в главный поток — `label.setText("Готово")` выполняется там. Если нажать кнопку повторно, `thread.start()` снова запустит поток. Обрати внимание: мы не трогаем виджеты из `run()` — только испускаем сигналы.

### Разбор 3
Решение:

```python
import sys, time
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QProgressBar, QVBoxLayout)

class CounterThread(QThread):
    progress = pyqtSignal(int)
    finished_ok = pyqtSignal()

    def run(self):
        for i in range(101):
            time.sleep(0.05)
            self.progress.emit(i)
        self.finished_ok.emit()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Прогресс")
window.resize(350, 180)

bar = QProgressBar()
label = QLabel("0%")
button = QPushButton("Считать")
layout = QVBoxLayout(window)
layout.addWidget(bar)
layout.addWidget(label)
layout.addWidget(button)

thread = CounterThread()
thread.progress.connect(bar.setValue)
thread.progress.connect(lambda v: label.setText(f"{v}%"))
thread.finished_ok.connect(lambda: label.setText("Готово!"))
button.clicked.connect(thread.start)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? Поток испускает `progress` с числами 0–100, и оба слота (`bar.setValue` и лямбда с процентом) выполняются в главном потоке. `QProgressBar.setValue` заполняет шкалу. Так как поток живёт отдельно, UI не замирает. `finished_ok` вызывается после цикла и меняет текст ярлыка. Обрати внимание на `button.clicked.connect(thread.start)`: метод `start` — слот `QThread`, его можно подключать напрямую.

### Разбор 4
Решение:

```python
import sys, time
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QProgressBar, QVBoxLayout)

class Worker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def work(self):
        for i in range(101):
            time.sleep(0.02)
            self.progress.emit(i)
        self.finished.emit()

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Worker + moveToThread")
window.resize(350, 180)

bar = QProgressBar()
label = QLabel("0%")
button = QPushButton("Запустить")
layout = QVBoxLayout(window)
layout.addWidget(bar)
layout.addWidget(label)
layout.addWidget(button)

thread = QThread()
worker = Worker()
worker.moveToThread(thread)

thread.started.connect(worker.work)
worker.progress.connect(bar.setValue)
worker.progress.connect(lambda v: label.setText(f"{v}%"))
worker.finished.connect(thread.quit)
worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)

button.clicked.connect(thread.start)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `Worker` — обычный `QObject`, у него нет своего потока; `moveToThread(thread)` переселяет его. Теперь `worker.work()` запустится в потоке `thread`, когда сработает `thread.started`. Сигналы `progress` доставляются в главный поток. `worker.finished` останавливает поток (`thread.quit`) и удаляет worker (`deleteLater`), а `thread.finished` удаляет сам поток. Это паттерн-стандарт: он разделяет логику (`Worker`) и инфраструктуру (`QThread`). Проверь, что после завершения программа закрывается без предупреждений о «уничтоженном» потоке.

### Разбор 5
Решение:

```python
import sys, time
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class TaskSignals(QObject):
    done = pyqtSignal(str)

class Task(QRunnable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.signals = TaskSignals()

    def run(self):
        for _ in range(50):
            time.sleep(0.02)
        self.signals.done.emit(f"Задача {self.name} завершена")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QThreadPool")
window.resize(350, 150)

label = QLabel("Нажми Запустить")
button = QPushButton("Запустить")
layout = QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button)

pool = QThreadPool.globalInstance()

def start_tasks():
    for i in range(5):
        task = Task(str(i + 1))
        task.signals.done.connect(label.setText)
        pool.start(task)

button.clicked.connect(start_tasks)

window.show()
sys.exit(app.exec())
```

Что здесь происходит? `Task` наследует `QRunnable` — Qt сам вызовет `run()` на свободном потоке пула. Сигналы не могут объявляться прямо в `QRunnable`, поэтому они вынесены в `TaskSignals`. `pool.start(task)` ставит задачу в очередь; пул использует до 5-8 потоков, поэтому все пять задач выполняются почти одновременно — суммарно около 1 секунды вместо 5. `label.setText` обновляется каждый раз, когда любая задача завершается.
<!--/SOLUTION-->

<!--QUIZ-->
Почему долгая операция в слоте «замораживает» окно?
- Python не поддерживает параллельные задачи
- Слот выполняется в главном потоке и блокирует цикл событий
- Qt запрещает любые вычисления
* Правильный ответ: Слот выполняется в главном потоке и блокирует цикл событий
Пока слот работает, цикл событий не обрабатывает клики и перерисовку.

Какой метод QThread нужно переопределить для выполнения работы в потоке?
- start()
- run()
- exec()
* Правильный ответ: run()
После start() Qt вызывает run() в новом потоке.

Как из потока обновить виджет?
- Напрямую вызвать label.setText(...)
- Испустить сигнал и поймать его в главном потоке
- Через print(...)
* Правильный ответ: Испустить сигнал и поймать его в главном потоке
Виджеты трогают только из главного потока; сигналы Qt доставляются безопасно.

Что делает moveToThread(thread)?
- Запускает поток
- Переселяет объект в заданный поток
- Создаёт новый поток
* Правильный ответ: Переселяет объект в заданный поток
После moveToThread методы объекта выполняются в потоке, куда его переселили.

Как запустить задачу в пуле потоков?
- pool.run(task)
- pool.start(task)
- task.start(pool)
* Правильный ответ: pool.start(task)
QThreadPool.start(QRunnable) ставит задачу в очередь пула.

Какой класс наследует задача для QThreadPool?
- QThread
- QRunnable
- QObject
* Правильный ответ: QRunnable
QRunnable — интерфейс задачи: Qt вызывает его метод run().

Можно ли объявить pyqtSignal прямо в QRunnable?
- Да, всегда
- Нет, сигналы нужен QObject — используют отдельный класс-носитель
- Да, если наследовать от QThread
* Правильный ответ: Нет, сигналы нужен QObject — используют отдельный класс-носитель
QRunnable не является QObject, поэтому сигналы выносятся в отдельный класс.

Что делает worker.deleteLater() после завершения работы?
- Мгновенно удаляет worker
- Безопасно удаляет объект при следующем событии
- Ничего
* Правильный ответ: Безопасно удаляет объект при следующем событии
deleteLater откладывает удаление до возврата в цикл событий — это безопасно для объектов в потоках.

Зачем нужен QThreadPool?
- Чтобы хранить виджеты
- Чтобы переиспользовать потоки для коротких параллельных задач
- Чтобы замедлить программу
* Правильный ответ: Чтобы переиспользовать потоки для коротких параллельных задач
Пул создаёт ограниченное число потоков и распределяет между ними очередь задач.

Какой сигнал сообщает о старте потока QThread?
- started
- begun
- launch
* Правильный ответ: started
thread.started испускается, когда поток начинает выполнение — к нему часто подключают запуск работы worker-объекта.
<!--/QUIZ-->
