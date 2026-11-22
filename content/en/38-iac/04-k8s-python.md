---
title: Deploying a Python Service to Kubernetes
summary: Docker image of a Python app, Deployment with readiness/liveness probes, ConfigMap, resources, and version updates.
order: 4
duration: 45 min
difficulty: advanced
tags: kubernetes, python, docker, deploy, probes
---

We have learned to create pods, deployments, and services. Now let's apply this to a real Python application: build an image, deploy a service, configure probes, and learn to update versions without downtime.

## Docker image of a Python application

Base `Dockerfile` for a FastAPI app:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and publish:

```bash
docker build -t myapp:v1 .
docker push registry.example.com/myapp:v1
```

An image is a self-contained artifact: it contains code, dependencies, and the startup command. In Kubernetes, a container from this image will live in a pod.

## Deployment manifest

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

`resources` describes guarantees (`requests`) and upper bounds (`limits`) for CPU and memory. The scheduler uses requests when placing a pod, and limits protect neighbors from a "gluttonous" application.

## Probes

Kubernetes checks the application's health with three kinds of probes:

- **livenessProbe** — whether the program is alive; if not, the container is restarted.
- **readinessProbe** — whether it is ready to accept traffic; if not, the pod is removed from the service.
- **startupProbe** — for slowly starting applications.

For HTTP services this is usually `httpGet` on the `/health` path:

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

## ConfigMap and environment variables

Configuration is moved into a ConfigMap — a separate resource:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

In the Deployment it is attached via `envFrom` — and the application reads the variables as usual:

```yaml
          envFrom:
            - configMapRef:
                name: myapp-config
```

## Updating versions

Changing the image means editing one line:

```bash
kubectl set image deployment/myapp myapp=registry.example.com/myapp:v2
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
```

A Deployment performs a rolling update: it creates new pods and smoothly drains old ones until the new ones pass readiness probes.

## Summary

We have walked the path of a Python application into Kubernetes: Docker image → Deployment with resources and probes → ConfigMap for configuration → update via rollout. Practice will cement each step.

<!--TASK-->
### Task 1
Create a file `deployment.yml` for the application `myapp`: two replicas, label and selector `app: myapp`, image `registry.example.com/myapp:v1`, container port `8000`, environment variable `APP_ENV=production` via an `env` block. Expected result: the manifest is valid, and you can explain why `env` and `resources` live inside the `containers` list item.

### Task 2
Write a pytest test `test_deployment.py` that reads `deployment.yml` and checks: `replicas == 2`, the image contains `myapp:v1`, port `containerPort == 8000`, and an `env` with name `APP_ENV` and value `production` is configured. Add a check that the container has both `resources.requests` and `resources.limits`. Expected result: `pytest test_deployment.py -v` is green.

### Task 3
Add `livenessProbe` and `readinessProbe` probes to `deployment.yml` with `httpGet` on `/health` and port `8000`, with `initialDelaySeconds` and `periodSeconds` (pick reasonable values). Then extend the test: check that both probes exist, each has `httpGet.path == "/health"`, `httpGet.port == 8000`, and also `initialDelaySeconds` and `periodSeconds`. Expected result: the test is green, and you can explain the difference between liveness and readiness.

### Task 4
Create `configmap.yml` with data `APP_ENV: production` and `LOG_LEVEL: info`, and in `deployment.yml` attach it via `envFrom.configMapRef.name` with value `myapp-config`. Extend the test: check that `configmap.yml` is valid (kind `ConfigMap`), and that the Deployment references `myapp-config` in `envFrom`. Expected result: tests pass, and configuration is separated from the image.

### Task 5
Create `service.yml` of type `ClusterIP` for `myapp`: selector `app: myapp`, port `80`, `targetPort: 8000`. Then write a test `test_rollout.py`: it checks that the image in `deployment.yml` is updatable (i.e., the manifest has an `image` key), and that the service points to the container port `8000`. Expected result: the whole test suite (`pytest -v`) is green, and the "service → deployment → container" chain is consistent.
<!--/TASK-->

<!--HINT-->
### Hint 1
`containers` is a list: even with one container, after `containers:` you need the list marker `-`. Inside the container: `name`, `image`, `ports` (a list), `env` (a list of `name`/`value` dicts), `resources`. The label `app: myapp` must be in both `selector.matchLabels` and `template.metadata.labels`.

### Hint 2
In the test work via `yaml.safe_load`. Access the container: `doc["spec"]["template"]["spec"]["containers"][0]`. Check `container["env"]` — it is a list; find the item with `name == "APP_ENV"`. For resources: `container["resources"]["requests"]` and `container["resources"]["limits"]`.

### Hint 3
Probes are keys inside the container: `livenessProbe` and `readinessProbe`. Each is a dict with `httpGet.path`, `httpGet.port`, `initialDelaySeconds`, `periodSeconds`. Don't forget: yaml is dicts and lists, so `httpGet` is a nested dict.

### Hint 4
ConfigMap: `apiVersion: v1`, `kind: ConfigMap`, `metadata.name`, `data` — a dict of strings. In the Deployment the `envFrom` block is a list: `- configMapRef: { name: myapp-config }`. In the test compare `envFrom[0]["configMapRef"]["name"] == "myapp-config"`.

### Hint 5
Service: `spec.selector.app` must equal `myapp`, and `spec.ports[0].targetPort` must be `8000`. In the test check that `deployment.yml` contains an `image` key (e.g., `container["image"]`) and that its value is non-empty. This guarantees the deployment is actually updatable.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

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

What is going on here? `containers` is a list, so `name` is preceded by a hyphen. Environment is a list of dicts with `name`/`value` pairs; that is the standard way to pass variables into a container. Note the nesting levels: `env` and `ports` live inside the container list item, not at the `spec` level. The label `app: myapp` is repeated in the selector and template — this is a requirement for the Deployment to manage its pods.

### Solution 2
Solution:

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

What is going on here? `get_container()` is a helper that returns the container dict directly, removing repetitive access to deep nesting. The tests check replicas, image, port, environment variable, and the presence of both resource blocks. `any(...)` is handy for checking a list item by condition. If `resources` is missing, `KeyError` will fail the test, which honestly signals the problem.

### Solution 3
Solution. Container fragment:

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

Test:

```python
def check_probe(probe):
    assert probe is not None, "probe is missing"
    assert probe["httpGet"]["path"] == "/health"
    assert probe["httpGet"]["port"] == 8000
    assert probe["initialDelaySeconds"] > 0
    assert probe["periodSeconds"] > 0


def test_probes():
    c = get_container()
    check_probe(c.get("livenessProbe"))
    check_probe(c.get("readinessProbe"))
```

What is going on here? `livenessProbe` decides whether to restart the container: if `/health` does not respond, the container is recreated. `readinessProbe` decides whether to send traffic to the pod: until the probe passes, the pod does not enter the service. `initialDelaySeconds` gives the application time to start; `periodSeconds` is the check frequency. The test checks both probes exist and have their key fields, catching typical typos in paths and ports.

### Solution 4
Solution. `configmap.yml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

Fragment of `deployment.yml`:

```yaml
          envFrom:
            - configMapRef:
                name: myapp-config
```

Test:

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

What is going on here? A ConfigMap stores configuration separately from the image: you can change settings without rebuilding. `envFrom` imports all `data` pairs as environment variables. The test checks both the ConfigMap itself and the reference to it from the Deployment. If the name in `envFrom` does not match `metadata.name`, Kubernetes simply will not pull the variables and the application will be left without configuration; the test guards against this.

### Solution 5
Solution. `service.yml`:

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

Test `test_rollout.py`:

```python
def test_image_is_updatable():
    assert get_container()["image"]


def test_service_targets_container_port():
    svc = load_yaml("service.yml")
    assert svc["spec"]["selector"]["app"] == "myapp"
    assert svc["spec"]["ports"][0]["targetPort"] == 8000
```

What is going on here? A `ClusterIP` service is an internal entry point: port `80` on the outside, `8000` inside the container. The selector `app: myapp` links the service to the deployment's pods. Checking `image` is non-empty guarantees the deployment can be updated with `kubectl set image`. The whole chain — service → selector → pods → container port — is now confirmed by tests that run in seconds without a cluster.

<!--/SOLUTION-->

<!--QUIZ-->
What does livenessProbe do?
- Restarts the container if the application doesn't respond
- Directs traffic to the pod
- Deletes the pod under overload
* Correct answer: Restarts the container if the application doesn't respond
liveness determines whether the process is alive; on failure the container is restarted.

What does readinessProbe do?
- Removes the pod from the service until it is ready
- Restarts the container
- Scales the deployment
* Correct answer: Removes the pod from the service until it is ready
readiness decides whether to accept traffic; an unready pod receives no requests.

What does the resources.requests block describe?
- Guaranteed resources for the container
- The resource limit of the whole cluster
- The number of replicas
* Correct answer: Guaranteed resources for the container
requests is the minimum CPU/memory reserved for the container.

What does the resources.limits block describe?
- The upper bound of the container's resources
- The lower bound of resources
- A threshold for auto-restart
* Correct answer: The upper bound of the container's resources
limits cap the container's consumption from above.

Why is a ConfigMap needed?
- To store configuration separately from the image
- To store secret passwords
- To build Docker images
* Correct answer: To store configuration separately from the image
A ConfigMap lets you change settings without rebuilding the image.

How do you attach a ConfigMap to a container?
- Via envFrom.configMapRef
- Via imagePullPolicy
- Via replicas
* Correct answer: Via envFrom.configMapRef
envFrom imports ConfigMap data as environment variables.

Which command changes the image in a deployment?
- kubectl set image deployment/myapp myapp=...:v2
- kubectl edit pod
- docker push
* Correct answer: kubectl set image deployment/myapp myapp=...:v2
set image updates the container image in the deployment.

What does kubectl rollout undo do?
- Rolls the deployment back to the previous version
- Cancels the apply command
- Deletes the image
* Correct answer: Rolls the deployment back to the previous version
rollout undo restores the previous revision.

Which port does a FastAPI application usually listen on in examples?
- 8000
- 80
- 443
* Correct answer: 8000
uvicorn listens on 8000 by default.

Why is a Deployment better than pods for an application?
- It recreates and updates pods automatically
- It starts faster
- It doesn't use images
* Correct answer: It recreates and updates pods automatically
A Deployment guarantees the desired replica count and can roll updates.

<!--/QUIZ-->
