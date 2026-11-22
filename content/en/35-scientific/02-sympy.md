---
title: Symbolic math with SymPy
summary: Symbols, equations, calculus.
order: 2
duration: 45 min
difficulty: advanced
tags: sympy
---

SymPy does algebra symbolically.

## Symbols

```python
from sympy import symbols, solve, diff, integrate, simplify

x = symbols("x")
```

## Solve

```python
print(solve(x ** 2 - 4, x))   # [-2, 2]
```

## Calculus

```python
print(diff(x ** 3, x))        # 3*x**2
print(integrate(x ** 2, x))   # x**3/3
```

## Simplify

```python
print(simplify((x + 1) * (x - 1)))   # x**2 - 1
```

## Lesson summary

SymPy = symbolic math in Python.

<!--TASK-->
### Task 1 — Symbols
Declare x.

### Task 2 — Solve
Solve a quadratic.

### Task 3 — Diff
Differentiate.

### Task 4 — Integrate
Integrate.

### Task 5 — Simplify
Simplify an expression.

### Task 6 — Expand
Expand.

### Task 7 — Limit
Compute a limit.
<!--/TASK-->

<!--HINT-->
### Hint 1
symbols.

### Hint 2
solve.

### Hint 3
diff.

### Hint 4
integrate.

### Hint 5
simplify.

### Hint 6
expand.

### Hint 7
limit.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
from sympy import symbols
x = symbols("x")
```

### Solution 2
```python
from sympy import solve
print(solve(x ** 2 - 4, x))   # [-2, 2]
```

### Solution 3
```python
print(diff(x ** 3, x))   # 3*x**2
```

### Solution 4
```python
print(integrate(x ** 2, x))   # x**3/3
```

### Solution 5
```python
print(simplify((x + 1) * (x - 1)))   # x**2 - 1
```

### Solution 6
```python
print(expand((x + 1) ** 2))   # x**2 + 2*x + 1
```

### Solution 7
```python
from sympy import limit, oo
print(limit(1 / x, x, oo))   # 0
```
<!--/SOLUTION-->

<!--QUIZ-->
What is SymPy?
- Symbolic math
- Numeric
- Plotting
- None
* Correct answer: Symbolic math
Symbols.

What is a symbol?
- Variable
- Number
- Function
- None
* Correct answer: Variable
x.

What is solve?
- Finds roots
- Integrates
- Plots
- None
* Correct answer: Finds roots
Equation.

What is diff?
- Derivative
- Integral
- Limit
- None
* Correct answer: Derivative
Calculus.

What is integrate?
- Integral
- Derivative
- Solve
- None
* Correct answer: Integral
Area.

What is simplify?
- Reduces
- Expands
- Solves
- None
* Correct answer: Reduces
Form.

What is expand?
- Opens brackets
- Simplifies
- Differentiates
- None
* Correct answer: Opens brackets
Product.

What is limit?
- Approaches value
- Solves
- Integrates
- None
* Correct answer: Approaches value
oo.

What is oo?
- Infinity
- Zero
- One
- None
* Correct answer: Infinity
Limit.

What is an expression?
- Math object
- Number
- Symbol
- None
* Correct answer: Math object
Formula.

What is exact?
- Symbolic result
- Decimal
- Approx
- None
* Correct answer: Symbolic result
x**2.

What is the benefit?
- Exact answers
- Numeric only
- Required
- None
* Correct answer: Exact answers
Algebra.
<!--/QUIZ-->
