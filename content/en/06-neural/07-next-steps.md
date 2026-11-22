---
title: Convolutional networks and next steps
summary: Conv layers, pooling, why CNN, further learning paths.
order: 7
duration: 50 min
difficulty: advanced
tags: cnn, conv, pooling
---

Convolutional networks are built for images.

## Convolution

```python
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 7 * 7, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

## Why CNN

- local patterns;
- fewer parameters;
- translation invariance via pooling.

## Next steps

ResNet, transfer learning, transformers, datasets, deployment.

## Lesson summary

Conv + pooling extract features; CNNs beat MLPs on images.

<!--TASK-->
### Task 1 — Conv2d
Create Conv2d(1, 8, 3) and print output shape on 28x28.

### Task 2 — Pool
Apply MaxPool2d(2) and see size halve.

### Task 3 — Model
Define SimpleCNN.

### Task 4 — Forward
Pass a batch and check output shape.

### Task 5 — Why conv
List two reasons in comments.

### Task 6 — Transfer learning
Mention pretrained models (e.g., ResNet).

### Task 7 — Next modules
List 3 directions to study next.
<!--/TASK-->

<!--HINT-->
### Hint 1
nn.Conv2d(1, 8, 3).

### Hint 2
nn.MaxPool2d(2).

### Hint 3
Same as above.

### Hint 4
model(x).shape.

### Hint 5
Local, fewer params.

### Hint 6
torchvision.models.

### Hint 7
Transformers, deployment, data.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import torch
import torch.nn as nn

conv = nn.Conv2d(1, 8, kernel_size=3, padding=1)
x = torch.randn(4, 1, 28, 28)
print(conv(x).shape)   # [4, 8, 28, 28]
```

### Solution 2
```python
pool = nn.MaxPool2d(2)
print(pool(conv(x)).shape)   # [4, 8, 14, 14]
```

### Solution 3
```python
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 7 * 7, 10)
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

### Solution 4
```python
model = SimpleCNN()
print(model(x).shape)   # [4, 10]
```

### Solution 5
```python
# 1) Локальные паттерны: рёбра, текстуры
# 2) Меньше параметров, чем у полносвязных
```

### Solution 6
```python
from torchvision import models
resnet = models.resnet18(pretrained=True)
```

### Solution 7
```python
# Трансформеры, MLOps, инференс-сервисы
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a convolution?
- Filter scanning image
- Pooling
- Flatten
- Dropout
* Correct answer: Filter scanning image
Feature extraction.

What does Conv2d do?
- 2D convolution
- Pooling
- Linear
- Norm
* Correct answer: 2D convolution
Layer.

What is MaxPool2d?
- Downsampling
- Conv
- Linear
- Dropout
* Correct answer: Downsampling
Reduces size.

What is padding?
- Keeps size
- Deletes
- Shrinks
- None
* Correct answer: Keeps size
Border.

What is kernel_size?
- Filter size
- Batch
- Channels
- Stride
* Correct answer: Filter size
3.

What is a feature map?
- Conv output
- Labels
- Loss
- Weight
* Correct answer: Conv output
Channels.

Why fewer parameters?
- Weight sharing
- More data
- Faster only
- None
* Correct answer: Weight sharing
Conv local.

Why pooling?
- Invariance, smaller
- Accuracy only
- Speed only
- None
* Correct answer: Invariance, smaller
Robust.

What is transfer learning?
- Use pretrained
- Train from zero
- Random
- None
* Correct answer: Use pretrained
ResNet.

What is ResNet?
- Deep CNN architecture
- A dataset
- A loss
- A loader
* Correct answer: Deep CNN architecture
Residual.

What shape enters Linear after pooling?
- 16*7*7
- 28
- 10
- 1
* Correct answer: 16*7*7
Flattened.

What is the final output size?
- 10 classes
- 28
- 16
- 1
* Correct answer: 10 classes
Logits.
<!--/QUIZ-->
