---
title: Money in Python: decimal
summary: Exact decimal arithmetic, rounding rules and why float is risky for money.
order: 14
duration: 35 min
difficulty: beginner
tags: decimal, money, rounding, float
---

Floating point is impressive for science but dangerous for money: 0.1 + 0.2 == 0.3 is False. The `decimal` module solves this.

## Float problem

```python
print(0.1 + 0.2)   # 0.30000000000000004
```

## Decimal

```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
```

Always pass strings to Decimal, not floats.

## Rounding

```python
from decimal import Decimal, ROUND_HALF_UP
price = Decimal("19.995")
print(price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))   # 20.00
```

## Using in finance

- prices, totals, taxes → Decimal;
- store as strings or use Decimal in DB;
- avoid mixing Decimal and float.

## Lesson summary

We learned why float is risky for money, how to use Decimal and round correctly.

<!--TASK-->
### Task 1 — Float problem
Print 0.1 + 0.2 and show why it is not 0.3.

### Task 2 — Decimal basics
Compute Decimal("0.1") + Decimal("0.2") and print the exact result.

### Task 3 — From strings
Create Decimal("10.50") and Decimal("3.75"); print their sum.

### Task 4 — Rounding
Round Decimal("2.675") to 2 places using ROUND_HALF_UP. Print the result.

### Task 5 — Tax calculator
Write a function total_with_tax(price_str) returning Decimal price with 20% tax, rounded to 2 places.

### Task 6 — Compare
Write a function that compares sum of two floats to sum of two Decimals for 0.1+0.2.

### Task 7 — Receipt
Create a small receipt: two items with prices, compute subtotal, tax and total as Decimal; print all three.
<!--/TASK-->

<!--HINT-->
### Hint 1
Run print(0.1 + 0.2) to see the artifact.

### Hint 2
from decimal import Decimal.

### Hint 3
Decimal("...") from strings.

### Hint 4
quantize(Decimal("0.01"), rounding=ROUND_HALF_UP).

### Hint 5
Multiply by Decimal("1.20"), then quantize.

### Hint 6
Compare results with ==.

### Hint 7
Prices as Decimal strings; tax = subtotal * Decimal("0.20").
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
print(0.1 + 0.2)   # 0.30000000000000004
```
Binary float cannot represent 0.1 exactly.

### Solution 2
```python
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))   # 0.3
```

### Solution 3
```python
a = Decimal("10.50")
b = Decimal("3.75")
print(a + b)   # 14.25
```

### Solution 4
```python
from decimal import Decimal, ROUND_HALF_UP
x = Decimal("2.675")
print(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))   # 2.68
```

### Solution 5
```python
def total_with_tax(price_str):
    price = Decimal(price_str)
    return (price * Decimal("1.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

print(total_with_tax("100.00"))   # 120.00
```

### Solution 6
```python
print(0.1 + 0.2 == 0.3)                    # False
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True
```

### Solution 7
```python
item1 = Decimal("49.99")
item2 = Decimal("19.50")
subtotal = item1 + item2
tax = (subtotal * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
total = (subtotal + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(subtotal, tax, total)
```
<!--/SOLUTION-->

<!--QUIZ-->
Why is 0.1 + 0.2 not 0.3?
- Float representation is approximate
- Python is wrong
- Rounding by user
- It is a bug in print
* Correct answer: Float representation is approximate
Binary floats approximate decimals.

What does Decimal("0.1") do?
- Creates an exact decimal
- Creates a float
- Rounds
- Errors
* Correct answer: Creates an exact decimal
From the string.

Why pass strings to Decimal?
- To avoid float artifacts
- Faster
- Required
- Shorter
* Correct answer: To avoid float artifacts
Decimal(float) inherits the artifact.

What does quantize(Decimal("0.01")) do?
- Rounds to 2 decimal places
- Converts to float
- Truncates
- Nothing
* Correct answer: Rounds to 2 decimal places
For money.

What is ROUND_HALF_UP?
- Round half away from zero
- Round down
- Round up always
- Banker's rounding
* Correct answer: Round half away from zero
Standard for money.

What is Decimal("0.2") + Decimal("0.1")?
- Decimal("0.3")
- 0.30000000000000004
- Decimal("0.30")
- Error
* Correct answer: Decimal("0.3")
Exact result.

Should money use float?
- No
- Yes
- Sometimes
- Only small
* Correct answer: No
Use Decimal.

What is Decimal("1.20") * Decimal("100.00")?
- Decimal("120.0000")
- 120
- 120.0
- Error
* Correct answer: Decimal("120.0000")
Decimal arithmetic preserves precision.

How to round a Decimal?
- .quantize(...)
- round(...)
- int(...)
- .format(...)
* Correct answer: .quantize(...)
Using exponent and rounding.

Which is a safe way to create 0.3?
- Decimal("0.3")
- 0.3
- float("0.3")
- 3/10
* Correct answer: Decimal("0.3")
Exact string.

What does Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) give?
- 2.68
- 2.67
- 2.675
- 3
* Correct answer: 2.68
Half rounded up.

When to use Decimal?
- Financial calculations
- Graphics
- Loops
- Network
* Correct answer: Financial calculations
Where exactness matters.
<!--/QUIZ-->
