---
title: Обработка видео
summary: Чтение видео через VideoCapture, обработка кадров, запись результата через VideoWriter, метрики потока.
order: 5
duration: 45 мин
difficulty: advanced
tags: opencv, видео, videocapture, videowriter
---

Изображение — это один кадр, а видео — это последовательность кадров, которую мы обрабатываем в цикле. OpenCV умеет читать видео и с файлов и с веб-камеры, а также записывать результат обработки в новый видеофайл.

## Читаем видео

`cv2.VideoCapture` открывает видеофайл или камеру (порядковый номер устройства, например `0`):

```python
import cv2

cap = cv2.VideoCapture("input.mp4")
if not cap.isOpened():
    print("Не удалось открыть видео")
    exit()
```

Свойства потока получают через `cap.get()` с константами:

```python
fps = cap.get(cv2.CAP_PROP_FPS)        # кадров в секунду
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # всего кадров
print(fps, width, height, frames_count)
```

## Читаем кадры

Кадры читаются в цикле методом `cap.read()`, который возвращает кортеж: флаг успеха `ret` и сам кадр (numpy-массив BGR):

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break  # видео закончилось (или ошибка)
    # ... обработка кадра ...
```

Флаг `ret` становится `False`, когда видео закончилось. Это условие выхода из цикла.

## Записываем видео

Для записи нужен `cv2.VideoWriter` с кодеком, частотой кадров и размером:

```python
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # кодек MPEG-4
writer = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))
```

Кодек выбирается строкой из четырёх символов: `"mp4v"` для MP4, `"XVID"` для AVI. Метод `write()` добавляет кадр в файл, а `release()` закрывает поток:

```python
writer.write(frame)   # внутри цикла
writer.release()      # после цикла
```

## Обработка кадров

Внутри цикла с каждым кадром можно делать всё, что мы уже умеем: переводить в серый, размывать, искать контуры, детектировать объекты. Например, серая версия видео:

```python
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # VideoWriter ждёт 3 канала
    writer.write(gray_bgr)
```

Обрати внимание: `VideoWriter` ожидает кадры той же ширины, высоты и числа каналов, что указаны при создании. Поэтому серый кадр перед записью переводят обратно в трёхканальный.

## Считаем кадры

Счётчик обработанных кадров — обычная переменная:

```python
count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
print(f"Обработано кадров: {count}")
```

## Потоковое чтение из камеры

Для веб-камеры открой `cv2.VideoCapture(0)`. Кадры читаются точно так же, но цикл не завершится сам — нужен явный выход (например, по нажатию клавиши `q`):

```python
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # показываем кадр в окне
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
```

## Итог

Обработка видео — это циклическое повторение обработки изображения: открыл поток → прочитал кадр → обработал → записал → прочитал следующий. Не забудь закрыть оба потока через `release()`. Теперь практика.

<!--TASK-->
### Задача 1
Напиши функцию `video_info(path)`, которая открывает видео через `cv2.VideoCapture` и выводит на экран: FPS, ширину, высоту и общее число кадров (свойства `CAP_PROP_FPS`, `CAP_PROP_FRAME_WIDTH`, `CAP_PROP_FRAME_HEIGHT`, `CAP_PROP_FRAME_COUNT`). Если видео не открылось — выведи `Не удалось открыть видео`. Проверь на любом своём видеофайле или сгенерируй тестовый через VideoWriter.

### Задача 2
Напиши функцию `save_first_frame(path, out_path)`, которая читает из видео ровно первый кадр и сохраняет его как изображение по `out_path`. Используй `cap.read()` и `cv2.imwrite`. Проверь, что файл создан и что это действительно изображение (его форма — трёхмерный массив).

### Задача 3
Напиши функцию `convert_to_gray_video(src, dst)`, которая читает видео `src`, превращает каждый кадр в серый (с последующим переводом обратно в BGR для записи) и сохраняет результат в `dst` с тем же FPS и размером кадра. Выведи, сколько кадров обработано. Запусти на коротком тестовом видео.

### Задача 4
Напиши функцию `process_frame(frame, mode)`, которая обрабатывает один кадр: при `mode="gray"` возвращает серый кадр, переведённый обратно в 3 канала; при `mode="blur"` — результат `cv2.GaussianBlur(frame, (5, 5), 0)`; при любом другом значении — исходный кадр. Напиши **pytest-тесты**: проверь, что форма кадра сохраняется во всех режимах, что серый результат имеет ровно 3 канала, и что для неизвестного режима возвращается тот же объект. Запусти тесты.

### Задача 5
Напиши функцию `count_frames(path)`, которая подсчитывает число кадров в видео, читая их в цикле (без `CAP_PROP_FRAME_COUNT`). Напиши **pytest-тесты**: создай тестовое видео с известным числом кадров (например, 10) через `cv2.VideoWriter`, затем проверь, что `count_frames` возвращает ровно столько же. Запусти тесты.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Свойства: `cap.get(cv2.CAP_PROP_FPS)` и т.д. Ширину и высоту оберни в `int()`. Проверка открытия — `cap.isOpened()`. Не забудь `cap.release()`.

### Подсказка 2
`ret, frame = cap.read()` — первый вызов вернёт первый кадр. Проверь `ret`, затем `cv2.imwrite(out_path, frame)`. Форма кадра — `frame.shape`.

### Подсказка 3
В цикле: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`, затем `gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)`. Видеорайтер: `cv2.VideoWriter(dst, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))`. Счётчик кадров увеличивай на 1 внутри цикла.

### Подсказка 4
Для серого: `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`, затем `cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)`. Для размытия — `cv2.GaussianBlur(frame, (5, 5), 0)`. В тестах создавай кадр через `np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)`.

### Подсказка 5
Для теста тебе нужно создать видеофайл: `writer = cv2.VideoWriter("test.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (320, 240))` и записать 10 кадров `np.zeros((240, 320, 3), dtype=np.uint8)` через `writer.write()`. Потом вызови `count_frames("test.mp4")`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import cv2

def video_info(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("Не удалось открыть видео")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(f"FPS: {fps}, размер: {width}x{height}, кадров: {total}")
    cap.release()

video_info("input.mp4")
```

Результат (пример):

```
FPS: 30.0, размер: 1920x1080, кадров: 300
```

Что здесь происходит? `CAP_PROP_FRAME_WIDTH` и `CAP_PROP_FRAME_HEIGHT` возвращают числа с плавающей точкой, поэтому их переводят в `int`. `CAP_PROP_FRAME_COUNT` — общее число кадров (у некоторых кодеков может быть недоступно). `release()` освобождает ресурсы потока — это важно, чтобы файл не остался заблокированным.

### Разбор 2
Решение:

```python
import cv2

def save_first_frame(path, out_path):
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    if not ret:
        print("Не удалось прочитать кадр")
        return
    cv2.imwrite(out_path, frame)
    print(f"Кадр сохранён: {frame.shape}")
    cap.release()

save_first_frame("input.mp4", "first_frame.png")
```

Результат:

```
Кадр сохранён: (1080, 1920, 3)
```

Что здесь происходит? Первый вызов `cap.read()` возвращает первый кадр видео. Проверка `ret` защищает от пустых видео. `cv2.imwrite` сохраняет кадр как обычное изображение. Так получают превью видео — один кадр, который удобно показать пользователю без перемотки всего файла.

### Разбор 3
Решение:

```python
import cv2

def convert_to_gray_video(src, dst):
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(dst, fourcc, fps, (width, height))
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        writer.write(gray_bgr)
        count += 1
    cap.release()
    writer.release()
    print(f"Обработано кадров: {count}")

convert_to_gray_video("input.mp4", "gray.mp4")
```

Что здесь происходит? Цикл читает кадры, пока `ret` не станет `False`. Каждый кадр переводится в серый, а затем обратно в BGR — иначе `VideoWriter`, созданный для трёхканальных кадров, не примет двумерный массив. Параметры писателя — те же, что у исходного видео: FPS и размер кадра. Счётчик позволяет убедиться, что не потеряно ни одного кадра.

### Разбор 4
Решение:

```python
import cv2

def process_frame(frame, mode):
    if mode == "gray":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if mode == "blur":
        return cv2.GaussianBlur(frame, (5, 5), 0)
    return frame
```

Тесты:

```python
import numpy as np

def test_process_gray_shape():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "gray")
    assert out.shape == (100, 100, 3)

def test_process_gray_channels():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "gray")
    assert out.shape[2] == 3

def test_process_blur_shape():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    out = process_frame(frame, "blur")
    assert out.shape == frame.shape

def test_process_unknown_mode():
    frame = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    assert process_frame(frame, "unknown") is frame
```

Что здесь происходит? Серый кадр перед возвратом переводится обратно в трёхканальный, поэтому `shape` сохраняется во всех режимах — это ключевое требование для `VideoWriter`. Тест `test_process_unknown_mode` проверяет, что неизвестный режим не приводит к ошибке, а возвращает исходный объект: `is` сравнивает идентичность объектов, а не значения.

### Разбор 5
Решение:

```python
import cv2

def count_frames(path):
    cap = cv2.VideoCapture(path)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
    cap.release()
    return count
```

Тесты:

```python
import numpy as np

def make_test_video(path, frames=10):
    writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"),
                              30.0, (320, 240))
    blank = np.zeros((240, 320, 3), dtype=np.uint8)
    for _ in range(frames):
        writer.write(blank)
    writer.release()

def test_count_frames():
    make_test_video("test.mp4", 10)
    assert count_frames("test.mp4") == 10
```

Что здесь происходит? Тест генерирует собственное видео: 10 одинаковых чёрных кадров. `count_frames` считает их, читая поток до конца. Такой подход проверяет реальную работу цикла, а не просто чтение метаданных. Обрати внимание: `VideoWriter` должен быть закрыт через `release()`, прежде чем другой поток сможет открыть этот файл — иначе файл может быть недописан.
<!--/SOLUTION-->

<!--QUIZ-->
Что возвращает cap.read()?
- Кортеж (ret, frame) — флаг успеха и кадр
- Только кадр
- Число кадров
* Правильный ответ: Кортеж (ret, frame) — флаг успеха и кадр
ret == False означает конец видео или ошибку чтения.

Как проверить, что видео открылось?
- cap.isOpened()
- cap.open()
- cap.valid()
* Правильный ответ: cap.isOpened()
isOpened возвращает True, если поток готов к чтению.

Как получить FPS видео?
- cap.get(cv2.CAP_PROP_FPS)
- cap.fps()
- cv2.fps(cap)
* Правильный ответ: cap.get(cv2.CAP_PROP_FPS)
Свойства потока читаются через cap.get с константой.

Что означает ret == False в цикле чтения?
- Видео закончилось или случилась ошибка
- Кадр обработан
- Камера выключена
* Правильный ответ: Видео закончилось или случилась ошибка
На этом условии строится выход из цикла.

Что делает cv2.VideoWriter_fourcc(*"mp4v")?
- Создаёт кодек MPEG-4 для записи
- Открывает видео на чтение
- Меняет FPS
* Правильный ответ: Создаёт кодек MPEG-4 для записи
fourcc — четырёхсимвольный идентификатор кодека.

Почему серый кадр переводят обратно в BGR перед записью?
- VideoWriter ожидает кадры той же формы и числа каналов
- Чтобы ускорить запись
- Это требование FPS
* Правильный ответ: VideoWriter ожидает кадры той же формы и числа каналов
Писатель настроен на конкретное разрешение и число каналов.

Что делает writer.write(frame)?
- Добавляет кадр в видеофайл
- Читает кадр
- Закрывает поток
* Правильный ответ: Добавляет кадр в видеофайл
write добавляет один кадр в выходной файл.

Что обязательно нужно сделать после цикла записи?
- writer.release() и cap.release()
- Ничего
- Перезапустить скрипт
* Правильный ответ: writer.release() и cap.release()
Закрытие потоков гарантирует, что файлы дописаны корректно.

Как открыть веб-камеру?
- cv2.VideoCapture(0)
- cv2.VideoCapture("webcam")
- cv2.openCamera(0)
* Правильный ответ: cv2.VideoCapture(0)
Номер 0 — первая камера устройства.

Сколько каналов у серого кадра?
- 1
- 3
- 4
* Правильный ответ: 1
Серое изображение двумерное, но перед записью его возвращают в 3 канала.
<!--/QUIZ-->
