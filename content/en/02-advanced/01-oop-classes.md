---
title: Classes and objects
summary: Classes, objects, attributes, methods, __init__ and self.
order: 1
duration: 30 min
difficulty: intermediate
tags: oop, class, object, methods, self
---

Object-oriented programming groups data and behavior into classes.

## Class and object

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} says woof!"

rex = Dog("Rex", 3)
print(rex.bark())
```

## Attributes

- `self.name`, `self.age` — attributes of the instance;
- accessed as `rex.name`.

## Methods

Methods are functions inside a class; the first parameter is always `self` (the instance).

## __init__

`__init__` runs when an object is created and initializes its attributes.

## Practice

Create classes for your domain: rectangles, bank accounts, tasks.

## Lesson summary

We learned class/object, attributes, methods and `__init__`.

<!--TASK-->
### Task 1 — Simple class
Create class Person with __init__(name, age) and method introduce() returning f"I am {name}, {age}".

### Task 2 — Bank account
Create class Account with balance=0; methods deposit(amount) and withdraw(amount) updating balance; print after each.

### Task 3 — Rectangle
Create class Rectangle(width, height) with area() and perimeter().

### Task 4 — Counter
Create class Counter with a count attribute, increment() and value() methods.

### Task 5 — Student
Create class Student with name and grades list; add method add_grade(g) and average().

### Task 6 — Comparing objects
Create a class Point(x, y) and a method distance_to(other) using math.hypot.

### Task 7 — Multiple objects
Create three Person objects and collect their introductions in a list; print each.
<!--/TASK-->

<!--HINT-->
### Hint 1
def __init__(self, name, age): self.name = name; self.age = age.

### Hint 2
self.balance += amount; check if enough before withdraw.

### Hint 3
area = width * height; perimeter = 2*(width+height).

### Hint 4
self.count = 0; increment: self.count += 1.

### Hint 5
self.grades = []; add_grade appends; average = sum/len.

### Hint 6
math.hypot(dx, dy).

### Hint 7
Loop over list of objects and call introduce().
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"I am {self.name}, {self.age}"

p = Person("Anna", 21)
print(p.introduce())
```

### Solution 2
```python
class Account:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Not enough money")

acc = Account()
acc.deposit(100)
acc.withdraw(30)
print(acc.balance)   # 70
```

### Solution 3
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(4, 5)
print(r.area(), r.perimeter())   # 20 18
```

### Solution 4
```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def value(self):
        return self.count

c = Counter()
c.increment(); c.increment()
print(c.value())   # 2
```

### Solution 5
```python
class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, g):
        self.grades.append(g)

    def average(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

s = Student("Boris")
s.add_grade(4); s.add_grade(5)
print(s.average())   # 4.5
```

### Solution 6
```python
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

a = Point(0, 0)
b = Point(3, 4)
print(a.distance_to(b))   # 5.0
```

### Solution 7
```python
people = [Person("Anna", 21), Person("Boris", 30)]
for p in people:
    print(p.introduce())
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a class?
- A blueprint for objects
- An object
- A function
- A list
* Correct answer: A blueprint for objects
Defines structure and behavior.

What is an object?
- An instance of a class
- A class
- A module
- A file
* Correct answer: An instance of a class
Created by calling the class.

What is self?
- The instance itself
- The class
- A parameter of the module
- None
* Correct answer: The instance itself
First parameter of methods.

When does __init__ run?
- When an object is created
- When a method is called
- On import
- Never
* Correct answer: When an object is created
Constructor/initializer.

What are attributes?
- Data attached to an object
- Methods
- Classes
- Functions
* Correct answer: Data attached to an object
Accessed as obj.attr.

How to access a method?
- obj.method()
- obj.method
- class.method(obj)
- method(obj)
* Correct answer: obj.method()
Call with parentheses.

What is self.dog in class Dog?
- An attribute of the instance
- A global
- A method
- A class
* Correct answer: An attribute of the instance
Set in __init__.

Can two objects have different attribute values?
- Yes
- No
- Only static
- Never
* Correct answer: Yes
Each instance has its own state.

What does Dog("Rex", 3) do?
- Creates an object
- Calls bark
- Defines a class
- Imports
* Correct answer: Creates an object
Calls __init__.

What is a method?
- A function inside a class
- A variable
- A module
- An object
* Correct answer: A function inside a class
Acts on the instance.

How to initialize two attributes?
- self.x = x; self.y = y
- x = 1; y = 2
- return x, y
- declare
* Correct answer: self.x = x; self.y = y
Inside __init__.

What happens if __init__ is absent?
- Object created without custom init
- Error
- Class not usable
- Return None
* Correct answer: Object created without custom init
Default behavior.
<!--/QUIZ-->
