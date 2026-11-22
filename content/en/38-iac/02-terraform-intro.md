---
title: Terraform: Infrastructure as Code
summary: Declarative infrastructure description: providers, resources, variables, outputs; the terraform init/plan/apply lifecycle.
order: 2
duration: 40 min
difficulty: advanced
tags: terraform, iac, hcl, providers, state
---

Ansible configures servers *from the inside*, but who creates the servers themselves, networks, databases, and load balancers? There is a second class of IaC tools for that — **Terraform**. If Ansible answers "what should a server look like", Terraform answers "what infrastructure should exist at all".

## Declarative approach

Terraform by HashiCorp describes the **desired state** of infrastructure in configuration files. You write "let there be a server with this image and this network", and Terraform brings reality to that description. It does not care about the order in which resources are created — it builds the dependency graph itself.

Main concepts:

- **Provider** — a plugin that knows the API of a specific platform: AWS, Google Cloud, Yandex Cloud, Azure, as well as local tools (for example, `random`, `local`).
- **Resource** — a single entity: a virtual machine, network, DNS record, file.
- **Variable** — configuration parameters.
- **Output** — published values, for example the IP address of a created server.
- **State** — the `terraform.tfstate` file where Terraform stores the current actual state.

## The HCL language

Terraform uses its own language — **HCL** (HashiCorp Configuration Language). Its syntax resembles JSON but reads more easily:

```hcl
provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "web-server"
  }
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

The key idea is **resource references**: `aws_instance.web.public_ip` accesses an attribute of the resource `aws_instance` named `web`. If resource `A` uses an attribute of resource `B`, Terraform understands the dependency and creates `B` first.

## Lifecycle

Main commands:

```bash
terraform init      # downloads providers and modules
terraform validate  # checks configuration syntax
terraform plan      # shows a change plan
terraform apply     # applies changes (creates/modifies resources)
terraform destroy   # removes all infrastructure
terraform show      # shows current state
```

`terraform plan` is a "dry run": it prints what will be created, changed, or deleted without touching anything. `terraform apply` asks for confirmation (or proceeds if you pass `-auto-approve`). After apply, `terraform.tfstate` appears in the directory — it must not be edited by hand and should be kept somewhere safe (for example, remote state on S3).

## Example: a local file

To try Terraform without a cloud, use the `local` provider:

```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello from Terraform!"
}
```

After `terraform init` and `terraform apply`, the file `hello.txt` appears. This is a convenient way to practice the lifecycle without money or accounts.

## Variables and tfvars

Variables are declared in `variables.tf`; default values go through `default`. Real values go into the `terraform.tfvars` file:

```hcl
# terraform.tfvars
project_name = "pythonpro"
instance_type = "t3.micro"
```

Terraform automatically reads `terraform.tfvars` on `plan`/`apply`. Value priority: command-line flags → tfvars files → environment variables → `default` in the declaration.

## Summary

Terraform declaratively manages the entire infrastructure: it creates, changes, and deletes resources, stores state, and builds dependencies. Together with Ansible they form a pair: Terraform spins up servers, Ansible configures them from the inside. Now let's reinforce with practice.

<!--TASK-->
### Task 1
Create a file `main.tf` with the `local` provider and a `local_file` resource named `hello` that creates the file `hello.txt` with the content `Hello from Terraform!`. Then create a file `variables.tf` with a variable `greeting` (type `string`, default value `Hello from Terraform!`) and use it in the resource's `content`. Expected result: the configuration has no "hardcoded" string literals, and `terraform validate` passes without errors.

### Task 2
Write a pytest test `test_main_tf.py` that parses `main.tf` with the `python-hcl2` library (function `hcl2.load`) and checks: the configuration has a `local` provider, a `local_file` resource named `hello`, and this resource declares the keys `filename` and `content`. Also add a check that `content` contains a reference to the variable `var.greeting`. Expected result: `pytest test_main_tf.py -v` is green.

### Task 3
Extend the configuration: add a `random_string` resource (`random` provider) with `length = 8`, `upper = false`, `special = false`, and in `local_file` add a third field `content` (or extend `content` by combining with `${var.greeting} ${random_string.result}`). Then add `output "greeting_file"` with the path `local_file.hello.filename`. Expected result: `main.tf` depends on `random_string` and has an output variable; `terraform validate` passes.

### Task 4
Write a pytest test `test_variables_tf.py`: check that `variables.tf` declares a variable `greeting`, it has a key `type` with value `string`, and it is actually used in `main.tf` (the reference `var.greeting` appears in the file text). Additionally, check that `terraform.tfvars` does not contain variables missing from `variables.tf`. Expected result: all checks pass, and you know how to protect configuration from "dangling" variables.

### Task 5
Create a file `terraform.tfvars` with the value `greeting = "Привет из Terraform!"` and a file `outputs.tf` with an output `greeting_content` that returns `local_file.hello.content`. Write a test `test_outputs_tf.py` that parses `outputs.tf` and checks that the output `greeting_content` exists and its `value` references `local_file.hello.content`. Expected result: the test is green, and the configuration is fully parameterized.
<!--/TASK-->

<!--HINT-->
### Hint 1
HCL syntax: a resource block — `resource "type" "name" { ... }`, a provider block — `provider "local" {}`. A variable is declared with a `variable "name" { type = string; default = ... }` block. Reference to a variable — `var.greeting`. Before `terraform validate` you need `terraform init` — otherwise Terraform does not know the providers.

### Hint 2
`python-hcl2` returns a dict where the key `"local_file"` may live in a list under the key `"resource"`. Use `cfg.get("resource", [])` and iterate the list to find the block containing `"local_file"`. For text checks you can read `main.tf` as plain text and look for `var.greeting`.

### Hint 3
The `random` provider is declared the same way as `local`. The `random_string` resource has an attribute `result`. Reference it from another resource as `random_string.<name>.result`. An output is declared with an `output "name" { value = ... }` block. Don't forget to add `provider "random" {}`.

### Hint 4
To check for "dangling" variables, read `terraform.tfvars` as plain text (or parse it), collect the key names, then compare with the set of names from `variables.tf`. In `variables.tf`, names come after `variable "` up to the closing quote.

### Hint 5
In `outputs.tf` an output block looks like this: `output "greeting_content" { value = local_file.hello.content }`. In the test use `hcl2.load` and find the `output` block, then check that `value` is a string containing `local_file.hello.content`.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution. `variables.tf`:

```hcl
variable "greeting" {
  type    = string
  default = "Hello from Terraform!"
}
```

`main.tf`:

```hcl
provider "local" {}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = var.greeting
}
```

What is going on here? The `local` provider can create local files without asking anything from the cloud. The `local_file` resource has two required fields: `filename` — the path to the file, and `content` — its contents. Instead of a literal, we reference the variable `var.greeting`. `terraform init && terraform validate` will show the configuration is correct. This example is ideal for first practice: it really runs without accounts and money.

### Solution 2
Solution:

```python
import hcl2


def load_tf(path):
    with open(path, encoding="utf-8") as f:
        return hcl2.load(f)


def test_has_local_provider():
    cfg = load_tf("main.tf")
    assert "local" in cfg.get("provider", [])[0]


def test_has_local_file_resource():
    cfg = load_tf("main.tf")
    resources = cfg.get("resource", [])
    found = any("local_file" in r for r in resources)
    assert found, "local_file resource not found"


def test_local_file_has_required_keys():
    cfg = load_tf("main.tf")
    for r in cfg.get("resource", []):
        if "local_file" in r:
            block = r["local_file"][0]["hello"]
            assert "filename" in block
            assert "content" in block
            assert "var.greeting" in str(block["content"])
            return
    raise AssertionError("local_file not found")
```

What is going on here? `hcl2.load` returns a dict where `provider` is a list of dicts, and `resource` is a list whose items have the resource type as key and a list of named blocks as value. The test finds the `local_file` block named `hello` and checks its keys. Since `content` references a variable, the string representation of the value will contain `var.greeting`. These checks catch typos and missing required fields before `terraform plan`.

### Solution 3
Solution. `main.tf`:

```hcl
provider "local" {}
provider "random" {}

resource "random_string" "suffix" {
  length  = 8
  upper   = false
  special = false
}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "${var.greeting} ${random_string.suffix.result}"
}

output "greeting_file" {
  value = local_file.hello.filename
}
```

What is going on here? The `random` provider generates random values; the `random_string` resource creates an 8-character string without uppercase or special characters. We reference it via `random_string.suffix.result` — this creates a dependency: Terraform will create `random_string` before `local_file`. The output `greeting_file` publishes the file path — after `terraform apply` you can see it in the outputs list (`terraform output`). The `random` provider is mostly used for resource names that must be unique.

### Solution 4
Solution:

```python
import re
import hcl2


def variable_names(path="variables.tf"):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return set(re.findall(r'variable\s+"([^"]+)"', text))


def test_greeting_variable_exists():
    names = variable_names()
    assert "greeting" in names


def test_greeting_has_type_string():
    with open("variables.tf", encoding="utf-8") as f:
        cfg = hcl2.load(f)
    greeting = cfg.get("variable", [])[0]["greeting"][0]
    assert greeting.get("type") == "string"


def test_no_dangling_vars_in_tfvars():
    declared = variable_names()
    with open("terraform.tfvars", encoding="utf-8") as f:
        text = f.read()
    used = set(re.findall(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=', text, flags=re.M))
    dangling = used - declared
    assert not dangling, f"dangling variables: {dangling}"
```

What is going on here? `variable_names` collects names via a regular expression. In `test_greeting_has_type_string` we parse `variables.tf` and check the type. The last test reads `terraform.tfvars`, finds key names by regex, and subtracts the declared ones — if "dangling" variables remain, the test fails. This is classic protection against typos: Terraform silently ignores unknown variables in tfvars, and a setting may silently not apply.

### Solution 5
Solution. `outputs.tf`:

```hcl
output "greeting_content" {
  value = local_file.hello.content
}
```

`terraform.tfvars`:

```hcl
greeting = "Привет из Terraform!"
```

Test `test_outputs_tf.py`:

```python
import hcl2


def test_output_exists():
    with open("outputs.tf", encoding="utf-8") as f:
        cfg = hcl2.load(f)
    outputs = cfg.get("output", [])
    assert any("greeting_content" in o for o in outputs)


def test_output_value_refers_to_local_file():
    with open("outputs.tf", encoding="utf-8") as f:
        cfg = hcl2.load(f)
    for o in cfg.get("output", []):
        if "greeting_content" in o:
            value = o["greeting_content"][0].get("value")
            assert "local_file.hello.content" in str(value)
            return
    raise AssertionError("output not found")
```

What is going on here? An `output` block publishes a value after apply. The `hcl2.load` parser returns, in `output`, a list of dicts whose items are output blocks; `value` is a string referencing a resource attribute. The test checks the output exists and references `local_file.hello.content`. Now the configuration is fully parameterized: the `greeting` value comes from `terraform.tfvars`, and the same path is available via `terraform output greeting_content`.

<!--/SOLUTION-->

<!--QUIZ-->
What does Terraform describe?
- The desired state of infrastructure
- A command sequence for a server
- Database contents
* Correct answer: The desired state of infrastructure
Terraform declaratively describes what infrastructure should exist.

What language are Terraform configurations written in?
- HCL
- YAML
- JSON
* Correct answer: HCL
Terraform uses its own language HCL (HashiCorp Configuration Language).

Which command downloads providers?
- terraform init
- terraform plan
- terraform apply
* Correct answer: terraform init
terraform init initializes the working directory and downloads providers.

Which command shows a change plan without applying?
- terraform plan
- terraform apply
- terraform destroy
* Correct answer: terraform plan
terraform plan performs a dry run and prints what will change.

Where does Terraform store the actual state of infrastructure?
- In the terraform.tfstate file
- In the main.tf file
- In environment variables
* Correct answer: In the terraform.tfstate file
The state file contains the actual state of resources and is not edited by hand.

How do you reference the variable greeting?
- var.greeting
- variable.greeting
- $greeting
* Correct answer: var.greeting
Variables in HCL are accessible with the var prefix.

What does terraform destroy do?
- Deletes all described infrastructure
- Stops the local server
- Clears command history
* Correct answer: Deletes all described infrastructure
terraform destroy brings reality to an "empty" state — it deletes resources.

What is an output block for?
- To publish a configuration value outward
- To download a file
- To declare a variable
* Correct answer: To publish a configuration value outward
Outputs show values after apply, e.g., IP addresses and paths.

Which provider can create local files?
- local
- aws
- random
* Correct answer: local
The local provider creates files on the local machine.

What happens if resource A references an attribute of resource B?
- Terraform will create B before A
- Terraform will create A before B
- Terraform will raise an error
* Correct answer: Terraform will create B before A
Terraform builds a dependency graph and orders resource creation.

<!--/QUIZ-->
