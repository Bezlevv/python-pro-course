---
title: Project: Full Infrastructure Stack
summary: An end-to-end project: Git → Ansible → Terraform → Kubernetes → Helm; assembling all manifests and protecting them with tests.
order: 6
duration: 60 min
difficulty: advanced
tags: project, devops, ansible, terraform, kubernetes, helm
---

This is the module's final lesson. We'll assemble the whole stack into one project and write end-to-end tests that validate infrastructure as code — without a cluster, in seconds. You'll create a `project/` folder with a complete set of manifests and tests for them.

## The full infrastructure cycle

In a real project, infrastructure lives through this cycle:

1. **Code** lands in Git; CI builds the Docker image.
2. **Terraform** creates the cluster and infrastructure (networks, nodes, image registry).
3. **Ansible** configures servers that are not yet in the cluster (or further configures nodes).
4. **Kubernetes + Helm** deploy the application: a chart with values and secrets.
5. **Secrets** are delivered securely — not in Git.

The final "code → image → pod" chain diagram looks like this:

```
Git → CI (image build) → Registry
                              ↓
Terraform → K8s cluster ← Helm (application chart)
                              ↓
                  Deployment → Pods → Service → traffic
```

Each layer is described by code, hence verified by tests.

## What should be in the project

Minimal set of application manifests:

- `configmap.yml` — environment configuration;
- `secret.yml` — secrets (base64);
- `deployment.yml` — the application with probes and resources;
- `service.yml` — the entry point.

Plus `Chart.yaml`/`values.yaml` if we use the Helm approach, and the templates folder itself. Our project will collect it all together.

## Infrastructure as testable code

The main skill of the lesson is **verifying infrastructure before applying it**. Until a manifest passes pytest, it should not go to the cluster. This is the same principle as "don't push code that hasn't passed the linter".

Practical checks:

- YAML is valid (syntax) — `yaml.safe_load`;
- required fields exist: `apiVersion`, `kind`, `metadata.name`;
- references are consistent: service → selector → pod labels;
- Deployment references existing ConfigMap and Secret;
- secrets never appear in plaintext in manifests.

## Commands for applying

When all tests are green, the project is applied with real commands:

```bash
terraform init && terraform plan
ansible-playbook -i hosts.yml site.yml
kubectl apply -f project/manifests/
helm upgrade --install myapp ./project/chart
kubectl get deployments,svc
```

But first — tests. Let's go.

<!--TASK-->
### Task 1
Create the folder `project/manifests/` and in it four files: `configmap.yml` (data `APP_ENV: production`, `LOG_LEVEL: info`), `secret.yml` (Secret `app-secret`, type `Opaque`, value `API_TOKEN` — base64 of `secret-token`), `deployment.yml` (Deployment `app`, two replicas, image `registry.example.com/app:v1`, port `8000`, `/health` probes, references to ConfigMap and Secret via `envFrom`), `service.yml` (Service `app-service`, selector `app: app`, port `80`, `targetPort: 8000`). Expected result: four valid YAML files.

### Task 2
Write a test `test_manifests.py` that iterates over all files in `project/manifests/`, parses each with `yaml.safe_load`, and checks: each has `apiVersion` and `kind`; for `Deployment` and `Service` the label `app: app` is present in the selector. Also check that no file raised an exception during parsing. Expected result: `pytest test_manifests.py -v` is green.

### Task 3
Add an end-to-end connectivity check to `test_manifests.py`: the service selector (`app: app`) matches the `app` label in the deployment template; the Deployment references a ConfigMap named `app-config` and a Secret named `app-secret` (search in `envFrom`); the service's `targetPort` equals the container port (`8000`). Expected result: the test is green, and the "deployment → configuration → service" links are confirmed.

### Task 4
Create a script `deploy.sh` that applies all manifests: `kubectl apply -f project/manifests/`, then waits for the deployment to be ready with `kubectl rollout status deployment/app` and prints the service list `kubectl get svc`. Make it executable (in a comment specify the command `chmod +x deploy.sh`). Write a test `test_deploy_sh.py` that checks the script exists, contains `kubectl apply` and `kubectl rollout status`, and starts with the shebang `#!/bin/bash`.

### Task 5
Write a test `test_no_plain_secrets.py`: read all YAML files from `project/manifests/` as text and check that nowhere does the plaintext string `secret-token` appear (it should exist only in base64 form inside the Secret). Additionally check that in `secret.yml` the `API_TOKEN` value decodes back to `secret-token`. Expected result: tests are green, and the secret has not "leaked" into manifests.
<!--/TASK-->

<!--HINT-->
### Hint 1
Remember list hyphens: `containers:` is a list, `envFrom:` is also a list. ConfigMap and Secret names must match across files: in `configmap.yml` use `metadata.name: app-config`, and in `deployment.yml` — `name: app-config` in `configMapRef`.

### Hint 2
Create a helper `def load_yaml(path):` with `open(path, encoding="utf-8")` and `yaml.safe_load`. For directory traversal — `os.listdir("project/manifests/")` and the `.endswith(".yml")` filter. Collect all errors into a list and at the end make one assert on the list being empty.

### Hint 3
Selector access: `dep["spec"]["selector"]["matchLabels"]["app"]`. Template label: `dep["spec"]["template"]["metadata"]["labels"]["app"]`. `envFrom` is a list: look for `ref["configMapRef"]["name"] == "app-config"`. Service `targetPort`: `svc["spec"]["ports"][0]["targetPort"] == 8000`.

### Hint 4
The shebang is the first line `#!/bin/bash`. Read the file as text and check `"kubectl apply" in text` and `"kubectl rollout status" in text`. Existence — `os.path.exists("deploy.sh")`.

### Hint 5
To check for the absence of a plaintext secret, iterate the files and do `assert "secret-token" not in text` — but only for files where `kind != "Secret"`. In the Secret itself check decoding: `base64.b64decode(yaml.safe_load(open("project/manifests/secret.yml"))["data"]["API_TOKEN"]).decode() == "secret-token"`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution. `project/manifests/configmap.yml`:

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

What is going on here? This is a complete minimal set: configuration in ConfigMap, secret in Secret (base64 of `secret-token`), the application in Deployment with references to both resources, traffic through Service. All names are consistent: `app-config`, `app-secret`, label `app: app`.

### Solution 2
Solution:

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
    assert not errors, f"invalid YAML: {errors}"


def test_required_fields():
    for path in list_manifests():
        doc = load_yaml(path)
        assert "apiVersion" in doc, f"{path}: no apiVersion"
        assert "kind" in doc, f"{path}: no kind"


def test_app_label_in_selectors():
    for path in list_manifests():
        doc = load_yaml(path)
        if doc.get("kind") in ("Deployment", "Service"):
            selector = doc["spec"].get("selector", {})
            labels = selector.get("matchLabels", selector)
            assert labels.get("app") == "app", f"{path}: no label app: app"
```

What is going on here? The tests iterate over all files: YAML validity, required fields, label presence in selectors. Validation errors are collected into a list so you see all problems at once, not just the first. Such a "scanning" test scales: add a new manifest and it automatically falls under the checks. `matchLabels` and `selector` differ between Deployment and Service, so we take `selector.get("matchLabels", selector)`.

### Solution 3
Solution:

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

What is going on here? This is the heart of the end-to-end check: the service sees the deployment's pods (selector = label), the Deployment references existing ConfigMap and Secret, and the service port leads to the container port. If these links are desynchronized in the cluster, the application silently does not work — the test finds the problem before deployment.

### Solution 4
Solution. `deploy.sh`:

```bash
#!/bin/bash
set -euo pipefail

kubectl apply -f project/manifests/
kubectl rollout status deployment/app
kubectl get svc
```

Test `test_deploy_sh.py`:

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

What is going on here? `set -euo pipefail` makes the script fail on any error — otherwise kubectl could silently fail to apply something. The shebang and commands are checked by tests. Executability is set with `chmod +x deploy.sh`. Such a script is the "one button" for applying the project's entire infrastructure.

### Solution 5
Solution:

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
        assert "secret-token" not in text, f"{path}: plaintext secret!"


def test_secret_decodes_back():
    secret = load_yaml(f"{MANIFESTS}/secret.yml")
    encoded = secret["data"]["API_TOKEN"]
    decoded = base64.b64decode(encoded).decode()
    assert decoded == "secret-token"
```

What is going on here? The first test goes through all manifests except the Secrets themselves and makes sure the plaintext string `secret-token` is nowhere. The second checks that the Secret value is really base64 and decodes back to the original. This is minimal leak protection: the secret exists in one place, in the right form, and is not duplicated in plaintext. In a real project, encryption (SOPS, Sealed Secrets) is used instead — but even a basic check filters out most mistakes.

<!--/SOLUTION-->

<!--QUIZ-->
Which tool creates a cluster and cloud infrastructure?
- Terraform
- Ansible
- Helm
* Correct answer: Terraform
Terraform manages infrastructure: networks, nodes, registries.

Which tool configures servers from the inside?
- Ansible
- Terraform
- kubectl apply
* Correct answer: Ansible
Ansible manages configuration on already-created servers.

What combines application manifests into a reusable package?
- Helm
- Docker
- pip
* Correct answer: Helm
Helm is a package manager for Kubernetes.

What should happen to a manifest before applying it in the cluster?
- Pass automated checks
- Be deleted
- Be committed only to a local branch
* Correct answer: Pass automated checks
Infrastructure as code is verified by tests before deployment.

What checks the "service → selector → pod labels" link?
- Consistency of references between manifests
- Network speed
- Python version
* Correct answer: Consistency of references between manifests
End-to-end tests cross-check references and labels between resources.

Why must secrets not be stored in plaintext in Git?
- They're easy to steal if the repository leaks
- They slow down the build
- They break YAML
* Correct answer: They're easy to steal if the repository leaks
Secrets in Git mean instant leakage whenever the repository leaks.

What does kubectl rollout status deployment/app do?
- Waits until the deployment reaches readiness
- Deletes the deployment
- Creates a new namespace
* Correct answer: Waits until the deployment reaches readiness
rollout status blocks until the update completes.

What does set -euo pipefail mean in a bash script?
- The script fails on any error
- The script cannot be stopped
- The script runs only as root
* Correct answer: The script fails on any error
This guards against silent partial applications.

How does base64 differ from encryption?
- base64 is easily decoded and doesn't protect
- base64 cannot be decoded
- base64 stores only numbers
* Correct answer: base64 is easily decoded and doesn't protect
base64 is an encoding format, not protection.

What does the test_no_plain_secrets test do?
- Looks for plaintext secrets in all manifests except Secret
- Checks for a docker image
- Checks the kubectl version
* Correct answer: Looks for plaintext secrets in all manifests except Secret
The test guarantees the secret is not duplicated in plaintext.

<!--/QUIZ-->
