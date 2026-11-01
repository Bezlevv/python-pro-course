---
title: Свёрточные сети и дальнейший путь
summary: Свёртка, пулинг и первая свёрточная сеть на MNIST. Обзор пути дальше: ResNet, трансформеры, трансферное обучение.
order: 7
duration: 45 мин
difficulty: advanced
---

Полносвязная сеть неплохо справилась с MNIST, но у неё есть принципиальный изъян: она видит каждый пиксель независимо и не понимает, что соседние пиксели образуют линии и узоры. Свёрточные сети (CNN) построены прямо на этой идее: они ищут локальные паттерны — сначала рёбра и углы, затем более сложные элементы, и в итоге целые объекты.

## Свёртка

Свёрточный слой проходит по изображению маленьким окном — фильтром (ядром), например 3×3. В каждом положении окна считается скалярное произведение весов фильтра с пикселями под ним — так получается одно число «карты признаков». Один фильтр ищет одну закономерность; обычно в слое сотни фильтров. Гиперпараметры: `kernel_size` (размер окна), `stride` (шаг), `padding` (дополнение краёв нулями, чтобы размер не уменьшался).

## Пулинг

После свёртки применяют подвыборку — пулинг (чаще всего макс-пулинг): окно 2×2 движется с шагом 2 и оставляет максимум из четырёх чисел. Размер карты уменьшается вдвое, а самые сильные реакции сохраняются. Это удешевляет вычисления и придаёт устойчивость к мелким сдвигам. После двух таких блоков картины 28×28 превращаются в карты 7×7, которые разворачивают в вектор и подают в полносвязный классификатор.

## Архитектура на PyTorch

Ничем не отличается от того, что мы уже видели: те же `nn.Module`, `forward`, оптимизатор и цикл. Новые слои: `nn.Conv2d(in_channels, out_channels, kernel_size, padding)` и `nn.MaxPool2d(2)`. Заметь, как резко падает число параметров относительно полносвязной сети: слой 784 → 128 содержит больше 100 тысяч весов, а свёртка 1 → 16 фильтрами 3×3 — всего 160.

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

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 28 -> 14
        x = self.pool(torch.relu(self.conv2(x)))   # 14 -> 7
        x = x.view(x.size(0), -1)
        return self.fc(x)

model = SimpleCNN()
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

Запусти код. Сеть из ~20 тысяч параметров уже после второй эпохи даст около 98.5% точности — лучше, чем полносвязная сеть со 100 тысячами параметров.

## Что дальше

Идею локальных паттернов развили в десятках архитектур: ResNet добавил обходные связи и научился обучать очень глубокие сети; Transformer перенёс внимание (attention) с текста на изображения (ViT); большие предобученные модели позволяют делать трансферное обучение — взять сеть, обученную на миллионах картинок, и дообучить на своей маленькой выборке. Это стандарт индустрии: свои сети с нуля тренируют редко.

## Практические советы

Обучай на видеокарте: в PyTorch достаточно перевести модель и тензоры через `.to('cuda')` — всё остальное работает так же. Следи за кривыми потерь на обучении и валидации, используй сохранение лучшей модели по чекпоинтам. И помни: данными управляешь ты — если данные предвзяты, модель усилит предвзятость. Для дальнейшего пути: документация PyTorch, курс fast.ai и участие в соревнованиях Kaggle. А сейчас — собери свою первую свёрточную сеть.

<!--TASK-->
**Задача.** Увеличь число фильтров в свёрточных слоях вдвое (16 → 32 и 32 → 64) и добавь слой `nn.Dropout(0.25)` перед полносвязным классификатором. Обучи сеть 3 эпохи и выведи точность на тесте после каждой. Дополнительно напечатай общее число параметров модели через `sum(p.numel() for p in model.parameters())`. Ожидаемый результат: точность на третьей эпохе не ниже 98%, а число параметров — порядка 50 тысяч.
<!--/TASK-->

<!--HINT-->
Когда число фильтров второго слоя станет 64, размер перед `fc` станет 64·7·7 = 3136 — поменяй вход `nn.Linear`. Dropout ставь после `view`, перед `fc`; он автоматически отключается в режиме `model.eval()`, поэтому менять `evaluate` не нужно.
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
train_loader = DataLoader(
    datasets.MNIST("./data", train=True, download=True, transform=transform),
    batch_size=64, shuffle=True,
)
test_loader = DataLoader(
    datasets.MNIST("./data", train=False, download=True, transform=transform),
    batch_size=256,
)

class WiderCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(0.25)
        self.fc = nn.Linear(64 * 7 * 7, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        return self.fc(x)

model = WiderCNN()
print("Параметров:", sum(p.numel() for p in model.parameters()))
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

Разбор шагов. Мы удвоили число фильтров: первый свёрточный слой теперь извлекает 32 признака, второй — 64. Соответственно выросла и карта перед классификатором: 64·7·7 = 3136 чисел, поэтому вход `fc` изменён. Число параметров считаем одной строкой: `p.numel()` возвращает количество чисел в тензоре параметра, а `sum` складывает их по всем слоям — получится около 50 тысяч.

Зачем dropout? При обучении он случайно обнуляет 25% нейронов перед выходным слоем, заставляя сеть не полагаться на отдельные признаки и тем самым уменьшая переобучение. Важно: `nn.Dropout` активен только в режиме `model.train()`, а в `model.eval()` превращается в тождественную операцию — поэтому точность считается корректно без правок.

Результат: 98–99% на тесте — это продакт-уровень для MNIST. Ключевой вывод урока: правильно выбранная архитектура (локалность свёрток) важнее простого увеличения числа параметров. Дальше — CNN, ResNet, трансформеры и свои проекты: ты готов.
<!--/SOLUTION-->
