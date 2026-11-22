---
title: Infrastructure as Code: Terraform basics
summary: Providers, resources, state.
order: 1
duration: 50 min
difficulty: advanced
tags: terraform, iac
---

Terraform manages infrastructure declaratively.

## Main

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}
```

## Commands

```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

## State

Terraform remembers resources in state files.

## Lesson summary

Declare resources; plan→apply.

<!--TASK-->
### Task 1 — Provider
Add a provider.

### Task 2 — Resource
Create a bucket.

### Task 3 — Init
terraform init.

### Task 4 — Plan
Show the plan.

### Task 5 — Apply
Apply changes.

### Task 6 — Destroy
Remove resources.

### Task 7 — State
Explain state.
<!--/TASK-->

<!--HINT-->
### Hint 1
provider.

### Hint 2
resource.

### Hint 3
init.

### Hint 4
plan.

### Hint 5
apply.

### Hint 6
destroy.

### Hint 7
Memory.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```hcl
provider "aws" {
  region = "us-east-1"
}
```

### Solution 2
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}
```

### Solution 3
```bash
terraform init
```

### Solution 4
```bash
terraform plan
# показывает, что будет создано/изменено
```

### Solution 5
```bash
terraform apply
```

### Solution 6
```bash
terraform destroy
```

### Solution 7
```text
State хранит соответствие ресурсов кода
и реальных объектов; по нему Terraform
понимает, что менять
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Terraform?
- IaC tool
- A database
- A browser
- None
* Correct answer: IaC tool
Declarative.

What is a provider?
- Cloud API
- Resource
- State
- None
* Correct answer: Cloud API
AWS.

What is a resource?
- Managed object
- Provider
- File
- None
* Correct answer: Managed object
Bucket.

What is HCL?
- HashiCorp language
- Python
- YAML
- None
* Correct answer: HashiCorp language
Config.

What is init?
- Downloads providers
- Applies
- Destroys
- None
* Correct answer: Downloads providers
Setup.

What is plan?
- Preview
- Applies
- Deletes
- None
* Correct answer: Preview
Diff.

What is apply?
- Executes
- Previews
- Initializes
- None
* Correct answer: Executes
Create.

What is destroy?
- Removes all
- Creates
- Plans
- None
* Correct answer: Removes all
Cleanup.

What is state?
- Record of resources
- Code
- Plan
- None
* Correct answer: Record of resources
tfstate.

What is immutable?
- Replace not edit
- Edit
- Keep
- None
* Correct answer: Replace not edit
Terraform.

What is drift?
- Real vs state
- Same
- Error
- None
* Correct answer: Real vs state
Diff.

What is the benefit?
- Reproducible infra
- Manual
- Required
- None
* Correct answer: Reproducible infra
Versioned.
<!--/QUIZ-->
