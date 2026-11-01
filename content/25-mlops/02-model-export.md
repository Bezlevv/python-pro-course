---
title: ONNX и экспорт моделей
summary: Формат ONNX, ручное построение графа, проверка модели, инференс через onnxruntime, экспорт из sklearn.
order: 2
duration: 40 мин
difficulty: advanced
tags: onnx, onnxruntime, экспорт, инференс, skl2onnx
---

Модель обучена в Python, но продакшен-сервисы не всегда могут (и не хотят) тянуть за собой десятки библиотек ML. Часто модель нужно запускать в другом языке, на другом сервере или на устройстве без Python. Для этого модели **экспортируют** в универсальный формат. Самый популярный — **ONNX** (Open Neural Network Exchange).

## Что такое ONNX

ONNX — это открытый формат представления моделей ML: модель описывается как **граф вычислений**. Граф состоит из:

- **узлов** (nodes) — операций: `MatMul`, `Add`, `Relu`, `Softmax`;
- **тензоров** — данных, которые текут по ребрам графа;
- **входов/выходов** — объявлений `X`, `Y` с их типами и размерностями.

Главное преимущество: формат **переносим**. Модель, обученная в scikit-learn, может выполняться в C++, Java, C# или в браузере — через рантаймы ONNX. Пакет `onnx` (библиотека для создания и проверки моделей) и `onnxruntime` (движок для их выполнения) ставятся просто:

```bash
pip install onnx onnxruntime numpy scikit-learn
```

## Строим первую ONNX-модель вручную

Не обязательно экспортировать готовую модель — граф можно собрать из операций. Сделаем простейшую линейную функцию `y = 2x + 1`:

```python
import onnx
from onnx import helper, TensorProto
import numpy as np
import onnxruntime as ort

# 1. Объявляем вход и выход
X = helper.make_tensor_value_info("X", TensorProto.FLOAT, [None, 1])
Y = helper.make_tensor_value_info("Y", TensorProto.FLOAT, [None, 1])

# 2. Константы — инициализаторы (веса)
W = helper.make_tensor("W", TensorProto.FLOAT, [1, 1], [2.0])
B = helper.make_tensor("B", TensorProto.FLOAT, [1], [1.0])

# 3. Узлы операций
mul = helper.make_node("MatMul", ["X", "W"], ["Z"])
add = helper.make_node("Add", ["Z", "B"], ["Y"])

# 4. Граф и модель
graph = helper.make_graph([mul, add], "linear", [X], [Y], initializer=[W, B])
model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)])

# 5. Проверка корректности
onnx.checker.check_model(model)
onnx.save(model, "linear.onnx")
```

Разбор. `make_tensor_value_info` объявляет тензор `X` типа `FLOAT` с размерностью `[None, 1]` (None — произвольное число строк, 1 — одна фича). `make_tensor` создаёт константы-веса. `make_node("MatMul", входы, выходы)` — узлы вычислений. `make_graph` собирает всё в граф, `make_model` — в модель. И наконец `checker.check_model` — обязательный шаг: он проверяет, что формат корректен.

## Запускаем модель через onnxruntime

```python
sess = ort.InferenceSession("linear.onnx")
x = np.array([[3.0]], dtype=np.float32)
y = sess.run(["Y"], {"X": x})[0]
print(y)  # [[7.]]
```

Что важно: вход должен быть `float32` и ровно той размерности, что объявлена (`[None, 1]` → матрица `(1, 1)`). `sess.run(["Y"], {"X": x})` принимает список нужных выходов и словарь входов; `[0]` — первый (и единственный) выход.

Проверяем честно:

```python
expected = 2 * 3.0 + 1.0
print("Совпадает:", float(y[0][0]) == expected)  # True
```

## Экспорт sklearn-модели

Вручную граф не собрать для сложной модели. На помощь приходит `skl2onnx`:

```bash
pip install skl2onnx
```

```python
from skl2onnx import convert_sklearn_model
from skl2onnx.common.data_types import FloatTensorType
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg = LinearRegression().fit(X_train, y_train)

initial_type = [("input", FloatTensorType([None, X.shape[1]]))]
onx = convert_sklearn_model(reg, initial_types=initial_type, target_opset=17)
onnx.save(onx, "diabetes_lr.onnx")
```

`convert_sklearn_model` — конвертер для моделей sklearn. Ему обязателен `initial_types`: список пар «имя входа — тип тензора». Дальше всё как обычно: сохраняем, проверяем, запускаем через `onnxruntime`. Разница между предсказаниями оригинальной модели и ONNX-версии практически равна нулю (числовые погрешности float32) — и это легко проверить сравнением.

## Типичные ошибки

1. **Не тот тип**: передал `int64` или `float64` — получишь ошибку вроде `Type Error: Type mismatch`. Решение — `.astype(np.float32)`.
2. **Не та размерность**: один вектор вместо матрицы. ONNX ждёт ровно то, что объявлено.
3. **Забыл checker**: модель с ошибкой графа упадёт уже в рантайме. Всегда запускай `onnx.checker.check_model` до сохранения.

## Итог

ONNX — это «эсперанто» для моделей: обучение в Python, выполнение где угодно. Понимание формата и рантайма — база для любого инференс-сервиса, и именно на ней мы построим следующий урок.

<!--TASK-->
### Задача 1
Собери вручную ONNX-модель функции `y = 3x + 5`. Объяви вход `X` и выход `Y` типа `float32` с размерностью `[None, 1]`, создай веса `W = [[3.0]]` и `B = [5.0]`, добавь узлы `MatMul` и `Add`. Запусти `onnx.checker.check_model`. Затем выведи список типов операций всех узлов графа (`model.graph.node[i].op_type`) и количество узлов. Ожидаемый результат: список `['MatMul', 'Add']`, количество 2.

### Задача 2
Сохрани модель из задачи 1 в файл `linear3.onnx` и выполни инференс через `onnxruntime.InferenceSession` для `x = 4.0`. Напечатай результат и проверь, что он равен `17.0`, а тип выходного массива — `numpy.float32`. Ожидаемый результат: `[[17.]]` и `dtype('float32')`.

### Задача 3
Обучи `LinearRegression` на датасете `load_diabetes` и экспортируй её через `convert_sklearn_model` с `FloatTensorType([None, 10])` (у диабета 10 признаков) и `target_opset=17`. Сохрани в `diabetes_lr.onnx`, проверь через `onnx.checker.check_model` и запусти инференс на тестовой выборке. Сравни предсказания оригинальной sklearn-модели и ONNX-версии: напечатай максимальную абсолютную разницу. Ожидаемый результат: разница меньше 1e-4.

### Задача 4
Возьми модель из задачи 3 и добавь вывод информации о размерностях: до вызова `onnx.shape_inference.infer_shapes` модель и оставшихся размерностях выходов (`None`), после — конкретные числа. Для этого: `inferred = onnx.shape_inference.infer_shapes(onx)` и сравни `onx.graph.output[0].type.tensor_type.shape` до и после. Напечатай обе строки. Ожидаемый результат: до — `None`, после — конкретные размерности (например, `[None, 1]`).

### Задача 5
Найди типичную ошибку. Запусти инференс модели `diabetes_lr.onnx` на данных типа `float64` (без приведения к float32), поймай исключение через `try/except` и напечатай его текст. Затем исправь данные (`astype(np.float32)`) и убедись, что всё работает. Ожидаемый результат: сначала выведена ошибка рантайма, затем успешный ответ.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Переиспользуй шаблон из теории: `make_tensor_value_info`, `make_tensor`, `make_node`, `make_graph`, `make_model`. Веса: `W = helper.make_tensor("W", TensorProto.FLOAT, [1, 1], [3.0])`, `B = helper.make_tensor("B", TensorProto.FLOAT, [1], [5.0])`. Перебор узлов: `for node in model.graph.node: print(node.op_type)`.

### Подсказка 2
После `onnx.save(model, "linear3.onnx")` вызови `ort.InferenceSession("linear3.onnx")`. Вход: `np.array([[4.0]], dtype=np.float32)`. Проверка типа: `print(y.dtype)` — должно быть `float32`.

### Подсказка 3
Формат `initial_types`: `[("input", FloatTensorType([None, 10]))]`. Для сравнения предсказаний: `np.max(np.abs(pred_onnx - pred_sklearn))`. Оба предсказания — numpy-массивы; размерности могут отличаться формой — используй `.ravel()`.

### Подсказка 4
До инференса размерность выхода может быть `[None, 1]` — то есть неконкретизированной. `infer_shapes` вычислит её по графу. Сравнивай через `str(...)` или атрибуты `dim_value`.

### Подсказка 5
onnxruntime при неправильном типе бросит `ValueError` или `Fail` с текстом вида `Type mismatch`. Перехвати через `except Exception as e: print(e)`. Затем вызови `x = x.astype(np.float32)` и повтори запуск.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import onnx
from onnx import helper, TensorProto

X = helper.make_tensor_value_info("X", TensorProto.FLOAT, [None, 1])
Y = helper.make_tensor_value_info("Y", TensorProto.FLOAT, [None, 1])

W = helper.make_tensor("W", TensorProto.FLOAT, [1, 1], [3.0])
B = helper.make_tensor("B", TensorProto.FLOAT, [1], [5.0])

mul = helper.make_node("MatMul", ["X", "W"], ["Z"])
add = helper.make_node("Add", ["Z", "B"], ["Y"])

graph = helper.make_graph([mul, add], "linear3", [X], [Y], initializer=[W, B])
model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)])

onnx.checker.check_model(model)

ops = [node.op_type for node in model.graph.node]
print(ops)
print("Количество узлов:", len(ops))
```

Разбор шагов. Мы повторяем структуру из теории, но с новыми весами: `W = [[3.0]]`, `B = [5.0]`. Внимание на порядок узлов: сначала `MatMul(X, W) → Z`, потом `Add(Z, B) → Y`. `checker.check_model` подтвердил, что граф валиден. Список `op_type` даёт `['MatMul', 'Add']`, длина — 2. Этот пример показывает, что ONNX-модель — это не «чёрный ящик», а обычный граф: разобрав его на узлы, мы видим всю математику. Такое понимание помогает отлаживать экспорт, когда модель ведёт себя неожиданно.

### Разбор 2
Решение:

```python
import onnx
import numpy as np
import onnxruntime as ort

onnx.save(model, "linear3.onnx")
sess = ort.InferenceSession("linear3.onnx")

x = np.array([[4.0]], dtype=np.float32)
y = sess.run(["Y"], {"X": x})[0]

print(y)
print(y.dtype)
assert float(y[0][0]) == 17.0
```

Разбор шагов. `onnx.save` записывает модель в файл — теперь она независима от процесса, что создал её. `InferenceSession` загружает её в рантайм. `sess.run(["Y"], {"X": x})` — ключевой вызов: первый аргумент — список имён выходов, которые нужны (можно запросить не все), второй — словарь входов. Ответ пришёл как `[[17.]]` — ровно `3*4+5`. Проверка `y.dtype` показывает `float32` — ONNX всегда работает в float32, поэтому для тяжёлых вычислений это и стандарт, и экономия памяти. `assert` подтверждает математику: ONNX выполнил граф правильно.

### Разбор 3
Решение:

```python
import numpy as np
import onnx
from skl2onnx import convert_sklearn_model
from skl2onnx.common.data_types import FloatTensorType
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

X, y = load_diabetes(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg = LinearRegression().fit(X_train, y_train)

initial_type = [("input", FloatTensorType([None, 10]))]
onx = convert_sklearn_model(reg, initial_types=initial_type, target_opset=17)
onnx.save(onx, "diabetes_lr.onnx")
onnx.checker.check_model(onx)

import onnxruntime as ort
sess = ort.InferenceSession("diabetes_lr.onnx")
x_test = X_test.astype(np.float32)
pred_onnx = sess.run(None, {"input": x_test})[0].ravel()
pred_sklearn = reg.predict(X_test)

diff = np.max(np.abs(pred_onnx - pred_sklearn))
print("Макс. разница:", diff)
```

Разбор шагов. `convert_sklearn_model` конвертирует обученную регрессию в ONNX-граф. `initial_types` обязателен: это объявление входа — имя `input`, тип `FloatTensorType`, форма `[None, 10]` (10 признаков диабета). Конвертер строит граф из узлов `MatMul` и `Add`, повторяющих формулу регрессии. Затем мы проверили модель и запустили инференс. `sess.run(None, ...)` — `None` означает «верни все выходы». `ravel()` выравнивает форму. Сравнение с оригинальной моделью показывает разницу меньше `1e-4` — это лишь округления float32. Вывод: ONNX-версия математически эквивалентна sklearn-оригиналу, но не зависит от scikit-learn.

### Разбор 4
Решение:

```python
import onnx

print("До shape inference:")
shape = onx.graph.output[0].type.tensor_type.shape
print([dim.dim_value for dim in shape.dim])

inferred = onnx.shape_inference.infer_shapes(onx)
print("После shape inference:")
shape2 = inferred.graph.output[0].type.tensor_type.shape
print([dim.dim_value for dim in shape2.dim])
```

Разбор шагов. `shape_inference.infer_shapes` — аналог компилятора: он проходит по графу и вычисляет размерности всех промежуточных тензоров. До вызова выход объявлен как `[None, 1]` — с неопределённой первой размерностью (`None`). После инференса размерности конкретизируются: если вход был `[None, 10]`, а веса — `[10, 1]`, выход станет `[None, 1]` — с точным числом колонок. `dim.dim_value` — численное значение размерности. Это мощный инструмент отладки: ошибки в размерностях всплывают сразу, до запуска рантайма. Также `infer_shapes` часто делается при подготовке модели к сериализации, чтобы на сервере не тратить время на вычисление форм.

### Разбор 5
Решение:

```python
import numpy as np
import onnxruntime as ort

sess = ort.InferenceSession("diabetes_lr.onnx")
x_bad = X_test  # float64 по умолчанию

try:
    sess.run(None, {"input": x_bad})
except Exception as e:
    print("Ошибка:", e)

x_good = x_bad.astype(np.float32)
result = sess.run(None, {"input": x_good})[0]
print("Успех, форма результата:", result.shape)
```

Разбор шагов. Передавая `float64`, мы провоцируем ошибку `Type mismatch` — сессия отказывается работать с типом, отличным от float32. Мы перехватили её через `try/except` и напечатали текст: так в реальном сервисе можно вернуть клиенту понятное сообщение вместо падения. Исправление — `.astype(np.float32)`. Этот урок — о самой частой боли при работе с onnxruntime: строгие типы. Запомни правило: входные данные всегда приводи к float32, а если ты принимаешь запросы из JSON — приводи к массиву с явным dtype. Тогда рантайм отработает без сюрпризов.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое ONNX?
- Открытый формат представления моделей ML в виде графа вычислений
- Фреймворк для обучения нейросетей
- База данных для метрик
* Правильный ответ: Открытый формат представления моделей ML в виде графа вычислений
ONNX описывает модель как граф узлов-операций над тензорами.

Чем onnx отличается от onnxruntime?
- onnx — библиотека для создания/проверки моделей, onnxruntime — движок для их выполнения
- Это две версии одной библиотеки
- onnxruntime — только для нейросетей
* Правильный ответ: onnx — библиотека для создания/проверки моделей, onnxruntime — движок для их выполнения
onnx собирает и проверяет граф, onnxruntime исполняет его.

Какой тип данных ожидает вход ONNX-модели по умолчанию?
- float32
- float64
- int32
* Правильный ответ: float32
Формат ONNX стандартно использует float32; другой тип вызывает ошибку.

Что делает onnx.checker.check_model()?
- Проверяет корректность структуры модели
- Обучает модель
- Конвертирует модель в sklearn
* Правильный ответ: Проверяет корректность структуры модели
Чекер валидирует граф, типы и согласованность узлов до сохранения.

Как запустить инференс в onnxruntime?
- Создать InferenceSession и вызвать sess.run(выходы, входы)
- Вызвать model.predict(x)
- Импортировать onnxruntime и вызвать predict()
* Правильный ответ: Создать InferenceSession и вызвать sess.run(выходы, входы)
InferenceSession загружает модель; run выполняет граф.

Зачем нужен параметр initial_types в convert_sklearn_model?
- Чтобы объявить имена и типы входов модели
- Чтобы выбрать цвет модели
- Чтобы указать путь сохранения
* Правильный ответ: Чтобы объявить имена и типы входов модели
Конвертер должен знать, что придёт на вход: имя и форму тензора.

Что делает onnx.shape_inference.infer_shapes()?
- Вычисляет точные размерности тензоров в графе
- Удаляет лишние узлы
- Меняет тип модели на float64
* Правильный ответ: Вычисляет точные размерности тензоров в графе
Shape inference конкретизирует размерности, выводя их из связей узлов.

Что произойдёт, если передать в onnxruntime float64?
- Возникнет ошибка типа Type mismatch
- Модель просто отработает
- Данные молча округлятся до float32
* Правильный ответ: Возникнет ошибка типа Type mismatch
Рантайм строг к типам; приводи данные к float32 заранее.
<!--/QUIZ-->
