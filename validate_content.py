"""
Валидатор контента: соответствие уроков спецификации content/FORMAT.md.

Проверяет: front-matter, минимум слов теории, минимум задач/подсказок/разборов,
минимум вопросов викторины, наличие схемы Mermaid, минимальный объём разборов.

Запуск:  python validate_content.py
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from learn.utils import (
    TASK_SECTION_RE,
    parse_lesson_file,
    parse_quiz,
    split_numbered_sections,
)

CONTENT = Path(__file__).resolve().parent / 'content'
MIN_THEORY_WORDS = 200
MIN_TASK_WORDS = 50
MIN_HINT_WORDS = 20
MIN_SOLUTION_WORDS = 80
MIN_TASKS = 7
MIN_QUIZ = 12
MERMAID_RE = re.compile(r'```mermaid', re.I)


def words_count(text):
    return len([w for w in text.split() if any(c.isalnum() for c in w)])


def main():
    errors = []
    warnings = []
    total_lessons = 0
    no_mermaid = 0

    if not CONTENT.exists():
        print('Нет папки content/')
        return 1

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
            tasks_count = len(split_numbered_sections(data.get('task_md', ''), TASK_SECTION_RE))
            quizzes_count = len(parse_quiz(data.get('quiz_md', '')))
            is_exam = str(data.get('exam', '')).strip().lower() == 'true'

            if is_exam:
                if quizzes_count < 8:
                    errors.append(f'{path}: у экзамена должно быть не меньше 8 вопросов (сейчас {quizzes_count})')
                continue

            if theory_words < MIN_THEORY_WORDS:
                errors.append(f'{path}: теория слишком короткая ({theory_words} слов < {MIN_THEORY_WORDS})')
            if task_words < MIN_TASK_WORDS:
                errors.append(f'{path}: задачи слишком короткие ({task_words} слов < {MIN_TASK_WORDS})')
            if hint_words < MIN_HINT_WORDS:
                errors.append(f'{path}: подсказки слишком короткие ({hint_words} слов < {MIN_HINT_WORDS})')
            if solution_words < MIN_SOLUTION_WORDS:
                errors.append(f'{path}: разборы слишком короткие ({solution_words} слов < {MIN_SOLUTION_WORDS})')
            if tasks_count < MIN_TASKS:
                errors.append(f'{path}: задач должно быть не меньше {MIN_TASKS} (сейчас {tasks_count})')
            if quizzes_count < MIN_QUIZ:
                errors.append(f'{path}: вопросов викторины должно быть не меньше {MIN_QUIZ} (сейчас {quizzes_count})')
            if not MERMAID_RE.search(data.get('theory_md', '')):
                no_mermaid += 1
                warnings.append(f'{path}: нет схемы Mermaid в теории')

    print(f'Уроков проверено: {total_lessons} (без схемы Mermaid: {no_mermaid})')
    if errors:
        print(f'\nОШИБКИ ({len(errors)}):')
        for e in errors:
            print('  - ' + e)
    if warnings:
        print(f'\nПредупреждения ({len(warnings)}):')
        for w in warnings[:40]:
            print('  - ' + w)
        if len(warnings) > 40:
            print(f'  ... и ещё {len(warnings) - 40}')
    print('\nИтог: ' + ('ЕСТЬ ОШИБКИ' if errors else 'OK'))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
