import csv
import json
import re
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Achievement,
    CodeAttempt,
    Comment,
    Lesson,
    LessonNote,
    LessonProgress,
    Module,
    UserAchievement,
)
from .utils import (
    build_lesson_tasks,
    lesson_difficulty_label,
    normalize_output,
    render_markdown,
    run_python_code,
)


# ---------- Вспомогательное ----------

def _module_progress(user):
    if not user.is_authenticated:
        return {}
    rows = (
        LessonProgress.objects
        .filter(user=user, completed_at__isnull=False)
        .values('lesson__module')
        .annotate(done=Count('id'))
    )
    return {row['lesson__module']: row['done'] for row in rows}


def _modules_data(user):
    progress = _module_progress(user)
    data = []
    for module in Module.objects.annotate(lesson_count=Count('lessons')):
        total = module.lesson_count
        done = progress.get(module.id, 0)
        data.append({
            'module': module,
            'total': total,
            'done': done,
            'pct': round(done / total * 100) if total else 0,
        })
    return data


def _streak(user):
    days = {
        d.date() for d in
        LessonProgress.objects.filter(user=user, completed_at__isnull=False)
        .values_list('completed_at', flat=True)
    }
    today = date.today()
    current = today if today in days else today - timedelta(days=1)
    streak = 0
    while current in days:
        streak += 1
        current -= timedelta(days=1)
    return streak


def _completed_modules_count(user):
    total = 0
    for module in Module.objects.annotate(cnt=Count('lessons')):
        done = LessonProgress.objects.filter(
            user=user, lesson__module=module, completed_at__isnull=False
        ).count()
        if module.cnt and done >= module.cnt:
            total += 1
    return total


def _award_achievements(user):
    """Выдаёт достижения, которые пользователь уже заслужил."""
    stats = {
        'lessons_count': LessonProgress.objects.filter(user=user, completed_at__isnull=False).count(),
        'modules_complete': _completed_modules_count(user),
        'streak_days': _streak(user),
    }
    awarded = []
    for ach in Achievement.objects.all():
        if stats.get(ach.kind, 0) >= ach.threshold and \
                not UserAchievement.objects.filter(user=user, achievement=ach).exists():
            UserAchievement.objects.create(user=user, achievement=ach)
            awarded.append(ach)
    return awarded


def _lesson_ctx(request, lesson):
    done_ids = set()
    read_ids = set()
    if request.user.is_authenticated:
        progress_rows = LessonProgress.objects.filter(user=request.user)
        done_ids = set(progress_rows.filter(completed_at__isnull=False).values_list('lesson_id', flat=True))
        read_ids = set(progress_rows.filter(read=True).values_list('lesson_id', flat=True))
    module_lessons = list(lesson.module.lessons.all())
    note = ''
    if request.user.is_authenticated:
        note_obj = LessonNote.objects.filter(user=request.user, lesson=lesson).first()
        note = note_obj.text if note_obj else ''
    return {
        'lesson': lesson,
        'theory_html': render_markdown(lesson.theory_md),
        'tasks': build_lesson_tasks(lesson),
        'module_lessons': module_lessons,
        'done_ids': done_ids,
        'read_ids': read_ids,
        'difficulty_label': lesson_difficulty_label(lesson.difficulty),
        'next_lesson': lesson.next_lesson(),
        'prev_lesson': lesson.prev_lesson(),
        'is_done': lesson.id in done_ids,
        'is_read': lesson.id in read_ids,
        'tags': lesson.tag_list(),
        'quizzes': list(lesson.quizzes.all()),
        'comments': list(lesson.comments.select_related('user')),
        'note': note,
        'module_done': sum(1 for l in module_lessons if l.id in done_ids),
        'module_pct': round(sum(1 for l in module_lessons if l.id in done_ids) / len(module_lessons) * 100) if module_lessons else 0,
    }


# ---------- Страницы ----------

def home(request):
    modules_data = _modules_data(request.user)
    total_lessons = Lesson.objects.count()
    completed = sum(item['done'] for item in modules_data)
    recent = Lesson.objects.select_related('module').order_by('-created')[:6]
    return render(request, 'home.html', {
        'modules_data': modules_data,
        'total_lessons': total_lessons,
        'completed': completed,
        'completed_pct': round(completed / total_lessons * 100) if total_lessons else 0,
        'recent': recent,
    })


def module_list(request):
    return render(request, 'modules.html', {'modules_data': _modules_data(request.user)})


def module_detail(request, module_slug):
    module = get_object_or_404(Module.objects.annotate(lesson_count=Count('lessons')), slug=module_slug)
    lessons = list(module.lessons.all())
    done_ids = set()
    if request.user.is_authenticated:
        done_ids = set(
            LessonProgress.objects.filter(user=request.user, lesson__module=module, completed_at__isnull=False)
            .values_list('lesson_id', flat=True)
        )
    return render(request, 'module_detail.html', {
        'module': module,
        'lessons': lessons,
        'done_ids': done_ids,
        'done_count': sum(1 for l in lessons if l.id in done_ids),
        'pct': round(sum(1 for l in lessons if l.id in done_ids) / len(lessons) * 100) if lessons else 0,
    })


def lesson_detail(request, module_slug, lesson_slug):
    module = get_object_or_404(Module, slug=module_slug)
    lesson = get_object_or_404(Lesson, module=module, slug=lesson_slug)
    return render(request, 'lesson_detail.html', _lesson_ctx(request, lesson))


@require_POST
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if created:
        progress.completed_at = None  # auto_now проставит время при save
        progress.save()
        awarded = _award_achievements(request.user)
        text = f'Отлично! Урок «{lesson.title}» отмечен решённым 🎉'
        if awarded:
            icons = ' '.join(a.icon for a in awarded)
            text += f' Новые достижения: {icons}'
        messages.success(request, text)
    else:
        progress.completed_at = None
        progress.save()
        messages.info(request, f'Отметка «{lesson.title}» снята.')
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def toggle_read(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.read = not progress.read
    progress.save()
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def run_code(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    try:
        payload = json.loads(request.body or '{}')
    except ValueError:
        payload = {}
    code = payload.get('code', '')
    if not code.strip():
        return JsonResponse({'ok': False, 'output': '', 'error': 'Введи код для запуска'})
    if len(code) > 20000:
        return JsonResponse({'ok': False, 'output': '', 'error': 'Код слишком длинный (максимум 20 000 символов)'})
    result = run_python_code(code)
    expected = lesson.expected_output_md.strip()
    if result.get('ok') and expected:
        result['passed'] = normalize_output(result['output']) == normalize_output(expected)
        result['verdict'] = (
            '✅ Вывод совпал с ожидаемым!'
            if result['passed'] else '❌ Вывод не совпал с ожидаемым — результат отличается.'
        )
    else:
        result['passed'] = bool(result.get('ok'))
        result['verdict'] = '' if result.get('ok') else 'Код завершился с ошибкой.'
    CodeAttempt.objects.create(
        user=request.user, lesson=lesson, code=code,
        output=result.get('output', ''), passed=result.get('passed'),
    )
    return JsonResponse(result)


@require_POST
def quiz_check(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = list(lesson.quizzes.all())
    try:
        answers = json.loads(request.body or '{}').get('answers', [])
    except ValueError:
        answers = []
    results = []
    for i, q in enumerate(quizzes):
        user_answer = answers[i] if i < len(answers) else None
        correct = isinstance(user_answer, int) and user_answer == q.correct_index
        results.append({
            'correct': correct,
            'correct_index': q.correct_index,
            'explanation': q.explanation,
            'question': q.question,
        })
    score = sum(1 for r in results if r['correct'])
    return JsonResponse({'score': score, 'total': len(results), 'results': results})


@require_POST
@login_required
def add_comment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    text = request.POST.get('text', '').strip()
    if text:
        Comment.objects.create(lesson=lesson, user=request.user, text=text[:3000])
        messages.success(request, 'Комментарий добавлен.')
    return redirect(lesson.get_absolute_url())


@require_POST
@login_required
def save_note(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    text = request.POST.get('text', '')
    LessonNote.objects.update_or_create(user=request.user, lesson=lesson, defaults={'text': text[:10000]})
    return JsonResponse({'ok': True})


def download_code(request, module_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, module__slug=module_slug, slug=lesson_slug)
    raw = '\n'.join([lesson.theory_md, lesson.task_md, lesson.solution_md])
    blocks = re.findall(r'```python\s*\n(.*?)```', raw, re.S)
    parts = [f'# {lesson.title}', f'# Модуль: {lesson.module.title}', '', 'from __future__ import annotations', '']
    parts.extend(blocks)
    content = '\n\n'.join(parts)
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{lesson.slug}.py"'
    return response


@login_required
def export_progress(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="python_pro_progress.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Модуль', 'Урок', 'Сложность', 'Прочитан', 'Решён', 'Дата решения', 'Теги'])
    rows = (
        LessonProgress.objects.filter(user=request.user)
        .select_related('lesson__module')
        .order_by('lesson__module__order', 'lesson__order')
    )
    for p in rows:
        writer.writerow([
            p.lesson.module.title,
            p.lesson.title,
            p.lesson.get_difficulty_display(),
            'да' if p.read else 'нет',
            'да' if p.completed_at else 'нет',
            p.completed_at.strftime('%d.%m.%Y %H:%M') if p.completed_at else '',
            p.lesson.tags,
        ])
    return response


def search(request):
    q = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '')
    tag = request.GET.get('tag', '')
    results = Lesson.objects.select_related('module')
    if q:
        results = results.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(theory_md__icontains=q))
    if difficulty in ('beginner', 'intermediate', 'advanced'):
        results = results.filter(difficulty=difficulty)
    if tag:
        results = results.filter(tags__icontains=tag)
    results = results.order_by('module__order', 'order')
    all_tags = sorted({t for lesson in Lesson.objects.all() for t in lesson.tag_list()})
    return render(request, 'search.html', {
        'q': q,
        'difficulty': difficulty,
        'tag': tag,
        'all_tags': all_tags,
        'results': results,
    })


@login_required
def profile(request):
    done = LessonProgress.objects.filter(user=request.user, completed_at__isnull=False).select_related('lesson__module')
    done_map = {p.lesson_id: p for p in done}
    modules = Module.objects.annotate(lesson_count=Count('lessons'))
    total = Lesson.objects.count()
    data = []
    for m in modules:
        lessons = list(m.lessons.all())
        done_in = sum(1 for l in lessons if l.id in done_map)
        data.append({
            'module': m,
            'total': len(lessons),
            'done': done_in,
            'pct': round(done_in / len(lessons) * 100) if lessons else 0,
        })
    last_done = sorted(done, key=lambda p: p.completed_at, reverse=True)[:5]
    achievements = (
        UserAchievement.objects.filter(user=request.user)
        .select_related('achievement').order_by('achievement__order')
    )
    all_achievements = Achievement.objects.all()
    achieved_ids = {ua.achievement_id for ua in achievements}
    return render(request, 'profile.html', {
        'data': data,
        'total_lessons': total,
        'completed': len(done),
        'pct_total': round(len(done) / total * 100) if total else 0,
        'last_done': last_done,
        'streak': _streak(request.user),
        'achievements': achievements,
        'achieved_ids': achieved_ids,
        'all_achievements': all_achievements,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт создан! Теперь войдите.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
