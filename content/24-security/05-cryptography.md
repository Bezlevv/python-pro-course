---
title: Криптография на практике
summary: Хеширование паролей с солью, симметричное шифрование Fernet, выработка ключей и HMAC-коды — на реальных API hashlib, secrets, hmac и cryptography.
order: 5
duration: 45 мин
difficulty: advanced
tags: криптография, hashlib, cryptography, hmac, secrets, kdf
---

Криптография в приложении — это не «прикрутить шифрование», а выбор правильного примитива для задачи. Сначала разберём, чем отличаются главные понятия, потом посмотрим на реальные API Python.

## Хеширование ≠ шифрование

**Хеширование** — одностороннее преобразование: из пароля получается хеш, из хеша пароль восстановить нельзя. **Шифрование** — двустороннее: есть ключ, и данные можно вернуть обратно. Хеши подходят для паролей (проверяем хеш, а не пароль), шифрование — для данных, которые нужно прочитать позже.

Хеш пароля нельзя считать просто `hashlib.sha256(password).hexdigest()` — это быстро, а значит атакующий переберёт пароль за секунды. Нужна **соль** (случайное значение на пользователя) и **замедлитель** — дорогая функция выработки ключа (KDF):

```python
import hashlib
import secrets

salt = secrets.token_bytes(16)
password = "Пароль123".encode()
digest = hashlib.pbkdf2_hmac("sha256", password, salt, 600_000)
print(salt.hex(), digest.hex())
```

`pbkdf2_hmac` применяет HMAC-SHA256 600 000 раз — это намеренно медленно. Альтернативы: `hashlib.scrypt` (учитывает память) и `argon2` (библиотека `argon2-cffi`, считается лучшей для паролей).

## Хранение пароля: формат строки

Храни всё необходимое для проверки в одной строке: `алгоритм$итерации$соль$хеш`. Проверка должна быть **постоянного времени** — через `hmac.compare_digest`:

```python
import hmac

stored = f"pbkdf2_sha256$600000${salt.hex()}${digest.hex()}"
_, _, _, salt_hex, digest_hex = stored.split("$")
ok = hmac.compare_digest(
    digest_hex,
    hashlib.pbkdf2_hmac("sha256", password, bytes.fromhex(salt_hex), 600_000).hex(),
)
```

## Симметричное шифрование: Fernet

`cryptography` — главная библиотека Python для криптографии. Её высокоуровневый интерфейс `Fernet` даёт шифрование AES-128-CBC с аутентификацией (HMAC) и временем жизни токена:

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()          # str: base64-ключ
f = Fernet(key)
token = f.encrypt("секретные данные".encode())
print(f.decrypt(token).decode())
```

Ключ — это base64 от 32 байт; он хранится в секретах (не в коде!). Fernet подходит для шифрования небольших данных: файлов конфигурации, токенов, строк.

## HRMAC: проверка целостности

Когда нужно просто убедиться, что данные не изменяли (без шифрования), используют HMAC:

```python
import hmac
import hashlib

key = "ключ".encode()
message = b"data"
mac = hmac.new(key, message, hashlib.sha256).hexdigest()
# проверка: hmac.new(key, message, hashlib.sha256).hexdigest() == mac
```

Сравнивать нужно через `hmac.compare_digest` — обычное `==` уязвимо к атакам по времени.

## Одноразовые пароли: HOTP

На практику — HOTP (RFC 4226): код из 6 цифр, вычисляемый из счётчика и ключа. Реальный пример HMAC:

```python
import hmac
import hashlib
import struct

def hotp(key: bytes, counter: int) -> str:
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(code % 1_000_000).zfill(6)

key = b"this-is-my-shared-secret"
print(hotp(key, 0), hotp(key, 1))
```

## Важные правила

- **Не изобретай свою криптографию.** Используй проверенные библиотеки: `cryptography`, `hashlib`, `hmac`, `secrets`.
- **Ключи — в секреты**, не в код (урок 2).
- **TLS/HTTPS** — шифрование в пути; прикладное шифрование — только для данных в покое.
- **Случайность** — только `secrets` (не `random`!) для криптографических целей.

## Итог урока

Для паролей — KDF с солью (pbkdf2, scrypt, argon2) и постоянное время сравнения. Для данных — Fernet из `cryptography`. Для целостности — HMAC. Для кодов — HOTP/TOTP. Главное — не изобретать велосипед и не использовать слабые примитивы.

<!--TASK-->
### Задача 1
Напиши класс `PasswordHasher` с двумя методами. `hash_password(password)` генерирует соль через `secrets.token_bytes(16)`, считает `hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)` и возвращает строку формата `pbkdf2_sha256$600000$<соль hex>$<хеш hex>`. `verify_password(password, stored)` разбирает строку через `split("$")`, заново считает контроль и сравнивает через `hmac.compare_digest`, возвращая `bool`. Проверь: `verify_password("пароль", hasher.hash_password("пароль"))` должно быть `True`, а `verify_password("другой", stored)` — `False`. Выведи оба результата.

### Задача 2
Напиши функции `encrypt_data(plaintext, key)` и `decrypt_data(token, key)` на основе `cryptography.fernet.Fernet`. Первая возвращает `Fernet(key).encrypt(plaintext.encode())`, вторая — `Fernet(key).decrypt(token).decode()`. Сгенерируй ключ через `Fernet.generate_key()`, зашифруй строку `"секретное сообщение"`, выведи зашифрованный токен (первые 40 символов) и расшифрованный текст. Убедись, что расшифрованный текст совпадает с исходным.

### Задача 3
Реализуй функцию `hotp(key, counter)` по RFC 4226, как в теории: `struct.pack(">Q", counter)`, HMAC-SHA1, dynamic truncation (offset = digest[-1] & 0x0F), `struct.unpack(">I", digest[offset:offset+4])[0] & 0x7FFFFFFF`, затем `% 1_000_000` и `zfill(6)`. Вызови для `key = b"shared-secret"` и счётчиков 0, 1, 2 и выведи три шестизначных кода. Коды должны отличаться друг от друга.

### Задача 4
Напиши функцию `derive_key(passphrase, salt)`, которая использует `hashlib.scrypt` для выработки 32-байтового ключа: `hashlib.scrypt(passphrase.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)`. Проверь, что при одинаковой пароле и соли ключи совпадают, а при разной соли — отличаются. Выведи оба hex-ключа: `key1`, `key2` и `key3`, где key1 и key2 — от одной пароли, key3 — от другой соли. Соль генерируй `secrets.token_bytes(16)`.

### Задача 5
Напиши функцию `constant_time_equals(a, b)`, которая возвращает `hmac.compare_digest(a, b)`. Продемонстрируй разницу: создай функцию `naive_equals(a, b)` на обычном `==` и сравнение время выполнения для двух длинных строк (1 000 000 символов), отличающихся последним символом: выведи `наивное сравнение: <сек>`, `постоянное время: <сек>` через `time.perf_counter()`. Убедись, что разница видна. Это наглядный пример, почему для секретов используют `compare_digest`.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Разбирай строку: `algo, iterations, salt_hex, digest_hex = stored.split("$")`. Для hex-преобразований используй `bytes.fromhex` и `.hex()`. `verify_password` принимает `password` как str — не забудь `.encode()`.
### Подсказка 2
`Fernet.generate_key()` возвращает байты-ключ; `Fernet(key)` создаёт шифратор. `encrypt` принимает байты, `decrypt` возвращает байты. Выведи `token[:40]` для демонстрации.
### Подсказка 3
Не забудь `import struct`. `digest[-1] & 0x0F` — младшие 4 бита последнего байта. `struct.unpack(">I", ...)` возвращает кортеж — бери `[0]`. TCP-число должно быть примерно 6 цифр.
### Подсказка 4
`hashlib.scrypt` (в Python 3.6+). Параметр `n` — степень двойки; `2**14` — компромисс скорость/безопасность для учебного примера. Возвращает байты — выводи их `.hex()`.
### Подсказка 5
`time.perf_counter()` до и после цикла: `t0 = time.perf_counter(); ...; dt = time.perf_counter() - t0`. Для наглядности повторяй сравнение, например, 50 раз в цикле. `hmac.compare_digest` тоже сравнивает байты/строки.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
import hashlib
import hmac
import secrets

class PasswordHasher:
    ITERATIONS = 600_000

    def hash_password(self, password):
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt, self.ITERATIONS
        )
        return f"pbkdf2_sha256${self.ITERATIONS}${salt.hex()}${digest.hex()}"

    def verify_password(self, password, stored):
        _, _, salt_hex, digest_hex = stored.split("$")
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode(),
            bytes.fromhex(salt_hex), self.ITERATIONS
        )
        return hmac.compare_digest(digest_hex, digest.hex())

h = PasswordHasher()
stored = h.hash_password("пароль")
print(h.verify_password("пароль", stored))
print(h.verify_password("другой", stored))
```

Результат:

```
True
False
```

Что здесь происходит? `hash_password` генерирует свежую соль (16 случайных байт), считает KDF с 600 000 итерациями и упаковывает всё в строку. В `verify_password` мы разбираем строку, восстанавливаем соль и итерации и заново считаем хеш. Сравнение — через `hmac.compare_digest`, чтобы время ответа не зависело от того, совпал ли первый символ. Первая проверка даёт `True`, вторая — `False`. Обрати внимание: при одинаковом пароле и разных солях хеши разные — поэтому соль обязана храниться вместе с хешем. Это стандартный формат хранения паролей в Django (`pbkdf2_sha256$...`).

### Разбор 2
Решение:

```python
from cryptography.fernet import Fernet

def encrypt_data(plaintext, key):
    return Fernet(key).encrypt(plaintext.encode())

def decrypt_data(token, key):
    return Fernet(key).decrypt(token).decode()

key = Fernet.generate_key()
token = encrypt_data("секретное сообщение", key)
print(token[:40])
print(decrypt_data(token, key))
```

Результат (примерно):

```
b'gAAAAAB...'  (первые 40 символов токена)
секретное сообщение
```

Что здесь происходит? `Fernet.generate_key()` создаёт 32-байтовый ключ, закодированный в base64. `encrypt` возвращает токен, который содержит и сам шифротекст, и HMAC-подпись, и время создания — это значит, что подменить или «состарить» токен нельзя. `decrypt` проверяет подпись и расшифровывает. Если данные меняли или ключ не тот — будет `InvalidToken`. В реальном проекте ключ лежит не в коде, а в секретах (урок 2), и каждый сервис получает его из окружения. Fernet — хороший выбор для шифрования строк конфигурации и персональных данных.

### Разбор 3
Решение:

```python
import hashlib
import hmac
import struct

def hotp(key, counter):
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(code % 1_000_000).zfill(6)

key = b"shared-secret"
for i in range(3):
    print(hotp(key, i))
```

Результат (пример):

```
780531
559742
881322
```

Что здесь происходит? HOTP — стандарт одноразовых паролей (RFC 4226). Счётчик упаковывается в 8 байт big-endian (`struct.pack(">Q", counter)`), от него считается HMAC-SHA1. Из дайджеста берём «dynamic truncation»: последний байт задаёт смещение `offset`, из него вырезаем 4 байта, приводим к беззнаковому int (31 бит) и берём остаток от деления на 1 000 000. `zfill(6)` дополняет нулями до шести цифр. Коды для разных счётчиков отличаются. HOTP используется в Google Authenticator-подобных приложениях; TOTP — та же идея, но счётчиком служит время, делённое на период.

### Разбор 4
Решение:

```python
import hashlib
import secrets

def derive_key(passphrase, salt):
    return hashlib.scrypt(
        passphrase.encode(), salt=salt,
        n=2**14, r=8, p=1, dklen=32,
    )

salt1 = secrets.token_bytes(16)
salt2 = secrets.token_bytes(16)
key1 = derive_key("Пароль", salt1)
key2 = derive_key("Пароль", salt1)
key3 = derive_key("Пароль", salt2)

print("key1:", key1.hex())
print("key2:", key2.hex())
print("key3:", key3.hex())
```

Что здесь происходит? `hashlib.scrypt` — KDF, устойчивая к подбору на GPU и ASIC: она требует много памяти (параметр `n` — параметр линейного размера). `key1` и `key2` одинаковы, потому что пароль и соль совпадают — это свойство детерминизма, нужно для проверки. `key3` отличается, потому что соль другая. Ключ, выработанный из пароля через KDF, можно использовать для шифрования (например, как ключ Fernet после base64). Хранить вместе с ним нужно соль и параметры (n, r, p), чтобы воспроизвести ключ позже.

### Разбор 5
Решение:

```python
import hmac
import time

def naive_equals(a, b):
    return a == b

def constant_time_equals(a, b):
    return hmac.compare_digest(a, b)

a = "A" * 1_000_000
b = "A" * 999_999 + "B"

t0 = time.perf_counter()
for _ in range(50):
    naive_equals(a, b)
t1 = time.perf_counter()
for _ in range(50):
    constant_time_equals(a, b)
t2 = time.perf_counter()

print(f"наивное сравнение: {t1 - t0:.4f} сек")
print(f"постоянное время: {t2 - t1:.4f} сек")
```

Что здесь происходит? Наивное `==` сравнивает строки посимвольно и останавливается на первом несовпадении — а оно у нас почти в конце, поэтому сравнение занимает долго. `hmac.compare_digest` всегда просматривает строку целиком, поэтому его время практически не зависит от того, где «порча». В реальности атакующий может замерять время ответа и по нему подбирать секрет символ за символом; именно поэтому для сравнения секретов, хешей и подписей используют функции с постоянным временем. Это одна из причин, почему нельзя проверять HMAC через обычный `==`.
<!--/SOLUTION-->

<!--QUIZ-->
Чем хеширование отличается от шифрования?
- Хеширование одностороннее, шифрование обратимо
- Это одно и то же
- Шифрование одностороннее
* Правильный ответ: Хеширование одностороннее, шифрование обратимо
Из хеша нельзя восстановить исходные данные, расшифровать можно.

Почему нельзя хранить пароль как sha256 без соли?
- Такой хеш считается слишком быстро, пароль легко перебрать
- Он занимает много места
- SHA256 не работает в Python
* Правильный ответ: Такой хеш считается слишком быстро, пароль легко перебрать
Быстрые хеши позволяют перебирать миллиарды вариантов в секунду.

Что такое соль в контексте паролей?
- Случайное значение, добавляемое к паролю перед хешированием
- Секретный ключ шифрования
- Пароль в открытом виде
* Правильный ответ: Случайное значение, добавляемое к паролю перед хешированием
Соль делает одинаковые пароли разными хешами.

Зачем нужен KDF вроде pbkdf2?
- Чтобы замедлить перебор паролей
- Чтобы ускорить вход
- Чтобы сжать хеш
* Правильный ответ: Чтобы замедлить перебор паролей
Тысячи итераций делают одну попытку проверки дорогой.

Что делает Fernet?
- Шифрует данные с аутентификацией
- Только хеширует
- Только сжимает
* Правильный ответ: Шифрует данные с аутентификацией
Токен Fernet содержит шифротекст и HMAC-подпись.

Что вернёт Fernet(key).decrypt(token), если ключ не тот?
- Исключение InvalidToken
- None
- Пустую строку
* Правильный ответ: Исключение InvalidToken
Подпись не сойдётся — расшифровка невозможна.

Зачем использовать hmac.compare_digest вместо ==?
- Чтобы время сравнения не зависело от данных
- Чтобы ускорить код
- Чтобы защититься от переполнения
* Правильный ответ: Чтобы время сравнения не зависело от данных
Постоянное время не выдаёт атакующему информацию по таймингу.

Что вычисляет HOTP?
- Одноразовый пароль из ключа и счётчика
- Хеш файла
- Ключ шифрования
* Правильный ответ: Одноразовый пароль из ключа и счётчика
HOTP = HMAC + счётчик; TOTP — то же, но по времени.

Что должен использовать для генерации ключей и соли?
- Модуль secrets
- Модуль random
- time.time()
* Правильный ответ: Модуль secrets
random и time предсказуемы и непригодны для криптографии.

Какая библиотека считается основной для криптографии в Python?
- cryptography
- json
- requests
* Правильный ответ: cryptography
cryptography даёт Fernet, асимметричные алгоритмы, KDF и другое.
<!--/QUIZ-->
