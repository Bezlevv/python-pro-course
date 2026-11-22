---
title: Exam: Infrastructure as Code
summary: Final exam of the module "Infrastructure as Code" — Ansible, Terraform, Kubernetes, Helm and secrets.
order: 99
duration: 30 min
difficulty: advanced
exam: true
tags: exam, ansible, terraform, kubernetes, helm
---

<!--QUIZ-->
Which tool describes the desired state of infrastructure and creates resources in the cloud?
- Terraform
- Ansible
- kubectl
* Correct answer: Terraform
Terraform manages infrastructure: servers, networks, registries. Ansible configures servers from the inside, and kubectl is an interface to Kubernetes.

Which Ansible command checks a playbook without applying changes?
- ansible-playbook --syntax-check
- ansible-playbook --run
- ansible-playbook --install
* Correct answer: ansible-playbook --syntax-check
--syntax-check verifies the YAML syntax and playbook structure.

What does idempotency mean in Ansible?
- Applying again does not change already-correct state
- The module works only once
- A playbook cannot be run twice
* Correct answer: Applying again does not change already-correct state
Idempotent modules bring the system to the desired state and don't break it again.

What does terraform plan do?
- Shows a change plan without applying
- Immediately applies changes
- Downloads providers
* Correct answer: Shows a change plan without applying
terraform plan is a dry run that prints what will be created, changed, or deleted.

What is a Pod in Kubernetes?
- The smallest unit for running containers
- A virtual machine
- A load balancer
* Correct answer: The smallest unit for running containers
A pod is the smallest unit of orchestration: one or more containers.

What happens if the pod template labels don't match the deployment selector?
- The deployment won't manage such pods
- The cluster will crash
- The pods won't start
* Correct answer: The deployment won't manage such pods
The controller selects pods strictly by the selector's key-value pairs.

Why is readinessProbe needed?
- To remove the pod from the service until it is ready
- To restart the container
- To delete the pod
* Correct answer: To remove the pod from the service until it is ready
readiness decides whether to direct traffic to the pod: an unready pod receives no requests.

How do you attach a ConfigMap to a container?
- Via envFrom.configMapRef
- Via imagePullPolicy
- Via replicas
* Correct answer: Via envFrom.configMapRef
envFrom imports ConfigMap data as environment variables.

What is Helm?
- A package manager for Kubernetes
- A Python compiler
- A database
* Correct answer: A package manager for Kubernetes
Helm packages manifests into charts and templates them.

What is stored in Secret data?
- Values encoded in base64
- Plaintext passwords
- Encrypted keys that cannot be decrypted
* Correct answer: Values encoded in base64
Secret encodes data in base64; it's a storage format, not encryption.

<!--/QUIZ-->
