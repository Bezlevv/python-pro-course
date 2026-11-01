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
    pattern = re.compile(r'<!--\s*(/)?\s*(TASK|HINT|SOLUTION)\s*-->')
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
