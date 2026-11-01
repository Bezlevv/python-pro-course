---
title: Самостоятельная работа: нейросеть-классификатор
summary: Подготовка данных, загрузчики, полносвязная сеть на PyTorch, цикл обучения, оценка точности и анализ ошибок на датасете MNIST.
order: 7
duration: 240 мин
difficulty: advanced
tags: pytorch, нейросети, mnist, классификация, обучение
---

# Самостоятельная работа: нейросеть-классификатор

Привет! Это самостоятельная работа уровня advanced. За 240 минут ты создашь полноценную нейросеть с нуля на PyTorch: от загрузки данных до обучения, оценки качества и анализа ошибок. Это не «игрушечный» пример, а реальный пайплайн, на котором решают задачи компьютерного зрения в индустрии.

## Постановка задачи

Банк «Цифра» внедряет распознавание рукописных цифр для автоматической обработки заявлений. Исторически клиенты заполняют анкеты от руки, и необходимо извлекать цифры (например, номер телефона или сумму) из изображений. Тебе нужно разработать прототип классификатора рукописных цифр на датасете MNIST: 70 000 чёрно-белых изображений 28×28 (60 000 обучающих, 10 000 тестовых), каждое — одна цифра от 0 до 9.

Требования к работе:

1. **Данные**: загрузка MNIST через `torchvision.datasets.MNIST`, нормализация пикселей, разделение обучающей выборки на train/validation, наглядный просмотр сэмплов.
2. **DataLoader**: пакетная подача данных с перемешиванием, корректный размер батча.
3. **Модель**: полносвязная сеть (MLP) на `nn.Module` — три слоя, функция активации ReLU, выход на 10 классов.
4. **Обучение**: функция потерь CrossEntropyLoss, оптимизатор Adam, несколько эпох, логирование потерь и точности, сохранение контрольной точки (checkpoint).
5. **Оценка**: точность на тестовой выборке, матрица ошибок (confusion matrix), предсказания для новых изображений, анализ ошибок и один эксперимент по улучшению модели (добавление слоя или dropout).

Критерии успеха:

- точность на тестовой выборке не ниже 97% для базовой модели;
- в отчёте должна быть матрица ошибок и примеры правильно/неправильно распознанных цифр;
- весь код — в одном или нескольких `.py`-файлах, запускаемых командой `python train.py`.

## Что ты повторишь

PyTorch: `torchvision.datasets`, `transforms.ToTensor` и `transforms.Normalize`, `DataLoader`, `nn.Module`, `nn.Linear`, `nn.ReLU`, `nn.Dropout`, `F.cross_entropy`, `optim.Adam`, `model.train()` / `model.eval()` / `torch.no_grad()`, `model.state_dict()`, `torch.save`. Метрики: accuracy, confusion matrix через `sklearn.metrics.confusion_matrix`.

## План работы

Этапы идут по порядку. Каждый следующий использует результат предыдущего. Результат каждого этапа проверяем запуском кода.

<!--TASK-->
### Задача 1
Создай `train.py` и загрузи датасет MNIST через `torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())` (для теста — `train=False`). Выведи: тип объекта датасета, `len(train_data)`, размер одного изображения (`train_data[0][0].shape`), количество классов (`len(train_data.classes)`), минимальное и максимальное значение пикселя. Раздели обучающую выборку на train/validation в пропорции 90/10 через `random_split` (не забудь `torch.manual_seed(42)`). Нарисуй сетку из 10 изображений (по одному на класс) с подписями, используя `matplotlib` и `plt.imshow(img.squeeze(), cmap="gray")`. Ожидаемый результат: консольный вывод с фактами о данных и картинка-сетка, на которой видны все 10 цифр.

### Задача 2
Создай `DataLoader` для train, validation и test: `batch_size=64`, `shuffle=True` для train, `shuffle=False` для validation/test. В цикле пройдись по одному батчу и выведи: форму тензора `images.shape`, форму тензора меток `labels.shape`, тип данных, диапазон значений пикселей (после `ToTensor` они должны быть в [0, 1]). Затем добавь нормализацию через `transforms.Normalize((0.1307,), (0.3081,))` (среднее и стандартное отклонение MNIST) — пересоздай датасеты и DataLoader с ней, и снова выведи диапазон значений. Ожидаемый результат: видно, что без нормализации пиксели от 0 до 1, а после — примерно от −4 до +4 (стандартное отклонение 1).

### Задача 3
Определи класс `Net(nn.Module)` — полносвязную сеть: `nn.Flatten()` (или `x.view(x.size(0), -1)`), `nn.Linear(28*28, 128)`, `nn.ReLU()`, `nn.Linear(128, 64)`, `nn.ReLU()`, `nn.Linear(64, 10)`. Напиши `forward(self, x)`, который принимает батч изображений (B, 1, 28, 28) и возвращает логиты формы (B, 10). Создай модель, выведи количество параметров (`sum(p.numel() for p in model.parameters())`) и прогони один пробный батч через `model(images)` — выведи форму выхода. Ожидаемый результат: модель создаётся, количество параметров выводится (должно быть около 120 тысяч), форма выхода — (64, 10).

### Задача 4
Напиши функции `train_one_epoch(model, loader, optimizer)` и `evaluate(model, loader)`. Первая: цикл по батчам, обнуление градиентов (`optimizer.zero_grad()`), прямой проход, подсчёт потерь через `F.cross_entropy(logits, labels)`, обратный проход (`loss.backward()`), шаг оптимизатора (`optimizer.step()`), накопление суммы потерь и числа верных предсказаний. Вторая: `model.eval()` + `torch.no_grad()`, возврат кортежа `(loss, accuracy)`. Обучи модель 5 эпох с `optim.Adam(model.parameters(), lr=1e-3)`; после каждой эпохи печатай: номер эпохи, train loss, val loss, val accuracy. В конце сохрани `model.state_dict()` в `mnist_mlp.pt`. Ожидаемый результат: val accuracy растёт от эпохи к эпохе и к 5-й достигает хотя бы 96%, файл контрольной точки появился.

### Задача 5
Оцени модель на тестовой выборке: выведи test loss и test accuracy. Посчитай матрицу ошибок через `from sklearn.metrics import confusion_matrix` и визуализируй её тепловой картой (`plt.imshow` + `plt.colorbar` + подписи классов). Визуализируй 5 примеров, где модель ошиблась (изображение, настоящая метка, предсказание). Проведи эксперимент по улучшению: добавь `nn.Dropout(0.3)` после первого ReLU (или третий скрытый слой), переобучи 5 эпох и сравни accuracy. Ожидаемый результат: test accuracy ≥ 97% для лучшей модели, тепловая карта матрицы ошибок сохранена, в отчёте — сравнение базовой и улучшенной модели.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`ToTensor()` сам переводит изображения PIL в тензоры, а `len(train_data)` и `train_data[0]` дадут кортеж (тензор, метка). Для `random_split` нужен список длин: `[int(len(train_data) * 0.9), len(train_data) - int(len(train_data) * 0.9)]`. Сетку рисуй так: `fig, axes = plt.subplots(2, 5, figsize=(12, 5))`, затем для каждой оси `axes[i // 5][i % 5].imshow(images[i].squeeze(), cmap="gray")` и задай `set_title`.

### Подсказка 2
Форма батча — `(64, 1, 28, 28)`, это четыре индекса: батч, канал, высота, ширина. `x.view(x.size(0), -1)` расплющивает (64, 1, 28, 28) в (64, 784). Для нормализации добавь `transforms.Normalize((0.1307,), (0.3081,))` — параметры это среднее и стандартное отклонение по всему MNIST; они превращают пиксели в значения со средним 0 и разбросом 1.

### Подсказка 3
В `__init__` объявляй слои как атрибуты: `self.fc1 = nn.Linear(784, 128)` и так далее. В `forward` — `x = self.fc1(x)`; `x = F.relu(x)` — не забудь импортировать `torch.nn.functional as F`. Создание модели: `model = Net()`. Пробный батч: `images, labels = next(iter(train_loader))`; дальше `out = model(images)`.

### Подсказка 4
`F.cross_entropy(logits, labels)` объединяет softmax и кросс-энтропию. Для точности: `correct = (logits.argmax(1) == labels).sum().item()`, точность = `correct / len(loader.dataset)`. В `evaluate` обязательно `model.eval()` и `with torch.no_grad():`. Оптимизатор и потери — в `train.py`, вне функций. Сохранение: `torch.save(model.state_dict(), "mnist_mlp.pt")`.

### Подсказка 5
Матрица ошибок: `cm = confusion_matrix(all_labels, all_preds)` — собери предсказания по всем батчам теста в списки. Тепловая карта: `plt.imshow(cm, cmap="Blues")` + `plt.colorbar()` + `plt.xticks(range(10))`. Для ошибок: пройдись по тестовым предсказаниям, собери индексы, где `pred != true`, возьми первые 5 и нарисуй через `plt.subplots(1, 5)`. Эксперимент: добавь `self.dropout = nn.Dropout(0.3)` и `x = self.dropout(x)` после первого ReLU; переобучи и сравни.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Начало `train.py`:

```python
import torch
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

torch.manual_seed(42)

transform = transforms.ToTensor()
train_data = datasets.MNIST(root="./data", train=True, download=True,
                            transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True,
                           transform=transform)

print("Размер train:", len(train_data))
print("Размер test:", len(test_data))
img, label = train_data[0]
print("Форма изображения:", img.shape)
print("Количество классов:", len(train_data.classes))
print("Мин/макс пикселя:", img.min().item(), img.max().item())

val_size = int(len(train_data) * 0.9)
train_size = len(train_data) - val_size
train_data, val_data = torch.utils.data.random_split(
    train_data, [train_size, val_size])

fig, axes = plt.subplots(2, 5, figsize=(12, 5))
examples = {}
for x, y in train_data:
    if y not in examples:
        examples[y] = x
    if len(examples) == 10:
        break
for i, (y, x) in enumerate(sorted(examples.items())):
    axes[i // 5][i % 5].imshow(x.squeeze(), cmap="gray")
    axes[i // 5][i % 5].set_title(f"Цифра {y}")
    axes[i // 5][i % 5].axis("off")
plt.tight_layout()
plt.savefig("mnist_samples.png")
```

MNIST скачивается автоматически при первом запуске в папку `./data`. `ToTensor()` переводит PIL-изображения в тензоры `torch.FloatTensor` формы (1, 28, 28) — канал один, высота и ширина 28. `random_split` принимает список длин подвыборок и возвращает вью-объекты, которые ведут себя как датасеты. `manual_seed(42)` фиксирует случайность и для разбиения, и для перемешивания — обучение воспроизводимо. Сетка собирается за один проход: мы храним по одному изображению каждого класса в словаре `examples`, пока не наберём все 10, затем рисуем. `squeeze()` убирает размерность канала: (1, 28, 28) → (28, 28) — иначе `imshow` покажет одноканальное изображение неправильно.

### Разбор 2
Добавляем DataLoader и нормализацию:

```python
from torch.utils.data import DataLoader

batch_size = 64
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

images, labels = next(iter(train_loader))
print("Форма батча:", images.shape)
print("Форма меток:", labels.shape)
print("Тип данных:", images.dtype)
print("Мин/макс:", images.min().item(), images.max().item())

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])

train_data = datasets.MNIST(root="./data", train=True, download=True,
                            transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True,
                           transform=transform)
val_size = int(len(train_data) * 0.1)
train_size = len(train_data) - val_size
train_data, val_data = torch.utils.data.random_split(
    train_data, [train_size, val_size])

train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

images, labels = next(iter(train_loader))
print("После нормализации мин/макс:", images.min().item(), images.max().item())
```

`DataLoader` оборачивает датасет и раздаёт данные батчами. `shuffle=True` для train перемешивает каждую эпоху — это снижает корреляцию между соседними примерами и помогает сходиться. Нормализация применяется внутри `transform` на лету, до подачи в сеть. Параметры 0.1307 и 0.3081 — это среднее и стандартное отклонение пикселей всего MNIST; после `(x - 0.1307) / 0.3081` данные близки к нулю и единичному масштабу. Без нормализации большие значения (район 1.0) замедляют сходимость и могут «насытить» сигмоидальные функции; с ней градиенты становятся равномерными. Распределение после нормализации: примерно от −4 до +4.

### Разбор 3
Определяем модель:

```python
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


model = Net()
print("Параметров:", sum(p.numel() for p in model.parameters()))

images, labels = next(iter(train_loader))
out = model(images)
print("Форма выхода:", out.shape)
```

`nn.Module` автоматически регистрирует слои, объявленные как атрибуты, — их параметры собираются через `model.parameters()`. `view(x.size(0), -1)` расплющивает (64, 1, 28, 28) в (64, 784): `x.size(0)` оставляет размер батча, `-1` вычисляет остальное автоматически. У нас нет скрытого слоя с входом 784 и выходом 128, затем 128→64, затем 64→10. ReLU — стандартная нелинейность, простая и быстрая. Выход — логиты (без softmax): его добавляет сама кросс-энтропия. Количество параметров: 784·128 + 128 + 128·64 + 64 + 64·10 + 10 = 100 352 + 8 256 + 650 = 109 258 — «лёгкая» сеть, обучается за минуты на CPU.

### Разбор 4
Обучение:

```python
import torch.optim as optim


def train_one_epoch(model, loader, optimizer):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in loader:
        optimizer.zero_grad()
        logits = model(images)
        loss = F.cross_entropy(logits, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * images.size(0)
        correct += (logits.argmax(1) == labels).sum().item()
        total += images.size(0)
    return total_loss / total, correct / total


def evaluate(model, loader):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for images, labels in loader:
            logits = model(images)
            loss = F.cross_entropy(logits, labels)
            total_loss += loss.item() * images.size(0)
            correct += (logits.argmax(1) == labels).sum().item()
            total += images.size(0)
    return total_loss / total, correct / total


optimizer = optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(1, 6):
    train_loss, train_acc = train_one_epoch(model, train_loader, optimizer)
    val_loss, val_acc = evaluate(model, val_loader)
    print(f"Эпоха {epoch}: train_loss={train_loss:.4f} "
          f"train_acc={train_acc:.4f} val_loss={val_loss:.4f} "
          f"val_acc={val_acc:.4f}")

torch.save(model.state_dict(), "mnist_mlp.pt")
```

Цикл обучения — четыре шага: `zero_grad()` (обнулить старые градиенты), `loss.backward()` (посчитать новые), `optimizer.step()` (обновить веса). `F.cross_entropy` объединяет softmax и потерю. `argmax(1)` берёт индекс максимального логита — предсказанный класс. В `evaluate` обязательны `model.eval()` (выключает dropout, если он есть) и `torch.no_grad()` (не строит граф — экономит память и ускоряет). Потери усредняются по числу примеров, а не батчей: `loss.item() * images.size(0)`. Adam с lr=1e-3 — надёжный выбор по умолчанию. Пять эпох обычно дают валидационную точность 97%+.

### Разбор 5
Оценка и анализ:

```python
from sklearn.metrics import confusion_matrix
import numpy as np

test_loss, test_acc = evaluate(model, test_loader)
print(f"Test: loss={test_loss:.4f} accuracy={test_acc:.4f}")

all_labels, all_preds = [], []
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        logits = model(images)
        all_labels.extend(labels.tolist())
        all_preds.extend(logits.argmax(1).tolist())

cm = confusion_matrix(all_labels, all_preds)
plt.figure(figsize=(8, 6))
plt.imshow(cm, cmap="Blues")
plt.colorbar()
plt.xlabel("Предсказано")
plt.ylabel("Настоящая цифра")
plt.xticks(range(10))
plt.yticks(range(10))
for i in range(10):
    for j in range(10):
        plt.text(j, i, cm[i, j], ha="center", va="center",
                 color="white" if cm[i, j] > cm.max() / 2 else "black")
plt.tight_layout()
plt.savefig("confusion_matrix.png")

mistakes = [(img, true, pred) for img, true, pred in
            zip(test_data, all_labels, all_preds) if true != pred]
fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, (img, true, pred) in zip(axes, mistakes[:5]):
    ax.imshow(img.squeeze(), cmap="gray")
    ax.set_title(f"Настоящая: {true}\nПредсказано: {pred}")
    ax.axis("off")
plt.tight_layout()
plt.savefig("mistakes.png")
```

Матрица ошибок показывает, какие пары цифр путает модель; обычно это «похожие» пары (4/9, 7/2) — это нормальное поведение для рукописных цифр. Тепловая карта с числами в ячейках делает матрицу читаемой. Сбор ошибок: проходим по тестовым примерам и берём те, где предсказание не совпало с настоящей меткой; рисуем первые пять. Для эксперимента по улучшению добавь в `Net` слой `nn.Dropout(0.3)` и примени его после первого ReLU в `forward`:

```python
class NetImproved(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        return self.fc3(x)
```

Dropout случайно обнуляет 30% нейронов во время обучения — сеть учится не полагаться на отдельные нейроны, что снижает переобучение. Обрати внимание: на валидации и тесте dropout отключён автоматически благодаря `model.eval()`. Переобучи и сравни точности: улучшенная модель обычно даёт +0.1–0.5% на тесте и более устойчива. Итоговый отчёт: точность базовой и улучшенной моделей, матрица ошибок, примеры ошибок, контрольная точка лучшей модели.
<!--/SOLUTION-->

## Критерии оценки

| Критерий | Что проверяется | Баллы |
|---|---|---|
| Загрузка и разведка данных | Корректные вызовы, факты о датасете, сетка примеров | 15 |
| DataLoader и нормализация | `batch_size`, перемешивание, диапазоны значений до/после | 15 |
| Модель | Класс `Net`, форма выхода, разумное число параметров | 20 |
| Обучение | Функции `train_one_epoch`/`evaluate`, рост точности, checkpoint | 20 |
| Оценка | Test accuracy ≥ 97%, матрица ошибок, примеры ошибок | 20 |
| Эксперимент | Улучшенная модель, сравнение с базовой | 10 |

Итого 100 баллов. Оценка: 90+ — «отлично», 75–89 — «хорошо», 60–74 — «удовлетворительно», меньше 60 — работа требует доработки.

## Что сдать

1. Файл `train.py` (или проект с несколькими `.py`-файлами) — полный код, который воспроизводит обучение с нуля.
2. Файл контрольной точки `mnist_mlp.pt` (лучшая модель).
3. Изображения: `mnist_samples.png`, `confusion_matrix.png`, `mistakes.png`.
4. Отчёт (README или markdown): сколько эпох, итоговая точность train/val/test, сравнение базовой и улучшенной моделей, описание того, что показала матрица ошибок.
5. Команды запуска в README: `pip install torch torchvision scikit-learn matplotlib` и `python train.py`.

<!--QUIZ-->
Какой тензор вернёт `train_data[0][0]` после `transforms.ToTensor()`?
- PIL-изображение
- Тензор torch формы (1, 28, 28) со значениями от 0 до 1
- Тензор формы (28, 28) со значениями от 0 до 255
- Массив NumPy
* Правильный ответ: Тензор torch формы (1, 28, 28) со значениями от 0 до 1
`ToTensor()` преобразует изображение в float-тензор и нормирует пиксели на [0, 1]; канал один, высота и ширина 28.

Зачем нужна нормализация `Normalize((0.1307,), (0.3081,))`?
- Чтобы картинки стали красивее
- Чтобы привести пиксели к среднему 0 и стандартному отклонению 1 — это ускоряет сходимость
- Чтобы уменьшить размер изображений
- Чтобы превратить картинки в чёрно-белые
* Правильный ответ: Чтобы привести пиксели к среднему 0 и стандартному отклонению 1 — это ускоряет сходимость
Параметры — среднее и стандартное отклонение пикселей MNIST; нормализация стабилизирует масштаб входных признаков.

Что делает `x.view(x.size(0), -1)`?
- Добавляет размерность канала
- Расплющивает батч изображений в матрицу (B, 784)
- Перемешивает батч
- Меняет тип данных
* Правильный ответ: Расплющивает батч изображений в матрицу (B, 784)
`view` меняет форму: (64, 1, 28, 28) → (64, 784), где 784 = 28·28; `-1` выводит размерность автоматически.

Сколько параметров примерно у модели с слоями 784→128→64→10?
- Около 10 000
- Около 109 000
- Около 1 000 000
- Ровно 784
* Правильный ответ: Около 109 000
Сумма: 784·128 + 128 + 128·64 + 64 + 64·10 + 10 = 109 258 параметров.

Что объединяет в себе `F.cross_entropy(logits, labels)`?
- Только функцию потерь
- Softmax и кросс-энтропию
- Сигмоиду и MSE
- Функцию активации ReLU
* Правильный ответ: Softmax и кросс-энтропию
`cross_entropy` применяет softmax к логитам и считает кросс-энтропию за одну операцию — численно устойчивее, чем вручную.

Зачем нужен `optimizer.zero_grad()` перед `loss.backward()`?
- Чтобы ускорить обучение
- Чтобы обнулить накопленные градиенты за прошлые батчи — иначе они суммируются
- Чтобы очистить память GPU
- Чтобы сбросить веса модели
* Правильный ответ: Чтобы обнулить накопленные градиенты за прошлые батчи — иначе они суммируются
PyTorch накапливает градиенты; без обнуления каждый батч вносил бы «хвосты» предыдущих шагов.

Что делает `model.eval()`?
- Начинает обучение
- Переключает модель в режим инференса: отключает dropout и нормализацию батча
- Сохраняет модель на диск
- Очищает градиенты
* Правильный ответ: Переключает модель в режим инференса: отключает dropout и нормализацию батча
В режиме оценки dropout выключается, и модель работает детерминированно.

Зачем нужен `torch.no_grad()` в функции оценки?
- Чтобы запретить обновление весов
- Чтобы не строить граф вычислений: экономит память и ускоряет оценку
- Чтобы выключить dropout
- Чтобы сделать предсказания точнее
* Правильный ответ: Чтобы не строить граф вычислений: экономит память и ускоряет оценку
При оценке градиенты не нужны; без построения графа код работает заметно быстрее.

Какую роль играет `nn.Dropout(0.3)` в улучшенной модели?
- Увеличивает число слоёв
- Случайно обнуляет 30% нейронов при обучении — снижает переобучение
- Ускоряет прямое распространение
- Заменяет ReLU
* Правильный ответ: Случайно обнуляет 30% нейронов при обучении — снижает переобучение
Dropout делает сеть устойчивее: она не может полагаться на отдельные нейроны, поэтому обобщает лучше.
<!--/QUIZ-->
