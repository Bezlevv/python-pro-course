---
title: Password Generators and Handy Utilities
summary: We'll write a secure password generator with the secrets module plus a few small utilities that come in handy every day.
order: 6
duration: 30 min
difficulty: intermediate
tags: secrets, random, generators, utilities
---

A password like "qwerty123" or "123456" is like an open door. But coming up with complex passwords by hand is also a pain. These are exactly the tasks that exist to be automated: today we'll write a password generator and a couple of related utilities.

## secrets vs random

The built-in `random` module is fine for games and simulations, but not for passwords and tokens: its algorithm is predictable. For cryptographically strong random numbers there's the `secrets` module:

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(12))
print(password)
```

`string.ascii_letters` — all Latin letters in both cases, `string.digits` — digits, `string.punctuation` — punctuation marks.

## Guaranteed Composition

Simply picking characters can yield a password without a single digit. To avoid that, we assemble the password from parts: at least one digit, one special character, and the rest random:

```python
def make_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    password += [secrets.choice(chars) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)
```

Shuffling matters: otherwise the first characters would always be predictable.

## Other Handy Utilities

Generating a token in one call — `secrets.token_urlsafe(n)`:

```python
token = secrets.token_urlsafe(16)
print(token)
```

Unique file names with dates — useful for backups:

```python
from datetime import datetime

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"backup_{stamp}.zip"
print(filename)
```

And hashing strings is the standard way to verify integrity (e.g., whether a password matches a "fingerprint"):

```python
import hashlib

h = hashlib.sha256("secret".encode()).hexdigest()
print(h)
```

This is a minimal toolkit that countless daily scripts grow from.

<!--TASK-->
### Task 1
Write a function `make_password(length=12)` that returns a password of the given length made of letters and digits (no special characters). Use `string.ascii_letters + string.digits` and `secrets.choice`. Print the result. Expected result: a string of 12 random characters (letters and digits) when calling `make_password()`.

### Task 2
Improve the generator so the password is guaranteed to contain at least one digit, one uppercase letter, and one lowercase letter. Length — 16. Hint: collect the required characters in a list, add the rest randomly, and shuffle with `secrets.SystemRandom().shuffle(password)`. Expected result: any generated password satisfies all three conditions.

### Task 3
Write a full generator `make_password(length=12)` including all four character types: lowercase, uppercase letters, digits, and punctuation (`string.punctuation`), with each type guaranteed present and shuffling. Expected result: a password with at least one character of each of the four types.

### Task 4
Write a utility `backup_filename()` that returns a string like `backup_20261101_123000.zip`, where the numbers are the current date and time. Use `datetime.now().strftime("%Y%m%d_%H%M%S")`. Print the result. Expected result: a file name with the current date and time in it.

### Task 5
Create a "fingerprint" generator: a function `hash_text(text)` that returns `hashlib.sha256(text.encode()).hexdigest()`. Then ask the user to enter a string, print its hash, ask for the string again, and compare the hashes — if they match, print `Correct!`, otherwise `Incorrect`. Expected result: `Hash: <64 characters>` and the verdict on the match.
<!--/TASK-->

<!--HINT-->
### Hint 1
`alphabet = string.ascii_letters + string.digits`; assemble the password with a generator expression: `"".join(secrets.choice(alphabet) for _ in range(length))`. Import `secrets` and `string`.

### Hint 2
Set up a list with guaranteed characters: `secrets.choice(string.ascii_lowercase)`, `secrets.choice(string.ascii_uppercase)`, `secrets.choice(string.digits)`. Fill to the needed length with random ones from the full alphabet, then `secrets.SystemRandom().shuffle(password)` and `"".join(password)`.

### Hint 3
Base it on the solution of task 2 and add a fourth required element — `secrets.choice(string.punctuation)`. The alphabet for the remaining characters is `string.ascii_letters + string.digits + string.punctuation`. Don't forget to shuffle.

### Hint 4
`from datetime import datetime`; `stamp = datetime.now().strftime("%Y%m%d_%H%M%S")`; return `f"backup_{stamp}.zip"`. The `%Y%m%d` format — year, month, day; `%H%M%S` — hours, minutes, seconds.

### Hint 5
`hashlib.sha256(text.encode()).hexdigest()` — note the `.encode()`: you hash bytes, not a string. To compare, store the first hash in a variable and compare it with the hash of the second input.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import secrets
import string

def make_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

print(make_password())
```

Result (example):

```
Kp7Qw2xR9aLm
```

What's going on here? `string.ascii_letters` is a string with all Latin letters in both cases, `string.digits` is "0123456789". Their sum is our alphabet. `secrets.choice(alphabet)` picks a random character from the alphabet, and the generator expression repeats the choice `length` times. `"".join(...)` glues the characters into a string. `secrets` uses the system entropy source, so the result is unpredictable — such a password can't be guessed by brute force with generator-state prediction.

### Solution 2
Solution:

```python
import secrets
import string

def make_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]
    password += [secrets.choice(alphabet) for _ in range(length - 3)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

print(make_password())
```

What's going on here? We guarantee the composition manually: the first character is lowercase, the second uppercase, the third a digit. Then we pad the password with `length - 3` random characters. But if we left it as is, the first three characters would be predictable — so `secrets.SystemRandom().shuffle(password)` shuffles the list in place. `SystemRandom` is `secrets`' companion for shuffling: it's also cryptographically strong. After joining, any password in any combination contains all three required character types.

### Solution 3
Solution:

```python
import secrets
import string

def make_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    password += [secrets.choice(chars) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)

print(make_password())
```

What's going on here? This is the final version: four guaranteed characters — one of each type — and the `chars` alphabet includes punctuation (`string.punctuation` — `!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`). Shuffling removes position predictability. Such a password passes most corporate complexity requirements. Note that `length - 4` is the number of "free" characters: with `length=12` there are eight of them, and the total length always matches what was requested.

### Solution 4
Solution:

```python
from datetime import datetime

def backup_filename():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{stamp}.zip"

print(backup_filename())
```

Result (example):

```
backup_20261101_123000.zip
```

What's going on here? `datetime.now()` returns the current date and time. The `strftime` method formats them per the template: `%Y` — four-digit year, `%m` — month, `%d` — day, `%H` — hours, `%M` — minutes, `%S` — seconds. Such a timestamp is unique within a second, so two backups won't overwrite each other. This is the standard trick for archives, logs, and temporary files: sorting by name automatically matches sorting by time.

### Solution 5
Solution:

```python
import hashlib

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

first = input("Enter a string: ")
print("Hash:", hash_text(first))

second = input("Enter the string again: ")
if hash_text(second) == hash_text(first):
    print("Correct!")
else:
    print("Incorrect")
```

Result (example):

```
Enter a string: secret
Hash: 4d7c5f5c7a4b1c5f6e3f0a8d2c9b1e5a7f3c6d8e0b9a2f4c1d5e6b7a8c3
Enter the string again: secret
Correct!
```

What's going on here? `hashlib.sha256` computes SHA-256 — a cryptographic hash of an arbitrary string. Only bytes can be hashed, so first `.encode()` turns the string into bytes (UTF-8 by default). `.hexdigest()` returns the hash as a 64-hex-character string. Identical strings give identical hashes, while the tiniest difference yields a completely different result. This is exactly how file integrity is verified and how passwords are stored in databases.
<!--/SOLUTION-->

<!--QUIZ-->
Why use secrets for passwords instead of random?
- secrets works faster
- random is predictable, while secrets gives cryptographically strong random values
- random cannot be imported
- secrets returns only numbers
* Correct answer: random is predictable, while secrets gives cryptographically strong random values
secrets uses the system entropy source and suits passwords and tokens.

What does string.ascii_letters contain?
- Only lowercase letters
- All Latin letters in both cases
- Letters and digits
- Only digits
* Correct answer: All Latin letters in both cases
It's the concatenation of ascii_lowercase and ascii_uppercase.

What does secrets.choice(seq) do?
- Returns the whole sequence
- Picks a random element from the sequence
- Shuffles the sequence
- Deletes a random element
* Correct answer: Picks a random element from the sequence
choice returns one random element, like random.choice, but in a strong way.

What does secrets.token_urlsafe(16) do?
- Prints 16 random numbers
- Returns a random URL-safe token
- Creates a link
- Encodes a string
* Correct answer: Returns a random URL-safe token
token_urlsafe generates a string that's safe to put in a URL: without characters like / and +.

How do you get the current date and time as a string?
- datetime.today().text()
- datetime.now().strftime("%Y%m%d_%H%M%S")
- time.current().format()
- date.now().string()
* Correct answer: datetime.now().strftime("%Y%m%d_%H%M%S")
strftime formats a datetime according to a template of %-directives.

What does hashlib.sha256("abc".encode()).hexdigest() return?
- A file object
- A string of 64 hexadecimal characters
- A number of bytes
- A list of characters
* Correct answer: A string of 64 hexadecimal characters
hexdigest() represents the SHA-256 hash as a hex string of 64 characters.

Why shuffle the password after assembling it from required parts?
- So the required characters don't sit at predictable positions
- To increase the password length
- To reduce the number of character types
- To add letters to the password
* Correct answer: So the required characters don't sit at predictable positions
Without shuffle, the first characters would always be the same types — that weakens the password.

Why convert a string with .encode() before hashing?
- Because hashlib works with bytes, not strings
- Because the hash gets shorter that way
- Because encode fixes typos
- It's optional, but customary
* Correct answer: Because hashlib works with bytes, not strings
sha256(text.encode()) turns the string into UTF-8 bytes; without .encode() the call raises a TypeError.
<!--/QUIZ-->
