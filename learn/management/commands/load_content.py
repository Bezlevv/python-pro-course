"""
Команда: python manage.py load_content

Загружает уроки из папки content/ в базу данных.
Структура:
    content/<модуль>/module.md            — front-matter модуля (title, order, description, icon)
    content/<модуль>/<урок>.md            — урок (front-matter + теория + блоки TASK/HINT/SOLUTION)
"""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from learn.models import Lesson, Module, QuizQuestion
from learn.utils import FRONT_MATTER_RE, parse_lesson_file, parse_quiz

CONTENT_DIR = Path(__file__).resolve().parent.parent.parent.parent / 'content'


def parse_module_meta(text):
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        key, _, value = line.partition(':')
        key = key.strip().lower()
        if key in {'title', 'order', 'description', 'icon', 'summary'}:
            meta[key] = value.strip()
    return meta


def _sync_quizzes(lesson, quiz_md):
    """Синхронизирует вопросы викторины урока с содержимым quiz_md."""
    lesson.quizzes.all().delete()
    for idx, q in enumerate(parse_quiz(quiz_md), start=1):
        QuizQuestion.objects.create(
            lesson=lesson,
            order=idx,
            question=q['question'],
            options=q['options'],
            correct_index=q['correct_index'],
            explanation=q['explanation'],
        )


class Command(BaseCommand):
    help = 'Загружает уроки из content/ в базу данных'

    def handle(self, *args, **options):
        if not CONTENT_DIR.exists():
            raise CommandError(f'Папка контента не найдена: {CONTENT_DIR}')

        modules_created = modules_updated = 0
        lessons_created = lessons_updated = 0
        errors = []

        for folder in sorted(CONTENT_DIR.iterdir()):
            if not folder.is_dir() or folder.name.startswith('.'):
                continue

            module_slug = folder.name
            module_meta = {}
            module_md = folder / 'module.md'
            if module_md.exists():
                module_meta = parse_module_meta(module_md.read_text(encoding='utf-8'))

            module, created = Module.objects.update_or_create(
                slug=module_slug,
                defaults={
                    'title': module_meta.get('title', module_slug.replace('-', ' ').title()),
                    'order': int(module_meta.get('order', 999)),
                    'description': module_meta.get('description', module_meta.get('summary', '')),
                    'icon': module_meta.get('icon', '📘'),
                },
            )
            if created:
                modules_created += 1
            else:
                modules_updated += 1

            lesson_files = sorted(
                p for p in folder.iterdir()
                if p.suffix.lower() == '.md' and p.name != 'module.md'
            )
            for i, path in enumerate(lesson_files, start=1):
                try:
                    data = parse_lesson_file(path.read_text(encoding='utf-8'))
                except Exception as e:
                    errors.append(f'{path.name}: {e}')
                    continue

                order = int(data.get('order', i))
                lesson, created = Lesson.objects.update_or_create(
                    slug=path.stem,
                    defaults={
                        'module': module,
                        'title': data.get('title', path.stem.replace('-', ' ').title()),
                        'order': order,
                        'summary': data.get('summary', ''),
                        'duration': data.get('duration', '20 мин'),
                        'difficulty': data.get('difficulty', 'beginner'),
                        'tags': data.get('tags', ''),
                        'is_exam': str(data.get('exam', '')).strip().lower() == 'true',
                        'theory_md': data['theory_md'],
                        'task_md': data['task_md'],
                        'hint_md': data['hint_md'],
                        'solution_md': data['solution_md'],
                        'quiz_md': data['quiz_md'],
                        'expected_output_md': data['expected_output_md'],
                        'test_cases_md': data['test_cases_md'],
                    },
                )
                _sync_quizzes(lesson, data['quiz_md'])
                if created:
                    lessons_created += 1
                else:
                    lessons_updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Модули: создано {modules_created}, обновлено {modules_updated}. '
            f'Уроки: создано {lessons_created}, обновлено {lessons_updated}.'
        ))
        if errors:
            self.stderr.write(self.style.ERROR(f'Ошибки ({len(errors)}):'))
            for e in errors:
                self.stderr.write('  - ' + e)
        if lessons_created + lessons_updated == 0:
            self.stderr.write(self.style.WARNING('Не загружено ни одного урока — проверьте папку content/.'))
