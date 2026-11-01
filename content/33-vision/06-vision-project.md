---
title: Финальный проект: распознавание
summary: Сквозной пайплайн: чтение, препроцессинг, детекция, постобработка, отчёт; юнит- и интеграционные тесты.
order: 6
duration: 60 мин
difficulty: advanced
tags: проект, пайплайн, распознавание, тесты
---

В этом модуле мы изучили все кирпичики компьютерного зрения: работу с изображениями, фильтры и контуры, дескрипторы, детекцию YOLO и обработку видео. Теперь соберём из них настоящее приложение — модуль распознавания, который находит объекты на изображении и формирует отчёт.

## Архитектура пайплайна

Любая реальная система компьютерного зрения строится по одному и тому же принципу — как конвейер:

1. **Чтение** — загрузить изображение (`cv2.imread`).
2. **Препроцессинг** — подготовить кадр (перевести в нужное пространство, изменить размер).
3. **Детекция** — найти объекты (YOLO, каскады, контуры — смотря по задаче).
4. **Постобработка** — отфильтровать по уверенности, нарисовать рамки, посчитать.
5. **Вывод** — вернуть отчёт и сохранить результат.

Каждый этап — отдельная функция. Это позволяет тестировать шаги по отдельности и заменять детектор, не трогая остальной код.

## Проектируем интерфейс

Соберём класс `Pipeline` с методами для каждого этапа и методом `run`, который выполняет весь конвейер:

```python
from dataclasses import dataclass, field

@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple  # (x1, y1, x2, y2)

@dataclass
class Pipeline:
    model_path: str
    conf_threshold: float = 0.5
    _model: object = field(default=None, repr=False)

    def _load_model(self):
        from ultralytics import YOLO
        if self._model is None:
            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image):
        model = self._load_model()
        results = model.predict(source=image, conf=self.conf_threshold)
        detections = []
        result = results[0]
        for box, conf, cls in zip(result.boxes.xyxy,
                                   result.boxes.conf,
                                   result.boxes.cls):
            detections.append(Detection(
                label=result.names[int(cls)],
                confidence=float(conf),
                box=tuple(map(int, box.tolist())),
            ))
        return detections
```

Преимущества: `Detection` — простая структура данных (датакласс), результаты детекции легко фильтровать и тестировать, а модель загружается лениво — один раз.

## Постобработка и отчёт

Добавим фильтрацию и текстовый отчёт:

```python
def filter_by_label(self, detections, label):
    return [d for d in detections if d.label == label]

def report(self, detections):
    lines = []
    for d in detections:
        lines.append(f"{d.label}: {d.confidence:.2f} {d.box}")
    return "\n".join(lines) if lines else "Объектов не найдено"
```

## Тестирование пайплайна

Мы не можем в каждом тесте запускать нейросеть, поэтому детектор заменяют на фиктивный. Это называется мокинг:

```python
class FakeModel:
    def predict(self, source, conf=0.5):
        return [FakeResults()]

class FakeResults:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([[10, 20, 30, 40]])
        self.conf = torch.tensor([0.9])
        self.cls = torch.tensor([0])
```

Подставив такой объект в пайплайн, мы проверим логику без скачивания весов и GPU. Это стандартный приём в индустрии: юнит-тесты на логике, интеграционные — на реальной модели.

## Производительность

Если известна типичная задача, изображение перед детекцией уменьшают — это ускоряет нейросеть в разы. Например:

```python
def resize_for_inference(self, image, max_side=1280):
    h, w = image.shape[:2]
    scale = min(1.0, max_side / max(h, w))
    if scale < 1.0:
        image = cv2.resize(image, None, fx=scale, fy=scale)
    return image
```

## Итог

Проект объединяет всё, что мы выучили: работа с изображениями, детекция и хороший код с тестами. Разделение на этапы и датаклассы делает систему поддерживаемой, а мокинг позволяет проверять логику быстро. Перед тобой — последние задачи модуля.

<!--TASK-->
### Задача 1
Собери каркас пайплайна: создай класс `Pipeline` с методом `detect(image)`, который принимает изображение (numpy-массив) и возвращает список объектов `Detection`. Детекция — через `YOLO` из `ultralytics`, порог уверенности — из поля `conf_threshold`. Если изображение не является numpy-массивом — выброси `TypeError`. Проверь на реальной модели: распечатай отчёт для любого изображения.

### Задача 2
Добавь в `Pipeline` метод `report(detections)`, который возвращает строку отчёта: по одной строке на объект вида `label: confidence box`. Если детекций нет — верни строку `Объектов не найдено`. Расширь класс `Detection` полями `label`, `confidence`, `box`. Убедись, что отчёт для пустого списка выводит правильное сообщение.

### Задача 3
Добавь метод `filter_by_label(detections, label)`, который возвращает только детекции с указанным классом, и метод `count_by_label(detections, label)`, возвращающий их количество. Проверь на результатах задачи 1: число людей не должно быть больше общего числа объектов.

### Задача 4
Напиши **pytest-тесты** для логики пайплайна с фиктивной моделью. Реализуй фиктивные классы `FakeModel`, `FakeResults`, `FakeBoxes` (как в теории), которые возвращают два объекта: `person` с уверенностью 0.9 и `car` с уверенностью 0.4. Подставь фиктивную модель в `Pipeline` (через поле `_model`) и проверь: `detect` возвращает 2 объекта, `filter_by_label(_, "person")` возвращает 1 объект, `count_by_label(_, "car")` возвращает 1, `report` содержит обе строки. Запусти тесты.

### Задача 5
Напиши интеграционный тест `test_pipeline_end_to_end`: создай синтетическое изображение с двумя белыми прямоугольниками на чёрном фоне, подставь фиктивную модель, которая возвращает один объект `box` с `(10, 10, 50, 50)`. Проверь, что `Pipeline.run` (придумай этот метод: чтение → детекция → отчёт) возвращает непустой отчёт и что в нём есть слово `box`. Также проверь, что при `_model=None` модель загружается (замени `YOLO` на фиктивную через мокинг `monkeypatch`). Запусти тесты.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`Detection` — датакласс с полями `label`, `confidence`, `box`. В `detect` вызывай `self._load_model()` и затем `model.predict(source=image, conf=self.conf_threshold)`. Проверка типа: `if not isinstance(image, np.ndarray): raise TypeError(...)`.

### Подсказка 2
В `report` используй f-строки: `f"{d.label}: {d.confidence:.2f} {d.box}"`. Для пустого списка — `if not detections: return "Объектов не найдено"`.

### Подсказка 3
`filter_by_label` — списковое включение: `[d for d in detections if d.label == label]`. `count_by_label` — `len(self.filter_by_label(detections, label))`.

### Подсказка 4
Фиктивная модель: `self._model = FakeModel()` в `Pipeline` перед вызовом `detect`. В `FakeBoxes` отдай `torch.tensor([[10, 20, 30, 40], [50, 60, 70, 80]])`, `torch.tensor([0.9, 0.4])`, `torch.tensor([0, 1])`. Имена: `{0: "person", 1: "car"}`.

### Подсказка 5
Метод `run` — `def run(self, image_path): img = cv2.imread(image_path); detections = self.detect(img); return self.report(detections)`. Для мокинга `YOLO` используй `monkeypatch.setattr("ultralytics.YOLO", FakeModel)`. Интеграционный тест должен проверить путь от файла до отчёта.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
from dataclasses import dataclass, field
import numpy as np

@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple

@dataclass
class Pipeline:
    model_path: str
    conf_threshold: float = 0.5
    _model: object = field(default=None, repr=False)

    def _load_model(self):
        from ultralytics import YOLO
        if self._model is None:
            self._model = YOLO(self.model_path)
        return self._model

    def detect(self, image):
        if not isinstance(image, np.ndarray):
            raise TypeError("image должен быть numpy-массивом")
        model = self._load_model()
        results = model.predict(source=image, conf=self.conf_threshold)
        detections = []
        result = results[0]
        for box, conf, cls in zip(result.boxes.xyxy,
                                   result.boxes.conf,
                                   result.boxes.cls):
            detections.append(Detection(
                label=result.names[int(cls)],
                confidence=float(conf),
                box=tuple(map(int, box.tolist())),
            ))
        return detections
```

Что здесь происходит? Датакласс `Detection` — простая структура данных без методов. `Pipeline` хранит путь к модели и порог уверенности, а поле `_model` — кеш загруженной модели (`field(default=None, repr=False)` скрывает его из `repr`). Ленивая загрузка `_load_model` означает, что модель будет скачана только при первом вызове `detect`. Проверка типа через `isinstance` защищает от ошибок использования.

### Разбор 2
Решение:

```python
def report(self, detections):
    if not detections:
        return "Объектов не найдено"
    lines = [f"{d.label}: {d.confidence:.2f} {d.box}"
             for d in detections]
    return "\n".join(lines)

def filter_by_label(self, detections, label):
    return [d for d in detections if d.label == label]

def count_by_label(self, detections, label):
    return len(self.filter_by_label(detections, label))
```

Что здесь происходит? `report` превращает список детекций в человекочитаемую строку: каждая детекция — отдельная строка, уверенность округляется до двух знаков (`:02f`). Пустой список обрабатывается отдельно — это лучше, чем возвращать пустую строку. `filter_by_label` и `count_by_label` — пара фильтр/счётчик; второй использует первый, что исключает дублирование логики.

### Разбор 3
Решение — это дополнение к классу из разбора 2:

```python
pipeline = Pipeline("yolov8n.pt", conf_threshold=0.5)
image = cv2.imread("photo.jpg")
detections = pipeline.detect(image)
print(pipeline.report(detections))
print("Людей:", pipeline.count_by_label(detections, "person"))
```

Что здесь происходит? Функции из задачи 3 уже добавлены в класс в разборе 2. Здесь показано применение: детектируем объекты, печатаем полный отчёт и отдельно — количество людей. Проверка «людей не больше общего числа» выполняется автоматически: `count_by_label` — это подмножество всех детекций, поэтому их количество физически не может превысить общее. Если хочется формальной проверки, это можно закрепить тестом.

### Разбор 4
Решение:

```python
import torch

class FakeBoxes:
    def __init__(self):
        self.xyxy = torch.tensor([[10, 20, 30, 40],
                                  [50, 60, 70, 80]])
        self.conf = torch.tensor([0.9, 0.4])
        self.cls = torch.tensor([0, 1])

class FakeResults:
    def __init__(self):
        self.boxes = FakeBoxes()
        self.names = {0: "person", 1: "car"}

class FakeModel:
    def predict(self, source, conf=0.5):
        return [FakeResults()]

def make_pipeline_with_fake():
    p = Pipeline("fake.pt")
    p._model = FakeModel()
    return p

def test_detect_returns_two():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    assert len(detections) == 2

def test_filter_by_label_person():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    persons = p.filter_by_label(detections, "person")
    assert len(persons) == 1
    assert persons[0].label == "person"

def test_count_by_label_car():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    assert p.count_by_label(detections, "car") == 1

def test_report_contains_lines():
    p = make_pipeline_with_fake()
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = p.detect(image)
    report = p.report(detections)
    assert "person" in report and "car" in report
```

Что здесь происходит? Фиктивная модель возвращает ровно те данные, которые мы указываем: два объекта — `person` с уверенностью 0.9 и `car` с 0.4. Подставляя `_model = FakeModel()`, мы полностью минуем реальную нейросеть. Тесты проверяют логику пайплайна: число детекций, фильтрацию, счётчик и содержимое отчёта. Это быстрые тесты без интернета и весов — их можно гонять после каждого изменения кода.

### Разбор 5
Решение:

```python
class Pipeline:
    # ... (предыдущие методы) ...

    def run(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Не найден файл: {image_path}")
        detections = self.detect(image)
        return self.report(detections)

def test_pipeline_end_to_end(monkeypatch):
    monkeypatch.setattr("ultralytics.YOLO", FakeModel)
    # создаём изображение с двумя белыми прямоугольниками
    image = np.zeros((200, 200, 3), dtype=np.uint8)
    image[20:60, 20:60] = 255
    image[120:160, 120:160] = 255
    cv2.imwrite("tmp_pipeline.png", image)

    p = Pipeline("fake.pt")
    report = p.run("tmp_pipeline.png")
    assert "box" in report

def test_run_raises_on_missing_file():
    p = Pipeline("fake.pt")
    p._model = FakeModel()
    try:
        p.run("no_such_file.png")
    except FileNotFoundError:
        pass
    else:
        assert False, "Должно быть исключение FileNotFoundError"
```

Что здесь происходит? `monkeypatch.setattr("ultralytics.YOLO", FakeModel)` подменяет класс `YOLO` в модуле `ultralytics` на фиктивный — теперь `_load_model` вернёт `FakeModel()`. Метод `run` связывает этапы в цепочку: чтение файла, детекция, отчёт. Второй тест проверяет обработку ошибки: если файла нет, `cv2.imread` вернёт `None`, и `run` должен бросить `FileNotFoundError`. Так выглядит настоящий интеграционный тест: путь от файла до пользовательского отчёта, но без реальной нейросети.
<!--/SOLUTION-->

<!--QUIZ-->
Для чего датакласс Detection в пайплайне?
- Для структурирования данных детекции
- Для загрузки модели
- Для чтения файлов
* Правильный ответ: Для структурирования данных детекции
Датакласс описывает один объект: класс, уверенность и рамку.

Что такое ленивая загрузка модели?
- Модель загружается только при первом использовании
- Модель никогда не загружается
- Модель загружается при импорте
* Правильный ответ: Модель загружается только при первом использовании
Это экономит время при старте программы.

Зачем нужны фиктивные модели в тестах?
- Чтобы проверять логику без реальной нейросети
- Чтобы ускорить реальную модель
- Чтобы обучить модель
* Правильный ответ: Чтобы проверять логику без реальной нейросети
Мокинг заменяет тяжёлую зависимость фиктивным объектом.

Что делает monkeypatch.setattr?
- Подменяет атрибут или класс на время теста
- Сохраняет тест в файл
- Чистит временные файлы
* Правильный ответ: Подменяет атрибут или класс на время теста
Это стандартный механизм pytest для мокинга.

Какой метод в Pipeline запускает весь конвейер?
- run
- detect
- report
* Правильный ответ: run
run связывает чтение, детекцию и отчёт в цепочку.

Что вернёт cv2.imread, если файла нет?
- None
- Пустой массив
- Исключение
* Правильный ответ: None
Поэтому в run проверяют image is None и бросают FileNotFoundError.

Зачем уменьшать изображение перед детекцией?
- Для скорости: меньше пикселей — быстрее нейросеть
- Чтобы улучшить точность
- Это обязательно для YOLO
* Правильный ответ: Для скорости: меньше пикселей — быстрее нейросеть
Уменьшение разрешения ускоряет инференс в разы.

Что возвращает filter_by_label?
- Список детекций только с указанным классом
- Количество всех объектов
- Отчёт строкой
* Правильный ответ: Список детекций только с указанным классом
Фильтрация по классу — обычное списковое включение.

Почему отчёт для пустого списка обрабатывают отдельно?
- Чтобы вернуть понятное сообщение «Объектов не найдено»
- Чтобы не печатать ничего
- Потому что report вернёт None
* Правильный ответ: Чтобы вернуть понятное сообщение «Объектов не найдено»
Пустая строка хуже читается пользователем.

Какой приём позволяет тестировать run без файлов на диске?
- Создать файл в тесте и удалить после
- Использовать случайные пути
- Тестировать нельзя
* Правильный ответ: Создать файл в тесте и удалить после
Тесты создают временные изображения через cv2.imwrite.
<!--/QUIZ-->
