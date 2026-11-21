---
title: Magic methods and property
summary: __str__, __repr__, __eq__, __len__, __getitem__, property and decorators.
order: 3
duration: 35 min
difficulty: intermediate
tags: magic methods, property, dunder, decorators
---

Magic (dunder) methods customize how objects behave with built-in operations.

## __str__ and __repr__

```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __str__(self):
        return f"{self.amount} руб."
    def __repr__(self):
        return f"Money({self.amount})"
```

## __eq__

```python
def __eq__(self, other):
    return self.amount == other.amount
```

## __len__ and __getitem__

```python
class Box:
    def __init__(self, items):
        self.items = items
    def __len__(self):
        return len(self.items)
    def __getitem__(self, i):
        return self.items[i]
```

## property

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    @property
    def celsius(self):
        return self._celsius
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Too cold")
        self._celsius = value
```

## Lesson summary

Magic methods integrate classes with Python syntax; property adds controlled access.

<!--TASK-->
### Task 1 — __str__
Create Book(title, author) with __str__ returning f"«title» — author". Print it.

### Task 2 — __repr__
Add __repr__ returning f"Book({title!r}, {author!r})". Print repr(book).

### Task 3 — __eq__
For two Book objects with the same title and author, compare with == → True.

### Task 4 — __len__
Create class Library with books list; implement __len__ and test len(library).

### Task 5 — __getitem__
Make Library support library[0] via __getitem__.

### Task 6 — property getter/setter
Create class Celsius with _value and property value (get/set with validation ≥ -273.15).

### Task 7 — __add__
Create class Vector(x, y) with __add__ returning a new Vector; test addition.
<!--/TASK-->

<!--HINT-->
### Hint 1
__str__ returns a human-readable string.

### Hint 2
__repr__ returns an unambiguous representation.

### Hint 3
__eq__ compares fields and returns bool.

### Hint 4
def __len__(self): return len(self.items).

### Hint 5
def __getitem__(self, index): return self.items[index].

### Hint 6
@property + @value.setter with validation.

### Hint 7
__add__ returns Vector(self.x+other.x, ...).
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    def __str__(self):
        return f"«{self.title}» — {self.author}"

print(Book("Python", "Anna"))   # «Python» — Anna
```

### Solution 2
```python
class Book:
    def __repr__(self):
        return f"Book({self.title!r}, {self.author!r})"

print(repr(Book("Python", "Anna")))   # Book('Python', 'Anna')
```

### Solution 3
```python
class Book:
    def __eq__(self, other):
        return (self.title, self.author) == (other.title, other.author)

b1 = Book("Python", "Anna")
b2 = Book("Python", "Anna")
print(b1 == b2)   # True
```

### Solution 4
```python
class Library:
    def __init__(self, books):
        self.books = books
    def __len__(self):
        return len(self.books)

lib = Library([Book("A", "1"), Book("B", "2")])
print(len(lib))   # 2
```

### Solution 5
```python
class Library:
    def __getitem__(self, index):
        return self.books[index]

print(lib[0].title)
```

### Solution 6
```python
class Celsius:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v < -273.15:
            raise ValueError("Too cold")
        self._value = v

c = Celsius(25)
c.value = 30
print(c.value)
```

### Solution 7
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
<!--/SOLUTION-->

<!--QUIZ-->
What does __str__ define?
- How str(obj) displays
- Memory layout
- Iteration
- Hashing
* Correct answer: How str(obj) displays
Human-readable form.

What does __repr__ define?
- Representation for developers
- Size
- Hash
- Iteration
* Correct answer: Representation for developers
Used by repr() and debugging.

What should __eq__ return?
- bool
- str
- None
- int
* Correct answer: bool
True if equal.

What does __len__ enable?
- len(obj)
- len(str)
- sum
- max
* Correct answer: len(obj)
Requires integer return.

What does __getitem__ enable?
- obj[index]
- len(obj)
- obj.attr
- obj()
* Correct answer: obj[index]
Index access.

What is property?
- Controlled attribute access
- A class
- A module
- A method type
* Correct answer: Controlled attribute access
With getter/setter.

Which decorator makes a getter?
- @property
- @staticmethod
- @classmethod
- @decorator
* Correct answer: @property
Marks the getter.

Which decorator sets a setter?
- @value.setter
- @property
- @setter
- @assign
* Correct answer: @value.setter
Companion to the property.

What does __add__ define?
- obj + other
- obj - other
- obj * other
- obj / other
* Correct answer: obj + other
Operator overloading.

What does __repr__ use !r for?
- repr() of the value in f-string
- str()
- int()
- bool()
* Correct answer: repr() of the value in f-string
f"{x!r}" uses repr.

Can __eq__ be defined without __hash__?
- Yes, but object becomes unhashable
- No
- Only with hash
- Always
* Correct answer: Yes, but object becomes unhashable
Python sets __hash__ to None.

Which magic method runs at len(obj)?
- __len__
- __size__
- __count__
- __items__
* Correct answer: __len__
Must return a non-negative int.
<!--/QUIZ-->
