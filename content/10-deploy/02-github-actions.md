---
title: CI/CD: GitHub Actions
summary: Как автоматизировать проверку кода, тесты и публикацию образа с помощью GitHub Actions: события, jobs, шаги, матрица версий и кэширование.
order: 2
duration: 40 мин
difficulty: advanced
tags: ci/cd, github actions, автоматизация, тесты, devops
---

Представь: ты выкатываешь новую фичу, и на сервере всё падает, потому что тесты не прогонялись, а зависимости изменились. CI/CD (Continuous Integration / Continuous Delivery) решает это автоматизацией: каждый пуш в репозиторий запускает проверки (CI), а при успехе — публикацию и деплой (CD). GitHub Actions — встроенный инструмент GitHub для таких конвейеров.

## Как устроены workflow

Workflow — это YAML-файл в папке `.github/workflows/`. В нём описываются события, которые его запускают, и задачи (jobs), которые выполняются на виртуальных машинах (runner).

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Клонируем репозиторий
        uses: actions/checkout@v4

      - name: Ставим Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Устанавливаем зависимости
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Запускаем тесты
        run: pytest
```

Ключевые элементы:

- `name` — название workflow (видно на вкладке Actions);
- `on` — события-триггеры: `push` в ветку `main`, `pull_request`;
- `jobs` — список задач; каждая выполняется на своём runner;
- `runs-on` — тип машины: `ubuntu-latest`, `windows-latest`, `macos-latest`;
- `steps` — последовательность шагов: `uses` подключает готовое действие, `run` выполняет команды в shell;
- `with` — параметры для действия.

## Матрица версий

Один workflow может прогнать тесты сразу на нескольких версиях Python — это называется матрицей:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements-dev.txt
      - run: pytest
```

GitHub запустит job дважды — для каждой версии из списка.

## Кэширование зависимостей

Установка pip-пакетов каждый раз — долго. `actions/setup-python` умеет кэшировать кэш pip автоматически:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
```

Кэш ключуется по `requirements.txt` — при изменении файла зависимости поставятся заново.

## Публикация образа Docker

Продолжим тему из урока про Docker: после успешных тестов можно собрать образ и опубликовать его в GitHub Container Registry:

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/username/my-app:latest
```

Блок `needs: test` гарантирует порядок: образ соберётся только после зелёных тестов. А `secrets.GITHUB_TOKEN` — это автоматически создаваемый секрет GitHub, пароль от которого не нужно хранить самому.

Схема типичного конвейера с зависимостями между job:

```mermaid
flowchart TD
    A["Событие: push или pull_request"] --> B["Workflow ci.yml"]
    B --> C["Job test"]
    B --> D["Job lint"]
    C --> E["Job docker"]
    D --> E
    E --> F["Образ в ghcr.io"]
```

## Итог урока

Мы разобрали устройство workflow: события, задачи, шаги, матрицу версий, кэширование и публикацию Docker-образа. Теперь каждый пуш в `main` будет автоматически запускать тесты — а ты узнаешь о провале до того, как код попадёт в продакшен.

<!--TASK-->
### Задача 1
В репозиторий `my-app` (Flask-приложение, тесты на pytest, зависимости в `requirements-dev.txt` с `pytest` и `flask`) добавь workflow-файл `.github/workflows/ci.yml`, который:

1. Запускается при `push` в ветку `main` и при любом `pull_request`;
2. Содержит job `test` на `ubuntu-latest`;
3. Клонирует репозиторий через `actions/checkout@v4`, ставит Python 3.12 через `actions/setup-python@v5` с кэшем pip;
4. Устанавливает зависимости (`pip install -r requirements-dev.txt`) и запускает `pytest`;
5. Содержит job `docker`, который запускается после `test` только для ветки `main` и публикует образ `ghcr.io/username/my-app:latest` через `docker/login-action@v3` и `docker/build-push-action@v6`.

После пуша зайди на вкладку Actions в GitHub: оба job должны завершиться с зелёной галочкой.

### Задача 2
Расширь job `test` из задачи 1: добавь блок `strategy` с матрицей `matrix.python-version: ["3.11", "3.12"]`, а в `actions/setup-python@v5` вместо фиксированной версии подставь `${{ matrix.python-version }}`. Запушь изменения и зайди на вкладку Actions. Ожидаемый результат: в прогоне workflow job `test` запустится дважды — для Python 3.11 и 3.12 — и обе строки будут зелёными. Остальные job выполнятся один раз.

### Задача 3
Добавь кэширование зависимостей: в `actions/setup-python@v5` укажи `cache: pip` (рядом с `python-version`). Сделай пустой коммит или любое изменение и запушь. Открой второй прогон workflow и разверни шаг `Setup Python` в job `test`: в логе должно появиться сообщение о восстановлении кэша (например, `Cache restored from key: ...`). Ожидаемый результат: шаг `Install dependencies` во втором прогоне выполняется быстрее, потому что пакеты берутся из кэша.

### Задача 4
Добавь в workflow третий job `lint`: он должен клонировать репозиторий, ставить Python и устанавливать `ruff` (`pip install ruff`), затем выполнять `ruff check .`. Измени job `docker` так, чтобы он зависел от обоих job: `needs: [test, lint]`. Запушь изменения. Ожидаемый результат: workflow содержит три job, все они зелёные, а публикация образа происходит только после успешных тестов и линтера.

### Задача 5
В job `test` после шага запуска pytest добавь два шага: сначала запусти `pytest --junitxml=junit.xml` (отчёт в формате JUnit), затем загрузи отчёт как артефакт через `actions/upload-artifact@v4` с `name: pytest-results` и `path: junit.xml`. Запушь, дождись зелёного прогона и открой его страницу: на вкладке Summary будет ссылка на артефакт `pytest-results`. Скачай его и открой `junit.xml`. Ожидаемый результат: артефакт доступен для скачивания, в XML видны результаты всех тестов.
### Задача 6
Добавь в workflow job `integration`, который проверяет приложение с настоящей базой данных. Опиши сервис-контейнер: `services: postgres: image: postgres:16-alpine`, `env: POSTGRES_PASSWORD: secret`, `ports: ["5432:5432"]`, `options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5`. Шаги: checkout, setup-python с кэшем pip, установка зависимостей, затем запуск `pytest tests/test_db.py -v` с переменной окружения `DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres`. Ожидаемый результат: job зелёный, в логе инициализации сервиса видно `database system is ready to accept connections`, а интеграционные тесты подключаются к базе на `localhost:5432` и проходят.

### Задача 7
Сделай проверку новой версии Python неблокирующей. В `strategy.matrix` добавь секцию `include` с записью `- python-version: "3.13"` и `experimental: true`, а к job `test` добавь строку `continue-on-error: ${{ matrix.experimental == true }}`. Запушь изменения и открой прогон на вкладке Actions. Ожидаемый результат: в матрице три job — 3.11, 3.12 и 3.13; если на 3.13 тесты падают, её строка красная, но сам workflow считается успешным, а job `docker` всё равно запускается. Для записей без поля `experimental` выражение даёт `false`, поэтому 3.11 и 3.12 остаются блокирующими.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Workflow лежит в `.github/workflows/ci.yml` — другого пути GitHub не увидит. Не забудь: `on` пишется без `:`, если события идут в списке; `needs: test` в job `docker`; для логина в GHCR используй `username: ${{ github.actor }}` и `password: ${{ secrets.GITHUB_TOKEN }}`. Если workflow не запускается — проверь отступы YAML: это строгий формат.

### Подсказка 2
Матрица задаётся внутри `jobs.test.strategy.matrix`, а значение версии подставляется через `${{ matrix.python-version }}`. Помни, что в YAML список версий пишется в квадратных скобках, а сама матрица должна находиться на правильном уровне отступов — внутри `strategy`, который лежит внутри `test`.

### Подсказка 3
Кэш включается одной строкой `cache: pip` внутри `with` у `actions/setup-python@v5` — его ключ строится на основе `requirements.txt`. Если в логе шага Setup Python не видно сообщения о восстановлении кэша, проверь, что файл `requirements.txt` существует в корне репозитория.

### Подсказка 4
Для `ruff` достаточно шага `run: pip install ruff` и затем `run: ruff check .`. Список зависимостей в `needs` пишется в квадратных скобках: `needs: [test, lint]`. Если `ruff` находит ошибки — job станет красным, и публикация образа не произойдёт.

### Подсказка 5
Артефакты загружаются действием `actions/upload-artifact@v4`: `name` — имя, под которым артефакт появится на вкладке Summary, `path` — путь к файлу относительно корня репозитория. Флаг `--junitxml=junit.xml` заставляет pytest писать отчёт в XML, а не только в консоль.
### Подсказка 6
Сервисы описываются на уровне job, рядом с `runs-on`, а не внутри `steps`. Порт из `ports` пробрасывается на `localhost` runner, поэтому в строке подключения хост — `localhost`. Параметр `options` передаёт аргументы в `docker create`; без health-check шаги могут начаться раньше, чем база примет соединения.

### Подсказка 7
`include` добавляет новые комбинации в матрицу, даже если такой версии нет в основном списке. Выражение `continue-on-error` вычисляется для каждого экземпляра job отдельно, а `matrix.experimental` у старых записей равно `null` — сравнивай именно с `true`, чтобы не получить истину случайно.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Полный файл `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run tests
        run: pytest

  docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ghcr.io/username/my-app:latest
```

Ожидаемый результат: после `git push origin main` на вкладке Actions появится workflow `CI`, job `test` пройдёт все тесты pytest, а job `docker` соберёт образ и опубликует его в `ghcr.io` под именем `ghcr.io/username/my-app:latest`. Для `pull_request` выполнится только `test`.

Что здесь происходит? Блок `on` регистрирует триггеры: push в `main` и создание/обновление pull request. Job `test` выполняется на чистом `ubuntu-latest`: checkout клонирует код, setup-python ставит Python 3.12 и включает кэш pip (второй запуск будет заметно быстрее), затем ставятся зависимости из `requirements-dev.txt` и запускается pytest. Job `docker` имеет `needs: test` — она стартует только после успешного `test`, а `if: github.ref == 'refs/heads/main'` ограничивает запуск веткой `main`. Логин в GHCR использует автоматический токен `GITHUB_TOKEN`, поэтому пароль нигде не хранится.

### Разбор 2
Изменённая секция `test`:

```yaml
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: pytest
```

Ожидаемый результат: на вкладке Actions внутри прогона workflow появятся две строки job `test` — `3.11` и `3.12` — и обе завершатся зелёными галочками.

Что здесь происходит? Блок `strategy.matrix` задаёт список значений, по которым GitHub «раскрывает» job: для каждого элемента списка создаётся отдельный экземпляр job. Внутри шагов значение подставляется через `${{ matrix.python-version }}` — при первом прогоне это `3.11`, при втором `3.12`. Так один workflow проверяет совместимость кода с несколькими версиями Python. Если на одной версии тесты падают, а на другой проходят — строки будут разного цвета, и ты сразу увидишь проблему совместимости.

### Разбор 3
Строка `cache: pip` добавляется в блок `with` действия `actions/setup-python@v5`:

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
```

Ожидаемый результат: в первом прогоне шаг `Setup Python` пишет что-то вроде `Cache not found for input keys: pip-Linux-...`, а во втором — `Cache restored from key: pip-Linux-...`; шаг `Install dependencies` во втором прогоне выполняется заметно быстрее.

Что здесь происходит? GitHub Actions умеет кэшировать каталог pip между прогонами. Ключ кэша строится автоматически на основе файлов зависимостей (`requirements.txt` и подобных): пока они не менялись, кэш подходит, и пакеты не скачиваются заново, а распаковываются из сохранённого состояния. При изменении `requirements.txt` ключ меняется, кэш становится неактуальным, и зависимости устанавливаются с нуля. Это одна из самых простых и эффективных оптимизаций: установка пакетов часто занимает больше половины времени всего CI.

### Разбор 4
Добавь job `lint`:

```yaml
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check .
```

и измени зависимость job `docker`:

```yaml
  docker:
    runs-on: ubuntu-latest
    needs: [test, lint]
    if: github.ref == 'refs/heads/main'
```

Ожидаемый результат: на вкладке Actions появляется три job — `test`, `lint`, `docker`; `lint` зелёный, а `docker` запускается только после успешных `test` и `lint`.

Что здесь происходит? `ruff` — быстрый линтер для Python: он находит стилистические проблемы, неиспользуемые импорты и потенциально опасные места. Job `lint` независима от `test`, поэтому оба job выполняются параллельно. Синтаксис `needs: [test, lint]` задаёт несколько зависимостей: GitHub запустит `docker` только после успешного завершения обоих job, причём они могут выполняться параллельно. Так образ не соберётся и не опубликуется, пока код не прошёл и тесты, и линтер.

### Разбор 5
Добавь в job `test` после шага запуска pytest:

```yaml
      - name: Run tests
        run: pytest --junitxml=junit.xml

      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results
          path: junit.xml
```

Ожидаемый результат: на странице успешного прогона, внизу раздела Summary, появляется блок Artifacts со ссылкой `pytest-results`, по которой можно скачать архив с файлом `junit.xml`.

Что здесь происходит? Флаг `--junitxml=junit.xml` заставляет pytest дополнительно записать результаты тестов в XML-файл в формате JUnit — машиночитаемом формате, который понимают многие инструменты. Действие `actions/upload-artifact@v4` сохраняет этот файл и привязывает его к конкретному прогону workflow. Артефакты хранятся ограниченное время (по умолчанию 90 дней) и полезны, когда нужно разобраться в провале: можно скачать отчёт и посмотреть, какие тесты упали и с каким сообщением, даже не имея доступа к логам прогона.
### Разбор 6
Job с сервисом Postgres:

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: secret
        ports:
          - "5432:5432"
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Интеграционные тесты
        env:
          DATABASE_URL: postgresql://postgres:secret@localhost:5432/postgres
        run: pytest tests/test_db.py -v
```

Ожидаемый результат: в логе job появляется блок `Initialize containers` с сообщением `database system is ready to accept connections`, затем тесты подключаются к базе и проходят — job зелёный.

Что здесь происходит? Блок `services` говорит GitHub поднять рядом с job вспомогательные контейнеры в той же сети. Postgres публикуется на `localhost:5432` runner, поэтому приложение подключается как к обычной локальной базе. `options` передаёт аргументы `docker create`: health-check `pg_isready` проверяет готовность базы, и GitHub ждёт его успеха, прежде чем запускать шаги. Без health-check первый же тест мог бы упасть с «connection refused», хотя база стартует всего на секунду позже. Переменная `DATABASE_URL` задаётся через `env` шага и не попадает в код — тот же принцип, что и в уроке про `.env`. Пароль здесь учебный; в реальном проекте его берут из `secrets`.

### Разбор 7
Изменённая секция `test`:

```yaml
  test:
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental == true }}
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
        include:
          - python-version: "3.13"
            experimental: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements-dev.txt
      - run: pytest
```

Ожидаемый результат: в прогоне три строки job `test` — `3.11`, `3.12` и `3.13`. Если на 3.13 тесты падают, строка помечена красным, но workflow в целом зелёный, а `docker` запускается.

Что здесь происходит? `include` умеет не только дополнять существующие комбинации, но и создавать новые: запись с `python-version: "3.13"` не совпадает ни с одной из основного списка, поэтому превращается в отдельный экземпляр job. `continue-on-error` вычисляется отдельно для каждого экземпляра: у 3.13 `matrix.experimental` равно `true`, у остальных — `null`, и сравнение `null == true` даёт `false`. Так новая версия проверяется, но не блокирует мерж и публикацию образа. Когда 3.13 станет стабильной, достаточно убрать `experimental` и перенести версию в основной список — тогда падения снова начнут ронять конвейер.
<!--/SOLUTION-->

<!--QUIZ-->
Где должны лежать workflow-файлы GitHub Actions?
- В корне репозитория
- В папке .github/workflows/
- В папке scripts/
* Правильный ответ: В папке .github/workflows/
GitHub ищет workflow именно в `.github/workflows/` — файлы из других папок игнорируются.

Что определяет блок on в workflow?
- Тип машины для выполнения
- События, которые запускают workflow
- Список секретов
* Правильный ответ: События, которые запускают workflow
`on` перечисляет триггеры: push, pull_request, schedule и другие.

Зачем нужен `needs: test` в job docker?
- Чтобы job docker выполнился до тестов
- Чтобы job docker запустился только после успешного выполнения job test
- Чтобы задать тип runner
* Правильный ответ: Чтобы job docker запустился только после успешного выполнения job test
`needs` задаёт зависимости между job: docker подождёт завершения test и не запустится при провале.

Что такое GITHUB_TOKEN?
- Секрет, который GitHub создаёт автоматически для каждого workflow
- Пароль от Docker Hub
- Личный токен разработчика
* Правильный ответ: Секрет, который GitHub создаёт автоматически для каждого workflow
`GITHUB_TOKEN` автоматически генерируется GitHub, живёт только во время выполнения workflow и отзывается после него.

Сколько раз выполнится job test, если в матрице указаны версии 3.11 и 3.12?
- Один раз
- Два раза
- Столько раз, сколько коммитов в ветке
* Правильный ответ: Два раза
Матрица раскрывает job для каждого элемента списка: две версии — два отдельных прогона.
Что делает шаг actions/checkout@v3 в workflow?
- Клонирует содержимое репозитория в runner
- Проверяет синтаксис Python
- Устанавливает зависимости проекта
* Правильный ответ: Клонирует содержимое репозитория в runner
Без checkout в runner не будет кода проекта — большинство job начинаются именно с этого шага.

Как в workflow обратиться к секрету SECRET_KEY?
- Через `${{ secrets.SECRET_KEY }}`
- Через `${{ env.SECRET_KEY }}`
- Через `?{{ vars.SECRET_KEY }}`
* Правильный ответ: Через `${{ secrets.SECRET_KEY }}`
Секреты задаются в настройках репозитория (Settings → Secrets) и попадают в workflow только через контекст `secrets`.

Что делает строка `runs-on: ubuntu-latest`?
- Выбирает операционную систему виртуальной машины runner
- Задаёт количество минут на выполнение job
- Указывает версию Python
* Правильный ответ: Выбирает операционную систему виртуальной машины runner
`runs-on` определяет среду, в которой выполнится job, — например, Ubuntu, Windows или macOS.
Что описывает блок services в job?
- Вспомогательные контейнеры (например, базу данных), доступные job по localhost
- Список секретов репозитория
- Набор runner, на которых выполнится job
* Правильный ответ: Вспомогательные контейнеры (например, базу данных), доступные job по localhost
GitHub поднимает их рядом с job в общей сети и ждёт health-check, прежде чем запускать шаги.

Что делает continue-on-error: true у job?
- Позволяет job упасть, не помечая весь workflow как проваленный
- Повторяет job до успешного завершения
- Отключает запуск следующих job
* Правильный ответ: Позволяет job упасть, не помечая весь workflow как проваленный
Это удобно для экспериментальных версий и необязательных проверок: результат виден, но не блокирует конвейер.

Какой триггер позволяет запускать workflow вручную кнопкой Run workflow?
- workflow_dispatch
- pull_request
- schedule
* Правильный ответ: workflow_dispatch
workflow_dispatch добавляет кнопку ручного запуска и позволяет передавать входные параметры через блок inputs.

Что произойдёт с job docker, если job test завершится с ошибкой?
- docker не запустится, потому что needs требует успешного завершения test
- docker запустится всё равно
- docker запустится, но только для pull_request
* Правильный ответ: docker не запустится, потому что needs требует успешного завершения test
`needs` строит жёсткую зависимость: при падении предка зависимая job пропускается.
Что делает матрица (matrix) в GitHub Actions?
- Запускает один job с несколькими комбинациями параметров
- Собирает несколько репозиториев
- Параллелит шаги внутри одного job
- Хранит секреты
* Правильный ответ: Запускает один job с несколькими комбинациями параметров
Например, тесты на 3.11/3.12/3.13 — три параллельных прогона.

Как правильно передать секрет в workflow?
- Через ${{ secrets.NAME }}
- Вписать значение в YAML
- Через переменную окружения в шаге
- Через собственный файл
* Правильный ответ: Через ${{ secrets.NAME }}
Секрет подставляется раннером; значение никогда не попадает в YAML.

Зачем кэшировать pip?
- Чтобы ускорить установку зависимостей между запусками
- Чтобы скрыть зависимости
- Чтобы обойти GitHub API
- Чтобы зафиксировать версии
* Правильный ответ: Чтобы ускорить установку зависимостей между запусками
Кэш по хешу requirements.txt не перезагружает скачанные пакеты.

Что добавляет workflow_dispatch?
- Кнопку ручного запуска workflow
- Автоматический запуск по расписанию
- Защиту от PR
- Логирование
* Правильный ответ: Кнопку ручного запуска workflow
Workflow можно запустить вручную из вкладки Actions в любой момент.

# 
<!--/QUIZ-->
