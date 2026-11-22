---
title: Mathematical optimization
summary: scipy.optimize: unconstrained and constrained minimization, linear programming, least squares, and global search.
order: 6
duration: 40 min
difficulty: advanced
tags: optimization, scipy.optimize, linprog
---

Optimization is the science of choosing the best among feasible solutions: fewer costs, more profit, a more accurate model. In Python, `scipy.optimize` handles it. We already saw `minimize` in the first lesson; now we will dig deeper into the toolkit: methods, constraints, linear programming, curve fitting, and global search.

## Unconstrained minimization

The function `minimize` solves the problem: find a vector x that minimizes f(x). The simplest example — a quadratic function:

```python
import numpy as np
from scipy.optimize import minimize

def f(z):
    return (z[0] - 3)**2 + (z[1] + 1)**2

res = minimize(f, [0.0, 0.0])
print(res.x, res.fun)   # [3. -1.] 0.0
```

`res.x` is the point of the minimum, `res.fun` is the function value. The default method is BFGS. For non-smooth functions use `method="Nelder-Mead"` — it does not require derivatives.

## Constraints: bounds

Often variables are restricted, for example a price cannot be negative. The `bounds` parameter sets box constraints:

```python
res = minimize(lambda z: (z[0] - 1)**2, [5.0],
               bounds=[(0, 10)])
print(res.x)   # [1.]
```

If the minimum lies outside the feasible region, the solution "sticks" to the boundary:

```python
res = minimize(lambda z: (z[0] - 20)**2, [5.0],
               bounds=[(0, 10)])
print(res.x)   # [10.]
```

## Equality and inequality constraints

More general constraints go through the `constraints` parameter. For example, a problem with the equality constraint x + y = 5:

```python
res = minimize(lambda z: z[0]**2 + z[1]**2, [1.0, 1.0],
               constraints={"type": "eq",
                            "fun": lambda z: z[0] + z[1] - 5})
print(res.x)   # [2.5 2.5]
```

These problems are solved by the SLSQP method (`method="SLSQP"`).

## Linear programming: linprog

When both the objective function and the constraints are linear, the problem is solved fast and guaranteed — this is linear programming. `linprog` minimizes cᵀx under inequalities A_ub x ≤ b_ub and bounds:

```python
from scipy.optimize import linprog

c = [-2, -3]                      # maximize 2x + 3y
A_ub = [[1, 1], [2, 1]]
b_ub = [4, 5]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
print(res.x, res.fun)   # [0. 4.] -12.0
```

The optimum is x = 0, y = 4, objective 2·0 + 3·4 = 12 (linprog minimizes −2x − 3y, so `res.fun` = −12).

## Curve fitting: curve_fit

A common task is fitting model parameters to data. `curve_fit` minimizes the sum of squared deviations:

```python
from scipy.optimize import curve_fit

rng = np.random.default_rng(1)
t = np.linspace(0, 5, 100)
y_true = 5 * np.exp(-0.5 * t)
y = y_true + rng.normal(0, 0.1, 100)

def model(t, a, k):
    return a * np.exp(-k * t)

popt, pcov = curve_fit(model, t, y, p0=[1, 1])
print(popt)   # ≈ [5. 0.5]
```

`popt` is the optimal parameters, `pcov` is the covariance matrix (standard errors are taken from it). `p0` is the initial guess.

## Global optimization

Local methods can get stuck in a local minimum. For multi-extremal functions there are global methods — `dual_annealing`, `basinhopping`, `differential_evolution`:

```python
from scipy.optimize import dual_annealing

def bumpy(z):
    return np.sin(3 * z[0]) + (z[0] - 1)**2

res = dual_annealing(bumpy, bounds=[(-5, 5)])
print(res.x, res.fun)
```

`dual_annealing` takes `bounds` — just a list of ranges. It "sweeps" the whole region, which is more expensive but more reliable.

## How to choose a tool

- smooth function, no constraints → `minimize` (BFGS);
- non-smooth → `Nelder-Mead`;
- box constraints → `bounds`;
- complex constraints → `constraints` + SLSQP;
- everything is linear → `linprog`;
- parameter fitting → `curve_fit` or `least_squares`;
- many local minima → `dual_annealing`.

## Why this matters

Optimization is a cross-cutting tool of data science. Training models is minimizing a loss function; hyperparameter tuning is optimizing a metric; production and logistics planning is linear programming; sensor calibration is least squares. Even neural networks are trained by gradient descent — the same family of methods that BFGS belongs to. Understanding the limitations and capabilities of `scipy.optimize` lets you choose the right tool: for example, don't try to solve a non-convex problem with a local method, or don't use slow global search where a fast gradient descent is enough. As in signal analysis, half the success is in stating the problem correctly, not in the library call itself.

Now let's apply this in the tasks.

<!--TASK-->
### Task 1
Minimize the function (x − 3)² + (y + 1)² via `scipy.optimize.minimize`, starting from [0, 0]. Print `res.x` and `res.fun`. Run the program: the minimum point should be [3, −1], the value — 0.0.

### Task 2
Solve two constrained problems. First: minimize (x − 1)² with the constraint x ∈ [0, 10], starting from 5. Second: minimize (x + 3)² with the constraint x ∈ [−5, −2], starting from −4. Print the solutions of both problems in turn. Expected: 1.0 and −3.0.

### Task 3
Solve via `linprog` the problem: maximize 2x + 3y under the constraints x + y ≤ 4, 2x + y ≤ 5, x ≥ 0, y ≥ 0. To do this pass `c = [-2, -3]`, `A_ub = [[1, 1], [2, 1]]`, `b_ub = [4, 5]`, bounds from zero to infinity. Print `res.x` and `res.fun`. Expected: x = 0, y = 4, fun = −12.

### Task 4
Create a file `optim_lab.py` with a function `fit_exponential(t, y)` that fits the model `a * exp(-k * t)` via `curve_fit` and returns a tuple `(a, k)` (from `popt`). Then create `test_optim_lab.py`: generate data y = 5·e^{−0.5t} + noise (seed 1, σ = 0.1, t from linspace(0, 5, 100)) and check that the recovered a and k differ from 5 and 0.5 by less than 0.1. Run pytest.

### Task 5
In `test_optim_lab.py` add two more tests. First: `minimize` on the function (x − 3)² + (y + 1)² finds the minimum to 1e-4 precision in both coordinates. Second: `dual_annealing` on the function sin(3x) + (x − 1)² within [−5, 5] gives a function value less than 0.1 (the global minimum is close to zero). Run pytest — all three tests should pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
The objective function takes a vector: `lambda z: (z[0] - 3)**2 + (z[1] + 1)**2`. The result is `res.x` (point) and `res.fun` (value).

### Hint 2
The `bounds` parameter is a list of tuples, one per variable: `bounds=[(0, 10)]`. If the minimum is outside the range, the solution lands on the boundary: in the second problem it is x = −2.

### Hint 3
Remember: linprog minimizes, so to maximize 2x + 3y take c = [−2, −3]. `res.fun` will be negative (−12). Constraints like x ≥ 0 are set via `bounds=[(0, None), (0, None)]`.

### Hint 4
`curve_fit(model, t, y, p0=[1, 1])` returns `(popt, pcov)` — unpack both. In the test compare `abs(a - 5) < 0.1` and `abs(k - 0.5) < 0.1`. Import `fit_exponential` from `optim_lab`.

### Hint 5
For the first test import `minimize` and check `abs(res.x[0] - 3) < 1e-4`, `abs(res.x[1] + 1) < 1e-4`. For the second — `dual_annealing` returns `res.fun`; the global minimum of the function is close to 0, so check `< 0.1`. Don't forget to pass `bounds=[(-5, 5)]`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import numpy as np
from scipy.optimize import minimize

def f(z):
    return (z[0] - 3)**2 + (z[1] + 1)**2

res = minimize(f, [0.0, 0.0])
print(res.x)
print(res.fun)
```

Result:

```
[ 3. -1.]
0.0
```

What's happening here? A quadratic function is a "bowl" with a minimum at (3, −1). BFGS moves along the gradient and finds the exact solution in a few iterations: the components of `res.x` are 3 and −1, and `res.fun` is 0.0 (the function vanishes). This is a benchmark for checking any optimizer: for convex functions the result is practically exact.

### Solution 2
Solution:

```python
from scipy.optimize import minimize

res1 = minimize(lambda z: (z[0] - 1)**2, [5.0], bounds=[(0, 10)])
res2 = minimize(lambda z: (z[0] + 3)**2, [-4.0], bounds=[(-5, -2)])
print(res1.x)
print(res2.x)
```

Result:

```
[1.]
[-2.]
```

What's happening here? In the first problem the minimum of (x − 1)² is at 1, and it lies inside the feasible range [0, 10], so the solution is 1. In the second the minimum of (x + 3)² is at −3, but the range [−5, −2] does not contain it: the nearest feasible point is −2. The method correctly "places" the solution on the boundary. This is a typical effect of constraints — the optimum lies on the boundary of the feasible set.

### Solution 3
Solution:

```python
from scipy.optimize import linprog

c = [-2, -3]
A_ub = [[1, 1], [2, 1]]
b_ub = [4, 5]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
print(res.x)
print(res.fun)
```

Result:

```
[0. 4.]
-12.0
```

What's happening here? The set of feasible points is a polygon with vertices (0,0), (2.5,0), (1,3), (0,4). In linear programming the optimum is always achieved at a vertex. Let's check: 2·0+3·4=12 at (0,4), 2·1+3·3=11 at (1,3), 2·2.5+3·0=5. The maximum is 12 at (0,4). Since linprog minimizes, fun = −12.

### Solution 4
File `optim_lab.py`:

```python
import numpy as np
from scipy.optimize import curve_fit

def fit_exponential(t, y):
    model = lambda t, a, k: a * np.exp(-k * t)
    popt, pcov = curve_fit(model, t, y, p0=[1, 1])
    return popt[0], popt[1]
```

File `test_optim_lab.py`:

```python
import numpy as np
from optim_lab import fit_exponential

def test_fit_exponential():
    rng = np.random.default_rng(1)
    t = np.linspace(0, 5, 100)
    y = 5 * np.exp(-0.5 * t) + rng.normal(0, 0.1, 100)
    a, k = fit_exponential(t, y)
    assert abs(a - 5) < 0.1
    assert abs(k - 0.5) < 0.1
```

Result: `1 passed`. What's happening here? `curve_fit` minimizes the sum of squared deviations of the model from the data. The true parameters are a = 5, k = 0.5; with small noise the estimates differ from them by fractions of a percent. The initial guess `p0=[1, 1]` is just a starting point; for smooth models a bad start does not hurt.

### Solution 5
Extend `test_optim_lab.py`:

```python
from scipy.optimize import minimize, dual_annealing

def test_minimize_quadratic():
    res = minimize(lambda z: (z[0] - 3)**2 + (z[1] + 1)**2, [0.0, 0.0])
    assert abs(res.x[0] - 3) < 1e-4
    assert abs(res.x[1] + 1) < 1e-4

def test_global_optimization():
    res = dual_annealing(lambda z: np.sin(3 * z[0]) + (z[0] - 1)**2,
                         bounds=[(-5, 5)])
    assert res.fun < 0.1
```

Result: `3 passed`. What's happening here? The first test checks the accuracy of local minimization on a smooth convex function. The second tests global optimization: the function sin(3x) + (x − 1)² has many local minima, and a local method can get stuck in the wrong one. `dual_annealing` sweeps the whole range [−5, 5] and finds the global minimum, close to zero. The `fun < 0.1` check filters out "getting stuck" in bad local minima.
<!--/SOLUTION-->

<!--QUIZ-->
Which method does scipy.optimize.minimize use by default?
- BFGS
- Nelder-Mead
- SLSQP
- L-BFGS-B
* Correct answer: BFGS
BFGS is a quasi-Newton method for smooth unconstrained problems.

Which method suits non-smooth functions?
- Nelder-Mead
- BFGS
- linprog
- curve_fit
* Correct answer: Nelder-Mead
Nelder-Mead (simplex method) does not use derivatives.

What is the bounds parameter in minimize for?
- For box constraints on variables
- For setting the starting point
- For choosing the method
- For limiting the number of iterations
* Correct answer: For box constraints on variables
bounds sets the feasible range of each variable.

What happens if the minimum lies outside bounds?
- The solution lands on the boundary of the range
- The function returns an error
- The minimum is ignored
- The process does not finish
* Correct answer: The solution lands on the boundary of the range
The optimal point under constraints may lie on the boundary of the feasible set.

What does linprog solve?
- Linear programming
- Nonlinear minimization
- Curve fitting
- Global optimization
* Correct answer: Linear programming
linprog solves problems with a linear objective and linear constraints.

How to maximize 2x + 3y via linprog?
- Pass c = [-2, -3]
- Pass c = [2, 3]
- Pass c = [0, 0]
- Multiply everything by 2
* Correct answer: Pass c = [-2, -3]
linprog minimizes, so the signs of the objective are flipped.

What does curve_fit return?
- A tuple (popt, pcov)
- Only popt
- The number of iterations
- A list of residuals
* Correct answer: A tuple (popt, pcov)
popt is the optimal parameters, pcov is the covariance matrix.

Why is p0 needed in curve_fit?
- As an initial guess for the parameters
- For constraints
- For choosing the method
- For accuracy
* Correct answer: As an initial guess for the parameters
p0 is the starting point for searching the optimal parameters.

Which method suits multi-extremal functions?
- dual_annealing
- BFGS
- linprog
- minimize with method="BFGS"
* Correct answer: dual_annealing
Global methods sweep the whole region without getting stuck in local minima.

What is stored in res.fun after minimize?
- The objective function value at the minimum point
- The minimum point
- The gradient
- The number of iterations
* Correct answer: The objective function value at the minimum point
res.fun is the minimum value of the function, res.x is the point where it is attained.
<!--/QUIZ-->
