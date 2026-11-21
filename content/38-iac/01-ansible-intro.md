---
title: Ansible: автоматизация серверов
summary: Что такое Ansible, инвентори, плейбуки, модули и хэндлеры; описываем конфигурацию серверов как код на YAML.
order: 1
duration: 40 мин
difficulty: advanced
tags: ansible, devops, yaml, плейбуки, автоматизация
---

Когда серверов один-два, их ещё можно настраивать руками: зайти по SSH, выполнить команды, сохранить заметку. Но как только их становится десять, сто или тысяча, ручное управление ломается: где-то забыли обновить пакет, где-то конфиг отличается на пару строк, и серверы «дрейфуют» — расходятся друг от друга. Выход — **инфраструктура как код (IaC)**: конфигурация хранится в файлах, как обычный код, версионируется в Git и применяется автоматически.

## Что такое Ansible

**Ansible** — один из самых популярных инструментов управления конфигурацией. Его ключевые особенности:

- **Без агентов (agentless):** на управляемых серверах не нужно устанавливать никакие агенты. Ansible подключается к ним по SSH и выполняет команды.
- **Push-модель:** управляющая машина (control node) сама «толкает» конфигурацию на хосты, в отличие от pull-подхода Chef/Puppet.
- **Декларативные сценарии:** вы описываете *желаемое состояние*, а не последовательность команд.
- **Всё на YAML:** плейбуки — это обычные YAML-файлы, их легко читать и ревьюить.

## Инвентори

**Инвентори (inventory)** — список хостов и групп, которыми управляет Ansible. Его можно писать в формате INI или YAML. Пример YAML-инвентори `hosts.yml`:

```yaml
all:
  children:
    web:
      hosts:
        web-01:
          ansible_host: 10.0.1.10
        web-02:
          ansible_host: 10.0.1.11
    db:
      hosts:
        db-01:
          ansible_host: 10.0.2.10
```

Группы можно вкладывать друг в друга, переменные — объявлять на любом уровне.

## Модули и ad-hoc команды

**Модуль** — готовая единица функциональности: `ping` (проверка соединения), `apt` (пакеты в Debian/Ubuntu), `yum`/`dnf` (в RHEL), `service` (управление службами), `copy` (копирование файлов), `template` (копирование с шаблонизацией), `command`/`shell` (произвольные команды). Ad-hoc команда выполняется без плейбука:

```bash
ansible -i hosts.yml all -m ping
ansible -i hosts.yml web -m apt -a "name=nginx state=present"
```

Модули **идемпотентны**: повторное применение не ломает состояние — если пакет уже установлен, Ansible ничего не переустанавливает. Это главное отличие от простых шелл-скриптов.

## Плейбуки

**Плейбук** — сценарий на YAML. Минимальный плейбук `install_nginx.yml`:

```yaml
---
- name: Установка и запуск Nginx
  hosts: web
  become: true
  tasks:
    - name: Установить nginx
      apt:
        name: nginx
        state: present

    - name: Запустить и включить nginx
      service:
        name: nginx
        state: started
        enabled: true
```

Ключевые поля верхнего уровня: `name` (имя плейбука), `hosts` (на какую группу действует), `become` (выполнять ли от root через sudo), `tasks` (список задач), `vars` (переменные), `handlers` (хэндлеры — задачи, запускаемые по событию). Задача, как правило, содержит `name` и вызов одного модуля.

Запуск и проверки:

```bash
ansible-playbook -i hosts.yml install_nginx.yml --syntax-check
ansible-playbook -i hosts.yml install_nginx.yml --check
ansible-playbook -i hosts.yml install_nginx.yml
```

`--syntax-check` проверяет синтаксис YAML и структуру плейбука, а `--check` — «сухой прогон»: Ansible показывает, что бы он сделал, ничего не меняя.

## Переменные и шаблоны Jinja2

Переменные объявляются в `vars`, в инвентори или в отдельных файлах. Внутри шаблонов и задач доступ к ним — через двойные фигурные скобки:

```yaml
---
- name: Настройка конфига nginx
  hosts: web
  become: true
  vars:
    server_name: example.com
    nginx_port: 8080
  tasks:
    - name: Скопировать конфиг из шаблона
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/default
      notify: restart_nginx

  handlers:
    - name: restart_nginx
      service:
        name: nginx
        state: restarted
```

Файл `nginx.conf.j2` — шаблон Jinja2, в котором переменные подставляются во время выполнения:

```jinja
server {
    listen {{ nginx_port }};
    server_name {{ server_name }};
    root /var/www/html;
}
```

Обрати внимание на `notify: restart_nginx`: задача не перезапускает службу сразу, а «уведомляет» хэндлер. Хэндлер выполнится в конце плейбука, и только если задача реально что-то изменила. Это экономит перезапуски и делает плейбук идемпотентным.

Вот как выглядит путь одной задачи от управляющей машины до изменения на сервере:

```mermaid
flowchart TD
    A["Control node"] --> B["Инвентори hosts.yml"]
    B --> C["Плейбук: задачи"]
    C --> D{"Что-то изменилось?"}
    D -->|"да"|" E["notify: хэндлер"]
    D -->|"нет"| F["ok, без действий"]
    E --> G["restart nginx"]
```

Схема подчёркивает главное: плейбук не «выполняет команды», а приводит хосты к состоянию и сообщает, что именно поменялось. Ветка `ok` — не ошибка, а признак идемпотентности.

## Итог

Мы разобрали основы Ansible: инвентори, модули, плейбуки, переменные, шаблоны и хэндлеры. Ansible — это способ превратить «я вручную починил сервер» в «вот файл, который воспроизводит состояние сервера». Дальше закрепим всё практикой.

<!--TASK-->
### Задача 1
Создай файл инвентори `hosts.yml`, в котором описана группа `web` из двух хостов (`web-01` и `web-02`) с IP-адресами `10.0.1.10` и `10.0.1.11`, и группа `db` с одним хостом `db-01` по адресу `10.0.2.10`. Для каждого хоста укажи переменную `ansible_user: ubuntu`. Затем напиши ad-hoc команду (в комментарии к файлу), которая проверит доступность всех хостов из инвентори. Ожидаемый результат: ты можешь объяснить, почему группа `web` не содержит вложенных групп и какие ключи YAML обязательны для хоста.

### Задача 2
Напиши плейбук `install_nginx.yml`, который применяется к группе `web`, выполняется с `become: true` и содержит две задачи: установку пакета `nginx` в состояние `present` (модуль `apt`) и запуск службы `nginx` с `state: started` и `enabled: true` (модуль `service`). Добавь понятные `name` обеим задачам. Ожидаемый результат: файл должен пройти `ansible-playbook --syntax-check` без ошибок, а при разборе видно, что у каждой задачи есть имя и модуль.

### Задача 3
Напиши pytest-тест `test_playbook.py`, который читает плейбук `install_nginx.yml` из задачи 2, парсит его через `yaml.safe_load` и проверяет: файл — это список ровно из одного «плей», у плей есть ключ `hosts` со значением `web`, есть ключ `tasks` с непустым списком, и каждая задача содержит ключ `name` и хотя бы один из модулей `apt`, `service`, `copy`, `template`, `command`, `shell`, `pip`. Тест должен завершаться без ошибок. Для запуска используй `pytest test_playbook.py -v`.

### Задача 4
Создай шаблон `nginx.conf.j2` для виртуального хоста Nginx с переменными `server_name` и `nginx_port`, а также pytest-тест `test_template.py`, который рендерит этот шаблон с помощью Jinja2 с данными `{"server_name": "example.com", "nginx_port": 8080}` и проверяет, что в результате есть строки `server_name example.com;` и `listen 8080;`. Ожидаемый результат: `pytest test_template.py -v` зелёный, и тест доказывает, что шаблон действительно использует переменные.

### Задача 5
Дополни плейбук из задачи 2: добавь задачу, которая копирует шаблон `nginx.conf.j2` в `/etc/nginx/sites-available/default` (модуль `template`, ключ `notify: restart_nginx`), и блок `handlers` с хэндлером `restart_nginx`, который перезапускает службу `nginx`. Затем расширь тест `test_playbook.py`: добавь проверку, что у каждой задачи с ключом `notify` этот хэндлер существует в `handlers` (по ключу `name`). Ожидаемый результат: все тесты проходят, и ты умеешь объяснять, почему хэндлер вызывается только при изменении файла.
### Задача 6
Вынеси переменные группы `web` в отдельный файл `group_vars/web.yml`: `ansible_user: ubuntu`, `nginx_port: 8080`, `server_name: example.com`. В `hosts.yml` у хостов оставь только `ansible_host`, а из блока `vars` плейбука убери `nginx_port` и `server_name`. Добавь в плейбук третью задачу с модулем `debug`, которая печатает адрес `http://{{ server_name }}:{{ nginx_port }}`, и поставь ей условие `when: nginx_port != 80`. Напиши тест `test_vars.py`: он проверяет, что в `group_vars/web.yml` есть все три переменные, что в инвентори у хостов нет `ansible_user` и что в плейбуке есть задача с ключом `when`, использующая `nginx_port`. Ожидаемый результат: `pytest test_vars.py -v` — 3 passed, а `ansible-playbook -i hosts.yml install_nginx.yml --check` не жалуется на неопределённые переменные.

### Задача 7
Создай файл `state.json` с фактическим состоянием: `{"web-01": 8080, "web-02": 8081, "db-01": 8080}` — это порты, на которых nginx реально слушает. Напиши скрипт `drift_report.py`, который читает `hosts.yml`, желаемый порт из `group_vars/web.yml` и `state.json`, а затем печатает отчёт по строке на хост: `web-01: ok`, `web-02: drift 8080 -> 8081`, `db-01: вне группы web`. Скрипт возвращает код `1`, если дрейф найден, и `0`, если всё совпало. Напиши тест `test_drift_report.py`, который запускает скрипт через `subprocess.run` и проверяет код возврата и все три строки вывода. Ожидаемый вывод: `web-01: ok`, `web-02: drift 8080 -> 8081`, `db-01: вне группы web`, код возврата `1`.

<!--/TASK-->

<!--HINT-->
### Подсказка 1
Формат инвентори YAML: корневой ключ `all`, внутри `children`, внутри группы — `hosts` со списком имён. Переменные хоста — обычные ключи внутри него. Проверка подключения: `ansible -i hosts.yml all -m ping` — модуль `ping` не делает пинг ICMP, а проверяет SSH-соединение и наличие Python на хосте.

### Подсказка 2
Структура плейбука: в начале `---`, затем `- name: ...`, `hosts: web`, `become: true`, и ключ `tasks:` со списком задач. Каждая задача: `- name: ...`, затем на следующей строке имя модуля (`apt:` или `service:`) с вложенными параметрами. Не забудь отступы: ровно два пробела на уровень вложенности.

### Подсказка 3
В тесте используй `import yaml` и `yaml.safe_load(open("install_nginx.yml", encoding="utf-8"))`. Проверки — через `assert`. Список допустимых модулей храни в `set`. Если `yaml` не установлен — поставь `pip install pyyaml pytest`.

### Подсказка 4
Jinja2: `from jinja2 import Template`; создай объект `Template(open("nginx.conf.j2", encoding="utf-8").read())` и вызови `.render(server_name="example.com", nginx_port=8080)`. В шаблоне переменные пишутся как `{{ server_name }}` и `{{ nginx_port }}`. Проверяй наличие итоговых строк через `assert "..." in rendered`.

### Подсказка 5
У плейбука появится ключ `handlers`, который находится на том же уровне, что и `tasks`, и содержит список задач с `name`. В тесте собери имена хэндлеров в множество (`{h["name"] for h in handlers}`) и сравни с каждым значением `notify` из задач. Не забудь, что `notify` может быть строкой или списком.
### Подсказка 6
Ansible сам подхватывает `group_vars/<имя_группы>.yml` рядом с инвентори: структура файла — плоский словарь без обёрток. В тесте читай оба файла через `yaml.safe_load`, а задачу с условием ищи так: `[t for t in play["tasks"] if "when" in t]`.

### Подсказка 7
Собери множество хостов группы из инвентори и сравни с ключами `state.json` — разница и есть «хосты вне группы». Для запуска скрипта из теста используй `subprocess.run(["python", "drift_report.py"], capture_output=True, text=True)` и смотри на `returncode` и `stdout`.

<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение:

```yaml
all:
  children:
    web:
      hosts:
        web-01:
          ansible_host: 10.0.1.10
          ansible_user: ubuntu
        web-02:
          ansible_host: 10.0.1.11
          ansible_user: ubuntu
    db:
      hosts:
        db-01:
          ansible_host: 10.0.2.10
          ansible_user: ubuntu
# Проверка доступности всех хостов:
# ansible -i hosts.yml all -m ping
```

Что здесь происходит? Корневой ключ `all` объединяет все хосты. В `children` перечислены группы: `web` и `db`. Внутри каждой группы — `hosts` со списком фактических имён хостов, и у каждого хоста объявлена переменная `ansible_user`. Ключи `ansible_host` и `ansible_user` — стандартные переменные подключения. Команда `ansible -i hosts.yml all -m ping` использует инвентори (`-i hosts.yml`), цель `all` (все хосты) и модуль `ping`. Этот модуль проверяет именно SSH-соединение и наличие Python, а не ICMP-пинг. ad-hoc команды удобны для быстрых действий, но для воспроизводимых настроек используют плейбуки.

### Разбор 2
Решение:

```yaml
---
- name: Установка и запуск Nginx
  hosts: web
  become: true
  tasks:
    - name: Установить nginx
      apt:
        name: nginx
        state: present

    - name: Запустить и включить nginx
      service:
        name: nginx
        state: started
        enabled: true
```

Что здесь происходит? Плейбук — это список, содержащий один «плей» (play) — блок с `hosts` и `tasks`. Ключ `become: true` говорит Ansible выполнять задачи от имени root через sudo. Первая задача использует модуль `apt` и гарантирует, что пакет `nginx` установлен (`state: present`). Вторая — модуль `service` — запускает службу и добавляет её в автозагрузку. Проверка `ansible-playbook -i hosts.yml install_nginx.yml --syntax-check` подтвердит корректность YAML и структуры. Важно, что каждая задача имеет `name` — по нему Ansible показывает прогресс и позволяет ссылаться на задачу из `notify`.

### Разбор 3
Решение:

```python
import yaml


def load_playbook(path="install_nginx.yml"):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


MODULES = {"apt", "service", "copy", "template", "command", "shell", "pip"}


def test_playbook_is_single_play():
    pb = load_playbook()
    assert isinstance(pb, list)
    assert len(pb) == 1


def test_play_has_hosts_and_tasks():
    play = load_playbook()[0]
    assert play.get("hosts") == "web"
    assert "tasks" in play
    assert isinstance(play["tasks"], list)
    assert len(play["tasks"]) >= 2


def test_every_task_has_name_and_known_module():
    for task in load_playbook()[0]["tasks"]:
        assert "name" in task, "у задачи нет имени"
        assert any(mod in task for mod in MODULES), \
            f"задача {task.get('name')} не использует известный модуль"
```

Что здесь происходит? Первый тест проверяет, что `yaml.safe_load` вернул список ровно из одного элемента — нашего плей. Второй — что у плей есть `hosts` со значением `web` и непустой список `tasks`. Третий — проходит по каждой задаче и проверяет наличие `name` и хотя бы одного известного модуля (пересечение ключей задачи с множеством `MODULES`). Такой тест — лёгкий «линтер» плейбука: он ловит опечатки в структуре до того, как плейбук поедет на реальные серверы. Запуск: `pytest test_playbook.py -v`.

### Разбор 4
Решение. Шаблон `nginx.conf.j2`:

```jinja
server {
    listen {{ nginx_port }};
    server_name {{ server_name }};
    root /var/www/html;
}
```

Тест `test_template.py`:

```python
from jinja2 import Template


def render_template(path, **data):
    with open(path, encoding="utf-8") as f:
        return Template(f.read()).render(**data)


def test_nginx_template_renders_variables():
    out = render_template("nginx.conf.j2", server_name="example.com", nginx_port=8080)
    assert "server_name example.com;" in out
    assert "listen 8080;" in out
```

Что здесь происходит? Функция `render_template` читает файл шаблона и рендерит его через Jinja2, подставляя данные. Шаблон использует синтаксис `{{ переменная }}`, и после рендеринга внутри результата обязаны появиться подставленные значения. Тест проверяет это двумя `assert`. Если бы в шаблоне была опечатка (например, `{{ nginx_por }}`), переменная не подставилась бы, и тест упал бы — именно так автоматизация ловит дрейф конфигурации до деплоя.

### Разбор 5
Решение. Плейбук с хэндлером:

```yaml
---
- name: Установка и запуск Nginx
  hosts: web
  become: true
  vars:
    server_name: example.com
    nginx_port: 8080
  tasks:
    - name: Установить nginx
      apt:
        name: nginx
        state: present

    - name: Скопировать конфиг из шаблона
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/default
      notify: restart_nginx

  handlers:
    - name: restart_nginx
      service:
        name: nginx
        state: restarted
```

Дополненный тест:

```python
def test_notify_refers_to_handler():
    play = load_playbook()[0]
    handler_names = {h.get("name") for h in play.get("handlers", [])}
    for task in play["tasks"]:
        notify = task.get("notify")
        if notify is None:
            continue
        for target in (notify if isinstance(notify, list) else [notify]):
            assert target in handler_names, f"хэндлер {target} не объявлен"
```

Что здесь происходит? Ключ `notify` связывает задачу с хэндлером: если задача реально изменила состояние (файл скопирован заново), Ansible в конце плейбука выполнит `restart_nginx`. Если изменений нет — хэндлер не сработает, и служба не будет перезапущена зря. Тест собирает имена хэндлеров в множество и проверяет, что каждое имя из `notify` (строка или список) там присутствует. Это защищает от классической ошибки — «handler не найден» на реальном прогоне.
### Разбор 6
Решение. `group_vars/web.yml`:

```yaml
ansible_user: ubuntu
nginx_port: 8080
server_name: example.com
```

`hosts.yml` — без переменных у хостов:

```yaml
all:
  children:
    web:
      hosts:
        web-01:
          ansible_host: 10.0.1.10
        web-02:
          ansible_host: 10.0.1.11
```

Фрагмент плейбука:

```yaml
    - name: Показать адрес сервиса
      debug:
        msg: "http://{{ server_name }}:{{ nginx_port }}"
      when: nginx_port != 80
```

Тест `test_vars.py`:

```python
import yaml


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_group_vars_web():
    data = load("group_vars/web.yml")
    assert data["ansible_user"] == "ubuntu"
    assert data["nginx_port"] == 8080
    assert data["server_name"] == "example.com"


def test_inventory_has_no_duplicated_vars():
    inv = load("hosts.yml")
    for host in inv["all"]["children"]["web"]["hosts"].values():
        assert "ansible_user" not in host


def test_playbook_uses_group_vars():
    play = load("install_nginx.yml")[0]
    conditional = [t for t in play["tasks"] if "when" in t]
    assert conditional, "нет задачи с when"
    assert any("nginx_port" in str(t) for t in conditional)
    assert "nginx_port" not in play.get("vars", {})
```

Что здесь происходит? `group_vars/web.yml` — стандартное место переменных группы: Ansible читает его автоматически, без `vars_files`. Переменные действуют на все хосты группы `web`, поэтому дублировать `ansible_user` в инвентори больше не нужно — и тест это охраняет. Задача с `debug` ничего не меняет на сервере, а `when` показывает условное выполнение: на окружении с портом `80` лишняя строка не печатается. Третий тест заодно запрещает возвращать переменные обратно в плейбук: одна переменная должна жить в одном месте, иначе окружения снова начнут расходиться.

### Разбор 7
Решение. `drift_report.py`:

```python
import json
import sys

import yaml


DESIRED_FILE = "group_vars/web.yml"
INVENTORY = "hosts.yml"
STATE = "state.json"


def main():
    with open(INVENTORY, encoding="utf-8") as f:
        inv = yaml.safe_load(f)
    with open(DESIRED_FILE, encoding="utf-8") as f:
        desired = yaml.safe_load(f)["nginx_port"]
    with open(STATE, encoding="utf-8") as f:
        actual = json.load(f)

    web_hosts = sorted(inv["all"]["children"]["web"]["hosts"])
    drift = False

    for host in web_hosts:
        port = actual.get(host)
        if port is None:
            print(f"{host}: нет данных")
            drift = True
        elif port != desired:
            print(f"{host}: drift {desired} -> {port}")
            drift = True
        else:
            print(f"{host}: ok")

    for host in sorted(set(actual) - set(web_hosts)):
        print(f"{host}: вне группы web")

    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
```

Тест `test_drift_report.py`:

```python
import subprocess


def run():
    return subprocess.run(
        ["python", "drift_report.py"],
        capture_output=True,
        text=True,
        check=False,
    )


def test_drift_exit_code():
    assert run().returncode == 1


def test_drift_output_lines():
    out = run().stdout
    assert "web-01: ok" in out
    assert "web-02: drift 8080 -> 8081" in out
    assert "db-01: вне группы web" in out
```

Что здесь происходит? Скрипт — маленькая модель того, чем занимается Ansible в режиме `--check`: он берёт желаемое состояние (`group_vars`), фактическое (`state.json`) и печатает расхождения. Порядок хостов берётся из инвентори и сортируется, поэтому вывод стабилен и его можно проверять тестом. Хосты из `state.json`, которых нет в группе, попадают в отдельную строку — это тоже дрейф, только «лишний» хост. Код возврата делает скрипт пригодным для CI: единица останавливает пайплайн. Тест запускает именно процесс, а не функцию, — так проверяется и парсинг аргументов, и формат вывода целиком.

<!--/SOLUTION-->

<!--QUIZ-->
Что такое Ansible?
- Инструмент управления конфигурацией без агентов
- Компилятор Python
- База данных
* Правильный ответ: Инструмент управления конфигурацией без агентов
Ansible подключается к хостам по SSH и не требует установки агентов.

Какой протокол использует Ansible для подключения к управляемым хостам?
- SSH
- FTP
- SMTP
* Правильный ответ: SSH
Ansible — agentless-инструмент, работающий поверх SSH.

Что описывает инвентори (inventory)?
- Список хостов и групп
- Список задач
- Версии Python
* Правильный ответ: Список хостов и групп
Инвентори перечисляет хосты, группы и их переменные.

Какой ключ плейбука разрешает выполнение задач от имени root?
- sudo
- become
- root
* Правильный ответ: become
become: true включает повышение привилегий через sudo.

Как называется проверка плейбука без реальных изменений?
- --check
- --dry-run-2
- --preview
* Правильный ответ: --check
--check выполняет «сухой прогон»: показывает, что бы изменилось, ничего не меняя.

Какой модуль копирует файл с подстановкой переменных?
- copy
- template
- shell
* Правильный ответ: template
Модуль template использует Jinja2 и подставляет переменные в шаблон.

Зачем нужны хэндлеры?
- Выполняются в конце плейбука только при изменении состояния
- Выполняются всегда в начале
- Заменяют модули
* Правильный ответ: Выполняются в конце плейбука только при изменении состояния
Хэндлер срабатывает по notify и только если задача что-то изменила.

Что означает идемпотентность модуля?
- Повторное применение не меняет уже корректное состояние
- Модуль можно запустить только один раз
- Модуль удаляет все файлы
* Правильный ответ: Повторное применение не меняет уже корректное состояние
Идемпотентность — повторный прогон не ломает состояние системы.

В каком формате пишутся плейбуки?
- YAML
- JSON
- XML
* Правильный ответ: YAML
Плейбуки Ansible — обычные YAML-файлы.

Какой модуль устанавливает пакеты в Debian/Ubuntu?
- apt
- yum
- pip
* Правильный ответ: apt
Модуль apt управляет пакетами в системах с apt (Debian, Ubuntu).
Что делает флаг --limit web?
- Ограничивает выполнение хостами группы web
- Ускоряет плейбук в два раза
- Удаляет группу web из инвентори
* Правильный ответ: Ограничивает выполнение хостами группы web
--limit сужает список целей, не меняя сам плейбук.

Где Ansible ищет переменные группы web?
- В файле group_vars/web.yml рядом с инвентори
- В файле vars/web.ini внутри плейбука
- Только в командной строке
* Правильный ответ: В файле group_vars/web.yml рядом с инвентори
group_vars подхватывается автоматически, без vars_files.

Что означает статус changed у задачи?
- Задача изменила состояние хоста
- Задача упала с ошибкой
- Задача была пропущена
* Правильный ответ: Задача изменила состояние хоста
changed показывает реальные изменения; ok — состояние уже совпадало.

Что делает serial: 1 в плейбуке?
- Выполняет плей на хостах по одному
- Запускает плей ровно один раз
- Ограничивает плей одним task
* Правильный ответ: Выполняет плей на хостах по одному
serial задаёт размер «волны» и используется для rolling-обновлений.

<!--/QUIZ-->
