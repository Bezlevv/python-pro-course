---
title: Генераторы паролей и полезные утилиты
summary: Напишем безопасный генератор паролей на модуле secrets и ещё несколько маленьких утилит, которые пригодятся каждый день.
order: 6
duration: 30 мин
difficulty: intermediate
tags: secrets, random, генераторы, утилиты
---

Пароль «qwerty123» или «123456» — это как открытая дверь. Но и придумывать сложные пароли руками — мука. Такие задачи и существуют, чтобы их автоматизировали: сегодня мы напишем генератор паролей и пару смежных утилит.

## secrets против random

Встроенный модуль `random` подходит для игр и симуляций, но для паролей и токенов он не годится: его алгоритм предсказуем. Для криптографически стойких случайных чисел существует модуль `secrets`:

```python
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(12))
print(password)
```

`string.ascii_letters` — все латинские буквы в обоих регистрах, `string.digits` — цифры, `string.punctuation` — знаки препинания.

## Гарантированный состав

Простой выбор символов может дать пароль без единой цифры. Чтобы такого не было, соберём пароль из частей: обязательно одна цифра, один спецсимвол, а остальные символы — случайные:

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

Перемешивание важно: иначе первые символы всегда будут предсказуемы.

## Другие полезные утилиты

Генерация токена одним вызовом — `secrets.token_urlsafe(n)`:

```python
token = secrets.token_urlsafe(16)
print(token)
```

Уникальные имена файлов с датой — пригодится для бэкапов:

```python
from datetime import datetime

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"backup_{stamp}.zip"
print(filename)
```

А хэширование строк — стандартный способ проверить целостность (например, совпадает ли пароль с «отпечатком»):

```python
import hashlib

h = hashlib.sha256("секрет".encode()).hexdigest()
print(h)
```

Это минимальный набор инструментов, из которых вырастает множество ежедневных скриптов.

<!--TASK-->
### Задача 1
Напиши функцию `make_password(length=12)`, которая возвращает пароль заданной длины из букв и цифр (без спецсимволов). Используй `string.ascii_letters + string.digits` и `secrets.choice`. Напечатай результат. Ожидаемый результат: строка из 12 случайных символов (буквы и цифры) при вызове `make_password()`.

### Задача 2
Доработай генератор так, чтобы в пароле гарантированно были хотя бы одна цифра, одна заглавная и одна строчная буква. Длина — 16. Подсказка: собери обязательные символы списком, добавь остальные случайные и перемешай через `secrets.SystemRandom().shuffle(password)`. Ожидаемый результат: любой сгенерированный пароль удовлетворяет всем трём условиям.

### Задача 3
Напиши полный генератор `make_password(length=12)`, включающий все четыре типа символов: строчные, заглавные буквы, цифры и знаки препинания (`string.punctuation`), с обязательным присутствием каждого типа и перемешиванием. Ожидаемый результат: пароль, в котором есть минимум один символ каждого из четырёх типов.

### Задача 4
Напиши утилиту `backup_filename()`, которая возвращает строку вида `backup_20261101_123000.zip`, где числа — текущие дата и время. Используй `datetime.now().strftime("%Y%m%d_%H%M%S")`. Напечатай результат. Ожидаемый результат: имя файла с текущей датой и временем в названии.

### Задача 5
Создай генератор «отпечатков»: функцию `hash_text(text)`, которая возвращает `hashlib.sha256(text.encode()).hexdigest()`. Затем попроси пользователя ввести строку, выведи её хэш, потом попроси ввести строку повторно и сравни хэши — если совпали, печатай `Верно!`, иначе `Неверно`. Ожидаемый результат: `Хэш: <64 символа>` и вердикт о совпадении.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`alphabet = string.ascii_letters + string.digits`; собери пароль генераторным выражением: `"".join(secrets.choice(alphabet) for _ in range(length))`. Импортируй `secrets` и `string`.

### Подсказка 2
Заведи список с гарантированными символами: `secrets.choice(string.ascii_lowercase)`, `secrets.choice(string.ascii_uppercase)`, `secrets.choice(string.digits)`. Дополни до нужной длины случайными из общего алфавита, затем `secrets.SystemRandom().shuffle(password)` и `"".join(password)`.

### Подсказка 3
Возьми за основу решение задачи 2 и добавь четвёртый обязательный элемент — `secrets.choice(string.punctuation)`. Алфавит для остальных символов — `string.ascii_letters + string.digits + string.punctuation`. Не забудь перемешать.

### Подсказка 4
`from datetime import datetime`; `stamp = datetime.now().strftime("%Y%m%d_%H%M%S")`; верни `f"backup_{stamp}.zip"`. Формат `%Y%m%d` — год, месяц, день; `%H%M%S` — часы, минуты, секунды.

### Подсказка 5
`hashlib.sha256(text.encode()).hexdigest()` — обрати внимание на `.encode()`: хэшировать нужно байты, а не строку. Для сравнения храни первый хэш в переменной и сравнивай с хэшем второго ввода.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import secrets
import string

def make_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

print(make_password())
```

Результат (пример):

```
Kp7Qw2xR9aLm
```

Что здесь происходит? `string.ascii_letters` — строка со всеми латинскими буквами в обоих регистрах, `string.digits` — «0123456789». Их сумма — наш алфавит. `secrets.choice(alphabet)` выбирает случайный символ из алфавита, а выражение-генератор повторяет выбор `length` раз. `"".join(...)` склеивает символы в строку. `secrets` использует системный источник энтропии, поэтому результат непредсказуем — такой пароль нельзя угадать перебором с предсказанием состояния генератора.

### Разбор 2
Решение:

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

Что здесь происходит? Мы гарантируем состав вручную: первый символ — строчная буква, второй — заглавная, третий — цифра. Затем дополняем пароль `length - 3` случайными символами. Но если оставить как есть, первые три символа будут предсказуемы — поэтому `secrets.SystemRandom().shuffle(password)` перемешивает список на месте. `SystemRandom` — спутник `secrets` для перемешивания: он тоже криптографически стойкий. После склейки любой пароль в любой комбинации содержит все три обязательных типа символов.

### Разбор 3
Решение:

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

Что здесь происходит? Это финальная версия: четыре гарантированных символа — по одному от каждого типа, а алфавит `chars` включает знаки препинания (`string.punctuation` — `!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`). Перемешивание убирает предсказуемость позиций. Такой пароль проходит большинство корпоративных требований сложности. Заметь, что `length - 4` — количество «свободных» символов: при `length=12` их восемь, и общая длина всегда совпадает с запрошенной.

### Разбор 4
Решение:

```python
from datetime import datetime

def backup_filename():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_{stamp}.zip"

print(backup_filename())
```

Результат (пример):

```
backup_20261101_123000.zip
```

Что здесь происходит? `datetime.now()` возвращает текущие дату и время. Метод `strftime` форматирует их по шаблону: `%Y` — год из четырёх цифр, `%m` — месяц, `%d` — день, `%H` — часы, `%M` — минуты, `%S` — секунды. Такая метка времени уникальна в пределах секунды, поэтому два бэкапа не перезапишут друг друга. Это стандартный приём для архивов, логов и временных файлов: сортировка по имени автоматически совпадает с сортировкой по времени.

### Разбор 5
Решение:

```python
import hashlib

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

first = input("Введи строку: ")
print("Хэш:", hash_text(first))

second = input("Введи строку повторно: ")
if hash_text(second) == hash_text(first):
    print("Верно!")
else:
    print("Неверно")
```

Результат (пример):

```
Введи строку: секрет
Хэш: 4d7c5f5c7a4b1c5f6e3f0a8d2c9b1e5a7f3c6d8e0b9a2f4c1d5e6b7a8c3
Введи строку повторно: секрет
Верно!
```

Что здесь происходит? `hashlib.sha256` вычисляет SHA-256 — криптографический хэш произвольной строки. Хэшировать можно только байты, поэтому сначала `.encode()` превращает строку в байты (по умолчанию UTF-8). `.hexdigest()` возвращает хэш как строку из 64 шестнадцатеричных символов. Одинаковые строки дают одинаковые хэши, а малейшее отличие — полностью другой результат. Именно так проверяют целостность файлов и хранят пароли в базах данных.
<!--/SOLUTION-->

<!--QUIZ-->
Почему для паролей используют secrets, а не random?
- secrets работает быстрее
- random предсказуем, а secrets даёт криптографически стойкие случайные значения
- random нельзя импортировать
- secrets возвращает только числа
* Правильный ответ: random предсказуем, а secrets даёт криптографически стойкие случайные значения
secrets использует системный источник энтропии и подходит для паролей и токенов.

Что содержит string.ascii_letters?
- Только строчные буквы
- Все латинские буквы в обоих регистрах
- Буквы и цифры
- Только цифры
* Правильный ответ: Все латинские буквы в обоих регистрах
Это конкатенация ascii_lowercase и ascii_uppercase.

Что делает secrets.choice(seq)?
- Возвращает всю последовательность
- Выбирает случайный элемент из последовательности
- Перемешивает последовательность
- Удаляет случайный элемент
* Правильный ответ: Выбирает случайный элемент из последовательности
choice возвращает один случайный элемент, как в random.choice, но стойким способом.

Что делает secrets.token_urlsafe(16)?
- Печатает 16 случайных чисел
- Возвращает случайный URL-безопасный токен
- Создаёт ссылку
- Кодирует строку
* Правильный ответ: Возвращает случайный URL-безопасный токен
token_urlsafe генерирует строку, которую безопасно вставлять в URL: без символов вроде / и +.

Как получить текущую дату и время в виде строки?
- datetime.today().text()
- datetime.now().strftime("%Y%m%d_%H%M%S")
- time.current().format()
- date.now().string()
* Правильный ответ: datetime.now().strftime("%Y%m%d_%H%M%S")
strftime форматирует дату-время по шаблону из %-директив.

Что возвращает hashlib.sha256("abc".encode()).hexdigest()?
- Объект файла
- Строку из 64 шестнадцатеричных символов
- Число байтов
- Список символов
* Правильный ответ: Строку из 64 шестнадцатеричных символов
hexdigest() представляет хэш SHA-256 как hex-строку длиной 64 символа.
<!--/QUIZ-->
