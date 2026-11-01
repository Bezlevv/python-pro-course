---
title: Kubernetes: поды, деплойменты, сервисы
summary: Архитектура кластера, поды, деплойменты, сервисы и labels; пишем первые манифесты и работаем через kubectl.
order: 3
duration: 45 мин
difficulty: advanced
tags: kubernetes, kubectl, поды, деплойменты, сервисы
---

Kubernetes (K8s) — оркестратор контейнеров: он запускает, масштабирует и самовосстанавливает контейнеры на пуле серверов. Если Docker упаковывает приложение в образ, то Kubernetes раскидывает контейнеры по кластеру и следит, чтобы их было ровно столько, сколько нужно.

## Архитектура кластера

Кластер состоит из двух ролей узлов:

- **Control plane** (управляющие узлы) — принимает решения: планировщик, API-сервер, хранилище `etcd` и контроллеры. Пользователь общается с ним через `kubectl`.
- **Worker-узлы** — выполняют контейнеры в **подах**.

Все манифесты отправляются в API-сервер, а контроллеры приводят кластер к желаемому состоянию.

## Поды

**Под (Pod)** — минимальная единица запуска: один или несколько контейнеров, которые разделяют сеть и хранилище. Обычно в поде один контейнер. Манифест пода:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
```

Запуск и просмотр:

```bash
kubectl apply -f pod.yml
kubectl get pods
kubectl describe pod web-pod
kubectl logs web-pod
```

Поды — эфемерные сущности. Если под упадёт, Kubernetes не «оживит» его сам — для этого нужны контроллеры.

## Деплойменты

**Deployment** — контроллер, который управляет набором одинаковых подов (через ReplicaSet). Он умеет пересоздавать поды, обновлять образы и катать откаты:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

Важный момент — **селектор**: `selector.matchLabels` обязан совпадать с метками подов в `template.metadata.labels`. Deployment «видит» только те поды, метки которых совпадают с селектором.

## Сервисы

Поды получают динамические IP и могут пересоздаваться. **Service** — стабильная точка входа. Тип `ClusterIP` даёт виртуальный IP внутри кластера:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
```

`selector` — те же метки `app: web`, а `port` — порт сервиса, `targetPort` — порт контейнера. Другие типы: `NodePort` (открывает порт на каждом узле) и `LoadBalancer` (внешний балансировщик в облаке).

## Namespace

**Namespace** — виртуальный кластер внутри кластера: логическое разделение (например, `dev`, `prod`). Полезные команды:

```bash
kubectl get namespaces
kubectl -n prod get pods
kubectl create namespace prod
```

## Итог

Мы познакомились с подами, деплойментами, сервисами и labels. Дальше — практика: напишем манифесты и научимся проверять их кодом.

<!--TASK-->
### Задача 1
Создай файл `pod.yml` с подом `web-pod`: образ `nginx:1.27`, метка `app: web`, порт контейнера `80`. Затем создай файл `deployment.yml` с деплойментом `web-deployment`: три реплики, селектор `app: web`, шаблон пода с той же меткой, образ `nginx:1.27`, порт `80`. Ожидаемый результат: оба файла — валидный YAML, и ты можешь объяснить, зачем поду нужны метки, если его создаёт деплоймент.

### Задача 2
Напиши pytest-тест `test_manifests.py`, который читает `deployment.yml` через `yaml.safe_load` и проверяет: `apiVersion` равен `apps/v1`, `kind` равен `Deployment`, в `spec` есть `replicas: 3`, и `selector.matchLabels.app` равно `web`. Добавь такую же проверку для `pod.yml` (kind `Pod`, `spec.containers[0].image` содержит `nginx`). Ожидаемый результат: `pytest test_manifests.py -v` зелёный.

### Задача 3
Расширь тест `test_manifests.py` проверкой согласованности: метки из `selector.matchLabels` деплоймента должны быть подмножеством меток `template.metadata.labels` его шаблона. Напиши отдельную функцию, которая делает этот assert. Если метки расходятся — тест должен падать. Ожидаемый результат: тест зелёный, и ты понимаешь, почему рассогласование селектора и меток ломает управление подами.

### Задача 4
Создай файл `service.yml` с сервисом `web-service` типа `ClusterIP`, селектором `app: web`, портом `80` и `targetPort: 80`. Добавь в тест проверку этого сервиса: kind `Service`, `spec.selector.app` равно `web`, порт `80`. Ожидаемый результат: все три файла проходят валидацию, и сервис «видит» поды деплоймента по меткам.

### Задача 5
Напиши функцию `test_selector_matches_service()`: проверь, что селектор сервиса (`spec.selector.app`) совпадает с меткой пода из шаблона деплоймента (`spec.template.metadata.labels.app`). Это финальная сквозная проверка связки «деплоймент → сервис». Ожидаемый результат: `pytest test_manifests.py -v` полностью зелёный, включая новую функцию.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
У пода обязательные поля: `apiVersion: v1`, `kind: Pod`, `metadata.name`, `spec.containers[0].image` и `ports[0].containerPort`. У деплоймента — `apiVersion: apps/v1`, `kind: Deployment`, `spec.replicas`, `spec.selector.matchLabels`, `spec.template.metadata.labels` и `spec.template.spec.containers`. Метки должны совпадать.

### Подсказка 2
В тесте используй `import yaml` и `yaml.safe_load`. Учитывай, что `yaml.safe_load` вернёт обычный словарь: `doc["spec"]["selector"]["matchLabels"]["app"]`. Если файла нет или он невалидный — `yaml` бросит исключение, и тест упадёт: это и есть проверка.

### Подсказка 3
Собери два множества: `set(doc["spec"]["selector"]["matchLabels"].items())` и `set(doc["spec"]["template"]["metadata"]["labels"].items())`. Затем проверь `assert selector_items <= template_items`. Множества сравниваются по парам «ключ-значение», поэтому совпадение должно быть точным.

### Подсказка 4
Сервис: `apiVersion: v1`, `kind: Service`, `metadata.name`, `spec.selector.app`, `spec.ports[0].port` и `spec.ports[0].targetPort`. В тесте заведи вспомогательную функцию `load_yaml(path)`, чтобы не повторять `open()` и `safe_load()` для каждого файла.

### Подсказка 5
Для сквозной проверки загрузи оба файла: `service = load_yaml("service.yml")`, `dep = load_yaml("deployment.yml")`. Сравни `service["spec"]["selector"]["app"]` и `dep["spec"]["template"]["metadata"]["labels"]["app"]`. Помни: если в кластере сервис ошибается в метке, он просто не получит трафик — тест ловит это заранее.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение. `pod.yml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:1.27
      ports:
        - containerPort: 80
```

`deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

Что здесь происходит? Под — атомарная сущность; его метки используются для группировки. Деплоймент создаёт поды из шаблона `template` и «узнаёт» их по селектору. Метка `app: web` в шаблоне обязана совпасть с `selector.matchLabels` — иначе контроллер не будет считать эти поды своими и создаст новые. Если такой под создать напрямую `kubectl apply -f pod.yml` и затем деплоймент — деплоймент не тронет чужой под, потому что он им не управляет.

### Разбор 2
Решение:

```python
import yaml


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_deployment_metadata():
    dep = load_yaml("deployment.yml")
    assert dep["apiVersion"] == "apps/v1"
    assert dep["kind"] == "Deployment"
    assert dep["metadata"]["name"] == "web-deployment"


def test_deployment_spec():
    dep = load_yaml("deployment.yml")
    spec = dep["spec"]
    assert spec["replicas"] == 3
    assert spec["selector"]["matchLabels"]["app"] == "web"


def test_pod_manifest():
    pod = load_yaml("pod.yml")
    assert pod["kind"] == "Pod"
    assert pod["metadata"]["labels"]["app"] == "web"
    image = pod["spec"]["containers"][0]["image"]
    assert "nginx" in image
```

Что здесь происходит? Функция `load_yaml` читает файл и превращает YAML в словарь. Дальше — обычные asserts по ключам. Если в файле синтаксическая ошибка, `yaml.safe_load` бросит `YAMLError`, и тест упадёт с понятным сообщением — так валидация формата работает сама по себе. Обрати внимание: доступ к вложенным ключам вида `spec["selector"]["matchLabels"]["app"]` — это самая частая точка ошибок, ведь в YAML легко потерять уровень вложенности.

### Разбор 3
Решение:

```python
def test_selector_labels_match_template():
    dep = load_yaml("deployment.yml")
    selector = set(dep["spec"]["selector"]["matchLabels"].items())
    template_labels = set(dep["spec"]["template"]["metadata"]["labels"].items())
    assert selector <= template_labels, \
        "селектор содержит метки, которых нет в шаблоне пода"
```

Что здесь происходит? Мы переводим оба словаря меток во множества пар «ключ-значение»: `{"app": "web"}` станет `{("app", "web")}`. Операция `<=` проверяет, что каждое требование селектора присутствует среди меток шаблона. Если в шаблоне написано `app: frontend`, а селектор ждёт `app: web` — тест падает. Зачем это нужно? В Kubernetes селектор работает как фильтр: контроллер выбирает поды ровно по этим парам. Рассогласование — одна из самых частых «тихих» ошибок: деплоймент создаёт поды, но не считает их своими.

### Разбор 4
Решение. `service.yml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
```

Дополнение в тест:

```python
def test_service_manifest():
    svc = load_yaml("service.yml")
    assert svc["apiVersion"] == "v1"
    assert svc["kind"] == "Service"
    assert svc["spec"]["selector"]["app"] == "web"
    port = svc["spec"]["ports"][0]
    assert port["port"] == 80
    assert port["targetPort"] == 80
```

Что здесь происходит? Сервис — стабильная точка входа. Селектор `app: web` направляет трафик на поды с этой меткой — на те самые, что создаёт деплоймент. `port` — порт, на котором сервис слушает внутри кластера, `targetPort` — порт контейнера. Если бы в сервисе стояла метка `app: frontend`, запросы не находили бы поды, и приложение было бы «мёртвым» без единой ошибки в логах. Тест защищает от такой ситуации.

### Разбор 5
Решение:

```python
def test_service_selector_matches_deployment_pods():
    svc = load_yaml("service.yml")
    dep = load_yaml("deployment.yml")
    service_selector = svc["spec"]["selector"]["app"]
    pod_label = dep["spec"]["template"]["metadata"]["labels"]["app"]
    assert service_selector == pod_label, \
        f"сервис ищет {service_selector}, а поды имеют метку {pod_label}"
```

Что здесь происходит? Это сквозная проверка связки: сервис должен видеть поды деплоймента. Мы вытаскиваем значение селектора сервиса и метку из шаблона деплоймента и сравниваем их. В реальном кластере эта связка — фундамент: без неё сервис не отдаёт трафик, а деплоймент живёт «в пустоте». Такой тест делает проверку инфраструктуры воспроизводимой: он запускается за секунды и ловит ошибки, которые в кластере могли бы всплыть только через минуты диагностики.
<!--/SOLUTION-->

<!--QUIZ-->
Что такое под (Pod) в Kubernetes?
- Минимальная единица запуска контейнеров
- Виртуальная машина
- Сетевой балансировщик
* Правильный ответ: Минимальная единица запуска контейнеров
Под — минимальная единица оркестрации: один или несколько контейнеров.

Кто управляет набором одинаковых подов и умеет их обновлять?
- Deployment
- Service
- Namespace
* Правильный ответ: Deployment
Деплоймент создаёт, обновляет и восстанавливает поды через ReplicaSet.

Зачем нужен селектор в деплойменте?
- Чтобы находить свои поды по меткам
- Чтобы дать поду IP-адрес
- Чтобы ограничить CPU
* Правильный ответ: Чтобы находить свои поды по меткам
selector.matchLabels выбирает поды по меткам из шаблона.

Какой тип сервиса открывает порт на каждом узле кластера?
- NodePort
- ClusterIP
- ExternalName
* Правильный ответ: NodePort
NodePort публикует сервис на порту каждого узла.

Что указывает targetPort в сервисе?
- Порт контейнера, на который ведётся трафик
- Порт API-сервера
- Порт балансировщика
* Правильный ответ: Порт контейнера, на который ведётся трафик
targetPort — порт пода/контейнера, а port — порт самого сервиса.

Какая команда показывает список подов?
- kubectl get pods
- kubectl run pods
- kubectl list pods
* Правильный ответ: kubectl get pods
kubectl get pods выводит поды и их статус.

Что произойдёт, если метки шаблона пода не совпадают с селектором?
- Деплоймент не будет управлять такими подами
- Поды не запустятся
- Кластер упадёт
* Правильный ответ: Деплоймент не будет управлять такими подами
Контроллер выбирает поды строго по селектору.

Что такое namespace?
- Виртуальный кластер для логического разделения ресурсов
- Тип пода
- Имя образа
* Правильный ответ: Виртуальный кластер для логического разделения ресурсов
Namespace разделяет объекты, например dev/prod.

Что делает kubectl describe pod?
- Показывает подробную информацию о поде
- Удаляет под
- Создаёт новый под
* Правильный ответ: Показывает подробную информацию о поде
describe выводит события, статус, контейнеры и причины проблем.

Почему под напрямую считается эфемерным?
- Он может быть пересоздан и не восстанавливается сам
- Он не имеет имени
- Он хранит данные базы
* Правильный ответ: Он может быть пересоздан и не восстанавливается сам
Поды не переживают сбои — для воспроизводимости нужны контроллеры вроде Deployment.
<!--/QUIZ-->
