"""Утилиты: парсинг уроков и рендер Markdown."""

import re
from markdown import markdown as md_to_html

# --- Парсинг Markdown-файла урока ---

FRONT_MATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.S)
FIELDS = ('title', 'summary', 'order', 'duration', 'difficulty')

SECTION_MARKERS = {
    'TASK': 'task_md',
    'HINT': 'hint_md',
    'SOLUTION': 'solution_md',
    'QUIZ': 'quiz_md',
    'EXPECTED_OUTPUT': 'expected_output_md',
}


def parse_front_matter(text):
    """Возвращает (meta: dict, body: str)."""
    m = FRONT_MATTER_RE.match(text)
    if not m:
        raise ValueError('Нет front-matter (---  в начале файла')
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' not in line:
            continue
        key, _, value = line.partition(':')
        key = key.strip().lower()
        value = value.strip()
        if key in FIELDS:
            meta[key] = value
    return meta, text[m.end():]


def split_sections(body):
    """Разбивает тело урока на части: theory / task / hint / solution."""
    parts = {'theory_md': []}
    for name in SECTION_MARKERS.values():
        parts[name] = []

    # токенизируем маркеры
    tokens = []
    pos = 0
    pattern = re.compile(r'<!--\s*(/)?\s*(TASK|HINT|SOLUTION|QUIZ|EXPECTED_OUTPUT)\s*-->')
    for m in pattern.finditer(body):
        if m.start() > pos:
            tokens.append(('text', body[pos:m.start()]))
        tokens.append(('close' if m.group(1) else 'open', m.group(2)))
        pos = m.end()
    if pos < len(body):
        tokens.append(('text', body[pos:]))

    current = None
    for kind, value in tokens:
        if kind == 'open':
            if current is not None:
                raise ValueError(f'Вложенный блок {value} внутри блока {current}')
            current = value
        elif kind == 'close':
            if current != value:
                raise ValueError(f'Закрывающий маркер {value} не совпадает с открытым {current}')
            current = None
        else:
            if current is None:
                parts['theory_md'].append(value)
            else:
                parts[SECTION_MARKERS[current]].append(value)

    if current is not None:
        raise ValueError(f'Не закрыт блок {current}')

    return {k: '\n'.join(v).strip() for k, v in parts.items()}


def parse_lesson_file(content):
    """Возвращает dict с данными урока из текста файла."""
    meta, body = parse_front_matter(content)
    sections = split_sections(body)
    return {**meta, **sections}


def parse_quiz(text):
    """Разбирает блок викторины в список вопросов.

    Формат: вопрос на первой строке, варианты через "- ",
    строка "* Правильный ответ: ..." и объяснение после неё.
    Вопросы разделяются пустыми строками.
    """
    questions = []
    if not text or not text.strip():
        return questions
    # Убираем возможные строки-маркеры блока
    lines_all = [ln for ln in text.splitlines() if ln.strip() not in ('<!--QUIZ-->', '<!--/QUIZ-->')]
    text = '\n'.join(lines_all)
    groups = re.split(r'\n\s*\n', text.strip())
    for group in groups:
        lines = [line.strip() for line in group.splitlines() if line.strip()]
        if not lines:
            continue
        question_lines, options, correct_text, explanation = [], [], None, []
        mode = 'q'
        for line in lines:
            if line.startswith('- ') and mode in ('q', 'o'):
                mode = 'o'
                options.append(line[2:].strip())
            elif line.startswith('*') and mode == 'o':
                m = re.match(r'\*\s*(?:Правильный ответ|Правильно|правильный ответ|Ответ)\s*[:—-]?\s*(.+)', line, re.I)
                correct_text = (m.group(1) if m else line.lstrip('*')).strip()
                mode = 'e'
            elif mode == 'e':
                explanation.append(line)
            elif mode == 'o' and correct_text is None:
                options[-1] += ' ' + line
            else:
                question_lines.append(line)
        if not options:
            continue
        correct_index = 0
        if correct_text is not None:
            lowered = correct_text.lower()
            for idx, opt in enumerate(options):
                if opt.lower() == lowered:
                    correct_index = idx
                    break
            else:
                for idx, opt in enumerate(options):
                    if lowered in opt.lower() or opt.lower() in lowered:
                        correct_index = idx
                        break
        questions.append({
            'question': ' '.join(question_lines),
            'options': options,
            'correct_index': correct_index,
            'explanation': ' '.join(explanation),
        })
    return questions


# --- Рендер Markdown в HTML ---

MD_EXTENSIONS = ['fenced_code', 'tables', 'sane_lists', 'nl2br']


def render_markdown(text):
    if not text:
        return ''
    return md_to_html(text, extensions=MD_EXTENSIONS)


def lesson_difficulty_label(value):
    return {
        'beginner': 'Начинающий',
        'intermediate': 'Средний',
        'advanced': 'Продвинутый',
    }.get(value, value)


# ---------- Разбор пронумерованных задач ----------

TASK_SECTION_RE = re.compile(r'(?m)^#{2,4}\s*(?:Задача|Задание)\s*(\d+)')
HINT_SECTION_RE = re.compile(r'(?m)^#{2,4}\s*Подсказка\s*(\d+)')
SOLUTION_SECTION_RE = re.compile(r'(?m)^#{2,4}\s*(?:Разбор|Решение)\s*(\d+)')


def split_numbered_sections(text, pattern):
    """Разбивает текст по пронумерованным заголовкам вида "### Задача 1".

    Возвращает список кортежей (номер, содержимое). Если нумерованных
    заголовков нет, весь текст считается одним разделом №1.
    """
    if not text or not text.strip():
        return []
    matches = list(pattern.finditer(text))
    if not matches:
        return [(1, text.strip())]
    sections = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append((int(m.group(1)), text[start:end].strip()))
    return sections


def build_lesson_tasks(lesson):
    """Собирает список задач урока с подсказками и разборами."""
    tasks_raw = split_numbered_sections(lesson.task_md, TASK_SECTION_RE)
    hints_raw = split_numbered_sections(lesson.hint_md, HINT_SECTION_RE)
    sols_raw = split_numbered_sections(lesson.solution_md, SOLUTION_SECTION_RE)
    hints_map = dict(hints_raw)
    sols_map = dict(sols_raw)

    tasks = []
    for num, body in tasks_raw:
        tasks.append({
            'num': num,
            'task_html': render_markdown(body),
            'hint_html': render_markdown(hints_map.get(num, '')),
            'solution_html': render_markdown(sols_map.get(num, '')),
        })

    # Запасной вариант: один неразмеченный блок
    if not tasks and lesson.task_md.strip():
        tasks.append({
            'num': 1,
            'task_html': render_markdown(lesson.task_md),
            'hint_html': render_markdown(lesson.hint_md),
            'solution_html': render_markdown(lesson.solution_md),
        })
    return tasks


# ---------- Песочница для запуска кода ----------

import ast
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BANNED_IMPORTS = {
    'os', 'sys', 'subprocess', 'socket', 'shutil', 'ctypes', 'importlib',
    'pathlib', 'multiprocessing', 'threading', 'requests', 'urllib', 'http',
    'ftplib', 'pickle', 'inspect', 'traceback', 'pdb', 'readline',
    'builtins', 'site', 'sysconfig', 'venv', 'ensurepip', 'platform', 'psutil',
}
BANNED_CALLS = {'eval', 'exec', 'compile', '__import__', 'breakpoint', 'input', 'open'}
SANDBOX_TIMEOUT = 6
SANDBOX_MAX_OUTPUT = 20000


def normalize_output(text):
    """Нормализует вывод для сравнения: убираем хвостовые пробелы строк и пустые края."""
    return '\n'.join(line.rstrip() for line in text.splitlines()).strip()


def _sandbox_violations(code):
    """Возвращает список запрещённых конструкций в коде."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return [f'Синтаксическая ошибка: {exc}']
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split('.')[0]
                if root in BANNED_IMPORTS:
                    hits.append(f'import {root}')
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in BANNED_IMPORTS:
                hits.append(f'from {node.module} import ...')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BANNED_CALLS:
                hits.append(f'{node.func.id}()')
    return hits


def run_python_code(code, timeout=SANDBOX_TIMEOUT):
    """Запускает код в песочнице, возвращает dict с результатом."""
    violations = _sandbox_violations(code)
    if violations:
        return {'ok': False, 'output': '', 'error': 'Запрещено в песочнице: ' + ', '.join(violations)}
    with tempfile.TemporaryDirectory() as tmpdir:
        script = Path(tmpdir) / 'main.py'
        script.write_text(code, encoding='utf-8')
        env = dict(os.environ)
        env['PYTHONUTF8'] = '1'
        env['PYTHONIOENCODING'] = 'utf-8'
        try:
            proc = subprocess.run(
                [sys.executable, '-B', '-s', str(script)],
                capture_output=True, text=True, encoding='utf-8',
                timeout=timeout, cwd=tmpdir, env=env,
            )
        except subprocess.TimeoutExpired:
            return {'ok': False, 'output': '', 'error': f'Превышен лимит времени ({timeout} c)'}
        output = (proc.stdout or '') + (proc.stderr or '')
        if len(output) > SANDBOX_MAX_OUTPUT:
            output = output[:SANDBOX_MAX_OUTPUT] + '\n... [вывод обрезан]'
        return {'ok': proc.returncode == 0, 'output': output, 'error': ''}
