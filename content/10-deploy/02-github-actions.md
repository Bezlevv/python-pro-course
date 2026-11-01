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
<!--/QUIZ-->
