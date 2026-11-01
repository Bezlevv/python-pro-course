---
title: Проект: нейросеть для распознавания цифр
summary: Обучаем нейронную сеть распознавать рукописные цифры из датасета MNIST: данные, модель, обучение, оценка точности.
order: 6
duration: 120 мин
difficulty: advanced
---

Привет! Это самый современный проект модуля: мы обучим настоящую нейронную сеть. Программа возьмёт изображения рукописных цифр, научится отличать «0» от «9» и проверит себя на тестовых картинках, которые никогда не видела.

## О проекте

Задача называется классификацией изображений. Датасет MNIST содержит 70 000 картинок 28×28 пикселей с цифрами. Основные шаги:

1. Загрузить данные и превратить их в тензоры PyTorch.
2. Собрать нейросеть — многослойный перцептрон (MLP).
3. Обучить: показать примеры, посчитать ошибку, обновить веса.
4. Оценить точность на тестовой выборке.

## План сборки

1. Установить PyTorch и torchvision.
2. Загрузить MNIST и собрать загрузчики данных.
3. Описать модель сети.
4. Написать цикл обучения.
5. Посчитать точность на тестах.
6. Сохранить модель и проверить предсказание.

## Шаг 1. Установка

```bash
pip install torch torchvision
```

Если на компьютере есть NVIDIA GPU, можно установить CUDA-версию с сайта pytorch.org, но для нашего проекта хватит и процессора.

## Шаг 2. Данные

MNIST входит в `torchvision.datasets`:

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])

train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)
```

`ToTensor()` превращает картинку в тензор (и делит яркость на 255), `Normalize` приводит значения к нулевому среднему. `DataLoader` выдаёт данные пакетами (batch) размером 64 и перемешивает тренировочные примеры.

## Шаг 3. Модель

Картинка 28×28 — это 784 числа. Сеть будет учить отображение из 784 входов в 10 вероятностей (цифры 0–9):

```python
class DigitsNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        return self.layers(x)
```

`nn.Flatten` вытягивает картинку в вектор, `nn.Linear` — полносвязный слой, `nn.ReLU` — функция активации (без неё слои нельзя складывать в глубокую сеть).

## Шаг 4. Обучение

Цикл обучения выглядит так:

```python
model = DigitsNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 5
for epoch in range(epochs):
    total_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Эпоха {epoch + 1}: loss = {total_loss / len(train_loader):.4f}")
```

Пять строк — сердце любого обучения: обнулить градиенты, посчитать предсказания, вычислить ошибку (`CrossEntropyLoss`), распространить её назад (`loss.backward()`) и сделать шаг оптимизатором (`optimizer.step()`).

## Шаг 5. Точность

Прогоним модель по тесту и посчитаем долю верных ответов:

```python
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        preds = outputs.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total
print(f"Точность: {accuracy:.2%}")
```

`torch.no_grad()` отключает вычисление градиентов — это ускоряет проверку и экономит память. `argmax(dim=1)` выбирает цифру с максимальной вероятностью.

## Шаг 6. Сохранение

```python
torch.save(model.state_dict(), "digits_model.pth")
```

А загрузка — `model.load_state_dict(torch.load("digits_model.pth"))`. Файл `.pth` содержит только веса — это стандартный формат PyTorch.

## Итог урока

Мы узнали:

- что такое тензоры и как загружать данные DataLoader'ами;
- как описывать сеть на `nn.Module`;
- как устроен цикл обучения;
- как оценивать точность и сохранять модель.

<!--TASK-->
**Задача.** Собери проект целиком и добейся точности не ниже 97% на тестовой выборке. Для этого:

1. Добавь второй скрытый слой (например, `nn.Linear(256, 128)` + `nn.ReLU()`).
2. Увеличь число эпох до 8–10.
3. Выведи точность после каждой эпохи на тренировочной выборке (можно посчитать на первых 1000 примерах, чтобы не ждать долго).
4. Сохрани модель и выведи точность на тесте после обучения.

Ожидаемый вывод: в конце обучения строка вида `Точность на тесте: 98.12%` (у MLP с одним скрытым слоем реально достижимо ~98%).
<!--/TASK-->

<!--HINT-->
Точность на обучающей выборке считается так же, как на тестовой, но по `train_loader` (или его части). Проверь, что `model.train()` стоит перед обучением, а `model.eval()` — перед оценкой: это правильный режим для PyTorch.
<!--/HINT-->

<!--SOLUTION-->
Полное решение (`mnist_mlp.py`):

```python
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,)),
])

train_data = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_data = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)


class DigitsNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.layers(x)


def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return correct / total


def train_one_epoch(model, criterion, optimizer, loader):
    model.train()
    total_loss = 0.0
    for images, labels in loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


model = DigitsNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

epochs = 10
for epoch in range(epochs):
    avg_loss = train_one_epoch(model, criterion, optimizer, train_loader)
    train_acc = evaluate(model, train_loader)
    print(f"Эпоха {epoch + 1}: loss = {avg_loss:.4f}, "
          f"train acc = {train_acc:.2%}")

test_acc = evaluate(model, test_loader)
print(f"Точность на тесте: {test_acc:.2%}")

torch.save(model.state_dict(), "digits_model.pth")
```

Разбор:

- Модель стала глубже: 784 → 256 → 128 → 10, между линейными слоями — `ReLU`. Больше параметров — выше потенциальная точность, но и дольше обучение.
- `evaluate` — универсальная функция: она работает и с `train_loader`, и с `test_loader`. Внутри обязательные `model.eval()` и `torch.no_grad()`.
- В `train_one_epoch` первой строкой стоит `model.train()` — верный режим сети во время обучения.
- Точность ~98% достижима уже за 10 эпох на CPU (2–5 минут). Если хочешь больше — добавь свёрточные слои (`nn.Conv2d`, `nn.MaxPool2d`), это стандартный следующий шаг для задач с картинками.
- Файл `digits_model.pth` сохраняет обученные веса; загружаются они через `model.load_state_dict(torch.load("digits_model.pth"))`.
<!--/SOLUTION-->
