---
title: Деплой Python-сервиса в Kubernetes
summary: Docker-образ Python-приложения, Deployment с readiness/liveness пробами, ConfigMap, ресурсы и обновление версий.
order: 4
duration: 45 мин
difficulty: advanced
tags: kubernetes, python, docker, деплой, пробы
---

Мы научились создавать поды, деплойменты и сервисы. Теперь применим это к настоящему Python-приложению: соберём образ, задеплоим сервис, настроим пробы и научимся обновлять версии без простоя.

## Docker-образ Python-приложения

Базовый `Dockerfile` для FastAPI-приложения:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Сборка и публикация:

```bash
docker build -t myapp:v1 .
docker push registry.example.com/myapp:v1
```

Образ — самодостаточный артефакт: он содержит код, зависимости и команду запуска. В Kubernetes контейнер из этого образа и будет жить в поде.

## Манифест Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:v1
          ports:
            - containerPort: 8000
          env:
            - name: APP_ENV
              value: production
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

`resources` описывают гарантии (`requests`) и верхние границы (`limits`) по CPU и памяти. Планировщик использует requests при размещении пода, а limits защищают соседей от «прожорливого» приложения.

## Пробы (probes)

Kubernetes проверяет здоровье приложения тремя видами проб:

- **livenessProbe** — жива ли программа; если нет, контейнер перезапускается.
- **readinessProbe** — готов ли принимать трафик; если нет, под исключается из сервиса.
- **startupProbe** — для медленно стартующих приложений.

Для HTTP-сервисов это обычно `httpGet` на путь `/health`:

```yaml
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 3
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 5
```

## ConfigMap и переменные окружения

Конфигурацию выносят в ConfigMap — отдельный ресурс:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

В Deployment она подключается через `envFrom` — и приложение читает переменные как обычно:

```yaml
          envFrom:
            - configMapRef:
                name: myapp-config
```

## Обновление версий

Смена образа — это правка одной строки:

```bash
kubectl set image deployment/myapp myapp=registry.example.com/myapp:v2
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
```

Deployment катает rolling update: создаёт новые поды и плавно выводит старые, пока новые не пройдут readiness-пробы.

## Итог

Мы собрали путь Python-приложения в Kubernetes: Docker-образ → Deployment с ресурсами и пробами → ConfigMap для конфигурации → обновление через rollout. Практика закрепит каждый шаг.

<!--TASK-->
### Задача 1
Создай файл `deployment.yml` для приложения `myapp`: две реплики, метка и селектор `app: myapp`, образ `registry.example.com/myapp:v1`, порт контейнера `8000`, переменная окружения `APP_ENV=production` через блок `env`. Ожидаемый результат: манифест валиден, и ты можешь объяснить, почему `env` и `resources` находятся внутри элемента списка `containers`.

### Задача 2
Напиши pytest-тест `test_deployment.py`, который читает `deployment.yml` и проверяет: `replicas == 2`, образ содержит `myapp:v1`, порт `containerPort == 8000`, и настроен `env` с именем `APP_ENV` и значением `production`. Добавь проверку, что у контейнера есть и `resources.requests`, и `resources.limits`. Ожидаемый результат: `pytest test_deployment.py -v` зелёный.

### Задача 3
Добавь в `deployment.yml` пробы `livenessProbe` и `readinessProbe` c `httpGet` на `/health` и порт `8000`, с `initialDelaySeconds` и `periodSeconds` (подбери разумные значения). Затем допиши тест: проверь, что обе пробы существуют, у каждой есть `httpGet.path == "/health"`, `httpGet.port == 8000`, а также `initialDelaySeconds` и `periodSeconds`. Ожидаемый результат: тест зелёный, и ты объясняешь разницу между liveness и readiness.

### Задача 4
Создай `configmap.yml` с данными `APP_ENV: production` и `LOG_LEVEL: info`, а в `deployment.yml` подключи его через `envFrom.configMapRef.name` со значением `myapp-config`. Допиши тест: проверь, что `configmap.yml` валиден (kind `ConfigMap`), и что Deployment ссылается на `myapp-config` в `envFrom`. Ожидаемый результат: тесты проходят, и конфигурация отделена от образа.

### Задача 5
Создай `service.yml` типа `ClusterIP` для `myapp`: селектор `app: myapp`, порт `80`, `targetPort: 8000`. Затем напиши тест `test_rollout.py`: он проверяет, что образ в `deployment.yml` обновляем (то есть в манифесте есть ключ `image`), и что сервис указывает на контейнерный порт `8000`. Ожидаемый результат: весь набор тестов (`pytest -v`) зелёный, и схема «сервис → деплоймент → контейнер» согласована.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
`containers` — это список: даже если контейнер один, после `containers:` нужен маркер списка `-`. Внутри контейнера: `name`, `image`, `ports` (список), `env` (список словарей `name`/`value`), `resources`. Метка `app: myapp` должна быть и в `selector.matchLabels`, и в `template.metadata.labels`.

### Подсказка 2
В тесте работай через `yaml.safe_load`. Доступ к контейнеру: `doc["spec"]["template"]["spec"]["containers"][0]`. Проверяй `container["env"]` — это список, найди в нём элемент с `name == "APP_ENV"`. Для ресурсов: `container["resources"]["requests"]` и `container["resources"]["limits"]`.

### Подсказка 3
Пробы — ключи внутри контейнера: `livenessProbe` и `readinessProbe`. Каждая — словарь с `httpGet.path`, `httpGet.port`, `initialDelaySeconds`, `periodSeconds`. Не забудь: yaml — это словари и списки, поэтому `httpGet` — вложенный словарь.

### Подсказка 4
ConfigMap: `apiVersion: v1`, `kind: ConfigMap`, `metadata.name`, `data` — словарь строк. В Deployment блок `envFrom` — список: `- configMapRef: { name: myapp-config }`. В тесте сравни `envFrom[0]["configMapRef"]["name"] == "myapp-config"`.

### Подсказка 5
Сервис: `spec.selector.app` должно быть равно `myapp`, а `spec.ports[0].targetPort` — `8000`. В тесте проверь, что `deployment.yml` содержит ключ `image` (например, `container["image"]`), и что его значение непустое. Так ты гарантируешь, что деплоймент реально обновляем.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:v1
          ports:
            - containerPort: 8000
          env:
            - name: APP_ENV
              value: production
```

Что здесь происходит? `containers` — список, поэтому перед `name` стоит дефис. Окружение — список словарей с парами `name`/`value`; это стандартный способ передать переменные в контейнер. Обрати внимание на уровни вложенности: `env` и `ports` лежат внутри элемента списка контейнеров, а не на уровне `spec`. Метка `app: myapp` повторяется в селекторе и шаблоне — это обязательное условие, чтобы Deployment управлял своими подами.

### Разбор 2
Решение:

```python
import yaml


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_container():
    dep = load_yaml("deployment.yml")
    return dep["spec"]["template"]["spec"]["containers"][0]


def test_replicas():
    dep = load_yaml("deployment.yml")
    assert dep["spec"]["replicas"] == 2


def test_image():
    assert "myapp:v1" in get_container()["image"]


def test_port():
    assert get_container()["ports"][0]["containerPort"] == 8000


def test_env_app_env():
    env = get_container()["env"]
    assert any(e["name"] == "APP_ENV" and e["value"] == "production" for e in env)


def test_resources_present():
    res = get_container()["resources"]
    assert "requests" in res and "limits" in res
```

Что здесь происходит? `get_container()` — вспомогательная функция, которая сразу возвращает словарь контейнера, убирая повторяющийся доступ к глубокой вложенности. Тесты проверяют реплики, образ, порт, переменную окружения и наличие обоих блоков ресурсов. `any(...)` удобен для проверки элемента списка по условию. Если `resources` отсутствует — `KeyError` уронит тест, что честно сигнализирует о проблеме.

### Разбор 3
Решение. Фрагмент контейнера:

```yaml
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 3
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 2
            periodSeconds: 5
```

Тест:

```python
def check_probe(probe):
    assert probe is not None, "проба отсутствует"
    assert probe["httpGet"]["path"] == "/health"
    assert probe["httpGet"]["port"] == 8000
    assert probe["initialDelaySeconds"] > 0
    assert probe["periodSeconds"] > 0


def test_probes():
    c = get_container()
    check_probe(c.get("livenessProbe"))
    check_probe(c.get("readinessProbe"))
```

Что здесь происходит? `livenessProbe` решает, перезапускать ли контейнер: если `/health` не отвечает — контейнер пересоздаётся. `readinessProbe` решает, направлять ли на под трафик: пока проба не прошла, под не попадает в сервис. `initialDelaySeconds` даёт приложению время запуститься, `periodSeconds` — частота проверок. Тест проверяет наличие обеих проб и их ключевые поля, ловя типичные опечатки в путях и портах.

### Разбор 4
Решение. `configmap.yml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

Фрагмент `deployment.yml`:

```yaml
          envFrom:
            - configMapRef:
                name: myapp-config
```

Тест:

```python
def test_configmap():
    cm = load_yaml("configmap.yml")
    assert cm["kind"] == "ConfigMap"
    assert cm["data"]["APP_ENV"] == "production"
    assert cm["data"]["LOG_LEVEL"] == "info"


def test_deployment_refers_to_configmap():
    c = get_container()
    env_from = c.get("envFrom", [])
    assert any(ref["configMapRef"]["name"] == "myapp-config" for ref in env_from)
```

Что здесь происходит? ConfigMap хранит конфигурацию отдельно от образа: можно менять настройки без пересборки. `envFrom` импортирует все пары `data` как переменные окружения. Тест проверяет и сам ConfigMap, и ссылку на него из Deployment. Если имя в `envFrom` не совпадёт с `metadata.name` — Kubernetes просто не подтянет переменные, и приложение останется без конфигурации; тест страхует от этого.

### Разбор 5
Решение. `service.yml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8000
```

Тест `test_rollout.py`:

```python
def test_image_is_updatable():
    assert get_container()["image"]


def test_service_targets_container_port():
    svc = load_yaml("service.yml")
    assert svc["spec"]["selector"]["app"] == "myapp"
    assert svc["spec"]["ports"][0]["targetPort"] == 8000
```

Что здесь происходит? Сервис типа `ClusterIP` — внутренняя точка входа: порт `80` снаружи, `8000` — внутрь контейнера. Селектор `app: myapp` связывает сервис с подами деплоймента. Проверка `image` непустого — гарантия, что деплоймент можно обновлять командой `kubectl set image`. Вся связка — сервис → селектор → поды → контейнерный порт — теперь подтверждена тестами, которые запускаются за секунды без кластера.
<!--/SOLUTION-->

<!--QUIZ-->
Что делает livenessProbe?
- Перезапускает контейнер, если приложение не отвечает
- Направляет трафик на под
- Удаляет под при перегрузке
* Правильный ответ: Перезапускает контейнер, если приложение не отвечает
liveness определяет, жив ли процесс; при провале контейнер перезапускается.

Что делает readinessProbe?
- Исключает под из сервиса, пока он не готов
- Перезапускает контейнер
- Масштабирует деплоймент
* Правильный ответ: Исключает под из сервиса, пока он не готов
readiness решает, принимать ли трафик; неготовый под не получает запросы.

Что описывает блок resources.requests?
- Гарантированные ресурсы для контейнера
- Лимит ресурсов всего кластера
- Количество реплик
* Правильный ответ: Гарантированные ресурсы для контейнера
requests — минимум CPU/памяти, который резервируется контейнеру.

Что описывает блок resources.limits?
- Верхнюю границу ресурсов контейнера
- Нижнюю границу ресурсов
- Порог для автоперезапуска
* Правильный ответ: Верхнюю границу ресурсов контейнера
limits ограничивают потребление контейнера сверху.

Зачем нужен ConfigMap?
- Хранить конфигурацию отдельно от образа
- Хранить секретные пароли
- Собирать Docker-образы
* Правильный ответ: Хранить конфигурацию отдельно от образа
ConfigMap позволяет менять настройки без пересборки образа.

Как подключить ConfigMap к контейнеру?
- Через envFrom.configMapRef
- Через imagePullPolicy
- Через replicas
* Правильный ответ: Через envFrom.configMapRef
envFrom импортирует данные ConfigMap как переменные окружения.

Какая команда меняет образ в деплойменте?
- kubectl set image deployment/myapp myapp=...:v2
- kubectl edit pod
- docker push
* Правильный ответ: kubectl set image deployment/myapp myapp=...:v2
set image обновляет образ контейнера в деплойменте.

Что делает kubectl rollout undo?
- Откатывает деплоймент к предыдущей версии
- Отменяет команду apply
- Удаляет образ
* Правильный ответ: Откатывает деплоймент к предыдущей версии
rollout undo возвращает предыдущую ревизию.

Какой порт обычно слушает FastAPI-приложение в примерах?
- 8000
- 80
- 443
* Правильный ответ: 8000
uvicorn по умолчанию слушает 8000.

Почему Deployment лучше подов для приложения?
- Он пересоздаёт и обновляет поды автоматически
- Он быстрее запускается
- Он не использует образы
* Правильный ответ: Он пересоздаёт и обновляет поды автоматически
Deployment гарантирует желаемое число реплик и умеет катать обновления.
<!--/QUIZ-->
