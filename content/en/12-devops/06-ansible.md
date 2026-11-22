---
title: Ansible and IaC basics
summary: Inventory, playbooks, idempotency.
order: 6
duration: 45 min
difficulty: advanced
tags: ansible, iac
---

Infrastructure as Code describes servers in files.

## Inventory

```ini
[web]
server1.example.com
```

## Playbook

```yaml
- hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

## Run

```bash
ansible-playbook -i inventory playbook.yml
```

## Idempotency

Running twice gives the same result.

## Lesson summary

IaC makes infrastructure reproducible.

<!--TASK-->
### Task 1 — Inventory
Write a simple inventory.

### Task 2 — Playbook
Install nginx with apt.

### Task 3 — Run
Run ansible-playbook.

### Task 4 — Idempotent
Explain the concept.

### Task 5 — Service
Ensure nginx running.

### Task 6 — Handler
Add a handler to restart.

### Task 7 — Compare
Ansible vs manual SSH.
<!--/TASK-->

<!--HINT-->
### Hint 1
[web].

### Hint 2
apt module.

### Hint 3
ansible-playbook.

### Hint 4
Same result.

### Hint 5
service module.

### Hint 6
handlers.

### Hint 7
Reproducible.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```ini
[web]
server1.example.com
```

### Solution 2
```yaml
- hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
```

### Solution 3
```bash
ansible-playbook -i inventory playbook.yml
```

### Solution 4
```python
# Повторный запуск даёт тот же результат:
# пакет уже установлен — Ansible ничего не меняет
```

### Solution 5
```yaml
- name: Ensure nginx running
  service:
    name: nginx
    state: started
    enabled: true
```

### Solution 6
```yaml
- name: Restart nginx
  service:
    name: nginx
    state: restarted
  when: nginx_conf.changed
```

### Solution 7
```python
# Ansible: декларативно, воспроизводимо, версионируемо
# SSH вручную: легко забыть шаг
```
<!--/SOLUTION-->

<!--QUIZ-->
What is IaC?
- Infra as code
- A server
- A language
- None
* Correct answer: Infra as code
Files.

What is inventory?
- Host list
- Tasks
- Modules
- None
* Correct answer: Host list
Groups.

What is a playbook?
- Task list
- Hosts only
- A module
- None
* Correct answer: Task list
YAML.

What is a task?
- One action
- A host
- A file
- None
* Correct answer: One action
Module.

What is apt?
- Package module
- Service
- Copy
- None
* Correct answer: Package module
Debian.

What is become?
- Privilege escalation
- Host
- Task
- None
* Correct answer: Privilege escalation
sudo.

What is idempotent?
- Same result each run
- Changes each time
- Fails
- None
* Correct answer: Same result each run
Desired.

What is state: present?
- Ensure installed
- Remove
- Start
- None
* Correct answer: Ensure installed
Idempotent.

What is a handler?
- Runs on change
- Always runs
- A host
- None
* Correct answer: Runs on change
Notify.

What is service module?
- Manages services
- Installs
- Copies
- None
* Correct answer: Manages services
Start/stop.

What is ansible-playbook?
- Runs playbooks
- Tests
- Deploys only
- None
* Correct answer: Runs playbooks
CLI.

What is the benefit?
- Reproducible
- Faster always
- Required
- None
* Correct answer: Reproducible
Versioned.
<!--/QUIZ-->
