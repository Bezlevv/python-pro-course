---
title: Аутентификация: Token и JWT, права
summary: TokenAuthentication, SimpleJWT (access/refresh), permissions: IsAuthenticated, IsAdminUser и свои классы прав.
order: 4
duration: 35 мин
difficulty: advanced
tags: drf, auth, jwt, permissions, token
---

Почти ни одно API не публикует данные всем подряд. Нужно понимать, кто обращается к серверу, и ограничивать доступ. В этом уроке мы разберёмся с двумя механизмами аутентификации в DRF — **Token Authentication** и **JWT** — и научимся управлять правами (permissions).

## Аутентификация vs права

- **Аутентификация** отвечает на вопрос «кто ты?» — проверяет учётные данные и опознаёт пользователя.
- **Авторизация (права)** отвечает на вопрос «что тебе можно?» — проверяет, есть ли у пользователя доступ к действию.

В DRF это два независимых слоя: аутентификация кладёт пользователя в `request.user`, а permissions решают, пропускать ли запрос дальше.

## Token Authentication

Простой способ: при логине выдать клиенту токен — случайную строку. Клиент отправляет её в заголовке `Authorization: Token <токен>`.

Настройка:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework.authtoken",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}
```

Примени миграции (`python manage.py migrate`) — появится таблица `authtoken_token`. Токен можно создать в консоли:

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.create_user("anna", password="secret123")
token, created = Token.objects.get_or_create(user=user)
print(token.key)  # например, "b8f3a1c9..."
```

Официальный способ получить токен через API — вьюха `obtain_auth_token`:

```python
# urls.py
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("api-token-auth/", obtain_auth_token),
]
```

Теперь клиент отправляет POST с `username` и `password`, а в ответ получает токен.

## JWT через SimpleJWT

**JWT** (JSON Web Token) — компактный токен с тремя частями: заголовок, полезная нагрузка и подпись. В отличие от обычного токена, JWT хранит данные (например, id пользователя) прямо внутри себя, а сервер подписывает его секретным ключом. Это позволяет не хранить токены в базе.

Устанавливаем и настраиваем:

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
```

Подключаем маршруты:

```python
# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
```

Клиент логинится:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "anna", "password": "secret123"}'
```

Ответ:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

Теперь каждый запрос отправляется с access-токеном в заголовке:

```
Authorization: Bearer <access>
```

Access-токен живёт недолго (по умолчанию 5 минут, мы поставили 30). Когда он истекает, клиент обновляет его через refresh-токен:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "<refresh-токен>"}'
```

Такой подход безопаснее: скомпрометированный access-токен быстро протухнет, а refresh-токен можно отозвать.

## Права (permissions)

Права проверяются классами из `rest_framework.permissions`:

- `AllowAny` — всем можно (по умолчанию);
- `IsAuthenticated` — только залогиненным;
- `IsAdminUser` — только админам (`is_staff=True`);
- `IsAuthenticatedOrReadOnly` — читать могут все, менять — только залогиненным.

Глобально:

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

Локально — на уровне вьюхи:

```python
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
```

## Свои классы прав

Если встроенных мало, пишем свой класс. Метод `has_permission` проверяет доступ к действию вообще, `has_object_permission` — к конкретному объекту:

```python
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.owner == request.user
```

Применение:

```python
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

## Итог

Token Authentication — просто и наглядно, но токены хранятся в базе. JWT — современный стандарт для API и SPA: без хранения, с короткими access и обновляемыми refresh-токенами. Права ограничивают доступ через встроенные или собственные классы permissions. В следующем уроке займёмся фильтрацией, поиском и пагинацией.

<!--TASK-->
### Задача 1
Настрой Token Authentication в проекте: добавь `rest_framework.authtoken` в `INSTALLED_APPS`, подключи `TokenAuthentication` как `DEFAULT_AUTHENTICATION_CLASSES` и выполни миграции. Создай пользователя через `createsuperuser` и получи его токен в Django shell (`Token.objects.get_or_create(user=...)`). Выведи токен на экран.

### Задача 2
Подключи в `urls.py` вьюху `obtain_auth_token` по адресу `/api-token-auth/`. Через curl отправь POST с `username` и `password`, получи токен в ответе. Затем отправь GET-запрос к любому своему эндпоинту с заголовком `Authorization: Token <токен>` и убедись, что он проходит.

### Задача 3
Установи `djangorestframework-simplejwt`, пропиши `JWTAuthentication` в настройки. Добавь маршруты `TokenObtainPairView` (`/api/token/`) и `TokenRefreshView` (`/api/token/refresh/`). Через curl получи access и refresh токены. Убедись, что access-токен с `Bearer`-префиксом принимается.

### Задача 4
Установи `DEFAULT_PERMISSION_CLASSES` в `IsAuthenticated`. Убедись, что без токена запрос к `/api/books/` возвращает `401 Unauthorized`, а с токеном — `200 OK`. Затем добавь permission `IsAuthenticatedOrReadOnly` на уровне одного из эндпоинтов.

### Задача 5
Создай класс прав `IsOwnerOrReadOnly` (как в теории) и добавь его в `permission_classes` для `BookViewSet`. Добавь модели `Book` поле `owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)`. Убедись, что невладелец не может обновить или удалить чужую книгу (получит `403 Forbidden`).
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`authtoken` — готовое приложение DRF: добавь его в `INSTALLED_APPS` и выполни `python manage.py migrate`. Создай пользователя: `python manage.py createsuperuser`. В shell: `from rest_framework.authtoken.models import Token; token, created = Token.objects.get_or_create(user=user)`.

### Подсказка 2
Импортируй `obtain_auth_token` из `rest_framework.authtoken.views`. curl: `curl -X POST http://127.0.0.1:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username": "...", "password": "..."}'`. Запрос с токеном: добавь заголовок `Authorization: Token <ключ>`.

### Подсказка 3
Пакет называется `djangorestframework-simplejwt`, импорты — из `rest_framework_simplejwt.views`. В настройках подключи `JWTAuthentication` вместо `TokenAuthentication`. В curl используй заголовок `Authorization: Bearer eyJ...`.

### Подсказка 4
Глобально: `REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]}`. Что касается вьюхи — задай `permission_classes = [IsAuthenticatedOrReadOnly]` в классе.

### Подсказка 5
`BasePermission` — из `rest_framework.permissions`. Метод `has_object_permission` получает `request`, `view` и `obj`. Для модели: `from django.contrib.auth.models import User`, поле `owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)`. Не забудь `makemigrations` и `migrate`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework.authtoken",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}
```

```bash
python manage.py migrate
python manage.py createsuperuser
```

```python
# shell
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username="anna")
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

Что здесь происходит? `authtoken` добавляет таблицу токенов в БД. `Token.objects.get_or_create` возвращает пару: сам токен и флаг, был ли он создан сейчас. Ключ токена — случайная строка; её сохраняет клиент. Обрати внимание: каждый пользователь может иметь только один токен, поэтому повторный вызов вернёт тот же ключ.

### Разбор 2
Решение:

```python
# urls.py
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ...
    path("api-token-auth/", obtain_auth_token),
]
```

```bash
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"username": "anna", "password": "secret123"}'
```

Ответ:

```json
{"token": "b8f3a1c9d2e4f5..."}
```

Теперь запрос с токеном:

```bash
curl -H "Authorization: Token b8f3a1c9d2e4f5..." \
     http://127.0.0.1:8000/api/books/
```

Что здесь происходит? `obtain_auth_token` проверяет логин и пароль, и если они верны — возвращает токен пользователя. Сервер сверяет заголовок `Authorization: Token ...` с таблицей токенов и опознаёт пользователя в `request.user`. Если токен неверный, DRF вернёт `401`.

### Разбор 3
Решение:

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
```

```python
# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
```

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "anna", "password": "secret123"}'
```

Что здесь происходит? `TokenObtainPairView` возвращает пару токенов. `access` используется для запросов, `refresh` — для обновления access. Запрос с токеном: `Authorization: Bearer <access>`. JWTAuthentication проверяет подпись и срок действия, поэтому база данных не нужна.

### Разбор 4
Решение:

```python
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

```bash
curl http://127.0.0.1:8000/api/books/
# 401 Unauthorized

curl -H "Authorization: Bearer <access>" \
     http://127.0.0.1:8000/api/books/
# 200 OK
```

Что здесь происходит? `IsAuthenticated` разрешает запрос только если `request.user` аутентифицирован (не `AnonymousUser`). Без токена DRF возвращает `401 Unauthorized`. `IsAuthenticatedOrReadOnly` пропускает все безопасные методы (GET, HEAD, OPTIONS) без аутентификации, а остальные — только для залогиненных.

### Разбор 5
Решение:

```python
# books/permissions.py
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.owner == request.user
```

```python
# books/models.py
from django.contrib.auth.models import User


class Book(models.Model):
    ...
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
```

```python
# books/views.py
from .permissions import IsOwnerOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

Что здесь происходит? `has_object_permission` вызывается для операций с конкретным объектом: PUT, PATCH, DELETE. Чтение разрешено всем аутентифицированным, а изменение — только если `obj.owner == request.user`. Иначе DRF вернёт `403 Forbidden`.
<!--/SOLUTION-->

<!--QUIZ-->
Что отвечает на вопрос «кто ты?»?
- Аутентификация
- Авторизация
- Сериализация
* Правильный ответ: Аутентификация
Аутентификация проверяет учётные данные и опознаёт пользователя.

Как передаётся Token Authentication в запросе?
- В заголовке Authorization: Token <токен>
- В теле запроса как text
- В файле cookie без шифрования
* Правильный ответ: В заголовке Authorization: Token <токен>
Клиент отправляет токен в заголовке Authorization с префиксом Token.

Что возвращает TokenObtainPairView?
- Пару токенов: access и refresh
- Один бессрочный токен
- Только refresh-токен
* Правильный ответ: Пару токенов: access и refresh
TokenObtainPairView выдаёт access для запросов и refresh для обновления.

Какой префикс использует JWT в заголовке Authorization?
- Bearer
- Token
- JWT
* Правильный ответ: Bearer
Заголовок выглядит так: Authorization: Bearer eyJhbGci...

Сколько живёт access-токен по умолчанию в SimpleJWT?
- 5 минут
- 30 дней
- 1 год
* Правильный ответ: 5 минут
По умолчанию 5 минут; срок настраивается через SIMPLE_JWT.

Какой класс разрешает доступ только залогиненным?
- IsAuthenticated
- AllowAny
- IsOwnerOrReadOnly
* Правильный ответ: IsAuthenticated
IsAuthenticated проверяет, что request.user — не AnonymousUser.

Что вернёт запрос без токена при IsAuthenticated?
- 401 Unauthorized
- 200 OK
- 302 Redirect
* Правильный ответ: 401 Unauthorized
Отсутствие аутентификации при требуемом праве даёт 401.

Какой метод должен реализовать свой класс прав для проверки объекта?
- has_object_permission
- check_object
- validate_permission
* Правильный ответ: has_object_permission
Метод получает request, view и obj и возвращает True/False.

Что делает refresh-токен?
- Обновляет access-токен после истечения
- Создаёт нового пользователя
- Меняет пароль
* Правильный ответ: Обновляет access-токен после истечения
POST на /api/token/refresh/ с refresh-токеном выдаёт новый access.

Что возвращает сервер, если владелец пытается изменить чужой объект?
- 403 Forbidden
- 200 OK
- 400 Bad Request
* Правильный ответ: 403 Forbidden
Права не прошли — запрет доступа (403).
<!--/QUIZ-->
