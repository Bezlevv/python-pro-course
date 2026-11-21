---
title: Error handling: try/except/raise
summary: Exceptions, catching errors, finally, raising your own errors.
order: 11
duration: 35 min
difficulty: intermediate
tags: exceptions, try, except, finally, raise
---

Errors happen. Python lets you catch them instead of crashing.

## Common exceptions

- ValueError — wrong value;
- TypeError — wrong type;
- KeyError — missing key;
- IndexError — index out of range;
- FileNotFoundError — missing file.

## try/except

```python
try:
    n = int(input("Number: "))
    print(10 / n)
except ValueError:
    print("Not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

## else and finally

- else runs if no error;
- finally runs always (e.g., close a resource).

## raise

```python
def set_age(age):
    if age < 0 or age > 120:
        raise ValueError("Invalid age")
    return age
```

## Lesson summary

We learned to catch exceptions, use else/finally, and raise our own errors.

<!--TASK-->
### Task 1 — Catch ValueError
Read an integer; if the user enters text, print "Not a number" via except ValueError.

### Task 2 — Catch ZeroDivisionError
Compute 10 / n; catch ZeroDivisionError and print a friendly message.

### Task 3 — Else block
In the try block, print "Success" in else when no error occurred.

### Task 4 — Finally
Use finally to print "Done" no matter what.

### Task 5 — Multiple exceptions
Catch both ValueError and ZeroDivisionError separately and print different messages.

### Task 6 — Raise
Write set_age(age): raise ValueError if age < 0 or > 120. Test with -5.

### Task 7 — FileNotFoundError
Try to open "missing.txt" and catch FileNotFoundError with a message.
<!--/TASK-->

<!--HINT-->
### Hint 1
int(input(...)) may raise ValueError.

### Hint 2
10 / n raises ZeroDivisionError when n == 0.

### Hint 3
else is placed after except blocks.

### Hint 4
finally follows except/else and always runs.

### Hint 5
List several except blocks.

### Hint 6
raise ValueError("...") throws a custom error.

### Hint 7
open("missing.txt") raises FileNotFoundError.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
try:
    n = int(input("Number: "))
except ValueError:
    print("Not a number")
```

### Solution 2
```python
try:
    n = int(input("Number: "))
    print(10 / n)
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Solution 3
```python
try:
    n = int(input("Number: "))
except ValueError:
    print("Not a number")
else:
    print("Success")
```

### Solution 4
```python
try:
    n = int(input("Number: "))
except ValueError:
    print("Not a number")
finally:
    print("Done")
```

### Solution 5
```python
try:
    n = int(input("Number: "))
    print(10 / n)
except ValueError:
    print("Not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Solution 6
```python
def set_age(age):
    if age < 0 or age > 120:
        raise ValueError("Invalid age")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)   # Invalid age
```

### Solution 7
```python
try:
    with open("missing.txt") as f:
        print(f.read())
except FileNotFoundError:
    print("File not found")
```
<!--/SOLUTION-->

<!--QUIZ-->
What does try do?
- Defines a block that may raise an error
- Catches errors
- Raises errors
- Prints errors
* Correct answer: Defines a block that may raise an error
The protected block.

What does except do?
- Catches specific exceptions
- Always runs
- Raises
- Returns
* Correct answer: Catches specific exceptions
Handles the error.

When does else run?
- If no exception occurred
- Always
- Only on error
- Never
* Correct answer: If no exception occurred
The success path.

When does finally run?
- Always
- Only on error
- Only on success
- Never
* Correct answer: Always
Cleanup guaranteed.

What is ZeroDivisionError?
- Dividing by zero
- Wrong type
- Missing file
- Bad key
* Correct answer: Dividing by zero
Raised by 10/0.

How to raise your own error?
- raise ValueError("...")
- error("...")
- throw ValueError
- except ValueError
* Correct answer: raise ValueError("...")
Custom exception.

What exception for a missing file?
- FileNotFoundError
- ValueError
- KeyError
- IndexError
* Correct answer: FileNotFoundError
open() raises it.

What is the syntax to catch and inspect?
- except ValueError as e
- except e
- catch ValueError
- except (e)
* Correct answer: except ValueError as e
e holds the exception.

Does except catch all if you write except:?
- Yes, all exceptions
- No
- Only ValueError
- Only system errors
* Correct answer: Yes, all exceptions
But it is usually too broad.

What happens with unhandled error?
- Program crashes with traceback
- Nothing
- It is ignored
- Python prints "ok"
* Correct answer: Program crashes with traceback
Unhandled exceptions stop the program.

Which is a bad practice?
- Bare except: pass
- except ValueError
- try/finally
- except Exception as e
* Correct answer: Bare except: pass
It hides all errors.

What does finally guarantee?
- Code runs even on error
- The result
- The exception
- Nothing
* Correct answer: Code runs even on error
Best for closing resources.
<!--/QUIZ-->
