---
title: Modules and import
summary: Importing, from import, aliases, creating your own module and __name__.
order: 13
duration: 30 min
difficulty: intermediate
tags: modules, import, from, __name__
---

Modules are Python files with reusable code. Importing lets you use them.

## Import styles

```python
import math
from math import sqrt, pi
import math as m
from mymod import helper
```

## Creating your own module

Create `utils.py` with functions, then in another file:

```python
import utils
print(utils.double(4))
```

## __name__ idiom

```python
if __name__ == "__main__":
    # runs only when executed directly
    main()
```

## Packages

A folder with `__init__.py` (or namespace package) forms a package: `from mypkg.sub import x`.

## Lesson summary

We learned import styles, creating modules and the `__name__` idiom.

<!--TASK-->
### Task 1 — import math
Import math and print math.sqrt(16), math.pi (approximation).

### Task 2 — from import
From math import sqrt, pi and use them without math.

### Task 3 — Alias
Import datetime as dt and use dt.date.today().

### Task 4 — Own module
Create utils.py with double(x). Import it in another script (print double(21)).

### Task 5 — __name__ test
Write a script that prints __name__ when run directly (expected "__main__").

### Task 6 — Random
Use random.randint(1, 6) to simulate a die; print 5 rolls.

### Task 7 — Package-like structure
Create a folder mypkg with __init__.py and a helper; import from it via from mypkg.helper import add.
<!--/TASK-->

<!--HINT-->
### Hint 1
math.sqrt and math.pi.

### Hint 2
from math import sqrt, pi.

### Hint 3
import datetime as dt.

### Hint 4
Place utils.py in the same folder.

### Hint 5
print(__name__) under if __name__ == "__main__".

### Hint 6
random.randint(1, 6).

### Hint 7
__init__.py can be empty.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import math
print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.14159...
```

### Solution 2
```python
from math import sqrt, pi
print(sqrt(9))   # 3.0
print(pi)
```

### Solution 3
```python
import datetime as dt
print(dt.date.today())
```

### Solution 4
```python
# utils.py
def double(x):
    return x * 2
```
```python
# main.py
import utils
print(utils.double(21))   # 42
```

### Solution 5
```python
def main():
    print("Running main")

if __name__ == "__main__":
    print(__name__)   # __main__
    main()
```

### Solution 6
```python
import random
for _ in range(5):
    print(random.randint(1, 6))
```

### Solution 7
```python
# mypkg/__init__.py  (empty)
# mypkg/helper.py
def add(a, b):
    return a + b
```
```python
from mypkg.helper import add
print(add(2, 3))   # 5
```
<!--/SOLUTION-->

<!--QUIZ-->
What does import math do?
- Makes module math available
- Copies its code
- Runs it
- Nothing
* Correct answer: Makes module math available
Access via math.name.

Which imports only sqrt and pi?
- from math import sqrt, pi
- import math
- import sqrt
- from math import *
* Correct answer: from math import sqrt, pi
Selective import.

What does import math as m do?
- Creates an alias m
- Copies math
- Renames file
- Error
* Correct answer: Creates an alias m
Use m.sqrt instead.

What is __name__ when running directly?
- "__main__"
- Module name
- None
- "main"
* Correct answer: "__main__"
The entry script.

Why guard with if __name__ == "__main__"?
- To run code only when executed directly
- To import faster
- To hide functions
- To avoid errors
* Correct answer: To run code only when executed directly
Prevents side effects on import.

What is a package?
- A folder with modules
- A single file
- A zip
- A function
* Correct answer: A folder with modules
Contains __init__.py.

How to import a function from your module?
- from utils import double
- import utils.double
- require utils
- include utils
* Correct answer: from utils import double
Direct name import.

What does random.randint(1, 6) return?
- An integer 1..6
- A float
- A list
- A string
* Correct answer: An integer 1..6
Random integer in range.

Which line imports datetime with alias?
- import datetime as dt
- import dt
- from datetime import dt
- datetime import
* Correct answer: import datetime as dt
Alias dt.

Can a module be imported multiple times?
- Yes, cached once
- No
- Errors
- Runs twice per import
* Correct answer: Yes, cached once
Python caches modules.

What is the extension of a module?
- .py
- .txt
- .m
- .mod
* Correct answer: .py
Python source.

What does from mypkg.helper import add do?
- Imports add from submodule helper
- Runs folder
- Loads mypkg
- Nothing
* Correct answer: Imports add from submodule helper
Package path syntax.
<!--/QUIZ-->
