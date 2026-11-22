---
title: Ansible: playbooks and roles
summary: Tasks, roles, variables.
order: 2
duration: 50 min
difficulty: advanced
tags: ansible
---

Ansible configures servers without agents.

## Playbook

```yaml
- hosts: web
  become: true
  vars:
    nginx_port: 80
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Ensure running
      service:
        name: nginx
        state: started
```

## Roles

Structure: tasks/, handlers/, templates/, vars/.

## Lesson summary

Playbooks + roles = server config as code.

<!--TASK-->
### Task 1 — Hosts
Set hosts: web.

### Task 2 — Vars
Add a variable.

### Task 3 — Tasks
Install a package.

### Task 4 — Service
Ensure it runs.

### Task 5 — Template
Use a Jinja template.

### Task 6 — Role
Create a role layout.

### Task 7 — Idempotency
Explain.
<!--/TASK-->

<!--HINT-->
### Hint 1
hosts.

### Hint 2
vars.

### Hint 3
apt.

### Hint 4
service.

### Hint 5
template.

### Hint 6
tasks.

### Hint 7
Same result.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```yaml
- hosts: web
  become: true
```

### Solution 2
```yaml
vars:
  nginx_port: 80
```

### Solution 3
```yaml
tasks:
  - name: Install nginx
    apt:
      name: nginx
      state: present
```

### Solution 4
```yaml
  - name: Ensure nginx running
    service:
      name: nginx
      state: started
```

### Solution 5
```yaml
  - name: Deploy config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
```

### Solution 6
```text
roles/nginx/
  tasks/main.yml
  handlers/main.yml
  templates/nginx.conf.j2
  vars/main.yml
```

### Solution 7
```text
Повторный запуск не меняет систему,
если желаемое состояние уже достигнуто
```
<!--/SOLUTION-->

<!--QUIZ-->
What is Ansible?
- Configuration tool
- A database
- A browser
- None
* Correct answer: Configuration tool
Agentless.

What is a playbook?
- Task file
- Hosts
- Role
- None
* Correct answer: Task file
YAML.

What is a task?
- One action
- A host
- A var
- None
* Correct answer: One action
Module.

What is a module?
- Reusable action
- Template
- Host
- None
* Correct answer: Reusable action
apt.

What is hosts?
- Targets
- Tasks
- Vars
- None
* Correct answer: Targets
Group.

What is become?
- sudo
- Host
- Module
- None
* Correct answer: sudo
Privilege.

What is vars?
- Variables
- Tasks
- Hosts
- None
* Correct answer: Variables
Port.

What is a template?
- Jinja file
- Script
- Module
- None
* Correct answer: Jinja file
.j2.

What is a role?
- Structured group
- Playbook
- Host
- None
* Correct answer: Structured group
Tasks.

What is handlers?
- On change
- Always
- Never
- None
* Correct answer: On change
Notify.

What is idempotent?
- Same result
- Changes
- Fails
- None
* Correct answer: Same result
Safe.

What is the inventory?
- Host list
- Tasks
- Roles
- None
* Correct answer: Host list
Groups.
<!--/QUIZ-->
