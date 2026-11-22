---
title: SciPy: integrals, interpolation, optimization
summary: An introduction to SciPy: numerical integration, solving differential equations, data interpolation, and finding optima.
order: 1
duration: 40 min
difficulty: advanced
tags: scipy, integrals, interpolation, optimization
---

Scientific computing in Python rarely goes without the SciPy library. It is built on top of NumPy and provides ready-made algorithms for integration, solving equations, interpolation, optimization, signal processing, and statistics. In this lesson we will get acquainted with four main submodules: `scipy.integrate`, `scipy.interpolate`, `scipy.optimize`, and `scipy.signal` (partially). You can install the library with the command `pip install scipy`.

## What is SciPy

SciPy is not a single thing but a collection of submodules, each solving its own class of problems:

- `scipy.integrate` — numerical integrals and ordinary differential equations (ODEs);
- `scipy.interpolate` — building functions from tabular data;
- `scipy.optimize` — finding minima, roots, and fitting parameters;
- `scipy.stats` — distributions and statistical tests (we will cover this in the next lesson);
- `scipy.signal` — filters, spectra, convolutions.

All functions expect NumPy arrays as input. This is important: SciPy does not work with Python lists as efficiently, so get used to converting data to `np.array` right away.

## Numerical integration: scipy.integrate

Not all integrals can be taken analytically. For such cases there are numerical methods. The function `quad` computes a definite integral using adaptive quadrature:

```python
import numpy as np
from scipy.integrate import quad

f = lambda x: np.exp(-x**2)
value, error = quad(f, 0, 1)
print(value, error)
```

`quad` returns a tuple of two numbers: the integral value itself and an estimate of the absolute error. Here we compute ∫₀¹ e^{−x²} dx ≈ 0.7468. Note: the integral of a Gaussian function cannot be expressed in terms of elementary functions — yet numerically it is computed in fractions of a second.

`quad` also works with infinite limits — this will come in handy in problems:

```python
value, error = quad(f, 0, np.inf)
print(value)  # ≈ 0.8862 = √π / 2
```

And if you have not a function but a table of values (an array of points), use `simpson` — integration by Simpson's rule:

```python
from scipy.integrate import simpson

x = np.linspace(0, np.pi, 100)
y = np.sin(x)
print(simpson(y, x))  # ≈ 2.0
```

## Ordinary differential equations: solve_ivp

Many problems in physics and biology reduce to ODEs: "how does a quantity change over time." SciPy solves the initial value problem via `solve_ivp`. Let's solve y′ = −y with the initial condition y(0) = 1:

```python
from scipy.integrate import solve_ivp

def rhs(t, y):
    return -y

sol = solve_ivp(rhs, (0, 1), [1.0], t_eval=[0, 1])
print(sol.y[0][-1])  # ≈ 0.3679 = e⁻¹
```

Here `(0, 1)` is the time interval, `[1.0]` is the initial values (a list, because there may be several equations), and `t_eval` is the points at which we want to see the solution. The analytical solution is y(t) = e^{−t}, so y(1) = e⁻¹ ≈ 0.3679. The default method is RK45 (Runge–Kutta 4th–5th order). The array `sol.y` has shape `(number of equations, number of points)`.

## Interpolation: scipy.interpolate

You have experimental points, but you need a function that passes through them so you can compute values between them. Linear interpolation gives polylines, while cubic splines give smooth curves. The class `CubicSpline` builds a piecewise cubic polynomial that is continuous together with its second derivative:

```python
from scipy.interpolate import CubicSpline

x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])
cs = CubicSpline(x, y)
print(cs(2.5))  # close to 6.25
```

The spline is guaranteed to pass through all knots: `cs(x[i]) == y[i]`. This is convenient to check in tests. There is also the function `interp1d` with a `kind` parameter: `"linear"`, `"cubic"`, and others.

## Optimization: scipy.optimize

Finding the minimum of a function is one of the most common tasks: fitting model parameters, portfolio balancing, training algorithms. The universal `minimize` function solves the unconstrained optimization problem:

```python
from scipy.optimize import minimize

def g(z):
    return (z[0] - 2)**2 + 3

res = minimize(g, [0.0])
print(res.x, res.fun)  # [2.] 3.0
```

`res.x` is the point of the minimum, `res.fun` is the function value there, `res.success` is a success flag. By default, the BFGS method is chosen — a quasi-Newton method for smooth functions.

Roots of equations are found separately — via `root` or `fsolve`:

```python
from scipy.optimize import root

res = root(lambda z: z**3 - 8, [1.0])
print(res.x)  # [2.]
```

## Where this is used

Integration — in computing areas, probabilities, and physical quantities; `solve_ivp` — in modeling dynamics (populations, radioactive decay, orbits); interpolation — when working with sparse sensor measurements; optimization — everywhere, from machine learning to engineering structures. This is the foundation on which higher-level libraries stand — statsmodels, scikit-learn.

## On the limits of applicability

Numerical methods are not a panacea — each has correctness conditions. `quad` works great with smooth functions but does not like strong singularities (for example, discontinuities): in such cases it makes sense to split the integral into segments. The `CubicSpline` spline interpolates perfectly between knots, but predictions **outside** the data range (extrapolation) are often meaningless: the spline behaves like a cubic polynomial and can shoot sharply up or down. The optimizer `minimize` finds a local minimum — from a different starting point it may arrive at a different "pit", so the starting point should be chosen sensibly, and for multi-extremal functions use global methods (we will cover them in the last lesson of the module). Understanding a tool's limitations is no less important than knowing how to call its API.

Now let's reinforce everything in practice.

<!--TASK-->
### Task 1
Write a program that uses `scipy.integrate.quad` to compute the integral ∫₀^π sin(x) dx and prints two numbers separated by a space: the integral value and the error estimate. The exact answer is 2.0, so the first number should be very close to 2. Run the program and make sure the integral value differs from 2 by less than 1e-8.

### Task 2
Create a file `sci_integrals.py` with a function `improper_integral()` that computes the improper integral ∫₀^∞ e^{−x²} dx via `quad` and returns a tuple `(value, error)`. Write a pytest test file `test_sci_integrals.py` with two tests: the first checks that `value` differs from `sqrt(pi) / 2` by less than 1e-6; the second — that `error` is less than 1e-6. Run `python -m pytest test_sci_integrals.py -v` and get two green tests.

### Task 3
Write a function `solve_decay()` in the file `sci_ode.py`: it solves y′ = −y via `solve_ivp` with the initial condition y(0) = 1 on the interval [0, 1] and returns the value y(1) (the last element of `sol.y[0]`). Then create `test_sci_ode.py`: the test checks that the result differs from `np.exp(-1)` by less than 1e-2. Run pytest and make sure the test passes. Hint: `np.exp(-1)` ≈ 0.3679.

### Task 4
Build a cubic spline `CubicSpline` through the points x = [0, 1, 2, 3, 4], y = [0, 1, 4, 9, 16] (these are points of the parabola y = x²). Print one line with the spline values at all nodes x (they must match y), then, separated by a space, the spline value at the point 2.5. Run the program and check that the first five numbers exactly repeat the original y: 0, 1, 4, 9, 16.

### Task 5
In the file `sci_optim.py` write a function `minimize_quadratic()` that minimizes the function (x − 2)² + 3 via `scipy.optimize.minimize`, starting from the point [0.0], and returns a tuple `(res.x[0], res.fun)`. Create `test_sci_optim.py`: the test checks that the minimum point differs from 2 by less than 1e-4 and the function value differs from 3 by less than 1e-4. Run pytest — both assertions should pass.
<!--/TASK-->

<!--HINT-->
### Hint 1
`quad` returns a tuple: `value, error = quad(np.sin, 0, np.pi)`. Pass both numbers to `print` separated by a comma — they will be printed separated by a space.

### Hint 2
An improper integral is obtained by passing `np.inf` as the upper limit. In the test use `from math import sqrt, pi` and compare via `abs(value - sqrt(pi) / 2) < 1e-6`. Don't forget that `improper_integral()` returns a tuple — unpack it.

### Hint 3
Pay attention to the shape of `sol.y`: it is an array of size `(number of equations, number of points)`. We have one equation, so the solution is `sol.y[0]`, and the last point is index -1: `sol.y[0][-1]`. In the test compare with `np.exp(-1)`.

### Hint 4
`CubicSpline(x, y)` is a callable object: `cs(x)` returns an array of values. Pass the whole array x to `cs` — you will get an array of five values. Then compute `cs(2.5)` separately.

### Hint 5
The function `minimize` takes an objective function and a starting point: `minimize(g, [0.0])`. The result is an object with fields `x`, `fun`, `success`. Unpack the needed values into a tuple and compare in the test with a tolerance of 1e-4.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import numpy as np
from scipy.integrate import quad

value, error = quad(np.sin, 0, np.pi)
print(value, error)
```

Run:

```bash
python integral_sin.py
```

Result:

```
2.0 2.220446049250313e-14
```

What's happening here? `quad` numerically integrates sin(x) from 0 to π. The integral of sine over a half-period is exactly 2, and the adaptive algorithm achieves accuracy down to machine precision: the error estimate is about 2e-14. Note: instead of a lambda function you can pass `np.sin` itself — it is an ordinary function taking a number and returning a number.

### Solution 2
File `sci_integrals.py`:

```python
import numpy as np
from scipy.integrate import quad

def improper_integral():
    value, error = quad(lambda x: np.exp(-x**2), 0, np.inf)
    return value, error
```

File `test_sci_integrals.py`:

```python
from math import pi, sqrt
from sci_integrals import improper_integral

def test_value_close_to_sqrt_pi_over_two():
    value, _ = improper_integral()
    assert abs(value - sqrt(pi) / 2) < 1e-6

def test_error_estimate_small():
    _, error = improper_integral()
    assert error < 1e-6
```

pytest result: `2 passed`. What's happening here? The integral of e^{−x²} over the whole line is √π, and over the half-line [0, ∞) it is exactly half: √π/2. `quad` handles the infinite limit by replacing it with a suitable finite one. The first test checks the result itself, the second — that the numerical error is indeed small.

### Solution 3
File `sci_ode.py`:

```python
import numpy as np
from scipy.integrate import solve_ivp

def solve_decay():
    sol = solve_ivp(lambda t, y: -y, (0, 1), [1.0], t_eval=[0, 1])
    return sol.y[0][-1]
```

File `test_sci_ode.py`:

```python
import numpy as np
from sci_ode import solve_decay

def test_decay_value():
    assert abs(solve_decay() - np.exp(-1)) < 1e-2
```

Result: `1 passed`. What's happening here? `solve_ivp` integrates y′ = −y from t = 0 to t = 1 with a step it chooses itself. The analytical solution is y(t) = e^{−t}, so y(1) = e⁻¹ ≈ 0.3679. The RK45 numerical method gives accuracy much better than 1e-2, so the test passes with room to spare.

### Solution 4
Solution:

```python
import numpy as np
from scipy.interpolate import CubicSpline

x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])
cs = CubicSpline(x, y)

print(cs(x), cs(2.5))
```

Result:

```
[ 0.  1.  4.  9. 16.] 6.25
```

What's happening here? `CubicSpline` builds a piecewise cubic polynomial that passes through every knot. Therefore `cs(x)` exactly reproduces the original values: 0, 1, 4, 9, 16. At the point 2.5 the spline gives exactly 6.25 — just like the real parabola y = x²: for quadratic data, a cubic spline reproduces it exactly. This is how the interpolation property is verified: the function is defined at any point of the segment, and at the knots the values coincide with the data.

### Solution 5
File `sci_optim.py`:

```python
from scipy.optimize import minimize

def minimize_quadratic():
    res = minimize(lambda z: (z[0] - 2)**2 + 3, [0.0])
    return res.x[0], res.fun
```

File `test_sci_optim.py`:

```python
from sci_optim import minimize_quadratic

def test_minimum_point_and_value():
    x_min, fun_min = minimize_quadratic()
    assert abs(x_min - 2) < 1e-4
    assert abs(fun_min - 3) < 1e-4
```

Result: `1 passed`. What's happening here? The function (x − 2)² + 3 is a parabola with a minimum at x = 2, where it equals 3. BFGS finds the minimum to machine precision. Note: `minimize` minimizes over all components of the vector, so we pass `z[0]` — the only coordinate.
<!--/SOLUTION-->

<!--QUIZ-->
Which SciPy submodule is responsible for numerical integration?
- scipy.integrate
- scipy.interpolate
- scipy.optimize
- scipy.signal
* Correct answer: scipy.integrate
It is in scipy.integrate that the functions quad, simpson, and solve_ivp live.

What does the quad function return?
- Only the integral value
- A tuple (value, error estimate)
- An array of points
- Nothing
* Correct answer: A tuple (value, error estimate)
quad returns two numbers: the integral itself and an estimate of the absolute error.

Which method does solve_ivp use by default?
- RK45
- Euler
- Trapezoid
- Simpson
* Correct answer: RK45
By default solve_ivp uses the explicit Runge–Kutta method of 4th–5th order.

What shape does the sol.y array of solve_ivp have?
- (number of points, number of equations)
- (number of equations, number of points)
- (number of points,)
- (number of equations,)
* Correct answer: (number of equations, number of points)
The first axis is equations, the second is time points, so the solution of a single equation is taken as sol.y[0].

What property does the cubic spline CubicSpline have?
- Passes exactly through all interpolation knots
- Minimizes the sum of squared deviations
- Is given by a single formula over the whole segment
- Is always a straight line
* Correct answer: Passes exactly through all interpolation knots
Unlike regression, interpolation requires exact coincidence at the knots.

What does scipy.optimize.minimize return in the res.x field?
- The function value at the minimum point
- The minimum point
- The number of iterations
- The gradient at the minimum
* Correct answer: The minimum point
res.x is the coordinates of the minimum point, and res.fun is the function value there.

Which method does minimize use by default for smooth functions?
- BFGS
- Nelder-Mead
- Simplex
- SLSQP
* Correct answer: BFGS
BFGS is a quasi-Newton method, the standard choice for smooth unconstrained problems.

Can quad use an infinite integration limit?
- Yes, for example np.inf
- No, only finite numbers
- Only 0
- Only for polynomials
* Correct answer: Yes, for example np.inf
quad correctly handles improper integrals with infinite limits.

What is the simpson function for?
- For integrating tabular data
- For solving equations
- For interpolation
- For signal filtering
* Correct answer: For integrating tabular data
simpson takes arrays x and y and computes the integral by Simpson's rule.

Which SciPy function is suitable for finding a root of an equation?
- root or fsolve
- quad
- minimize
- CubicSpline
* Correct answer: root or fsolve
root and fsolve find zeros of functions; quad integrates, and minimize minimizes.
<!--/QUIZ-->
