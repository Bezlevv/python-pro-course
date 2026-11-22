---
title: Kubernetes: Pods, Deployments, Services
summary: Cluster architecture, pods, deployments, services and labels; writing our first manifests and working with kubectl.
order: 3
duration: 45 min
difficulty: advanced
tags: kubernetes, kubectl, pods, deployments, services
---

Kubernetes (K8s) is a container orchestrator: it runs, scales, and self-heals containers across a pool of servers. If Docker packages an application into an image, Kubernetes distributes containers across the cluster and makes sure there are exactly as many as needed.

## Cluster architecture

A cluster consists of two node roles:

- **Control plane** (control nodes) — makes decisions: the scheduler, API server, `etcd` storage, and controllers. The user interacts with it through `kubectl`.
- **Worker nodes** — run containers inside **pods**.

All manifests are sent to the API server, and controllers bring the cluster to the desired state.

## Pods

A **Pod** is the smallest unit of execution: one or more containers that share a network and storage. Usually a pod has one container. A pod manifest:

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

Running and viewing:

```bash
kubectl apply -f pod.yml
kubectl get pods
kubectl describe pod web-pod
kubectl logs web-pod
```

Pods are ephemeral entities. If a pod dies, Kubernetes will not "revive" it by itself — that is what controllers are for.

## Deployments

A **Deployment** is a controller that manages a set of identical pods (via a ReplicaSet). It can recreate pods, update images, and roll back:

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

An important point — the **selector**: `selector.matchLabels` must match the labels of pods in `template.metadata.labels`. A Deployment only "sees" pods whose labels match the selector.

## Services

Pods get dynamic IPs and can be recreated. A **Service** is a stable entry point. Type `ClusterIP` provides a virtual IP inside the cluster:

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

`selector` — the same `app: web` labels, `port` is the service port, `targetPort` is the container port. Other types: `NodePort` (opens a port on every node) and `LoadBalancer` (an external cloud load balancer).

## Namespace

A **Namespace** is a virtual cluster inside the cluster: logical separation (for example, `dev`, `prod`). Useful commands:

```bash
kubectl get namespaces
kubectl -n prod get pods
kubectl create namespace prod
```

## Summary

We got acquainted with pods, deployments, services, and labels. Next — practice: we'll write manifests and learn to verify them with code.

<!--TASK-->
### Task 1
Create a file `pod.yml` with a pod `web-pod`: image `nginx:1.27`, label `app: web`, container port `80`. Then create a file `deployment.yml` with a deployment `web-deployment`: three replicas, selector `app: web`, pod template with the same label, image `nginx:1.27`, port `80`. Expected result: both files are valid YAML, and you can explain why a pod needs labels when it is created by a deployment.

### Task 2
Write a pytest test `test_manifests.py` that reads `deployment.yml` via `yaml.safe_load` and checks: `apiVersion` equals `apps/v1`, `kind` equals `Deployment`, `spec` has `replicas: 3`, and `selector.matchLabels.app` equals `web`. Add the same check for `pod.yml` (kind `Pod`, `spec.containers[0].image` contains `nginx`). Expected result: `pytest test_manifests.py -v` is green.

### Task 3
Extend the test `test_manifests.py` with a consistency check: the labels from the deployment's `selector.matchLabels` must be a subset of the labels of its template's `template.metadata.labels`. Write a separate function that makes this assert. If the labels diverge, the test must fail. Expected result: the test is green, and you understand why selector/label mismatch breaks pod management.

### Task 4
Create a file `service.yml` with a service `web-service` of type `ClusterIP`, selector `app: web`, port `80`, and `targetPort: 80`. Add a check for this service to the test: kind `Service`, `spec.selector.app` equals `web`, port `80`. Expected result: all three files pass validation, and the service "sees" the deployment's pods by labels.

### Task 5
Write a function `test_selector_matches_service()`: check that the service's selector (`spec.selector.app`) matches the pod label from the deployment template (`spec.template.metadata.labels.app`). This is the final end-to-end check of the "deployment → service" link. Expected result: `pytest test_manifests.py -v` is fully green, including the new function.
<!--/TASK-->

<!--HINT-->
### Hint 1
A pod's required fields: `apiVersion: v1`, `kind: Pod`, `metadata.name`, `spec.containers[0].image`, and `ports[0].containerPort`. For a deployment: `apiVersion: apps/v1`, `kind: Deployment`, `spec.replicas`, `spec.selector.matchLabels`, `spec.template.metadata.labels`, and `spec.template.spec.containers`. Labels must match.

### Hint 2
In the test use `import yaml` and `yaml.safe_load`. Note that `yaml.safe_load` returns an ordinary dict: `doc["spec"]["selector"]["matchLabels"]["app"]`. If the file is missing or invalid, `yaml` will raise an exception and the test will fail — that itself is the check.

### Hint 3
Collect two sets: `set(doc["spec"]["selector"]["matchLabels"].items())` and `set(doc["spec"]["template"]["metadata"]["labels"].items())`. Then check `assert selector_items <= template_items`. Sets are compared by "key-value" pairs, so the match must be exact.

### Hint 4
Service: `apiVersion: v1`, `kind: Service`, `metadata.name`, `spec.selector.app`, `spec.ports[0].port`, and `spec.ports[0].targetPort`. In the test create a helper function `load_yaml(path)` to avoid repeating `open()` and `safe_load()` for each file.

### Hint 5
For the end-to-end check load both files: `service = load_yaml("service.yml")`, `dep = load_yaml("deployment.yml")`. Compare `service["spec"]["selector"]["app"]` and `dep["spec"]["template"]["metadata"]["labels"]["app"]`. Remember: if the service has a wrong label in the cluster, it simply will not receive traffic — the test catches this in advance.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution. `pod.yml`:

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

What is going on here? A pod is an atomic entity; its labels are used for grouping. A deployment creates pods from the `template` and "recognizes" them by the selector. The label `app: web` in the template must match `selector.matchLabels` — otherwise the controller will not consider those pods its own and will create new ones. If you create such a pod directly with `kubectl apply -f pod.yml` and then a deployment, the deployment will not touch someone else's pod because it does not manage it.

### Solution 2
Solution:

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

What is going on here? `load_yaml` reads the file and turns YAML into a dict. Then come ordinary asserts on keys. If the file has a syntax error, `yaml.safe_load` raises `YAMLError`, and the test fails with a clear message — format validation works by itself. Note: accessing nested keys like `spec["selector"]["matchLabels"]["app"]` is the most common source of errors, since it is easy to lose a nesting level in YAML.

### Solution 3
Solution:

```python
def test_selector_labels_match_template():
    dep = load_yaml("deployment.yml")
    selector = set(dep["spec"]["selector"]["matchLabels"].items())
    template_labels = set(dep["spec"]["template"]["metadata"]["labels"].items())
    assert selector <= template_labels, \
        "selector contains labels that are not in the pod template"
```

What is going on here? We convert both label dicts into sets of "key-value" pairs: `{"app": "web"}` becomes `{("app", "web")}`. The `<=` operation checks that every selector requirement is present among the template labels. If the template says `app: frontend` but the selector expects `app: web`, the test fails. Why is this needed? In Kubernetes the selector acts as a filter: the controller selects pods exactly by these pairs. Mismatch is one of the most common "silent" errors: a deployment creates pods but does not consider them its own.

### Solution 4
Solution. `service.yml`:

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

Addition to the test:

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

What is going on here? A service is a stable entry point. The selector `app: web` directs traffic to pods with that label — exactly the ones the deployment creates. `port` is the port the service listens on inside the cluster, `targetPort` is the container port. If the service had the label `app: frontend`, requests would not find pods and the application would be "dead" without a single error in the logs. The test protects against that.

### Solution 5
Solution:

```python
def test_service_selector_matches_deployment_pods():
    svc = load_yaml("service.yml")
    dep = load_yaml("deployment.yml")
    service_selector = svc["spec"]["selector"]["app"]
    pod_label = dep["spec"]["template"]["metadata"]["labels"]["app"]
    assert service_selector == pod_label, \
        f"service looks for {service_selector}, but pods have label {pod_label}"
```

What is going on here? This is an end-to-end check of the link: the service must see the deployment's pods. We extract the service selector value and the label from the deployment template and compare them. In a real cluster this link is the foundation: without it the service does not deliver traffic and the deployment lives "in a void". Such a test makes infrastructure verification reproducible: it runs in seconds and catches errors that in a cluster might surface only after minutes of diagnostics.

<!--/SOLUTION-->

<!--QUIZ-->
What is a Pod in Kubernetes?
- The smallest unit for running containers
- A virtual machine
- A network load balancer
* Correct answer: The smallest unit for running containers
A pod is the smallest unit of orchestration: one or more containers.

Who manages a set of identical pods and can update them?
- Deployment
- Service
- Namespace
* Correct answer: Deployment
A deployment creates, updates, and restores pods via a ReplicaSet.

Why does a deployment need a selector?
- To find its pods by labels
- To give a pod an IP address
- To limit CPU
* Correct answer: To find its pods by labels
selector.matchLabels selects pods by the labels from the template.

Which service type opens a port on every node of the cluster?
- NodePort
- ClusterIP
- ExternalName
* Correct answer: NodePort
NodePort publishes the service on a port of every node.

What does targetPort indicate in a service?
- The container port that receives traffic
- The API server port
- The load balancer port
* Correct answer: The container port that receives traffic
targetPort is the pod/container port, while port is the service's own port.

Which command shows the list of pods?
- kubectl get pods
- kubectl run pods
- kubectl list pods
* Correct answer: kubectl get pods
kubectl get pods lists pods and their status.

What happens if the pod template labels don't match the selector?
- The deployment won't manage such pods
- The pods won't start
- The cluster will crash
* Correct answer: The deployment won't manage such pods
The controller selects pods strictly by the selector.

What is a namespace?
- A virtual cluster for logically separating resources
- A pod type
- An image name
* Correct answer: A virtual cluster for logically separating resources
A namespace separates objects, e.g., dev/prod.

What does kubectl describe pod do?
- Shows detailed information about a pod
- Deletes a pod
- Creates a new pod
* Correct answer: Shows detailed information about a pod
describe outputs events, status, containers, and causes of problems.

Why is a bare pod considered ephemeral?
- It can be recreated and doesn't recover on its own
- It has no name
- It stores database data
* Correct answer: It can be recreated and doesn't recover on its own
Pods don't survive failures — for reproducibility you need controllers like Deployment.

<!--/QUIZ-->
