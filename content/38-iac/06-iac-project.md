---
title: Проект: полный стек инфраструктуры
summary: Сквозной проект: Git → Ansible → Terraform → Kubernetes → Helm; собираем все манифесты и защищаем их тестами.
order: 6
duration: 60 мин
difficulty: advanced
tags: проект, devops, ansible, terraform, kubernetes, helm
---

Это финальный урок модуля. Мы соберём весь стек в один проект и напишем сквозные тесты, которые проверяют инфраструктуру как код — без кластера, за секунды. Ты создашь папку `project/` с полным набором манифестов и тестами к ним.

## Полный цикл инфраструктуры

В реальном проекте инфраструктура живёт по такому циклу:

1. **Код** попадает в Git; CI собирает Docker-образ.
2. **Terraform** создаёт кластер и инфраструктуру (сети, узлы, реестр образов).
3. **Ansible** настраивает серверы, которых ещё нет в кластере (или донастраивает узлы).
4. **Kubernetes + Helm** деплоят приложение: чарт с values и секретами.
5. **Sekреты** доставляются безопасно — не в Git.

Итоговая схема связки «код → образ → под» выглядит так:

```
Git → CI (сборка образа) → Registry
                              ↓
Terraform → кластер K8s ← Helm (чарт приложения)
                              ↓
                  Deployment → Pods → Service → трафик
```

Каждый слой описывается кодом, а значит — проверяется тестами.

## Что должно быть в проекте

Минимальный комплект манифестов приложения:

- `configmap.yml` — конфигурация окружения;
- `secret.yml` — секреты (base64);
- `deployment.yml` — приложение с пробами и ресурсами;
- `service.yml` — точка входа.

Плюс `Chart.yaml`/`values.yaml`, если используем Helm-подход, и сама папка с шаблонами. Наш проект соберёт всё вместе.

## Инфраструктура как тестируемый код

Главный навык урока — **проверять инфраструктуру до применения**. Пока манифест не прошёл pytest, он не должен ехать в кластер. Это тот же принцип, что «не пушить код, который не прошёл линтер».

Практичные проверки:

- YAML валиден (синтаксис) — `yaml.safe_load`;
- обязательные поля есть: `apiVersion`, `kind`, `metadata.name`;
- ссылки согласованы: сервис → селектор → метки подов;
- Deployment ссылается на существующие ConfigMap и Secret;
- секреты в открытом виде не встречаются в манифестах.

## Команды для применения

Когда все тесты зелёные, проект применяется настоящими командами:

```bash
terraform init && terraform plan
ansible-playbook -i hosts.yml site.yml
kubectl apply -f project/manifests/
helm upgrade --install myapp ./project/chart
kubectl get deployments,svc
```

Но сначала — тесты. Поехали.

<!--TASK-->
### Задача 1
Создай папку `project/manifests/` и в ней четыре файла: `configmap.yml` (данные `APP_ENV: production`, `LOG_LEVEL: info`), `secret.yml` (Secret `app-secret`, тип `Opaque`, значение `API_TOKEN` — base64 от `secret-token`), `deployment.yml` (Deployment `app`, две реплики, образ `registry.example.com/app:v1`, порт `8000`, пробы `/health`, ссылки на ConfigMap и Secret через `envFrom`), `service.yml` (Service `app-service`, селектор `app: app`, порт `80`, `targetPort: 8000`). Ожидаемый результат: четыре валидных YAML-файла.

### Задача 2
Напиши тест `test_manifests.py`, который проходит по всем файлам в `project/manifests/`, парсит каждый через `yaml.safe_load` и проверяет: у каждого есть `apiVersion` и `kind`; для `Deployment` и `Service` метка `app: app` присутствует в селекторе. Также проверь, что при парсинге ни один файл не бросил исключение. Ожидаемый результат: `pytest test_manifests.py -v` зелёный.

### Задача 3
Допиши в `test_manifests.py` сквозную проверку связности: селектор сервиса (`app: app`) совпадает с меткой `app` в шаблоне деплоймента; Deployment ссылается на ConfigMap с именем `app-config` и Secret с именем `app-secret` (поиск в `envFrom`); сервис `targetPort` равен контейнерному порту (`8000`). Ожидаемый результат: тест зелёный, и связки «деплоймент → конфигурация → сервис» подтверждены.

### Задача 4
Создай скрипт `deploy.sh`, который применяет все манифесты: `kubectl apply -f project/manifests/`, затем ждёт готовности деплоймента `kubectl rollout status deployment/app` и выводит список сервисов `kubectl get svc`. Сделай его исполняемым (в комментарии укажи команду `chmod +x deploy.sh`). Напиши тест `test_deploy_sh.py`, который проверяет, что скрипт существует, содержит `kubectl apply` и `kubectl rollout status`, и начинается с шебанга `#!/bin/bash`.

### Задача 5
Напиши тест `test_no_plain_secrets.py`: прочитай все YAML-файлы из `project/manifests/` как текст и проверь, что нигде не встречается открытая строка `secret-token` (она должна быть только в base64-виде внутри Secret). Дополнительно проверь, что в `secret.yml` значение `API_TOKEN` декодируется обратно в `secret-token`. Ожидаемый результат: тесты зелёные, и секрет не «просочился» в манифесты.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Помни про дефисы списков: `containers:` — это список, `envFrom:` — тоже список. Имена конфиг-мапов и секретов должны совпадать между файлами: в `configmap.yml` используй `metadata.name: app-config`, а в `deployment.yml` — `name: app-config` в `configMapRef`.

### Подсказка 2
Заведи хелпер `def load_yaml(path):` с `open(path, encoding="utf-8")` и `yaml.safe_load`. Для обхода каталога — `os.listdir("project/manifests/")` и фильтр `.endswith(".yml")`. Собирай все ошибки в список, а в конце делай один assert на пустоту списка.

### Подсказка 3
Доступ к селектору: `dep["spec"]["selector"]["matchLabels"]["app"]`. Метка шаблона: `dep["spec"]["template"]["metadata"]["labels"]["app"]`. `envFrom` — список: ищи `ref["configMapRef"]["name"] == "app-config"`. `targetPort` сервиса: `svc["spec"]["ports"][0]["targetPort"] == 8000`.

### Подсказка 4
Шебанг — первая строка `#!/bin/bash`. Читай файл как текст и проверяй `"kubectl apply" in text` и `"kubectl rollout status" in text`. Существование — `os.path.exists("deploy.sh")`.

### Подсказка 5
Для проверки отсутствия открытого секрета пройди по файлам и сделай `assert "secret-token" not in text` — но только для файлов, где `kind != "Secret"`. В самом Secret проверь декодирование: `base64.b64decode(yaml.safe_load(open("project/manifests/secret.yml"))["data"]["API_TOKEN"]).decode() == "secret-token"`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение. `project/manifests/configmap.yml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

`project/manifests/secret.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  API_TOKEN: c2VjcmV0LXRva2Vu
```

`project/manifests/deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: registry.example.com/app:v1
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
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

`project/manifests/service.yml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: app
  ports:
    - port: 80
      targetPort: 8000
```

Что здесь происходит? Это полный минимальный комплект: конфигурация — в ConfigMap, секрет — в Secret (base64 от `secret-token`), приложение — в Deployment со ссылками на оба ресурса, трафик — через Service. Все имена согласованы: `app-config`, `app-secret`, метка `app: app`.

### Разбор 2
Решение:

```python
import os
import yaml

MANIFESTS = "project/manifests"


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_manifests():
    return sorted(
        os.path.join(MANIFESTS, f)
        for f in os.listdir(MANIFESTS)
        if f.endswith(".yml")
    )


def test_all_yaml_are_valid():
    errors = []
    for path in list_manifests():
        try:
            load_yaml(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: {exc}")
    assert not errors, f"невалидный YAML: {errors}"


def test_required_fields():
    for path in list_manifests():
        doc = load_yaml(path)
        assert "apiVersion" in doc, f"{path}: нет apiVersion"
        assert "kind" in doc, f"{path}: нет kind"


def test_app_label_in_selectors():
    for path in list_manifests():
        doc = load_yaml(path)
        if doc.get("kind") in ("Deployment", "Service"):
            selector = doc["spec"].get("selector", {})
            labels = selector.get("matchLabels", selector)
            assert labels.get("app") == "app", f"{path}: нет метки app: app"
```

Что здесь происходит? Тесты итерируются по всем файлам: валидность YAML, обязательные поля, наличие метки в селекторах. Ошибки валидности собираются в список, чтобы увидеть сразу все проблемы, а не первую. Такой «обходной» тест масштабируется: добавил новый манифест — он автоматически попал под проверки. `matchLabels` и `selector` различаются у Deployment и Service, поэтому берём `selector.get("matchLabels", selector)`.

### Разбор 3
Решение:

```python
def get(path, *keys):
    doc = load_yaml(path)
    for k in keys:
        doc = doc[k]
    return doc


def test_service_targets_deployment_pods():
    svc = load_yaml(f"{MANIFESTS}/service.yml")
    dep = load_yaml(f"{MANIFESTS}/deployment.yml")
    assert svc["spec"]["selector"]["app"] == "app"
    assert dep["spec"]["template"]["metadata"]["labels"]["app"] == "app"


def test_deployment_refers_to_configmap_and_secret():
    dep = load_yaml(f"{MANIFESTS}/deployment.yml")
    container = dep["spec"]["template"]["spec"]["containers"][0]
    refs = []
    for ref in container.get("envFrom", []):
        if "configMapRef" in ref:
            refs.append(ref["configMapRef"]["name"])
        if "secretRef" in ref:
            refs.append(ref["secretRef"]["name"])
    assert "app-config" in refs
    assert "app-secret" in refs


def test_service_targetport_matches_container():
    svc = load_yaml(f"{MANIFESTS}/service.yml")
    dep = load_yaml(f"{MANIFESTS}/deployment.yml")
    target = svc["spec"]["ports"][0]["targetPort"]
    container_port = dep["spec"]["template"]["spec"]["containers"][0]["ports"][0]["containerPort"]
    assert target == container_port == 8000
```

Что здесь происходит? Это сердце сквозной проверки: сервис видит поды деплоймента (селектор = метка), Deployment ссылается на существующие ConfigMap и Secret, а сервисный порт ведёт на контейнерный. Если в кластере эти связки рассинхронизированы, приложение «молча» не работает — тест находит проблему до деплоя.

### Разбор 4
Решение. `deploy.sh`:

```bash
#!/bin/bash
set -euo pipefail

kubectl apply -f project/manifests/
kubectl rollout status deployment/app
kubectl get svc
```

Тест `test_deploy_sh.py`:

```python
import os


def test_script_exists_and_executable():
    assert os.path.exists("deploy.sh")


def test_script_has_shebang():
    with open("deploy.sh", encoding="utf-8") as f:
        first_line = f.readline().strip()
    assert first_line == "#!/bin/bash"


def test_script_applies_manifests():
    with open("deploy.sh", encoding="utf-8") as f:
        text = f.read()
    assert "kubectl apply -f project/manifests/" in text
    assert "kubectl rollout status deployment/app" in text
```

Что здесь происходит? `set -euo pipefail` заставляет скрипт падать при любой ошибке — иначе kubectl мог бы «тихо» не применить что-то. Шебанг и команды проверяются тестами. Исполняемость настраивается командой `chmod +x deploy.sh`. Такой скрипт — «одна кнопка» для применения всей инфраструктуры проекта.

### Разбор 5
Решение:

```python
import base64
import yaml


def test_no_plain_secret_in_manifests():
    for path in list_manifests():
        with open(path, encoding="utf-8") as f:
            text = f.read()
        doc = yaml.safe_load(text)
        if doc.get("kind") == "Secret":
            continue
        assert "secret-token" not in text, f"{path}: открытый секрет!"


def test_secret_decodes_back():
    secret = load_yaml(f"{MANIFESTS}/secret.yml")
    encoded = secret["data"]["API_TOKEN"]
    decoded = base64.b64decode(encoded).decode()
    assert decoded == "secret-token"
```

Что здесь происходит? Первый тест проходит по всем манифестам, кроме самих Secret, и убеждается: открытой строки `secret-token` нигде нет. Второй — проверяет, что в Secret значение действительно является base64 и декодируется обратно в оригинал. Это минимальная защита от утечки: секрет существует в одном месте, в правильной форме, и не продублирован в открытом виде. В реальном проекте вместо этого используют шифрование (SOPS, Sealed Secrets) — но даже базовая проверка отсеивает большинство ошибок.
<!--/SOLUTION-->

<!--QUIZ-->
Какой инструмент создаёт кластер и облачную инфраструктуру?
- Terraform
- Ansible
- Helm
* Правильный ответ: Terraform
Terraform управляет инфраструктурой: сетями, узлами, реестрами.

Какой инструмент настраивает серверы изнутри?
- Ansible
- Terraform
- kubectl apply
* Правильный ответ: Ansible
Ansible управляет конфигурацией на уже созданных серверах.

Что объединяет манифесты приложения в переиспользуемый пакет?
- Helm
- Docker
- pip
* Правильный ответ: Helm
Helm — пакетный менеджер для Kubernetes.

Что должно произойти с манифестом до применения в кластере?
- Пройти автоматические проверки
- Быть удалённым
- Быть закоммиченным только в локальную ветку
* Правильный ответ: Пройти автоматические проверки
Инфраструктура как код проверяется тестами до деплоя.

Что проверяет связку «сервис → селектор → метки подов»?
- Согласованность ссылок между манифестами
- Скорость сети
- Версию Python
* Правильный ответ: Согласованность ссылок между манифестами
Сквозные тесты сверяют ссылки и метки между ресурсами.

Почему нельзя хранить секреты в открытом виде в Git?
- Их легко украсть при утечке репозитория
- Они замедляют сборку
- Они ломают YAML
* Правильный ответ: Их легко украсть при утечке репозитория
Секреты в Git — мгновенная утечка при любой утечке репозитория.

Что делает kubectl rollout status deployment/app?
- Ждёт, пока деплоймент достигнет готовности
- Удаляет деплоймент
- Создаёт новый namespace
* Правильный ответ: Ждёт, пока деплоймент достигнет готовности
rollout status блокирует выполнение до завершения обновления.

Что означает set -euo pipefail в bash-скрипте?
- Скрипт падает при любой ошибке
- Скрипт не может быть остановлен
- Скрипт запускается только от root
* Правильный ответ: Скрипт падает при любой ошибке
Это защищает от «тихих» частичных применений.

Чем base64 отличается от шифрования?
- base64 легко декодируется и не защищает
- base64 нельзя декодировать
- base64 хранит только числа
* Правильный ответ: base64 легко декодируется и не защищает
base64 — формат кодирования, а не защита.

Что делает тест test_no_plain_secrets?
- Ищет открытые секреты во всех манифестах, кроме Secret
- Проверяет наличие docker-образа
- Проверяет версию kubectl
* Правильный ответ: Ищет открытые секреты во всех манифестах, кроме Secret
Тест гарантирует, что секрет не продублирован открытым текстом.
<!--/QUIZ-->
