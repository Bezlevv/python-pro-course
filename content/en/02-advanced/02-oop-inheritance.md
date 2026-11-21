---
title: Inheritance and polymorphism
summary: Subclasses, overriding, super(), polymorphism and isinstance.
order: 2
duration: 35 min
difficulty: intermediate
tags: inheritance, subclass, super, polymorphism
---

Inheritance lets a class reuse and extend another class.

## Basic inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"
```

## Overriding

The subclass redefines a method with the same name.

## super()

```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```

`super()` calls the parent implementation.

## Polymorphism

The same method name works differently per class:

```python
for a in [Dog("Rex"), Cat("Tom")]:
    print(a.speak())
```

## isinstance

```python
isinstance(Dog("Rex"), Animal)   # True
```

## Lesson summary

We learned subclassing, overriding, super(), and polymorphism.

<!--TASK-->
### Task 1 — Shape hierarchy
Create class Shape with area() returning 0; classes Square(side) and Circle(radius) overriding area().

### Task 2 — super() init
Create class Employee with name and salary; class Manager(Employee) that also stores team_size and calls super().__init__.

### Task 3 — Override __str__
Override __str__ in Employee to return f"Employee(name, salary)". Print an instance.

### Task 4 — Polymorphism loop
Given animals list (Dog, Cat), loop and print speak() for each.

### Task 5 — isinstance check
Create objects and check isinstance for Dog vs Animal and Dog vs object.

### Task 6 — Method resolution
Create class A with greet(); class B(A) overriding greet; call B().greet() and A().greet() to see the difference.

### Task 7 — Multi-level
Create class A, B(A), C(B); add a method in A and call it from C instance.
<!--/TASK-->

<!--HINT-->
### Hint 1
class Square(Shape): def area(self): return self.side**2.

### Hint 2
Manager.__init__ calls super().__init__(name, salary).

### Hint 3
return f"Employee({self.name}, {self.salary})".

### Hint 4
Loop over the list and call speak().

### Hint 5
isinstance(obj, Animal) — True for subclasses.

### Hint 6
Overriding replaces the parent method.

### Hint 7
C inherits from B which inherits from A; method found up the chain.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        import math
        return math.pi * self.radius ** 2

print(Square(4).area())   # 16
print(Circle(2).area())
```

### Solution 2
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

m = Manager("Anna", 100000, 5)
print(m.name, m.team_size)
```

### Solution 3
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    def __str__(self):
        return f"Employee({self.name}, {self.salary})"

print(Employee("Boris", 50000))
```

### Solution 4
```python
animals = [Dog("Rex"), Cat("Tom")]
for a in animals:
    print(a.speak())
# Woof / Meow
```

### Solution 5
```python
d = Dog("Rex")
print(isinstance(d, Animal))   # True
print(isinstance(d, Dog))      # True
print(isinstance(d, object))   # True
```

### Solution 6
```python
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

print(A().greet())   # Hello from A
print(B().greet())   # Hello from B
```

### Solution 7
```python
class A:
    def hello(self):
        return "A.hello"

class B(A):
    pass

class C(B):
    pass

print(C().hello())   # A.hello
```
<!--/SOLUTION-->

<!--QUIZ-->
What is inheritance?
- Reusing and extending a class
- Creating an object
- A module
- A loop
* Correct answer: Reusing and extending a class
Subclass gets parent behavior.

Which keyword creates a subclass?
- class Dog(Animal):
- class Dog:
- subclass Dog
- extend Dog
* Correct answer: class Dog(Animal):
Parent in parentheses.

What is overriding?
- Redefining a method in the subclass
- Deleting a method
- Importing
- Renaming
* Correct answer: Redefining a method in the subclass
Same name, new behavior.

What does super() do?
- Calls the parent implementation
- Creates a new object
- Deletes
- Nothing
* Correct answer: Calls the parent implementation
Useful in __init__.

How to call parent __init__?
- super().__init__(args)
- self.__init__
- parent().__init__
- Animal.init
* Correct answer: super().__init__(args)
Runs the parent initializer.

What is polymorphism?
- Same interface, different behavior
- One class only
- Static methods
- Errors
* Correct answer: Same interface, different behavior
speak() works per class.

What does isinstance(d, Animal) check?
- Whether d is an Animal or subclass
- If d is a string
- The memory
- The method
* Correct answer: Whether d is an Animal or subclass
Inheritance-aware check.

If B(A) overrides greet, which runs for B().greet()?
- B's version
- A's version
- Both
- None
* Correct answer: B's version
Overriding wins.

What is multi-level inheritance?
- A → B → C chain
- Two parents
- Interfaces
- Modules
* Correct answer: A → B → C chain
C inherits from B, B from A.

What is the parent of all classes?
- object
- Animal
- Class
- Base
* Correct answer: object
Everything inherits from object.

Can a subclass add new attributes?
- Yes
- No
- Only methods
- Only static
* Correct answer: Yes
New attributes are added in __init__.

What does super().__init__(name) do in Dog?
- Sets name from Animal
- Creates Animal
- Deletes name
- Nothing
* Correct answer: Sets name from Animal
Reuses parent initialization.
<!--/QUIZ-->
