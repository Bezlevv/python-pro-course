---
title: Обучение сети на MNIST
summary: Первая настоящая задача: распознавание рукописных цифр. Датасет MNIST, DataLoader, кросс-энтропия и оценка точности на тесте.
order: 6
duration: 45 мин
difficulty: advanced
---

Пришло время применить всё, что мы узнали, к настоящей задаче: распознавание рукописных цифр. MNIST — классический датасет: 60 000 обучающих и 10 000 тестовых чёрно-белых изображений 28×28, каждое с меткой от 0 до 9. Это «привет, мир» компьютерного зрения: на нём проверяют новые архитектуры, а точность выше человеческой (около 98%) достигли уже первые свёрточные сети в 1990-х.

## Torchvision

Помимо ядра, у PyTorch есть библиотека `torchvision` с готовыми датасетами. `datasets.MNIST(root, train=True, download=True)` скачает данные один раз. Чтобы подать их в сеть, каждое изображение превращают в тензор (`transforms.ToTensor`) и нормируют: пиксели из диапазона 0–255 переводятся в 0–1, затем вычитается среднее и делится на стандартное отклонение — так данные центрируются вокруг нуля и обучение идёт стабильнее.

## DataLoader

Загружать все данные сразу неудобно, поэтому данные нарезают на батчи. `DataLoader(dataset, batch_size=64, shuffle=True)` создаёт итератор, который выдаёт пары (изображения, метки): тензор формы (64, 1, 28, 28) и вектор из 64 меток. Опция `shuffle` перемешивает данные перед каждой эпохой — это улучшает обучение.

## Архитектура

Изображение 28×28 разворачиваем в вектор из 784 чисел (`nn.Flatten`). Дальше — два полносвязных слоя: 784 → 128 с ReLU и 128 → 10 без активации. Десять выходов — оценки для десяти классов. Чтобы получить вероятности, применяют softmax, но в PyTorch его объединяют с потерей, поэтому в сети он не нужен.

## Кросс-энтропия

Функция `F.cross_entropy(logits, labels)` внутри применяет softmax и считает логарифмическую потерю. Она поощряет модель ставить большую вероятность на правильный класс. Метка — целое число от 0 до 9, а не one-hot вектор: PyTorch это делает сам.

## Цикл обучения

Он почти такой же, как в прошлом уроке, но появились две детали. Во-первых, батч: шаг оптимизатора после каждой порции данных. Во-вторых, режимы: `model.train()` включает обучение (для batchnorm/dropout), `model.eval()` — режим оценки, в котором не считаются градиенты и отключаются случайные механизмы. Точность на тесте считаем так: `argmax` по выходу сети сравниваем с меткой.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_data = datasets.MNIST("./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST("./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=256)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    acc = evaluate(model, test_loader)
    print(f"epoch={epoch}  test_acc={acc:.4f}")
```

Запусти код — первые две эпохи дадут точность около 95–96%, третья — около 96–97%. Обрати внимание: обучение занимает меньше минуты даже на CPU.

## Сколько эпох нужно

Обычно точность на тесте растёт, а потом стабилизируется или начинает падать — это сигнал переобучения. Для нашего одностраничного примера трёх эпох хватит, чтобы получить примерно 96–97%.

## Итог урока

Мы прошли весь конвейер настоящего ML-проекта: данные → нормализация → батчи → архитектура → обучение → оценка на тесте. В следующем уроке мы заменим полносвязную сеть на свёрточную и увидим, насколько лучше она справляется с изображениями.

<!--TASK-->
### Задача 1
Добавь к сети с одним скрытым слоем ещё один: после слоя 784 → 128 поставь слой 128 → 64 с ReLU, затем выходной 64 → 10. Обучи сеть так же, как в теории (Adam, lr = 1e-3, 3 эпохи, батч 64) и выведи точность на тесте после каждой эпохи. Ожидаемый результат: три строки вида `epoch=0 test_acc=0.9621 ...`; точность на третьей эпохе не ниже 95% и выше, чем у базовой сети (96–97%).

### Задача 2
Увеличь скрытый слой базовой MLP с 128 до 512 нейронов и обучи сеть (Adam, lr = 1e-3, 3 эпохи, батч 64). Выведи точность на тесте после каждой эпохи. Ожидаемый результат: точность сравнима с базовой сетью — около 96–97.5%. Больше параметров не гарантирует заметного выигрыша: возможности ограничены самими данными и архитектурой.

### Задача 3
Добавь в базовую MLP слой `nn.Dropout(0.25)` после первого ReLU. Обучи сеть так же (Adam, lr = 1e-3, 3 эпохи) и выведи точность на тесте после каждой эпохи. Ожидаемый результат: точность около 96–97.5%, похожая на базовую — dropout чаще помогает на больших сетях и данных, а здесь его эффект невелик.

### Задача 4
Обучи базовую MLP с двумя разными скоростями обучения: lr = 1e-2 и lr = 1e-4 (Adam, 3 эпохи, батч 64). Выведи финальную точность (после третьей эпохи) для каждой. Ожидаемый результат: обе ниже, чем при lr = 1e-3: слишком большая скорость расшатывает обучение, слишком малая — не успевает сойтись за три эпохи.

### Задача 5
После обучения базовой MLP посчитай точность отдельно на обучающей выборке (весь `train_loader`) и на тестовой. Выведи обе. Ожидаемый результат: точность на обучении выше — около 98–99%, на тесте — около 96–97%. Это нормальный признак лёгкого переобучения: модель частично запоминает примеры.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Вставь `self.fc_mid = nn.Linear(128, 64)` между `fc1` и `fc2` и не забудь ReLU между скрытыми слоями. Вход второго скрытого слоя — 128, выход — 64. Код цикла обучения и `evaluate` менять не нужно.

### Подсказка 2
Меняется только одна строка: `self.fc1 = nn.Linear(28 * 28, 512)`. Остальной код — дословно из теории. Обрати внимание: у сети станет примерно 400 тысяч параметров, но точность вырастет лишь на доли процента.

### Подсказка 3
Добавь поле `self.dropout = nn.Dropout(0.25)` в `__init__` и примени его в `forward` после ReLU: `x = self.dropout(torch.relu(self.fc1(x)))`. В функции `evaluate` модель переключается в `eval()`-режим, где dropout автоматически отключается, поэтому правок не требуется.

### Подсказка 4
Создай две модели и обучи их в отдельных циклах с разными `lr`. Лучше оформить обучение как функцию, принимающую `lr` и возвращающую точность после третьей эпохи, чтобы не дублировать код.

### Подсказка 5
Функция `evaluate` уже умеет считать точность: вызови её дважды — `evaluate(model, train_loader)` и `evaluate(model, test_loader)`. Для обучающей выборки это будет медленнее (60 000 изображений), но всё равно быстро.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полное решение:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_data = datasets.MNIST("./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST("./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=256)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc_mid = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc_mid(x))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    acc = evaluate(model, test_loader)
    print(f"epoch={epoch}  test_acc={acc:.4f}")
```

Изменения — только в архитектуре: между двумя полносвязными слоями появился третий, 128 → 64. Теперь сеть сначала сжимает 784 пикселя до 128 признаков, потом до 64, и лишь затем выдаёт 10 оценок. Число параметров выросло примерно на `128·64 + 64 = 8256` — это небольшая добавка к базовым ~102 тысячам. Что изменилось на практике? Глубокая сеть учится чуть дольше на эпоху, но обычно достигает заметно более высокой точности: около 97–97.5% против 96–97% у базовой. Чем больше скрытых слоёв, тем более сложные комбинации признаков может построить модель — но до порога: на 28×28 чёрно-белых картинках очень глубокие полносвязные сети почти перестают давать выигрыш и просто учатся дольше. Обрати внимание на функцию `evaluate`: она переключает модель в режим оценки, отключает градиенты через `torch.no_grad()` и считает долю правильных `argmax`-ответов. Этот же шаблон мы будем использовать и в следующем уроке, когда сеть станет свёрточной.

### Разбор 2
Решение:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_loader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=64, shuffle=True,
)
test_loader = DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transform),
    batch_size=256,
)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 512)
        self.fc2 = nn.Linear(512, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    acc = evaluate(model, test_loader)
    print(f"epoch={epoch}  test_acc={acc:.4f}")
```

Мы увеличили первый скрытый слой в четыре раза: 128 → 512 нейронов, и число параметров выросло до ~400 тысяч. Однако точность почти не меняется: после трёх эпох она остаётся около 96–97.5%. Почему? Потому что у полносвязной сети на изображениях главный ограничитель — не мощность, а сама архитектура: она видит пиксели независимо и не использует их соседство. Добавляя нейроны, мы просто усложняем модель без новой информации, и в итоге она либо учится дольше, либо начинает понемногу переобучаться. Этот вывод — важная идея курса: качество модели растёт не столько от количества параметров, сколько от правильных предположений о структуре данных. В следующем уроке свёрточные слои дадут тот же уровень точности при в пять раз меньшем числе параметров.

### Разбор 3
Решение:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_loader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=64, shuffle=True,
)
test_loader = DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transform),
    batch_size=256,
)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.dropout = nn.Dropout(0.25)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.dropout(torch.relu(self.fc1(x)))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    acc = evaluate(model, test_loader)
    print(f"epoch={epoch}  test_acc={acc:.4f}")
```

Dropout — это регуляризация: во время обучения он случайно обнуляет 25% нейронов первого скрытого слоя, заставляя сеть не полагаться на отдельные признаки. Важно: в режиме `model.train()` dropout активен, а в `model.eval()` (внутри `evaluate`) он превращается в тождественную операцию — поэтому точность измеряется корректно без правок. На нашей модели эффект небольшой: точность остаётся около 96–97.5%, потому что базовое переобучение за три эпохи ещё невелико. На больших сетях с длинным обучением dropout обычно даёт ощутимый прирост и защищает от переобучения. Это стандартный инструмент, который стоит добавлять в архитектуры, когда обучающая ошибка заметно ниже тестовой.

### Разбор 4
Решение:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_loader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=64, shuffle=True,
)
test_loader = DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transform),
    batch_size=256,
)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

def train_and_eval(lr, epochs=3):
    model = MLP()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad()
            loss = F.cross_entropy(model(images), labels)
            loss.backward()
            optimizer.step()
    return evaluate(model, test_loader)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

print("lr=1e-2:", round(train_and_eval(1e-2), 4))
print("lr=1e-4:", round(train_and_eval(1e-4), 4))
```

Мы вынесли обучение в функцию, принимающую lr, и прогнали два эксперимента. При lr = 1e-2 шаги слишком велики: параметры «прыгают», и модель не успевает стабильно сойтись — точность падает. При lr = 1e-4 обучение идёт настолько медленно, что за три эпохи модель проходит лишь малую часть пути — точность тоже ниже. Золотая середина в этом примере — 1e-3, при которой за три эпохи сеть достигает ~97%. Такой перебор гиперпараметров — обычная практика: начинают с грубой сетки значений (1e-2, 1e-3, 1e-4) и выбирают ту, где качество на валидационной или тестовой выборке максимально.

### Разбор 5
Решение:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])
train_loader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=64, shuffle=True,
)
test_loader = DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transform),
    batch_size=256,
)

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

def evaluate(model, loader):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in loader:
            preds = model(images).argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.numel()
    return correct / total

for epoch in range(3):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()

train_acc = evaluate(model, train_loader)
test_acc = evaluate(model, test_loader)
print("Точность на обучении:", round(train_acc, 4))
print("Точность на тесте:", round(test_acc, 4))
```

Мы переиспользуем функцию `evaluate` для обеих выборок. Точность на обучающих данных получается выше (около 98–99%), чем на тестовых (96–97%): модель запоминает часть примеров и использует это преимущество именно на знакомых данных. Разрыв в 1–2 процентных пункта — нормальное поведение после трёх эпох; если бы разрыв был большим, следовало бы добавить регуляризацию (dropout), собрать больше данных или упростить модель. Сравнение обучающей и тестовой ошибок — обязательная проверка в любом ML-проекте: по ней судят о переобучении.
<!--/SOLUTION-->

<!--QUIZ-->
Сколько обучающих изображений в MNIST?
- 10 000
- 60 000
- 28 000
- 784 000
* Правильный ответ: 60 000
Плюс 10 000 тестовых изображений.

Зачем нужен transforms.Normalize?
- Чтобы превратить изображение в чёрно-белое
- Чтобы центрировать данные: вычесть среднее и поделить на стандартное отклонение
- Чтобы увеличить яркость
- Чтобы ускорить загрузку
* Правильный ответ: Чтобы центрировать данные: вычесть среднее и поделить на стандартное отклонение
Так данные распределены вокруг нуля, и обучение идёт стабильнее.

Зачем DataLoader использует shuffle=True?
- Чтобы данные помещались в память
- Чтобы перемешивать примеры перед каждой эпохой
- Чтобы ускорить загрузку
- Чтобы обеспечить одинаковый порядок
* Правильный ответ: Чтобы перемешивать примеры перед каждой эпохой
Перемешивание улучшает обучение.

Почему у выходного слоя сети 10 выходов?
- Потому что изображения имеют 10 каналов
- По числу классов — цифр от 0 до 9
- Потому что 10 — это стандарт для всех сетей
- Это случайный выбор
* Правильный ответ: По числу классов — цифр от 0 до 9
Каждый выход — оценка для своего класса.

Что делает F.cross_entropy(logits, labels)?
- Применяет softmax и считает логарифмическую потерю
- Сравнивает предсказания с эталоном
- Применяет argmax
- Считает точность
* Правильный ответ: Применяет softmax и считает логарифмическую потерю
Softmax объединён с потерей, поэтому отдельно он не нужен.

Зачем вызывать model.eval() перед оценкой?
- Чтобы включить dropout
- Чтобы отключить случайные механизмы и подсчёт градиентов
- Чтобы ускорить обучение
- Чтобы обнулить параметры
* Правильный ответ: Чтобы отключить случайные механизмы и подсчёт градиентов
В режиме оценки модель ведёт себя детерминированно.
<!--/QUIZ-->
