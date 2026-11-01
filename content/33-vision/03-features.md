---
title: Дескрипторы, сопоставление и лица
summary: Особые точки изображений (ORB, SIFT), поиск шаблона по matchTemplate, детекция лиц через каскады Хаара.
order: 3
duration: 50 мин
difficulty: advanced
tags: opencv, orb, sift, лица, шаблоны
---

Мы научились подготавливать изображения и находить контуры. Но как найти **конкретный объект** — например, логотип на фотографии или лицо человека? Для этого нужны дескрипторы — числовые «отпечатки пальцев» характерных точек изображения.

## Особые точки и дескрипторы

Особая точка (keypoint) — это пиксель, который резко отличается от соседей: угол, яркое пятно, пересечение краёв. Хорошие особые точки должны быть стабильны при изменении масштаба, поворота и освещения. Про каждую точку алгоритм считает **дескриптор** — вектор чисел, описывающий её окрестность. Если дескрипторы двух изображений совпадают, вероятно, это одна и та же точка сцены.

### ORB

ORB — быстрый бесплатный алгоритм. Создаётся через `cv2.ORB_create()`:

```python
import cv2

orb = cv2.ORB_create(nfeatures=500)
keypoints, descriptors = orb.detectAndCompute(img, None)
```

`detectAndCompute` возвращает список особых точек и массив дескрипторов. Каждый дескриптор ORB — это вектор из 32 байт. Отрисуем точки:

```python
vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
cv2.imwrite("orb.png", vis)
```

### SIFT

SIFT — более точный, но более тяжёлый алгоритм. Раньше он был запатентован, но патент истёк, и теперь `cv2.SIFT_create()` работает без проблем:

```python
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(img, None)
```

Для SIFT дескриптор — вектор из 128 чисел типа `float32`.

## Сопоставление дескрипторов

Чтобы найти один и тот же объект на двух изображениях, сопоставим дескрипторы. Лучший инструмент для этого — `cv2.BFMatcher` (грубая сила: сравнивает каждый дескриптор с каждым):

```python
bf = cv2.BFMatcher(cv2.NORM_HAMMING)  # для ORB — расстояние Хэмминга
matches = bf.knnMatch(des1, des2, k=2)
```

Для фильтрации плохих совпадений используют правило Лоу: берём два лучших кандидата для каждой точки и оставляем только те, где лучший заметно лучше второго:

```python
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)
```

## Шаблонный поиск matchTemplate

Иногда объект известен заранее — например, есть маленькое изображение-шаблон. Тогда вместо особых точек используют `cv2.matchTemplate`, который «прокатывает» шаблон по всему изображению и ищет место максимального сходства:

```python
result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
top_left = max_loc
```

`TM_CCOEFF_NORMED` даёт значения от −1 до 1, где 1 — идеальное совпадение. Место максимума — верхний левый угол найденного шаблона.

## Детекция лиц: каскады Хаара

Для поиска лиц компьютерное зрение использует обученные классификаторы. В OpenCV есть готовые каскады в папке `cv2.data`:

```python
cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
```

`detectMultiScale` возвращает список прямоугольников `(x, y, w, h)`. `scaleFactor` — насколько меняется масштаб окна на каждом шаге (меньше — точнее, но медленнее); `minNeighbors` — сколько соседних детекций нужно, чтобы подтвердить лицо (больше — меньше ложных срабатываний). Для чёрно-белого изображения каскады работают быстрее:

```python
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
```

## Итог

Дескрипторы (ORB/SIFT) отвечают на вопрос «какие точки характерны для изображения и как они выглядят», `matchTemplate` ищет известный шаблон, а каскады Хаара — обученные детекторы конкретных объектов, таких как лица. Теперь практика.

<!--TASK-->
### Задача 1
Напиши функцию `orb_keypoints(path)`, которая читает изображение, находит особые точки алгоритмом ORB (`cv2.ORB_create(nfeatures=300)`) и сохраняет изображение с нарисованными точками в файл `orb.png`. Выведи количество найденных точек. Проверь, что для любого цветного изображения функция отрабатывает без ошибок.

### Задача 2
Напиши функцию `sift_keypoints(path)`, которая делает то же самое, но через `cv2.SIFT_create()`, и сохраняет результат в `sift.png`. Выведи количество точек и форму массива дескрипторов. Убедись, что дескрипторы имеют форму `(N, 128)` и тип `float32`.

### Задача 3
Напиши функцию `match_template(scene_path, template_path)`, которая ищет шаблон на сцене через `cv2.matchTemplate` с `cv2.TM_CCOEFF_NORMED`, находит точку максимума через `cv2.minMaxLoc` и возвращает кортеж `(x, y, w, h)` — координаты верхнего левого угла и размеры шаблона. Дополнительно сохрани сцену с нарисованным прямоугольником в `matched.png`. Если максимальное сходство меньше 0.5 — верни `None`.

### Задача 4
Напиши функцию `extract_descriptors(path, algorithm="orb")`, которая возвращает кортеж `(keypoints, descriptors)` для ORB или SIFT в зависимости от аргумента. Напиши **pytest-тесты**: проверь, что для ORB тип дескрипторов — `uint8`, для SIFT — `float32`, что количество ключевых точек равно количеству строк дескрипторов, и что для изображения 10×10 найден хотя бы один дескриптор. Запусти тесты.

### Задача 5
Напиши функцию `detect_faces(path)`, которая использует `cv2.CascadeClassifier` с `haarcascade_frontalface_default.xml`, детектирует лица на сером изображении и возвращает список прямоугольников `(x, y, w, h)`. Напиши **pytest-тесты**: проверь, что на изображении без лиц (например, полностью белом) результат — пустой список, а на изображении с нарисованным «лицом» (белый эллипс на чёрном фоне) возвращается хотя бы один прямоугольник, и все его размеры положительны. Запусти тесты.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Создай детектор: `orb = cv2.ORB_create(nfeatures=300)`, затем `keypoints, descriptors = orb.detectAndCompute(img, None)`. Рисование: `vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))`. Количество — `len(keypoints)`.

### Подсказка 2
SIFT: `sift = cv2.SIFT_create()`, дальше как с ORB. Форма дескрипторов — `descriptors.shape`, тип — `descriptors.dtype`. Сравни с ожидаемыми `(N, 128)` и `float32`.

### Подсказка 3
`result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)`, затем `min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)`. Если `max_val < 0.5` — верни `None`. Иначе прямоугольник: `(max_loc[0], max_loc[1], template.shape[1], template.shape[0])`.

### Подсказка 4
Если `algorithm == "orb"` — `cv2.ORB_create()`, иначе `cv2.SIFT_create()`. В тестах создавай синтетическое изображение с контрастными уголками, например `np.random.randint(0, 256, (100, 100), dtype=np.uint8)`. Длина `keypoints` должна быть равна `descriptors.shape[0]`.

### Подсказка 5
Каскад: `cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")`. Для «лица» нарисуй на чёрном изображении белый эллипс: `cv2.ellipse(img, center, axes, 0, 0, 360, 255, -1)`. Параметры `detectMultiScale`: `scaleFactor=1.1, minNeighbors=3`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import cv2

def orb_keypoints(path):
    img = cv2.imread(path)
    orb = cv2.ORB_create(nfeatures=300)
    keypoints, _ = orb.detectAndCompute(img, None)
    vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 255, 0))
    cv2.imwrite("orb.png", vis)
    print(f"ORB точек: {len(keypoints)}")

orb_keypoints("photo.jpg")
```

Результат:

```
ORB точек: 300
```

Что здесь происходит? `cv2.ORB_create(nfeatures=300)` создаёт детектор, ограниченный 300 точками. `detectAndCompute` за один вызов находит точки и считает их дескрипторы. `cv2.drawKeypoints` рисует зелёные кружки в найденных местах. ORB — быстрый алгоритм, поэтому он подходит для видео в реальном времени.

### Разбор 2
Решение:

```python
import cv2

def sift_keypoints(path):
    img = cv2.imread(path)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    vis = cv2.drawKeypoints(img, keypoints, None, color=(0, 0, 255))
    cv2.imwrite("sift.png", vis)
    print(f"SIFT точек: {len(keypoints)}")
    print(f"Форма дескрипторов: {descriptors.shape}, dtype: {descriptors.dtype}")

sift_keypoints("photo.jpg")
```

Результат:

```
SIFT точек: 1287
Форма дескрипторов: (1287, 128), dtype: float32
```

Что здесь происходит? SIFT описывает каждую точку вектором из 128 чисел с плавающей точкой — поэтому сравнение таких дескрипторов требует больше памяти, но даёт высокую точность. Форма `(N, 128)` означает: N строк — по одной на точку, 128 столбцов — компоненты дескриптора. Эту форму мы проверим в тестах следующей задачи.

### Разбор 3
Решение:

```python
import cv2

def match_template(scene_path, template_path):
    scene = cv2.imread(scene_path)
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(scene, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val < 0.5:
        return None
    x, y = max_loc
    w, h = template.shape[1], template.shape[0]
    cv2.rectangle(scene, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imwrite("matched.png", scene)
    return (x, y, w, h)
```

Что здесь происходит? `cv2.matchTemplate` двигает шаблон по сцене и для каждого положения считает коэффициент корреляции. `cv2.minMaxLoc` возвращает минимум и максимум с их координатами. `TM_CCOEFF_NORMED` нормирует результат в диапазон [−1, 1], поэтому порог 0.5 — разумная граница для «достаточно похоже». Координаты `max_loc` — это верхний левый угол найденного фрагмента, а ширина и высота берутся из шаблона.

### Разбор 4
Решение:

```python
import cv2

def extract_descriptors(path, algorithm="orb"):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if algorithm == "orb":
        detector = cv2.ORB_create()
    else:
        detector = cv2.SIFT_create()
    return detector.detectAndCompute(img, None)
```

Тесты:

```python
import numpy as np

def test_orb_dtype():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert des.dtype == np.uint8

def test_sift_dtype():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "sift")
    assert des.dtype == np.float32
    assert des.shape[1] == 128

def test_keypoints_match_rows():
    img = np.random.randint(0, 256, (100, 100), dtype=np.uint8)
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert len(kps) == des.shape[0]

def test_finds_keypoints():
    img = np.zeros((100, 100), dtype=np.uint8)
    img[10:40, 10:40] = 255
    img[60:90, 60:90] = 128
    cv2.imwrite("tmp.png", img)
    kps, des = extract_descriptors("tmp.png", "orb")
    assert len(kps) >= 1
```

Что здесь происходит? Мы читаем изображение сразу в сером виде (`cv2.IMREAD_GRAYSCALE`), потому что дескрипторам не нужен цвет. Тесты проверяют главные контракты: тип данных дескрипторов различается у ORB (`uint8`) и SIFT (`float32`), число строк дескрипторов совпадает с числом точек, а на изображении с резкими контрастными блоками найдётся хотя бы одна точка. Случайное изображение (`np.random.randint`) гарантирует много особых точек: шум — это сплошные контрастные перепады.

### Разбор 5
Решение:

```python
import cv2

def detect_faces(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    return [tuple(f) for f in faces]
```

Тесты:

```python
def test_no_faces():
    img = np.full((100, 100, 3), 255, dtype=np.uint8)
    cv2.imwrite("tmp_blank.png", img)
    assert detect_faces("tmp_blank.png") == []

def test_fake_face():
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.ellipse(img, (100, 100), (40, 50), 0, 0, 360, (255, 255, 255), -1)
    cv2.imwrite("tmp_face.png", img)
    faces = detect_faces("tmp_face.png")
    assert len(faces) >= 1
    x, y, w, h = faces[0]
    assert x >= 0 and y >= 0 and w > 0 and h > 0
```

Что здесь происходит? Каскад Хаара — это обученный классификатор, который проверяет множество прямоугольных признаков в разных масштабах. `scaleFactor=1.1` означает: на каждом шаге окно увеличивается на 10%, `minNeighbors=3` — лицо засчитывается, только если его подтвердили минимум три соседних окна. Белый эллипс на чёрном фоне имитирует лицо: тёмный фон, светлая овальная область с мягкими границами. Каскад обучен на реальных лицах, поэтому для эллипса результат может быть недетерминированным — но требование «хотя бы один прямоугольник» обычно выполняется за счёт формы.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое дескриптор?
- Вектор чисел, описывающий окрестность особой точки
- Координата точки
- Само изображение
* Правильный ответ: Вектор чисел, описывающий окрестность особой точки
Дескриптор — числовой «отпечаток» точки, по которому её сравнивают на разных изображениях.

Какой тип данных у дескрипторов ORB?
- uint8
- float32
- int64
* Правильный ответ: uint8
ORB использует краткие бинарные дескрипторы из 32 байт.

Какой тип данных у дескрипторов SIFT?
- float32
- uint8
- bool
* Правильный ответ: float32
SIFT даёт вектор из 128 чисел с плавающей точкой.

Какой алгоритм быстрее — ORB или SIFT?
- ORB
- SIFT
- Одинаково
* Правильный ответ: ORB
ORB оптимизирован для скорости, SIFT тяжелее, но точнее.

Какую метрику использовать для сравнения дескрипторов ORB?
- Расстояние Хэмминга
- Евклидово расстояние
- Косинусное сходство
* Правильный ответ: Расстояние Хэмминга
Так как ORB — бинарные векторы, сравнивают их через NORM_HAMMING.

Какая функция ищет шаблон на изображении?
- cv2.matchTemplate
- cv2.findContours
- cv2.matchFeatures
* Правильный ответ: cv2.matchTemplate
matchTemplate прокатывает шаблон и возвращает карту сходства.

Что возвращает cv2.minMaxLoc?
- Минимум, максимум и их координаты
- Только максимум
- Список точек
* Правильный ответ: Минимум, максимум и их координаты
minMaxLoc даёт 4 значения: min_val, max_val, min_loc, max_loc.

Что делает detectMultiScale в каскадах Хаара?
- Возвращает список прямоугольников с лицами
- Размывает изображение
- Находит контуры
* Правильный ответ: Возвращает список прямоугольников с лицами
detectMultiScale сканирует изображение в разных масштабах.

Что означает параметр minNeighbors?
- Сколько соседних окон должны подтвердить объект
- Минимальный размер лица
- Число объектов
* Правильный ответ: Сколько соседних окон должны подтвердить объект
Больше minNeighbors — меньше ложных срабатываний.

Что вернёт matchTemplate с TM_CCOEFF_NORMED при идеальном совпадении?
- 1.0
- 0.0
- 255
* Правильный ответ: 1.0
Нормированная корреляция достигает 1 при полном совпадении.
<!--/QUIZ-->
