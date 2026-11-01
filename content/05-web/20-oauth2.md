---
title: OAuth2: потоки авторизации и интеграции
summary: Как работает OAuth2: authorization code, PKCE, client credentials, refresh-токены, интроспекция и вход через GitHub, Google и ВКонтакте.
order: 20
duration: 60 мин
difficulty: advanced
tags: oauth2, openid, jose, социальный вход
---

Ты уже умеешь авторизовать пользователей с помощью паролей и JWT-токенов (урок 12). Но настоящие приложения редко изобретают собственный вход: гораздо удобнее дать пользователю войти через GitHub, Google или ВКонтакте. Именно эту задачу решает **OAuth 2.0** — открытый стандарт децентрализованной авторизации. В этом уроке ты разберёшься, как устроены его потоки, научишься подключать социальный вход и, главное, защищать свои интеграции.

## Зачем нужен OAuth2

Представь сервис, который хочет «Войти через GitHub». Если бы он попросил твой пароль от GitHub — это была бы катастрофа: приложение получило бы полный доступ к твоему аккаунту, не смогло бы ограничить права, а ты не смог бы отозвать доступ, не сменив пароль. OAuth2 решает это через **делегирование**: пользователь не отдаёт пароль, а выдаёт приложению **токен доступа** (access token) — строку с ограниченными правами и сроком жизни.

В OAuth2 участвуют четыре роли:

- **Resource Owner** — владелец данных: твой пользователь;
- **Client** — приложение, которое хочет получить доступ (наш сайт или мобильное приложение);
- **Authorization Server** — провайдер, который выпускает токены: GitHub, Google, ВКонтакте;
- **Resource Server** — API, которое отдаёт данные по токену: например, `https://api.github.com`.

Токен сопровождается **scopes** — областями доступа: `user:email`, `read:profile`, `offline_access`. Пользователь видит список прав в окне согласия и может отказать.

## Типы клиентов и потоки (flows)

Клиенты бывают двух типов:

- **confidential** — серверные приложения, которые могут хранить секрет (client_secret): у них есть бэкенд;
- **public** — одностраничные приложения (SPA) и мобильные: секрет хранить нельзя, код виден пользователю.

Поток (грант) выбирают по типу клиента:

| Поток | Когда использовать | Кто секрет |
|---|---|---|
| Authorization Code | веб-приложения с серверной частью | confidential |
| Authorization Code + PKCE | SPA, мобильные, и рекомендовано всем | public |
| Client Credentials | machine-to-machine: микросервисы, CI, фоновые задачи | confidential |
| Refresh Token | продлить сессию без повторного входа | любой |
| Device Authorization | устройства без браузера (телевизоры, CLI) | по типу устройства |

## Поток Authorization Code

Это самый распространённый поток. Разберём по шагам (клиент — наш сайт, провайдер — GitHub):

1. Клиент **перенаправляет браузер** пользователя на Authorization Server с параметрами: `client_id`, `redirect_uri`, `scope`, `state`, `response_type=code`.
2. Пользователь входит в GitHub и соглашается.
3. GitHub редиректит обратно на `redirect_uri` с однимразовым **кодом авторизации** (`?code=...&state=...`).
4. Клиент обменивает код на токены: серверный POST-запрос на эндпоинт `/token` с `client_id`, `client_secret`, `code`, `redirect_uri`, `grant_type=authorization_code`.
5. Authorization Server отвечает JSON: `access_token`, `token_type`, `refresh_token`, `expires_in`.
6. Клиент вызывает API с заголовком `Authorization: Bearer <access_token>`.
7. Когда токен истекает — клиент использует `refresh_token`.

Соберём URL авторизации:

```python
import urllib.parse

authorize_url = "https://github.com/login/oauth/authorize"
params = {
    "client_id": "Iv1.ваш_client_id",
    "redirect_uri": "https://app.example.com/callback",
    "response_type": "code",
    "scope": "user:email",
    "state": "ny9k2p1z",
}
print(authorize_url + "?" + urllib.parse.urlencode(params))
```

Обмен кода на токены через `httpx`:

```python
import httpx

resp = httpx.post(
    "https://github.com/login/oauth/access_token",
    data={
        "client_id": "Iv1.ваш_client_id",
        "client_secret": "секрет",
        "code": "временный-код-из-callback",
        "redirect_uri": "https://app.example.com/callback",
        "grant_type": "authorization_code",
    },
    headers={"Accept": "application/json"},
)
tokens = resp.json()
print(tokens["access_token"], tokens["expires_in"])
```

Код одноразовый: если перехватчик успеет применить его раньше — клиент получит ошибку `invalid_grant`.

## PKCE: защита публичных клиентов

У SPA и мобильных приложений нет секрета — код авторизации может перехватить вредоносное приложение. **PKCE** (RFC 7636) спасает даже без секрета. Идея:

1. Клиент заранее генерирует случайную строку **code_verifier** (43–128 символов);
2. Вычисляет **code_challenge** — хэш verifier'а (S256 или plain);
3. Передаёт challenge в URL авторизации;
4. При обмене кода отправляет и verbifier;
5. Authorization Server проверяет: совпадает ли challenge с хэшем присланного verifier. Перехватчик без verifier не сможет обменять код.

Пример генерации (исполняемый):

```python
import base64
import hashlib
import secrets

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"


def generate_code_verifier(length: int = 64) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def compute_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


verifier = generate_code_verifier()
challenge = compute_code_challenge(verifier)
print(verifier, challenge, sep="\n")
```

Теперь в URL авторизации добавятся `code_challenge` и `code_challenge_method=S256`, а в POST-обмен — `code_verifier`. Даже если злоумышленник перехватит код, без verifier он ему бесполезен.

## Client Credentials

Этот поток не про пользователей: он для сервисных аккаунтов. Сервис авторизуется сам, без человека:

```python
import httpx

resp = httpx.post(
    "https://oauth.example.com/token",
    data={
        "grant_type": "client_credentials",
        "client_id": "сервисный-id",
        "client_secret": "секрет-сервиса",
        "scope": "metrics:read",
    },
)
token = resp.json()["access_token"]
```

Применяется в фоновых воркерах, интеграциях «сервер–сервер», где не нужен пользовательский контекст.

## Refresh-токены

Access-токены живут недолго (15–60 минут), чтобы ограничить ущерб от утечки. Чтобы не заставлять пользователя входить каждый час, выдают **refresh_token** — долгоживущий (дни/месяцы). Клиент обменивает его на новый access-токен:

```python
import httpx

resp = httpx.post(
    "https://oauth.example.com/token",
    data={
        "grant_type": "refresh_token",
        "refresh_token": "старый-refresh-токен",
        "client_id": "client-id",
        "client_secret": "секрет",
    },
)
new_tokens = resp.json()
print(new_tokens["access_token"])
```

Правила безопасности: храни refresh-токен только на сервере, в защищённом хранилище; используй **ротацию** — каждая выдача нового refresh-токена отзывает старый; при подозрении на утечку отзывай токен (эндпоинт `/revoke`). У Google refresh-токен получают только с `access_type=offline&prompt=consent`, и только если приложение привязано к серверной части.

## Проверка токенов: интроспекция и JOSE

Как Resource Server проверяет предъявленный токен? Два пути.

**1. Интроспекция (RFC 7662).** Resource Server отправляет токен на эндпоинт `/introspect` и получает JSON со статусом:

```python
import httpx

resp = httpx.post(
    "https://oauth.example.com/introspect",
    data={"token": "непрозрачный-токен", "client_id": "api", "client_secret": "секрет"},
)
print(resp.json())
# {"active": true, "scope": "read:profile", "client_id": "...", "exp": 1730000000}
```

**2. Локальная проверка JWT.** Многие провайдеры выпускают токены как **JWT** — подписанный JSON (семейство стандартов **JOSE**: JWT, JWS, JWK, JWKS). Сервер может проверить подпись сам, без сети:

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "секрет-подписи"  # на практике — публичный ключ из JWKS

# выпуск токена (это делает Authorization Server)
payload = {
    "iss": "https://oauth.example.com",
    "sub": "user-42",
    "scope": "read:profile",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
}
token = jwt.encode(payload, SECRET, algorithm="HS256")

# проверка (это делает Resource Server)
decoded = jwt.decode(token, SECRET, algorithms=["HS256"], issuer="https://oauth.example.com")
print(decoded["sub"])  # user-42
```

В продакшене провайдеры используют асимметричный алгоритм **RS256**: ключ подписи держит Authorization Server, а публичный ключ публикуется по адресу из JWKS (`/.well-known/jwks.json`). JWК — это JSON с «отпечатком» ключа, JWKS — коллекция таких ключей. Проверка по JWKS — стандартный приём в реальных проектах.

## OpenID Connect

OAuth2 авторизует доступ к данным, но не «говорит», кто пользователь. **OpenID Connect (OIDC)** — надстройка над OAuth2: в ответе появляется **id_token** (JWT с утверждениями о личности: `sub`, `email`, `name`, `email_verified`), плюс эндпоинт `userinfo` и endpoint discovery (`https://provider/.well-known/openid-configuration`). Если ты видишь `openid` в scope — это OIDC. Пример получения профиля:

```python
import httpx

resp = httpx.get(
    "https://openidconnect.googleapis.com/v1/userinfo",
    headers={"Authorization": "Bearer " + access_token},
)
print(resp.json())  # {"sub": "...", "name": "Аня", "email": "anya@example.com"}
```

## Интеграции: GitHub, Google, ВКонтакте

Три популярных провайдера — ключевые адреса:

| Провайдер | URL авторизации | Эндпоинт токена | Профиль | Scopes |
|---|---|---|---|---|
| GitHub | `https://github.com/login/oauth/authorize` | `https://github.com/login/oauth/access_token` | `https://api.github.com/user` | `read:user`, `user:email` |
| Google | `https://accounts.google.com/o/oauth2/v2/auth` | `https://oauth2.googleapis.com/token` | `https://openidconnect.googleapis.com/v1/userinfo` | `openid email profile` |
| ВКонтакте | `https://oauth.vk.com/authorize` | `https://oauth.vk.com/access_token` | `https://api.vk.com/method/users.get` | `email`, `phone` |

Особенности:

- **GitHub**: ответ по умолчанию в query-строке, чтобы получить JSON — заголовок `Accept: application/json`; не выдаёт refresh-токены (для продления — повторная авторизация с `prompt=consent`).
- **Google**: требует `access_type=offline` для refresh-токена; scope `openid` включает id_token; возвращает `expires_in`.
- **ВКонтакте**: authorize-URL часто открывается в отдельном окне (там есть кнопка «Разрешить»), callback идёт с `code` + `state`; для расшифровки email нужен scope `email`. ВК также умеет в callback-подпись (`sig`) — но это отдельный механизм, его не путай с OAuth2.

Универсальный каркас клиента можно вынести в класс:

```python
import httpx


class OAuthProvider:
    def __init__(self, authorize_url, token_url, client_id, client_secret):
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret

    def exchange_code(self, code, redirect_uri, code_verifier=None):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if code_verifier:
            data["code_verifier"] = code_verifier
        resp = httpx.post(self.token_url, data=data, headers={"Accept": "application/json"})
        resp.raise_for_status()
        return resp.json()


github = OAuthProvider(
    "https://github.com/login/oauth/authorize",
    "https://github.com/login/oauth/access_token",
    "Iv1.client_id",
    "секрет",
)
```

## Безопасность интеграций

Три правила, которые закрывают большинство уязвимостей:

1. **state против CSRF и перехвата.** `state` — случайная строка, которая связывает запрос с ответом. До редиректта на провайдера клиент кладёт её в сессию, а в callback сверяет. Без проверки злоумышленник может подменить код и войти в чужой аккаунт. Проверка всегда должна быть точной (`==`), без префиксных совпадений.

2. **redirect_uri — строгая валидация.** Провайдер должен разрешать только точно зарегистрированные URI. Сравнение «начинается с» опасно: `https://app.example.com.evil.io` начинается с `https://app.example.com`? Нет, но `https://app.example.com` — префикс `https://app.example.com.evil.io`, так что префиксная проверка по «началу строки» пропустит злоумышленника. Сравнивай полное равенство. Никогда не допускай подстановку `redirect_uri` из запроса пользователя без сверки с белым списком.

3. **Секреты — только на сервере.** `client_secret` не должен попадать в браузер, в Git-репозиторий или в логи. Храни его в переменных окружения (`.env`, secrets manager). Токены тоже не логируй, а `expires_in` используй, чтобы не держать токен дольше нужного.

Напомним: весь обмен идёт по HTTPS; код авторизации — одноразовый; публичный клиент обязан использовать PKCE.

## Итог

Ты познакомился с ролями OAuth2, потоками authorization code, PKCE и client credentials, разобрался с refresh-токенами, интроспекцией и JOSE/JWT, узнал, как подключить вход через GitHub, Google и ВКонтакте, и запомнил три столпа безопасности: state, redirect_uri и секреты. Теперь закрепим всё задачами.

<!--TASK-->
### Задача 1
Реализуй две функции для PKCE в файле `pkce.py`: `generate_code_verifier(length=64)` — возвращает случайную строку длиной `length` из символов алфавита `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~`, и `compute_code_challenge(verifier)` — возвращает SHA-256-хэш верификатора в кодировке base64url без символов `=` на конце. Затем напиши в файле `test_pkce.py` pytest-тесты: (1) верификатор имеет длину 64 и состоит только из разрешённых символов; (2) вызов `compute_code_challenge` для одной и той же строки всегда возвращает одно и то же значение; (3) для примера из RFC 7636 — верификатор `dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk` должен давать challenge `E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM`. Запусти `python -m pytest test_pkce.py -q` и убедись, что все тесты зелёные.

### Задача 2
Напиши в файле `authorize.py` функцию `build_authorize_url(authorize_url, client_id, redirect_uri, scope, state, code_challenge=None)`, которая собирает URL авторизации с параметрами `client_id`, `redirect_uri`, `response_type=code`, `scope`, `state`, а если передан `code_challenge` — ещё и `code_challenge` с `code_challenge_method=S256`. Параметры должны быть корректно URL-закодированы. В файле `test_authorize.py` напиши pytest-тесты: (1) URL содержит все обязательные параметры и `response_type=code`; (2) при передаче `code_challenge` в URL появляются `code_challenge` и `code_challenge_method=S256`; (3) пробел в `redirect_uri` кодируется (строка `Callback URI` превращается в `Callback%20URI`, подставь значение с пробелом для проверки); (4) `state` передаётся в URL без изменений. Запусти тесты и убедись, что они проходят.

### Задача 3
Создай в файле `exchange.py` класс `OAuthError(Exception)` и функцию `exchange_code(client, code, redirect_uri, code_verifier=None)`, которая принимает `httpx.Client` (с настроенным transport), делает POST-запрос на относительный путь `/token` с параметрами `grant_type=authorization_code`, `code`, `redirect_uri`, `client_id`, `client_secret` (их передай отдельными аргументами функции) и `code_verifier` (если передан). Если в ответе есть ключ `error` — подними `OAuthError` с текстом ошибки; иначе верни JSON-ответ как dict. В файле `test_exchange.py` напиши два pytest-теста с `httpx.MockTransport`: в первом эндпоинт `/token` проверяет, что получил `grant_type=authorization_code` и `code_verifier`, и возвращает `{"access_token": "...", "expires_in": 3600}` — функция должна вернуть этот dict; во втором эндпоинт возвращает `{"error": "invalid_grant", "error_description": "code expired"}` — функция должна поднять `OAuthError` с этим текстом. Запусти тесты.

### Задача 4
В файле `validate.py` напиши две функции: `check_state(received, expected)` — возвращает `True`, только если строки совпадают точно; и `check_redirect_uri(uri, allowed_uri)` — возвращает `True`, только если `uri` точно равен `allowed_uri` (никакого префиксного сравнения). В файле `test_validate.py` напиши pytest-тесты: (1) `check_state("abc", "abc")` → `True`, а `check_state("abc", "abd")` → `False`; (2) `check_redirect_uri("https://app.example.com/cb", "https://app.example.com/cb")` → `True`; (3) `check_redirect_uri("https://app.example.com.evil.io/cb", "https://app.example.com/cb")` → `False` (это ключевая проверка против редирект-атак); (4) `check_redirect_uri("https://app.example.com/cb/extra", "https://app.example.com/cb")` → `False`. Запусти тесты и убедись, что все четыре проходят.

### Задача 5
Напиши скрипт `session.py`, который моделирует сессию с refresh-токеном. Секретом подписи задай строку `"dev-secret"`. Напиши функции: `issue_access_token(sub, secret, lifetime_minutes=30)` — выпускает JWT с полями `sub`, `scope: "read:profile"`, `iat`, `exp` (через `datetime.now(timezone.utc)`); `introspect(token, secret)` — декодирует токен и возвращает dict с полями `active: True`, `sub`, `exp`; если токен просрочен или подпись неверна — возвращает `{"active": False}`. Затем в `if __name__ == "__main__":` выпусти токен и напечатай результат `introspect` для него. Чтобы показать обработку просрочки, выпусти ещё один токен с `lifetime_minutes=-1` (его `exp` окажется в прошлом) и убедись, что `introspect` вернул `active: False`. В выводе должно быть два print-блока: `{'active': True, ...}` и `{'active': False}`. Запусти скрипт и убедись, что вывод соответствует ожидаемому.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Для «разрешённых символов» просто сравнивай каждый символ верификатора с множеством из алфавита: `set(verifier) <= set(ALPHABET)`. Для base64url без `=` используй `base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")`. Хэш — `hashlib.sha256(verifier.encode("ascii")).digest()`. В тесте 3 сверяйся с точными строками из RFC 7636.

### Подсказка 2
Используй `urllib.parse.urlencode(params)` — он сам кодирует пробелы и спецсимволы. В тесте 3 подставь `redirect_uri="https://example.com/Callback URI"` и проверь, что `Callback%20URI` присутствует в URL. Не забудь, что `response_type=code` должен попасть в параметры. `code_challenge_method` добавляй только вместе с `code_challenge`.

### Подсказка 3
`httpx.MockTransport` заменяет сеть: `client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://provider.example.com")`. В handler-функции читай `request.url.path`, `request.read()` или `request.content.decode()` для тела запроса и возвращай `httpx.Response(200, json={...})`. Ошибку поднимай до возврата: `if payload.get("error"): raise OAuthError(payload["error_description"])`.

### Подсказка 4
Сравнивай только через оператор `==`. Внимательно: `"https://app.example.com.evil.io/cb" == "https://app.example.com/cb"` → `False` само по себе, но если бы ты использовал `uri.startswith(allowed_uri)` — вернулось бы `True`. Важно проверить именно точное равенство, включая полный путь.

### Подсказка 5
Для эмуляции просрочки не используй паузы: просто передай `lifetime_minutes=-1`, и `exp` окажется в прошлом. В `introspect` лови `jwt.ExpiredSignatureError` и `jwt.InvalidTokenError` отдельно. Вспомни: `datetime.now(timezone.utc) + timedelta(minutes=lifetime_minutes)` — там `timedelta` из модуля `datetime`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```python
# pkce.py
import base64
import hashlib
import secrets

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"


def generate_code_verifier(length: int = 64) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def compute_code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
```

```python
# test_pkce.py
from pkce import ALPHABET, compute_code_challenge, generate_code_verifier


def test_verifier_length_and_alphabet():
    verifier = generate_code_verifier(64)
    assert len(verifier) == 64
    assert set(verifier) <= set(ALPHABET)


def test_challenge_is_deterministic():
    verifier = generate_code_verifier()
    assert compute_code_challenge(verifier) == compute_code_challenge(verifier)


def test_rfc7636_example():
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    assert compute_code_challenge(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```

Запуск: `python -m pytest test_pkce.py -q` → `3 passed`. Что здесь происходит? `secrets.choice` — криптографически безопасный генератор случайных символов. `rstrip(b"=")` убирает паддинг base64, как требует RFC 7636. Тест с примером из RFC — эталон: если он проходит, реализация соответствует стандарту.

### Разбор 2
Решение:

```python
# authorize.py
import urllib.parse


def build_authorize_url(authorize_url, client_id, redirect_uri, scope, state, code_challenge=None):
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
    }
    if code_challenge is not None:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return authorize_url + "?" + urllib.parse.urlencode(params)
```

```python
# test_authorize.py
from authorize import build_authorize_url


def test_required_params_present():
    url = build_authorize_url(
        "https://github.com/login/oauth/authorize", "client-1",
        "https://app.example.com/cb", "user:email", "st-9",
    )
    assert "client_id=client-1" in url
    assert "response_type=code" in url
    assert "scope=user%3Aemail" in url
    assert "state=st-9" in url


def test_pkce_params_added_when_challenge_given():
    url = build_authorize_url(
        "https://oauth.example.com/auth", "c2",
        "https://app.example.com/cb", "openid", "s1", code_challenge="chall",
    )
    assert "code_challenge=chall" in url
    assert "code_challenge_method=S256" in url


def test_redirect_uri_is_urlencoded():
    url = build_authorize_url(
        "https://oauth.example.com/auth", "c3",
        "https://example.com/Callback URI", "read", "s2",
    )
    assert "Callback%20URI" in url
    assert "Callback URI" not in url


def test_state_preserved_exactly():
    url = build_authorize_url(
        "https://oauth.example.com/auth", "c4",
        "https://app.example.com/cb", "read", "a b c",
    )
    assert "state=a%20b%20c" in url
```

Запуск: `python -m pytest test_authorize.py -q` → `4 passed`. `urlencode` кодирует и `:`, и пробелы — поэтому `scope=user:email` превращается в `scope=user%3Aemail`, а пробелы — в `%20`. Внимание: `state` тоже кодируется, но именно это и нужно — при разборе URL браузер декодирует его обратно.

### Разбор 3
Решение:

```python
# exchange.py
import httpx


class OAuthError(Exception):
    pass


def exchange_code(client, code, redirect_uri, client_id, client_secret, code_verifier=None):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    resp = client.post("/token", data=data)
    payload = resp.json()
    if payload.get("error"):
        raise OAuthError(payload.get("error_description", payload["error"]))
    return payload
```

```python
# test_exchange.py
import httpx
import pytest

from exchange import OAuthError, exchange_code


def test_exchange_success():
    def handler(request):
        assert request.url.path == "/token"
        body = request.read().decode()
        assert "grant_type=authorization_code" in body
        assert "code_verifier=abc" in body
        return httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://p.example.com")
    result = exchange_code(client, "code1", "https://app.example.com/cb", "c1", "secret", "abc")
    assert result["access_token"] == "tok"


def test_exchange_error_raises():
    def handler(request):
        return httpx.Response(400, json={"error": "invalid_grant", "error_description": "code expired"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://p.example.com")
    with pytest.raises(OAuthError, match="code expired"):
        exchange_code(client, "bad", "https://app.example.com/cb", "c1", "secret")
```

Запуск: `python -m pytest test_exchange.py -q` → `2 passed`. `MockTransport` перехватывает HTTP-вызовы, поэтому тест работает без сети. Мы проверяем не только результат, но и что в теле POST-запроса действительно есть `code_verifier` — это защищает от типичной ошибки «забыл PKCE».

### Разбор 4
Решение:

```python
# validate.py
def check_state(received, expected):
    return received == expected


def check_redirect_uri(uri, allowed_uri):
    return uri == allowed_uri
```

```python
# test_validate.py
from validate import check_redirect_uri, check_state


def test_state_exact_match():
    assert check_state("abc", "abc") is True
    assert check_state("abc", "abd") is False


def test_redirect_uri_exact_match():
    assert check_redirect_uri("https://app.example.com/cb", "https://app.example.com/cb") is True


def test_redirect_uri_evil_domain_rejected():
    assert check_redirect_uri("https://app.example.com.evil.io/cb", "https://app.example.com/cb") is False


def test_redirect_uri_extra_path_rejected():
    assert check_redirect_uri("https://app.example.com/cb/extra", "https://app.example.com/cb") is False
```

Запуск: `python -m pytest test_validate.py -q` → `4 passed`. Почему это важно? Если бы мы писали `uri.startswith(allowed_uri)`, тест `test_redirect_uri_evil_domain_rejected` провалился бы: `https://app.example.com` действительно является префиксом `https://app.example.com.evil.io/cb`, и злоумышленник смог бы перенаправить код авторизации на свой домен. Точное равенство строк — единственный безопасный вариант.

### Разбор 5
Решение:

```python
# session.py
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "dev-secret"


def issue_access_token(sub, secret, lifetime_minutes=30):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "scope": "read:profile",
        "iat": now,
        "exp": now + timedelta(minutes=lifetime_minutes),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def introspect(token, secret):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return {"active": False}
    return {"active": True, "sub": payload["sub"], "exp": payload["exp"].timestamp()}


if __name__ == "__main__":
    good = issue_access_token("user-42", SECRET)
    print(introspect(good, SECRET))
    expired = issue_access_token("user-42", SECRET, lifetime_minutes=-1)
    print(introspect(expired, SECRET))
```

Результат (примерно):

```python
{'active': True, 'sub': 'user-42', 'exp': 1769580800.0}
{'active': False}
```

Что здесь происходит? `jwt.decode` сам проверяет `exp` — если срок истёк, поднимается `ExpiredSignatureError`, и мы возвращаем `active: False`. Это модель реальной интроспекции: локальная проверка подписи и срока (как по JWKS) вместо сетевого вызова. Функция `issue_access_token` используется для эмуляции Authorization Server, чтобы скрипт был самодостаточным и работал без сети.
<!--/SOLUTION-->

<!--QUIZ-->
Какой поток OAuth2 предназначен для публичных клиентов (SPA и мобильных приложений)?
- Authorization Code + PKCE
- Client Credentials
- Resource Owner Password
* Правильный ответ: Authorization Code + PKCE
У публичных клиентов нет секрета, поэтому обязателен PKCE, который защищает код авторизации.

Что такое параметр state в OAuth2?
- Тип токена
- Случайная строка для защиты от CSRF и перехвата
- Секрет клиента
* Правильный ответ: Случайная строка для защиты от CSRF и перехвата
state связывает запрос авторизации с обратным вызовом: без неё злоумышленник может подменить код.

Для чего нужен code_challenge при PKCE?
- Чтобы зашифровать access_token
- Чтобы связать код авторизации с заранее известным verifier'ом
- Чтобы получить refresh_token
* Правильный ответ: Чтобы связать код авторизации с заранее известным verifier'ом
При обмене кода клиент отправляет verifier, а сервер сравнивает его хэш с challenge — перехваченный код без verifier бесполезен.

Какой грант используется для machine-to-machine интеграций (микросервисы, CI)?
- Authorization Code
- Client Credentials
- Refresh Token
* Правильный ответ: Client Credentials
Клиент авторизуется сам, своим client_id и client_secret, без участия пользователя.

Зачем нужен refresh-токен?
- Чтобы получить новый access-токен без повторного входа пользователя
- Чтобы заменить client_secret
- Чтобы шифровать запросы
* Правильный ответ: Чтобы получить новый access-токен без повторного входа пользователя
Access-токены короткоживущие, а refresh позволяет продлить сессию, обменяв его на новый access-токен.

Что возвращает эндпоинт интроспекции токена?
- Новый токен
- JSON со статусом токена: active, scope, exp и другие поля
- Код авторизации
* Правильный ответ: JSON со статусом токена: active, scope, exp и другие поля
Интроспекция (RFC 7662) сообщает, действует ли токен, и его метаданные.

Чем OpenID Connect отличается от OAuth2?
- Это одно и то же
- OIDC добавляет id_token (JWT о личности) и эндпоинт userinfo
- OIDC отменяет токены
* Правильный ответ: OIDC добавляет id_token (JWT о личности) и эндпоинт userinfo
OAuth2 авторизует доступ к данным, а OIDC ещё и сообщает, кто пользователь, через id_token и userinfo.

Почему нельзя проверять redirect_uri методом «начинается с»?
- Потому что это медленно
- Потому что https://app.example.com — префикс https://app.example.com.evil.io, и атака пройдёт
- Потому что redirect_uri не важен
* Правильный ответ: Потому что https://app.example.com — префикс https://app.example.com.evil.io, и атака пройдёт
Только точное равенство строк допускает зарегистрированный URI; иначе код авторизации можно увести на злонамеренный домен.

Где должен храниться client_secret?
- В JavaScript на странице клиента
- Только на сервере, в переменных окружения или secrets manager
- В публичном Git-репозитории
* Правильный ответ: Только на сервере, в переменных окружения или secrets manager
Секрет, попавший в клиентский код, считается скомпрометированным.

Какой алгоритм подписи JWT обычно используют провайдеры в продакшене?
- RS256 — асимметричный, публичный ключ публикуется в JWKS
- HS256 — с общим секретом
- MD5
* Правильный ответ: RS256 — асимметричный, публичный ключ публикуется в JWKS
Провайдер подписывает приватным ключом, а любой ресурсный сервер проверяет подпись публичным ключом из JWKS — секрет никуда передавать не нужно.

Что произойдёт, если использовать код авторизации дважды?
- Провайдер вернёт ошибку invalid_grant
- Пользователь получит два токена
- Ничего страшного
* Правильный ответ: Провайдер вернёт ошибку invalid_grant
Код авторизации одноразовый: повторное использование говорит об атаке, и сервер его отклоняет.

Какой scope нужен для получения id_token в OpenID Connect?
- user:email
- openid
- offline_access
* Правильный ответ: openid
Строго говоря, именно scope openid включает OIDC-механику: id_token и userinfo.
<!--/QUIZ-->
