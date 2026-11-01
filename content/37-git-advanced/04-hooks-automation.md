---
title: Git hooks и автоматизация
summary: Как Git вызывает хуки в ключевые моменты, как писать pre-commit, commit-msg и pre-push хуки, как хранить их в репозитории.
order: 4
duration: 40 мин
difficulty: advanced
tags: git, hooks, pre-commit, commit-msg, pre-push, автоматизация
---

Git hooks (хуки) — это скрипты, которые Git запускает автоматически в ключевые моменты: перед коммитом, перед push, после merge и так далее. Они превращают Git из «просто хранилища версий» в инструмент дисциплины: нельзя закоммитить код с запрещёнными секретами, нельзя запушить кривые сообщения, нельзя обойти тесты. Это самый практичный способ автоматизировать контроль качества на уровне репозитория.

## Где живут хуки

Хуки лежат в `$GIT_DIR/hooks/` (по умолчанию `.git/hooks/`):

```bash
ls .git/hooks/
# applypatch-msg.sample  commit-msg.sample  post-commit.sample
# pre-commit.sample  pre-push.sample  ...
```

Всё, что в `.git/hooks/` — часть локального репозитория, а не кода, поэтому в git оно **не** попадает. Чтобы делиться хуками с командой, храни их в репозитории (например, в `scripts/hooks/`) и укажи Git, где их искать:

```bash
mkdir -p scripts/hooks
git config core.hooksPath scripts/hooks
```

Теперь Git выполняет `scripts/hooks/pre-commit` вместо `.git/hooks/pre-commit`. Файл обязан быть исполняемым (`chmod +x`).

## Как работает хук

Хук — это исполняемый скрипт (bash, Python, что угодно). Выходной код решает всё:

- **0** — действие разрешено, Git продолжает;
- **ненулевой** — Git **останавливает** операцию с сообщением из stderr.

Пример простейшего `pre-commit` на bash:

```bash
#!/bin/sh
echo "Коммитим!" 
exit 0
```

## Важные хуки

**pre-commit** — перед созданием коммита. Классика: прогнать линтер/тесты, проверить, что нет маркеров конфликтов и секретов:

```bash
#!/bin/sh
if git grep -n '<<<<<<<' -- ':!*.md'; then
  echo "Найдены маркеры конфликтов"; exit 1
fi
```

**commit-msg** — после ввода сообщения, до создания коммита. Получает путь к файлу с сообщением. Идеален для проверки формата:

```bash
#!/bin/sh
grep -qE '^(feat|fix|docs|refactor|test|chore):' "$1" \
  || { echo "Сообщение должно начинаться с feat:/fix:/..."; exit 1; }
```

**pre-push** — перед отправкой в remote. Получает имя remote и URL. Стандартная защита: не пушить в `main` напрямую, прогнать тесты:

```bash
#!/bin/sh
pytest -q || exit 1
```

**Другие:** `pre-rebase` (запрет rebase опубликованных веток), `post-commit` (уведомления, генерация метрик), `post-merge`, `post-checkout`, `prepare-commit-msg` (автоподстановка номера задачи).

## Хук на Python

Хук не обязан быть на bash. Например, `pre-commit` на Python:

```python
#!/usr/bin/env python3
import subprocess, sys

out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                     capture_output=True, text=True).stdout
if any("secret" in name.lower() for name in out.splitlines()):
    print("Не коммить файлы со словом secret в имени!")
    sys.exit(1)
```

## Хорошие практики

- Локально для быстрого старта: `git config core.hooksPath scripts/hooks` + скрипты в `scripts/hooks/`.
- В команде: договорись о наборе хуков, положи их в репозиторий, инструкцию по включению — в README. Для автоматической установки используют инструменты вроде pre-commit (Python) или husky (JavaScript) — они сами ставят хуки.
- Не делай хуки слишком медленными: если `pre-commit` гоняет весь тестовый набор по 5 минут, коллеги начнут обходить его (`git commit --no-verify`). Проверяй только то, что касается индекса.
- Помни: хук — не защита, а напоминание: `--no-verify` обходит любой хук, поэтому критичные проверки должны жить и в CI.

<!--TASK-->
### Задача 1
Создай репозиторий и первый хук:

1. `git init`; настрой имя и почту; создай `app.py` и сделай базовый коммит.
2. Создай `.git/hooks/pre-commit` — bash-скрипт, который через `git grep -n '<<<<<<<'` ищет маркеры конфликтов в индексе и при нахождении завершается с кодом 1.
3. Сделай его исполняемым.
4. Добавь в `app.py` маркер `<<<<<<< HEAD` и попробуй закоммитить — коммит должен быть заблокирован.
5. Убери маркер и закоммить снова — должно пройти.

Ожидаемый результат: первая попытка коммита завершается с ошибкой и сообщением из хука; вторая проходит, `git log --oneline` показывает два коммита.

### Задача 2
Напиши pytest-тест `test_commit_msg_hook.py`: временный репозиторий, в `.git/hooks/commit-msg` — скрипт, который разрешает только сообщения вида `feat: ...` или `fix: ...` (regex `^(feat|fix):`). Затем:

1. Попытка `git commit -m "bad message"` должна завершиться ненулевым кодом и не создать коммит.
2. `git commit -m "feat: добавлена проверка"` — успешно.
3. Проверь, что `git log --oneline` содержит ровно один коммит (базовый + feat).

Запусти `pytest test_commit_msg_hook.py -v`: ожидаемый результат — `1 passed`.

### Задача 3
Напиши pytest-тест `test_pre_push_hook.py`: временный репозиторий с remote-репозиторием (голым, `git init --bare`), в `.git/hooks/pre-push` — скрипт, который всегда завершается с кодом 1 и сообщением `push запрещён`. Затем:

1. `git push origin main` должен завершиться ненулевым кодом.
2. Проверь, что в remote-репозитории нет коммитов (`git log` там падает или пустой).

Запусти `pytest test_pre_push_hook.py -v`: ожидаемый результат — `1 passed`.

### Задача 4
Вынеси хуки в репозиторий. В репозитории из задачи 1:

1. Создай папку `scripts/hooks` и перенеси туда свой `pre-commit`.
2. Выполни `git config core.hooksPath scripts/hooks`.
3. Закоммить изменения (сам хук-скрипт тоже должен попасть в историю).
4. Проверь, что хук продолжает работать: снова добавь маркер, попробуй закоммитить — блокировка должна сработать.

Ожидаемый результат: `git config core.hooksPath` возвращает `scripts/hooks`, а хук блокирует коммит с маркером даже после того, как ты удалил `.git/hooks/pre-commit`.

### Задача 5
Напиши хук `pre-commit` на Python, который прогоняет pytest по изменённым файлам:

1. Скрипт: запускает `pytest -q` (через `subprocess.run`), при падении выводит `Тесты не прошли!` и завершается с кодом 1.
2. Добавь в репозиторий тест `test_math.py` с заведомо падающим тестом — попробуй закоммитить: коммит должен быть заблокирован.
3. Исправь тест, закоммить повторно.

Ожидаемый результат: первый коммит заблокирован с сообщением `Тесты не прошли!`, второй проходит.
<!--/TASK-->

<!--HINT-->
### Подсказка 1
Внутри хука `$1`-аргументов нет — работаем с индексированными изменениями. `git grep -n '<<<<<<<'` ищет по всему дереву, включая рабочие файлы; чтобы ограничиться индексом, можно использовать `git diff --cached` и `grep`, либо упрощённо — `git grep` по файлам и проверку через `if ...; then echo "..."; exit 1; fi`. Обязательно `chmod +x .git/hooks/pre-commit`.

### Подсказка 2
Hook-скрипт получает путь к файлу с сообщением как `$1`. Проверка: `grep -qE '^(feat|fix):' "$1"`. В тесте вызывай `git commit` с `check=False` и проверяй `returncode != 0`, а затем `git log --format=%s` — сообщение `bad message` там отсутствовать.

### Подсказка 3
Для push нужен remote: создай bare-репозиторий командой `git init --bare remote.git` в временной папке, добавь его `git remote add origin <путь>`. Хук `pre-push` срабатывает до отправки, так что ненулевой код — пустой remote. Проверка пустоты: `git log` в bare-репозитории вернёт ошибку `does not have any commits` (ненулевой код) либо проверь через `git rev-parse --verify HEAD` с `check=False`.

### Подсказка 4
`git config core.hooksPath scripts/hooks` — локальная настройка репозитория, хранится в `.git/config`, не в коде. После переноса скрипта убедись, что он остался исполняемым. `git add scripts/hooks/pre-commit` закоммитит сам хук — команда увидит его в истории.

### Подсказка 5
Python-хук: `#!/usr/bin/env python3`, `subprocess.run(["pytest", "-q"])`, `sys.exit(1)` при `returncode != 0`. Помни: хук выполняется из корня репозитория, поэтому путь к тесту — относительно него. Проверь, что файл исполняемый и начинается с shebang.
<!--/HINT-->

<!--SOLUTION-->
### Разбор 1
Хук:

```bash
#!/bin/sh
if git grep -q -n '<<<<<<<' -- '*.py'; then
  echo "Ошибка: найдены маркеры конфликтов" >&2
  exit 1
fi
```

Сохраняем в `.git/hooks/pre-commit`, делаем исполняемым:

```bash
chmod +x .git/hooks/pre-commit
```

Теперь добавляем в `app.py` строку `<<<<<<< HEAD` и пробуем коммитить:

```bash
echo '<<<<<<< HEAD' >> app.py
git add app.py
git commit -m "плохой коммит"
# Ошибка: найдены маркеры конфликтов
# Коммит не создан
```

Убираем маркер:

```bash
sed -i '/<<<<<<< HEAD/d' app.py
git add app.py
git commit -m "хороший коммит"
```

Разбор: Git при вызове `git commit` запускает `pre-commit`. Скрипт ищет маркеры `git grep -q`, и если нашёл — печатает сообщение в stderr и возвращает 1. Git видит ненулевой код и отменяет коммит. Это самый надёжный способ не «запушить» конфликт случайно: маркеры часто остаются после ручного разрешения, и хук ловит их до того, как они попадут в историю.

### Разбор 2
Решение:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def test_commit_msg_hook_blocks_bad_format():
    with tempfile.TemporaryDirectory() as repo:
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        (Path(repo) / "app.py").write_text("print('hi')\n")
        git("add", "app.py", cwd=repo)
        git("commit", "-m", "base", cwd=repo)

        hook = Path(repo) / ".git/hooks/commit-msg"
        hook.write_text("#!/bin/sh\ngrep -qE '^(feat|fix):' \"$1\" || { echo 'bad format'; exit 1; }\n")
        hook.chmod(0o755)

        bad = git("commit", "--allow-empty", "-m", "bad message",
                  cwd=repo, check=False)
        assert bad.returncode != 0

        good = git("commit", "--allow-empty", "-m", "feat: добавлена проверка",
                   cwd=repo, check=False)
        assert good.returncode == 0

        log = git("log", "--format=%s", cwd=repo).stdout
        assert "bad message" not in log
        assert "feat: добавлена проверка" in log
```

Разбор: хук `commit-msg` получает путь к временному файлу с сообщением как `$1`. `grep -qE '^(feat|fix):'` проверяет формат; при неудаче — 1, и Git отклоняет коммит. В тесте первый коммит (`bad message`) отклонён, второй (`feat: ...`) принят; проверки лога подтверждают, что плохое сообщение не попало в историю. `--allow-empty` нужен, чтобы не привязываться к содержимому файлов. Запуск: `pytest test_commit_msg_hook.py -v` → `1 passed`.

### Разбор 3
Решение:

```python
import subprocess
import tempfile
from pathlib import Path

import pytest


def git(*args, cwd, check=True):
    return subprocess.run(
        ["git", *args], cwd=cwd, check=check,
        capture_output=True, text=True,
    )


def test_pre_push_hook_blocks_push():
    with tempfile.TemporaryDirectory() as tmp:
        repo = str(Path(tmp) / "repo")
        remote = str(Path(tmp) / "remote.git")
        Path(repo).mkdir()
        git("init", "--bare", remote)
        git("init", cwd=repo)
        git("config", "user.name", "Тест", cwd=repo)
        git("config", "user.email", "test@example.com", cwd=repo)

        (Path(repo) / "app.py").write_text("x = 1\n")
        git("add", "app.py", cwd=repo)
        git("commit", "-m", "base", cwd=repo)
        git("remote", "add", "origin", remote, cwd=repo)

        hook = Path(repo) / ".git/hooks/pre-push"
        hook.write_text("#!/bin/sh\necho 'push запрещён' >&2; exit 1\n")
        hook.chmod(0o755)

        result = git("push", "origin", "main", cwd=repo, check=False)
        assert result.returncode != 0
        assert "push запрещён" in result.stderr

        head = git("rev-parse", "--verify", "HEAD", cwd=remote, check=False)
        assert head.returncode != 0
```

Разбор: `pre-push` срабатывает до отправки объектов. Скрипт всегда возвращает 1 — push отклонён. Проверка: `returncode != 0` у push и отсутствие HEAD в bare-репозитории (`rev-parse --verify HEAD` возвращает ненулевой код, потому что в remote нет коммитов). Это точная модель ситуации «хук не пускает в прод»: например, когда забыли прогнать тесты или ветка не прошла ревью. Запуск: `pytest test_pre_push_hook.py -v` → `1 passed`.

### Разбор 4
Шаги:

```bash
mkdir -p scripts/hooks
git mv .git/hooks/pre-commit scripts/hooks/pre-commit   # или просто cp
git config core.hooksPath scripts/hooks
git add scripts/hooks/pre-commit
git commit -m "chore: добавить хук pre-commit в репозиторий"
rm .git/hooks/pre-commit   # больше не нужен — Git смотрит в scripts/hooks
```

Проверка:

```bash
git config core.hooksPath        # scripts/hooks
echo '<<<<<<< HEAD' >> app.py
git add app.py
git commit -m "тест"            # заблокировано хуком
```

Разбор: `core.hooksPath` перенаправляет поиск хуков из `.git/hooks/` в `scripts/hooks/`. Теперь хук — часть кода: его видно в ревью, он не потеряется при клонировании, его можно версионировать. Единственный нюанс — `core.hooksPath` не распространяется автоматически на других (это локальная настройка), поэтому при подключении новых разработчиков они должны один раз выполнить ту же команду. Именно для автоматизации этого шага существуют инструменты вроде pre-commit/husky, которые генерируют конфиг и ставят хуки сами.

### Разбор 5
Хук:

```python
#!/usr/bin/env python3
import subprocess
import sys

result = subprocess.run(["pytest", "-q", "test_math.py"])
if result.returncode != 0:
    print("Тесты не прошли!", file=sys.stderr)
    sys.exit(1)
```

Сохраняем в `.git/hooks/pre-commit`, `chmod +x`. Тест:

```python
def test_add():
    assert 1 + 1 == 3  # заведомо провальный
```

Попытка коммита:

```bash
git add test_math.py pre_commit.py
git commit -m "feat: добавить тест"
# Тесты не прошли!
# Коммит отменён
```

Исправляем `assert 1 + 1 == 2`, коммитим — проходит. Разбор: хук на Python удобнее bash для сложной логики. Ключевой момент: `pytest` запускается из корня репозитория, поэтому пути относительные. Перехват через `subprocess` даёт полный контроль: можно выводить не только код возврата, но и фрагмент вывода, список упавших тестов, ветку, имя пользователя. Такой `pre-commit` — первая линия обороны: он ловит падающие тесты до того, как они попадут в историю, а CI остаётся второй линией.
<!--/SOLUTION-->

<!--QUIZ-->
Где Git ищет хуки по умолчанию?
- В папке .git/hooks/
- В корне репозитория
- В папке scripts/
- В папке .github/hooks/
* Правильный ответ: В папке .git/hooks/
По умолчанию хуки живут в .git/hooks/ (файлы .sample — примеры).

Какой код возврата разрешает операцию хуку?
- 0
- 1
- 255
- 400
* Правильный ответ: 0
Нулевой код означает успех; любой ненулевой — остановку операции.

Что делает хук pre-commit?
- Запускается перед созданием коммита и может его заблокировать
- Запускается после push
- Проверяет сообщение коммита
- Создаёт ветки
* Правильный ответ: Запускается перед созданием коммита и может его заблокировать
pre-commit выполняется до записи коммита; ненулевой код отменяет коммит.

Какой хук проверяет формат сообщения коммита?
- commit-msg
- pre-commit
- post-commit
- pre-push
* Правильный ответ: commit-msg
commit-msg получает путь к файлу с сообщением и может отклонить коммит из-за плохого формата.

Что получает commit-msg в качестве аргумента?
- Путь к файлу с сообщением коммита
- Хэш коммита
- Имя ветки
- Имя автора
* Правильный ответ: Путь к файлу с сообщением коммита
В $1 лежит путь к временному файлу, в котором Git хранит текст сообщения.

Как запретить push в remote хуком?
- Скрипт pre-push должен вернуть ненулевой код
- Скрипт post-push должен вернуть 0
- Удалить remote
- Отключить pre-commit
* Правильный ответ: Скрипт pre-push должен вернуть ненулевой код
pre-push выполняется до отправки; ненулевой код отменяет push.

Как заставить Git брать хуки из scripts/hooks?
- git config core.hooksPath scripts/hooks
- git hooks --path scripts/hooks
- git config hooks.dir scripts/hooks
- Переименовать папку в .git/hooks
* Правильный ответ: git config core.hooksPath scripts/hooks
Настройка core.hooksPath указывает каталог хуков вместо .git/hooks.

Какая команда обходит хуки?
- git commit --no-verify
- git commit --force
- git commit --direct
- git commit --skip-hooks
* Правильный ответ: git commit --no-verify
--no-verify пропускает хуки, поэтому критичные проверки должны дублироваться в CI.

Какой язык можно использовать для хуков?
- Любой исполняемый: bash, Python, и т. д.
- Только bash
- Только C
- Только JavaScript
* Правильный ответ: Любой исполняемый: bash, Python, и т. д.
Хук — любой исполняемый файл с shebang; Git не ограничивает язык.

Зачем хранить хуки в репозитории, а не только в .git/hooks?
- Чтобы делиться ими с командой и версионировать
- Чтобы они работали быстрее
- Чтобы их нельзя было обойти
- Чтобы Git их автоматически включал
* Правильный ответ: Чтобы делиться ими с командой и версионировать
Хуки в scripts/hooks попадают в историю и видны всем; включение — одна команда core.hooksPath.
<!--/QUIZ-->
