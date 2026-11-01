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
**Задача.** Добавь к сети с одним скрытым слоем ещё один: после слоя 784 → 128 поставь слой 128 → 64 с ReLU, затем выходной 64 → 10. Обучи сеть так же, как в теории (Adam, lr = 1e-3, 3 эпохи, батч 64) и выведи точность на тесте после каждой эпохи. Ожидаемый результат: три строки вида `epoch=0 test_acc=0.9621 ...`; точность на третьей эпохе не ниже 95% и выше, чем у базовой сети (96–97%).
<!--/TASK-->

<!--HINT-->
Вставь `self.fc_mid = nn.Linear(128, 64)` между `fc1` и `fc2` и не забудь ReLU между скрытыми слоями. Вход второго скрытого слоя — 128, выход — 64. Код цикла обучения и `evaluate` менять не нужно.
<!--/HINT-->

<!--SOLUTION-->
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

Разбор шагов. Изменения — только в архитектуре: между двумя полносвязными слоями появился третий, 128 → 64. Теперь сеть сначала сжимает 784 пикселя до 128 признаков, потом до 64, и лишь затем выдаёт 10 оценок. Число параметров выросло примерно на `128·64 + 64 = 8256` — это небольшая добавка к базовым ~102 тысячам.

Что изменилось на практике? Глубокая сеть учится чуть дольше на эпоху, но обычно достигает заметно более высокой точности: около 97–97.5% против 96–97% у базовой. Чем больше скрытых слоёв, тем более сложные комбинации признаков может построить модель — но до порога: на 28×28 чёрно-белых картинках очень глубокие полносвязные сети почти перестают давать выигрыш и просто учатся дольше.

Обрати внимание на функцию `evaluate`: она переключает модель в режим оценки, отключает градиенты через `torch.no_grad()` и считает долю правильных `argmax`-ответов. Этот же шаблон мы будем использовать и в следующем уроке, когда сеть станет свёрточной.
<!--/SOLUTION-->
