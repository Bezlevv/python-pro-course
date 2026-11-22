---
title: SciPy: scientific computing
summary: Optimization, integration, stats.
order: 1
duration: 45 min
difficulty: advanced
tags: scipy
---

SciPy extends NumPy with algorithms.

## Stats

```python
from scipy import stats

data = [1.2, 2.1, 2.9, 3.4]
print(stats.describe(data))
print(stats.ttest_1samp(data, 2.0))
```

## Optimization

```python
from scipy.optimize import minimize

def f(x):
    return (x[0] - 1) ** 2 + (x[1] + 2) ** 2

result = minimize(f, [0, 0])
print(result.x)
```

## Lesson summary

SciPy = stats + optimize + integrate.

<!--TASK-->
### Task 1 — Describe
Summarize data.

### Task 2 — T-test
Run a t-test.

### Task 3 — Normal
Probability density.

### Task 4 — Optimize
Minimize a function.

### Task 5 — Integrate
Integrate numerically.

### Task 6 — Interpolate
Interpolate points.

### Task 7 — Choose
When use SciPy?
<!--/TASK-->

<!--HINT-->
### Hint 1
stats.describe.

### Hint 2
ttest.

### Hint 3
norm.pdf.

### Hint 4
minimize.

### Hint 5
quad.

### Hint 6
interp1d.

### Hint 7
Scientific.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from scipy import stats
data = [1.2, 2.1, 2.9, 3.4]
print(stats.describe(data))
```

### Solution 2
```python
print(stats.ttest_1samp(data, 2.0))
```

### Solution 3
```python
x = stats.norm.pdf(0, loc=0, scale=1)
print(x)
```

### Solution 4
```python
from scipy.optimize import minimize

def f(x):
    return (x[0] - 1) ** 2 + (x[1] + 2) ** 2

print(minimize(f, [0, 0]).x)   # [1, -2]
```

### Solution 5
```python
from scipy.integrate import quad
result, error = quad(lambda x: x ** 2, 0, 1)
# 0.333...
```

### Solution 6
```python
from scipy.interpolate import interp1d
f = interp1d([0, 1, 2], [0, 1, 4])
print(f(1.5))   # 2.5
```

### Solution 7
```text
Когда нужны готовые алгоритмы: статистика,
оптимизация, интегрирование, интерполяция
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SciPy?
- Scientific library
- Web
- GUI
- None
* Correct answer: Scientific library
Algorithms.

What is stats?
- Statistics module
- Data
- Plot
- None
* Correct answer: Statistics module
Tests.

What is describe?
- Summary
- Plot
- Test
- None
* Correct answer: Summary
Stats.

What is t-test?
- Mean comparison
- Plot
- Integral
- None
* Correct answer: Mean comparison
Significance.

What is minimize?
- Optimization
- Integration
- Stats
- None
* Correct answer: Optimization
Minimum.

What is quad?
- Numerical integral
- Derivative
- Test
- None
* Correct answer: Numerical integral
Area.

What is interp1d?
- Interpolation
- Extrapolation
- Stats
- None
* Correct answer: Interpolation
Function.

What is norm?
- Normal distribution
- Data
- Test
- None
* Correct answer: Normal distribution
PDF.

What is pdf?
- Density
- CDF
- Mean
- None
* Correct answer: Density
Value.

What is p-value?
- Significance
- Mean
- Variance
- None
* Correct answer: Significance
Test.

What is a result?
- Solution
- Data
- Error
- None
* Correct answer: Solution
Optimized.

What is the benefit?
- Ready-made math
- Writing from scratch
- Required
- None
* Correct answer: Ready-made math
Robust.
<!--/QUIZ-->
