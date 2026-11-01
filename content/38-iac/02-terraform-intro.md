---
title: Terraform: инфраструктура как код
summary: Декларативное описание инфраструктуры: провайдеры, ресурсы, переменные, выходы; жизненный цикл terraform init/plan/apply.
order: 2
duration: 40 мин
difficulty: advanced
tags: terraform, iac, hcl, провайдеры, стейт
---

Ansible настраивает серверы *внутри*, но кто создаёт сами серверы, сети, базы данных и балансировщики? Для этого есть второй класс инструментов IaC — **Terraform**. Если Ansible отвечает на вопрос «как должен выглядеть сервер», то Terraform отвечает на вопрос «какая инфраструктура вообще должна существовать».

## Декларативный подход

Terraform от HashiCorp описывает **желаемое состояние** инфраструктуры в конфигурационных файлах. Вы пишете «пусть будет сервер с таким-то образом и такой-то сетью», и Terraform приводит реальность к этому описанию. Ему не важно, в каком порядке создавать ресурсы, — он сам строит граф зависимостей.

Основные понятия:

- **Провайдер (provider)** — плагин, который знает API конкретной платформы: AWS, Google Cloud, Yandex Cloud, Azure, а также локальные инструменты (например, `random`, `local`).
- **Ресурс (resource)** — единичная сущность: виртуальная машина, сеть, DNS-запись, файл.
- **Переменные (variable)** — параметры конфигурации.
- **Выходы (output)** — публикуемые значения, например IP-адрес созданного сервера.
- **Стейт (state)** — файл `terraform.tfstate`, в котором Terraform хранит текущее фактическое состояние.

## Язык HCL

Terraform использует свой язык — **HCL** (HashiCorp Configuration Language). По синтаксису он похож на JSON, но читается легче:

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
  description = "Имя проекта"
  type        = string
  default     = "myapp"
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

Ключевая идея — **ссылки на ресурсы**: `aws_instance.web.public_ip` обращается к атрибуту ресурса `aws_instance` с именем `web`. Если ресурс `A` использует атрибут ресурса `B`, Terraform поймёт зависимость и создаст `B` первым.

## Жизненный цикл

Основные команды:

```bash
terraform init      # скачивает провайдеры и модули
terraform validate  # проверяет синтаксис конфигурации
terraform plan      # показывает план изменений
terraform apply     # применяет изменения (создаёт/меняет ресурсы)
terraform destroy   # удаляет всю инфраструктуру
terraform show      # показывает текущее состояние
```

`terraform plan` — «сухой прогон»: он печатает, что будет создано, изменено или удалено, ничего не трогая. `terraform apply` спрашивает подтверждение (или выполняет, если передать `-auto-approve`). После apply в каталоге появляется `terraform.tfstate` — его нельзя редактировать руками и его стоит хранить в безопасном месте (например, в remote state на S3).

## Пример: локальный файл

Чтобы попробовать Terraform без облака, используем провайдер `local`:

```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello from Terraform!"
}
```

После `terraform init` и `terraform apply` появится файл `hello.txt`. Это удобный способ отработать lifecycle без денег и аккаунтов.

## Переменные и tfvars

Переменные объявляются в `variables.tf`, значения по умолчанию — через `default`. Реальные значения кладут в файл `terraform.tfvars`:

```hcl
# terraform.tfvars
project_name = "pythonpro"
instance_type = "t3.micro"
```

Terraform автоматически читает `terraform.tfvars` при `plan`/`apply`. Приоритет значений: флаги командной строки → файлы tfvars → переменные окружения → `default` в объявлении.

## Итог

Terraform декларативно управляет всей инфраструктурой: создаёт, меняет и удаляет ресурсы, хранит состояние, выстраивает зависимости. Вместе с Ansible они образуют связку: Terraform поднимает серверы, Ansible настраивает их изнутри. Теперь закрепим практикой.

<!--TASK-->
### Задача 1
Создай файл `main.tf` с провайдером `local` и ресурсом `local_file` с именем `hello`, который создаёт файл `hello.txt` с содержимым `Hello from Terraform!`. Затем создай файл `variables.tf` с переменной `greeting` (тип `string`, значение по умолчанию `Hello from Terraform!`) и используй её в `content` ресурса. Ожидаемый результат: в конфигурации нет «зашитых» строковых литералов, а `terraform validate` проходит без ошибок.

### Задача 2
Напиши pytest-тест `test_main_tf.py`, который парсит `main.tf` библиотекой `python-hcl2` (функция `hcl2.load`) и проверяет: в конфигурации есть провайдер `local`, есть ресурс `local_file` с именем `hello`, и у этого ресурса объявлены ключи `filename` и `content`. Добавь также проверку, что внутри `content` используется ссылка на переменную `var.greeting`. Ожидаемый результат: `pytest test_main_tf.py -v` зелёный.

### Задача 3
Расширь конфигурацию: добавь ресурс `random_string` (провайдер `random`) с `length = 8` и `upper = false`, `special = false`, а в `local_file` добавь третье поле `content` (или дополни `content`, объединив через `` `${var.greeting} ${random_string.result}` ``). Затем добавь `output "greeting_file"` с путём `local_file.hello.filename`. Ожидаемый результат: в `main.tf` есть зависимость от `random_string` и выходная переменная; `terraform validate` проходит.

### Задача 4
Напиши pytest-тест `test_variables_tf.py`: проверь, что в `variables.tf` объявлена переменная `greeting`, у неё есть ключ `type` со значением `string`, и она действительно используется в `main.tf` (ссылка `var.greeting` встречается в тексте файла). Дополнительно проверь, что `terraform.tfvars` не содержит переменных, отсутствующих в `variables.tf`. Ожидаемый результат: все проверки проходят, и ты умеешь защищать конфигурацию от «висячих» переменных.

### Задача 5
Создай файл `terraform.tfvars` со значением `greeting = "Привет из Terraform!"` и файл `outputs.tf` с выходом `greeting_content`, который возвращает `local_file.hello.content`. Напиши тест `test_outputs_tf.py`, который парсит `outputs.tf` и проверяет, что выход `greeting_content` существует и его `value` ссылается на `local_file.hello.content`. Ожидаемый результат: тест зелёный, и конфигурация полностью параметризована.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Синтаксис HCL: блок ресурса — `resource "тип" "имя" { ... }`, блок провайдера — `provider "local" {}`. Переменная объявляется блоком `variable "имя" { type = string; default = ... }`. Ссылка на переменную — `var.greeting`. Minecraft `terraform validate` нужен `terraform init` — иначе Terraform не знает провайдеров.

### Подсказка 2
`python-hcl2` возвращает словарь, где ключ `"local_file"` может лежать в списке по ключу `"resource"`. Используй `cfg.get("resource", [])` и пройди по списку, находи блок, где есть `"local_file"`. Для текстовых проверок можешь читать `main.tf` как обычный текст и искать `var.greeting`.

### Подсказка 3
Провайдер `random` объявляется так же, как `local`. Ресурс `random_string` имеет атрибут `result`. Обращение к нему из другого ресурса — `random_string.<имя>.result`. Выход объявляется блоком `output "имя" { value = ... }`. Не забудь добавить `provider "random" {}`.

### Подсказка 4
Для проверки «висячих» переменных прочитай `terraform.tfvars` как обычный текст (или распарси его), собери имена ключей, а затем сравни с множеством имён из `variables.tf`. В `variables.tf` имена лежат после `variable "` до закрывающей кавычки.

### Подсказка 5
В `outputs.tf` блок выхода выглядит так: `output "greeting_content" { value = local_file.hello.content }`. В тесте используй `hcl2.load` и найди блок `output`, затем проверь, что `value` — строка, содержащая `local_file.hello.content`.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Решение. `variables.tf`:

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

Что здесь происходит? Провайдер `local` умеет создавать локальные файлы, ничего не запрашивая в облаке. Ресурс `local_file` имеет два обязательных поля: `filename` — путь к файлу, и `content` — содержимое. Вместо литерала мы ссылаемся на переменную `var.greeting`. Проверка `terraform init && terraform validate` покажет, что конфигурация корректна. Такой пример идеален для первой практики: он реально исполняется без аккаунтов и денег.

### Разбор 2
Решение:

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
    assert found, "ресурс local_file не найден"


def test_local_file_has_required_keys():
    cfg = load_tf("main.tf")
    for r in cfg.get("resource", []):
        if "local_file" in r:
            block = r["local_file"][0]["hello"]
            assert "filename" in block
            assert "content" in block
            assert "var.greeting" in str(block["content"])
            return
    raise AssertionError("local_file не найден")
```

Что здесь происходит? `hcl2.load` возвращает словарь, где `provider` — список словарей, а `resource` — список, внутри каждого элемента которого ключ — тип ресурса, а значение — список блоков с именами. Тест находит блок `local_file` с именем `hello` и проверяет ключи. Поскольку `content` ссылается на переменную, в строковом представлении значения будет `var.greeting`. Эти проверки ловят опечатки и отсутствие обязательных полей ещё до `terraform plan`.

### Разбор 3
Решение. `main.tf`:

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

Что здесь происходит? Провайдер `random` умеет генерировать случайные значения; ресурс `random_string` создаёт строку из 8 символов без верхнего регистра и спецсимволов. Мы ссылаемся на неё через `random_string.suffix.result` — так образуется зависимость: Terraform создаст `random_string` раньше `local_file`. Выход `greeting_file` публикует путь к файлу — после `terraform apply` его можно увидеть в списке выходов (`terraform output`). Провайдер `random` в основном используют для имён ресурсов, которые должны быть уникальны.

### Разбор 4
Решение:

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
    assert not dangling, f"висячие переменные: {dangling}"
```

Что здесь происходит? `in_names` собирает имена через регулярное выражение. В `test_greeting_has_type_string` мы парсим `variables.tf` и проверяем тип. Последний тест читает `terraform.tfvars`, находит имена ключей по регулярному выражению и вычитает объявленные — если остались «висячие» переменные, тест падает. Это классическая защита от опечаток: Terraform молча игнорирует незнакомые переменные в tfvars, и настройка может «молча» не примениться.

### Разбор 5
Решение. `outputs.tf`:

```hcl
output "greeting_content" {
  value = local_file.hello.content
}
```

`terraform.tfvars`:

```hcl
greeting = "Привет из Terraform!"
```

Тест `test_outputs_tf.py`:

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
    raise AssertionError("выход не найден")
```

Что здесь происходит? Блок `output` публикует значение после apply. Парсер `hcl2.load` в `output` возвращает список словарей, внутри — блоки выходов; `value` — строка с ссылкой на атрибут ресурса. Тест проверяет, что выход существует и ссылается именно на `local_file.hello.content`. Теперь конфигурация полностью параметризована: значение `greeting` приходит из `terraform.tfvars`, и тот же путь доступен через `terraform output greeting_content`.
<!--/SOLUTION-->

<!--QUIZ-->
Что описывает Terraform?
- Желаемое состояние инфраструктуры
- Последовательность команд для сервера
- Содержимое базы данных
* Правильный ответ: Желаемое состояние инфраструктуры
Terraform декларативно описывает, какая инфраструктура должна существовать.

На каком языке пишутся конфигурации Terraform?
- HCL
- YAML
- JSON
* Правильный ответ: HCL
Terraform использует собственный язык HCL (HashiCorp Configuration Language).

Какая команда скачивает провайдеры?
- terraform init
- terraform plan
- terraform apply
* Правильный ответ: terraform init
terraform init инициализирует рабочую директорию и скачивает провайдеры.

Какая команда показывает план изменений без применения?
- terraform plan
- terraform apply
- terraform destroy
* Правильный ответ: terraform plan
terraform plan выполняет «сухой прогон» и печатает, что изменится.

Где Terraform хранит фактическое состояние инфраструктуры?
- В файле terraform.tfstate
- В файле main.tf
- В переменных окружения
* Правильный ответ: В файле terraform.tfstate
Стейт-файл содержит фактическое состояние ресурсов и не редактируется руками.

Как сослаться на переменную greeting?
- var.greeting
- variable.greeting
- $greeting
* Правильный ответ: var.greeting
Переменные в HCL доступны через префикс var.

Что делает terraform destroy?
- Удаляет всю описанную инфраструктуру
- Останавливает локальный сервер
- Очищает историю команд
* Правильный ответ: Удаляет всю описанную инфраструктуру
terraform destroy приводит реальность к «пустому» состоянию — удаляет ресурсы.

Для чего нужен блок output?
- Чтобы опубликовать значение конфигурации наружу
- Чтобы скачать файл
- Чтобы объявить переменную
* Правильный ответ: Чтобы опубликовать значение конфигурации наружу
Выходы показывают значения после apply, например IP-адреса и пути.

Какой провайдер позволяет создавать локальные файлы?
- local
- aws
- random
* Правильный ответ: local
Провайдер local создаёт файлы на локальной машине.

Что произойдёт, если ресурс A ссылается на атрибут ресурса B?
- Terraform создаст B раньше A
- Terraform создаст A раньше B
- Terraform выдаст ошибку
* Правильный ответ: Terraform создаст B раньше A
Terraform строит граф зависимостей и упорядочивает создание ресурсов.
<!--/QUIZ-->
