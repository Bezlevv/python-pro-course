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
### Задача 1
Увеличь число фильтров в свёрточных слоях вдвое (16 → 32 и 32 → 64) и добавь слой `nn.Dropout(0.25)` перед полносвязным классификатором. Обучи сеть 3 эпохи и выведи точность на тесте после каждой. Дополнительно напечатай общее число параметров модели через `sum(p.numel() for p in model.parameters())`. Ожидаемый результат: точность на третьей эпохе не ниже 98%, а число параметров — порядка 50 тысяч.

### Задача 2
Добавь третий свёрточный блок: после `conv2` поставь `nn.Conv2d(32, 128, kernel_size=3, padding=1)`, затем ReLU и `MaxPool2d(2)`. Вход полносвязного слоя станет `128 * 3 * 3` (после пулинга карта 7×7 превращается в 3×3). Обучи сеть 3 эпохи, выведи точность после каждой эпохи и число параметров. Ожидаемый результат: точность не ниже 98%, параметров около 53 тысяч.

### Задача 3
Обучи сеть из задачи 1 не 3, а 5 эпох и выведи точность после каждой. Ожидаемый результат: точность продолжает расти — на пятой эпохе около 98.5–99%. Если рост замедлился, это сигнал, что сеть почти достигла предела своих возможностей на данном датасете.

### Задача 4
Добавь `nn.BatchNorm2d(16)` сразу после первого ReLU (до пулинга) в сеть из задачи 1. Обучи сеть 3 эпохи и выведи точность после каждой. Ожидаемый результат: точность около 98% и выше — батч-нормализация стабилизирует распределения внутри сети и часто ускоряет сходимость.

### Задача 5
Возьми первый батч тестовых данных (`images, labels = next(iter(test_loader))`) и выведи предсказанные и настоящие цифры для первых пяти изображений (через `preds[:5]` и `labels[:5]`). Ожидаемый результат: два списка из пяти чисел, которые почти полностью совпадают — сеть уверенно распознаёт цифры.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Когда число фильтров второго слоя станет 64, размер перед `fc` станет 64·7·7 = 3136 — поменяй вход `nn.Linear`. Dropout ставь после `view`, перед `fc`; он автоматически отключается в режиме `model.eval()`, поэтому менять `evaluate` не нужно.

### Подсказка 2
Новый блок повторяет структуру предыдущих: свёртка → ReLU → пулинг. Убедись, что `in_channels` третьей свёртки равен 32 (выход второй), а `out_channels` — 128. После пулинга размер карты уменьшается с 7 до 3 (7 // 2 = 3), поэтому `fc` получит 128·3·3.

### Подсказка 3
Просто замени `range(3)` на `range(5)` в цикле обучения. Печать уже настроена на вывод точности после каждой эпохи, так что изменения ограничатся одной строкой.

### Подсказка 4
Вставь `self.bn1 = nn.BatchNorm2d(16)` в `__init__` и примени в `forward` сразу после ReLU: `x = self.pool(self.bn1(torch.relu(self.conv1(x))))`. Важно: `BatchNorm2d` ведёт себя по-разному в режимах `train()` и `eval()` — обе функции уже вызывают нужные режимы.

### Подсказка 5
После обучения добавь: `images, labels = next(iter(test_loader))`, затем `preds = model(images).argmax(dim=1)` и напечатай `preds[:5]` и `labels[:5]`. Помни: модель должна быть в режиме `eval()`, иначе batch-norm и dropout дадут случайные результаты.
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

Мы удвоили число фильтров: первый свёрточный слой теперь извлекает 32 признака, второй — 64. Соответственно выросла и карта перед классификатором: 64·7·7 = 3136 чисел, поэтому вход `fc` изменён. Число параметров считаем одной строкой: `p.numel()` возвращает количество чисел в тензоре параметра, а `sum` складывает их по всем слоям — получится около 50 тысяч. Зачем dropout? При обучении он случайно обнуляет 25% нейронов перед выходным слоем, заставляя сеть не полагаться на отдельные признаки и тем самым уменьшая переобучение. Важно: `nn.Dropout` активен только в режиме `model.train()`, а в `model.eval()` превращается в тождественную операцию — поэтому точность считается корректно без правок. Результат: 98–99% на тесте — это продакт-уровень для MNIST. Ключевой вывод урока: правильно выбранная архитектура (локалность свёрток) важнее простого увеличения числа параметров. Дальше — CNN, ResNet, трансформеры и свои проекты: ты готов.

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

class DeepCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(128 * 3 * 3, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))   # 28 -> 14
        x = self.pool(torch.relu(self.conv2(x)))   # 14 -> 7
        x = self.pool(torch.relu(self.conv3(x)))   # 7 -> 3
        x = x.view(x.size(0), -1)
        return self.fc(x)

model = DeepCNN()
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

Третий блок устроен так же, как предыдущие: свёртка с padding = 1 не меняет пространственный размер (7×7 остаётся 7×7), а пулинг уменьшает его вдвое с округлением вниз: 7 → 3. Поэтому после третьего пулинга карта имеет размер 3×3, и вектор для классификатора содержит 128·3·3 = 1152 числа. Число параметров при этом около 53 тысяч: основную массу составляют веса третьей свёртки (128·(32·9 + 1) = 36 992) и полносвязного слоя (1152·10 + 10 = 11 530). Точность на тесте остаётся на уровне 98%+ — глубина добавляет выразительность, но на простых цифрах MNIST выигрыш по сравнению с широкой сетью из задачи 1 уже мал. Это ещё одна иллюстрация: и ширина, и глубина полезны до определённого предела, дальше которого качество упирается в данные.

### Разбор 3
Решение:

```python
# Сеть WiderCNN из задачи 1 остаётся без изменений.
# Меняется только число эпох в цикле обучения:
for epoch in range(5):
    model.train()
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = F.cross_entropy(model(images), labels)
        loss.backward()
        optimizer.step()
    acc = evaluate(model, test_loader)
    print(f"epoch={epoch}  test_acc={acc:.4f}")
```

Увеличение числа эпох с 3 до 5 позволяет модели продолжить улучшать веса: после третьей эпохи точность обычно около 98%, к пятой она подрастает до 98.5–99%. При этом прирост с каждой эпохой становится всё меньше — кривая обучения «выходит на плато». Это типичная картина: точность сначала растёт быстро, затем всё медленнее, а после длительного обучения может начать падать из-за переобучения. Правильная стратегия — наблюдать за тестовой точностью и останавливаться, когда прирост становится пренебрежимо малым; для этого как раз и нужна функция `evaluate`, которую мы вывели в отдельную процедуру. Дополнительно можно сохранять лучшую модель по чекпоинтам — это стандартная практика в реальных проектах.

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

class BNCnn(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(0.25)
        self.fc = nn.Linear(64 * 7 * 7, 10)

    def forward(self, x):
        x = self.pool(self.bn1(torch.relu(self.conv1(x))))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        return self.fc(x)

model = BNCnn()
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

Батч-нормализация нормирует активации внутри батча: для каждого канала она вычитает среднее и делит на стандартное отклонение, а затем применяет обучаемые коэффициенты масштаба и сдвига. Это стабилизирует распределения на входах следующих слоёв и обычно позволяет использовать более высокие скорости обучения и реже зависать в плохих локальных минимумах. В `forward` мы вставили `bn1` сразу после ReLU первого свёрточного слоя. Критически важна пара режимов: в `model.train()` BatchNorm использует статистики текущего батча, а в `model.eval()` — накопленные скользящие средние, поэтому оценка без `eval()` дала бы неверные результаты. Точность на тесте остаётся на уровне 98%+ — как и без BatchNorm, но сходимость обычно становится стабильнее, что особенно ценно на больших моделях.

### Разбор 5
Решение:

```python
# После цикла обучения и до вывода точности добавь:
model.eval()
images, labels = next(iter(test_loader))
with torch.no_grad():
    preds = model(images).argmax(dim=1)

print("Предсказания:", preds[:5].tolist())
print("Настоящие:", labels[:5].tolist())
```

`next(iter(test_loader))` достаёт первый батч тестовых данных — 256 изображений и меток. Мы прогоняем их через модель в режиме `eval()` и без градиентов, берём `argmax` по десяти выходам — индекс наибольшей оценки и есть предсказанная цифра. Вывод первых пяти элементов двух списков показывает, что сеть распознаёт цифры: предсказания, как правило, совпадают с настоящими метками. Это уже не абстрактное «обучение», а работающий классификатор, который можно применить к любому новому изображению 28×28. С этого момента ты можешь брать любые данные — переводить их в тензоры нужной формы и прогонять через обученную модель. Дальнейший путь — свёрточные архитектуры глубже (ResNet), трансформеры и трансферное обучение, о которых говорится в теории урока.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает свёрточный фильтр?
- Проходит по изображению окном и считает скалярное произведение с пикселями
- Уменьшает число каналов
- Перемешивает пиксели
- Дублирует изображение
* Правильный ответ: Проходит по изображению окном и считает скалярное произведение с пикселями
Так появляются карты признаков.

Зачем нужен макс-пулинг?
- Чтобы увеличить разрешение
- Чтобы уменьшить размер карты вдвое и сохранить самые сильные реакции
- Чтобы добавить цвет
- Чтобы удалить шум
* Правильный ответ: Чтобы уменьшить размер карты вдвое и сохранить самые сильные реакции
Пулинг удешевляет вычисления и даёт устойчивость к сдвигам.

Сколько параметров у слоя nn.Conv2d(1, 16, kernel_size=3)?
- 160
- 16
- 144
- 1000
* Правильный ответ: 160
16 фильтров × (1 канал × 9 весов + 1 сдвиг) = 160.

Почему CNN с примерно 20 тысячами параметров побеждает MLP со 100 тысячами на MNIST?
- Потому что CNN учитывает локальность пикселей
- Потому что CNN использует больше данных
- Потому что она быстрее работает
- Это случайность
* Правильный ответ: Потому что CNN учитывает локальность пикселей
Свёртки ищут локальные паттерны — рёбра, углы, узоры.

Что такое трансферное обучение?
- Перенос предобученной модели на свою задачу
- Обучение с нуля
- Копирование весов из одного слоя в другой
- Обучение на трансформерах
* Правильный ответ: Перенос предобученной модели на свою задачу
Берут модель, обученную на миллионах изображений, и дообучивают на своей выборке.

Зачем нужен dropout?
- Чтобы уменьшить переобучение, случайно обнуляя часть нейронов
- Чтобы ускорить обучение
- Чтобы увеличить точность на обучении
- Чтобы добавить шум в данные
* Правильный ответ: Чтобы уменьшить переобучение, случайно обнуляя часть нейронов
Модель учится не полагаться на отдельные признаки.

Что делает padding=1 в свёрточном слое?
- Дополняет края изображения нулями, чтобы размер карты не уменьшался
- Увеличивает число фильтров
- Включает пулинг
- Добавляет цветовые каналы
* Правильный ответ: Дополняет края изображения нулями, чтобы размер карты не уменьшался
С фильтром 3×3 и padding=1 выходная карта сохраняет размер входа.

Что такое ResNet?
- Архитектура с обходными связями, позволяющая обучать очень глубокие сети
- Библиотека для работы с текстом
- Датасет изображений
- Оптимизатор
* Правильный ответ: Архитектура с обходными связями, позволяющая обучать очень глубокие сети
Обходные связи (skip connections) помогают градиентам проходить через десятки и сотни слоёв.
<!--/QUIZ-->
