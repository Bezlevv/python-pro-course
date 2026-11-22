---
title: Configs and Secrets: Helm Basics
summary: Helm chart structure, values.yaml, manifest templating, Kubernetes Secrets, and secure secret storage.
order: 5
duration: 45 min
difficulty: advanced
tags: helm, kubernetes, secrets, templates, values
---

By the third deployment you realize: there are many manifests, they are almost identical, and changing the image version means editing several files at once. **Helm** solves this: it is a package manager for Kubernetes that templates manifests and bundles them into **charts**.

## Chart structure

A minimal chart is a folder with files:

```
myapp/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    └── service.yaml
```

- `Chart.yaml` — chart metadata: name, version, description.
- `values.yaml` — default values; everything that changes between environments goes here.
- `templates/` — Go templates of manifests, where values are substituted via `{{ .Values.name }}`.

Example `Chart.yaml`:

```yaml
apiVersion: v2
name: myapp
description: Python service
type: application
version: 0.1.0
appVersion: "1.0"
```

Example `values.yaml`:

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

## Templating

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

The `{{ ... }}` syntax is Go templates; `.Values` accesses values.yaml, `.Chart` accesses Chart.yaml. The pipe `| default "..."` sets a default value.

Viewing final manifests without installing:

```bash
helm template myapp ./myapp
helm lint ./myapp
```

## Install and upgrade

```bash
helm install myapp ./myapp
helm upgrade myapp ./myapp --set image.tag=v2
helm list
helm uninstall myapp
```

The `--set` flag overrides any value on the fly, and `helm upgrade` updates the release. Helm marks all created resources with its release labels and remembers their state.

## Secrets

A **Secret** is a Kubernetes resource for sensitive data: passwords, tokens, keys. Unlike ConfigMap, the data is stored in base64:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJfc2VjcmV0
```

The value `c3VwZXJfc2VjcmV0` is base64 of `super_secret`. In a template, a Secret is attached the same way as a ConfigMap — via `envFrom` or `secretKeyRef`.

**Important:** base64 is not encryption but encoding. Secrets must not end up in Git in plaintext. In practice, tools like Sealed Secrets, SOPS, or vaults (Vault) are used. The rule is simple: secrets — only via secure delivery mechanisms, not in playbooks and charts.

## Summary

Helm combines manifests into a reusable parameterized chart, and Secret safely stores sensitive data. All that remains is to cement it with practice.

<!--TASK-->
### Task 1
Create the chart structure `myapp/`: files `Chart.yaml` (name `myapp`, version `0.1.0`, `appVersion: "1.0"`, `type: application`) and `values.yaml` with keys `replicaCount: 2`, `image.repository`, `image.tag: v1`, `service.port: 80`, `config.logLevel: info`. Expected result: the directory `myapp/templates/` exists (you may create it empty), and both YAML files are valid.

### Task 2
Write a pytest test `test_chart.py` that checks the chart structure: files `Chart.yaml`, `values.yaml` exist; `Chart.yaml` contains `apiVersion: v2`, `name: myapp`, `version: 0.1.0`; `values.yaml` contains all keys listed in task 1. Use `os.path.exists` for files and `yaml.safe_load` for contents. Expected result: `pytest test_chart.py -v` is green.

### Task 3
Create `templates/deployment.yaml` with templating: `replicas: {{ .Values.replicaCount }}`, image `"{{ .Values.image.repository }}:{{ .Values.image.tag }}"`, label `app: {{ .Chart.Name }}`. Then write a test `test_render.py` that renders this template via Jinja2 with a context assembled from `values.yaml` and `Chart.yaml` (emulating Helm), and checks that the result contains `replicas: 2`, `image: registry.example.com/myapp:v1`, and `app: myapp`. Expected result: rendering succeeds, and the resulting YAML is valid.

### Task 4
Create `templates/service.yaml` with templating of the service type and port: `type: {{ .Values.service.type }}`, `port: {{ .Values.service.port }}`, `targetPort: 8000`, label `app: {{ .Chart.Name }}`. Add a service rendering check to `test_render.py`. Expected result: both templates render correctly, and the test is green.

### Task 5
Create `secret.yml` with a Secret resource `myapp-secret` (type `Opaque`), where `DB_PASSWORD` is base64-encoded from the string `super_secret`. Write a test `test_secret.py` that checks: kind `Secret`, the value `DB_PASSWORD` is valid base64, and its decoded value equals `super_secret`. Expected result: the test is green, and you can explain why base64 is not protection but just a storage format.
<!--/TASK-->

<!--HINT-->
### Hint 1
The key order in `Chart.yaml` does not matter, but the names are required: `apiVersion`, `name`, `description`, `type`, `version`, `appVersion`. In `values.yaml` nested keys: `image: { repository: ..., tag: v1 }`, `service: { port: 80 }`, `config: { logLevel: info }`.

### Hint 2
For checking keys write small helpers: `def load_yaml(path): ...`. Check nested keys via nested asserts, e.g., `assert values["image"]["tag"] == "v1"`. Don't forget `import os` and `os.path.exists`.

### Hint 3
Jinja2 and Helm use different syntax, but for learning purposes we render via `Template(...).render(**ctx)`. Build the context: `ctx = {"Values": values, "Chart": chart}` — and in the template use `{{ Values.replicaCount }}` and `{{ Chart.Name }}` (without dot prefixes, unlike Helm). After rendering, parse the result with `yaml.safe_load` and check keys.

### Hint 4
The service renders the same way: `{{ Values.service.type }}`, `{{ Values.service.port }}`, `{{ Chart.Name }}`. After rendering check `yaml.safe_load(rendered)["spec"]["ports"][0]["port"] == 80`. Specify targetPort as the constant `8000`.

### Hint 5
Encode the value in advance: `import base64; encoded = base64.b64encode(b"super_secret").decode()`. In the test decode it back: `base64.b64decode(secret["data"]["DB_PASSWORD"]).decode() == "super_secret"`. To check base64 validity you can wrap decoding in `try/except binascii.Error`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution. `myapp/Chart.yaml`:

```yaml
apiVersion: v2
name: myapp
description: Python service
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

What is going on here? `Chart.yaml` is the chart's passport: `version` — the chart's version, `appVersion` — the version of the application inside. `values.yaml` — all the "knobs": replica count, image, service, configuration. Environments differ precisely in values, not templates: for stage you create your own `values-stage.yaml`, and the manifests stay unchanged.

### Solution 2
Solution:

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

What is going on here? The first test checks the files exist and the `templates` directory is in place. Then the contents: `Chart.yaml` must contain schema version `v2` and the name, and `values.yaml` — all keys the templates will rely on. If a key is missing from values, templating will fail — the test catches it in advance.

### Solution 3
Solution. `myapp/templates/deployment.yaml`:

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

Test `test_render.py`:

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

What is going on here? We emulate Helm: `render_template` substitutes a context — the `Values` and `Chart` dicts — into the template. The difference from real Helm is only in syntax (`Values.replicaCount` instead of `.Values.replicaCount`). After rendering the result is parsed as YAML, and the test checks actual values. Such a test is the "gold standard" for a chart: it validates the template without installing a cluster.

### Solution 4
Solution. `myapp/templates/service.yaml`:

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

Addition to `test_render.py`:

```python
def test_service_renders():
    rendered = render_template("myapp/templates/service.yaml", build_context())
    doc = yaml.safe_load(rendered)
    assert doc["spec"]["type"] == "ClusterIP"
    assert doc["spec"]["ports"][0]["port"] == 80
    assert doc["spec"]["ports"][0]["targetPort"] == 8000
    assert doc["spec"]["selector"]["app"] == "myapp"
```

What is going on here? The service takes its type and port from values, and the selector from the chart name. `targetPort: 8000` is a constant because it is the container port determined by the application code. The test checks all values were substituted. Now changing the port in values changes both Deployment and Service — consistently, without editing two files.

### Solution 5
Solution. `secret.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJfc2VjcmV0
```

Test `test_secret.py`:

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
        raise AssertionError("value is not valid base64")
    assert decoded == "super_secret"
```

What is going on here? `base64.b64decode` with `validate=True` strictly checks encoding correctness. The value `c3VwZXJfc2VjcmV0` is `super_secret` in base64. It is important to understand: base64 is not encryption — anyone can decode a Secret from the cluster. That is why in real projects secrets are encrypted and stored outside Git, delivered to the cluster via Sealed Secrets or Vault. The test only checks the format, not security.

<!--/SOLUTION-->

<!--QUIZ-->
What is Helm?
- A package manager for Kubernetes
- A Docker image build tool
- A database for logs
* Correct answer: A package manager for Kubernetes
Helm packages and templates Kubernetes manifests.

What does values.yaml contain?
- Default values for chart parameters
- Secret passwords in plaintext
- Application code
* Correct answer: Default values for chart parameters
values.yaml holds the "knobs" that change between environments.

How do you access a value from values.yaml in a Helm template?
- {{ .Values.name }}
- {{ .Data.name }}
- {{ values.name }}
* Correct answer: {{ .Values.name }}
Access to values goes through .Values, and to Chart.yaml through .Chart.

Which command shows final manifests without installing?
- helm template
- helm install
- helm uninstall
* Correct answer: helm template
helm template renders manifests and prints them without installing anything.

Which command updates a release with a new image?
- helm upgrade myapp ./myapp --set image.tag=v2
- helm install myapp ./myapp
- helm list
* Correct answer: helm upgrade myapp ./myapp --set image.tag=v2
helm upgrade applies changes; --set overrides a value.

What is a Secret in Kubernetes?
- A resource for storing sensitive data in base64
- A resource for storing public configs
- A pod type
* Correct answer: A resource for storing sensitive data in base64
A Secret stores passwords and tokens in encoded form.

Is base64 encryption?
- No, it's just encoding
- Yes, it's reliable encryption
- Only for passwords
* Correct answer: No, it's just encoding
base64 is easily decoded — it's a storage format, not protection.

Which tool helps store secrets encrypted outside Git?
- Sealed Secrets or SOPS
- kubectl run
- docker build
* Correct answer: Sealed Secrets or SOPS
They encrypt secrets before they reach the repository.

What does helm lint do?
- Checks the chart's syntax and structure
- Installs the chart
- Deletes the chart
* Correct answer: Checks the chart's syntax and structure
helm lint finds typical errors in a chart.

Which Chart.yaml key stores the version of the application inside the chart?
- appVersion
- version
- apiVersion
* Correct answer: appVersion
appVersion is the application's version; version is the chart's own version.

<!--/QUIZ-->
