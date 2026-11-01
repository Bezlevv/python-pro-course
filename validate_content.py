#!/usr/bin/env python
"""
Валидатор контента: проверяет все файлы уроков в content/ на соответствие формату.

Запуск:  python validate_content.py
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from learn.utils import parse_lesson_file

CONTENT = Path(__file__).resolve().parent / 'content'
MIN_THEORY_WORDS = 200
MIN_TASK_WORDS = 50
MIN_HINT_WORDS = 20
MIN_SOLUTION_WORDS = 80


def words_count(text):
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def main():
    errors = []
    warnings = []

    if not CONTENT.exists():
        print('Нет папки content/')
        return 1

    total_lessons = 0
    for folder in sorted(CONTENT.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        module_md = folder / 'module.md'
        if not module_md.exists():
            errors.append(f'{folder.name}: отсутствует module.md')
            continue

        for path in sorted(folder.glob('*.md')):
            if path.name == 'module.md':
                continue
            total_lessons += 1
            try:
                data = parse_lesson_file(path.read_text(encoding='utf-8'))
            except Exception as exc:
                errors.append(f'{path}: {exc}')
                continue

            if not data.get('title'):
                errors.append(f'{path}: нет поля title')
            if not data.get('order'):
                warnings.append(f'{path}: нет поля order')
            if data.get('difficulty') not in ('beginner', 'intermediate', 'advanced'):
                warnings.append(f'{path}: difficulty={data.get("difficulty")!r}')
            if not data.get('duration'):
                warnings.append(f'{path}: нет поля duration')

            theory_words = words_count(data.get('theory_md', ''))
            task_words = words_count(data.get('task_md', ''))
            hint_words = words_count(data.get('hint_md', ''))
            solution_words = words_count(data.get('solution_md', ''))

            if theory_words < MIN_THEORY_WORDS:
                errors.append(f'{path}: теория слишком короткая ({theory_words} слов < {MIN_THEORY_WORDS})')
            if task_words < MIN_TASK_WORDS:
                errors.append(f'{path}: задача слишком короткая ({task_words} слов < {MIN_TASK_WORDS})')
            if hint_words < MIN_HINT_WORDS:
                errors.append(f'{path}: подсказка слишком короткая ({hint_words} слов < {MIN_HINT_WORDS})')
            if solution_words < MIN_SOLUTION_WORDS:
                errors.append(f'{path}: разбор слишком короткий ({solution_words} слов < {MIN_SOLUTION_WORDS})')

    print(f'Уроков проверено: {total_lessons}')
    if errors:
        print(f'\nОШИБКИ ({len(errors)}):')
        for e in errors:
            print('  - ' + e)
    if warnings:
        print(f'\nПредупреждения ({len(warnings)}):')
        for w in warnings:
            print('  - ' + w)
    print('\nИтог: ' + ('ЕСТЬ ОШИБКИ' if errors else 'OK'))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
