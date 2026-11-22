---
title: Independent Work: Neural Network Classifier
summary: Data preparation, loaders, a fully connected network in PyTorch, the training loop, accuracy evaluation, and error analysis on the MNIST dataset.
order: 7
duration: 240 min
difficulty: advanced
tags: pytorch, neural networks, mnist, classification, training
---

# Independent Work: Neural Network Classifier

Hi! This is an advanced-level independent work. In 240 minutes you will build a full neural network from scratch in PyTorch: from data loading to training, quality evaluation, and error analysis. This is not a "toy" example but a real pipeline used for computer vision tasks in industry.

## Problem statement

The bank «Цифра» is rolling out handwritten digit recognition for automatic processing of applications. Historically, clients fill out forms by hand, and digits (for example, a phone number or an amount) must be extracted from images. You need to develop a prototype classifier of handwritten digits on the MNIST dataset: 70,000 black-and-white 28×28 images (60,000 training, 10,000 test), each one a digit from 0 to 9.

Requirements:

1. **Data**: load MNIST via `torchvision.datasets.MNIST`, normalize pixels, split the training set into train/validation, and visually inspect samples.
2. **DataLoader**: batched data feeding with shuffling, correct batch size.
3. **Model**: a fully connected network (MLP) on `nn.Module` — three layers, ReLU activation, output for 10 classes.
4. **Training**: CrossEntropyLoss loss function, Adam optimizer, several epochs, logging losses and accuracy, saving a checkpoint.
5. **Evaluation**: test-set accuracy, confusion matrix, predictions for new images, error analysis, and one model improvement experiment (adding a layer or dropout).

Success criteria:

- test-set accuracy of at least 97% for the baseline model;
- the report must include a confusion matrix and examples of correctly/incorrectly recognized digits;
- all code — in one or several `.py` files, runnable with `python train.py`.

## What you will review

PyTorch: `torchvision.datasets`, `transforms.ToTensor` and `transforms.Normalize`, `DataLoader`, `nn.Module`, `nn.Linear`, `nn.ReLU`, `nn.Dropout`, `F.cross_entropy`, `optim.Adam`, `model.train()` / `model.eval()` / `torch.no_grad()`, `model.state_dict()`, `torch.save`. Metrics: accuracy, confusion matrix via `sklearn.metrics.confusion_matrix`.

## Work plan

Stages go in order. Each next one uses the result of the previous. The result of each stage is verified by running the code.

<!--TASK-->
### Task 1
Create `train.py` and load the MNIST dataset via `torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())` (for the test set — `train=False`). Print: the dataset object type, `len(train_data)`, one image's size (`train_data[0][0].shape`), the number of classes (`len(train_data.classes)`), and the minimum and maximum pixel values. Split the training set into train/validation in a 90/10 ratio via `random_split` (don't forget `torch.manual_seed(42)`). Draw a grid of 10 images (one per class) with labels, using `matplotlib` and `plt.imshow(img.squeeze(), cmap="gray")`. Expected result: console output with facts about the data and a grid picture showing all 10 digits.

### Task 2
Create `DataLoader` for train, validation, and test: `batch_size=64`, `shuffle=True` for train, `shuffle=False` for validation/test. In a loop, go through one batch and print: the tensor shape `images.shape`, the label tensor shape `labels.shape`, the data type, and the pixel value range (after `ToTensor` they should be in [0, 1]). Then add normalization via `transforms.Normalize((0.1307,), (0.3081,))` (MNIST mean and standard deviation) — recreate the datasets and DataLoaders with it, and print the value range again. Expected result: without normalization pixels are from 0 to 1, and after — roughly from −4 to +4 (standard deviation 1).

### Task 3
Define the class `Net(nn.Module)` — a fully connected network: `nn.Flatten()` (or `x.view(x.size(0), -1)`), `nn.Linear(28*28, 128)`, `nn.ReLU()`, `nn.Linear(128, 64)`, `nn.ReLU()`, `nn.Linear(64, 10)`. Write `forward(self, x)` that takes a batch of images (B, 1, 28, 28) and returns logits of shape (B, 10). Create the model, print the number of parameters (`sum(p.numel() for p in model.parameters())`), and run one test batch through `model(images)` — print the output shape. Expected result: the model is created, the parameter count is printed (should be about 120 thousand), and the output shape is (64, 10).

### Task 4
Write the functions `train_one_epoch(model, loader, optimizer)` and `evaluate(model, loader)`. The first: loop over batches, zero gradients (`optimizer.zero_grad()`), forward pass, compute loss via `F.cross_entropy(logits, labels)`, backward pass (`loss.backward()`), optimizer step (`optimizer.step()`), accumulate the loss sum and the number of correct predictions. The second: `model.eval()` + `torch.no_grad()`, return a tuple `(loss, accuracy)`. Train the model for 5 epochs with `optim.Adam(model.parameters(), lr=1e-3)`; after each epoch print: epoch number, train loss, val loss, val accuracy. At the end save `model.state_dict()` to `mnist_mlp.pt`. Expected result: val accuracy grows from epoch to epoch and reaches at least 96% by the 5th; a checkpoint file appears.

### Task 5
Evaluate the model on the test set: print test loss and test accuracy. Compute a confusion matrix via `from sklearn.metrics import confusion_matrix` and visualize it as a heatmap (`plt.imshow` + `plt.colorbar` + class labels). Visualize 5 examples where the model erred (image, true label, prediction). Run an improvement experiment: add `nn.Dropout(0.3)` after the first ReLU (or a third hidden layer), retrain for 5 epochs, and compare accuracy. Expected result: test accuracy ≥ 97% for the best model, the confusion matrix heatmap is saved, and the report compares the baseline and improved models.

<!--/TASK-->

<!--HINT-->
### Hint 1
`ToTensor()` converts PIL images into tensors itself, and `len(train_data)` and `train_data[0]` give a tuple (tensor, label). For `random_split` you need a list of lengths: `[int(len(train_data) * 0.9), len(train_data) - int(len(train_data) * 0.9)]`. Draw the grid like this: `fig, axes = plt.subplots(2, 5, figsize=(12, 5))`, then for each axis `axes[i // 5][i % 5].imshow(images[i].squeeze(), cmap="gray")` and set `set_title`.

### Hint 2
The batch shape is `(64, 1, 28, 28)` — four indices: batch, channel, height, width. `x.view(x.size(0), -1)` flattens (64, 1, 28, 28) into (64, 784). For normalization add `transforms.Normalize((0.1307,), (0.3081,))` — these parameters are the mean and standard deviation across all MNIST; they turn pixels into values with mean 0 and spread 1.

### Hint 3
In `__init__`, declare layers as attributes: `self.fc1 = nn.Linear(784, 128)` and so on. In `forward` — `x = self.fc1(x)`; `x = F.relu(x)` — don't forget to import `torch.nn.functional as F`. Create the model: `model = Net()`. Test batch: `images, labels = next(iter(train_loader))`; then `out = model(images)`.

### Hint 4
`F.cross_entropy(logits, labels)` combines softmax and cross-entropy. For accuracy: `correct = (logits.argmax(1) == labels).sum().item()`, accuracy = `correct / len(loader.dataset)`. In `evaluate`, definitely `model.eval()` and `with torch.no_grad():`. The optimizer and loss live in `train.py`, outside functions. Saving: `torch.save(model.state_dict(), "mnist_mlp.pt")`.

### Hint 5
Confusion matrix: `cm = confusion_matrix(all_labels, all_preds)` — collect predictions across all test batches into lists. Heatmap: `plt.imshow(cm, cmap="Blues")` + `plt.colorbar()` + `plt.xticks(range(10))`. For errors: iterate over test predictions, collect indices where `pred != true`, take the first 5, and draw via `plt.subplots(1, 5)`. Experiment: add `self.dropout = nn.Dropout(0.3)` and `x = self.dropout(x)` after the first ReLU; retrain and compare.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
The beginning of `train.py`:

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

MNIST downloads automatically on the first run into the `./data` folder. `ToTensor()` converts PIL images into `torch.FloatTensor` tensors of shape (1, 28, 28) — one channel, height and width 28. `random_split` takes a list of subset lengths and returns view objects that behave like datasets. `manual_seed(42)` fixes randomness for both the split and the shuffling — training is reproducible. The grid is collected in one pass: we store one image per class in the `examples` dictionary until we have all 10, then draw. `squeeze()` removes the channel dimension: (1, 28, 28) → (28, 28) — otherwise `imshow` would render a single-channel image incorrectly.

### Solution 2
We add DataLoader and normalization:

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

`DataLoader` wraps the dataset and serves data in batches. `shuffle=True` for train shuffles every epoch — this reduces correlation between neighboring examples and helps convergence. Normalization is applied inside `transform` on the fly, before feeding the network. The parameters 0.1307 and 0.3081 are the mean and standard deviation of all MNIST pixels; after `(x - 0.1307) / 0.3081` the data is close to zero with unit scale. Without normalization, large values (around 1.0) slow convergence and can "saturate" sigmoid functions; with it, gradients become uniform. The distribution after normalization: roughly from −4 to +4.

### Solution 3
We define the model:

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

`nn.Module` automatically registers layers declared as attributes — their parameters are collected via `model.parameters()`. `view(x.size(0), -1)` flattens (64, 1, 28, 28) into (64, 784): `x.size(0)` keeps the batch size, `-1` computes the rest automatically. We have a hidden layer with input 784 and output 128, then 128→64, then 64→10. ReLU is the standard nonlinearity — simple and fast. The output is logits (without softmax): cross-entropy adds it itself. Parameter count: 784·128 + 128 + 128·64 + 64 + 64·10 + 10 = 100,352 + 8,256 + 650 = 109,258 — a "light" network that trains in minutes on CPU.

### Solution 4
Training:

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

The training loop is four steps: `zero_grad()` (clear old gradients), `loss.backward()` (compute new ones), `optimizer.step()` (update weights). `F.cross_entropy` combines softmax and the loss. `argmax(1)` takes the index of the maximum logit — the predicted class. In `evaluate`, `model.eval()` (disables dropout, if any) and `torch.no_grad()` (doesn't build the graph — saves memory and speeds up) are mandatory. Loss is averaged over the number of examples, not batches: `loss.item() * images.size(0)`. Adam with lr=1e-3 is a reliable default choice. Five epochs usually give validation accuracy of 97%+.

### Solution 5
Evaluation and analysis:

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

The confusion matrix shows which digit pairs the model confuses; usually these are "similar" pairs (4/9, 7/2) — that's normal behavior for handwritten digits. The heatmap with numbers in cells makes the matrix readable. Collecting errors: we walk over test examples and take those where the prediction differs from the true label; we draw the first five. For the improvement experiment, add `nn.Dropout(0.3)` to `Net` and apply it after the first ReLU in `forward`:

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

Dropout randomly zeros 30% of neurons during training — the network learns not to rely on individual neurons, which reduces overfitting. Note: on validation and test, dropout is automatically disabled thanks to `model.eval()`. Retrain and compare accuracies: the improved model usually gives +0.1–0.5% on test and is more stable. Final report: baseline and improved model accuracies, confusion matrix, error examples, and the best model's checkpoint.

<!--/SOLUTION-->

## Assessment criteria

| Criterion | What is checked | Points |
|---|---|---|
| Loading and data exploration | Correct calls, dataset facts, example grid | 15 |
| DataLoader and normalization | `batch_size`, shuffling, value ranges before/after | 15 |
| Model | `Net` class, output shape, reasonable parameter count | 20 |
| Training | `train_one_epoch`/`evaluate` functions, accuracy growth, checkpoint | 20 |
| Evaluation | Test accuracy ≥ 97%, confusion matrix, error examples | 20 |
| Experiment | Improved model, comparison with baseline | 10 |

Total 100 points. Grade: 90+ — "excellent", 75–89 — "good", 60–74 — "satisfactory", below 60 — the work needs refinement.

## What to submit

1. The file `train.py` (or a project with several `.py` files) — full code that reproduces training from scratch.
2. The checkpoint file `mnist_mlp.pt` (best model).
3. Images: `mnist_samples.png`, `confusion_matrix.png`, `mistakes.png`.
4. A report (README or markdown): how many epochs, final train/val/test accuracy, comparison of baseline and improved models, a description of what the confusion matrix showed.
5. Run commands in the README: `pip install torch torchvision scikit-learn matplotlib` and `python train.py`.

<!--QUIZ-->
What tensor will `train_data[0][0]` return after `transforms.ToTensor()`?
- A PIL image
- A torch tensor of shape (1, 28, 28) with values from 0 to 1
- A tensor of shape (28, 28) with values from 0 to 255
- A NumPy array
* Correct answer: A torch tensor of shape (1, 28, 28) with values from 0 to 1
`ToTensor()` converts the image into a float tensor and normalizes pixels to [0, 1]; one channel, height and width 28.

Why is `Normalize((0.1307,), (0.3081,))` normalization needed?
- To make the pictures prettier
- To bring pixels to mean 0 and standard deviation 1 — this speeds up convergence
- To reduce image size
- To make the pictures black-and-white
* Correct answer: To bring pixels to mean 0 and standard deviation 1 — this speeds up convergence
The parameters are the mean and standard deviation of MNIST pixels; normalization stabilizes the input feature scale.

What does `x.view(x.size(0), -1)` do?
- Adds a channel dimension
- Flattens a batch of images into a matrix (B, 784)
- Shuffles the batch
- Changes the data type
* Correct answer: Flattens a batch of images into a matrix (B, 784)
`view` changes the shape: (64, 1, 28, 28) → (64, 784), where 784 = 28·28; `-1` infers the dimension automatically.

About how many parameters does a model with layers 784→128→64→10 have?
- About 10,000
- About 109,000
- About 1,000,000
- Exactly 784
* Correct answer: About 109,000
The sum: 784·128 + 128 + 128·64 + 64 + 64·10 + 10 = 109,258 parameters.

What does `F.cross_entropy(logits, labels)` combine?
- Only the loss function
- Softmax and cross-entropy
- Sigmoid and MSE
- The ReLU activation
* Correct answer: Softmax and cross-entropy
`cross_entropy` applies softmax to logits and computes cross-entropy in one operation — numerically more stable than doing it by hand.

Why is `optimizer.zero_grad()` needed before `loss.backward()`?
- To speed up training
- To zero the gradients accumulated from previous batches — otherwise they sum up
- To clear GPU memory
- To reset the model weights
* Correct answer: To zero the gradients accumulated from previous batches — otherwise they sum up
PyTorch accumulates gradients; without zeroing, each batch would carry "tails" from previous steps.

What does `model.eval()` do?
- Starts training
- Switches the model to inference mode: disables dropout and batch normalization
- Saves the model to disk
- Clears gradients
* Correct answer: Switches the model to inference mode: disables dropout and batch normalization
In evaluation mode dropout is turned off, and the model works deterministically.

Why is `torch.no_grad()` needed in the evaluation function?
- To forbid weight updates
- To avoid building the computation graph: saves memory and speeds up evaluation
- To disable dropout
- To make predictions more accurate
* Correct answer: To avoid building the computation graph: saves memory and speeds up evaluation
Gradients aren't needed during evaluation; without building the graph the code runs noticeably faster.

What role does `nn.Dropout(0.3)` play in the improved model?
- Increases the number of layers
- Randomly zeros 30% of neurons during training — reduces overfitting
- Speeds up the forward pass
- Replaces ReLU
* Correct answer: Randomly zeros 30% of neurons during training — reduces overfitting
Dropout makes the network more robust: it can't rely on individual neurons, so it generalizes better.
<!--/QUIZ-->
