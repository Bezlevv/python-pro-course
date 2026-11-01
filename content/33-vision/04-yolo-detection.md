---
title: Детекция объектов: YOLO
summary: Нейросети детекции объектов, Ultralytics YOLO, предсказания, фильтрация по уверенности, аннотации.
order: 4
duration: 50 мин
difficulty: advanced
tags: yolo, ultralytics, детекция, нейросети
---

Классические методы вроде каскадов Хаара умеют находить только один тип объектов (лица) и требуют отдельного обучения под каждую задачу. Современная детекция объектов работает иначе: одна нейросеть за один проход находит все объекты на изображении, рисует вокруг них рамки и сообщает класс каждого объекта и уверенность. Самый известный представитель такого подхода — YOLO (You Only Look Once).

## Что такое YOLO

YOLO делит изображение на сетку и сразу предсказывает для каждой ячейки: какие объекты в ней находятся, где их рамки (bounding boxes) и насколько модель уверена в каждом предсказании. Отсюда и название — «смотришь один раз». Это делает YOLO очень быстрым: он обрабатывает десятки кадров в секунду и может работать на видео в реальном времени.

## Ultralytics YOLO

В Python самые удобные готовые модели YOLO даёт библиотека Ultralytics:

```bash
pip install ultralytics
```

Модель загружается одной строкой — программировать архитектуру нейросети не нужно:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")   # предобученная нейросеть (n — nano, самая лёгкая)
```

При первом вызове Ultralytics скачает веса модели из интернета (примерно 6 МБ). Теперь предскажем объекты на изображении:

```python
results = model.predict(source="photo.jpg", conf=0.5)
```

`conf=0.5` — порог уверенности: предсказания слабее 50% отбрасываются.

## Структура результата

`model.predict` возвращает список `results` — по одному объекту на каждое изображение (можно передать папку сразу с несколькими). Для одного изображения берём `results[0]`.

```python
result = results[0]

# Рамки: тензор (N, 4) — координаты x1, y1, x2, y2
boxes = result.boxes.xyxy
# Уверенность: тензор (N,)
confs = result.boxes.conf
# Классы: тензор (N,)
classes = result.boxes.cls
# Имена классов
names = result.names
```

Разберём один объект:

```python
for box, conf, cls in zip(boxes, confs, classes):
    x1, y1, x2, y2 = map(int, box.tolist())
    label = names[int(cls)]
    print(f"{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]")
```

Вывод будет примерно таким:

```
person: 0.92 [112, 48, 340, 512]
car: 0.87 [540, 260, 800, 420]
```

## Аннотация результата

Ultralytics умеет рисовать рамки и подписи сама — метод `plot()` возвращает изображение в формате BGR, готовое для сохранения:

```python
annotated = result.plot()          # BGR-массив с рамками
cv2.imwrite("annotated.jpg", annotated)
```

## Обработка списка объектов

Часто нужно не просто увидеть рамки, а посчитать объекты или отфильтровать их. Например, сколько людей на кадре:

```python
people = sum(1 for cls in classes if names[int(cls)] == "person")
```

## Куда дальше

У Ultralytics есть предобученные модели разных размеров: `yolov8n.pt` (nano), `yolov8s.pt` (small), `yolov8m.pt` (medium). Чем больше модель, тем выше точность, но ниже скорость. Кроме того, самые модели можно дообучать на своих данных — это тема отдельного курса. Мы же сосредоточимся на использовании готовой модели.

## Итог

Детекция через YOLO — это три шага: загрузить модель (`YOLO("yolov8n.pt")`), вызвать `predict` и разобрать `result.boxes`. Данные рамок лежат в тензорах PyTorch, поэтому для удобства их переводят в Python-списки через `tolist()`. Закрепим практикой.

<!--TASK-->
### Задача 1
Напиши функцию `load_and_predict(model_path, image_path)`, которая загружает модель YOLO и вызывает `predict` с порогом `conf=0.5`. Для каждого найденного объекта выведи на экран строку вида `класс: уверенность [x1, y1, x2, y2]`. Для преобразования координат в int используй `map(int, box.tolist())`. Если результат пуст, выведи `Объектов не найдено`.

### Задача 2
Напиши функцию `annotate_image(model_path, image_path, out_path)`, которая делает предсказание, получает аннотированное изображение через `result.plot()`, сохраняет его по указанному пути и возвращает `None`. Проверь, что файл на диске появился и его размер больше нуля. Используй `os.path.getsize` для проверки.

### Задача 3
Напиши функцию `count_detections(results)`, которая принимает список результатов и возвращает общее количество объектов во всех изображениях (сумму длин `boxes` по всем результатам). В качестве фиктивных данных можно передать пустой список — функция должна вернуть 0. Проверь на реальном предсказании: число объектов должно совпасть с количеством напечатанных строк из задачи 1.

### Задача 4
Напиши функцию `parse_boxes(result, conf_thr=0.5)`, которая возвращает список словарей вида `{"class": имя_класса, "conf": float, "box": (x1, y1, x2, y2)}` для всех объектов с уверенностью не ниже `conf_thr`. Напиши **pytest-тесты**: создай фиктивный объект результата с известными полями (через простой класс с атрибутами `boxes`, `names` и тензорами `torch.tensor`) и проверь, что фильтрация по порогу работает и что координаты преобразуются в кортеж int. Запусти тесты.

### Задача 5
Напиши функцию `most_frequent_class(result)`, которая возвращает строку с названием класса, который встречается чаще всего (при равенстве — любой). Напиши **pytest-тесты**: создай фиктивный результат с классами `[0, 1, 0, 2, 0]` и именами `{0: "person", 1: "car", 2: "dog"}` — функция должна вернуть `"person"`. Также проверь поведение на пустом результате: функция должна вернуть `None`. Запусти тесты.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Модель: `model = YOLO(model_path)`. Предсказание: `results = model.predict(source=image_path, conf=0.5)`. Данные: `boxes = results[0].boxes.xyxy`, `confs = results[0].boxes.conf`, `classes = results[0].boxes.cls`, `names = results[0].names`.

### Подсказка 2
Аннотация: `annotated = results[0].plot()` — массив в BGR. Сохраняй через `cv2.imwrite(out_path, annotated)`. Размер файла: `os.path.getsize(out_path) > 0`.

### Подсказка 3
Общее число объектов: `sum(len(r.boxes) for r in results)`. Для пустого списка сумма будет равна 0.

### Подсказка 4
Создай класс `class FakeBoxes: pass` с атрибутами `xyxy = torch.tensor([[10, 20, 30, 40]])`, `conf = torch.tensor([0.7])`, `cls = torch.tensor([0])`, и `class FakeResult` с `boxes = FakeBoxes()` и `names = {0: "person"}`. Сравнивай результат с ожидаемым списком словарей.

### Подсказка 5
Подсчитай частоты через обычный словарь или `collections.Counter`. Для пустого результата верни `None`. Обрати внимание: классы — это индексы, а вернуть нужно имя из `names`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from ultralytics import YOLO

def load_and_predict(model_path, image_path):
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=0.5)
    result = results[0]
    boxes = result.boxes.xyxy
    confs = result.boxes.conf
    classes = result.boxes.cls
    names = result.names
    if len(boxes) == 0:
        print("Объектов не найдено")
        return
    for box, conf, cls in zip(boxes, confs, classes):
        x1, y1, x2, y2 = map(int, box.tolist())
        label = names[int(cls)]
        print(f"{label}: {conf:.2f} [{x1}, {y1}, {x2}, {y2}]")

load_and_predict("yolov8n.pt", "photo.jpg")
```

Результат (пример):

```
person: 0.92 [112, 48, 340, 512]
car: 0.87 [540, 260, 800, 420]
```

Что здесь происходит? `model.predict` возвращает список результатов — по одному на изображение. `result.boxes.xyxy` — тензор координат рамок в формате `(x1, y1, x2, y2)` (левый верхний и правый нижний углы). `map(int, box.tolist())` превращает числа из тензора в обычные целые. Класс — это индекс, а имя берётся из словаря `result.names`.

### Разбор 2
Решение:

```python
import os
import cv2
from ultralytics import YOLO

def annotate_image(model_path, image_path, out_path):
    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=0.5)
    annotated = results[0].plot()
    cv2.imwrite(out_path, annotated)
    print(f"Сохранено в {out_path}, размер {os.path.getsize(out_path)} байт")

annotate_image("yolov8n.pt", "photo.jpg", "annotated.jpg")
```

Что здесь происходит? `result.plot()` рисует рамки, подписи классов и проценты уверенности прямо на копии изображения и возвращает BGR-массив. Дальше всё как обычно: `cv2.imwrite`. `os.path.getsize` проверяет, что файл реально создан. Такой же подход используется, когда нужно показать детекцию на видео — каждый кадр обрабатывается и аннотируется.

### Разбор 3
Решение:

```python
def count_detections(results):
    return sum(len(r.boxes) for r in results)
```

Что здесь происходит? Каждый элемент `results` имеет атрибут `boxes`, а у него — `.xyxy` с одной строкой на объект, поэтому `len(r.boxes)` — количество объектов на одном изображении. Суммируем по всем результатам. Для пустого списка генератор ничего не даст, и сумма будет 0. Эту функцию удобно использовать вместе с задачей 1 — число строк на экране должно совпасть с её возвратом.

### Разбор 4
Решение:

```python
import torch

def parse_boxes(result, conf_thr=0.5):
    parsed = []
    boxes = result.boxes.xyxy
    confs = result.boxes.conf
    classes = result.boxes.cls
    for box, conf, cls in zip(boxes, confs, classes):
        if conf.item() < conf_thr:
            continue
        x1, y1, x2, y2 = map(int, box.tolist())
        parsed.append({
            "class": result.names[int(cls)],
            "conf": conf.item(),
            "box": (x1, y1, x2, y2),
        })
    return parsed
```

Тесты:

```python
class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([
            [10, 20, 30, 40],
            [50, 60, 70, 80],
        ])
        self.conf = torch.tensor([0.9, 0.3])
        self.cls = torch.tensor([0, 1])

class FakeResult:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

def test_parse_boxes_filter():
    res = parse_boxes(FakeResult(), conf_thr=0.5)
    assert len(res) == 1
    assert res[0]["class"] == "person"
    assert res[0]["conf"] == 0.9
    assert res[0]["box"] == (10, 20, 30, 40)

def test_parse_boxes_all():
    res = parse_boxes(FakeResult(), conf_thr=0.0)
    assert len(res) == 2
    assert res[1]["class"] == "car"
```

Что здесь происходит? Мы не можем в тестах запускать нейросеть — это долго и требует скачивания весов. Поэтому создаём фиктивный класс с теми же атрибутами, что у настоящего результата. Ключевой момент: значения из тензоров PyTorch извлекаются через `.item()` и `.tolist()`. Фильтрация по порогу отбрасывает объект с уверенностью 0.3 — его нет в первом тесте, но он появляется при пороге 0.0 во втором.

### Разбор 5
Решение:

```python
from collections import Counter

def most_frequent_class(result):
    classes = result.boxes.cls
    if len(classes) == 0:
        return None
    counter = Counter(int(cls) for cls in classes)
    top_index = counter.most_common(1)[0][0]
    return result.names[top_index]
```

Тесты:

```python
import torch

class FakeBoxes:
    def __init__(self):
        self.cls = torch.tensor([0, 1, 0, 2, 0])

class FakeResult:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car", 2: "dog"}

def test_most_frequent_person():
    assert most_frequent_class(FakeResult()) == "person"

class FakeEmptyBoxes:
    def __init__(self):
        self.cls = torch.tensor([])

class FakeEmptyResult:
    def __init__(self):
        self.boxes = FakeEmptyBoxes()
        self.names = {}

def test_most_frequent_empty():
    assert most_frequent_class(FakeEmptyResult()) is None
```

Что здесь происходит? `collections.Counter` считает вхождения каждого класса. `most_common(1)` возвращает список из одного элемента — пару `(класс, количество)`, из которой берём индекс. Затем по индексу достаём имя из `result.names`. В фиктивных данных класс 0 (`person`) встречается трижды, поэтому ответ — `"person"`. Пустой результат обрабатывается отдельно: если объектов нет, возвращаем `None`, а не падаем с ошибкой индексации.
<!--/SOLUTION-->

<!--QUIZ-->
Что означает расшифровка YOLO?
- You Only Look Once — «смотришь один раз»
- Your Own Local Objects
- Yielding Object Learning Output
* Правильный ответ: You Only Look Once — «смотришь один раз»
Сеть осматривает изображение за один проход.

Какая библиотека даёт готовые модели YOLO в Python?
- ultralytics
- scikit-learn
- pygame
* Правильный ответ: ultralytics
Ultralytics поддерживает модели YOLOv8 и новее.

Что делает YOLO("yolov8n.pt")?
- Загружает предобученную модель YOLOv8 nano
- Запускает обучение
- Устанавливает CUDA
* Правильный ответ: Загружает предобученную модель YOLOv8 nano
Буква n — nano, самая лёгкая версия.

Какой формат координат рамок в result.boxes.xyxy?
- (x1, y1, x2, y2) — два противоположных угла
- (x, y, w, h) — угол и размеры
- (cx, cy, w, h) — центр и размеры
* Правильный ответ: (x1, y1, x2, y2) — два противоположных угла
xyxy хранит левый верхний и правый нижний углы.

Что означает параметр conf в predict?
- Порог уверенности: слабее отбрасываются
- Число объектов
- Размер рамки
* Правильный ответ: Порог уверенности: слабее отбрасываются
Для conf=0.5 останутся предсказания с уверенностью от 50%.

Как получить имя класса по его индексу?
- result.names[int(cls)]
- result.labels[cls]
- result.classes[cls]
* Правильный ответ: result.names[int(cls)]
names — словарь, где индекс соответствует названию класса.

Что возвращает result.plot()?
- Аннотированное изображение в BGR
- Список рамок
- Текст отчёта
* Правильный ответ: Аннотированное изображение в BGR
plot рисует рамки и подписи и возвращает numpy-массив.

Что делают тензоры PyTorch в API Ultralytics?
- Хранят координаты, уверенности и классы
- Управляют GPU-памятью вручную
- Заменяют numpy полностью
* Правильный ответ: Хранят координаты, уверенности и классы
boxes, conf, cls — тензоры, значения берут через .tolist() и .item().

Какая модель точнее — yolov8n или yolov8m?
- yolov8m (medium)
- yolov8n (nano)
- Они одинаковые
* Правильный ответ: yolov8m (medium)
Больше модель — выше точность, но ниже скорость.

Что вернёт predict для пустого изображения?
- Пустые тензоры рамок, проверностей и классов
- None
- Ошибку
* Правильный ответ: Пустые тензоры рамок, уверностей и классов
Список объектов просто будет пустым.
<!--/QUIZ-->
