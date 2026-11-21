---
title: Magic methods in depth
summary: Operator overloading, comparisons, containers, callables, copying and attribute control.
order: 16
duration: 60 min
difficulty: advanced
tags: magic methods, dunder, operators, overloading
---

Dunder methods make classes act like built-in types: addition, comparison, indexing, calling, copying.

## Arithmetic

```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __add__(self, other):
        return Money(self.amount + other.amount)
    def __radd__(self, other):
        return self.__add__(other)
    def __str__(self):
        return f"{self.amount} руб."
```

## Comparisons

```python
class Vector:
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))
```

## Containers

```python
def __getitem__(self, i):
    return self.items[i]

def __len__(self):
    return len(self.items)
```

## Callable

```python
class Counter:
    def __call__(self, x):
        return x * 2
```

## Copying

```python
def __copy__(self):
    return My(self.x, self.y)
```

## Summary

Dunder methods integrate classes with operators, containers, calls, and copy.

<!--TASK-->
### Task 1 — __add__
Implement __add__ for Vector; test v1+v2.

### Task 2 — __radd__
Implement __radd__ so sum([v1, v2]) works.

### Task 3 — __eq__/__lt__
Implement both and sort a list of vectors.

### Task 4 — __hash__
Implement onhash__ for Vector and use it in a set.

### Task 5 — __getitem__/__len__
Implement for a custom list wrapper.

### Task 6 — __call__
Create a Callable class that counts calls.

### Task 7 — __copy__/__deepcopy__
Implement copying and verify independence.
<!--/TASK-->

<!--HINT-->
### Hint 1
return Vector(self.x+other.x, ...).

### Hint 2
__radd__ for right operands.

### Hint 3
__lt__ via tuple comparison.

### Hint 4
hash((x, y)).

### Hint 5
delegate to inner list.

### Hint 6
self.count += 1; return func(...).

### Hint 7
copy module; __copy__ returns a new instance.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

print(Vector(1, 2) + Vector(3, 4))   # Vector(4, 6)
```

### Solution 2
```python
def __radd__(self, other):
    return self.__add__(other)

# sum([Vector(1,1), Vector(2,2)]) works: starts with 0 + first
```
For sum to work, add support for int 0.

### Solution 3
```python
class Vector:
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

vecs = [Vector(3,1), Vector(1,2)]
print(sorted(vecs))
```

### Solution 4
```python
def __hash__(self):
    return hash((self.x, self.y))

s = {Vector(1,1), Vector(1,1)}
print(len(s))   # 1
```

### Solution 5
```python
class MyList:
    def __init__(self, items):
        self.items = items
    def __getitem__(self, i):
        return self.items[i]
    def __len__(self):
        return len(self.items)

m = MyList([10,20,30])
print(m[1], len(m))   # 20 3
```

### Solution 6
```python
class Assign:
    def __init__(self):
        self.calls = 0
    def __call__(self, x):
        self.calls += 1
        return x * 2

a = Assign()
print(a(5))   # 10
print(a.calls)   # 1
```

### Solution 7
```python
import copy

class Item:
    def __init__(self, x):
        self.x = x
    def __copy__(self):
        return Item(self.x)
    def __deepcopy__(self, memo):
        return Item(self.x)

i = Item(5)
j = copy.deepcopy(i)
j.x = 10
print(i.x)   # 5
```
<!--/SOLUTION-->

<!--QUIZ-->
What does __add__ overload?
- The + operator
- - operator
- *
- /
* Correct answer: The + operator
Left operand method.

What does __radd__ handle?
- Right operand addition
- Left only
- Subtraction
- None
* Correct answer: Right operand addition
When left doesn't support.

What does __eq__ define?
- Equality
- Ordering
- Hashing
- Copy
* Correct answer: Equality
== operator.

What does __lt__ define?
- Less than
- Equal
- Greater
- Sum
* Correct answer: Less than
Sorting uses it.

Why implement __hash__ with __eq__?
- To stay hashable
- To speed
- To print
- Nothing
* Correct answer: To stay hashable
Sets/dicts keys.

What does __getitem__ enable?
- obj[index]
- len(obj)
- obj()
- str(obj)
* Correct answer: obj[index]
Indexing.

What does __len__ enable?
- len(obj)
- obj[index]
- obj()
- iter(obj)
* Correct answer: len(obj)
Must return int.

What does __call__ enable?
- Calling an instance
- Adding
- Comparing
- Copying
* Correct answer: Calling an instance
obj(args).

What does __copy__ define?
- Shallow copy behavior
- Deep copy
- Delete
- Compare
* Correct answer: Shallow copy behavior
Used by copy.copy.

What does __deepcopy__ define?
- Deep copy behavior
- Shallow
- Compare
- Print
* Correct answer: Deep copy behavior
Used by copy.deepcopy.

What is __repr__ for?
- Developer representation
- User string
- Size
- Hash
* Correct answer: Developer representation
Unambiguous.

What happens without __hash__ when __eq__ defined?
- Object becomes unhashable
- Still hashable
- Error at import
- Nothing
* Correct answer: Object becomes unhashable
Python sets __hash__ to None.
<!--/QUIZ-->
