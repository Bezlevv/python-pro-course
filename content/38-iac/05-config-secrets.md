---
title: Конфиги и секреты: Helm-основы
summary: Структура Helm-чарта, values.yaml, шаблонизация манифестов, Kubernetes Secrets и безопасное хранение секретов.
order: 5
duration: 45 мин
difficulty: advanced
tags: helm, kubernetes, секреты, шаблоны, values
---

К третьему деплойменту выясняется: манифестов много, они почти одинаковые, а менять номер версии образа приходится в нескольких файлах сразу. **Helm** решает эту проблему: это пакетный менеджер для Kubernetes, который шаблонизирует манифесты и объединяет их в **чарты** (charts).

## Структура чарта

Минимальный чарт — папка с файлами:

```
myapp/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    └── service.yaml
```

- `Chart.yaml` — метаданные чарта: имя, версия, описание.
- `values.yaml` — значения по умолчанию, туда выносят всё, что меняется между окружениями.
- `templates/` — Go-шаблоны манифестов, в которых через `{{ .Values.имя }}` подставляются значения.

Пример `Chart.yaml`:

```yaml
apiVersion: v2
name: myapp
description: Python-сервис
type: application
version: 0.1.0
appVersion: "1.0"
```

Пример `values.yaml`:

```yaml
replicaCount: 2
image:
  repository: registry.example.com/myapp
  tag: v1
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
config:
  logLevel: info
```

## Шаблонизация

`templates/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.fullnameOverride | default .Chart.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ .Chart.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          env:
            - name: LOG_LEVEL
              value: {{ .Values.config.logLevel }}
```

Синтаксис `{{ ... }}` — Go-шаблоны; `.Values` — доступ к values.yaml, `.Chart` — к Chart.yaml. Пайп `| default "..."` задаёт значение по умолчанию.

Просмотр итоговых манифестов без установки:

```bash
helm template myapp ./myapp
helm lint ./myapp
```

## Установка и обновление

```bash
helm install myapp ./myapp
helm upgrade myapp ./myapp --set image.tag=v2
helm list
helm uninstall myapp
```

Флаг `--set` переопределяет любое значение на лету, а `helm upgrade` обновляет релиз. Helm помечает все созданные ресурсы метками своего релиза и помнит их состояние.

## Секреты

**Secret** — ресурс Kubernetes для чувствительных данных: паролей, токенов, ключей. В отличие от ConfigMap, данные хранятся в base64:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJfc2VjcmV0
```

Значение `c3VwZXJfc2VjcmV0` — это base64 от `super_secret`. В шаблоне Secret подключается так же, как ConfigMap — через `envFrom` или `secretKeyRef`.

**Важно:** base64 — не шифрование, а кодирование. Секреты не должны попадать в Git в открытом виде. На практике используют инструменты вроде Sealed Secrets, SOPS или хранилища (Vault). Правило простое: секреты — только через механизмы безопасной доставки, а не в плейбуках и чартах.

## Итог

Helm объединяет манифесты в переиспользуемый чарт с параметрами, а Secret безопасно хранит чувствительные данные. Осталось закрепить практикой.

<!--TASK-->
### Задача 1
Создай структуру чарта `myapp/`: файлы `Chart.yaml` (название `myapp`, версия `0.1.0`, `appVersion: "1.0"`, `type: application`) и `values.yaml` с ключами `replicaCount: 2`, `image.repository`, `image.tag: v1`, `service.port: 80`, `config.logLevel: info`. Ожидаемый результат: каталог `myapp/templates/` существует (можешь создать пустым), и оба YAML-файла валидны.

### Задача 2
Напиши pytest-тест `test_chart.py`, который проверяет структуру чарта: файлы `Chart.yaml`, `values.yaml` существуют; `Chart.yaml` содержит `apiVersion: v2`, `name: myapp`, `version: 0.1.0`; `values.yaml` содержит все перечисленные в задаче 1 ключи. Используй `os.path.exists` для файлов и `yaml.safe_load` для содержимого. Ожидаемый результат: `pytest test_chart.py -v` зелёный.

### Задача 3
Создай `templates/deployment.yaml` с шаблонизацией: `replicas: {{ .Values.replicaCount }}`, образ `"{{ .Values.image.repository }}:{{ .Values.image.tag }}"`, метка `app: {{ .Chart.Name }}`. Затем напиши тест `test_render.py`, который рендерит этот шаблон через Jinja2 с контекстом, собранным из `values.yaml` и `Chart.yaml` (эмулируя Helm), и проверяет, что в результате есть `replicas: 2`, `image: registry.example.com/myapp:v1` и `app: myapp`. Ожидаемый результат: рендеринг проходит, и результирующий YAML валиден.

### Задача 4
Создай `templates/service.yaml` с шаблонизацией типа сервиса и порта: `type: {{ .Values.service.type }}`, `port: {{ .Values.service.port }}`, `targetPort: 8000`, метка `app: {{ .Chart.Name }}`. Добавь в `test_render.py` проверку рендеринга сервиса. Ожидаемый результат: оба шаблона рендерятся корректно, и тест зелёный.

### Задача 5
Создай `secret.yml` с Secret-ресурсом `myapp-secret` (тип `Opaque`), в котором `DB_PASSWORD` закодирован base64 от строки `super_secret`. Напиши тест `test_secret.py`, который проверяет: kind `Secret`, значение `DB_PASSWORD` — валидный base64, и его декодированное значение равно `super_secret`. Ожидаемый результат: тест зелёный, и ты можешь объяснить, почему base64 — это не защита, а лишь формат хранения.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Порядок ключей в `Chart.yaml` не важен, но имена обязательны: `apiVersion`, `name`, `description`, `type`, `version`, `appVersion`. В `values.yaml` вложенные ключи: `image: { repository: ..., tag: v1 }`, `service: { port: 80 }`, `config: { logLevel: info }`.

### Подсказка 2
Для проверки ключей пиши маленькие хелперы: `def load_yaml(path): ...`. Проверяй наличие вложенных ключей через вложенные `assert`, например `assert values["image"]["tag"] == "v1"`. Не забудь `import os` и `os.path.exists`.

### Подсказка 3
Jinja2 и Helm используют разный синтаксис, но для учебных целей мы рендерим через `Template(...).render(**ctx)`. Собери контекст: `ctx = {"Values": values, "Chart": chart}` — а в шаблоне используй `{{ Values.replicaCount }}` и `{{ Chart.Name }}` (без точек-префиксов, как в Helm). После рендеринга распарси результат через `yaml.safe_load` и проверяй ключи.

### Подсказка 4
Сервис рендерится так же: `{{ Values.service.type }}`, `{{ Values.service.port }}`, `{{ Chart.Name }}`. После рендеринга проверь `yaml.safe_load(rendered)["spec"]["ports"][0]["port"] == 80`. targetPort укажи константой `8000`.

### Подсказка 5
Закодируй значение заранее: `import base64; encoded = base64.b64encode(b"super_secret").decode()`. В тесте декодируй обратно: `base64.b64decode(secret["data"]["DB_PASSWORD"]).decode() == "super_secret"`. Для проверки валидности base64 можно обернуть декодирование в `try/except binascii.Error`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение. `myapp/Chart.yaml`:

```yaml
apiVersion: v2
name: myapp
description: Python-сервис
type: application
version: 0.1.0
appVersion: "1.0"
```

`myapp/values.yaml`:

```yaml
replicaCount: 2
image:
  repository: registry.example.com/myapp
  tag: v1
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
config:
  logLevel: info
```

Что здесь происходит? `Chart.yaml` — паспорт чарта: `version` — версия самого чарта, `appVersion` — версия приложения внутри. `values.yaml` — все «ручки» настройки: количество реплик, образ, сервис, конфигурация. Между окружениями различаются именно values, а не шаблоны: для stage создадут свой `values-stage.yaml`, и манифесты останутся неизменными.

### Разбор 2
Решение:

```python
import os
import yaml


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_files_exist():
    assert os.path.exists("myapp/Chart.yaml")
    assert os.path.exists("myapp/values.yaml")
    assert os.path.isdir("myapp/templates")


def test_chart_metadata():
    chart = load_yaml("myapp/Chart.yaml")
    assert chart["apiVersion"] == "v2"
    assert chart["name"] == "myapp"
    assert chart["version"] == "0.1.0"
    assert chart["type"] == "application"


def test_values_content():
    values = load_yaml("myapp/values.yaml")
    assert values["replicaCount"] == 2
    assert values["image"]["repository"] == "registry.example.com/myapp"
    assert values["image"]["tag"] == "v1"
    assert values["service"]["port"] == 80
    assert values["config"]["logLevel"] == "info"
```

Что здесь происходит? Первый тест проверяет, что файлы существуют и каталог `templates` на месте. Дальше — содержимое: `Chart.yaml` обязан содержать версию схемы `v2` и имя, а `values.yaml` — все ключи, на которые будут опираться шаблоны. Если в values пропущен ключ, шаблонизация упадёт — тест ловит это заранее.

### Разбор 3
Решение. `myapp/templates/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ Chart.Name }}
spec:
  replicas: {{ Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ Chart.Name }}
  template:
    metadata:
      labels:
        app: {{ Chart.Name }}
    spec:
      containers:
        - name: {{ Chart.Name }}
          image: "{{ Values.image.repository }}:{{ Values.image.tag }}"
```

Тест `test_render.py`:

```python
import yaml
from jinja2 import Template


def render_template(path, ctx):
    with open(path, encoding="utf-8") as f:
        return Template(f.read()).render(**ctx)


def build_context():
    values = load_yaml("myapp/values.yaml")
    chart = load_yaml("myapp/Chart.yaml")
    return {"Values": values, "Chart": chart}


def test_deployment_renders():
    rendered = render_template("myapp/templates/deployment.yaml", build_context())
    doc = yaml.safe_load(rendered)
    assert doc["spec"]["replicas"] == 2
    image = doc["spec"]["template"]["spec"]["containers"][0]["image"]
    assert image == "registry.example.com/myapp:v1"
    assert doc["spec"]["template"]["metadata"]["labels"]["app"] == "myapp"
```

Что здесь происходит? Мы эмулируем Helm: `render_template` подставляет в шаблон контекст — словари `Values` и `Chart`. Разница с настоящим Helm лишь в синтаксисе (`Values.replicaCount` вместо `.Values.replicaCount`). После рендеринга результат парсится как YAML, и тест проверяет фактические значения. Такой тест — «золотой стандарт» для чарта: он проверяет шаблон без установки кластера.

### Разбор 4
Решение. `myapp/templates/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ Chart.Name }}-service
spec:
  type: {{ Values.service.type }}
  selector:
    app: {{ Chart.Name }}
  ports:
    - port: {{ Values.service.port }}
      targetPort: 8000
```

Дополнение в `test_render.py`:

```python
def test_service_renders():
    rendered = render_template("myapp/templates/service.yaml", build_context())
    doc = yaml.safe_load(rendered)
    assert doc["spec"]["type"] == "ClusterIP"
    assert doc["spec"]["ports"][0]["port"] == 80
    assert doc["spec"]["ports"][0]["targetPort"] == 8000
    assert doc["spec"]["selector"]["app"] == "myapp"
```

Что здесь происходит? Сервис берёт тип и порт из values, а селектор — из имени чарта. `targetPort: 8000` — константа, потому что это порт контейнера, который определяет код приложения. Тест проверяет, что все значения подставились. Теперь изменение порта в values меняет и Deployment, и Service — согласованно, без правки двух файлов.

### Разбор 5
Решение. `secret.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJfc2VjcmV0
```

Тест `test_secret.py`:

```python
import base64
import binascii
import yaml


def test_secret_kind():
    with open("secret.yml", encoding="utf-8") as f:
        secret = yaml.safe_load(f)
    assert secret["kind"] == "Secret"
    assert secret["type"] == "Opaque"


def test_secret_value_is_base64():
    with open("secret.yml", encoding="utf-8") as f:
        secret = yaml.safe_load(f)
    encoded = secret["data"]["DB_PASSWORD"]
    try:
        decoded = base64.b64decode(encoded, validate=True).decode()
    except (binascii.Error, ValueError):
        raise AssertionError("значение не является валидным base64")
    assert decoded == "super_secret"
```

Что здесь происходит? `base64.b64decode` с `validate=True` строго проверяет корректность кодирования. Значение `c3VwZXJfc2VjcmV0` — это `super_secret` в base64. Важно понимать: base64 — это не шифрование, любой может декодировать Secret из кластера. Поэтому в реальных проектах секреты шифруют и хранят вне Git, а в кластер доставляют через Sealed Secrets или Vault. Тест лишь проверяет формат, а не безопасность.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое Helm?
- Пакетный менеджер для Kubernetes
- Инструмент сборки Docker-образов
- База данных для логов
* Правильный ответ: Пакетный менеджер для Kubernetes
Helm упаковывает и шаблонизирует манифесты Kubernetes.

Что содержит values.yaml?
- Значения по умолчанию для параметров чарта
- Секретные пароли в открытом виде
- Код приложения
* Правильный ответ: Значения по умолчанию для параметров чарта
values.yaml — «ручки настройки», которые меняются между окружениями.

Как в шаблоне Helm обратиться к значению из values.yaml?
- {{ .Values.имя }}
- {{ .Data.имя }}
- {{ values.имя }}
* Правильный ответ: {{ .Values.имя }}
Доступ к values — через .Values, а к Chart.yaml — через .Chart.

Какая команда показывает итоговые манифесты без установки?
- helm template
- helm install
- helm uninstall
* Правильный ответ: helm template
helm template рендерити манифесты и печатает их, ничего не устанавливая.

Какая команда обновляет релиз с новым образом?
- helm upgrade myapp ./myapp --set image.tag=v2
- helm install myapp ./myapp
- helm list
* Правильный ответ: helm upgrade myapp ./myapp --set image.tag=v2
helm upgrade применяет изменения; --set переопределяет значение.

Что такое Secret в Kubernetes?
- Ресурс для хранения чувствительных данных в base64
- Ресурс для хранения публичных конфигов
- Тип пода
* Правильный ответ: Ресурс для хранения чувствительных данных в base64
Secret хранит пароли и токены в кодированном виде.

Является ли base64 шифрованием?
- Нет, это лишь кодирование
- Да, это надёжное шифрование
- Только для паролей
* Правильный ответ: Нет, это лишь кодирование
base64 легко декодируется — это формат хранения, а не защита.

Какой инструмент помогает хранить секреты зашифрованными вне Git?
- Sealed Secrets или SOPS
- kubectl run
- docker build
* Правильный ответ: Sealed Secrets или SOPS
Они шифруют секреты до попадания в репозиторий.

Что делает helm lint?
- Проверяет синтаксис и структуру чарта
- Устанавливает чарт
- Удаляет чарт
* Правильный ответ: Проверяет синтаксис и структуру чарта
helm lint находит типичные ошибки в чарте.

Какой ключ Chart.yaml хранит версию приложения внутри чарта?
- appVersion
- version
- apiVersion
* Правильный ответ: appVersion
appVersion — версия приложения, version — версия самого чарта.
<!--/QUIZ-->
