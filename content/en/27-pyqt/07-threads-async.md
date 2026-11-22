---
title: Threads in GUI: QThread and QThreadPool
summary: Why the UI freezes during long operations, and how to fix it with QThread, the worker + moveToThread pattern, and QThreadPool with QRunnable.
order: 7
duration: 45 min
difficulty: advanced
tags: PyQt6, PySide6, QThread, QThreadPool, QRunnable, threads, async
---

Soon you'll notice: as soon as a long operation appears in the program — downloading a file, processing a large list, querying a database — the window "freezes" and stops responding to clicks. This is a fundamental GUI problem, and today we'll figure out why it happens and how to fix it.

## Why the UI freezes

Remember lesson 1: the `app.exec()` event loop waits for events and dispatches them to handlers. While a handler runs, the loop doesn't spin. If a handler "hangs" for 10 seconds — for all those 10 seconds clicks and keys wait in queue, and the window looks frozen.

```python
# ❌ Don't do this: the slot blocks the event loop
def hard_work():
    time.sleep(5)          # 5 seconds of "dead" pause
    label.setText("Done")

button.clicked.connect(hard_work)
```

Ordinary programs run in a single thread. A **thread** is a separate "line" of execution. To keep the event loop unblocked, long work must be moved to a separate thread, and the result returned to the main one via signals.

## QThread — basic thread

`QThread` is Qt's class for threads. The simplest way is to subclass `QThread` and override `run()`:

```python
from PyQt6.QtCore import QThread, pyqtSignal
import time

class Worker(QThread):
    progress = pyqtSignal(int)        # progress signal
    finished_ok = pyqtSignal(str)     # result signal

    def run(self):
        for i in range(101):
            time.sleep(0.05)
            self.progress.emit(i)
        self.finished_ok.emit("Work finished")
```

Start via `start()`; stop a thread with `quit()` or the `requestInterruption()` flag:

```python
worker = Worker()
worker.progress.connect(progress_bar.setValue)
worker.finished_ok.connect(label.setText)
worker.start()
```

⚠️ IMPORTANT: `run()` methods execute **not** in the main thread, so they must not touch widgets directly. Interaction is only via signals! Qt safely delivers the signal to the main thread if the slot is there.

## The worker + moveToThread pattern

The classic way — a worker class based on `QObject`, with the thread created separately:

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
worker.moveToThread(thread)          # move the worker into the thread
thread.started.connect(worker.work)  # on thread start — begin work
worker.progress.connect(progress_bar.setValue)
worker.finished.connect(thread.quit) # on completion — stop the thread
worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)
thread.start()
```

Breaking down the key points:

- `moveToThread(thread)` "relocates" the object into another thread;
- the `thread.started` signal fires on thread start and launches `work()`;
- `worker.finished` is the signal that returns control to the main thread (the `thread.quit` slot runs there);
- `deleteLater` safely deletes objects after completion.

## QThreadPool and QRunnable

For "short" tasks Qt has a thread pool — `QThreadPool`. A task is an object of class `QRunnable`:

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
        # long work
        for i in range(50):
            time.sleep(0.02)
        self.signals.done.emit(f"Task {self.name} finished")

pool = QThreadPool.globalInstance()   # shared pool
task = Task("A")
task.signals.done.connect(label.setText)
pool.start(task)
```

`QThreadPool` manages threads itself: tasks queue up and run as threads free up. `globalInstance()` is a pool shared by the whole application. `QRunnable` can't have signals directly — so signals live in a separate `QObject` class (e.g., `TaskSignals`).

## Checking: is this the thread?

Sometimes it's important to know which thread runs code (e.g., to avoid touching widgets from a thread):

```python
from PyQt6.QtCore import QThread

print(QThread.currentThread() is QThread.currentThread())  # True
```

In the main thread `QThread.currentThread()` is the "main" thread object. Inside `run()` — the worker thread object.

## Lesson summary

- Long operations in the main thread "freeze" the GUI;
- `QThread` + overriding `run()` — the simplest thread;
- the `worker` + `moveToThread` pattern — separating logic from lifecycle;
- `QThreadPool` + `QRunnable` — a pool for parallel short tasks;
- communicating with the UI only via signals; never touch widgets directly from a thread.

Now practice.

<!--TASK-->
### Task 1
Create a window with a "Start" button and a label. On press — `time.sleep(3)` in the slot, then the label shows "Done". Run the program, press the button, and try moving the window during those 3 seconds. Describe in a code comment what happened and why (this is a demonstration of the problem).

### Task 2
Rewrite the program from task 1 so the pause runs in a `QThread`: create a class `SleepThread(QThread)` with a method `run()` that does `time.sleep(3)` and emits a signal `done = pyqtSignal()`. Connect the signal to a slot that sets "Done". Verify the window stays "alive" during the pause.

### Task 3
Create a thread that counts from 0 to 100 in steps of 1 (delay 0.05 s) and via the signal `progress = pyqtSignal(int)` updates a `QProgressBar` progress bar. On completion — a `finished` signal that outputs "Done!" into a label. Make sure the progress bar fills smoothly and the window doesn't freeze.

### Task 4
Implement the worker + moveToThread pattern: a class `Worker(QObject)` with a method `work()` that does 100 iterations of `time.sleep(0.02)` and emits `progress`. Create a thread via `QThread`, move the worker via `moveToThread`, start it, and connect `finished` to stopping the thread `thread.quit()`. Verify that after the thread completes the program exits cleanly without errors.

### Task 5
Use `QThreadPool` and `QRunnable`: create 5 tasks, each of which "works" for 1 second (a loop of `time.sleep(0.02)`) and emits a `done` signal with the text `Task N finished`. Connect the signals of all tasks to a shared label that shows the last received text. Launch all 5 tasks via `pool.start(task)` and verify they run in parallel (total time — noticeably less than 5 seconds).
<!--/TASK-->

<!--HINT-->
### Hint 1
Create a slot `def start_work(): time.sleep(3); label.setText("Done")` and connect it to `button.clicked`. Try dragging the window during the pause — it "won't listen". This happens because the slot blocks the event loop.

### Hint 2
Create a class `SleepThread(QThread)` with `done = pyqtSignal()` and `run()`, inside which `time.sleep(3)` and `self.done.emit()`. Connect `thread.done.connect(lambda: label.setText("Done"))` and start `thread.start()`. Now the window can be moved.

### Hint 3
In `run()` do `for i in range(101): time.sleep(0.05); self.progress.emit(i)`. The progress bar — `QProgressBar`, create it in the main window and connect `thread.progress.connect(bar.setValue)`. `QProgressBar` has a `setValue` method that takes a number.

### Hint 4
Create `thread = QThread()` and `worker = Worker()`, then `worker.moveToThread(thread)`. Launch: `thread.started.connect(worker.work)`. Completion: `worker.finished.connect(thread.quit)` and `worker.finished.connect(worker.deleteLater)`, plus `thread.finished.connect(thread.deleteLater)`. Don't forget `thread.start()`.

### Hint 5
Create a class `TaskSignals(QObject)` with `done = pyqtSignal(str)` and `Task(QRunnable)` whose `self.signals = TaskSignals()`. In `run()` — a loop and `self.signals.done.emit(...)`. Get `pool = QThreadPool.globalInstance()` and start all 5 tasks. Connect `task.signals.done` to a shared slot that updates the label.
<!--/HINT-->

<!--SOLUTION-->
### Walkthrough 1
Solution:

```python
import sys, time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Freezing")
window.resize(300, 150)

label = QLabel("Waiting…")
button = QPushButton("Start")
layout = QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button)

def start_work():
    # ❌ Blocking the event loop for 3 seconds
    time.sleep(3)
    label.setText("Done")

button.clicked.connect(start_work)

window.show()
sys.exit(app.exec())
```

What's happening here? When you press the button, the `start_work` slot runs in the main thread. `time.sleep(3)` stops execution for 3 seconds — and with it the event loop. The window stops responding: it can't be moved, buttons don't answer. This is a classic "freeze". Note: there's no error — the application is just temporarily dead. Threads solve exactly this problem.

### Walkthrough 2
Solution:

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
window.setWindowTitle("Thread")
window.resize(300, 150)

label = QLabel("Waiting…")
button = QPushButton("Start")
layout = QVBoxLayout(window)
layout.addWidget(label)
layout.addWidget(button)

thread = SleepThread()
thread.done.connect(lambda: label.setText("Done"))

def start():
    label.setText("Waiting…")
    thread.start()

button.clicked.connect(start)

window.show()
sys.exit(app.exec())
```

What's happening here? `run()` executes in a separate thread, so `time.sleep(3)` doesn't touch the event loop — the window stays active and can be moved. When the pause ends, the thread emits the `done` signal, and Qt safely delivers it to the main thread — `label.setText("Done")` runs there. If you press the button again, `thread.start()` starts the thread once more. Note: we don't touch widgets from `run()` — we only emit signals.

### Walkthrough 3
Solution:

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
window.setWindowTitle("Progress")
window.resize(350, 180)

bar = QProgressBar()
label = QLabel("0%")
button = QPushButton("Count")
layout = QVBoxLayout(window)
layout.addWidget(bar)
layout.addWidget(label)
layout.addWidget(button)

thread = CounterThread()
thread.progress.connect(bar.setValue)
thread.progress.connect(lambda v: label.setText(f"{v}%"))
thread.finished_ok.connect(lambda: label.setText("Done!"))
button.clicked.connect(thread.start)

window.show()
sys.exit(app.exec())
```

What's happening here? The thread emits `progress` with numbers 0–100, and both slots (`bar.setValue` and the percentage lambda) run in the main thread. `QProgressBar.setValue` fills the scale. Since the thread lives separately, the UI doesn't freeze. `finished_ok` is called after the loop and changes the label text. Note `button.clicked.connect(thread.start)`: the `start` method is a `QThread` slot, so it can be connected directly.

### Walkthrough 4
Solution:

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
button = QPushButton("Start")
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

What's happening here? `Worker` is a regular `QObject`; it has no thread of its own; `moveToThread(thread)` relocates it. Now `worker.work()` will run in the `thread` when `thread.started` fires. The `progress` signals are delivered to the main thread. `worker.finished` stops the thread (`thread.quit`) and deletes the worker (`deleteLater`), and `thread.finished` deletes the thread itself. This is the standard pattern: it separates logic (`Worker`) from infrastructure (`QThread`). Verify that after completion the program closes without warnings about a "destroyed" thread.

### Walkthrough 5
Solution:

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
        self.signals.done.emit(f"Task {self.name} finished")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("QThreadPool")
window.resize(350, 150)

label = QLabel("Press Start")
button = QPushButton("Start")
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

What's happening here? `Task` inherits `QRunnable` — Qt itself will call `run()` on a free pool thread. Signals can't be declared directly in `QRunnable`, so they are moved into `TaskSignals`. `pool.start(task)` queues the task; the pool uses up to 5–8 threads, so all five tasks run almost simultaneously — about 1 second total instead of 5. `label.setText` updates each time any task finishes.
<!--/SOLUTION-->

<!--QUIZ-->
Why does a long operation in a slot "freeze" the window?
- Python doesn't support parallel tasks
- The slot runs in the main thread and blocks the event loop
- Qt forbids any computation
* Correct answer: The slot runs in the main thread and blocks the event loop
While the slot works, the event loop doesn't process clicks and repaints.

Which QThread method must be overridden to do work in a thread?
- start()
- run()
- exec()
* Correct answer: run()
After start() Qt calls run() in the new thread.

How to update a widget from a thread?
- Call label.setText(...) directly
- Emit a signal and catch it in the main thread
- Via print(...)
* Correct answer: Emit a signal and catch it in the main thread
Widgets are touched only from the main thread; Qt signals are delivered safely.

What does moveToThread(thread) do?
- Starts the thread
- Relocates the object into the given thread
- Creates a new thread
* Correct answer: Relocates the object into the given thread
After moveToThread the object's methods run in the thread it was moved to.

How to launch a task in a thread pool?
- pool.run(task)
- pool.start(task)
- task.start(pool)
* Correct answer: pool.start(task)
QThreadPool.start(QRunnable) queues the task into the pool.

Which class does a task for QThreadPool inherit?
- QThread
- QRunnable
- QObject
* Correct answer: QRunnable
QRunnable is the task interface: Qt calls its run() method.

Can pyqtSignal be declared directly in QRunnable?
- Yes, always
- No, signals need QObject — a separate carrier class is used
- Yes, if inheriting from QThread
* Correct answer: No, signals need QObject — a separate carrier class is used
QRunnable is not a QObject, so signals are moved to a separate class.

What does worker.deleteLater() do after the work finishes?
- Deletes the worker instantly
- Safely deletes the object at the next event
- Nothing
* Correct answer: Safely deletes the object at the next event
deleteLater postpones deletion until returning to the event loop — it's safe for objects in threads.

Why is QThreadPool needed?
- To store widgets
- To reuse threads for short parallel tasks
- To slow the program down
* Correct answer: To reuse threads for short parallel tasks
The pool creates a limited number of threads and distributes the task queue among them.

Which signal reports the start of a QThread?
- started
- begun
- launch
* Correct answer: started
thread.started is emitted when the thread begins execution — it is often used to start a worker object's work.
<!--/QUIZ-->
